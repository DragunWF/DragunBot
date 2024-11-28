import random
import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.database_helper import DatabaseHelper


class Confess(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.footer_emojis = ("🪐", "☄️", "💫", "❄️", "✨")
        self.headers = ("Anonymous", "Secret", "Mystery")

    @discord.app_commands.command(name="confess", description="Submit a confession")
    @discord.app_commands.describe(message="The contents of your confession")
    async def confess(self, interaction: discord.Interaction, message: str):
        # Defer the interaction to prevent timeout
        await interaction.response.defer(ephemeral=True)

        # Input Validation
        channel_id = DatabaseHelper.get_confessions_channel(
            interaction.guild_id)
        if channel_id is None:
            await interaction.followup.send("Confessions channel has not been set up yet for this guild. Please use `/setup_confessions` first if you're an admin.")
            return

        # Fetch the channel using the stored channel ID
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            await interaction.followup.send("Failed to find the confessions channel. Please set it up again.")
            return

        # Send the confession message to the specified channel
        embed = discord.Embed(
            title=f"{random.choice(self.headers)} Confession (#{DatabaseHelper.get_confessions_count(interaction.guild_id) + 1})",
            description=f'"{message}"',
            color=Utils.get_random_color()
        )
        embed.set_footer(
            text=f"{random.choice(self.footer_emojis)} If you want to send your own confession, simply type /confess"
        )

        # Database update and message send functionality
        DatabaseHelper.add_confession(
            guild_id=interaction.guild_id,
            author_id=interaction.user.id,
            author=interaction.user.name,
            content=message
        )
        await channel.send(embed=embed)

        # Send confirmation message to the user
        await interaction.followup.send("Your confession has been sent!", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Confess(bot))
