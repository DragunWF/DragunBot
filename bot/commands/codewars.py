import discord
import requests
from discord.ext import commands

from helpers.utils import Utils


class CodeWars(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="codewars", description="Display the stats of a given user")
    @discord.app_commands.describe(username="The username of the CodeWars account you to see that stats of")
    async def execute(self, interaction: discord.Interaction, username: str):
        url = f"https://www.codewars.com/api/v1/users/{username}"
        response = requests.get(url)
        if response.status_code != 200:
            await interaction.response.send_message(f"Failed to fetch data for user: {username}", ephemeral=True)
            return

        data: dict = response.json()
        embed = discord.Embed(title=f"CodeWars Stats for {username}",
                              color=Utils.get_color("red"))
        embed.add_field(name="Honor", value=data["honor"])
        embed.add_field(name="Leaderboard Position",
                        value=data["leaderboardPosition"])
        embed.add_field(name="Rank",
                        value=data["ranks"]["overall"]["name"].title())
        embed.add_field(name="Katas Solved",
                        value=data["codeChallenges"]["totalCompleted"])
        embed.add_field(name="Clan", value=data["clan"])
        embed.add_field(name="Skills",
                        value=", ".join(data["skills"]))
        embed.set_footer(text=f"https://www.codewars.com/users/{username}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CodeWars(bot))
