import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from helpers.utils import Utils
from helpers.data import DataHandler


class Bot:
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="!", intents=intents)

    @staticmethod
    async def load_extensions(dir_name: str):
        extensions = [name.split(".")[0]  # Ignores ".py"
                      for name in Utils.list_files(dir_name)
                      if name.endswith(".py")]
        for extension in extensions:
            extension_name = f'{dir_name}.{extension}'
            try:
                await Bot.client.load_extension(extension_name)
                print(f'Loaded extension "{extension_name}"')
            except Exception as err:
                print(f'Failed to load extension "{extension_name}": {err}')

    @staticmethod
    async def run():
        load_dotenv()
        async with Bot.client:
            await Bot.load_extensions("commands")
            await Bot.load_extensions("events")
            await Bot.client.start(os.environ.get("BOT"))


if __name__ == '__main__':
    asyncio.run(Bot.run())
