# brain Strategy Hyperopt
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: INSTALL TA BEFOUR RUN:
# :~$ pip install ta
# freqtrade hyperopt --hyperopt brainHo --hyperopt-loss SharpeHyperOptLossDaily --spaces buy sell roi --strategy brain -j 3 -e 700
# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List, Reversible

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer  # noqa

from freqtrade.optimize.hyperopt_interface import IHyperOpt

# --------------------------------
# Add your lib to import here
# import talib.abstract as ta  # noqa
from ta import add_all_ta_features
from ta.utils import dropna
import freqtrade.vendor.qtpylib.indicators as qtpylib

##################### SETTINGS #########################
# this is your trading brain nodes count
# you can change it and see the results...
# Importand will same with brain.py
nodes = 4
decimals = 2

#################### END SETTINGS ######################

# do not edit this line:
decimals = 10 ** decimals


PastKnowledges = ["open", "high", "low", "close", "volume", "volume_adi", "volume_obv",
                  "volume_cmf", "volume_fi", "volume_mfi", "volume_em", "volume_sma_em", "volume_vpt",
                  "volume_nvi", "volume_vwap", "volatility_atr", "volatility_bbm", "volatility_bbh",
                  "volatility_bbl", "volatility_bbw", "volatility_bbp", "volatility_bbhi",
                  "volatility_bbli", "volatility_kcc", "volatility_kch", "volatility_kcl",
                  "volatility_kcw", "volatility_kcp", "volatility_kchi", "volatility_kcli",
                  "volatility_dcl", "volatility_dch", "volatility_dcm", "volatility_dcw",
                  "volatility_dcp", "volatility_ui", "trend_macd", "trend_macd_signal",
                  "trend_macd_diff", "trend_sma_fast", "trend_sma_slow", "trend_ema_fast",
                  "trend_ema_slow", "trend_adx", "trend_adx_pos", "trend_adx_neg", "trend_vortex_ind_pos",
                  "trend_vortex_ind_neg", "trend_vortex_ind_diff", "trend_trix",
                  "trend_mass_index", "trend_cci", "trend_dpo", "trend_kst",
                  "trend_kst_sig", "trend_kst_diff", "trend_ichimoku_conv",
                  "trend_ichimoku_base", "trend_ichimoku_a", "trend_ichimoku_b",
                  "trend_visual_ichimoku_a", "trend_visual_ichimoku_b", "trend_aroon_up",
                  "trend_aroon_down", "trend_aroon_ind", "trend_psar_up", "trend_psar_down",
                  "trend_psar_up_indicator", "trend_psar_down_indicator", "trend_stc",
                  "momentum_rsi", "momentum_stoch_rsi", "momentum_stoch_rsi_k",
                  "momentum_stoch_rsi_d", "momentum_tsi", "momentum_uo", "momentum_stoch",
                  "momentum_stoch_signal", "momentum_wr", "momentum_ao", "momentum_kama",
                  "momentum_roc", "momentum_ppo", "momentum_ppo_signal", "momentum_ppo_hist",
                  "others_dr", "others_dlr", "others_cr"]


print(decimals)


class brainHo(IHyperOpt):

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        brain = list()

        for i in range(nodes):
            brain.append(Categorical(PastKnowledges, name=f'buy-node-input-{i}'))
            brain.append(Categorical([0, 1], name=f'buy-node-enabled-{i}'))
            brain.append(Categorical([-1, 1], name=f'buy-node-reversed-{i}'))
            brain.append(Integer(0, decimals, name=f'buy-node-wight-{i}'))

        return brain

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
            RESULT = 0

            for i in range(nodes):
                DFINP = dataframe[params[f'buy-node-input-{i}']]
                ENABLED = params[f'buy-node-enabled-{i}']
                REVERSE = params[f'buy-node-reversed-{i}']
                WIGHT = params[f'buy-node-wight-{i}']/decimals
                RESULT += DFINP*ENABLED*REVERSE*WIGHT

            conditions.append(RESULT > 0)

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
        brain = list()

        for i in range(nodes):
            brain.append(Categorical(PastKnowledges, name=f'sell-node-input-{i}'))
            brain.append(Categorical([0, 1], name=f'sell-node-enabled-{i}'))
            brain.append(Categorical([-1, 1], name=f'sell-node-reversed-{i}'))
            brain.append(Integer(0, decimals, name=f'sell-node-wight-{i}'))

        return brain

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
            RESULT = 0
            for i in range(nodes):
                DFINP = dataframe[params[f'sell-node-input-{i}']]
                ENABLED = params[f'sell-node-enabled-{i}']
                REVERSE = params[f'sell-node-reversed-{i}']
                WIGHT = params[f'sell-node-wight-{i}']/decimals
                RESULT += DFINP*ENABLED*REVERSE*WIGHT

            conditions.append(RESULT > 0)

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell']=1

            return dataframe

        return populate_sell_trend
