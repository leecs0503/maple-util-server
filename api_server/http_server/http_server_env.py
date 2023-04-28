from typing import TypeVar
from ..base.db import BaseDB

DB = TypeVar("DB", bound=BaseDB)

class HTTPServerEnv:
    def __init__(
        self,
        port: int,
    ):
        self.port = port
