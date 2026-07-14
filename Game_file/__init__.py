"""
MAIN GAME FILE
Current no.of issues:03
"""

import pygame
import pytmx
from pathlib import Path

class Assets:#checked
    """asset path object maker class"""
    def __init__(self, folder : str, file_name : str) -> None:
        self.folder = folder
        self.file_name = file_name
    def path_obj(self) -> Path:
        """returns the path object"""
        self.path_object = Path(self.folder)
        self.path = self.path_object / self.file_name
        return self.path

class Game_settings:#checked
    """ SETTINGS of the game"""
    def __init__(self) -> None: 
        self.WINDOW_WIDTH = 800 #windows width
        self.WINDOW_HEIGHT = 400 #windows height
        self.TILE_SIZE = 48 #unit tile size of the game
        self.WINDOW_SIZE = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT) #windows size, tuple
        self.FPS = 60 #frames per second of the game
        self.SCALE = 3
        self.DISPLAY_SURF = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Panacea")
        self.clock = pygame.time.Clock()

class Player:#checked
    """ Player class """
    def __init__(self) -> None:
        self.game_settings = Game_settings()#issue 1
        self.PLAYER_SPEED = 5
        self.PLAYER_SIZE = 48

        #assets loading and transformation
        self.player_up = pygame.image.load(Assets("Assets", "player-up.png").path_obj())
        self.player_down = pygame.image.load(Assets("Assets", "player-down.png").path_obj())
        self.player_left = pygame.image.load(Assets("Assets", "player-left.png").path_obj())
        self.player_right = pygame.image.load(Assets("Assets", "player-right.png").path_obj())
        self.player_surf_up = pygame.transform.scale(self.player_up, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_down = pygame.transform.scale(self.player_down, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_left = pygame.transform.scale(self.player_left, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_surf_right = pygame.transform.scale(self.player_right, (self.PLAYER_SIZE, self.PLAYER_SIZE))
        
        #current player image
        self.current_player_img = self.player_surf_down

        #player position control and hitbox rect
        self.player_rect = self.current_player_img.get_rect()
        self.player_rect.center = (self.game_settings.WINDOW_WIDTH/2, self.game_settings.WINDOW_HEIGHT/2)
        self.hitbox = pygame.Rect(self.player_rect.x + 10,self.player_rect.y + 18,28,28)

    def player_hitbox_move(self, del_x : int, del_y : int) -> None:
        """move the player hitbox"""
        self.hitbox = self.hitbox.move(del_x, del_y)
        
    def reset_hit_box(self, del_x : int, del_y : int) -> None:
        """resets the hitbox back to its place"""
        self.hitbox = self.hitbox.move(-del_x, -del_y)

class Map:#checked but probably has that collision bug
    """Everything map related"""
    def __init__(self,  folder : str, file_name : str) -> None:
        self.tmx_data = pytmx.util_pygame.load_pygame(Assets(folder, file_name).path_obj())
        self.collision_rects = []
        self.game_settings = Game_settings()#issue 2
        

    def collision_rect_maker(self, camera_x : int, camera_y : int) -> None:
        """makes collision rects"""
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision layer":
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(x * self.tmx_data.tilewidth * self.game_settings.SCALE + camera_x, y * self.tmx_data.tileheight * self.game_settings.SCALE + camera_y, self.tmx_data.tilewidth * self.game_settings.SCALE, self.tmx_data.tileheight * self.game_settings.SCALE)
                        self.collision_rects.append(rect)

    def draw_map(self, camera_x : int, camera_y : int) -> None:
        """blits the map to the display surface"""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (self.tmx_data.tilewidth * self.game_settings.SCALE, self.tmx_data.tileheight * self.game_settings.SCALE))
                        self.game_settings.DISPLAY_SURF.blit(tile, (x * self.tmx_data.tilewidth * self.game_settings.SCALE + camera_x, y * self.tmx_data.tileheight * self.game_settings.SCALE + camera_y))
    
    def del_map_rect(self) -> None:
        """deletes all the present rects of the map"""
        self.collision_rects.clear()

class Game:#checked except the main method
    """ THE GAME CLASS!! """
    def __init__(self) -> None:
        pygame.init()
        self.current_map = "Villlage.tmx"
        self.camera_x = -200
        self.camera_y = -1300
        self.player = Player()
        self.map = Map("Assets", "Villlage.tmx")

    def handle_keys(self) -> bool:
        """ Handles Keys """
        key_press = False
        key = pygame.key.get_pressed()
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            key_press = True
            self.camera_y -= self.player.PLAYER_SPEED 
            self.player.current_player_img = self.player.player_surf_down

        if key[pygame.K_w] or key[pygame.K_UP]:
            key_press = True
            self.camera_y += self.player.PLAYER_SPEED 
            self.player.current_player_img = self.player.player_surf_up

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            key_press = True
            self.camera_x -= self.player.PLAYER_SPEED 
            self.player.current_player_img = self.player.player_surf_right

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            key_press = True
            self.camera_x += self.player.PLAYER_SPEED 
            self.player.current_player_img = self.player.player_surf_left

        return key_press
    
    def main(self) -> None:
        """ Main function """
        self.map.collision_rect_maker(self.camera_x, self.camera_y)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            old_camera_x = self.camera_x
            old_camera_y = self.camera_y

            key_press = self.handle_keys()
            if key_press:
                print("key pressed")
                del_x = self.camera_x - old_camera_x
                del_y = self.camera_y - old_camera_y
                print(old_camera_x)
                print(old_camera_y)
                print(del_x)
                print(del_y)
                self.player.player_hitbox_move(del_x, del_y)
                check = self.player.hitbox.collidelist(self.map.collision_rects)
                self.player.reset_hit_box(del_x, del_y)
                print(check)
                if check != -1:
                    #collide
                    print("collided")
                    self.camera_x = old_camera_x
                    self.camera_y = old_camera_y

                elif check == -1:
                    #not collide
                    print("not collided")
                    for index, rect in enumerate(self.map.collision_rects):
                        new_rect = rect.move(del_x, del_y)
                        self.map.collision_rects[index] = new_rect

            self.map.draw_map(self.camera_x, self.camera_y)
            self.player.game_settings.DISPLAY_SURF.blit(self.player.current_player_img,self.player.player_rect)
            
            #issue 3 : player stuck @ colllision
            #un comment this if u want to check the rect issue
            for rect in self.map.collision_rects:
                pygame.draw.rect(self.player.game_settings.DISPLAY_SURF, (255, 0, 0), rect, 2)

            pygame.display.update()
            self.player.game_settings.clock.tick(self.player.game_settings.FPS)
            print("**************************************")

game = Game()
game.main()
