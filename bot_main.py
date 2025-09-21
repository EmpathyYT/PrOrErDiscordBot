import asyncio
import os

import discord
from discord.ext import commands

from dotenv import load_dotenv
from github import Github

from DB.database_service_controller import DBServiceController
from DB.supabase_service_provider import SupabaseServiceProvider
from cogs.views.confirm_view import ConfirmView
from cogs.views.download_button import GithubReleaseDownload

from cogs.views.vote_button import VoteButton
from constants import *
from models.channel_model import ChannelModel
from utils.bot_logging import setup_logging

load_dotenv()


def download_link_builder(data, tag) -> str:
    repository = data['repository']['full_name']
    return \
        f'https://github.com/{repository}/releases/tag/{tag}'


def get_appropriate_channel(data: ChannelModel) -> discord.Object:
    if data.is_testing:
        return testing_channel
    if data.is_suggestion:
        return feature_request_channel
    elif data.is_closed:
        return closed_bug_report_channel if data.is_bug_report else closed_updates_channel
    else:
        return open_bug_report_channel if data.is_bug_report else open_updates_channel


async def generate_embed(author, release_body, release_tag: str):
    build_number = release_tag.split('alpha.')[1]
    embed = discord.Embed(title=f"New Alpha Release",
                          description=
                          f'\n\n**Change Log**: {release_body[:3800]}'
                          f'\n**Version:** {release_tag}'
                          f'\n**Build:** {build_number}\n\n',
                          color=discord.Color.blurple())
    embed.set_footer(text=f"Authored by {author}\n"
                          f"Press the button below to download the new alpha release of PrOrEr.")
    return embed


class PrOrErClient(commands.Bot):
    provider: DBServiceController = DBServiceController(provider=SupabaseServiceProvider())
    testing: bool

    def __init__(self, is_testing: bool):
        self.testing = is_testing
        self.cogs_to_load = "cogs"
        intents = discord.Intents.default()
        self.github = Github(os.getenv('GITHUB_TOKEN')).get_repo("EmpathyYT/GymTracker")
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='', intents=intents)

    async def setup_hook(self):
        setup_logging()
        await self.load_cogs()
        await self.provider.initialize()
        self.add_view(ConfirmView())
        self.add_dynamic_items(VoteButton)
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
        await asyncio.sleep(60)
        release = data['release']
        release_tag = str(release['tag_name'])
        author = data['repository']['owner']['login']
        release_body = release['body']
        is_closed = "closed" in release_tag.lower()
        if is_closed:
            release_body += '\n\n**Note:** This is a closed alpha release. ' \
                            'It may be highly unstable and could include features that might be removed or changed in future public releases.'

        download = download_link_builder(data, release_tag)
        embed = await generate_embed(author, release_body, release_tag)

        channel = self.get_channel(
            get_appropriate_channel(ChannelModel(is_testing=self.testing, is_release=True, is_closed=is_closed)).id)

        version_tracker = self.get_channel(version_tracker_channel.id)

        await channel.send(f'<@&{app_tester_role.id if not is_closed else closed_tester_role.id}> ', embed=embed,
                           view=GithubReleaseDownload(link=download))
        if not is_closed:
            await version_tracker.edit(name=f'Latest Version: {release_tag}')
