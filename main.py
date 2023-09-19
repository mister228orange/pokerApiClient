import json
import pandas as pd
import requests
from src.utils import get_headers, get_statistics_headers
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

# from src.collector import Collector
#
# coll = Collector(['Winamax.fr', 'PokerStars', 'PokerStars(FR-ES-PT)', 'GGNetwork'])
# coll.update_data()
# coll.stat()


# def create
#
#

#
# tournaments = res['Response']['RegisteringTournamentsResponse']['RegisteringTournaments']['RegisteringTournament']
# df = pd.DataFrame(tournaments)
# print(df.columns)

network = 'Winamax.fr'
# url = f'https://ru.sharkscope.com/poker-statistics/networks/{network}/activeTournaments?Filter=Type:H,NL;Type!:SAT,HU;Date!:2D;Class:SCHEDULED'
# resp = requests.get(url, headers=get_statistics_headers())
# res = resp.json()
#
# active_tours = res['Response']['RegisteringTournamentsResponse']['RegisteringTournaments']['RegisteringTournament']
# df = pd.DataFrame(active_tours)
# df.to_json('tmp.json')


from src.predicters.ability_predictor import AbilityPredictor

df = pd.read_json('tmp.json')
ap = AbilityPredictor(network)
prediction = ap.predict(df)
# print(prediction.columns)
# prediction['buyin'] = prediction['@rake'] + prediction['@stake']
# for buyin in sorted(prediction['buyin'].unique().tolist()):
#     print(prediction[prediction['buyin'] == buyin])
# print(prediction)

from src.predicters.rank_predictor import RankPredictor
from src.predicters.simple_rank_predictor import SimpleRankPredictor


rp = SimpleRankPredictor('Winamax.fr')
u = rp.predict(prediction)
print(u)
# https://www.sharkscope.com/poker-statistics/networks/PokerStars/bareTournaments?tournamentIDs=376797050,375781297

# tours = pd.read_excel('/home/dron/poker_data/predict.xlsx')
# ids = list(tours['@id'])
#
#
# def get_tournaments_by_ids(network, ids):
#     network_data = pd.read_csv(f'/home/dron/poker_data/{network}.csv')
#     result = []
#     for idx in ids:
#         if len(network_data[network_data['@id'] == idx]['AvAbility']):
#             result.append(network_data[network_data['@id'] == idx]['AvAbility'].iloc[0])
#         else:
#             result.append(None)
#     return pd.Series(result)
#
#
# tours['viewedAvAbility'] = get_tournaments_by_ids('PokerStars', ids)
#
# tours.to_excel('/home/dron/poker_data/res.xlsx')




# data = get_sharkscope_data(['GGNetwork'], 50, 230, 1, 2000)
# tour_list = data['Response']['CompletedTournamentsResponse']['CompletedTournaments']['CompletedTournament']
# tournaments = [prepare_tour(t) for t in tour_list]
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
