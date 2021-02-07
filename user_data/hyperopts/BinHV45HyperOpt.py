# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

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


class BinHV45HyperOpt(IHyperOpt):
    """
    Hyperopt file for optimizing BinHV45Strategy.
    Uses ranges to find best parameter combination for bbdelta, closedelta and tail
    of the buy strategy.

    Sell strategy is ignored, because it's ignored in BinHV45Strategy as well.
    This strategy therefor works without explicit sell signal therefor hyperopting
    for 'roi' is recommend as well

    Also, this is just ONE way to optimize this strategy - others might also include
    disabling certain conditions completely. This file is just a starting point, feel free
    to improve and PR.
    """

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

            conditions.append(dataframe['lower'].shift().gt(0))
            conditions.append(dataframe['bbdelta'].gt(
                dataframe['close'] * params['bbdelta'] / 1000))
            conditions.append(dataframe['closedelta'].gt(
                dataframe['close'] * params['closedelta'] / 1000))
            conditions.append(dataframe['tail'].lt(dataframe['bbdelta'] * params['tail'] / 1000))
            conditions.append(dataframe['close'].lt(dataframe['lower'].shift()))
            conditions.append(dataframe['close'].le(dataframe['close'].shift()))

            # Check that the candle had volume
            conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
            Integer(1, 15, name='bbdelta'),
            Integer(15, 20, name='closedelta'),
            Integer(20, 30, name='tail'),
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            no sell signal
            """
            dataframe['sell'] = 0
            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return []
