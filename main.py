import pygame
from sys import exit
from random import randint

from obstacle import Obstacle
from obstacle_kind import ObstacleKind
from player import Player

pygame.init()

WIDTH = 800
HEIGHT = 400
GROUND_POSITION = 300
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Runner")

clock = pygame.time.Clock()
MAX_FPS = 60

TEXT_COLOUR = (64, 64, 64)  # In RGB
BOX_COLOUR = "#c0e8ec"
text_font = pygame.font.Font("assets/fonts/Pixeltype.ttf", 50)

# Convert images into a format that pygame can with easily
sky_surface = pygame.image.load("assets/graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("assets/graphics/ground.png").convert_alpha()

SCORE_POSITION = (WIDTH / 2, 50)

# Title screen surfaces
TITLE_POSITION = (WIDTH / 2, 70)
TITLE_SCREEN_BG = (94, 129, 162)
title_surface = text_font.render("Pixel Runner", False, TEXT_COLOUR)
title_rectangle = title_surface.get_rect(center=TITLE_POSITION)

title_player_surface = pygame.image.load("assets/graphics/player/player_stand.png").convert_alpha()
title_player_surface = pygame.transform.rotozoom(title_player_surface, 0, 2)
title_player_rectangle = title_player_surface.get_rect(center=screen.get_rect().center)

instruction_surface = text_font.render("Press ENTER to play", False, TEXT_COLOUR)
instruction_rectangle = instruction_surface.get_rect(center=(WIDTH / 2, HEIGHT - 50))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

game_active = False
start_time = 0
score = 0

player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

obstacle_group = pygame.sprite.Group()


def display_score():
    global score_surface, score_rectangle, score
    current_time = pygame.time.get_ticks() - start_time
    # Antialiasing has been set to False only because this is a pixel art game
    # For other applications, antialiasing should be set to True
    score = current_time // 1000
    score_surface = text_font.render(f"Score: {score}", False, TEXT_COLOUR)
    score_rectangle = score_surface.get_rect(center=SCORE_POSITION)
    pygame.draw.rect(screen, BOX_COLOUR, score_rectangle)
    screen.blit(score_surface, score_rectangle)


def has_collided() -> bool:
    global player_group, obstacle_group
    sprite_list = pygame.sprite.spritecollide(player_group.sprite, obstacle_group, False)

    collided = len(sprite_list) > 0

    if collided:
        obstacle_group.empty()

    return collided


while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 4) == 0:
                    obstacle_group.add(Obstacle(ObstacleKind.FLY))
                else:
                    obstacle_group.add(Obstacle(ObstacleKind.SNAIL))

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # player_rectangle.midbottom = PLAYER_START_POSITION
                    # obstacle_rectangle_list.clear()
                    start_time = pygame.time.get_ticks()
                    game_active = True

    # Game logic        
    if game_active:
        if score > 0 and score % 20 == 0:
            Obstacle.OBSTACLE_SPEED += 0.01

        # Draw elements
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, GROUND_POSITION))

        display_score()

        player_group.draw(screen)
        player_group.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = not has_collided()

    else:
        if start_time > 0:
            pygame.time.wait(1200)

        screen.fill(TITLE_SCREEN_BG)
        screen.blit(title_surface, title_rectangle)

        if start_time > 0:
            score_surface = text_font.render(f"Score: {score}", False, TEXT_COLOUR)
            score_rectangle = score_surface.get_rect(center=(WIDTH / 2, HEIGHT - 70))
            screen.blit(score_surface, score_rectangle)
        else:
            screen.blit(instruction_surface, instruction_rectangle)

        screen.blit(title_player_surface, title_player_rectangle)

    # Update screen
    pygame.display.update()

    # Ensure that the while loop runs at a maximum frame rate of MAX_FPS
    clock.tick(MAX_FPS)
