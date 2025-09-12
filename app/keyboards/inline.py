from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.texts import Keyboards


def get_back_button():
    return InlineKeyboardButton(
        text="⬅️ Back to menu", callback_data="admin_back_menu"
    )


def get_language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇬🇧 English", callback_data="lang_en"
                ),
                InlineKeyboardButton(text="🇮🇷 فارسی", callback_data="lang_fa"),
            ]
        ]
    )


def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=str(Keyboards.ADMIN_CHANNEL),
                    callback_data="admin_channels",
                )
            ],
        ]
    )
    return keyboard
