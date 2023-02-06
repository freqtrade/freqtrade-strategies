# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
from datetime import datetime
from typing import Optional

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

import talib.abstract as ta
from freqtrade.persistence import Trade
from freqtrade.strategy import (CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy)
from freqtrade.exchange import date_minus_candles
import freqtrade.vendor.qtpylib.indicators as qtpylib

from technical.util import resample_to_interval, resampled_merge


class VolatilitySystem(IStrategy):
    """
    Volatility System strategy.
    Based on https://www.tradingview.com/script/3hhs0XbR/

    Leverage is optional but the lower the better to limit liquidations
    """
    can_short = True

    minimal_roi = {
        "0": 100
    }

    stoploss = -1

    # Optimal ticker interval for the strategy
    timeframe = '1h'

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        'main_plot': {
        },
        'subplots': {
            "Volatility system": {
                "atr": {"color": "white"},
                "abs_close_change": {"color": "red"},
            }
        }
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let easyprofiler do the work for you in finding out which indicators
        are worth adding.
        """
        resample_int = 60 * 3
        resampled = resample_to_interval(dataframe, resample_int)
        # Average True Range (ATR)
        resampled['atr'] = ta.ATR(resampled, timeperiod=14) * 2.0
        # Absolute close change
        resampled['close_change'] = resampled['close'].diff()
        resampled['abs_close_change'] = resampled['close_change'].abs()

        dataframe = resampled_merge(dataframe, resampled, fill_na=True)
        dataframe['atr'] = dataframe[f'resample_{resample_int}_atr']
        dataframe['close_change'] = dataframe[f'resample_{resample_int}_close_change']
        dataframe['abs_close_change'] = dataframe[f'resample_{resample_int}_abs_close_change']

        # Average True Range (ATR)
        # dataframe['atr'] = ta.ATR(dataframe, timeperiod=14) * 2.0
        # Absolute close change
        # dataframe['close_change'] = dataframe['close'].diff()
        # dataframe['abs_close_change'] = dataframe['close_change'].abs()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy and sell signals for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy and sell columns
        """
        # Use qtpylib.crossed_above to get only one signal, otherwise the signal is active
        # for the whole "long" timeframe.
        dataframe.loc[
            # qtpylib.crossed_above(dataframe['close_change'] * 1, dataframe['atr']),
            (dataframe['close_change'] * 1 > dataframe['atr'].shift(1)),
            'enter_long'] = 1
        dataframe.loc[
            # qtpylib.crossed_above(dataframe['close_change'] * -1, dataframe['atr']),
            (dataframe['close_change'] * -1 > dataframe['atr'].shift(1)),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        use sell/buy signals as long/short indicators
        """
        dataframe.loc[
            dataframe['enter_long'] == 1,
            'exit_short'] = 1
        dataframe.loc[
            dataframe['enter_short'] == 1,
            'exit_long'] = 1
        return dataframe

    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: Optional[float], max_stake: float,
                            leverage: float, entry_tag: Optional[str], side: str,
                            **kwargs) -> float:
        # 50% stake amount on initial entry
        return proposed_stake / 2

    position_adjustment_enable = True

    def adjust_trade_position(self, trade: Trade, current_time: datetime,
                              current_rate: float, current_profit: float,
                              min_stake: Optional[float], max_stake: float,
                              current_entry_rate: float, current_exit_rate: float,
                              current_entry_profit: float, current_exit_profit: float,
                              **kwargs) -> Optional[float]:
        dataframe, _ = self.dp.get_analyzed_dataframe(trade.pair, self.timeframe)
        if len(dataframe) > 2:
            last_candle = dataframe.iloc[-1].squeeze()
            previous_candle = dataframe.iloc[-2].squeeze()
            signal_name = 'enter_long' if not trade.is_short else 'enter_short'
            prior_date = date_minus_candles(self.timeframe, 1, current_time)
            # Only enlarge position on new signal.
            if (
                last_candle[signal_name] == 1
                and previous_candle[signal_name] != 1
                and trade.nr_of_successful_entries < 2
                and trade.orders[-1].order_date_utc < prior_date
            ):
                return trade.stake_amount
        return None

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, side: str,
                 **kwargs) -> float:
        """
        Customize leverage for each new trade. This method is only called in futures mode.

        :param pair: Pair that's currently analyzed
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param proposed_leverage: A leverage proposed by the bot.
        :param max_leverage: Max leverage allowed on this pair
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the proposed trade
        :return: A leverage amount, which is between 1.0 and max_leverage.
        """
        return 2.0
