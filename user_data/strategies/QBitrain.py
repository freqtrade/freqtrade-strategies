# QBitrain Strategy QBit + Brain + train
# The idea is that some neurons of a brain connecting to each other to make a sum of
# numbers that help to make decisions to buy and sell.Mixed With Quantum Bits State!
# That multiple with the neuron value to change the neuron data to a wighted data.
# -1 is fully reversed, 0 means fully disabled, 1 is fully active.
# but its a range between -1 to 1 like quantum state of the particles!
# Author: @Mablue (Masoud Azizi)
# github: https://github.com/mablue/
# freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy roi trailing sell --strategy QBitrain
# --- Do not remove these libs ---
# from freqtrade import data
from freqtrade.strategy.hyper import CategoricalParameter, DecimalParameter, IntParameter

# from numpy.lib import math
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# --------------------------------

# Add your lib to import here
# TODO: talib is fast but have not more indicators
import talib.abstract as ta
from functools import reduce
#  TODO: this gene is removed 'MAVP' cuz or error on periods
AllLearntKnowledges = {
    'Overlap Studies': {
        'BBANDS-0',             # Bollinger Bands
        'BBANDS-1',             # Bollinger Bands
        'BBANDS-2',             # Bollinger Bands
        'DEMA',                 # Double Exponential Moving Average
        'EMA',                  # Exponential Moving Average
        'HT_TRENDLINE',         # Hilbert Transform - Instantaneous Trendline
        'KAMA',                 # Kaufman Adaptive Moving Average
        'MA',                   # Moving average
        'MAMA-0',               # MESA Adaptive Moving Average
        'MAMA-1',               # MESA Adaptive Moving Average
        # TODO: Fix this
        # 'MAVP',               # Moving average with variable period
        'MIDPOINT',             # MidPoint over period
        'MIDPRICE',             # Midpoint Price over period
        'SAR',                  # Parabolic SAR
        'SAREXT',               # Parabolic SAR - Extended
        'SMA',                  # Simple Moving Average
        'T3',                   # Triple Exponential Moving Average (T3)
        'TEMA',                 # Triple Exponential Moving Average
        'TRIMA',                # Triangular Moving Average
        'WMA',                  # Weighted Moving Average
    },
    'Momentum Indicators': {
        'ADX',                  # Average Directional Movement Index
        'ADXR',                 # Average Directional Movement Index Rating
        'APO',                  # Absolute Price Oscillator
        'AROON-0',              # Aroon
        'AROON-1',              # Aroon
        'AROONOSC',             # Aroon Oscillator
        'BOP',                  # Balance Of Power
        'CCI',                  # Commodity Channel Index
        'CMO',                  # Chande Momentum Oscillator
        'DX',                   # Directional Movement Index
        'MACD-0',               # Moving Average Convergence/Divergence
        'MACD-1',               # Moving Average Convergence/Divergence
        'MACD-2',               # Moving Average Convergence/Divergence
        'MACDEXT-0',            # MACD with controllable MA type
        'MACDEXT-1',            # MACD with controllable MA type
        'MACDEXT-2',            # MACD with controllable MA type
        'MACDFIX-0',            # Moving Average Convergence/Divergence Fix 12/26
        'MACDFIX-1',            # Moving Average Convergence/Divergence Fix 12/26
        'MACDFIX-2',            # Moving Average Convergence/Divergence Fix 12/26
        'MFI',                  # Money Flow Index
        'MINUS_DI',             # Minus Directional Indicator
        'MINUS_DM',             # Minus Directional Movement
        'MOM',                  # Momentum
        'PLUS_DI',              # Plus Directional Indicator
        'PLUS_DM',              # Plus Directional Movement
        'PPO',                  # Percentage Price Oscillator
        'ROC',                  # Rate of change : ((price/prevPrice)-1)*100
        # Rate of change Percentage: (price-prevPrice)/prevPrice
        'ROCP',
        'ROCR',                 # Rate of change ratio: (price/prevPrice)
        # Rate of change ratio 100 scale: (price/prevPrice)*100
        'ROCR100',
        'RSI',                  # Relative Strength Index
        'STOCH-0',              # Stochastic
        'STOCH-1',              # Stochastic
        'STOCHF-0',             # Stochastic Fast
        'STOCHF-1',             # Stochastic Fast
        'STOCHRSI-0',           # Stochastic Relative Strength Index
        'STOCHRSI-1',           # Stochastic Relative Strength Index
        # 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
        'TRIX',
        'ULTOSC',               # Ultimate Oscillator
        'WILLR',                # Williams' %R
    },
    'Volume Indicators': {
        'AD',                   # Chaikin A/D Line
        'ADOSC',                # Chaikin A/D Oscillator
        'OBV',                  # On Balance Volume
    },
    'Volatility Indicators': {
        'ATR',                  # Average True Range
        'NATR',                 # Normalized Average True Range
        'TRANGE',               # True Range
    },
    'Price Transform': {
        'AVGPRICE',             # Average Price
        'MEDPRICE',             # Median Price
        'TYPPRICE',             # Typical Price
        'WCLPRICE',             # Weighted Close Price
    },
    'Cycle Indicators': {
        'HT_DCPERIOD',          # Hilbert Transform - Dominant Cycle Period
        'HT_DCPHASE',           # Hilbert Transform - Dominant Cycle Phase
        'HT_PHASOR-0',          # Hilbert Transform - Phasor Components
        'HT_PHASOR-1',          # Hilbert Transform - Phasor Components
        'HT_SINE-0',            # Hilbert Transform - SineWave
        'HT_SINE-1',            # Hilbert Transform - SineWave
        'HT_TRENDMODE',         # Hilbert Transform - Trend vs Cycle Mode
    },
    'Pattern Recognition': {
        'CDL2CROWS',            # Two Crows
        'CDL3BLACKCROWS',       # Three Black Crows
        'CDL3INSIDE',           # Three Inside Up/Down
        'CDL3LINESTRIKE',       # Three-Line Strike
        'CDL3OUTSIDE',          # Three Outside Up/Down
        'CDL3STARSINSOUTH',     # Three Stars In The South
        'CDL3WHITESOLDIERS',    # Three Advancing White Soldiers
        'CDLABANDONEDBABY',     # Abandoned Baby
        'CDLADVANCEBLOCK',      # Advance Block
        'CDLBELTHOLD',          # Belt-hold
        'CDLBREAKAWAY',         # Breakaway
        'CDLCLOSINGMARUBOZU',   # Closing Marubozu
        'CDLCONCEALBABYSWALL',  # Concealing Baby Swallow
        'CDLCOUNTERATTACK',     # Counterattack
        'CDLDARKCLOUDCOVER',    # Dark Cloud Cover
        'CDLDOJI',              # Doji
        'CDLDOJISTAR',          # Doji Star
        'CDLDRAGONFLYDOJI',     # Dragonfly Doji
        'CDLENGULFING',         # Engulfing Pattern
        'CDLEVENINGDOJISTAR',   # Evening Doji Star
        'CDLEVENINGSTAR',       # Evening Star
        'CDLGAPSIDESIDEWHITE',  # Up/Down-gap side-by-side white lines
        'CDLGRAVESTONEDOJI',    # Gravestone Doji
        'CDLHAMMER',            # Hammer
        'CDLHANGINGMAN',        # Hanging Man
        'CDLHARAMI',            # Harami Pattern
        'CDLHARAMICROSS',       # Harami Cross Pattern
        'CDLHIGHWAVE',          # High-Wave Candle
        'CDLHIKKAKE',           # Hikkake Pattern
        'CDLHIKKAKEMOD',        # Modified Hikkake Pattern
        'CDLHOMINGPIGEON',      # Homing Pigeon
        'CDLIDENTICAL3CROWS',   # Identical Three Crows
        'CDLINNECK',            # In-Neck Pattern
        'CDLINVERTEDHAMMER',    # Inverted Hammer
        'CDLKICKING',           # Kicking
        'CDLKICKINGBYLENGTH',   # Kicking - bull/bear determined by the longer marubozu
        'CDLLADDERBOTTOM',      # Ladder Bottom
        'CDLLONGLEGGEDDOJI',    # Long Legged Doji
        'CDLLONGLINE',          # Long Line Candle
        'CDLMARUBOZU',          # Marubozu
        'CDLMATCHINGLOW',       # Matching Low
        'CDLMATHOLD',           # Mat Hold
        'CDLMORNINGDOJISTAR',   # Morning Doji Star
        'CDLMORNINGSTAR',       # Morning Star
        'CDLONNECK',            # On-Neck Pattern
        'CDLPIERCING',          # Piercing Pattern
        'CDLRICKSHAWMAN',       # Rickshaw Man
        'CDLRISEFALL3METHODS',  # Rising/Falling Three Methods
        'CDLSEPARATINGLINES',   # Separating Lines
        'CDLSHOOTINGSTAR',      # Shooting Star
        'CDLSHORTLINE',         # Short Line Candle
        'CDLSPINNINGTOP',       # Spinning Top
        'CDLSTALLEDPATTERN',    # Stalled Pattern
        'CDLSTICKSANDWICH',     # Stick Sandwich
        # Takuri (Dragonfly Doji with very long lower shadow)
        'CDLTAKURI',
        'CDLTASUKIGAP',         # Tasuki Gap
        'CDLTHRUSTING',         # Thrusting Pattern
        'CDLTRISTAR',           # Tristar Pattern
        'CDLUNIQUE3RIVER',      # Unique 3 River
        'CDLUPSIDEGAP2CROWS',   # Upside Gap Two Crows
        'CDLXSIDEGAP3METHODS',  # Upside/Downside Gap Three Methods

    },
    'Statistic Functions': {
        'BETA',                 # Beta
        'CORREL',               # Pearson's Correlation Coefficient (r)
        'LINEARREG',            # Linear Regression
        'LINEARREG_ANGLE',      # Linear Regression Angle
        'LINEARREG_INTERCEPT',  # Linear Regression Intercept
        'LINEARREG_SLOPE',      # Linear Regression Slope
        'STDDEV',               # Standard Deviation
        'TSF',                  # Time Series Forecast
        'VAR',                  # Variance
    }

}
LearntKnowledges = set()
########################### SETTINGS ##############################

