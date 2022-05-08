from typing import Optional


class ICacheService:
    """Cache service interface."""
    def ping(self) -> bool:
        """Check connectivity to cache."""
        pass

    def exists(self, key: str) -> bool:
        """Check if item with given key exists in cache."""
        pass

    def set(self, key: str, content: object, days_ttl: int) -> None:
        """Set a single cache item with given key, content to be serialized, and TTL in days."""
        pass

    def get(self, key: str) -> Optional[object]:
        """Get a single deserialized cache item with given key."""
        pass
