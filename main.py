import asyncio
import os
import discord
from discord.ext import commands


class Main:
    intents = discord.Intents.default()
    bot = commands.Bot(intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {Main.bot.user}!')

    async def run():
        async with Main.bot:
            await Main.bot.load_extension('cogs.my_cog')
            await Main.bot.start(os.environ.get("TEST"))


if __name__ == '__main__':
    asyncio.run(Main.run())
