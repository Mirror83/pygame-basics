import pygame
from sys import exit
from random import randint

pygame.init()

WIDTH = 800
HEIGHT = 400
GROUND_POSITION = 300
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Runner")

clock = pygame.time.Clock()
MAX_FPS = 60

text_color = (64, 64, 64) # In RGB
box_color = "#c0e8ec"
text_font = pygame.font.Font("assets/fonts/Pixeltype.ttf", 50)

# Convert images into a format that pygame can with easily
sky_surface = pygame.image.load("assets/graphics/sky.png").convert_alpha()
ground_surface = pygame.image.load("assets/graphics/ground.png").convert_alpha()

SCORE_POSITION = (WIDTH / 2, 50)

obstacle_rectangle_list: list[pygame.Rect] = []
snail_surface = pygame.image.load("assets/graphics/snail/snail_1.png").convert_alpha()
SNAIL_START_POSITION = (WIDTH, GROUND_POSITION)

fly_surface = pygame.image.load("assets/graphics/fly/fly_1.png").convert_alpha()
FLY_Y_BOTTOM = GROUND_POSITION - 100
obstacle_speed = 4

player_surface = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
PLAYER_START_POSITION = (80, GROUND_POSITION)
player_rectangle = player_surface.get_rect(midbottom=PLAYER_START_POSITION)
# player_collision_rect = pygame.Rect(player_rectangle.left, player_rectangle.top, player_rectangle.width, player_rectangle.width)
player_gravity = 0

# Title screen surfaces
TITLE_POSITION = (WIDTH / 2, 70)
TITLE_SCREEN_BG = (94, 129, 162)
title_surface = text_font.render("Pixel Runner", False, text_color)
title_rectangle = title_surface.get_rect(center=TITLE_POSITION)

title_player_surface = pygame.image.load("assets/graphics/player/player_stand.png").convert_alpha()
title_player_surface = pygame.transform.rotozoom(title_player_surface, 0, 2)
title_player_rectangle = title_player_surface.get_rect(center=screen.get_rect().center)

instruction_surface = text_font.render("Press ENTER to play", False, text_color)
instruction_rectangle = instruction_surface.get_rect(center=(WIDTH / 2, HEIGHT - 50))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)


game_active = False
start_time = 0
score = 0


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    # Antialiasing has been set to False only because this is a pixel art game
    # For other applications, antialiasing should be set to True
    score = current_time // 1000
    score_surface = text_font.render(f"Score: {score}", False, text_color)
    score_rectangle = score_surface.get_rect(center=SCORE_POSITION)
    pygame.draw.rect(screen, box_color, score_rectangle)
    screen.blit(score_surface, score_rectangle)

    return score

def move_obstacles(obstacle_rectangle_list: list[pygame.Rect]):
    global game_active
    if len(obstacle_rectangle_list) > 0:
        for obstacle_rectangle in obstacle_rectangle_list:
            obstacle_rectangle.x -= obstacle_speed

            if (obstacle_rectangle.bottom == FLY_Y_BOTTOM):
                screen.blit(fly_surface, obstacle_rectangle)

                if obstacle_rectangle.collidepoint(player_rectangle.midtop):
                # if obstacle_rectangle.colliderect(player_rectangle):
                    game_active = False
            else:
                screen.blit(snail_surface, obstacle_rectangle)
                
                if obstacle_rectangle.collidepoint(player_rectangle.midbottom[0], player_rectangle.midbottom[1] - 10):
                # if obstacle_rectangle.colliderect(player_rectangle):
                    game_active = False

            obstacle_rectangle_list = [obstacle_rectangle \
                                       for obstacle_rectangle in obstacle_rectangle_list \
                                        if obstacle_rectangle.x > -100
                ]
            
    return obstacle_rectangle_list



while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if player_rectangle.bottom >= GROUND_POSITION:   
                        if player_rectangle.collidepoint(event.pos):
                            print("Clicked on player")
                            player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rectangle.bottom >= GROUND_POSITION: 
                        player_gravity = -20

            if event.type == obstacle_timer:
                if (randint(0, 4) == 0):
                    obstacle_rectangle = fly_surface.get_rect(bottomright=(randint(1000, 1400), FLY_Y_BOTTOM))
                else:
                    obstacle_rectangle = snail_surface.get_rect(bottomright=(randint(1000, 1400), GROUND_POSITION))
                obstacle_rectangle_list.append(obstacle_rectangle)
                
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_rectangle.midbottom = PLAYER_START_POSITION
                    obstacle_rectangle_list.clear()
                    start_time = pygame.time.get_ticks()
                    game_active = True

    # Game logic        
    if game_active:
        if score > 0 and score % 10 == 0 :
            obstacle_speed += 0.01
        # Draw elements
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, GROUND_POSITION))

        score = display_score()

        # Player gravity
        player_gravity += 1
        player_rectangle.y += player_gravity

        if player_rectangle.bottom >= GROUND_POSITION:
            player_rectangle.bottom = GROUND_POSITION

        screen.blit(player_surface, player_rectangle)

        obstacle_rectangle_list = move_obstacles(obstacle_rectangle_list)

    else:
        if start_time > 0:
            pygame.time.wait(1200)

        screen.fill(TITLE_SCREEN_BG)
        screen.blit(title_surface, title_rectangle)

        if start_time > 0:
            score_surface = text_font.render(f"Score: {score}", False, text_color)
            score_rectangle = score_surface.get_rect(center=(WIDTH / 2, HEIGHT - 70))
            screen.blit(score_surface, score_rectangle)
        else:
            screen.blit(instruction_surface, instruction_rectangle)

        screen.blit(title_player_surface, title_player_rectangle)

    # Update screen
    pygame.display.update()

    # Ensure that the while loop runs at a maximum framerate of MAX_FPS
    clock.tick(MAX_FPS)

