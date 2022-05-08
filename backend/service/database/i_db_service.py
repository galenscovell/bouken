from typing import List, Optional

from model.exterior_map import ExteriorMap
from model.interior_map import InteriorMap
from model.user import User


class IDbService:
    """Database service interface."""
    def _query(self, base_cmd: str, params: List[str]) -> None:
        pass

    def _query_with_return(self, base_cmd: str, params: List[str]) -> Optional[object]:
        pass

    def ping(self) -> bool:
        pass

    def create_user(self, email: str, password: str) -> None:
        pass

    def get_user(self, email: str) -> Optional[User]:
        pass

    def create_exterior_map(self, user_guid: str) -> None:
        pass

    def get_exterior_map(self, guid: str) -> Optional[ExteriorMap]:
        pass

    def update_exterior_map(self, guid: str) -> None:
        pass

    def create_interior_map(self) -> None:
        pass

    def get_interior_map(self, guid: str) -> Optional[InteriorMap]:
        pass

    def update_interior_map(self, guid: str) -> None:
        pass