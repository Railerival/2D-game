#creation of simple game that works with display,movement and collision

import pygame
import pytmx
from sys import exit
from pathlib import Path
class Sprites:
    def __init__(self):
        self.ASSETS = Path('Assets')
        self.player_up = pygame.image.load(self.ASSETS / "player-up.png").convert_alpha()
        self.player_down = pygame.image.load(self.ASSETS / "player-down.png").convert_alpha()
        self.player_left = pygame.image.load(self.ASSETS / "player-left.png").convert_alpha()
        self.player_right = pygame.image.load(self.ASSETS / "player-right.png").convert_alpha()

class Game:
    """ A class for the game
        contains:
                -map blitter
                -keyboard event handler
                -game loop
    """

    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 60
        self.SCALE = 3
        self.TILE_SIZE = 48
        self.PLAYER_SPEED = 5
        self.current_map = "Assets/revised_ground_floor_map.tmx"
        self.camera_x = -150 # first map start coords
        self.camera_y = -1050 # first map start coords
        self.game_loop()

    def draw_map(self)-> None:
        """Function to draw the map"""
        tile_w = self.tmx_data.tilewidth * self.SCALE
        tile_h = self.tmx_data.tileheight * self.SCALE

        for layer in self.tmx_data.visible_layers:
           #added cache system
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    if gid == 0:
                        continue
                    if gid not in self.scaled_tiles:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            self.scaled_tiles[gid] = pygame.transform.scale(tile, (tile_w, tile_h))
                    if gid in self.scaled_tiles:
                        self.screen.blit(self.scaled_tiles[gid], (x * tile_w + self.player.camera_x, y * tile_h + self.player.camera_y))

    def handle_keys(self)-> None:
        """ Handles Key interactions, camera offsets and current player image"""
        key = pygame.key.get_pressed()
        if key[pygame.K_s] or key[pygame.K_DOWN]:

            self.camera_y -= self.game.PLAYER_SPEED 
            self.y += self.game.PLAYER_SPEED 
            self.player_img = self.player_surf_down

        if key[pygame.K_w] or key[pygame.K_UP]:

            self.camera_y += self.game.PLAYER_SPEED 
            self.y -= self.game.PLAYER_SPEED 
            self.player_img = self.player_surf_up

        if key[pygame.K_d] or key[pygame.K_RIGHT]:

            self.camera_x -= self.game.PLAYER_SPEED 
            self.x += self.game.PLAYER_SPEED 
            self.player_img = self.player_surf_right

        if key[pygame.K_a] or key[pygame.K_LEFT]:

            self.camera_x += self.game.PLAYER_SPEED 
            self.x -= self.game.PLAYER_SPEED
            self.player_img = self.player_surf_left

    def game_loop(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.handle_keys()

class Player:

    """A class for the player"""

    def __init__(self, game: Game):

        self.game = game

        # Player image loading,resizing,variable for current image and rect for player
        self.PLAYER_SIZE = 48
        self.player_up = pygame.image.load(os.path.join(ASSETS_DIR, "player-up.png")).convert_alpha()
        self.player_down = pygame.image.load(os.path.join(ASSETS_DIR, "player-down.png")).convert_alpha()
        self.player_left = pygame.image.load(os.path.join(ASSETS_DIR, "player-left.png")).convert_alpha()
        self.player_right = pygame.image.load(os.path.join(ASSETS_DIR, "player-right.png")).convert_alpha()
        self.player_surf_up = pygame.transform.scale(self.player_up, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_down = pygame.transform.scale(self.player_down, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_left = pygame.transform.scale(self.player_left, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_right = pygame.transform.scale(self.player_right, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_img = self.player_surf_down 
        self.player_rect = self.player_img.get_rect(center = (game.WIDTH // 2, game.HEIGHT // 2))

        # Camera coordinates for the village map(first map)
     
        self.x = 0
        self.y = 0
        self.hitbox = pygame.Rect(self.player_rect.x + 10,self.player_rect.y + 18,28,28)
         

    def draw(self)-> None:

        """ Draw on surface """

        self.game.screen.blit(self.player_img, self.player_rect)

    def collision(self)-> bool:

        """creates smaller hitbox for the player,checks if there is collision with the map rects and returns collision as a bool"""

        self.hitbox.topleft = (
            self.player_rect.x + 10,
            self.player_rect.y + 18
        )

        future_hitbox = self.hitbox.move(self.x, self.y)

        collision = False

        for rect in self.game.collision_rects:

            moved_rect = rect.move(self.camera_x, self.camera_y)

            if future_hitbox.colliderect(moved_rect):
                collision = True
                break
        return collision

if __name__ == "__main__":
    game = Game()
