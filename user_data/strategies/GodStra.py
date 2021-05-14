# GodStra Strategy
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell --strategy GodStraNew
# --- Do not remove these libs ---
from freqtrade.strategy.hyper import CategoricalParameter, RealParameter

from numpy.lib import math
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# --------------------------------

# Add your lib to import here
# TODO: talib is fast but have not more indicators
import talib.abstract as ta
# TODO: ta library is not speedy!
# from ta import add_all_ta_features, add_trend_ta, add_volatility_ta
import pandas as pd
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce
import numpy as np
from random import shuffle
#  TODO: this gene is removed 'MAVP' cuz or error on periods
god_genes = [
    'ACOS', 'AD', 'ADD', 'ADOSC', 'ADX', 'ADXR', 'APO',
    'AROON-0', 'AROON-1', 'AROONOSC', 'ASIN', 'ATAN', 'ATR', 'AVGPRICE',
    'BBANDS-0', 'BBANDS-1', 'BBANDS-2', 'BETA',
    'BOP', 'CCI', 'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE',
    'CDL3OUTSIDE', 'CDL3STARSINSOUTH', 'CDL3WHITESOLDIERS', 'CDLABANDONEDBABY',
    'CDLADVANCEBLOCK', 'CDLBELTHOLD', 'CDLBREAKAWAY', 'CDLCLOSINGMARUBOZU',
    'CDLCONCEALBABYSWALL', 'CDLCOUNTERATTACK', 'CDLDARKCLOUDCOVER', 'CDLDOJI',
    'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLENGULFING', 'CDLEVENINGDOJISTAR',
    'CDLEVENINGSTAR', 'CDLGAPSIDESIDEWHITE', 'CDLGRAVESTONEDOJI', 'CDLHAMMER',
    'CDLHANGINGMAN', 'CDLHARAMI', 'CDLHARAMICROSS', 'CDLHIGHWAVE', 'CDLHIKKAKE',
    'CDLHIKKAKEMOD', 'CDLHOMINGPIGEON', 'CDLIDENTICAL3CROWS', 'CDLINNECK',
    'CDLINVERTEDHAMMER', 'CDLKICKING', 'CDLKICKINGBYLENGTH', 'CDLLADDERBOTTOM',
    'CDLLONGLEGGEDDOJI', 'CDLLONGLINE', 'CDLMARUBOZU', 'CDLMATCHINGLOW',
    'CDLMATHOLD', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR', 'CDLONNECK',
    'CDLPIERCING', 'CDLRICKSHAWMAN', 'CDLRISEFALL3METHODS', 'CDLSEPARATINGLINES',
    'CDLSHOOTINGSTAR', 'CDLSHORTLINE', 'CDLSPINNINGTOP', 'CDLSTALLEDPATTERN',
    'CDLSTICKSANDWICH', 'CDLTAKURI', 'CDLTASUKIGAP', 'CDLTHRUSTING', 'CDLTRISTAR',
    'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS', 'CDLXSIDEGAP3METHODS', 'CEIL', 'CMO',
    'CORREL', 'COS', 'COSH', 'DEMA', 'DIV', 'DX', 'EMA', 'EXP', 'FLOOR',
    'HT_DCPERIOD', 'HT_DCPHASE',
    'HT_PHASOR-0', 'HT_PHASOR-1', 'HT_SINE-0', 'HT_SINE-1', 'HT_TRENDLINE',
    'HT_TRENDMODE', 'KAMA', 'LINEARREG', 'LINEARREG_ANGLE', 'LINEARREG_INTERCEPT',
    'LINEARREG_SLOPE', 'LN', 'LOG10', 'MA',
    'MACD-0', 'MACD-1', 'MACD-2', 'MACDEXT-0', 'MACDEXT-1', 'MACDEXT-2',
    'MACDFIX-0', 'MACDFIX-1', 'MACDFIX-2',
    # 'MAVP',
    'MAMA-0', 'MAMA-1',
    'MAX', 'MAXINDEX', 'MEDPRICE', 'MFI', 'MIDPOINT', 'MIDPRICE',
    'MIN', 'MININDEX', 'MINMAX-0', 'MINMAX-1', 'MINMAXINDEX-0', 'MINMAXINDEX-1',
    'MINUS_DI', 'MINUS_DM', 'MOM',
    'MULT', 'NATR', 'OBV', 'PLUS_DI', 'PLUS_DM', 'PPO', 'ROC', 'ROCP', 'ROCR',
    'ROCR100', 'RSI', 'SAR', 'SAREXT', 'SIN', 'SINH', 'SMA', 'SQRT', 'STDDEV',
    'STOCH-0', 'STOCH-1', 'STOCHF-0', 'STOCHF-1', 'STOCHRSI-0', 'STOCHRSI-1',
    'SUB', 'SUM', 'T3', 'TAN', 'TANH', 'TEMA',
    'TRANGE', 'TRIMA', 'TRIX', 'TSF', 'TYPPRICE', 'ULTOSC', 'VAR', 'WCLPRICE',
    'WILLR', 'WMA'
]
########################### SETTINGS ##############################
# shuffle(god_genes)
# god_genes = god_genes[:5]
# god_genes = ['SMA', 'EMA', 'RSI', 'MFI']
timeperiods = [5, 10, 100, 6, 15, 145]
operators = [
    "D",  # Disabled gene
    ">",  # Indicator, bigger than cross indicator
    "<",  # Indicator, smaller than cross indicator
    "=",  # Indicator, equal with cross indicator
    "C",  # Indicator, crossed the cross indicator
    "CA",  # Indicator, crossed above the cross indicator
    "CB",  # Indicator, crossed below the cross indicator
    ">R",  # Normalized indicator, bigger than real number
    "=R",  # Normalized indicator, equal with real number
    "<R",  # Normalized indicator, smaller than real number
    "/>R",  # Normalized indicator devided to cross indicator, bigger than real number
    "/=R",  # Normalized indicator devided to cross indicator, equal with real number
    "/<R",  # Normalized indicator devided to cross indicator, smaller than real number
    "UT",  # Indicator, is in UpTrend status
    "DT",  # Indicator, is in DownTrend status
    "OT",  # Indicator, is in Off trend status(horizontal slope)
    "CUT",  # Indicator, Entered to UpTrend status
    "CDT",  # Indicator, Entered to DownTrend status
    "COT"  # Indicator, Entered to Off trend status(horizontal slope)
]
# number of candles to check up,don,off trend.
TREND_CHECK_CANDLES = 4

