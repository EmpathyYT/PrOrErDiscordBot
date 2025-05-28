import os

from dotenv import load_dotenv
from supabase._async.client import AsyncClient as Client, create_client

from DB.database_service_provider import DBServiceProvider
from constants import bug_users_table, message_id_field_name, user_id_field_name, feature_users_table

load_dotenv()


class SupabaseServiceProvider(DBServiceProvider):
    def __init__(self, db_path=None):
        super().__init__(db_path)
        self.client: Client | None = None

    async def initialize(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        self.client: Client = await create_client(url, key)

    async def add_bug_user(self, message_id, user_id):
        data = {
            message_id_field_name: message_id,
            user_id_field_name: user_id
        }
        await self.client.from_(bug_users_table).insert(data).execute()

    async def remove_bug_user(self, message_id, user_id):
        await self.client.from_(bug_users_table).delete().match({
            message_id_field_name: message_id,
            user_id_field_name: user_id
        }).execute()

    async def get_bug_users(self, message_id):
        response = await self.client.from_(bug_users_table).select(user_id_field_name).eq(message_id_field_name,
                                                                                          message_id).execute()
        return [user[user_id_field_name] for user in response.data] if response.data else []

    async def add_feature_user(self, message_id, user_id):
        data = {
            message_id_field_name: message_id,
            user_id_field_name: user_id
        }
        await self.client.from_(feature_users_table).insert(data).execute()

    async def remove_feature_user(self, message_id, user_id):
        await self.client.from_(feature_users_table).delete().match({
            message_id_field_name: message_id,
            user_id_field_name: user_id
        }).execute()

    async def get_feature_users(self, message_id):
        response = await self.client.from_(feature_users_table).select(user_id_field_name).eq(message_id_field_name,
                                                                                              message_id).execute()
        return [user[user_id_field_name] for user in response.data] if response.data else []
