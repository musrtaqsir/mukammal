# handlers/user/start.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from services.db import get_user_by_id, create_user, update_user_lang
from keyboards.language_keyboard import get_language_keyboard
from texts.texts import texts
from datetime import datetime
from services.user_level import get_rank_by_xp

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await get_user_by_id(message.from_user.id)

    if not user:
        # Foydalanuvchini DBga qo‘shamiz va boshlang‘ich XP beramiz
        await create_user(
            user_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            lang_code="none",  # Hozircha til tanlanmagan
            joined_at=datetime.utcnow()
        )

    await message.answer(
        text="Tilni tanlang / Choose your language / Выберите язык:",
        reply_markup=get_language_keyboard()
    )


@router.callback_query(F.data.startswith("lang_"))
async def lang_chosen(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_id = callback.from_user.id

    # Foydalanuvchining tilini yangilaymiz
    await update_user_lang(user_id, lang)

    # Matnlarni tanlangan tilga moslab chiqaramiz
    text = texts["welcome"].get(lang, "Xush kelibsiz!")
    await callback.message.edit_text(text=text)
