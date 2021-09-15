# Rainbow Strategy
# Rainbow proposed to findAway with Ribbons idea.
# That can make signals by watching sort of Ribbons.
# It uses time_ranges, Rolling And Shift on an MovingAverage indicator
# To Make sort of Ribbons to generate signals. You Can Change ta.MA indicator
# In populate_indicators function to any you want for example ta.RSI and hyperopt
# And See What will happen. The key thing we use in this strategy Is Driver that controls
# That Which (tf, rolling, shift) setting of an indicator will use to make Ribbons.
# There isAcomperator param that used for find best comperatorare operator to generated ribbons.
# freqtrade backtesting -s Rainbow -c configusdt.json
# freqtrade hyperopt --hyperopt-loss ShortTradeDurHyperOptLoss --strategy Rainbow -c configusdt.json --eps
# $ freqtrade hyperopt --hyperopt-loss OnlyProfitHyperOptLoss --strategy Rainbow -c configusdt.json --eps
# $$$ freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy Rainbow -c configusdt.json --eps
# $ freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --strategy Rainbow -c configusdt.json --eps
# $$ freqtrade hyperopt --hyperopt-loss SortinoHyperOptLoss --strategy Rainbow -c configusdt.json --eps
# $ freqtrade hyperopt --hyperopt-loss SortinoHyperOptLossDaily --strategy Rainbow -c configusdt.json --eps

# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/

# --- Do not remove these libs ---
from freqtrade.strategy.hyper import CategoricalParameter, IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce


# A function to generate prime numbers
def sieve_of_eratosthenes(n):
    # CreateAboolean array "prime[0..n]" and initialize
    # all entries it as true.Avalue in prime[i] will
    # finally be false if i is NotAprime, else true.
    prime = [True]*(n + 1)
    p = 2
    while (p * p <= n):
        # Update all multiples of p
        if (prime[p] == True):
            for i in range(p ** 2, n + 1, p):
                prime[i] = False
        p += 1
    return [i for i in list(range(2, n)) if prime[i] == True]