# LearntKnowledges = {'ADX', 'MOM', 'PLUS_DI', 'PLUS_DM'}
LearntKnowledges |= AllLearntKnowledges['Overlap Studies']
LearntKnowledges |= AllLearntKnowledges['Momentum Indicators']
LearntKnowledges |= AllLearntKnowledges['Volume Indicators']
LearntKnowledges |= AllLearntKnowledges['Volatility Indicators']
LearntKnowledges |= AllLearntKnowledges['Price Transform']
LearntKnowledges |= AllLearntKnowledges['Cycle Indicators']
LearntKnowledges |= AllLearntKnowledges['Pattern Recognition']
LearntKnowledges |= AllLearntKnowledges['Statistic Functions']

timeperiods = [6, 12, 24]
# timeperiods = [10, 12, 15]

# number of candles to check up,don,off trend.
TREND_CHECK_CANDLES = 4
DECIMALS = 2
# will use it without sell in hyperopt:
# dualfit is fast but just uses buy params for both buy and sell
DUALFIT = False
########################### END SETTINGS ##########################
# DATAFRAME = DataFrame()

LearntKnowledges = list(LearntKnowledges)
# print('selected indicators for optimzatin: \n', LearntKnowledges)

LearntKnowledges_with_timeperiod = list()
for LearntKnowledge in LearntKnowledges:
    for timeperiod in timeperiods:
        LearntKnowledges_with_timeperiod.append(
            f'{LearntKnowledge}-{timeperiod}')

