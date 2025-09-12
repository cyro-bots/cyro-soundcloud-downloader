from aiogram import F
from aiogram.types import Message

from app.filters.filters import IsAdminFilter
from app.keyboards.inline import get_admin_keyboard
from app.texts import Messages

from . import router


# --- /admin command ---
@router.message((F.text == "/admin"), IsAdminFilter())
async def admin_menu(message: Message):
    keyboard = get_admin_keyboard()
    await message.reply(str(Messages.ADMIN_WELCOME), reply_markup=keyboard)
