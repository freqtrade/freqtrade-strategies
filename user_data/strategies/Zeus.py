# Zeus Strategy: First Generation of GodStra Strategy with maximum AVG/MID profit in USDT
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: INSTALL TA BEFOUR RUN(pip install ta)
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

    # 33/200:    506 trades. 424/64/18 Wins/Draws/Losses. Avg profit   2.40%. Median profit   2.10%. Total profit  12349.45456035 USDT ( 1212.89Σ%). Avg duration 682.4 min. Objective: -116.68109

    # Buy hyperspace params:
    buy_params = {
        'buy-oper-0': '<R', 'buy-real-0': 0.09117
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-oper-0': '=R', 'sell-real-0': 0.46353
    }

    # ROI table:
    minimal_roi = {
        "0": 0.38489,
        "383": 0.19302,
        "961": 0.04516,
        "1399": 0
    }

    # Stoploss:
    stoploss = -0.18723

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01755
    trailing_stop_positive_offset = 0.02783
    trailing_only_offset_is_reached = True
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

        # Normalization
        tib = dataframe['trend_ichimoku_base']
        dataframe['trend_ichimoku_base'] = (tib-tib.min())/(tib.max()-tib.min())
        tkd = dataframe['trend_kst_diff']
        dataframe['trend_kst_diff'] = (tkd-tkd.min())/(tkd.max()-tkd.min())
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        IND = 'trend_ichimoku_base'
        REAL = self.buy_params['buy-real-0']
        OPR = self.buy_params['buy-oper-0']
        DFIND = dataframe[IND]

        if OPR == ">R":
            conditions.append(DFIND > REAL)
        elif OPR == "=R":
            conditions.append(np.isclose(DFIND, REAL))
        elif OPR == "<R":
            conditions.append(DFIND < REAL)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        IND = 'trend_kst_diff'
        REAL = self.sell_params['sell-real-0']
        DFIND = dataframe[IND]
        OPR = self.sell_params['sell-oper-0']

        if OPR == ">R":
            conditions.append(DFIND > REAL)
        elif OPR == "=R":
            conditions.append(np.isclose(DFIND, REAL))
        elif OPR == "<R":
            conditions.append(DFIND < REAL)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe
