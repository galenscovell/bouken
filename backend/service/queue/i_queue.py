from typing import Optional


class IQueue:
    """Queue service interface."""
    def get_message(self) -> Optional[str]:
        """Pull a single str message from the queue."""
        pass

    def push_message(self, payload: str) -> None:
        """Push a single str message to the queue."""
        pass
