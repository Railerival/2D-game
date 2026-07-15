from pathlib import Path

class Assets:#checked
    """asset path object maker class"""
    def __init__(self, folder : str, file_name : str) -> None:
        self.folder = folder
        self.file_name = file_name
    def path_obj(self) -> Path:
        """returns the path object"""
        self.path_object = Path(self.folder)
        self.path = self.path_object / self.file_name
        return self.path