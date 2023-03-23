import json
import pandas as pd
import requests
from src.utils import get_headers
from config import cfg

print(cfg.__dict__)


#url = f'https://www.sharkscope.com/api/maxev/activeTournaments?limit=100'
# url = f'https://www.sharkscope.com/api/maxev/networks/fulltilt/tournaments?filter=Type:OMAHA&Order=Last,1~1000'
# resp = requests.get(url, headers=headers)
# print(resp, resp.json())
# open('tour.json', 'w').write(resp.text)


def prepare_tour(tour):
    if 'Statistics' in tour:
        stat = tour['Statistics']
        for s in stat['Statistic']:
            tour[s['@id']] = s['$']
        tour.pop('Statistics')
    return tour


# tournaments = json.loads(open('tour.json').read())['Response']
# tour_list = tournaments['CompletedTournamentsResponse']['CompletedTournaments']['CompletedTournament']
# print(len(tour_list))
# tour = tour_list[0]
# tour = prepare_tour(tour)
# tournaments = list(map(prepare_tour, tour_list))
# df = pd.DataFrame(tournaments)
# df['@date'] = pd.to_datetime(df['@date'], unit='s')
# df['weekDay'] = df['@date'].dt.day_name()
# print(df)
# df.to_csv('tournaments.csv')

# url = f'https://www.sharkscope.com/api/maxev/playergroups'
# head = get_headers()
# resp = requests.get(url, headers=head)
# print(resp, resp.text)

url = f'https://www.sharkscope.com/api/maxev/networks/fulltilt/players/keNnyRus/completedTournaments?order=player,1~1000'
head = get_headers()
resp = requests.get(url, headers=head)
open('kenny_tornaments.json', 'w').write(resp.text)
st = resp.json()
# player_stat = json.loads(open('kennystat.json').read())
print(st.keys())

