"""Returns a dataframe of champions

Returns:
    DataFrame: Returns df of champions
"""
from functools import lru_cache
import pandas as pd
import requests


class Champions:
    """
    Data dragon data.
    """

    def __init__(self):
        self.champions = self.get_champions()

    @lru_cache
    def get_champions(self):
        """
        Get this patch's champions.
        https://ddragon.leagueoflegends.com/cdn/13.12.1/data/en_US/champion.json
        """
        champions_url = (
            "https://ddragon.leagueoflegends.com/cdn/13.12.1/data/en_US/champion.json"
        )
        req = requests.get(champions_url, timeout=60).json()
        data = pd.DataFrame(req["data"]).T.reset_index()
        data = pd.concat(
            [data, pd.json_normalize(data.stats), pd.json_normalize(data["info"])],
            axis=1,
        )
        data[["primary_role", "secondary_role"]] = pd.DataFrame(
            data.tags.tolist(), index=data.index
        )
        data = data.drop(["index", "info", "image", "stats", "tags", "id"], axis=1)

        data = data.rename(
            {
                "key": "champion_id",
                "partype": "resource",
                # info
                "attack": "info_attack",
                "defense": "info_defense",
                "magic": "info_magic",
                "difficulty": "info_difficulty",
                # stats
                # hp
                "hp": "hp",
                "hpperlevel": "hp_level",
                "hpregen": "hp_regen",
                "hpregenperlevel": "hpregen_level",
                # mp
                "mp": "mp",
                "mpperlevel": "mp_level",
                "mpregen": "mp_regen",
                "mpregenperlevel": "mpregen_level",
                # ad
                "attackdamage": "attack",
                "attackdamageperlevel": "attack_level",
                # crit
                "crit": "crit",
                "critperlevel": "crit_level",
                # armour
                "armor": "armor",
                "armorperlevel": "armor_level",
                # attack speed
                "attackspeed": "atk_spd",
                "attackspeedperlevel": "atk_spd_level",
                # ms
                "movespeed": "move_spd",
                # attack range
                "attackrange": "atk_range",
                # spellblock
                "spellblock": "spellblock",
                "spellblockperlevel": "spellblock_level",
            },
            axis=1,
        )
        data.insert(0, "champion_id", data.pop("champion_id"))

        return data
