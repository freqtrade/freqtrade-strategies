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
buyGodGenes = ['trend_ichimoku_base']
sellGodGenes = ['trend_kst_diff']

# you can filter GodGenes with this:
# GodGenes = list(filter(lambda k: 'momentum' in k, GodGenes))


class ZeusHo(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        gene = list()
        # Operations
        gene.append(Integer(-100, 100, name='buy-real-0'))
        gene.append(Categorical([">I", "=I", "<I"], name='buy-oper-0'))
        return gene

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
            OPR = params['buy-oper-0']
            IND = 'trend_ichimoku_base'
            REAL = params['buy-real-0']

            DFIND = dataframe[IND]

            if OPR == ">I":
                conditions.append(DFIND > REAL)
            elif OPR == "=I":
                conditions.append(np.isclose(DFIND, REAL))
            elif OPR == "<I":
                conditions.append(DFIND < REAL)

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
        gene = list()
        # Operations
        gene.append(Integer(-100, 100, name='sell-real-0'))
        gene.append(Categorical([">I", "=I", "<I"], name='sell-oper-0'))
        return gene

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

            OPR = params['sell-oper-0']
            IND = 'trend_kst_diff'
            REAL = params['sell-real-0']
            DFIND = dataframe[IND]

            if OPR == ">I":
                conditions.append(DFIND > REAL)
            elif OPR == "=I":
                conditions.append(np.isclose(DFIND, REAL))
            elif OPR == "<I":
                conditions.append(DFIND < REAL)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell']=1

            return dataframe

        return populate_sell_trend
