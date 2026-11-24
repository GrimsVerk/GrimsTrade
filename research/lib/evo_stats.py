"""Data-snooping tests for a rule search (research/evo-1.md, "The correction").

White's Reality Check (2000) and Hansen's SPA (2005) on Sharpe differences to a benchmark, with
the stationary bootstrap. The statistic of a rule is d = Sharpe(rule) - Sharpe(benchmark) on the
same days. Rules arrive in chunks (`SnoopTest.add`), so the universe never has to be in memory
at once: every chunk is resampled with the same fixed draws and only running maxima are kept.

A resample only needs how often each day was drawn: with the count matrix C (draws x days), the
resampled mean of every rule is C @ R / n and the mean of squares is C @ R**2 / n.
"""

from __future__ import annotations

import math

import numpy as np
import stats

_TIE = 1e-9  # a draw that ties the statistic up to rounding counts as reaching it


def _sharpes(m1: np.ndarray, m2: np.ndarray) -> np.ndarray:
    """Annualised Sharpe from first and second moments; 0 where the series does not move."""
    var = np.maximum(m2 - m1 * m1, 0.0)
    sd = np.sqrt(var)
    out = np.zeros_like(m1)
    np.divide(m1, sd, out=out, where=sd > 1e-15)
    return out * math.sqrt(stats.DAYS)


class SnoopTest:
    """Reality Check and SPA over every rule added, against one benchmark series."""

    def __init__(
        self, bench: np.ndarray, draws: int = 1000, mean_block: float = 20, seed: int = 0
    ) -> None:
        self.n = len(bench)
        rng = np.random.default_rng(seed)
        counts = np.zeros((draws, self.n))
        for b in range(draws):
            idx = stats._stationary_indices(self.n, mean_block, rng)
            counts[b] = np.bincount(idx, minlength=self.n)
        self._c = counts / self.n
        bench = np.asarray(bench, dtype=float)
        m1, m2 = np.array([bench.mean()]), np.array([(bench**2).mean()])
        self.bench_sharpe = float(_sharpes(m1, m2)[0])
        self._bench_boot = _sharpes(self._c @ bench, self._c @ bench**2)  # (draws,)
        self.rules = 0
        self.best_d = -math.inf
        self.best_t = -math.inf  # best studentised difference
        self._rc_max = np.full(draws, -math.inf)
        # SPA running maxima per draw for the lower, consistent and upper recentring
        self._spa_max = np.full((3, draws), -math.inf)

    def add(self, r: np.ndarray) -> np.ndarray:
        """Add a chunk of rules, daily returns of shape (days, rules). Returns their d."""
        r = np.asarray(r, dtype=float)
        if r.ndim == 1:
            r = r[:, None]
        if r.shape[0] != self.n:
            raise ValueError("rules must cover the benchmark's days")
        d = _sharpes(r.mean(axis=0), (r * r).mean(axis=0)) - self.bench_sharpe
        boot = _sharpes(self._c @ r, self._c @ (r * r)) - self._bench_boot[:, None]
        self.rules += r.shape[1]
        self.best_d = max(self.best_d, float(d.max()))
        # Reality Check: the luck of the best, every rule recentred on its own d.
        self._rc_max = np.maximum(self._rc_max, (boot - d).max(axis=1))
        # SPA: studentise by the bootstrap standard error of each d; a rule that never differs
        # from the benchmark (se 0) carries no information and is left out.
        se = boot.std(axis=0)
        ok = se > 1e-12
        if ok.any():
            dk, bk, sk = d[ok], boot[:, ok], se[ok]
            self.best_t = max(self.best_t, float((dk / sk).max()))
            clearly_bad = dk < -sk * math.sqrt(2 * math.log(math.log(self.n)))
            centres = (
                np.maximum(dk, 0.0),  # lower: every bad rule is as bad as it looks
                np.where(clearly_bad, 0.0, dk),  # consistent: only the clearly bad ones are
                dk,  # upper: no rule is bad (the Reality Check's assumption)
            )
            for k, g in enumerate(centres):
                self._spa_max[k] = np.maximum(self._spa_max[k], ((bk - g) / sk).max(axis=1))
        return d

    def result(self) -> dict[str, float]:
        if self.rules == 0:
            raise ValueError("no rules added")
        t = max(self.best_t, 0.0)
        spa = [float((np.maximum(m, 0.0) >= t - _TIE).mean()) for m in self._spa_max]
        return {
            "rules": float(self.rules),
            "best_d": self.best_d,
            "rc_p": float((self._rc_max >= self.best_d - _TIE).mean()),
            "spa_lower_p": spa[0],
            "spa_consistent_p": spa[1],
            "spa_upper_p": spa[2],
        }


def effective_n(r: np.ndarray) -> float:
    """Participation ratio of the correlation matrix of the rules' daily returns (days x rules):
    (sum of eigenvalues)^2 / sum of squared eigenvalues. K for uncorrelated rules, 1 for copies."""
    r = np.asarray(r, dtype=float)
    sd = r.std(axis=0)
    z = (r[:, sd > 0] - r[:, sd > 0].mean(axis=0)) / sd[sd > 0]
    k = z.shape[1]
    if k == 0:
        return 0.0
    corr = z.T @ z / z.shape[0]
    return float(k * k / (corr * corr).sum())


def deflated_best(d: np.ndarray, se_best: float, n_trials: float) -> float:
    """P(the best rule's true Sharpe difference > the expected best of n unskilled tries), with
    the spread of differences `d` seen across the universe (Bailey & Lopez de Prado 2014)."""
    d = np.asarray(d, dtype=float)
    expected = stats.expected_max_sharpe(max(int(round(n_trials)), 1), float(d.var()))
    return float(stats._N.cdf((float(d.max()) - expected) / se_best)) if se_best > 0 else 0.0
