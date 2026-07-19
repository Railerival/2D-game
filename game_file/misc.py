from pathlib import Path

# Automatically find the root directory (2 levels up from misc.py)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

class Assets:
    """Robust asset path object maker class"""
    def __init__(self, folder: str, file_name: str) -> None:
        # Anchor the folder to the PROJECT_ROOT so it ALWAYS works
        self.path = PROJECT_ROOT / folder / file_name

    def path_obj(self) -> Path:
        """Returns the absolute path object"""
        return self.path