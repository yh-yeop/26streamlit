import pygame
import numpy as np
import random
import sys

# -------------------
# 설정
# -------------------
CELL = 40
GRID_SIZE = 10
WIDTH = CELL * GRID_SIZE
HEIGHT = CELL * GRID_SIZE + 150

WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
GRAY = (100, 100, 100)
BLUE = (80, 180, 255)

BLOCKS = [
    np.array([[1]]),
    np.array([[1, 1]]),
    np.array([[1, 1, 1]]),
    np.array([[1, 1],
              [1, 1]]),
    np.array([[1, 1, 1],
              [0, 1, 0]])
]

# -------------------
# 초기화
# -------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

score = 0
selected_block = None
blocks = [random.choice(BLOCKS) for _ in range(3)]

# -------------------
# 함수
# -------------------
def can_place(grid, block, x, y):
    h, w = block.shape
    if x + h > GRID_SIZE or y + w > GRID_SIZE:
        return False
    return np.all(grid[x:x+h, y:y+w] + block <= 1)

def place(grid, block, x, y):
    h, w = block.shape
    grid[x:x+h, y:y+w] += block
    return grid

def clear_lines(grid):
    global score

    for i in range(GRID_SIZE):
        if np.all(grid[i, :] == 1):
            grid[i, :] = 0
            score += 10

    for j in range(GRID_SIZE):
        if np.all(grid[:, j] == 1):
            grid[:, j] = 0
            score += 10

    return grid

def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j*CELL, i*CELL, CELL, CELL)
            color = BLUE if grid[i][j] else WHITE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def draw_blocks():
    for idx, b in enumerate(blocks):
        for i in range(b.shape[0]):
            for j in range(b.shape[1]):
                if b[i][j]:
                    x = j * 20 + idx * 120 + 20
                    y = GRID_SIZE * CELL + i * 20 + 20
                    pygame.draw.rect(screen, BLUE, (x, y, 18, 18))

def game_over():
    for b in blocks:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if can_place(grid, b, i, j):
                    return False
    return True

# -------------------
# 메인 루프
# -------------------
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            grid_x = my // CELL
            grid_y = mx // CELL

            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                if selected_block is not None:
                    block = blocks[selected_block]

                    if can_place(grid, block, grid_x, grid_y):
                        grid = place(grid, block, grid_x, grid_y)
                        grid = clear_lines(grid)

                        blocks[selected_block] = random.choice(BLOCKS)

    # 키 입력 (블록 선택)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        selected_block = 0
    if keys[pygame.K_2]:
        selected_block = 1
    if keys[pygame.K_3]:
        selected_block = 2

    draw_grid()
    draw_blocks()

    # 점수 표시
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, HEIGHT - 40))

    # 게임 오버
    if game_over():
        over = font.render("GAME OVER", True, (255, 100, 100))
        screen.blit(over, (WIDTH//2 - 80, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()