########################### END SETTINGS ##########################

print('selected indicators for optimzatin: \n', god_genes)

god_genes_with_timeperiod = list()
for gene in god_genes:
    for timeperiod in timeperiods:
        god_genes_with_timeperiod.append(f'{gene}-{timeperiod}')

if len(god_genes) == 1:
    god_genes = god_genes*2
if len(timeperiods) == 1:
    timeperiods = timeperiods*2
if len(operators) == 1:
    operators = operators*2


def normalize(df):
    return (df-df.min())/(df.max()-df.min())


def gene_calculator(dataframe, indicator):
    if indicator in dataframe.index:
        return dataframe[indicator]
    else:
        gene = indicator.split("-")
        gene_name = gene[0]
        result = None
        if len(gene) == 2:
            gene_timeperiod = int(gene[1])
            result = getattr(ta, gene_name)(
                dataframe,
                timeperiod=gene_timeperiod,
            )

        elif len(gene) == 3:
            gene_index = int(gene[1])
            gene_timeperiod = int(gene[2])
            result = getattr(ta, gene_name)(
                dataframe,
                timeperiod=gene_timeperiod,
            ).iloc[:, gene_index]
        return normalize(result).fillna(0)


def condition_generator(dataframe, operator, indicator, crossed_indicator, real_num):
    condition = (dataframe['volume'] > 10)

    # TODO : it ill callculated in populate indicators.
    indicator_dataframe = gene_calculator(dataframe, indicator)
    crossed_indicator_dataframe = gene_calculator(
        dataframe, crossed_indicator)

    if operator == ">":
        condition = (
            indicator_dataframe > crossed_indicator_dataframe
        )
    elif operator == "=":
        condition = (
            np.isclose(indicator_dataframe, crossed_indicator_dataframe)
        )
    elif operator == "<":
        condition = (
            indicator_dataframe < crossed_indicator_dataframe
        )
    elif operator == "C":
        condition = (
            (qtpylib.crossed_below(indicator_dataframe, crossed_indicator_dataframe)) |
            (qtpylib.crossed_above(indicator_dataframe, crossed_indicator_dataframe))
        )
    elif operator == "CA":
        condition = (
            qtpylib.crossed_above(indicator_dataframe,
                                  crossed_indicator_dataframe)
        )
    elif operator == "CB":
        condition = (
            qtpylib.crossed_below(
                indicator_dataframe, crossed_indicator_dataframe)
        )
    elif operator == ">R":
        condition = (
            indicator_dataframe > real_num
        )
    elif operator == "=R":
        condition = (
            np.isclose(indicator_dataframe, real_num)
        )
    elif operator == "<R":
        condition = (
            indicator_dataframe < real_num
        )
    elif operator == "/>R":
        condition = (
            indicator_dataframe.div(crossed_indicator_dataframe) > real_num
        )
    elif operator == "/=R":
        condition = (
            np.isclose(indicator_dataframe.div(
                crossed_indicator_dataframe), real_num)
        )
    elif operator == "/<R":
        condition = (
            indicator_dataframe.div(crossed_indicator_dataframe) < real_num
        )
    elif operator == "UT":
        condition = (
            indicator_dataframe > ta.SMA(
                indicator_dataframe, TREND_CHECK_CANDLES)
        )
    elif operator == "DT":
        condition = (
            indicator_dataframe < ta.SMA(
                indicator_dataframe, TREND_CHECK_CANDLES)
        )
    elif operator == "OT":
        condition = (

            np.isclose(indicator_dataframe, ta.SMA(
                indicator_dataframe, TREND_CHECK_CANDLES))
        )
    elif operator == "CUT":
        condition = (
            (
                qtpylib.crossed_above(
                    indicator_dataframe,
                    ta.SMA(indicator_dataframe, TREND_CHECK_CANDLES)
                )
            ) &
            (
                indicator_dataframe > ta.SMA(
                    indicator_dataframe, TREND_CHECK_CANDLES)
            )
        )
    elif operator == "CDT":
        condition = (
            (
                qtpylib.crossed_below(
                    indicator_dataframe,
                    ta.SMA(indicator_dataframe, TREND_CHECK_CANDLES)
                )
            ) &
            (
                indicator_dataframe < ta.SMA(
                    indicator_dataframe, TREND_CHECK_CANDLES)
            )
        )
    elif operator == "COT":
        condition = (
            (
                (
                    qtpylib.crossed_below(
                        indicator_dataframe,
                        ta.SMA(indicator_dataframe, TREND_CHECK_CANDLES)
                    )
                ) |
                (
                    qtpylib.crossed_above(
                        indicator_dataframe,
                        ta.SMA(indicator_dataframe, TREND_CHECK_CANDLES)
                    )
                )
            ) &
            (
                np.isclose(indicator_dataframe, ta.SMA(
                    indicator_dataframe, TREND_CHECK_CANDLES))
            )
        )

    return condition


