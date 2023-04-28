from aiohttp import web

from http import HTTPStatus
from .crwaler import Crwaler
from dataclasses import asdict
import json

class HTTPServerRoutingHandler:
    def __init__(self):
        self.crwaler = Crwaler()

    def get_routes(self):
        return [
            web.get("/", self.index_handler),
            web.get("/healthcheck", self.healthcheck_handler),
            web.get('/user/{user_name}', self.user_handler),
        ]

    async def healthcheck_handler(self, request: web.Request):
        return web.Response(body="200 OK", status=HTTPStatus.OK)

    async def index_handler(self, request: web.Request):
        return web.Response(body="-", status=HTTPStatus.OK)

    async def user_handler(self, request: web.Request):
        user_name = request.match_info['user_name']
        item_infos = await self.crwaler.get_item_infos(user_name=user_name)
        result = [
            asdict(item_info) if item_info else None
            for item_info in item_infos
        ]
        return web.Response(body=json.dumps(result), status=HTTPStatus.OK)