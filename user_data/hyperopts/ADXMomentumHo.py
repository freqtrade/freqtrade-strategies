# author: Masoud Azizi @mablue
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


class ADXMomentumHo(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
            Integer(0, 100, name='buy-adx-value'),
            # Categorical([True, False], name='buy-adx-enabled'),
            Integer(-100, 100, name='buy-mom-value'),
            # Categorical([True, False], name='buy-mom-enabled'),
            Integer(0, 100, name='buy-pd-value'),
            # Categorical([True, False], name='buy-pd-enabled'),
            # Categorical([True, False], name='buy-com-enabled'),

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
            # if params.get('buy-adx-enabled'):
            conditions.append(dataframe['adx'] > params['buy-adx-value'])
            # if params.get('buy-mom-enabled'):
            conditions.append(dataframe['mom'] > params['buy-mom-value'])
            # if params.get('buy-pd-enabled'):
            conditions.append(dataframe['plus_di'] > params['buy-pd-value'])
            # if params.get('buy-com-enabled'):
            conditions.append(dataframe['plus_di'] > dataframe['minus_di'])

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
            Integer(0, 100, name='sell-adx-value'),
            # Categorical([True, False], name='sell-adx-enabled'),
            Integer(-10, 10, name='sell-mom-value'),
            # Categorical([True, False], name='sell-mom-enabled'),
            Integer(0, 100, name='sell-min-value'),
            # Categorical([True, False], name='sell-min-enabled'),
            # Categorical([True, False], name='sell-com-enabled'),

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
            # if params.get('sell-adx-enabled'):
            conditions.append(dataframe['adx'] > params['sell-adx-value'])
            # if params.get('sell-mom-enabled'):
            conditions.append(dataframe['mom'] < params['sell-mom-value'])
            # if params.get('sell-min-enabled'):
            conditions.append(dataframe['minus_di'] > params['sell-min-value'])
            # if params.get('sell-com-enabled'):
            conditions.append(dataframe['plus_di'] < dataframe['minus_di'])

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend
