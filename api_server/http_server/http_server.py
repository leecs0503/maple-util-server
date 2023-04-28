from .http_server_context import HTTPServerContext
from .http_server_db_handler import HTTPServerDbHandler
from .http_server_routing_handler import HTTPServerRoutingHandler
from aiohttp import web
from aiohttp_middlewares import cors_middleware

class HTTPServer:
    def __init__(
        self,
        ctx: HTTPServerContext,
    ):
        self.ctx = ctx
        self.db_handler = HTTPServerDbHandler(ctx=ctx)
        self.routing_handler = HTTPServerRoutingHandler()
        self.app = web.Application(
            middlewares=[cors_middleware(allow_all=True)]
        )
        self.routes = self.routing_handler.get_routes()
        self.app.add_routes(self.routes)

    def run(self):
        print(f"server start! routing info: {self.routes}")
        web.run_app(self.app, port=self.ctx.env.port)