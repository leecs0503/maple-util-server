from .base.db import BaseDB
import aiomysql

class AioMysqlDB(BaseDB):
    def __init__(
        self,
        db_host: str,
        db_port: int,
        db_user: str,
        db_password: str,
        db_name: str,
    ):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.pool = None

    async def _get_pool(self):
        if self.pool:
            return self.pool
        self.pool = await aiomysql.create_pool(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            db=self.db_name,
        )
        return self.pool

    async def insert_query(
        self,
        sql: str,
        args: dict,
    ):
        pool = await self._get_pool()
        pass

    def select_query(
        self,
        sql: str,
        args: dict,
    ):
        pass

    def update_query(
        self,
        sql: str,
        args: dict,
    ):
        pass

    def delete_query(
        self,
        sql: str,
        args: dict,
    ):
        pass