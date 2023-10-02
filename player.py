import pygame


class Player(pygame.sprite.Sprite):
    GROUND_POSITION = 300
    START_POSITION = (80, GROUND_POSITION)

    def __init__(self) -> None:
        super().__init__()
        self.gravity = 0

        player_walk_1 = pygame.image.load("assets/graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("assets/graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk_list: list[pygame.Surface] = [player_walk_1, player_walk_2]
        self.player_walk_index = 0

        self.player_jump = pygame.image.load("assets/graphics/player/player_jump.png").convert_alpha()
        self.jump_sound = pygame.mixer.Sound("assets/audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

        self.image = self.player_walk_list[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom=Player.START_POSITION)

    def is_on_ground(self) -> bool:
        return self.rect.bottom >= Player.GROUND_POSITION

    def check_for_jump(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.is_on_ground():
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self) -> None:
        self.gravity += 1

        self.rect.y += self.gravity

        if self.is_on_ground():
            self.rect.bottom = Player.GROUND_POSITION

    def reset_position(self) -> None:
        self.rect.bottom = Player.GROUND_POSITION

    def update_animation_state(self) -> None:
        if self.is_on_ground():
            self.player_walk_index += 0.1
            if self.player_walk_index >= len(self.player_walk_list):
                self.player_walk_index = 0
            self.image = self.player_walk_list[int(self.player_walk_index)]
        else:
            self.image = self.player_jump

    def update(self) -> None:
        self.apply_gravity()
        self.check_for_jump()
        self.update_animation_state()
