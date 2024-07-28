import traceback
import functools
import logging

import discord
from discord import app_commands


class Debug:
    @staticmethod
    def error_handler(coro):
        """
            Decorator to catch and log exceptions for asynchronous functions.

            Args:
                coro: The coroutine function to be decorated.

            Returns:
                The decorated function with error handling.

            This decorator is primarily for events because events don't have an
            in-built error handler method within discord.py 
        """
        @functools.wraps(coro)
        async def wrapper(*args, **kwargs):
            try:
                await coro(*args, **kwargs)
            except Exception as err:
                TB_STR = ''.join(traceback.format_exception(
                    type(err),  # Type of the exception
                    err,  # The actual exception instance
                    err.__traceback__  # The traceback object
                ))
                logging.error(f'{coro.__name__}:\n{TB_STR}')
        return wrapper

    @staticmethod
    async def on_app_command_error(interaction: discord.Interaction, err: app_commands.AppCommandError):
        await interaction.response.send_message("An error occurred while executing the command.",
                                                ephemeral=True)
        TB_STR = ''.join(traceback.format_exception(
            type(err),
            err,
            err.__traceback__
        ))
        logging.error(f'"{interaction.command.name}": {TB_STR}')
