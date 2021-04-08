# by: Mablue (Masoud Azizi)

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


class mabStraHo(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
            Real(0, 1, name='buy-div-min'),
            Real(0, 1, name='buy-div-max'),
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

            # div result limited to 0~1 so allways in buy position slowMa is lower than fastMa
            # optimum number will calculate by this two lines
            conditions.append(dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                              > params['buy-div-min'])
            conditions.append(dataframe['buy-fastMA'].div(dataframe['buy-slowMA'])
                              < params['buy-div-max'])

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
            Real(0, 1, name='sell-div-min'),
            Real(0, 1, name='sell-div-max'),
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

            conditions.append(dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                              > params['sell-div-min'])
            conditions.append(dataframe['sell-slowMA'].div(dataframe['sell-fastMA'])
                              < params['sell-div-max'])

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend
