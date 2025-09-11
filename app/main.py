import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

from . import logger
from .config import settings
from .database import init_db
from .handlers.callbacks import router as callbacks_router
from .handlers.commands import router as commands_router
from .handlers.messages import router as messages_router
from .i18n import i18n_middleware
from .services.downloader import SoundCloudDownloader


async def main():
    if settings.PROXY:
        session = AiohttpSession(proxy=settings.PROXY)
    else:
        session = None

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    downloader = SoundCloudDownloader(settings.PROXY, debug=settings.DEBUG)
    dp = Dispatcher(downloader=downloader)
    dp.update.middleware(i18n_middleware)

    # Create tables
    await init_db()

    # Include routers
    dp.include_router(commands_router)
    dp.include_router(callbacks_router)
    dp.include_router(messages_router)

    logger.info("Bot is starting...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
