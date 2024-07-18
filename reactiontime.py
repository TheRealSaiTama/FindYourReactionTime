import pygame
import time
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (240, 240, 240)
TEXT_COLOR = (50, 50, 50)
BUTTON_COLOR = (0, 150, 136)
BUTTON_HOVER_COLOR = (0, 137, 123)
COUNTDOWN_COLOR = (233, 30, 99)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elegant Reaction Time Test")

# Fonts
title_font = pygame.font.Font(None, 64)
button_font = pygame.font.Font(None, 36)
result_font = pygame.font.Font(None, 48)
countdown_font = pygame.font.Font(None, 150)

clock = pygame.time.Clock()

def draw_text(text, font, color, x, y, centered=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    text_surf = button_font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)

def countdown():
    start_time = time.time()
    countdown_time = 3
    while countdown_time > 0:
        screen.fill(BACKGROUND_COLOR)
        
        # Draw pulsating circle
        circle_radius = 100 + math.sin(time.time() * 5) * 10
        pygame.draw.circle(screen, COUNTDOWN_COLOR, (WIDTH // 2, HEIGHT // 2), int(circle_radius))
        
        draw_text(str(math.ceil(countdown_time)), countdown_font, (255, 255, 255), WIDTH // 2, HEIGHT // 2)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        pygame.display.flip()
        countdown_time -= 1 / 60
        clock.tick(60)

    screen.fill(COUNTDOWN_COLOR)
    draw_text("CLICK!", countdown_font, (255, 255, 255), WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Reaction time: {time.time() - start_time - 3}")
                return

        clock.tick(60)

def main():
    reaction_time = None
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        draw_text("Reaction Time Test", title_font, TEXT_COLOR, WIDTH // 2, 50)

        if reaction_time is None:
            draw_text("Test your reaction time!", result_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 50)
            draw_button("Start Test", WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: globals().update(reaction_time=countdown()))
        else:
            draw_text(f"Your reaction time: {reaction_time:.3f} seconds", result_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 - 50)
            draw_button("Try Again", WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda: globals().update(reaction_time=None))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()