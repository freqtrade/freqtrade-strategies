# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

import talib.abstract as ta
import numpy as np
import freqtrade.vendor.qtpylib.indicators as qtpylib
from pandas import DataFrame
from typing import Dict, Any, Callable, List
from functools import reduce
from skopt.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt_interface import IHyperOpt

__author__ = "Kevin Ossenbrueck"
__github__ = "github.com/OtenMoten"
__linkedin__ = "linkedin.com/in/kevin-ossenbrueck/?locale=en_US"
__twitter__ = "twitter.com/ossenbrueck"
__instagram__ = "instagram.com/kevin_ossenbrueck"
__facebook__ = "facebook.com/kevin.ossenbrueck"
__creator__ = ["github.com/xmatthias", "github.com/mishaker"]
__credits__ = ["MontrealTradingGroup", "Udemy", "Mohsen Hassan", "Ilyass Tabiai"]
__version__ = "3.0"
__copyright__ = "GNU GPL"
__status__ = "Live"

"""
I was inspired by: https://github.com/freqtrade/freqtrade-strategies/blob/master/user_data/strategies/Strategy005.py
Therefore, I wrote this hyperopt to make it more better. Thank you xmatthias and mishaker!
"""

# Rolling volume range
volumeAvgValueMin = 50
volumeAvgValueMax = 300

# RSI range
rsiValueMin = 1
rsiValueMax = 100

# STOCH FAST range
fastdValueMin = 1
fastdValueMax = 100

# MINUS DI range
minusdiValueMin = 1
minusdiValueMax = 100

fishRsiNormaValueMin = 1
fishRsiNormaValueMax = 100


class HODobby(IHyperOpt):
    """
    Hyperopt file for Strategy005
    """

    ############### THIS STRATEGY IS DESIGNED FOR 5m TIMEFRAME ###############

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:

        # MACD
        # tadoc.org/indicator/MACD.htm
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']

        # MINUS DI
        # tadoc.org/indicator/MINUS_DI.htm
        dataframe['minus_di'] = ta.MINUS_DI(dataframe)

        # RSI
        # tadoc.org/indicator/RSI.htm
        # tradingview.com/scripts/fishertransform/
        # goo.gl/2JGGoy
        dataframe['rsi'] = ta.RSI(dataframe)
        rsi = 0.1 * (dataframe['rsi'] - 50)
        dataframe['fisher_rsi'] = (np.exp(2 * rsi) - 1) / (np.exp(2 * rsi) + 1) # Inverse Fisher transform on RSI, values [-1.0, 1.0]
        dataframe['fisher_rsi_norma'] = 50 * (dataframe['fisher_rsi'] + 1) # Inverse Fisher transform on RSI normalized, value [0.0, 100.0]

        # STOCH FAST
        # tadoc.org/indicator/STOCHF.htm
        stoch_fast = ta.STOCHF(dataframe)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']

        # SAR
        dataframe['sar'] = ta.SAR(dataframe)

        # SMA
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=50)

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            conditions = []

            # TRIGGER and GUARD
            if 'buy-trigger' in params:

                conditions.append(dataframe['close'] > 0.00000200)
                conditions.append(dataframe['volume'] > dataframe['volume'].rolling(params['volumeAVG-buy-value']).mean())
                conditions.append(dataframe['close'] < dataframe['sma'])
                conditions.append(dataframe['rsi'] > params['rsi-buy-value'])
                conditions.append(dataframe['fastd'] > dataframe['fastk'])
                conditions.append(dataframe['fastd'] > params['fastd-buy-value'])
                conditions.append(dataframe['fisher_rsi_norma'] < params['fishRsiNorma-buy-value'])

            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:

        buyTriggerList = ["True"]

        return [
            Integer(volumeAvgValueMin, volumeAvgValueMax, name='volumeAVG-buy-value'),
            Integer(rsiValueMin, rsiValueMax, name='rsi-buy-value'),
            Integer(fastdValueMin, fastdValueMax, name='fastd-buy-value'),
            Integer(fishRsiNormaValueMin, fishRsiNormaValueMax, name='fishRsiNorma-buy-value'),
            Categorical(buyTriggerList, name='buy-trigger')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:

            # TRIGGERS and GUARDS
            # Solving a mistery: Which sell trigger is better?
            # The winner of both will be displayed in the output of the hyperopt.

            conditions = []

            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'rsi-macd-minusdi':
                    conditions.append(qtpylib.crossed_above(dataframe['rsi'], params['rsi-sell-value']))
                    conditions.append(dataframe['macd'] < 0)
                    conditions.append(dataframe['minus_di'] > params['minusdi-sell-value'])

            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'sar-fisherRsi':
                    conditions.append(dataframe['sar'] > dataframe['close'])
                    conditions.append(dataframe['fisher_rsi'] > params['fishRsiNorma-sell-value'])

            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:

        sellTriggerList = ["rsi-macd-minusdi", "sar-fisherRsi"]

        return [
            Integer(rsiValueMin, rsiValueMax, name='rsi-sell-value'),
            Integer(minusdiValueMin, minusdiValueMax, name='minusdi-sell-value'),
            Integer(fishRsiNormaValueMin, fishRsiNormaValueMax, name='fishRsiNorma-sell-value'),
            Categorical(sellTriggerList, name='sell-trigger')
        ]
