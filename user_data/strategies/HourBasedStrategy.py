# Hour Strategy
# In this strategy we try to find the best hours to buy and sell in a day.(in hourly timeframe)
# Because of that you should just use 1h timeframe on this strategy.
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# Requires hyperopt before running.
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy HourBasedStrategy -e 200


from freqtrade.strategy import IntParameter, IStrategy
from pandas import DataFrame

# --------------------------------
# Add your lib to import here
# No need to These imports. just for who want to add more conditions:
# import talib.abstract as ta
# import freqtrade.vendor.qtpylib.indicators as qtpylib


class HourBasedStrategy(IStrategy):
    # SHIB/USDT, 1000$x1:100days
    # 158/1000:     51 trades. 29/19/3 Wins/Draws/Losses. Avg profit   4.02%. Median profit   2.48%. Total profit  4867.53438466 USDT ( 486.75%). Avg duration 1 day, 19:38:00 min. Objective: -4.17276
    # buy_params = {"buy_hour_max": 18,"buy_hour_min": 7,}
    # sell_params = {"sell_hour_max": 9,"sell_hour_min": 21,}
    # minimal_roi = {"0": 0.18,"171": 0.155,"315": 0.075,"1035": 0}
    # stoploss = -0.292

    # SHIB/USDT, 1000$x1:100days
    # 36/1000:    113 trades. 55/14/44 Wins/Draws/Losses. Avg profit   2.06%. Median profit   0.00%. Total profit  5126.14785426 USDT ( 512.61%). Avg duration 16:48:00 min. Objective: -4.57837
    # buy_params = {"buy_hour_max": 21,"buy_hour_min": 6,}
    # sell_params = {"sell_hour_max": 6,"sell_hour_min": 4,}
    # minimal_roi = {"0": 0.247,"386": 0.186,"866": 0.052,"1119": 0}
    # stoploss = -0.302

    # SAND/USDT, 1000$x1:100days
    # 72/1000:    158 trades. 67/13/78 Wins/Draws/Losses. Avg profit   1.37%. Median profit   0.00%. Total profit  4274.73622346 USDT ( 427.47%). Avg duration 13:50:00 min. Objective: -4.87331
    # buy_params = {"buy_hour_max": 23,"buy_hour_min": 4,}
    # sell_params = {"sell_hour_max": 23,"sell_hour_min": 3,}
    # minimal_roi = {"0": 0.482,"266": 0.191,"474": 0.09,"1759": 0}
    # stoploss = -0.05

    # KDA/USDT, 1000$x1:100days
    # 7/1000:     65 trades. 40/23/2 Wins/Draws/Losses. Avg profit   6.42%. Median profit   7.59%. Total profit  41120.00939125 USDT ( 4112.00%). Avg duration 1 day, 9:40:00 min. Objective: -8.46089
    # buy_params = {"buy_hour_max": 22,"buy_hour_min": 9,}
    # sell_params = {"sell_hour_max": 1,"sell_hour_min": 7,}
    # minimal_roi = {"0": 0.517,"398": 0.206,"1003": 0.076,"1580": 0}
    # stoploss = -0.338

    # {KDA/USDT, BTC/USDT, DOGE/USDT, SAND/USDT, ETH/USDT, SOL/USDT}, 1000$x1:100days, ShuffleFilter42
    # 56/1000:     63 trades. 41/19/3 Wins/Draws/Losses. Avg profit   4.60%. Median profit   8.89%. Total profit  11596.50333022 USDT ( 1159.65%). Avg duration 1 day, 14:46:00 min. Objective: -5.76694

    INTERFACE_VERSION: int = 3
    # Buy hyperspace params:
    buy_params = {
        "buy_hour_max": 24,
        "buy_hour_min": 4,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_hour_max": 21,
        "sell_hour_min": 22,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.528,
        "169": 0.113,
        "528": 0.089,
        "1837": 0
    }

    # Stoploss:
    stoploss = -0.10

    # Optimal timeframe
    timeframe = '1h'

    buy_hour_min = IntParameter(0, 24, default=1, space='buy')
    buy_hour_max = IntParameter(0, 24, default=0, space='buy')

    sell_hour_min = IntParameter(0, 24, default=1, space='sell')
    sell_hour_max = IntParameter(0, 24, default=0, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['hour'] = dataframe['date'].dt.hour
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['hour'].between(self.buy_hour_min.value, self.buy_hour_max.value))
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['hour'].between(self.sell_hour_min.value, self.sell_hour_max.value))
            ),
            'exit_long'] = 1
        return dataframe
