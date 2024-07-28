import discord
import logging
from discord.ext import commands

from helpers.debug import Debug


class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    @Debug.error_handler
    async def on_ready(self):
        logging.info(f'Logged in as {self.bot.user}!')
        await self.bot.tree.sync()
        logging.info("Commands have been synchronized")
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name="my overlord..."))


async def setup(bot: commands.Bot):
    await bot.add_cog(OnReady(bot))
