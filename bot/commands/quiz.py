import logging
import requests
import random
import html

import discord
from discord.ext import commands
from discord import app_commands

from helpers.utils import Utils


class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.API_URL = "https://opentdb.com/api.php"
        # To be used with random.choice() method
        self.difficulties = [*["easy" for i in range(5)],  # 5/10 = 50% chance for easy questions
                             # 4/10 = 40% chance for medium questions
                             *["medium" for i in range(4)],
                             "hard"]  # 1/10 = 10% chance for hard questions
        self.categories = [
            9,  # General Knowledge
            10,  # Entertainment: Books
            11,  # Entertainment: Film
            12,  # Entertainment: Music
            14,  # Entertainment: Television
            15,  # Entertainment: Video Games
            16,  # Entertainment: Board Games
            18,  # Science: Computers
            19,  # Science: Mathematics
            20,  # Mythology
            22,  # Geography
            23,  # History
            25,  # Art
            28,  # Vehicles
            30,  # Science: Gadgets
            31,  # Entertainment: Japanese Anime & Manga
            32  # Entertainment: Cartoon & Animations
        ]

    def get_trivia_question(self, category: int | None, difficulty: str | None) -> dict | None:
        response = requests.get(self.API_URL, {
            "amount": 1,
            "category": category if not category is None else random.choice(self.categories),
            "difficulty": difficulty if difficulty else random.choice(self.difficulties),
            "type": "multiple"
        })
        if response.status_code != 200:
            return None
        return response.json()["results"][0]

    def format_category_name(self, category: str) -> str:
        if ":" in category:
            return html.unescape(category.split(":")[1].lstrip())
        return html.unescape(category)

    @discord.app_commands.command(name="quiz", description="Test your general knowledge with a random trivia question")
    @app_commands.describe(category="Choose a category. This is optional, you'll get a random category if you don't choose one",
                           difficulty="Choose a difficulty level. This is optional, you'll get a random difficulty level if you leave this empty")
    @app_commands.choices(category=[
        app_commands.Choice(name="General Knowledge", value=9),
        app_commands.Choice(name="Books", value=10),
        app_commands.Choice(name="Film", value=11),
        app_commands.Choice(name="Music", value=12),
        app_commands.Choice(name="Television", value=14),
        app_commands.Choice(name="Video Games", value=15),
        app_commands.Choice(name="Board Games", value=16),
        app_commands.Choice(name="Computers", value=18),
        app_commands.Choice(name="Mathematics", value=19),
        app_commands.Choice(name="Mythology", value=20),
        app_commands.Choice(name="Geography", value=22),
        app_commands.Choice(name="History", value=23),
        app_commands.Choice(name="Art", value=25),
        app_commands.Choice(name="Vehicles", value=28),
        app_commands.Choice(name="Gadgets", value=30),
        app_commands.Choice(name="Anime & Manga", value=31),
        app_commands.Choice(name="Cartoon & Animations", value=32),
    ], difficulty=[
        app_commands.Choice(name="Easy", value="easy"),
        app_commands.Choice(name="Medium", value="medium"),
        app_commands.Choice(name="Hard", value="hard"),
    ])
    async def execute(self, interaction: discord.Interaction, category: int = None, difficulty: str = None):
        data: dict[str, str | list[str]] | None = self.get_trivia_question(
            category, difficulty)
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
        embed.add_field(name="Category",
                        value=self.format_category_name(data["category"]))
        embed.add_field(name="Question",
                        value=html.unescape(data["question"]),
                        inline=False)
        embed.set_footer(text=f"Data fetched from {self.API_URL}")
        await interaction.response.send_message(embed=embed,
                                                view=TriviaView(CORRECT_ANSWER,
                                                                options, interaction.user.id))


class TriviaButton(discord.ui.Button):
    def __init__(self, label: str, correct_answer: str, user_id: int):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.correct_answer = correct_answer
        self.user = user_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user:
            await interaction.response.send_message(
                "Only the person who executed the command can answer the question!",
                ephemeral=True
            )
            return
        if self.label == self.correct_answer:
            await interaction.response.send_message(f"**{self.label}** is indeed correct! Congrats, you got the question right")
        else:
            await interaction.response.send_message(f"**{self.label}** is wrong! The correct answer was **{self.correct_answer}**")

        self.view.disable_all_buttons()
        await interaction.message.edit(view=self.view)


class TriviaView(discord.ui.View):
    def __init__(self, correct_answer: str, options: list[str], user_id: int):
        super().__init__()
        for answer in options:
            self.add_item(TriviaButton(label=answer,
                                       correct_answer=correct_answer,
                                       user_id=user_id))

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True


async def setup(bot: commands.Bot):
    await bot.add_cog(Quiz(bot))
