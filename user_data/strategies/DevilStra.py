# DevilStra Strategy
# 𝔇𝔢𝔳𝔦𝔩 𝔦𝔰 𝔞𝔩𝔴𝔞𝔶𝔰 𝔰𝔱𝔯𝔬𝔫𝔤𝔢𝔯 𝔱𝔥𝔞𝔫 𝔊𝔬𝔡. 
# 𝔅𝔲𝔱 𝔱𝔥𝔢 𝔬𝔫𝔩𝔶 𝔬𝔫𝔢 𝔴𝔥𝔬 𝔥𝔞𝔰 𝔱𝔥𝔢 𝔞𝔟𝔦𝔩𝔦𝔱𝔶 
# 𝔱𝔬 𝔠𝔯𝔢𝔞𝔱𝔢 𝔫𝔢𝔴 𝔠𝔯𝔢𝔞𝔱𝔲𝔯𝔢𝔰 𝔦𝔰 𝔊𝔬𝔡.
# 𝔄𝔫𝔡 𝔱𝔥𝔢 𝔡𝔢𝔳𝔦𝔩 𝔪𝔞𝔨𝔢𝔰 𝔭𝔬𝔴𝔢𝔯𝔣𝔲𝔩 𝔰𝔭𝔢𝔩𝔩𝔰 
# 𝔣𝔯𝔬𝔪 𝔱𝔥𝔦𝔰 𝔰𝔪𝔞𝔩𝔩 𝔠𝔯𝔢𝔞𝔱𝔲𝔯𝔢𝔰 (𝔩𝔦𝔨𝔢 𝔣𝔯𝔬𝔤𝔰, 𝔢𝔱𝔠.) 
# 𝔱𝔬 𝔪𝔞𝔨𝔢 𝔥𝔦𝔰 𝔰𝔭𝔢𝔩𝔩𝔰 𝔴𝔦𝔱𝔥 𝔉𝔯𝔞𝔤𝔪𝔢𝔫𝔱𝔞𝔱𝔦𝔬𝔫 𝔞𝔫𝔡 𝔪𝔦𝔵𝔦𝔫𝔤 𝔱𝔥𝔢𝔪.
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell --strategy GodStraNew
# --- Do not remove these libs ---
import random
from freqtrade.strategy.hyper import CategoricalParameter, DecimalParameter, IntParameter

from numpy.lib import math
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# --------------------------------

# Add your lib to import here
# TODO: talib is fast but have not more indicators
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce
import numpy as np
#  TODO: this gene is removed 'MAVP' cuz or error on periods

