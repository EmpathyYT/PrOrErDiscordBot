import asyncio
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

from cogs.views.bug_vote_dynamic_item import BugVoteDynamicItem
from cogs.views.confirm_view import ConfirmView
from cogs.views.download_button import GithubReleaseDownload
from cogs.views.suggestion_vote_dynamic_item import SuggestionVoteDynamicItem
from utils.bot_logging import setup_logging

load_dotenv()

updates_channel_id = discord.Object(id=1367019660142448674)
guild_id = discord.Object(id=os.getenv('GUILD_ID'))
app_tester_role_id = discord.Object(id=1373542685243080704)


def download_link_builder(data, tag) -> str:
    repository = data['repository']['name']
    file_name = data['release']['assets'][0]['name']
    return \
        f'https://github.com/{repository}/releases/download/{tag}/{file_name}'


class PrOrErClient(commands.Bot):
    def __init__(self):
        self.cogs_to_load = "cogs"
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='', intents=intents)

    async def setup_hook(self):
        setup_logging()
        await self.load_cogs()
        self.add_view(ConfirmView())
        self.add_dynamic_items(BugVoteDynamicItem)
        self.add_dynamic_items(SuggestionVoteDynamicItem)
        # self.tree.copy_global_to(guild=guild_id)
        # self.tree.clear_commands(guild=guild_id)
        # self.tree.clear_commands(guild=None)
        await self.tree.sync(guild=None)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def load_cogs(self):
        for filename in os.listdir(self.cogs_to_load):
            if filename.endswith('.py'):
                await self.load_extension(f'{self.cogs_to_load}.{filename[:-3]}')

    async def on_github_hook(self, data):
        await asyncio.sleep(480) # sleep for 8 minutes to allow for the build to finish
        release = data['release']
        release_tag = release['tag_name']
        author = data['repository']['owner']['login']
        release_body = release['body']

        download = download_link_builder(data, release_tag)

        embed = discord.Embed(title=f"New Alpha Release",
                              description=
                              f'\n\n**Change Log**: {release_body[:3000]}'
                              f'\n**Version:** {release_tag}\n\n',
                              color=discord.Color.blurple())
        embed.set_footer(text=f"Authored by {author}\n"
                              f"Press the button below to download the new alpha release of PrOrEr.")
        channel = self.get_channel(updates_channel_id.id)
        await channel.send(f'<@&{app_tester_role_id.id}> ', embed=embed, view=GithubReleaseDownload(link=download))
