import pygame
import sys
import numpy as np
from databaseSetup import setup_database_and_execute_scripts
from colors import *

# Function to run the start menu
def run_start_menu():
    # Initialize Pygame
#    pygame.init()

    # Screen settings
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Trivial Compute")

    # Load background image
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Fonts
    font = pygame.font.Font(None, 40)

    # Button class
    class Button:
        def __init__(self, text, x, y, width, height, color, action=None):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color
            self.action = action
            self.highlighted_color = [min(255, c + 30) for c in color]
            self.shadow_color = [max(0, c - 30) for c in color]

        def draw(self, screen):
            # Draw shadow
            shadow_rect = self.rect.copy()
            shadow_rect.topleft = (self.rect.x + 2, self.rect.y + 2)
            pygame.draw.rect(screen, self.shadow_color, shadow_rect)

            # Draw main button
            pygame.draw.rect(screen, self.highlighted_color, self.rect)
            pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4))

            # Draw text
            text_surf = font.render(self.text, True, black)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        def check_click(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        return self.action()
            return None

    # Button actions
    def start_game():
        print("Start Game button clicked")
        return "start"

    def exit_game():
        print("Exit Game button clicked")
        return "exit"

    def setup_database():
        print("Database Setup button clicked")
        setup_database_and_execute_scripts()


    # Create buttons
    setup_database_button = Button("Setup Database", 850, 100, 300, 100, blue, setup_database)
    start_button = Button("Start Game", 850, 300, 300, 100, green, start_game)
    exit_button = Button("Exit Game", 850, 500, 300, 100, red, exit_game)


    buttons = [setup_database_button, start_button, exit_button]

    # Main loop
    running = True
    while running:
        # Draw background image
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            for button in buttons:
                result = button.check_click(event)
                if result is not None:
                    return result

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    return "exit"