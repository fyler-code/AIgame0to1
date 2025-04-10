import pygame

class MessageBox:
    """消息盒子类，用于记录基本的游戏信息以及发生了什么"""
    
    def __init__(self, screen, player_chessboard=None):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 计算缩放比例（基于参考分辨率1920*1200）
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1200)
        
        # 初始化游戏信息
        self.gold = 0
        self.round = 1
        self.round_to_reward = 3  # 每隔3回合获得一次奖励
        
        # 消息盒子大小
        self.width = int(300 * self.scale_factor)
        self.height = int(300 * self.scale_factor)
        
        # 设置消息盒子位置（位于玩家棋盘左边一个棋子的距离）
        if player_chessboard:
            chessboard_x, chessboard_y = player_chessboard.position
            self.position = (
                chessboard_x - self.width - int(player_chessboard.grid_size * self.scale_factor),
                chessboard_y
            )
        else:
            # 如果没有提供棋盘位置，使用默认位置
            self.position = (int(50 * self.scale_factor), int(50 * self.scale_factor))
        
        # 颜色定义
        self.BACKGROUND = (240, 240, 240)  # 背景色
        self.BORDER = (100, 100, 100)  # 边框色
        self.TEXT_COLOR = (0, 0, 0)  # 文本颜色
        self.GOLD_COLOR = (255, 215, 0)  # 金币颜色
        
        # 消息列表，用于显示游戏中发生的事件
        self.messages = []
        self.max_messages = 8  # 最多显示的消息数量
    
    def draw(self):
        """绘制消息盒子"""
        x, y = self.position
        
        # 绘制背景
        pygame.draw.rect(self.screen, self.BACKGROUND, (x, y, self.width, self.height))
        # 绘制边框
        pygame.draw.rect(self.screen, self.BORDER, (x, y, self.width, self.height), 2)
        
        # 创建字体
        title_font = pygame.font.Font(None, int(30 * self.scale_factor))
        info_font = pygame.font.Font(None, int(24 * self.scale_factor))
        message_font = pygame.font.Font(None, int(20 * self.scale_factor))
        
        # 绘制标题
        title = title_font.render("Game Info", True, self.TEXT_COLOR)
        title_rect = title.get_rect(center=(x + self.width // 2, y + int(20 * self.scale_factor)))
        self.screen.blit(title, title_rect)
        
        # 绘制游戏基本信息
        gold_text = info_font.render(f"Gold: {self.gold}", True, self.GOLD_COLOR)
        round_text = info_font.render(f"Round: {self.round}", True, self.TEXT_COLOR)
        reward_text = info_font.render(f"Rounds to Reward: {self.round_to_reward - (self.round % self.round_to_reward)}", True, self.TEXT_COLOR)
        
        self.screen.blit(gold_text, (x + int(20 * self.scale_factor), y + int(50 * self.scale_factor)))
        self.screen.blit(round_text, (x + int(20 * self.scale_factor), y + int(80 * self.scale_factor)))
        self.screen.blit(reward_text, (x + int(20 * self.scale_factor), y + int(110 * self.scale_factor)))
        
        # 绘制消息分隔线
        pygame.draw.line(
            self.screen, 
            self.BORDER, 
            (x + int(10 * self.scale_factor), y + int(140 * self.scale_factor)), 
            (x + self.width - int(10 * self.scale_factor), y + int(140 * self.scale_factor)), 
            1
        )
        
        # 绘制消息标题
        message_title = info_font.render("Messages:", True, self.TEXT_COLOR)
        self.screen.blit(message_title, (x + int(20 * self.scale_factor), y + int(150 * self.scale_factor)))
        
        # 绘制消息列表
        message_y = y + int(180 * self.scale_factor)
        for message in self.messages[-self.max_messages:]:  # 只显示最后max_messages条消息
            message_text = message_font.render(message, True, self.TEXT_COLOR)
            self.screen.blit(message_text, (x + int(20 * self.scale_factor), message_y))
            message_y += int(15 * self.scale_factor)
    
    def add_message(self, message):
        """添加一条游戏消息"""
        self.messages.append(message)
        # 如果消息数量超过限制，移除最早的消息
        if len(self.messages) > self.max_messages * 2:  # 保留两倍的限制，避免频繁删除
            self.messages = self.messages[-self.max_messages:]
    
    def add_gold(self, amount):
        """增加金币"""
        self.gold += amount
        self.add_message(f"Gained {amount} gold")
    
    def spend_gold(self, amount):
        """花费金币"""
        if self.gold >= amount:
            self.gold -= amount
            self.add_message(f"Spent {amount} gold")
            return True
        else:
            self.add_message("Not enough gold!")
            return False
    
    def next_round(self):
        """进入下一回合"""
        self.round += 1
        self.add_message(f"Round {self.round} started")
        
        # 检查是否到达奖励回合
        if self.round % self.round_to_reward == 0:
            self.add_message("Reward round reached!")
            return True  # 返回True表示应该给予奖励
        return False
    
    def update_position(self, player_chessboard):
        """根据棋盘位置更新消息盒子位置"""
        if player_chessboard:
            chessboard_x, chessboard_y = player_chessboard.position
            self.position = (
                chessboard_x - self.width - int(player_chessboard.grid_size * self.scale_factor),
                chessboard_y
            ) 