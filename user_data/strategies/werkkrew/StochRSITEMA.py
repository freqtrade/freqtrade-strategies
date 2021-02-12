# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
from functools import reduce
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import IStrategy

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class StochRSITEMA(IStrategy):
    """
    author@: werkkrew
    github@: https://github.com/werkkrew/freqtrade-strategies

    Reference: Strategy #1 @ https://tradingsim.com/blog/5-minute-bar/

    Trade entry signals are generated when the stochastic oscillator and relative strength index provide confirming signals.

    Buy:
        - Stoch slowd and slowk below lower band and cross above
        - Stoch slowk above slowd
        - RSI below lower band and crosses above

    You should exit the trade once the price closes beyond the TEMA in the opposite direction of the primary trend.
    There are many cases when candles are move partially beyond the TEMA line. We disregard such exit points and we exit the market when the price fully breaks the TEMA.

    Sell:
        - Candle closes below TEMA line (or open+close or average of open/close)
        - ROI, Stoploss, Trailing Stop
    """

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    """
    HYPEROPT SETTINGS
    The following is set by Hyperopt, or can be set by hand if you wish:

    - minimal_roi table
    - stoploss
    - trailing stoploss
    - for buy
        - Stoch lower band location (range: 10-50)
        - RSI period (range: 5-30)
        - RSI lower band location (range: 10-50)
    - for sell
        - TEMA period (range: 5-50)
        - TEMA trigger (close, average, both (open and close))

    PASTE OUTPUT FROM HYPEROPT HERE
    """

    # Buy hyperspace params:
    buy_params = {
       'rsi-lower-band': 46, 
       'rsi-period': 30, 
       'stoch-lower-band': 23
    }

    # Sell hyperspace params:
    sell_params = {
        'tema-period': 8, 
        'tema-trigger': 'close'
    }

    # ROI table:
    minimal_roi = {
        "0": 0.13771,
        "17": 0.07172,
        "31": 0.01378,
        "105": 0
    }

    # Stoploss:
    stoploss = -0.3279

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.32791
    trailing_stop_positive_offset = 0.40339
    trailing_only_offset_is_reached = True


    """
    END HYPEROPT
    """

    # Just here for easier adjustments if desired
    stoch_params = {
        'stoch-fastk-period': 14,
        'stoch-slowk-period': 3,
        'stoch-slowd-period': 3,
    }

    timeframe = '5m'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # Number of candles the strategy requires before producing valid signals
    # Set this to the highest period value in the indicator_params dict or highest of the ranges in the hyperopt settings (default: 72)
    startup_candle_count: int = 72
    
    """
    Not currently being used for anything, thinking about implementing this later.
    """
    def informative_pairs(self):
        # https://www.freqtrade.io/en/latest/strategy-customization/#additional-data-informative_pairs
        informative_pairs = [(f"{self.config['stake_currency']}/USD", self.timeframe)]
        return informative_pairs

    """
    Populate all of the indicators we need (note: indicators are separate for buy/sell)
    """
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Stochastic Slow
        # fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        stoch_slow = ta.STOCH(dataframe, fastk_period=self.stoch_params['stoch-fastk-period'], slowk_period=self.stoch_params['stoch-slowk-period'], slowd_period=self.stoch_params['stoch-slowd-period'])
        dataframe['stoch-slowk'] = stoch_slow['slowk']
        dataframe['stoch-slowd'] = stoch_slow['slowd']

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.buy_params['rsi-period'])

        # TEMA - Triple Exponential Moving Average
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=self.sell_params['tema-period'])

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], self.buy_params['rsi-lower-band'])) &  # Signal: RSI crosses above lower band
                (qtpylib.crossed_above(dataframe['stoch-slowd'], self.buy_params['stoch-lower-band'])) &  # Signal: Stoch slowd crosses above lower band
                (qtpylib.crossed_above(dataframe['stoch-slowk'], self.buy_params['stoch-lower-band'])) &  # Signal: Stoch slowk crosses above lower band
                (qtpylib.crossed_above(dataframe['stoch-slowk'], dataframe['stoch-slowd'])) &  # Signal: Stoch slowk crosses slowd
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []
        if self.sell_params['tema-trigger'] == 'close':
            conditions.append(dataframe['close'] < dataframe['tema'])
        if self.sell_params['tema-trigger'] == 'both':
            conditions.append((dataframe['close'] < dataframe['tema']) & (dataframe['open'] < dataframe['tema']))
        if self.sell_params['tema-trigger'] == 'average':
            conditions.append(((dataframe['close'] + dataframe['open']) / 2) < dataframe['tema'])

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe
    