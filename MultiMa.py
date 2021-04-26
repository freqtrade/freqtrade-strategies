# MultiMa Strategy
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# (First Hyperopt it.A hyperopt file is available)
#
# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce


class MultiMa(IStrategy):
    #  38/5000:    820 trades. 701/0/119 Wins/Draws/Losses. Avg profit   2.61%. Median profit   1.95%. Total profit  0.29474423 BTC ( 2140.92Σ%). Avg duration 602.9 min. Objective: -15.64380

    # Buy hyperspace params:
    buy_params = {
        'buy-ma-count': 3, 'buy-ma-gap': 4, 'buy-ma-shift': 2
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-ma-count': 3, 'sell-ma-gap': 4, 'sell-ma-shift': 2
    }

    # ROI table:
    minimal_roi = {
        "0": 0.30873,
        "569": 0.16689,
        "3211": 0.06473,
        "7617": 0
    }

    # Stoploss:
    stoploss = -1

    # Buy hypers
    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA - Simple Moving Average
        for i in range(1, self.buy_params['buy-ma-count']):
            dataframe[f'buy-ma-{i}'] = ta.SMA(dataframe,
                                              timeperiod=int(i * self.buy_params['buy-ma-gap']))

        for i in range(1, self.sell_params['sell-ma-count']):
            dataframe[f'sell-ma-{i}'] = ta.SMA(dataframe,
                                               timeperiod=int(i * self.sell_params['sell-ma-gap']))

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        for i in range(1, self.buy_params['buy-ma-count']):
            if i > 1:
                for shift in range(self.buy_params['buy-ma-shift']):
                    conditions.append(
                        dataframe[f'buy-ma-{i}'].shift(shift) > dataframe[f'buy-ma-{i-1}'].shift(shift))
        dataframe.loc[
            reduce(lambda x, y: x & y, conditions),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        for i in range(1, self.sell_params['sell-ma-count']):
            if i > 1:
                for shift in range(self.sell_params['sell-ma-shift']):
                    conditions.append(
                        dataframe[f'sell-ma-{i}'].shift(shift) < dataframe[f'sell-ma-{i-1}'].shift(shift))
        dataframe.loc[
            reduce(lambda x, y: x & y, conditions),
            'sell'] = 1
        return dataframe
