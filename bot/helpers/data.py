import json
from pathlib import Path
from .utils import Utils


class DataHandler:
    __settings = json.loads(
        Path(f"{Utils.get_bot_dir_path()}/config/settings.json").read_text()
    )

    @property
    def settings(self) -> dict:
        return DataHandler.__settings

    @property
    def owner_username(self) -> str:
        return DataHandler.__settings["owner"]["username"]

    @property
    def owner_id(self) -> str:
        return DataHandler.__settings["owner"]["id"]
