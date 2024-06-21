from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='src/conf/.env', env_file_encoding='utf-8')

    BIND_IP: str
    BIND_PORT: int
    DB_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SECRET_SALT: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_CACHE_PREFIX: str
    CELERY_BROKER_URL: str
    PAGE_LIMIT: int

    BOT_TOKEN: str

settings = Settings()
