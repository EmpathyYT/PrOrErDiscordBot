import discord

from DB.vote_controller import VoteController
from utils.bot_logging import log_message


class SuggestionVoteController(VoteController):
    def __init__(self, owner_id):
        super().__init__(owner_id, '⬆️', 'Suggest Feature')

    def log_user_vote(self, user, title):
        log_message(f"{user.name} has interacted with suggestion feature button\nTitle:{title}")

    async def add_user_vote(self, message_id, user_id):
        await self.db_provider.add_feature_user(message_id, user_id)

    async def remove_user_vote(self, message_id, user_id):
        await self.db_provider.remove_feature_user(message_id, user_id)

    async def get_user_votes(self, message_id):
        return await self.db_provider.get_feature_users(message_id)

    def message_gen(self, count):
        return '1 person is suggesting this feature.' if count == 1 else (f'{count} '
                                                                             f'people are suggesting this feature.')
    def get_style(self):
        return discord.ButtonStyle.green