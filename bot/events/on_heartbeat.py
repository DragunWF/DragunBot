import logging

from discord.ext import tasks, commands
import discord

from helpers.session_data import SessionData


class HeartbeatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Note: Temporarily disabled to prevent getting API requests getting limited
        # self.heartbeat.start()  # Start the background task
        self.heartbeats = 0

    @tasks.loop(minutes=15)  # Run every 15 minutes
    async def heartbeat(self):
        try:
            # Increase the heartbeat count and log it
            self.heartbeats += 1
            logging.info(f"Heartbeat Count: {self.heartbeats}")

            # Temporarily change the bot's status to trigger activity
            await self.bot.change_presence(activity=discord.Game(name="Maintaining connection"))

            # Revert to default status (None) if you don't have a custom one set
            await self.bot.change_presence(activity=SessionData.get_discord_status())
        except discord.HTTPException as e:
            logging.info(f"Heartbeat failed: {e}")

    @heartbeat.before_loop
    async def before_heartbeat(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(HeartbeatCog(bot))
