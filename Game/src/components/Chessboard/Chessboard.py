import pygame
from src.components.Chess.ChessPiece import ChessPiece

class Chessboard:
    def __init__(self, screen):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 棋盘大小
        self.size = 300  # 整个棋盘的大小
        self.grid_size = self.size // 3  # 每个格子的大小 (100x100)
        
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
                2
            )
            # 水平线
            pygame.draw.line(
                self.screen, 
                self.BLACK, 
                (x, y + i * self.grid_size), 
                (x + self.size, y + i * self.grid_size), 
                2
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
            row = (y - board_y) // self.grid_size
            col = (x - board_x) // self.grid_size
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
            return

        # 根据攻击方决定检查方向
        if is_player:
            # 玩家棋子从下往上检查
            target_rows = range(2, -1, -1)
        else:
            # 敌方棋子从上往下检查
            target_rows = range(3)

        # 在对手棋盘上寻找同一列的第一个棋子
        for target_row in target_rows:
            target_piece = opponent_board.grid[target_row][col]
            if target_piece and isinstance(target_piece, ChessPiece):
                # 计算伤害
                target_piece.take_damage(attacker.get_attack())
                print(f"{attacker.get_job()} 攻击了 {target_piece.get_job()}，造成 {attacker.get_attack()} 点伤害")
                # 检查目标棋子是否死亡
                if target_piece.get_lifepoint() <= 0:
                    opponent_board.remove_piece(target_row, col)
                    print(f"{target_piece.get_job()} 被击败")
                break