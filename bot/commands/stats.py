import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.database_helper import DatabaseHelper, Keys


class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="stats", description="Check the user's stats")
    @discord.app_commands.describe(username="The Discord username of the user you want to check")
    async def execute(self, interaction: discord.Interaction, username: str):
        if not DatabaseHelper.is_username_exists():
            await interaction.response.send_message(
                (f'The user "{username}" is not recognized! The user has either not yet executed a'
                 " DragunBot command or the user does not exist. Make sure you don't have any typos")
            )
            return
        
        data = DatabaseHelper.get_user(1)
        embed = discord.Embed(title=f"{username}'s Stats", color=Utils.get_color("royal blue"))
        embed.add_field(name="Commands Executed", value=f"`{data[Keys.COMMANDS_EXECUTED.value]}`", inline=False)
        embed.add_field(name="Trivia Points", value=f"`{data[Keys.TRIVIA_POINTS.value]}`", inline=False)
        embed.add_field(name="Times Counted", value=f"`{data[Keys.TIMES_COUNTED.value]}`", inline=False)
        embed.set_footer(text="fuck")
        
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
