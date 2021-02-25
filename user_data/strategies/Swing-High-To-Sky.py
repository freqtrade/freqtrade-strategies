# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy # noqa

__author__      = "Kevin Ossenbrück"
__copyright__   = "Free For Use"
__credits__     = ["Bloom Trading, Mohsen Hassan"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Kevin Ossenbrück"
__email__       = "kevin.ossenbrueck@pm.de"
__status__      = "Live"

class_name = 'SwingHighToSky'
class SwingHighToSky(IStrategy):

    # Disable ROI
    # Could be replaced with new ROI from hyperopt.
    minimal_roi = {
         "0":  100
    }

    stoploss = -0.30
  
    ### Do extra hyperopt for trailing seperat. Use "--spaces default" and then "--spaces trailing".
    ### See here for more information: https://www.freqtrade.io/en/latest/hyperopt
    trailing_stop = True
    trailing_stop_positive = 0.08
    trailing_stop_positive_offset = 0.10
    trailing_only_offset_is_reached = True

    ticker_interval = '30m'

    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        
        ### Add timeperiod from hyperopt (replace xx with value):
        ### "xx" must be replaced even before the first hyperopt is run,
        ### else "xx" would be a syntax error because it must be a Integer value.
        dataframe['cci-buy'] = ta.CCI(dataframe, timeperiod=xx)
        dataframe['cci-sell'] = ta.CCI(dataframe, timeperiod=xx)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            (
                (dataframe['macd'] > dataframe['macdsignal']) &
                (dataframe['cci-buy'] <= -100.0) # Replace with value from hyperopt.
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            ( 
                (dataframe['macd'] < dataframe['macdsignal']) & 
                (dataframe['cci-sell'] >= 200.0) # Replace with value from hyperopt.
            ),
            'sell'] = 1
            
        return dataframe
