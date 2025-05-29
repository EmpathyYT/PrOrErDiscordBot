import discord

from utils.vote_controller import VoteController
from utils.bot_logging import log_message


class BugVoteController(VoteController):
    def __init__(self, owner_id):
        super().__init__(owner_id, '🪲', 'Report Bug')

    def log_user_vote(self, user, title):
        log_message(f"{user.name} has interacted with bug report button\n{title}")

    async def add_user_vote(self, report_id, user_id):
        await self.db_provider.add_bug_user(report_id, user_id)

    async def remove_user_vote(self, report_id, user_id):
        await self.db_provider.remove_bug_user(report_id, user_id)

    async def get_user_votes(self, report_id):
        return await self.db_provider.get_bug_users(report_id)

    async def initialize(self, message_id: int):
        report_id = await self.db_provider.create_bug_report(message_id)
        await self.add_user_vote(report_id, self.owner_id)
        return report_id

    def message_gen(self, count):
        return '1 person is experiencing this bug.' if count == 1 else (f'{count} '
                                                                             f'people are experiencing this bug.')
    def get_style(self):
        return discord.ButtonStyle.red
