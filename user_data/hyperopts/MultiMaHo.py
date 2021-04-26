# MultiMa Strategy Hyperopt
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: hyperopt without stoploss space.
# (--spaces buy sell trailing roi)
# So: hyperopt again with just stoploss.
# IMPORTANT: do not choise results that have
# very small stoploss (for example: -2% or -0.02)
#
# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa

from freqtrade.optimize.hyperopt_interface import IHyperOpt

# --------------------------------
# Add your lib to import here
import talib.abstract as ta  # noqa
import freqtrade.vendor.qtpylib.indicators as qtpylib


class MultiMaHo(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
            Integer(2, 10, name='buy-ma-count'),
            Integer(0, 10, name='buy-ma-shift'),
            Integer(2, 10, name='buy-ma-gap'),

        ]

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by Hyperopt.
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use.
            """
            conditions = []
            # GUARDS AND TRENDS
            for i in range(1, params['buy-ma-count']):
                dataframe[f'buy-ma-{i}'] = ta.SMA(dataframe,
                                                  timeperiod=int(i * params['buy-ma-gap']))
                if i > 1:
                    for shift in range(params['buy-ma-shift']):
                        conditions.append(
                            dataframe[f'buy-ma-{i}'].shift(shift) > dataframe[f'buy-ma-{i-1}'].shift(shift))

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return [
            Integer(2, 10, name='sell-ma-count'),
            Integer(0, 10, name='sell-ma-shift'),
            Integer(2, 10, name='sell-ma-gap'),
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Sell strategy Hyperopt will build and use.
            """
            conditions = []

            # GUARDS AND TRENDS

            for i in range(1, params['sell-ma-count']):
                dataframe[f'sell-ma-{i}'] = ta.SMA(dataframe,
                                                   timeperiod=int(i * params['sell-ma-gap']))
                if i > 1:
                    for shift in range(params['sell-ma-shift']):
                        conditions.append(
                            dataframe[f'sell-ma-{i}'].shift(shift) < dataframe[f'sell-ma-{i-1}'].shift(shift))
            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend
