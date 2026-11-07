"""Freqtrade 2026.10 paper example. Existing API walls become frozen exit bounds."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

from freqtrade.strategy import IStrategy, stoploss_from_absolute
from pandas import DataFrame

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE if (HERE / "hk_strategy_core.py").is_file() else HERE.parents[1] / "strategies"))
from hk_strategy_core import LevelsFeed, LongPlan, Timeline


class HunterKillerWalls(IStrategy):
    INTERFACE_VERSION = 3
    can_short = False
    timeframe = "5m"
    startup_candle_count = 1
    process_only_new_candles = True
    minimal_roi = {}
    stoploss = -0.15
    use_custom_stoploss = True
    use_exit_signal = True
    position_adjustment_enable = False
    order_types = {"entry": "market", "exit": "market", "stoploss": "market", "stoploss_on_exchange": False}

    def bot_start(self, **kwargs):
        if not self.config.get("dry_run", True):
            raise ValueError("This teaching example allows paper trading only")
        options = self.config.get("hk_levels", {})
        self._feed = LevelsFeed(key=options.get("key"), probe=options.get("probe", False))
        mode = getattr(self.config.get("runmode"), "value", self.config.get("runmode", ""))
        self._historical = mode not in {"dry_run", "live"}
        if self._historical and not options.get("replay"):
            raise ValueError("Historical runs require an explicit hk_levels.replay file")
        self._timeline = (Timeline.read(options["replay"], allow_publication_proxy=bool(options.get("public_wall_proxy")))
                          if self._historical else self._feed.timeline)

    def bot_loop_start(self, current_time: datetime, **kwargs):
        if not self._historical:
            self._feed.poll(current_time.timestamp())

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["hk_entry_tag"] = None
        if metadata["pair"] != "BTC/USDT":
            return dataframe
        for index, row in dataframe.iterrows():
            # Freqtrade dates are candle opens. The decision uses its completed close.
            decision_at = row["date"].timestamp() + 300
            sample = self._timeline.at(decision_at)
            plan = sample.long_plan(float(row["close"]), decision_at) if sample else None
            if plan is not None:
                dataframe.at[index, "hk_entry_tag"] = plan.tag()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        mask = dataframe["hk_entry_tag"].notna() & (dataframe["volume"] > 0)
        dataframe.loc[mask, "enter_long"] = 1
        dataframe.loc[mask, "enter_tag"] = dataframe.loc[mask, "hk_entry_tag"]
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["exit_long"] = 0
        return dataframe

    def confirm_trade_entry(self, pair, order_type, amount, rate, time_in_force,
                            current_time, entry_tag, side, **kwargs):
        plan = LongPlan.from_tag(entry_tag)
        return bool(pair == "BTC/USDT" and side == "long" and plan
                    and 0 <= current_time.timestamp() - plan.available_at <= 900
                    and plan.stop < rate < plan.target
                    and (rate - plan.stop) / rate <= 0.15
                    and plan.target - rate >= rate - plan.stop)

    def custom_stoploss(self, pair, trade, current_time, current_rate,
                        current_profit, after_fill=False, **kwargs):
        plan = LongPlan.from_tag(trade.enter_tag)
        if plan is None or current_rate <= plan.stop:
            return None
        return stoploss_from_absolute(plan.stop, current_rate, is_short=False, leverage=1.0)

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        plan = LongPlan.from_tag(trade.enter_tag)
        if plan is None:
            return "missing_wall_plan"
        if current_rate <= plan.stop:
            return "wall_stop"
        if current_rate >= plan.target:
            return "wall_target"
        if (current_time - trade.open_date_utc).total_seconds() >= 86400:
            return "wall_time_limit"
        return None
