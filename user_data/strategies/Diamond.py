# 𝐼𝓉 𝒾𝓈 𝒟𝒾𝒶𝓂𝑜𝓃𝒹 𝒮𝓉𝓇𝒶𝓉𝑒𝑔𝓎.
# 𝒯𝒽𝒶𝓉 𝓉𝒶𝓀𝑒𝓈 𝒽𝑒𝓇 𝑜𝓌𝓃 𝓇𝒾𝑔𝒽𝓉𝓈 𝓁𝒾𝓀𝑒 𝒜𝒻𝑔𝒽𝒶𝓃𝒾𝓈𝓉𝒶𝓃 𝓌𝑜𝓂𝑒𝓃
# 𝒯𝒽𝑜𝓈𝑒 𝓌𝒽𝑜 𝓈𝓉𝒾𝓁𝓁 𝓅𝓇𝑜𝓊𝒹 𝒶𝓃𝒹 𝒽𝑜𝓅𝑒𝒻𝓊𝓁.
# 𝒯𝒽𝑜𝓈𝑒 𝓌𝒽𝑜 𝓉𝒽𝑒 𝓂𝑜𝓈𝓉 𝒷𝑒𝒶𝓊𝓉𝒾𝒻𝓊𝓁 𝒸𝓇𝑒𝒶𝓉𝓊𝓇𝑒𝓈 𝒾𝓃 𝓉𝒽𝑒 𝒹𝑒𝓅𝓉𝒽𝓈 𝑜𝒻 𝓉𝒽𝑒 𝒹𝒶𝓇𝓀𝑒𝓈𝓉.
# 𝒯𝒽𝑜𝓈𝑒 𝓌𝒽𝑜 𝓈𝒽𝒾𝓃𝑒 𝓁𝒾𝓀𝑒 𝒹𝒾𝒶𝓂𝑜𝓃𝒹𝓈 𝒷𝓊𝓇𝒾𝑒𝒹 𝒾𝓃 𝓉𝒽𝑒 𝒽𝑒𝒶𝓇𝓉 𝑜𝒻 𝓉𝒽𝑒 𝒹𝑒𝓈𝑒𝓇𝓉 ...
# 𝒲𝒽𝓎 𝓃𝑜𝓉 𝒽𝑒𝓁𝓅 𝓌𝒽𝑒𝓃 𝓌𝑒 𝒸𝒶𝓃?
# 𝐼𝒻 𝓌𝑒 𝒷𝑒𝓁𝒾𝑒𝓋𝑒 𝓉𝒽𝑒𝓇𝑒 𝒾𝓈 𝓃𝑜 𝓂𝒶𝓃 𝓁𝑒𝒻𝓉 𝓌𝒾𝓉𝒽 𝓉𝒽𝑒𝓂
# (𝒲𝒽𝒾𝒸𝒽 𝒾𝓈 𝓅𝓇𝑜𝒷𝒶𝒷𝓁𝓎 𝓉𝒽𝑒 𝓅𝓇𝑜𝒹𝓊𝒸𝓉 𝑜𝒻 𝓉𝒽𝑒 𝓉𝒽𝑜𝓊𝑔𝒽𝓉 𝑜𝒻 𝓅𝒶𝒾𝓃𝓁𝑒𝓈𝓈 𝒸𝑜𝓇𝓅𝓈𝑒𝓈)
# 𝒲𝒽𝑒𝓇𝑒 𝒽𝒶𝓈 𝑜𝓊𝓇 𝒽𝓊𝓂𝒶𝓃𝒾𝓉𝓎 𝑔𝑜𝓃𝑒?
# 𝒲𝒽𝑒𝓇𝑒 𝒽𝒶𝓈 𝒽𝓊𝓂𝒶𝓃𝒾𝓉𝓎 𝑔𝑜𝓃𝑒?
# 𝒲𝒽𝓎 𝓃𝑜𝓉 𝒽𝑒𝓁𝓅 𝓌𝒽𝑒𝓃 𝓌𝑒 𝒸𝒶𝓃?
# IMPORTANT: This strategy
# thanks to: @Kroissan, @drakes00 And @xmatthias for his patience and helps
# * freqtrade hyperopt --hyperopt-loss ShortTradeDurHyperOptLoss --spaces buy sell roi trailing --strategy Diamond -e 700 -j 2
# * freqtrade backtesting --strategy Diamond
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# --- Do not remove these libs ---
from freqtrade.strategy.hyper import CategoricalParameter, DecimalParameter, IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
from functools import reduce
import freqtrade.vendor.qtpylib.indicators as qtpylib


class Diamond(IStrategy):
    # ###################### RESULT PLACE ######################
    # 1/700:     20 trades. 13/4/3 Wins/Draws/Losses. Avg profit   6.30%. Median profit   7.19%. Total profit  0.04159258 BTC (  41.59%). Avg duration 2 days, 22:24:00 min. Objective: 1.83361
    # Buy hyperspace params:
    buy_params = {
        "buy_fast": 22,
        "buy_push": 1.65,
        "buy_slow": 16,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_fast": 10,
        "sell_push": 1.53,
        "sell_slow": 50,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.647,
        "992": 0.285,
        "2659": 0.072,
        "7323": 0
    }

    # Stoploss:
    stoploss = -0.259
    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.222
    trailing_stop_positive_offset = 0.284
    trailing_only_offset_is_reached = True

    # Buy hypers
    timeframe = '4h'
    # #################### END OF RESULT PLACE ####################
    buy_push = DecimalParameter(1, 2, decimals=2, default=1, space='buy')
    sell_push = DecimalParameter(1, 2, decimals=2,  default=1, space='sell')
    buy_fast = IntParameter(2, 30, default=1, space='buy')
    buy_slow = IntParameter(2, 50, default=1, space='buy')
    sell_fast = IntParameter(2, 30, default=1, space='sell')
    sell_slow = IntParameter(2, 50, default=1, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['buy_ma_fast'] = ta.SMA(
            dataframe, timeperiod=int(self.buy_fast.value))
        dataframe['buy_ma_slow'] = ta.SMA(
            dataframe, timeperiod=int(self.buy_slow.value))

        conditions = []
        conditions.append(
            (dataframe['buy_ma_fast']/dataframe['buy_ma_slow']
             ).between(1, self.buy_push.value)

        )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['sell_ma_fast'] = ta.SMA(
            dataframe, timeperiod=int(self.sell_fast.value))
        dataframe['sell_ma_slow'] = ta.SMA(
            dataframe, timeperiod=int(self.sell_slow.value))

        conditions = []
        conditions.append(
            (dataframe['sell_ma_slow']/dataframe['sell_ma_fast']
             ).between(1, self.sell_push.value)
        )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
