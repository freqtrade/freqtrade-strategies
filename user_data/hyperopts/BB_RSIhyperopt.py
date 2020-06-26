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

'''
Please set the ranges to work with the optimization.
Steps reduce the number of possible triggers.
The loops go up to the end value, not including it.
'''

bbperiodRangeStart = 5
bbperiodRangeStop = 60
bbperiodRangeStep = 5

bbstdRangeStart = 1
bbstdRangeStop = 4
bbstdRangeStep = 0.5

class BB_RSIhyperopt(IHyperOpt):
    """
    Hyperopt file for optimizing a Bollinger Band strategy with RSI as guard.
    Based on the averagehyperopt.
    """
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        This method can also be loaded from the strategy, if it doesn't exist in the hyperopt class.
        """
        dataframe['rsi'] = ta.RSI(dataframe)

        # Bollinger bands
        for bbperiod in np.arange(bbperiodRangeStart,bbperiodRangeStop,bbperiodRangeStep):
            for bbstd in np.arange(bbstdRangeStart,bbstdRangeStop,bbstdRangeStep):
                bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=bbperiod, stds=bbstd)
                dataframe[f'BB_lowerband({bbperiod},{bbstd})']= bollinger['lower']
                dataframe[f'BB_middleband({bbperiod},{bbstd})']= bollinger['mid']
                dataframe[f'BB_upperband({bbperiod},{bbstd})']= bollinger['upper']


        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by hyperopt
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use
            """
            conditions = []
            # GUARDS AND TRENDS
            if 'aboversi-enabled' in params and params['aboversi-enabled']:
                conditions.append(dataframe['rsi'] > params['rsi-value'])
            if 'belowrsi-enabled' in params and params['belowrsi-enabled']:
                conditions.append(dataframe['rsi'] < params['rsi-value'])

            # TRIGGERS
            if 'trigger' in params:
                if params['trigger'][2] == 'below':
                    conditions.append(dataframe['close'] < dataframe[f"BB_lowerband({params['trigger'][0]},{params['trigger'][1]})"])
                if params['trigger'][2] == 'crossedabove':
                    conditions.append(qtpylib.crossed_above(dataframe['close'],dataframe[f"BB_lowerband({params['trigger'][0]},{params['trigger'][1]})"]))


            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching strategy parameters
        """
        buyTriggerList = []
        for bbperiod in np.arange(bbperiodRangeStart,bbperiodRangeStop,bbperiodRangeStep):
            for bbstd in np.arange(bbstdRangeStart,bbstdRangeStop,bbstdRangeStep):
                buyTriggerList.append((bbperiod,bbstd,'crossedabove'))
                buyTriggerList.append((bbperiod,bbstd,'below'))

        return [
            Integer(10, 60, name='rsi-value'),
            Categorical([True, False], name='aboversi-enabled'),
            Categorical([True, False], name='belowrsi-enabled'),
            Categorical(buyTriggerList, name='trigger')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by hyperopt
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Sell strategy Hyperopt will build and use
            """
            # print(params)
            conditions = []
            # GUARDS AND TRENDS
            if 'sell-aboversi-enabled' in params and params['sell-aboversi-enabled']:
                conditions.append(dataframe['rsi'] > params['sell-rsi-value'])
            if 'sell-belowrsi-enabled' in params and params['sell-belowrsi-enabled']:
                conditions.append(dataframe['rsi'] < params['sell-rsi-value'])

            # TRIGGERS
            if 'sell-trigger' in params and params['sell-trigger']:

                if params['sell-trigger'][2] == 'crossedaboveupper':
                    conditions.append(qtpylib.crossed_above(dataframe['close'],dataframe[f"BB_upperband({params['sell-trigger'][0]},{params['sell-trigger'][1]})"]))
                if params['sell-trigger'][2] == 'crossedabovemiddle':
                    conditions.append(qtpylib.crossed_above(dataframe['close'],dataframe[f"BB_middleband({params['sell-trigger'][0]},{params['sell-trigger'][1]})"]))
                if params['sell-trigger'][2] == 'crossedabovelower':
                    conditions.append(qtpylib.crossed_above(dataframe['close'],dataframe[f"BB_lowerband({params['sell-trigger'][0]},{params['sell-trigger'][1]})"]))



            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters
        """
        sellTriggerList = []
        for bbperiod in np.arange(bbperiodRangeStart,bbperiodRangeStop,bbperiodRangeStep):
            for bbstd in np.arange(bbstdRangeStart,bbstdRangeStop,bbstdRangeStep):
                sellTriggerList.append((bbperiod,bbstd,'crossedaboveupper'))
                sellTriggerList.append((bbperiod,bbstd,'crossedabovemiddle'))
                sellTriggerList.append((bbperiod,bbstd,'crossedabovelower'))


        return [
            Integer(10, 90, name='sell-rsi-value'),
            Categorical([True, False], name='sell-aboversi-enabled'),
            Categorical([True, False], name='sell-belowrsi-enabled'),
            Categorical(sellTriggerList, name='sell-trigger')
        ]


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators.
        Can be a copy of the corresponding method from the strategy,
        or will be loaded from the strategy.
        Must align to populate_indicators used (either from this File, or from the strategy)
        Only used when --spaces does not include buy
        """
        dataframe.loc[
            (
                (dataframe['close'] < dataframe[f'BB_lowerband({bbperiodRangeStart},{bbstdRangeStart})']) &
                (dataframe['rsi'] < 21)
            ),
            'buy'] = 1

        return dataframe
    
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:    
        dataframe.loc[
            (
                
                (dataframe['close'] > dataframe[f'BB_upperband({bbperiodRangeStart},{bbstdRangeStart})']) &
                (dataframe['rsi'] > 67)
                
            ),
            'sell'] = 1
        return dataframe
    