from pandas import DataFrame
from technical.indicators import cmf

from freqtrade.strategy import IStrategy


class TechnicalExampleStrategy(IStrategy):
    INTERFACE_VERSION: int = 3
    minimal_roi = {
        "0": 0.01
    }

    stoploss = -0.05

    # Optimal timeframe for the strategy
    timeframe = '5m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['cmf'] = cmf(dataframe, 21)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    (dataframe['cmf'] < 0)

                )
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # different strategy used for sell points, due to be able to duplicate it to 100%
        dataframe.loc[
            (
                (dataframe['cmf'] > 0)
            ),
            'exit_long'] = 1
        return dataframe
