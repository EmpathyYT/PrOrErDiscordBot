import discord
from discord.ext import commands

from bot_main import PrOrErClient
from cogs.views.bug_form_modal import BugFormModal
from cogs.views.suggestion_form_modal import SuggestionFormModal
from constants import bug_report_channel, submittal_confirmation_channel, message_id_field_name


class AppCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @discord.app_commands.command(name='ping', description='Ping Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    @discord.app_commands.command(name='bug-report', description='This is for reporting bugs')
    async def bug_report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugFormModal(self.bot, submittal_confirmation_channel))

    @discord.app_commands.command(name='feature-request', description='This is for requesting features')
    async def feature_request(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SuggestionFormModal(self.bot, submittal_confirmation_channel))

    @discord.app_commands.command(name='resolve-bug',
                                  description='This is a moderation command used to mark a bug as resolved')
    @discord.app_commands.checks.has_role(1373543360572162048)
    @discord.app_commands.describe(report_id='The ID of the bug report message to resolve')
    @discord.app_commands.rename(report_id='report-id')
    async def resolve_bug(self, interaction: discord.Interaction, report_id: str):
        report_id = int(report_id)
        report = await PrOrErClient.provider.get_bug_report(report_id)

        if report is None:
            await interaction.response.send_message("No bug report found with that ID.", ephemeral=True)
            return

        message_id = report.message_id
        message: discord.Message = await self.bot.get_channel(bug_report_channel).fetch_message(message_id)
        embed: discord.Embed = message.embeds[0]
        embed.colour = discord.Color.green()
        embed.title = 'Bug Resolved'
        new_text = embed.footer.text
        if "1" in new_text:
            new_text = new_text.replace("is", "was", 1)
        else:
            new_text = new_text.replace("are", "were", 1)

        embed.set_footer(text=new_text)
        await message.edit(embed=embed, view=None)
        await interaction.response.send_message("Bug report updated!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(AppCommands(bot))
    print(f'Loaded cog: {AppCommands.__name__}')
