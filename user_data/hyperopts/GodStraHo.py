# GodStra Strategy Hyperopt
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: Hyperopt without stoploss space to find the best strategy.
# freqtrade hyperopt --hyperopt GodStraHo --hyperopt-loss SharpeHyperOptLossDaily --spaces buy sell roi trailing --strategy GodStra --config config.json -e 100

# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa

from freqtrade.optimize.hyperopt_interface import IHyperOpt

# --------------------------------
import freqtrade.vendor.qtpylib.indicators as qtpylib
from random import randint
# this is your trading strategy DNA Size
# you can change it and see the results...
DNA_SIZE = 1
SELL_DNA_SIZE = 1
tplist = [5, 10, 50, 100]
GodGeneIndicators = [
    'ACOS', 'AD', 'ADD', 'ADOSC', 'ADX', 'ADXR', 'APO',
    'AROON0', 'AROON1', 'AROONOSC', 'ASIN', 'ATAN', 'ATR', 'AVGPRICE',
    'BBANDS0', 'BBANDS1', 'BBANDS2', 'BETA',
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
    'HT_PHASOR0', 'HT_PHASOR1', 'HT_SINE0', 'HT_SINE1', 'HT_TRENDLINE',
    'HT_TRENDMODE', 'KAMA', 'LINEARREG', 'LINEARREG_ANGLE', 'LINEARREG_INTERCEPT',
    'LINEARREG_SLOPE', 'LN', 'LOG10', 'MA',
    'MACD0', 'MACD1', 'MACD2', 'MACDEXT0', 'MACDEXT1', 'MACDEXT2',
    'MACDFIX0', 'MACDFIX1', 'MACDFIX2', 'MAMA0', 'MAMA1',
    'MAX', 'MAXINDEX', 'MEDPRICE', 'MFI', 'MIDPOINT', 'MIDPRICE',
    'MIN', 'MININDEX', 'MINMAX0', 'MINMAX1', 'MINMAXINDEX0', 'MINMAXINDEX1',
    'MINUS_DI', 'MINUS_DM', 'MOM',
    'MULT', 'NATR', 'OBV', 'PLUS_DI', 'PLUS_DM', 'PPO', 'ROC', 'ROCP', 'ROCR',
    'ROCR100', 'RSI', 'SAR', 'SAREXT', 'SIN', 'SINH', 'SMA', 'SQRT', 'STDDEV',
    'STOCH0', 'STOCH1', 'STOCHF0', 'STOCHF1', 'STOCHRSI0', 'STOCHRSI1',
    'SUB', 'SUM', 'T3', 'TAN', 'TANH', 'TEMA',
    'TRANGE', 'TRIMA', 'TRIX', 'TSF', 'TYPPRICE', 'ULTOSC', 'VAR', 'WCLPRICE',
    'WILLR', 'WMA'
]


GodGenes = list()

for gene in GodGeneIndicators:
    for tp in tplist:
        GodGenes.append(f'{gene}-{tp}')

# GodGenes.extend(['open', 'high', 'low', 'close', 'volume'])


class GodStraHo(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        gene = list()

        for i in range(DNA_SIZE):
            gene.append(Categorical(GodGenes, name=f'buy-indicator-{i}'))
            gene.append(Categorical(GodGenes, name=f'buy-cross-{i}'))
            gene.append(Real(-1, 1, name=f'buy-real-{i}'))
            # Operations
            # CA: Crossed Above, CB: Crossed Below,
            # R: Real, D: Disabled
            gene.append(Categorical([
                "D",
                ">",
                "<",
                "=",
                "CA",
                "CB",
                ">R",
                "=R",
                "<R",
            ], name=f'buy-oper-{i}'))
        return gene

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by Hyperopt.
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use.
            """
            conditions = []
            # GUARDS AND TRENDS
            for i in range(DNA_SIZE):

                OPR = params[f'buy-oper-{i}']
                IND = params[f'buy-indicator-{i}']
                CRS = params[f'buy-cross-{i}']
                REAL = params[f'buy-real-{i}']
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

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @ staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        gene = list()

        for i in range(SELL_DNA_SIZE):
            gene.append(Categorical(GodGenes, name=f'sell-indicator-{i}'))
            gene.append(Categorical(GodGenes, name=f'sell-cross-{i}'))
            gene.append(Real(-1, 1, name=f'sell-real-{i}'))
            # Operations
            # CA: Crossed Above, CB: Crossed Below,
            # R: Real, D: Disabled
            gene.append(Categorical(["D", ">", "<", "=", "CA", "CB",
                                     ">R", "=R", "<R"], name=f'sell-oper-{i}'))
        return gene

    @ staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Sell strategy Hyperopt will build and use.
            """
            conditions = []

            # GUARDS AND TRENDS
            for i in range(SELL_DNA_SIZE):

                OPR = params[f'sell-oper-{i}']
                IND = params[f'sell-indicator-{i}']
                CRS = params[f'sell-cross-{i}']
                REAL = params[f'sell-real-{i}']
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

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell']=1

            return dataframe

        return populate_sell_trend
