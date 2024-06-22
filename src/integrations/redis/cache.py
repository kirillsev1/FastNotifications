from typing import Any

import orjson

from src.conf.config import settings
from src.integrations.redis.key_builder import get_cache_key
from src.integrations.redis.redis import get_redis
from src.metrics import async_integrations_timer


@async_integrations_timer
async def redis_set(field: str, item_id: int, payload: Any) -> None:
    redis = get_redis()
    redis_key = await get_cache_key(field, item_id)
    await redis.set(redis_key, orjson.dumps(payload), ex=settings.EXPIRE_TIME)


@async_integrations_timer
async def redis_get(field: str, item_id: int) -> dict[str, str]:
    redis = get_redis()
    redis_key = await get_cache_key(field, item_id)
    cache = await redis.get(redis_key)
    if cache is None:
        return {}
    return orjson.loads(cache)


@async_integrations_timer
async def redis_drop_key(field: str, item_id: int) -> None:
    redis = get_redis()
    redis_key = await get_cache_key(field, item_id)
    await redis.delete(redis_key)
