import pygame
from . import game_settings


class Entity:
    def __init__(
        self,
        entity_up_loc: str,
        entity_down_loc: str,
        entity_left_loc: str,
        entity_right_loc: str,
        entity_speed: int = 5,
        entity_size: int = 48,
    ):
        self.entity_speed = entity_speed
        self.entity_size = entity_size

        self.entity_up_img = pygame.image.load(game_settings.ASSETS / entity_up_loc)
        self.entity_down_img = pygame.image.load(game_settings.ASSETS / entity_down_loc)
        self.entity_left_img = pygame.image.load(game_settings.ASSETS / entity_left_loc)
        self.entity_right_img = pygame.image.load(
            game_settings.ASSETS / entity_right_loc
        )
        self.entity_surf_up = pygame.transform.scale(
            self.entity_up_img, (self.entity_size, self.entity_size)
        )
        self.entity_surf_down = pygame.transform.scale(
            self.entity_down_img, (self.entity_size, self.entity_size)
        )
        self.entity_surf_left = pygame.transform.scale(
            self.entity_left_img, (self.entity_size, self.entity_size)
        )
        self.entity_surf_right = pygame.transform.scale(
            self.entity_right_img, (self.entity_size, self.entity_size)
        )
        self.current_entity_img = self.entity_surf_down


class Player(Entity):
    def __init__(self):
        super().__init__(
            "player-up.png", "player-down.png", "player-left.png", "player-right.png"
        )
        self.player_rect = self.current_entity_img.get_rect()
        self.player_rect.center = (
            game_settings.WINDOW_WIDTH / 2,
            game_settings.WINDOW_HEIGHT / 2,
        )
        self.hitbox = pygame.Rect(
            game_settings.WINDOW_WIDTH // 2 - self.entity_size // 2 + 10,
            game_settings.WINDOW_HEIGHT // 2 - self.entity_size // 2 + 18,
            28,
            28,
        )

    def player_hitbox_move(self, del_x: int, del_y: int) -> None:
        """move the player hitbox"""
        self.hitbox = self.hitbox.move(del_x, del_y)

    def reset_hit_box(self, del_x: int, del_y: int) -> None:
        """resets the hitbox back to the middle of the screen"""
        self.player_hitbox_move(-del_x, -del_y)
