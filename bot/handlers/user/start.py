# handlers/user/start.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.keyboards.language_keyboard import get_language_keyboard
from bot.services.db import get_user, create_user
from bot.states.register import RegisterState
from data.config import AVAILABLE_LANGUAGES
from data.texts import texts

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)

    if user:
        lang = user.get("language", "uz")
        await message.answer(texts["already_registered"][lang])
        return

    await message.answer(
        "\n".join([
            texts["choose_language"]["uz"],
            texts["choose_language"]["ru"],
            texts["choose_language"]["en"]
        ]),
        reply_markup=get_language_keyboard()
    )
    await state.set_state(RegisterState.main_menu)


@router.callback_query(RegisterState.main_menu)
async def language_chosen(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    print(lang)

    if lang not in AVAILABLE_LANGUAGES:
        await call.answer("Noto‘g‘ri til!", show_alert=True)
        return

    await state.update_data(language=lang)

    await call.message.edit_text(texts["language_selected"][lang])
    await call.message.answer(texts["welcome"][lang])