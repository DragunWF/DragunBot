import discord
import logging
from discord.ext import commands

from helpers.database_helper import DatabaseHelper, Keys


class CommandLogger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def update_user_data(self, interaction: discord.Interaction):
        if DatabaseHelper.is_user_exists(interaction.user.id):
            user_data = DatabaseHelper.get_user(interaction.user.id)
            if user_data[Keys.USERNAME.value] != interaction.user.name:
                DatabaseHelper.update_user_name(
                    interaction.user.id, interaction.user.name
                )

    def update_guild_data(self, interaction: discord.Interaction):
        guild_data = DatabaseHelper.get_guild(interaction.guild_id)
        if interaction.guild.name != guild_data[Keys.GUILD_NAME.value]:
            DatabaseHelper.update_guild_name(
                interaction.guild_id, interaction.guild.name
            )

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        self.update_user_data(interaction)
        self.update_guild_data(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(CommandLogger(bot))
