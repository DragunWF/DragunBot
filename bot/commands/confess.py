import random
import discord
from discord.ext import commands

from helpers.utils import Utils


class Confess(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = None
        self.footer_emojis = ("🪐", "☄️", "💫", "❄️", "✨")

    def get_random_emoji(self) -> str:
        return self.footer_emojis[random.randint(0, len(self.footer_emojis) - 1)]

    @discord.app_commands.command(name="setup_confessions",
                                  description="Setup a confessions channel. Enter this command in the channel you want to designate")
    async def setup(self, interaction: discord.Interaction):
        self.channel_id = interaction.channel_id
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an admin to use this command!")
            return
        await interaction.response.send_message("Confessions channel has been set up!")

    @discord.app_commands.command(name="confess", description="Submit a confession")
    @discord.app_commands.describe(message="The contents of your confession")
    async def confess(self, interaction: discord.Interaction, message: str):
        if self.channel_id is None:
            await interaction.response.send_message("Confessions channel has not been set up yet. Please use `/setup_confessions` first.")
            return

        # Fetch the channel using the stored channel ID
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            await interaction.response.send_message("Failed to find the confessions channel. Please set it up again.")
            return

        # Send the confession message to the specified channel
        embed = discord.Embed(title="Anonymous Confession",
                              description=f'"{message}"',
                              color=Utils.get_random_color())
        embed.set_footer(
            text=f"{self.get_random_emoji()} If you want to send your own confession, simply type /confess")
        await channel.send(embed=embed)
        await interaction.response.send_message("Your confession has been sent!", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Confess(bot))
