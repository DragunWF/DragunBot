import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from helpers.utils import Utils


class Bot:
    intents = discord.Intents.default()
    client = commands.Bot(command_prefix="!", intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {Bot.client.user}!')

    async def run():
        load_dotenv()
        async with Bot.client:
            extensions = [name.split(".")[0]  # Ignores ".py"
                          for name in Utils.list_files("cogs")]
            for extension in extensions:
                await Bot.client.load_extension(f"cogs.{extension}")
            await Bot.client.start(os.environ.get("TEST"))


if __name__ == '__main__':
    asyncio.run(Bot.run())
