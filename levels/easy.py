import pygame
import random
import os

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
get_font = os.path.join(root_dir, "../worm_simple_game/fonts", "game_font.ttf")
get_eat_sound = os.path.join(root_dir, "../worm_simple_game/sounds", "eat.wav")
get_apple_image = os.path.join(
    root_dir, "../worm_simple_game/images", "apple_1.png")
get_background_image = os.path.join(
    root_dir, "../worm_simple_game/images", "background.png")

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

pygame.font.init()
score_font = pygame.font.Font(get_font, 40)
# Updated font for game over screen
game_over_font = pygame.font.Font(get_font, 50)
# Updated font for play again text
play_again_font = pygame.font.Font(get_font, 30)
score = 0

# Color definition
BACKGROUND_COLOR = (160, 193, 212)
SNAKE_COLOR = (189, 227, 79)
EYE_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Sound effects
pygame.mixer.init()
eating_sound = pygame.mixer.Sound(get_eat_sound)

# Initialize Pygame
pygame.init()

# Setting up display
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Setting up clock
clock = pygame.time.Clock()

# Load the background image
background_image = pygame.image.load(get_background_image)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Snake and food initialization
snake_pos = [[WIDTH // 2, HEIGHT // 2]]
snake_speed = [0, BLOCK_SIZE]


def generate_food():
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_pos = [x, y]
        if food_pos not in snake_pos:
            return food_pos


food_pos = generate_food()
apple_image = pygame.image.load(get_apple_image)
apple_image = pygame.transform.scale(
    apple_image, (BLOCK_SIZE * 2, BLOCK_SIZE * 2))


def draw_objects():
    win.blit(background_image, (0, 0))

    for i, pos in enumerate(snake_pos):
        pygame.draw.rect(win, SNAKE_COLOR, pygame.Rect(
            pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        if i == 0:
            draw_snake_eyes(pos[0], pos[1])

    score_text = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    win.blit(score_text, (10, 10))

    win.blit(
        apple_image, (food_pos[0] - BLOCK_SIZE // 2, food_pos[1] - BLOCK_SIZE // 2))


def draw_snake_eyes(x, y):
    eye1_x, eye1_y = x + 5, y + 5
    eye2_x, eye2_y = x + BLOCK_SIZE - 10, y + 5
    pygame.draw.circle(win, EYE_COLOR, (eye1_x, eye1_y), 2)
    pygame.draw.circle(win, EYE_COLOR, (eye2_x, eye2_y), 2)


def update_snake():
    global food_pos, score, apple_image
    new_head = [snake_pos[0][0] + snake_speed[0],
                snake_pos[0][1] + snake_speed[1]]

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
        snake_pos.insert(0, new_head)
    else:
        snake_pos.pop()
        snake_pos.insert(0, new_head)


def game_over():
    return snake_pos[0] in snake_pos[1:] or \
        snake_pos[0][0] > WIDTH - BLOCK_SIZE or \
        snake_pos[0][0] < 0 or \
        snake_pos[0][1] > HEIGHT - BLOCK_SIZE or \
        snake_pos[0][1] < 0


def game_over_screen():
    global score
    win.blit(background_image, (0, 0))
    game_over_text = game_over_font.render(
        f"Game Over! Score: {score}", True, TEXT_COLOR)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() //
             2, HEIGHT // 2 - game_over_text.get_height() // 2))

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
    global snake_speed, snake_pos, food_pos, score
    snake_pos = [[WIDTH // 2, HEIGHT // 2]]
    snake_speed = [0, BLOCK_SIZE]
    food_pos = generate_food()
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if snake_speed[1] != BLOCK_SIZE:
                        snake_speed = [0, -BLOCK_SIZE]
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if snake_speed[1] != -BLOCK_SIZE:
                        snake_speed = [0, BLOCK_SIZE]
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if snake_speed[0] != BLOCK_SIZE:
                        snake_speed = [-BLOCK_SIZE, 0]
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if snake_speed[0] != -BLOCK_SIZE:
                        snake_speed = [BLOCK_SIZE, 0]

        draw_objects()
        update_snake()
        if game_over():
            game_over_screen()
            break
        pygame.display.update()
        clock.tick(9)
    pygame.quit()


if __name__ == '__main__':
    pygame.display.set_caption('Worm Simple Game 2024 [Easy mode]')
    run()
