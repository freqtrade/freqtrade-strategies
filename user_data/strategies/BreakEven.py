# --- Do not remove these libs ---
from freqtrade.strategy import IStrategy
from pandas import DataFrame

# --------------------------------


class BreakEven(IStrategy):
    """
    author@: lenik

    Sometimes I want to close the bot ASAP, but not have the positions floating around.

    I can "/stopbuy" and wait for the positions to get closed by the bot rules, which is
    waiting for some profit, etc -- this usually takes too long...

    What I would prefer is to close everything that is over 0% profit to avoid the losses.

    Here's a simple strategy with empty buy/sell signals and "minimal_roi = { 0 : 0 }" that
    sells everything already at profit and wait until the positions at loss will come to break
    even point (or the small profit you provide in ROI table).

    You may restart the bot with the new strategy as a command-line parameter.

    Another way would be to specify the original strategy in the config file, then change to
    this one and simply "/reload_config" from the Telegram bot.

    """

    INTERFACE_VERSION: int = 3
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.01,      # at least 1% at first
        "10": 0         # after 10min, everything goes
    }

    # This is more radical version that sells everything above the profit level
#    minimal_roi = {
#        "0": 0
#    }

    # And this is basically "/forcesell all", that sells no matter what profit
#    minimal_roi = {
#        "0": -1
#    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.05

    # Optimal timeframe for the strategy
    timeframe = '5m'

    # don't generate any buy or sell signals, everything is handled by ROI and stop_loss
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            ),
            'enter_long'] = 0
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            ),
            'exit_long'] = 0
        return dataframe
