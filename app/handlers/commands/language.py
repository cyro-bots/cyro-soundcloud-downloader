from aiogram import F
from aiogram.types import Message

from app.keyboards.reply import get_language_keyboard
from app.texts import Messages

from . import router


@router.message(F.text == "/language")
async def cmd_start(message: Message):
    keyboard = get_language_keyboard()
    text = str(Messages.SELECT_LANGUAGE)
    await message.answer(text, reply_markup=keyboard)
