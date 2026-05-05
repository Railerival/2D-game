#----------------------------------------------UNDER DEVELOPMENT---------------------------------------------------------------------
import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
clock =  pygame.time.Clock()
pygame.display.set_caption("the dungen")#-----------------we can change the name later
background = pygame.image.load("...")#------------file name


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#----------when player closes the screen
            pygame.quit()
            exit()

        if even.type == pygame.KEYDOWN:
            if event.key == pygame.k_w or event.key == pygame.K_UP:
                #move the character forwards
                pass
            elif event.key == pygame.k_s or event.key == pygame.K_DOWN:
                #move the character backwards
                pass
            elif event.key == pygame.k_a or event.key == pygame.K_LEFT:
                #move the character left
                pass
            elif event.key == pygame.k_d or event.key == pygame.K_RIGHT:
                #move the character right
    screen.blit(background,(0,0))
    pygame.display.update()
    clock.tick(60)#-------------frame rate here its 60 fps

#this might go in __init__.py