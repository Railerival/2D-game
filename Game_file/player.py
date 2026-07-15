import pygame 
from . import misc
from . import game_settings

class Player:#refactored
    """ Player class """

    PLAYER_SPEED = 5
    PLAYER_SIZE = 48

    #assets loading and transformation
    player_up = pygame.image.load(misc.Assets("Assets", "player-up.png").path_obj())
    player_down = pygame.image.load(misc.Assets("Assets", "player-down.png").path_obj())
    player_left = pygame.image.load(misc.Assets("Assets", "player-left.png").path_obj())
    player_right = pygame.image.load(misc.Assets("Assets", "player-right.png").path_obj())
    player_surf_up = pygame.transform.scale(player_up, (PLAYER_SIZE, PLAYER_SIZE))
    player_surf_down = pygame.transform.scale(player_down, (PLAYER_SIZE, PLAYER_SIZE))
    player_surf_left = pygame.transform.scale(player_left, (PLAYER_SIZE, PLAYER_SIZE))
    player_surf_right = pygame.transform.scale(player_right, (PLAYER_SIZE, PLAYER_SIZE))
    current_player_img = player_surf_down

    #player position control and hitbox rect
    player_rect = current_player_img.get_rect()
    player_rect.center = (game_settings.Game_settings.WINDOW_WIDTH/2, game_settings.Game_settings.WINDOW_HEIGHT/2)
    hitbox = pygame.Rect(player_rect.x + 10,player_rect.y + 18,28,28)
    
    def player_hitbox_move(self, del_x : int, del_y : int) -> None:
        """move the player hitbox"""
        self.hitbox = self.hitbox.move(del_x, del_y)
    
    def reset_hit_box(self, del_x : int, del_y : int) -> None:
        """resets the hitbox back to its place"""
        self.hitbox = self.hitbox.move(-del_x, -del_y)
