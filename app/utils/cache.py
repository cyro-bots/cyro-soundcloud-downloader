# app/utils/cache.py
import asyncio
from datetime import datetime, timedelta, timezone


class ChannelCache:
    _channels = []
    _last_refresh = datetime.min.replace(tzinfo=timezone.utc)
    _lock = asyncio.Lock()
    _ttl = timedelta(seconds=60)  # cache refresh every 60 seconds

    @classmethod
    async def get_channels(cls, fetch_func):
        """Returns cached channels, refreshes if expired."""
        async with cls._lock:
            now = datetime.now(timezone.utc)
            if not cls._channels or now - cls._last_refresh > cls._ttl:
                cls._channels = await fetch_func()
                cls._last_refresh = now
            return cls._channels
