import pygame
import sys
import os
from src.components.Chessboard.Chessboard import Chessboard
from src.components.Chess.ChessPiece import ChessPiece
from src.components.BackPack.BackPack import BackPack
from src.components.Item.Item import Item
from src.components.RewardBox.RewardBox import RewardBox
from src.components.Message.MessageBoard import MessageBoard
from src.components.Grid.PathGrid import PathGrid
from src.components.Animation.BulletAnimation import BulletAnimation

# 获取项目根目录路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_size = (1440, 700)
screen = pygame.display.set_mode(screen_size)

# 计算缩放比例（基于参考分辨率1920*1200）
scale_factor = min(screen_size[0] / 1920, screen_size[1] / 1200)

# 设置窗口标题
pygame.display.set_caption("Card Game")

# 定义颜色
WHITE = (255, 255, 255)

# 计算棋盘横向居中位置
center_x = int((screen_size[0] - int(300 * scale_factor)) //4)

# 初始化玩家棋盘（位于屏幕底部边框）
myChessboard = Chessboard(screen)
myChessboard.position = (center_x, screen_size[1] - int(400 * scale_factor))  # 将y坐标调整到屏幕高度减去棋盘高度的位置

# 初始化对手棋盘（位于屏幕上方）
opponentChessboard = Chessboard(screen)
opponentChessboard.position = (center_x, int(50 * scale_factor))

# 初始化背包（位于玩家棋盘右侧两个格子的距离）
backpack = BackPack(screen, myChessboard)

# 初始化奖励盒子（位于屏幕中央）
rewardBox = RewardBox(screen)

# 初始化消息板（位于玩家棋盘左侧一个棋子的距离）
messageBoard = MessageBoard(screen, myChessboard)
messageBoard.add_message("游戏开始！准备战斗！")
messageBoard.update_coins(100)  # 初始金币

# 初始化路径网格
pathGrid = PathGrid(screen, myChessboard)
# 修改路径网格位置，放置在右上角
pathGrid.position = (
    screen_size[0] - pathGrid.width - int(20 * scale_factor),  # 距离右边缘20个像素
    int(20 * scale_factor)  # 距离上边缘20个像素
)

# 添加一些示例物品和棋子到奖励盒子
reward_items = [
    Item(attack=20, lifepoint=15, ability="增加20点攻击力和15点生命值"),
    ChessPiece(attack=10, lifepoint=12, job="奖励战士", is_fusion=False, color=(255, 215, 0)),
    Item(attack=5, lifepoint=30, ability="增加5点攻击力和30点生命值")
]

# 将物品和棋子添加到奖励盒子
for item in reward_items:
    rewardBox.add_item(item)

# 显示棋盘和盒子位置信息
print(f"屏幕尺寸: {screen_size}")
print(f"我的棋盘位置: {myChessboard.position}")
print(f"对手棋盘位置: {opponentChessboard.position}")
print(f"背包位置: {backpack.position}")
print(f"奖励盒子位置: {rewardBox.position}")
print(f"消息板位置: {messageBoard.position}")
print(f"棋盘大小: {myChessboard.size}x{myChessboard.size}")
print(f"背包大小: {backpack.width}x{backpack.height}")
print(f"奖励盒子大小: {rewardBox.width}x{rewardBox.height}")
print(f"消息板大小: {messageBoard.width}x{messageBoard.height}")
print(f"背包格子大小: {backpack.grid_size}")
print(f"棋盘格子大小: {myChessboard.grid_size}")
print(f"奖励盒子格子大小: {rewardBox.grid_size}")
print(f"缩放比例: {scale_factor}")

# 创建示例棋子 - 玩家
warrior = ChessPiece(attack=5, lifepoint=10, job="战士", is_fusion=False, color=(255, 0, 0))
mage = ChessPiece(attack=8, lifepoint=5, job="法师", is_fusion=False, color=(0, 0, 255))
fusion_piece = ChessPiece(attack=12, lifepoint=12, job="融合战士", is_fusion=True, color=(255, 100, 100))
archer = ChessPiece(attack=7, lifepoint=7, job="弓箭手", is_fusion=False, color=(0, 255, 0))

# 使用setChess方法在玩家棋盘上放置棋子
myChessboard.setChess(warrior, 1)    # 第一格 (左上角)
myChessboard.setChess(mage, 5)       # 第五格 (中间)
myChessboard.setChess(fusion_piece, 9)  # 第九格 (右下角)
myChessboard.setChess(archer, 4)     # 第四格 (第二排第一个)

# 创建示例棋子 - 对手
enemy_warrior = ChessPiece(attack=6, lifepoint=9, job="敌方战士", is_fusion=False, color=(200, 50, 50))
enemy_mage = ChessPiece(attack=9, lifepoint=4, job="敌方法师", is_fusion=False, color=(50, 50, 200))
enemy_fusion = ChessPiece(attack=13, lifepoint=11, job="敌方融合战士", is_fusion=True, color=(220, 80, 80))
enemy_archer = ChessPiece(attack=8, lifepoint=6, job="敌方弓箭手", is_fusion=False, color=(50, 200, 50))

# 使用setChess方法在对手棋盘上放置棋子
opponentChessboard.setChess(enemy_warrior, 1)  # 第一格 (左上角)
opponentChessboard.setChess(enemy_mage, 5)     # 第五格 (中间)
opponentChessboard.setChess(enemy_fusion, 9)   # 第九格 (右下角)
opponentChessboard.setChess(enemy_archer, 4)   # 第四格 (第二排第一个)

# 创建一些额外的棋子放入背包
backpack_pieces = [
    ChessPiece(attack=6, lifepoint=8, job="背包战士1", is_fusion=False, color=(255, 100, 0)),
    ChessPiece(attack=7, lifepoint=7, job="背包法师1", is_fusion=False, color=(100, 100, 255)),
    ChessPiece(attack=9, lifepoint=4, job="背包弓手1", is_fusion=False, color=(0, 200, 100)),
    ChessPiece(attack=15, lifepoint=15, job="背包融合战士", is_fusion=True, color=(255, 150, 150))
]

# 将棋子添加到背包
for piece in backpack_pieces:
    backpack.add_piece(piece)

# 打印棋子状态信息
print("\n玩家棋子状态:")
print(f"战士: {warrior}")
print(f"法师: {mage}")
print(f"融合战士: {fusion_piece}")
print(f"弓箭手: {archer}")

print("\n对手棋子状态:")
print(f"敌方战士: {enemy_warrior}")
print(f"敌方法师: {enemy_mage}")
print(f"敌方融合战士: {enemy_fusion}")
print(f"敌方弓箭手: {enemy_archer}")

print(f"\n背包中的棋子数量: {backpack.count_pieces()}")

# 加载回合结束按钮的图片
button_images = []
for i in range(1, 22):
    try:
        # 修改路径，加入"遥感图片"文件夹
        img_path = os.path.join(project_root, "assets", "images", "摇杆图片", f"{i}.png")
        img = pygame.image.load(img_path)
        # 调整图片大小，根据需要调整
        img = pygame.transform.scale(img, (int(400 * scale_factor), int(400 * scale_factor)))
        button_images.append(img)
    except Exception as e:
        print(f"无法加载图片: {i}.png - 错误: {e}")
        # 创建一个默认图片（红色方块）
        default_img = pygame.Surface((int(100 * scale_factor), int(100 * scale_factor)))
        default_img.fill((255, 0, 0))
        button_images.append(default_img)

# 按钮动画状态
button_animation_active = False
button_animation_start_time = 0
button_animation_frame = 0
button_animation_duration = 250  # 2秒内完成动画
button_animation_frames = len(button_images)

# 修改回合结束按钮的位置代码
button_size = button_images[0].get_size()
button_rect = pygame.Rect(
    screen_size[0] - button_size[0] - int(20 * scale_factor),
    screen_size[1] - button_size[1] - int(50 * scale_factor),
    button_size[0],
    button_size[1]
)

# 在游戏初始化部分添加玩家信息和当前位置
# 玩家信息
player = {
    'color': (0, 100, 255),  # 玩家标记颜色
    'name': '玩家1',         # 玩家名称
    'position': None         # 当前位置，初始为None
}

# 在主循环之前，初始化一些设置
# 高亮显示起始位置
pathGrid.highlight_cell(0, 0, True)  # 第一列第一个格子高亮

# 高亮显示可移动的下一步位置（第二列的临近格子）
if pathGrid.cols_config[1] >= 1:  # 确保第二列至少有一个格子
    # 高亮第二列中与起点相邻的格子（第一行和第二行）
    for r in range(0, min(2, pathGrid.cols_config[1])):
        pathGrid.highlight_cell(1, r, True)

# 游戏主循环
running = True
clock = pygame.time.Clock()
button_animation_timer = 0
animation_duration = 2000  # 动画持续时间（毫秒）
button_clicked = False
current_frame = 0
active_animations = []  # 用于存储活跃的子弹动画

# 拖拽状态变量
currently_dragging = None  # 可以是 "my_chessboard", "opponent_chessboard", "backpack" 或 None
dragged_piece = None

while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                # 检查是否点击了路径网格
                cell = pathGrid.get_cell_at_position(event.pos)
                if cell:
                    col, row = cell['position'][1], cell['position'][0]  # position 是 (row, col)
                    
                    # 检查是否可以移动到这个格子
                    can_move = False
                    
                    # 第一次移动，可以从起点开始
                    if player['position'] is None and col == 0 and row == 0:
                        can_move = True
                    # 后续移动规则：只能移动到下一列的临近两格
                    elif player['position']:
                        current_col, current_row = player['position']
                        
                        # 检查是否是相邻列
                        if col == current_col + 1:
                            # 检查是否是临近两格（当前行、上一行或下一行）
                            if abs(row - current_row) <= 1:
                                can_move = True
                    
                    if can_move:
                        # 如果当前有位置，清除旧位置
                        if player['position']:
                            old_col, old_row = player['position']
                            pathGrid.clear_cell(old_col, old_row)
                        
                        # 高亮可移动的下一步位置
                        pathGrid.clear_all_highlights()
                        next_col = col + 1
                        if next_col < pathGrid.num_cols:
                            # 获取下一列的行数
                            next_col_rows = pathGrid.cols_config[next_col]
                            # 高亮当前行和相邻行（如果存在）
                            for r in range(max(0, row-1), min(next_col_rows, row+2)):
                                pathGrid.highlight_cell(next_col, r, True)
                        
                        # 更新玩家位置
                        player['position'] = (col, row)
                        pathGrid.occupy_cell(col, row, player)
                        
                        # 添加移动消息
                        messageBoard.add_message(f"移动到位置: 列{col+1}行{row+1}")
                        
                        # 如果到达终点（最后一列）
                        if col == pathGrid.num_cols - 1:
                            messageBoard.add_message("到达终点！")
                            # 这里可以添加到达终点的奖励逻辑
                
                # 处理菜单点击
                if myChessboard.show_menu:
                    if myChessboard.handle_menu_click(event.pos):
                        # 选择了攻击选项
                        row, col = myChessboard.menu_target
                        piece = myChessboard.grid[row][col]
                        if piece and piece.can_attack():
                            success, attack_message, attacker_pos, target_pos = myChessboard.attack_opponent(opponentChessboard, row, col, is_player=True)
                            if success:
                                messageBoard.add_message(attack_message)
                            piece.mark_as_attacked()
                        myChessboard.show_menu = False
                    # 不管点击了菜单上的什么，都阻止下面的拖拽逻辑
                    continue
                
                # 检查是否在奖励盒子中开始拖拽
                if rewardBox.start_drag(event.pos):
                    currently_dragging = "reward_box"
                    dragged_piece = rewardBox.dragged_piece
                    continue
                
                # 检查是否在背包中开始拖拽
                if backpack.start_drag(event.pos):
                    currently_dragging = "backpack"
                    dragged_piece = backpack.dragged_piece
                    continue
                
                # 尝试从我方棋盘拖拽
                if not currently_dragging:
                    myChessboard.start_drag(event.pos)
                    if myChessboard.dragging:
                        currently_dragging = "my_chessboard"
                        dragged_piece = myChessboard.dragged_piece
                        continue
                
                # 尝试从对手棋盘拖拽（通常不应该允许，但保留代码以便将来可能的使用）
                if not currently_dragging:
                    opponentChessboard.start_drag(event.pos)
                    if opponentChessboard.dragging:
                        currently_dragging = "opponent_chessboard"
                        dragged_piece = opponentChessboard.dragged_piece
                        continue
                
                # 检查是否点击了回合结束按钮
                if button_rect.collidepoint(event.pos):
                    # 开始按钮动画
                    button_animation_active = True
                    button_animation_start_time = pygame.time.get_ticks()
                    button_animation_frame = 0  # 从第一帧开始
                    
                    # 进入下一回合
                    messageBoard.next_turn()
                    messageBoard.update_coins(10)  # 每回合增加10金币
                    
                    # 敌方棋子攻击逻辑
                    for row in range(3):
                        for col in range(3):
                            enemy_piece = opponentChessboard.grid[row][col]
                            if enemy_piece and enemy_piece.can_attack():
                                success, attack_message, attacker_pos, target_pos = opponentChessboard.attack_opponent(myChessboard, row, col, is_player=False)
                                if success:
                                    messageBoard.add_message(attack_message)
                                    enemy_piece.mark_as_attacked()
                    
                    # 重置所有棋子的攻击状态
                    for row in range(3):
                        for col in range(3):
                            # 重置我方棋子的攻击状态
                            piece = myChessboard.grid[row][col]
                            if piece:
                                piece.reset_attack_status()
                            
                            # 重置敌方棋子的攻击状态
                            enemy_piece = opponentChessboard.grid[row][col]
                            if enemy_piece:
                                enemy_piece.reset_attack_status()
            
            elif event.button == 3:  # 右键点击
                # 检查玩家棋盘上的点击
                pos = myChessboard.get_grid_position(event.pos)
                if pos:
                    row, col = pos
                    piece = myChessboard.grid[row][col]
                    if piece:
                        # 显示右键菜单
                        myChessboard.show_context_menu(event.pos, row, col)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左键释放
                if currently_dragging == "reward_box":
                    # 检查是否释放在我方棋盘上
                    my_pos = myChessboard.get_grid_position(event.pos)
                    if my_pos:
                        row, col = my_pos
                        piece = myChessboard.grid[row][col]
                        
                        # 记录原始位置，避免索引错误
                        orig_row, orig_col = dragged_piece.position
                        
                        # 如果是物品且目标位置有棋子，应用物品效果
                        if piece and isinstance(dragged_piece, Item):
                            # 如果是物品，应用到棋子上
                            if dragged_piece.apply_to_piece(piece):
                                # 物品使用成功，从奖励盒子中移除
                                if 0 <= orig_row < rewardBox.rows and 0 <= orig_col < rewardBox.cols:
                                    rewardBox.grid[orig_row][orig_col] = None
                                rewardBox.dragged_piece = None
                                rewardBox.dragging = False
                                currently_dragging = None
                                dragged_piece = None
                                continue
                        # 如果是棋子且目标位置为空，将棋子放置到棋盘上
                        elif not piece and isinstance(dragged_piece, ChessPiece):
                            # 从奖励盒子移动棋子到我方棋盘
                            myChessboard.grid[row][col] = dragged_piece
                            dragged_piece.set_position(row, col)
                            if 0 <= orig_row < rewardBox.rows and 0 <= orig_col < rewardBox.cols:
                                rewardBox.grid[orig_row][orig_col] = None
                            rewardBox.dragged_piece = None
                            rewardBox.dragging = False
                            currently_dragging = None
                            dragged_piece = None
                            continue
                    
                    # 检查是否释放在对手棋盘上
                    opponent_pos = opponentChessboard.get_grid_position(event.pos)
                    if opponent_pos:
                        row, col = opponent_pos
                        piece = opponentChessboard.grid[row][col]
                        
                        # 记录原始位置，避免索引错误
                        orig_row, orig_col = dragged_piece.position
                        
                        if piece and isinstance(dragged_piece, Item):
                            # 如果是物品，应用到棋子上
                            if dragged_piece.apply_to_piece(piece):
                                # 物品使用成功，从奖励盒子中移除
                                if 0 <= orig_row < rewardBox.rows and 0 <= orig_col < rewardBox.cols:
                                    rewardBox.grid[orig_row][orig_col] = None
                                rewardBox.dragged_piece = None
                                rewardBox.dragging = False
                                currently_dragging = None
                                dragged_piece = None
                                continue
                    
                    # 检查是否释放在背包上
                    bp_pos = backpack.get_grid_position(event.pos)
                    if bp_pos:
                        row, col = bp_pos
                        piece = backpack.grid[row][col]
                        
                        # 记录原始位置，避免索引错误
                        orig_row, orig_col = dragged_piece.position
                        
                        # 如果背包位置为空，移动到背包
                        if not piece:
                            backpack.grid[row][col] = dragged_piece
                            dragged_piece.set_position(row, col)
                            if 0 <= orig_row < rewardBox.rows and 0 <= orig_col < rewardBox.cols:
                                rewardBox.grid[orig_row][orig_col] = None
                            rewardBox.dragged_piece = None
                            rewardBox.dragging = False
                            currently_dragging = None
                            dragged_piece = None
                            continue
                    
                    # 如果不是放在棋盘或背包上，恢复到奖励盒子中
                    rewardBox.end_drag(event.pos)
                    currently_dragging = None
                    dragged_piece = None
                
                elif currently_dragging == "backpack":
                    # 检查是否释放在我方棋盘上
                    my_pos = myChessboard.get_grid_position(event.pos)
                    if my_pos:
                        row, col = my_pos
                        piece = myChessboard.grid[row][col]
                        
                        # 如果是物品且目标位置有棋子，应用物品效果
                        if piece and isinstance(dragged_piece, Item):
                            # 如果是物品，应用到棋子上
                            if dragged_piece.apply_to_piece(piece):
                                # 物品使用成功，从背包中移除
                                backpack.grid[dragged_piece.position[0]][dragged_piece.position[1]] = None
                                backpack.dragged_piece = None
                                backpack.dragging = False
                                currently_dragging = None
                                dragged_piece = None
                                continue
                        # 如果是棋子，处理交换逻辑
                        elif isinstance(dragged_piece, ChessPiece):
                            # 获取背包中原始位置
                            bp_row, bp_col = dragged_piece.position
                            
                            # 如果目标位置有棋子，交换位置
                            if piece:
                                # 将棋盘上的棋子移动到背包
                                backpack.grid[bp_row][bp_col] = piece
                                piece.set_position(bp_row, bp_col)
                            else:
                                # 如果目标位置为空，清空背包中的位置
                                backpack.grid[bp_row][bp_col] = None
                            
                            # 将拖拽的棋子放到棋盘上
                            myChessboard.grid[row][col] = dragged_piece
                            dragged_piece.set_position(row, col)
                            
                            backpack.dragged_piece = None
                            backpack.dragging = False
                            currently_dragging = None
                            dragged_piece = None
                            continue
                    
                    # 检查是否释放在对手棋盘上
                    opponent_pos = opponentChessboard.get_grid_position(event.pos)
                    if opponent_pos:
                        row, col = opponent_pos
                        piece = opponentChessboard.grid[row][col]
                        if piece and isinstance(dragged_piece, Item):
                            # 如果是物品，应用到棋子上
                            if dragged_piece.apply_to_piece(piece):
                                # 物品使用成功，从背包中移除
                                backpack.grid[dragged_piece.position[0]][dragged_piece.position[1]] = None
                                backpack.dragged_piece = None
                                backpack.dragging = False
                                currently_dragging = None
                                dragged_piece = None
                                continue
                    
                    # 如果不是放在棋盘上，尝试放回背包
                    backpack.end_drag(event.pos)
                    currently_dragging = None
                    dragged_piece = None
                
                elif currently_dragging == "my_chessboard":
                    # 检查是否释放在背包上
                    bp_pos = backpack.get_grid_position(event.pos)
                    if bp_pos:
                        row, col = bp_pos
                        piece = backpack.grid[row][col]
                        
                        # 获取棋盘上原始位置
                        chess_row, chess_col = dragged_piece.position
                        
                        # 如果背包位置有棋子，交换位置
                        if piece:
                            # 将背包中的棋子移动到棋盘
                            myChessboard.grid[chess_row][chess_col] = piece
                            piece.set_position(chess_row, chess_col)
                        else:
                            # 如果背包位置为空，清空棋盘上的位置
                            myChessboard.grid[chess_row][chess_col] = None
                        
                        # 将拖拽的棋子放到背包中
                        backpack.grid[row][col] = dragged_piece
                        dragged_piece.set_position(row, col)
                        
                        myChessboard.dragged_piece = None
                        myChessboard.dragging = False
                        currently_dragging = None
                        dragged_piece = None
                        continue
                    
                    # 如果不是放在背包上，结束拖拽
                    myChessboard.end_drag(event.pos)
                    currently_dragging = None
                    dragged_piece = None
                
                elif currently_dragging == "opponent_chessboard":
                    # 结束对手棋盘的拖拽（通常不允许）
                    opponentChessboard.end_drag(event.pos)
                    currently_dragging = None
                    dragged_piece = None

    # 填充背景色
    screen.fill(WHITE)

    # 绘制两个棋盘、背包、奖励盒子和消息板
    myChessboard.draw()
    opponentChessboard.draw()
    backpack.draw()
    rewardBox.draw()
    messageBoard.draw()
    pathGrid.draw()
    
    # 绘制当前拖拽的棋子（如果有）
    if dragged_piece:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 假设棋子图片大小为80x80像素
        piece_size = int(80 * scale_factor)
        img_x = mouse_x - piece_size // 2
        img_y = mouse_y - piece_size // 2
        
        # 获取棋子图片
        if dragged_piece.image:
            scaled_image = pygame.transform.scale(dragged_piece.image, (piece_size, piece_size))
            screen.blit(scaled_image, (img_x, img_y))
        else:
            # 如果没有图片，绘制一个圆形代表棋子
            pygame.draw.circle(screen, dragged_piece.color, (mouse_x, mouse_y), int(40 * scale_factor))
        
        # 创建半透明黑色背景使属性文字更清晰
        text_bg_width = int(60 * scale_factor)
        text_bg_height = int(24 * scale_factor)
        text_bg = pygame.Surface((text_bg_width, text_bg_height))
        text_bg.set_alpha(150)  # 半透明
        text_bg.fill((0, 0, 0))
        
        # 绘制属性背景
        bg_x = mouse_x - text_bg_width // 2
        bg_y = mouse_y + int(30 * scale_factor)
        screen.blit(text_bg, (bg_x, bg_y))
        
        # 绘制棋子属性
        font = pygame.font.Font(None, int(24 * scale_factor))
        attack_text = font.render(str(dragged_piece.attack), True, (255, 0, 0))  # 攻击力红色
        lifepoint_text = font.render(str(dragged_piece.lifepoint), True, (0, 255, 0))  # 生命值绿色
        screen.blit(attack_text, (bg_x + int(10 * scale_factor), bg_y + int(4 * scale_factor)))
        screen.blit(lifepoint_text, (bg_x + int(35 * scale_factor), bg_y + int(4 * scale_factor)))

    # 绘制回合结束按钮
    if button_animation_active:
        # 如果动画激活，计算当前应该显示的帧
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - button_animation_start_time
        
        # 计算当前应该显示的帧索引（在2秒内从1.png播放到12.png）
        frame_index = min(int(elapsed_time / button_animation_duration * button_animation_frames), button_animation_frames - 1)
        screen.blit(button_images[frame_index], button_rect)
        
        # 动画结束重置
        if elapsed_time >= button_animation_duration:
            button_animation_active = False
            button_animation_frame = 0
    else:
        # 如果动画没有激活，显示第一帧
        screen.blit(button_images[0], button_rect)

    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 清理并退出
pygame.quit()
sys.exit() 