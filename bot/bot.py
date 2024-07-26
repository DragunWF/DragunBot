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

    @client.event
    async def on_ready():
        print(f'Logged in as {Bot.client.user}!')
        await Bot.client.change_presence(activity=discord.Game(name="Servant to my overlord..."))

    async def run():
        load_dotenv()
        async with Bot.client:
            extensions = [name.split(".")[0]  # Ignores ".py"
                          for name in Utils.list_files("cogs")]
            for extension in extensions:
                try:
                    await Bot.client.load_extension(f"cogs.{extension}")
                    print(f'Loaded extension cogs.{extension}')
                except Exception as err:
                    print(f'Failed to load extension "cogs.{extension}": {err}')
            await Bot.client.start(os.environ.get("TEST"))


if __name__ == '__main__':
    asyncio.run(Bot.run())
