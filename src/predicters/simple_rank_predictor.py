import pandas as pd

from src.predicters.rank_predictor import RankPredictor
from src.utils import ABI_by_rank
from random import randint


TOTAL_RANKS_COUNT = 20

class SimpleRegressor:

    def __init__(self, raw_data):
        raw_data['buyin'] = raw_data['@rake'] + raw_data['@stake']
        self.min_value = raw_data['buyin'].min()
        self.max_value = raw_data['buyin'].max()
        print(sorted(raw_data['buyin'].tolist()))
        self.buyin_ranges = [raw_data['buyin'].quantile(q / 100) for q in range(0, 100, 5)] + [10 ** 9]

    def predict(self, data):
        data['buyin'] = data['@rake'] + data['@stake']
        return pd.Series([self.rank_by_buyin(bi) for bi in data['buyin']])

    def rank_by_buyin(self, buyin):
        rank = 1
        while abs(buyin - ABI_by_rank[rank]) < abs(buyin - ABI_by_rank[rank - 1]):
            rank += 1
        return rank


class SimpleRankPredictor(RankPredictor):
    def __init__(self, network):
        self._network = network
        raw_data = self.get_data_by_network()
        self.model = SimpleRegressor(raw_data)

