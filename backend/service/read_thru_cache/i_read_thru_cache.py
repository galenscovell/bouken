from typing import Optional

from util.i_logger import ILogger


class IReadThruCache:
    """Read-Through cache service interface."""
    def ping(self) -> bool:
        """Check connectivity to read-through cache and underlying data store."""
        pass

    def exists_in_cache(self, key: str) -> bool:
        """Check if item with given key exists in cache."""
        pass

    def exists_in_datastore(self, key: str) -> bool:
        """Check if item with given key exists in underlying data store."""
        pass

    def set(self, key: str, content: object, days_ttl: int) -> None:
        """
        Set (or update) a single read-through cache item with given key, content to be
        serialized, and TTL in days. Item will be created in underlying data
        store as well as cache, with TTL on cache item.
        """
        pass

    def get(self, key: str, days_ttl: int) -> Optional[object]:
        """
        Get a single deserialized read-through cache item with given key.
        If item does not exist in cache, will check underlying data store.
        If item found in data store but not cache, item will be added to
        cache with TTL in days.
        """
        pass
