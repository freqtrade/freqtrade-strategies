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


class ThreeBlackCrows(IStrategy):
    # By: Masoud Azizi (@mablue)
    # Investopedia Link: https://www.investopedia.com/terms/t/three_black_crows.asp

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '5m'

    # Can this strategy go short?
    can_short: bool = False

    # $ freqtrade hyperopt -s ThreeBlackCrows --hyperopt-loss SharpeHyperOptLossDaily

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

    # 44/100:     73 trades. 33/39/1 Wins/Draws/Losses.
    # Avg profit   1.04%.
    # Median profit   0.00%.
    # Total profit 754.07546328 USDT (  75.41%).
    # Avg duration 10:04:00 min.
    # Objective: -9.94281

    # Buy hyperspace params:
    buy_params = {
        "buy_pow": 1.821,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_pow": 1.989,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.19,
        "29": 0.049,
        "60": 0.027,
        "152": 0
    }

    # Stoploss:
    stoploss = -0.213

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Strategy parameters
    buy_pow = DecimalParameter(1, 2, decimals=3, default=1.5, space="buy")
    sell_pow = DecimalParameter(1, 2, decimals=3, default=1.5, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['close'].shift(0) > dataframe['close'].shift(2) ** self.buy_pow.value) &
                    (dataframe['close'].shift(1) > dataframe['close'].shift(3) ** self.buy_pow.value) &
                    (dataframe['close'].shift(2) > dataframe['close'].shift(4) ** self.buy_pow.value)

            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(
                (dataframe['close'].shift(0) < dataframe['close'].shift(2) ** self.sell_pow.value) |
                (dataframe['close'].shift(1) < dataframe['close'].shift(3) ** self.sell_pow.value) |
                (dataframe['close'].shift(2) < dataframe['close'].shift(4) ** self.sell_pow.value)
        ),
        'exit_long'] = 1

        return dataframe
