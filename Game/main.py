import pygame
import sys
import os
from src.components.Chessboard.Chessboard import Chessboard
from src.components.Chess.ChessPiece import ChessPiece

# 获取项目根目录路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_size = (1440, 900)
screen = pygame.display.set_mode(screen_size)

# 设置窗口标题
pygame.display.set_caption("Card Game")

# 定义颜色
WHITE = (255, 255, 255)

# 计算棋盘横向居中位置
center_x = (screen_size[0] - 600) // 2

# 初始化玩家棋盘（位于屏幕底部边框）
myChessboard = Chessboard(screen)
myChessboard.position = (center_x, screen_size[1] - 400)  # 将y坐标调整到屏幕高度减去棋盘高度的位置

# 初始化对手棋盘（位于屏幕上方）
opponentChessboard = Chessboard(screen)
opponentChessboard.position = (center_x, 50)

# 显示棋盘位置信息
print(f"屏幕尺寸: {screen_size}")
print(f"我的棋盘位置: {myChessboard.position}")
print(f"对手棋盘位置: {opponentChessboard.position}")
print(f"棋盘大小: {myChessboard.size}x{myChessboard.size}")

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

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                myChessboard.start_drag(event.pos)
                opponentChessboard.start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 左键释放
                myChessboard.end_drag(event.pos)
                opponentChessboard.end_drag(event.pos)

    # 填充背景色
    screen.fill(WHITE)

    # 绘制两个棋盘
    myChessboard.draw()
    opponentChessboard.draw()

    # 更新显示
    pygame.display.flip()

# 清理并退出
pygame.quit()
sys.exit() 