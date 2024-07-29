import requests
import random
import discord
import html
from discord.ext import commands

from helpers.utils import Utils


class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.API_URL = "https://opentdb.com/api.php"
        # To be used with get_random_difficulty() method
        self.difficulties = [*["easy" for i in range(5)],  # 5/10 = 50% chance for easy questions
                             # 4/10 = 40% chance for medium questions
                             *["medium" for i in range(4)],
                             "hard"]  # 1/10 = 10% chance for hard questions

    def get_random_difficulty(self) -> str:
        return self.difficulties[random.randint(0, len(self.difficulties) - 1)]

    def get_trivia_question(self) -> dict | None:
        response = requests.get(self.API_URL, {
            "amount": 1,
            "category": 9,  # General Knowledge Category
            "difficulty": self.get_random_difficulty(),
            "type": "multiple"
        })
        if response.status_code != 200:
            return None
        return response.json()["results"][0]

    @discord.app_commands.command(name="quiz", description="Test your general knowledge with a random trivia question")
    async def execute(self, interaction: discord.Interaction):
        data: dict[str, str | list[str]] | None = self.get_trivia_question()
        if data is None:
            await interaction.response.send_message("Failed to fetch trivia question data. Please try again later!")
            return
        CORRECT_ANSWER = html.unescape(data["correct_answer"])
        options = [*[html.unescape(answer) for answer in data["incorrect_answers"]],
                   CORRECT_ANSWER]
        random.shuffle(options)

        embed = discord.Embed(title="Trivia Question",
                              color=Utils.get_random_color())
        embed.add_field(name="Difficulty",
                        value=data["difficulty"].capitalize())
        embed.add_field(name="Category", value=data["category"])
        embed.add_field(name="Question",
                        value=html.unescape(data["question"]),
                        inline=False)
        embed.set_footer(text=f"Data fetched from {self.API_URL}")
        await interaction.response.send_message(embed=embed,
                                                view=TriviaView(CORRECT_ANSWER,
                                                                options))


class TriviaButton(discord.ui.Button):
    def __init__(self, label, correct_answer):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.correct_answer = correct_answer

    async def callback(self, interaction: discord.Interaction):
        if self.label == self.correct_answer:
            await interaction.response.send_message("Congrats, you got the question right!")
        else:
            await interaction.response.send_message(f"Wrong! The correct answer was **{self.correct_answer}**")

        self.view.disable_all_buttons()
        await interaction.message.edit(view=self.view)


class TriviaView(discord.ui.View):
    def __init__(self, correct_answer: str, options: list[str]):
        super().__init__()
        for answer in options:
            self.add_item(TriviaButton(label=answer,
                                       correct_answer=correct_answer))

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True


async def setup(bot: commands.Bot):
    await bot.add_cog(Quiz(bot))
