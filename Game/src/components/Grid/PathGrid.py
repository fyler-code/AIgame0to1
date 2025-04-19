import pygame
import os

class PathGrid:
    """玩家走格子的网格类，不同列有不同数量的格子"""
    
    def __init__(self, screen, chessboard=None):
        self.screen = screen
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()
        
        # 计算缩放比例（基于参考分辨率1920*1200）
        self.scale_factor = min(self.screen_width / 1920, self.screen_height / 1200)
        
        # 如果提供了棋盘，使用与棋盘相同的格子大小
        if chessboard:
            self.grid_size = chessboard.grid_size
        else:
            self.base_grid_size = 80  # 基础格子大小，会根据屏幕缩放
            self.grid_size = int(self.base_grid_size * self.scale_factor)
        
        # 定义每列的格子数量
        self.cols_config = [1, 2, 3, 4, 4, 4, 4, 4, 3, 2, 1]
        self.num_cols = len(self.cols_config)
        self.max_rows = max(self.cols_config)
        
        # 计算网格总宽度和高度
        self.width = self.num_cols * self.grid_size
        self.height = self.max_rows * self.grid_size
        
        # 设置网格位置（默认在屏幕中央）
        self.position = (
            (self.screen_width - self.width) // 2,
            (self.screen_height - self.height) // 2
        )
        
        # 颜色定义
        self.GRID_COLOR = (220, 220, 220)  # 网格背景色
        self.BORDER_COLOR = (100, 100, 100)  # 网格边框色
        self.HIGHLIGHT_COLOR = (200, 255, 200)  # 高亮色
        
        # 初始化网格数据
        self.grid = []
        for col_idx, num_rows in enumerate(self.cols_config):
            col_cells = []
            for row_idx in range(self.max_rows):
                # 只有在有效的行范围内才创建格子
                if row_idx < num_rows:
                    col_cells.append({
                        'occupied': False,  # 是否被占用
                        'player': None,     # 占用的玩家
                        'highlight': False, # 是否高亮显示
                        'position': (row_idx, col_idx)  # 格子在网格中的位置 (row, col)
                    })
                else:
                    col_cells.append(None)  # 无效的格子位置
            self.grid.append(col_cells)
    
    def draw(self):
        """绘制网格"""
        # 绘制标题
        font = pygame.font.Font(None, int(36 * self.scale_factor))
        title = font.render("路径网格", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.position[0] + self.width // 2, self.position[1] - int(30 * self.scale_factor)))
        self.screen.blit(title, title_rect)
        
        # 遍历每列
        for col_idx, col_cells in enumerate(self.grid):
            # 计算这一列的有效格子数
            num_cells = self.cols_config[col_idx]
            # 计算这一列第一个格子的垂直偏移（使每列居中）
            v_offset = (self.max_rows - num_cells) * self.grid_size // 2
            
            # 特殊处理第五列、第七列和第九列，向下移动半个格子
            if col_idx in [4, 6, 8]:  # 由于索引从0开始，所以第5、7、9列对应索引4、6、8
                v_offset += self.grid_size // 2
            
            # 遍历这一列的每个有效格子
            for row_idx, cell in enumerate(col_cells):
                if cell is not None:  # 只绘制有效的格子
                    # 计算格子的屏幕坐标
                    x = self.position[0] + col_idx * self.grid_size
                    y = self.position[1] + row_idx * self.grid_size + v_offset
                    
                    # 选择颜色（高亮或普通）
                    if cell['highlight']:
                        color = self.HIGHLIGHT_COLOR
                    else:
                        color = self.GRID_COLOR
                    
                    # 绘制格子
                    pygame.draw.rect(self.screen, color, 
                                    pygame.Rect(x, y, self.grid_size, self.grid_size))
                    pygame.draw.rect(self.screen, self.BORDER_COLOR, 
                                    pygame.Rect(x, y, self.grid_size, self.grid_size), 
                                    max(1, int(2 * self.scale_factor)))
                    
                    # 如果格子被占用，绘制玩家标记
                    if cell['occupied'] and cell['player']:
                        # 这里可以自定义如何绘制玩家标记
                        player_color = cell['player'].get('color', (255, 0, 0))  # 默认红色
                        pygame.draw.circle(self.screen, player_color,
                                          (x + self.grid_size // 2, y + self.grid_size // 2),
                                          int(self.grid_size * 0.3))
    
    def get_cell_at_position(self, screen_pos):
        """根据屏幕坐标获取对应的格子"""
        x, y = screen_pos
        grid_x, grid_y = self.position
        
        # 检查是否在网格范围内
        if not (grid_x <= x < grid_x + self.width and grid_y <= y < grid_y + self.height):
            return None
        
        # 计算列索引
        col_idx = (x - grid_x) // self.grid_size
        if not (0 <= col_idx < self.num_cols):
            return None
        
        # 获取这一列的有效格子数
        num_cells = self.cols_config[col_idx]
        
        # 计算这一列的垂直偏移
        v_offset = (self.max_rows - num_cells) * self.grid_size // 2
        
        # 特殊处理第五列、第七列和第九列
        if col_idx in [4, 6, 8]:
            v_offset += self.grid_size // 2
        
        # 调整后的y坐标
        adjusted_y = y - grid_y - v_offset
        
        # 计算行索引
        row_idx = adjusted_y // self.grid_size
        
        # 检查行索引是否有效
        if not (0 <= row_idx < num_cells):
            return None
        
        # 返回对应的格子
        return self.grid[col_idx][row_idx]
    
    def set_cell_state(self, col, row, occupied=False, player=None, highlight=False):
        """设置格子状态"""
        # 检查索引是否有效
        if 0 <= col < self.num_cols:
            num_cells = self.cols_config[col]
            if 0 <= row < num_cells:
                cell = self.grid[col][row]
                if cell is not None:
                    cell['occupied'] = occupied
                    cell['player'] = player
                    cell['highlight'] = highlight
                    return True
        return False
    
    def highlight_cell(self, col, row, highlight=True):
        """高亮显示或取消高亮指定格子"""
        return self.set_cell_state(col, row, 
                                  occupied=self.grid[col][row]['occupied'],
                                  player=self.grid[col][row]['player'], 
                                  highlight=highlight)
    
    def occupy_cell(self, col, row, player):
        """玩家占据指定格子"""
        return self.set_cell_state(col, row, occupied=True, player=player, 
                                  highlight=self.grid[col][row]['highlight'])
    
    def clear_cell(self, col, row):
        """清除指定格子的占用状态"""
        return self.set_cell_state(col, row, occupied=False, player=None, 
                                  highlight=self.grid[col][row]['highlight'])
    
    def clear_all_highlights(self):
        """清除所有格子的高亮状态"""
        for col_idx, col_cells in enumerate(self.grid):
            for row_idx, cell in enumerate(col_cells):
                if cell is not None:
                    cell['highlight'] = False
    
    def get_cell_screen_position(self, col, row):
        """获取指定格子的屏幕坐标（左上角）"""
        # 检查索引是否有效
        if 0 <= col < self.num_cols:
            num_cells = self.cols_config[col]
            if 0 <= row < num_cells:
                # 计算这一列的垂直偏移
                v_offset = (self.max_rows - num_cells) * self.grid_size // 2
                
                # 特殊处理第五列、第七列和第九列
                if col in [4, 6, 8]:
                    v_offset += self.grid_size // 2
                
                # 计算格子的屏幕坐标
                x = self.position[0] + col * self.grid_size
                y = self.position[1] + row * self.grid_size + v_offset
                
                return (x, y)
        return None
    
    def get_cell_center(self, col, row):
        """获取指定格子的屏幕中心坐标"""
        pos = self.get_cell_screen_position(col, row)
        if pos:
            x, y = pos
            return (x + self.grid_size // 2, y + self.grid_size // 2)
        return None 