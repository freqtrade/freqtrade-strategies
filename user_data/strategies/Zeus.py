# Zeus Strategy: First Generation of GodStra Strategy with maximum AVG/MID profit in USDT
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: INSTALL TA BEFOUR RUN(pip install ta)
# IMPORTANT: Use Smallest "max_open_trades" for getting best results inside config.json
# "max_open_trades": 3,
# "stake_currency": "BNB",
# "stake_amount": "unlimited",
# "tradable_balance_ratio": 1,
# "fiat_display_currency": "USD",
# "timeframe": "4h",
# freqtrade hyperopt --hyperopt ZeusHo --hyperopt-loss SharpeHyperOptLoss --spaces buy sell roi trailing --strategy Zeus --config bnbhunter.json
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


class Zeus(IStrategy):

    # 64/100:     29 trades. 22/4/3 Wins/Draws/Losses. Avg profit  11.09%. Median profit  10.52%. Total profit  12.90910475 BNB ( 321.58Σ%). Avg duration 3533.8 min. Objective: -11.62011

    # Buy hyperspace params:
    buy_params = {
        'buy-oper-0': '<R', 'buy-real-0': 95
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-oper-0': '<R', 'sell-real-0': -67
    }

    # ROI table:
    minimal_roi = {
        "0": 0.35113,
        "1035": 0.19467,
        "1917": 0.1116,
        "7190": 0
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01661
    trailing_stop_positive_offset = 0.08806
    trailing_only_offset_is_reached = True

    stoploss = -1
    # Buy hypers
    timeframe = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add all ta features
        # Clean NaN values
        dataframe = dropna(dataframe)

        dataframe['trend_ichimoku_base'] = ta.trend.ichimoku_base_line(
            dataframe['high'],
            dataframe['low'],
            window1=9,
            window2=26,
            visual=False,
            fillna=False
        )
        KST = ta.trend.KSTIndicator(
            close=dataframe['close'],
            roc1=10,
            roc2=15,
            roc3=20,
            roc4=30,
            window1=10,
            window2=10,
            window3=10,
            window4=15,
            nsig=9,
            fillna=False
        )

        dataframe['trend_kst_diff'] = KST.kst_diff()

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        IND = 'trend_ichimoku_base'
        REAL = self.buy_params['buy-real-0']
        DFIND = dataframe[IND]

        dataframe.loc[
            (DFIND > REAL),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        IND = 'trend_kst_diff'
        REAL = self.sell_params['sell-real-0']
        DFIND = dataframe[IND]

        dataframe.loc[
            (np.isclose(DFIND, REAL)),
            'sell'] = 1

        return dataframe
