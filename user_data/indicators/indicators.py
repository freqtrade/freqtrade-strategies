
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas as pd

"""
Indicators for Freqtrade
author@: Gerald Lonlas
github@: https://github.com/freqtrade/freqtrade-strategies
"""

def pivots_points(dataframe: pd.DataFrame, timeperiod=30, levels=3) -> pd.DataFrame:
    """
    Pivots Points

    Formula:
    Pivot = (Previous High + Previous Low + Previous Close)/3

    Resistance #1 = (2 x Pivot) - Previous Low
    Support #1 = (2 x Pivot) - Previous High

    Resistance #2 = (Pivot - Support #1) + Resistance #1
    Support #2 = Pivot - (Resistance #1 - Support #1)

    Resistance #3 = (Pivot - Support #2) + Resistance #2
    Support #3 = Pivot - (Resistance #2 - Support #2)
    ...

    :param dataframe:
    :param timeperiod: Period to compare (in ticker)
    :param levels: Num of support/resistance desired
    :return: dataframe
    """

    data = {}

    low = qtpylib.rolling_mean(
        series=pd.Series(
            index=dataframe.index,
            data=dataframe['low']
        ),
        window=timeperiod
    )

    high = qtpylib.rolling_mean(
        series=pd.Series(
            index=dataframe.index,
            data=dataframe['high']
        ),
        window=timeperiod
    )

    # Pivot
    data['pivot'] = qtpylib.rolling_mean(
        series=qtpylib.typical_price(dataframe),
        window=timeperiod
    )

    # Resistance #1
    data['r1'] = (2 * data['pivot']) - low

    # Resistance #2
    data['s1'] = (2 * data['pivot']) - high

    # Calculate Resistances and Supports >1
    for i in range(2, levels+1):
        prev_support = data['s' + str(i - 1)]
        prev_resistance = data['r' + str(i - 1)]

        # Resitance
        data['r'+ str(i)] = (data['pivot'] - prev_support) + prev_resistance

        # Support
        data['s' + str(i)] = data['pivot'] - (prev_resistance - prev_support)

    return pd.DataFrame(
        index=dataframe.index,
        data=data
    )

