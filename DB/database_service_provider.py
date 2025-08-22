class DBServiceProvider:
    def __init__(self, db_path = None):
        self.db_path = db_path

    async def initialize(self):
        pass

    async def add_bug_user(self, report_id, user_id):
        pass

    async def remove_bug_user(self, report_id, user_id):
        pass

    async def get_bug_users(self, report_id):
        pass

    async def add_feature_user(self, report_id, user_id):
        pass

    async def remove_feature_user(self, report_id, user_id):
        pass

    async def get_feature_users(self, report_id):
        pass

    async def create_bug_report(self, message_id, is_closed_alpha):
        pass

    async def create_feature_request(self, message_id):
        pass

    async def get_bug_report(self, report_id):
        pass

    async def get_feature_request(self, report_id):
        pass

