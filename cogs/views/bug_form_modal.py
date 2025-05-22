import discord

from cogs.views.base_modal import BaseModal


class BugFormModal(BaseModal):
    def __init__(self, bot, channel):
        super().__init__(
            title="New Bug Report Submittal",
            description="Please fill out the form below to report a bug.",
            color=discord.Color.red(),
            channel=channel,
            bot=bot
        )
        self.build_ui()

    async def on_submit(self, interaction: discord.Interaction):
        await super().custom_on_submit(
            interaction.user,
            f"**Bug Description**: {self.children[0]}\n"
            f"**Steps to Reproduce**: {self.children[1]}\n"
            f"**Expected Result**: {self.children[2]}\n"
            f"**Actual Result**: {self.children[3]}"
        )
        await interaction.response.send_message(
            "Thank you for your report! We will look into it as soon as possible.",
            ephemeral=True
        )

    def build_ui(self):
        self.add_item(discord.ui.TextInput(label="Bug Description", style=discord.TextStyle.long))
        self.add_item(discord.ui.TextInput(label="Steps to Reproduce", style=discord.TextStyle.long))
        self.add_item(discord.ui.TextInput(label="Expected Result", style=discord.TextStyle.long))
        self.add_item(discord.ui.TextInput(label="Actual Result", style=discord.TextStyle.long))
