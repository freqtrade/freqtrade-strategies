# Zeus Strategy: First Generation of GodStra Strategy with maximum
# AVG/MID profit in USDT
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: INSTALL TA BEFOUR RUN(pip install ta)
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell roi --strategy Zeus
# --- Do not remove these libs ---
import logging
from freqtrade.strategy import CategoricalParameter, DecimalParameter

from numpy.lib import math
from freqtrade.strategy import IStrategy
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

    # *    1/43:     86 trades. 72/6/8 Wins/Draws/Losses. Avg profit  12.66%. Median profit  11.99%. Total profit  0.10894395 BTC ( 108.94Σ%). Avg duration 3 days, 0:31:00 min. Objective: -48.48793
    # "max_open_trades": 10,
    # "stake_currency": "BTC",
    # "stake_amount": 0.01,
    # "tradable_balance_ratio": 0.99,
    # "timeframe": "4h",
    # "dry_run_wallet": 0.1,

    INTERFACE_VERSION: int = 3
    # Buy hyperspace params:
    buy_params = {
        "buy_cat": "<R",
        "buy_real": 0.0128,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_cat": "=R",
        "sell_real": 0.9455,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.564,
        "567": 0.273,
        "2814": 0.12,
        "7675": 0
    }

    # Stoploss:
    stoploss = -0.256

    buy_real = DecimalParameter(
        0.001, 0.999, decimals=4, default=0.11908, space='buy')
    buy_cat = CategoricalParameter(
        [">R", "=R", "<R"], default='<R', space='buy')
    sell_real = DecimalParameter(
        0.001, 0.999, decimals=4, default=0.59608, space='sell')
    sell_cat = CategoricalParameter(
        [">R", "=R", "<R"], default='>R', space='sell')

    # Buy hypers
    timeframe = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add all ta features

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

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
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
                'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
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
                'exit_long'] = 1

        return dataframe
