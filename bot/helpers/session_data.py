import discord
from queue import LifoQueue


class SessionData:
    __deleted_messages: dict[int, LifoQueue] = {}
    __edited_messages: dict[int, LifoQueue] = {}

    @staticmethod
    def get_recent_deleted_message(guild_id: int) -> discord.Message | None:
        if not SessionData.__deleted_messages.get(guild_id, LifoQueue()).empty():
            return SessionData.__deleted_messages[guild_id].get()
        return None

    @staticmethod
    def get_recent_edited_message(guild_id: int) -> dict | None:
        if not SessionData.__edited_messages.get(guild_id, LifoQueue()).empty():
            return SessionData.__edited_messages[guild_id].get()
        return None

    @staticmethod
    def record_deleted_message(message: discord.Message):
        if message.guild.id not in SessionData.__deleted_messages:
            SessionData.__deleted_messages[message.guild.id] = LifoQueue()
        SessionData.__deleted_messages[message.guild.id].put(message)

    @staticmethod
    def record_edited_message(before: discord.Message, after: discord.Message):
        if before.guild.id not in SessionData.__edited_messages:
            SessionData.__edited_messages[before.guild.id] = LifoQueue()
        SessionData.__edited_messages[before.guild.id].put(
            {"before": before, "after": after})
