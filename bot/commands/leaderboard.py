import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.database_helper import DatabaseHelper, Keys


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.top_user_count = 0
        self.leaderboard_text = None

    def create_leaderboard(self, guild: discord.Guild):
        self.generate_leaderboard(self.sort_users(self.get_users(guild)))

    def generate_leaderboard(self, sorted_users: list[dict]):
        output = []
        # Limit leaderboard output to users <= 10
        self.top_user_count = min(len(sorted_users), 10)
        for i in range(0, self.top_user_count):
            user: dict = sorted_users[i]
            output.append(
                f"`#{i + 1}:` **{user[Keys.USERNAME.value]}** - {user[Keys.TRIVIA_POINTS.value]} Trivia Points"
            )
        self.leaderboard_text = "\n".join(output)

    def sort_users(self, users: list[dict]) -> list[dict]:
        return sorted(users, key=lambda user: user[Keys.TRIVIA_POINTS.value], reverse=True)

    def get_users(self, guild: discord.Guild) -> list[dict]:
        users = DatabaseHelper.get_users()
        output = []
        for id in users:
            if self.is_user_in_guild(int(id), guild):
                output.append(users[id])
        return output

    def is_user_in_guild(self, user_id: int, guild: discord.Guild) -> bool:
        return guild.get_member(user_id) is not None

    @discord.app_commands.command(name="leaderboard", description="Display the users with the most amount of trivia points")
    async def leaderboard_quiz(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Trivia Quiz Points Leaderboard",
                              color=Utils.get_color("royal blue"))
        self.create_leaderboard(interaction.guild)
        embed.add_field(name=f"Top {self.top_user_count} Users in {interaction.guild.name}",
                        value=self.leaderboard_text)
        embed.set_footer(
            text="Type /quiz to play the trivia quiz game and earn points!"
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))
