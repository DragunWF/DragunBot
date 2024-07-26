from pathlib import Path


class Utils:
    @staticmethod
    def list_files(directory: str) -> list[str]:
        def get_bot_dir_path() -> str:
            directories: list[str] = Path(__file__).__str__().split('\\')
            while directories[-1] != "bot":
                directories.pop()
            return "\\".join(directories)

        try:
            path = Path(f"{get_bot_dir_path()}/{directory}")
            files = [f.name for f in path.iterdir() if f.is_file()]
            return files
        except FileNotFoundError:
            print(f"The directory {directory} does not exist.")
            return []
