import discord
import requests
from discord.ext import commands

from helpers.utils import Utils


class CodeWars(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data: dict = None
        self.languages: dict[str, dict] = None

    def get_most_used_language(self) -> str:
        most_used, max_score = None, 0
        for language, attributes in self.languages.items():
            if attributes["score"] > max_score:
                most_used = language.capitalize()
                max_score = attributes["score"]
        return most_used

    def get_languages(self) -> str:
        return [language for language in self.languages]

    @discord.app_commands.command(name="codewars", description="Display the stats of a given user")
    @discord.app_commands.describe(username="The username of the CodeWars account")
    async def execute(self, interaction: discord.Interaction, username: str):
        # Defer the response to avoid timeouts
        await interaction.response.defer()

        url = f"https://www.codewars.com/api/v1/users/{username}"
        response = requests.get(url)
        if response.status_code != 200:
            await interaction.followup.send(f'Failed to fetch data for `{username}`, user does not exist! ' +
                                            "Make sure you typed in the correct username!",
                                            ephemeral=True)
            return

        # Data from the API
        self.data = response.json()
        self.languages = self.data["ranks"]["languages"]

        # Embed message data
        embed = discord.Embed(title="CodeWars Stats",
                              color=Utils.get_color("red"))
        embed.add_field(name="Username", value=f"`{username}`", inline=False)
        embed.add_field(name="Honor",
                        value=f"`{Utils.format_num(self.data['honor'])}`")
        embed.add_field(name="Rank",
                        value=f"`{self.data['ranks']['overall']['name'].title()}`")
        embed.add_field(name="Leaderboard",
                        value=f"`Top #{Utils.format_num(self.data['leaderboardPosition'])}`" if self.data["leaderboardPosition"] else f"`None`")
        embed.add_field(name="Katas Solved",
                        value=f"`{Utils.format_num(self.data['codeChallenges']['totalCompleted'])}`")
        embed.add_field(name="Most Used",
                        value=f"`{self.get_most_used_language()}`")
        embed.add_field(name="Clan",
                        value=f"`{self.data['clan'] if self.data['clan'] else 'None'}`")
        embed.add_field(name="Programming Languages",
                        value=", ".join(self.get_languages()), inline=False)
        embed.add_field(name="Profile Link",
                        value=f"https://www.codewars.com/users/{username}", inline=False)
        embed.set_footer(text=f"Data fetched from {url}")

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CodeWars(bot))
