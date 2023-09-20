import pygame
from sys import exit

pygame.init()

WIDTH = 800
HEIGHT = 400
GROUND_POSISTION = 300
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("Runner")

text_font = pygame.font.Font("assets/fonts/Pixeltype.ttf", 50)

clock = pygame.time.Clock()
MAX_FPS = 60

# Convert images into a format that pygame can with easily
sky_surface = pygame.image.load("assets/graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("assets/graphics/ground.png").convert_alpha()

# Antialiasing has been set to False only because this is a pixel art game
# For other applications, antialiasing should be set to True
text_surface = text_font.render("My game", False, "Black")

snail_surface = pygame.image.load("assets/graphics/snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom=(600, GROUND_POSISTION))
snail_speed = 2

player_surface = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
# Takes a surface and draws a rectangle around it
player_rectangle = player_surface.get_rect(midbottom=(80, GROUND_POSISTION))
has_collided = False

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            if player_rectangle.collidepoint(event.pos):
                print("Mouse over player")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rectangle.collidepoint(event.pos):
                print("Clicked on player")
            print(event)

    # Draw elements
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, HEIGHT - 100))
    screen.blit(text_surface, (WIDTH / 2 - text_surface.get_rect().width / 2, 20))
    if snail_rectangle.left < -100:
        snail_rectangle.left = WIDTH

    snail_rectangle.x -= snail_speed
    screen.blit(snail_surface, snail_rectangle)
    screen.blit(player_surface, player_rectangle)

    if player_rectangle.colliderect(snail_rectangle) and has_collided == False:
        has_collided = True
        print("Collided")

    # Update screen
    pygame.display.update()

    # Ensure that the while loop runs at a maximum framerate of MAX_FPS
    clock.tick(MAX_FPS)
