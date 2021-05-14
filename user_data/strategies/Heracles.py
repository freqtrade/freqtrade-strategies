# Heracles Strategy: Strongest Son of GodStra
# ( With just 1 Genome! its a bacteria :D )
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT:Add to your pairlists inside config.json (Under StaticPairList):
#   {
#       "method": "AgeFilter",
#       "min_days_listed": 100
#   },
# IMPORTANT: INSTALL TA BEFOUR RUN(pip install ta)
# ######################################################################
# Optimal config settings:
# "max_open_trades": 100,
# "stake_amount": "unlimited",

# --- Do not remove these libs ---
import logging

from numpy.lib import math
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
# import talib.abstract as ta
import pandas as pd
import ta
from ta.utils import dropna
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce
import numpy as np


class Heracles(IStrategy):
    # ROI table:
    minimal_roi = {
        "0": 0.32836,
        "1629": 0.17896,
        "6302": 0.05372,
        "10744": 0
    }

    # Stoploss:
    stoploss = -0.04655

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.02444
    trailing_stop_positive_offset = 0.04406
    trailing_only_offset_is_reached = True

    # Buy hypers
    timeframe = '12h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add all ta features
        dataframe = dropna(dataframe)

        dataframe['volatility_kcw'] = ta.volatility.keltner_channel_wband(
            dataframe['high'],
            dataframe['low'],
            dataframe['close'],
            window=20,
            window_atr=10,
            fillna=False,
            original_version=True
        )
        dataframe['volatility_dcp'] = ta.volatility.donchian_channel_pband(
            dataframe['high'],
            dataframe['low'],
            dataframe['close'],
            window=10,
            offset=0,
            fillna=False
        )
        dataframe['trend_macd_signal'] = ta.trend.macd_signal(
            dataframe['close'],
            window_slow=26,
            window_fast=12,
            window_sign=9,
            fillna=False
        )

        dataframe['trend_ema_fast'] = ta.trend.EMAIndicator(
            close=dataframe['close'], window=12, fillna=False
        ).ema_indicator()

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        DFIND = dataframe['volatility_dcp']
        DFCRS = dataframe['volatility_kcw']

        dataframe.loc[
            (DFIND < DFCRS),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        DFIND = dataframe['trend_ema_fast']
        DFCRS = dataframe['trend_macd_signal']

        dataframe.loc[
            (np.isclose(DFIND, DFCRS)),
            'sell'] = 1

        return dataframe
