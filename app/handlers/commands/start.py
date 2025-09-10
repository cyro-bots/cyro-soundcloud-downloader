from aiogram import F
from aiogram.types import Message

from app.database.models import User
from app.keyboards.reply import get_language_keyboard
from app.texts import Commands, Messages

from . import router


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    from_user = message.from_user

    chat_id = from_user.id
    fullname = from_user.full_name
    username = from_user.username

    user, created = await User.get_or_create(chat_id, fullname, username)

    if not created and user.language:
        keyboard = None
        text = Commands.START.format(fullname=fullname)
    else:
        keyboard = get_language_keyboard()
        text = str(Messages.SELECT_LANGUAGE)

    await message.answer(text, reply_markup=keyboard)
