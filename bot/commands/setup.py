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
    async def setup_counting(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You must be an admin to use this command!")
            return

        embed = discord.Embed(title="Counting channel has been designated to this channel!",
                              color=Utils.get_color("royal blue"))
        embed.add_field(name="How to Play the Counting Game",
                        value=(
                            "1. **Start at 1**: The first person starts the count with the number 1.\n"
                            "2. **Take Turns**: Each player takes turns to count, increasing the number by 1 each time.\n"
                            "3. **No Double Counts**: The same person cannot count twice in a row. The next number must be posted by a different player.\n"
                            "4. **Avoid Mistakes**: If someone makes a mistake (e.g., posts the wrong number or two people post at the same time), the count resets back to 1.\n"
                            "5. **Record High Scores**: Aim for the highest count! The highest scores will be recorded and celebrated.\n\n"
                        ))
        embed.set_footer(
            text='1️⃣ No need to type any command, just type the number to start counting!'
        )
        DatabaseHelper.set_counting_channel(
            interaction.guild_id, interaction.channel_id
        )
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="setup_confessions",
                                  description="Setup a confessions channel. Enter this command in the channel you want to designate")
    async def setup_confessions(self, interaction: discord.Interaction):
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
            interaction.guild_id, interaction.channel_id
        )
        await self.bot.get_channel(interaction.channel_id).send(embed=embed)
        await interaction.response.send_message(f"<#{interaction.channel_id}> has been set up as the confessions channel!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))
