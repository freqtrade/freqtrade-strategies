# --- Do not remove these libs ---
from functools import reduce
from freqtrade.strategy import IStrategy
from freqtrade.strategy import timeframe_to_minutes
from freqtrade.strategy import BooleanParameter, IntParameter
from pandas import DataFrame
from technical.util import resample_to_interval, resampled_merge
import numpy  # noqa
# --------------------------------
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class ReinforcedSmoothScalp(IStrategy):
    """
        this strategy is based around the idea of generating a lot of potentatils buys and make tiny profits on each trade

        we recommend to have at least 60 parallel trades at any time to cover non avoidable losses
    """

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.02
    }
    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    # should not be below 3% loss

    stoploss = -0.1
    # Optimal timeframe for the strategy
    # the shorter the better
    timeframe = '1m'

    # resample factor to establish our general trend. Basically don't buy if a trend is not given
    resample_factor = 5

    buy_adx = IntParameter(20, 50, default=32, space='buy')
    buy_fastd = IntParameter(15, 45, default=30, space='buy')
    buy_fastk = IntParameter(15, 45, default=26, space='buy')
    buy_mfi = IntParameter(10, 25, default=22, space='buy')
    buy_adx_enabled = BooleanParameter(default=True, space='buy')
    buy_fastd_enabled = BooleanParameter(default=True, space='buy')
    buy_fastk_enabled = BooleanParameter(default=False, space='buy')
    buy_mfi_enabled = BooleanParameter(default=True, space='buy')

    sell_adx = IntParameter(50, 100, default=53, space='sell')
    sell_cci = IntParameter(100, 200, default=183, space='sell')
    sell_fastd = IntParameter(50, 100, default=79, space='sell')
    sell_fastk = IntParameter(50, 100, default=70, space='sell')
    sell_mfi = IntParameter(75, 100, default=92, space='sell')

    sell_adx_enabled = BooleanParameter(default=False, space='sell')
    sell_cci_enabled = BooleanParameter(default=True, space='sell')
    sell_fastd_enabled = BooleanParameter(default=True, space='sell')
    sell_fastk_enabled = BooleanParameter(default=True, space='sell')
    sell_mfi_enabled = BooleanParameter(default=False, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        tf_res = timeframe_to_minutes(self.timeframe) * 5
        df_res = resample_to_interval(dataframe, tf_res)
        df_res['sma'] = ta.SMA(df_res, 50, price='close')
        dataframe = resampled_merge(dataframe, df_res, fill_na=True)
        dataframe['resample_sma'] = dataframe[f'resample_{tf_res}_sma']

        dataframe['ema_high'] = ta.EMA(dataframe, timeperiod=5, price='high')
        dataframe['ema_close'] = ta.EMA(dataframe, timeperiod=5, price='close')
        dataframe['ema_low'] = ta.EMA(dataframe, timeperiod=5, price='low')
        stoch_fast = ta.STOCHF(dataframe, 5, 3, 0, 3, 0)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']
        dataframe['adx'] = ta.ADX(dataframe)
        dataframe['cci'] = ta.CCI(dataframe, timeperiod=20)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['mfi'] = ta.MFI(dataframe)

        # required for graphing
        bollinger = qtpylib.bollinger_bands(dataframe['close'], window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['bb_middleband'] = bollinger['mid']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []
        if self.buy_mfi_enabled.value:
            conditions.append(dataframe['mfi'] < self.buy_mfi.value)
        if self.buy_fastd_enabled.value:
            conditions.append(dataframe['fastd'] < self.buy_fastd.value)
        if self.buy_fastk_enabled.value:
            conditions.append(dataframe['fastk'] < self.buy_fastk.value)
        if self.buy_adx_enabled.value:
            conditions.append(dataframe['adx'] > self.buy_adx.value)

        # Some static conditions which always apply
        conditions.append(qtpylib.crossed_above(dataframe['fastk'], dataframe['fastd']))
        conditions.append(dataframe['resample_sma'] < dataframe['close'])

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        # Some static conditions which always apply
        conditions.append(dataframe['open'] > dataframe['ema_high'])

        if self.sell_mfi_enabled.value:
            conditions.append(dataframe['mfi'] > self.sell_mfi.value)
        if self.sell_fastd_enabled.value:
            conditions.append(dataframe['fastd'] > self.sell_fastd.value)
        if self.sell_fastk_enabled.value:
            conditions.append(dataframe['fastk'] > self.sell_fastk.value)
        if self.sell_adx_enabled.value:
            conditions.append(dataframe['adx'] < self.sell_adx.value)
        if self.sell_cci_enabled.value:
            conditions.append(dataframe['cci'] > self.sell_cci.value)

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe
