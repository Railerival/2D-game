# game_file/player.py
import pygame
from . import misc

class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 32, 32) # Adjust width/height to match your art
        self.speed = 5
        
        try:
            # Use YOUR robust Assets class to get absolute paths
            # Updated to match YOUR actual file structure
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
            print(f"Pygame looked for the file at this EXACT location:\n➡️  {e.filename}")
            print("\nPlease check:")
            print("1. Do the files have .png extensions? (Check in Tiled or Properties)")
            print("2. Are the files named exactly: player-up, player-down, player-left, player-right?")
            print("3. Are the files in the Assets folder (not in a subfolder)?")
            print("="*60 + "\n")
            pygame.quit()
            exit(1)
        
        self.current_player_img = self.player_surf_down

    def move(self, dx: int, dy: int, collision_rects: list):
        """Moves the player and handles collisions robustly by separating X and Y."""
        # 1. Move and check X axis
        self.rect.x += dx
        self._handle_collisions(collision_rects, 'x', dx)

        # 2. Move and check Y axis
        self.rect.y += dy
        self._handle_collisions(collision_rects, 'y', dy)

    def _handle_collisions(self, collision_rects: list, axis: str, delta: int):
        """Resolves collisions by pushing the player out of the wall (enables wall sliding)."""
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if axis == 'x':
                    if delta > 0: # Moving right
                        self.rect.right = rect.left
                    elif delta < 0: # Moving left
                        self.rect.left = rect.right
                        
                elif axis == 'y':
                    if delta > 0: # Moving down
                        self.rect.bottom = rect.top
                    elif delta < 0: # Moving up
                        self.rect.top = rect.bottom