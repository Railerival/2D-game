import pygame
from . import game_settings
from . import entity
from . import map
from . import misc


class Game:
    def __init__(self):
        pygame.init()
        self.DISPLAY_SURF = pygame.display.set_mode(game_settings.WINDOW_SIZE)
        pygame.display.set_caption("Panacea")
        self.clock = pygame.time.Clock()
        self.current_map = "Villlage.tmx"
        self.camera_x = -200
        self.camera_y = -1300
        self.player = entity.Player()
        self.world_map = map.Map(self.camera_x, self.camera_y)
        self.world_map.load_map(self.current_map)
        self.collide = False

    def handle_keys(self) -> None:
        """Handles Keys - changes the offset and current player image"""

        key = pygame.key.get_pressed()
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            self.camera_y -= self.player.entity_speed
            self.player.current_entity_img = self.player.entity_surf_down

        if key[pygame.K_w] or key[pygame.K_UP]:
            self.camera_y += self.player.entity_speed
            self.player.current_entity_img = self.player.entity_surf_up

        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.camera_x -= self.player.entity_speed
            self.player.current_entity_img = self.player.entity_surf_right

        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.camera_x += self.player.entity_speed
            self.player.current_entity_img = self.player.entity_surf_left

    def main(self) -> None:

        self.world_map.create_collision_rects(self.camera_x, self.camera_y)
        self.world_map.create_doors()

        while True:
            door_event = False
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

            for door in self.world_map.doors:
                door_event = self.player.hitbox.colliderect(door.door_rect)
                if door_event:
                    break

            self.player.reset_hit_box(del_x, del_y)

            if door_event:
                self.world_map.del_doors()
                self.world_map.del_map_rect()
                self.world_map.load_map(door.target_map)

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
                for door in self.world_map.doors:
                    door.door_rect = door.door_rect.move(-del_x, -del_y)

            self.world_map.draw_map(self.camera_x, self.camera_y, self.DISPLAY_SURF)
            self.DISPLAY_SURF.blit(self.player.current_entity_img, self.player.player_rect)

            misc.display_debug(f"(o_camx = {self.old_camera_x}, o_camy = {self.old_camera_y})")
            misc.display_debug(f"(camx = {self.camera_x}, camy = {self.camera_y})", y=35)
            misc.display_debug(f"collision {check=}", y=60)
            misc.display_debug("FPS = " + str(self.clock.tick(game_settings.FPS)), y=85)
            # un comment this if u want to check the rect drawn
            for rect in self.world_map.collision_rects:
                pygame.draw.rect(self.DISPLAY_SURF, (255, 0, 0), rect, 2)
            pygame.draw.rect(self.DISPLAY_SURF, (255, 0, 0), self.player.hitbox, 2)
            pygame.display.update()
            for door in self.world_map.doors:
                pygame.draw.rect(self.DISPLAY_SURF, (0, 0, 255), door.door_rect, 2)

if __name__ == "__main__":
    game = Game()
    game.main()
