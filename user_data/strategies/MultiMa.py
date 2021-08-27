# MultiMa Strategy
# MultiMa proposed to find a way with Ribbons idea.
# That can make signals by watching sort of Ribbons.
# It uses Timeframes, Rolling And Shift on an MovingAverage indicator
# To Make sort of Ribbons to generate signals. You Can Change ta.MA indicator 
# In populate_indicators function to any you want for example ta.RSI and hyperopt
# And See What will happen. The key thing we use in this strategy Is Driver that controls
# That Which (tf,rolling,shift) setting of an indicator will use to make Ribbons.
# There is a comp param that used for find best compare operator to generated ribbons.
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy MultiMa -j 2

# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/

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
    #     34/100:    574 trades. 225/339/10 Wins/Draws/Losses. Avg profit   0.64%. Median profit   0.00%. Total profit  365.79045436 USDT (  36.58%). Avg duration 12:54:00 min. Objective: -125.03491


    # Buy hyperspace params:
    buy_params = {
        "buy_ma_comp": ">",
        "buy_ma_driver": "rolling",
        "buy_ma_rolling": 10,
        "buy_ma_shift": 17,
        "buy_ma_timeframe": 26,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_ma_comp": "==",
        "sell_ma_driver": "shift",
        "sell_ma_rolling": 12,
        "sell_ma_shift": 4,
        "sell_ma_timeframe": 69,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.106,
        "15": 0.092,
        "52": 0.036,
        "165": 0
    }

    # Stoploss:
    stoploss = -0.249

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy
    # Timeframe
    timeframe = '5m'

    # timeframes that you want to use in strategy
    timeframes = range(2,100)

    buy_ma_timeframe = CategoricalParameter(timeframes, default=10, space='buy')
    buy_ma_rolling = IntParameter(0, 30, default=2, space='buy')
    buy_ma_shift = IntParameter(0, 30, default=0, space='buy')
    buy_ma_driver = CategoricalParameter(['timeframe', 'rolling', 'shift'], default='shift', space='buy')
    buy_ma_comp = CategoricalParameter(['<','>','!=','=='], default='>', space='buy')
    
    sell_ma_timeframe = CategoricalParameter(timeframes, default=10, space='sell')
    sell_ma_rolling = IntParameter(0, 30, default=2, space='sell')
    sell_ma_shift = IntParameter(0, 30, default=0, space='sell')
    sell_ma_driver = CategoricalParameter(['timeframe', 'rolling', 'shift'], default='shift', space='sell')
    sell_ma_comp = CategoricalParameter(['<','>','!=','=='], default='<', space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for i in self.buy_ma_timeframe.range:
            dataframe[i] = ta.MA(dataframe, timeperiod=int(i))

        for i in self.sell_ma_timeframe.range:
            dataframe[i] = ta.MA(dataframe, timeperiod=int(i))

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        conditions = []
        if self.buy_ma_driver.value == 'timeframe':
            rng = self.buy_ma_timeframe.range
            for idx, timeframe in enumerate(rng):
                if idx-1 > 1:
                    dataframe['A'] = dataframe[timeframe].rolling(int(self.buy_ma_rolling.value)).sum().shift(self.buy_ma_shift.value)
                    dataframe['B'] =  dataframe.iloc[:, idx - 1].rolling(int(self.buy_ma_rolling.value)).sum().shift(self.buy_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.buy_ma_comp.value} B '))
        elif self.buy_ma_driver.value == 'rolling':
            rng = self.buy_ma_rolling.range
            for rolling in rng:
                if rolling-1 >= 0:
                    dataframe['A'] = dataframe[self.buy_ma_timeframe.value].rolling(rolling).sum().shift(self.buy_ma_shift.value)
                    dataframe['B'] =  dataframe[self.buy_ma_timeframe.value].rolling(int(rolling-1)).sum().shift(self.buy_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.buy_ma_comp.value} B '))
        elif self.buy_ma_driver.value == 'shift':
            rng = self.buy_ma_shift.range
            for shift in rng:
                dataframe['A'] = dataframe[self.buy_ma_timeframe.value].rolling(int(self.buy_ma_rolling.value)).sum().shift(shift)
                dataframe['B'] =  dataframe[self.buy_ma_timeframe.value].rolling(int(self.buy_ma_rolling.value)).sum().shift(shift-1)
                conditions.append(dataframe.eval(f' A {self.buy_ma_comp.value} B '))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        if self.sell_ma_driver.value == 'timeframe':
            rng = self.sell_ma_timeframe.range
            for idx, timeframe in enumerate(rng):
                if idx-1 > 1:
                    dataframe['A'] = dataframe[timeframe].rolling(int(self.sell_ma_rolling.value)).sum().shift(self.sell_ma_shift.value)
                    dataframe['B'] =  dataframe.iloc[:, idx - 1].rolling(int(self.sell_ma_rolling.value)).sum().shift(self.sell_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.sell_ma_comp.value} B '))
        elif self.sell_ma_driver.value == 'rolling':
            rng = self.sell_ma_rolling.range
            for rolling in rng:
                if rolling-1 >= 0:
                    dataframe['A'] = dataframe[self.sell_ma_timeframe.value].rolling(rolling).sum().shift(self.sell_ma_shift.value)
                    dataframe['B'] =  dataframe[self.sell_ma_timeframe.value].rolling(int(rolling-1)).sum().shift(self.sell_ma_shift.value)
                    conditions.append(dataframe.eval(f' A {self.sell_ma_comp.value} B '))
        elif self.sell_ma_driver.value == 'shift':
            rng = self.sell_ma_shift.range
            for shift in rng:
                dataframe['A'] = dataframe[self.sell_ma_timeframe.value].rolling(int(self.sell_ma_rolling.value)).sum().shift(shift)
                dataframe['B'] =  dataframe[self.sell_ma_timeframe.value].rolling(int(self.sell_ma_rolling.value)).sum().shift(shift-1)
                conditions.append(dataframe.eval(f' A {self.sell_ma_comp.value} B '))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
