import logging
import discord
from discord.ext import commands

from helpers.config_manager import ConfigManager
from helpers.utils import Utils
from helpers.session_data import SessionData
from helpers.debug import Debug
from helpers.database_helper import DatabaseHelper, Keys
from services.counting_game import CountingGame
from services.ai_chatbot import AIChatbot


class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_guild: str = None
        self.last_channel: str = None

    def message_log(self, text: str):
        print(f"<MESSAGE LOG> {text}")

    def log_message_location(self, message: discord.Message):
        if message.guild.name != self.last_guild:
            self.message_log(f"Guild: {message.guild.name}")
            self.last_guild = message.guild.name
        if message.channel.name != self.last_channel:
            self.message_log(f"Channel: #{message.channel.name}")
            self.last_channel = message.channel.name

    @commands.Cog.listener()
    @Debug.error_handler
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        self.log_message_location(message)
        self.message_log(f'[{message.author}]: {message.content}')

        # Counting game logging
        if CountingGame.is_counting_channel(message.guild.id, message.channel.id):
            if message.content.isdigit():
                await CountingGame.count(message)

        # AI Chatbot Service
        if AIChatbot.is_ai_channel(message.guild.id, message.channel.id):
            await AIChatbot.on_user_message(message)
        elif self.bot.user in message.mentions:
            await AIChatbot.on_bot_ping(message)

        await self.bot.process_commands(message)

    @commands.Cog.listener()
    @Debug.error_handler
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        SessionData.record_deleted_message(message)
        self.log_message_location(message)
        self.message_log(
            f"[{message.author}] (Deleted Message): {message.content}"
        )

        embed = discord.Embed(title="Deleted Message",
                              color=Utils.get_random_color())
        embed.set_author(name=message.author.name,
                         icon_url=message.author.avatar.url)
        embed.add_field(name=f"#{message.channel.name}",
                        value=message.content)
        embed.set_footer(text=f"Guild: {message.guild.name}")

        await self.bot.get_channel(ConfigManager.deleted_messages_channel()).send(embed=embed)

    @commands.Cog.listener()
    @Debug.error_handler
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        # This condition prevents logging messages with no edits and messages from bots
        if before.content != after.content and not before.author.bot:
            SessionData.record_edited_message(before, after)
            self.log_message_location(before)
            self.message_log(
                f"[{after.author.name}] (Edited Message): {after.content}"
            )

            embed = discord.Embed(title="Edited Message",
                                  color=Utils.get_random_color())
            embed.set_author(name=before.author.name,
                             icon_url=before.author.avatar.url)
            embed.add_field(name="Before Edit", value=before.content)
            embed.add_field(name="After Edit", value=after.content)
            embed.set_footer(text=f"Guild: {before.guild.name}")

            await self.bot.get_channel(ConfigManager.edited_messages_channel()).send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnMessage(bot))
