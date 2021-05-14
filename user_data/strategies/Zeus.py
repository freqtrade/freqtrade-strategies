# Zeus Strategy: First Generation of GodStra Strategy with maximum
# AVG/MID profit in USDT
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: INSTALL TA BEFOUR RUN(pip install ta)
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell roi trailing --strategy Zeus
# --- Do not remove these libs ---
import logging
from freqtrade.strategy.hyper import CategoricalParameter, RealParameter

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
    # *    2/1000:     38 trades. 34/0/4 Wins/Draws/Losses. Avg profit  320.22%. Median profit  21.85%. Total profit  1.21764343 BTC ( 1217.64Σ%). Avg duration 9 days, 19:54:00 min. Objective: -10.91136

    # Buy hyperspace params:
    buy_params = {
        "buy_cat": '<R',
        "buy_real": 0.11908,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_cat": '>R',
        "sell_real": 0.59608,
    }
    buy_real = RealParameter(
        0.001, 0.999, default=0.11908, space='buy')
    buy_cat = CategoricalParameter(
        [">R", "=R", "<R"], default='<R', space='buy')
    sell_real = RealParameter(
        0.001, 0.999, default=0.59608, space='sell')
    sell_cat = CategoricalParameter(
        [">R", "=R", "<R"], default='>R', space='sell')

    # Stoploss:
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
        tib = dataframe['trend_ichimoku_base']
        dataframe['trend_ichimoku_base'] = (
            tib-tib.min())/(tib.max()-tib.min())
        tkd = dataframe['trend_kst_diff']
        dataframe['trend_kst_diff'] = (tkd-tkd.min())/(tkd.max()-tkd.min())
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        IND = 'trend_ichimoku_base'
        REAL = self.buy_real.value
        OPR = self.buy_cat.value
        DFIND = dataframe[IND]
        # print(DFIND.mean())
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
        REAL = self.sell_real.value
        OPR = self.sell_cat.value
        DFIND = dataframe[IND]
        # print(DFIND.mean())

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
