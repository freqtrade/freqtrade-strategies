# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy.interface import IStrategy

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from datetime import datetime
from freqtrade.persistence import Trade
from freqtrade.state import RunMode

class TrailingSL(IStrategy):
    """
    this is an abstract stump class, just implmenting `custom_stoploss`
    you are supposed to inherit from it in your own strategy, e.g.:

    # see example class at end of this file
    class MyAwesomeStrategy(CustomStoploss):

    """

    custom_info = {}
    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:

        SL_INDICATOR_NAME = 'atr'
        result = 1
        if self.custom_info and pair in self.custom_info and trade:
            # using current_time directly (like below) will only work in backtesting/hyperopt.
            # in live / dry-run, it'll be really the current time
            relative_sl = None
            if self.dp:
                # backtesting/hyperopt
                if self.dp.runmode.value in ('backtest', 'hyperopt'):
                    relative_sl = self.custom_info[pair].loc[current_time][SL_INDICATOR_NAME]
                # for live, dry-run, storing the dataframe is not really necessary,
                # it's available from get_analyzed_dataframe()
                else:
                    # so we need to get analyzed_dataframe from dp
                    dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=pair,
                                                                             timeframe=self.timeframe)
                    # only use .iat[-1] in live mode, otherwise you will look into the future
                    # see: https://www.freqtrade.io/en/latest/strategy-customization/#common-mistakes-when-developing-strategies
                    relative_sl = dataframe[SL_INDICATOR_NAME].iat[-1]

            if (relative_sl is not None):
                # print("custom_stoploss().relative_sl: {}".format(relative_sl))
                # calculate new_stoploss relative to current_rate
                new_stoploss = (current_rate-relative_sl)/current_rate
                # turn into relative negative offset required by `custom_stoploss` return implementation
                result = new_stoploss - 1

        # print("custom_stoploss() -> {}".format(result))
        return result

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['atr'] = ta.ATR(dataframe)
        if self.dp.runmode.value in ('backtest', 'hyperopt'):
            self.custom_info[metadata['pair']] = dataframe[['date', 'atr']].copy().set_index('date')
        return dataframe
