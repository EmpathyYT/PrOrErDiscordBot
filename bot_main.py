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
from utils.bot_logging import setup_logging

load_dotenv()

version_tracker_channel = discord.Object(id=1384565719953571892)
updates_channel = discord.Object(id=1367019660142448674)
guild = discord.Object(id=os.getenv('GUILD_ID'))
app_tester_role = discord.Object(id=1373542685243080704)


def download_link_builder(data, tag, file_name) -> str:
    repository = data['repository']['full_name']
    return \
        f'https://github.com/{repository}/releases/download/{tag}/{file_name}'


class PrOrErClient(commands.Bot):
    provider: DBServiceController = DBServiceController(provider=SupabaseServiceProvider())

    def __init__(self):
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
        # await self.tree.sync(guild=None)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def load_cogs(self):
        for filename in os.listdir(self.cogs_to_load):
            if filename.endswith('.py'):
                await self.load_extension(f'{self.cogs_to_load}.{filename[:-3]}')

    async def on_github_hook(self, data):
        await asyncio.sleep(60)
        release = data['release']
        release_tag = release['tag_name']
        author = data['repository']['owner']['login']
        release_body = release['body']
        file_name = await self.get_release(release_tag)
        download = download_link_builder(data, release_tag, file_name)
        embed = discord.Embed(title=f"New Alpha Release",
                              description=
                              f'\n\n**Change Log**: {release_body[:3000]}'
                              f'\n**Version:** {release_tag}\n\n',
                              color=discord.Color.blurple())
        embed.set_footer(text=f"Authored by {author}\n"
                              f"Press the button below to download the new alpha release of PrOrEr.")
        channel = self.get_channel(updates_channel.id)
        version_tracker = self.get_channel(version_tracker_channel.id)
        await channel.send(f'<@&{app_tester_role.id}> ', embed=embed, view=GithubReleaseDownload(link=download))
        await version_tracker.edit(name=f'Latest Version: {release_tag}')


    async def get_release(self, tag):
        releases = self.github.get_release(tag)
        for asset in releases.get_assets():
            if asset.name.endswith('.apk'):
                return asset.name

        return None
