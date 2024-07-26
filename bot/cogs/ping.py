import discord
from discord.ext import commands
from helpers.utils import Utils


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Check the bot's latency")
    async def execute(self, interaction: discord.Interaction):
        # Temporary try and catch
        # TODO: Find an in-built event method that auto logs exceptions from slash commands
        try:
            embed = discord.Embed(
                title="🏓 Pong!",
                description=f"Latency: `{self.bot.latency * 1000:.2f}ms`",
                color=Utils.get_random_color()
            )
            await interaction.response.send_message(embed=embed)
        except Exception as err:
            print(err)


async def setup(bot):
    await bot.add_cog(Ping(bot))
