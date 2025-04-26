import pygame
import os

class MessageBoard:
    """消息板类，用于显示游戏信息：金币数量、当前回合和游戏消息"""
    
    def __init__(self, screen, player_chessboard=None):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 计算缩放比例（基于参考分辨率1920*1200）
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1200)
        
        # 初始化游戏信息
        self.coins = 0
        self.current_turn = 1
        self.message = "准备开始游戏！"
        
        # 消息历史记录
        self.message_history = []
        self.max_messages = 5  # 最多显示5条历史消息
        
        # 消息板大小
        self.width = int(300 * self.scale_factor)
        self.height = int(400 * self.scale_factor)
        
        # 设置消息板位置（位于玩家棋盘左边一个棋子的距离）
        if player_chessboard:
            self.update_position_relative_to_chessboard(player_chessboard)
        else:
            # 如果没有提供棋盘位置，使用默认位置
            self.position = (int(50 * self.scale_factor), int(50 * self.scale_factor))
        
        # 颜色定义
        self.BACKGROUND = (230, 220, 240)  # 浅紫色背景
        self.BORDER = (100, 80, 120)  # 深紫色边框
        self.TEXT_COLOR = (40, 40, 40)  # 深灰色文本
        self.COIN_COLOR = (255, 215, 0)  # 金币颜色（金色）
        self.TURN_COLOR = (80, 100, 200)  # 回合数颜色（蓝色）
        self.HIGHLIGHT_COLOR = (120, 20, 120)  # 高亮颜色（紫色）
        
        # 初始化字体
        self.initialize_font()
    
    def initialize_font(self):
        """初始化字体，尝试加载中文字体，如果失败则使用默认字体"""
        try:
            # 尝试使用系统中文字体
            system_fonts = [
                "simhei.ttf",   # 黑体
                "simsun.ttc",    # 宋体
                "msyh.ttc",      # 微软雅黑
                "simkai.ttf"     # 楷体
            ]
            
            font_found = False
            for font_name in system_fonts:
                # 尝试使用系统字体路径
                system_font_path = os.path.join("C:\\Windows\\Fonts", font_name)
                if os.path.exists(system_font_path):
                    self.title_font = pygame.font.Font(system_font_path, int(32 * self.scale_factor))
                    self.info_font = pygame.font.Font(system_font_path, int(28 * self.scale_factor))
                    self.message_font = pygame.font.Font(system_font_path, int(24 * self.scale_factor))
                    self.history_font = pygame.font.Font(system_font_path, int(20 * self.scale_factor))
                    font_found = True
                    # 记录使用的字体名称
                    self.font_name = font_name
                    break
            
            # 如果没有找到中文字体，使用默认字体
            if not font_found:
                self.title_font = pygame.font.Font(None, int(32 * self.scale_factor))
                self.info_font = pygame.font.Font(None, int(28 * self.scale_factor))
                self.message_font = pygame.font.Font(None, int(24 * self.scale_factor))
                self.history_font = pygame.font.Font(None, int(20 * self.scale_factor))
                self.font_name = "默认字体"
                
        except Exception as e:
            print(f"加载字体时出错: {e}")
            # 使用默认字体
            self.title_font = pygame.font.Font(None, int(32 * self.scale_factor))
            self.info_font = pygame.font.Font(None, int(28 * self.scale_factor))
            self.message_font = pygame.font.Font(None, int(24 * self.scale_factor))
            self.history_font = pygame.font.Font(None, int(20 * self.scale_factor))
            self.font_name = "默认字体"
    
    def update_position_relative_to_chessboard(self, chessboard):
        """根据棋盘位置更新消息板位置"""
        chessboard_x, chessboard_y = chessboard.position
        # 放置在棋盘左侧一个格子的距离
        self.position = (
            chessboard_x - self.width - chessboard.grid_size,
            chessboard_y-20  # 与棋盘顶部对齐
        )
    
    def add_message(self, message):
        """添加新消息并更新当前消息"""
        # 将当前消息移至历史记录
        if self.message:
            self.message_history.insert(0, self.message)
        
        # 设置新的当前消息
        self.message = message
        
        # 如果历史消息过多，删除最早的
        if len(self.message_history) > self.max_messages:
            self.message_history = self.message_history[:self.max_messages]
    
    def update_coins(self, amount):
        """更新金币数量"""
        new_value = self.coins + amount
        # 确保金币不会变为负数
        self.coins = max(0, new_value)
        
        # 添加消息
        if amount > 0:
            self.add_message(f"获得了 {amount} 枚金币!")
        else:
            self.add_message(f"使用了 {abs(amount)} 枚金币.")
        
        return self.coins
    
    def next_turn(self):
        """前进到下一回合"""
        self.current_turn += 1
        self.add_message(f"第 {self.current_turn} 回合开始!")
        return self.current_turn
    
    def wrap_text(self, text, font, max_width):
        """将文本分成多行，确保每行不超过指定的最大宽度"""
        lines = []
        # 对于中文，按字符拆分更合适
        words = list(text)
        current_line = ""
        
        for word in words:
            test_line = current_line + word
            # 检查这一行加上新字符是否会太长
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        # 添加最后一行
        if current_line:
            lines.append(current_line)
            
        return lines
    
    def draw(self):
        """绘制消息板"""
        x, y = self.position
        
        # 绘制背景
        pygame.draw.rect(self.screen, self.BACKGROUND, (x, y, self.width, self.height))
        # 绘制边框
        pygame.draw.rect(self.screen, self.BORDER, (x, y, self.width, self.height), 3)
        
        # 绘制标题
        title = self.title_font.render("游戏信息", True, self.HIGHLIGHT_COLOR)
        title_rect = title.get_rect(center=(x + self.width // 2, y + int(25 * self.scale_factor)))
        self.screen.blit(title, title_rect)
        
        # 绘制分隔线
        pygame.draw.line(
            self.screen, 
            self.BORDER, 
            (x + int(20 * self.scale_factor), y + int(50 * self.scale_factor)), 
            (x + self.width - int(20 * self.scale_factor), y + int(50 * self.scale_factor)), 
            2
        )
        
        # 绘制金币和回合信息
        coin_text = self.info_font.render(f"金币: {self.coins}", True, self.COIN_COLOR)
        turn_text = self.info_font.render(f"回合: {self.current_turn}", True, self.TURN_COLOR)
        
        self.screen.blit(coin_text, (x + int(30 * self.scale_factor), y + int(70 * self.scale_factor)))
        self.screen.blit(turn_text, (x + int(30 * self.scale_factor), y + int(105 * self.scale_factor)))
        
        # 绘制第二条分隔线
        pygame.draw.line(
            self.screen, 
            self.BORDER, 
            (x + int(20 * self.scale_factor), y + int(140 * self.scale_factor)), 
            (x + self.width - int(20 * self.scale_factor), y + int(140 * self.scale_factor)), 
            2
        )
        
        # 绘制当前消息标题
        current_msg_title = self.info_font.render("当前消息:", True, self.HIGHLIGHT_COLOR)
        self.screen.blit(current_msg_title, (x + int(30 * self.scale_factor), y + int(160 * self.scale_factor)))
        
        # 绘制当前消息
        if self.message:
            max_text_width = self.width - int(60 * self.scale_factor)
            lines = self.wrap_text(self.message, self.message_font, max_text_width)
            
            # 绘制消息的每一行
            msg_y = y + int(195 * self.scale_factor)
            for line in lines:
                message_text = self.message_font.render(line, True, self.TEXT_COLOR)
                self.screen.blit(message_text, (x + int(30 * self.scale_factor), msg_y))
                msg_y += int(25 * self.scale_factor)
        
        # 绘制第三条分隔线
        pygame.draw.line(
            self.screen, 
            self.BORDER, 
            (x + int(20 * self.scale_factor), y + int(250 * self.scale_factor)), 
            (x + self.width - int(20 * self.scale_factor), y + int(250 * self.scale_factor)), 
            2
        )
        
        # 绘制历史消息标题
        history_title = self.info_font.render("历史消息:", True, self.HIGHLIGHT_COLOR)
        self.screen.blit(history_title, (x + int(30 * self.scale_factor), y + int(270 * self.scale_factor)))
        
        # 绘制历史消息
        history_y = y + int(300 * self.scale_factor)
        for i, message in enumerate(self.message_history):
            # 对历史消息进行截断，确保不会太长
            max_text_width = self.width - int(60 * self.scale_factor)
            if self.history_font.size(message)[0] > max_text_width:
                # 计算能显示多少字符
                for j in range(len(message), 0, -1):
                    if self.history_font.size(message[:j] + "...")[0] <= max_text_width:
                        message = message[:j] + "..."
                        break
            
            history_text = self.history_font.render(message, True, self.TEXT_COLOR)
            self.screen.blit(history_text, (x + int(30 * self.scale_factor), history_y))
            history_y += int(20 * self.scale_factor) 