import pygame
import random

pygame.init()

Width, Height = 800, 600
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Wack The Mole")

Mole_Radius = 40
Mole_color = (110, 39, 18)

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

score = 0
mole_timer = 0

def get_mole_duration(score):
    return max(1000 - score * 30, 300)

mole_duration = get_mole_duration(score)
mole_pos = (random.randint(100, Width - 100), random.randint(100, Height - 100))


def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action:
            return action
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)
    return None

def show_menu():
    menu_running = True
    while menu_running:
        screen.fill((50, 150, 200))
        title_text = font.render("Wack-The-Mole", True, (255, 255, 255))
        screen.blit(title_text, (Width // 2 - title_text.get_width() // 2, 100))

        if draw_button("Start", Width // 2 - 100, 250, 200, 60, (0, 128, 0), (0, 180, 0), "start") == "start":
            menu_running = False
        if draw_button("Exit", Width // 2 - 100, 350, 200, 60, (128, 0, 0), (180, 0, 0), "exit") == "exit":
            pygame.quit()
            exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(60)

show_menu()


running = True
while running:
    screen.fill((173, 216, 230))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            dx = mouse_pos[0] - mole_pos[0]
            dy = mouse_pos[1] - mole_pos[1]
            if dx * dx + dy * dy < Mole_Radius * Mole_Radius:
                score += 1
                mole_duration = get_mole_duration(score)
                mole_pos = (random.randint(100, Width - 100), random.randint(100, Height - 100))
                mole_timer = current_time

    if current_time - mole_timer > mole_duration:
        mole_pos = (random.randint(100, Width - 100), random.randint(100, Height - 100))
        mole_timer = current_time

    pygame.draw.circle(screen, Mole_color, mole_pos, Mole_Radius)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
