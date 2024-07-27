import discord
from discord.ext import commands

from helpers.config_manager import ConfigManager
from helpers.utils import Utils


class OnMessageEvents(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        print(f'Message from {message.author}: {message.content}')
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        try:
            embed = discord.Embed(title="Deleted Message",
                                  color=Utils.get_random_color())
            embed.set_author(name=message.author.name,
                             icon_url=message.author.avatar.url)
            embed.add_field(name=f"#{message.channel.name}",
                            value=message.content)
            embed.set_footer(text=f"Guild: {message.guild.name}")
            await self.bot.get_channel(ConfigManager.deleted_messages_channel()).send(embed=embed)
        except Exception as err:
            print(err)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        try:
            if before.content != after.content:
                embed = discord.Embed(title="Edited Message",
                                      color=Utils.get_random_color())
                embed.set_author(name=before.author.name,
                                 icon_url=before.author.avatar.url)
                embed.add_field(name="Before Edit:", value=before.content)
                embed.add_field(name="After Edit:", value=after.content)
                embed.set_footer(text=f"Guild: {before.guild.name}")
                await self.bot.get_channel(ConfigManager.edited_messages_channel()).send(embed=embed)
        except Exception as err:
            print(err)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnMessageEvents(bot))
