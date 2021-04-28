# GodStra Strategy
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# hyperopt befour run
# --- Do not remove these libs ---
import logging

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


tplist = [7, 14]
GodGeneIndicators = ['ACOS', 'AD', 'ADD', 'ADOSC', 'ADX', 'ADXR', 'APO',
                     'AROON', 'AROONOSC', 'ASIN', 'ATAN', 'ATR', 'AVGPRICE', 'BBANDS', 'BETA',
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
                     'HT_DCPERIOD', 'HT_DCPHASE', 'HT_PHASOR', 'HT_SINE', 'HT_TRENDLINE',
                     'HT_TRENDMODE', 'KAMA', 'LINEARREG', 'LINEARREG_ANGLE', 'LINEARREG_INTERCEPT',
                     'LINEARREG_SLOPE', 'LN', 'LOG10', 'MA', 'MACD', 'MACDEXT', 'MACDFIX',
                     'MAMA', 'MAX', 'MAXINDEX', 'MEDPRICE', 'MFI', 'MIDPOINT', 'MIDPRICE',
                     'MIN', 'MININDEX', 'MINMAX', 'MINMAXINDEX', 'MINUS_DI', 'MINUS_DM', 'MOM',
                     'MULT', 'NATR', 'OBV', 'PLUS_DI', 'PLUS_DM', 'PPO', 'ROC', 'ROCP', 'ROCR',
                     'ROCR100', 'RSI', 'SAR', 'SAREXT', 'SIN', 'SINH', 'SMA', 'SQRT', 'STDDEV',
                     'STOCH', 'STOCHF', 'STOCHRSI', 'SUB', 'SUM', 'T3', 'TAN', 'TANH', 'TEMA',
                     'TRANGE', 'TRIMA', 'TRIX', 'TSF', 'TYPPRICE', 'ULTOSC', 'VAR', 'WCLPRICE',
                     'WILLR', 'WMA']
#  TODO: this gene is removed 'MAVP' cuz or error on periods


class GodStra(IStrategy):
    # 62/500:    300 trades. 270/14/16 Wins/Draws/Losses. Avg profit   4.15%. Median profit   3.23%. Total profit  0.13750577 BTC ( 1244.80Σ%). Avg duration 2408.8 min. Objective: -96.12528
    
    # Buy hyperspace params:
    buy_params = {
        'buy-cross-0': 'CDLSPINNINGTOP-14',
        'buy-indicator-0': 'MAMA1-14',
        'buy-int-0': 100,
        'buy-oper-0': '<I',
        'buy-real-0': -0.97467
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-cross-0': 'RSI-7',
        'sell-indicator-0': 'CDLHAMMER-7',
        'sell-int-0': 86,
        'sell-oper-0': '=R',
        'sell-real-0': 0.27656
    }

    # ROI table:
    minimal_roi = {
        "0": 0.25707,
        "1415": 0.19249,
        "3356": 0.12085,
        "8420": 0
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.02803
    trailing_stop_positive_offset = 0.04082
    trailing_only_offset_is_reached = False

    # Stoploss:
    stoploss = -1
    # Buy hypers
    timeframe = '4h'

    # devided to 5: Cuz We have 5 Group of
    # variables inside buy_param:
    # (cross, indicator, int, oper, real)
    Buy_DNA_Size = int(len(buy_params)/5)
    Sell_DNA_Size = int(len(sell_params)/5)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add all ta features

        for gene in GodGeneIndicators:
            for tp in tplist:
                # print(gene)
                res = getattr(ta, gene)(
                    dataframe,
                    timeperiod=tp,
                )
                # TODO: fix MAVP error
                if type(res) == pd.core.series.Series and gene != 'MAVP':
                    dataframe[f'{gene}-{tp}'] = res
                else:
                    for idx, df in enumerate(res):
                        dataframe[f'{gene}{idx}-{tp}'] = res.iloc[:, idx]

        print(metadata['pair'])
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = list()
        for i in range(self.Buy_DNA_Size):

            OPR = self.buy_params[f'buy-oper-{i}']
            IND = self.buy_params[f'buy-indicator-{i}']
            CRS = self.buy_params[f'buy-cross-{i}']
            INT = self.buy_params[f'buy-int-{i}']
            REAL = self.buy_params[f'buy-real-{i}']
            DFIND = dataframe[IND]
            DFCRS = dataframe[CRS]

            if OPR == ">":
                conditions.append(DFIND > DFCRS)
            elif OPR == "=":
                conditions.append(np.isclose(DFIND, DFCRS))
            elif OPR == "<":
                conditions.append(DFIND < DFCRS)
            elif OPR == "CA":
                conditions.append(qtpylib.crossed_above(DFIND, DFCRS))
            elif OPR == "CB":
                conditions.append(qtpylib.crossed_below(DFIND, DFCRS))
            elif OPR == ">I":
                conditions.append(DFIND > INT)
            elif OPR == "=I":
                conditions.append(DFIND == INT)
            elif OPR == "<I":
                conditions.append(DFIND < INT)
            elif OPR == ">R":
                conditions.append(DFIND > REAL)
            elif OPR == "=R":
                conditions.append(np.isclose(DFIND, REAL))
            elif OPR == "<R":
                conditions.append(DFIND < REAL)

        if self.Buy_DNA_Size > 0:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = list()
        for i in range(self.Sell_DNA_Size):
            OPR = self.sell_params[f'sell-oper-{i}']
            IND = self.sell_params[f'sell-indicator-{i}']
            CRS = self.sell_params[f'sell-cross-{i}']
            INT = self.sell_params[f'sell-int-{i}']
            REAL = self.sell_params[f'sell-real-{i}']
            DFIND = dataframe[IND]
            DFCRS = dataframe[CRS]

            if OPR == ">":
                conditions.append(DFIND > DFCRS)
            elif OPR == "=":
                conditions.append(np.isclose(DFIND, DFCRS))
            elif OPR == "<":
                conditions.append(DFIND < DFCRS)
            elif OPR == "CA":
                conditions.append(qtpylib.crossed_above(DFIND, DFCRS))
            elif OPR == "CB":
                conditions.append(qtpylib.crossed_below(DFIND, DFCRS))
            elif OPR == ">I":
                conditions.append(DFIND > INT)
            elif OPR == "=I":
                conditions.append(DFIND == INT)
            elif OPR == "<I":
                conditions.append(DFIND < INT)
            elif OPR == ">R":
                conditions.append(DFIND > REAL)
            elif OPR == "=R":
                conditions.append(np.isclose(DFIND, REAL))
            elif OPR == "<R":
                conditions.append(DFIND < REAL)

        if self.Sell_DNA_Size > 0:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe
