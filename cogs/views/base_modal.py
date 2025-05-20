import discord
from discord.ext import commands

from cogs.views.confirm_view import ConfirmView


class BaseModal(discord.ui.Modal):
    def __init__(self, title: str, description: str, color: discord.Color, channel: int, bot: commands.Bot):
        super().__init__(title=title, timeout=300)
        self.description = description
        self.title = title
        self.channel = channel
        self.color = color
        self.bot = bot

    async def custom_on_submit(self, user: discord.User, modal_response: str):
        embed = discord.Embed(
            title=self.title,
            description=modal_response,
            color=self.color
        )
        await self.bot.get_channel(self.channel).send( f"Submittal by {user.mention}",embed=embed, view=ConfirmView())
