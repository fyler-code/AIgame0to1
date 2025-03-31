import pygame
import os
import sys

# 添加项目根目录到Python路径，解决导入问题
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.components.Chess.Chess import Chess

class ChessPiece(Chess):
    """
    具体的棋子类，继承自Chess基类，添加了绘制和位置功能
    """
    def __init__(self, attack=0, lifepoint=0, job="", is_fusion=False, position=None, color=(255, 0, 0), image_path=None):
        """
        初始化棋子
        
        参数:
            attack (int): 攻击力
            lifepoint (int): 生命值
            job (str): 棋子职业/类型
            is_fusion (bool): 是否为融合棋子
            position (tuple): 棋子在棋盘上的位置(row, col)
            color (tuple): 棋子的颜色(R,G,B)
            image_path (str): 棋子图片路径，如果为None则使用默认图片
        """
        super().__init__(attack, lifepoint, job, is_fusion, image_path)
        self.position = position  # (row, col)
        self.color = color
        self.radius = 40  # 棋子绘制半径，仅在图片无法加载时使用
        
    def draw(self, screen, board_position, grid_size):
        """
        在屏幕上绘制棋子
        
        参数:
            screen: pygame屏幕对象
            board_position: 棋盘左上角位置
            grid_size: 格子大小
        """
        if self.position is None:
            return
            
        row, col = self.position
        board_x, board_y = board_position
        
        # 计算棋子中心位置
        center_x = board_x + col * grid_size + grid_size // 2
        center_y = board_y + row * grid_size + grid_size // 2
        
        # 绘制棋子
        if self.image:
            # 计算图片左上角位置（使图片居中）
            img_x = center_x - self.image.get_width() // 2
            img_y = center_y - self.image.get_height() // 2
            
            # 绘制棋子图片
            screen.blit(self.image, (img_x, img_y))
        else:
            # 如果图片加载失败，使用圆形代替
            pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)
        
        # 绘制棋子属性（攻击力和生命值）
        font = pygame.font.Font(None, 24)
        attack_text = font.render(str(self.attack), True, (255, 255, 255))
        lifepoint_text = font.render(str(self.lifepoint), True, (255, 255, 255))
        
        # 在棋子上显示攻击力和生命值
        screen.blit(attack_text, (center_x - 15, center_y - 10))
        screen.blit(lifepoint_text, (center_x + 5, center_y - 10))
        
        # 如果是融合棋子，添加特殊标记
        if self.isFusion:
            pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y - 25), 5)
            
    def set_position(self, row, col):
        """设置棋子在棋盘上的位置"""
        self.position = (row, col)
        
    def get_position(self):
        """获取棋子在棋盘上的位置"""
        return self.position 