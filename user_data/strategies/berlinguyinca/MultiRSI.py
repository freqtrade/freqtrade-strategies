# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------
import talib.abstract as ta


class MultiRSI(IStrategy):
    """

    author@: Gert Wohlgemuth

    based on work from Creslin

    """
    minimal_roi = {
        "0": 0.01
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.05

    # Optimal ticker interval for the strategy
    ticker_interval = '5m'

    def get_ticker_indicator(self):
        return int(self.ticker_interval[:-1])

    def populate_indicators(self, dataframe: DataFrame) -> DataFrame:
        from technical.util import resample_to_interval
        from technical.util import resampled_merge

        dataframe['sma5'] = ta.SMA(dataframe, timeperiod=5)
        dataframe['sma200'] = ta.SMA(dataframe, timeperiod=200)

        # resample our dataframes
        dataframe_short = resample_to_interval(dataframe, self.get_ticker_indicator() * 2)
        dataframe_long = resample_to_interval(dataframe, self.get_ticker_indicator() * 8)

        # compute our RSI's
        dataframe_short['rsi'] = ta.RSI(dataframe_short, timeperiod=14)
        dataframe_long['rsi'] = ta.RSI(dataframe_long, timeperiod=14)

        # merge dataframe back together
        dataframe = resampled_merge(dataframe, dataframe_short)
        dataframe = resampled_merge(dataframe, dataframe_long)

        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        dataframe.fillna(method='ffill', inplace=True)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame) -> DataFrame:
        dataframe.loc[
            (
                # must be bearish
                (dataframe['sma5'] >= dataframe['sma200']) &
                (dataframe['rsi'] < (dataframe['resample_{}_rsi'.format(self.get_ticker_indicator() * 8)] - 20))
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > dataframe['resample_{}_rsi'.format(self.get_ticker_indicator()*2)]) &
                (dataframe['rsi'] > dataframe['resample_{}_rsi'.format(self.get_ticker_indicator()*8)])
            ),
            'sell'] = 1
        return dataframe
