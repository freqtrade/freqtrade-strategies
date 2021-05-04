# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
from functools import reduce


# --------------------------------


class ADXMomentum(IStrategy):
    """

    author@: Gert Wohlgemuth

    converted from:

        https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/AdxMomentum.cs

    """
    # Buy hyperspace params:
    buy_params = {
        'buy-adx-enabled': True,
        'buy-adx-value': 25,
        'buy-com-enabled': True,
        'buy-mom-enabled': True,
        'buy-mom-value': 0,
        'buy-pd-value': 25,
        'buy-pd-enabled': True
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-adx-enabled': True,
        'sell-adx-value': 25,
        'sell-com-enabled': True,
        'sell-min-enabled': True,
        'sell-min-value': 25,
        'sell-mom-enabled': True,
        'sell-mom-value': 0
    }
    # Minimal ROI designed for the strategy.
    # adjust based on market
    minimal_roi = {
        "0": 0.01
    }

    # Optimal stoploss designed for the strategy
    # stoploss = -0.25
    stoploss = -1

    # Optimal timeframe for the strategy
    timeframe = '1h'

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)
        # dataframe['sar'] = ta.SAR(dataframe)
        dataframe['mom'] = ta.MOM(dataframe, timeperiod=14)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        if self.buy_params.get('buy-adx-enabled'):
            conditions.append(dataframe['adx'] > self.buy_params['buy-adx-value'])
        if self.buy_params.get('buy-mom-enabled'):
            conditions.append(dataframe['mom'] > self.buy_params['buy-mom-value'])
        if self.buy_params.get('buy-pd-enabled'):
            conditions.append(dataframe['plus_di'] > self.buy_params['buy-pd-value'])
        if self.buy_params.get('buy-com-enabled'):
            conditions.append(dataframe['plus_di'] > dataframe['minus_di'])
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        if self.sell_params.get('sell-adx-enabled'):
            conditions.append(dataframe['adx'] > self.sell_params['sell-adx-value'])
        if self.sell_params.get('sell-mom-enabled'):
            conditions.append(dataframe['mom'] < self.sell_params['sell-mom-value'])
        if self.sell_params.get('sell-min-enabled'):
            conditions.append(dataframe['minus_di'] > self.sell_params['sell-min-value'])
        if self.sell_params.get('sell-com-enabled'):
            conditions.append(dataframe['plus_di'] < dataframe['minus_di'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1
        return dataframe
