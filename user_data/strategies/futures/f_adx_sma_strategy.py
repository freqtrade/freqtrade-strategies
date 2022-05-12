# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
from functools import reduce
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IStrategy,
    IntParameter,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# This class is a sample. Feel free to customize it.
class FAdxSmaStrategy(IStrategy):

    INTERFACE_VERSION = 3
    timeframe = "1h"
    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {"60": 0.075, "30": 0.1, "0": 0.05}
    # minimal_roi = {"0": 1}

    stoploss = -0.05
    can_short = True

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 14

    # Hyperoptable parameters

    # Define the guards spaces
    pos_entry_adx = DecimalParameter(15, 40, decimals=1, default=30.0, space="buy")
    pos_exit_adx = DecimalParameter(15, 40, decimals=1, default=30.0, space="sell")

    # Define the parameter spaces
    adx_period = IntParameter(4, 24, default=14)
    sma_short_period = IntParameter(4, 24, default=12)
    sma_long_period = IntParameter(12, 175, default=48)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # Calculate all adx values
        for val in self.adx_period.range:
            dataframe[f"adx_{val}"] = ta.ADX(dataframe, timeperiod=val)

        # Calculate all sma_short values
        for val in self.sma_short_period.range:
            dataframe[f"sma_short_{val}"] = ta.SMA(dataframe, timeperiod=val)

        # Calculate all sma_long values
        for val in self.sma_long_period.range:
            dataframe[f"sma_long_{val}"] = ta.SMA(dataframe, timeperiod=val)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions_long = []
        conditions_short = []

        # GUARDS AND TRIGGERS
        conditions_long.append(
            dataframe[f"adx_{self.adx_period.value}"] > self.pos_entry_adx.value
        )
        conditions_short.append(
            dataframe[f"adx_{self.adx_period.value}"] > self.pos_entry_adx.value
        )

        conditions_long.append(
            qtpylib.crossed_above(
                dataframe[f"sma_short_{self.sma_short_period.value}"],
                dataframe[f"sma_long_{self.sma_long_period.value}"],
            )
        )
        conditions_short.append(
            qtpylib.crossed_below(
                dataframe[f"sma_short_{self.sma_short_period.value}"],
                dataframe[f"sma_long_{self.sma_long_period.value}"],
            )
        )

        dataframe.loc[
            reduce(lambda x, y: x & y, conditions_long),
            "enter_long",
        ] = 1

        dataframe.loc[
            reduce(lambda x, y: x & y, conditions_short),
            "enter_short",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions_close = []
        conditions_close.append(
            dataframe[f"adx_{self.adx_period.value}"] < self.pos_entry_adx.value
        )

        dataframe.loc[
            reduce(lambda x, y: x & y, conditions_close),
            "exit_long",
        ] = 1

        dataframe.loc[
            reduce(lambda x, y: x & y, conditions_close),
            "exit_short",
        ] = 1

        return dataframe
