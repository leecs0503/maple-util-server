from aiohttp import web, ClientSession

import requests
from urllib.parse import urlparse
from http import HTTPStatus
from ..constants import MAPLESTORY_URL
from bs4 import BeautifulSoup
from lxml import html

RANKING_PATH = "{url}/N23Ranking/World/Total?c={user_name}&w={server_code}"
PAGE_PATH = "{url}{routing_path}"

class HTTPServerRoutingHandler:
    def __init__(self):
        pass

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

        async with ClientSession() as session:
            user_route_path = await self._get_user_route_path(session, user_name)
            equip_route_path = await self._get_equip_path(user_route_path=user_route_path)
            result = await self._get_item_list(
                session=session,
                equip_route_path=equip_route_path
            )
            result
        return web.Response(body="!!", status=HTTPStatus.OK)

    async def _get_item_list(
        self,
        session: ClientSession,
        equip_route_path: str,
    ):
        url = PAGE_PATH.format(
            url=MAPLESTORY_URL,
            routing_path=equip_route_path,
        )
        # print(url)
        html_content = await self._fetch(session, url)
        soup = BeautifulSoup(html_content, 'html.parser')
        item_pot = str(soup.find_all(class_='item_pot')[0])

        item_pot_soup = BeautifulSoup(item_pot, 'html.parser')
        li_tags = item_pot_soup.find_all('li')
        result = []
        for li_tag in li_tags:
            li_tag_str = str(li_tag)
            li_soup = BeautifulSoup(li_tag_str, 'html.parser')
            link_tags = li_soup.find_all('a')
            if len(link_tags) == 0:
                result.append(None)
                continue
            path = link_tags[0].get('href')
            result.append(path)
        for path in result:
            if not path:
                continue
            url =PAGE_PATH.format(
                url=MAPLESTORY_URL,
                routing_path=path,
            )
            X = requests.get(url, headers={
                "X-Requested-With": "XMLHttpRequest",
            })
            print("@@")
            print(X.text)

    async def _get_user_route_path(
        self,
        session: ClientSession,
        user_name: str,
    ):
        ranking_url = RANKING_PATH.format(
            url=MAPLESTORY_URL,
            user_name=user_name,
            server_code=2,
        )
        html_content = await self._fetch(session, ranking_url)

        soup = BeautifulSoup(html_content, 'html.parser')
        rank_table = str(soup.find_all(class_='rank_table')[0])

        rank_soup = BeautifulSoup(rank_table, 'html.parser')
        link_tags = rank_soup.find_all('a')
        result = [
            link_tag
            for link_tag in link_tags
            if user_name in link_tag
        ][0]
        user_route_path = result.get('href')

        return user_route_path

    async def _get_equip_path(
        self,
        user_route_path: str,
    ):
        parsed_url = urlparse(user_route_path)
        return parsed_url.path + '/Equipment?' + parsed_url.query

    async def _fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()