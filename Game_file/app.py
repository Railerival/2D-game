#----------------------------------------------UNDER DEVELOPMENT---------------------------------------------------------------------
import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

pygame.display.set_caption("The Dungeon")#--------------------we can always change the name

# Images
playerup = pygame.image.load("player-up.png").convert_alpha()
playerdown = pygame.image.load("player-down.png").convert_alpha()
playerleft = pygame.image.load("player-left.png").convert_alpha()
playerright = pygame.image.load("player-right.png").convert_alpha()

# Current player image
player = playerdown

playerrect = player.get_rect(center=(400, 200))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        playerrect.y -= 2
        player = playerup

    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        playerrect.y += 2
        player = playerdown

    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        playerrect.x -= 2
        player = playerleft

    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        playerrect.x += 2
        player = playerright

    screen.fill((30, 30, 30))

    screen.blit(player, playerrect)

    pygame.display.update()

    clock.tick(60)

#this might go in __init__.py