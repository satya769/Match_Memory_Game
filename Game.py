import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 4, 4
TILE_SIZE = WIDTH // COLS
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Match Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (100, 255, 100)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 48)

# Generate card values
def create_board():
    values = list(range(1, 9)) * 2  # 8 pairs
    random.shuffle(values)
    board = [values[i * COLS:(i + 1) * COLS] for i in range(ROWS)]
    return board

board = create_board()
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
matched = [[False for _ in range(COLS)] for _ in range(ROWS)]

first_pick = None
second_pick = None
match_check_time = 0

def draw_board():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if matched[row][col] or revealed[row][col]:
                pygame.draw.rect(screen, GREEN, rect)
                text = font.render(str(board[row][col]), True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
    pygame.display.flip()

def get_tile(pos):
    x, y = pos
    row, col = y // TILE_SIZE, x // TILE_SIZE
    if row < ROWS and col < COLS:
        return row, col
    return None

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)
    draw_board()

    current_time = pygame.time.get_ticks()
    if first_pick and second_pick and current_time - match_check_time > 1000:
        r1, c1 = first_pick
        r2, c2 = second_pick
        if board[r1][c1] == board[r2][c2]:
            matched[r1][c1] = True
            matched[r2][c2] = True
        else:
            revealed[r1][c1] = False
            revealed[r2][c2] = False
        first_pick = None
        second_pick = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not first_pick or (first_pick and not second_pick):
                tile = get_tile(event.pos)
                if tile:
                    row, col = tile
                    if not revealed[row][col] and not matched[row][col]:
                        revealed[row][col] = True
                        if not first_pick:
                            first_pick = tile
                        else:
                            second_pick = tile
                            match_check_time = pygame.time.get_ticks()

pygame.quit()
