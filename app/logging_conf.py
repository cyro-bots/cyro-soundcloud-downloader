import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import settings


def setup_logging():
    # Ensure log directory exists
    log_dir = Path(settings.LOGGING_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Filename based on current date
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{today}.log"

    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"

    # Root logger configuration
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                filename=log_file,
                mode="a",  # append if exists
                maxBytes=5_000_000,  # 5 MB per file
                backupCount=5,  # keep 5 backups
                encoding="utf-8",
            ),
        ],
    )

    # Optional: silence noisy libraries
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.dialects").setLevel(logging.WARNING)

    logger = logging.getLogger("bot")
    logger.info(f"Logging is configured. Log file: {log_file}")

    return logger