class GodStra(IStrategy):
    # #################### RESULTS PASTE PLACE ####################
    # *   12/1000:      6 trades.
    # 6/0/0 Wins/Draws/Losses.
    # Avg profit  114.67%.
    # Median profit  127.86%.
    # Total profit  0.13885893 BTC ( 138.86Σ%).
    # Avg duration 30 days, 10:00:00 min.
    # Objective: -6.09827

    # Buy hyperspace params:
    buy_params = {
        "buy_crossed_indicator0": "MAMA-0-6",
        "buy_crossed_indicator1": "SQRT-100",
        "buy_crossed_indicator2": "HT_PHASOR-0-100",
        "buy_indicator0": "CDLSHORTLINE-100",
        "buy_indicator1": "CORREL-100",
        "buy_indicator2": "CDLLONGLINE-100",
        "buy_operator0": "C",
        "buy_operator1": "=",
        "buy_operator2": "<R",
        "buy_real_num0": 0.00599,
        "buy_real_num1": 0.97236,
        "buy_real_num2": 0.9266,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_crossed_indicator0": "CDLTASUKIGAP-5",
        "sell_crossed_indicator1": "SAR-5",
        "sell_crossed_indicator2": "TRIX-5",
        "sell_indicator0": "LINEARREG-5",
        "sell_indicator1": "MIDPOINT-145",
        "sell_indicator2": "MEDPRICE-145",
        "sell_operator0": "CDT",
        "sell_operator1": ">",
        "sell_operator2": "UT",
        "sell_real_num0": 0.2614,
        "sell_real_num1": 0.13667,
        "sell_real_num2": 0.37739,
    }
    # #################### END OF RESULT PLACE ####################

    # TODO: Its not dry code!
    # Buy Hyperoptable Parameters/Spaces.
    buy_crossed_indicator0 = CategoricalParameter(
        god_genes_with_timeperiod, default="ADD-20", space='buy')
    buy_crossed_indicator1 = CategoricalParameter(
        god_genes_with_timeperiod, default="ASIN-6", space='buy')
    buy_crossed_indicator2 = CategoricalParameter(
        god_genes_with_timeperiod, default="CDLEVENINGSTAR-50", space='buy')

    buy_indicator0 = CategoricalParameter(
        god_genes_with_timeperiod, default="SMA-100", space='buy')
    buy_indicator1 = CategoricalParameter(
        god_genes_with_timeperiod, default="WILLR-50", space='buy')
    buy_indicator2 = CategoricalParameter(
        god_genes_with_timeperiod, default="CDLHANGINGMAN-20", space='buy')

    buy_operator0 = CategoricalParameter(operators, default="/<R", space='buy')
    buy_operator1 = CategoricalParameter(operators, default="<R", space='buy')
    buy_operator2 = CategoricalParameter(operators, default="CB", space='buy')

    buy_real_num0 = RealParameter(0, 1, default=0.89009, space='buy')
    buy_real_num1 = RealParameter(0, 1, default=0.56953, space='buy')
    buy_real_num2 = RealParameter(0, 1, default=0.38365, space='buy')

    # Sell Hyperoptable Parameters/Spaces.
    sell_crossed_indicator0 = CategoricalParameter(
        god_genes_with_timeperiod, default="CDLSHOOTINGSTAR-150", space='sell')
    sell_crossed_indicator1 = CategoricalParameter(
        god_genes_with_timeperiod, default="MAMA-1-100", space='sell')
    sell_crossed_indicator2 = CategoricalParameter(
        god_genes_with_timeperiod, default="CDLMATHOLD-6", space='sell')

    sell_indicator0 = CategoricalParameter(
        god_genes_with_timeperiod, default="CDLUPSIDEGAP2CROWS-5", space='sell')
    sell_indicator1 = CategoricalParameter(
        god_genes_with_timeperiod, default="CDLHARAMICROSS-150", space='sell')
    sell_indicator2 = CategoricalParameter(
        god_genes_with_timeperiod, default="CDL2CROWS-5", space='sell')

    sell_operator0 = CategoricalParameter(
        operators, default="<R", space='sell')
    sell_operator1 = CategoricalParameter(operators, default="D", space='sell')
    sell_operator2 = CategoricalParameter(
        operators, default="/>R", space='sell')

    sell_real_num0 = RealParameter(0, 1, default=0.09731, space='sell')
    sell_real_num1 = RealParameter(0, 1, default=0.81657, space='sell')
    sell_real_num2 = RealParameter(0, 1, default=0.87267, space='sell')

    # Stoploss:
    stoploss = -1
    # Buy hypers
    timeframe = '4h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        '''
        It's good to calculate all indicators in all time periods here and so optimize the strategy.
        But this strategy can take much time to generate anything that may not use in his optimization.
        I just calculate the specific indicators in specific time period inside buy and sell strategy populator methods if needed.
        Also, this method (populate_indicators) just calculates default value of hyperoptable params
        so using this method have not big benefits instade of calculating useable things inside buy and sell trand populators
        '''
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = list()
        # TODO: Its not dry code!
        buy_indicator = self.buy_indicator0.value
        buy_crossed_indicator = self.buy_crossed_indicator0.value
        buy_operator = self.buy_operator0.value
        buy_real_num = self.buy_real_num0.value
        conditions.append(condition_generator(dataframe,
                                              buy_operator, buy_indicator, buy_crossed_indicator, buy_real_num))

        buy_indicator = self.buy_indicator1.value
        buy_crossed_indicator = self.buy_crossed_indicator1.value
        buy_operator = self.buy_operator1.value
        buy_real_num = self.buy_real_num1.value
        conditions.append(condition_generator(dataframe,
                                              buy_operator, buy_indicator, buy_crossed_indicator, buy_real_num))

        buy_indicator = self.buy_indicator2.value
        buy_crossed_indicator = self.buy_crossed_indicator2.value
        buy_operator = self.buy_operator2.value
        buy_real_num = self.buy_real_num2.value
        conditions.append(condition_generator(dataframe,
                                              buy_operator, buy_indicator, buy_crossed_indicator, buy_real_num))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = list()
        # TODO: Its not dry code!
        sell_indicator = self.sell_indicator0.value
        sell_crossed_indicator = self.sell_crossed_indicator0.value
        sell_operator = self.sell_operator0.value
        sell_real_num = self.sell_real_num0.value
        conditions.append(condition_generator(dataframe,
                                              sell_operator, sell_indicator, sell_crossed_indicator, sell_real_num))

        sell_indicator = self.sell_indicator1.value
        sell_crossed_indicator = self.sell_crossed_indicator1.value
        sell_operator = self.sell_operator1.value
        sell_real_num = self.sell_real_num1.value
        conditions.append(condition_generator(dataframe,
                                              sell_operator, sell_indicator, sell_crossed_indicator, sell_real_num))

        sell_indicator = self.sell_indicator2.value
        sell_crossed_indicator = self.sell_crossed_indicator2.value
        sell_operator = self.sell_operator2.value
        sell_real_num = self.sell_real_num2.value
        conditions.append(condition_generator(dataframe,
                                              sell_operator, sell_indicator, sell_crossed_indicator, sell_real_num))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
