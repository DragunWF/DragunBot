import discord
import logging
from discord.ext import commands

from helpers.debug import Debug
from helpers.database_helper import DatabaseHelper


class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def update_guilds_data(self):
        guilds = self.bot.guilds
        for guild in guilds:
            if not DatabaseHelper.is_guild_exists(guild.id):
                DatabaseHelper.add_guild(guild.id)
        logging.info("Guilds data is now up to date!")

    @commands.Cog.listener()
    @Debug.error_handler
    async def on_ready(self):
        logging.info(f'Logged in as {self.bot.user}!')
        await self.bot.tree.sync()
        logging.info("Commands have been synchronized")
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name="my overlord...")
        )
        logging.info("Bot status has been set!")
        self.update_guilds_data()


async def setup(bot: commands.Bot):
    await bot.add_cog(OnReady(bot))
