import logging

from discord.ext import tasks, commands
import discord


class HeartbeatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.heartbeat.start()  # Start the background task
        self.heartbeats = 0

    @tasks.loop(minutes=15)  # Run every 30 minutes
    async def heartbeat(self):
        try:
            # Simple ping to keep the bot active
            self.heartbeats += 1
            logging.info(f"Heartbeat Count: {self.heartbeats}")
            await self.bot.user.edit(username="DragunBot")
        except discord.HTTPException as e:
            logging.info(f"Heartbeat failed: {e}")

    @heartbeat.before_loop
    async def before_heartbeat(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(HeartbeatCog(bot))
