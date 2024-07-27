import discord
from discord.ext import commands


class OnMessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        print(f'Message from {message.author}: {message.content}')
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        pass


async def setup(bot):
    await bot.add_cog(OnMessageEvents(bot))
