import discord
from discord.ext import commands

from helpers.utils import Utils


class Confess(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="setup confession channel",
                                  description="Setup a confessions channel. Type this command in the channel you want to designate the confessions channel to")
    async def setup(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
        await interaction.response.send_message("This command is still in development!")

    @discord.app_commands.command(name="confess", description="Submit a confession")
    @discord.app_commands.describe(message="The contents of your confession")
    async def confess(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message("This command is still under development!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Confess(bot))
