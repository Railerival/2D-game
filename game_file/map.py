import pygame
import pytmx
from . import misc
from . import game_settings

class Door:
    """Represents a teleportation trigger."""
    def __init__(self, rect: pygame.Rect, target_map: str, spawn_x: int, spawn_y: int):
        self.rect = rect              # world‑space rect
        self.target_map = target_map  # filename of the next map 
        self.spawn_x = spawn_x        # world pixel coordinate where player appears
        self.spawn_y = spawn_y

class Map:
    def __init__(self, folder: str, file_name: str) -> None:
        self.tmx_data = pytmx.util_pygame.load_pygame(misc.Assets(folder, file_name).path_obj())
        self.collision_rects = []
        self.doors = []
        self._scaled_tile_cache = {}

        self._generate_collision_rects()
        self._generate_doors()

    def _generate_collision_rects(self) -> None:
        self.collision_rects.clear()
        scale = game_settings.Game_settings.SCALE
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision layer":  
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(
                            x * self.tmx_data.tilewidth * scale,
                            y * self.tmx_data.tileheight * scale,
                            self.tmx_data.tilewidth * scale,
                            self.tmx_data.tileheight * scale
                        )
                        self.collision_rects.append(rect)

    def _generate_doors(self) -> None:
        self.doors.clear()
        try:
            door_layer = self.tmx_data.get_layer_by_name("Door Layer")
        except ValueError:
            return 

        scale = game_settings.Game_settings.SCALE
        for obj in door_layer:
            
            rect = pygame.Rect(
                obj.x * scale,
                obj.y * scale,
                obj.width * scale,
                obj.height * scale
            )
            target = obj.properties.get("target", "")
            spawn_x = obj.properties.get("spawn_x", 0)
            spawn_y = obj.properties.get("spawn_y", 0)
           
            self.doors.append(Door(rect, target, spawn_x, spawn_y))

    def get_door_at(self, world_rect: pygame.Rect):
        """Return the first Door whose rect collides with world_rect, or None."""
        for door in self.doors:
            if world_rect.colliderect(door.rect):
                return door
        return None

    def draw_map(self, camera_x: int, camera_y: int) -> None:
        scale = game_settings.Game_settings.SCALE
        tile_w = self.tmx_data.tilewidth * scale
        tile_h = self.tmx_data.tileheight * scale
        display = game_settings.Game_settings.DISPLAY_SURF

        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    if gid != 0:
                        if gid not in self._scaled_tile_cache:
                            raw_tile = self.tmx_data.get_tile_image_by_gid(gid)
                            if raw_tile:
                                self._scaled_tile_cache[gid] = pygame.transform.scale(raw_tile, (tile_w, tile_h))
                        scaled_tile = self._scaled_tile_cache.get(gid)
                        if scaled_tile:
                            screen_x = (x * self.tmx_data.tilewidth * scale) - camera_x
                            screen_y = (y * self.tmx_data.tileheight * scale) - camera_y
                            display.blit(scaled_tile, (screen_x, screen_y))