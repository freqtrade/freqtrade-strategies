"""Run inside the pinned Freqtrade image. Synthetic inputs, real framework API."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "user_data/strategies"))
from HunterKillerWalls import HunterKillerWalls
from test_core import fixture, T


class TestFreqtradeAdapter(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        replay = Path(self.folder.name) / "fixture.jsonl"
        replay.write_text(json.dumps({"received_at": T, "payload": fixture()}) + "\n")
        self.config = {"dry_run": True, "runmode": SimpleNamespace(value="backtest"),
                       "hk_levels": {"replay": str(replay)}}
        self.strategy = HunterKillerWalls(self.config)
        self.strategy.bot_start()

    def test_completed_candle_selects_only_its_known_receipt_and_backtest_never_polls(self):
        frame = pd.DataFrame({"date": pd.to_datetime([T - 600, T - 300], unit="s", utc=True),
                              "open": [100.0, 100.0], "high": [100.5, 100.5], "low": [99.5, 99.5],
                              "close": [100.0, 100.0], "volume": [10.0, 10.0]})
        frame = self.strategy.populate_indicators(frame, {"pair": "BTC/USDT"})
        frame = self.strategy.populate_entry_trend(frame, {"pair": "BTC/USDT"})
        self.assertTrue(pd.isna(frame.iloc[0].get("enter_long")))
        self.assertEqual(frame.iloc[1]["enter_long"], 1)
        tag = frame.iloc[1]["enter_tag"]
        now = datetime.fromtimestamp(T, timezone.utc)
        self.assertTrue(self.strategy.confirm_trade_entry("BTC/USDT", "market", 1, 100, "GTC", now, tag, "long"))
        self.assertFalse(self.strategy.confirm_trade_entry("BTC/USDT", "market", 1, 104, "GTC", now, tag, "long"))
        with patch.object(self.strategy._feed, "poll", side_effect=AssertionError("live HTTP in historical run")):
            self.strategy.bot_loop_start(now)

    def test_native_stop_helper_and_frozen_exit_walls(self):
        now = datetime.fromtimestamp(T, timezone.utc)
        trade = SimpleNamespace(enter_tag=f"hk:98:103:{T}", open_date_utc=now)
        self.assertAlmostEqual(self.strategy.custom_stoploss("BTC/USDT", trade, now, 100, 0, after_fill=True), 0.02)
        self.assertIsNone(self.strategy.custom_exit("BTC/USDT", trade, now, 100, 0))
        self.assertEqual(self.strategy.custom_exit("BTC/USDT", trade, now, 104, 0.04), "wall_target")
        self.assertEqual(self.strategy.custom_exit("BTC/USDT", trade, now, 97, -0.03), "wall_stop")
        later = datetime.fromtimestamp(T + 86401, timezone.utc)
        self.assertEqual(self.strategy.custom_exit("BTC/USDT", trade, later, 100, 0), "wall_time_limit")

    def test_live_capital_and_implicit_history_are_rejected(self):
        with self.assertRaises(ValueError):
            HunterKillerWalls({**self.config, "dry_run": False}).bot_start()
        with self.assertRaisesRegex(ValueError, "explicit hk_levels.replay"):
            HunterKillerWalls({"dry_run": True, "runmode": "backtest"}).bot_start()

    def test_future_prices_do_not_change_the_already_closed_prefix(self):
        frame = pd.DataFrame({"date": pd.to_datetime([T - 300, T, T + 300], unit="s", utc=True),
                              "open": [100.0, 100.0, 110.0], "high": [101.0, 101.0, 112.0],
                              "low": [99.0, 99.0, 109.0], "close": [100.0, 100.0, 111.0],
                              "volume": [10.0, 10.0, 10.0]})
        full = self.strategy.populate_indicators(frame.copy(), {"pair": "BTC/USDT"})
        prefix = self.strategy.populate_indicators(frame.iloc[:2].copy(), {"pair": "BTC/USDT"})
        self.assertEqual(full.iloc[:2]["hk_entry_tag"].tolist(), prefix["hk_entry_tag"].tolist())


if __name__ == "__main__":
    unittest.main()
