# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import IStrategy

import talib.abstract as ta

import logging
import os

logger = logging.getLogger(__name__)


class SystemRRiskManaged(IStrategy):
    """
    Momentum strategy with System R pre-trade risk management.

    Uses EMA crossover + RSI for entry signals, then validates every trade
    through System R's pre_trade_gate before execution.

    System R checks:
    1. Position sizing via G-formula (Kelly criterion variant)
    2. Risk validation via Iron Fist rules (max drawdown, concentration, etc.)
    3. System health (if R-multiples are tracked)

    Requires:
        pip install httpx
        Set SYSTEMR_API_KEY environment variable
        Register free at: https://agents.systemr.ai/v1/agents/register

    More info: https://github.com/System-R-AI/demo-trading-agent
    """

    INTERFACE_VERSION: int = 3

    # Strategy parameters
    minimal_roi = {"0": 0.1, "30": 0.05, "60": 0.02, "120": 0}
    stoploss = -0.03
    timeframe = "1h"
    startup_candle_count = 50

    # System R config
    systemr_api_key = os.environ.get("SYSTEMR_API_KEY", "")
    systemr_base_url = os.environ.get(
        "SYSTEMR_BASE_URL", "https://agents.systemr.ai"
    )

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Add EMA and RSI indicators."""
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=20)
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """EMA crossover + RSI filter for entries."""
        dataframe.loc[
            (
                (dataframe["ema_fast"] > dataframe["ema_slow"])
                & (dataframe["rsi"] > 50)
                & (dataframe["rsi"] < 70)
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """EMA crossunder for exits."""
        dataframe.loc[
            (
                (dataframe["ema_fast"] < dataframe["ema_slow"])
                & (dataframe["volume"] > 0)
            ),
            "exit_long",
        ] = 1
        return dataframe

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time,
        entry_tag,
        side: str,
        **kwargs,
    ) -> bool:
        """
        Validate trade through System R pre_trade_gate before execution.

        If the gate blocks the trade, it is skipped. If System R is
        unavailable, the trade proceeds (fail-open for backtesting).
        """
        if not self.systemr_api_key:
            return True

        try:
            import httpx
        except ImportError:
            logger.warning("httpx not installed -- skipping System R gate")
            return True

        stop_price = rate * (1 + self.stoploss)
        equity = str(self.wallets.get_total("USDT") if self.wallets else 10000)

        try:
            resp = httpx.post(
                f"{self.systemr_base_url}/v1/compound/pre-trade-gate",
                headers={"X-API-Key": self.systemr_api_key},
                json={
                    "symbol": pair.split("/")[0],
                    "direction": "long" if side == "long" else "short",
                    "entry_price": str(rate),
                    "stop_price": str(round(stop_price, 6)),
                    "equity": equity,
                },
                timeout=10.0,
            )
            resp.raise_for_status()
            gate = resp.json()

            if gate["gate_passed"]:
                score = gate["risk"]["score"]
                shares = gate["sizing"]["shares"]
                logger.info(
                    f"System R APPROVED {pair}: score={score}, "
                    f"recommended_size={shares}"
                )
                return True
            else:
                errors = gate["risk"].get("errors", [])
                logger.info(f"System R BLOCKED {pair}: {errors}")
                return False

        except Exception as e:
            logger.warning(f"System R gate error for {pair}: {e} -- allowing trade")
            return True
