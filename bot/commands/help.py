import discord
from discord.ext import commands

from helpers.utils import Utils


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generate_command_list(self) -> str:
        output = []
        commands = await self.bot.tree.fetch_commands()
        for command in commands:
            output.append(f"- `/{command.name}` - {command.description}")
        return "\n".join(output)

    @discord.app_commands.command(name="help", description="Show the list of slash commands.")
    async def execute(self, interaction: discord.Interaction):
        # TODO: Add information, make it dynamic
        try:
            embed = discord.Embed(title="List of Commands",
                                  color=Utils.get_color("royal blue"))
            embed.add_field(name="Commands",
                            value=await self.generate_command_list())
            await interaction.response.send_message(embed=embed)
        except Exception as err:
            print(err)


async def setup(bot):
    await bot.add_cog(Help(bot))