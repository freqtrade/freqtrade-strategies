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
    # +--------+-------------+----------+------------------+--------------+-------------------------------+----------------+-------------+
    # |   Best |       Epoch |   Trades |    Win Draw Loss |   Avg profit |                        Profit |   Avg duration |   Objective |
    # |--------+-------------+----------+------------------+--------------+-------------------------------+----------------+-------------|
    # | * Best |     3/10000 |      173 |     85   81    7 |        3.01% |  620.75905077 USDT  (520.87%) |      2,888.3 m |    -40.2497 |
    # | * Best |     5/10000 |      191 |    103   78   10 |        2.86% |  750.69797015 USDT  (547.02%) |      2,675.5 m |    -60.2058 |
    # | * Best |     7/10000 |      194 |    107   80    7 |        3.41% | 1,175.92643785 USDT  (661.67%) |      2,576.3 m |     -62.129 |
    # | * Best |    13/10000 |      191 |    104   78    9 |        3.07% |  767.17774276 USDT  (586.41%) |      2,676.1 m |    -64.2776 |
    # | * Best |    20/10000 |      395 |    279  108    8 |        3.94% | 4,750.85816781 USDT (1,558.19%) |      1,238.4 m |    -121.725 |
    # [Epoch 33 of 10000 (  0%)] |/                                                              | [ETA:   2:56:10, Elapsed Time: 0:00:34]^C
    # User interrupted..
    # Best result:
    # *   20/10000:    395 trades. 279/108/8 Wins/Draws/Losses. Avg profit   3.94%. Median profit   2.52%. Total profit  4750.85816781 USDT ( 1558.19Σ%). Avg duration 1238.4 min. Objective: -121.72542

    # Buy hyperspace params:
    buy_params = {
        'buy-oper-0': '<R', 'buy-real-0': 0.95244
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-oper-0': '=R', 'sell-real-0': 0.29348
    }

    # ROI table:
    minimal_roi = {
        "0": 0.50334,
        "282": 0.1246,
        "552": 0.02526,
        "1100": 0
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.05256
    trailing_stop_positive_offset = 0.08016
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

        # Normalization
        dataframe['trend_ichimoku_base'] = dataframe['trend_ichimoku_base']/(
            dataframe['trend_ichimoku_base'].max()-dataframe['trend_ichimoku_base'].min()
        )

        dataframe['trend_kst_diff'] = dataframe['trend_kst_diff']/(
            dataframe['trend_kst_diff'].max()-dataframe['trend_kst_diff'].min()
        )
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
