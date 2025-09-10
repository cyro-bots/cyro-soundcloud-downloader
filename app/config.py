from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DEBUG: bool = False

    PROXY: str = ""

    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "secret"
    DB_NAME: str = "soundcloud_bot"

    DOWNLOAD_DIR: str = "downloads"
    LOGGING_DIR: str = "logs"

    DEFAULT_LANG: str = "en"

    MAX_CONCURRENT_DOWNLOADS: int = 3

    class Config:
        env_file = ".env"


settings = Settings()