class Rainbow(IStrategy):
    #     53/100:     81 trades. 27/53/1 Wins/Draws/Losses. Avg profit   0.25%. Median profit   0.00%. Total profit  200.27435768 USDT (  20.03Σ%). Avg duration 15:54:00 min. Objective: -3.73368


    # Buy hyperspace params:
    buy_params = {
        "buy_ma_comperator": "A<B",
        "buy_ma_driver": "shift",
        "buy_ma_rolling": 22,
        "buy_ma_shift": 23,
        "buy_ma_time_range": 13,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_ma_comperator": "A>B",
        "sell_ma_driver": "shift",
        "sell_ma_rolling": 0,
        "sell_ma_shift": 25,
        "sell_ma_time_range": 29,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.175,
        "24": 0.058,
        "51": 0.023,
        "133": 0
    }

    # Stoploss:
    stoploss = -0.338
    
    # Opt Timeframe
    timeframe = '5m'

    # time_ranges that you want to use in strategy
    # Example1:
    # min, 2~inf
    # max, 3~inf
    # steps 1~max
    # time_ranges = range(2, 102, 4)

    # Example2 (costume time_ranges):
    # time_ranges=[3,7,14,28,56,112,224]

    # Example3 (Prime Numbers)
    time_ranges = sieve_of_eratosthenes(50)

    buy_ma_time_range = CategoricalParameter(time_ranges, default=10, space='buy')
    buy_ma_rolling = IntParameter(0, 25, default=25, space='buy')
    buy_ma_shift = IntParameter(0, 25, default=0, space='buy')
    # You can get info about drivers by watching top!
    buy_ma_driver = CategoricalParameter(
        ['time_range', 'rolling', 'shift'], default='shift', space='buy')
    # '0.99<A/B<1.01' means A == B by 0.01 error
    # '0.99<A/B<1.01' means A == B by 0.01 error
    # you can add more comprators to it for example : A>=B
    buy_ma_comperator = CategoricalParameter(
        ['A>B', 'A<B', '0.99<A/B<1.01', 'crossed_above', 'crossed_below'], default='>', space='buy')

    sell_ma_time_range = CategoricalParameter(time_ranges, default=10, space='sell')
    sell_ma_rolling = IntParameter(0, 25, default=25, space='sell')
    sell_ma_shift = IntParameter(0, 25, default=0, space='sell')
    sell_ma_driver = CategoricalParameter(
        ['time_range', 'rolling', 'shift'], default='shift', space='sell')
    sell_ma_comperator = CategoricalParameter(
        ['A>B', 'A<B', '0.99<A/B<1.01', 'crossed_above', 'crossed_below'], default='<', space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        for tr in self.time_ranges:
            dataframe[tr] = ta.EMA(dataframe, timeperiod=tr)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        if self.buy_ma_driver.value == 'time_range':
            rng = self.time_ranges
            for i, tr in enumerate(rng):
                if i-1 > 0:
                    dataframe['A'] = dataframe.iloc[:, i].rolling(
                        self.buy_ma_rolling.value).mean().shift(self.buy_ma_shift.value)
                    dataframe['B'] = dataframe.iloc[:, i-1].rolling(
                        self.buy_ma_rolling.value).mean().shift(self.buy_ma_shift.value)
                    conditions.append(self.ConditionGenerator(
                        self.buy_ma_comperator.value, dataframe, dataframe['A'], dataframe['B']))

        elif self.buy_ma_driver.value == 'rolling':
            rng = self.buy_ma_rolling.range
            for rolling in rng:
                if rolling-1 >= 0:
                    dataframe['A'] = dataframe[self.buy_ma_time_range.value].rolling(
                        rolling).mean().shift(self.buy_ma_shift.value)
                    dataframe['B'] = dataframe[self.buy_ma_time_range.value].rolling(
                        rolling-1).mean().shift(self.buy_ma_shift.value)
                    conditions.append(self.ConditionGenerator(
                        self.buy_ma_comperator.value, dataframe, dataframe['A'], dataframe['B']))

        elif self.buy_ma_driver.value == 'shift':
            rng = self.buy_ma_shift.range
            for shift in rng:
                dataframe['A'] = dataframe[self.buy_ma_time_range.value].rolling(
                    self.buy_ma_rolling.value).mean().shift(shift)
                dataframe['B'] = dataframe[self.buy_ma_time_range.value].rolling(
                    self.buy_ma_rolling.value).mean().shift(shift-1)
                conditions.append(self.ConditionGenerator(
                    self.buy_ma_comperator.value, dataframe, dataframe['A'], dataframe['B']))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions), 'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        if self.sell_ma_driver.value == 'time_range':
            rng = self.time_ranges
            for i, tr in enumerate(rng):
                if i-1 > 0:
                    dataframe['A'] = dataframe.iloc[:, i].rolling(
                        self.sell_ma_rolling.value).mean().shift(self.sell_ma_shift.value)
                    dataframe['B'] = dataframe.iloc[:, i-1].rolling(
                        self.sell_ma_rolling.value).mean().shift(self.sell_ma_shift.value)
                    conditions.append(self.ConditionGenerator(
                        self.sell_ma_comperator.value, dataframe, dataframe['A'], dataframe['B']))

        elif self.sell_ma_driver.value == 'rolling':
            rng = self.sell_ma_rolling.range
            for rolling in rng: 
                if rolling-1 >= 0:
                    dataframe['A'] = dataframe[self.sell_ma_time_range.value].rolling(
                        rolling).mean().shift(self.sell_ma_shift.value)
                    dataframe['B'] = dataframe[self.sell_ma_time_range.value].rolling(
                        rolling-1).mean().shift(self.sell_ma_shift.value)
                    conditions.append(self.ConditionGenerator(
                        self.sell_ma_comperator.value, dataframe, dataframe['A'], dataframe['B']))

        elif self.sell_ma_driver.value == 'shift':
            rng = self.sell_ma_shift.range
            for shift in rng:
                dataframe['A'] = dataframe[self.sell_ma_time_range.value].rolling(
                    self.sell_ma_rolling.value).mean().shift(shift)
                dataframe['B'] = dataframe[self.sell_ma_time_range.value].rolling(
                    self.sell_ma_rolling.value).mean().shift(shift-1)
                conditions.append(self.ConditionGenerator(
                    self.sell_ma_comperator.value, dataframe, dataframe['A'], dataframe['B']))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x | y, conditions), 'sell']=1

        return dataframe

    # you can add more conditions here with new tags and than add
    # them to comperator hyperoptable variable.
    def ConditionGenerator(self, comperator, df, A, B):
        # comperator == 'Tag':
        if comperator == 'crossed_above':
            return qtpylib.crossed_above(A, B)
        elif comperator == 'crossed_below':
            return qtpylib.crossed_below(A, B)
        else:
            return df.eval(comperator)
