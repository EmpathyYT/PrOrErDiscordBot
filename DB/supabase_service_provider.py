import os

from dotenv import load_dotenv
from supabase._async.client import AsyncClient as Client, create_client

from DB.database_service_provider import DBServiceProvider
from constants import *
from models.submittal_object import SubmittalObject

load_dotenv()


class SupabaseServiceProvider(DBServiceProvider):
    def __init__(self, db_path=None):
        super().__init__(db_path)
        self.client: Client | None = None
        self.app_client: Client | None = None

    async def initialize(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        app_url = os.getenv('APP_SUPABASE_URL')
        app_key = os.getenv('APP_SUPABASE_KEY')
        self.app_client = await create_client(app_url, app_key)
        self.client = await create_client(url, key)

    async def add_bug_user(self, report_id, user_id):
        data = {
            bug_report_id_field_name: report_id,
            user_id_field_name: user_id
        }
        await self.client.from_(bug_users_table).insert(data).execute()

    async def remove_bug_user(self, report_id, user_id):
        await self.client.from_(bug_users_table).delete().match({
            bug_report_id_field_name: report_id,
            user_id_field_name: user_id
        }).execute()

    async def get_bug_users(self, report_id):
        response = await self.client.from_(bug_users_table).select(user_id_field_name).eq(bug_report_id_field_name,
                                                                                          report_id).execute()
        return [user[user_id_field_name] for user in response.data] if response.data else []

    async def add_feature_user(self, report_id, user_id):
        data = {
            feature_request_id_field_name: report_id,
            user_id_field_name: user_id
        }
        await self.client.from_(feature_users_table).insert(data).execute()

    async def remove_feature_user(self, report_id, user_id):
        await self.client.from_(feature_users_table).delete().match({
            feature_request_id_field_name: report_id,
            user_id_field_name: user_id
        }).execute()

    async def get_feature_users(self, report_id):
        response = await self.client.from_(feature_users_table).select(user_id_field_name).eq(
            feature_request_id_field_name,
            report_id).execute()
        return [user[user_id_field_name] for user in response.data] if response.data else []

    async def create_bug_report(self, message_id, is_closed_alpha=False):
        data = {
            message_id_field_name: message_id,
            closed_alpha_field_name: is_closed_alpha
        }
        data = await self.client.from_(bug_reports_table).insert(data).execute()
        return data.data[0][id_field_name] if data.data else None

    async def create_feature_request(self, message_id):
        data = {
            message_id_field_name: message_id,
        }
        data = await self.client.from_(feature_requests_table).insert(data).execute()
        return data.data[0][id_field_name] if data.data else None

    async def get_bug_report(self, report_id):
        response = await self.client.from_(bug_reports_table).select().eq(id_field_name, report_id).execute()
        return SubmittalObject.from_dict(response.data[0]) if response.data else None

    async def get_feature_request(self, report_id):
        response = await self.client.from_(feature_requests_table).select().eq(id_field_name, report_id).execute()
        return SubmittalObject.from_dict(response.data[0]) if response.data else None
    
    async def add_version_to_app_db(self, version):
        data = {
            app_versions_field_name: version,
            outdated_field_name: False
        }
        await self.app_client.from_(app_versions_table).insert(data).execute()

    async def outdate_previous_versions(self, version):
        await self.app_client.from_(app_versions_table).update({outdated_field_name: True}).neq(app_versions_field_name, version).execute()

    async def outdate_version(self, version):
        await self.app_client.from_(app_versions_table).update({outdated_field_name: True}).eq(app_versions_field_name, version).execute()

    async def allow_version(self, version):
        await self.app_client.from_(app_versions_table).update({outdated_field_name: False}).eq(app_versions_field_name, version).execute()
    