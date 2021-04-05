from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy

__author__      = "Kevin Ossenbrück"
__copyright__   = "Free For Use"
__credits__     = ["Bloom Trading, Mohsen Hassan"]
__license__     = "MIT"
__version__     = "1.0"
__maintainer__  = "Kevin Ossenbrück"
__email__       = "kevin.ossenbrueck@pm.de"
__status__      = "Live"

# CCI timerperiods and values
cciBuyTP = 72
cciBuyVal = -175
cciSellTP = 66
cciSellVal = -106

# RSI timeperiods and values
rsiBuyTP = 36
rsiBuyVal = 90
rsiSellTP = 45
rsiSellVal = 88
    
class SwingHighToSky(IStrategy):

    timeframe = '15m'
    
    stoploss = -0.34338
    
    minimal_roi = {"0": 0.27058, "33": 0.0853, "64": 0.04093, "244": 0}
    
    def informative_pairs(self):
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    
        dataframe['cci-'+str(cciBuyTP)] = ta.CCI(dataframe, timeperiod=cciBuyTP)
        dataframe['cci-'+str(cciSellTP)] = ta.CCI(dataframe, timeperiod=cciSellTP)     

        dataframe['rsi-'+str(rsiBuyTP)] = ta.RSI(dataframe, timeperiod=rsiBuyTP)
        dataframe['rsi-'+str(rsiSellTP)] = ta.RSI(dataframe, timeperiod=rsiSellTP)
        
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            (
                (dataframe['cci-'+str(cciBuyTP)] < cciBuyVal) &
                (dataframe['rsi-'+str(rsiBuyTP)] < rsiBuyVal)
            ),
            'buy'] = 1
            
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        dataframe.loc[
            ( 
                (dataframe['cci-'+str(cciSellTP)] > cciSellVal) & 
                (dataframe['rsi-'+str(rsiSellTP)] > rsiSellVal)
            ),
            'sell'] = 1
            
        return dataframe
