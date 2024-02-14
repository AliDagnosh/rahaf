import pygame
import os
import sys
import random

root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
button_click_sound = os.path.join(
    root_dir, "worm_simple_game/sounds", "button_click_sound.wav")
background_image_path = os.path.join(
    root_dir, "worm_simple_game/images", "background_start_game.png")
play_game_image = os.path.join(
    root_dir, "worm_simple_game/images", "play_game.png")
game_out_image = os.path.join(
    root_dir, "worm_simple_game/images", "game_out.png")
font = os.path.join(
    root_dir, "worm_simple_game/fonts", "game_font.ttf")

play = os.path.join(
    root_dir, "worm_simple_game/menu", "choose_level.py")


def open_game(level):
    os.system(level)


class Bubble:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.image = pygame.image.load(os.path.join(
            root_dir, "worm_simple_game/images", "bubble.png"))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.window_width)
        self.rect.y = random.randint(-100, 0)
        self.speed = random.randint(1, 2)  # Adjusted speed for slower movement

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.window_height:
            self.rect.y = random.randint(-100, 0)
            self.rect.x = random.randint(0, self.window_width)
            # Adjusted speed for slower movement
            self.speed = random.randint(1, 2)

    def draw(self, window):
        window.blit(self.image, self.rect)


# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
scale = "1:1"
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Worm Simple Game 2024")

# Load background image
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(
    background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Load custom font for the title
title_font = pygame.font.Font(font, 55)

# Load button images
button_easy = pygame.image.load(play_game_image)
button_game_out = pygame.image.load(game_out_image)

# Resize button images to match button dimensions
button_width = 250  # Increased button width
button_height = 100  # Increased button height
button_easy = pygame.transform.scale(
    button_easy, (button_width, button_height))
button_game_out = pygame.transform.scale(
    button_game_out, (button_width, button_height))

# Load sound for button click
button_click_sound = pygame.mixer.Sound(button_click_sound)

# Calculate positions to center the buttons vertically and horizontally
button_spacing = 20
total_button_height = button_height * 3 + button_spacing * 2
button_x = (WINDOW_WIDTH - button_width) // 2
button_y = (WINDOW_HEIGHT - total_button_height) // 2

# Create buttons for Easy and Game Out
easy_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
game_out_button_rect = pygame.Rect(
    button_x, button_y + button_height + button_spacing, button_width, button_height)

# Create a list to hold bubble objects
bubbles = []
for _ in range(5):  # Adjusted the number of bubbles
    bubbles.append(Bubble(WINDOW_WIDTH, WINDOW_HEIGHT))

# Game loop
running = True

# Load background music
pygame.mixer.music.load(os.path.join(
    root_dir, "worm_simple_game/sounds", "background.mp3"))
pygame.mixer.music.play(-1)  # Play music infinitely

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if easy_button_rect.collidepoint(mouse_pos):
                open_game(play)
                button_click_sound.play()
            elif game_out_button_rect.collidepoint(mouse_pos):
                pygame.quit()  # Close the window if the "Game Out" button is clicked
                sys.exit()

    # Clear the screen
    window.fill((0, 0, 0))

    # Draw background
    window.blit(background_image, (0, 0))

    # Draw bubbles
    for bubble in bubbles:
        bubble.update()
        bubble.draw(window)

    # Draw title
    title_text = title_font.render(
        "Worm Simple Game 2024", True, (255, 255, 255))
    title_rect = title_text.get_rect(
        center=(WINDOW_WIDTH // 2, 50))  # Adjusted the Y position
    window.blit(title_text, title_rect)

    # Draw buttons with hover effect
    if easy_button_rect.collidepoint(pygame.mouse.get_pos()):
        button_hover = pygame.transform.scale(
            button_easy, (270, 110))  # Scale up on hover
        # Adjust position on hover
        window.blit(button_hover, (button_x - 10, button_y - 5))
    else:
        window.blit(button_easy, easy_button_rect)

    if game_out_button_rect.collidepoint(pygame.mouse.get_pos()):
        button_hover = pygame.transform.scale(
            button_game_out, (270, 110))  # Scale up on hover
        # Adjust position on hover
        window.blit(button_hover, (button_x - 10,
                                   button_y + button_height + 15))
    else:
        window.blit(button_game_out, game_out_button_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame outside the game loop
pygame.quit()
sys.exit()
