from DB.database_service_provider import DBServiceProvider


class DBServiceController(DBServiceProvider):
    def __init__(self, *, provider:DBServiceProvider, db_path=None):
        super().__init__(db_path)
        self.db_path = db_path
        self.provider = provider

    async def initialize(self):
        await self.provider.initialize()

    async def add_bug_user(self, message_id, user_id):
        await self.provider.add_bug_user(message_id, user_id)

    async def remove_bug_user(self, message_id, user_id):
        await self.provider.remove_bug_user(message_id, user_id)

    async def get_bug_users(self, message_id):
        return await self.provider.get_bug_users(message_id)

    async def add_feature_user(self, message_id, user_id):
        await self.provider.add_feature_user(message_id, user_id)

    async def remove_feature_user(self, message_id, user_id):
        await self.provider.remove_feature_user(message_id, user_id)

    async def get_feature_users(self, message_id):
        return await self.provider.get_feature_users(message_id)