# Let give somethings to CatagoricalParam to Play with them
# When just one thing is inside catagorical lists
# TODO: its Not True Way :)
if len(LearntKnowledges) == 1:
    LearntKnowledges = LearntKnowledges*2
if len(timeperiods) == 1:
    timeperiods = timeperiods*2


def knowledge_calculator(dataframe, indicator):
    # Cuz Timeperiods not effect calculating CDL patterns recognations
    # TODO: I think I'm wrong!:S Timeperiods will effect cuz chart shape is changing when TP changes!
    # but it make the algo very fast and I cheked, this make good results!! :S
    if 'CDL' in indicator:
        splited_indicator = indicator.split('-')
        splited_indicator[1] = "0"
        new_indicator = "-".join(splited_indicator)
        # print(indicator, new_indicator)
        indicator = new_indicator

    knowledge = indicator.split("-")

    knowledge_name = knowledge[0]
    knowledge_len = len(knowledge)

    if indicator in dataframe.keys():
        # print(f"{indicator}, calculated befoure")
        # print(len(dataframe.keys()))
        return dataframe[indicator]
    else:
        result = None
        # For Pattern Recognations
        if knowledge_len == 1:
            # print('knowledge_len == 1\t', indicator)
            result = getattr(ta, knowledge_name)(
                dataframe
            )
            return result
        elif knowledge_len == 2:
            # print('knowledge_len == 2\t', indicator)
            knowledge_timeperiod = int(knowledge[1])
            result = getattr(ta, knowledge_name)(
                dataframe,
                timeperiod=knowledge_timeperiod,
            )
            return result
        # For
        elif knowledge_len == 3:
            # print('knowledge_len == 3\t', indicator)
            knowledge_timeperiod = int(knowledge[2])
            knowledge_index = int(knowledge[1])
            result = getattr(ta, knowledge_name)(
                dataframe,
                timeperiod=knowledge_timeperiod,
            ).iloc[:, knowledge_index]
            return result
        # For trend operators(MA-5-SMA-4)
        elif knowledge_len == 4:
            # print('knowledge_len == 4\t', indicator)
            knowledge_timeperiod = int(knowledge[1])
            sharp_indicator = f'{knowledge_name}-{knowledge_timeperiod}'
            dataframe[sharp_indicator] = getattr(ta, knowledge_name)(
                dataframe,
                timeperiod=knowledge_timeperiod,
            )
            return ta.SMA(dataframe[sharp_indicator].fillna(0), TREND_CHECK_CANDLES)
        # For trend operators(STOCH-0-4-SMA-4)
        elif knowledge_len == 5:
            # print('knowledge_len == 5\t', indicator)
            knowledge_timeperiod = int(knowledge[2])
            knowledge_index = int(knowledge[1])
            sharp_indicator = f'{knowledge_name}-{knowledge_index}-{knowledge_timeperiod}'
            dataframe[sharp_indicator] = getattr(ta, knowledge_name)(
                dataframe,
                timeperiod=knowledge_timeperiod,
            ).iloc[:, knowledge_index]
            return ta.SMA(dataframe[sharp_indicator].fillna(0), TREND_CHECK_CANDLES)

# OK. Dont worry!! its used in end result


def normalize(df):
    df = 2*(df-df.min())/(df.max()-df.min()) - 1
    return df


class QBitrain(IStrategy):
    # #################### RESULTS LearntE PLACE ##################
    # *   22/100:     16 trades. 13/3/0 Wins/Draws/Losses. Avg profit   4.92%. Median profit   4.31%. Total profit  0.26254039 BTC (  26.25Σ%). Avg duration 1 day, 14:00:00 min. Objective: -21.56636
    # Buy hyperspace params:
    buy_params = {
        "buy_indicator_0": "CDLTRISTAR-24",
        "buy_indicator_1": "CDLEVENINGDOJISTAR-12",
        "buy_indicator_2": "MACD-2-12",
        "buy_indicator_3": "STOCH-1-12",
        "buy_indicator_4": "PPO-6",
        "buy_indicator_5": "MOM-6",
        "buy_node_quantum_state_0": -0.5,
        "buy_node_quantum_state_1": -0.24,
        "buy_node_quantum_state_2": 0.51,
        "buy_node_quantum_state_3": -0.27,
        "buy_node_quantum_state_4": 0.35,
        "buy_node_quantum_state_5": 0.99,
    }

    # Sell hyperspace params:
    sell_params = {
        "sell_indicator_0": "BBANDS-2-6",
        "sell_indicator_1": "EMA-24",
        "sell_indicator_2": "BBANDS-2-12",
        "sell_indicator_3": "BBANDS-0-24",
        "sell_indicator_4": "MACD-1-12",
        "sell_indicator_5": "HT_PHASOR-1-12",
        "sell_node_quantum_state_0": -0.15,
        "sell_node_quantum_state_1": -0.4,
        "sell_node_quantum_state_2": -0.56,
        "sell_node_quantum_state_3": -0.64,
        "sell_node_quantum_state_4": 0.64,
        "sell_node_quantum_state_5": 0.36,
    }

    # ROI table:
    minimal_roi = {
        "0": 0.636,
        "1133": 0.112,
        "2179": 0.049,
        "4307": 0
    }

    # Stoploss:
    stoploss = -0.256
    # #################### END OF RESULT PLACE ####################
    timeframe = '5m'

    # TODO: Its not dry code!
    # Buy Hyperoptable Parameters/Spaces.
    # #########################################################
    buy_indicator_0 = CategoricalParameter(
        LearntKnowledges_with_timeperiod, default="CDLTRISTAR-24", space='buy')
    buy_indicator_1 = CategoricalParameter(
        LearntKnowledges_with_timeperiod, default="CDLEVENINGDOJISTAR-12", space='buy')
    buy_indicator_2 = CategoricalParameter(
        LearntKnowledges_with_timeperiod, default="MACD-2-12", space='buy')
    buy_indicator_3 = CategoricalParameter(
        LearntKnowledges_with_timeperiod, default="STOCH-1-12", space='buy')
    buy_indicator_4 = CategoricalParameter(
        LearntKnowledges_with_timeperiod, default="PPO-6", space='buy')
    buy_indicator_5 = CategoricalParameter(
        LearntKnowledges_with_timeperiod, default="MOM-6", space='buy')

    buy_node_quantum_state_0 = DecimalParameter(
        -1, 1, decimals=DECIMALS, default=-0.5, space='buy')
    buy_node_quantum_state_1 = DecimalParameter(-1, 1,
                                                decimals=DECIMALS, default=-0.24, space='buy')
    buy_node_quantum_state_2 = DecimalParameter(
        -1, 1, decimals=DECIMALS, default=0.51, space='buy')
    buy_node_quantum_state_3 = DecimalParameter(-1, 1,
                                                decimals=DECIMALS, default=-0.27, space='buy')
    buy_node_quantum_state_4 = DecimalParameter(
        -1, 1, decimals=DECIMALS, default=0.35, space='buy')
    buy_node_quantum_state_5 = DecimalParameter(
        -1, 1, decimals=DECIMALS, default=0.99, space='buy')

    if DUALFIT == False:
        sell_indicator_0 = CategoricalParameter(
            LearntKnowledges_with_timeperiod, default="BBANDS-2-6", space='sell')
        sell_indicator_1 = CategoricalParameter(
            LearntKnowledges_with_timeperiod, default="EMA-24", space='sell')
        sell_indicator_2 = CategoricalParameter(
            LearntKnowledges_with_timeperiod, default="BBANDS-2-12", space='sell')
        sell_indicator_3 = CategoricalParameter(
            LearntKnowledges_with_timeperiod, default="BBANDS-0-24", space='sell')
        sell_indicator_4 = CategoricalParameter(
            LearntKnowledges_with_timeperiod, default="MACD-1-12", space='sell')
        sell_indicator_5 = CategoricalParameter(
            LearntKnowledges_with_timeperiod, default="HT_PHASOR-1-12", space='sell')

        sell_node_quantum_state_0 = DecimalParameter(-1, 1,
                                                     decimals=DECIMALS, default=-0.15, space='sell')
        sell_node_quantum_state_1 = DecimalParameter(-1, 1,
                                                     decimals=DECIMALS, default=-0.4, space='sell')
        sell_node_quantum_state_2 = DecimalParameter(-1, 1,
                                                     decimals=DECIMALS, default=-0.56, space='sell')
        sell_node_quantum_state_3 = DecimalParameter(-1, 1,
                                                     decimals=DECIMALS, default=-0.64, space='sell')
        sell_node_quantum_state_4 = DecimalParameter(-1, 1,
                                                     decimals=DECIMALS, default=0.64, space='sell')
        sell_node_quantum_state_5 = DecimalParameter(-1, 1,
                                                     decimals=DECIMALS, default=0.36, space='sell')

    #########################################################

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        '''
        It's good to calculate all indicators in all time periods here and so optimize the strategy.
        But this strategy can take much time to generate anything that may not use in his optimization.
        I just calculate the specific indicators in specific time period inside buy and sell strategy populator methods if needed.
        Also, this method (populate_indicators) just calculates default value of hyperoptable params
        so using this method have not big benefits instade of calculating useable things inside buy and sell trand populators
        '''
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # TODO: Its not dry code!

        conditions = []
        RESULT = 0

        IND = self.buy_indicator_0.value
        DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
        QS = self.buy_node_quantum_state_0.value
        RESULT += DFINP*QS

        IND = self.buy_indicator_1.value
        DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
        QS = self.buy_node_quantum_state_1.value
        RESULT += DFINP*QS

        IND = self.buy_indicator_2.value
        DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
        QS = self.buy_node_quantum_state_2.value
        RESULT += DFINP*QS

        IND = self.buy_indicator_3.value
        DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
        QS = self.buy_node_quantum_state_3.value
        RESULT += DFINP*QS

        IND = self.buy_indicator_4.value
        DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
        QS = self.buy_node_quantum_state_4.value
        RESULT += DFINP*QS

        IND = self.buy_indicator_5.value
        DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
        QS = self.buy_node_quantum_state_5.value
        RESULT += DFINP*QS

        RESULT = normalize(RESULT*dataframe['close'])
        # print(RESULT.head)

        # 0.333 to 1 : buy
        conditions.append(RESULT > 0.333)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        RESULT = 0
        if DUALFIT == True:
            IND = self.buy_indicator_0.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.buy_node_quantum_state_0.value
            RESULT += DFINP*QS

            IND = self.buy_indicator_1.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.buy_node_quantum_state_1.value
            RESULT += DFINP*QS

            IND = self.buy_indicator_2.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.buy_node_quantum_state_2.value
            RESULT += DFINP*QS

            IND = self.buy_indicator_3.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.buy_node_quantum_state_3.value
            RESULT += DFINP*QS

            IND = self.buy_indicator_4.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.buy_node_quantum_state_4.value
            RESULT += DFINP*QS

            IND = self.buy_indicator_5.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.buy_node_quantum_state_5.value
            RESULT += DFINP*QS

        else:
            IND = self.sell_indicator_0.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.sell_node_quantum_state_0.value
            RESULT += DFINP*QS

            IND = self.sell_indicator_1.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.sell_node_quantum_state_1.value
            RESULT += DFINP*QS

            IND = self.sell_indicator_2.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.sell_node_quantum_state_2.value
            RESULT += DFINP*QS

            IND = self.sell_indicator_3.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.sell_node_quantum_state_3.value
            RESULT += DFINP*QS

            IND = self.sell_indicator_4.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.sell_node_quantum_state_4.value
            RESULT += DFINP*QS

            IND = self.sell_indicator_5.value
            DFINP = dataframe[IND] = knowledge_calculator(dataframe, IND)
            QS = self.sell_node_quantum_state_5.value
            RESULT += DFINP*QS

        RESULT = normalize(RESULT*dataframe['close'])
        # -1 to -0.333: sell
        conditions.append(RESULT < -0.333)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell']=1

        return dataframe
