import logging
import time

import requests
import pandas as pd

from src.utils import get_headers

logger = logging.getLogger("updater")
logger.setLevel('INFO')


class Collector:
    def __init__(self, networks, min_buyin=40, max_buyin=240):
        self.networks = networks
        self.today_searches = self.get_today_searches()
        self.buyin_range = (min_buyin, max_buyin)

    @staticmethod
    def get_today_searches():
        try:
            resp = requests.get(f'https://www.sharkscope.com/api/maxev/playergroups', headers=get_headers())
            return int(resp.json()['Response']['UserInfo']['Subscriptions']['@totalSearchesRemaining'])
        except Exception as e:
            logger.error(e)
            return 0

    def update_data(self):
        for room in self.networks:
            if self.today_searches <= 0:
                logger.info('Searches is over today')
                break
            self.update_network(room)

    def update_network(self, network):
        last_tour_time = self.get_last_tour_time(f'./{network}.csv')
        tour_list = self.get_tournaments(last_tour_time, network)
        if tour_list:
            logger.info(f'From {network} received {len(tour_list)} tournaments')
            self.add_tournaments(tour_list)

    def get_tournaments(self, begin_time, network):
        try:
            url = f'https://www.sharkscope.com/api/maxev/networks/{network}/tournaments?' \
                  f'Filter=Class:SCHEDULED;StakePlusRake:USD{self.buyin_range[0]}~{self.buyin_range[1]};Type:H,NL;' \
                  f'Type!:SAT,HU;' \
                  f'Date:{begin_time}~{int(time.time())}&Order=Last,{1}~{self.today_searches * 10}'
            resp = requests.get(url, headers=get_headers())
            # print(resp.text)
            return resp.json()['Response']['CompletedTournamentsResponse']['CompletedTournaments']['CompletedTournament']
        except Exception as e:
            logger.error(e)

    def add_tournaments(self, tour_list):
        print('huy')
        pass

    @staticmethod
    def get_last_tour_time(filename):
        try:
            df = pd.read_csv(f'./{filename}')
            return df['timestamp'].max()
        except Exception as e:
            return None
