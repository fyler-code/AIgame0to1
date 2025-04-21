import pygame
import math

class BulletAnimation:
    """子弹动画类，处理攻击时的子弹飞行效果"""
    
    def __init__(self, start_pos, target_pos, color=(255, 0, 0), size=50, speed=10):
        """
        初始化子弹动画
        
        参数:
            start_pos (tuple): 子弹起始位置 (x, y)
            target_pos (tuple): 子弹目标位置 (x, y)
            color (tuple): 子弹颜色，默认为红色
            size (int): 子弹大小，默认为10
            speed (int): 子弹飞行速度，默认为10
        """
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.current_pos = list(start_pos)
        self.color = color
        self.size = size
        self.speed = speed
        self.completed = False
        
        # 计算方向和距离
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        self.distance = math.sqrt(dx * dx + dy * dy)
        
        # 计算每一步的移动量
        if self.distance > 0:
            self.step_x = (dx / self.distance) * self.speed
            self.step_y = (dy / self.distance) * self.speed
        else:
            self.step_x = 0
            self.step_y = 0
            self.completed = True
        
        # 拖尾效果
        self.trail = []
        self.trail_length = 5
    
    def update(self):
        """更新子弹位置，返回是否完成动画"""
        if self.completed:
            return True
        
        # 保存当前位置到拖尾列表
        self.trail.append(tuple(self.current_pos))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)
        
        # 更新位置
        self.current_pos[0] += self.step_x
        self.current_pos[1] += self.step_y
        
        # 检查是否到达目标
        current_distance = math.sqrt((self.current_pos[0] - self.start_pos[0]) ** 2 + 
                                    (self.current_pos[1] - self.start_pos[1]) ** 2)
        
        if current_distance >= self.distance:
            self.current_pos = list(self.target_pos)
            self.completed = True
            
        return self.completed
    
    def draw(self, screen):
        """在屏幕上绘制子弹"""
        # 绘制拖尾效果
        for i, pos in enumerate(self.trail):
            # 拖尾透明度逐渐降低
            alpha = int(255 * (i + 1) / len(self.trail))
            s = int(self.size * (i + 1) / len(self.trail))
            
            # 创建带透明度的表面
            surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (s, s), s)
            screen.blit(surf, (pos[0] - s, pos[1] - s))
        
        # 绘制子弹
        pygame.draw.circle(screen, self.color, 
                          (int(self.current_pos[0]), int(self.current_pos[1])), 
                          self.size)
    
    def is_completed(self):
        """返回动画是否完成"""
        return self.completed 