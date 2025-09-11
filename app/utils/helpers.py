import re


def sanitize_filename(s: str) -> str:
    """Replace illegal characters in filenames."""
    return re.sub(r"[\\/<>:\"|?*]", "_", s)
