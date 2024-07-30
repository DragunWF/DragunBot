import random
import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.config_manager import ConfigManager


class Confess(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = None
        self.footer_emojis = ("🪐", "☄️", "💫", "❄️", "✨")

    @discord.app_commands.command(name="setup_confessions",
                                  description="Setup a confessions channel. Enter this command in the channel you want to designate")
    async def setup(self, interaction: discord.Interaction):
        self.channel_id = interaction.channel_id
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an admin to use this command!")
            return

        embed = discord.Embed(title="Confessions channel has been setup!",
                              color=Utils.get_color("royal blue"))
        embed.add_field(name="Command to send a confession",
                        value="`/confess`", inline=False)
        embed.add_field(name="Description",
                        value=(
                            "To send a confession, simply type `/confess`. Your confessions remain entirely private; "
                            "even the bot's developer cannot see who sent a confession. "
                            "For complete transparency, you can review the bot's source code (linked below) "
                            "to verify that all confessions are truly anonymous."
                        ))
        embed.add_field(name="Source Code",
                        value=ConfigManager.bot_source_code(), inline=False)
        embed.set_footer(
            text="☄️ If you have any suggestions for this feature; please message the developer, dragunwf."
        )
        await self.bot.get_channel(self.channel_id).send(embed=embed)
        await interaction.response.send_message(f"<#{self.channel_id}> has been set up as the confessions channel!")

    @discord.app_commands.command(name="confess", description="Submit a confession")
    @discord.app_commands.describe(message="The contents of your confession")
    async def confess(self, interaction: discord.Interaction, message: str):
        if self.channel_id is None:
            await interaction.response.send_message("Confessions channel has not been set up yet for this guild. Please use `/setup_confessions` first if you're an admin.")
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
            text=f"{random.choice(self.footer_emojis)} If you want to send your own confession, simply type /confess"
        )
        await channel.send(embed=embed)
        await interaction.response.send_message("Your confession has been sent!", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Confess(bot))
