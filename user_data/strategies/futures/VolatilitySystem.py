from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class VolatilitySystem(IStrategy):

    INTERFACE_VERSION: int = 3
    # ROI table:
    minimal_roi = {"0": 0.15, "30": 0.1, "60": 0.05}
    # minimal_roi = {"0": 1}

    # Stoploss:
    stoploss = -0.265

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.1
    trailing_only_offset_is_reached = False

    timeframe = "5m"

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate ATR
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14) * 2.0
        dataframe['close_change'] = dataframe['close'].pct_change()
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add long entry signals
        dataframe.loc[
            (dataframe['close_change'] > dataframe['atr']) & 
            (dataframe['close'].shift(1) <= dataframe['atr'].shift(1)), 
            'enter_long'] = 1
        
        # Add short entry signals
        dataframe.loc[
            (dataframe['close_change'] < -dataframe['atr']) & 
            (dataframe['close'].shift(1) >= -dataframe['atr'].shift(1)), 
            'enter_short'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add long exit signals
        dataframe.loc[
            (dataframe['close_change'] < dataframe['atr']) & 
            (dataframe['close'].shift(1) >= dataframe['atr'].shift(1)), 
            'exit_long'] = 1
        
        # Add short exit signals
        dataframe.loc[
            (dataframe['close_change'] > -dataframe['atr']) & 
            (dataframe['close'].shift(1) <= -dataframe['atr'].shift(1)), 
            'exit_short'] = 1
        
        return dataframe
