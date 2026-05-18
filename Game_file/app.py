#----------------------------------------------UNDER DEVELOPMENT---------------------------------------------------------------------
import pygame
import pytmx
from sys import exit

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH = 1000
HEIGHT = 700
FPS = 60

SCALE = 3
PLAYER_SPEED = 3

# ---------------- WINDOW ----------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Dungeon")

clock = pygame.time.Clock()

# ---------------- LOAD MAP ----------------
tmx_data = pytmx.load_pygame("map.tmx")

# ---------------- LOAD PLAYER ----------------
playerup = pygame.image.load("player-up.png").convert_alpha()
playerdown = pygame.image.load("player-down.png").convert_alpha()
playerleft = pygame.image.load("player-left.png").convert_alpha()
playerright = pygame.image.load("player-right.png").convert_alpha()

# Scale player sprites
PLAYER_SIZE = 48

playerup = pygame.transform.scale(playerup, (PLAYER_SIZE, PLAYER_SIZE))
playerdown = pygame.transform.scale(playerdown, (PLAYER_SIZE, PLAYER_SIZE))
playerleft = pygame.transform.scale(playerleft, (PLAYER_SIZE, PLAYER_SIZE))
playerright = pygame.transform.scale(playerright, (PLAYER_SIZE, PLAYER_SIZE))

# Current player image
player = playerdown

# ---------------- PLAYER RECT ----------------
playerrect = player.get_rect(center=(280, 250))

# Smaller collision hitbox
hitbox = pygame.Rect(
    playerrect.x + 10,
    playerrect.y + 18,
    28,
    24
)

# ---------------- COLLISION SYSTEM ----------------
collision_rects = []

for layer in tmx_data.visible_layers:

    
    if layer.name == "OBject layer":

        for x, y, gid in layer:

            
            if gid != 0:

                rect = pygame.Rect(
                    x * tmx_data.tilewidth * SCALE,
                    y * tmx_data.tileheight * SCALE,
                    tmx_data.tilewidth * SCALE,
                    tmx_data.tileheight * SCALE
                )

                collision_rects.append(rect)

# ---------------- GAME LOOP ----------------
while True:

    # -------- EVENTS --------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # -------- INPUT --------
    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dy = -PLAYER_SPEED
        player = playerup

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dy = PLAYER_SPEED
        player = playerdown

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        dx = -PLAYER_SPEED
        player = playerleft

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        dx = PLAYER_SPEED
        player = playerright

    # -------- X COLLISION --------
    future_hitbox = hitbox.move(dx, 0)

    blocked = False

    for rect in collision_rects:

        if future_hitbox.colliderect(rect):
            blocked = True
            break

    if not blocked:
        playerrect.x += dx
        hitbox.x += dx

    # -------- Y COLLISION --------
    future_hitbox = hitbox.move(0, dy)

    blocked = False

    for rect in collision_rects:

        if future_hitbox.colliderect(rect):
            blocked = True
            break

    if not blocked:
        playerrect.y += dy
        hitbox.y += dy

    # -------- DRAW --------
    screen.fill((20, 20, 20))

    # map layers
    for layer in tmx_data.visible_layers:

        if hasattr(layer, "tiles"):

            for x, y, gid in layer:

                tile = tmx_data.get_tile_image_by_gid(gid)

                if tile:

                    # Scale map tiles
                    tile = pygame.transform.scale(
                        tile,
                        (
                            tmx_data.tilewidth * SCALE,
                            tmx_data.tileheight * SCALE
                        )
                    )

                    screen.blit(
                        tile,
                        (
                            x * tmx_data.tilewidth * SCALE,
                            y * tmx_data.tileheight * SCALE
                        )
                    )

    # Draw player
    screen.blit(player, playerrect)

    # ---------------- DEBUG ----------------
    # Show collision boxes

    # for rect in collision_rects:
    #     pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    # Show player hitbox

    # pygame.draw.rect(screen, (0, 255, 0), hitbox, 2)
    print(playerrect.center)

    pygame.display.update()
    clock.tick(FPS)
#this might go in __init__.py