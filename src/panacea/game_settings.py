"""All game settings go here"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
TILE_SIZE = 48
FPS = 60
SCALE = 3
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
GAME_NAME = "Panacea"
ASSETS = PROJECT_ROOT / "assets"
