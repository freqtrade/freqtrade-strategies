# Khayyam Strategy
# In this strategy we try to find the best hours to buy and sell in a day.(in hourly timeframe)
# Cuz of that you should just use 1h timeframe on this strategy.
# Name of this strategy come from the Omar khayyam who was a Persian polymath, 
# mathematician, astronomer, philosopher, and poet! 
# https://en.wikipedia.org/wiki/Omar_Khayyam
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy Khayyam

from freqtrade.strategy.hyper import IntParameter
from freqtrade.strategy import IStrategy
from pandas import DataFrame
# --------------------------------
# Add your lib to import here


class Khayyam(IStrategy):
    # ROI table:
    minimal_roi = {
        "0": 0.434,
        "391": 0.116,
        "511": 0.025,
        "1919": 0
    }

    # Stoploss:
    stoploss = -0.29

    # Optimal timeframe
    timeframe = '1h'

    buy_hour_max = IntParameter(0, 24, default=24, space='buy')
    buy_hour_min = IntParameter(0, 24, default=11, space='buy')

    sell_hour_max = IntParameter(0, 24, default=6, space='sell')
    sell_hour_min = IntParameter(0, 24, default=15, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                dataframe['date'].apply(lambda x: x.hour).between(
                    self.buy_hour_min.value, self.buy_hour_max.value)
            ),

            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                dataframe['date'].apply(lambda x: x.hour).between(
                    self.sell_hour_min.value, self.sell_hour_max.value)
            ),
            'sell'] = 1
        return dataframe
