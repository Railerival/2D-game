"""
This is just an old file i made not deleting it yet
"""

import pygame
import pytmx
from pathlib import Path

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
WINDOW_SIZE = (WINDOW_WIDTH, 400)
FPS = 60
SCALE = 3
DISPLAY_SURF = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Panacea")
clock = pygame.time.Clock()
ASSETS = Path("Assets")

class Game:
    def __init__(self):
        self.PLAYER_SPEED = 3
        self.PLAYER_SIZE = self.TILE_SIZE = 48
        self.current_map = "Villlage.tmx"
        self.player_up = pygame.image.load(ASSETS / "player-up.png")
        self.player_down = pygame.image.load(ASSETS / "player-down.png")
        self.player_left = pygame.image.load(ASSETS / "player-left.png")
        self.player_right = pygame.image.load(ASSETS / "player-right.png")
        self.player_surf_up = pygame.transform.scale(self.player_up, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_down = pygame.transform.scale(self.player_down, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_left = pygame.transform.scale(self.player_left, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_right = pygame.transform.scale(self.player_right, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_img = self.player_surf_down
        self.player_rect = self.player_img.get_rect()
        self.player_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.hitbox = pygame.Rect(self.player_rect.x + 10,self.player_rect.y + 18,28,28)
        self.tmx_data = pytmx.util_pygame.load_pygame(ASSETS / self.current_map)
        self.camera_x = -200
        self.camera_y = -1300
        self.collision_rects = []
        self.check = 0
        
    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.camera_y -= self.PLAYER_SPEED 
            self.player_img = self.player_surf_down
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.camera_y += self.PLAYER_SPEED 
            self.player_img = self.player_surf_up
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.camera_x -= self.PLAYER_SPEED 
            self.player_img = self.player_surf_right
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.camera_x += self.PLAYER_SPEED 
            self.player_img = self.player_surf_left

    def draw_map(self):
        """Just a function to keep the code DRY"""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (self.tmx_data.tilewidth * SCALE, self.tmx_data.tileheight * SCALE))
                        DISPLAY_SURF.blit(tile, (x * self.tmx_data.tilewidth * SCALE + self.camera_x, y * self.tmx_data.tileheight * SCALE + self.camera_y))

    def map_rect(self):
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision layer":
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(x * self.tmx_data.tilewidth * SCALE + self.camera_x, y * self.tmx_data.tileheight * SCALE + self.camera_y, self.tmx_data.tilewidth * SCALE, self.tmx_data.tileheight * SCALE)
                        self.collision_rects.append(rect)

    def main(self): 
        """Main loop"""
        self.map_rect()
        while True: # main game loop
            print(self.collision_rects[142])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            old_camera_x = self.camera_x
            old_camera_y = self.camera_y
            self.handle_keys()
            self.check = self.player_rect.collidelist(self.collision_rects)
            if self.check != -1:
                #not collide
                self.camera_x = old_camera_x
                self.camera_y = old_camera_y
            elif self.check == -1:
                #collide
                for index, rect in enumerate(self.collision_rects):
                    new_rect = rect.move(self.camera_x-old_camera_x, self.camera_y-old_camera_y)
                    self.collision_rects[index] = new_rect
            self.draw_map()
            DISPLAY_SURF.blit(self.player_img,self.player_rect)
            pygame.display.update()
            clock.tick(FPS)



game = Game()
game.main()