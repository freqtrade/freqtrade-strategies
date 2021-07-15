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
#
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces roi buy sell --strategy Heracles
# ######################################################################
# --- Do not remove these libs ---
from freqtrade.strategy.hyper import IntParameter, DecimalParameter
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
    ########################################## RESULT PASTE PLACE ##########################################
    # 18/100:    111 trades. 77/23/11 Wins/Draws/Losses. Avg profit   3.81%. Median profit   4.40%. Total profit  2114.06222218 USDT (  42.28Σ%). Avg duration 3 days, 3:04:00 min. Objective: -16.78579

    # Buy hyperspace params:
    buy_params = {
        "buy_crossed_indicator_shift": 5,
        "buy_div": 3.61,
        "buy_indicator_shift": 1,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_atol": 0.30989,
        "sell_crossed_indicator_shift": 2,
        "sell_indicator_shift": 5,
        "sell_rtol": 0.19449,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.725,
        "889": 0.171,
        "2776": 0.044,
        "5299": 0
    }
    # Stoploss:
    stoploss = -0.312

    ########################################## END RESULT PASTE PLACE ######################################

    # buy params
    buy_div = DecimalParameter(-5, 5, default=0.51844, decimals=4, space='buy')
    buy_indicator_shift = IntParameter(-5, 5, default=4, space='buy')
    buy_crossed_indicator_shift = IntParameter(-5, 5, default=1, space='buy')

    # sell params
    sell_rtol = DecimalParameter(1.e-10, 1.e-0, default=0.05468, decimals=10, space='sell')
    sell_atol = DecimalParameter(1.e-16, 1.e-0, default=0.00019, decimals=10, space='sell')
    sell_indicator_shift = IntParameter(-5, 5, default=4, space='sell')
    sell_crossed_indicator_shift = IntParameter(-5, 5, default=1, space='sell')

    # Optimal timeframe use it in your config
    timeframe = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
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

        # for checking crossovers!
        # but we dont need to crossovers we just calculate dividation

        # import matplotlib.pyplot as plt
        # dataframe.iloc[:,6:].plot(subplots=False)
        # plt.tight_layout()
        # plt.show()

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Buy strategy Hyperopt will build and use.
        """
        conditions = []

        IND = 'volatility_dcp'
        CRS = 'volatility_kcw'
        DFIND = dataframe[IND]
        DFCRS = dataframe[CRS]

        conditions.append(
            DFIND.shift(self.buy_indicator_shift.value).div(
                DFCRS.shift(self.buy_crossed_indicator_shift.value)
            ) <= self.buy_div.value
        )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Sell strategy Hyperopt will build and use.
        """
        conditions = []

        IND = 'trend_ema_fast'
        CRS = 'trend_macd_signal'
        DFIND = dataframe[IND]
        DFCRS = dataframe[CRS]

        conditions.append(
            np.isclose(
                DFIND.shift(self.sell_indicator_shift.value),
                DFCRS.shift(self.sell_crossed_indicator_shift.value),
                rtol=self.sell_rtol.value,
                atol=self.sell_rtol.value
            )
        )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1

        return dataframe
