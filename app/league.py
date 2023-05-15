"""
this will be the main folder for league stuff
"""
from os import environ
from dotenv import load_dotenv
import pandas as pd
from riotwatcher import LolWatcher

load_dotenv()
RIOT_API = environ["RIOT_API"]
lol_watcher = LolWatcher(RIOT_API)
my_region = "na1"
NA = "na1"


class League:
    def __init__(self, region) -> None:
        self.versions = self.Versions(region)
        self.champions = self.get_champions(region)

    class Versions:
        def __init__(self, region) -> None:
            self.versions_ = lol_watcher.data_dragon.versions_for_region(region)
            self.versions_item = self.versions_["n"]["item"]
            self.versions_rune = self.versions_["n"]["rune"]
            self.versions_mastery = self.versions_["n"]["mastery"]
            self.versions_summoner = self.versions_["n"]["summoner"]
            self.versions_champion = self.versions_["n"]["champion"]

    def get_champions(self, region):
        champions = (
            pd.DataFrame.from_dict(
                lol_watcher.data_dragon.champions(
                    self.Versions(region).versions_champion
                )
            )
            .reset_index()
            .rename(columns={"index": "champion"})
        )

        champions = (
            pd.concat([champions, pd.json_normalize(champions.data)], axis=1)
            .drop(columns=["type", "format", "version", "data", "name", "id"])
            .rename(
                {
                    "key": "champion_id",
                    "tags": "roles",
                    "partype": "resource",
                    # info
                    "info.attack": "attack",
                    "info.defense": "defense",
                    "info.magic": "magic",
                    "info.difficulty": "difficulty",
                    # stats
                    # hp
                    "stats.hp": "hp",
                    "stats.hpperlevel": "hp_level",
                    "stats.hpregen": "hp_regen",
                    "stats.hpregenperlevel": "hpregen_level",
                    # mp
                    "stats.mp": "mp",
                    "stats.mpperlevel": "mp_level",
                    "stats.mpregen": "mp_regen",
                    "stats.mpregenperlevel": "mpregen_level",
                    # ad
                    "stats.attackdamage": "attack",
                    "stats.attackdamageperlevel": "attack_level",
                    # crit
                    "stats.crit": "crit",
                    "stats.critperlevel": "crit_level",
                    # armour
                    "stats.armor": "armor",
                    "stats.armorperlevel": "armor_level",
                    # attack speed
                    "stats.attackspeed": "atk_spd",
                    "stats.attackspeedperlevel": "atk_spd_level",
                    # ms
                    "stats.movespeed": "move_spd",
                    # attack range
                    "stats.attackrange": "atk_range",
                    # spellblock
                    "stats.spellblock": "spellblock",
                    "stats.spellblockperlevel": "spellblock_level",
                },
                axis=1,
            )
        )

        champions.insert(0, "champion_id", champions.pop("champion_id"))

        # change datatype
        champions.resource = champions.resource.astype("category")

        return champions
