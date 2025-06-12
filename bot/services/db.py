from motor.motor_asyncio import AsyncIOMotorClient
from data.config import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.anime_bot

async def get_user(user_id: int):
    return await db.users.find_one({"user_id": user_id})


async def create_user(user_id: int, full_name: str, language: str) -> None:
    """
    Foydalanuvchini bazaga qo‘shadi.
    """
    user_data = {
        "user_id": user_id,
        "full_name": full_name,
        "language": language,
        "xp": 0,
        "rank": "E"
    }
    await db.users.insert_one(user_data)

async def update_user_xp(user_id: int, amount: int) -> None:
    """
    XP miqdorini foydalanuvchiga qo‘shadi.
    """
    await db.users.update_one({"user_id": user_id}, {"$inc": {"xp": amount}})
