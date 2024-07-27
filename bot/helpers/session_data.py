import discord
from queue import LifoQueue


class SessionData:
    __deleted_messages: dict[int, LifoQueue] = {}
    __edited_messages: dict[int, LifoQueue] = {}

    @staticmethod
    def get_recent_deleted_message() -> discord.Message:
        if not SessionData.__deleted_messages.empty():
            return SessionData.__deleted_messages.get()
        return None

    @staticmethod
    def get_recent_edited_message() -> dict:
        if not SessionData.__edited_messages.empty():
            return SessionData.__edited_messages.get()
        return None

    @staticmethod
    def record_deleted_message(message: discord.Message):
        if not message.guild.id in SessionData.__deleted_messages:
            SessionData.__deleted_messages[message.guild.id] = LifoQueue()
        SessionData.__deleted_message[message.guild.id].put(message)

    @staticmethod
    def record_edited_message(before: discord.Message, after: discord.Message):
        if not before.guild.id in SessionData.__edited_messages:
            SessionData.__edited_messages[before.guild.id] = LifoQueue()
        SessionData.__edited_messages[before.guild.id].put(
            {"before": before, "after": after})