########################### SETTINGS ##############################
# you can find exact value of is inside GodStra
TREND_CHECK_CANDLES = 4
# Set the pain range of devil(2~infinite)
PAIN_RANGE = 30000
# Add GodStra Generated Results As spells inside SPELLS.
# Set them unic phonemes like 'Zi' 'Gu' or 'Lu'!
# * Use below replacement on GodStra results to
# * Change God Generated Creatures to Spells:
# +--------------------------+----------------------+
# | GodStra Hyperopt Results |   DevilStra Spells   |
# +--------------------------+----------------------+
# |                          | "phonem" : {         |
# | buy_params =  {          |    "buy_params" : {  |
# |   ...                    |      ...             |
# | }                        |    },                |
# | sell_params = {          |    "sell_params" : { |
# |   ...                    |      ...             |
# | }                        |    }                 |
# |                          | },                   |
# +--------------------------+----------------------+
SPELLS = {
    "Zi": {
        "buy_params": {
            "buy_crossed_indicator0": "BOP-4",
            "buy_crossed_indicator1": "MACD-0-50",
            "buy_crossed_indicator2": "DEMA-52",
            "buy_indicator0": "MINUS_DI-50",
            "buy_indicator1": "HT_TRENDMODE-50",
            "buy_indicator2": "CORREL-128",
            "buy_operator0": "/>R",
            "buy_operator1": "CA",
            "buy_operator2": "CDT",
            "buy_real_num0": 0.1763,
            "buy_real_num1": 0.6891,
            "buy_real_num2": 0.0509,
        },
        "sell_params": {
            "sell_crossed_indicator0": "WCLPRICE-52",
            "sell_crossed_indicator1": "AROONOSC-15",
            "sell_crossed_indicator2": "CDLRISEFALL3METHODS-52",
            "sell_indicator0": "COS-50",
            "sell_indicator1": "CDLCLOSINGMARUBOZU-30",
            "sell_indicator2": "CDL2CROWS-130",
            "sell_operator0": "DT",
            "sell_operator1": ">R",
            "sell_operator2": "/>R",
            "sell_real_num0": 0.0678,
            "sell_real_num1": 0.8698,
            "sell_real_num2": 0.3917,
        }
    },
    "Gu": {
        "buy_params": {
            "buy_crossed_indicator0": "SMA-20",
            "buy_crossed_indicator1": "CDLLADDERBOTTOM-20",
            "buy_crossed_indicator2": "OBV-50",
            "buy_indicator0": "MAMA-1-50",
            "buy_indicator1": "SUM-40",
            "buy_indicator2": "VAR-30",
            "buy_operator0": "<R",
            "buy_operator1": "D",
            "buy_operator2": "D",
            "buy_real_num0": 0.2644,
            "buy_real_num1": 0.0736,
            "buy_real_num2": 0.8954,
        },
        "sell_params": {
            "sell_crossed_indicator0": "CDLLADDERBOTTOM-50",
            "sell_crossed_indicator1": "CDLHARAMICROSS-50",
            "sell_crossed_indicator2": "CDLDARKCLOUDCOVER-30",
            "sell_indicator0": "CDLLADDERBOTTOM-10",
            "sell_indicator1": "MAMA-1-40",
            "sell_indicator2": "OBV-30",
            "sell_operator0": "UT",
            "sell_operator1": ">R",
            "sell_operator2": "CUT",
            "sell_real_num0": 0.2707,
            "sell_real_num1": 0.7987,
            "sell_real_num2": 0.6891,
        }
    },
    "Lu": {
        "buy_params": {
            "buy_crossed_indicator0": "HT_SINE-0-28",
            "buy_crossed_indicator1": "ADD-130",
            "buy_crossed_indicator2": "ADD-12",
            "buy_indicator0": "ADD-28",
            "buy_indicator1": "AVGPRICE-15",
            "buy_indicator2": "AVGPRICE-12",
            "buy_operator0": "DT",
            "buy_operator1": "D",
            "buy_operator2": "C",
            "buy_real_num0": 0.3676,
            "buy_real_num1": 0.4284,
            "buy_real_num2": 0.372,
        },
        "sell_params": {
            "sell_crossed_indicator0": "HT_SINE-0-5",
            "sell_crossed_indicator1": "HT_SINE-0-4",
            "sell_crossed_indicator2": "HT_SINE-0-28",
            "sell_indicator0": "ADD-30",
            "sell_indicator1": "AVGPRICE-28",
            "sell_indicator2": "ADD-50",
            "sell_operator0": "CUT",
            "sell_operator1": "DT",
            "sell_operator2": "=R",
            "sell_real_num0": 0.3205,
            "sell_real_num1": 0.2055,
            "sell_real_num2": 0.8467,
        }
    },
    "A": {
        "buy_params": {
            "buy_crossed_indicator0": "WMA-14",
            "buy_crossed_indicator1": "MAMA-1-14",
            "buy_crossed_indicator2": "CDLHIKKAKE-14",
            "buy_indicator0": "T3-14",
            "buy_indicator1": "BETA-14",
            "buy_indicator2": "HT_PHASOR-1-14",
            "buy_operator0": "/>R",
            "buy_operator1": ">",
            "buy_operator2": ">R",
            "buy_real_num0": 0.0551,
            "buy_real_num1": 0.3469,
            "buy_real_num2": 0.3871,
        },
        "sell_params": {
            "sell_crossed_indicator0": "HT_TRENDLINE-14",
            "sell_crossed_indicator1": "LINEARREG-14",
            "sell_crossed_indicator2": "STOCHRSI-1-14",
            "sell_indicator0": "CDLDARKCLOUDCOVER-14",
            "sell_indicator1": "AD-14",
            "sell_indicator2": "CDLSTALLEDPATTERN-14",
            "sell_operator0": "/=R",
            "sell_operator1": "COT",
            "sell_operator2": "OT",
            "sell_real_num0": 0.3992,
            "sell_real_num1": 0.7747,
            "sell_real_num2": 0.7415,
        }
    },
    "Si": {
        "buy_params": {
            "buy_crossed_indicator0": "MACDEXT-2-14",
            "buy_crossed_indicator1": "CORREL-14",
            "buy_crossed_indicator2": "CMO-14",
            "buy_indicator0": "MA-14",
            "buy_indicator1": "ADXR-14",
            "buy_indicator2": "CDLMARUBOZU-14",
            "buy_operator0": "<",
            "buy_operator1": "/<R",
            "buy_operator2": "<R",
            "buy_real_num0": 0.7883,
            "buy_real_num1": 0.8286,
            "buy_real_num2": 0.6512,
        },
        "sell_params": {
            "sell_crossed_indicator0": "AROON-1-14",
            "sell_crossed_indicator1": "STOCHRSI-0-14",
            "sell_crossed_indicator2": "SMA-14",
            "sell_indicator0": "T3-14",
            "sell_indicator1": "AROONOSC-14",
            "sell_indicator2": "MIDPOINT-14",
            "sell_operator0": "C",
            "sell_operator1": "CA",
            "sell_operator2": "CB",
            "sell_real_num0": 0.372,
            "sell_real_num1": 0.5948,
            "sell_real_num2": 0.9872,
        }
    },
    "Pa": {
        "buy_params": {
            "buy_crossed_indicator0": "AROON-0-60",
            "buy_crossed_indicator1": "APO-60",
            "buy_crossed_indicator2": "BBANDS-0-60",
            "buy_indicator0": "WILLR-12",
            "buy_indicator1": "AD-15",
            "buy_indicator2": "MINUS_DI-12",
            "buy_operator0": "D",
            "buy_operator1": ">",
            "buy_operator2": "CA",
            "buy_real_num0": 0.2208,
            "buy_real_num1": 0.1371,
            "buy_real_num2": 0.6389,
        },
        "sell_params": {
            "sell_crossed_indicator0": "MACDEXT-0-15",
            "sell_crossed_indicator1": "BBANDS-2-15",
            "sell_crossed_indicator2": "DEMA-15",
            "sell_indicator0": "ULTOSC-15",
            "sell_indicator1": "MIDPOINT-12",
            "sell_indicator2": "PLUS_DI-12",
            "sell_operator0": "<",
            "sell_operator1": "DT",
            "sell_operator2": "COT",
            "sell_real_num0": 0.278,
            "sell_real_num1": 0.0643,
            "sell_real_num2": 0.7065,
        }
    },
    "De": {
        "buy_params": {
            "buy_crossed_indicator0": "HT_DCPERIOD-12",
            "buy_crossed_indicator1": "HT_PHASOR-0-12",
            "buy_crossed_indicator2": "MACDFIX-1-15",
            "buy_indicator0": "CMO-12",
            "buy_indicator1": "TRIMA-12",
            "buy_indicator2": "MACDEXT-0-15",
            "buy_operator0": "<",
            "buy_operator1": "D",
            "buy_operator2": "<",
            "buy_real_num0": 0.3924,
            "buy_real_num1": 0.5546,
            "buy_real_num2": 0.7648,
        },
        "sell_params": {
            "sell_crossed_indicator0": "MACDFIX-1-15",
            "sell_crossed_indicator1": "MACD-1-15",
            "sell_crossed_indicator2": "WMA-15",
            "sell_indicator0": "ROC-15",
            "sell_indicator1": "MACD-2-15",
            "sell_indicator2": "CCI-60",
            "sell_operator0": "CA",
            "sell_operator1": "<R",
            "sell_operator2": "/<R",
            "sell_real_num0": 0.4989,
            "sell_real_num1": 0.4131,
            "sell_real_num2": 0.8904,
        }
    },
    "Ra": {
        "buy_params": {
            "buy_crossed_indicator0": "EMA-110",
            "buy_crossed_indicator1": "SMA-5",
            "buy_crossed_indicator2": "SMA-6",
            "buy_indicator0": "SMA-6",
            "buy_indicator1": "EMA-12",
            "buy_indicator2": "EMA-5",
            "buy_operator0": "D",
            "buy_operator1": "<",
            "buy_operator2": "/<R",
            "buy_real_num0": 0.9814,
            "buy_real_num1": 0.5528,
            "buy_real_num2": 0.0541,
        },
        "sell_params": {
            "sell_crossed_indicator0": "SMA-50",
            "sell_crossed_indicator1": "EMA-12",
            "sell_crossed_indicator2": "SMA-100",
            "sell_indicator0": "EMA-110",
            "sell_indicator1": "EMA-50",
            "sell_indicator2": "EMA-15",
            "sell_operator0": "<",
            "sell_operator1": "COT",
            "sell_operator2": "/=R",
            "sell_real_num0": 0.3506,
            "sell_real_num1": 0.8767,
            "sell_real_num2": 0.0614,
        }
    },
    "Cu": {
        "buy_params": {
            "buy_crossed_indicator0": "SMA-110",
            "buy_crossed_indicator1": "SMA-110",
            "buy_crossed_indicator2": "SMA-5",
            "buy_indicator0": "SMA-110",
            "buy_indicator1": "SMA-55",
            "buy_indicator2": "SMA-15",
            "buy_operator0": "<R",
            "buy_operator1": "<",
            "buy_operator2": "CA",
            "buy_real_num0": 0.5,
            "buy_real_num1": 0.7,
            "buy_real_num2": 0.9,
        },
        "sell_params": {
            "sell_crossed_indicator0": "SMA-55",
            "sell_crossed_indicator1": "SMA-50",
            "sell_crossed_indicator2": "SMA-100",
            "sell_indicator0": "SMA-5",
            "sell_indicator1": "SMA-50",
            "sell_indicator2": "SMA-50",
            "sell_operator0": "/=R",
            "sell_operator1": "CUT",
            "sell_operator2": "DT",
            "sell_real_num0": 0.4,
            "sell_real_num1": 0.2,
            "sell_real_num2": 0.7,
        }
    }
}
######################### END SETTINGS ############################


