# main.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from data.config import BOT_TOKEN
from bot.handlers.user import start
# from bot.middlewares.subscription import SubscriptionMiddleware

async def main():
    # 🎯 Bot, dispatcher va FSM storage
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # 🔄 Middleware'ni ulash
    # dp.message.middleware(SubscriptionMiddleware())

    # 🚏 Routerlarni ulash
    dp.include_router(start.router)

    # 🚀 Komandalarni sozlash

    # ✅ Botni ishga tushirish
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
