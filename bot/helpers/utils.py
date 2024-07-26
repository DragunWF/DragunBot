import random
from pathlib import Path


class Utils:
    __colors = {
        "red": 0xFF0000,
        "orange": 0xFFA500,
        "yellow": 0xFFFF00,
        "green": 0x00FF00,
        "blue": 0x0000FF,
        "purple": 0x800080,
        "pink": 0xFFC0CB,
        "gray": 0x808080,
        "black": 0x000000,
        "white": 0xFFFFFF,
        "dark red": 0x8B0000,
        "light coral": 0xF08080,
        "gold": 0xFFD700,
        "lime": 0x00FF00,
        "aqua": 0x00FFFF,
        "royal blue": 0x4169E1,
        "medium purple": 0x9370DB,
        "hot pink": 0xFF69B4,
        "silver": 0xC0C0C0
    }

    @staticmethod
    def list_files(directory: str) -> list[str]:
        try:
            path = Path(f"{Utils.get_bot_dir_path()}/{directory}")
            files = [f.name for f in path.iterdir() if f.is_file()]
            return files
        except FileNotFoundError:
            print(f"The directory {directory} does not exist.")
            return []

    @staticmethod
    def get_bot_dir_path() -> str:
        directories: list[str] = Path(__file__).__str__().split('\\')
        while directories[-1] != "bot":
            directories.pop()
        return "\\".join(directories)

    @staticmethod
    def get_color(color: str) -> int:
        DEFAULT_COLOR = Utils.__colors["purple"]
        if color in Utils.__colors:
            return Utils.__colors[color]
        return DEFAULT_COLOR

    @staticmethod
    def get_random_color() -> int:
        color_keys = tuple(Utils.__colors.keys())
        return Utils.__colors[color_keys[random.randint(0, len(color_keys)) - 1]]
