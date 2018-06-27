# --- Do not remove these libs ---
import numpy as np
# --------------------------------
import talib.abstract as ta
from pandas import DataFrame

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy

def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, lower_band


class CombinedBinHAndCluc(IStrategy):
    # Based on a backtesting:
    # - the best perfomance is reached with "max_open_trades" = 2 (in average for any market),
    #   so it is better to increase "stake_amount" value rather then "max_open_trades" to get more profit
    # - if the market is constantly green(like in JAN 2018) the best performance is reached with
    #   "max_open_trades" = 2 and minimal_roi = 0.01
    minimal_roi = {
        "0": 0.02
    }
    stoploss = -0.15
    ticker_interval = '5m'

    def populate_indicators(self, dataframe: DataFrame) -> DataFrame:
        mid, lower = bollinger_bands(dataframe['close'], window_size=40, num_of_std=2)
        dataframe['mid'] = np.nan_to_num(mid)
        dataframe['lower'] = np.nan_to_num(lower)
        dataframe['bbdelta'] = (dataframe['mid'] - dataframe['lower']).abs()
        dataframe['pricedelta'] = (dataframe['open'] - dataframe['close']).abs()
        dataframe['closedelta'] = (dataframe['close'] - dataframe['close'].shift()).abs()
        dataframe['tail'] = (dataframe['close'] - dataframe['low']).abs()
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=5)
        rsiframe = DataFrame(dataframe['rsi']).rename(columns={'rsi': 'close'})
        dataframe['emarsi'] = ta.EMA(rsiframe, timeperiod=5)
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['adx'] = ta.ADX(dataframe)
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=50)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
        dataframe.loc[
            (
                    dataframe['lower'].shift().gt(0) &
                    dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &
                    dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &
                    dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &
                    dataframe['close'].lt(dataframe['lower'].shift()) &
                    dataframe['close'].le(dataframe['close'].shift())
            )
            |
            (
                    (dataframe['close'] < dataframe['ema100']) &
                    (dataframe['close'] < 0.985 * dataframe['bb_lowerband']) &
                    (dataframe['volume'] < (dataframe['volume'].rolling(window=30).mean().shift(1) * 20))
            )
            ,
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame) -> DataFrame:
        """
        """
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['bb_middleband'])
            ),
            'sell'] = 1
        return dataframe
