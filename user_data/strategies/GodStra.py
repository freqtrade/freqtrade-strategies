# GodStra Strategy
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
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
# TODO: Will use new normalization methods to reduce noisy data and increase comparing quality
# from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()

# This will be same as tplist in GodStraHo.py
tplist = [7, 14]

#  TODO: this gene is removed 'MAVP' cuz or error on periods
GodGeneIndicators = [
    'ACOS', 'AD', 'ADD', 'ADOSC', 'ADX', 'ADXR', 'APO',
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
    # 'MAVP',
    'MAMA', 'MAX', 'MAXINDEX', 'MEDPRICE', 'MFI', 'MIDPOINT', 'MIDPRICE',
    'MIN', 'MININDEX', 'MINMAX', 'MINMAXINDEX', 'MINUS_DI', 'MINUS_DM', 'MOM',
    'MULT', 'NATR', 'OBV', 'PLUS_DI', 'PLUS_DM', 'PPO', 'ROC', 'ROCP', 'ROCR',
    'ROCR100', 'RSI', 'SAR', 'SAREXT', 'SIN', 'SINH', 'SMA', 'SQRT', 'STDDEV',
    'STOCH', 'STOCHF', 'STOCHRSI', 'SUB', 'SUM', 'T3', 'TAN', 'TANH', 'TEMA',
    'TRANGE', 'TRIMA', 'TRIX', 'TSF', 'TYPPRICE', 'ULTOSC', 'VAR', 'WCLPRICE',
    'WILLR', 'WMA'
]

# This will be same as tplist in GodStraHo.py
# If you need aroon just add here ['AROON0', 'AROON1'] in GodStraHo,
# And add just ['AROON'] in GodStra.py
# Cuz some indicators returns more than one number in ta-lib.
# Examples:
# GodGeneIndicators = ['RSI', 'MFI', 'AROON', 'SMA']
# GodGeneIndicators = ['BBANDS']
# GodGeneIndicators = ['FLOOR']


class GodStra(IStrategy):
    # *   29/5000:     56 trades. 35/3/18 Wins/Draws/Losses. Avg profit   4.39%. Median profit   3.86%. Total profit  11.07139661 BNB ( 245.89Σ%). Avg duration 2010.0 min. Objective: -13.44284

    # Buy hyperspace params:
    buy_params = {
        'buy-cross-0': 'BBANDS1-7',
        'buy-cross-1': 'BBANDS1-14',
        'buy-indicator-0': 'BBANDS0-7',
        'buy-indicator-1': 'BBANDS0-14',
        'buy-oper-0': 'CA',
        'buy-oper-1': '>',
        'buy-real-0': 0.42666,
        'buy-real-1': 1.08515
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-cross-0': 'BBANDS1-7',
        'sell-cross-1': 'BBANDS2-7',
        'sell-indicator-0': 'BBANDS2-14',
        'sell-indicator-1': 'BBANDS2-7',
        'sell-oper-0': 'CA',
        'sell-oper-1': '=',
        'sell-real-0': 1.0595,
        'sell-real-1': 0.48984
    }

    # ROI table:
    minimal_roi = {
        "0": 0.34719,
        "676": 0.11262,
        "1497": 0.03862,
        "4706": 0
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.13352
    trailing_stop_positive_offset = 0.18623
    trailing_only_offset_is_reached = True
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
            condition = True

            # enable this line if you are not in hyperopt, for ultra Speedup the algorythm.
            # condition = gene in str(self.buy_params.values())+str(self.sell_params.values())
            if condition:
                for tp in tplist:
                    # print(gene)
                    res = getattr(ta, gene)(
                        dataframe,
                        timeperiod=tp,
                    )
                    # TODO: fix MAVP error
                    if type(res) == pd.core.series.Series and gene != 'MAVP':
                        # print(gene)
                        dataframe[f'{gene}-{tp}'] = (res-res.min())/(res.max()-res.min())
                        # TODO: use other normalisation methods to reduce noisy data
                        # scaler.fit_transform(
                        #     res.replace(
                        #         [np.inf, -np.inf], np.zeros, inplace=True
                        #     ).values.reshape(0, 1)
                        # )

                    else:
                        for idx in range(len(res.keys())):
                            ress = res.iloc[:, idx]
                            dataframe[f'{gene}{idx}-{tp}'] = \
                                (ress - ress.min())/(ress.max()-ress.min())
                            # scaler.fit_transform(
                            #     res.iloc[:, idx].replace(
                            #         [np.inf, -np.inf], np.zeros, inplace=True
                            #     ).values.reshape(0, 1)
                            # )
        print(metadata['pair'])
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = list()
        for i in range(self.Buy_DNA_Size):

            OPR = self.buy_params[f'buy-oper-{i}']
            IND = self.buy_params[f'buy-indicator-{i}']
            CRS = self.buy_params[f'buy-cross-{i}']
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
