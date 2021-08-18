# It is AfghanWoman Strategy.
# That takes her own rights like Afghanstan women
# Those who still proud and hopeful.
# Those who the most beautiful creatures in the depths of the darkest.
# Those who shine like diamonds buried in the heart of the desert ...
# Why not help when we can?
# If we believe there is no man left with them
# (Which is probably the product of the thought of painless corpses)
# Where has our humanity gone?
# Where has humanity gone?
# Why not help when we can?

# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# (First Hyperopt it.A hyperopt file is available)
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell --strategy AfghanWoman -j 2
# freqtrade backtesting --strategy AfghanWoman

# --- Do not remove these libs ---
from freqtrade.strategy.hyper import IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
from functools import reduce

##### SETINGS #####
# It hyperopt just one set of params for all buy and sell strategies if true.
DUALFIT = False
# how much Candles to check trand
TCC = 1
### END SETINGS ###


class AfghanWoman(IStrategy):
    # ###################### RESULT PLACE ######################
    # *    4/100:     80 trades. 28/0/52 Wins/Draws/Losses. Avg profit   2.64%. Median profit  -0.19%. Total profit  3366.29721754 USDT ( 336.63Σ%). Avg duration 9:09:00 min. Objective: -8.35746

    # Buy hyperspace params:
    buy_params = {
        "buy_count": 2,
        "buy_gap": 15,
        "buy_shift": 14,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_count": 5,
        "sell_gap": 13,
        "sell_shift": 4,
    }
    # ROI table:
    minimal_roi = {
        "0": 1,
        "13": 1,
        "64": 1,
        "178": 1
    }
    # Stoploss:
    stoploss = -0.256

    # Buy hypers
    timeframe = '5m'
    # #################### END OF RESULT PLACE ####################
    buy_count = IntParameter(2, 25, default=6, space='buy')
    buy_gap = IntParameter(2, 25, default=13, space='buy')
    buy_shift = IntParameter(0, 25, default=14, space='buy')
    if not DUALFIT:
        sell_count = IntParameter(2, 25, default=20, space='sell')
        sell_gap = IntParameter(2, 25, default=3, space='sell')
        sell_shift = IntParameter(0, 25, default=0, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['PLUS_DM'] = ta.PLUS_DM(dataframe, timeperiod=14)
        dataframe['MINUS_DM'] = ta.MINUS_DM(dataframe, timeperiod=14)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(dataframe['PLUS_DM'] > dataframe['MINUS_DM'])
        count = gap = shift = None

        count = self.buy_count.value
        gap = self.buy_gap.value
        shift = self.buy_shift.value

        for i in range(1, count+1):
            dataframe[f'buy-ma-{i}'] = ta.EMA(dataframe,
                                              timeperiod=int(i * gap))
            for s in range(1, shift+1):
                if i > 1:
                    conditions.append(
                        dataframe[f'buy-ma-{i}'].shift(s) >
                        dataframe[f'buy-ma-{i-1}'].shift(s)
                    )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(dataframe['PLUS_DM'] <= dataframe['MINUS_DM'])

        count = gap = shift = None

        if DUALFIT:
            count = self.buy_count.value
            gap = self.buy_gap.value
            shift = self.buy_shift.value
        else:
            count = self.sell_count.value
            gap = self.sell_gap.value
            shift = self.sell_shift.value
        for i in range(1, count+1):
            dataframe[f'buy-ma-{i}'] = ta.EMA(dataframe,
                                              timeperiod=int(i * gap))
            for s in range(1, shift+1):
                if i > 1:
                    conditions.append(
                        dataframe[f'buy-ma-{i}'].shift(s) <
                        dataframe[f'buy-ma-{i-1}'].shift(s)
                    )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
