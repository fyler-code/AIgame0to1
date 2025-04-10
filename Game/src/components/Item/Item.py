import pygame
import os

class Item:
    def __init__(self, attack=0, lifepoint=0, ability="", image_path=None):
        self.attack = attack
        self.lifepoint = lifepoint
        self.ability = ability
        self.image = None
        self.position = (0, 0)  # 在背包中的位置
        self.size = None  # 物品大小，将在set_Pic中设置
        
        # 设置默认图片路径
        if image_path is None:
            # 获取项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            image_path = os.path.join(project_root, "assets", "images", "coke.png")
        
        self.set_Pic(image_path)
    
    def set_Pic(self, image_path):
        """设置物品图片"""
        try:
            self.image = pygame.image.load(image_path)
            # 获取图片原始大小
            self.size = self.image.get_size()
        except:
            # 如果图片加载失败，创建一个默认的红色矩形
            self.size = (80, 80)  # 默认大小
            self.image = pygame.Surface(self.size)
            self.image.fill((255, 0, 0))  # 红色
    
    def set_position(self, row, col):
        """设置物品在背包中的位置"""
        self.position = (row, col)
    
    def draw(self, screen, position, grid_size):
        """绘制物品"""
        if self.image:
            # 计算物品在背包中的实际位置
            x = position[0] + self.position[1] * grid_size
            y = position[1] + self.position[0] * grid_size
            
            # 计算缩放比例
            scale = grid_size / max(self.size)
            new_size = (int(self.size[0] * scale), int(self.size[1] * scale))
            
            # 缩放图片
            scaled_image = pygame.transform.scale(self.image, new_size)
            
            # 计算居中位置
            x += (grid_size - new_size[0]) // 2
            y += (grid_size - new_size[1]) // 2
            
            # 绘制图片
            screen.blit(scaled_image, (x, y))
            
            # 计算屏幕大小和缩放比例
            screen_width, screen_height = screen.get_size()
            scale_factor = min(screen_width / 1920, screen_height / 1200)
            
            # 计算物品中心位置（用于显示属性）
            center_x = x + new_size[0] // 2
            center_y = y + new_size[1]
            
            # 绘制物品属性（攻击力和生命值）
            font = pygame.font.Font(None, int(20 * scale_factor))
            attack_text = font.render(str(self.attack), True, (255, 0, 0))
            lifepoint_text = font.render(str(self.lifepoint), True, (0, 255, 0))
            
            # 创建黑色背景使文字更清晰
            text_bg_width = int(50 * scale_factor)
            text_bg_height = int(20 * scale_factor)
            text_bg = pygame.Surface((text_bg_width, text_bg_height))
            text_bg.set_alpha(150)  # 半透明
            text_bg.fill((0, 0, 0))
            
            # 计算背景位置（物品底部）
            bg_x = center_x - text_bg_width // 2
            bg_y = center_y - text_bg_height // 2
            
            # 绘制背景和文字
            screen.blit(text_bg, (bg_x, bg_y))
            screen.blit(attack_text, (bg_x + int(10 * scale_factor), bg_y + int(2 * scale_factor)))
            screen.blit(lifepoint_text, (bg_x + int(30 * scale_factor), bg_y + int(2 * scale_factor)))
    
    def apply_to_piece(self, piece):
        """将物品效果应用到棋子上"""
        if piece:
            # 更新棋子的属性
            piece.attack += self.attack
            piece.lifepoint += self.lifepoint
            if self.ability:
                if piece.ability:
                    piece.ability += f", {self.ability}"
                else:
                    piece.ability = self.ability
            return True
        return False 