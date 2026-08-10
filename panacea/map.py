import pygame
import pytmx

from . import game_settings


class Map:
    def __init__(self, camera_x: int, camera_y: int) -> None:
        self.collision_rects: list[pygame.Rect] = []
        self.doors: list[Door] = []
        self.tmx_data: pytmx.TiledMap
        self.camera_x = camera_x
        self.camera_y = camera_y

    def load_map(self, mapname: str):
        self.tmx_data = pytmx.util_pygame.load_pygame(game_settings.ASSETS / mapname)

    def create_collision_rects(self, camera_x: int, camera_y: int) -> None:

        self.del_map_rect()
        for layer in self.tmx_data.visible_layers:
            if layer.name == "Collision layer":
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(x * self.tmx_data.tilewidth * game_settings.SCALE+ camera_x, y * self.tmx_data.tileheight * game_settings.SCALE + camera_y, self.tmx_data.tilewidth * game_settings.SCALE, self.tmx_data.tileheight * game_settings.SCALE)
                        self.collision_rects.append(rect)

    def create_doors(self) -> None:
        """creates and appends door object to doors list"""
        door_layer = self.tmx_data.get_layer_by_name("Door Layer")
        for obj in door_layer:
            left = obj.x - (obj.width / 2)
            right = obj.y - (obj.height / 2)
            spawn_coords = (obj.properties["spawn_x"], obj.properties["spawn_y"])
            target_map = obj.properties["target"]
            door = Door(self, left, right, obj.width, obj.height, spawn_coords, target_map)
            self.doors.append(door)

            # print(dir(obj))
            # print(obj.x)
            # print(obj.y)
            # print(obj.width)
            # print(obj.height)
            # print(obj.properties) #{'spawn_x': 0, 'spawn_y': 0, 'target': 'Assets/revised_ground_floor_map.tmx'}

        print(self.doors[0].door_rect)

    def del_doors(self) -> None:
        self.doors.clear()

    def del_map_rect(self) -> None:
        self.collision_rects.clear()

    def draw_map(
        self, camera_x: int, camera_y: int, DISPLAY_SURF: pygame.Surface) -> None:
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (self.tmx_data.tilewidth * game_settings.SCALE, self.tmx_data.tileheight * game_settings.SCALE))
                        DISPLAY_SURF.blit(tile, ((x * self.tmx_data.tilewidth * game_settings.SCALE + camera_x), (y * self.tmx_data.tileheight * game_settings.SCALE + camera_y)))


class Door:
    def __init__(self,map: Map, door_x: int, door_y: int, door_width: int, door_height: int, spawn_coords: tuple, target_map: str):

        self.door_x = door_x
        self.door_y = door_y
        self.door_width = door_width
        self.door_height = door_height
        self.spawn_coords = spawn_coords
        self.target_map = target_map
        self.door_rect = pygame.Rect(
            self.door_x * map.tmx_data.tilewidth * game_settings.SCALE + map.camera_x,
            self.door_y * map.tmx_data.tilewidth * game_settings.SCALE + map.camera_y,
            self.door_width,
            self.door_height,
        )
