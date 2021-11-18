# Ichess Strategy  ichimoku_score
# Associate various ichimoku signals with a score.
# For example, bullish signal => positive score,
# and bearish signal => negative score. If the total score is above 0, it may indicate a bullish trend .
# Otherwise, if it is below 0, it may indicate a bearish trend .
# We used two smoothed moving averages to find the trend.
# More info:
# https://github.com/freqtrade/freqtrade-strategies/issues/97
# https://www.tradingview.com/script/P1bybHZA-Ichimoku-Cloud-Signal-Score-v2-0-0/
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/

# --- Do not remove these libs ---
from freqtrade.strategy import IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import numpy as np
# --------------------------------

# Add your lib to import here
# import talib.abstract as ta
import talib as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce

class Ichess(IStrategy):
    
    # ROI table:
    minimal_roi = {
        "0": 0.642,
        "8834": 0.37,
        "25392": 0.118,
        "55146": 0
    }

    # Stoploss:
    stoploss = -0.314

    # Opt Timeframe
    timeframe = '1d'

    buy_fast_timeperiod = IntParameter(2, 50, default=9, space="buy")
    buy_slow_timeperiod = IntParameter(2, 50, default=10, space="buy")

    sell_fast_timeperiod = IntParameter(2, 50, default=15, space="sell")
    sell_slow_timeperiod = IntParameter(2, 50, default=16, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conversion_line_period = 9
        base_line_periods = 26
        laggin_span = 52
        displacement = 26

        df = dataframe.copy()

        # Heikin Ashi Strategy
        heikinashi = qtpylib.heikinashi(df)
        df['ha_open'] = heikinashi['open']
        df['ha_close'] = heikinashi['close']
        df['ha_high'] = heikinashi['high']
        df['ha_low'] = heikinashi['low']

        df['tenkan'] = (df['ha_high'].rolling(window=conversion_line_period).max() +
                        df['ha_low'].rolling(window=conversion_line_period).min()) / 2
        df['kijun'] = (df['ha_high'].rolling(window=base_line_periods).max() +
                       df['ha_low'].rolling(window=base_line_periods).min()) / 2
        df['senkou_leading_a'] = (df['tenkan'] + df['kijun']) / 2
        df['senkou_leading_b'] = (df['ha_high'].rolling(
            window=laggin_span).max() + df['ha_low'].rolling(window=laggin_span).min()) / 2
        df['senkou_span_a'] = df['senkou_leading_a'].shift(displacement)
        df['senkou_span_b'] = df['senkou_leading_b'].shift(displacement)
        df['chikou_span'] = df['ha_close'].shift(displacement)

        df['tenkan1'] = df['tenkan'].shift(+1)
        df['kijun1'] = df['kijun'].shift(+1)
        df['senkou_leading_a1'] = df['senkou_leading_a'].shift(+1)
        df['senkou_leading_b1'] = df['senkou_leading_b'].shift(+1)
        df['senkou_span_a1'] = df['senkou_span_a'].shift(+1)
        df['senkou_span_b1'] = df['senkou_span_b'].shift(+1)
        df['chikou_span1'] = df['chikou_span'].shift(+1)

        df['ha_close1'] = df['ha_close'].shift(+1)

        # // == Price and Kijun Sen (standard line) Cross ==

        def calcTkCross(
            tenkan,
            kijun,
            tenkan1,
            kijun1,
            senkou_span_a,
            senkou_span_b,
        ):
            if (tenkan > kijun) and (tenkan1 <= kijun1):
                intersect = (tenkan1 * (kijun - kijun1) - kijun1 * (tenkan -
                             tenkan1)) / ((kijun - kijun1) - (tenkan - tenkan1))
                if (intersect > senkou_span_a) and (intersect > senkou_span_b):
                    return 2
                elif(intersect < senkou_span_a) and (intersect < senkou_span_b):
                    return 0.5
                else:
                    return 1
            elif (tenkan < kijun) and (tenkan1 >= kijun1):
                intersect = (tenkan1 * (kijun - kijun1) - kijun1 * (tenkan -
                             tenkan1)) / ((kijun - kijun1) - (tenkan - tenkan1))
                if (intersect > senkou_span_a) and (intersect > senkou_span_b):
                    return -0.5
                elif(intersect < senkou_span_a) and (intersect < senkou_span_b):
                    return -2
                else:
                    return -1
            else:
                return 0

        # df['tkCrossScore'] = np.vectorize(calcTkCross)()
        df['tkCrossScore'] = np.vectorize(calcTkCross)(
            df['tenkan'],
            df['kijun'],
            df['tenkan1'],
            df['kijun1'],
            df['senkou_span_a'],
            df['senkou_span_b'],
        )
        # // == Price and Kijun Sen (standard line) Cross ==

        def calcPkCross(
            ha_close,
            kijun,
            ha_close1,
            kijun1,
            senkou_span_a,
            senkou_span_b,
        ):
            if (ha_close > kijun) and (ha_close1 <= kijun1):
                intersect = (ha_close1 * (kijun - kijun1) - kijun1 * (ha_close -
                             ha_close1)) / ((kijun - kijun1) - (ha_close - ha_close1))
                if (intersect > senkou_span_a) and (intersect > senkou_span_b):
                    return 2
                elif(intersect < senkou_span_a) and (intersect < senkou_span_b):
                    return 0.5
                else:
                    return 1
            elif (ha_close < kijun) and (ha_close1 >= kijun1):
                intersect = (ha_close1 * (kijun - kijun1) - kijun1 * (ha_close -
                             ha_close1)) / ((kijun - kijun1) - (ha_close - ha_close1))
                if (intersect > senkou_span_a) and (intersect > senkou_span_b):
                    return -0.5
                elif(intersect < senkou_span_a) and (intersect < senkou_span_b):
                    return -2
                else:
                    return -1
            else:
                return 0

        df['pkCrossScore'] = np.vectorize(calcPkCross)(
            df['ha_close'],
            df['kijun'],
            df['ha_close1'],
            df['kijun1'],
            df['senkou_span_a'],
            df['senkou_span_b'],
        )

        # // == Kumo Breakouts ==
        def calcKumoBreakout(
            ha_close,
            senkou_span_a,
            ha_close1,
            senkou_span_a1,
            senkou_span_b,
            senkou_span_b1,
        ):
            if (((ha_close > senkou_span_a) and (ha_close1 <= senkou_span_a1) and (senkou_span_a > senkou_span_b)) or ((ha_close > senkou_span_b) and (ha_close1 <= senkou_span_b1) and (senkou_span_a < senkou_span_b))):
                return 2
            elif(((ha_close < senkou_span_a) and (ha_close1 >= senkou_span_a1) and (senkou_span_a < senkou_span_b)) or ((ha_close < senkou_span_b) and (ha_close1 >= senkou_span_b1) and (senkou_span_a > senkou_span_b))):
                return -2
            else:
                return 0

        df['kumoBreakoutScore'] = np.vectorize(calcKumoBreakout)(
            df['ha_close'],
            df['senkou_span_a'],
            df['ha_close1'],
            df['senkou_span_a1'],
            df['senkou_span_b'],
            df['senkou_span_b1'],
        )

        # // == Senkou Span Cross ==
        def calcSenkouCross(
            senkou_leading_a,
            senkou_leading_b,
            senkou_leading_a1,
            senkou_leading_b1,
            ha_close,
            senkou_span_a,
            senkou_span_b,
        ):
            if (senkou_leading_a > senkou_leading_b) and (senkou_leading_a1 <= senkou_leading_b1):
                if (ha_close > senkou_span_a) and (ha_close > senkou_span_b):
                    return 2
                elif(ha_close < senkou_span_a) and (ha_close < senkou_span_b):
                    return 0.5
                else:
                    return 1
            elif (senkou_leading_a < senkou_leading_b) and (senkou_leading_a1 >= senkou_leading_b1):
                if (ha_close > senkou_span_a) and (ha_close > senkou_span_b):
                    return -0.5
                elif(ha_close < senkou_span_a) and (ha_close < senkou_span_b):
                    return -2
                else:
                    return -1
            else:
                return 0

        df['senkouCrossScore'] = np.vectorize(calcSenkouCross)(
            df['senkou_leading_a'],
            df['senkou_leading_b'],
            df['senkou_leading_a1'],
            df['senkou_leading_b1'],
            df['ha_close'],
            df['senkou_span_a'],
            df['senkou_span_b'],
        )
        # // == Chikou Span Cross ==

        def calcChikouCross(
            ha_close,
            chikou_span,
            ha_close1,
            chikou_span1,
            senkou_span_a,
            senkou_span_b,
        ):
            if (ha_close > chikou_span) and (ha_close1 <= chikou_span1):
                intersect = (ha_close1 * (chikou_span - chikou_span1) - chikou_span1 * (
                    ha_close - ha_close1)) / ((chikou_span - chikou_span1) - (ha_close - ha_close1))
                if (intersect > senkou_span_a) and (intersect > senkou_span_b):
                    return 2
                elif(intersect < senkou_span_a) and (intersect < senkou_span_b):
                    return 0.5
                else:
                    return 1
            elif (ha_close < chikou_span) and (ha_close1 >= chikou_span1):
                intersect = (ha_close1 * (chikou_span - chikou_span1) - chikou_span1 * (
                    ha_close - ha_close1)) / ((chikou_span - chikou_span1) - (ha_close - ha_close1))
                if (intersect > senkou_span_a) and (intersect > senkou_span_b):
                    return -0.5
                elif(intersect < senkou_span_a) and (intersect < senkou_span_b):
                    return -2
                else:
                    return -1
            else:
                return 0

        df['chikouCrossScore'] = np.vectorize(calcChikouCross)(
            df['ha_close'],
            df['chikou_span'],
            df['ha_close1'],
            df['chikou_span1'],
            df['senkou_span_a'],
            df['senkou_span_b'],
        )

        # // == price relative to cloud ==
        def calcPricePlacement(
            ha_close,
            senkou_span_a,
            senkou_span_b,
        ):
            if (ha_close > senkou_span_a) and (ha_close > senkou_span_b):
                return 2
            elif(ha_close < senkou_span_a) and (ha_close < senkou_span_b):
                return -2
            else:
                return 0

        df['pricePlacementScore'] = np.vectorize(calcPricePlacement)(
            df['ha_close'],
            df['senkou_span_a'],
            df['senkou_span_b'],
        )

        # // == lag line releative to cloud ==
        def calcChikouPlacement(
            ha_close,
            senkou_leading_a,
            senkou_leading_b,
        ):
            if (ha_close > senkou_leading_a) and (ha_close > senkou_leading_b):
                return 2
            elif(ha_close < senkou_leading_a) and (ha_close < senkou_leading_b):
                return -2
            else:
                return 0

        df['chikouPlacementScore'] = np.vectorize(calcChikouPlacement)(
            df['ha_close'],
            df['senkou_leading_a'],
            df['senkou_leading_b'],
        )

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # //
        dataframe['Ichimoku_Score'] = (
            df['tkCrossScore'] +
            df['pkCrossScore'] +
            df['kumoBreakoutScore'] +
            df['senkouCrossScore'] +
            df['chikouCrossScore']
        ).rolling(1).sum().cumsum()

        print(metadata['pair'],dataframe['Ichimoku_Score'].median())

        return dataframe


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # exit()
        dataframe.loc[
            # (dataframe['Ichimoku_Score']>0)&
            qtpylib.crossed_above(
                ta.SMA(dataframe['Ichimoku_Score'], self.buy_fast_timeperiod.value),
                ta.SMA(dataframe['Ichimoku_Score'], self.buy_slow_timeperiod.value)
            ), 'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
                # (dataframe['Ichimoku_Score']<0)|
                (
                qtpylib.crossed_below(
                    ta.SMA(dataframe['Ichimoku_Score'], self.sell_fast_timeperiod.value),
                    ta.SMA(dataframe['Ichimoku_Score'], self.sell_slow_timeperiod.value)
                )
            ), 'sell'] = 1

        return dataframe
