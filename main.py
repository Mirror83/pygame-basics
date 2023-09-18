import pygame
from sys import exit

pygame.init()

WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("Runner")

test_surface = pygame.Surface(size=(100, 200))
test_surface.fill("Red")

clock = pygame.time.Clock()
MAX_FPS = 60

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Draw elements
    # Place test_surface on the screen
    screen.blit(test_surface, (200, 100))

    # Update screen
    pygame.display.update()

    # Ensure that the while loop runs at the framerate of MAX_FPS
    clock.tick(MAX_FPS)
