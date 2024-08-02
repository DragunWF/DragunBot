import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.database_helper import DatabaseHelper
from helpers.config_manager import ConfigManager


class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="setup_counting",
                                  description="Setup a counting channel. Enter this command in the channel you want to designate")
    async def setup(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an admin to use this command!")
            return

        embed = discord.Embed()
        await self.bot.get_channel(channel_id).send(embed=embed)
        await interaction.response.send_message(f"<#{channel_id}> has been set up as the counting channel. Happy counting!")

    @discord.app_commands.command(name="setup_confessions",
                                  description="Setup a confessions channel. Enter this command in the channel you want to designate")
    async def setup(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
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
        DatabaseHelper.set_confessions_channel(
            interaction.guild_id, channel_id)
        await self.bot.get_channel(channel_id).send(embed=embed)
        await interaction.response.send_message(f"<#{channel_id}> has been set up as the confessions channel!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))
