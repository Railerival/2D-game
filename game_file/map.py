import pygame
import pytmx
from . import misc
from . import game_settings

class Map:
    """Everything map related, optimized and robust."""
    
    def __init__(self, folder: str, file_name: str) -> None:
        # 1. Load TMX data using your robust path system
        self.tmx_data = pytmx.util_pygame.load_pygame(misc.Assets(folder, file_name).path_obj())
        
        self.collision_rects = []
        self._generate_collision_rects() # Generate ONCE in World Space!
        
        # 2. Cache for scaled tiles to prevent massive FPS drops
        self._scaled_tile_cache = {}

    def _generate_collision_rects(self) -> None:
        """
        Generates collision rects ONCE in WORLD coordinates. 
        NO camera offset is applied here. They are static.
        """
        self.collision_rects.clear()
        scale = game_settings.Game_settings.SCALE
        
        for layer in self.tmx_data.visible_layers:
            # IMPORTANT: Make sure this matches the EXACT name of your collision layer in Tiled!
            # (e.g., "Collision", "Collision layer", "Collisions")
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

    def draw_map(self, camera_x: int, camera_y: int) -> None:
        """Blits the map to the display surface using proper camera subtraction."""
        scale = game_settings.Game_settings.SCALE
        tile_w = self.tmx_data.tilewidth * scale
        tile_h = self.tmx_data.tileheight * scale
        display = game_settings.Game_settings.DISPLAY_SURF

        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    if gid != 0:
                        # PERFORMANCE BOOST: Cache scaled tiles so we don't scale them 60 times a second
                        if gid not in self._scaled_tile_cache:
                            raw_tile = self.tmx_data.get_tile_image_by_gid(gid)
                            if raw_tile:
                                self._scaled_tile_cache[gid] = pygame.transform.scale(raw_tile, (tile_w, tile_h))
                        
                        scaled_tile = self._scaled_tile_cache.get(gid)
                        if scaled_tile:
                            # CAMERA MATH: World Position MINUS Camera Offset = Screen Position
                            screen_x = (x * self.tmx_data.tilewidth * scale) - camera_x
                            screen_y = (y * self.tmx_data.tileheight * scale) - camera_y
                            
                            display.blit(scaled_tile, (screen_x, screen_y))