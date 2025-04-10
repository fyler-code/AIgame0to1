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
    def __init__(self, attack=0, lifepoint=0, job="", is_fusion=False, position=None, color=(255, 0, 0), image_path=None, ability=""):
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
            ability (str): 棋子的能力
        """
        super().__init__(attack, lifepoint, job, is_fusion, image_path)
        self.position = position  # (row, col)
        self.color = color
        self.base_radius = 40  # 基础棋子绘制半径，仅在图片无法加载时使用
        self.ability = ability  # 新增ability属性
        self.attacked = False  # 是否已经攻击过
        
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
        
        # 计算屏幕大小
        screen_width, screen_height = screen.get_size()
        # 计算缩放比例（基于参考分辨率1920*1200）
        scale_factor = min(screen_width / 1920, screen_height / 1200)
        # 计算缩放后的棋子半径
        radius = int(self.base_radius * scale_factor)
            
        row, col = self.position
        board_x, board_y = board_position
        
        # 计算棋子中心位置
        center_x = board_x + col * grid_size + grid_size // 2
        center_y = board_y + row * grid_size + grid_size // 2
        
        # 绘制棋子
        if self.image:
            # 调整图片大小以适应缩放
            scaled_size = int(80 * scale_factor)
            
            # 保持宽高比例缩放
            original_width, original_height = self.image.get_size()
            scaled_height = int(original_height * scaled_size / original_width)
            scaled_image = pygame.transform.scale(self.image, (scaled_size, scaled_height))
            
            # 计算图片左上角位置（使图片居中）
            img_x = center_x - scaled_image.get_width() // 2
            img_y = center_y - scaled_image.get_height() // 2
            
            # 绘制棋子图片
            screen.blit(scaled_image, (img_x, img_y))
        else:
            # 如果图片加载失败，使用圆形代替
            pygame.draw.circle(screen, self.color, (center_x, center_y), radius)
            
        # 如果是融合棋子，添加特殊标记
        if self.isFusion:
            pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y - int(25 * scale_factor)), int(5 * scale_factor))
        
        # 创建半透明黑色背景使属性文字更清晰
        text_bg_width = int(60 * scale_factor)
        text_bg_height = int(24 * scale_factor)
        text_bg = pygame.Surface((text_bg_width, text_bg_height))
        text_bg.set_alpha(150)  # 半透明
        text_bg.fill((0, 0, 0))
        
        # 计算背景位置（棋子底部）
        bg_x = center_x - text_bg_width // 2
        bg_y = center_y + (grid_size // 2) - text_bg_height - int(10 * scale_factor)
        
        # 绘制背景
        screen.blit(text_bg, (bg_x, bg_y))
        
        # 绘制棋子属性（攻击力和生命值）
        font = pygame.font.Font(None, int(24 * scale_factor))
        attack_text = font.render(str(self.attack), True, (255, 0, 0))  # 攻击力红色
        lifepoint_text = font.render(str(self.lifepoint), True, (0, 255, 0))  # 生命值绿色
        
        # 在背景上显示攻击力和生命值
        screen.blit(attack_text, (bg_x + int(10 * scale_factor), bg_y + int(4 * scale_factor)))
        screen.blit(lifepoint_text, (bg_x + int(35 * scale_factor), bg_y + int(4 * scale_factor)))
        
    def set_position(self, row, col):
        """设置棋子在棋盘上的位置"""
        self.position = (row, col)
        
    def get_position(self):
        """获取棋子在棋盘上的位置"""
        return self.position 