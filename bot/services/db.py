# services/db.py

from motor.motor_asyncio import AsyncIOMotorClient
from data.config import MONGO_URI
from datetime import datetime, timezone

client = AsyncIOMotorClient(MONGO_URI)
db = client.anime_bot  # <-- bazaning nomi
users_collection = db.users


async def   get_or_create_user(user_id: int, full_name: str, language_code: str) -> tuple[dict, bool]:
    """
    Foydalanuvchini bazadan topadi yoki yaratadi.
    :return: (user_data, created=True/False)
    """
    user = await users_collection.find_one({"user_id": user_id})

    if user:
        return user, False

    new_user = {
        "user_id": user_id,
        "full_name": full_name,
        "language_code": language_code,
        "xp": 0,
        "referrals": 0,
        "joined_channels": [],
        "rank": "E",
        "created_at": datetime.now(timezone.utc)
    }

    await users_collection.insert_one(new_user)
    # services/db.py ichida yoki Mongo shellda bir marta qo‘shilsa kifoya:
    await db.configs.insert_one({
    "_id": "xp_config",
    "ranks": [
        {"name": "SSS", "min_xp": 5000},
        {"name": "SS", "min_xp": 3000},
        {"name": "S", "min_xp": 1500},
        {"name": "A", "min_xp": 900},
        {"name": "B", "min_xp": 500},
        {"name": "C", "min_xp": 250},
        {"name": "D", "min_xp": 100},
        {"name": "E", "min_xp": 0}
    ]
})

    return new_user, True


async def update_user_xp(user_id: int, xp_amount: int) -> None:
    """
    Foydalanuvchining XP sini belgilangan miqdorga oshiradi.
    """
    await users_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"xp": xp_amount}}
    )


