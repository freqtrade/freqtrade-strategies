# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
"""
HMMRegimeFilter

An EMA trend entry that is only taken while a 3-state Gaussian hidden Markov model, fitted
to the pair's own log returns, does not put the market in its turbulent regime.

The HMM is fitted with Baum-Welch (scaled forward-backward) in plain numpy, so the strategy
needs nothing beyond a standard freqtrade install. With the same starting parameters the fit
matches hmmlearn's GaussianHMM (no covariance prior) to about 1e-15.

States are ordered by volatility after every fit: 0 = calm, 1 = normal, 2 = turbulent.
On intraday crypto returns the state means are close to zero and poorly identified, while the
volatility levels separate cleanly, so the regime is defined by volatility, not by drift.

No lookahead:
- The model is refitted every `hmm_refit_every` candles on the `hmm_train_window` returns
  *before* the refit candle, and only forward (filtered) probabilities are used: the
  probability at a candle depends on returns up to and including that candle. Smoothed
  (forward-backward) or Viterbi states over the whole dataframe would look ahead and are
  never used for signals.
- Refit candles are anchored to absolute time (candle number since the epoch modulo
  `hmm_refit_every`), not to the first row of the dataframe, so backtest, dry-run and live
  fit the same windows once `startup_candle_count` candles are available.

Entry: P(turbulent) < buy_max_turbulent, EMA fast > EMA slow and close > EMA slow.
Exit:  EMA fast crosses below EMA slow, or the stoploss.

Cost: a 500-return fit takes well under a second; a backtest runs one fit per pair per
`hmm_refit_every` candles (about 52 per pair-year on 4h candles).

The regime model is adapted from srfm-lab's HMMRegimeDetector (MIT), rewritten with a full
Baum-Welch fit (the original fitted a Gaussian mixture and never updated its transition
matrix) and walk-forward filtering.

This is an example strategy for educational purposes. Run backtesting, lookahead-analysis
and recursive-analysis on your own pairs and timerange before using it.
"""

from functools import reduce

import numpy as np
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.exchange import timeframe_to_seconds
from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy
from technical import qtpylib


def _emission(x: np.ndarray, means: np.ndarray, stds: np.ndarray) -> np.ndarray:
    """Gaussian densities, shape (len(x), n_states), floored to avoid all-zero rows."""
    z = (x[:, None] - means[None, :]) / stds[None, :]
    dens = np.exp(-0.5 * z * z) / (stds[None, :] * np.sqrt(2.0 * np.pi))
    return np.maximum(dens, 1e-300)


def _forward(
    x: np.ndarray, start: np.ndarray, trans: np.ndarray, means: np.ndarray, stds: np.ndarray
):
    """Scaled forward pass. Returns filtered probabilities (T, K) and scale factors (T,)."""
    b = _emission(x, means, stds)
    n_obs, k = b.shape
    alpha = np.empty((n_obs, k))
    scale = np.empty(n_obs)
    a = start * b[0]
    for t in range(n_obs):
        if t > 0:
            a = (alpha[t - 1] @ trans) * b[t]
        s = a.sum()
        scale[t] = s
        alpha[t] = a / s
    return alpha, scale


def fit_gaussian_hmm(x: np.ndarray, n_states: int = 3, n_iter: int = 30, tol: float = 1e-6):
    """Baum-Welch for a Gaussian HMM on a 1-d series.

    Returns (start, trans, means, stds) with states sorted by volatility (ascending).
    """
    x = np.asarray(x, dtype=float)
    k = n_states
    # Initialise from return quantiles: state j gets the j-th slice of the sorted returns.
    srt = np.sort(x)
    parts = np.array_split(srt, k)
    means = np.array([p.mean() for p in parts])
    stds = np.array([max(p.std(), 1e-8) for p in parts])
    stds = np.maximum(stds, 0.25 * x.std() + 1e-12)
    trans = np.full((k, k), 0.05 / (k - 1))
    np.fill_diagonal(trans, 0.95)
    start = np.full(k, 1.0 / k)
    var_floor = (1e-3 * x.std()) ** 2 + 1e-18

    prev_ll = -np.inf
    for _ in range(n_iter):
        b = _emission(x, means, stds)
        alpha, scale = _forward(x, start, trans, means, stds)
        n_obs = len(x)
        beta = np.empty((n_obs, k))
        beta[-1] = 1.0
        for t in range(n_obs - 2, -1, -1):
            beta[t] = (trans @ (b[t + 1] * beta[t + 1])) / scale[t + 1]
        gamma = alpha * beta
        gamma /= gamma.sum(axis=1, keepdims=True)
        # Expected transitions: sum_t alpha_t(i) a_ij b_j(x_t+1) beta_t+1(j) / c_t+1
        right = (b[1:] * beta[1:]) / scale[1:, None]
        xi = alpha[:-1, :, None] * trans[None, :, :] * right[:, None, :]
        xi_sum = xi.sum(axis=0)

        start = gamma[0]
        trans = xi_sum / np.maximum(xi_sum.sum(axis=1, keepdims=True), 1e-300)
        weight = gamma.sum(axis=0)
        means = (gamma * x[:, None]).sum(axis=0) / weight
        var = (gamma * (x[:, None] - means[None, :]) ** 2).sum(axis=0) / weight
        stds = np.sqrt(np.maximum(var, var_floor))

        ll = float(np.log(scale).sum())
        if ll - prev_ll < tol:
            break
        prev_ll = ll

    order = np.argsort(stds)
    return start[order], trans[np.ix_(order, order)], means[order], stds[order]


