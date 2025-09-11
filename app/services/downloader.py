import asyncio
import os
import shutil
from typing import Any, Dict, List, Optional

import yt_dlp

from app import logger
from app.config import settings


class SoundCloudDownloader:
    def __init__(
        self, proxy: Optional[str] = None, debug: Optional[bool] = False
    ):
        self._ffmpeg_path = self._find_ffmpeg()
        self._proxy = proxy
        self._debug = debug
        logger.info(f"FFmpeg path: {self._ffmpeg_path}")
        if self._proxy:
            logger.info(f"Using proxy: {self._proxy}")

    @staticmethod
    def _find_ffmpeg() -> str:
        try:
            return shutil.which("ffmpeg") or "ffmpeg"
        except Exception as e:
            logger.error(f"FFmpeg detection failed: {str(e)}")
            return "ffmpeg"

    def _base_opts(
        self, download: bool = False, format_id: Optional[str] = None
    ) -> Dict[str, Any]:
        opts: Dict[str, Any] = {
            "quiet": True,
            "noplaylist": True,
            "ffmpeg_location": self._ffmpeg_path,
            "socket_timeout": 15,
            "verbose": self._debug,
        }

        if self._proxy:
            opts["proxy"] = self._proxy

        if download:
            opts.update(
                {
                    "format": format_id or "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                    "outtmpl": os.path.join(
                        settings.DOWNLOAD_DIR, "%(title)s_%(id)s.%(ext)s"
                    ),
                    "overwrites": True,
                }
            )
        else:
            opts["simulate"] = True

        return opts

    async def get_track_info(self, url: str) -> dict:
        """Return metadata and formats in one dict."""

        def _extract():
            with yt_dlp.YoutubeDL(self._base_opts(download=False)) as ydl:
                return ydl.extract_info(url, download=False)

        return await asyncio.to_thread(_extract)

    async def get_available_formats(self, info: dict) -> List[Dict[str, Any]]:
        """Take already extracted info dict and return audio-only formats."""
        formats = []
        for fmt in info.get("formats", []):
            if fmt.get("acodec") or fmt.get("vcodec") == "none":  # audio-only
                formats.append(
                    {
                        "format_id": fmt.get("format_id", "unknown"),
                        "ext": fmt.get("ext", "unknown"),
                        "abr": fmt.get("abr", fmt.get("tbr", 0)),
                        "protocol": fmt.get("protocol", ""),
                        "filesize": fmt.get("filesize") or 0,
                        "url": fmt.get("url", ""),
                    }
                )
        return formats

    async def download_format(
        self, info: dict, format_id: str
    ) -> Optional[str]:
        """Download using an existing info dict to avoid re-extraction."""

        def _download():
            opts = self._base_opts(download=True, format_id=format_id)
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Actually download using the URL from info
                result = ydl.extract_info(
                    info.get("webpage_url"), download=True
                )
                # Get the real file path (after postprocessor changes)
                file_path = ydl.prepare_filename(result)
                postprocessors = opts.get("postprocessors", [])
                if postprocessors:
                    preferred_codec = postprocessors[0].get("preferredcodec")
                    if result.get("ext") != preferred_codec:
                        base, _ = file_path.rsplit(".", 1)
                        file_path = f"{base}.{preferred_codec}"

                return file_path

        file_path = await asyncio.to_thread(_download)
        logger.info(f"Downloaded file: {file_path}")
        return file_path

    async def download_best_format(self, info: dict) -> Optional[str]:
        formats = await self.get_available_formats(info)
        if not formats:
            logger.error("No audio formats available for this track")
            return None

        mp3_formats = [f for f in formats if f.get("ext") == "mp3"]
        if mp3_formats:
            best_format = max(mp3_formats, key=lambda f: f.get("abr", 0))
        else:
            best_format = max(formats, key=lambda f: f.get("abr", 0))

        format_id = best_format.get("format_id")
        if not format_id:
            logger.error("Best format has no format_id")
            return None

        os.makedirs(settings.DOWNLOAD_DIR, exist_ok=True)

        return await self.download_format(info, format_id)
