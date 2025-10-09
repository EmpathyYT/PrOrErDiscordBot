import logging
import os
from random import choices

import discord
from discord import app_commands, TextChannel, Message
from discord.ext import commands
from discord.app_commands import Choice
from bot_main import PrOrErClient, get_appropriate_channel
from cogs.views.bug_form_modal import BugFormModal
from cogs.views.closed_tester_modal import ClosedTesterBugReportModal
from cogs.views.suggestion_form_modal import SuggestionFormModal
from constants import submittal_confirmation_channel, message_id_field_name, closed_tester_role, \
    closed_bug_report_channel, open_bug_report_channel, app_dev_role, to_do_channel, to_do_seperator, guild, \
    feature_request_channel
from models.channel_model import ChannelModel
from typing import Tuple, Any, Coroutine


async def edit_to_do_original_item(msg: Message, is_adding: bool = True):
    if is_adding:
        original_embed = msg.embeds[0]
        original_embed.colour = discord.Color.orange()
        original_embed.description = "**This Item is currently being worked on!**\n\n" + original_embed.description
        await msg.edit(embed=original_embed)
    else:
        original_embed = msg.embeds[0]
        original_embed.colour = discord.Color.blurple()
        original_embed.description = original_embed.description.replace(
            "**This Item is currently being worked on!**\n\n", "")
        await msg.edit(embed=original_embed)


class AppCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: PrOrErClient = bot

    @discord.app_commands.command(name='ping', description='Ping Pong!')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    @discord.app_commands.command(name='bug-report', description='This is for reporting bugs')
    async def bug_report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugFormModal(self.bot, submittal_confirmation_channel.id))

    @discord.app_commands.command(name='closed-bug-report',
                                  description='This is for reporting bugs in the closed alpha')
    async def closed_bug_report(self, interaction: discord.Interaction):
        user = interaction.user
        guild_id = guild.id
        member = self.bot.get_guild(guild_id).get_member(user.id)
        if closed_tester_role.id not in [role.id for role in member.roles]:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.send_modal(ClosedTesterBugReportModal(self.bot, submittal_confirmation_channel.id))

    @discord.app_commands.checks.has_role(app_dev_role.id)
    @discord.app_commands.command(name='generate-to-do', description='This is for generating the server-to-do list')
    async def generate_to_do(self, interaction: discord.Interaction):
        message = ("**To-do List**\nHello, this is an automated message (obviously) "
                   "which displays the features that are currently a WIP.")
        message += f"\n\n{to_do_seperator}\n"
        message += f"{to_do_seperator}"
        await self.bot.get_channel(to_do_channel.id).send(message)
        await interaction.response.send_message("Done!", ephemeral=True)

    @discord.app_commands.checks.has_role(app_dev_role.id)
    @discord.app_commands.choices(
        suggestion_or_bug=[
            Choice(name="Feature Request", value="Feature Request"),
            Choice(name="Bug Report", value="Bug Report")
        ]
    )
    @discord.app_commands.command(name='add-to-do', description='This is for adding to server-to-do list')
    async def add_to_do(self, interaction: discord.Interaction, suggestion_or_bug: app_commands.Choice[str],
                        report_id: int):

        data = await self.check_to_do_exists(suggestion_or_bug, report_id)
        if data[0]:
            await interaction.response.send_message("Item Already Exists", ephemeral=True)
            return

        to_do_message = data[1][0]
        to_do_spliced_messages = data[1][1]
        message_to_add: str
        original_message: Message
        if suggestion_or_bug.value == "Feature Request":
            suggestion_report = await PrOrErClient.provider.get_feature_request(report_id)
            if suggestion_report is not None:
                report_message, link, original_message = await self.get_report_title_and_link(False,
                                                                                              suggestion_report.message_id)
                message_to_add = f"- [Feature Request #{report_id}](<{link}>): {report_message}"
                await edit_to_do_original_item(original_message, True)
            else:
                await interaction.response.send_message("Invalid Id", ephemeral=True)
                return
        else:
            bug_report = await PrOrErClient.provider.get_bug_report(report_id)
            if bug_report is not None:
                report_message, link, original_message = await self.get_report_title_and_link(True,
                                                                                              bug_report.message_id)
                message_to_add = f"- [Bug Report #{report_id}](<{link}>): {report_message}"
            else:
                await interaction.response.send_message("Invalid Id", ephemeral=True)
                return

        if to_do_spliced_messages[1] == "\n":
            to_do_spliced_messages[1] = f"\n{message_to_add}\n"
        else:
            to_do_spliced_messages[1] += f"{message_to_add}\n"

        new_message = to_do_seperator.join(to_do_spliced_messages)
        await to_do_message.edit(content=new_message)
        await interaction.response.send_message("Done!", ephemeral=True)

    @discord.app_commands.checks.has_role(app_dev_role.id)
    @discord.app_commands.choices(
        suggestion_or_bug=[
            Choice(name="Feature Request", value="Feature Request"),
            Choice(name="Bug Report", value="Bug Report")
        ]
    )
    @discord.app_commands.command(name='remove-to-do', description='This is for removing from server-to-do list')
    async def remove_to_do(self, interaction: discord.Interaction, suggestion_or_bug: app_commands.Choice[str],
                           report_id: int):

        exists, data = await self.check_to_do_exists(
            suggestion_or_bug,
            report_id
        )
        if not exists:
            await interaction.response.send_message("Invalid Data", ephemeral=True)
            return

        to_do_message, to_do_spliced_messages, message_list, original_message = data

        if len(message_list) == 1:
            to_do_spliced_messages[1] = f"\n"
        else:
            message_list[0] = f"\n{message_list[0]}"
            to_do_spliced_messages[1] = "\n".join(message_list)

        new_message = to_do_seperator.join(to_do_spliced_messages)
        await to_do_message.edit(content=new_message)
        if suggestion_or_bug.value == "Feature Request":
            await edit_to_do_original_item(original_message, False)

        await interaction.response.send_message("Done!", ephemeral=True)

    @discord.app_commands.command(name='feature-request', description='This is for requesting features')
    async def feature_request(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SuggestionFormModal(self.bot, submittal_confirmation_channel.id))

    @discord.app_commands.command(name='resolve-bug',
                                  description='This is a moderation command used to mark a bug as resolved')
    @discord.app_commands.checks.has_role(app_dev_role.id)
    @discord.app_commands.describe(report_id='The ID of the bug report message to resolve')
    @discord.app_commands.rename(report_id='report-id')
    async def resolve_bug(self, interaction: discord.Interaction, report_id: str):
        report_id = int(report_id)
        report = await PrOrErClient.provider.get_bug_report(report_id)

        if report is None:
            await interaction.response.send_message("No bug report found with that ID.", ephemeral=True)
            return

        channel = closed_bug_report_channel.id if report.is_closed_alpha else open_bug_report_channel.id
        message_id = report.message_id
        message: discord.Message = await self.bot.get_channel(channel).fetch_message(message_id)
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

    @discord.app_commands.command(name='resolve-feature-request',
                                  description='This is a moderation command used to mark a feature as resolved')
    @discord.app_commands.checks.has_role(app_dev_role.id)
    @discord.app_commands.describe(report_id='The ID of the feature request message to resolve')
    @discord.app_commands.rename(report_id='report-id')
    async def resolve_feature_request(self, interaction: discord.Interaction, report_id: str):
        report_id = int(report_id)
        report = await PrOrErClient.provider.get_feature_request(report_id)

        if report is None:
            await interaction.response.send_message("No feature request found with that ID.", ephemeral=True)
            return

        channel = feature_request_channel.id
        message_id = report.message_id
        message: discord.Message = await self.bot.get_channel(channel).fetch_message(message_id)
        embed: discord.Embed = message.embeds[0]
        embed.colour = discord.Color.green()
        embed.title = 'Feature Resolved'
        new_text = embed.footer.text
        if "1" in new_text:
            new_text = new_text.replace("is", "was", 1)
        else:
            new_text = new_text.replace("are", "were", 1)

        embed.set_footer(text=new_text)
        await message.edit(embed=embed, view=None)
        await interaction.response.send_message("Feature request updated!", ephemeral=True)

    
    @discord.app_commands.checks.has_role(app_dev_role.id)
    @discord.app_commands.describe(report_id='This pushes a new version to the app versions database')
    async def push_version(self, interaction: discord.Interaction, report_id: str):
        version = report_id
        await PrOrErClient.provider.add_version_to_app_db(version)
        await interaction.response.send_message(f"Version {version} added to the database!", ephemeral=True)
    
    async def get_report_title_and_link(self, is_bug: bool, message_id: int) -> Tuple[str, str, Message]:
        embed_to_extract_from: discord.Embed
        original_message: discord.Message
        link: str
        if is_bug:
            channel = self.bot.get_channel(get_appropriate_channel(ChannelModel(is_bug_report=True)).id)
            original_message = (await channel.fetch_message(message_id))
            link = original_message.jump_url
            embed_to_extract_from = original_message.embeds[0]
        else:
            channel = self.bot.get_channel(get_appropriate_channel(ChannelModel(is_suggestion=True)).id)
            original_message = (await channel.fetch_message(message_id))
            link = original_message.jump_url
            embed_to_extract_from = original_message.embeds[0]

        message = embed_to_extract_from.description.split('\n')[0].split(":")[1].strip()
        return message, link, original_message

    async def check_to_do_exists(self, suggestion_or_bug, report_id) -> tuple[bool, tuple[
        Message, list[str], list[str], Message]] | tuple[bool, tuple[Message, list[str]]]:
        to_do_fetched_channel: TextChannel = await self.bot.fetch_channel(to_do_channel.id)
        to_do_message = [message async for message in to_do_fetched_channel.history(limit=1)][0]
        to_do_message_content = to_do_message.content
        to_do_spliced_messages = to_do_message_content.split(to_do_seperator)
        if to_do_spliced_messages[0] == '\n':
            return False, (to_do_message, to_do_spliced_messages)
        message_list = to_do_spliced_messages[1][2:].split("\n")
        original_message: Message
        for message in message_list:
            if f"[{suggestion_or_bug.value} #{report_id}]" in message:
                channel_model = ChannelModel(
                    is_bug_report=True) if suggestion_or_bug.value == "Bug Report" else ChannelModel(is_suggestion=True)
                message_id = int(message.split("/")[-1].split(">")[0])
                channel = (get_appropriate_channel(channel_model)).id
                original_message = await self.bot.get_channel(channel).fetch_message(message_id)
                message_list.remove(message)
                return True, (to_do_message, to_do_spliced_messages, message_list, original_message)

        return False, (to_do_message, to_do_spliced_messages)




async def setup(bot):
    await bot.add_cog(AppCommands(bot))
    print(f'Loaded cog: {AppCommands.__name__}')
