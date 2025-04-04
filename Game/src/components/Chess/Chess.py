import pygame
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

class Chess:
    """
    棋子基类，提供基本属性和方法
    """
    def __init__(self, attack=0, lifepoint=0, job="", is_fusion=False, image_path=None):
        """
        初始化棋子
        
        参数:
            attack (int): 攻击力
            lifepoint (int): 生命值
            job (str): 棋子职业/类型
            is_fusion (bool): 是否为融合棋子
            image_path (str): 棋子图片路径，如果为None则使用默认图片
        """
        self.attack = attack
        self.lifepoint = lifepoint
        self.job = job
        self.isFusion = is_fusion
        self.isAttack = 0  # 新增属性，标记棋子是否已经攻击过
        
        # 图片相关属性
        self.image = None
        self.default_image_path = os.path.join(project_root, "assets", "images", "MainChar.jpg")
        
        # 加载图片
        self.load_image(image_path)
        
    def load_image(self, custom_path=None):
        """
        加载棋子图片
        
        参数:
            custom_path (str): 自定义图片路径，如果为None则使用默认图片
        """
        path = custom_path if custom_path else self.default_image_path
        
        try:
            # 加载图片
            self.image = pygame.image.load(path)
            
            # 将图片缩放为适合棋盘格子的大小 (80x80像素)
            self.image = pygame.transform.scale(self.image, (80, 80))
            return True
        except (pygame.error, FileNotFoundError) as e:
            print(f"无法加载棋子图片 {path}: {e}")
            self.image = None
            return False
    
    def set_image(self, image_path):
        """设置新的棋子图片"""
        return self.load_image(image_path)
    
    def get_image(self):
        """获取棋子图片"""
        return self.image
    
    def get_attack(self):
        """获取攻击力"""
        return self.attack
        
    def get_lifepoint(self):
        """获取生命值"""
        return self.lifepoint
        
    def get_job(self):
        """获取职业"""
        return self.job
        
    def is_fusion(self):
        """检查是否为融合棋子"""
        return self.isFusion
        
    def set_attack(self, attack):
        """设置攻击力"""
        self.attack = attack
        
    def set_lifepoint(self, lifepoint):
        """设置生命值"""
        self.lifepoint = lifepoint
        
    def set_job(self, job):
        """设置职业"""
        self.job = job
        
    def set_fusion(self, is_fusion):
        """设置是否为融合棋子"""
        self.isFusion = is_fusion
        
    def take_damage(self, damage):
        """
        受到伤害
        
        参数:
            damage (int): 伤害值
            
        返回:
            bool: 如果棋子死亡返回True，否则返回False
        """
        self.lifepoint -= damage
        return self.lifepoint <= 0
        
    def __str__(self):
        """返回棋子的字符串表示"""
        fusion_status = "融合棋子" if self.isFusion else "普通棋子"
        return f"{self.job} - 攻击力:{self.attack} 生命值:{self.lifepoint} ({fusion_status})"

    def reset_attack_status(self):
        """重置攻击状态"""
        self.isAttack = 0

    def mark_as_attacked(self):
        """标记为已攻击"""
        self.isAttack = 1

    def can_attack(self):
        """检查是否可以攻击"""
        return self.isAttack == 0 