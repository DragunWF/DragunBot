import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="help", description="Show the list of slash commands.")
    async def execute(self, interaction: discord.Interaction):
        # TODO: Add information, make it dynamic
        embed = discord.Embed()
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
