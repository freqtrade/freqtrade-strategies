# MultiMa Strategy
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# (First Hyperopt it.A hyperopt file is available)
#
# --- Do not remove these libs ---
from freqtrade.strategy.hyper import IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce

##### SETINGS #####
# It hyperopt just one set of params for all buy and sell strategies if true.
DUALFIT = True
### END SETINGS ###


class MultiMa(IStrategy):
    # ###################### RESULT PLACE ######################
    # CONF: 3*333=1000USDT, 5m, PL: .*/USDT, spaces: buy trailing
    # PL for hyp:
    #       "MFT/USDT",
    #       "ONG/USDT",
    #       "REP/USDT",
    #       "SUSHI/USDT",
    #       "STX/USDT",
    #       "KEY/USDT",
    #       "MATIC/USDT",
    #       "BTC/USDT",
    #       "ETH/USDT",
    #       "XRP/USDT",
    #       "DOGE/USDT",
    #       "ADA/USDT"

    #    43/100:     30 trades. 28/0/2 Wins/Draws/Losses. Avg profit   6.19%. Median profit   6.05%. Total profit  619.44561139 USDT (  61.94Σ%). Avg duration 2 days, 21:33:00 min. Objective: -33.61648

    # Buy hyperspace params:
    buy_params = {
        "buy_ma_count": 7,
        "buy_ma_gap": 3,
        "buy_ma_shift": 14,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_ma_count": 0,  # value loaded from strategy
        "sell_ma_gap": 0,  # value loaded from strategy
        "sell_ma_shift": 0,  # value loaded from strategy
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.023
    trailing_stop_positive_offset = 0.067

    # ROI table:
    minimal_roi = {
        "0": 1,
    }
    # Stoploss:
    stoploss = -0.256

    # Buy hypers
    timeframe = '5m'
    # #################### END OF RESULT PLACE ####################

    buy_ma_count = IntParameter(2, 15, default=10, space='buy')
    buy_ma_gap = IntParameter(2, 15, default=2, space='buy')
    buy_ma_shift = IntParameter(0, 20, default=0, space='buy')
    # buy_ma_rolling = IntParameter(0, 10, default=0, space='buy')

    sell_ma_count = IntParameter(2, 20, default=10, space='sell')
    sell_ma_gap = IntParameter(2, 15, default=2, space='sell')
    sell_ma_shift = IntParameter(0, 15, default=0, space='sell')
    # sell_ma_rolling = IntParameter(0, 10, default=0, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # We will dinamicly generate the indicators
        # cuz this method just run one time in hyperopts
        # if you have static timeframes you can move first loop of buy and sell trends populators inside this method

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # print(self.sell_ma_count.value)
        # exit()
        conditions = []

        for i in range(1, self.buy_ma_count.value+1):
            dataframe[f'buy-ma-{i}'] = ta.EMA(dataframe,
                                              timeperiod=int(i * self.buy_ma_gap.value))
            for shift in range(1, self.buy_ma_shift.value+1):
                if i > 1:
                    conditions.append(
                        dataframe[f'buy-ma-{i}'].shift(shift) <
                        dataframe[f'buy-ma-{i-1}'].shift(shift)
                    )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        if DUALFIT:
            for i in range(1, self.buy_ma_count.value+1):
                dataframe[f'buy-ma-{i-1}'] = ta.EMA(dataframe,
                                                    timeperiod=int(i * self.buy_ma_gap.value))
                for shift in range(1, self.buy_ma_shift.value+1):
                    if i > 1:
                        conditions.append(
                            dataframe[f'buy-ma-{i}'].shift(shift) >
                            dataframe[f'buy-ma-{i-1}'].shift(shift)
                        )
        else:
            for i in range(1, self.sell_ma_count.value+1):
                dataframe[f'sell-ma-{i}'] = ta.EMA(dataframe,
                                                   timeperiod=int(i * self.sell_ma_gap.value))

                for shift in range(1, self.sell_ma_shift.value+1):
                    if i > 1:
                        conditions.append(
                            dataframe[f'sell-ma-{i}'].shift(shift) >
                            dataframe[f'sell-ma-{i-1}'].shift(shift)
                        )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
