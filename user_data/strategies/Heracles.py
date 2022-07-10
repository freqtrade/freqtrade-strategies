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
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces roi buy --strategy Heracles
# ######################################################################
# --- Do not remove these libs ---
from freqtrade.strategy import IntParameter, DecimalParameter, IStrategy
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
    # 10/100:     25 trades. 18/4/3 Wins/Draws/Losses. Avg profit   5.92%. Median profit   6.33%. Total profit  0.04888306 BTC (  48.88Σ%). Avg duration 4 days, 6:24:00 min. Objective: -11.42103

    INTERFACE_VERSION: int = 3
    # Buy hyperspace params:
    buy_params = {
        "buy_crossed_indicator_shift": 9,
        "buy_div_max": 0.75,
        "buy_div_min": 0.16,
        "buy_indicator_shift": 15,
    }

    # Sell hyperspace params:
    sell_params = {
    }

    # ROI table:
    minimal_roi = {
        "0": 0.598,
        "644": 0.166,
        "3269": 0.115,
        "7289": 0
    }

    # Stoploss:
    stoploss = -0.256

    # Optimal timeframe use it in your config
    timeframe = '4h'

    ########################################## END RESULT PASTE PLACE ######################################

    # buy params
    buy_div_min = DecimalParameter(0, 1, default=0.16, decimals=2, space='buy')
    buy_div_max = DecimalParameter(0, 1, default=0.75, decimals=2, space='buy')
    buy_indicator_shift = IntParameter(0, 20, default=16, space='buy')
    buy_crossed_indicator_shift = IntParameter(0, 20, default=9, space='buy')

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

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Buy strategy Hyperopt will build and use.
        """
        conditions = []

        IND = 'volatility_dcp'
        CRS = 'volatility_kcw'
        DFIND = dataframe[IND]
        DFCRS = dataframe[CRS]

        d = DFIND.shift(self.buy_indicator_shift.value).div(
            DFCRS.shift(self.buy_crossed_indicator_shift.value))

        # print(d.min(), "\t", d.max())
        conditions.append(
            d.between(self.buy_div_min.value, self.buy_div_max.value))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long']=1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Sell strategy Hyperopt will build and use.
        """
        dataframe.loc[:, 'exit_long'] = 0
        return dataframe
