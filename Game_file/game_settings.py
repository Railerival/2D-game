"""All game settings go here"""
import pygame

class Game_settings:#checked
    """ SETTINGS of the game""" 
    WINDOW_WIDTH = 800 #windows width
    WINDOW_HEIGHT = 400 #windows height
    TILE_SIZE = 48 #unit tile size of the game
    FPS = 60 #frames per second of the game
    SCALE = 3
    WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT) #windows size, tuple
    DISPLAY_SURF = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Panacea")
    
