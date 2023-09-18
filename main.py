import pygame
from sys import exit

pygame.init()

WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("Runner")

text_font = pygame.font.Font("assets/fonts/Pixeltype.ttf", 50)

clock = pygame.time.Clock()
MAX_FPS = 60

sky_surface = pygame.image.load("assets/graphics/sky.png")
ground_surface = pygame.image.load("assets/graphics/ground.png")

# Antialiasing has been set to False only because this is a pixel art game
# For other applications, antialiasing should be set to True
text_surface = text_font.render("My game", False, "Black")

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Draw elements
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, HEIGHT - 100))
    screen.blit(text_surface, (WIDTH / 2 - text_surface.get_rect().width / 2, 20))

    # Update screen
    pygame.display.update()

    # Ensure that the while loop runs at a maximum framerate of MAX_FPS
    clock.tick(MAX_FPS)