def spell_finder(index, space):
    return SPELLS[index][space+"_params"]


def normalize(df):
    df = (df-df.min())/(df.max()-df.min())
    return df


def gene_calculator(dataframe, indicator):
    # Cuz Timeperiods not effect calculating CDL patterns recognations
    if 'CDL' in indicator:
        splited_indicator = indicator.split('-')
        splited_indicator[1] = "0"
        new_indicator = "-".join(splited_indicator)
        # print(indicator, new_indicator)
        indicator = new_indicator

    gene = indicator.split("-")

    gene_name = gene[0]
    gene_len = len(gene)

    if indicator in dataframe.keys():
        # print(f"{indicator}, calculated befoure")
        # print(len(dataframe.keys()))
        return dataframe[indicator]
    else:
        result = None
        # For Pattern Recognations
        if gene_len == 1:
            # print('gene_len == 1\t', indicator)
            result = getattr(ta, gene_name)(
                dataframe
            )
            return normalize(result)
        elif gene_len == 2:
            # print('gene_len == 2\t', indicator)
            gene_timeperiod = int(gene[1])
            result = getattr(ta, gene_name)(
                dataframe,
                timeperiod=gene_timeperiod,
            )
            return normalize(result)
        # For
        elif gene_len == 3:
            # print('gene_len == 3\t', indicator)
            gene_timeperiod = int(gene[2])
            gene_index = int(gene[1])
            result = getattr(ta, gene_name)(
                dataframe,
                timeperiod=gene_timeperiod,
            ).iloc[:, gene_index]
            return normalize(result)
        # For trend operators(MA-5-SMA-4)
        elif gene_len == 4:
            # print('gene_len == 4\t', indicator)
            gene_timeperiod = int(gene[1])
            sharp_indicator = f'{gene_name}-{gene_timeperiod}'
            dataframe[sharp_indicator] = getattr(ta, gene_name)(
                dataframe,
                timeperiod=gene_timeperiod,
            )
            return normalize(ta.SMA(dataframe[sharp_indicator].fillna(0), TREND_CHECK_CANDLES))
        # For trend operators(STOCH-0-4-SMA-4)
        elif gene_len == 5:
            # print('gene_len == 5\t', indicator)
            gene_timeperiod = int(gene[2])
            gene_index = int(gene[1])
            sharp_indicator = f'{gene_name}-{gene_index}-{gene_timeperiod}'
            dataframe[sharp_indicator] = getattr(ta, gene_name)(
                dataframe,
                timeperiod=gene_timeperiod,
            ).iloc[:, gene_index]
            return normalize(ta.SMA(dataframe[sharp_indicator].fillna(0), TREND_CHECK_CANDLES))


def condition_generator(dataframe, operator, indicator, crossed_indicator, real_num):

    condition = (dataframe['volume'] > 10)

    # TODO : it ill callculated in populate indicators.

    dataframe[indicator] = gene_calculator(dataframe, indicator)
    dataframe[crossed_indicator] = gene_calculator(dataframe, crossed_indicator)

    indicator_trend_sma = f"{indicator}-SMA-{TREND_CHECK_CANDLES}"
    if operator in ["UT", "DT", "OT", "CUT", "CDT", "COT"]:
        dataframe[indicator_trend_sma] = gene_calculator(dataframe, indicator_trend_sma)

    if operator == ">":
        condition = (
            dataframe[indicator] > dataframe[crossed_indicator]
        )
    elif operator == "=":
        condition = (
            np.isclose(dataframe[indicator], dataframe[crossed_indicator])
        )
    elif operator == "<":
        condition = (
            dataframe[indicator] < dataframe[crossed_indicator]
        )
    elif operator == "C":
        condition = (
            (qtpylib.crossed_below(dataframe[indicator], dataframe[crossed_indicator])) |
            (qtpylib.crossed_above(dataframe[indicator], dataframe[crossed_indicator]))
        )
    elif operator == "CA":
        condition = (
            qtpylib.crossed_above(dataframe[indicator], dataframe[crossed_indicator])
        )
    elif operator == "CB":
        condition = (
            qtpylib.crossed_below(
                dataframe[indicator], dataframe[crossed_indicator])
        )
    elif operator == ">R":
        condition = (
            dataframe[indicator] > real_num
        )
    elif operator == "=R":
        condition = (
            np.isclose(dataframe[indicator], real_num)
        )
    elif operator == "<R":
        condition = (
            dataframe[indicator] < real_num
        )
    elif operator == "/>R":
        condition = (
            dataframe[indicator].div(dataframe[crossed_indicator]) > real_num
        )
    elif operator == "/=R":
        condition = (
            np.isclose(dataframe[indicator].div(dataframe[crossed_indicator]), real_num)
        )
    elif operator == "/<R":
        condition = (
            dataframe[indicator].div(dataframe[crossed_indicator]) < real_num
        )
    elif operator == "UT":
        condition = (
            dataframe[indicator] > dataframe[indicator_trend_sma]
        )
    elif operator == "DT":
        condition = (
            dataframe[indicator] < dataframe[indicator_trend_sma]
        )
    elif operator == "OT":
        condition = (

            np.isclose(dataframe[indicator], dataframe[indicator_trend_sma])
        )
    elif operator == "CUT":
        condition = (
            (
                qtpylib.crossed_above(
                    dataframe[indicator],
                    dataframe[indicator_trend_sma]
                )
            ) &
            (
                dataframe[indicator] > dataframe[indicator_trend_sma]
            )
        )
    elif operator == "CDT":
        condition = (
            (
                qtpylib.crossed_below(
                    dataframe[indicator],
                    dataframe[indicator_trend_sma]
                )
            ) &
            (
                dataframe[indicator] < dataframe[indicator_trend_sma]
            )
        )
    elif operator == "COT":
        condition = (
            (
                (
                    qtpylib.crossed_below(
                        dataframe[indicator],
                        dataframe[indicator_trend_sma]
                    )
                ) |
                (
                    qtpylib.crossed_above(
                        dataframe[indicator],
                        dataframe[indicator_trend_sma]
                    )
                )
            ) &
            (
                np.isclose(
                    dataframe[indicator],
                    dataframe[indicator_trend_sma]
                )
            )
        )

    return condition, dataframe


