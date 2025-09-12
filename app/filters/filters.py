from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.config import settings
from app.database.channels import Channel
from app.utils.cache import ChannelCache


class IsJoinedChannelsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Fetch active channels from cache (auto-refresh)
        active_channels = await ChannelCache.get_channels(
            Channel.get_active_channels
        )
        if not active_channels:
            return True  # no channels configured

        for channel_username in active_channels:
            try:
                member = await message.bot.get_chat_member(
                    chat_id=channel_username, user_id=message.from_user.id
                )
                if member.status not in ["member", "administrator", "creator"]:
                    return False
            except TelegramBadRequest:
                return False

        return True


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        print("IM IN HERE")
        return message.from_user.id in settings.ADMINS
