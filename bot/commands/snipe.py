import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.session_data import SessionData
from helpers.config_manager import ConfigManager


class Snipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="snipe", description="Show the most recently deleted message")
    async def snipe(self, interaction: discord.Interaction):
        try:
            deleted_message: discord.Message = SessionData.get_recent_deleted_message()
            if deleted_message is None:
                await interaction.response.send_message("My spellbook doesn't have any deleted messages stored at the moment!")
            elif deleted_message.author.id == ConfigManager.owner_id():
                await interaction.response.send_message("Thou shall not snipe the overlord!")
            else:
                embed = discord.Embed(title="Deleted Message",
                                      description=deleted_message.content,
                                      color=Utils.get_color("royal blue"))
                embed.set_author(name=deleted_message.author.name,
                                 icon_url=deleted_message.author.avatar.url)
                embed.set_footer(text=f"#{deleted_message.channel.name}")
                await interaction.response.send_message(embed=embed)
        except Exception as err:
            print(err)

    @discord.app_commands.command(name="esnipe", description="Show the most recently edited message")
    async def esnipe(self, interaction: discord.Interaction):
        edited_message: discord.Message = SessionData.get_recent_edited_message()


async def setup(bot: commands.Bot):
    await bot.add_cog(Snipe(bot))
