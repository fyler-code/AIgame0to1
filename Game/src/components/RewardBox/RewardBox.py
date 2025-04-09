import pygame
from src.components.Chess.ChessPiece import ChessPiece
from src.components.Item.Item import Item

class RewardBox:
    """奖励盒子类，用于存储游戏奖励的物品和棋子"""
    
    def __init__(self, screen):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 计算缩放比例（基于参考分辨率1920*1200）
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1200)
        
        # 奖励盒子大小和格子设置 - 只有1*3的格子
        self.rows = 1
        self.cols = 3
        
        # 设置格子大小
        self.base_grid_size = 80  # 基础格子大小，会根据屏幕缩放
        self.grid_size = int(self.base_grid_size * self.scale_factor)
            
        self.width = self.cols * self.grid_size
        self.height = self.rows * self.grid_size
        
        # 奖励盒子位置 - 屏幕中央
        self.position = (
            (self.screen_width - self.width) // 2,
            (self.screen_height - self.height) // 2
        )
        
        # 颜色定义
        self.GOLD = (218, 165, 32)  # 奖励盒子背景色（金色）
        self.BLACK = (0, 0, 0)  # 网格线颜色
        self.HIGHLIGHT = (255, 215, 0)  # 高亮颜色（亮金色）
        
        # 初始化奖励盒子状态 (3格，初始为空)
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 拖拽相关状态
        self.dragging = False
        self.dragged_piece = None
        self.original_position = None
    
    def draw(self):
        """绘制奖励盒子"""
        # 绘制奖励盒子标题
        font = pygame.font.Font(None, int(36 * self.scale_factor))
        title = font.render("奖励盒子", True, self.BLACK)
        title_rect = title.get_rect(center=(self.position[0] + self.width // 2, self.position[1] - int(30 * self.scale_factor)))
        self.screen.blit(title, title_rect)
        
        # 绘制奖励盒子背景
        x, y = self.position
        pygame.draw.rect(self.screen, self.GOLD, pygame.Rect(x, y, self.width, self.height))
        pygame.draw.rect(self.screen, self.BLACK, pygame.Rect(x, y, self.width, self.height), max(1, int(2 * self.scale_factor)))
        
        # 绘制网格线
        for j in range(1, self.cols):
            # 垂直线
            pygame.draw.line(
                self.screen, 
                self.BLACK, 
                (x + j * self.grid_size, y), 
                (x + j * self.grid_size, y + self.height), 
                max(1, int(1 * self.scale_factor))
            )
        
        # 绘制格子中的棋子和物品
        for row in range(self.rows):
            for col in range(self.cols):
                piece = self.grid[row][col]
                if piece:
                    if isinstance(piece, ChessPiece):
                        piece.draw(self.screen, self.position, self.grid_size)
                    elif isinstance(piece, Item):
                        piece.draw(self.screen, self.position, self.grid_size)
    
    def get_grid_position(self, mouse_pos):
        """根据鼠标位置返回对应的网格坐标"""
        x, y = mouse_pos
        box_x, box_y = self.position
        
        # 检查点击是否在奖励盒子内
        if (box_x <= x <= box_x + self.width and 
            box_y <= y <= box_y + self.height):
            # 计算格子坐标
            row = int((y - box_y) // self.grid_size)
            col = int((x - box_x) // self.grid_size)
            
            # 确保坐标在有效范围内
            if 0 <= row < self.rows and 0 <= col < self.cols:
                return row, col
        return None
    
    def start_drag(self, mouse_pos):
        """开始拖动棋子或物品"""
        pos = self.get_grid_position(mouse_pos)
        if pos:
            row, col = pos
            piece = self.grid[row][col]
            if piece:
                self.dragging = True
                self.dragged_piece = piece
                self.original_position = (row, col)
                self.grid[row][col] = None
                return True
        return False
    
    def end_drag(self, mouse_pos):
        """结束拖动棋子或物品"""
        if not self.dragging:
            return False
            
        # 尝试放回奖励盒子
        new_pos = self.get_grid_position(mouse_pos)
        if new_pos:
            new_row, new_col = new_pos
            if self.grid[new_row][new_col] is None:
                # 移动到奖励盒子新位置
                self.grid[new_row][new_col] = self.dragged_piece
                self.dragged_piece.set_position(new_row, new_col)
            else:
                # 如果目标位置有物品/棋子，恢复原位
                if self.original_position:
                    orig_row, orig_col = self.original_position
                    self.grid[orig_row][orig_col] = self.dragged_piece
                    self.dragged_piece.set_position(orig_row, orig_col)
        else:
            # 如果拖到奖励盒子外，恢复原位
            if self.original_position:
                orig_row, orig_col = self.original_position
                self.grid[orig_row][orig_col] = self.dragged_piece
                self.dragged_piece.set_position(orig_row, orig_col)
        
        # 重置拖拽状态
        result = self.dragged_piece
        self.dragging = False
        self.dragged_piece = None
        self.original_position = None
        return result
    
    def add_item(self, item):
        """添加物品或棋子到奖励盒子
        
        参数:
            item: 要添加的物品或棋子
            
        返回:
            bool: 添加成功返回True，否则返回False
        """
        # 查找第一个空位置
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] is None:
                    self.grid[row][col] = item
                    item.set_position(row, col)
                    return True
        return False  # 奖励盒子已满
    
    def place_item(self, item, row, col):
        """放置物品或棋子到指定位置
        
        参数:
            item: 要放置的物品或棋子
            row: 行索引
            col: 列索引
            
        返回:
            bool: 放置成功返回True，否则返回False
        """
        if 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] is None:
            self.grid[row][col] = item
            item.set_position(row, col)
            return True
        return False
    
    def remove_item(self, row, col):
        """移除指定位置的物品或棋子
        
        参数:
            row: 行索引
            col: 列索引
            
        返回:
            item: 移除的物品或棋子，如果位置为空则返回None
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            item = self.grid[row][col]
            self.grid[row][col] = None
            return item
        return None
    
    def is_full(self):
        """检查奖励盒子是否已满"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] is None:
                    return False
        return True
    
    def count_items(self):
        """统计奖励盒子中的物品和棋子数量"""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] is not None:
                    count += 1
        return count 