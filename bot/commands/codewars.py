import discord
import requests
from discord.ext import commands

from helpers.utils import Utils


class CodeWars(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.data: dict = None
        self.languages: dict = None

    def get_most_used_language(self) -> str:
        most_used, max_score = None, 0
        for language, attributes in self.languages.items():
            if attributes["score"] > max_score:
                most_used = language.capitalize()
                max_score = attributes["score"]
        return most_used

    def get_languages(self) -> str:
        return [language for language in self.languages]

    def mono(self, text: str) -> str:
        return f"`{text}`"  # Turns text into monospace via Discord markdown

    @discord.app_commands.command(name="codewars", description="Display the stats of a given user")
    @discord.app_commands.describe(username="The username of the CodeWars account you to see that stats of")
    async def execute(self, interaction: discord.Interaction, username: str):
        url = f"https://www.codewars.com/api/v1/users/{username}"
        response = requests.get(url)
        if response.status_code != 200:
            await interaction.response.send_message(f'Failed to fetch data for "{username}". ' +
                                                    "Make sure you typed in the correct username!",
                                                    ephemeral=True)
            return

        self.data = response.json()
        self.languages = self.data["ranks"]["languages"]
        embed = discord.Embed(title=f"CodeWars Stats",
                              color=Utils.get_color("red"))
        embed.add_field(name="Username",
                        value=self.mono(username), inline=False)
        embed.add_field(name="Honor",
                        value=self.mono(Utils.format_num(self.data["honor"])))
        embed.add_field(name="Rank",
                        value=self.mono(self.data["ranks"]["overall"]["name"].title()))
        embed.add_field(name="Leaderboard",
                        value=self.mono(f"Top #{Utils.format_num(self.data['leaderboardPosition'])}"))
        embed.add_field(name="Katas Solved",
                        value=self.mono(Utils.format_num(self.data["codeChallenges"]["totalCompleted"])))
        embed.add_field(name="Most Used",
                        value=self.mono(self.get_most_used_language()))
        embed.add_field(name="Clan",
                        value=self.mono(self.data["clan"] if self.data["clan"] else "None"))
        embed.add_field(name="Programming Languages",
                        value=", ".join(self.get_languages()),
                        inline=False)
        embed.add_field(name="Profile Link",
                        value=f"https://www.codewars.com/users/{username}",
                        inline=False)
        embed.set_footer(text=f"Data fetched from {url}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(CodeWars(bot))
