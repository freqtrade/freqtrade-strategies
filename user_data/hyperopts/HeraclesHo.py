# Heracles Strategy Hyperopt
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: INSTALL TA BEFOUR RUN:
# :~$ pip install ta
# freqtrade hyperopt --hyperopt GodStraHo --hyperopt-loss SharpeHyperOptLossDaily --gene all --strategy GodStra --config config.json -e 100

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
# import talib.abstract as ta  # noqa
from ta import add_all_ta_features
from ta.utils import dropna
import freqtrade.vendor.qtpylib.indicators as qtpylib
# this is your trading strategy DNA Size
# you can change it and see the results...


class HeraclesHo(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """

        return [
            Real(-0.1, 1.1, name='buy-div'),
            Integer(0, 5, name='DFINDShift'),
            Integer(0, 5, name='DFCRSShift'),
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

            IND = 'volatility_dcp'
            CRS = 'volatility_kcw'
            DFIND = dataframe[IND]
            DFCRS = dataframe[CRS]

            conditions.append(
                DFIND.shift(params['DFINDShift']).div(
                    DFCRS.shift(params['DFCRSShift'])
                ) <= params['buy-div']
            )

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @ staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return [
            Real(1.e-10, 1.e-0, name='sell-rtol'),
            Real(1.e-16, 1.e-0, name='sell-atol'),
            Integer(0, 5, name='DFINDShift'),
            Integer(0, 5, name='DFCRSShift'),
        ]

    @ staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
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
                    DFIND.shift(params['DFINDShift']),
                    DFCRS.shift(params['DFCRSShift']),
                    rtol=params['sell-rtol'],
                    atol=params['sell-atol']
                )
            )

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell']=1

            return dataframe

        return populate_sell_trend
