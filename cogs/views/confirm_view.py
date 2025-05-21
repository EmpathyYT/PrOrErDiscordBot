import os

import discord
from discord import Interaction
from dotenv import load_dotenv
from enum import Enum

from cogs.views.bug_vote_dynamic_item import BugVoteDynamicItem
from cogs.views.suggestion_vote_dynamic_item import SuggestionVoteDynamicItem

load_dotenv()


class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id='confirm_button')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.reply("Confirmed!")
        channel = self.get_channel_to_send_to(interaction)
        view, footer = self.get_appropriate_view(channel, interaction)
        embed = interaction.message.embeds[0]
        embed.set_footer(text=footer)
        await interaction.guild.get_channel(channel.value.id).send(
            embed=embed,
            view=view,
        )
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

    def get_appropriate_view(self, channel, interaction) -> (discord.ui.View, str):
        view = discord.ui.View(timeout=None)
        footer = ''
        match channel:
            case Channels.BUG_REPORT:
                view.add_item(BugVoteDynamicItem(interaction.user.id, 'Report Bug',
                                                 [str(interaction.user.id)], '🪲'))
                footer = 'This bug has been reported by 1 person.'

            case Channels.SUGGESTION:
                view.add_item(SuggestionVoteDynamicItem(interaction.user.id, 'Suggest Feature',
                                                        [str(interaction.user.id)], '⬆️'))
                footer = 'This suggestion is requested by 1 person.'

            case Channels.ALPHA_TESTER:
                view.add_item(SuggestionVoteDynamicItem(interaction.user.id, 'Suggest Feature',
                                                 [str(interaction.user.id)], '⬆️'))
                footer = 'This suggestion is requested by 1 person.'

        return view, footer


class Channels(Enum):
    BUG_REPORT = discord.Object(id=1374419412924371065)
    SUGGESTION = discord.Object(id=1374432042988732578)
    ALPHA_TESTER = discord.Object(id=1374399824392224909)
