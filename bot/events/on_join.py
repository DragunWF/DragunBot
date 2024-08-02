import discord
import logging
from discord.ext import commands

from helpers.debug import Debug
from helpers.database_helper import DatabaseHelper


class GuildJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def update_guild_data(self, guild: discord.Guild):
        if not DatabaseHelper.is_guild_exists(guild.id):
            DatabaseHelper.add_guild(guild.name, guild.id)

    @commands.Cog.listener()
    @Debug.error_handler
    async def on_guild_join(self, guild: discord.Guild):
        logging.info(f"Bot has joined a new guild: {guild.name} (ID: {guild.id})")
        self.update_guild_data(guild)


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildJoin(bot))
