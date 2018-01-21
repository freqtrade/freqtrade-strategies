
# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from hyperopt import hp
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy # noqa


# Update this variable if you change the class name
class_name = 'CustomStrategy'


class CustomStrategy(IStrategy):
    """
    Prod strategy 003
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

        # Stoch
        stoch = ta.STOCH(dataframe)
        dataframe['slowk'] = stoch['slowk']

        # MFI
        dataframe['mfi'] = ta.MFI(dataframe)

        # Stoch fast
        stoch_fast = ta.STOCHF(dataframe)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        # Inverse Fisher transform on RSI, values [-1.0, 1.0] (https://goo.gl/2JGGoy)
        rsi = 0.1 * (dataframe['rsi'] - 50)
        dataframe['fisher_rsi'] = (numpy.exp(2 * rsi) - 1) / (numpy.exp(2 * rsi) + 1)

        # Bollinger bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']

        # EMA - Exponential Moving Average
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)

        # SAR Parabol
        dataframe['sar'] = ta.SAR(dataframe)

        # SMA - Simple Moving Average
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=40)

        # TEMA - Triple Exponential Moving Average
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)

        # Hammer: values [0, 100]
        dataframe['CDLHAMMER'] = ta.CDLHAMMER(dataframe)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (dataframe['rsi'] < 28) &
                (dataframe['rsi'] > 0) &
                (dataframe['close'] < dataframe['sma']) &
                (dataframe['fisher_rsi'] < -0.94) &
                (dataframe['mfi'] < 16.0) &
                (
                    (dataframe['ema50'] > dataframe['ema100']) |
                    (qtpylib.crossed_above(dataframe['ema5'], dataframe['ema10']))
                ) &
                (dataframe['fastd'] > dataframe['fastk']) &
                (dataframe['fastd'] > 0)
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
                (dataframe['sar'] > dataframe['close']) &
                (dataframe['fisher_rsi'] > 0.3)
            ),
            'sell'] = 1
        return dataframe

    def hyperopt_space(self) -> List[Dict]:
        """
        Define your Hyperopt space for the strategy
        :return: Dict
        """
        space = {
            'rsi_gt': hp.choice('rsi_gt', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('rsi_gt-value', 0, 40, 1)}
            ]),
            'rsi_lt': hp.choice('rsi_lt', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('rsi_lt-value', 20, 40, 1)}
            ]),
            'close_sma': hp.choice('close_sma', [
                {'enabled': False},
                {'enabled': True}
            ]),
            'fisher_rsi': hp.choice('fisher_rsi', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('fisher_rsi-value', -1, 1, 0.1)}
            ]),
            'mfi': hp.choice('mfi', [
                {'enabled': False},
                {'enabled': True, 'value': hp.quniform('mfi-value', 5, 25, 1)}
            ]),
            'fastd_fastk': hp.choice('fastd_fastk', [
                {'enabled': False},
                {'enabled': True}
            ]),
            'fastd_gt0': hp.choice('fastd_gt0', [
                {'enabled': False},
                {'enabled': True}
            ]),
            'trigger': hp.choice('trigger', [
                {'type': 'ema5_cross_ema10'},
                {'type': 'ema20_cross_ema50'},
                {'type': 'ema50_cross_ema100'},
                {'type': 'faststoch10'},
                {'type': 'sar_reversal'},
                {'type': 'stochf_cross'},
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
            if 'rsi_gt' in params and params['rsi_gt']['enabled']:
                conditions.append(dataframe['rsi'] > params['rsi_gt']['value'])

            if 'rsi_lt' in params and params['rsi_lt']['enabled']:
                conditions.append(dataframe['rsi'] < params['rsi_lt']['value'])

            if 'close_sma' in params and params['close_sma']['enabled']:
                conditions.append(dataframe['close'] < dataframe['sma'])

            if 'fisher_rsi' in params and params['fisher_rsi']['enabled']:
                conditions.append(
                    dataframe['fisher_rsi'] < params['fisher_rsi']['value']
                )

            if 'fastd_fastk' in params and params['fastd_fastk']['enabled']:
                conditions.append(dataframe['fastd'] > dataframe['fastk'])

            if 'fastd_gt0' in params and params['fastd_gt0']['enabled']:
                conditions.append(dataframe['fastd'] > 0)

            # TRIGGERS
            triggers = {
                'ema5_cross_ema10': (qtpylib.crossed_above(
                    dataframe['ema5'], dataframe['ema10']
                )),
                'ema20_cross_ema50': (qtpylib.crossed_above(
                    dataframe['ema20'], dataframe['ema50']
                )),
                'ema50_cross_ema100': (qtpylib.crossed_above(
                    dataframe['ema50'], dataframe['ema100']
                )),
                'faststoch10': (qtpylib.crossed_above(
                    dataframe['fastd'], 10.0
                )),
                'stochf_cross': (qtpylib.crossed_above(
                    dataframe['fastk'], dataframe['fastd']
                )),
                'sar_reversal': (qtpylib.crossed_above(
                    dataframe['close'], dataframe['sar']
                )),
            }
            conditions.append(triggers.get(params['trigger']['type']))

            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

            return dataframe

        return populate_buy_trend