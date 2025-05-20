import discord
from discord.ext import commands


class AppCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='ping', description='Ping Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

async def setup(bot):
    await bot.add_cog(AppCommands(bot))
    print(f'Loaded cog: {AppCommands.__name__}')