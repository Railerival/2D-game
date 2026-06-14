#----------------------------------------------UNDER DEVELOPMENT----------------------------------------------
#This is the main code.
#Dungeon = D, Floor = F

import pygame
import pytmx
import os
from sys import exit


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "Assets")

pygame.init()
class Game:

    """General Game class for the game"""

    def __init__(self):

        # Settings
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 60
        self.SCALE = 3
        #MASTER FILE PATH
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "Assets")
        self.current_map = os.path.join(ASSETS_DIR, "Village.tmx")
        
        self.TILE_SIZE = 48
        self.PLAYER_SPEED = 8

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Panacea")
        self.tmx_data = pytmx.load_pygame(self.current_map)
        self.player = Player(self)
        self.collision_rects = []
        self.door_rects = []
        self.scaled_tiles = {}
        self.collision()
        self.door()

    def Door_event(self)-> bool:

        """function for event of using a door
        returns 1 if the event happens"""

        EVENT = False
        for door in self.door_rects:
            moved_rect = door["rect"].move(self.player.camera_x, self.player.camera_y)

            if self.player.hitbox.colliderect(moved_rect):
                print("check")
                self.current_map = door["target"]
                print(self.current_map)

                self.player.camera_x = door["spawn_x"]
                self.player.camera_y = door["spawn_y"]
                EVENT = True

                self.scaled_tiles = {}

        return EVENT

    def collision(self)-> None:

        """function for creating collision rects"""

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

    def door(self)-> None:

        """function to make list with door rects, target map of the door, and spawn points of the new map"""

        self.door_rects = []
        
        # 🚨 SAFE LOOP: Only looks for the Door Layer if it exists!
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Door Layer":
                
                for obj in layer:
                    door_rect = pygame.Rect(
                    int(obj.x * self.SCALE),
                    int(obj.y * self.SCALE),
                    int(obj.width * self.SCALE),
                    int(obj.height * self.SCALE)
                    )
                    target_map = obj.properties["target"]

                    if target_map.startswith("Assets/"):
                        target_map = target_map.replace("Assets/", "")

                    if not target_map.endswith(".tmx"):
                        target_map += ".tmx"

                    target_map = os.path.join(ASSETS_DIR, target_map)

                    spawn_x = obj.properties["spawn_x"]
                    spawn_y = obj.properties["spawn_y"]

                    self.door_rects.append({
                        "rect": door_rect,
                        "target": target_map,
                        "spawn_x": spawn_x,
                        "spawn_y" : spawn_y
                    })
    
    def draw_map(self)-> None:

        """Function to draw the map"""
        tile_w = self.tmx_data.tilewidth * self.SCALE
        tile_h = self.tmx_data.tileheight * self.SCALE

        for layer in self.tmx_data.visible_layers:
            # 🚨 FIX: Check if the layer actually has tiles to draw!
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    if gid == 0:
                        continue
                    if gid not in self.scaled_tiles:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            self.scaled_tiles[gid] = pygame.transform.scale(tile, (tile_w, tile_h))
                    if gid in self.scaled_tiles:
                        self.screen.blit(
                            self.scaled_tiles[gid],
                            (
                                x * tile_w + self.player.camera_x,
                                y * tile_h + self.player.camera_y
                            )
                        )

    def main(self)-> None:

        """Main code and game loop"""

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            old_camera_x = self.player.camera_x
            old_camera_y = self.player.camera_y

            self.player.handle_keys()
            collided = self.player.collision()
            if collided:
                self.player.camera_x = old_camera_x
                self.player.camera_y = old_camera_y
            event = self.Door_event()
            if event == True:
                self.tmx_data = pytmx.load_pygame(self.current_map)

                self.collision()
                self.door()

            self.screen.fill((0, 0, 0))
            self.player.x = 0
            self.player.y = 0
            
            self.draw_map() #To blit the tmx map
            self.player.draw() # To blit the player

            pygame.display.update()

            self.clock.tick(self.FPS)
            # print(player.camera_x,player.camera_y)
            event = 0

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
        self.camera_x = -150
        self.camera_y = -1050

        self.x = 0
        self.y = 0
        self.hitbox = pygame.Rect(self.player_rect.x + 10,self.player_rect.y + 18,28,28)
         

    def draw(self)-> None:

        """ Draw on surface """

        self.game.screen.blit(self.player_img, self.player_rect)

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


game = Game()
game.main()
