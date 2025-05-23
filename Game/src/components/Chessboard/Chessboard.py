import pygame
from src.components.Chess.ChessPiece import ChessPiece

class Chessboard:
    def __init__(self, screen):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 计算缩放比例（基于参考分辨率1920*1200）
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1200)
        
        # 棋盘大小
        self.base_size = 300  # 基础棋盘大小（在1920*1200分辨率下）
        self.size = int(self.base_size * self.scale_factor)  # 根据屏幕大小缩放
        self.grid_size = self.size // 3  # 每个格子的大小
        
        # 计算棋盘位置 - 屏幕左边
        self.position = (
            50,  # 距离左边缘50像素
            (self.screen_height - self.size) // 2 + 200  # 垂直居中往下200像素（保持垂直位置不变）
        )
        
        # 颜色定义
        self.GRAY = (169, 169, 169)  # 棋盘背景色
        self.BLACK = (0, 0, 0)  # 网格线颜色
        
        # 初始化棋盘状态 (3x3网格，初始为空)
        self.grid = [[None for _ in range(3)] for _ in range(3)]
        
        # 新增属性用于拖动功能
        self.dragging = False
        self.dragged_piece = None
        self.original_position = None
        
        # 右键菜单相关
        self.show_menu = False
        self.menu_position = (0, 0)
        self.menu_options = ["Attck", "Cancel"]
        self.menu_selected = None
        self.menu_target = None
        self.menu_font = pygame.font.Font(None, int(24 * self.scale_factor))  # 菜单字体也缩放

    def draw(self):
        # 绘制棋盘背景
        x, y = self.position
        pygame.draw.rect(self.screen, self.GRAY, pygame.Rect(x, y, self.size, self.size))
        
        # 绘制3x3网格线
        for i in range(1, 3):
            # 垂直线
            pygame.draw.line(
                self.screen, 
                self.BLACK, 
                (x + i * self.grid_size, y), 
                (x + i * self.grid_size, y + self.size), 
                max(1, int(2 * self.scale_factor))  # 线宽也缩放，但最小为1
            )
            # 水平线
            pygame.draw.line(
                self.screen, 
                self.BLACK, 
                (x, y + i * self.grid_size), 
                (x + self.size, y + i * self.grid_size), 
                max(1, int(2 * self.scale_factor))  # 线宽也缩放，但最小为1
            )
            
        # 绘制棋子
        for row in range(3):
            for col in range(3):
                piece = self.grid[row][col]
                if piece and isinstance(piece, ChessPiece):
                    piece.draw(self.screen, self.position, self.grid_size)
        
        # 绘制拖动中的棋子
        if self.dragging and self.dragged_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            img_x = mouse_x - self.dragged_piece.image.get_width() // 2
            img_y = mouse_y - self.dragged_piece.image.get_height() // 2
            self.screen.blit(self.dragged_piece.image, (img_x, img_y))
            
        # 绘制右键菜单
        if self.show_menu:
            self.draw_menu()

    def draw_menu(self):
        """绘制右键菜单"""
        menu_width = int(100 * self.scale_factor)
        menu_height = int(len(self.menu_options) * 30 * self.scale_factor)
        menu_x, menu_y = self.menu_position
        
        # 绘制菜单背景
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, (220, 220, 220), menu_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), menu_rect, max(1, int(2 * self.scale_factor)))
        
        # 绘制菜单选项
        for i, option in enumerate(self.menu_options):
            option_y = menu_y + int(i * 30 * self.scale_factor)
            option_rect = pygame.Rect(menu_x, option_y, menu_width, int(30 * self.scale_factor))
            
            # 检查鼠标是否悬停在选项上
            mouse_pos = pygame.mouse.get_pos()
            if option_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (200, 200, 255), option_rect)
                self.menu_selected = i
            
            # 绘制选项文本
            text = self.menu_font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(menu_x + menu_width // 2, option_y + int(15 * self.scale_factor)))
            self.screen.blit(text, text_rect)

    def show_context_menu(self, pos, row, col):
        """显示右键菜单"""
        if self.grid[row][col] is not None:
            self.show_menu = True
            self.menu_position = pos
            self.menu_target = (row, col)
        else:
            self.show_menu = False
            self.menu_target = None

    def handle_menu_click(self, pos):
        """处理菜单点击事件"""
        if not self.show_menu:
            return False
            
        menu_width = int(100 * self.scale_factor)
        menu_height = int(len(self.menu_options) * 30 * self.scale_factor)
        menu_x, menu_y = self.menu_position
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        
        if not menu_rect.collidepoint(pos):
            self.show_menu = False
            return False
            
        # 计算点击了哪个选项
        option_index = int((pos[1] - menu_y) / (30 * self.scale_factor))
        if 0 <= option_index < len(self.menu_options):
            if option_index == 0:  # 攻击选项
                return True
            else:  # 取消选项
                self.show_menu = False
                
        return False
    
    def place_piece(self, piece, row, col):
        """在指定位置放置棋子"""
        if 0 <= row < 3 and 0 <= col < 3 and self.grid[row][col] is None:
            self.grid[row][col] = piece
            
            # 更新棋子的位置
            if isinstance(piece, ChessPiece):
                piece.set_position(row, col)
                
            return True
        return False
    
    def remove_piece(self, row, col):
        """移除指定位置的棋子"""
        if 0 <= row < 3 and 0 <= col < 3:
            piece = self.grid[row][col]
            self.grid[row][col] = None
            return piece
        return None
    
    def get_grid_position(self, mouse_pos):
        """根据鼠标位置返回对应的网格坐标"""
        x, y = mouse_pos
        board_x, board_y = self.position
        
        # 检查点击是否在棋盘内
        if (board_x <= x <= board_x + self.size and 
            board_y <= y <= board_y + self.size):
            # 计算格子坐标
            row = int((y - board_y) // self.grid_size)
            col = int((x - board_x) // self.grid_size)
            return row, col
        return None 

    def setChess(self, chess, position):
        """
        根据位置序号设置棋子
        
        参数:
            chess: 要放置的棋子对象
            position: 位置序号 (1-9)，其中:
                1 2 3
                4 5 6
                7 8 9
        
        返回:
            bool: 放置成功返回True，否则返回False
        """
        # 检查position是否在1-9之间
        if not (1 <= position <= 9):
            return False
            
        # 将位置序号转换为网格坐标
        position -= 1  # 转为0-8
        row = position // 3
        col = position % 3
        
        # 调用place_piece方法放置棋子
        return self.place_piece(chess, row, col) 

    def start_drag(self, mouse_pos):
        """开始拖动棋子"""
        if self.show_menu:
            return  # 如果菜单正在显示，不执行拖动
            
        pos = self.get_grid_position(mouse_pos)
        if pos:
            row, col = pos
            piece = self.grid[row][col]
            if piece:
                self.dragging = True
                self.dragged_piece = piece
                self.original_position = (row, col)
                self.grid[row][col] = None

    def end_drag(self, mouse_pos):
        """结束拖动棋子"""
        if self.dragging:
            new_pos = self.get_grid_position(mouse_pos)
            if new_pos:
                new_row, new_col = new_pos
                if self.grid[new_row][new_col]:
                    # 如果目标位置有棋子，交换位置
                    old_piece = self.grid[new_row][new_col]
                    old_piece.set_position(*self.original_position)
                    self.grid[self.original_position[0]][self.original_position[1]] = old_piece
                self.dragged_piece.set_position(new_row, new_col)
                self.grid[new_row][new_col] = self.dragged_piece
            else:
                # 如果拖动到棋盘外，放回原位
                self.dragged_piece.set_position(*self.original_position)
                self.grid[self.original_position[0]][self.original_position[1]] = self.dragged_piece

            self.dragging = False
            self.dragged_piece = None
            self.original_position = None

    def attack_opponent(self, opponent_board, row, col, is_player=True):
        """攻击对手棋盘上同一列的第一个棋子，方向根据攻击方决定"""
        attacker = self.grid[row][col]
        if not attacker or not isinstance(attacker, ChessPiece):
            return False, "没有棋子可以攻击", None, None

        # 根据攻击方决定检查方向
        if is_player:
            # 玩家棋子从下往上检查
            target_rows = range(2, -1, -1)
        else:
            # 敌方棋子从上往下检查
            target_rows = range(3)

        # 获取攻击者在棋盘上的绝对位置（中心点）
        attacker_pos = self.get_piece_center_position(row, col)
        target_pos = None  # 目标位置，初始为None
        target_piece = None  # 攻击的目标，初始为None

        # 在对手棋盘上寻找同一列的第一个棋子
        for target_row in target_rows:
            target_piece = opponent_board.grid[target_row][col]
            if target_piece and isinstance(target_piece, ChessPiece):
                # 找到目标，获取目标中心位置
                target_pos = opponent_board.get_piece_center_position(target_row, col)
                
                # 构造攻击消息
                attack_message = f"{attacker.get_job()} 攻击了 {target_piece.get_job()}，造成 {attacker.get_attack()} 点伤害"
                print(attack_message)
                
                # 因为伤害应用延迟到动画完成后，这里不再直接扣减生命值
                # 但保留原先的代码逻辑注释，以便理解流程
                # target_piece.take_damage(attacker.get_attack())
                # 检查目标棋子是否死亡
                # if target_piece.get_lifepoint() <= 0:
                #    opponent_board.remove_piece(target_row, col)
                #    death_message = f"{target_piece.get_job()} 被击败"
                #    print(death_message)
                #    attack_message += f"，{death_message}"
                
                return True, attack_message, attacker_pos, target_pos
                
        return False, "没有找到攻击目标", None, None
    
    def get_piece_center_position(self, row, col):
        """获取棋子中心点的屏幕坐标"""
        board_x, board_y = self.position
        grid_size = self.grid_size
        
        # 计算棋子中心位置
        x = board_x + col * grid_size + grid_size // 2
        y = board_y + row * grid_size + grid_size // 2
        
        return (x, y)