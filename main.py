import json
import pandas as pd
import requests
from src.utils import get_headers
from config import cfg


#https://ru.sharkscope.com/poker-statistics/networks/PokerStars(FR-ES-PT)/tournaments?&Filter=Entrants:8~*;Type!:SAT,HU;Date:1667329200~1668193199;Class:SCHEDULED&Order=Last,1~10
def get_sharkscope_data(networks, min_buyin, max_buyin, offset, count):
    url = f'https://www.sharkscope.com/api/maxev/networks/{",".join(networks)}/tournaments?' \
          f'Filter=Class:SCHEDULED;StakePlusRake:USD{min_buyin}~{max_buyin};Type:H,NL;Type!:SAT,HU&Order=Last,{offset}~{offset + count}'
    resp = requests.get(url, headers=get_headers())
    print(resp.text)
    return resp.json()


def prepare_tour(tour):
    if 'Statistics' in tour:
        stat = tour['Statistics']
        if 'Statistic' in stat:
            stat = stat['Statistic']
            if type(stat) == list:
                for s in stat:
                    tour[s['@id']] = s['$']
            else:
                tour[stat['@id']] = stat['$']
        tour.pop('Statistics')
    return tour


# https://ru.sharkscope.com/poker-statistics/networks/PokerStars(FR-ES-PT),Winamax.fr/activeTournaments?Filter=Entrants:12~*;StakePlusRake:USD11~16;Date!:1H
networks = ['GGNetwork', '888Poker', 'Chico', 'iPoker', 'PartyPoker', 'PokerStars', 'Revolution', 'SkyPoker', 'WPN',
            'PokerStars(FR-ES-PT)', 'Winamax.fr'
            ]

from src.collector import Collector

coll = Collector(['Winamax.fr', 'PokerStars', 'PokerStars(FR-ES-PT)', 'GGNetwork'])
coll.update_data()
print('')

# data = get_sharkscope_data(['GGNetwork'], 50, 230, 1, 2000)
# tour_list = data['Response']['CompletedTournamentsResponse']['CompletedTournaments']['CompletedTournament']
# tournaments = [prepare_tour(t) for t in touer_list]
#
# df = pd.DataFrame(tournaments)
# df['timestamp'] = df['@date']
# df['@date'] = pd.to_datetime(df['@date'], unit='s')
# df['weekDay'] = df['@date'].dt.day_name()
# print(df)
# df.to_csv('GGNetwork.csv')

# url = f'https://www.sharkscope.com/api/maxev/playergroups'
# head = get_headers()
# resp = requests.get(url, headers=head)
# print(resp, resp.text)

# url = f'https://www.sharkscope.com/api/maxev/networks/fulltilt/players/keNnyRus/completedTournaments?order=player,1~1000'
# head = get_headers()
# resp = requests.get(url, headers=head)
# open('kenny_tornaments.json', 'w').write(resp.text)
# st = resp.json()
# player_stat = json.loads(open('kennystat.json').read())
# print(st.keys())


# collect = []
# for i in range(1, 7):
#     filename = f'tour_mid{str(i) if i > 1 else ""}.csv'
#     collect.append(pd.read_csv(filename))
# un = pd.concat(collect)
# print(un)
# un.to_csv('collect.csv')
