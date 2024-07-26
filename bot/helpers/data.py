import json
from .utils import Utils
from pathlib import Path


class DataHandler:
    __settings = json.loads(
        Path(f"{Utils.get_bot_dir_path()}/config/settings.json").read_text()
    )

    @staticmethod
    def get_settings() -> dict:
        return DataHandler.__settings
