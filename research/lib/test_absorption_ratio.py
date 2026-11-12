"""uv run --with numpy python research/lib/test_absorption_ratio.py"""

from __future__ import annotations

import math
from datetime import date

import common as c
import harness
import numpy as np
import stats
from harness import SECTORS, Panel, decide_time, load_history

IDEA = "absorption-ratio"
START = date(2002, 1, 1)  # first full month in which the shift exists
SPLIT = date(2011, 1, 1)  # the paper's data end in 2010
_signal: dict[str, object] = {}


def _shift(x: np.ndarray) -> np.ndarray:
    """(15-day mean - 252-day mean) / 252-day standard deviation, at each row (causal)."""
    out = np.full(len(x), np.nan)
    for i in range(251, len(x)):
        year = x[i - 251 : i + 1]
        if not np.isnan(year).any() and year.std() > 0:
            out[i] = (x[i - 14 : i + 1].mean() - year.mean()) / year.std()
    return out


def absorption(r: np.ndarray, upto: int | None = None) -> np.ndarray:
    """Share of variance in the top 2 eigenvectors, 500 rows, 250-row half-life, per row."""
    n = len(r) if upto is None else upto
    out = np.full(len(r), np.nan)
    w = 0.5 ** (np.arange(500)[::-1] / 250)
    for i in range(499, n):
        x = r[i - 499 : i + 1]
        if np.isnan(x).any():
            continue
        cov = (x * w[:, None]).T @ x / w.sum()
        ev = np.linalg.eigvalsh(cov)
        out[i] = ev[-2:].sum() / ev.sum()
    return out


def signal(period: str) -> tuple[Panel, np.ndarray, np.ndarray]:
    """Sector panel plus the two shift series on its SPY-date grid (row i uses rows <= i)."""
    if period not in _signal:
        pan = Panel(load_history(period, True, [*SECTORS, "SPY"]))
        r = np.diff(np.log(pan.grid), axis=0)
        r = np.vstack([np.full((1, r.shape[1]), np.nan), r])  # row i = return into grid day i
        sectors = r[:, : len(SECTORS)]
        ar = absorption(sectors)
        check = absorption(sectors[:3000], 3000)  # causality: truncating the data changes nothing
        assert np.allclose(check[2900:3000], ar[2900:3000], equal_nan=True)
        spy = r[:, len(SECTORS)]
        vol = np.full(len(spy), np.nan)
        for i in range(20, len(spy)):
            vol[i] = spy[i - 19 : i + 1].std()
        _signal[period] = (pan, _shift(ar), _shift(vol))
    return _signal[period]  # type: ignore[return-value]


def rule(period: str, which: int, risk: list[str]) -> c.ResearchStrategy:
    """Equal weight; risk assets go to cash while the chosen shift (0 = AR, 1 = vol) is above 1."""

    def f(view: c.View) -> c.Weights:
        pan, *series = signal(period)
        row = pan.view(decide_time(view.today)).n_grid - 1
        sh = series[which][row] if row >= 0 else math.nan
        held = c.live(view)
        off = (not math.isnan(sh)) and sh > 1
        return {s: 1 / len(held) for s in held if not (off and s in risk)}

    return f


def halves(a: harness.Run, b: harness.Run) -> str:
    out = []
    for name, lo, hi in [
        ("2002-2010", START, date(2010, 12, 31)),
        ("2011-2025", SPLIT, a.days[-1]),
    ]:
        x, y = a.rets_between(lo, hi), b.rets_between(lo, hi)
        if len(x) > 250:
            out.append(f"{name}: {stats.sharpe(x):.2f} vs {stats.sharpe(y):.2f}")
    return "; ".join(out)


def block(title: str, name: str, variant: str, risk: list[str], kind: str, out: list[str]):
    u = c.ctx(name)
    v = c.go(IDEA, variant, c.weekly(rule("train", 0, risk)), u, kind, start=START)
    t = c.go(IDEA, "vol-shift", c.weekly(rule("train", 1, risk)), u, "baseline", start=START)
    e = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), u, "baseline", log=False,
             start=START)  # fmt: skip
    out += [f"## {title}", "", c.table([v, t, e], versus=t), ""]
    out += [f"Sharpe, rule vs twin, before and after publication: {halves(v, t)}", ""]
    return v, t, e


def main() -> None:
    out = ["# absorption-ratio: market tightness from sector eigenvalues", ""]
    out += ["Card: `cards/absorption-ratio.md`. All runs start 2002-01-01.", ""]
    pan, ar_shift, vol_shift = signal("train")
    ok = ~np.isnan(ar_shift) & ~np.isnan(vol_shift)
    out += [
        f"Share of weeks-days with the signal on (shift > 1): absorption ratio "
        f"{(ar_shift[ok] > 1).mean():.0%}, volatility twin {(vol_shift[ok] > 1).mean():.0%}; "
        f"correlation of the two shifts {np.corrcoef(ar_shift[ok], vol_shift[ok])[0, 1]:.2f}.",
        "",
    ]
    v, t, e = block(
        "The six live assets", "six", "six", ["SPY", "QQQ", "BTC", "ETH"], "variant", out
    )
    out += ["Total return inside each stress window:", "", c.stress_table([v, t, e]), ""]
    v2, t2, _ = block("SPY alone", "SPY", "spy", ["SPY"], "variant", out)
    signs = {}
    risk = ["IWM", "EFA", "EEM", "VNQ", "DBC", "SLV"]
    ve, te, _ = block("Out of universe: 8 other ETFs", "etf", "six", risk, "robustness", out)
    signs["etf"] = c.describe(ve)["sharpe"] - c.describe(te)["sharpe"]
    d = []
    for nm in ["N225", "FTSE", "GDAXI"]:
        vi, ti, _ = block(f"Out of universe: {nm} alone", nm, "six", [nm], "robustness", out)
        d.append(c.describe(vi)["sharpe"] - c.describe(ti)["sharpe"])
    signs["idx"] = sum(d) / len(d)

    a, b = c.align(v, t)
    diff, pval, _, _ = stats.sharpe_diff_boot(a, b)
    ep, et = c.era_sharpes(v), c.era_sharpes(t)
    both = [n for n in ep if not (math.isnan(ep[n]) or math.isnan(et[n]))]
    ahead = sum(ep[n] > et[n] for n in both)
    post = stats.sharpe(v.rets_between(SPLIT, v.days[-1])) - stats.sharpe(
        t.rets_between(SPLIT, t.days[-1])
    )
    dv, dt, de = c.describe(v), c.describe(t), c.describe(e)
    bars = [
        ("1. Sharpe beats twin `vol-shift` with p < 0.10", diff > 0 and pval < 0.10,
         f"difference {diff:+.2f}, p = {pval:.2f}"),
        (f"2. Ahead of the twin in at least 3 of {len(both)} eras", ahead >= 3,
         f"{ahead} of {len(both)}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Same sign out of universe in both applicable sets",
         diff > 0 and all(x > 0 for x in signs.values()),
         ", ".join(f"{k} {x:+.2f}" for k, x in signs.items())),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) Not behind the twin after publication, 2011-2025", post >= 0, f"{post:+.2f}"),
    ]  # fmt: skip
    out += ["## Pass bar (primary variant `six`)", ""]
    out += [f"- {'PASS' if ok_ else 'FAIL'}: {text} ({detail})" for text, ok_, detail in bars]
    out += ["", f"**{'PASSES' if all(x for _, x, _ in bars) else 'FAILS'} train.**", ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
