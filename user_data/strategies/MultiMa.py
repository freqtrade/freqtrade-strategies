# MultiMa Strategy
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# (First Hyperopt it.A hyperopt file is available)
#
# --- Do not remove these libs ---
from freqtrade.strategy.hyper import IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce


class MultiMa(IStrategy):

    buy_ma_count = IntParameter(2, 10, default=10, space='buy')
    buy_ma_gap = IntParameter(2, 10, default=2, space='buy')
    buy_ma_shift = IntParameter(0, 10, default=0, space='buy')
    # buy_ma_rolling = IntParameter(0, 10, default=0, space='buy')

    sell_ma_count = IntParameter(2, 10, default=10, space='sell')
    sell_ma_gap = IntParameter(2, 10, default=2, space='sell')
    sell_ma_shift = IntParameter(0, 10, default=0, space='sell')
    # sell_ma_rolling = IntParameter(0, 10, default=0, space='sell')

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
    timeframe = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA - Simple Moving Average

        for i in range(1, self.buy_ma_count.value+1):
            dataframe[f'buy-ma-{i}'] = ta.SMA(dataframe,
                                              timeperiod=int(i * self.buy_ma_gap.value))

        for i in range(1, self.sell_ma_count.value+1):
            dataframe[f'sell-ma-{i}'] = ta.SMA(dataframe,
                                               timeperiod=int(i * self.sell_ma_gap.value))

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        for i in range(1, self.buy_ma_count.value):
            if i > 1:
                shift = self.buy_ma_shift.value
                for shift in range(self.buy_ma_shift.value):
                    conditions.append(
                        dataframe[f'buy-ma-{i}'].shift(shift) >
                        dataframe[f'buy-ma-{i-1}'].shift(shift)
                    )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        for i in range(1, self.sell_ma_count.value):
            if i > 1:
                shift = self.sell_ma_shift.value
                for shift in range(self.sell_ma_shift.value):
                    conditions.append(
                        dataframe[f'sell-ma-{i}'].shift(shift) <
                        dataframe[f'sell-ma-{i-1}'].shift(shift)
                    )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
