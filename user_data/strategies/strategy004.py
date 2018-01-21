
# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from hyperopt import hp
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta


# Update this variable if you change the class name
class_name = 'CustomStrategy'


class CustomStrategy(IStrategy):
    """
    Prod strategy 004
    author@: Gerald Lonlas
    github@: https://github.com/glonlas/freqtrade-strategies
    """

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "60":  0.01,
        "30":  0.03,
        "20":  0.04,
        "0":  0.05
    }

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.3

    # Optimal ticker interval for the strategy
    ticker_interval = 5

    def populate_indicators(self, dataframe: DataFrame) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        """

        # ADX
        dataframe['adx'] = ta.ADX(dataframe)
        dataframe['slowadx'] = ta.ADX(dataframe, 35)

        # Commodity Channel Index: values Oversold:<-100, Overbought:>100
        dataframe['cci'] = ta.CCI(dataframe)

        # Stoch
        stoch = ta.STOCHF(dataframe, 5)
        dataframe['fastd'] = stoch['fastd']
        dataframe['fastk'] = stoch['fastk']
        dataframe['fastk-previous'] = dataframe.fastk.shift(1)
        dataframe['fastd-previous'] = dataframe.fastd.shift(1)

        # Slow Stoch
        slowstoch = ta.STOCHF(dataframe, 50)
        dataframe['slowfastd'] = slowstoch['fastd']
        dataframe['slowfastk'] = slowstoch['fastk']
        dataframe['slowfastk-previous'] = dataframe.slowfastk.shift(1)
        dataframe['slowfastd-previous'] = dataframe.slowfastd.shift(1)

        # EMA - Exponential Moving Average
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)

        dataframe['mean-volume'] = dataframe['volume'].mean()

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (
                    (dataframe['adx'] > 50) |
                    (dataframe['slowadx'] > 26)
                ) &
                (dataframe['cci'] < -100) &
                (
                    (dataframe['fastk-previous'] < 20) &
                    (dataframe['fastd-previous'] < 20)
                ) &
                (
                    (dataframe['slowfastk-previous'] < 30) &
                    (dataframe['slowfastd-previous'] < 30)
                ) &
                (dataframe['fastk-previous'] < dataframe['fastd-previous']) &
                (dataframe['fastk'] > dataframe['fastd']) &
                (dataframe['mean-volume'] > 0.75) &
                (dataframe['close'] > 0.00000100)
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (dataframe['slowadx'] < 25) &
                ((dataframe['fastk'] > 70) | (dataframe['fastd'] > 70)) &
                (dataframe['fastk-previous'] < dataframe['fastd-previous']) &
                (dataframe['close'] > dataframe['ema5'])
            ),
            'sell'] = 1
        return dataframe

    def hyperopt_space(self) -> List[Dict]:
        """
        Define your Hyperopt space for the strategy
        :return: Dict
        """
        space = {
            'adx': hp.choice('adx', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('adx-value', 20, 80, 1)}
            ]),
            'slowadx': hp.choice('slowadx', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('slowadx-value', 20, 80, 1)}
            ]),
            'cci': hp.choice('cci', [
                {'enabled': False},
                {'enabled': True}
            ]),
            'fastkd': hp.choice('fastkd', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('fastkd-value', 0, 80, 1)}
            ]),
            'slowfastkd': hp.choice('slowfastkd', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('slowfastkd-value', 0, 80, 1)}
            ]),
            'fastk_fastd_prev': hp.choice('fastk_fastd_prev', [
                {'enabled': False},
                {'enabled': True}
            ]),
            'meanvolume': hp.choice('meanvolume', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('meanvolume-value', 0.0, 1.0, 1)}
            ]),

            'trigger': hp.choice('trigger', [
                {'type': 'fastk_fastd'},
            ]),
            'stoploss': hp.uniform('stoploss', -0.5, -0.01),
        }
        return space

    def buy_strategy_generator(self, params) -> None:
        """
        Define the buy strategy parameters to be used by hyperopt
        """
        def populate_buy_trend(dataframe: DataFrame) -> DataFrame:
            conditions = []
            # GUARDS AND TRENDS
            if 'adx' in params and params['adx']['enabled']:
                conditions.append(dataframe['adx'] > params['adx']['value'])

            if 'slowadx' in params and params['slowadx']['enabled']:
                conditions.append(dataframe['slowadx'] > params['slowadx']['value'])

            if 'cci' in params and params['cci']['enabled']:
                conditions.append(dataframe['cci'] == 100)

            if 'fastkd' in params and params['fastkd']['enabled']:
                conditions.append(
                    (dataframe['fastk-previous'] < params['fastkd']['value']) &
                    (dataframe['fastd-previous'] < params['fastkd']['value'])
                )

            if 'slowfastkd' in params and params['slowfastkd']['enabled']:
                conditions.append(
                    (dataframe['fastk-previous'] < params['slowfastkd']['value']) &
                    (dataframe['fastd-previous'] < params['slowfastkd']['value'])
                )

            if 'fastk_fastd_prev' in params and params['fastk_fastd_prev']['enabled']:
                conditions.append((dataframe['fastk-previous'] < dataframe['fastd-previous']))

            if 'meanvolume' in params and params['meanvolume']['enabled']:
                conditions.append(dataframe['mean-volume'] > params['meanvolume']['value'])

            # TRIGGERS
            triggers = {
                'fastk_fastd': (dataframe['fastk'] > dataframe['fastd'])
            }
            conditions.append(triggers.get(params['trigger']['type']))

            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

            return dataframe

        return populate_buy_trend