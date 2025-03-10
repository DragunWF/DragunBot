import discord
from discord.ext import commands
from helpers.utils import Utils

# TODO: Categorize commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def generate_command_list(self) -> str:
        output = []
        commands = await self.bot.tree.fetch_commands()
        for command in commands:
            if command.name == "help":
                continue
            output.append(f"- `/{command.name}` - {command.description}")
        return "\n".join(output)

    @discord.app_commands.command(name="help", description="Show the list of slash commands")
    async def execute(self, interaction: discord.Interaction):
        # Defer the interaction response to prevent timeout
        await interaction.response.defer()

        # Generate command list and prepare the embed
        embed = discord.Embed(
            title="List of Commands",
            color=Utils.get_color("royal blue")
        )
        embed.add_field(
            name="Commands",
            value=await self.generate_command_list()
        )

        # Send the message after generating the content
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
