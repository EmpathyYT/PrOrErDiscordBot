from DB.database_service_provider import DBServiceProvider


class DBServiceController(DBServiceProvider):
    def __init__(self, *, provider: DBServiceProvider, db_path=None):
        super().__init__(db_path)
        self.db_path = db_path
        self.provider = provider

    async def initialize(self):
        await self.provider.initialize()

    async def add_bug_user(self, report_id, user_id):
        await self.provider.add_bug_user(report_id, user_id)

    async def remove_bug_user(self, report_id, user_id):
        await self.provider.remove_bug_user(report_id, user_id)

    async def get_bug_users(self, report_id):
        return await self.provider.get_bug_users(report_id)

    async def add_feature_user(self, report_id, user_id):
        await self.provider.add_feature_user(report_id, user_id)

    async def remove_feature_user(self, report_id, user_id):
        await self.provider.remove_feature_user(report_id, user_id)

    async def get_feature_users(self, report_id):
        return await self.provider.get_feature_users(report_id)

    async def create_bug_report(self, message_id):
        return await self.provider.create_bug_report(message_id)

    async def create_feature_request(self, message_id):
        return await self.provider.create_feature_request(message_id)

    async def get_bug_report(self, report_id):
        return await self.provider.get_bug_report(report_id)

    async def get_feature_request(self, report_id):
        return await self.provider.get_feature_request(report_id)
