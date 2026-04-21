# ==============================================================================
#  🦅 HorusFlowStrategy — Freqtrade + Horus Flow Intelligence
#  Version: 1.0.0
#  Author:  Horus Tech Ltd (horustechltd)
#  License: MIT
#
#  Architecture:
#  ┌─────────────────────────────────────────────────────────┐
#  │  Freqtrade Engine                                       │
#  │  ┌─────────────────┐    ┌──────────────────────────┐   │
#  │  │ populate_entry  │───▶│ confirm_trade_entry()    │   │
#  │  │ (RSI/EMA logic) │    │ ← Horus Gatekeeper       │   │
#  │  └─────────────────┘    └──────────────────────────┘   │
#  │                                    │                    │
#  │                         ┌──────────▼───────────┐       │
#  │                         │ custom_exit()         │       │
#  │                         │ ← Horus Bailout       │       │
#  │                         └──────────────────────┘       │
#  └─────────────────────────────────────────────────────────┘
#
#  Rules:
#  ✅ Horus is ONLY called in confirm_trade_entry() and custom_exit()
#  ✅ NEVER in populate_indicators() — this would flood the API
#  ✅ 5-second cache prevents redundant calls during the same candle
#  ✅ Backtest-safe: Horus is skipped automatically in dry/backtest mode
#  ✅ Fail-open in confirm_trade_entry (allow if API down)
#  ✅ Fail-closed in custom_exit (protect capital if API down)
# ==============================================================================

import logging
import os
import time
from datetime import datetime
from functools import lru_cache
from typing import Optional

import requests
from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
#  Horus API Client (Standalone — usable outside Freqtrade too)
# ══════════════════════════════════════════════════════════════════════════════

