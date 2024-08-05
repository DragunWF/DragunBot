import logging
import discord

from helpers.database_helper import DatabaseHelper, Keys


class CountingGame:
    @staticmethod
    def is_counting_channel(guild_id: int, channel_id: int) -> bool:
        return DatabaseHelper.get_counting_channel(guild_id) == channel_id

    @staticmethod
    async def is_new_high_score(guild_id: int) -> bool:
        return

    @staticmethod
    async def reset_counting(message: discord.Message):
        DatabaseHelper.update_counting(message.guild.id, -1, 0)
        await message.add_reaction("❌")

    @staticmethod
    async def count(message: discord.Message) -> bool:
        try:
            counting_data = DatabaseHelper.get_counting_data(message.guild.id)
            NEXT_NUM = counting_data[Keys.COUNT.value] + 1
            CURRENT_NUM = int(message.content)
            USER_PING = f"<@{message.author.id}>"
            if counting_data[Keys.LAST_USER_ID.value] == message.author.id:
                await CountingGame.reset_counting(message)
                await message.channel.send(
                    f"{USER_PING} got it wrong. The same user cannot count two consecutive times! We're back to counting at **1**"
                )
            elif CURRENT_NUM == NEXT_NUM:
                DatabaseHelper.update_counting(message.guild.id, message.author.id,
                                               NEXT_NUM)
                await message.add_reaction("✅" if CURRENT_NUM % 2 != 0 else "☑️")
            else:
                await CountingGame.reset_counting(message)
                await message.channel.send(
                    f"{USER_PING} messed up. The next number was **{NEXT_NUM}**, not **{CURRENT_NUM}**! We're starting the count over at **1**"
                )
        except ValueError as err:
            logging.error(err)
