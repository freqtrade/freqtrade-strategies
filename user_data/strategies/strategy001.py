
# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from hyperopt import hp
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# Update this variable if you change the class name
class_name = 'CustomStrategy'


class CustomStrategy(IStrategy):
    """
    Prod strategy 001
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

        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)

        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['ha_open'] = heikinashi['open']
        dataframe['ha_close'] = heikinashi['close']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                qtpylib.crossed_above(dataframe['ema20'], dataframe['ema50']) &
                (dataframe['ha_close'] > dataframe['ema20']) &
                (dataframe['ha_open'] < dataframe['ha_close'])  # green bar
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
                qtpylib.crossed_above(dataframe['ema50'], dataframe['ema100']) &
                (dataframe['ha_close'] < dataframe['ema20']) &
                (dataframe['ha_open'] > dataframe['ha_close'])  # red bar
            ),
            'sell'] = 1
        return dataframe

    def hyperopt_space(self) -> List[Dict]:
        """
        Define your Hyperopt space for the strategy
        :return: Dict
        """
        space = {
            'ha_close_ema20': hp.choice('ha_close_ema20', [
                {'enabled': False},
                {'enabled': True}
            ]),
            'ha_open_close': hp.choice('ha_open_close', [
                {'enabled': False},
                {'enabled': True}
            ]),
            'trigger': hp.choice('trigger', [
                {'type': 'ema50_cross_ema100'},
                {'type': 'ema5_cross_ema10'},
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
            if 'ha_close_ema20' in params and params['ha_close_ema20']['enabled']:
                conditions.append(dataframe['ha_close'] > dataframe['ema20'])

            if 'ha_open_close' in params and params['ha_open_close']['enabled']:
                conditions.append(dataframe['ha_open'] < dataframe['ha_close'])


            # TRIGGERS
            triggers = {
                'ema20_cross_ema50': (qtpylib.crossed_above(dataframe['ema20'], dataframe['ema50'])),
                'ema50_cross_ema100': (qtpylib.crossed_above(dataframe['ema50'], dataframe['ema100'])),
            }
            conditions.append(triggers.get(params['trigger']['type']))

            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

            return dataframe

        return populate_buy_trend