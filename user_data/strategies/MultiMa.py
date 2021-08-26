# MultiMa Strategy
# MultiMa proposed to find a way with making Ribbon idea.
# That can make signals by watching sort of Ribbon of sort of data.
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# (First Hyperopt it.A hyperopt file is available)
#
# --- Do not remove these libs ---
import pandas
from freqtrade.strategy.hyper import CategoricalParameter, IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce


class MultiMa(IStrategy):
    # *    3/5000:    201 trades. 88/110/3 Wins/Draws/Losses. Avg profit   0.58%. Median profit   0.00%. Total profit  469.48458465 USDT (  46.95%). Avg duration 11:29:00 min. Objective: -469.48458


    # Buy hyperspace params:
    buy_params = {
        "buy_ma_comp": "!=",
        "buy_ma_count": 150,
        "buy_ma_driver": "g",
        "buy_ma_rolling": 80,
        "buy_ma_shift": 90,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_ma_comp": ">",
        "sell_ma_count": 150,
        "sell_ma_driver": "s",
        "sell_ma_rolling": 54,
        "sell_ma_shift": 14,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.119,
        "34": 0.07,
        "50": 0.022,
        "110": 0
    }

    # Stoploss:
    stoploss = -0.267

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy
    
    # Timeframe
    timeframe = '5m'

    
    timeframes = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
    buy_ma_count = CategoricalParameter(timeframes, default=10, space='buy')
    buy_ma_rolling = IntParameter(0, 100, default=2, space='buy')
    buy_ma_shift = IntParameter(0, 100, default=0, space='buy')
    buy_ma_driver = CategoricalParameter(['c', 'g', 's'], default='s', space='buy')
    buy_ma_comp = CategoricalParameter(['<','>','!=','=='], default='>', space='buy')
    
    sell_ma_count = CategoricalParameter(timeframes, default=10, space='sell')
    sell_ma_rolling = IntParameter(0, 100, default=2, space='sell')
    sell_ma_shift = IntParameter(0, 100, default=0, space='sell')
    sell_ma_driver = CategoricalParameter(['c', 'g', 's'], default='s', space='sell')
    sell_ma_comp = CategoricalParameter(['<','>','!=','=='], default='<', space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        for i in self.buy_ma_count.range:
            dataframe[i] = ta.MA(dataframe, timeperiod=int(i))

        for i in self.sell_ma_count.range:
            dataframe[i] = ta.MA(dataframe, timeperiod=int(i))

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []
        if self.buy_ma_driver.value == 'c':
            rng = self.buy_ma_count.range
            for idx, count in enumerate(rng):
                if idx-1 > 1:
                    dataframe['A'] = dataframe[count].rolling(int(self.buy_ma_rolling.value)).sum().shift(self.buy_ma_shift.value)
                    dataframe['B'] =  dataframe.iloc[:, idx - 1].rolling(int(self.buy_ma_rolling.value)).sum().shift(self.buy_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.buy_ma_comp.value} B '))
        elif self.buy_ma_driver.value == 'g':
            rng = self.buy_ma_rolling.range
            for rolling in rng:
                if rolling-1 >= 0:
                    dataframe['A'] = dataframe[self.buy_ma_count.value].rolling(rolling).sum().shift(self.buy_ma_shift.value)
                    dataframe['B'] =  dataframe[self.buy_ma_count.value].rolling(int(rolling-1)).sum().shift(self.buy_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.buy_ma_comp.value} B '))
        elif self.buy_ma_driver.value == 's':
            rng = self.buy_ma_shift.range
            for shift in rng:
                dataframe['A'] = dataframe[self.buy_ma_count.value].rolling(int(self.buy_ma_rolling.value)).sum().shift(shift)
                dataframe['B'] =  dataframe[self.buy_ma_count.value].rolling(int(self.buy_ma_rolling.value)).sum().shift(shift-1)
                conditions.append(dataframe.eval(f' A {self.buy_ma_comp.value} B '))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        if self.sell_ma_driver.value == 'c':
            rng = self.sell_ma_count.range
            for idx, count in enumerate(rng):
                if idx-1 > 1:
                    dataframe['A'] = dataframe[count].rolling(int(self.sell_ma_rolling.value)).sum().shift(self.sell_ma_shift.value)
                    dataframe['B'] =  dataframe.iloc[:, idx - 1].rolling(int(self.sell_ma_rolling.value)).sum().shift(self.sell_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.sell_ma_comp.value} B '))
        elif self.sell_ma_driver.value == 'g':
            rng = self.sell_ma_rolling.range
            for rolling in rng:
                if rolling-1 >= 0:
                    dataframe['A'] = dataframe[self.sell_ma_count.value].rolling(rolling).sum().shift(self.sell_ma_shift.value)
                    dataframe['B'] =  dataframe[self.sell_ma_count.value].rolling(int(rolling-1)).sum().shift(self.sell_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.sell_ma_comp.value} B '))
        elif self.sell_ma_driver.value == 's':
            rng = self.sell_ma_shift.range
            for shift in rng:
                dataframe['A'] = dataframe[self.sell_ma_count.value].rolling(int(self.sell_ma_rolling.value)).sum().shift(shift)
                dataframe['B'] =  dataframe[self.sell_ma_count.value].rolling(int(self.sell_ma_rolling.value)).sum().shift(shift-1)
                conditions.append(dataframe.eval(f' A {self.sell_ma_comp.value} B '))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
