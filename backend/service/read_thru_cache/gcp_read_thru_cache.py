import json

from typing import Optional
from redis.client import Redis

from service.read_thru_cache.i_read_thru_cache import IReadThruCache
from util.i_logger import ILogger


class GCPReadThruCache(IReadThruCache):
    """Google Cloud read-Through cache service implementation using Redis and Firestore."""
    def __init__(self, logger: ILogger):
        self.logger: ILogger = logger
        self.host: str = 'localhost'
        self.redis: Redis = Redis(host=self.host, port=6379, db=0, password='')
        self.seconds_in_day: int = 24 * 60 * 60

    def ping(self) -> bool:
        try:
            res: bool = self.redis.ping()
            if not res:
                self.logger.error('Unable to ping redis cache!')
            return res
        except Exception as ex:
            self.logger.error('Unable to ping redis cache', ex)
            return False

    def exists_in_cache(self, key: str) -> bool:
        try:
            res: int = self.redis.exists(key)
            return res > 0
        except Exception as ex:
            self.logger.error(f'Unable to check if item exists in redis cache, key: {key}', ex)
            return False

    def exists_in_datastore(self, key: str) -> bool:
        pass

    def set(self, key: str, content: object, days_ttl: int) -> None:
        try:
            val: str = json.dumps(content)
            expiration_seconds: int = days_ttl * self.seconds_in_day
            res: bool = self.redis.set(key, val, ex=expiration_seconds)
            if not res:
                self.logger.error(f'Unable to set item in redis cache, key: {key}')
        except Exception as ex:
            self.logger.error(f'Unable to set item in redis cache, key: {key}', ex)

    def get(self, key: str, days_ttl: int) -> Optional[object]:
        try:
            res: str = self.redis.get(key)
            return res
        except Exception as ex:
            self.logger.error(f'Unable to get item from redis cache, key: {key}', ex)
            return None