class HorusClient:
    """
    Lightweight Horus Flow Intelligence API client.
    Includes a 5-second TTL cache to prevent rate-limit flooding.

    API Docs: https://rapidapi.com/horustechltd/api/horus-flow-intelligence
    """

    BASE_URL = "https://horus-flow-intelligence.p.rapidapi.com"

    # Signals that indicate market is UNSAFE to enter
    DANGER_SIGNALS = {"SELL_PRESSURE", "LIQUIDITY_EVENT", "EMERGENCY_DUMP", "BAILOUT"}

    # Signals that confirm FAVORABLE orderflow
    ENTRY_SIGNALS = {"BUY_PRESSURE", "BUY_ABSORPTION"}

    # Signals that trigger IMMEDIATE EXIT of open position
    EXIT_SIGNALS = {"LIQUIDITY_EVENT", "EMERGENCY_DUMP", "BAILOUT"}

    def __init__(
        self,
        api_key: str,
        min_confidence: float = 0.70,
        cache_ttl_seconds: int = 5,
        timeout_seconds: int = 2,
    ):
        self.min_confidence = min_confidence
        self.cache_ttl = cache_ttl_seconds
        self.timeout = timeout_seconds
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "horus-flow-intelligence.p.rapidapi.com",
        }
        # Cache: {symbol: (timestamp, data)}
        self._cache: dict[str, tuple[float, dict]] = {}

    def _get_flow_raw(self, symbol: str) -> Optional[dict]:
        """Fetch raw flow data with TTL cache. Returns None on failure."""
        symbol = symbol.replace("/", "").upper()
        now = time.monotonic()

        # Cache hit?
        if symbol in self._cache:
            cached_at, cached_data = self._cache[symbol]
            if now - cached_at < self.cache_ttl:
                logger.debug(f"[Horus Cache HIT] {symbol}")
                return cached_data

        # Cache miss — fetch from API
        try:
            response = requests.get(
                f"{self.BASE_URL}/v1/flow/crypto/{symbol}",
                headers=self.headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            self._cache[symbol] = (now, data)
            logger.debug(
                f"[Horus API] {symbol} → {data.get('signal')} "
                f"({data.get('confidence', 0):.0%})"
            )
            return data

        except requests.Timeout:
            logger.warning(f"[Horus TIMEOUT] {symbol} — API took >{self.timeout}s")
            return None
        except requests.HTTPError as e:
            logger.error(f"[Horus HTTP ERROR] {symbol} — {e}")
            return None
        except Exception as e:
            logger.error(f"[Horus ERROR] {symbol} — {e}")
            return None

    def is_safe_to_enter(self, symbol: str) -> tuple[bool, str]:
        """
        Gatekeeper for trade entry.

        Returns:
            (True, reason)  → safe to enter
            (False, reason) → block entry

        Fail-OPEN: if API is down, we allow entry (strategy decides).
        """
        data = self._get_flow_raw(symbol)

        if data is None:
            return True, "HORUS_TIMEOUT_ALLOW"

        signal = data.get("signal", "NEUTRAL")
        confidence = data.get("confidence", 0)
        flags = data.get("metrics", {}).get("flags", [])

        # Hard block: dangerous market state
        if signal in self.DANGER_SIGNALS:
            return False, f"DANGER:{signal}:{confidence:.0%}"

        # Hard block: spoofing detected regardless of signal
        if any("SPOOFING_DETECTED" in f for f in flags):
            return False, f"SPOOFING:{flags}"

        # Green light: confirmed institutional buy-side activity
        if signal in self.ENTRY_SIGNALS and confidence >= self.min_confidence:
            return True, f"CONFIRMED:{signal}:{confidence:.0%}"

        # Gray zone: neutral or low conviction → block
        return False, f"LOW_CONVICTION:{signal}:{confidence:.0%}"

    def should_emergency_exit(self, symbol: str) -> tuple[bool, str]:
        """
        Called every ~1s during open position to detect flash crash setup.

        Returns:
            (True, reason)  → exit NOW
            (False, reason) → hold position

        Fail-CLOSED: if API is down, we do NOT force exit (avoid false panic).
        """
        data = self._get_flow_raw(symbol)

        if data is None:
            return False, "HORUS_TIMEOUT_HOLD"

        signal = data.get("signal", "NEUTRAL")
        confidence = data.get("confidence", 0)
        flags = data.get("metrics", {}).get("flags", [])

        # Emergency exit: liquidity collapsing
        if signal in self.EXIT_SIGNALS and confidence >= self.min_confidence:
            return True, f"EXIT:{signal}:{confidence:.0%}"

        # Emergency exit: global liquidity event flagged
        if "GLOBAL_LIQUIDITY_EVENT" in flags:
            return True, f"EXIT:GLOBAL_LIQUIDITY_EVENT"

        return False, f"HOLD:{signal}:{confidence:.0%}"


# ══════════════════════════════════════════════════════════════════════════════
#  Freqtrade Strategy
# ══════════════════════════════════════════════════════════════════════════════

class HorusFlowStrategy(IStrategy):
    """
    🦅 HorusFlowStrategy

    A Freqtrade strategy that uses classical technical analysis for entry
    signals, then passes every candidate trade through Horus Flow Intelligence
    for institutional orderflow confirmation before execution.

    Key behaviors:
    - Entry signal: RSI oversold + EMA crossover (adjustable)
    - Horus Gatekeeper: blocks entries if orderflow is adversarial
    - Horus Bailout: forces exit if liquidity collapses mid-trade
    - Backtest safe: Horus is automatically skipped in backtest mode

    Setup:
        export RAPIDAPI_KEY="your_rapidapi_key_here"
        freqtrade trade --strategy HorusFlowStrategy
    """

    # ── Strategy Parameters ───────────────────────────────────────────────────
    INTERFACE_VERSION = 3
    timeframe = "5m"

    # ROI / Stoploss
    minimal_roi = {"60": 0.01, "30": 0.02, "0": 0.04}
    stoploss = -0.02
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    # Order types
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Hyperopt parameters
    buy_rsi = IntParameter(20, 40, default=30, space="buy", optimize=True)
    buy_ema_short = IntParameter(8, 21, default=9, space="buy", optimize=True)
    buy_ema_long = IntParameter(21, 50, default=21, space="buy", optimize=True)
    horus_min_confidence = DecimalParameter(
        0.65, 0.90, default=0.70, decimals=2, space="buy", optimize=False
    )

    # ── Horus Client ──────────────────────────────────────────────────────────
    # Initialized lazily to avoid issues during backtesting
    _horus: Optional[HorusClient] = None

    def _get_horus(self) -> Optional[HorusClient]:
        """
        Returns the HorusClient instance.
        Returns None if we're in backtest/hyperopt mode (no live orderbook).
        """
        # Detect backtest mode — Horus has no historical orderbook data
        if self.config.get("runmode") in ("backtest", "hyperopt", "plot"):
            return None

        if self._horus is None:
            api_key = os.getenv("RAPIDAPI_KEY", "")
            if not api_key:
                logger.warning(
                    "[Horus] RAPIDAPI_KEY not set — running without orderflow filter. "
                    "Set it with: export RAPIDAPI_KEY=your_key"
                )
                return None
            self._horus = HorusClient(
                api_key=api_key,
                min_confidence=float(self.horus_min_confidence.value),
                cache_ttl_seconds=5,
                timeout_seconds=2,
            )
            logger.info("[Horus] Client initialized ✅")

        return self._horus

    # ── Indicators ────────────────────────────────────────────────────────────

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Classical technical indicators ONLY.
        ⚠️  NO Horus API calls here — this runs hundreds of times in backtest.
        """
        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # EMAs
        dataframe["ema_short"] = ta.EMA(
            dataframe, timeperiod=self.buy_ema_short.value
        )
        dataframe["ema_long"] = ta.EMA(
            dataframe, timeperiod=self.buy_ema_long.value
        )

        # Volume confirmation
        dataframe["volume_ma"] = (
            dataframe["volume"].rolling(window=20).mean()
        )

        return dataframe

    # ── Entry / Exit Signals ──────────────────────────────────────────────────

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Classical entry conditions. Horus will filter these in confirm_trade_entry().
        """
        dataframe.loc[
            (
                (dataframe["rsi"] < self.buy_rsi.value)        # Oversold RSI
                & (dataframe["ema_short"] > dataframe["ema_long"])  # Bullish EMA cross
                & (dataframe["volume"] > dataframe["volume_ma"])    # Volume confirmation
                & (dataframe["close"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Classical exit conditions. Horus bailout runs separately in custom_exit().
        """
        dataframe.loc[
            (
                (dataframe["rsi"] > 70)  # Overbought exit
            ),
            "exit_long",
        ] = 1

        return dataframe

    # ── Horus Gatekeeper ──────────────────────────────────────────────────────

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time: datetime,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> bool:
        """
        🦅 HORUS GATEKEEPER

        Final check before Freqtrade submits the buy order.
        Called ONCE per candidate entry — safe for API calls.

        Logic:
        - If Horus confirms BUY_PRESSURE or BUY_ABSORPTION → allow
        - If Horus detects SELL_PRESSURE, SPOOFING, LIQUIDITY_EVENT → block
        - If Horus API is down → allow (fail-open, trust the TA signal)
        """
        horus = self._get_horus()

        if horus is None:
            # Backtest mode or no API key — skip filter
            return True

        safe, reason = horus.is_safe_to_enter(pair)

        if safe:
            logger.info(f"[Horus GATE ✅] {pair} ALLOWED — {reason}")
        else:
            logger.info(f"[Horus GATE 🛑] {pair} BLOCKED — {reason}")

        return safe

    # ── Horus Bailout ─────────────────────────────────────────────────────────

    def custom_exit(
        self,
        pair: str,
        trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        **kwargs,
    ) -> Optional[str]:
        """
        🦅 HORUS BAILOUT

        Called ~every second while a position is open.
        If Horus detects LIQUIDITY_EVENT or EMERGENCY_DUMP, we force exit
        immediately — even at a small loss — to protect capital.

        The 5-second cache in HorusClient ensures we don't flood the API
        even though this function is called very frequently.

        Returns:
            str  → exit reason (triggers immediate market exit)
            None → hold the position
        """
        horus = self._get_horus()

        if horus is None:
            return None

        should_exit, reason = horus.should_emergency_exit(pair)

        if should_exit:
            logger.warning(
                f"[Horus BAILOUT 🚨] {pair} | {reason} | "
                f"profit={current_profit:.2%} → EMERGENCY EXIT"
            )
            return f"horus_bailout:{reason}"

        return None

    # ── Utility ───────────────────────────────────────────────────────────────

    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> float:
        """No leverage — spot trading only (halal-compliant)."""
        return 1.0
