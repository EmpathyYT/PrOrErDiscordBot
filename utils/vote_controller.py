from discord import User
import bot_main


class VoteController:
    def __init__(self, owner_id, emoji, title):
        self.owner_id = owner_id
        self.emoji = emoji
        self.title = title
        self.db_provider = bot_main.PrOrErClient.provider

    def log_user_vote(self, user: User, title) -> str:
        pass

    async def add_user_vote(self, report_id, user_id):
        pass

    async def initialize(self, message_id: int) -> int:
        pass

    async def remove_user_vote(self, report_id, user_id):
        pass

    async def get_user_votes(self, report_id):
        pass

    def message_gen(self, count) -> str:
        pass

    def get_style(self):
        pass

    def get_emoji(self) -> str:
        return self.emoji

    def get_title(self) -> str:
        return self.title
