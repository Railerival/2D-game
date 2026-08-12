"""All game settings go here"""

import pygame

class Game_settings:
    """ SETTINGS of the game""" 
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    TILE_SIZE = 48          # final tile size
    FPS = 60
    SCALE = 3               
    WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    DISPLAY_SURF = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Panacea")