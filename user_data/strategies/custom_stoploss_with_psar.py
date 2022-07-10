# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import IStrategy

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from datetime import datetime
from freqtrade.persistence import Trade


class CustomStoplossWithPSAR(IStrategy):
    """
    this is an example class, implementing a PSAR based trailing stop loss
    you are supposed to take the `custom_stoploss()` and `populate_indicators()`
    parts and adapt it to your own strategy

    the populate_entry_trend() function is pretty nonsencial
    """
    INTERFACE_VERSION: int = 3
    timeframe = '1h'
    stoploss = -0.2
    custom_info = {}
    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:

        result = 1
        if self.custom_info and pair in self.custom_info and trade:
            # using current_time directly (like below) will only work in backtesting/hyperopt.
            # in live / dry-run, it'll be really the current time
            relative_sl = None
            if self.dp:
                # so we need to get analyzed_dataframe from dp
                dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
                # only use .iat[-1] in callback methods, never in "populate_*" methods.
                # see: https://www.freqtrade.io/en/latest/strategy-customization/#common-mistakes-when-developing-strategies
                last_candle = dataframe.iloc[-1].squeeze()
                relative_sl = last_candle['sar']

            if (relative_sl is not None):
                # print("custom_stoploss().relative_sl: {}".format(relative_sl))
                # calculate new_stoploss relative to current_rate
                new_stoploss = (current_rate - relative_sl) / current_rate
                # turn into relative negative offset required by `custom_stoploss` return implementation
                result = new_stoploss - 1

        # print("custom_stoploss() -> {}".format(result))
        return result

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['sar'] = ta.SAR(dataframe)
        if self.dp.runmode.value in ('backtest', 'hyperopt'):
            self.custom_info[metadata['pair']] = dataframe[['date', 'sar']].copy().set_index('date')

        # all "normal" indicators:
        # e.g.
        # dataframe['rsi'] = ta.RSI(dataframe)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Placeholder Strategy: buys when SAR is smaller then candle before
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (dataframe['sar'] < dataframe['sar'].shift())
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Placeholder Strategy: does nothing
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        # Deactivated sell signal to allow the strategy to work correctly
        dataframe.loc[:, 'exit_long'] = 0
        return dataframe
