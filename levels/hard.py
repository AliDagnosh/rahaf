import pygame
import random
import os

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
get_font = os.path.join(root_dir, "../worm_simple_game/fonts", "game_font.ttf")
get_eat_sound = os.path.join(root_dir, "../worm_simple_game/sounds", "eat.wav")
get_apple_image = os.path.join(
    root_dir, "../worm_simple_game/images", "apple_3.png")
get_background_image = os.path.join(
    root_dir, "../worm_simple_game/images", "background_3.png")  # New background image

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20

pygame.font.init()
score_font = pygame.font.Font(get_font, 40)  # Custom font for the score
# Custom font for game over screen
game_over_font = pygame.font.Font(get_font, 50)
# Custom font for play again text
play_again_font = pygame.font.Font(get_font, 30)
score = 0

# Sound effects
pygame.mixer.init()
eating_sound = pygame.mixer.Sound(get_eat_sound)

# Initialize Pygame
pygame.init()

# Setting up display
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Load background image
background_image = pygame.image.load(get_background_image)
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Worm and food initialization
worm_pos = [[WIDTH // 2, HEIGHT // 2]]
worm_speed = [0, BLOCK_SIZE]


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
    apple_image, (BLOCK_SIZE * 2, BLOCK_SIZE * 2))  # Making the apple bigger


# Add obstacle initialization
obstacles = []


# Add a function to generate obstacles
def generate_obstacles():
    num_obstacles = 10  # You can adjust the number of obstacles as per your preference
    for _ in range(num_obstacles):
        while True:
            x = random.randint(0, (WIDTH - BLOCK_SIZE) //
                               BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (HEIGHT - BLOCK_SIZE) //
                               BLOCK_SIZE) * BLOCK_SIZE
            obstacle_pos = [x, y]
            # Ensure that the obstacle does not overlap with the worm or other obstacles
            if obstacle_pos not in worm_pos and obstacle_pos not in obstacles:
                obstacles.append(obstacle_pos)
                break


def draw_objects():
    # Draw background image
    win.blit(background_image, (0, 0))

    for pos in obstacles:
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(
            pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    for i, pos in enumerate(worm_pos):
        pygame.draw.rect(win, (189, 227, 79), pygame.Rect(
            pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        if i == 0:  # Draw eyes only for the first segment
            draw_worm_eyes(pos[0], pos[1])

    # Render the score text using custom font
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))  # draws the score on the top-left corner

    # Display the apple
    win.blit(
        apple_image, (food_pos[0] - BLOCK_SIZE // 2, food_pos[1] - BLOCK_SIZE // 2))


def draw_worm_eyes(x, y):
    # Calculate eye positions relative to the worm head
    eye1_x, eye1_y = x + 5, y + 5
    eye2_x, eye2_y = x + BLOCK_SIZE - 10, y + 5
    # Draw eyes
    pygame.draw.circle(win, (0, 0, 0), (eye1_x, eye1_y), 2)
    pygame.draw.circle(win, (0, 0, 0), (eye2_x, eye2_y), 2)


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

    game_over_text = game_over_font.render(
        f"Game Over! Score: {score}", True, (255, 255, 255))
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() //
             2, HEIGHT // 2 - game_over_text.get_height() // 2))

    play_again_text = play_again_font.render(
        "To play again, click 'R'", True, (255, 255, 255))
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
    obstacles = []  # Reset obstacles
    generate_obstacles()  # Generate new obstacles
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if worm_speed[1] != BLOCK_SIZE:
                        worm_speed = [0, -BLOCK_SIZE]  # Move up
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if worm_speed[1] != -BLOCK_SIZE:
                        worm_speed = [0, BLOCK_SIZE]  # Move down
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if worm_speed[0] != BLOCK_SIZE:
                        worm_speed = [-BLOCK_SIZE, 0]  # Move left
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if worm_speed[0] != -BLOCK_SIZE:
                        worm_speed = [BLOCK_SIZE, 0]  # Move right

        draw_objects()
        update_worm()
        if game_over():
            game_over_screen()
            break
        pygame.display.update()
        pygame.time.delay(50)  # Decreased delay for faster gameplay


if __name__ == '__main__':
    pygame.display.set_caption(
        'Worm Simple Game 2024 [Hard mode]')  # Changed the title
    run()
