# GodStra Strategy Hyperopt
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# IMPORTANT: INSTALL TA BEFOUR RUN:
# :~$ pip install ta
# freqtrade hyperopt --hyperopt GodStraHo --hyperopt-loss SharpeHyperOptLossDaily --spaces all --strategy GodStra --config config.json -e 100

# --- Do not remove these libs ---
from functools import reduce
from typing import Any, Callable, Dict, List

import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer, Real  # noqa

from freqtrade.optimize.hyperopt_interface import IHyperOpt

# --------------------------------
# Add your lib to import here
# import talib.abstract as ta  # noqa
from ta import add_all_ta_features
from ta.utils import dropna
import freqtrade.vendor.qtpylib.indicators as qtpylib
# this is your trading strategy DNA Size
# you can change it and see the results...
DNA_SIZE = 1


GodGenes = ["open", "high", "low", "close", "volume", "volume_adi", "volume_obv",
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
            gene.append(Integer(-1, 101, name=f'buy-int-{i}'))
            gene.append(Real(-1.1, 1.1, name=f'buy-real-{i}'))
            # Operations
            # CA: Crossed Above, CB: Crossed Below,
            # I: Integer, R: Real, D: Disabled
            gene.append(Categorical(["D", ">", "<", "=", "CA", "CB",
                                     ">I", "=I", "<I", ">R", "=R", "<R"], name=f'buy-oper-{i}'))
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
                INT = params[f'buy-int-{i}']
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

        for i in range(DNA_SIZE):
            gene.append(Categorical(GodGenes, name=f'sell-indicator-{i}'))
            gene.append(Categorical(GodGenes, name=f'sell-cross-{i}'))
            gene.append(Integer(-1, 101, name=f'sell-int-{i}'))
            gene.append(Real(-0.01, 1.01, name=f'sell-real-{i}'))
            # Operations
            # CA: Crossed Above, CB: Crossed Below,
            # I: Integer, R: Real, D: Disabled
            gene.append(Categorical(["D", ">", "<", "=", "CA", "CB",
                                     ">I", "=I", "<I", ">R", "=R", "<R"], name=f'sell-oper-{i}'))
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
            for i in range(DNA_SIZE):

                OPR = params[f'sell-oper-{i}']
                IND = params[f'sell-indicator-{i}']
                CRS = params[f'sell-cross-{i}']
                INT = params[f'sell-int-{i}']
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

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell']=1

            return dataframe

        return populate_sell_trend
