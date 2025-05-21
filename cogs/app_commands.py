import discord
from discord.ext import commands

from cogs.views.bug_form_modal import BugFormModal
from cogs.views.suggestion_form_modal import SuggestionFormModal
feature_request_channel_id = 1374477393800073337


class AppCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='ping', description='Ping Pong!')

    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    @discord.app_commands.command(name='bug-report', description='This is for reporting bugs')
    async def bug_report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugFormModal(self.bot, feature_request_channel_id))

    @discord.app_commands.command(name='feature-request', description='This is for requesting features')
    async def feature_request(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SuggestionFormModal(self.bot, feature_request_channel_id))

async def setup(bot):
    await bot.add_cog(AppCommands(bot))
    print(f'Loaded cog: {AppCommands.__name__}')