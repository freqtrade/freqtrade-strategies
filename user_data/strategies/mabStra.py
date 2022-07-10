# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: DO NOT USE IT WITHOUT HYPEROPT:
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces all --strategy mabStra --config config.json -e 100

# --- Do not remove these libs ---
from freqtrade.strategy import IntParameter, DecimalParameter, IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta


class mabStra(IStrategy):

    INTERFACE_VERSION: int = 3
    # #################### RESULTS PASTE PLACE ####################
    # ROI table:
    minimal_roi = {
        "0": 0.598,
        "644": 0.166,
        "3269": 0.115,
        "7289": 0
    }

    # Stoploss:
    stoploss = -0.128
    # Buy hypers
    timeframe = '4h'

    # #################### END OF RESULT PLACE ####################

    # buy params
    buy_mojo_ma_timeframe = IntParameter(2, 100, default=7, space='buy')
    buy_fast_ma_timeframe = IntParameter(2, 100, default=14, space='buy')
    buy_slow_ma_timeframe = IntParameter(2, 100, default=28, space='buy')
    buy_div_max = DecimalParameter(
        0, 2, decimals=4, default=2.25446, space='buy')
    buy_div_min = DecimalParameter(
        0, 2, decimals=4, default=0.29497, space='buy')
    # sell params
    sell_mojo_ma_timeframe = IntParameter(2, 100, default=7, space='sell')
    sell_fast_ma_timeframe = IntParameter(2, 100, default=14, space='sell')
    sell_slow_ma_timeframe = IntParameter(2, 100, default=28, space='sell')
    sell_div_max = DecimalParameter(
        0, 2, decimals=4, default=1.54593, space='sell')
    sell_div_min = DecimalParameter(
        0, 2, decimals=4, default=2.81436, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA - ex Moving Average
        dataframe['buy-mojoMA'] = ta.SMA(dataframe,
                                         timeperiod=self.buy_mojo_ma_timeframe.value)
        dataframe['buy-fastMA'] = ta.SMA(dataframe,
                                         timeperiod=self.buy_fast_ma_timeframe.value)
        dataframe['buy-slowMA'] = ta.SMA(dataframe,
                                         timeperiod=self.buy_slow_ma_timeframe.value)
        dataframe['sell-mojoMA'] = ta.SMA(dataframe,
                                          timeperiod=self.sell_mojo_ma_timeframe.value)
        dataframe['sell-fastMA'] = ta.SMA(dataframe,
                                          timeperiod=self.sell_fast_ma_timeframe.value)
        dataframe['sell-slowMA'] = ta.SMA(dataframe,
                                          timeperiod=self.sell_slow_ma_timeframe.value)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (dataframe['buy-mojoMA'].div(dataframe['buy-fastMA'])
                    > self.buy_div_min.value) &
                (dataframe['buy-mojoMA'].div(dataframe['buy-fastMA'])
                    < self.buy_div_max.value) &
                (dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                    > self.buy_div_min.value) &
                (dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                    < self.buy_div_max.value)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['sell-fastMA'].div(dataframe['sell-mojoMA'])
                    > self.sell_div_min.value) &
                (dataframe['sell-fastMA'].div(dataframe['sell-mojoMA'])
                    < self.sell_div_max.value) &
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    > self.sell_div_min.value) &
                (dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                    < self.sell_div_max.value)
            ),
            'exit_long'] = 1
        return dataframe
