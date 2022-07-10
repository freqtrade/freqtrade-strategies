"""
author      = "Kevin Ossenbrück"
copyright   = "Free For Use"
credits     = ["Bloom Trading, Mohsen Hassan"]
license     = "MIT"
version     = "1.0"
maintainer  = "Kevin Ossenbrück"
email       = "kevin.ossenbrueck@pm.de"
status      = "Live"
"""

from freqtrade.strategy import IStrategy
from freqtrade.strategy import IntParameter
from functools import reduce
from pandas import DataFrame

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy



# CCI timerperiods and values
cciBuyTP = 72
cciBuyVal = -175
cciSellTP = 66
cciSellVal = -106

# RSI timeperiods and values
rsiBuyTP = 36
rsiBuyVal = 90
rsiSellTP = 45
rsiSellVal = 88


class SwingHighToSky(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = '15m'

    stoploss = -0.34338

    minimal_roi = {"0": 0.27058, "33": 0.0853, "64": 0.04093, "244": 0}

    buy_cci = IntParameter(low=-200, high=200, default=100, space='buy', optimize=True)
    buy_cciTime = IntParameter(low=10, high=80, default=20, space='buy', optimize=True)
    buy_rsi = IntParameter(low=10, high=90, default=30, space='buy', optimize=True)
    buy_rsiTime = IntParameter(low=10, high=80, default=26, space='buy', optimize=True)

    sell_cci = IntParameter(low=-200, high=200, default=100, space='sell', optimize=True)
    sell_cciTime = IntParameter(low=10, high=80, default=20, space='sell', optimize=True)
    sell_rsi = IntParameter(low=10, high=90, default=30, space='sell', optimize=True)
    sell_rsiTime = IntParameter(low=10, high=80, default=26, space='sell', optimize=True)

    # Buy hyperspace params:
    buy_params = {
        "buy_cci": -175,
        "buy_cciTime": 72,
        "buy_rsi": 90,
        "buy_rsiTime": 36,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_cci": -106,
        "sell_cciTime": 66,
        "sell_rsi": 88,
        "sell_rsiTime": 45,
    }

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        for val in self.buy_cciTime.range:
            dataframe[f'cci-{val}'] = ta.CCI(dataframe, timeperiod=val)

        for val in self.sell_cciTime.range:
            dataframe[f'cci-sell-{val}'] = ta.CCI(dataframe, timeperiod=val)

        for val in self.buy_rsiTime.range:
            dataframe[f'rsi-{val}'] = ta.RSI(dataframe, timeperiod=val)

        for val in self.sell_rsiTime.range:
            dataframe[f'rsi-sell-{val}'] = ta.RSI(dataframe, timeperiod=val)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe[f'cci-{self.buy_cciTime.value}'] < self.buy_cci.value) &
                (dataframe[f'rsi-{self.buy_rsiTime.value}'] < self.buy_rsi.value)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe[f'cci-sell-{self.sell_cciTime.value}'] > self.sell_cci.value) &
                (dataframe[f'rsi-sell-{self.sell_rsiTime.value}'] > self.sell_rsi.value)
            ),
            'exit_long'] = 1

        return dataframe
