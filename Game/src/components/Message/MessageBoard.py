import pygame

class MessageBoard:
    """消息板类，显示游戏信息如金币数量、当前回合数和消息文本"""
    
    def __init__(self, screen, player_chessboard=None):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 计算缩放比例（基于参考分辨率1920*1200）
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1200)
        
        # 游戏状态信息
        self.coins = 100  # 初始金币数量
        self.current_turn = 1  # 当前回合数
        self.message = "游戏开始！"  # 初始消息
        self.message_history = []  # 消息历史记录
        self.max_history = 5  # 最多显示5条历史消息
        
        # 如果提供了玩家棋盘，使用与其一致的大小
        if player_chessboard:
            self.width = player_chessboard.size
            self.height = player_chessboard.size
        else:
            self.base_size = 300  # 基础大小，会根据屏幕缩放
            self.width = int(self.base_size * self.scale_factor)
            self.height = int(self.base_size * self.scale_factor)
            
        # 消息板位置 - 默认位置，将在设置玩家棋盘位置时更新
        self.position = (
            int(50 * self.scale_factor),
            (self.screen_height - self.height) // 2
        )
        
        # 如果提供了玩家棋盘，设置相对于它的位置
        if player_chessboard:
            self.update_position_relative_to_chessboard(player_chessboard)
        
        # 颜色定义
        self.BACKGROUND = (230, 230, 250)  # 消息板背景色，浅紫色
        self.BLACK = (0, 0, 0)  # 文本颜色
        self.GOLD = (255, 215, 0)  # 金币颜色
        self.TURN_COLOR = (70, 130, 180)  # 回合数颜色，钢蓝色
        self.SEPARATOR_COLOR = (200, 200, 200)  # 分隔线颜色
        
        # 字体设置
        self.title_font = pygame.font.Font(None, int(36 * self.scale_factor))
        self.info_font = pygame.font.Font(None, int(30 * self.scale_factor))
        self.message_font = pygame.font.Font(None, int(24 * self.scale_factor))
    
    def update_position_relative_to_chessboard(self, chessboard):
        """根据玩家棋盘位置更新消息板位置"""
        # 获取棋盘位置
        board_x, board_y = chessboard.position
        
        # 计算消息板应该放在的位置：棋盘左侧一个格子的距离
        gap = chessboard.grid_size  # 一个棋子的宽度
        self.position = (
            board_x - self.width - gap,  # 棋盘左边 - 消息板宽度 - 间隔
            board_y  # 与棋盘上边缘对齐
        )
    
    def add_message(self, message):
        """添加新消息"""
        self.message = message
        self.message_history.insert(0, message)
        if len(self.message_history) > self.max_history:
            self.message_history.pop()
    
    def update_coins(self, amount):
        """更新金币数量"""
        self.coins += amount
        if self.coins < 0:
            self.coins = 0
        return self.coins
    
    def next_turn(self):
        """进入下一回合"""
        self.current_turn += 1
        self.add_message(f"回合 {self.current_turn} 开始")
        return self.current_turn
    
    def draw(self):
        """绘制消息板"""
        # 绘制消息板标题
        title = self.title_font.render("消息面板", True, self.BLACK)
        title_rect = title.get_rect(center=(self.position[0] + self.width // 2, self.position[1] - int(30 * self.scale_factor)))
        self.screen.blit(title, title_rect)
        
        # 绘制消息板背景
        x, y = self.position
        pygame.draw.rect(self.screen, self.BACKGROUND, pygame.Rect(x, y, self.width, self.height))
        pygame.draw.rect(self.screen, self.BLACK, pygame.Rect(x, y, self.width, self.height), max(1, int(2 * self.scale_factor)))
        
        # 绘制金币和回合信息区域
        info_area_height = int(80 * self.scale_factor)
        pygame.draw.rect(self.screen, (240, 240, 255), pygame.Rect(x, y, self.width, info_area_height))
        
        # 绘制分隔线
        pygame.draw.line(
            self.screen,
            self.SEPARATOR_COLOR,
            (x, y + info_area_height),
            (x + self.width, y + info_area_height),
            max(1, int(2 * self.scale_factor))
        )
        
        # 绘制金币信息
        coins_text = self.info_font.render(f"金币: {self.coins}", True, self.GOLD)
        coins_rect = coins_text.get_rect()
        coins_rect.left = x + int(20 * self.scale_factor)
        coins_rect.top = y + int(20 * self.scale_factor)
        self.screen.blit(coins_text, coins_rect)
        
        # 绘制回合信息
        turn_text = self.info_font.render(f"回合: {self.current_turn}", True, self.TURN_COLOR)
        turn_rect = turn_text.get_rect()
        turn_rect.right = x + self.width - int(20 * self.scale_factor)
        turn_rect.top = y + int(20 * self.scale_factor)
        self.screen.blit(turn_text, turn_rect)
        
        # 绘制当前消息
        y_pos = y + info_area_height + int(20 * self.scale_factor)
        current_msg = self.message_font.render(self.message, True, self.BLACK)
        current_msg_rect = current_msg.get_rect()
        current_msg_rect.left = x + int(20 * self.scale_factor)
        current_msg_rect.top = y_pos
        self.screen.blit(current_msg, current_msg_rect)
        
        # 绘制消息历史
        for i, msg in enumerate(self.message_history):
            y_pos += int(30 * self.scale_factor)
            hist_msg = self.message_font.render(msg, True, (100, 100, 100))
            hist_msg_rect = hist_msg.get_rect()
            hist_msg_rect.left = x + int(20 * self.scale_factor)
            hist_msg_rect.top = y_pos
            self.screen.blit(hist_msg, hist_msg_rect) 