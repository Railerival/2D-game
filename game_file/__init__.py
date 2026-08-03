"""
MAIN GAME FILE

"""

import pygame
from . import game_settings
from . import player
from . import map
from . import misc

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
        self.collide = False

    def handle_keys(self) -> bool:
        """ Handles Keys """
        key = pygame.key.get_pressed()
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.camera_y -= self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_down

        if key[pygame.K_w] or key[pygame.K_UP]:
            self.camera_y += self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_up

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.camera_x -= self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_right

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.camera_x += self.player.PLAYER_SPEED 
            player.Player.current_player_img = player.Player.player_surf_left      

    def main(self) -> None:
        """ Main function """
        self.world_map.collision_rect_maker(self.camera_x, self.camera_y)
        #self.world_map.door_rect_maker()
        while True:
            #self.world_map.door_rect_maker(self.camera_x, self.camera_y, self.current_map)
            self.collide = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            self.old_camera_x = self.camera_x
            self.old_camera_y = self.camera_y
            
            self.handle_keys()
            del_x = -(self.camera_x - self.old_camera_x)
            del_y = -(self.camera_y - self.old_camera_y)
    
            self.player.player_hitbox_move(del_x, del_y)
            check = self.player.hitbox.collidelist(self.world_map.collision_rects)
            self.player.reset_hit_box(del_x, del_y)
            if check == -1:
                self.collide = False
            else:
                self.collide = True
    
            if self.collide:
                self.camera_x = self.old_camera_x
                self.camera_y = self.old_camera_y
    
            else:
                for index, rect in enumerate(self.world_map.collision_rects):
                    new_rect = rect.move(-del_x, -del_y)
                    self.world_map.collision_rects[index] = new_rect

            self.world_map.draw_map(self.camera_x, self.camera_y, self.DISPLAY_SURF)
            self.DISPLAY_SURF.blit(self.player.current_player_img, self.player.player_rect)
            misc.display_debug(f"(o_camx = {self.old_camera_x}, o_camy = {self.old_camera_y})")
            misc.display_debug(f"(camx = {self.camera_x}, camy = {self.camera_y})", y = 35)
            misc.display_debug(f"{check=}", y = 60)
            #issue 3 : player stuck @ colllision
            #un comment this if u want to check the rect issue
            for rect in self.world_map.collision_rects:
                pygame.draw.rect(self.DISPLAY_SURF, (255, 0, 0), rect, 2)
            pygame.draw.rect(self.DISPLAY_SURF, (255, 0, 0), self.player.hitbox, 2)
            pygame.display.update()
            self.clock.tick(game_settings.FPS)
            
game = Game()
game.main()
