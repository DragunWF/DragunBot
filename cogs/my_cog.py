import discord
from discord.ext import commands


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Add the slash command to the bot's command tree
        if not self.bot.tree.get_command('hello'):
            self.bot.tree.add_command(self.hello)

    @discord.app_commands.command(name='hello', description='Say hello!')
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Hello, {interaction.user.name}!')


async def setup(bot):
    await bot.add_cog(MyCog(bot))
