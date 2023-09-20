import pygame
from sys import exit

pygame.init()

WIDTH = 800
HEIGHT = 400
GROUND_POSISTION = 300
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("Runner")

clock = pygame.time.Clock()
MAX_FPS = 60


text_color = (64, 64, 64) # In RGB
box_color = "#c0e8ec"
text_font = pygame.font.Font("assets/fonts/Pixeltype.ttf", 50)


# Convert images into a format that pygame can with easily
sky_surface = pygame.image.load("assets/graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("assets/graphics/ground.png").convert_alpha()

# Antialiasing has been set to False only because this is a pixel art game
# For other applications, antialiasing should be set to True
score_surface = text_font.render("My game", False, text_color)
score_rectangle = score_surface.get_rect(center=(WIDTH / 2, 50))

snail_surface = pygame.image.load("assets/graphics/snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom=(600, GROUND_POSISTION))
snail_speed = 4

player_surface = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(80, GROUND_POSISTION))
player_gravity = 0
has_collided = False

while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if player_rectangle.bottom >= GROUND_POSISTION:   
                    if player_rectangle.collidepoint(event.pos):
                        print("Clicked on player")
                        player_gravity = -20

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player_rectangle.bottom >= GROUND_POSISTION: 
                    player_gravity = -20
            
    # Draw elements
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, GROUND_POSISTION))

    pygame.draw.rect(screen, box_color, score_rectangle)
    screen.blit(score_surface, score_rectangle)

    # Snail animation
    snail_rectangle.x -= snail_speed
    if snail_rectangle.left < -100:
        snail_rectangle.left = WIDTH

    screen.blit(snail_surface, snail_rectangle)

    # Player gravity
    player_gravity += 1
    player_rectangle.y += player_gravity

    if player_rectangle.bottom >= GROUND_POSISTION:
        player_rectangle.bottom = GROUND_POSISTION

    screen.blit(player_surface, player_rectangle)

    if player_rectangle.colliderect(snail_rectangle) and has_collided == False:
        has_collided = True
        print("Collided")

    # Update screen
    pygame.display.update()

    # Ensure that the while loop runs at a maximum framerate of MAX_FPS
    clock.tick(MAX_FPS)
