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

    def draw(self):
        # 绘制棋盘标题
        font = pygame.font.Font(None, 36)
        title = font.render("战斗棋盘", True, self.BLACK)
        title_rect = title.get_rect(center=(self.position[0] + self.size // 2, self.position[1] - 30))
        self.screen.blit(title, title_rect)
        
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