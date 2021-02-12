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

"""
author@: werkkrew
github@: https://github.com/werkkrew/freqtrade-strategies

Hyperopt for my KAMACCIRSI strategy.

Optimizes:
- Period for indicators within specified ranges
- Should RSI and/or CCI be enabled
    - Cross points for RSI / CCI on both buy and sell side separately
- Should KAMA use a crossing point or slope

Default Ranges for dynamic indicator periods:

kshortStart = 4
kshortEnd = 20
klongStart = 36
klongEnd = 72
cciStart = 12
cciEnd = 60
rsiStart = 4
rsiEnd = 40

Default ranges for cross points:
RSI:
    - Buy: 0-100
    - Sell: 0-100
CCI: 
    - Buy: 0-200
    - Sell: -200-0
"""

# Ranges for dynamic indicator periods
kshortStart = 4
kshortEnd = 20
klongStart = 36
klongEnd = 72
cciStart = 12
cciEnd = 60
rsiStart = 4
rsiEnd = 40

# Periods for static indicators, only used when --spaces does not include buy or sell
# Adjust based on optimal results
cciStatic = 18
rsiStatic = 12
kamaShortStatic = 12
kamaLongStatic = 48

class KAMACCIRSIHyperopt(IHyperOpt):

    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Dynamic TA indicators
        Used so hyperopt can optimized around the period of various indicators
        """
        for kshort in range(kshortStart, (kshortEnd + 1)):
            dataframe[f'kama-short({kshort})'] = ta.KAMA(dataframe, timeperiod=kshort)

        for klong in range(klongStart, (klongEnd + 1)):
            dataframe[f'kama-long({klong})'] = ta.KAMA(dataframe, timeperiod=klong)

        for klong in range(klongStart, (klongEnd + 1)):
            dataframe[f'kama-long-slope({klong})'] = (dataframe[f'kama-long({klong})'] / dataframe[f'kama-long({klong})'].shift())

        for ccip in range(cciStart, (cciEnd + 1)):
            dataframe[f'cci({ccip})'] = ta.CCI(dataframe, timeperiod=ccip)

        for rsip in range(rsiStart, (rsiEnd + 1)):
            dataframe[f'rsi({rsip})'] = ta.RSI(dataframe, timeperiod=rsip)

        """
        Static TA indicators.
        Only used when --spaces does not include buy or sell
        """
        dataframe['cci'] = ta.CCI(dataframe, timeperiod=cciStatic)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=rsiStatic)

        # KAMA - Kaufman Adaptive Moving Average
        dataframe['kama-short'] = ta.KAMA(dataframe, timeperiod=kamaShortStatic)
        dataframe['kama-long'] = ta.KAMA(dataframe, timeperiod=kamaLongStatic)
        dataframe['kama-long-slope'] = (dataframe['kama-long'] / dataframe['kama-long'].shift())

        return dataframe

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Ranges and Options for BUY strategy
        """
        return [
            Integer(kshortStart, kshortEnd, name='kama-short-period'),
            Integer(klongStart, klongEnd, name='kama-long-period'),
            Integer(cciStart, cciEnd, name='cci-period'),
            Integer(rsiStart, rsiEnd, name='rsi-period'),
            Integer(100, 200, name='cci-limit'),
            Integer(40, 90, name='rsi-limit'),           
            Categorical([True, False], name='cci-enabled'),
            Categorical([True, False], name='rsi-enabled'),
            Categorical(['cross', 'slope'], name='kama-trigger')
        ]

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Ranges andOptions for SELL strategy
        """
        return [
            Integer(kshortStart, kshortEnd, name='sell-kama-short-period'),
            Integer(klongStart, klongEnd, name='sell-kama-long-period'),
            Integer(cciStart, cciEnd, name='sell-cci-period'),
            Integer(rsiStart, rsiEnd, name='sell-rsi-period'),
            Integer(-200, -100, name='sell-cci-limit'),
            Integer(40, 90, name='sell-rsi-limit'), 
            Categorical([True, False], name='sell-cci-enabled'),
            Categorical([True, False], name='sell-rsi-enabled'),
            Categorical(['cross', 'slope'], name='sell-kama-trigger')
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

            if params.get('cci-enabled'):
                conditions.append(dataframe[f"cci({params['cci-period']})"] > params['cci-limit'])
            if params.get('rsi-enabled'):
                conditions.append(dataframe[f"rsi({params['rsi-period']})"] > params['rsi-limit'])

            if params['kama-trigger'] == 'cross':
                conditions.append(dataframe[f"kama-short({params['kama-short-period']})"] > dataframe[f"kama-long({params['kama-long-period']})"])

            if params['kama-trigger'] == 'slope':
                conditions.append(dataframe[f"kama-long({params['kama-long-period']})"] > 1)

            # Check that the candle had volume
            conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

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

            if params.get('sell-cci-enabled'):
                conditions.append(dataframe[f"cci({params['sell-cci-period']})"] < params['sell-cci-limit'])
            if params.get('sell-rsi-enabled'):
                conditions.append(dataframe[f"rsi({params['sell-rsi-period']})"] < params['sell-rsi-limit'])

            if params['sell-kama-trigger'] == 'cross':
                conditions.append(dataframe[f"kama-short({params['sell-kama-short-period']})"] > dataframe[f"kama-long({params['sell-kama-long-period']})"])

            if params['sell-kama-trigger'] == 'slope':
                conditions.append(dataframe[f"kama-long({params['sell-kama-long-period']})"] > 1)

            # Check that the candle had volume
            conditions.append(dataframe['volume'] > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Only used when --spaces does not include buy
        """
        dataframe.loc[
            (
                (dataframe['kama-short'] > dataframe['kama-long']) & # KAMA lines cross
                (dataframe['rsi'] > 70) &  # Signal: RSI is enabled and crosses above value
                (dataframe['cci'] > 198) &  # Signal: CCI is enabled and crosses above value
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Only used when --spaces does not include sell
        """
        dataframe.loc[
            (
                (dataframe['kama-short'] < dataframe['kama-long']) & # KAMA lines cross
                (dataframe['rsi'] < 69) &  # Signal: RSI is enabled and crosses below value
                (dataframe['cci'] < -144) &  # Signal: CCI is enabled and crosses below value
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'sell'] = 1
        return dataframe