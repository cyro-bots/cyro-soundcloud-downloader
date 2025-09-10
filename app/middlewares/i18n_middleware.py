from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18nMiddleware

from app.database.models import User


class CustomI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: dict) -> str:
        """
        Override this to fetch locale from DB/session instead of
        Telegram `language_code`.
        """

        print("##############################")
        print(data)
        print("##############################")
        if "locale" in data:
            return data["locale"]

        user = data.get("event_from_user")
        if user:
            lang = await User.get_user_language(user.id)
            if lang:
                return lang

        return self.i18n.default_locale
