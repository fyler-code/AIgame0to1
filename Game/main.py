import pygame
import sys
import os
from src.components.Chessboard.Chessboard import Chessboard
from src.components.Chess.ChessPiece import ChessPiece
from src.components.BackPack.BackPack import BackPack
from src.components.Item.Item import Item

# 获取项目根目录路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_size = (1440, 900)
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

# 显示棋盘位置信息
print(f"屏幕尺寸: {screen_size}")
print(f"我的棋盘位置: {myChessboard.position}")
print(f"对手棋盘位置: {opponentChessboard.position}")
print(f"背包位置: {backpack.position}")
print(f"棋盘大小: {myChessboard.size}x{myChessboard.size}")
print(f"背包大小: {backpack.width}x{backpack.height}")
print(f"背包格子大小: {backpack.grid_size}")
print(f"棋盘格子大小: {myChessboard.grid_size}")
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

# 游戏主循环
running = True
clock = pygame.time.Clock()

# 拖拽状态变量
currently_dragging = None  # 可以是 "my_chessboard", "opponent_chessboard", "backpack" 或 None
dragged_piece = None

# 回合结束按钮
button_font = pygame.font.Font(None, int(36 * scale_factor))
button_text = button_font.render("Time End", True, (0, 0, 0))
button_rect = button_text.get_rect(center=(screen_size[0] // 2, screen_size[1] - int(50 * scale_factor)))

while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                # 处理菜单点击
                if myChessboard.show_menu:
                    if myChessboard.handle_menu_click(event.pos):
                        # 选择了攻击选项
                        row, col = myChessboard.menu_target
                        piece = myChessboard.grid[row][col]
                        if piece and piece.can_attack():
                            myChessboard.attack_opponent(opponentChessboard, row, col, is_player=True)
                            piece.mark_as_attacked()
                        myChessboard.show_menu = False
                    # 不管点击了菜单上的什么，都阻止下面的拖拽逻辑
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
                    # 敌方棋子攻击逻辑
                    for row in range(3):
                        for col in range(3):
                            enemy_piece = opponentChessboard.grid[row][col]
                            if enemy_piece and enemy_piece.can_attack():
                                opponentChessboard.attack_opponent(myChessboard, row, col, is_player=False)
                                enemy_piece.mark_as_attacked()
                    # 重置我方棋子的攻击状态
                    for row in range(3):
                        for col in range(3):
                            piece = myChessboard.grid[row][col]
                            if piece:
                                piece.reset_attack_status()
            
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
                if currently_dragging == "backpack":
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

    # 绘制两个棋盘和背包
    myChessboard.draw()
    opponentChessboard.draw()
    backpack.draw()
    
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
            # 绘制棋子属性
            font = pygame.font.Font(None, int(24 * scale_factor))
            attack_text = font.render(str(dragged_piece.attack), True, (255, 255, 255))
            lifepoint_text = font.render(str(dragged_piece.lifepoint), True, (255, 255, 255))
            screen.blit(attack_text, (mouse_x - int(15 * scale_factor), mouse_y - int(10 * scale_factor)))
            screen.blit(lifepoint_text, (mouse_x + int(5 * scale_factor), mouse_y - int(10 * scale_factor)))

    # 绘制回合结束按钮
    pygame.draw.rect(screen, (200, 200, 200), button_rect.inflate(int(20 * scale_factor), int(10 * scale_factor)))
    screen.blit(button_text, button_rect)

    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 清理并退出
pygame.quit()
sys.exit() 