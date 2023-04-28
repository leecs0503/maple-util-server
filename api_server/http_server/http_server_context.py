from typing import TypeVar
from ..base.db import BaseDB
from .http_server_env import HTTPServerEnv

DB = TypeVar("DB", bound=BaseDB)

class HTTPServerContext:
    def __init__(
        self,
        db: DB,
        env: HTTPServerEnv,
    ):
        self.db = db
        self.env = env