class HMMRegimeFilter(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "4h"
    can_short = False

    # ROI disabled: exits come from the EMA cross and the stoploss.
    minimal_roi = {}
    stoploss = -0.08
    trailing_stop = False

    process_only_new_candles = True
    use_exit_signal = True
    exit_profit_only = False

    # HMM settings. Changing them changes the fitted windows, so they are not hyperoptable.
    hmm_states = 3
    hmm_train_window = 500  # about 83 days of 4h candles
    hmm_refit_every = 42  # one week of 4h candles
    hmm_iterations = 30

    startup_candle_count = hmm_train_window + hmm_refit_every

    buy_max_turbulent = DecimalParameter(0.05, 0.5, default=0.2, decimals=2, space="buy")
    buy_ema_fast = IntParameter(10, 40, default=20, space="buy")
    buy_ema_slow = IntParameter(50, 150, default=100, space="buy")

    plot_config = {
        "main_plot": {
            "ema_fast": {"color": "orange"},
            "ema_slow": {"color": "blue"},
        },
        "subplots": {
            "HMM regime": {
                "hmm_calm": {"color": "green"},
                "hmm_normal": {"color": "gray"},
                "hmm_turbulent": {"color": "red"},
            },
        },
    }

    def hmm_regime_probabilities(self, dataframe: DataFrame) -> np.ndarray:
        """Walk-forward filtered state probabilities, shape (len(dataframe), n_states).

        Rows without a full training window before them are NaN.
        """
        close = dataframe["close"].to_numpy(dtype=float)
        n = len(close)
        k = self.hmm_states
        out = np.full((n, k), np.nan)
        if n < 2:
            return out
        ret = np.zeros(n)
        ret[1:] = np.diff(np.log(close))

        w, step = self.hmm_train_window, self.hmm_refit_every
        # Candle number since the epoch, so refit points do not depend on where the data starts.
        tf_seconds = timeframe_to_seconds(self.timeframe)
        epoch_index = dataframe["date"].iloc[0].value // 10**9 // tf_seconds
        first_refit = (-epoch_index) % step
        refits = [r for r in range(first_refit, n, step) if r - w >= 1]
        if not refits:
            return out
        for r in refits:
            fit_data = ret[r - w : r]
            start, trans, means, stds = fit_gaussian_hmm(fit_data, k, self.hmm_iterations)
            end = min(r + step, n)
            # Filter from the start of the training window through the block, keep the block.
            alpha, _ = _forward(ret[r - w : end], start, trans, means, stds)
            out[r:end] = alpha[w:]
        return out

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        probs = self.hmm_regime_probabilities(dataframe)
        dataframe["hmm_calm"] = probs[:, 0]
        dataframe["hmm_normal"] = probs[:, 1]
        dataframe["hmm_turbulent"] = probs[:, 2]

        for val in self.buy_ema_fast.range:
            dataframe[f"ema_fast_{val}"] = ta.EMA(dataframe, timeperiod=val)
        for val in self.buy_ema_slow.range:
            dataframe[f"ema_slow_{val}"] = ta.EMA(dataframe, timeperiod=val)
        dataframe["ema_fast"] = dataframe[f"ema_fast_{self.buy_ema_fast.value}"]
        dataframe["ema_slow"] = dataframe[f"ema_slow_{self.buy_ema_slow.value}"]
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        fast = dataframe[f"ema_fast_{self.buy_ema_fast.value}"]
        slow = dataframe[f"ema_slow_{self.buy_ema_slow.value}"]
        conditions = [
            dataframe["hmm_turbulent"] < self.buy_max_turbulent.value,
            fast > slow,
            dataframe["close"] > slow,
            dataframe["volume"] > 0,
        ]
        dataframe.loc[reduce(lambda a, b: a & b, conditions), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        fast = dataframe[f"ema_fast_{self.buy_ema_fast.value}"]
        slow = dataframe[f"ema_slow_{self.buy_ema_slow.value}"]
        dataframe.loc[
            qtpylib.crossed_below(fast, slow) & (dataframe["volume"] > 0),
            "exit_long",
        ] = 1
        return dataframe
