from .http_server_context import HTTPServerContext

class HTTPServerDbHandler:
    def __init__(
        self,
        ctx:HTTPServerContext
    ):
        self.ctx = ctx
