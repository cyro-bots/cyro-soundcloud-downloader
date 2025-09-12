from aiogram import F
from aiogram.types import CallbackQuery

from app.database import User
from app.i18n import ctx_locale
from app.texts import Messages

from . import router


@router.callback_query(F.data.startswith("lang_"))
async def set_language_callback(callback: CallbackQuery):
    chat_id = callback.from_user.id
    lang = callback.data.split("_")[1]
    await User.set_user_language(chat_id, lang)
    token = ctx_locale.set(lang)
    try:
        await callback.message.edit_text(str(Messages.LANGUAGE_CHANGED))
        await callback.answer()
    finally:
        ctx_locale.reset(token)
