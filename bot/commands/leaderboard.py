import discord
from discord.ext import commands

from helpers.utils import Utils


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="leaderboard", description="Display the users with the most amount of trivia points")
    async def leaderboard_quiz(self, interaction: discord.Interaction):
        # TODO: Implement this feature (There will be other leaderboards for other games in the future)
        embed = discord.Embed(title="Trivia Quiz Leaderboard",
                              color=Utils.get_color("royal blue"))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))
