from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
