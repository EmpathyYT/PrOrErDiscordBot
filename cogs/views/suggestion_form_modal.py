import discord

from cogs.views.base_modal import BaseModal


class SuggestionFormModal(BaseModal):
    def __init__(self, bot, channel):
        super().__init__(
            title="New Feature Request Submittal",
            description="Please fill out the form below to request a submittal.",
            color=discord.Color.blurple(),
            channel=channel,
            bot=bot
        )
        self.build_ui()

    async def on_submit(self, interaction: discord.Interaction):
        await super().custom_on_submit(
            interaction.user,
            f"Title: {self.children[0]}\n"
            f"Description: {self.children[1]}\n"
        )
        await interaction.response.send_message(
            "Thank you for your request! We will look into it as soon as possible.",
            ephemeral=True
        )

    def build_ui(self):
        self.add_item(discord.ui.TextInput(label="Feature title", style=discord.TextStyle.short))
        self.add_item(discord.ui.TextInput(label="More detailed information", style=discord.TextStyle.long))
