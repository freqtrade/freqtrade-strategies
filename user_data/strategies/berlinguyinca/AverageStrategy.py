# --- Do not remove these libs ---
from functools import reduce
from freqtrade.strategy import IStrategy
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class AverageStrategy(IStrategy):
    """

    author@: Gert Wohlgemuth

    idea:
        buys and sells on crossovers - doesn't really perfom that well and its just a proof of concept
    """

    INTERFACE_VERSION: int = 3
    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.5
    }

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.2

    # Optimal timeframe for the strategy
    timeframe = '4h'

    buy_range_short = IntParameter(5, 20, default=8)
    buy_range_long = IntParameter(20, 120, default=21)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Combine all ranges ... to avoid duplicate calculation
        for val in list(set(list(self.buy_range_short.range) + list(self.buy_range_long.range))):
            dataframe[f'ema{val}'] = ta.EMA(dataframe, timeperiod=val)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                qtpylib.crossed_above(
                    dataframe[f'ema{self.buy_range_short.value}'],
                    dataframe[f'ema{self.buy_range_long.value}']
                ) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                qtpylib.crossed_above(
                    dataframe[f'ema{self.buy_range_long.value}'],
                    dataframe[f'ema{self.buy_range_short.value}']
                    ) &
                (dataframe['volume'] > 0)
            ),
            'exit_long'] = 1
        return dataframe
