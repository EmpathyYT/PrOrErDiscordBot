import os

import discord
from discord import Interaction
from dotenv import load_dotenv

load_dotenv()


class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, custom_id='confirm_button')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.reply("Confirmed!")
        channel_id = self.get_channel_to_send_to()

        await interaction.guild.get_channel(channel_id.id).send(
            embed=interaction.message.embeds[0],
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

    def get_channel_to_send_to(self):
        if "Bug Report" in self.children[0].label:
            return discord.Object(id=1374419412924371065)
        else:
            return discord.Object(id=1374432042988732578)
