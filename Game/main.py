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
screen_size = (1920, 1080)
screen = pygame.display.set_mode(screen_size)

# 设置窗口标题
pygame.display.set_caption("Card Game")

# 定义颜色
WHITE = (255, 255, 255)

# 初始化棋盘（位于屏幕左侧）
chessboard = Chessboard(screen)

# 显示棋盘位置信息
print(f"屏幕尺寸: {screen_size}")
print(f"棋盘位置: {chessboard.position}")
print(f"棋盘大小: {chessboard.size}x{chessboard.size}")
print(f"棋盘位置: 屏幕左侧，距离左边缘50像素")

# 创建示例棋子
warrior = ChessPiece(attack=5, lifepoint=10, job="战士", is_fusion=False, color=(255, 0, 0))
mage = ChessPiece(attack=8, lifepoint=5, job="法师", is_fusion=False, color=(0, 0, 255))
fusion_piece = ChessPiece(attack=12, lifepoint=12, job="融合战士", is_fusion=True, color=(255, 100, 100))
archer = ChessPiece(attack=7, lifepoint=7, job="弓箭手", is_fusion=False, color=(0, 255, 0))

# 使用setChess方法放置棋子
chessboard.setChess(warrior, 1)  # 第一格 (左上角)
chessboard.setChess(mage, 5)     # 第五格 (中间)
chessboard.setChess(fusion_piece, 9)  # 第九格 (右下角)
chessboard.setChess(archer, 4)   # 第四格 (第二排第一个)

# 打印棋子状态信息
print("\n棋子状态:")
print(f"战士: {warrior}")
print(f"法师: {mage}")
print(f"融合战士: {fusion_piece}")
print(f"弓箭手: {archer}")

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 点击事件处理
            if event.button == 1:  # 左键点击
                pos = chessboard.get_grid_position(event.pos)
                if pos:
                    row, col = pos
                    position = row * 3 + col + 1  # 计算位置序号
                    print(f"点击了棋盘位置: {row}, {col} (位置序号: {position})")

    # 填充背景色
    screen.fill(WHITE)

    # 绘制棋盘
    chessboard.draw()

    # 更新显示
    pygame.display.flip()

# 清理并退出
pygame.quit()
sys.exit() 