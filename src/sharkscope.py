import requests

from config import cfg
from src.utils import get_headers


class Sharkscope:

    def __init__(self):
        self._headers = get_headers()
        self._prefix = 'https://www.sharkscope.com/api'


    def get_tournaments(self, count=1000):
        url = f'{self._prefix}/{cfg.USER}/networks/fulltilt/tournaments?filter=Type:OMAHA&Order=Last,1~{count}'
        print(url, get_headers())
        resp = requests.get(url, headers=self._headers)
        if resp.ok:
            return resp.json()

    def get_player_stat(self, player):
        url = f'{self._prefix}/{cfg.USER}/networks/fulltilt/players/{player}/'
        resp = requests.get(url, headers=self._headers)
        if resp.ok:
            return resp.json()