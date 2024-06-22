from src.conf.config import settings


async def get_cache_key(field: str, item_id: int) -> str:
    return f'{settings.REDIS_CACHE_PREFIX}:{field}:{item_id}'
