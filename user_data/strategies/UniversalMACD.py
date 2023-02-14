# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class UniversalMACD(IStrategy):
    # By: Masoud Azizi (@mablue)
    # Tradingview Page: https://www.tradingview.com/script/xNEWcB8s-Universal-Moving-Average-Convergence-Divergence/

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '5m'

    # Can this strategy go short?
    can_short: bool = False

    # $ freqtrade hyperopt -s UniversalMACD --hyperopt-loss SharpeHyperOptLossDaily

    # "max_open_trades": 1,
    # "stake_currency": "USDT",
    # "stake_amount": 990,
    # "dry_run_wallet": 1000,
    # "trading_mode": "spot",
    # "XMR/USDT","ATOM/USDT","FTM/USDT","CHR/USDT","BNB/USDT","ALGO/USDT","XEM/USDT","XTZ/USDT","ZEC/USDT","ADA/USDT",
    # "CHZ/USDT","BTT/USDT","LUNA/USDT","VRA/USDT","KSM/USDT","DASH/USDT","COMP/USDT","CRO/USDT","WAVES/USDT","MKR/USDT",
    # "DIA/USDT","LINK/USDT","DOT/USDT","YFI/USDT","UNI/USDT","FIL/USDT","AAVE/USDT","KCS/USDT","LTC/USDT","BSV/USDT",
    # "XLM/USDT","ETC/USDT","ETH/USDT","BTC/USDT","XRP/USDT","TRX/USDT","VET/USDT","NEO/USDT","EOS/USDT","BCH/USDT",
    # "CRV/USDT","SUSHI/USDT","KLV/USDT","DOGE/USDT","CAKE/USDT","AVAX/USDT","MANA/USDT","SAND/USDT","SHIB/USDT",
    # "KDA/USDT","ICP/USDT","MATIC/USDT","ELON/USDT","NFT/USDT","ARRR/USDT","NEAR/USDT","CLV/USDT","SOL/USDT","SLP/USDT",
    # "XPR/USDT","DYDX/USDT","FTT/USDT","KAVA/USDT","XEC/USDT"
    # "method": "StaticPairList"

    # *16 / 100: 40    trades.
    # 31 / 9 / 0    Wins / Draws / Losses.
    # Avg    profit    2.34 %.
    # Median    profit    3.00 %.
    # Total    profit    928.95036811    USDT(92.90 %).
    # Avg    duration    3: 13:00    min.\
    # Objective: -11.63412

    # ROI table:
    minimal_roi = {
        "0": 0.213,
        "27": 0.099,
        "60": 0.03,
        "164": 0
    }

    # Stoploss:
    stoploss = -0.318

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Strategy parameters
    buy_umacd_max = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.01176, space="buy")
    buy_umacd_min = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.01416, space="buy")
    sell_umacd_max = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.02323, space="sell")
    sell_umacd_min = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.00707, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ma12'] = ta.EMA(dataframe, timeperiod=12)
        dataframe['ma26'] = ta.EMA(dataframe, timeperiod=26)
        dataframe['umacd'] = (dataframe['ma12'] / dataframe['ma26']) - 1

        # Just for show user the min and max of indicator in different coins to set inside hyperoptable variables.cuz
        # in different timeframes should change the min and max in hyperoptable variables.
        # print(dataframe['umacd'].min(), dataframe['umacd'].max())

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['umacd'].between(self.buy_umacd_min.value, self.buy_umacd_max.value))

            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['umacd'].between(self.sell_umacd_min.value, self.sell_umacd_max.value))
            ),
            'exit_long'] = 1

        return dataframe
