import pygame

_ = pygame.init()
font = pygame.font.Font(None, 30)


def display_debug(info: str, y: int = 10, x: int = 10):
    surface = pygame.display.get_surface()
    text = font.render(str(info), True, "white")
    rect = text.get_rect(topleft=(x, y))

    if surface is not None:
        pygame.draw.rect(surface, "Black", rect)
        surface.blit(text, rect)
