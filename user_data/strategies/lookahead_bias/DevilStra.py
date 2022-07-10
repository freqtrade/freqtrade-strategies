# DevilStra Strategy
# 𝔇𝔢𝔳𝔦𝔩 𝔦𝔰 𝔞𝔩𝔴𝔞𝔶𝔰 𝔰𝔱𝔯𝔬𝔫𝔤𝔢𝔯 𝔱𝔥𝔞𝔫 𝔊𝔬𝔡.
# 𝔅𝔲𝔱 𝔱𝔥𝔢 𝔬𝔫𝔩𝔶 𝔬𝔫𝔢 𝔴𝔥𝔬 𝔥𝔞𝔰 𝔱𝔥𝔢 𝔞𝔟𝔦𝔩𝔦𝔱𝔶
# 𝔗𝔬 𝔠𝔯𝔢𝔞𝔱𝔢 𝔫𝔢𝔴 𝔠𝔯𝔢𝔞𝔱𝔲𝔯𝔢𝔰 𝔦𝔰 𝔊𝔬𝔡.
# 𝔄𝔫𝔡 𝔱𝔥𝔢 𝔇𝔢𝔳𝔦𝔩 𝔪𝔞𝔨𝔢𝔰 𝔭𝔬𝔴𝔢𝔯𝔣𝔲𝔩 𝔰𝔭𝔢𝔩𝔩𝔰
# 𝔉𝔯𝔬𝔪 𝔱𝔥𝔦𝔰 𝔰𝔪𝔞𝔩𝔩 𝔠𝔯𝔢𝔞𝔱𝔲𝔯𝔢𝔰 (𝔩𝔦𝔨𝔢 𝔣𝔯𝔬𝔤𝔰, 𝔢𝔱𝔠.)
# 𝔚𝔦𝔱𝔥 𝔣𝔯𝔞𝔤𝔪𝔢𝔫𝔱𝔞𝔱𝔦𝔬𝔫 𝔞𝔫𝔡 𝔪𝔦𝔵𝔦𝔫𝔤 𝔱𝔥𝔢𝔪.
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# * IMPORTANT: You Need An "STATIC" Pairlist On Your Config.json !
# * IMPORTANT: First set PAIR_LIST_LENGHT={pair_whitelist size}
# * And re-hyperopt the Sell strategy And paste result in exact
# * place(lines 535~564)

# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell -s 𝕯𝖊𝖛𝖎𝖑𝕾𝖙𝖗𝖆

# --- Do not remove these libs ---
import numpy as np
from functools import reduce
import freqtrade.vendor.qtpylib.indicators as qtpylib
import talib.abstract as ta
import random
from freqtrade.strategy import CategoricalParameter, IStrategy

from numpy.lib import math
from pandas import DataFrame

