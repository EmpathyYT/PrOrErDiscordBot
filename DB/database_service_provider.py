class DBServiceProvider:
    def __init__(self, db_path):
        self.db_path = db_path

    async def add_bug_user(self, message_id, user_id):
        pass

    async def remove_bug_user(self, message_id, user_id):
        pass

    async def get_bug_users(self, message_id):
        pass

    async def add_feature_user(self, message_id, user_id):
        pass

    async def remove_feature_user(self, message_id, user_id):
        pass

    async def get_feature_users(self, message_id):
        pass
