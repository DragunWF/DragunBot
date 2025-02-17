import logging
import discord

from helpers.database_helper import DatabaseHelper, Keys


class CountingGame:
    @staticmethod
    async def __reset_counting(message: discord.Message, last_num: int):
        counting_data = DatabaseHelper.get_counting_data(message.guild.id)
        OLD_HIGH_SCORE = counting_data["high_score"]

        DatabaseHelper.update_counting(message.guild.id, -1, 0)
        await message.add_reaction("❌")

        if last_num > OLD_HIGH_SCORE:
            DatabaseHelper.set_counting_high_score(message.guild.id, last_num)
            await message.channel.send(
                f"Congratulations! A new high score of **{last_num}** has been achieved, beating the old high score of **{OLD_HIGH_SCORE}**!"
            )

    @staticmethod
    def __validate_user(user_id: int, username: str):
        if not DatabaseHelper.is_user_exists(user_id):
            DatabaseHelper.add_user(user_id, username)

    @staticmethod
    def is_counting_channel(guild_id: int, channel_id: int) -> bool:
        return DatabaseHelper.get_counting_channel(guild_id) == channel_id

    @staticmethod
    async def count(message: discord.Message) -> bool:
        CountingGame.__validate_user(message.author.id, message.author.name)

        try:
            counting_data = DatabaseHelper.get_counting_data(message.guild.id)
            NEXT_NUM = counting_data[Keys.COUNT.value] + 1
            CURRENT_NUM = int(message.content)
            USER_PING = f"<@{message.author.id}>"
            if counting_data[Keys.LAST_USER_ID.value] == message.author.id:
                await message.channel.send(
                    f"{USER_PING} got it wrong. The same user cannot count two consecutive times! We're back to counting at **1**"
                )
                await CountingGame.__reset_counting(message, NEXT_NUM - 1)
            elif CURRENT_NUM == NEXT_NUM:
                DatabaseHelper.update_counting(message.guild.id, message.author.id,
                                               NEXT_NUM)
                DatabaseHelper.add_user_times_counted(message.author.id)
                await message.add_reaction("✅" if CURRENT_NUM % 2 != 0 else "☑️")
            else:
                await message.channel.send(
                    f"{USER_PING} messed up. The next number was **{NEXT_NUM}**, not **{CURRENT_NUM}**! We're starting the count over at **1**"
                )
                await CountingGame.__reset_counting(message, NEXT_NUM - 1)
        except ValueError as err:
            logging.error(err)
