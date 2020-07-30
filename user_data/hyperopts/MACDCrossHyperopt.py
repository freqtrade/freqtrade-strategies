import talib.abstract as ta
from pandas import DataFrame
from typing import Dict, Any, Callable, List
from functools import reduce

from skopt.space import Categorical, Dimension, Integer, Real

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt


'''
Please set the ranges to work with the optimization.
Steps reduce the number of possible triggers.
The loops go up to the end value, not including it.
'''

fastRangeBegin = 6
fastRangeEnd = 19
fastRangeStep = 2

slowRangeBegin = 20
slowRangeEnd = 52
slowRangeStep = 3

signalRangeBegin = 3
signalRangeEnd = 19
signalRangeStep = 2


class MACDCrossHyperopt(IHyperOpt):
    """
    Hyperopt file for optimizing MACD cross strategy.
    Based on the averagehyperopt.
    """

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:

        for fast in range(fastRangeBegin, fastRangeEnd, fastRangeStep):
            for slow in range(slowRangeBegin, slowRangeEnd, slowRangeStep):
                for signal in range(signalRangeBegin, signalRangeEnd, signalRangeStep):
                    macd = ta.MACD(dataframe, fastperiod=fast,
                                   slowperiod=slow, signalperiod=signal)

                    dataframe[f'MACD({fast},{slow},{signal})'] = macd['macd']
                    dataframe[f'MACDsignal({fast},{slow},{signal})'] = macd['macdsignal']

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:

        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            This strategy triggers a buy when the MACD line crosses the signal line and both are under 0.
            """
            conditions = []
            # TRIGGERS
            if 'trigger' in params:
                conditions.append(qtpylib.crossed_above(
                    dataframe[f"MACD({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"],
                    dataframe[f"MACDsignal({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"]) &

                    (dataframe[f"MACD({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"] < 0) &
                    (dataframe[f"MACDsignal({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"] < 0)
                )

            # Check that volume is not 0
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
        Define your Hyperopt space for searching strategy parameters
        """
        buyTriggerList = []
        for fast in range(fastRangeBegin, fastRangeEnd, fastRangeStep):
            for slow in range(slowRangeBegin, slowRangeEnd, slowRangeStep):
                for signal in range(signalRangeBegin, signalRangeEnd, signalRangeStep):

                    buyTriggerList.append(
                        (fast, slow, signal)
                    )
        return [
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

            conditions = []

            # TRIGGERS
            if 'sell-trigger' in params:
                conditions.append(qtpylib.crossed_below(
                    dataframe[f"MACD({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"],
                    dataframe[f"MACDsignal({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"]) &

                    (dataframe[f"MACD({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"] > 0) &
                    (dataframe[f"MACDsignal({params['trigger'][0]},{params['trigger'][1]},{params['trigger'][2]})"] > 0)
                )

            # Check that volume is not 0
            conditions.append(dataframe['volume'] > 0)

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
        for fast in range(fastRangeBegin, fastRangeEnd, fastRangeStep):
            for slow in range(slowRangeBegin, slowRangeEnd, slowRangeStep):
                for signal in range(signalRangeBegin, signalRangeEnd, signalRangeStep):

                    sellTriggerList.append(
                        (fast, slow, signal)
                    )

        return [
            Categorical(sellTriggerList, name='sell-trigger')
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of from strategy
        must align to populate_indicators in this file
        Only used when --spaces does not include buy
        """
        dataframe.loc[
            (
                qtpylib.crossed_above(
                    dataframe[f'MACD({fastRangeBegin},{slowRangeBegin},{signalRangeBegin})'],
                    dataframe[f'MACDsignal({fastRangeBegin},{slowRangeBegin},{signalRangeBegin})']) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of from strategy
        must align to populate_indicators in this file
        Only used when --spaces does not include sell
        """
        dataframe.loc[
            (
                qtpylib.crossed_below(
                    dataframe[f'MACD({fastRangeBegin},{slowRangeBegin},{signalRangeBegin})'],
                    dataframe[f'MACDsignal({fastRangeBegin},{slowRangeBegin},{signalRangeBegin})']) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'sell'] = 1

        return dataframe
