# services/settings_service.py

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["media_bot"]

async def get_admin_ids() -> list[int]:
    doc = await db.settings.find_one({"_id": "admins"})
    return doc["user_ids"] if doc else []

async def get_required_channels() -> list[int]:
    doc = await db.settings.find_one({"_id": "channels"})
    return doc["channel_ids"] if doc else []

async def add_admin(user_id: int):
    await db.settings.update_one(
        {"_id": "admins"},
        {"$addToSet": {"user_ids": user_id}},
        upsert=True
    )

async def add_required_channel(channel_id: int):
    await db.settings.update_one(
        {"_id": "channels"},
        {"$addToSet": {"channel_ids": channel_id}},
        upsert=True
    )
