import json

from redis import Redis
from typing import Optional

from service.cache.i_cache_service import ICacheService
from util.i_logger import ILogger


class RedisService(ICacheService):
    """Primary redis cache service implementation."""
    def __init__(self, logger: ILogger, host: str):
        self.logger: ILogger = logger
        self.redis: Redis = Redis(host=host, port=6379, db=0, password='')
        self.seconds_in_day: int = 24 * 60 * 60

    def ping(self) -> bool:
        res: bool = self.redis.ping()
        if not res:
            self.logger.error('Unable to ping redis cache!')
        return res

    def exists(self, key: str) -> bool:
        res: int = self.redis.exists(key)
        return res > 0

    def set(self, key: str, content: object, days_ttl: int) -> None:
        val: str = json.dumps(content)
        expiration_seconds: int = days_ttl * self.seconds_in_day
        res: bool = self.redis.set(key, val, ex=expiration_seconds)
        if not res:
            self.logger.error(f'Unable to set item in redis cache, key: {key}')

    def get(self, key: str) -> Optional[str]:
        res: str = self.redis.get(key)
        return res

