from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any
from aioredis import Redis
from fastapi import Depends

from db.redis import get_redis


class ICache(ABC):

    @abstractmethod
    async def get(self, key: str) -> Any:
        raise NotImplementedError
    
    @abstractmethod
    async def set(self, key: str, value: Any,
                           expire_time: int | None = None) -> None:
        raise NotImplementedError
    

class RedisCache(ICache):

    def __init__(self, redis_db: Redis) -> None:
        self.redis_db = redis_db

    async def get(self, key: str) -> Any:
        if not await self.redis_db.ping():
            return None
        
        return await self.redis_db.get(key)
    
    async def set(self, key: str, value: Any,
                           expiry_time: int | None = None) -> None:
        if not await self.redis_db.ping():
            return
        
        await self.redis_db.set(key, value)
        if not expiry_time is None:
            await self.redis_db.expire(key, expiry_time)

@lru_cache
def get_cache_storage(redis_db: Redis=Depends(get_redis)):
    return RedisCache(redis_db=redis_db)
