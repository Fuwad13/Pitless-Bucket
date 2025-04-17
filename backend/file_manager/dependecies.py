from redis import asyncio as aioredis

from backend.db.redis import pool


def get_redis():
    return aioredis.Redis(connection_pool=pool)
