import discord
import motor.motor_asyncio as motor
from typing import Optional, List


class Database:
    def __init__(self, url: str):
        self.cluster = motor.AsyncIOMotorClient(url)
        self.db = self.cluster['cluster0']
        self.channel_logs = self.db['channel_logs']
        self.blacklist_data = self.db['blacklists']
        self.blacklist_cache = []


    async def blacklist(self, user_id: int, reason: str):
        return await self.blacklist_data.update_one(
            filter={"_id": user_id},
            update={"$set": {"reason": reason}},
            upsert=True
        )

    async def unblacklist(self, user_id: int):
        return await self.blacklist_data.delete_one({"_id": user_id})

    async def get_blacklist_cache(self):
        cursor = self.blacklist_data.find({})
        list_of_docs = await cursor.to_list(length=None)
        self.blacklist_cache = [e['_id'] for e in list_of_docs]

    async def set_channel(self):
        return await self.channel_logs.update_one(
            filter={"_id": "guild_id"},
            update={"$set": {"channel_id": "channel_id"}},
            upsert=True
        )
