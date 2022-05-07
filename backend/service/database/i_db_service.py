from typing import List, Optional

from backend.model.exterior_map import ExteriorMap
from backend.model.interior_map import InteriorMap
from backend.model.user import User


class IDbService:
    """Database service interface."""
    def _query(self, base_cmd: str, params: List[str]) -> None:
        pass

    def _query_with_return(self, base_cmd: str, params: List[str]) -> Optional[object]:
        pass

    def create_user(self, email: str, password: str) -> None:
        pass

    def get_user(self, email: str) -> User:
        pass

    def create_exterior_map(self, user_guid: str) -> None:
        pass

    def get_exterior_map(self, guid: str) -> ExteriorMap:
        pass

    def update_exterior_map(self, guid: str) -> None:
        pass

    def create_interior_map(self) -> None:
        pass

    def get_interior_map(self, guid: str) -> InteriorMap:
        pass

    def update_interior_map(self, guid: str) -> None:
        pass