import re


def is_soundcloud_url(url: str) -> bool:
    """Basic validation for SoundCloud URLs"""
    pattern = r"(https:\/\/|http:\/\/)(on\.|m\.|)soundcloud\.com\/.+"
    return bool(re.match(pattern, url))
