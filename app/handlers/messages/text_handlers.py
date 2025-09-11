import logging

from aiogram import Dispatcher, F
from aiogram.types import FSInputFile, Message, URLInputFile

from app.services.downloader import SoundCloudDownloader
from app.texts import Messages
from app.utils.helpers import sanitize_filename
from app.utils.validators import is_soundcloud_url

from . import router


@router.message(F.text & ~F.text.startswith("/"))
async def handle_soundcloud_url(message: Message, dispatcher: Dispatcher):
    url = message.text
    downloader: SoundCloudDownloader = dispatcher["downloader"]

    if not is_soundcloud_url(url):
        await message.reply(str(Messages.INVALID_URL))
        return

    loading_message = await message.reply("⏳")

    try:
        info = await downloader.get_track_info(url)

        if not info:
            await message.reply(str(Messages.NO_AUDIO_FORMATS))
            return

        # --- Send artwork and track info ---
        thumbnail = info.get("thumbnail")
        thumbnails = info.get("thumbnails", [{}])

        if thumbnail:
            artwork_url = thumbnail
        else:
            artwork_url = thumbnails[-1].get("url")

        thumbnail_url = None
        for thumbnail in thumbnails:
            thumbnail_url = thumbnail["url"]
            if thumbnail["width"] >= 300:
                break

        title = info.get("title")
        artist = info.get("artist") or info.get("uploader")
        duration = int(info.get("duration", 0))
        duration_string = info.get("duration_string")
        views = info.get("view_count", 0)
        likes = info.get("like_count", 0)
        description = info.get("description", "")

        track_details = (
            f"🎵 <b>{title}</b>\n"
            f"👤 Artist: {artist}\n"
            f"⏱ Duration: {duration_string}\n"
            f"👁 Views: {views}\n"
            f"❤️ Likes: {likes}\n"
            f"📝 Description: {description}"
        )
        await loading_message.delete()

        if artwork_url:
            await message.reply_photo(
                photo=artwork_url, caption=track_details, parse_mode="HTML"
            )
        else:
            await message.reply(track_details, parse_mode="HTML")

        # --- Download best quality format ---
        audio_file_path = await downloader.download_best_format(info)

        if audio_file_path:
            safe_title = sanitize_filename(info.get("title") or "audio")
            audio = FSInputFile(audio_file_path, filename=safe_title)
            artwork = URLInputFile(thumbnail_url)
            await message.answer_audio(
                audio=audio,
                title=safe_title,
                caption=f"🎵 {safe_title} - {artist}",
                duration=duration,
                thumbnail=artwork,
                performer=artist or "Cyro",
            )

    except Exception as e:
        await message.reply(str(Messages.DOWNLOAD_ERROR))
        logging.exception(f"Error handling SoundCloud URL: {e}")
