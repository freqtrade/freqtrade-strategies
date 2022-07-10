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
# 𝓁𝑒𝓉𝓈 𝓅𝒾𝓅 𝓊𝓃𝒾𝓃𝓈𝓉𝒶𝓁𝓁 𝓉𝒶-𝓁𝒾𝒷 𝑜𝓃 𝒜𝒻𝑔𝒽𝒶𝓃𝒾𝓈𝓉𝒶𝓃

# IMPORTANT: Diamond strategy is designed to be pure and
# cuz of that it have not any indicator population. idea is that
# It is just use the pure dataframe ohlcv data for calculation
# of buy/sell signals, But you can add your indicators and add
# your key names inside catagorical hyperoptable params and
# than you be able to hyperopt them as well.
# thanks to: @Kroissan, @drakes00 And @xmatthias for his patience and helps
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# * freqtrade backtesting --strategy Diamond

# freqtrade hyperopt --hyperopt-loss ShortTradeDurHyperOptLoss --spaces buy sell roi trailing stoploss --strategy Diamond -j 2 -e 10
# *    3/10:     76 trades. 51/18/7 Wins/Draws/Losses. Avg profit   1.92%. Median profit   2.40%. Total profit  0.04808472 BTC (  48.08%). Avg duration 5:06:00 min. Objective: 1.75299
# freqtrade hyperopt --hyperopt-loss OnlyProfitHyperOptLoss --spaces buy sell roi trailing stoploss --strategy Diamond -j 2 -e 10
# *   10/10:     76 trades. 39/34/3 Wins/Draws/Losses. Avg profit   0.61%. Median profit   0.05%. Total profit  0.01528359 BTC (  15.28%). Avg duration 17:32:00 min. Objective: -0.01528
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell roi trailing stoploss --strategy Diamond -j 2 -e 10
# *    4/10:     15 trades. 10/2/3 Wins/Draws/Losses. Avg profit   1.52%. Median profit   7.99%. Total profit  0.00754274 BTC (   7.54%). Avg duration 1 day, 0:04:00 min. Objective: -0.90653
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --spaces buy sell roi trailing stoploss --strategy Diamond -j 2 -e 10
# *    7/10:    130 trades. 68/54/8 Wins/Draws/Losses. Avg profit   0.71%. Median profit   0.06%. Total profit  0.03050369 BTC (  30.50%). Avg duration 10:07:00 min. Objective: -11.08185
# freqtrade hyperopt --hyperopt-loss SortinoHyperOptLoss --spaces buy sell roi trailing stoploss --strategy Diamond -j 2 -e 10
# *    2/10:     10 trades. 7/0/3 Wins/Draws/Losses. Avg profit   5.50%. Median profit   7.05%. Total profit  0.01817970 BTC (  18.18%). Avg duration 0:27:00 min. Objective: -11.72450
# freqtrade hyperopt --hyperopt-loss SortinoHyperOptLossDaily --spaces buy sell roi trailing stoploss --strategy Diamond -j 2 -e 10
#   | * Best |    3/10 |      165 |     98   63    4 |        1.00% |    0.05453885 BTC   (54.54%) | 0 days 08:02:00 |    0.00442974 BTC   (13.41%) |     -41.371 |
#   | * Best |    7/10 |      101 |     56   42    3 |        0.73% |    0.02444518 BTC   (24.45%) | 0 days 13:08:00 |    0.00107122 BTC    (3.24%) |    -66.7687 |
# *    7/10:    101 trades. 56/42/3 Wins/Draws/Losses. Avg profit   0.73%. Median profit   0.13%. Total profit  0.02444518 BTC (  24.45%). Avg duration 13:08:00 min. Objective: -66.76866
# freqtrade hyperopt --hyperopt-loss OnlyProfitHyperOptLoss --spaces buy sell roi trailing stoploss --strategy Diamond -j 2 -e 10
# *    7/10:    117 trades. 74/41/2 Wins/Draws/Losses. Avg profit   1.91%. Median profit   1.50%. Total profit  0.07370921 BTC (  73.71%). Avg duration 9:26:00 min. Objective: -0.07371

# --- Do not remove these libs ---
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter, IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
from functools import reduce
import freqtrade.vendor.qtpylib.indicators as qtpylib


class Diamond(IStrategy):
    # ###################### RESULT PLACE ######################
    #    Config: 5 x UNLIMITED STOCK costume pair list,
    #    hyperopt : 5000 x SortinoHyperOptLossDaily,
    #    34/5000: 297 trades. 136/156/5 Wins/Draws/Losses. Avg profit   0.49%. Median profit   0.00%. Total profit  45.84477237 USDT (  33.96Σ%). Avg duration 11:54:00 min. Objective: -46.50379
    INTERFACE_VERSION: int = 3

    # Buy hyperspace params:
    buy_params = {
        "buy_fast_key": "high",
        "buy_horizontal_push": 7,
        "buy_slow_key": "volume",
        "buy_vertical_push": 0.942,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_fast_key": "high",
        "sell_horizontal_push": 10,
        "sell_slow_key": "low",
        "sell_vertical_push": 1.184,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.242,
        "13": 0.044,
        "51": 0.02,
        "170": 0
    }

    # Stoploss:
    stoploss = -0.271

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.011
    trailing_stop_positive_offset = 0.054
    trailing_only_offset_is_reached = False
    # timeframe
    timeframe = '5m'
    # #################### END OF RESULT PLACE ####################

    buy_vertical_push = DecimalParameter(0.5, 1.5, decimals=3, default=1, space='buy')
    buy_horizontal_push = IntParameter(0, 10, default=0, space='buy')
    buy_fast_key = CategoricalParameter(['open', 'high', 'low', 'close', 'volume',
                                         #  you can not enable this lines befour you
                                         #  populate an indicator for them and set
                                         #  the same key name for it
                                         #  'ma_fast', 'ma_slow', {...}
                                         ], default='ma_fast', space='buy')
    buy_slow_key = CategoricalParameter(['open', 'high', 'low', 'close', 'volume',
                                         #  'ma_fast', 'ma_slow', {...}
                                         ], default='ma_slow', space='buy')

    sell_vertical_push = DecimalParameter(0.5, 1.5, decimals=3,  default=1, space='sell')
    sell_horizontal_push = IntParameter(0, 10, default=0, space='sell')
    sell_fast_key = CategoricalParameter(['open', 'high', 'low', 'close', 'volume',
                                          #  'ma_fast', 'ma_slow', {...}
                                          ], default='ma_fast', space='sell')
    sell_slow_key = CategoricalParameter(['open', 'high', 'low', 'close', 'volume',
                                          #  'ma_fast', 'ma_slow', {...}
                                          ], default='ma_slow', space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # you can add new indicators and enable them inside
        # hyperoptable categorical params on the top
        # dataframe['ma_fast'] = ta.SMA(dataframe, timeperiod=9)
        # dataframe['ma_slow'] = ta.SMA(dataframe, timeperiod=18)
        # dataframe['{...}'] = ta.{...}(dataframe, timeperiod={...})
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            qtpylib.crossed_above
            (
                dataframe[self.buy_fast_key.value].shift(self.buy_horizontal_push.value),
                dataframe[self.buy_slow_key.value] * self.buy_vertical_push.value
            )
        )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long']=1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            qtpylib.crossed_below
            (
                dataframe[self.sell_fast_key.value].shift(self.sell_horizontal_push.value),
                dataframe[self.sell_slow_key.value] * self.sell_vertical_push.value
            )
        )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'exit_long']=1
        return dataframe
