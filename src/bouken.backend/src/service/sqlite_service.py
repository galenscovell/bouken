"""
Interacts with core SQLite DB.
"""

import json
import os
import sqlite3


class SqliteService:
    def __init__(self):
        self.db_file = os.path.join(os.getcwd(), 'bouken.db')

    def _query(self):
        conn = sqlite3.connect(self.db_file)

        try:
            print('todo')
        except Exception as ex:
            print('todo')
        finally:
            conn.close()