# ########################## SETTINGS ##############################
# pairlist lenght(use exact count of pairs you used in whitelist size+1):
PAIR_LIST_LENGHT = 269
# you can find exact value of this inside GodStraNew
TREND_CHECK_CANDLES = 4
# Set the pain range of devil(2~9999)
PAIN_RANGE = 1000
# Add "GodStraNew" Generated Results As spells inside SPELLS.
# Set them unic phonemes like 'Zi' 'Gu' or 'Lu'!
# * Use below replacement on GodStraNew results to
# * Change God Generated Creatures to Spells:
# +-----------------------------+----------------------+
# | GodStraNew Hyperopt Results |   DevilStra Spells   |
# +-----------------------------+----------------------+
# |                             | "phonem" : {         |
# |    buy_params =  {          |    "buy_params" : {  |
# |      ...                    |      ...             |
# |    }                        |    },                |
# |    sell_params = {          |    "sell_params" : { |
# |      ...                    |      ...             |
# |    }                        |    }                 |
# |                             | },                   |
# +-----------------------------+----------------------+
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
    "La": {
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
# ######################## END SETTINGS ############################


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
    dataframe[crossed_indicator] = gene_calculator(
        dataframe, crossed_indicator)

    indicator_trend_sma = f"{indicator}-SMA-{TREND_CHECK_CANDLES}"
    if operator in ["UT", "DT", "OT", "CUT", "CDT", "COT"]:
        dataframe[indicator_trend_sma] = gene_calculator(
            dataframe, indicator_trend_sma)

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
            (qtpylib.crossed_above(
                dataframe[indicator], dataframe[crossed_indicator]))
        )
    elif operator == "CA":
        condition = (
            qtpylib.crossed_above(
                dataframe[indicator], dataframe[crossed_indicator])
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
            np.isclose(dataframe[indicator].div(
                dataframe[crossed_indicator]), real_num)
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
    # #################### RESULT PASTE PLACE ####################
    # 16/16:    108 trades. 75/18/15 Wins/Draws/Losses. Avg profit   7.77%. Median profit   8.89%. Total profit  0.08404983 BTC (  84.05Σ%). Avg duration 3 days, 6:49:00 min. Objective: -11.22849

    INTERFACE_VERSION: int = 3
    # Buy hyperspace params:
    buy_params = {
        "buy_spell": "Zi,Lu,Ra,Ra,La,Si,Pa,Si,Cu,La,De,Lu,De,La,Zi,Zi,Zi,Zi,Zi,Lu,Lu,Lu,Si,La,Ra,Pa,La,Zi,Zi,Gu,Ra,De,Gu,Zi,Ra,Ra,Ra,Cu,Pa,De,De,La,Lu,Lu,Lu,La,Zi,Cu,Ra,Gu,Pa,La,Zi,Zi,Si,Lu,Ra,Cu,Cu,Pa,Si,Gu,De,De,Lu,Gu,Zi,Pa,Lu,Pa,Ra,Gu,Cu,La,Pa,Lu,Zi,La,Zi,Gu,Zi,De,Cu,Ra,Lu,Ra,Gu,Si,Ra,La,La,Lu,Gu,Zi,Si,La,Pa,Pa,Cu,Cu,Zi,Gu,Pa,Zi,Pa,Cu,Lu,Pa,Si,De,Gu,Lu,Lu,Cu,Ra,Si,Pa,Gu,Si,Cu,Pa,Zi,Pa,Zi,Gu,Lu,Ra,Pa,Ra,De,Ra,Pa,Zi,La,Pa,De,Pa,Cu,Gu,De,Lu,La,Ra,Zi,Si,Zi,Zi,Cu,Cu,De,Pa,Pa,Zi,De,Ra,La,Lu,De,Lu,Gu,Cu,Cu,La,De,Gu,Lu,Ra,Pa,Lu,Cu,Pa,Pa,De,Si,Zi,Cu,De,De,De,Lu,Si,Zi,Gu,Si,Si,Ra,Pa,Si,La,La,Lu,Lu,De,Gu,Gu,Zi,Ra,La,Lu,Lu,La,Si,Zi,Si,Zi,Si,Lu,Cu,Zi,Lu,De,La,Ra,Ra,Lu,De,Pa,Zi,Gu,Cu,Zi,Pa,De,Si,Lu,De,Cu,De,Zi,Ra,Gu,De,Si,Lu,Lu,Ra,De,Gu,Cu,Gu,La,De,Lu,Lu,Si,Cu,Lu,Zi,Lu,Cu,Gu,Lu,Lu,Ra,Si,Ra,Pa,Lu,De,Ra,Zi,Gu,Gu,Zi,Lu,Cu,Cu,Cu,Lu",
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_spell": "La,Pa,De,De,La,Si,Si,La,La,La,Si,Pa,Pa,Lu,De,Cu,Cu,Gu,Lu,Ra,Lu,Si,Ra,De,La,Cu,La,La,Gu,La,De,Ra,Ra,Ra,Gu,Lu,Si,Si,Zi,Zi,La,Pa,Pa,Zi,Cu,Gu,Gu,Pa,Gu,Cu,Si,Ra,Ra,La,Gu,De,Si,La,Ra,Pa,Si,Lu,Pa,De,Zi,De,Lu,Si,Gu,De,Lu,De,Ra,Ra,Zi,De,Cu,Zi,Gu,Pa,Ra,De,Pa,De,Pa,Ra,Si,Si,Zi,Cu,Lu,Zi,Ra,De,Ra,Zi,Zi,Pa,Lu,Zi,Cu,Pa,Gu,Pa,Cu,De,Zi,De,De,Pa,Pa,Zi,Lu,Ra,Pa,Ra,Lu,Zi,Gu,Zi,Si,Lu,Ra,Ra,Zi,Lu,Pa,Lu,Si,Pa,Pa,Pa,Si,Zi,La,La,Lu,De,Zi,Gu,Ra,Ra,Ra,Zi,Pa,Zi,Cu,Lu,Gu,Cu,De,Lu,Gu,Lu,Gu,Si,Pa,Pa,Si,La,Gu,Ra,Pa,Si,Si,Si,Cu,Cu,Cu,Si,De,Lu,Gu,Gu,Lu,De,Ra,Gu,Gu,Gu,Cu,La,De,Cu,Zi,Pa,Si,De,Pa,Pa,Pa,La,De,Gu,Zi,La,De,Cu,La,Pa,Ra,Si,Si,Zi,Cu,Ra,Pa,Gu,Pa,Ra,Zi,De,Zi,Gu,Gu,Pa,Cu,Lu,Gu,De,Si,Pa,La,Cu,Zi,Gu,De,Gu,La,Cu,Gu,De,Cu,Cu,Gu,Ra,Lu,Zi,De,La,Ra,Pa,Pa,Si,La,Lu,La,De,De,Ra,De,La,La,Pa,Cu,Lu,Pa,Ra,Pa,Pa,Cu,Zi,Gu,Cu,Gu,La,Si,Ra,Pa",
    }

    # ROI table:
    minimal_roi = {
        "0": 0.574,
        "1757": 0.158,
        "3804": 0.089,
        "6585": 0
    }

    # Stoploss:
    stoploss = -0.28
    # #################### END OF RESULT PLACE ####################

    # 𝖂𝖔𝖗𝖘𝖙, 𝖀𝖓𝖎𝖉𝖊𝖆𝖑, 𝕾𝖚𝖇𝖔𝖕𝖙𝖎𝖒𝖆𝖑, 𝕸𝖆𝖑𝖆𝖕𝖗𝖔𝖕𝖔𝖘 𝕬𝖓𝖉 𝕯𝖎𝖘𝖒𝖆𝖑 𝖙𝖎𝖒𝖊𝖋𝖗𝖆𝖒𝖊 𝖋𝖔𝖗 𝖙𝖍𝖎𝖘 𝖘𝖙𝖗𝖆𝖙𝖊𝖌𝖞:
    timeframe = '4h'

    spell_pot = [
        ",".join(
            tuple(
                random.choices(
                    list(SPELLS.keys()),
                    # TODO: k will be change to len(pairlist)
                    k=PAIR_LIST_LENGHT
                )
            )
        )for i in range(PAIN_RANGE)
    ]

    buy_spell = CategoricalParameter(
        spell_pot, default=spell_pot[0], space='buy')
    sell_spell = CategoricalParameter(
        spell_pot, default=spell_pot[0], space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        pairs = self.dp.current_whitelist()
        pairs_len = len(pairs)
        pair_index = pairs.index(metadata['pair'])

        buy_spells = self.buy_spell.value.split(",")
        buy_spells_len = len(buy_spells)

        if pairs_len > buy_spells_len:
            print(
                f"First set PAIR_LIST_LENGHT={pairs_len + 1} And re-hyperopt the")
            print("Buy strategy And paste result in exact place(lines 535~564)")
            print("IMPORTANT: You Need An 'STATIC' Pairlist On Your Config.json !!!")
            exit()

        buy_params_index = buy_spells[pair_index]

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
                'enter_long']=1

        # print(len(dataframe.keys()))

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        pairs = self.dp.current_whitelist()
        pairs_len = len(pairs)
        pair_index = pairs.index(metadata['pair'])

        sell_spells = self.sell_spell.value.split(",")
        sell_spells_len = len(sell_spells)

        if pairs_len > sell_spells_len:
            print(
                f"First set PAIR_LIST_LENGHT={pairs_len + 1} And re-hyperopt the")
            print("Sell strategy And paste result in exact place(lines 535~564)")
            print("IMPORTANT: You Need An 'STATIC' Pairlist On Your Config.json !!!")
            exit()

        sell_params_index = sell_spells[pair_index]

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
                'exit_long']=1
        return dataframe
