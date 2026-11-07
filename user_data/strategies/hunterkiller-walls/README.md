# Freqtrade wall example

```sh
curl --fail-with-body --max-time 20 https://hunterkiller.io/api/v1/levels/BTCUSDT
```

The keyless rollout is pending a live receipt; a 401 is a failure, not data.
[API key signup](https://hunterkiller.io/signup) and the
[agent documentation](https://hunterkiller.io/for-agents) describe the key path.
Free data is 2 hours behind on six coins. A supplied live key can consume credits.

`HunterKillerWalls.py` is a Freqtrade 2026.10 paper only strategy. It uses the
API's nearest lower wall as a stop and upper wall as a target. It requires a
price inside that pair and at least as much room to the target as to the stop.
The pair stays fixed for an open position. No parameter search was performed.
An unavailable feed cannot create a new position. Historical mode requires a
receipt file and never fetches today's walls.

From the canonical examples repository root:

```sh
python -m pip install ./packages/langchain
cp examples/freqtrade/HunterKillerWalls.py strategies/hk_strategy_core.py user_data/strategies/
```

Keep `dry_run: true`, a static `BTC/USDT` pair, one open position and a bounded
stake. `dry_run: false` is rejected. The optional `hk_levels.key` is application
supplied; an omitted key stays omitted. Never commit it or put it in logs.

## Historical public wall proxy

This is a historical public wall proxy, not an API replay or live performance.
The ledger retains actual public wall publications but not their original
snapshot age. Unknown time and delay remain null. The pair is reconstructed
with the unchanged public selector. Ambiguous observations become gaps.

| UTC period | Native Freqtrade net result, USDT |
| --- | ---: |
| November 5, 2026 | -4.01 |
| November 6, 2026 | -0.38 |
| Full window | -4.38 |

The fixed cohort uses real Bybit BTC/USDT spot candles. Starting simulated
cash was 1000 USDT, stake 100 USDT. All 5 closed positions lost. Assumed costs
are 0.10 percent fees plus a 0.05 percent adverse execution allowance per side,
encoded as a combined fee in native Freqtrade. Displayed daily numbers are
rounded; the full record keeps exact amounts. This does not establish a trading
advantage.

[All positions, losing periods, costs and reproduction commands](https://github.com/Irishman-Management-LLC/hunterkiller-examples/blob/71fcc2c41fbd/strategies/RESULTS.md)
are public. The native CI job runs the complete backtest with network disabled.
The [input manifest](https://github.com/Irishman-Management-LLC/hunterkiller-examples/blob/71fcc2c41fbd/strategies/data/20261105-20261107/dataset.manifest.json)
binds the dated candles and public wall observations. API snapshot capture began
November 7 for a second table no earlier than November 21, with coverage gaps
disclosed.

Affiliation: this example is maintained by Hunter Killer.

Canonical source and complete reproduction: https://github.com/Irishman-Management-LLC/hunterkiller-examples/tree/71fcc2c41fbd/examples/freqtrade .

The optional transport is not uploaded to PyPI yet. Clone the canonical repository and install `python -m pip install ./packages/langchain`; the shared helper sits beside the strategy in this contribution. No package upload or working keyless claim is made here.
