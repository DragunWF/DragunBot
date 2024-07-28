import discord
import requests
from discord.ext import commands

from helpers.utils import Utils


class ZenQuotes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.API_URL = "http://zenquotes.io/api/random"
        self.quotes = []
        self.index = 0  # To be specifically used with the quotes list

    def get_quote(self) -> dict | None:
        if self.index >= len(self.quotes):
            response = requests.get(self.API_URL)
            if response.status_code != 200:
                return None
            self.quotes = response.json()
            self.index = 0
        self.index += 1
        return self.quotes[self.index - 1]

    @discord.app_commands.command(name="zenquote", description="Display a random zen quote")
    async def execute(self, interaction: discord.Interaction):
        quote = self.get_quote()
        if quote is None:
            await interaction.response.send_message("Failed to fetch data from ZenQuotes server!",
                                                    ephemeral=True)
            return
        embed = discord.Embed(
            title="Zen Quote",
            description=f'_"{quote["q"]}"_ - {quote["a"]}',
            color=Utils.get_random_color()
        )
        embed.set_footer(text=f"Data fetched from {self.API_URL}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ZenQuotes(bot))
