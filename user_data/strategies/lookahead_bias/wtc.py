# WTC Strategy: WTC(World Trade Center Tabriz)
# is the biggest skyscraper of Tabriz, city of Iran
# (What you want?it not enough for you?that's just it!)
# No, no, I'm kidding. It's also mean Wave Trend with Crosses
# algo by LazyBare(in TradingView) that I reduce it
# signals noise with dividing it to Stoch-RSI indicator.
# Also thanks from discord: @aurax for his/him
# request to making this strategy.
# hope you enjoy and get profit
# Author: @Mablue (Masoud Azizi)
# IMPORTANT: install sklearn befoure you run this strategy:
# pip install sklearn
# github: https://github.com/mablue/
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell --strategy wtc

import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta
from freqtrade.strategy import DecimalParameter
from freqtrade.strategy import IStrategy
from pandas import DataFrame
#
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from sklearn import preprocessing

# --------------------------------
# Add your lib to import here


class wtc(IStrategy):
    ################################ SETTINGS ################################
    # 61 trades. 16/0/45 Wins/Draws/Losses.
    # * Avg profit: 132.53%.
    # Median profit: -12.97%.
    # Total profit: 0.80921449 BTC ( 809.21Σ%).
    # Avg duration 4 days, 7:47:00 min.
    # Objective: -15.73417

    # Config:
    # "max_open_trades": 10,
    # "stake_currency": "BTC",
    # "stake_amount": 0.01,
    # "tradable_balance_ratio": 0.99,
    # "timeframe": "30m",
    # "dry_run_wallet": 0.1,

    INTERFACE_VERSION: int = 3
    # Buy hyperspace params:
    buy_params = {
        "buy_max": 0.9609,
        "buy_max0": 0.8633,
        "buy_max1": 0.9133,
        "buy_min": 0.0019,
        "buy_min0": 0.0102,
        "buy_min1": 0.6864,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_max": -0.7979,
        "sell_max0": 0.82,
        "sell_max1": 0.9821,
        "sell_min": -0.5377,
        "sell_min0": 0.0628,
        "sell_min1": 0.4461,
    }
    minimal_roi = {
        "0": 0.30873,
        "569": 0.16689,
        "3211": 0.06473,
        "7617": 0
    }
    stoploss = -0.128
    ############################## END SETTINGS ##############################
    timeframe = '30m'

    buy_max = DecimalParameter(-1, 1, decimals=4, default=0.4393, space='buy')
    buy_min = DecimalParameter(-1, 1, decimals=4, default=-0.4676, space='buy')
    sell_max = DecimalParameter(-1, 1, decimals=4,
                                default=-0.9512, space='sell')
    sell_min = DecimalParameter(-1, 1, decimals=4,
                                default=0.6519, space='sell')

    buy_max0 = DecimalParameter(0, 1, decimals=4, default=0.4393, space='buy')
    buy_min0 = DecimalParameter(0, 1, decimals=4, default=-0.4676, space='buy')
    sell_max0 = DecimalParameter(
        0, 1, decimals=4, default=-0.9512, space='sell')
    sell_min0 = DecimalParameter(
        0, 1, decimals=4, default=0.6519, space='sell')

    buy_max1 = DecimalParameter(0, 1, decimals=4, default=0.4393, space='buy')
    buy_min1 = DecimalParameter(0, 1, decimals=4, default=-0.4676, space='buy')
    sell_max1 = DecimalParameter(
        0, 1, decimals=4, default=-0.9512, space='sell')
    sell_min1 = DecimalParameter(
        0, 1, decimals=4, default=0.6519, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # WAVETREND
        try:
            ap = (dataframe['high']+dataframe['low'] + dataframe['close'])/3

            esa = ta.EMA(ap, 10)

            d = ta.EMA((ap - esa).abs(), 10)
            ci = (ap - esa).div(0.0015 * d)
            tci = ta.EMA(ci, 21)

            wt1 = tci
            wt2 = ta.SMA(np.nan_to_num(wt1), 4)

            dataframe['wt1'], dataframe['wt2'] = wt1, wt2

            stoch = ta.STOCH(dataframe, 14)
            slowk = stoch['slowk']
            dataframe['slowk'] = slowk
            # print(dataframe.iloc[:, 6:].keys())
            x = dataframe.iloc[:, 6:].values  # returns a numpy array
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            dataframe.iloc[:, 6:] = pd.DataFrame(x_scaled)
            # print('wt:\t', dataframe['wt'].min(), dataframe['wt'].max())
            # print('stoch:\t', dataframe['stoch'].min(), dataframe['stoch'].max())
            dataframe['def'] = dataframe['slowk']-dataframe['wt1']
            # print('def:\t', dataframe['def'].min(), "\t", dataframe['def'].max())
        except:
            dataframe['wt1'], dataframe['wt2'], dataframe['def'], dataframe['slowk'] = 0, 10, 100, 1000
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['wt1'], dataframe['wt2']))
                & (dataframe['wt1'].between(self.buy_min0.value, self.buy_max0.value))
                & (dataframe['slowk'].between(self.buy_min1.value, self.buy_max1.value))
                & (dataframe['def'].between(self.buy_min.value, self.buy_max.value))

            ),

            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # print(dataframe['slowk']/dataframe['wt1'])
        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['wt1'], dataframe['wt2']))
                & (dataframe['wt1'].between(self.sell_min0.value, self.sell_max0.value))
                & (dataframe['slowk'].between(self.sell_min1.value, self.sell_max1.value))
                & (dataframe['def'].between(self.sell_min.value, self.sell_max.value))

            ),
            'exit_long'] = 1
        return dataframe
