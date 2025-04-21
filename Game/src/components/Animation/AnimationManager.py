import pygame
from src.components.Animation.BulletAnimation import BulletAnimation

class AnimationManager:
    """动画管理器类，用于管理多个动画实例"""
    
    def __init__(self):
        """初始化动画管理器"""
        self.animations = []
    
    def add_bullet_animation(self, start_pos, target_pos, color=(255, 0, 0), size=10, speed=10):
        """
        添加一个新的子弹动画
        
        参数:
            start_pos (tuple): 子弹起始位置 (x, y)
            target_pos (tuple): 子弹目标位置 (x, y)
            color (tuple): 子弹颜色
            size (int): 子弹大小
            speed (int): 子弹飞行速度
        
        返回:
            BulletAnimation: 创建的子弹动画实例
        """
        bullet = BulletAnimation(start_pos, target_pos, color, size, speed)
        self.animations.append(bullet)
        return bullet
    
    def update(self):
        """
        更新所有动画，移除已完成的动画
        
        返回:
            bool: 是否所有动画都已完成
        """
        # 使用列表推导式过滤掉已完成的动画
        active_animations = []
        
        for anim in self.animations:
            anim.update()
            if not anim.is_completed():
                active_animations.append(anim)
        
        # 更新动画列表
        self.animations = active_animations
        
        # 返回是否还有活跃的动画
        return len(self.animations) == 0
    
    def draw(self, screen):
        """
        绘制所有活跃的动画
        
        参数:
            screen: pygame屏幕对象
        """
        for anim in self.animations:
            anim.draw(screen)
    
    def clear(self):
        """清除所有动画"""
        self.animations.clear()
    
    def has_active_animations(self):
        """
        检查是否有活跃的动画
        
        返回:
            bool: 是否有活跃的动画
        """
        return len(self.animations) > 0 