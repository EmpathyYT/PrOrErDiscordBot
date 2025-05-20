import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')
guild_id = discord.Object(id=os.getenv('GUILD_ID'))


class PrOrErClient(commands.Bot):
    def __init__(self):
        self.cogs_to_load = "cogs"
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='', intents=intents)

    async def setup_hook(self):
        await self.load_cogs()

        self.tree.copy_global_to(guild=guild_id)
        await self.tree.sync(guild=guild_id)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def load_cogs(self):
        for filename in os.listdir(self.cogs_to_load):
            if filename.endswith('.py'):
                await self.load_extension(f'{self.cogs_to_load}.{filename[:-3]}')
