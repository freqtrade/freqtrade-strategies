# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from freqtrade.strategy import IStrategy
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class hlhb(IStrategy):
    """
    The HLHB ("Huck loves her bucks!") System simply aims to catch short-term forex trends.
    More information in https://www.babypips.com/trading/forex-hlhb-system-explained
    """

    INTERFACE_VERSION: int = 3

    position_stacking = "True"

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.6225,
        "703": 0.2187,
        "2849": 0.0363,
        "5520": 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.3211

    # Trailing stoploss
    trailing_stop = True
    trailing_stop_positive = 0.0117
    trailing_stop_positive_offset = 0.0186
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy.
    timeframe = '4h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the "ask_strategy" section in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        'main_plot': {
            'ema5': {},
            'ema10': {},
        },
        'subplots': {
            # Subplots - each dict defines one additional plot
            "RSI": {
                'rsi': {'color': 'red'},
            },
            "ADX": {
                'adx': {},
            }
        }
    }

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['hl2'] = (dataframe["close"] + dataframe["open"]) / 2

        # Momentum Indicators
        # ------------------------------------

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=10, price='hl2')

        # # EMA - Exponential Moving Average
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)

        # ADX
        dataframe['adx'] = ta.ADX(dataframe)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 50)) &
                (qtpylib.crossed_above(dataframe['ema5'], dataframe['ema10'])) &
                (dataframe['adx'] > 25) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['rsi'], 50)) &
                (qtpylib.crossed_below(dataframe['ema5'], dataframe['ema10'])) &
                (dataframe['adx'] > 25) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'exit_long'] = 1
        return dataframe

