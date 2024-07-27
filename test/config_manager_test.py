import sys
import os

project_root = os.path.abspath(
os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
        sys.path.append(project_root)

from rich import print
from bot.helpers.config_manager import ConfigManager


def test() -> None:
    # TODO: Write a more detailed test
    print(ConfigManager.deleted_messages_channel)
    print(ConfigManager.edited_messages_channel)


if __name__ == '__main__':
    test()
