# Persia Strategy
# Iran also called Persia is home to one of the world's
# oldest civilizations,beginning with the formation of the
# Elamite kingdoms in the fourth millennium BC. "Cyrus the
# Great" founded the "Achaemenid" Empire, which became one of
# the largest empires in history and the world's first
# superpower. Iran In Last 50 years officially called the
# "Islamic Republic of Iran". And everything was changed!
# Now we need support of free peoples around the world. We
# don't want to change fully to somthig like North-Korea OR
# Afghanistan. I'll show what happen if you "RANDOMLY" born
# in Iran In two steps:
# 1) fully vaccinated people til 25Aug2021:
#   Total doses given	19,9M
#   People fully vaccinated	4,38M
#   % fully vaccinated	5,3 %
# 2) Hacktivists leak videos of abuse in Iran Evin prison (Hot News):
#   https://mega.nz/folder/1l5WxKRY#QK7QXPo1IaMvqQSROMZg6w
# Anyway ...................................................
# NOT IMPORTANT GUIDE:
#   Buy me a Coffee:
#       BTC: 1FvX1JbsmbK6BjcGnzTmUy5AvVgYHsgEpA
#       ETH(ERC20): 0x675c1a0753b49752f445a978cb75d106417f0547
#       DOGE: D6fVdhucaToyLUg3iCEjzP4g6mjbvibrTC
#       USDT(TRC20): THmmW5k65WRw8TP6w58TvG156LccAgDtL3
#       XRP: rDt7d2bf2CSKzTFug2etkhbr8yQjbZtLE7 TAG: 86584953
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy Persia
# --- Do not remove these libs ---
from typing import get_type_hints
from numpy.lib.function_base import append

from pandas.core.series import Series

from freqtrade.strategy.hyper import CategoricalParameter, IntParameter, DecimalParameter
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
# import freqtrade.vendor.qtpylib.indicators as qtpylib
from functools import reduce
import pandas as pd
import numpy as np
###################################### SETINGS ######################################

# INDICATORS
COSTUMEINDICATORSENABLED = True
COSTUMEINDICATORS = ['SMA', 'EMA', 'TEMA', 'DEMA']

# TIMEFRAMES
TIMEFRAMES = 10  # number of populated indicators
TFGAP = 3  # gap between each timeframe
COSTUMETFENABLED = True
COSTUMETF = [3, 7, 9, 21, 27, 63, 81, 189]

# REALS
REALSRANGE = [-2, 2]
DECIMALS = 1

# CONDITIONS
CONDITIONS = 3  # (max 100)

# FORMULAS
FORMULAS = [
    # '(A**2+B**2)>R**2',
    # '(A**2+B**2)<R**2',
    'A>B',
    'A<B',
    'A*R==B',
    'A==R',
    'A!=R',
    'A/B>R',
    'B/A>R',
    '0<=A<=1',
    '0<=B<=1',
    # 'A+R<B',
    # 'A-R>B',
    # '(R/(A+B))<A',
    # '(R/(A+B))<B',
    # '(R/(A+B))>A',
    # '(R/(A+B))>B',

    # 'A*(1+R)**2>5', # FV
    # 'A/(1+R)**2>5', # PV
    # '100-(100/(1+A/B))>70', # RSI
    # '100-(100/(1+A/B))<30', # RSI
]
#################################### END SETINGS ####################################


ta_funcs = ta.__TA_FUNCTION_NAMES__
ta_funcs.pop(107)
ta_funcs = [f for f in ta_funcs if not f.startswith('CDL')]
indicators = COSTUMEINDICATORS if COSTUMEINDICATORSENABLED else ta_funcs

tf_arr = np.arange(TIMEFRAMES)*TFGAP+TFGAP
# TODO: Not Costumized timeframes not work!
timeframes = COSTUMETF  # if COSTUMETFENABLED else np.delete(tf_arr,np.argwhere(tf_arr < 2))

reals = REALSRANGE

formulas = FORMULAS


