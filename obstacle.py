from random import randint

import pygame
from obstacle_kind import ObstacleKind


class Obstacle(pygame.sprite.Sprite):
    MIN_START_X, MAX_START_X = 1000, 1400
    OBSTACLE_SPEED = 4

    def __init__(self, kind: ObstacleKind):
        super().__init__()
        self.frame_index = 0
        self.frame_list: list[pygame.Surface] = []

        match kind:
            case ObstacleKind.FLY:
                fly_frame_1 = pygame.image.load("assets/graphics/fly/fly_1.png").convert_alpha()
                fly_frame_2 = pygame.image.load("assets/graphics/fly/fly_2.png").convert_alpha()
                self.frame_list.append(fly_frame_1)
                self.frame_list.append(fly_frame_2)

            case ObstacleKind.SNAIL:
                snail_frame_1 = pygame.image.load("assets/graphics/snail/snail_1.png").convert_alpha()
                snail_frame_2 = pygame.image.load("assets/graphics/snail/snail_2.png").convert_alpha()
                self.frame_list.append(snail_frame_1)
                self.frame_list.append(snail_frame_2)

            case _:
                raise TypeError("kind must be of type ObstacleType")

        self.kind = kind
        self.image = self.frame_list[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(
                randint(Obstacle.MIN_START_X, Obstacle.MAX_START_X),
                kind.get_bottom_y()
            )
        )

    def move_obstacle(self):
        self.rect.x -= Obstacle.OBSTACLE_SPEED
        if self.rect.x < -100:
            self.kill()

    def update_animation_state(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frame_list):
            self.frame_index = 0
            self.image = self.frame_list[int(self.frame_index)]

    def update(self):
        self.update_animation_state()
        self.move_obstacle()
