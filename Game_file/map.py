import pygame
import pytmx
from . import misc
from . import game_settings

class Map:#checked but probably has that collision bug
    """Everything map related"""
    def __init__(self,  folder : str, file_name : str) -> None:
        self.tmx_data = pytmx.util_pygame.load_pygame(misc.Assets(folder, file_name).path_obj())
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