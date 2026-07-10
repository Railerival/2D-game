"""refactoring again with simple goal:creation of simple game that works with display,movement and collision
added comments during refactor
added dependancies..., added pathlib and all do uv sync in terminal to sync it."""

import pygame
import pytmx
from sys import exit
from pathlib import Path

class Sprites: #need to add a few more maps and all..
    def __init__(self):
        """All images,sprites,maps become attributes here"""
        self.ASSETS = Path('Assets')
        self.player_up = pygame.image.load(self.ASSETS / "player-up.png").convert_alpha()
        self.player_down = pygame.image.load(self.ASSETS / "player-down.png").convert_alpha()
        self.player_left = pygame.image.load(self.ASSETS / "player-left.png").convert_alpha()
        self.player_right = pygame.image.load(self.ASSETS / "player-right.png").convert_alpha()
        self.dungeon_ground_floor_map = self.ASSETS / "revised_ground_floor_map.tmx"
        self.village_map = ""

class Game(Sprites):
    """ A class for the game
        contains:
                -map blitter
                -keyboard event handler
                -game loop
    """

    def __init__(self): #checked but might have some issue
        player = Player()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 60
        self.SCALE = 3
        self.TILE_SIZE = 48
        self.PLAYER_SPEED = 5
        self.current_map = " "
        self.camera_x = -150 # first map start coords
        self.camera_y = -1050 # first map start coords
        self.x = 0
        self.y = 0
        self.collision_rects = []
        self.map_collision_rects()
        self.game_loop()

    def map_collision_rects(self)-> None: #definitely some issue here
        """function for creating collision rects of the map"""
        self.collision_rects = []
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision layer":
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(
                            x * self.tmx_data.tilewidth * self.SCALE,
                            y * self.tmx_data.tileheight * self.SCALE,
                            self.tmx_data.tilewidth * self.SCALE,
                            self.tmx_data.tileheight * self.SCALE
                        )
                        self.collision_rects.append(rect)

    def draw_map(self)-> None: #the issue in map_collision_rects is probably affected here too
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

    def handle_keys(self)-> None: #checked and refactored
        """ Handles Key interactions, camera offsets and current player image"""
        key = pygame.key.get_pressed()
        if key[pygame.K_s] or key[pygame.K_DOWN]:

            self.camera_y -= self.PLAYER_SPEED 
            self.y += self.PLAYER_SPEED 
            self.player_img = self.player.player_down 

        if key[pygame.K_w] or key[pygame.K_UP]:

            self.camera_y += self.PLAYER_SPEED 
            self.y -= self.PLAYER_SPEED 
            self.player_img = self.player_up

        if key[pygame.K_d] or key[pygame.K_RIGHT]:

            self.camera_x -= self.PLAYER_SPEED 
            self.x += self.PLAYER_SPEED 
            self.player_img = self.player_right

        if key[pygame.K_a] or key[pygame.K_LEFT]:

            self.camera_x += self.PLAYER_SPEED 
            self.x -= self.PLAYER_SPEED
            self.player_img = self.player_left
    
    def collision(self)-> bool:#looks like no issue but maybe linked to map_collision_rect issue

        """creates smaller hitbox for the player,checks if there is collision with the map rects and returns collision as a bool"""

        self.player.hitbox.topleft = (self.player.player_rect.x + 10, self.player.player_rect.y + 18)

        future_hitbox = self.hitbox.move(self.x, self.y)

        collision = False

        for rect in self.map_collision_rects:

            moved_rect = rect.move(self.camera_x, self.camera_y)

            if future_hitbox.colliderect(moved_rect):
                collision = True
                break
        return collision

    def game_loop(self): #this looks clean
        """Main game loop"""
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            old_camera_x = self.camera_x
            old_camera_y = self.camera_y

            self.handle_keys()
            collided = self.collision()

            if collided:
                self.player.camera_x = old_camera_x
                self.player.camera_y = old_camera_y

            self.draw_map() #To blit the tmx map
            self.player.draw() # To blit the player

class Player(Sprites):#look like this one is kinda safe and doesnt need much refactor need a final check with the other ones.

    """A class for the player"""

    def __init__(self):

        self.PLAYER_SIZE = 48
        self.player_surf_up = pygame.transform.scale(self.player_up, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_down = pygame.transform.scale(self.player_down, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_left = pygame.transform.scale(self.player_left, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_right = pygame.transform.scale(self.player_right, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_img_current = self.player_down 
        self.player_rect = self.player_img.get_rect(center = (game.WIDTH // 2, game.HEIGHT // 2))   
        self.hitbox = pygame.Rect(self.player_rect.x + 10, self.player_rect.y + 18,28,28)
         
    def draw(self)-> None:
        """ Draw on surface """
        self.game.screen.blit(self.player_img_current, self.player_rect)


if __name__ == "__main__":
    game = Game()
