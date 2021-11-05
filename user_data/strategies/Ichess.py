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
from freqtrade.strategy.hyper import IntParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
# import talib.abstract as ta
import talib as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce

# Settings


class Ichess(IStrategy):
    #     98/100:      9 trades. 8/0/1 Wins/Draws/Losses. Avg profit  20.91%. Median profit  14.19%. Total profit  746.86178061 USDT (  74.69%). Avg duration 9 days, 0:00:00 min. Objective: 1.62888


    # Buy hyperspace params:
    buy_params = {
        "buy_vol_max": 3,
        "buy_vol_min": 23,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_vol_max": 48,
        "sell_vol_min": 20,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.534,
        "6699": 0.186,
        "17925": 0.142,
        "51598": 0
    }

    # Stoploss:
    stoploss = -0.341

    # Trailing stop:
    trailing_stop = False  # value loaded from strategy
    trailing_stop_positive = None  # value loaded from strategy
    trailing_stop_positive_offset = 0.0  # value loaded from strategy
    trailing_only_offset_is_reached = False  # value loaded from strategy
    # Opt Timeframe
    timeframe = '1d'

    buy_vol_min = IntParameter(2, 50, default=0, space="buy")
    buy_vol_max = IntParameter(2, 50, default=0, space="buy")

    sell_vol_min = IntParameter(2, 50, default=0, space="sell")
    sell_vol_max = IntParameter(2, 50, default=0, space="sell")

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

        def calcTkCross(x):
            if (x['tenkan'] > x['kijun']) and (x['tenkan1'] <= x['kijun1']):
                intersect = (x['tenkan1'] * (x['kijun'] - x['kijun1']) - x['kijun1'] * (x['tenkan'] -
                             x['tenkan1'])) / ((x['kijun'] - x['kijun1']) - (x['tenkan'] - x['tenkan1']))
                if (intersect > x['senkou_span_a']) and (intersect > x['senkou_span_b']):
                    return 2
                elif(intersect < x['senkou_span_a']) and (intersect < x['senkou_span_b']):
                    return 0.5
                else:
                    return 1
            elif (x['tenkan'] < x['kijun']) and (x['tenkan1'] >= x['kijun1']):
                intersect = (x['tenkan1'] * (x['kijun'] - x['kijun1']) - x['kijun1'] * (x['tenkan'] -
                             x['tenkan1'])) / ((x['kijun'] - x['kijun1']) - (x['tenkan'] - x['tenkan1']))
                if (intersect > x['senkou_span_a']) and (intersect > x['senkou_span_b']):
                    return -0.5
                elif(intersect < x['senkou_span_a']) and (intersect < x['senkou_span_b']):
                    return -2
                else:
                    return -1
            else:
                return 0

        df['tkCrossScore'] = df.apply(calcTkCross, axis=1)

        # // == Price and Kijun Sen (standard line) Cross ==
        def calcPkCross(x):
            if (x['ha_close'] > x['kijun']) and (x['ha_close1'] <= x['kijun1']):
                intersect = (x['ha_close1'] * (x['kijun'] - x['kijun1']) - x['kijun1'] * (x['ha_close'] -
                             x['ha_close1'])) / ((x['kijun'] - x['kijun1']) - (x['ha_close'] - x['ha_close1']))
                if (intersect > x['senkou_span_a']) and (intersect > x['senkou_span_b']):
                    return 2
                elif(intersect < x['senkou_span_a']) and (intersect < x['senkou_span_b']):
                    return 0.5
                else:
                    return 1
            elif (x['ha_close'] < x['kijun']) and (x['ha_close1'] >= x['kijun1']):
                intersect = (x['ha_close1'] * (x['kijun'] - x['kijun1']) - x['kijun1'] * (x['ha_close'] -
                             x['ha_close1'])) / ((x['kijun'] - x['kijun1']) - (x['ha_close'] - x['ha_close1']))
                if (intersect > x['senkou_span_a']) and (intersect > x['senkou_span_b']):
                    return -0.5
                elif(intersect < x['senkou_span_a']) and (intersect < x['senkou_span_b']):
                    return -2
                else:
                    return -1
            else:
                return 0

        df['pkCrossScore'] = df.apply(calcPkCross, axis=1)

        # // == Kumo Breakouts ==
        def calcKumoBreakout(x):
            if (((x['ha_close'] > x['senkou_span_a']) and (x['ha_close1'] <= x['senkou_span_a1']) and (x['senkou_span_a'] > x['senkou_span_b'])) or ((x['ha_close'] > x['senkou_span_b']) and (x['ha_close1'] <= x['senkou_span_b1']) and (x['senkou_span_a'] < x['senkou_span_b']))):
                return 2
            elif(((x['ha_close'] < x['senkou_span_a']) and (x['ha_close1'] >= x['senkou_span_a1']) and (x['senkou_span_a'] < x['senkou_span_b'])) or ((x['ha_close'] < x['senkou_span_b']) and (x['ha_close1'] >= x['senkou_span_b1']) and (x['senkou_span_a'] > x['senkou_span_b']))):
                return -2
            else:
                return 0

        df['kumoBreakoutScore'] = df.apply(calcKumoBreakout, axis=1)

        # // == Senkou Span Cross ==
        def calcSenkouCross(x):
            if (x['senkou_leading_a'] > x['senkou_leading_b']) and (x['senkou_leading_a1'] <= x['senkou_leading_b1']):
                if (x['ha_close'] > x['senkou_span_a']) and (x['ha_close'] > x['senkou_span_b']):
                    return 2
                elif(x['ha_close'] < x['senkou_span_a']) and (x['ha_close'] < x['senkou_span_b']):
                    return 0.5
                else:
                    return 1
            elif (x['senkou_leading_a'] < x['senkou_leading_b']) and (x['senkou_leading_a1'] >= x['senkou_leading_b1']):
                if (x['ha_close'] > x['senkou_span_a']) and (x['ha_close'] > x['senkou_span_b']):
                    return -0.5
                elif(x['ha_close'] < x['senkou_span_a']) and (x['ha_close'] < x['senkou_span_b']):
                    return -2
                else:
                    return -1
            else:
                return 0

        df['senkouCrossScore'] = df.apply(calcSenkouCross, axis=1)

        # // == Chikou Span Cross ==
        def calcChikouCross(x):
            if (x['ha_close'] > x['chikou_span']) and (x['ha_close1'] <= x['chikou_span1']):
                intersect = (x['ha_close1'] * (x['chikou_span'] - x['chikou_span1']) - x['chikou_span1'] * (
                    x['ha_close'] - x['ha_close1'])) / ((x['chikou_span'] - x['chikou_span1']) - (x['ha_close'] - x['ha_close1']))
                if (intersect > x['senkou_span_a']) and (intersect > x['senkou_span_b']):
                    return 2
                elif(intersect < x['senkou_span_a']) and (intersect < x['senkou_span_b']):
                    return 0.5
                else:
                    return 1
            elif (x['ha_close'] < x['chikou_span']) and (x['ha_close1'] >= x['chikou_span1']):
                intersect = (x['ha_close1'] * (x['chikou_span'] - x['chikou_span1']) - x['chikou_span1'] * (
                    x['ha_close'] - x['ha_close1'])) / ((x['chikou_span'] - x['chikou_span1']) - (x['ha_close'] - x['ha_close1']))
                if (intersect > x['senkou_span_a']) and (intersect > x['senkou_span_b']):
                    return -0.5
                elif(intersect < x['senkou_span_a']) and (intersect < x['senkou_span_b']):
                    return -2
                else:
                    return -1
            else:
                return 0

        df['chikouCrossScore'] = df.apply(calcChikouCross, axis=1)

        # // == price relative to cloud ==
        def calcPricePlacement(x):
            if (x['ha_close'] > x['senkou_span_a']) and (x['ha_close'] > x['senkou_span_b']):
                return 2
            elif(x['ha_close'] < x['senkou_span_a']) and (x['ha_close'] < x['senkou_span_b']):
                return -2
            else:
                return 0

        df['pricePlacementScore'] = df.apply(calcPricePlacement, axis=1)

        # // == lag line releative to cloud ==
        def calcChikouPlacement(x):
            if (x['ha_close'] > x['senkou_leading_a']) and (x['ha_close'] > x['senkou_leading_b']):
                return 2
            elif(x['ha_close'] < x['senkou_leading_a']) and (x['ha_close'] < x['senkou_leading_b']):
                return -2
            else:
                return 0

        df['chikouPlacementScore'] = df.apply(calcChikouPlacement, axis=1)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # //
        dataframe['Ichimoku_Score'] = (
            df['tkCrossScore'] +
            df['pkCrossScore'] +
            df['kumoBreakoutScore'] +
            df['senkouCrossScore'] +
            df['chikouCrossScore']
        ).cumsum()
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            qtpylib.crossed_above(
                ta.SMA(dataframe['Ichimoku_Score'], self.buy_vol_min.value),
                ta.SMA(dataframe['Ichimoku_Score'], self.buy_vol_max.value)
            ), 'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            qtpylib.crossed_above(
                ta.SMA(dataframe['Ichimoku_Score'], self.sell_vol_min.value),
                ta.SMA(dataframe['Ichimoku_Score'], self.sell_vol_max.value)
            ), 'sell'] = 1

        return dataframe
