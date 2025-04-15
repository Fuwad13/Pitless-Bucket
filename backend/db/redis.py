from redis import asyncio as aioredis

from backend.config import Config


def create_redis():
  return aioredis.ConnectionPool(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        decode_responses=True,
        username=Config.REDIS_USERNAME,
        password=Config.REDIS_PASSWORD,
    )

pool = create_redis()