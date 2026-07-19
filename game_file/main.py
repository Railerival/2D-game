import pygame
from . import game_settings
from . import player
from . import map

class Game:
    def __init__(self) -> None:
        # pygame.init() is now safely handled in game_settings.py
        self.clock = pygame.time.Clock()
        self.display = game_settings.Game_settings.DISPLAY_SURF
        
        self.camera_x = 0
        self.camera_y = 0
        
        # Initialize Player in WORLD SPACE
        self.player = player.Player(500, 500) 
        
        # Initialize Map (Ensure map.py generates rects in WORLD coordinates)
        self.map = map.Map("Assets", "Villlage.tmx") 

    def handle_input(self):
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.player.speed
            self.player.current_player_img = self.player.player_surf_up
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.player.speed
            self.player.current_player_img = self.player.player_surf_down
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.player.speed
            self.player.current_player_img = self.player.player_surf_left
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.player.speed
            self.player.current_player_img = self.player.player_surf_right
            
        return dx, dy

    def update_camera(self):
        screen_w = self.display.get_width()
        screen_h = self.display.get_height()
        
        target_cam_x = self.player.rect.centerx - (screen_w // 2)
        target_cam_y = self.player.rect.centery - (screen_h // 2)
        
        self.camera_x = target_cam_x
        self.camera_y = target_cam_y

    def draw(self):
        self.display.fill((0, 0, 0)) 
        
        self.map.draw_map(self.camera_x, self.camera_y)
        
        # Draw Player (Apply camera offset to get Screen coordinates)
        screen_x = self.player.rect.x - self.camera_x
        screen_y = self.player.rect.y - self.camera_y
        self.display.blit(self.player.current_player_img, (screen_x, screen_y))
        
        # Draw Debug Rects
        for rect in self.map.collision_rects:
            debug_rect = rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.display, (255, 0, 0), debug_rect, 2)
            
        player_debug_rect = self.player.rect.move(-self.camera_x, -self.camera_y)
        pygame.draw.rect(self.display, (0, 255, 0), player_debug_rect, 2)

        pygame.display.update()

    def main(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            dx, dy = self.handle_input()
            
            # Move Player & Resolve Collisions (World Space)
            self.player.move(dx, dy, self.map.collision_rects)
            
            self.update_camera()
            self.draw()
            
            self.clock.tick(game_settings.Game_settings.FPS)