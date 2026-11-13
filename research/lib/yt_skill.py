"""The ideas-1 indicators scored alone (no rule): which are worth keeping as RL inputs.

    uv run --with numpy python research/lib/yt_skill.py

Same method as `macro_skill.py`: each indicator as known on the Friday (week and month values
count from the day after the first bar of the next period; macro from the day after release)
against the next 28-day log return of SPY, TLT, GLD and BTC. Spearman rho on all Fridays, t from
every fourth Friday, and the rank correlation with the asset's own 12-month return. Train only.
No backtest; nothing logged in tries.md.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from datetime import date, timedelta

import harness
import idea_yt as yt
import macro
import numpy as np
from macro_skill import ASSETS, spearman

Series = Callable[[np.ndarray, np.ndarray, str], macro.Step]


def _step(dates: np.ndarray, idx: list[int], vals: list[float]) -> macro.Step:
    """Value computed at bar idx[k] - 1, usable from the day after bar idx[k]'s date."""
    days = [date.fromordinal(int(dates[i])) + timedelta(days=1) for i in idx]
    return macro.Step(days, vals)


def bbwp(dates: np.ndarray, close: np.ndarray, s: str) -> macro.Step:
    ends = yt._period_ends(dates, yt._week)
    w = close[ends]
    bbw = np.full(len(w), np.nan)
    idx, vals = [], []
    for k in range(19, len(w)):
        x = w[k - 19 : k + 1]
        bbw[k] = 4 * x.std() / x.mean()
        prev = bbw[max(19, k - 252) : k]
        if len(prev) >= 104:
            idx.append(int(ends[k]) + 1)
            vals.append(100 * float(np.mean(prev < bbw[k])))
    return _step(dates, idx, vals)


def srsi_k(dates: np.ndarray, close: np.ndarray, s: str) -> macro.Step:
    ends = yt._period_ends(dates, yt._month)
    rsi = yt._rsi(close[ends])
    st = np.full(len(rsi), np.nan)
    for k in range(13, len(rsi)):
        win = rsi[k - 13 : k + 1]
        if not np.isnan(win).any() and win.max() > win.min():
            st[k] = 100 * (rsi[k] - win.min()) / (win.max() - win.min())
    idx, vals = [], []
    for k in range(2, len(rsi)):
        v = float(st[k - 2 : k + 1].mean())
        if not math.isnan(v):
            idx.append(int(ends[k]) + 1)
            vals.append(v)
    return _step(dates, idx, vals)


def since_breakout(dates: np.ndarray, close: np.ndarray, s: str) -> macro.Step:
    """Breakout dates (card 3's rule); the feature is days since the latest, read on the day."""
    t = yt.trig_ath(dates, close, s)
    idx = [int(i) for i in np.flatnonzero(t)]
    return _step(dates, idx, [float(dates[i]) for i in idx])


def near_high(dates: np.ndarray, close: np.ndarray, s: str) -> macro.Step:
    idx = list(range(251, len(close)))
    vals = [float(close[i] / close[i - 251 : i + 1].max()) for i in idx]
    return macro.Step([date.fromordinal(int(dates[i])) + timedelta(days=1) for i in idx], vals)


def _macro_steps() -> dict[str, macro.Step]:
    def pct(snap: dict[date, float], obs: list[date]) -> float:
        prev = [snap[o] for o in obs[-241:-1]]
        return 100 * float(np.mean(np.array(prev) < snap[obs[-1]])) if len(prev) >= 120 else math.nan

    def chg(days: int, log: bool) -> Callable[[list[date], list[float], int], float]:
        def f(obs: list[date], vals: list[float], i: int) -> float:
            a = yt._price_before(obs, vals, i, days)
            if log:
                return math.log(vals[i] / a) if a > 0 and vals[i] > 0 else math.nan
            return vals[i] - a

        return f

    return {
        "umcsent_pct": macro.vintage_feature(macro.vintage_records("UMCSENT"), pct),
        "wti_chg182": macro.market_feature(macro.market_records("DCOILWTICO"), chg(182, True)),
        "dgs10_chg91": macro.market_feature(macro.market_records("DGS10"), chg(91, False)),
        "fng": yt.fng_step(),
    }


PER_ASSET: dict[str, Series] = {
    "bbwp": bbwp,
    "srsi_k": srsi_k,
    "days_since_breakout": since_breakout,
    "near_high": near_high,
}


def main() -> None:
    glob = _macro_steps()
    hist = harness.load_history("train")
    out = [
        "# ideas-1 indicators scored alone (no rule)",
        "",
        "Run ideas-1. Script `lib/yt_skill.py`, method of `macro_skill.py`: each indicator as",
        "known on the Friday against the next 28-day log return; rho = Spearman on all Fridays,",
        "t from every fourth Friday (non-overlapping); `vs 12m` = rank correlation with the asset's",
        "own 12-month return. Train only. 8 indicators x 4 assets x 2 windows: a few |t| > 2 are",
        "expected from luck. `days_since_breakout` is days since card 3's breakout (any age).",
        "",
    ]
    for start in (date(1994, 2, 4), date(2003, 1, 3)):
        out += [f"## Fridays from {start}", ""]
        out += ["| Indicator | " + " | ".join(f"{a} rho (t) | {a} vs 12m" for a in ASSETS) + " |"]
        out += ["|---|" + "---:|---:|" * len(ASSETS)]
        names = list(PER_ASSET) + list(glob)
        cells: dict[str, list[str]] = {n: [] for n in names}
        for a in ASSETS:
            bars = hist[a]
            d = np.array([b.date.toordinal() for b in bars])
            c = np.array([b.close for b in bars])
            steps = {n: f(d, c, a) for n, f in PER_ASSET.items()} | glob
            xs, ys, ts = [], [], []
            fr = start
            while fr <= harness.TRAIN_END - timedelta(days=28):
                i = int(np.searchsorted(d, fr.toordinal(), side="right")) - 1
                j = int(np.searchsorted(d, fr.toordinal() + 28, side="right")) - 1
                k = int(np.searchsorted(d, fr.toordinal() - 365, side="right")) - 1
                if k >= 0 and i > k and d[0] <= fr.toordinal() - 365:
                    xs.append(fr)
                    ys.append(math.log(c[j] / c[i]))
                    ts.append(math.log(c[i] / c[k]))
                fr += timedelta(days=7)
            for n in names:
                v = [steps[n].at(x) for x in xs]
                if n == "days_since_breakout":
                    v = [x.toordinal() - b for x, b in zip(xs, v, strict=True)]
                x = np.array(v, dtype=float)
                ok = ~np.isnan(x)
                y, t, x = np.array(ys)[ok], np.array(ts)[ok], x[ok]
                rho = spearman(x, y)
                sub = np.arange(len(x)) % 4 == 0
                r4 = spearman(x[sub], y[sub])
                tv = r4 * math.sqrt((sub.sum() - 2) / max(1 - r4 * r4, 1e-9)) if r4 == r4 else 0
                cells[n].append(f"{rho:+.2f} ({tv:+.1f}) | {spearman(x, t):+.2f}")
        out += [f"| {n} | " + " | ".join(cells[n]) + " |" for n in names]
        out.append("")
    text = "\n".join(out)
    (harness.RESEARCH / "results" / "yt-skill.md").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
