from redis import asyncio as aioredis

from backend.config import settings


def create_redis():
  return aioredis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
        username=settings.REDIS_USERNAME,
        password=settings.REDIS_PASSWORD,
    )

pool = create_redis()