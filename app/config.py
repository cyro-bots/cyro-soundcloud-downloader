from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Bot ---
    BOT_TOKEN: str
    DEBUG: bool = False
    PROXY: str = ""

    # --- Database ---
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "secret"
    DB_NAME: str = "soundcloud_bot"

    # --- Files & logging ---
    DOWNLOAD_DIR: str = "downloads"
    LOGGING_DIR: str = "logs"

    # --- Defaults ---
    DEFAULT_LANG: str = "en"
    MAX_CONCURRENT_DOWNLOADS: int = 3

    # --- Admins ---
    # Example .env: ADMINS=[123545345,123456789]
    ADMINS: List[int] = []

    class Config:
        env_file = ".env"


# --- Create settings instance ---
settings = Settings()
