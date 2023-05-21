"""
this will be the main folder for league stuff
"""
from os import environ
from dotenv import load_dotenv
import pandas as pd
import requests

load_dotenv("env")

API_KEY = environ["RIOT_API"]


class Region:
    """
    Returns the region. Nothing Fancy.
    """

    def __init__(self) -> str:
        self.na = "na1"
        self.br = "br1"
        self.eun = "eun1"
        self.euw = "euw1"
        self.jp = "jp1"
        self.kr = "kr"
        self.la1 = "la1"
        self.la2 = "la2"
        self.oc = "oc1"
        self.ph = "ph2"
        self.ru = "ru"
        self.sg = "sg2"
        self.th = "th2"
        self.tr = "tr1"
        self.tw = "tw2"
        self.vn = "vn2"


class Summoner:
    """
    Returns summoner level data.
    """

    def __init__(self, region, summoner_name):
        self.data = self.get_data(region, summoner_name)
        self.id = self.data.id[0]
        self.account_id = self.data.accountId[0]
        self.puuid = self.data.puuid[0]
        self.name = self.data.name[0]
        self.profile_icon_id = self.data.profileIconId[0]
        self.revision_date = self.data.revisionDate[0]
        self.summoner_level = self.data.summonerLevel[0]
        self.masteries = self.get_mastery_data(region, self.id)

    def get_data(self, region, summoner_name):
        """
        Get the summoner data.
        https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}
        """
        summoner_url = (
            f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
            + "?api_key="
            + API_KEY
        )
        req = requests.get(summoner_url, timeout=60)
        data = pd.json_normalize(req.json())

        return data

    def get_mastery_data(self, region, id):
        """
        Get the summoner's mastery data.
        https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}
        """
        mastery_url = (
            f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}"
            + "?api_key="
            + API_KEY
        )
        req = requests.get(mastery_url, timeout=60)
        data = pd.DataFrame.from_dict(req.json())

        return data


class League:
    """
    Data dragon data.
    """

    def __init__(self):
        self.champions = self.get_champions()

    def get_champions(self):
        """
        Get this patch's champions.
        http://ddragon.leagueoflegends.com/cdn/13.10.1/data/en_US/champion.json
        """
        champions_url = (
            "http://ddragon.leagueoflegends.com/cdn/13.10.1/data/en_US/champion.json"
        )
        req = requests.get(champions_url, timeout=60).json()
        data = pd.DataFrame(req["data"]).T.reset_index()
        data = pd.concat(
            [data, pd.json_normalize(data.stats), pd.json_normalize(data["info"])],
            axis=1,
        )
        data = data.drop(
            [
                "index",
                "info",
                "image",
                "stats",
            ],
            axis=1,
        )

        return data
