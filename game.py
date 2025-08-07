import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mole Box - Whack Challenge")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_COLOR = (200, 200, 200)
MOLE_COLOR = (139, 69, 19)
TEXT_COLOR = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
DARK_METALLIC_BLUE = (10, 25, 45)
HIGHLIGHT_BLUE = (20, 40, 70)

font = pygame.font.SysFont("comicsansms", 28)
big_font = pygame.font.SysFont("comicsansms", 50)

MOLE_RADIUS = 35
HOLE_POSITIONS = [
    (150, 200), (300, 200), (450, 200),
    (150, 320), (300, 320), (450, 320),
    (150, 440), (300, 440), (450, 440)
]

MOLE_KEYS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

score = 0
misses = 0
max_misses = 3
game_over = False
show_retry_button = False
in_main_menu = True
mole_index = None
mole_timer = 0
MOLE_DURATION = 1500
MOLE_SPEED_MULTIPLIER = 1.0

def draw_background():
    screen.fill(DARK_METALLIC_BLUE)
    for i in range(0, WIDTH, 60):
        pygame.draw.line(screen, HIGHLIGHT_BLUE, (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 60):
        pygame.draw.line(screen, HIGHLIGHT_BLUE, (0, i), (WIDTH, i), 1)

def draw_main_menu():
    draw_background()
    draw_text("Whack-a-Mole Challenge", WIDTH // 2, HEIGHT // 2 - 80, size=40)
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 100, HEIGHT // 2, 200, 60))
    draw_text("Start Game", WIDTH // 2, HEIGHT // 2 + 30, size=30)

def draw_mole_box():
    pygame.draw.rect(screen, BORDER_COLOR, (75, 150, 450, 350), 5)
    for pos in HOLE_POSITIONS:
        pygame.draw.circle(screen, BLACK, pos, MOLE_RADIUS)

def draw_mole(index):
    if index is not None:
        pygame.draw.circle(screen, MOLE_COLOR, HOLE_POSITIONS[index], MOLE_RADIUS)

def draw_text(text, x, y, size=28, center=True, color=TEXT_COLOR):
    f = pygame.font.SysFont("comicsansms", size)
    txt = f.render(text, True, color)
    rect = txt.get_rect(center=(x, y) if center else (x, y))
    screen.blit(txt, rect)

def draw_retry_button():
    pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 80, HEIGHT // 2 + 80, 160, 50))
    draw_text("Retry", WIDTH // 2, HEIGHT // 2 + 105, size=30)

def reset_game():
    global score, misses, game_over, show_retry_button, mole_index, mole_timer, MOLE_DURATION, MOLE_SPEED_MULTIPLIER
    score = 0
    misses = 0
    game_over = False
    show_retry_button = False
    mole_index = None
    mole_timer = 0
    MOLE_DURATION = 1500
    MOLE_SPEED_MULTIPLIER = 1.0

running = True
reset_game()

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_main_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and HEIGHT // 2 <= y <= HEIGHT // 2 + 60:
                    in_main_menu = False
                    reset_game()
        elif not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and mole_index is not None:
                mx, my = pygame.mouse.get_pos()
                hole_x, hole_y = HOLE_POSITIONS[mole_index]
                distance = ((mx - hole_x) ** 2 + (my - hole_y) ** 2) ** 0.5
                if distance <= MOLE_RADIUS:
                    score += 1
                    mole_index = None
                    mole_timer = 0
                    if score % 5 == 0:
                        MOLE_SPEED_MULTIPLIER *= 1.5
                        MOLE_DURATION = max(300, int(1500 / MOLE_SPEED_MULTIPLIER))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH // 2 - 80 <= x <= WIDTH // 2 + 80 and HEIGHT // 2 + 80 <= y <= HEIGHT // 2 + 130:
                    in_main_menu = True

    if in_main_menu:
        draw_main_menu()
    else:
        draw_background()
        draw_mole_box()
        draw_mole(mole_index)

        if not game_over:
            if mole_index is None:
                mole_index = random.randint(0, 8)
                mole_timer = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - mole_timer > MOLE_DURATION:
                    misses += 1
                    mole_index = None
                    mole_timer = 0
                    if misses >= max_misses:
                        game_over = True
                        show_retry_button = True

        draw_text(f"Score: {score}", 80, 40)
        draw_text(f"Misses: {misses}/{max_misses}", WIDTH - 140, 40)

        if game_over:
            draw_text("GAME OVER", WIDTH // 2, HEIGHT // 2 - 50, size=50, color=RED)
            if show_retry_button:
                draw_retry_button()

    pygame.display.flip()

pygame.quit()
sys.exit()
