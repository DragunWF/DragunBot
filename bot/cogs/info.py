import discord
from discord.ext import commands
from helpers.data import DataHandler


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.socials = {
            "Website": "https://dragunwf.onrender.com/",
            "GitHub": "https://github.com/DragunWF",
            "Itch.io": "https://dragonwf.itch.io/",
            "CodeWars": "https://www.codewars.com/users/DragunWF",
            "TypeRacer": "https://data.typeracer.com/pit/profile?user=dragonwf"
        }

    def get_developer_socials(self) -> str:
        output = []
        for key, value in self.socials.items():
            output.append(f"- [{key}]({value})")
        return "\n".join(output)

    @discord.app_commands.command(name="info", description="See information about DragunBot.")
    async def execute(self, interaction: discord.Interaction):
        embed = discord.Embed(title="General Information")
        embed.set_author(
            name="DragunBot",
            icon_url="https://cdn.discordapp.com/avatars/1266325919597989888/d87657cefbef95a96176eae20f2a6d16.webp?size=128"
        )
        embed.add_field(
            name="Description",
            value="Hi there, this is a general purpose Discord bot with commands on fun, " +
            "games, information, stats, logging, and APIs. If you want to see the list of " +
            "commands, you can do so by typing `/help`.",
            inline=False
        )
        embed.add_field(
            name="Developer's Username",
            value=f"This bot was developed by `{DataHandler.get_owner_username()}`",
            inline=False
        )
        embed.add_field(
            name="Developer's Socials",
            value=self.get_developer_socials(),
            inline=False
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))