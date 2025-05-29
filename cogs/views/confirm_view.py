import os
import re
from typing import Tuple

import discord
from discord import Interaction
from dotenv import load_dotenv
from enum import Enum

from cogs.views.vote_button import VoteButton

load_dotenv()


class ConfirmView(discord.ui.View):
    def __init__(self, initial_user_id: int = None):
        super().__init__(timeout=None)
        self.initial_user_id = initial_user_id

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id='confirm_button')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.reply("Confirmed!")
        channel = get_channel_to_send_to(interaction)
        embed = interaction.message.embeds[0]
        message = await interaction.guild.get_channel(channel.value.id).send(
            embed=embed,
        )
        view, footer, report_id = await self.initialize_view(channel, interaction, message.id)
        embed.set_footer(text=footer)
        embed.title += f" #{report_id}"
        await message.edit(embed=embed, view=view)
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

    async def initialize_view(self, channel, interaction, message_id) -> Tuple[discord.ui.View, str, int]:
        view = discord.ui.View(timeout=None)
        button: VoteButton | None = None
        report_id: int | None = None
        if self.initial_user_id is None:
            self.initial_user_id = int(re.findall(r'\d+', interaction.message.content)[0])

        initial_params = (self.initial_user_id, [self.initial_user_id])

        match channel:
            case Channels.BUG_REPORT:
                button, report_id = await VoteButton.initialize(*initial_params, 0, message_id)

            case Channels.SUGGESTION:
                button, report_id = await VoteButton.initialize(*initial_params, 1, message_id)

            case Channels.ALPHA_TESTER:
                button, report_id = await VoteButton.initialize(*initial_params, 1, message_id)

        view.add_item(button)
        return view, button.get_message(), report_id


class Channels(Enum):
    BUG_REPORT = discord.Object(id=1374419412924371065)
    SUGGESTION = discord.Object(id=1374432042988732578)
    ALPHA_TESTER = discord.Object(id=1374399824392224909)


def get_channel_to_send_to(interaction):
    # return Channels.ALPHA_TESTER
    if "Bug Report" in interaction.message.embeds[0].title:
        return Channels.BUG_REPORT
    else:
        return Channels.SUGGESTION
