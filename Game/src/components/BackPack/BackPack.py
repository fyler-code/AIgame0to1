import pygame
from src.components.Chess.ChessPiece import ChessPiece
from src.components.Item.Item import Item

class BackPack:
    """背包类，用于存储玩家收集到的备用棋子和物品"""
    
    def __init__(self, screen, player_chessboard=None):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 计算缩放比例（基于参考分辨率1920*1200）
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1200)
        
        # 背包大小和格子设置
        self.rows = 3
        self.cols = 6
        
        # 如果提供了玩家棋盘，使用与其一致的格子大小
        if player_chessboard:
            self.grid_size = player_chessboard.grid_size
        else:
            self.base_grid_size = 80  # 基础格子大小，会根据屏幕缩放
            self.grid_size = int(self.base_grid_size * self.scale_factor)
            
        self.width = self.cols * self.grid_size
        self.height = self.rows * self.grid_size
        
        # 背包位置 - 默认位置，将在设置玩家棋盘位置时更新
        self.position = (
            self.screen_width - self.width - int(50 * self.scale_factor),
            (self.screen_height - self.height) // 2
        )
        
        # 如果提供了玩家棋盘，设置相对于它的位置
        if player_chessboard:
            self.update_position_relative_to_chessboard(player_chessboard)
        
        # 颜色定义
        self.GRAY = (200, 200, 200)  # 背包背景色
        self.BLACK = (0, 0, 0)  # 网格线颜色
        self.HIGHLIGHT = (255, 255, 200)  # 高亮颜色
        
        # 初始化背包状态 (6x3网格，初始为空)
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 拖拽相关状态
        self.dragging = False
        self.dragged_piece = None
        self.original_position = None
        self.drag_origin = "backpack"  # 标记拖拽来源，可以是"backpack"或"chessboard"
        
        # 初始化一些可乐物品
        self.initialize_items()
    
    def initialize_items(self):
        """初始化一些可乐物品"""
        # 创建不同类型的可乐
        coke1 = Item(attack=5, lifepoint=10, ability="恢复5点生命值")
        coke2 = Item(attack=10, lifepoint=20, ability="恢复10点生命值")
        coke3 = Item(attack=15, lifepoint=30, ability="恢复15点生命值")
        
        # 将可乐放入背包
        self.place_piece(coke1, 0, 0)  # 第一行第一列
        self.place_piece(coke2, 0, 1)  # 第一行第二列
        self.place_piece(coke3, 0, 2)  # 第一行第三列
    
    def update_position_relative_to_chessboard(self, chessboard):
        """根据玩家棋盘位置更新背包位置"""
        # 获取棋盘位置和大小
        board_x, board_y = chessboard.position
        board_size = chessboard.size
        
        # 计算背包应该放在的位置：棋盘右侧两个格子的距离
        gap = chessboard.grid_size  # 两个棋子的宽度
        self.position = (
            board_x + board_size + gap,  # 棋盘右边 + 间隔
            board_y  # 与棋盘上边缘对齐
        )
    
    def draw(self):
        """绘制背包"""
        # 绘制背包标题
        font = pygame.font.Font(None, int(36 * self.scale_factor))
        title = font.render("背包", True, self.BLACK)
        title_rect = title.get_rect(center=(self.position[0] + self.width // 2, self.position[1] - int(30 * self.scale_factor)))
        self.screen.blit(title, title_rect)
        
        # 绘制背包背景
        x, y = self.position
        pygame.draw.rect(self.screen, self.GRAY, pygame.Rect(x, y, self.width, self.height))
        pygame.draw.rect(self.screen, self.BLACK, pygame.Rect(x, y, self.width, self.height), max(1, int(2 * self.scale_factor)))
        
        # 绘制网格线
        for i in range(1, self.rows):
            # 水平线
            pygame.draw.line(
                self.screen, 
                self.BLACK, 
                (x, y + i * self.grid_size), 
                (x + self.width, y + i * self.grid_size), 
                max(1, int(1 * self.scale_factor))
            )
        
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
        board_x, board_y = self.position
        
        # 检查点击是否在背包内
        if (board_x <= x <= board_x + self.width and 
            board_y <= y <= board_y + self.height):
            # 计算格子坐标
            row = int((y - board_y) // self.grid_size)
            col = int((x - board_x) // self.grid_size)
            
            # 确保坐标在有效范围内
            if 0 <= row < self.rows and 0 <= col < self.cols:
                return row, col
        return None
    
    def start_drag(self, mouse_pos):
        """开始拖动棋子"""
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
    
    def end_drag(self, mouse_pos, target=None):
        """结束拖动棋子
        
        参数:
            mouse_pos: 鼠标位置
            target: 拖拽的目标，如果为None，则尝试放回背包，否则是目标棋盘
        """
        if not self.dragging:
            return False
            
        if target is None:
            # 尝试放回背包
            new_pos = self.get_grid_position(mouse_pos)
            if new_pos:
                new_row, new_col = new_pos
                if self.grid[new_row][new_col] is None:
                    # 移动到背包新位置
                    self.grid[new_row][new_col] = self.dragged_piece
                    self.dragged_piece.set_position(new_row, new_col)
                else:
                    # 如果目标位置有棋子，恢复原位
                    if self.original_position:
                        orig_row, orig_col = self.original_position
                        self.grid[orig_row][orig_col] = self.dragged_piece
                        self.dragged_piece.set_position(orig_row, orig_col)
            else:
                # 如果拖到背包外，恢复原位
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
    
    def add_piece(self, piece):
        """添加棋子到背包中的第一个空位置
        
        参数:
            piece: 要添加的棋子
            
        返回:
            bool: 添加成功返回True，否则返回False
        """
        # 查找第一个空位置
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] is None:
                    self.grid[row][col] = piece
                    piece.set_position(row, col)
                    return True
        return False  # 背包已满
    
    def place_piece(self, piece, row, col):
        """放置棋子或物品到指定位置
        
        参数:
            piece: 要放置的棋子或物品
            row: 行索引
            col: 列索引
            
        返回:
            bool: 放置成功返回True，否则返回False
        """
        if 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] is None:
            self.grid[row][col] = piece
            piece.set_position(row, col)
            return True
        return False
    
    def remove_piece(self, row, col):
        """移除指定位置的棋子
        
        参数:
            row: 行索引
            col: 列索引
            
        返回:
            piece: 移除的棋子，如果位置为空则返回None
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            piece = self.grid[row][col]
            self.grid[row][col] = None
            return piece
        return None
    
    def is_full(self):
        """检查背包是否已满"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] is None:
                    return False
        return True
    
    def count_pieces(self):
        """统计背包中的棋子数量"""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] is not None:
                    count += 1
        return count 