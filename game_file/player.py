# game_file/player.py
import pygame
from . import misc

class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.speed = 5
        
        try:
            up_path = misc.Assets("Assets", "player-up.png").path_obj()
            self.player_surf_up = pygame.image.load(str(up_path)).convert_alpha()
            
            down_path = misc.Assets("Assets", "player-down.png").path_obj()
            self.player_surf_down = pygame.image.load(str(down_path)).convert_alpha()
            
            left_path = misc.Assets("Assets", "player-left.png").path_obj()
            self.player_surf_left = pygame.image.load(str(left_path)).convert_alpha()
            
            right_path = misc.Assets("Assets", "player-right.png").path_obj()
            self.player_surf_right = pygame.image.load(str(right_path)).convert_alpha()
            
        except FileNotFoundError as e:
            print("\n" + "="*60)
            print("CRITICAL ERROR: Player image not found!")
            exit(1)
        
        self.current_player_img = self.player_surf_down

    def get_draw_offset(self):
        """Return offset to center sprite on hitbox."""
        sprite_w = self.current_player_img.get_width()
        sprite_h = self.current_player_img.get_height()
        hitbox_w = self.rect.width
        hitbox_h = self.rect.height
        return ((sprite_w - hitbox_w) // 2, (sprite_h - hitbox_h) // 2)

    def move(self, dx: int, dy: int, collision_rects: list):
        self.rect.x += dx
        self._handle_collisions(collision_rects, 'x', dx)
        self.rect.y += dy
        self._handle_collisions(collision_rects, 'y', dy)

    def _handle_collisions(self, collision_rects: list, axis: str, delta: int):
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if axis == 'x':
                    if delta > 0:
                        self.rect.right = rect.left
                    elif delta < 0:
                        self.rect.left = rect.right
                elif axis == 'y':
                    if delta > 0:
                        self.rect.bottom = rect.top
                    elif delta < 0:
                        self.rect.top = rect.bottom