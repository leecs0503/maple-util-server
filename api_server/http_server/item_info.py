from typing import Optional

from dataclasses import dataclass

@dataclass
class ItemInfo:
    name: str
    item_type: str
    req_level: str
    thumbnail: str
    soul_name: Optional[str] = None
    soul_option_all: Optional[int] = None
    soul_option_atk: Optional[int] = None
    soul_option_matk: Optional[int] = None
    soul_option_boss_damage: Optional[int] = None
    soul_option_ignore_shield: Optional[int] = None
    soul_option_: Optional[int] = None
    starforce: Optional[int] = None
    seed_level: Optional[int] = None
    plus_str: Optional[int] = None
    plus_dex: Optional[int] = None
    plus_int: Optional[int] = None
    plus_luk: Optional[int] = None
    plus_all: Optional[int] = None
    plus_hp: Optional[int] = None
    plus_ATK: Optional[int] = None
    plus_MATK: Optional[int] = None
    plus_damage: Optional[int] = None
    plus_boss_damage: Optional[int] = None
    potential_str: Optional[int] = None
    potential_dex: Optional[int] = None
    potential_int: Optional[int] = None
    potential_luk: Optional[int] = None
    potential_all: Optional[int] = None
    potential_hp: Optional[int] = None
    potential_ATK: Optional[int] = None
    potential_MATK: Optional[int] = None
    potential_damage: Optional[int] = None
    potential_boss_damage: Optional[int] = None
    potential_ignore_shield: Optional[int] = None