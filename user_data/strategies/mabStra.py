# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: DO NOT USE IT WITHOUT HYPEROPT:
# freqtrade hyperopt --hyperopt mabStraHo --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy mabStra --config config.json -e 100

# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

MTF, FTF, STF = 7, 14, 28


class mabStra(IStrategy):
    # 10
    # 617/5000:    364 trades. 344/11/9 Wins/Draws/Losses. Avg profit   2.70%. Median profit   1.77%. Total profit  0.41965282 BTC ( 983.46Σ%). Avg duration 794.5 min. Objective: -354.49129

    # Buy hyperspace params:
    buy_params = {
        'buy-div-max': 2.25446, 'buy-div-min': 0.29497
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-div-max': 1.54593, 'sell-div-min': 2.81436
    }

    # ROI table:
    minimal_roi = {
        "0": 0.80087,
        "1430": 0.2385,
        "2075": 0.07112,
        "4162": 0
    }

    # Trailing stop:
    trailing_stop = False
    trailing_stop_positive = 1
    trailing_stop_positive_offset = 1
    trailing_only_offset_is_reached = False

    stoploss = -1

    # Optimal timeframe use it in your config
    timeframe = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA - ex Moving Average
        dataframe['buy-mojoMA'] = ta.SMA(dataframe, timeperiod=MTF)
        dataframe['buy-fastMA'] = ta.SMA(dataframe, timeperiod=FTF)
        dataframe['buy-slowMA'] = ta.SMA(dataframe, timeperiod=STF)
        dataframe['sell-mojoMA'] = ta.SMA(dataframe, timeperiod=MTF)
        dataframe['sell-fastMA'] = ta.SMA(dataframe, timeperiod=FTF)
        dataframe['sell-slowMA'] = ta.SMA(dataframe, timeperiod=STF)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['buy-mojoMA'].div(dataframe['buy-fastMA'])
                    > self.buy_params['buy-div-min']) &
                (dataframe['buy-mojoMA'].div(dataframe['buy-fastMA'])
                    < self.buy_params['buy-div-max']) &
                (dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                    > self.buy_params['buy-div-min']) &
                (dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                    < self.buy_params['buy-div-max'])
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['sell-fastMA'].div(dataframe['sell-mojoMA'])
                    > self.sell_params['sell-div-min']) &
                (dataframe['sell-fastMA'].div(dataframe['sell-mojoMA'])
                    < self.sell_params['sell-div-max']) &
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    > self.sell_params['sell-div-min']) &
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    < self.sell_params['sell-div-max'])
            ),
            'sell'] = 1
        return dataframe