class DevilStra(IStrategy):
    # #################### RESULTS PASTE PLACE ####################
    # * 11/1000:    123 trades. 80/0/43 Wins/Draws/Losses. Avg profit  18.06%. Median profit   7.08%. Total profit  0.02199610 BTC (  22.00Σ%). Avg duration 22 days, 18:28:00 min. Objective: -36.39438

    # Buy hyperspace params:
    buy_params = {
        "buy_spell": ('Lu', 'Lu', 'Si', 'Pa', 'Zi', 'Si', 'Gu', 'Zi', 'Si', 'Gu', 'Ra', 'Lu', 'Gu', 'A', 'Pa', 'A', 'Zi', 'De', 'Cu', 'Gu', 'Cu', 'Ra', 'Cu', 'Pa', 'Lu', 'Gu', 'Cu', 'Zi', 'Si', 'Zi', 'Cu', 'A', 'Ra', 'De', 'Si', 'Zi', 'A', 'Ra', 'Gu', 'De', 'De', 'Lu', 'Si', 'Gu', 'Gu', 'Pa', 'De', 'Lu', 'Si', 'Zi', 'Pa', 'Si', 'Gu', 'Zi', 'De', 'Cu', 'Gu', 'Si', 'Pa', 'Pa', 'Si', 'A', 'Zi', 'De', 'Ra', 'Si', 'Gu', 'Si', 'De', 'Gu', 'Pa', 'De', 'A', 'Si', 'De', 'Pa', 'Ra', 'Zi', 'De', 'Pa', 'Zi', 'Ra', 'A', 'Cu', 'Pa', 'Pa', 'Lu', 'Pa', 'De', 'Gu', 'Gu', 'Ra', 'Lu', 'De', 'Cu', 'Ra', 'Zi', 'Si', 'Ra', 'Lu', 'De', 'A', 'Zi', 'Cu', 'Gu', 'Pa', 'De', 'Ra', 'Pa', 'Pa', 'A', 'Si', 'Ra', 'Cu', 'De', 'Gu', 'Si', 'Gu', 'Zi', 'Cu', 'A', 'Lu', 'Lu', 'A', 'Si', 'Pa', 'Zi', 'Zi', 'Cu', 'Ra', 'Lu', 'Ra', 'De', 'De', 'A', 'Si', 'Pa', 'De', 'Lu', 'Pa', 'De', 'Ra', 'Ra', 'Pa', 'Pa', 'Gu', 'Gu', 'Ra', 'Gu', 'Ra', 'Pa', 'Lu', 'A', 'Zi', 'Gu', 'Lu', 'Lu', 'Zi', 'Gu', 'A', 'Ra', 'Gu', 'Zi', 'Si', 'A', 'Cu', 'Pa', 'De', 'Lu', 'Cu', 'A', 'Zi', 'A', 'Lu', 'Lu', 'Gu', 'Pa', 'Gu', 'A', 'Gu', 'Gu', 'Cu', 'Si', 'Lu', 'Zi', 'De', 'Gu', 'Zi', 'Si', 'Ra', 'De', 'Pa', 'Gu', 'Gu', 'Zi', 'Lu', 'Zi', 'Lu', 'Si', 'Zi', 'Gu', 'Si', 'Ra', 'Lu', 'Pa', 'A', 'A', 'Lu', 'Pa', 'De', 'De', 'Cu', 'Ra', 'Lu', 'De', 'Si', 'Cu', 'Si', 'Si', 'Zi', 'De', 'Si', 'Si', 'Cu', 'Gu', 'Si', 'Ra', 'Si', 'Cu', 'A', 'Zi', 'De', 'Gu', 'Pa', 'Lu', 'Cu', 'Cu', 'Pa', 'Cu', 'A', 'Si', 'Zi', 'Cu', 'Zi', 'Ra', 'Si', 'Lu', 'Lu', 'De', 'Cu', 'Cu', 'Lu', 'Pa', 'Ra', 'Cu', 'Lu', 'Ra', 'Zi', 'Gu', 'Ra', 'Cu', 'A', 'De', 'Cu', 'Ra', 'Ra', 'De', 'Zi', 'De', 'De', 'A', 'Pa', 'A', 'Gu', 'Lu', 'De', 'De', 'A', 'Pa', 'Gu', 'Gu', 'De', 'Gu', 'Cu', 'Zi', 'Si', 'Gu', 'Ra', 'Pa', 'Gu', 'Lu', 'A', 'Lu', 'A', 'Si', 'Si', 'Pa', 'Ra', 'Cu', 'Lu'),
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_spell": ('A', 'Lu', 'Lu', 'Cu', 'De', 'Zi', 'Si', 'Lu', 'Cu', 'A', 'A', 'Pa', 'Si', 'Pa', 'Si', 'Zi', 'Si', 'Zi', 'Pa', 'Cu', 'Zi', 'A', 'De', 'Si', 'A', 'Gu', 'Gu', 'Pa', 'Lu', 'Ra', 'De', 'Gu', 'Pa', 'Gu', 'Ra', 'Gu', 'Gu', 'Zi', 'Lu', 'Gu', 'Ra', 'Si', 'Lu', 'Ra', 'Zi', 'De', 'Gu', 'Ra', 'Si', 'Ra', 'De', 'Si', 'Ra', 'Cu', 'Lu', 'Lu', 'Ra', 'Cu', 'A', 'De', 'Pa', 'Cu', 'Pa', 'Pa', 'A', 'Zi', 'Lu', 'Zi', 'Lu', 'Si', 'A', 'Lu', 'Zi', 'Pa', 'Gu', 'Ra', 'Zi', 'De', 'Cu', 'A', 'Si', 'Gu', 'De', 'Cu', 'De', 'Ra', 'Cu', 'Si', 'Gu', 'De', 'Cu', 'Pa', 'Si', 'Zi', 'Cu', 'Lu', 'Lu', 'Si', 'Cu', 'Zi', 'A', 'Pa', 'De', 'Zi', 'Si', 'Si', 'Cu', 'Pa', 'Zi', 'Si', 'Si', 'Lu', 'Pa', 'Lu', 'De', 'Si', 'Cu', 'Cu', 'Zi', 'Gu', 'Si', 'Ra', 'Pa', 'Gu', 'Gu', 'Lu', 'Pa', 'Cu', 'Zi', 'Pa', 'Si', 'Ra', 'A', 'Gu', 'Pa', 'A', 'A', 'A', 'A', 'Si', 'Cu', 'Gu', 'De', 'Pa', 'De', 'Cu', 'Zi', 'Pa', 'A', 'Cu', 'Zi', 'Gu', 'Gu', 'Lu', 'Zi', 'A', 'Gu', 'Pa', 'Lu', 'Si', 'Zi', 'A', 'A', 'Pa', 'Gu', 'Zi', 'De', 'Ra', 'De', 'Cu', 'Ra', 'Pa', 'Pa', 'Lu', 'Zi', 'Si', 'Gu', 'Zi', 'Ra', 'De', 'Cu', 'Zi', 'Cu', 'Gu', 'De', 'Lu', 'A', 'A', 'Si', 'De', 'Si', 'Zi', 'Gu', 'Si', 'Cu', 'Ra', 'Lu', 'Lu', 'De', 'Gu', 'Cu', 'Pa', 'Ra', 'Lu', 'Si', 'Ra', 'Gu', 'Cu', 'De', 'Si', 'Pa', 'Gu', 'Zi', 'Si', 'A', 'Cu', 'Lu', 'Si', 'Si', 'Zi', 'Si', 'Gu', 'A', 'Cu', 'A', 'Gu', 'A', 'Zi', 'Ra', 'Zi', 'Zi', 'Zi', 'Ra', 'Gu', 'De', 'Zi', 'Ra', 'Zi', 'A', 'De', 'De', 'Ra', 'A', 'Gu', 'De', 'Lu', 'Cu', 'Gu', 'Si', 'A', 'Cu', 'Lu', 'Cu', 'A', 'Zi', 'De', 'Gu', 'Si', 'Zi', 'Gu', 'Pa', 'Si', 'Gu', 'Lu', 'Cu', 'Gu', 'De', 'Cu', 'Cu', 'Ra', 'Gu', 'Pa', 'Cu', 'De', 'De', 'Zi', 'Pa', 'A', 'Cu', 'Zi', 'A', 'Zi', 'De', 'Lu', 'Cu', 'Cu', 'De', 'Cu', 'Ra', 'Ra', 'Zi', 'Si', 'Cu', 'Ra', 'De', 'Cu', 'Gu', 'Lu', 'Pa', 'Gu'),
    }
    # #################### END OF RESULT PLACE ####################
    spell_pot = [
        tuple(
            random.choices(
                list(SPELLS.keys()),
                # TODO: k will be change to len(pairlist)
                k=300
            )
        )for i in range(PAIN_RANGE)
    ]

    buy_spell = CategoricalParameter(spell_pot, default=spell_pot[0], space='buy')
    sell_spell = CategoricalParameter(spell_pot, default=spell_pot[0], space='sell')

    # Stoploss:
    stoploss = -0.1
    # Buy hypers
    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        pairs = self.dp.current_whitelist()
        pair_index = pairs.index(metadata['pair'])
        buy_params_index = self.buy_spell.value[pair_index]

        params = spell_finder(buy_params_index, 'buy')
        conditions = list()
        # TODO: Its not dry code!
        buy_indicator = params['buy_indicator0']
        buy_crossed_indicator = params['buy_crossed_indicator0']
        buy_operator = params['buy_operator0']
        buy_real_num = params['buy_real_num0']
        condition, dataframe = condition_generator(
            dataframe,
            buy_operator,
            buy_indicator,
            buy_crossed_indicator,
            buy_real_num
        )
        conditions.append(condition)
        # backup
        buy_indicator = params['buy_indicator1']
        buy_crossed_indicator = params['buy_crossed_indicator1']
        buy_operator = params['buy_operator1']
        buy_real_num = params['buy_real_num1']

        condition, dataframe = condition_generator(
            dataframe,
            buy_operator,
            buy_indicator,
            buy_crossed_indicator,
            buy_real_num
        )
        conditions.append(condition)

        buy_indicator = params['buy_indicator2']
        buy_crossed_indicator = params['buy_crossed_indicator2']
        buy_operator = params['buy_operator2']
        buy_real_num = params['buy_real_num2']
        condition, dataframe = condition_generator(
            dataframe,
            buy_operator,
            buy_indicator,
            buy_crossed_indicator,
            buy_real_num
        )
        conditions.append(condition)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        # print(len(dataframe.keys()))

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        pairs = self.dp.current_whitelist()
        pair_index = pairs.index(metadata['pair'])
        sell_params_index = self.sell_spell.value[pair_index]

        params = spell_finder(sell_params_index, 'sell')

        conditions = list()
        # TODO: Its not dry code!
        sell_indicator = params['sell_indicator0']
        sell_crossed_indicator = params['sell_crossed_indicator0']
        sell_operator = params['sell_operator0']
        sell_real_num = params['sell_real_num0']
        condition, dataframe = condition_generator(
            dataframe,
            sell_operator,
            sell_indicator,
            sell_crossed_indicator,
            sell_real_num
        )
        conditions.append(condition)

        sell_indicator = params['sell_indicator1']
        sell_crossed_indicator = params['sell_crossed_indicator1']
        sell_operator = params['sell_operator1']
        sell_real_num = params['sell_real_num1']
        condition, dataframe = condition_generator(
            dataframe,
            sell_operator,
            sell_indicator,
            sell_crossed_indicator,
            sell_real_num
        )
        conditions.append(condition)

        sell_indicator = params['sell_indicator2']
        sell_crossed_indicator = params['sell_crossed_indicator2']
        sell_operator = params['sell_operator2']
        sell_real_num = params['sell_real_num2']
        condition, dataframe = condition_generator(
            dataframe,
            sell_operator,
            sell_indicator,
            sell_crossed_indicator,
            sell_real_num
        )
        conditions.append(condition)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1
        return dataframe
