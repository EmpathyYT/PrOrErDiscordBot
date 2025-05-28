from DB.database_service_provider import DBServiceProvider
import aiosqlite


class SQLiteServiceProvider(DBServiceProvider):
    def __init__(self, db_path):
        super().__init__(self)
        self.db_path = db_path

    async def initialize(self):
        pass

    async def execute_query(self, query, params=None):
        async with aiosqlite.connect(self.db_path) as conn:
            if params:
                await conn.execute(query, params)
            else:
                await conn.execute(query)
            await conn.commit()

    async def fetch_all(self, query, params=None):
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.execute(query, params or ()) as cursor:
                return await cursor.fetchall()

    async def fetch_one(self, query, params=None):
        async with aiosqlite.connect(self.db_path) as conn:
            async with conn.execute(query, params or ()) as cursor:
                return await cursor.fetchone()

    async def add_bug_user(self, message_id, user_id):
        query = "INSERT INTO bug_users (message_id, user_id) VALUES (?, ?)"
        await self.execute_query(query, (message_id, user_id))

    async def remove_bug_user(self, message_id, user_id):
        query = "DELETE FROM bug_users WHERE message_id = ? AND user_id = ?"
        await self.execute_query(query, (message_id, user_id))

    async def get_bug_users(self, message_id) -> list[int]:
        query = "SELECT user_id FROM bug_users WHERE message_id = ?"
        rows = await self.fetch_all(query, (message_id,))
        rows = [int(row[0]) for row in rows]
        return rows

    async def add_feature_user(self, message_id, user_id):
        query = "INSERT INTO suggestion_users (message_id, user_id) VALUES (?, ?)"
        await self.execute_query(query, (message_id, user_id))

    async def remove_feature_user(self, message_id, user_id):
        query = "DELETE FROM suggestion_users WHERE message_id = ? AND user_id = ?"
        await self.execute_query(query, (message_id, user_id))

    async def get_feature_users(self, message_id):
        query = "SELECT user_id FROM suggestion_users WHERE message_id = ?"
        rows = await self.fetch_all(query, (message_id,))
        rows = [int(row[0]) for row in rows]
        return rows
