import pygame
from . import game_settings
from . import player
from . import map

class Game:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.display = game_settings.Game_settings.DISPLAY_SURF

        self.camera_x = 0
        self.camera_y = 0

        # Start with the main map
        self.load_new_map("Village.tmx", 18, 29)  

    def load_new_map(self, map_name: str, spawn_x: int, spawn_y: int):
        """Load a map and place the player at tile (spawn_x, spawn_y)."""
        self.map = map.Map("Assets", map_name)
    
        # Convertinng thee tile indices to world pixel coordinates
        tile_size = self.map.tmx_data.tilewidth * game_settings.Game_settings.SCALE
        world_x = spawn_x * tile_size
        world_y = spawn_y * tile_size
    
       
        #print(f"Spawning at tile ({spawn_x}, {spawn_y}) -> world pixels ({world_x}, {world_y})") --> optional for debugging
    
        self.player = player.Player(world_x, world_y)

    def handle_input(self):
        dx, dy = 0, 0
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
        # Center camera on player
        screen_w = self.display.get_width()
        screen_h = self.display.get_height()
        target_cam_x = self.player.rect.centerx - (screen_w // 2)
        target_cam_y = self.player.rect.centery - (screen_h // 2)
        self.camera_x = target_cam_x
        self.camera_y = target_cam_y

    def draw(self):
        self.display.fill((0, 0, 0))
        self.map.draw_map(self.camera_x, self.camera_y)

        # Hitbox thingy
        offset_x, offset_y = self.player.get_draw_offset()
        screen_x = self.player.rect.x - self.camera_x - offset_x
        screen_y = self.player.rect.y - self.camera_y - offset_y
        self.display.blit(self.player.current_player_img, (screen_x, screen_y))

        # Debug: draw collision rects and doors (optional)
        for rect in self.map.collision_rects:
            debug_rect = rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.display, (255, 0, 0), debug_rect, 2)
        for door in self.map.doors:
            debug_rect = door.rect.move(-self.camera_x, -self.camera_y)
            pygame.draw.rect(self.display, (0, 0, 255), debug_rect, 2)
        # Player hitbox debug
        player_debug = self.player.rect.move(-self.camera_x, -self.camera_y)
        pygame.draw.rect(self.display, (0, 255, 0), player_debug, 2)

        pygame.display.update()

    def main(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            dx, dy = self.handle_input()
            self.player.move(dx, dy, self.map.collision_rects)

            # --- DOOR TRANSITION CHECK ---
            door = self.map.get_door_at(self.player.rect)
            if door:
                
                self.load_new_map(door.target_map, door.spawn_x, door.spawn_y)
                

            self.update_camera()
            self.draw()
            self.clock.tick(game_settings.Game_settings.FPS)