class Persia(IStrategy):
    ###################### RESULT PLACE ######################
    buy_params = {
        "formula0": "A!=R",
        "formula1": "0<=B<=1",
        "formula2": "B/A>R",
        "indicator0": "TEMA",
        "indicator1": "DEMA",
        "indicator2": "DEMA",
        "timeframe0": 9,
        "timeframe1": 3,
        "timeframe2": 27,
        "crossed0": "TEMA",
        "crossed1": "EMA",
        "crossed2": "DEMA",
        "crossed_timeframe0": 81,
        "crossed_timeframe1": 27,
        "crossed_timeframe2": 63,
        "real0": 0.5,
        "real1": 1.8,
        "real2": -1.4,
    }
    sell_params = {
        "sell_formula0": "A==R",
        "sell_formula1": "B/A>R",
        "sell_formula2": "A!=R",
        "sell_indicator0": "EMA",
        "sell_indicator1": "DEMA",
        "sell_indicator2": "TEMA",
        "sell_timeframe0": 21,
        "sell_timeframe1": 21,
        "sell_timeframe2": 3,
        "sell_crossed0": "SMA",
        "sell_crossed1": "TEMA",
        "sell_crossed2": "EMA",
        "sell_crossed_timeframe0": 27,
        "sell_crossed_timeframe1": 27,
        "sell_crossed_timeframe2": 3,
        "sell_real0": 1.5,
        "sell_real1": 1.4,
        "sell_real2": 1.6,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.273,
        "26": 0.084,
        "79": 0.033,
        "187": 0
    }

    # Stoploss:
    stoploss = -0.19

    timeframe = '5m'
    # #################### END OF RESULT PLACE ####################

    ###############################################################
    # BUY HYPEROPTABLE PARAMS:
    formula0 = CategoricalParameter(
        formulas, default=formulas[0], optimize=0 < CONDITIONS, space='buy')
    formula1 = CategoricalParameter(
        formulas, default=formulas[0], optimize=1 < CONDITIONS, space='buy')
    formula2 = CategoricalParameter(
        formulas, default=formulas[0], optimize=2 < CONDITIONS, space='buy')
    formula3 = CategoricalParameter(
        formulas, default=formulas[0], optimize=3 < CONDITIONS, space='buy')
    formula4 = CategoricalParameter(
        formulas, default=formulas[0], optimize=4 < CONDITIONS, space='buy')
    formula5 = CategoricalParameter(
        formulas, default=formulas[0], optimize=5 < CONDITIONS, space='buy')
    formula6 = CategoricalParameter(
        formulas, default=formulas[0], optimize=6 < CONDITIONS, space='buy')
    formula7 = CategoricalParameter(
        formulas, default=formulas[0], optimize=7 < CONDITIONS, space='buy')
    formula8 = CategoricalParameter(
        formulas, default=formulas[0], optimize=8 < CONDITIONS, space='buy')
    formula9 = CategoricalParameter(
        formulas, default=formulas[0], optimize=9 < CONDITIONS, space='buy')
    formula10 = CategoricalParameter(
        formulas, default=formulas[0], optimize=10 < CONDITIONS, space='buy')
    formula11 = CategoricalParameter(
        formulas, default=formulas[0], optimize=11 < CONDITIONS, space='buy')
    formula12 = CategoricalParameter(
        formulas, default=formulas[0], optimize=12 < CONDITIONS, space='buy')
    formula13 = CategoricalParameter(
        formulas, default=formulas[0], optimize=13 < CONDITIONS, space='buy')
    formula14 = CategoricalParameter(
        formulas, default=formulas[0], optimize=14 < CONDITIONS, space='buy')
    formula15 = CategoricalParameter(
        formulas, default=formulas[0], optimize=15 < CONDITIONS, space='buy')
    formula16 = CategoricalParameter(
        formulas, default=formulas[0], optimize=16 < CONDITIONS, space='buy')
    formula17 = CategoricalParameter(
        formulas, default=formulas[0], optimize=17 < CONDITIONS, space='buy')
    formula18 = CategoricalParameter(
        formulas, default=formulas[0], optimize=18 < CONDITIONS, space='buy')
    formula19 = CategoricalParameter(
        formulas, default=formulas[0], optimize=19 < CONDITIONS, space='buy')
    formula20 = CategoricalParameter(
        formulas, default=formulas[0], optimize=20 < CONDITIONS, space='buy')
    formula21 = CategoricalParameter(
        formulas, default=formulas[0], optimize=21 < CONDITIONS, space='buy')
    formula22 = CategoricalParameter(
        formulas, default=formulas[0], optimize=22 < CONDITIONS, space='buy')
    formula23 = CategoricalParameter(
        formulas, default=formulas[0], optimize=23 < CONDITIONS, space='buy')
    formula24 = CategoricalParameter(
        formulas, default=formulas[0], optimize=24 < CONDITIONS, space='buy')
    formula25 = CategoricalParameter(
        formulas, default=formulas[0], optimize=25 < CONDITIONS, space='buy')
    formula26 = CategoricalParameter(
        formulas, default=formulas[0], optimize=26 < CONDITIONS, space='buy')
    formula27 = CategoricalParameter(
        formulas, default=formulas[0], optimize=27 < CONDITIONS, space='buy')
    formula28 = CategoricalParameter(
        formulas, default=formulas[0], optimize=28 < CONDITIONS, space='buy')
    formula29 = CategoricalParameter(
        formulas, default=formulas[0], optimize=29 < CONDITIONS, space='buy')
    formula30 = CategoricalParameter(
        formulas, default=formulas[0], optimize=30 < CONDITIONS, space='buy')
    formula31 = CategoricalParameter(
        formulas, default=formulas[0], optimize=31 < CONDITIONS, space='buy')
    formula32 = CategoricalParameter(
        formulas, default=formulas[0], optimize=32 < CONDITIONS, space='buy')
    formula33 = CategoricalParameter(
        formulas, default=formulas[0], optimize=33 < CONDITIONS, space='buy')
    formula34 = CategoricalParameter(
        formulas, default=formulas[0], optimize=34 < CONDITIONS, space='buy')
    formula35 = CategoricalParameter(
        formulas, default=formulas[0], optimize=35 < CONDITIONS, space='buy')
    formula36 = CategoricalParameter(
        formulas, default=formulas[0], optimize=36 < CONDITIONS, space='buy')
    formula37 = CategoricalParameter(
        formulas, default=formulas[0], optimize=37 < CONDITIONS, space='buy')
    formula38 = CategoricalParameter(
        formulas, default=formulas[0], optimize=38 < CONDITIONS, space='buy')
    formula39 = CategoricalParameter(
        formulas, default=formulas[0], optimize=39 < CONDITIONS, space='buy')
    formula40 = CategoricalParameter(
        formulas, default=formulas[0], optimize=40 < CONDITIONS, space='buy')
    formula41 = CategoricalParameter(
        formulas, default=formulas[0], optimize=41 < CONDITIONS, space='buy')
    formula42 = CategoricalParameter(
        formulas, default=formulas[0], optimize=42 < CONDITIONS, space='buy')
    formula43 = CategoricalParameter(
        formulas, default=formulas[0], optimize=43 < CONDITIONS, space='buy')
    formula44 = CategoricalParameter(
        formulas, default=formulas[0], optimize=44 < CONDITIONS, space='buy')
    formula45 = CategoricalParameter(
        formulas, default=formulas[0], optimize=45 < CONDITIONS, space='buy')
    formula46 = CategoricalParameter(
        formulas, default=formulas[0], optimize=46 < CONDITIONS, space='buy')
    formula47 = CategoricalParameter(
        formulas, default=formulas[0], optimize=47 < CONDITIONS, space='buy')
    formula48 = CategoricalParameter(
        formulas, default=formulas[0], optimize=48 < CONDITIONS, space='buy')
    formula49 = CategoricalParameter(
        formulas, default=formulas[0], optimize=49 < CONDITIONS, space='buy')
    formula50 = CategoricalParameter(
        formulas, default=formulas[0], optimize=50 < CONDITIONS, space='buy')
    formula51 = CategoricalParameter(
        formulas, default=formulas[0], optimize=51 < CONDITIONS, space='buy')
    formula52 = CategoricalParameter(
        formulas, default=formulas[0], optimize=52 < CONDITIONS, space='buy')
    formula53 = CategoricalParameter(
        formulas, default=formulas[0], optimize=53 < CONDITIONS, space='buy')
    formula54 = CategoricalParameter(
        formulas, default=formulas[0], optimize=54 < CONDITIONS, space='buy')
    formula55 = CategoricalParameter(
        formulas, default=formulas[0], optimize=55 < CONDITIONS, space='buy')
    formula56 = CategoricalParameter(
        formulas, default=formulas[0], optimize=56 < CONDITIONS, space='buy')
    formula57 = CategoricalParameter(
        formulas, default=formulas[0], optimize=57 < CONDITIONS, space='buy')
    formula58 = CategoricalParameter(
        formulas, default=formulas[0], optimize=58 < CONDITIONS, space='buy')
    formula59 = CategoricalParameter(
        formulas, default=formulas[0], optimize=59 < CONDITIONS, space='buy')
    formula60 = CategoricalParameter(
        formulas, default=formulas[0], optimize=60 < CONDITIONS, space='buy')
    formula61 = CategoricalParameter(
        formulas, default=formulas[0], optimize=61 < CONDITIONS, space='buy')
    formula62 = CategoricalParameter(
        formulas, default=formulas[0], optimize=62 < CONDITIONS, space='buy')
    formula63 = CategoricalParameter(
        formulas, default=formulas[0], optimize=63 < CONDITIONS, space='buy')
    formula64 = CategoricalParameter(
        formulas, default=formulas[0], optimize=64 < CONDITIONS, space='buy')
    formula65 = CategoricalParameter(
        formulas, default=formulas[0], optimize=65 < CONDITIONS, space='buy')
    formula66 = CategoricalParameter(
        formulas, default=formulas[0], optimize=66 < CONDITIONS, space='buy')
    formula67 = CategoricalParameter(
        formulas, default=formulas[0], optimize=67 < CONDITIONS, space='buy')
    formula68 = CategoricalParameter(
        formulas, default=formulas[0], optimize=68 < CONDITIONS, space='buy')
    formula69 = CategoricalParameter(
        formulas, default=formulas[0], optimize=69 < CONDITIONS, space='buy')
    formula70 = CategoricalParameter(
        formulas, default=formulas[0], optimize=70 < CONDITIONS, space='buy')
    formula71 = CategoricalParameter(
        formulas, default=formulas[0], optimize=71 < CONDITIONS, space='buy')
    formula72 = CategoricalParameter(
        formulas, default=formulas[0], optimize=72 < CONDITIONS, space='buy')
    formula73 = CategoricalParameter(
        formulas, default=formulas[0], optimize=73 < CONDITIONS, space='buy')
    formula74 = CategoricalParameter(
        formulas, default=formulas[0], optimize=74 < CONDITIONS, space='buy')
    formula75 = CategoricalParameter(
        formulas, default=formulas[0], optimize=75 < CONDITIONS, space='buy')
    formula76 = CategoricalParameter(
        formulas, default=formulas[0], optimize=76 < CONDITIONS, space='buy')
    formula77 = CategoricalParameter(
        formulas, default=formulas[0], optimize=77 < CONDITIONS, space='buy')
    formula78 = CategoricalParameter(
        formulas, default=formulas[0], optimize=78 < CONDITIONS, space='buy')
    formula79 = CategoricalParameter(
        formulas, default=formulas[0], optimize=79 < CONDITIONS, space='buy')
    formula80 = CategoricalParameter(
        formulas, default=formulas[0], optimize=80 < CONDITIONS, space='buy')
    formula81 = CategoricalParameter(
        formulas, default=formulas[0], optimize=81 < CONDITIONS, space='buy')
    formula82 = CategoricalParameter(
        formulas, default=formulas[0], optimize=82 < CONDITIONS, space='buy')
    formula83 = CategoricalParameter(
        formulas, default=formulas[0], optimize=83 < CONDITIONS, space='buy')
    formula84 = CategoricalParameter(
        formulas, default=formulas[0], optimize=84 < CONDITIONS, space='buy')
    formula85 = CategoricalParameter(
        formulas, default=formulas[0], optimize=85 < CONDITIONS, space='buy')
    formula86 = CategoricalParameter(
        formulas, default=formulas[0], optimize=86 < CONDITIONS, space='buy')
    formula87 = CategoricalParameter(
        formulas, default=formulas[0], optimize=87 < CONDITIONS, space='buy')
    formula88 = CategoricalParameter(
        formulas, default=formulas[0], optimize=88 < CONDITIONS, space='buy')
    formula89 = CategoricalParameter(
        formulas, default=formulas[0], optimize=89 < CONDITIONS, space='buy')
    formula90 = CategoricalParameter(
        formulas, default=formulas[0], optimize=90 < CONDITIONS, space='buy')
    formula91 = CategoricalParameter(
        formulas, default=formulas[0], optimize=91 < CONDITIONS, space='buy')
    formula92 = CategoricalParameter(
        formulas, default=formulas[0], optimize=92 < CONDITIONS, space='buy')
    formula93 = CategoricalParameter(
        formulas, default=formulas[0], optimize=93 < CONDITIONS, space='buy')
    formula94 = CategoricalParameter(
        formulas, default=formulas[0], optimize=94 < CONDITIONS, space='buy')
    formula95 = CategoricalParameter(
        formulas, default=formulas[0], optimize=95 < CONDITIONS, space='buy')
    formula96 = CategoricalParameter(
        formulas, default=formulas[0], optimize=96 < CONDITIONS, space='buy')
    formula97 = CategoricalParameter(
        formulas, default=formulas[0], optimize=97 < CONDITIONS, space='buy')
    formula98 = CategoricalParameter(
        formulas, default=formulas[0], optimize=98 < CONDITIONS, space='buy')
    formula99 = CategoricalParameter(
        formulas, default=formulas[0], optimize=99 < CONDITIONS, space='buy')

    indicator0 = CategoricalParameter(
        indicators, default=indicators[0], optimize=0 < CONDITIONS, space='buy')
    indicator1 = CategoricalParameter(
        indicators, default=indicators[0], optimize=1 < CONDITIONS, space='buy')
    indicator2 = CategoricalParameter(
        indicators, default=indicators[0], optimize=2 < CONDITIONS, space='buy')
    indicator3 = CategoricalParameter(
        indicators, default=indicators[0], optimize=3 < CONDITIONS, space='buy')
    indicator4 = CategoricalParameter(
        indicators, default=indicators[0], optimize=4 < CONDITIONS, space='buy')
    indicator5 = CategoricalParameter(
        indicators, default=indicators[0], optimize=5 < CONDITIONS, space='buy')
    indicator6 = CategoricalParameter(
        indicators, default=indicators[0], optimize=6 < CONDITIONS, space='buy')
    indicator7 = CategoricalParameter(
        indicators, default=indicators[0], optimize=7 < CONDITIONS, space='buy')
    indicator8 = CategoricalParameter(
        indicators, default=indicators[0], optimize=8 < CONDITIONS, space='buy')
    indicator9 = CategoricalParameter(
        indicators, default=indicators[0], optimize=9 < CONDITIONS, space='buy')
    indicator10 = CategoricalParameter(
        indicators, default=indicators[0], optimize=10 < CONDITIONS, space='buy')
    indicator11 = CategoricalParameter(
        indicators, default=indicators[0], optimize=11 < CONDITIONS, space='buy')
    indicator12 = CategoricalParameter(
        indicators, default=indicators[0], optimize=12 < CONDITIONS, space='buy')
    indicator13 = CategoricalParameter(
        indicators, default=indicators[0], optimize=13 < CONDITIONS, space='buy')
    indicator14 = CategoricalParameter(
        indicators, default=indicators[0], optimize=14 < CONDITIONS, space='buy')
    indicator15 = CategoricalParameter(
        indicators, default=indicators[0], optimize=15 < CONDITIONS, space='buy')
    indicator16 = CategoricalParameter(
        indicators, default=indicators[0], optimize=16 < CONDITIONS, space='buy')
    indicator17 = CategoricalParameter(
        indicators, default=indicators[0], optimize=17 < CONDITIONS, space='buy')
    indicator18 = CategoricalParameter(
        indicators, default=indicators[0], optimize=18 < CONDITIONS, space='buy')
    indicator19 = CategoricalParameter(
        indicators, default=indicators[0], optimize=19 < CONDITIONS, space='buy')
    indicator20 = CategoricalParameter(
        indicators, default=indicators[0], optimize=20 < CONDITIONS, space='buy')
    indicator21 = CategoricalParameter(
        indicators, default=indicators[0], optimize=21 < CONDITIONS, space='buy')
    indicator22 = CategoricalParameter(
        indicators, default=indicators[0], optimize=22 < CONDITIONS, space='buy')
    indicator23 = CategoricalParameter(
        indicators, default=indicators[0], optimize=23 < CONDITIONS, space='buy')
    indicator24 = CategoricalParameter(
        indicators, default=indicators[0], optimize=24 < CONDITIONS, space='buy')
    indicator25 = CategoricalParameter(
        indicators, default=indicators[0], optimize=25 < CONDITIONS, space='buy')
    indicator26 = CategoricalParameter(
        indicators, default=indicators[0], optimize=26 < CONDITIONS, space='buy')
    indicator27 = CategoricalParameter(
        indicators, default=indicators[0], optimize=27 < CONDITIONS, space='buy')
    indicator28 = CategoricalParameter(
        indicators, default=indicators[0], optimize=28 < CONDITIONS, space='buy')
    indicator29 = CategoricalParameter(
        indicators, default=indicators[0], optimize=29 < CONDITIONS, space='buy')
    indicator30 = CategoricalParameter(
        indicators, default=indicators[0], optimize=30 < CONDITIONS, space='buy')
    indicator31 = CategoricalParameter(
        indicators, default=indicators[0], optimize=31 < CONDITIONS, space='buy')
    indicator32 = CategoricalParameter(
        indicators, default=indicators[0], optimize=32 < CONDITIONS, space='buy')
    indicator33 = CategoricalParameter(
        indicators, default=indicators[0], optimize=33 < CONDITIONS, space='buy')
    indicator34 = CategoricalParameter(
        indicators, default=indicators[0], optimize=34 < CONDITIONS, space='buy')
    indicator35 = CategoricalParameter(
        indicators, default=indicators[0], optimize=35 < CONDITIONS, space='buy')
    indicator36 = CategoricalParameter(
        indicators, default=indicators[0], optimize=36 < CONDITIONS, space='buy')
    indicator37 = CategoricalParameter(
        indicators, default=indicators[0], optimize=37 < CONDITIONS, space='buy')
    indicator38 = CategoricalParameter(
        indicators, default=indicators[0], optimize=38 < CONDITIONS, space='buy')
    indicator39 = CategoricalParameter(
        indicators, default=indicators[0], optimize=39 < CONDITIONS, space='buy')
    indicator40 = CategoricalParameter(
        indicators, default=indicators[0], optimize=40 < CONDITIONS, space='buy')
    indicator41 = CategoricalParameter(
        indicators, default=indicators[0], optimize=41 < CONDITIONS, space='buy')
    indicator42 = CategoricalParameter(
        indicators, default=indicators[0], optimize=42 < CONDITIONS, space='buy')
    indicator43 = CategoricalParameter(
        indicators, default=indicators[0], optimize=43 < CONDITIONS, space='buy')
    indicator44 = CategoricalParameter(
        indicators, default=indicators[0], optimize=44 < CONDITIONS, space='buy')
    indicator45 = CategoricalParameter(
        indicators, default=indicators[0], optimize=45 < CONDITIONS, space='buy')
    indicator46 = CategoricalParameter(
        indicators, default=indicators[0], optimize=46 < CONDITIONS, space='buy')
    indicator47 = CategoricalParameter(
        indicators, default=indicators[0], optimize=47 < CONDITIONS, space='buy')
    indicator48 = CategoricalParameter(
        indicators, default=indicators[0], optimize=48 < CONDITIONS, space='buy')
    indicator49 = CategoricalParameter(
        indicators, default=indicators[0], optimize=49 < CONDITIONS, space='buy')
    indicator50 = CategoricalParameter(
        indicators, default=indicators[0], optimize=50 < CONDITIONS, space='buy')
    indicator51 = CategoricalParameter(
        indicators, default=indicators[0], optimize=51 < CONDITIONS, space='buy')
    indicator52 = CategoricalParameter(
        indicators, default=indicators[0], optimize=52 < CONDITIONS, space='buy')
    indicator53 = CategoricalParameter(
        indicators, default=indicators[0], optimize=53 < CONDITIONS, space='buy')
    indicator54 = CategoricalParameter(
        indicators, default=indicators[0], optimize=54 < CONDITIONS, space='buy')
    indicator55 = CategoricalParameter(
        indicators, default=indicators[0], optimize=55 < CONDITIONS, space='buy')
    indicator56 = CategoricalParameter(
        indicators, default=indicators[0], optimize=56 < CONDITIONS, space='buy')
    indicator57 = CategoricalParameter(
        indicators, default=indicators[0], optimize=57 < CONDITIONS, space='buy')
    indicator58 = CategoricalParameter(
        indicators, default=indicators[0], optimize=58 < CONDITIONS, space='buy')
    indicator59 = CategoricalParameter(
        indicators, default=indicators[0], optimize=59 < CONDITIONS, space='buy')
    indicator60 = CategoricalParameter(
        indicators, default=indicators[0], optimize=60 < CONDITIONS, space='buy')
    indicator61 = CategoricalParameter(
        indicators, default=indicators[0], optimize=61 < CONDITIONS, space='buy')
    indicator62 = CategoricalParameter(
        indicators, default=indicators[0], optimize=62 < CONDITIONS, space='buy')
    indicator63 = CategoricalParameter(
        indicators, default=indicators[0], optimize=63 < CONDITIONS, space='buy')
    indicator64 = CategoricalParameter(
        indicators, default=indicators[0], optimize=64 < CONDITIONS, space='buy')
    indicator65 = CategoricalParameter(
        indicators, default=indicators[0], optimize=65 < CONDITIONS, space='buy')
    indicator66 = CategoricalParameter(
        indicators, default=indicators[0], optimize=66 < CONDITIONS, space='buy')
    indicator67 = CategoricalParameter(
        indicators, default=indicators[0], optimize=67 < CONDITIONS, space='buy')
    indicator68 = CategoricalParameter(
        indicators, default=indicators[0], optimize=68 < CONDITIONS, space='buy')
    indicator69 = CategoricalParameter(
        indicators, default=indicators[0], optimize=69 < CONDITIONS, space='buy')
    indicator70 = CategoricalParameter(
        indicators, default=indicators[0], optimize=70 < CONDITIONS, space='buy')
    indicator71 = CategoricalParameter(
        indicators, default=indicators[0], optimize=71 < CONDITIONS, space='buy')
    indicator72 = CategoricalParameter(
        indicators, default=indicators[0], optimize=72 < CONDITIONS, space='buy')
    indicator73 = CategoricalParameter(
        indicators, default=indicators[0], optimize=73 < CONDITIONS, space='buy')
    indicator74 = CategoricalParameter(
        indicators, default=indicators[0], optimize=74 < CONDITIONS, space='buy')
    indicator75 = CategoricalParameter(
        indicators, default=indicators[0], optimize=75 < CONDITIONS, space='buy')
    indicator76 = CategoricalParameter(
        indicators, default=indicators[0], optimize=76 < CONDITIONS, space='buy')
    indicator77 = CategoricalParameter(
        indicators, default=indicators[0], optimize=77 < CONDITIONS, space='buy')
    indicator78 = CategoricalParameter(
        indicators, default=indicators[0], optimize=78 < CONDITIONS, space='buy')
    indicator79 = CategoricalParameter(
        indicators, default=indicators[0], optimize=79 < CONDITIONS, space='buy')
    indicator80 = CategoricalParameter(
        indicators, default=indicators[0], optimize=80 < CONDITIONS, space='buy')
    indicator81 = CategoricalParameter(
        indicators, default=indicators[0], optimize=81 < CONDITIONS, space='buy')
    indicator82 = CategoricalParameter(
        indicators, default=indicators[0], optimize=82 < CONDITIONS, space='buy')
    indicator83 = CategoricalParameter(
        indicators, default=indicators[0], optimize=83 < CONDITIONS, space='buy')
    indicator84 = CategoricalParameter(
        indicators, default=indicators[0], optimize=84 < CONDITIONS, space='buy')
    indicator85 = CategoricalParameter(
        indicators, default=indicators[0], optimize=85 < CONDITIONS, space='buy')
    indicator86 = CategoricalParameter(
        indicators, default=indicators[0], optimize=86 < CONDITIONS, space='buy')
    indicator87 = CategoricalParameter(
        indicators, default=indicators[0], optimize=87 < CONDITIONS, space='buy')
    indicator88 = CategoricalParameter(
        indicators, default=indicators[0], optimize=88 < CONDITIONS, space='buy')
    indicator89 = CategoricalParameter(
        indicators, default=indicators[0], optimize=89 < CONDITIONS, space='buy')
    indicator90 = CategoricalParameter(
        indicators, default=indicators[0], optimize=90 < CONDITIONS, space='buy')
    indicator91 = CategoricalParameter(
        indicators, default=indicators[0], optimize=91 < CONDITIONS, space='buy')
    indicator92 = CategoricalParameter(
        indicators, default=indicators[0], optimize=92 < CONDITIONS, space='buy')
    indicator93 = CategoricalParameter(
        indicators, default=indicators[0], optimize=93 < CONDITIONS, space='buy')
    indicator94 = CategoricalParameter(
        indicators, default=indicators[0], optimize=94 < CONDITIONS, space='buy')
    indicator95 = CategoricalParameter(
        indicators, default=indicators[0], optimize=95 < CONDITIONS, space='buy')
    indicator96 = CategoricalParameter(
        indicators, default=indicators[0], optimize=96 < CONDITIONS, space='buy')
    indicator97 = CategoricalParameter(
        indicators, default=indicators[0], optimize=97 < CONDITIONS, space='buy')
    indicator98 = CategoricalParameter(
        indicators, default=indicators[0], optimize=98 < CONDITIONS, space='buy')
    indicator99 = CategoricalParameter(
        indicators, default=indicators[0], optimize=99 < CONDITIONS, space='buy')

    crossed0 = CategoricalParameter(
        indicators, default=indicators[0], optimize=0 < CONDITIONS, space='buy')
    crossed1 = CategoricalParameter(
        indicators, default=indicators[0], optimize=1 < CONDITIONS, space='buy')
    crossed2 = CategoricalParameter(
        indicators, default=indicators[0], optimize=2 < CONDITIONS, space='buy')
    crossed3 = CategoricalParameter(
        indicators, default=indicators[0], optimize=3 < CONDITIONS, space='buy')
    crossed4 = CategoricalParameter(
        indicators, default=indicators[0], optimize=4 < CONDITIONS, space='buy')
    crossed5 = CategoricalParameter(
        indicators, default=indicators[0], optimize=5 < CONDITIONS, space='buy')
    crossed6 = CategoricalParameter(
        indicators, default=indicators[0], optimize=6 < CONDITIONS, space='buy')
    crossed7 = CategoricalParameter(
        indicators, default=indicators[0], optimize=7 < CONDITIONS, space='buy')
    crossed8 = CategoricalParameter(
        indicators, default=indicators[0], optimize=8 < CONDITIONS, space='buy')
    crossed9 = CategoricalParameter(
        indicators, default=indicators[0], optimize=9 < CONDITIONS, space='buy')
    crossed10 = CategoricalParameter(
        indicators, default=indicators[0], optimize=10 < CONDITIONS, space='buy')
    crossed11 = CategoricalParameter(
        indicators, default=indicators[0], optimize=11 < CONDITIONS, space='buy')
    crossed12 = CategoricalParameter(
        indicators, default=indicators[0], optimize=12 < CONDITIONS, space='buy')
    crossed13 = CategoricalParameter(
        indicators, default=indicators[0], optimize=13 < CONDITIONS, space='buy')
    crossed14 = CategoricalParameter(
        indicators, default=indicators[0], optimize=14 < CONDITIONS, space='buy')
    crossed15 = CategoricalParameter(
        indicators, default=indicators[0], optimize=15 < CONDITIONS, space='buy')
    crossed16 = CategoricalParameter(
        indicators, default=indicators[0], optimize=16 < CONDITIONS, space='buy')
    crossed17 = CategoricalParameter(
        indicators, default=indicators[0], optimize=17 < CONDITIONS, space='buy')
    crossed18 = CategoricalParameter(
        indicators, default=indicators[0], optimize=18 < CONDITIONS, space='buy')
    crossed19 = CategoricalParameter(
        indicators, default=indicators[0], optimize=19 < CONDITIONS, space='buy')
    crossed20 = CategoricalParameter(
        indicators, default=indicators[0], optimize=20 < CONDITIONS, space='buy')
    crossed21 = CategoricalParameter(
        indicators, default=indicators[0], optimize=21 < CONDITIONS, space='buy')
    crossed22 = CategoricalParameter(
        indicators, default=indicators[0], optimize=22 < CONDITIONS, space='buy')
    crossed23 = CategoricalParameter(
        indicators, default=indicators[0], optimize=23 < CONDITIONS, space='buy')
    crossed24 = CategoricalParameter(
        indicators, default=indicators[0], optimize=24 < CONDITIONS, space='buy')
    crossed25 = CategoricalParameter(
        indicators, default=indicators[0], optimize=25 < CONDITIONS, space='buy')
    crossed26 = CategoricalParameter(
        indicators, default=indicators[0], optimize=26 < CONDITIONS, space='buy')
    crossed27 = CategoricalParameter(
        indicators, default=indicators[0], optimize=27 < CONDITIONS, space='buy')
    crossed28 = CategoricalParameter(
        indicators, default=indicators[0], optimize=28 < CONDITIONS, space='buy')
    crossed29 = CategoricalParameter(
        indicators, default=indicators[0], optimize=29 < CONDITIONS, space='buy')
    crossed30 = CategoricalParameter(
        indicators, default=indicators[0], optimize=30 < CONDITIONS, space='buy')
    crossed31 = CategoricalParameter(
        indicators, default=indicators[0], optimize=31 < CONDITIONS, space='buy')
    crossed32 = CategoricalParameter(
        indicators, default=indicators[0], optimize=32 < CONDITIONS, space='buy')
    crossed33 = CategoricalParameter(
        indicators, default=indicators[0], optimize=33 < CONDITIONS, space='buy')
    crossed34 = CategoricalParameter(
        indicators, default=indicators[0], optimize=34 < CONDITIONS, space='buy')
    crossed35 = CategoricalParameter(
        indicators, default=indicators[0], optimize=35 < CONDITIONS, space='buy')
    crossed36 = CategoricalParameter(
        indicators, default=indicators[0], optimize=36 < CONDITIONS, space='buy')
    crossed37 = CategoricalParameter(
        indicators, default=indicators[0], optimize=37 < CONDITIONS, space='buy')
    crossed38 = CategoricalParameter(
        indicators, default=indicators[0], optimize=38 < CONDITIONS, space='buy')
    crossed39 = CategoricalParameter(
        indicators, default=indicators[0], optimize=39 < CONDITIONS, space='buy')
    crossed40 = CategoricalParameter(
        indicators, default=indicators[0], optimize=40 < CONDITIONS, space='buy')
    crossed41 = CategoricalParameter(
        indicators, default=indicators[0], optimize=41 < CONDITIONS, space='buy')
    crossed42 = CategoricalParameter(
        indicators, default=indicators[0], optimize=42 < CONDITIONS, space='buy')
    crossed43 = CategoricalParameter(
        indicators, default=indicators[0], optimize=43 < CONDITIONS, space='buy')
    crossed44 = CategoricalParameter(
        indicators, default=indicators[0], optimize=44 < CONDITIONS, space='buy')
    crossed45 = CategoricalParameter(
        indicators, default=indicators[0], optimize=45 < CONDITIONS, space='buy')
    crossed46 = CategoricalParameter(
        indicators, default=indicators[0], optimize=46 < CONDITIONS, space='buy')
    crossed47 = CategoricalParameter(
        indicators, default=indicators[0], optimize=47 < CONDITIONS, space='buy')
    crossed48 = CategoricalParameter(
        indicators, default=indicators[0], optimize=48 < CONDITIONS, space='buy')
    crossed49 = CategoricalParameter(
        indicators, default=indicators[0], optimize=49 < CONDITIONS, space='buy')
    crossed50 = CategoricalParameter(
        indicators, default=indicators[0], optimize=50 < CONDITIONS, space='buy')
    crossed51 = CategoricalParameter(
        indicators, default=indicators[0], optimize=51 < CONDITIONS, space='buy')
    crossed52 = CategoricalParameter(
        indicators, default=indicators[0], optimize=52 < CONDITIONS, space='buy')
    crossed53 = CategoricalParameter(
        indicators, default=indicators[0], optimize=53 < CONDITIONS, space='buy')
    crossed54 = CategoricalParameter(
        indicators, default=indicators[0], optimize=54 < CONDITIONS, space='buy')
    crossed55 = CategoricalParameter(
        indicators, default=indicators[0], optimize=55 < CONDITIONS, space='buy')
    crossed56 = CategoricalParameter(
        indicators, default=indicators[0], optimize=56 < CONDITIONS, space='buy')
    crossed57 = CategoricalParameter(
        indicators, default=indicators[0], optimize=57 < CONDITIONS, space='buy')
    crossed58 = CategoricalParameter(
        indicators, default=indicators[0], optimize=58 < CONDITIONS, space='buy')
    crossed59 = CategoricalParameter(
        indicators, default=indicators[0], optimize=59 < CONDITIONS, space='buy')
    crossed60 = CategoricalParameter(
        indicators, default=indicators[0], optimize=60 < CONDITIONS, space='buy')
    crossed61 = CategoricalParameter(
        indicators, default=indicators[0], optimize=61 < CONDITIONS, space='buy')
    crossed62 = CategoricalParameter(
        indicators, default=indicators[0], optimize=62 < CONDITIONS, space='buy')
    crossed63 = CategoricalParameter(
        indicators, default=indicators[0], optimize=63 < CONDITIONS, space='buy')
    crossed64 = CategoricalParameter(
        indicators, default=indicators[0], optimize=64 < CONDITIONS, space='buy')
    crossed65 = CategoricalParameter(
        indicators, default=indicators[0], optimize=65 < CONDITIONS, space='buy')
    crossed66 = CategoricalParameter(
        indicators, default=indicators[0], optimize=66 < CONDITIONS, space='buy')
    crossed67 = CategoricalParameter(
        indicators, default=indicators[0], optimize=67 < CONDITIONS, space='buy')
    crossed68 = CategoricalParameter(
        indicators, default=indicators[0], optimize=68 < CONDITIONS, space='buy')
    crossed69 = CategoricalParameter(
        indicators, default=indicators[0], optimize=69 < CONDITIONS, space='buy')
    crossed70 = CategoricalParameter(
        indicators, default=indicators[0], optimize=70 < CONDITIONS, space='buy')
    crossed71 = CategoricalParameter(
        indicators, default=indicators[0], optimize=71 < CONDITIONS, space='buy')
    crossed72 = CategoricalParameter(
        indicators, default=indicators[0], optimize=72 < CONDITIONS, space='buy')
    crossed73 = CategoricalParameter(
        indicators, default=indicators[0], optimize=73 < CONDITIONS, space='buy')
    crossed74 = CategoricalParameter(
        indicators, default=indicators[0], optimize=74 < CONDITIONS, space='buy')
    crossed75 = CategoricalParameter(
        indicators, default=indicators[0], optimize=75 < CONDITIONS, space='buy')
    crossed76 = CategoricalParameter(
        indicators, default=indicators[0], optimize=76 < CONDITIONS, space='buy')
    crossed77 = CategoricalParameter(
        indicators, default=indicators[0], optimize=77 < CONDITIONS, space='buy')
    crossed78 = CategoricalParameter(
        indicators, default=indicators[0], optimize=78 < CONDITIONS, space='buy')
    crossed79 = CategoricalParameter(
        indicators, default=indicators[0], optimize=79 < CONDITIONS, space='buy')
    crossed80 = CategoricalParameter(
        indicators, default=indicators[0], optimize=80 < CONDITIONS, space='buy')
    crossed81 = CategoricalParameter(
        indicators, default=indicators[0], optimize=81 < CONDITIONS, space='buy')
    crossed82 = CategoricalParameter(
        indicators, default=indicators[0], optimize=82 < CONDITIONS, space='buy')
    crossed83 = CategoricalParameter(
        indicators, default=indicators[0], optimize=83 < CONDITIONS, space='buy')
    crossed84 = CategoricalParameter(
        indicators, default=indicators[0], optimize=84 < CONDITIONS, space='buy')
    crossed85 = CategoricalParameter(
        indicators, default=indicators[0], optimize=85 < CONDITIONS, space='buy')
    crossed86 = CategoricalParameter(
        indicators, default=indicators[0], optimize=86 < CONDITIONS, space='buy')
    crossed87 = CategoricalParameter(
        indicators, default=indicators[0], optimize=87 < CONDITIONS, space='buy')
    crossed88 = CategoricalParameter(
        indicators, default=indicators[0], optimize=88 < CONDITIONS, space='buy')
    crossed89 = CategoricalParameter(
        indicators, default=indicators[0], optimize=89 < CONDITIONS, space='buy')
    crossed90 = CategoricalParameter(
        indicators, default=indicators[0], optimize=90 < CONDITIONS, space='buy')
    crossed91 = CategoricalParameter(
        indicators, default=indicators[0], optimize=91 < CONDITIONS, space='buy')
    crossed92 = CategoricalParameter(
        indicators, default=indicators[0], optimize=92 < CONDITIONS, space='buy')
    crossed93 = CategoricalParameter(
        indicators, default=indicators[0], optimize=93 < CONDITIONS, space='buy')
    crossed94 = CategoricalParameter(
        indicators, default=indicators[0], optimize=94 < CONDITIONS, space='buy')
    crossed95 = CategoricalParameter(
        indicators, default=indicators[0], optimize=95 < CONDITIONS, space='buy')
    crossed96 = CategoricalParameter(
        indicators, default=indicators[0], optimize=96 < CONDITIONS, space='buy')
    crossed97 = CategoricalParameter(
        indicators, default=indicators[0], optimize=97 < CONDITIONS, space='buy')
    crossed98 = CategoricalParameter(
        indicators, default=indicators[0], optimize=98 < CONDITIONS, space='buy')
    crossed99 = CategoricalParameter(
        indicators, default=indicators[0], optimize=99 < CONDITIONS, space='buy')

    timeframe0 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=0 < CONDITIONS, space='buy')
    timeframe1 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=1 < CONDITIONS, space='buy')
    timeframe2 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=2 < CONDITIONS, space='buy')
    timeframe3 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=3 < CONDITIONS, space='buy')
    timeframe4 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=4 < CONDITIONS, space='buy')
    timeframe5 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=5 < CONDITIONS, space='buy')
    timeframe6 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=6 < CONDITIONS, space='buy')
    timeframe7 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=7 < CONDITIONS, space='buy')
    timeframe8 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=8 < CONDITIONS, space='buy')
    timeframe9 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=9 < CONDITIONS, space='buy')
    timeframe10 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=10 < CONDITIONS, space='buy')
    timeframe11 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=11 < CONDITIONS, space='buy')
    timeframe12 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=12 < CONDITIONS, space='buy')
    timeframe13 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=13 < CONDITIONS, space='buy')
    timeframe14 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=14 < CONDITIONS, space='buy')
    timeframe15 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=15 < CONDITIONS, space='buy')
    timeframe16 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=16 < CONDITIONS, space='buy')
    timeframe17 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=17 < CONDITIONS, space='buy')
    timeframe18 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=18 < CONDITIONS, space='buy')
    timeframe19 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=19 < CONDITIONS, space='buy')
    timeframe20 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=20 < CONDITIONS, space='buy')
    timeframe21 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=21 < CONDITIONS, space='buy')
    timeframe22 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=22 < CONDITIONS, space='buy')
    timeframe23 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=23 < CONDITIONS, space='buy')
    timeframe24 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=24 < CONDITIONS, space='buy')
    timeframe25 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=25 < CONDITIONS, space='buy')
    timeframe26 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=26 < CONDITIONS, space='buy')
    timeframe27 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=27 < CONDITIONS, space='buy')
    timeframe28 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=28 < CONDITIONS, space='buy')
    timeframe29 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=29 < CONDITIONS, space='buy')
    timeframe30 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=30 < CONDITIONS, space='buy')
    timeframe31 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=31 < CONDITIONS, space='buy')
    timeframe32 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=32 < CONDITIONS, space='buy')
    timeframe33 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=33 < CONDITIONS, space='buy')
    timeframe34 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=34 < CONDITIONS, space='buy')
    timeframe35 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=35 < CONDITIONS, space='buy')
    timeframe36 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=36 < CONDITIONS, space='buy')
    timeframe37 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=37 < CONDITIONS, space='buy')
    timeframe38 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=38 < CONDITIONS, space='buy')
    timeframe39 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=39 < CONDITIONS, space='buy')
    timeframe40 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=40 < CONDITIONS, space='buy')
    timeframe41 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=41 < CONDITIONS, space='buy')
    timeframe42 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=42 < CONDITIONS, space='buy')
    timeframe43 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=43 < CONDITIONS, space='buy')
    timeframe44 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=44 < CONDITIONS, space='buy')
    timeframe45 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=45 < CONDITIONS, space='buy')
    timeframe46 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=46 < CONDITIONS, space='buy')
    timeframe47 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=47 < CONDITIONS, space='buy')
    timeframe48 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=48 < CONDITIONS, space='buy')
    timeframe49 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=49 < CONDITIONS, space='buy')
    timeframe50 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=50 < CONDITIONS, space='buy')
    timeframe51 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=51 < CONDITIONS, space='buy')
    timeframe52 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=52 < CONDITIONS, space='buy')
    timeframe53 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=53 < CONDITIONS, space='buy')
    timeframe54 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=54 < CONDITIONS, space='buy')
    timeframe55 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=55 < CONDITIONS, space='buy')
    timeframe56 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=56 < CONDITIONS, space='buy')
    timeframe57 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=57 < CONDITIONS, space='buy')
    timeframe58 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=58 < CONDITIONS, space='buy')
    timeframe59 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=59 < CONDITIONS, space='buy')
    timeframe60 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=60 < CONDITIONS, space='buy')
    timeframe61 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=61 < CONDITIONS, space='buy')
    timeframe62 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=62 < CONDITIONS, space='buy')
    timeframe63 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=63 < CONDITIONS, space='buy')
    timeframe64 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=64 < CONDITIONS, space='buy')
    timeframe65 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=65 < CONDITIONS, space='buy')
    timeframe66 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=66 < CONDITIONS, space='buy')
    timeframe67 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=67 < CONDITIONS, space='buy')
    timeframe68 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=68 < CONDITIONS, space='buy')
    timeframe69 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=69 < CONDITIONS, space='buy')
    timeframe70 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=70 < CONDITIONS, space='buy')
    timeframe71 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=71 < CONDITIONS, space='buy')
    timeframe72 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=72 < CONDITIONS, space='buy')
    timeframe73 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=73 < CONDITIONS, space='buy')
    timeframe74 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=74 < CONDITIONS, space='buy')
    timeframe75 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=75 < CONDITIONS, space='buy')
    timeframe76 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=76 < CONDITIONS, space='buy')
    timeframe77 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=77 < CONDITIONS, space='buy')
    timeframe78 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=78 < CONDITIONS, space='buy')
    timeframe79 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=79 < CONDITIONS, space='buy')
    timeframe80 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=80 < CONDITIONS, space='buy')
    timeframe81 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=81 < CONDITIONS, space='buy')
    timeframe82 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=82 < CONDITIONS, space='buy')
    timeframe83 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=83 < CONDITIONS, space='buy')
    timeframe84 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=84 < CONDITIONS, space='buy')
    timeframe85 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=85 < CONDITIONS, space='buy')
    timeframe86 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=86 < CONDITIONS, space='buy')
    timeframe87 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=87 < CONDITIONS, space='buy')
    timeframe88 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=88 < CONDITIONS, space='buy')
    timeframe89 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=89 < CONDITIONS, space='buy')
    timeframe90 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=90 < CONDITIONS, space='buy')
    timeframe91 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=91 < CONDITIONS, space='buy')
    timeframe92 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=92 < CONDITIONS, space='buy')
    timeframe93 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=93 < CONDITIONS, space='buy')
    timeframe94 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=94 < CONDITIONS, space='buy')
    timeframe95 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=95 < CONDITIONS, space='buy')
    timeframe96 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=96 < CONDITIONS, space='buy')
    timeframe97 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=97 < CONDITIONS, space='buy')
    timeframe98 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=98 < CONDITIONS, space='buy')
    timeframe99 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=99 < CONDITIONS, space='buy')

    crossed_timeframe0 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=0 < CONDITIONS, space='buy')
    crossed_timeframe1 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=1 < CONDITIONS, space='buy')
    crossed_timeframe2 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=2 < CONDITIONS, space='buy')
    crossed_timeframe3 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=3 < CONDITIONS, space='buy')
    crossed_timeframe4 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=4 < CONDITIONS, space='buy')
    crossed_timeframe5 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=5 < CONDITIONS, space='buy')
    crossed_timeframe6 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=6 < CONDITIONS, space='buy')
    crossed_timeframe7 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=7 < CONDITIONS, space='buy')
    crossed_timeframe8 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=8 < CONDITIONS, space='buy')
    crossed_timeframe9 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=9 < CONDITIONS, space='buy')
    crossed_timeframe10 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=10 < CONDITIONS, space='buy')
    crossed_timeframe11 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=11 < CONDITIONS, space='buy')
    crossed_timeframe12 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=12 < CONDITIONS, space='buy')
    crossed_timeframe13 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=13 < CONDITIONS, space='buy')
    crossed_timeframe14 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=14 < CONDITIONS, space='buy')
    crossed_timeframe15 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=15 < CONDITIONS, space='buy')
    crossed_timeframe16 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=16 < CONDITIONS, space='buy')
    crossed_timeframe17 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=17 < CONDITIONS, space='buy')
    crossed_timeframe18 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=18 < CONDITIONS, space='buy')
    crossed_timeframe19 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=19 < CONDITIONS, space='buy')
    crossed_timeframe20 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=20 < CONDITIONS, space='buy')
    crossed_timeframe21 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=21 < CONDITIONS, space='buy')
    crossed_timeframe22 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=22 < CONDITIONS, space='buy')
    crossed_timeframe23 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=23 < CONDITIONS, space='buy')
    crossed_timeframe24 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=24 < CONDITIONS, space='buy')
    crossed_timeframe25 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=25 < CONDITIONS, space='buy')
    crossed_timeframe26 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=26 < CONDITIONS, space='buy')
    crossed_timeframe27 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=27 < CONDITIONS, space='buy')
    crossed_timeframe28 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=28 < CONDITIONS, space='buy')
    crossed_timeframe29 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=29 < CONDITIONS, space='buy')
    crossed_timeframe30 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=30 < CONDITIONS, space='buy')
    crossed_timeframe31 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=31 < CONDITIONS, space='buy')
    crossed_timeframe32 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=32 < CONDITIONS, space='buy')
    crossed_timeframe33 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=33 < CONDITIONS, space='buy')
    crossed_timeframe34 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=34 < CONDITIONS, space='buy')
    crossed_timeframe35 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=35 < CONDITIONS, space='buy')
    crossed_timeframe36 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=36 < CONDITIONS, space='buy')
    crossed_timeframe37 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=37 < CONDITIONS, space='buy')
    crossed_timeframe38 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=38 < CONDITIONS, space='buy')
    crossed_timeframe39 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=39 < CONDITIONS, space='buy')
    crossed_timeframe40 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=40 < CONDITIONS, space='buy')
    crossed_timeframe41 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=41 < CONDITIONS, space='buy')
    crossed_timeframe42 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=42 < CONDITIONS, space='buy')
    crossed_timeframe43 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=43 < CONDITIONS, space='buy')
    crossed_timeframe44 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=44 < CONDITIONS, space='buy')
    crossed_timeframe45 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=45 < CONDITIONS, space='buy')
    crossed_timeframe46 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=46 < CONDITIONS, space='buy')
    crossed_timeframe47 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=47 < CONDITIONS, space='buy')
    crossed_timeframe48 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=48 < CONDITIONS, space='buy')
    crossed_timeframe49 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=49 < CONDITIONS, space='buy')
    crossed_timeframe50 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=50 < CONDITIONS, space='buy')
    crossed_timeframe51 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=51 < CONDITIONS, space='buy')
    crossed_timeframe52 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=52 < CONDITIONS, space='buy')
    crossed_timeframe53 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=53 < CONDITIONS, space='buy')
    crossed_timeframe54 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=54 < CONDITIONS, space='buy')
    crossed_timeframe55 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=55 < CONDITIONS, space='buy')
    crossed_timeframe56 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=56 < CONDITIONS, space='buy')
    crossed_timeframe57 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=57 < CONDITIONS, space='buy')
    crossed_timeframe58 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=58 < CONDITIONS, space='buy')
    crossed_timeframe59 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=59 < CONDITIONS, space='buy')
    crossed_timeframe60 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=60 < CONDITIONS, space='buy')
    crossed_timeframe61 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=61 < CONDITIONS, space='buy')
    crossed_timeframe62 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=62 < CONDITIONS, space='buy')
    crossed_timeframe63 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=63 < CONDITIONS, space='buy')
    crossed_timeframe64 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=64 < CONDITIONS, space='buy')
    crossed_timeframe65 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=65 < CONDITIONS, space='buy')
    crossed_timeframe66 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=66 < CONDITIONS, space='buy')
    crossed_timeframe67 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=67 < CONDITIONS, space='buy')
    crossed_timeframe68 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=68 < CONDITIONS, space='buy')
    crossed_timeframe69 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=69 < CONDITIONS, space='buy')
    crossed_timeframe70 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=70 < CONDITIONS, space='buy')
    crossed_timeframe71 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=71 < CONDITIONS, space='buy')
    crossed_timeframe72 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=72 < CONDITIONS, space='buy')
    crossed_timeframe73 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=73 < CONDITIONS, space='buy')
    crossed_timeframe74 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=74 < CONDITIONS, space='buy')
    crossed_timeframe75 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=75 < CONDITIONS, space='buy')
    crossed_timeframe76 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=76 < CONDITIONS, space='buy')
    crossed_timeframe77 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=77 < CONDITIONS, space='buy')
    crossed_timeframe78 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=78 < CONDITIONS, space='buy')
    crossed_timeframe79 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=79 < CONDITIONS, space='buy')
    crossed_timeframe80 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=80 < CONDITIONS, space='buy')
    crossed_timeframe81 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=81 < CONDITIONS, space='buy')
    crossed_timeframe82 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=82 < CONDITIONS, space='buy')
    crossed_timeframe83 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=83 < CONDITIONS, space='buy')
    crossed_timeframe84 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=84 < CONDITIONS, space='buy')
    crossed_timeframe85 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=85 < CONDITIONS, space='buy')
    crossed_timeframe86 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=86 < CONDITIONS, space='buy')
    crossed_timeframe87 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=87 < CONDITIONS, space='buy')
    crossed_timeframe88 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=88 < CONDITIONS, space='buy')
    crossed_timeframe89 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=89 < CONDITIONS, space='buy')
    crossed_timeframe90 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=90 < CONDITIONS, space='buy')
    crossed_timeframe91 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=91 < CONDITIONS, space='buy')
    crossed_timeframe92 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=92 < CONDITIONS, space='buy')
    crossed_timeframe93 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=93 < CONDITIONS, space='buy')
    crossed_timeframe94 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=94 < CONDITIONS, space='buy')
    crossed_timeframe95 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=95 < CONDITIONS, space='buy')
    crossed_timeframe96 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=96 < CONDITIONS, space='buy')
    crossed_timeframe97 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=97 < CONDITIONS, space='buy')
    crossed_timeframe98 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=98 < CONDITIONS, space='buy')
    crossed_timeframe99 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='buy')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=99 < CONDITIONS, space='buy')

    real0 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=0 < CONDITIONS, space='buy')
    real1 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=1 < CONDITIONS, space='buy')
    real2 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=2 < CONDITIONS, space='buy')
    real3 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=3 < CONDITIONS, space='buy')
    real4 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=4 < CONDITIONS, space='buy')
    real5 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=5 < CONDITIONS, space='buy')
    real6 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=6 < CONDITIONS, space='buy')
    real7 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=7 < CONDITIONS, space='buy')
    real8 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=8 < CONDITIONS, space='buy')
    real9 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                             decimals=DECIMALS, optimize=9 < CONDITIONS, space='buy')
    real10 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=10 < CONDITIONS, space='buy')
    real11 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=11 < CONDITIONS, space='buy')
    real12 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=12 < CONDITIONS, space='buy')
    real13 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=13 < CONDITIONS, space='buy')
    real14 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=14 < CONDITIONS, space='buy')
    real15 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=15 < CONDITIONS, space='buy')
    real16 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=16 < CONDITIONS, space='buy')
    real17 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=17 < CONDITIONS, space='buy')
    real18 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=18 < CONDITIONS, space='buy')
    real19 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=19 < CONDITIONS, space='buy')
    real20 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=20 < CONDITIONS, space='buy')
    real21 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=21 < CONDITIONS, space='buy')
    real22 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=22 < CONDITIONS, space='buy')
    real23 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=23 < CONDITIONS, space='buy')
    real24 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=24 < CONDITIONS, space='buy')
    real25 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=25 < CONDITIONS, space='buy')
    real26 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=26 < CONDITIONS, space='buy')
    real27 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=27 < CONDITIONS, space='buy')
    real28 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=28 < CONDITIONS, space='buy')
    real29 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=29 < CONDITIONS, space='buy')
    real30 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=30 < CONDITIONS, space='buy')
    real31 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=31 < CONDITIONS, space='buy')
    real32 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=32 < CONDITIONS, space='buy')
    real33 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=33 < CONDITIONS, space='buy')
    real34 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=34 < CONDITIONS, space='buy')
    real35 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=35 < CONDITIONS, space='buy')
    real36 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=36 < CONDITIONS, space='buy')
    real37 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=37 < CONDITIONS, space='buy')
    real38 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=38 < CONDITIONS, space='buy')
    real39 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=39 < CONDITIONS, space='buy')
    real40 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=40 < CONDITIONS, space='buy')
    real41 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=41 < CONDITIONS, space='buy')
    real42 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=42 < CONDITIONS, space='buy')
    real43 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=43 < CONDITIONS, space='buy')
    real44 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=44 < CONDITIONS, space='buy')
    real45 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=45 < CONDITIONS, space='buy')
    real46 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=46 < CONDITIONS, space='buy')
    real47 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=47 < CONDITIONS, space='buy')
    real48 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=48 < CONDITIONS, space='buy')
    real49 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=49 < CONDITIONS, space='buy')
    real50 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=50 < CONDITIONS, space='buy')
    real51 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=51 < CONDITIONS, space='buy')
    real52 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=52 < CONDITIONS, space='buy')
    real53 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=53 < CONDITIONS, space='buy')
    real54 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=54 < CONDITIONS, space='buy')
    real55 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=55 < CONDITIONS, space='buy')
    real56 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=56 < CONDITIONS, space='buy')
    real57 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=57 < CONDITIONS, space='buy')
    real58 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=58 < CONDITIONS, space='buy')
    real59 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=59 < CONDITIONS, space='buy')
    real60 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=60 < CONDITIONS, space='buy')
    real61 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=61 < CONDITIONS, space='buy')
    real62 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=62 < CONDITIONS, space='buy')
    real63 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=63 < CONDITIONS, space='buy')
    real64 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=64 < CONDITIONS, space='buy')
    real65 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=65 < CONDITIONS, space='buy')
    real66 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=66 < CONDITIONS, space='buy')
    real67 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=67 < CONDITIONS, space='buy')
    real68 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=68 < CONDITIONS, space='buy')
    real69 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=69 < CONDITIONS, space='buy')
    real70 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=70 < CONDITIONS, space='buy')
    real71 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=71 < CONDITIONS, space='buy')
    real72 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=72 < CONDITIONS, space='buy')
    real73 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=73 < CONDITIONS, space='buy')
    real74 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=74 < CONDITIONS, space='buy')
    real75 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=75 < CONDITIONS, space='buy')
    real76 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=76 < CONDITIONS, space='buy')
    real77 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=77 < CONDITIONS, space='buy')
    real78 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=78 < CONDITIONS, space='buy')
    real79 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=79 < CONDITIONS, space='buy')
    real80 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=80 < CONDITIONS, space='buy')
    real81 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=81 < CONDITIONS, space='buy')
    real82 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=82 < CONDITIONS, space='buy')
    real83 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=83 < CONDITIONS, space='buy')
    real84 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=84 < CONDITIONS, space='buy')
    real85 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=85 < CONDITIONS, space='buy')
    real86 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=86 < CONDITIONS, space='buy')
    real87 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=87 < CONDITIONS, space='buy')
    real88 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=88 < CONDITIONS, space='buy')
    real89 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=89 < CONDITIONS, space='buy')
    real90 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=90 < CONDITIONS, space='buy')
    real91 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=91 < CONDITIONS, space='buy')
    real92 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=92 < CONDITIONS, space='buy')
    real93 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=93 < CONDITIONS, space='buy')
    real94 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=94 < CONDITIONS, space='buy')
    real95 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=95 < CONDITIONS, space='buy')
    real96 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=96 < CONDITIONS, space='buy')
    real97 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=97 < CONDITIONS, space='buy')
    real98 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=98 < CONDITIONS, space='buy')
    real99 = DecimalParameter(reals[0], reals[-1], default=reals[0],
                              decimals=DECIMALS, optimize=99 < CONDITIONS, space='buy')

    # SELL HYPEROPTABLE PARAMS:
    sell_formula0 = CategoricalParameter(
        formulas, default=formulas[0], optimize=0 < CONDITIONS, space='sell')
    sell_formula1 = CategoricalParameter(
        formulas, default=formulas[0], optimize=1 < CONDITIONS, space='sell')
    sell_formula2 = CategoricalParameter(
        formulas, default=formulas[0], optimize=2 < CONDITIONS, space='sell')
    sell_formula3 = CategoricalParameter(
        formulas, default=formulas[0], optimize=3 < CONDITIONS, space='sell')
    sell_formula4 = CategoricalParameter(
        formulas, default=formulas[0], optimize=4 < CONDITIONS, space='sell')
    sell_formula5 = CategoricalParameter(
        formulas, default=formulas[0], optimize=5 < CONDITIONS, space='sell')
    sell_formula6 = CategoricalParameter(
        formulas, default=formulas[0], optimize=6 < CONDITIONS, space='sell')
    sell_formula7 = CategoricalParameter(
        formulas, default=formulas[0], optimize=7 < CONDITIONS, space='sell')
    sell_formula8 = CategoricalParameter(
        formulas, default=formulas[0], optimize=8 < CONDITIONS, space='sell')
    sell_formula9 = CategoricalParameter(
        formulas, default=formulas[0], optimize=9 < CONDITIONS, space='sell')
    sell_formula10 = CategoricalParameter(
        formulas, default=formulas[0], optimize=10 < CONDITIONS, space='sell')
    sell_formula11 = CategoricalParameter(
        formulas, default=formulas[0], optimize=11 < CONDITIONS, space='sell')
    sell_formula12 = CategoricalParameter(
        formulas, default=formulas[0], optimize=12 < CONDITIONS, space='sell')
    sell_formula13 = CategoricalParameter(
        formulas, default=formulas[0], optimize=13 < CONDITIONS, space='sell')
    sell_formula14 = CategoricalParameter(
        formulas, default=formulas[0], optimize=14 < CONDITIONS, space='sell')
    sell_formula15 = CategoricalParameter(
        formulas, default=formulas[0], optimize=15 < CONDITIONS, space='sell')
    sell_formula16 = CategoricalParameter(
        formulas, default=formulas[0], optimize=16 < CONDITIONS, space='sell')
    sell_formula17 = CategoricalParameter(
        formulas, default=formulas[0], optimize=17 < CONDITIONS, space='sell')
    sell_formula18 = CategoricalParameter(
        formulas, default=formulas[0], optimize=18 < CONDITIONS, space='sell')
    sell_formula19 = CategoricalParameter(
        formulas, default=formulas[0], optimize=19 < CONDITIONS, space='sell')
    sell_formula20 = CategoricalParameter(
        formulas, default=formulas[0], optimize=20 < CONDITIONS, space='sell')
    sell_formula21 = CategoricalParameter(
        formulas, default=formulas[0], optimize=21 < CONDITIONS, space='sell')
    sell_formula22 = CategoricalParameter(
        formulas, default=formulas[0], optimize=22 < CONDITIONS, space='sell')
    sell_formula23 = CategoricalParameter(
        formulas, default=formulas[0], optimize=23 < CONDITIONS, space='sell')
    sell_formula24 = CategoricalParameter(
        formulas, default=formulas[0], optimize=24 < CONDITIONS, space='sell')
    sell_formula25 = CategoricalParameter(
        formulas, default=formulas[0], optimize=25 < CONDITIONS, space='sell')
    sell_formula26 = CategoricalParameter(
        formulas, default=formulas[0], optimize=26 < CONDITIONS, space='sell')
    sell_formula27 = CategoricalParameter(
        formulas, default=formulas[0], optimize=27 < CONDITIONS, space='sell')
    sell_formula28 = CategoricalParameter(
        formulas, default=formulas[0], optimize=28 < CONDITIONS, space='sell')
    sell_formula29 = CategoricalParameter(
        formulas, default=formulas[0], optimize=29 < CONDITIONS, space='sell')
    sell_formula30 = CategoricalParameter(
        formulas, default=formulas[0], optimize=30 < CONDITIONS, space='sell')
    sell_formula31 = CategoricalParameter(
        formulas, default=formulas[0], optimize=31 < CONDITIONS, space='sell')
    sell_formula32 = CategoricalParameter(
        formulas, default=formulas[0], optimize=32 < CONDITIONS, space='sell')
    sell_formula33 = CategoricalParameter(
        formulas, default=formulas[0], optimize=33 < CONDITIONS, space='sell')
    sell_formula34 = CategoricalParameter(
        formulas, default=formulas[0], optimize=34 < CONDITIONS, space='sell')
    sell_formula35 = CategoricalParameter(
        formulas, default=formulas[0], optimize=35 < CONDITIONS, space='sell')
    sell_formula36 = CategoricalParameter(
        formulas, default=formulas[0], optimize=36 < CONDITIONS, space='sell')
    sell_formula37 = CategoricalParameter(
        formulas, default=formulas[0], optimize=37 < CONDITIONS, space='sell')
    sell_formula38 = CategoricalParameter(
        formulas, default=formulas[0], optimize=38 < CONDITIONS, space='sell')
    sell_formula39 = CategoricalParameter(
        formulas, default=formulas[0], optimize=39 < CONDITIONS, space='sell')
    sell_formula40 = CategoricalParameter(
        formulas, default=formulas[0], optimize=40 < CONDITIONS, space='sell')
    sell_formula41 = CategoricalParameter(
        formulas, default=formulas[0], optimize=41 < CONDITIONS, space='sell')
    sell_formula42 = CategoricalParameter(
        formulas, default=formulas[0], optimize=42 < CONDITIONS, space='sell')
    sell_formula43 = CategoricalParameter(
        formulas, default=formulas[0], optimize=43 < CONDITIONS, space='sell')
    sell_formula44 = CategoricalParameter(
        formulas, default=formulas[0], optimize=44 < CONDITIONS, space='sell')
    sell_formula45 = CategoricalParameter(
        formulas, default=formulas[0], optimize=45 < CONDITIONS, space='sell')
    sell_formula46 = CategoricalParameter(
        formulas, default=formulas[0], optimize=46 < CONDITIONS, space='sell')
    sell_formula47 = CategoricalParameter(
        formulas, default=formulas[0], optimize=47 < CONDITIONS, space='sell')
    sell_formula48 = CategoricalParameter(
        formulas, default=formulas[0], optimize=48 < CONDITIONS, space='sell')
    sell_formula49 = CategoricalParameter(
        formulas, default=formulas[0], optimize=49 < CONDITIONS, space='sell')
    sell_formula50 = CategoricalParameter(
        formulas, default=formulas[0], optimize=50 < CONDITIONS, space='sell')
    sell_formula51 = CategoricalParameter(
        formulas, default=formulas[0], optimize=51 < CONDITIONS, space='sell')
    sell_formula52 = CategoricalParameter(
        formulas, default=formulas[0], optimize=52 < CONDITIONS, space='sell')
    sell_formula53 = CategoricalParameter(
        formulas, default=formulas[0], optimize=53 < CONDITIONS, space='sell')
    sell_formula54 = CategoricalParameter(
        formulas, default=formulas[0], optimize=54 < CONDITIONS, space='sell')
    sell_formula55 = CategoricalParameter(
        formulas, default=formulas[0], optimize=55 < CONDITIONS, space='sell')
    sell_formula56 = CategoricalParameter(
        formulas, default=formulas[0], optimize=56 < CONDITIONS, space='sell')
    sell_formula57 = CategoricalParameter(
        formulas, default=formulas[0], optimize=57 < CONDITIONS, space='sell')
    sell_formula58 = CategoricalParameter(
        formulas, default=formulas[0], optimize=58 < CONDITIONS, space='sell')
    sell_formula59 = CategoricalParameter(
        formulas, default=formulas[0], optimize=59 < CONDITIONS, space='sell')
    sell_formula60 = CategoricalParameter(
        formulas, default=formulas[0], optimize=60 < CONDITIONS, space='sell')
    sell_formula61 = CategoricalParameter(
        formulas, default=formulas[0], optimize=61 < CONDITIONS, space='sell')
    sell_formula62 = CategoricalParameter(
        formulas, default=formulas[0], optimize=62 < CONDITIONS, space='sell')
    sell_formula63 = CategoricalParameter(
        formulas, default=formulas[0], optimize=63 < CONDITIONS, space='sell')
    sell_formula64 = CategoricalParameter(
        formulas, default=formulas[0], optimize=64 < CONDITIONS, space='sell')
    sell_formula65 = CategoricalParameter(
        formulas, default=formulas[0], optimize=65 < CONDITIONS, space='sell')
    sell_formula66 = CategoricalParameter(
        formulas, default=formulas[0], optimize=66 < CONDITIONS, space='sell')
    sell_formula67 = CategoricalParameter(
        formulas, default=formulas[0], optimize=67 < CONDITIONS, space='sell')
    sell_formula68 = CategoricalParameter(
        formulas, default=formulas[0], optimize=68 < CONDITIONS, space='sell')
    sell_formula69 = CategoricalParameter(
        formulas, default=formulas[0], optimize=69 < CONDITIONS, space='sell')
    sell_formula70 = CategoricalParameter(
        formulas, default=formulas[0], optimize=70 < CONDITIONS, space='sell')
    sell_formula71 = CategoricalParameter(
        formulas, default=formulas[0], optimize=71 < CONDITIONS, space='sell')
    sell_formula72 = CategoricalParameter(
        formulas, default=formulas[0], optimize=72 < CONDITIONS, space='sell')
    sell_formula73 = CategoricalParameter(
        formulas, default=formulas[0], optimize=73 < CONDITIONS, space='sell')
    sell_formula74 = CategoricalParameter(
        formulas, default=formulas[0], optimize=74 < CONDITIONS, space='sell')
    sell_formula75 = CategoricalParameter(
        formulas, default=formulas[0], optimize=75 < CONDITIONS, space='sell')
    sell_formula76 = CategoricalParameter(
        formulas, default=formulas[0], optimize=76 < CONDITIONS, space='sell')
    sell_formula77 = CategoricalParameter(
        formulas, default=formulas[0], optimize=77 < CONDITIONS, space='sell')
    sell_formula78 = CategoricalParameter(
        formulas, default=formulas[0], optimize=78 < CONDITIONS, space='sell')
    sell_formula79 = CategoricalParameter(
        formulas, default=formulas[0], optimize=79 < CONDITIONS, space='sell')
    sell_formula80 = CategoricalParameter(
        formulas, default=formulas[0], optimize=80 < CONDITIONS, space='sell')
    sell_formula81 = CategoricalParameter(
        formulas, default=formulas[0], optimize=81 < CONDITIONS, space='sell')
    sell_formula82 = CategoricalParameter(
        formulas, default=formulas[0], optimize=82 < CONDITIONS, space='sell')
    sell_formula83 = CategoricalParameter(
        formulas, default=formulas[0], optimize=83 < CONDITIONS, space='sell')
    sell_formula84 = CategoricalParameter(
        formulas, default=formulas[0], optimize=84 < CONDITIONS, space='sell')
    sell_formula85 = CategoricalParameter(
        formulas, default=formulas[0], optimize=85 < CONDITIONS, space='sell')
    sell_formula86 = CategoricalParameter(
        formulas, default=formulas[0], optimize=86 < CONDITIONS, space='sell')
    sell_formula87 = CategoricalParameter(
        formulas, default=formulas[0], optimize=87 < CONDITIONS, space='sell')
    sell_formula88 = CategoricalParameter(
        formulas, default=formulas[0], optimize=88 < CONDITIONS, space='sell')
    sell_formula89 = CategoricalParameter(
        formulas, default=formulas[0], optimize=89 < CONDITIONS, space='sell')
    sell_formula90 = CategoricalParameter(
        formulas, default=formulas[0], optimize=90 < CONDITIONS, space='sell')
    sell_formula91 = CategoricalParameter(
        formulas, default=formulas[0], optimize=91 < CONDITIONS, space='sell')
    sell_formula92 = CategoricalParameter(
        formulas, default=formulas[0], optimize=92 < CONDITIONS, space='sell')
    sell_formula93 = CategoricalParameter(
        formulas, default=formulas[0], optimize=93 < CONDITIONS, space='sell')
    sell_formula94 = CategoricalParameter(
        formulas, default=formulas[0], optimize=94 < CONDITIONS, space='sell')
    sell_formula95 = CategoricalParameter(
        formulas, default=formulas[0], optimize=95 < CONDITIONS, space='sell')
    sell_formula96 = CategoricalParameter(
        formulas, default=formulas[0], optimize=96 < CONDITIONS, space='sell')
    sell_formula97 = CategoricalParameter(
        formulas, default=formulas[0], optimize=97 < CONDITIONS, space='sell')
    sell_formula98 = CategoricalParameter(
        formulas, default=formulas[0], optimize=98 < CONDITIONS, space='sell')
    sell_formula99 = CategoricalParameter(
        formulas, default=formulas[0], optimize=99 < CONDITIONS, space='sell')

    sell_indicator0 = CategoricalParameter(
        indicators, default=indicators[0], optimize=0 < CONDITIONS, space='sell')
    sell_indicator1 = CategoricalParameter(
        indicators, default=indicators[0], optimize=1 < CONDITIONS, space='sell')
    sell_indicator2 = CategoricalParameter(
        indicators, default=indicators[0], optimize=2 < CONDITIONS, space='sell')
    sell_indicator3 = CategoricalParameter(
        indicators, default=indicators[0], optimize=3 < CONDITIONS, space='sell')
    sell_indicator4 = CategoricalParameter(
        indicators, default=indicators[0], optimize=4 < CONDITIONS, space='sell')
    sell_indicator5 = CategoricalParameter(
        indicators, default=indicators[0], optimize=5 < CONDITIONS, space='sell')
    sell_indicator6 = CategoricalParameter(
        indicators, default=indicators[0], optimize=6 < CONDITIONS, space='sell')
    sell_indicator7 = CategoricalParameter(
        indicators, default=indicators[0], optimize=7 < CONDITIONS, space='sell')
    sell_indicator8 = CategoricalParameter(
        indicators, default=indicators[0], optimize=8 < CONDITIONS, space='sell')
    sell_indicator9 = CategoricalParameter(
        indicators, default=indicators[0], optimize=9 < CONDITIONS, space='sell')
    sell_indicator10 = CategoricalParameter(
        indicators, default=indicators[0], optimize=10 < CONDITIONS, space='sell')
    sell_indicator11 = CategoricalParameter(
        indicators, default=indicators[0], optimize=11 < CONDITIONS, space='sell')
    sell_indicator12 = CategoricalParameter(
        indicators, default=indicators[0], optimize=12 < CONDITIONS, space='sell')
    sell_indicator13 = CategoricalParameter(
        indicators, default=indicators[0], optimize=13 < CONDITIONS, space='sell')
    sell_indicator14 = CategoricalParameter(
        indicators, default=indicators[0], optimize=14 < CONDITIONS, space='sell')
    sell_indicator15 = CategoricalParameter(
        indicators, default=indicators[0], optimize=15 < CONDITIONS, space='sell')
    sell_indicator16 = CategoricalParameter(
        indicators, default=indicators[0], optimize=16 < CONDITIONS, space='sell')
    sell_indicator17 = CategoricalParameter(
        indicators, default=indicators[0], optimize=17 < CONDITIONS, space='sell')
    sell_indicator18 = CategoricalParameter(
        indicators, default=indicators[0], optimize=18 < CONDITIONS, space='sell')
    sell_indicator19 = CategoricalParameter(
        indicators, default=indicators[0], optimize=19 < CONDITIONS, space='sell')
    sell_indicator20 = CategoricalParameter(
        indicators, default=indicators[0], optimize=20 < CONDITIONS, space='sell')
    sell_indicator21 = CategoricalParameter(
        indicators, default=indicators[0], optimize=21 < CONDITIONS, space='sell')
    sell_indicator22 = CategoricalParameter(
        indicators, default=indicators[0], optimize=22 < CONDITIONS, space='sell')
    sell_indicator23 = CategoricalParameter(
        indicators, default=indicators[0], optimize=23 < CONDITIONS, space='sell')
    sell_indicator24 = CategoricalParameter(
        indicators, default=indicators[0], optimize=24 < CONDITIONS, space='sell')
    sell_indicator25 = CategoricalParameter(
        indicators, default=indicators[0], optimize=25 < CONDITIONS, space='sell')
    sell_indicator26 = CategoricalParameter(
        indicators, default=indicators[0], optimize=26 < CONDITIONS, space='sell')
    sell_indicator27 = CategoricalParameter(
        indicators, default=indicators[0], optimize=27 < CONDITIONS, space='sell')
    sell_indicator28 = CategoricalParameter(
        indicators, default=indicators[0], optimize=28 < CONDITIONS, space='sell')
    sell_indicator29 = CategoricalParameter(
        indicators, default=indicators[0], optimize=29 < CONDITIONS, space='sell')
    sell_indicator30 = CategoricalParameter(
        indicators, default=indicators[0], optimize=30 < CONDITIONS, space='sell')
    sell_indicator31 = CategoricalParameter(
        indicators, default=indicators[0], optimize=31 < CONDITIONS, space='sell')
    sell_indicator32 = CategoricalParameter(
        indicators, default=indicators[0], optimize=32 < CONDITIONS, space='sell')
    sell_indicator33 = CategoricalParameter(
        indicators, default=indicators[0], optimize=33 < CONDITIONS, space='sell')
    sell_indicator34 = CategoricalParameter(
        indicators, default=indicators[0], optimize=34 < CONDITIONS, space='sell')
    sell_indicator35 = CategoricalParameter(
        indicators, default=indicators[0], optimize=35 < CONDITIONS, space='sell')
    sell_indicator36 = CategoricalParameter(
        indicators, default=indicators[0], optimize=36 < CONDITIONS, space='sell')
    sell_indicator37 = CategoricalParameter(
        indicators, default=indicators[0], optimize=37 < CONDITIONS, space='sell')
    sell_indicator38 = CategoricalParameter(
        indicators, default=indicators[0], optimize=38 < CONDITIONS, space='sell')
    sell_indicator39 = CategoricalParameter(
        indicators, default=indicators[0], optimize=39 < CONDITIONS, space='sell')
    sell_indicator40 = CategoricalParameter(
        indicators, default=indicators[0], optimize=40 < CONDITIONS, space='sell')
    sell_indicator41 = CategoricalParameter(
        indicators, default=indicators[0], optimize=41 < CONDITIONS, space='sell')
    sell_indicator42 = CategoricalParameter(
        indicators, default=indicators[0], optimize=42 < CONDITIONS, space='sell')
    sell_indicator43 = CategoricalParameter(
        indicators, default=indicators[0], optimize=43 < CONDITIONS, space='sell')
    sell_indicator44 = CategoricalParameter(
        indicators, default=indicators[0], optimize=44 < CONDITIONS, space='sell')
    sell_indicator45 = CategoricalParameter(
        indicators, default=indicators[0], optimize=45 < CONDITIONS, space='sell')
    sell_indicator46 = CategoricalParameter(
        indicators, default=indicators[0], optimize=46 < CONDITIONS, space='sell')
    sell_indicator47 = CategoricalParameter(
        indicators, default=indicators[0], optimize=47 < CONDITIONS, space='sell')
    sell_indicator48 = CategoricalParameter(
        indicators, default=indicators[0], optimize=48 < CONDITIONS, space='sell')
    sell_indicator49 = CategoricalParameter(
        indicators, default=indicators[0], optimize=49 < CONDITIONS, space='sell')
    sell_indicator50 = CategoricalParameter(
        indicators, default=indicators[0], optimize=50 < CONDITIONS, space='sell')
    sell_indicator51 = CategoricalParameter(
        indicators, default=indicators[0], optimize=51 < CONDITIONS, space='sell')
    sell_indicator52 = CategoricalParameter(
        indicators, default=indicators[0], optimize=52 < CONDITIONS, space='sell')
    sell_indicator53 = CategoricalParameter(
        indicators, default=indicators[0], optimize=53 < CONDITIONS, space='sell')
    sell_indicator54 = CategoricalParameter(
        indicators, default=indicators[0], optimize=54 < CONDITIONS, space='sell')
    sell_indicator55 = CategoricalParameter(
        indicators, default=indicators[0], optimize=55 < CONDITIONS, space='sell')
    sell_indicator56 = CategoricalParameter(
        indicators, default=indicators[0], optimize=56 < CONDITIONS, space='sell')
    sell_indicator57 = CategoricalParameter(
        indicators, default=indicators[0], optimize=57 < CONDITIONS, space='sell')
    sell_indicator58 = CategoricalParameter(
        indicators, default=indicators[0], optimize=58 < CONDITIONS, space='sell')
    sell_indicator59 = CategoricalParameter(
        indicators, default=indicators[0], optimize=59 < CONDITIONS, space='sell')
    sell_indicator60 = CategoricalParameter(
        indicators, default=indicators[0], optimize=60 < CONDITIONS, space='sell')
    sell_indicator61 = CategoricalParameter(
        indicators, default=indicators[0], optimize=61 < CONDITIONS, space='sell')
    sell_indicator62 = CategoricalParameter(
        indicators, default=indicators[0], optimize=62 < CONDITIONS, space='sell')
    sell_indicator63 = CategoricalParameter(
        indicators, default=indicators[0], optimize=63 < CONDITIONS, space='sell')
    sell_indicator64 = CategoricalParameter(
        indicators, default=indicators[0], optimize=64 < CONDITIONS, space='sell')
    sell_indicator65 = CategoricalParameter(
        indicators, default=indicators[0], optimize=65 < CONDITIONS, space='sell')
    sell_indicator66 = CategoricalParameter(
        indicators, default=indicators[0], optimize=66 < CONDITIONS, space='sell')
    sell_indicator67 = CategoricalParameter(
        indicators, default=indicators[0], optimize=67 < CONDITIONS, space='sell')
    sell_indicator68 = CategoricalParameter(
        indicators, default=indicators[0], optimize=68 < CONDITIONS, space='sell')
    sell_indicator69 = CategoricalParameter(
        indicators, default=indicators[0], optimize=69 < CONDITIONS, space='sell')
    sell_indicator70 = CategoricalParameter(
        indicators, default=indicators[0], optimize=70 < CONDITIONS, space='sell')
    sell_indicator71 = CategoricalParameter(
        indicators, default=indicators[0], optimize=71 < CONDITIONS, space='sell')
    sell_indicator72 = CategoricalParameter(
        indicators, default=indicators[0], optimize=72 < CONDITIONS, space='sell')
    sell_indicator73 = CategoricalParameter(
        indicators, default=indicators[0], optimize=73 < CONDITIONS, space='sell')
    sell_indicator74 = CategoricalParameter(
        indicators, default=indicators[0], optimize=74 < CONDITIONS, space='sell')
    sell_indicator75 = CategoricalParameter(
        indicators, default=indicators[0], optimize=75 < CONDITIONS, space='sell')
    sell_indicator76 = CategoricalParameter(
        indicators, default=indicators[0], optimize=76 < CONDITIONS, space='sell')
    sell_indicator77 = CategoricalParameter(
        indicators, default=indicators[0], optimize=77 < CONDITIONS, space='sell')
    sell_indicator78 = CategoricalParameter(
        indicators, default=indicators[0], optimize=78 < CONDITIONS, space='sell')
    sell_indicator79 = CategoricalParameter(
        indicators, default=indicators[0], optimize=79 < CONDITIONS, space='sell')
    sell_indicator80 = CategoricalParameter(
        indicators, default=indicators[0], optimize=80 < CONDITIONS, space='sell')
    sell_indicator81 = CategoricalParameter(
        indicators, default=indicators[0], optimize=81 < CONDITIONS, space='sell')
    sell_indicator82 = CategoricalParameter(
        indicators, default=indicators[0], optimize=82 < CONDITIONS, space='sell')
    sell_indicator83 = CategoricalParameter(
        indicators, default=indicators[0], optimize=83 < CONDITIONS, space='sell')
    sell_indicator84 = CategoricalParameter(
        indicators, default=indicators[0], optimize=84 < CONDITIONS, space='sell')
    sell_indicator85 = CategoricalParameter(
        indicators, default=indicators[0], optimize=85 < CONDITIONS, space='sell')
    sell_indicator86 = CategoricalParameter(
        indicators, default=indicators[0], optimize=86 < CONDITIONS, space='sell')
    sell_indicator87 = CategoricalParameter(
        indicators, default=indicators[0], optimize=87 < CONDITIONS, space='sell')
    sell_indicator88 = CategoricalParameter(
        indicators, default=indicators[0], optimize=88 < CONDITIONS, space='sell')
    sell_indicator89 = CategoricalParameter(
        indicators, default=indicators[0], optimize=89 < CONDITIONS, space='sell')
    sell_indicator90 = CategoricalParameter(
        indicators, default=indicators[0], optimize=90 < CONDITIONS, space='sell')
    sell_indicator91 = CategoricalParameter(
        indicators, default=indicators[0], optimize=91 < CONDITIONS, space='sell')
    sell_indicator92 = CategoricalParameter(
        indicators, default=indicators[0], optimize=92 < CONDITIONS, space='sell')
    sell_indicator93 = CategoricalParameter(
        indicators, default=indicators[0], optimize=93 < CONDITIONS, space='sell')
    sell_indicator94 = CategoricalParameter(
        indicators, default=indicators[0], optimize=94 < CONDITIONS, space='sell')
    sell_indicator95 = CategoricalParameter(
        indicators, default=indicators[0], optimize=95 < CONDITIONS, space='sell')
    sell_indicator96 = CategoricalParameter(
        indicators, default=indicators[0], optimize=96 < CONDITIONS, space='sell')
    sell_indicator97 = CategoricalParameter(
        indicators, default=indicators[0], optimize=97 < CONDITIONS, space='sell')
    sell_indicator98 = CategoricalParameter(
        indicators, default=indicators[0], optimize=98 < CONDITIONS, space='sell')
    sell_indicator99 = CategoricalParameter(
        indicators, default=indicators[0], optimize=99 < CONDITIONS, space='sell')

    sell_crossed0 = CategoricalParameter(
        indicators, default=indicators[0], optimize=0 < CONDITIONS, space='sell')
    sell_crossed1 = CategoricalParameter(
        indicators, default=indicators[0], optimize=1 < CONDITIONS, space='sell')
    sell_crossed2 = CategoricalParameter(
        indicators, default=indicators[0], optimize=2 < CONDITIONS, space='sell')
    sell_crossed3 = CategoricalParameter(
        indicators, default=indicators[0], optimize=3 < CONDITIONS, space='sell')
    sell_crossed4 = CategoricalParameter(
        indicators, default=indicators[0], optimize=4 < CONDITIONS, space='sell')
    sell_crossed5 = CategoricalParameter(
        indicators, default=indicators[0], optimize=5 < CONDITIONS, space='sell')
    sell_crossed6 = CategoricalParameter(
        indicators, default=indicators[0], optimize=6 < CONDITIONS, space='sell')
    sell_crossed7 = CategoricalParameter(
        indicators, default=indicators[0], optimize=7 < CONDITIONS, space='sell')
    sell_crossed8 = CategoricalParameter(
        indicators, default=indicators[0], optimize=8 < CONDITIONS, space='sell')
    sell_crossed9 = CategoricalParameter(
        indicators, default=indicators[0], optimize=9 < CONDITIONS, space='sell')
    sell_crossed10 = CategoricalParameter(
        indicators, default=indicators[0], optimize=10 < CONDITIONS, space='sell')
    sell_crossed11 = CategoricalParameter(
        indicators, default=indicators[0], optimize=11 < CONDITIONS, space='sell')
    sell_crossed12 = CategoricalParameter(
        indicators, default=indicators[0], optimize=12 < CONDITIONS, space='sell')
    sell_crossed13 = CategoricalParameter(
        indicators, default=indicators[0], optimize=13 < CONDITIONS, space='sell')
    sell_crossed14 = CategoricalParameter(
        indicators, default=indicators[0], optimize=14 < CONDITIONS, space='sell')
    sell_crossed15 = CategoricalParameter(
        indicators, default=indicators[0], optimize=15 < CONDITIONS, space='sell')
    sell_crossed16 = CategoricalParameter(
        indicators, default=indicators[0], optimize=16 < CONDITIONS, space='sell')
    sell_crossed17 = CategoricalParameter(
        indicators, default=indicators[0], optimize=17 < CONDITIONS, space='sell')
    sell_crossed18 = CategoricalParameter(
        indicators, default=indicators[0], optimize=18 < CONDITIONS, space='sell')
    sell_crossed19 = CategoricalParameter(
        indicators, default=indicators[0], optimize=19 < CONDITIONS, space='sell')
    sell_crossed20 = CategoricalParameter(
        indicators, default=indicators[0], optimize=20 < CONDITIONS, space='sell')
    sell_crossed21 = CategoricalParameter(
        indicators, default=indicators[0], optimize=21 < CONDITIONS, space='sell')
    sell_crossed22 = CategoricalParameter(
        indicators, default=indicators[0], optimize=22 < CONDITIONS, space='sell')
    sell_crossed23 = CategoricalParameter(
        indicators, default=indicators[0], optimize=23 < CONDITIONS, space='sell')
    sell_crossed24 = CategoricalParameter(
        indicators, default=indicators[0], optimize=24 < CONDITIONS, space='sell')
    sell_crossed25 = CategoricalParameter(
        indicators, default=indicators[0], optimize=25 < CONDITIONS, space='sell')
    sell_crossed26 = CategoricalParameter(
        indicators, default=indicators[0], optimize=26 < CONDITIONS, space='sell')
    sell_crossed27 = CategoricalParameter(
        indicators, default=indicators[0], optimize=27 < CONDITIONS, space='sell')
    sell_crossed28 = CategoricalParameter(
        indicators, default=indicators[0], optimize=28 < CONDITIONS, space='sell')
    sell_crossed29 = CategoricalParameter(
        indicators, default=indicators[0], optimize=29 < CONDITIONS, space='sell')
    sell_crossed30 = CategoricalParameter(
        indicators, default=indicators[0], optimize=30 < CONDITIONS, space='sell')
    sell_crossed31 = CategoricalParameter(
        indicators, default=indicators[0], optimize=31 < CONDITIONS, space='sell')
    sell_crossed32 = CategoricalParameter(
        indicators, default=indicators[0], optimize=32 < CONDITIONS, space='sell')
    sell_crossed33 = CategoricalParameter(
        indicators, default=indicators[0], optimize=33 < CONDITIONS, space='sell')
    sell_crossed34 = CategoricalParameter(
        indicators, default=indicators[0], optimize=34 < CONDITIONS, space='sell')
    sell_crossed35 = CategoricalParameter(
        indicators, default=indicators[0], optimize=35 < CONDITIONS, space='sell')
    sell_crossed36 = CategoricalParameter(
        indicators, default=indicators[0], optimize=36 < CONDITIONS, space='sell')
    sell_crossed37 = CategoricalParameter(
        indicators, default=indicators[0], optimize=37 < CONDITIONS, space='sell')
    sell_crossed38 = CategoricalParameter(
        indicators, default=indicators[0], optimize=38 < CONDITIONS, space='sell')
    sell_crossed39 = CategoricalParameter(
        indicators, default=indicators[0], optimize=39 < CONDITIONS, space='sell')
    sell_crossed40 = CategoricalParameter(
        indicators, default=indicators[0], optimize=40 < CONDITIONS, space='sell')
    sell_crossed41 = CategoricalParameter(
        indicators, default=indicators[0], optimize=41 < CONDITIONS, space='sell')
    sell_crossed42 = CategoricalParameter(
        indicators, default=indicators[0], optimize=42 < CONDITIONS, space='sell')
    sell_crossed43 = CategoricalParameter(
        indicators, default=indicators[0], optimize=43 < CONDITIONS, space='sell')
    sell_crossed44 = CategoricalParameter(
        indicators, default=indicators[0], optimize=44 < CONDITIONS, space='sell')
    sell_crossed45 = CategoricalParameter(
        indicators, default=indicators[0], optimize=45 < CONDITIONS, space='sell')
    sell_crossed46 = CategoricalParameter(
        indicators, default=indicators[0], optimize=46 < CONDITIONS, space='sell')
    sell_crossed47 = CategoricalParameter(
        indicators, default=indicators[0], optimize=47 < CONDITIONS, space='sell')
    sell_crossed48 = CategoricalParameter(
        indicators, default=indicators[0], optimize=48 < CONDITIONS, space='sell')
    sell_crossed49 = CategoricalParameter(
        indicators, default=indicators[0], optimize=49 < CONDITIONS, space='sell')
    sell_crossed50 = CategoricalParameter(
        indicators, default=indicators[0], optimize=50 < CONDITIONS, space='sell')
    sell_crossed51 = CategoricalParameter(
        indicators, default=indicators[0], optimize=51 < CONDITIONS, space='sell')
    sell_crossed52 = CategoricalParameter(
        indicators, default=indicators[0], optimize=52 < CONDITIONS, space='sell')
    sell_crossed53 = CategoricalParameter(
        indicators, default=indicators[0], optimize=53 < CONDITIONS, space='sell')
    sell_crossed54 = CategoricalParameter(
        indicators, default=indicators[0], optimize=54 < CONDITIONS, space='sell')
    sell_crossed55 = CategoricalParameter(
        indicators, default=indicators[0], optimize=55 < CONDITIONS, space='sell')
    sell_crossed56 = CategoricalParameter(
        indicators, default=indicators[0], optimize=56 < CONDITIONS, space='sell')
    sell_crossed57 = CategoricalParameter(
        indicators, default=indicators[0], optimize=57 < CONDITIONS, space='sell')
    sell_crossed58 = CategoricalParameter(
        indicators, default=indicators[0], optimize=58 < CONDITIONS, space='sell')
    sell_crossed59 = CategoricalParameter(
        indicators, default=indicators[0], optimize=59 < CONDITIONS, space='sell')
    sell_crossed60 = CategoricalParameter(
        indicators, default=indicators[0], optimize=60 < CONDITIONS, space='sell')
    sell_crossed61 = CategoricalParameter(
        indicators, default=indicators[0], optimize=61 < CONDITIONS, space='sell')
    sell_crossed62 = CategoricalParameter(
        indicators, default=indicators[0], optimize=62 < CONDITIONS, space='sell')
    sell_crossed63 = CategoricalParameter(
        indicators, default=indicators[0], optimize=63 < CONDITIONS, space='sell')
    sell_crossed64 = CategoricalParameter(
        indicators, default=indicators[0], optimize=64 < CONDITIONS, space='sell')
    sell_crossed65 = CategoricalParameter(
        indicators, default=indicators[0], optimize=65 < CONDITIONS, space='sell')
    sell_crossed66 = CategoricalParameter(
        indicators, default=indicators[0], optimize=66 < CONDITIONS, space='sell')
    sell_crossed67 = CategoricalParameter(
        indicators, default=indicators[0], optimize=67 < CONDITIONS, space='sell')
    sell_crossed68 = CategoricalParameter(
        indicators, default=indicators[0], optimize=68 < CONDITIONS, space='sell')
    sell_crossed69 = CategoricalParameter(
        indicators, default=indicators[0], optimize=69 < CONDITIONS, space='sell')
    sell_crossed70 = CategoricalParameter(
        indicators, default=indicators[0], optimize=70 < CONDITIONS, space='sell')
    sell_crossed71 = CategoricalParameter(
        indicators, default=indicators[0], optimize=71 < CONDITIONS, space='sell')
    sell_crossed72 = CategoricalParameter(
        indicators, default=indicators[0], optimize=72 < CONDITIONS, space='sell')
    sell_crossed73 = CategoricalParameter(
        indicators, default=indicators[0], optimize=73 < CONDITIONS, space='sell')
    sell_crossed74 = CategoricalParameter(
        indicators, default=indicators[0], optimize=74 < CONDITIONS, space='sell')
    sell_crossed75 = CategoricalParameter(
        indicators, default=indicators[0], optimize=75 < CONDITIONS, space='sell')
    sell_crossed76 = CategoricalParameter(
        indicators, default=indicators[0], optimize=76 < CONDITIONS, space='sell')
    sell_crossed77 = CategoricalParameter(
        indicators, default=indicators[0], optimize=77 < CONDITIONS, space='sell')
    sell_crossed78 = CategoricalParameter(
        indicators, default=indicators[0], optimize=78 < CONDITIONS, space='sell')
    sell_crossed79 = CategoricalParameter(
        indicators, default=indicators[0], optimize=79 < CONDITIONS, space='sell')
    sell_crossed80 = CategoricalParameter(
        indicators, default=indicators[0], optimize=80 < CONDITIONS, space='sell')
    sell_crossed81 = CategoricalParameter(
        indicators, default=indicators[0], optimize=81 < CONDITIONS, space='sell')
    sell_crossed82 = CategoricalParameter(
        indicators, default=indicators[0], optimize=82 < CONDITIONS, space='sell')
    sell_crossed83 = CategoricalParameter(
        indicators, default=indicators[0], optimize=83 < CONDITIONS, space='sell')
    sell_crossed84 = CategoricalParameter(
        indicators, default=indicators[0], optimize=84 < CONDITIONS, space='sell')
    sell_crossed85 = CategoricalParameter(
        indicators, default=indicators[0], optimize=85 < CONDITIONS, space='sell')
    sell_crossed86 = CategoricalParameter(
        indicators, default=indicators[0], optimize=86 < CONDITIONS, space='sell')
    sell_crossed87 = CategoricalParameter(
        indicators, default=indicators[0], optimize=87 < CONDITIONS, space='sell')
    sell_crossed88 = CategoricalParameter(
        indicators, default=indicators[0], optimize=88 < CONDITIONS, space='sell')
    sell_crossed89 = CategoricalParameter(
        indicators, default=indicators[0], optimize=89 < CONDITIONS, space='sell')
    sell_crossed90 = CategoricalParameter(
        indicators, default=indicators[0], optimize=90 < CONDITIONS, space='sell')
    sell_crossed91 = CategoricalParameter(
        indicators, default=indicators[0], optimize=91 < CONDITIONS, space='sell')
    sell_crossed92 = CategoricalParameter(
        indicators, default=indicators[0], optimize=92 < CONDITIONS, space='sell')
    sell_crossed93 = CategoricalParameter(
        indicators, default=indicators[0], optimize=93 < CONDITIONS, space='sell')
    sell_crossed94 = CategoricalParameter(
        indicators, default=indicators[0], optimize=94 < CONDITIONS, space='sell')
    sell_crossed95 = CategoricalParameter(
        indicators, default=indicators[0], optimize=95 < CONDITIONS, space='sell')
    sell_crossed96 = CategoricalParameter(
        indicators, default=indicators[0], optimize=96 < CONDITIONS, space='sell')
    sell_crossed97 = CategoricalParameter(
        indicators, default=indicators[0], optimize=97 < CONDITIONS, space='sell')
    sell_crossed98 = CategoricalParameter(
        indicators, default=indicators[0], optimize=98 < CONDITIONS, space='sell')
    sell_crossed99 = CategoricalParameter(
        indicators, default=indicators[0], optimize=99 < CONDITIONS, space='sell')

    sell_timeframe0 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=0 < CONDITIONS, space='sell')
    sell_timeframe1 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=1 < CONDITIONS, space='sell')
    sell_timeframe2 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=2 < CONDITIONS, space='sell')
    sell_timeframe3 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=3 < CONDITIONS, space='sell')
    sell_timeframe4 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=4 < CONDITIONS, space='sell')
    sell_timeframe5 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=5 < CONDITIONS, space='sell')
    sell_timeframe6 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=6 < CONDITIONS, space='sell')
    sell_timeframe7 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=7 < CONDITIONS, space='sell')
    sell_timeframe8 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=8 < CONDITIONS, space='sell')
    sell_timeframe9 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=9 < CONDITIONS, space='sell')
    sell_timeframe10 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=10 < CONDITIONS, space='sell')
    sell_timeframe11 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=11 < CONDITIONS, space='sell')
    sell_timeframe12 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=12 < CONDITIONS, space='sell')
    sell_timeframe13 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=13 < CONDITIONS, space='sell')
    sell_timeframe14 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=14 < CONDITIONS, space='sell')
    sell_timeframe15 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=15 < CONDITIONS, space='sell')
    sell_timeframe16 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=16 < CONDITIONS, space='sell')
    sell_timeframe17 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=17 < CONDITIONS, space='sell')
    sell_timeframe18 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=18 < CONDITIONS, space='sell')
    sell_timeframe19 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=19 < CONDITIONS, space='sell')
    sell_timeframe20 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=20 < CONDITIONS, space='sell')
    sell_timeframe21 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=21 < CONDITIONS, space='sell')
    sell_timeframe22 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=22 < CONDITIONS, space='sell')
    sell_timeframe23 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=23 < CONDITIONS, space='sell')
    sell_timeframe24 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=24 < CONDITIONS, space='sell')
    sell_timeframe25 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=25 < CONDITIONS, space='sell')
    sell_timeframe26 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=26 < CONDITIONS, space='sell')
    sell_timeframe27 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=27 < CONDITIONS, space='sell')
    sell_timeframe28 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=28 < CONDITIONS, space='sell')
    sell_timeframe29 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=29 < CONDITIONS, space='sell')
    sell_timeframe30 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=30 < CONDITIONS, space='sell')
    sell_timeframe31 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=31 < CONDITIONS, space='sell')
    sell_timeframe32 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=32 < CONDITIONS, space='sell')
    sell_timeframe33 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=33 < CONDITIONS, space='sell')
    sell_timeframe34 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=34 < CONDITIONS, space='sell')
    sell_timeframe35 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=35 < CONDITIONS, space='sell')
    sell_timeframe36 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=36 < CONDITIONS, space='sell')
    sell_timeframe37 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=37 < CONDITIONS, space='sell')
    sell_timeframe38 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=38 < CONDITIONS, space='sell')
    sell_timeframe39 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=39 < CONDITIONS, space='sell')
    sell_timeframe40 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=40 < CONDITIONS, space='sell')
    sell_timeframe41 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=41 < CONDITIONS, space='sell')
    sell_timeframe42 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=42 < CONDITIONS, space='sell')
    sell_timeframe43 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=43 < CONDITIONS, space='sell')
    sell_timeframe44 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=44 < CONDITIONS, space='sell')
    sell_timeframe45 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=45 < CONDITIONS, space='sell')
    sell_timeframe46 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=46 < CONDITIONS, space='sell')
    sell_timeframe47 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=47 < CONDITIONS, space='sell')
    sell_timeframe48 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=48 < CONDITIONS, space='sell')
    sell_timeframe49 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=49 < CONDITIONS, space='sell')
    sell_timeframe50 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=50 < CONDITIONS, space='sell')
    sell_timeframe51 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=51 < CONDITIONS, space='sell')
    sell_timeframe52 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=52 < CONDITIONS, space='sell')
    sell_timeframe53 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=53 < CONDITIONS, space='sell')
    sell_timeframe54 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=54 < CONDITIONS, space='sell')
    sell_timeframe55 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=55 < CONDITIONS, space='sell')
    sell_timeframe56 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=56 < CONDITIONS, space='sell')
    sell_timeframe57 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=57 < CONDITIONS, space='sell')
    sell_timeframe58 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=58 < CONDITIONS, space='sell')
    sell_timeframe59 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=59 < CONDITIONS, space='sell')
    sell_timeframe60 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=60 < CONDITIONS, space='sell')
    sell_timeframe61 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=61 < CONDITIONS, space='sell')
    sell_timeframe62 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=62 < CONDITIONS, space='sell')
    sell_timeframe63 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=63 < CONDITIONS, space='sell')
    sell_timeframe64 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=64 < CONDITIONS, space='sell')
    sell_timeframe65 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=65 < CONDITIONS, space='sell')
    sell_timeframe66 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=66 < CONDITIONS, space='sell')
    sell_timeframe67 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=67 < CONDITIONS, space='sell')
    sell_timeframe68 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=68 < CONDITIONS, space='sell')
    sell_timeframe69 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=69 < CONDITIONS, space='sell')
    sell_timeframe70 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=70 < CONDITIONS, space='sell')
    sell_timeframe71 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=71 < CONDITIONS, space='sell')
    sell_timeframe72 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=72 < CONDITIONS, space='sell')
    sell_timeframe73 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=73 < CONDITIONS, space='sell')
    sell_timeframe74 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=74 < CONDITIONS, space='sell')
    sell_timeframe75 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=75 < CONDITIONS, space='sell')
    sell_timeframe76 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=76 < CONDITIONS, space='sell')
    sell_timeframe77 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=77 < CONDITIONS, space='sell')
    sell_timeframe78 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=78 < CONDITIONS, space='sell')
    sell_timeframe79 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=79 < CONDITIONS, space='sell')
    sell_timeframe80 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=80 < CONDITIONS, space='sell')
    sell_timeframe81 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=81 < CONDITIONS, space='sell')
    sell_timeframe82 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=82 < CONDITIONS, space='sell')
    sell_timeframe83 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=83 < CONDITIONS, space='sell')
    sell_timeframe84 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=84 < CONDITIONS, space='sell')
    sell_timeframe85 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=85 < CONDITIONS, space='sell')
    sell_timeframe86 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=86 < CONDITIONS, space='sell')
    sell_timeframe87 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=87 < CONDITIONS, space='sell')
    sell_timeframe88 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=88 < CONDITIONS, space='sell')
    sell_timeframe89 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=89 < CONDITIONS, space='sell')
    sell_timeframe90 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=90 < CONDITIONS, space='sell')
    sell_timeframe91 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=91 < CONDITIONS, space='sell')
    sell_timeframe92 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=92 < CONDITIONS, space='sell')
    sell_timeframe93 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=93 < CONDITIONS, space='sell')
    sell_timeframe94 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=94 < CONDITIONS, space='sell')
    sell_timeframe95 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=95 < CONDITIONS, space='sell')
    sell_timeframe96 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=96 < CONDITIONS, space='sell')
    sell_timeframe97 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=97 < CONDITIONS, space='sell')
    sell_timeframe98 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=98 < CONDITIONS, space='sell')
    sell_timeframe99 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=99 < CONDITIONS, space='sell')

    sell_crossed_timeframe0 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=0 < CONDITIONS, space='sell')
    sell_crossed_timeframe1 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=1 < CONDITIONS, space='sell')
    sell_crossed_timeframe2 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=2 < CONDITIONS, space='sell')
    sell_crossed_timeframe3 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=3 < CONDITIONS, space='sell')
    sell_crossed_timeframe4 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=4 < CONDITIONS, space='sell')
    sell_crossed_timeframe5 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=5 < CONDITIONS, space='sell')
    sell_crossed_timeframe6 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=6 < CONDITIONS, space='sell')
    sell_crossed_timeframe7 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=7 < CONDITIONS, space='sell')
    sell_crossed_timeframe8 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=8 < CONDITIONS, space='sell')
    sell_crossed_timeframe9 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=9 < CONDITIONS, space='sell')
    sell_crossed_timeframe10 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=10 < CONDITIONS, space='sell')
    sell_crossed_timeframe11 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=11 < CONDITIONS, space='sell')
    sell_crossed_timeframe12 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=12 < CONDITIONS, space='sell')
    sell_crossed_timeframe13 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=13 < CONDITIONS, space='sell')
    sell_crossed_timeframe14 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=14 < CONDITIONS, space='sell')
    sell_crossed_timeframe15 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=15 < CONDITIONS, space='sell')
    sell_crossed_timeframe16 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=16 < CONDITIONS, space='sell')
    sell_crossed_timeframe17 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=17 < CONDITIONS, space='sell')
    sell_crossed_timeframe18 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=18 < CONDITIONS, space='sell')
    sell_crossed_timeframe19 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=19 < CONDITIONS, space='sell')
    sell_crossed_timeframe20 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=20 < CONDITIONS, space='sell')
    sell_crossed_timeframe21 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=21 < CONDITIONS, space='sell')
    sell_crossed_timeframe22 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=22 < CONDITIONS, space='sell')
    sell_crossed_timeframe23 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=23 < CONDITIONS, space='sell')
    sell_crossed_timeframe24 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=24 < CONDITIONS, space='sell')
    sell_crossed_timeframe25 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=25 < CONDITIONS, space='sell')
    sell_crossed_timeframe26 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=26 < CONDITIONS, space='sell')
    sell_crossed_timeframe27 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=27 < CONDITIONS, space='sell')
    sell_crossed_timeframe28 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=28 < CONDITIONS, space='sell')
    sell_crossed_timeframe29 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=29 < CONDITIONS, space='sell')
    sell_crossed_timeframe30 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=30 < CONDITIONS, space='sell')
    sell_crossed_timeframe31 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=31 < CONDITIONS, space='sell')
    sell_crossed_timeframe32 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=32 < CONDITIONS, space='sell')
    sell_crossed_timeframe33 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=33 < CONDITIONS, space='sell')
    sell_crossed_timeframe34 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=34 < CONDITIONS, space='sell')
    sell_crossed_timeframe35 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=35 < CONDITIONS, space='sell')
    sell_crossed_timeframe36 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=36 < CONDITIONS, space='sell')
    sell_crossed_timeframe37 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=37 < CONDITIONS, space='sell')
    sell_crossed_timeframe38 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=38 < CONDITIONS, space='sell')
    sell_crossed_timeframe39 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=39 < CONDITIONS, space='sell')
    sell_crossed_timeframe40 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=40 < CONDITIONS, space='sell')
    sell_crossed_timeframe41 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=41 < CONDITIONS, space='sell')
    sell_crossed_timeframe42 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=42 < CONDITIONS, space='sell')
    sell_crossed_timeframe43 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=43 < CONDITIONS, space='sell')
    sell_crossed_timeframe44 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=44 < CONDITIONS, space='sell')
    sell_crossed_timeframe45 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=45 < CONDITIONS, space='sell')
    sell_crossed_timeframe46 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=46 < CONDITIONS, space='sell')
    sell_crossed_timeframe47 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=47 < CONDITIONS, space='sell')
    sell_crossed_timeframe48 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=48 < CONDITIONS, space='sell')
    sell_crossed_timeframe49 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=49 < CONDITIONS, space='sell')
    sell_crossed_timeframe50 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=50 < CONDITIONS, space='sell')
    sell_crossed_timeframe51 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=51 < CONDITIONS, space='sell')
    sell_crossed_timeframe52 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=52 < CONDITIONS, space='sell')
    sell_crossed_timeframe53 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=53 < CONDITIONS, space='sell')
    sell_crossed_timeframe54 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=54 < CONDITIONS, space='sell')
    sell_crossed_timeframe55 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=55 < CONDITIONS, space='sell')
    sell_crossed_timeframe56 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=56 < CONDITIONS, space='sell')
    sell_crossed_timeframe57 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=57 < CONDITIONS, space='sell')
    sell_crossed_timeframe58 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=58 < CONDITIONS, space='sell')
    sell_crossed_timeframe59 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=59 < CONDITIONS, space='sell')
    sell_crossed_timeframe60 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=60 < CONDITIONS, space='sell')
    sell_crossed_timeframe61 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=61 < CONDITIONS, space='sell')
    sell_crossed_timeframe62 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=62 < CONDITIONS, space='sell')
    sell_crossed_timeframe63 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=63 < CONDITIONS, space='sell')
    sell_crossed_timeframe64 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=64 < CONDITIONS, space='sell')
    sell_crossed_timeframe65 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=65 < CONDITIONS, space='sell')
    sell_crossed_timeframe66 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=66 < CONDITIONS, space='sell')
    sell_crossed_timeframe67 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=67 < CONDITIONS, space='sell')
    sell_crossed_timeframe68 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=68 < CONDITIONS, space='sell')
    sell_crossed_timeframe69 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=69 < CONDITIONS, space='sell')
    sell_crossed_timeframe70 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=70 < CONDITIONS, space='sell')
    sell_crossed_timeframe71 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=71 < CONDITIONS, space='sell')
    sell_crossed_timeframe72 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=72 < CONDITIONS, space='sell')
    sell_crossed_timeframe73 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=73 < CONDITIONS, space='sell')
    sell_crossed_timeframe74 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=74 < CONDITIONS, space='sell')
    sell_crossed_timeframe75 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=75 < CONDITIONS, space='sell')
    sell_crossed_timeframe76 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=76 < CONDITIONS, space='sell')
    sell_crossed_timeframe77 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=77 < CONDITIONS, space='sell')
    sell_crossed_timeframe78 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=78 < CONDITIONS, space='sell')
    sell_crossed_timeframe79 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=79 < CONDITIONS, space='sell')
    sell_crossed_timeframe80 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=80 < CONDITIONS, space='sell')
    sell_crossed_timeframe81 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=81 < CONDITIONS, space='sell')
    sell_crossed_timeframe82 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=82 < CONDITIONS, space='sell')
    sell_crossed_timeframe83 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=83 < CONDITIONS, space='sell')
    sell_crossed_timeframe84 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=84 < CONDITIONS, space='sell')
    sell_crossed_timeframe85 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=85 < CONDITIONS, space='sell')
    sell_crossed_timeframe86 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=86 < CONDITIONS, space='sell')
    sell_crossed_timeframe87 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=87 < CONDITIONS, space='sell')
    sell_crossed_timeframe88 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=88 < CONDITIONS, space='sell')
    sell_crossed_timeframe89 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=89 < CONDITIONS, space='sell')
    sell_crossed_timeframe90 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=90 < CONDITIONS, space='sell')
    sell_crossed_timeframe91 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=91 < CONDITIONS, space='sell')
    sell_crossed_timeframe92 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=92 < CONDITIONS, space='sell')
    sell_crossed_timeframe93 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=93 < CONDITIONS, space='sell')
    sell_crossed_timeframe94 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=94 < CONDITIONS, space='sell')
    sell_crossed_timeframe95 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=95 < CONDITIONS, space='sell')
    sell_crossed_timeframe96 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=96 < CONDITIONS, space='sell')
    sell_crossed_timeframe97 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=97 < CONDITIONS, space='sell')
    sell_crossed_timeframe98 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=98 < CONDITIONS, space='sell')
    sell_crossed_timeframe99 = CategoricalParameter(timeframes, default=timeframes[0], optimize=0 < CONDITIONS, space='sell')if COSTUMETFENABLED else IntParameter(
        timeframes[0], timeframes[-1], default=timeframes[0], optimize=99 < CONDITIONS, space='sell')

    sell_real0 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=0 < CONDITIONS, space='sell')
    sell_real1 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=1 < CONDITIONS, space='sell')
    sell_real2 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=2 < CONDITIONS, space='sell')
    sell_real3 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=3 < CONDITIONS, space='sell')
    sell_real4 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=4 < CONDITIONS, space='sell')
    sell_real5 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=5 < CONDITIONS, space='sell')
    sell_real6 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=6 < CONDITIONS, space='sell')
    sell_real7 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=7 < CONDITIONS, space='sell')
    sell_real8 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=8 < CONDITIONS, space='sell')
    sell_real9 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=9 < CONDITIONS, space='sell')
    sell_real10 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=10 < CONDITIONS, space='sell')
    sell_real11 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=11 < CONDITIONS, space='sell')
    sell_real12 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=12 < CONDITIONS, space='sell')
    sell_real13 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=13 < CONDITIONS, space='sell')
    sell_real14 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=14 < CONDITIONS, space='sell')
    sell_real15 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=15 < CONDITIONS, space='sell')
    sell_real16 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=16 < CONDITIONS, space='sell')
    sell_real17 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=17 < CONDITIONS, space='sell')
    sell_real18 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=18 < CONDITIONS, space='sell')
    sell_real19 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=19 < CONDITIONS, space='sell')
    sell_real20 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=20 < CONDITIONS, space='sell')
    sell_real21 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=21 < CONDITIONS, space='sell')
    sell_real22 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=22 < CONDITIONS, space='sell')
    sell_real23 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=23 < CONDITIONS, space='sell')
    sell_real24 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=24 < CONDITIONS, space='sell')
    sell_real25 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=25 < CONDITIONS, space='sell')
    sell_real26 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=26 < CONDITIONS, space='sell')
    sell_real27 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=27 < CONDITIONS, space='sell')
    sell_real28 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=28 < CONDITIONS, space='sell')
    sell_real29 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=29 < CONDITIONS, space='sell')
    sell_real30 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=30 < CONDITIONS, space='sell')
    sell_real31 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=31 < CONDITIONS, space='sell')
    sell_real32 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=32 < CONDITIONS, space='sell')
    sell_real33 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=33 < CONDITIONS, space='sell')
    sell_real34 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=34 < CONDITIONS, space='sell')
    sell_real35 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=35 < CONDITIONS, space='sell')
    sell_real36 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=36 < CONDITIONS, space='sell')
    sell_real37 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=37 < CONDITIONS, space='sell')
    sell_real38 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=38 < CONDITIONS, space='sell')
    sell_real39 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=39 < CONDITIONS, space='sell')
    sell_real40 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=40 < CONDITIONS, space='sell')
    sell_real41 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=41 < CONDITIONS, space='sell')
    sell_real42 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=42 < CONDITIONS, space='sell')
    sell_real43 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=43 < CONDITIONS, space='sell')
    sell_real44 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=44 < CONDITIONS, space='sell')
    sell_real45 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=45 < CONDITIONS, space='sell')
    sell_real46 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=46 < CONDITIONS, space='sell')
    sell_real47 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=47 < CONDITIONS, space='sell')
    sell_real48 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=48 < CONDITIONS, space='sell')
    sell_real49 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=49 < CONDITIONS, space='sell')
    sell_real50 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=50 < CONDITIONS, space='sell')
    sell_real51 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=51 < CONDITIONS, space='sell')
    sell_real52 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=52 < CONDITIONS, space='sell')
    sell_real53 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=53 < CONDITIONS, space='sell')
    sell_real54 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=54 < CONDITIONS, space='sell')
    sell_real55 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=55 < CONDITIONS, space='sell')
    sell_real56 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=56 < CONDITIONS, space='sell')
    sell_real57 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=57 < CONDITIONS, space='sell')
    sell_real58 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=58 < CONDITIONS, space='sell')
    sell_real59 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=59 < CONDITIONS, space='sell')
    sell_real60 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=60 < CONDITIONS, space='sell')
    sell_real61 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=61 < CONDITIONS, space='sell')
    sell_real62 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=62 < CONDITIONS, space='sell')
    sell_real63 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=63 < CONDITIONS, space='sell')
    sell_real64 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=64 < CONDITIONS, space='sell')
    sell_real65 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=65 < CONDITIONS, space='sell')
    sell_real66 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=66 < CONDITIONS, space='sell')
    sell_real67 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=67 < CONDITIONS, space='sell')
    sell_real68 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=68 < CONDITIONS, space='sell')
    sell_real69 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=69 < CONDITIONS, space='sell')
    sell_real70 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=70 < CONDITIONS, space='sell')
    sell_real71 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=71 < CONDITIONS, space='sell')
    sell_real72 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=72 < CONDITIONS, space='sell')
    sell_real73 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=73 < CONDITIONS, space='sell')
    sell_real74 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=74 < CONDITIONS, space='sell')
    sell_real75 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=75 < CONDITIONS, space='sell')
    sell_real76 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=76 < CONDITIONS, space='sell')
    sell_real77 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=77 < CONDITIONS, space='sell')
    sell_real78 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=78 < CONDITIONS, space='sell')
    sell_real79 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=79 < CONDITIONS, space='sell')
    sell_real80 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=80 < CONDITIONS, space='sell')
    sell_real81 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=81 < CONDITIONS, space='sell')
    sell_real82 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=82 < CONDITIONS, space='sell')
    sell_real83 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=83 < CONDITIONS, space='sell')
    sell_real84 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=84 < CONDITIONS, space='sell')
    sell_real85 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=85 < CONDITIONS, space='sell')
    sell_real86 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=86 < CONDITIONS, space='sell')
    sell_real87 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=87 < CONDITIONS, space='sell')
    sell_real88 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=88 < CONDITIONS, space='sell')
    sell_real89 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=89 < CONDITIONS, space='sell')
    sell_real90 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=90 < CONDITIONS, space='sell')
    sell_real91 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=91 < CONDITIONS, space='sell')
    sell_real92 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=92 < CONDITIONS, space='sell')
    sell_real93 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=93 < CONDITIONS, space='sell')
    sell_real94 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=94 < CONDITIONS, space='sell')
    sell_real95 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=95 < CONDITIONS, space='sell')
    sell_real96 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=96 < CONDITIONS, space='sell')
    sell_real97 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=97 < CONDITIONS, space='sell')
    sell_real98 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=98 < CONDITIONS, space='sell')
    sell_real99 = DecimalParameter(
        reals[0], reals[-1], default=reals[0], decimals=DECIMALS, optimize=99 < CONDITIONS, space='sell')
    ###############################################################

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = dataframe.shift(1)
        # print(timeframes)
        for indicator in indicators:
            for tf_idx in timeframes:
                tf_idx = int(tf_idx)
                try:
                    dataframe[f'{indicator}-{tf_idx}'] = getattr(
                        ta, indicator)(dataframe, timeperiod=tf_idx)
                except:
                    try:
                        dataframe[f'{indicator}-{tf_idx}'] = getattr(
                            ta, indicator)(dataframe, timeperiod=float(tf_idx))
                    except:
                        try:
                            dataframe[f'{indicator}-{tf_idx}'] = getattr(ta, indicator)(
                                dataframe,  timeperiod=tf_idx).iloc[:, 0]
                        except:
                            raise
        # print(dataframe.keys())
        # print("\t",metadata['pair'],end="\h")
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        for i in range(CONDITIONS):
            i = str(i)
            indicator = f'{getattr(self,"indicator"+i).value}'
            crossed = f'{getattr(self,"crossed"+i).value}'
            timeframe = f'{getattr(self,"timeframe"+i).value}'
            crossed_timeframe = f'{getattr(self,"crossed_timeframe"+i).value}'
            formula = f'{getattr(self,"formula"+i).value}'

            A = dataframe[f'{indicator}-{timeframe}']
            B = dataframe[f'{crossed}-{crossed_timeframe}']
            R = pd.Series([float(f'{getattr(self,"real"+i).value}')]*len(A))
            df = pd.DataFrame({'A': A, 'B': A, 'R': R})

            conditions.append(df.eval(formula))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy']=1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []

        formula = []
        max_loop = CONDITIONS
        i = 0
        last_df = pd.DataFrame
        last_opr = None
        for i in range(CONDITIONS):
            i = str(i)
            indicator = f'{getattr(self,"sell_indicator"+i).value}'
            crossed = f'{getattr(self,"sell_crossed"+i).value}'
            tf_idx = f'{getattr(self,"sell_timeframe"+i).value}'
            crossed_timeframe_idx = f'{getattr(self,"sell_crossed_timeframe"+i).value}'
            formula = f'{getattr(self,"sell_formula"+i).value}'

            A = dataframe[f'{indicator}-{tf_idx}']
            B = dataframe[f'{crossed}-{crossed_timeframe_idx}']
            R = pd.Series([float(f'{getattr(self,"sell_real"+i).value}')]*len(A))
            df = pd.DataFrame({'A': A, 'B': A, 'R': R})

            conditions.append(df.eval(formula))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1

        return dataframe
