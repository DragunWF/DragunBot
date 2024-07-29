import asyncio
import os
import logging
from dotenv import load_dotenv

import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.debug import Debug
from helpers.server import Server
from helpers.config_manager import ConfigManager


class Bot:
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="!", intents=intents)

    @staticmethod
    def configure_bot():
        # Sets the method/function that gets called whenever an error occurs on a command
        Bot.client.tree.on_error = Debug.on_app_command_error

        # For terminal and file logging
        LOG_FILE_LOCATION = "logs/basic.log"
        LOG_DIR = os.path.dirname(LOG_FILE_LOCATION)
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(LOG_FILE_LOCATION),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    async def load_extensions(dir_name: str):
        extensions = [name.split(".")[0]  # Ignores ".py"
                      for name in Utils.list_files(dir_name)
                      if name.endswith(".py")]
        for extension in extensions:
            cog_name = f'{dir_name}.{extension}'
            try:
                await Bot.client.load_extension(cog_name)
                logging.info(f'Loaded extension "{cog_name}"')
            except Exception as err:
                logging.error(f'Failed to load extension "{cog_name}": {err}')

    @staticmethod
    async def run():
        server = Server()
        load_dotenv()
        Bot.configure_bot()
        async with Bot.client:
            if not ConfigManager.is_test_mode():  # To stop the bot more conviently when shutting down
                server.keep_alive()
            await Bot.load_extensions("commands")
            await Bot.load_extensions("events")
            await Bot.client.start(os.environ.get("BOT"))


if __name__ == '__main__':
    try:
        asyncio.run(Bot.run())
    except KeyboardInterrupt:
        logging.info("Bot was stopped by user.")
