import discord
from discord.ext import commands

from helpers.utils import Utils
from helpers.session_data import SessionData
from helpers.config_manager import ConfigManager


class Snipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def create_base_embed(self, message: discord.Message, title: str, description: str | None = None) -> discord.Embed:
        embed = discord.Embed(title=title,
                              description=description,
                              color=Utils.get_color("royal blue"))
        embed.set_author(name=message.author.name,
                         icon_url=message.author.avatar.url)
        embed.set_footer(text=f"Channel: #{message.channel.name}")
        return embed

    @discord.app_commands.command(name="snipe", description="Show the most recently deleted message")
    async def snipe(self, interaction: discord.Interaction):
        deleted_message: discord.Message = SessionData.get_recent_deleted_message(
            interaction.guild_id)
        if deleted_message is None:
            await interaction.response.send_message("My spellbook doesn't have any deleted messages stored at the moment!")
        elif deleted_message.author.id == ConfigManager.owner_id():
            await interaction.response.send_message("Thou shall not snipe the overlord!")
        else:
            embed = self.create_base_embed(deleted_message, "Deleted Message",
                                           deleted_message.content)
            await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="esnipe", description="Show the most recently edited message")
    async def esnipe(self, interaction: discord.Interaction):
        edited_message: dict = SessionData.get_recent_edited_message(
            interaction.guild_id)
        if edited_message is None:
            await interaction.response.send_message("My spellbook doesn't have any edited messages stored at the moment!")
        else:
            before: discord.Message = edited_message["before"]
            after: discord.Message = edited_message["after"]
            if before.author.id == ConfigManager.owner_id():
                await interaction.response.send_message("Thou shall not esnipe the overlord!")
                return

            embed = self.create_base_embed(before, "Edited Message")
            embed.add_field(name="Before Edit",
                            value=before.content, inline=False)
            embed.add_field(name="After Edit",
                            value=after.content, inline=False)
            return await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Snipe(bot))
