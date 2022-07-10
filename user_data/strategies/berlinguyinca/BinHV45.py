# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from freqtrade.strategy import IntParameter
from pandas import DataFrame
import numpy as np
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, lower_band


class BinHV45(IStrategy):
    INTERFACE_VERSION: int = 3

    minimal_roi = {
        "0": 0.0125
    }

    stoploss = -0.05
    timeframe = '1m'

    buy_bbdelta = IntParameter(low=1, high=15, default=30, space='buy', optimize=True)
    buy_closedelta = IntParameter(low=15, high=20, default=30, space='buy', optimize=True)
    buy_tail = IntParameter(low=20, high=30, default=30, space='buy', optimize=True)

    # Hyperopt parameters
    buy_params = {
        "buy_bbdelta": 7,
        "buy_closedelta": 17,
        "buy_tail": 25,
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        bollinger = qtpylib.bollinger_bands(dataframe['close'], window=40, stds=2)

        dataframe['upper'] = bollinger['upper']
        dataframe['mid'] = bollinger['mid']
        dataframe['lower'] = bollinger['lower']
        dataframe['bbdelta'] = (dataframe['mid'] - dataframe['lower']).abs()
        dataframe['pricedelta'] = (dataframe['open'] - dataframe['close']).abs()
        dataframe['closedelta'] = (dataframe['close'] - dataframe['close'].shift()).abs()
        dataframe['tail'] = (dataframe['close'] - dataframe['low']).abs()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                dataframe['lower'].shift().gt(0) &
                dataframe['bbdelta'].gt(dataframe['close'] * self.buy_bbdelta.value / 1000) &
                dataframe['closedelta'].gt(dataframe['close'] * self.buy_closedelta.value / 1000) &
                dataframe['tail'].lt(dataframe['bbdelta'] * self.buy_tail.value / 1000) &
                dataframe['close'].lt(dataframe['lower'].shift()) &
                dataframe['close'].le(dataframe['close'].shift())
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        no sell signal
        """
        dataframe.loc[:, 'exit_long'] = 0
        return dataframe
