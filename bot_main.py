import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

from cogs.views.confirm_view import ConfirmView
from cogs.views.download_button import GithubReleaseDownload

load_dotenv()

updates_channel_id = discord.Object(id=1367019660142448674)
guild_id = discord.Object(id=os.getenv('GUILD_ID'))
app_tester_role_id = discord.Object(id=1373542685243080704)


class PrOrErClient(commands.Bot):
    def __init__(self):
        self.cogs_to_load = "cogs"
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='', intents=intents)

    async def setup_hook(self):
        await self.load_cogs()
        self.add_view(ConfirmView())
        self.tree.copy_global_to(guild=guild_id)
        await self.tree.sync(guild=guild_id)
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def load_cogs(self):
        for filename in os.listdir(self.cogs_to_load):
            if filename.endswith('.py'):
                await self.load_extension(f'{self.cogs_to_load}.{filename[:-3]}')

    async def on_github_hook(self, data):
        release = data['release']
        release_tag = release['tag_name']
        author = release['author']['login']
        release_body = release['body']
        assets = release.get('assets', [])

        if not assets:
            return

        download = release['assets'][0]['browser_download_url']
        embed = discord.Embed(title=f"New Alpha Release",
                              description=
                              f'\n\n**Change Log**: {release_body[:3000]}'
                              f'\n**Version:** {release_tag}\n\n',
                              color=discord.Color.blurple())
        embed.set_footer(text=f"Authored by {author}\n"
                              f"Press the button below to download the new alpha release of PrOrEr.")
        channel = self.get_channel(updates_channel_id.id)
        await channel.send(f'<@&{app_tester_role_id.id}> ', embed=embed, view=GithubReleaseDownload(link=download))
