import discord
from discord.ext import commands


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}!')
        await self.bot.tree.sync()
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name="to my overlord..."))


async def setup(bot):
    await bot.add_cog(OnReady(bot))
