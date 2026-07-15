"""
MAIN GAME FILE

"""

import pygame
import pytmx
from . import game_settings
from . import functions_file as func

class Player:#refactored
    """ Player class """

    PLAYER_SPEED = 5
    PLAYER_SIZE = 48

    #assets loading and transformation
    player_up = pygame.image.load(func.Assets("Assets", "player-up.png").path_obj())
    player_down = pygame.image.load(func.Assets("Assets", "player-down.png").path_obj())
    player_left = pygame.image.load(func.Assets("Assets", "player-left.png").path_obj())
    player_right = pygame.image.load(func.Assets("Assets", "player-right.png").path_obj())
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

class Map:#checked but probably has that collision bug
    """Everything map related"""
    def __init__(self,  folder : str, file_name : str) -> None:
        self.tmx_data = pytmx.util_pygame.load_pygame(func.Assets(folder, file_name).path_obj())
        self.collision_rects = []

    def collision_rect_maker(self, camera_x : int, camera_y : int) -> None:
        """makes collision rects"""
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision layer":
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(x * self.tmx_data.tilewidth * game_settings.Game_settings.SCALE + camera_x, y * self.tmx_data.tileheight * game_settings.Game_settings.SCALE + camera_y, self.tmx_data.tilewidth * game_settings.Game_settings.SCALE, self.tmx_data.tileheight * game_settings.Game_settings.SCALE)
                        self.collision_rects.append(rect)

    def draw_map(self, camera_x : int, camera_y : int) -> None:
        """blits the map to the display surface"""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (self.tmx_data.tilewidth * game_settings.Game_settings.SCALE, self.tmx_data.tileheight * game_settings.Game_settings.SCALE))
                        game_settings.Game_settings.DISPLAY_SURF.blit(tile, (x * self.tmx_data.tilewidth * game_settings.Game_settings.SCALE + camera_x, y * self.tmx_data.tileheight * game_settings.Game_settings.SCALE + camera_y))
    
    def del_map_rect(self) -> None:
        """deletes all the present rects of the map"""
        self.collision_rects.clear()

class Game:#checked except the main method
    """ THE GAME CLASS!! """
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
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
            Player.current_player_img = Player.player_surf_down

        if key[pygame.K_w] or key[pygame.K_UP]:
            key_press = True
            self.camera_y += self.player.PLAYER_SPEED 
            Player.current_player_img = Player.player_surf_up

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            key_press = True
            self.camera_x -= self.player.PLAYER_SPEED 
            Player.current_player_img = Player.player_surf_right

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            key_press = True
            self.camera_x += self.player.PLAYER_SPEED 
            Player.current_player_img = Player.player_surf_left

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
                check = Player.hitbox.collidelist(self.map.collision_rects)
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
            game_settings.Game_settings.DISPLAY_SURF.blit(self.player.current_player_img,self.player.player_rect)
            
            #issue 3 : player stuck @ colllision
            #un comment this if u want to check the rect issue
            for rect in self.map.collision_rects:
                pygame.draw.rect(game_settings.Game_settings.DISPLAY_SURF, (255, 0, 0), rect, 2)
            pygame.draw.rect(game_settings.Game_settings.DISPLAY_SURF, (255, 0, 0), Player.hitbox, 2)
            pygame.display.update()
            self.clock.tick(game_settings.Game_settings.FPS)
            print("**************************************")

game = Game()
game.main()
