import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Check the bot's latency")
    async def execute(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! Latency is `{self.bot.latency * 1000:.2f}ms`")


async def setup(bot):
    await bot.add_cog(Ping(bot))
