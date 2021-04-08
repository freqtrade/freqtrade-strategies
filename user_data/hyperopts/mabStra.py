# author: Masoud Azizi @mablue

# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

FTF, STF = 5, 10


class mabStra(IStrategy):

    # 100/100:    727 trades. 486/191/50 Wins/Draws/Losses. Avg profit   3.53 % . Median profit   5.97 % . Total profit  1502.52014358 USDT (2566.80Σ %). Avg duration 1396.1 min. Objective: -15.62092

    # Buy hyperspace params:
    buy_params = {
        'buy-div-max': 0.96451, 'buy-div-min': 0.22313
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-div-max': 0.75476, 'sell-div-min': 0.16599
    }

    # ROI table:
    minimal_roi = {
        "0": 0.45574,
        "307": 0.21971,
        "428": 0.06762,
        "1387": 0
    }

    # Stoploss:
    stoploss = -0.34773

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01573
    trailing_stop_positive_offset = 0.06651
    trailing_only_offset_is_reached = True
    # Optimal timeframe use it in your config
    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA - ex Moving Average
        dataframe['buy-fastMA'] = ta.SMA(dataframe, timeperiod=FTF)
        dataframe['buy-slowMA'] = ta.SMA(dataframe, timeperiod=STF)
        dataframe['sell-fastMA'] = ta.SMA(dataframe, timeperiod=FTF)
        dataframe['sell-slowMA'] = ta.SMA(dataframe, timeperiod=STF)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
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
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    > self.sell_params['sell-div-min']) &
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    < self.sell_params['sell-div-max'])
            ),
            'sell'] = 1
        return dataframe
