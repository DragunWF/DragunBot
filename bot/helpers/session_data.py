import discord
from queue import LifoQueue


class SessionData:
    __deleted_messages = LifoQueue()
    __edited_messages = LifoQueue()

    @staticmethod
    def get_recent_deleted_message() -> discord.Message:
        if not SessionData.__deleted_messages.empty():
            return SessionData.__deleted_messages.get()

    @staticmethod
    def get_recent_edited_message() -> dict:
        if not SessionData.__edited_messages.empty():
            return SessionData.__edited_messages.get()

    @staticmethod
    def record_deleted_message(message: discord.Message):
        SessionData.__deleted_message.put(message)

    @staticmethod
    def record_edited_message(before: discord.Message, after: discord.Message):
        SessionData.__edited_messages.put({"before": before, "after": after})
