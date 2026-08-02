import pygame 
from . import game_settings

class Player:#checked 
    """ Player class """

    PLAYER_SPEED = 5
    PLAYER_SIZE = 48

    #assets loading and transformation
    player_up = pygame.image.load(game_settings.ASSETS / "player-up.png")
    player_down = pygame.image.load(game_settings.ASSETS / "player-down.png")
    player_left = pygame.image.load(game_settings.ASSETS / "player-left.png")
    player_right = pygame.image.load(game_settings.ASSETS / "player-right.png")
    player_surf_up = pygame.transform.scale(player_up, (PLAYER_SIZE, PLAYER_SIZE))
    player_surf_down = pygame.transform.scale(player_down, (PLAYER_SIZE, PLAYER_SIZE))
    player_surf_left = pygame.transform.scale(player_left, (PLAYER_SIZE, PLAYER_SIZE))
    player_surf_right = pygame.transform.scale(player_right, (PLAYER_SIZE, PLAYER_SIZE))
    current_player_img = player_surf_down

    #player position control and hitbox rect
    player_rect = current_player_img.get_rect()
    player_rect.center = (game_settings.WINDOW_WIDTH/2, game_settings.WINDOW_HEIGHT/2)
    hitbox = pygame.Rect(game_settings.WINDOW_WIDTH // 2 - PLAYER_SIZE // 2 + 10, game_settings.WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2 + 18, 28, 28)
    hitbox_centered = hitbox.copy()
    
    def player_hitbox_move(self, del_x : int, del_y : int) -> None:
        """move the player hitbox"""
        self.hitbox = self.hitbox.move(del_x, del_y)
    
    def reset_hit_box(self, del_x : int, del_y : int) -> None:
        """resets the hitbox back to the middle of the screen"""
        self.player_hitbox_move(-del_x, -del_y)
        

                            
