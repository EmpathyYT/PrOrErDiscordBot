from discord import User

from DB.sqlite_service_provider import SQLiteServiceProvider
from constants import db_path


class VoteController:
    def __init__(self, owner_id, emoji, title):
        self.owner_id = owner_id
        self.emoji = emoji
        self.title = title
        self.db_provider = SQLiteServiceProvider(db_path)

    def log_user_vote(self, user: User, title) -> str:
        pass

    async def add_user_vote(self, message_id, user_id):
        pass

    async def remove_user_vote(self, message_id, user_id):
        pass

    async def get_user_votes(self, message_id):
        pass

    def get_custom_id(self) -> str:
        return f'user:{self.owner_id}'

    def message_gen(self, count) -> str:
        pass

    def get_style(self):
        pass

    def get_emoji(self) -> str:
        return self.emoji

    def get_title(self) -> str:
        return self.title