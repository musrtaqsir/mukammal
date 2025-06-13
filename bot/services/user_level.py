# services/user_level.py

from services.db import db

async def get_rank_by_xp(xp: int) -> str:
    """
    XP asosida foydalanuvchi darajasini aniqlaydi.
    Ma'lumot MongoDB'dagi configs kolleksiyasidan olinadi.
    """
    config = await db.configs.find_one({"_id": "xp_config"})
    if not config or "ranks" not in config:
        return "E"  # Default daraja

    ranks = sorted(config["ranks"], key=lambda r: r["min_xp"], reverse=True)

    for rank in ranks:
        if xp >= rank["min_xp"]:
            return rank["name"]

    return "E"
