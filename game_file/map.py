import pygame
import pytmx
from . import game_settings

class Map:#checked but probably has that collision bug
    """Everything map related"""
    def __init__(self) -> None:
        self.collision_rects: list[pygame.Rect] = []
        self.tmx_data: pytmx.TiledMap

    def load_map(self, mapname: str):
        self.tmx_data = pytmx.util_pygame.load_pygame(game_settings.ASSETS / mapname)

    def collision_rect_maker(self, camera_x : int, camera_y : int) -> None:
        """makes collision rects"""
        self.del_map_rect()
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision layer":
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(x * self.tmx_data.tilewidth * game_settings.SCALE + camera_x, y * self.tmx_data.tileheight * game_settings.SCALE + camera_y, self.tmx_data.tilewidth * game_settings.SCALE, self.tmx_data.tileheight * game_settings.SCALE)
                        self.collision_rects.append(rect)

    def del_map_rect(self) -> None:
        """deletes all the present rects of the map"""
        self.collision_rects.clear()
        
    def draw_map(self, camera_x : int, camera_y : int, DISPLAY_SURF) -> None:
        """blits the map to the display surface"""
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (self.tmx_data.tilewidth * game_settings.SCALE, self.tmx_data.tileheight * game_settings.SCALE))
                        DISPLAY_SURF.blit(tile, ((x * self.tmx_data.tilewidth * game_settings.SCALE + camera_x), (y * self.tmx_data.tileheight * game_settings.SCALE + camera_y)))
    
    