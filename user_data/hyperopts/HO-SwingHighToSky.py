# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
from pandas import DataFrame
from typing import Dict, Any, Callable, List
from functools import reduce

import numpy as np
from skopt.space import Categorical, Dimension, Integer, Real
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt

__author__      = "Kevin Ossenbrück"
__copyright__   = "Free For Use"
__credits__     = ["Bloom Trading, Mohsen Hassan"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Kevin Ossenbrück"
__email__       = "kevin.ossenbrueck@pm.de"
__status__      = "Live"

cciTimeMin = 10
cciTimeMax = 80
cciValueMin = -200
cciValueMax = 200
cciTimeRange = range(cciTimeMin, cciTimeMax)

rsiTimeMin = 10
rsiTimeMax = 80
rsiValueMin = 10
rsiValueMax = 90
rsiTimeRange = range(rsiTimeMin, rsiTimeMax)

class HOSwingHighToSky(IHyperOpt):

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:

        for cciTime in cciTimeRange:

            cciName = "cci-" + str(cciTime)
            dataframe[cciName] = ta.CCI(dataframe, timeperiod = cciTime)

        for rsiTime in rsiTimeRange:

            rsiName = "rsi-" + str(rsiTime)
            dataframe[rsiName] = ta.RSI(dataframe, timeperiod = rsiTime)

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            conditions = []

            # TRIGGERS & GUARDS
            if 'cci-buy-trigger' in params:

                for cciTime in cciTimeRange:

                    cciName = "cci-" + str(cciTime)

                    if params['cci-buy-trigger'] == cciName:
                        conditions.append(dataframe[cciName] < params["cci-buy-value"])
                        conditions.append(dataframe['volume'] > 0)

            if 'rsi-buy-trigger' in params:

                for rsiTime in rsiTimeRange:

                    rsiName = "rsi-" + str(rsiTime)

                    if params['rsi-buy-trigger'] == rsiName:
                        conditions.append(dataframe[rsiName] < params["rsi-buy-value"])
                        conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:

        cciBuyTriggerList = []
        rsiBuyTriggerList = []

        for cciTime in cciTimeRange:

            cciName = "cci-" + str(cciTime)
            cciBuyTriggerList.append(cciName)

        for rsiTime in rsiTimeRange:

            rsiName = "rsi-" + str(rsiTime)
            rsiBuyTriggerList.append(rsiName)

        return [
            Integer(cciValueMin, cciValueMax, name='cci-buy-value'),
            Integer(rsiValueMin, rsiValueMax, name='rsi-buy-value'),
            Categorical(cciBuyTriggerList, name='cci-buy-trigger'),
            Categorical(rsiBuyTriggerList, name='rsi-buy-trigger')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            conditions = []

            # TRIGGERS & GUARDS
            if 'cci-sell-trigger' in params:

                for cciTime in cciTimeRange:

                    cciName = "cci-" + str(cciTime)

                    if params['cci-sell-trigger'] == cciName:
                        conditions.append(dataframe[cciName] > params["cci-sell-value"])

            if 'rsi-sell-trigger' in params:

                for rsiTime in rsiTimeRange:

                    rsiName = "rsi-" + str(rsiTime)

                    if params['rsi-sell-trigger'] == rsiName:
                        conditions.append(dataframe[rsiName] > params["rsi-sell-value"])

            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:

        cciSellTriggerList = []
        rsiSellTriggerList = []

        for cciTime in cciTimeRange:

            cciName = "cci-" + str(cciTime)
            cciSellTriggerList.append(cciName)

        for rsiTime in rsiTimeRange:

            rsiName = "rsi-" + str(rsiTime)
            rsiSellTriggerList.append(rsiName)

        return [
            Integer(cciValueMin, cciValueMax, name='cci-sell-value'),
            Integer(rsiValueMin, rsiValueMax, name='rsi-sell-value'),
            Categorical(cciSellTriggerList, name='cci-sell-trigger'),
            Categorical(rsiSellTriggerList, name='rsi-sell-trigger')
        ]
