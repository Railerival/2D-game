import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
clock =  pygame.time.Clock()
pygame.display.set_caption("the dungen")#-----------------we can change the name later


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#----------when player closes the screen
            pygame.quit()
            exit()
    #whole game here
    pygame.display.update()
    clock.tick(60)#-------------frame rate here its 60 fps