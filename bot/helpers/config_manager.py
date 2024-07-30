import json
from pathlib import Path

from .utils import Utils


class ConfigManager:
    __settings = json.loads(
        Path(f"{Utils.get_bot_dir_path()}/config/settings.json").read_text()
    )

    @staticmethod
    def settings() -> dict:
        return ConfigManager.__settings

    @staticmethod
    def owner_username() -> str:
        return ConfigManager.__settings["owner"]["username"]

    @staticmethod
    def owner_id() -> str:
        return ConfigManager.__settings["owner"]["id"]

    @staticmethod
    def logging_channels() -> dict:
        return ConfigManager.__settings["logging_channels"]

    @staticmethod
    def deleted_messages_channel() -> int:
        return ConfigManager.logging_channels()["deleted_messages"]

    @staticmethod
    def edited_messages_channel() -> int:
        return ConfigManager.logging_channels()["edited_messages"]

    @staticmethod
    def bot_name() -> str:
        return ConfigManager.__settings["bot"]["name"]

    @staticmethod
    def bot_icon_url() -> str:
        return ConfigManager.__settings["bot"]["icon_url"]

    @staticmethod
    def bot_source_code() -> str:
        return ConfigManager.__settings["bot"]["source_code"]

    @staticmethod
    def is_test_mode() -> bool:
        return ConfigManager.__settings["development"]["test_mode"]

    @staticmethod
    def log_file_enabled() -> bool:
        return ConfigManager.__settings["development"]["log_file_enabled"]
