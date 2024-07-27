import json
import discord
from pathlib import Path
from queue import LifoQueue

from .utils import Utils


class ConfigManager:
    __settings = json.loads(
        Path(f"{Utils.get_bot_dir_path()}/config/settings.json").read_text()
    )

    @property
    def settings(self) -> dict:
        return ConfigManager.__settings

    @property
    def owner_username(self) -> str:
        return ConfigManager.__settings["owner"]["username"]

    @property
    def owner_id(self) -> str:
        return ConfigManager.__settings["owner"]["id"]

    @property
    def logging_channels(self) -> dict:
        return ConfigManager.__settings["logging_channels"]

    @property
    def deleted_messages_channel(self) -> int:
        return ConfigManager.logging_channels["deleted_messages"]

    @property
    def edited_messages_channel(self) -> int:
        return ConfigManager.logging_channels["edited_messages"]
