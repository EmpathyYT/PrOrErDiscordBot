import os
import re
from collections.abc import Callable, Coroutine

import discord
from discord import Interaction
from dotenv import load_dotenv
from enum import Enum

from DB.sqlite_service_provider import SQLiteServiceProvider
from cogs.views.bug_vote_dynamic_item import BugVoteDynamicItem
from cogs.views.suggestion_vote_dynamic_item import SuggestionVoteDynamicItem
from constants import db_path

load_dotenv()


class ConfirmView(discord.ui.View):
    def __init__(self, initial_user_id: int = None):
        super().__init__(timeout=None)
        self.initial_user_id = initial_user_id

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id='confirm_button')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.reply("Confirmed!")
        channel = self.get_channel_to_send_to(interaction)
        view, footer, fn = await self.get_appropriate_view(channel, interaction)
        embed = interaction.message.embeds[0]
        embed.set_footer(text=footer)
        message = await interaction.guild.get_channel(channel.value.id).send(
            embed=embed,
            view=view,
        )
        await fn(message.id, self.initial_user_id)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, custom_id='cancel_button')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.reply("Rejected!")
        self.stop()

    async def interaction_check(self, interaction: Interaction, /) -> bool:
        if interaction.guild.get_role(int(os.getenv('MANAGER_ROLE_ID'))) not in interaction.user.roles:
            await interaction.response.send_message("You are not allowed to use this button.", ephemeral=True)
            return False
        return True

    def get_channel_to_send_to(self, interaction):
        # return Channels.ALPHA_TESTER
        if "Bug Report" in interaction.message.embeds[0].title:
            return Channels.BUG_REPORT
        else:
            return Channels.SUGGESTION

    async def get_appropriate_view(self, channel, interaction) -> (discord.ui.View, str, Coroutine):
        view = discord.ui.View(timeout=None)
        if self.initial_user_id is None:
            self.initial_user_id = int(re.findall(r'\d+', interaction.message.content)[0])
        footer = ''
        db_provider = SQLiteServiceProvider(db_path)
        fn = None
        match channel:
            case Channels.BUG_REPORT:
                fn = db_provider.add_bug_user
                view.add_item(BugVoteDynamicItem(self.initial_user_id, 'Report Bug',
                                                 [self.initial_user_id], '🪲', db_provider))
                footer = '1 person is experiencing this bug.'

            case Channels.SUGGESTION:
                fn = db_provider.add_feature_user
                view.add_item(SuggestionVoteDynamicItem(self.initial_user_id, 'Suggest Feature',
                                                        [self.initial_user_id], '⬆️', db_provider))
                footer = '1 person is requesting this feature.'

            case Channels.ALPHA_TESTER:
                fn = db_provider.add_feature_user
                view.add_item(SuggestionVoteDynamicItem(self.initial_user_id, 'Suggest Feature',
                                                        [self.initial_user_id], '⬆️', db_provider))
                footer = 'This suggestion is requested by 1 person.'

        return view, footer, fn


class Channels(Enum):
    BUG_REPORT = discord.Object(id=1374419412924371065)
    SUGGESTION = discord.Object(id=1374432042988732578)
    ALPHA_TESTER = discord.Object(id=1374399824392224909)
