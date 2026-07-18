"""
MAIN GAME FILE

"""

import pygame
from . import game_settings
from . import player
from . import map

class Game:#checked except the main method
    """ THE GAME CLASS!! """
    def __init__(self) -> None:
        pygame.init()
        self.DISPLAY_SURF = pygame.display.set_mode(game_settings.WINDOW_SIZE)
        pygame.display.set_caption("Panacea")
        self.clock = pygame.time.Clock()
        self.current_map = "Villlage.tmx"
        self.camera_x = -200
        self.camera_y = -1300
        self.player = player.Player()
        self.world_map = map.Map()
        self.world_map.load_map(self.current_map)
        

    def handle_keys(self) -> bool:
        """ Handles Keys """
        key_press = False
        key = pygame.key.get_pressed()
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            key_press = True
            self.camera_y -= self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_down

        if key[pygame.K_w] or key[pygame.K_UP]:
            key_press = True
            self.camera_y += self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_up

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            key_press = True
            self.camera_x -= self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_right

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            key_press = True
            self.camera_x += self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_left

        return key_press
    
    def main(self) -> None:
        """ Main function """
        self.world_map.collision_rect_maker(self.camera_x, self.camera_y)
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
                check = player.Player.hitbox.collidelist(self.world_map.collision_rects)
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
                    for index, rect in enumerate(self.world_map.collision_rects):
                        new_rect = rect.move(del_x, del_y)
                        self.world_map.collision_rects[index] = new_rect

            self.world_map.draw_map(self.camera_x, self.camera_y, self.DISPLAY_SURF)
            self.DISPLAY_SURF.blit(self.player.current_player_img,self.player.player_rect)
            
            #issue 3 : player stuck @ colllision
            #un comment this if u want to check the rect issue
            for rect in self.world_map.collision_rects:
                pygame.draw.rect(self.DISPLAY_SURF, (255, 0, 0), rect, 2)
            pygame.draw.rect(self.DISPLAY_SURF, (255, 0, 0), player.Player.hitbox, 2)
            pygame.display.update()
            self.clock.tick(game_settings.FPS)
            print("**************************************")

game = Game()
game.main()
