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
    # #################### END OF RESULT PLACE ####################
    # config: 3*333=1000USDT
    # *    4/700:    102 trades. 68/33/1 Wins/Draws/Losses. Avg profit   0.68%. Median profit   0.53%. Total profit  232.72544754 USDT (  23.27Σ%). Avg duration 5:23:00 min. Objective: -45.59136

    # Buy hyperspace params:
    buy_params = {
        "buy_ma_count": 3,
        "buy_ma_gap": 6,
        "buy_ma_shift": 6,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_ma_count": 4,
        "sell_ma_gap": 2,
        "sell_ma_shift": 7,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.237,
        "37": 0.08,
        "89": 0.018,
        "175": 0
    }

    # Stoploss:
    stoploss = -0.256

    # Buy hypers
    timeframe = '5m'
    # #################### END OF RESULT PLACE ####################

    buy_ma_count = IntParameter(2, 10, default=10, space='buy')
    buy_ma_gap = IntParameter(2, 10, default=2, space='buy')
    buy_ma_shift = IntParameter(0, 10, default=0, space='buy')
    # buy_ma_rolling = IntParameter(0, 10, default=0, space='buy')

    sell_ma_count = IntParameter(2, 10, default=10, space='sell')
    sell_ma_gap = IntParameter(2, 10, default=2, space='sell')
    sell_ma_shift = IntParameter(0, 10, default=0, space='sell')
    # sell_ma_rolling = IntParameter(0, 10, default=0, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # We will dinamicly generate the indicators
        # cuz this method just run one time in hyperopts
        # if you have static timeframes you can move first loop of buy and sell trends populators inside this method

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # print(self.buy_ma_count.range)
        for i in self.buy_ma_count.range:

            dataframe[f'buy-ma-{i}'] = ta.SMA(dataframe,
                                              timeperiod=int(i * self.buy_ma_gap.value))
        # print(dataframe.keys())

        conditions = []

        for i in self.buy_ma_count.range:
            if i > 2:
                shift = self.buy_ma_shift.value
                for shift in self.buy_ma_shift.range:
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
        for i in self.sell_ma_count.range:
            dataframe[f'sell-ma-{i}'] = ta.SMA(dataframe,
                                               timeperiod=int(i * self.sell_ma_gap.value))

        conditions = []

        for i in self.sell_ma_count.range:
            if i > 2:
                shift = self.sell_ma_shift.value
                for shift in self.sell_ma_shift.range:
                    conditions.append(
                        dataframe[f'sell-ma-{i}'].shift(shift) <
                        dataframe[f'sell-ma-{i-1}'].shift(shift)
                    )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
