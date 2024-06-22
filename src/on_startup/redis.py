from redis.asyncio import ConnectionPool, Redis

from src.conf.config import settings
from src.integrations.redis import redis


async def start_redis() -> None:
    pool = ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
    )
    redis.redis = Redis(
        connection_pool=pool,
    )
