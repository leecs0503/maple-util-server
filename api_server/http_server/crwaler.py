from urllib.parse import urlparse
from aiohttp import ClientSession
import json
import re
import requests
from ..constants import MAPLESTORY_URL
from bs4 import BeautifulSoup
from .item_info import ItemInfo

RANKING_PATH = "{url}/N23Ranking/World/Total?c={user_name}&w={server_code}"
PAGE_PATH = "{url}{routing_path}"

def get_tags_from_class(
    html: str,
    cls: str,
):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all(class_=cls)


class Crwaler:
    def __init__(self):
        pass

    async def get_item_infos(
        self,
        user_name: str,
    ):
        async with ClientSession() as session:
            user_route_path = await self._get_user_route_path(session, user_name)
            equip_route_path = await self._equip_path_of(user_route_path=user_route_path)
            result = await self._get_item_list(
                session=session,
                equip_route_path=equip_route_path
            )
            return result

    async def _get_item_list(
        self,
        session: ClientSession,
        equip_route_path: str,
    ):
        url = PAGE_PATH.format(
            url=MAPLESTORY_URL,
            routing_path=equip_route_path,
        )
        html_content = await self._fetch(session, url)

        item_pot_tag = get_tags_from_class(html_content, 'item_pot')[0]
        li_tags = item_pot_tag.find_all('li')

        paths = []
        for li_tag in li_tags:
            link_tags = li_tag.find_all('a')
            if len(link_tags) == 0:
                paths.append(None)
                continue
            path = link_tags[0].get('href')
            paths.append(path)

        result = []
        for path in paths:
            if not path:
                result.append(None)
                continue
            url =PAGE_PATH.format(
                url=MAPLESTORY_URL,
                routing_path=path,
            )
            response = requests.get(url, headers={
                "X-Requested-With": "XMLHttpRequest",
            })
            view = json.loads(response.text)["view"]
            item_info = self._item_info_of(view)

            result.append(item_info)
        return result

    def _item_info_of(
        self,
        view: str
    ):
        # TODO: view to ItemInfo
        item_name, thumbnail, starforce = self._parse_item_title(view)
        req_level, item_type = self._parse_item_ability(view)
        stet_infos = self._parse_stet_info(view)

        return ItemInfo(
            name=item_name,
            thumbnail=thumbnail,
            item_type=item_type,
            req_level=int(req_level),
            starforce=starforce,
            **stet_infos
        )

    def _parse_item_title(self, view: str):
        tag = get_tags_from_class(html=view, cls='item_title')[0]
        img_tag = tag.find_all('img')[0]
        item_name = img_tag.get('alt')
        thumbnail = img_tag.get('src')

        starforce = None
        em_tags = tag.find_all('em')
        if len(em_tags) > 0:
            pattern = r'(\d+)성'
            match = re.search(pattern, em_tags[0].text)
            starforce = int(match.group(1))
        return item_name, thumbnail, starforce

    def _parse_item_ability(self, view: str):
        tag = get_tags_from_class(html=view, cls='item_ability')[0]
        em_tags = tag.find_all('em')
        req_level = em_tags[0].text
        item_type = em_tags[-1].text
        return req_level, item_type

    def _parse_stet_info(self, view: str):
        tag = get_tags_from_class(html=view, cls='stet_info')[0]
        li_tags = tag.find_all('li')
        result = {}
        rev_dict = {
            "STR": "plus_str",
            "DEX": "plus_dex",
            "INT": "plus_int",
            "LUK": "plus_luk",
            "MaxHP": "plus_hp",
            "올스탯": "plus_all",
            "공격력": "plus_ATK",
            "마력": "plus_MATK",
            "데미지": "plus_damage",
            "보스 몬스터 공격 시 데미지": "plus_boss_damage",
        }
        potential_rev_dict = {
            "STR": "potential_str",
            "DEX": "potential_dex",
            "INT": "potential_int",
            "LUK": "potential_luk",
            "올스탯": "potential_all",
            "공격력": "potential_ATK",
            "마력": "potential_MATK",
            "데미지": "potential_damage",
            "보스 몬스터 공격 시 데미지": "potential_boss_damage",
            "몬스터 방어율 무시": "potential_ignore_shield",
        }
        for li_tag in li_tags:
            type = li_tag.find('span').text
            if "에디셔널 잠재옵션" in type:
                continue
            if "잠재옵션" in type:
                st_tags = get_tags_from_class(str(li_tag), "point_td")
                if len(st_tags) == 0:
                    continue
                st_tag = st_tags[0]
                value = st_tag.text
                pattern = r"([가-힣\sA-Z]+)\s:\s([+-]?\d+)%?"

                matches = re.findall(pattern, value)
                for match in matches:
                    prop_name = match[0].strip()
                    prop_value = match[1]
                    if prop_value[0] == '+':
                        val = int(prop_value[1:])
                    if prop_name in potential_rev_dict:
                        key = potential_rev_dict[prop_name]
                        result[key] = result.get(key, 0) + val
                    else:
                        print("!!", prop_name)
                continue
            if type == "소울옵션":
                continue
            if type == "기타":
                seed_level = None
                if "링 1레벨" in str(li_tag):
                    seed_level = 1
                if "링 2레벨" in str(li_tag):
                    seed_level = 2
                if "링 3레벨" in str(li_tag):
                    seed_level = 3
                if "링 4레벨" in str(li_tag):
                    seed_level = 4
                if seed_level:
                    result["seed_level"] = seed_level
                continue
            if type in ["STR", "DEX", "INT", "LUK", "MaxHP", "공격력", "마력"]:
                st_tag = get_tags_from_class(str(li_tag), "point_td")[0]
                value_str = st_tag.text
                if '(' not in value_str:
                    continue
                pattern = r'\+(\w+)\s*\((\w+)\s*\+\s*(\w+)\s*\+\s*(\w+)\)'
                match = re.search(pattern, value_str)
                key = rev_dict[type]
                result[key] = int(match.group(3))
                continue
            if type in ["올스탯", "데미지", "보스 몬스터 공격 시 데미지"]:
                st_tag = get_tags_from_class(str(li_tag), "point_td")[0]
                value_str = st_tag.text
                if '(' not in value_str:
                    continue
                pattern = r'\+(\d+)%\s*\((\d+)%\s*\+\s*(\d+)%\)'
                match = re.search(pattern, value_str)
                key = rev_dict[type]
                result[key] = int(match.group(3))
                continue
        return result



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

        rank_table_tag = get_tags_from_class(html_content, 'rank_table')[0]
        link_tags = rank_table_tag.find_all('a')
        result = [
            link_tag
            for link_tag in link_tags
            if user_name in link_tag
        ][0]
        user_route_path = result.get('href')

        return user_route_path

    async def _equip_path_of(
        self,
        user_route_path: str,
    ):
        parsed_url = urlparse(user_route_path)
        return parsed_url.path + '/Equipment?' + parsed_url.query

    async def _fetch(self, session: ClientSession, url):
        async with session.get(url) as response:
            return await response.text()