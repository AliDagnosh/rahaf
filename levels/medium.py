import pygame
import random
import os

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
get_font = os.path.join(root_dir, "../worm_simple_game/fonts", "game_font.ttf")
get_eat_sound = os.path.join(root_dir, "../worm_simple_game/sounds", "eat.wav")
get_apple_image = os.path.join(
    root_dir, "../worm_simple_game/images", "apple_2.png")
get_background_image = os.path.join(
    root_dir, "../worm_simple_game/images", "background_2.png")

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

pygame.font.init()
score_font = pygame.font.Font(get_font, 40)
score = 0

# Color definition
BACKGROUND_COLOR = (160, 193, 212)  # Hex: A0C1D4
WORM_COLOR = (189, 227, 79)  # BDE34F
EYE_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (255, 0, 0)  # Red color

# Sound effects
pygame.mixer.init()
eating_sound = pygame.mixer.Sound(get_eat_sound)

# Initialize Pygame
pygame.init()

# Setting up display
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Setting up clock
clock = pygame.time.Clock()

# Worm and food initialization
worm_pos = [[WIDTH // 2, HEIGHT // 2]]
worm_speed = [0, BLOCK_SIZE]

# Load background image
background_image = pygame.image.load(get_background_image)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


def generate_food():
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_pos = [x, y]
        if food_pos not in worm_pos:
            return food_pos


food_pos = generate_food()
apple_image = pygame.image.load(get_apple_image)
apple_image = pygame.transform.scale(
    apple_image, (BLOCK_SIZE * 2, BLOCK_SIZE * 2))


# Function to generate obstacles
def generate_obstacles():
    num_obstacles = 5  # Adjust the number of obstacles
    obstacles = []
    for _ in range(num_obstacles):
        while True:
            x = random.randint(0, (WIDTH - BLOCK_SIZE) //
                               BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (HEIGHT - BLOCK_SIZE) //
                               BLOCK_SIZE) * BLOCK_SIZE
            obstacle_pos = [x, y]
            if obstacle_pos not in worm_pos and obstacle_pos != food_pos and obstacle_pos not in obstacles:
                obstacles.append(obstacle_pos)
                break
    return obstacles


obstacles = generate_obstacles()


def draw_objects():
    # Draw background image
    win.blit(background_image, (0, 0))

    # Draw obstacles in specified color
    for pos in obstacles:
        pygame.draw.rect(win, OBSTACLE_COLOR, pygame.Rect(
            pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw worm
    for i, pos in enumerate(worm_pos):
        pygame.draw.rect(win, WORM_COLOR, pygame.Rect(
            pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        if i == 0:
            draw_worm_eyes(pos[0], pos[1])

    # Render the score text using custom font
    score_text = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    win.blit(score_text, (10, 10))

    # Display the apple
    win.blit(
        apple_image, (food_pos[0] - BLOCK_SIZE // 2, food_pos[1] - BLOCK_SIZE // 2))


def draw_worm_eyes(x, y):
    eye1_x, eye1_y = x + 5, y + 5
    eye2_x, eye2_y = x + BLOCK_SIZE - 10, y + 5
    pygame.draw.circle(win, EYE_COLOR, (eye1_x, eye1_y), 2)
    pygame.draw.circle(win, EYE_COLOR, (eye2_x, eye2_y), 2)


def update_worm():
    global food_pos, score, apple_image
    new_head = [worm_pos[0][0] + worm_speed[0],
                worm_pos[0][1] + worm_speed[1]]

    if new_head[0] >= WIDTH:
        new_head[0] = 0
    elif new_head[0] < 0:
        new_head[0] = WIDTH - BLOCK_SIZE
    if new_head[1] >= HEIGHT:
        new_head[1] = 0
    elif new_head[1] < 0:
        new_head[1] = HEIGHT - BLOCK_SIZE

    if new_head == food_pos:
        food_pos = generate_food()
        score += 1
        eating_sound.play()
        for _ in range(5):
            apple_image.set_alpha(0)
            draw_objects()
            pygame.display.update()
            pygame.time.delay(100)
            apple_image.set_alpha(255)
            draw_objects()
            pygame.display.update()
            pygame.time.delay(100)
        worm_pos.insert(0, new_head)
    else:
        worm_pos.pop()
        worm_pos.insert(0, new_head)


def game_over():
    return worm_pos[0] in worm_pos[1:] or \
        worm_pos[0][0] > WIDTH - BLOCK_SIZE or \
        worm_pos[0][0] < 0 or \
        worm_pos[0][1] > HEIGHT - BLOCK_SIZE or \
        worm_pos[0][1] < 0 or \
        worm_pos[0] in obstacles


def game_over_screen():
    global score
    # Draw the same background image as the playing screen
    win.blit(background_image, (0, 0))

    game_over_font = pygame.font.Font(get_font, 50)
    game_over_text = game_over_font.render(
        f"Game Over! Score: {score}", True, TEXT_COLOR)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() //
             2, HEIGHT // 2 - game_over_text.get_height() // 2))

    play_again_font = pygame.font.Font(get_font, 30)
    play_again_text = play_again_font.render(
        "To play again, click 'R'", True, TEXT_COLOR)
    win.blit(play_again_text, (WIDTH // 2 -
             play_again_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return


def run():
    global worm_speed, worm_pos, food_pos, score, obstacles
    worm_pos = [[WIDTH // 2, HEIGHT // 2]]
    worm_speed = [0, BLOCK_SIZE]
    food_pos = generate_food()
    score = 0
    obstacles = generate_obstacles()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if worm_speed[1] != BLOCK_SIZE:
                        worm_speed = [0, -BLOCK_SIZE]
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if worm_speed[1] != -BLOCK_SIZE:
                        worm_speed = [0, BLOCK_SIZE]
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if worm_speed[0] != BLOCK_SIZE:
                        worm_speed = [-BLOCK_SIZE, 0]
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if worm_speed[0] != -BLOCK_SIZE:
                        worm_speed = [BLOCK_SIZE, 0]

        draw_objects()
        update_worm()
        if game_over():
            game_over_screen()
            break
        pygame.display.update()
        clock.tick(10)  # Increased the clock tick rate by one unit
    pygame.quit()


if __name__ == '__main__':
    pygame.display.set_caption('Worm Simple Game 2024 [Medium mode]')
    run()
