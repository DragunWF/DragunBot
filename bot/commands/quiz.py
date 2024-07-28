import requests
import random
import discord
from discord.ext import commands

from helpers.utils import Utils


class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.API_URL = "https://opentdb.com/api.php"
        self.difficulties = ("easy", "medium", "hard")

    def get_trivia_question(self) -> dict | None:
        response = requests.get(self.API_URL, {
            "amount": 1,
            "category": 9,
            "difficulty": self.difficulties[random.randint(0, len(self.difficulties) - 1)],
            "type": "multiple"
        })
        if response.status_code != 200:
            return None

    @discord.app_commands.command(name="quiz", description="Test your general knowledge with a random trivia question")
    async def execute(self, interaction: discord.Interaction):
        await interaction.response.send_message("This command is still under development!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Quiz(bot))
