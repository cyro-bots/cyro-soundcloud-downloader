import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from yt_dlp import YoutubeDL

from ..config import settings

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=2)

YTDLP_OPTS = {
    "format": "bestaudio/best",
    "outtmpl": str(Path(settings.DOWNLOAD_DIR) / "%(title)s - %(id)s.%(ext)s"),
    "quiet": True,
    "no_warnings": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


def _download_sync(url: str) -> dict:
    """Blocking download using yt-dlp Python API."""
    with YoutubeDL(YTDLP_OPTS) as ydl:
        info = ydl.extract_info(url, download=True)
    return info


async def download(url: str) -> dict:
    loop = asyncio.get_running_loop()
    logger.info("Scheduling download for %s", url)
    result = await loop.run_in_executor(_executor, _download_sync, url)
    return result
