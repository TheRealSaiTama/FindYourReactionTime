import pygame
import random
import time
import math


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Reaction Time Game")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)


font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 32)


circle_pos = None
start_time = None
clicks = 0
total_time = 0
max_clicks = 10


difficulties = {
    "Easy": {"radius": 40, "time_range": (1.0, 2.5)},
    "Medium": {"radius": 30, "time_range": (0.7, 2.0)},
    "Hard": {"radius": 20, "time_range": (0.5, 1.5)}
}
current_difficulty = "Medium"


particles = []


background_shapes = []
for _ in range(20):
    shape = {
        "pos": [random.randint(0, width), random.randint(0, height)],
        "size": random.randint(10, 50),
        "speed": random.uniform(0.5, 2),
        "angle": random.uniform(0, 2 * math.pi)
    }
    background_shapes.append(shape)

def create_particles(pos):
    for _ in range(20):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        size = random.randint(2, 5)
        lifetime = random.uniform(0.5, 1.5)
        particles.append({
            "pos": list(pos),
            "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
            "size": size,
            "lifetime": lifetime
        })

def update_particles(dt):
    for particle in particles[:]:
        particle["pos"][0] += particle["vel"][0]
        particle["pos"][1] += particle["vel"][1]
        particle["lifetime"] -= dt
        if particle["lifetime"] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        alpha = int(255 * (particle["lifetime"] / 1.5))
        color = (*RED[:3], alpha)
        pygame.draw.circle(screen, color, [int(particle["pos"][0]), int(particle["pos"][1])], particle["size"])

def update_background(dt):
    for shape in background_shapes:
        shape["pos"][0] += math.cos(shape["angle"]) * shape["speed"] * dt
        shape["pos"][1] += math.sin(shape["angle"]) * shape["speed"] * dt
        
        if shape["pos"][0] < -shape["size"]:
            shape["pos"][0] = width + shape["size"]
        elif shape["pos"][0] > width + shape["size"]:
            shape["pos"][0] = -shape["size"]
        
        if shape["pos"][1] < -shape["size"]:
            shape["pos"][1] = height + shape["size"]
        elif shape["pos"][1] > height + shape["size"]:
            shape["pos"][1] = -shape["size"]

def draw_background():
    screen.fill(LIGHT_BLUE)
    for shape in background_shapes:
        pygame.draw.circle(screen, WHITE, [int(shape["pos"][0]), int(shape["pos"][1])], shape["size"], 1)

def draw_circle():
    global circle_pos
    radius = difficulties[current_difficulty]["radius"]
    x = random.randint(radius, width - radius)
    y = random.randint(radius, height - radius)
    circle_pos = (x, y)
    pygame.draw.circle(screen, RED, circle_pos, radius)

def draw_start_screen():
    draw_background()
    title = font_large.render("Reaction Time Game", True, BLACK)
    difficulty_text = font_medium.render(f"Difficulty: {current_difficulty}", True, BLACK)
    start_text = font_medium.render("Click to start, Press E/M/H to change difficulty", True, BLACK)
    screen.blit(title, (width // 2 - title.get_width() // 2, height // 3))
    screen.blit(difficulty_text, (width // 2 - difficulty_text.get_width() // 2, height // 2))
    screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height * 2 // 3))

def draw_end_screen(avg_time):
    draw_background()
    title = font_large.render("Game Over", True, BLACK)
    result = font_medium.render(f"Average Time: {avg_time:.3f}s ({current_difficulty})", True, BLACK)
    restart_text = font_small.render("Click to play again, Press E/M/H to change difficulty", True, BLACK)
    screen.blit(title, (width // 2 - title.get_width() // 2, height // 3))
    screen.blit(result, (width // 2 - result.get_width() // 2, height // 2))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height * 2 // 3))

def game_loop():
    global circle_pos, start_time, clicks, total_time, current_difficulty

    running = True
    game_started = False
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60) / 1000.0  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    game_started = True
                    circle_pos = None
                    start_time = time.time()
                    clicks = 0
                    total_time = 0
                elif circle_pos:
                    mouse_pos = pygame.mouse.get_pos()
                    radius = difficulties[current_difficulty]["radius"]
                    if math.hypot(mouse_pos[0] - circle_pos[0], mouse_pos[1] - circle_pos[1]) <= radius:
                        total_time += time.time() - start_time
                        clicks += 1
                        create_particles(circle_pos)
                        circle_pos = None
                        if clicks >= max_clicks:
                            return True
                        start_time = time.time() + random.uniform(*difficulties[current_difficulty]["time_range"])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    current_difficulty = "Easy"
                elif event.key == pygame.K_m:
                    current_difficulty = "Medium"
                elif event.key == pygame.K_h:
                    current_difficulty = "Hard"

        update_background(dt)

        if not game_started:
            draw_start_screen()
        else:
            draw_background()
            update_particles(dt)
            draw_particles()
            if circle_pos:
                pygame.draw.circle(screen, RED, circle_pos, difficulties[current_difficulty]["radius"])
            elif start_time and time.time() > start_time:
                draw_circle()
                start_time = time.time()

       
            score_text = font_small.render(f"Clicks: {clicks}/{max_clicks} | Difficulty: {current_difficulty}", True, BLACK)
            screen.blit(score_text, (10, 10))

        pygame.display.flip()

    return False

def main():
    play_again = True
    while play_again:
        play_again = game_loop()
        if play_again:
            avg_time = total_time / max_clicks
            draw_end_screen(avg_time)
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play_again = False
                        waiting = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_e, pygame.K_m, pygame.K_h]:
                            if event.key == pygame.K_e:
                                current_difficulty = "Easy"
                            elif event.key == pygame.K_m:
                                current_difficulty = "Medium"
                            elif event.key == pygame.K_h:
                                current_difficulty = "Hard"
                            draw_end_screen(avg_time)
                            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()