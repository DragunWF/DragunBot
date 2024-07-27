import discord
from queue import LifoQueue


class SessionData:
    __deleted_messages = LifoQueue()
    __edited_messages = LifoQueue()

    @staticmethod
    def get_recent_deleted_message() -> discord.Message:
        return SessionData.__deleted_messages.get()

    @staticmethod
    def get_recent_edited_message() -> tuple[discord.Message, discord.Message]:
        return SessionData.__edited_messages.get()
