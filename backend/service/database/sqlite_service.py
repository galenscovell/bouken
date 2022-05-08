import hashlib
import json
import os
import sqlite3
import uuid

from typing import List, Optional

from model.exterior_map import ExteriorMap
from model.interior_map import InteriorMap
from model.user import User
from service.database.i_db_service import IDbService
from util.i_logger import ILogger


class SqliteService(IDbService):
    """SQLite implementation of database service."""
    def __init__(self, logger: ILogger) -> None:
        self.logger: ILogger = logger
        self.db_file = os.path.join(os.getcwd(), 'data', 'bouken.db')

    @staticmethod
    def _hash_value(s: str) -> str:
        # TODO: password hashing
        salt: bytes = os.urandom(32)
        key: bytes = hashlib.pbkdf2_hmac('sha256', salt, 100000)
        return s

    @staticmethod
    def _generate_guid() -> str:
        return str(uuid.uuid4())

    def ping(self) -> bool:
        return True

    def _query(self, base_cmd: str, params: List[str]) -> None:
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            c.execute(base_cmd, params)
        except Exception as ex:
            self.logger.error(f'Error querying DB, query: {base_cmd}, params: {params}', ex)
        finally:
            conn.commit()
            c.close()
            conn.close()

    def _query_with_return(self, base_cmd: str, params: List[str]) -> Optional[object]:
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            c.execute(base_cmd, params)
            found: List = c.fetchall()
            if not found:
                raise Exception('Not found')
            return found[0]
        except Exception as ex:
            self.logger.error(f'Error querying DB, query: {base_cmd}, params: {params}', ex)
            return None
        finally:
            conn.commit()
            c.close()
            conn.close()

    def create_user(self, email: str, password: str) -> None:
        guid: str = self._generate_guid()
        hashed_password: str = self._hash_value(password)
        params: List[str] = [guid, email, hashed_password]
        self._query('INSERT into User values("?", "?", "?")', params)

    def get_user(self, email: str) -> Optional[User]:
        return self._query_with_return('SELECT User WHERE EMAIL="?"', [email])

    def create_exterior_map(self, user_guid: str) -> None:
        guid: str = self._generate_guid()
        params: List[str] = [guid, '', '', '']
        self._query('INSERT into ExteriorMap values("?", "?", "?", "?")', params)

    def get_exterior_map(self, guid: str) -> Optional[ExteriorMap]:
        return self._query_with_return('SELECT ExteriorMap WHERE GUID="?"', [guid])

    def update_exterior_map(self, guid: str) -> None:
        pass

    def create_interior_map(self) -> None:
        guid: str = self._generate_guid()
        params: List[str] = [guid, '', '', '', '']
        self._query('INSERT into ExteriorMap values("?", "?", "?", "?", "?")', params)

    def get_interior_map(self, guid: str) -> Optional[InteriorMap]:
        return self._query_with_return('SELECT InteriorMap WHERE GUID="?"', [guid])

    def update_interior_map(self, guid: str) -> None:
        pass
    
