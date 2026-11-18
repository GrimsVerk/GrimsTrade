"""uv run --with numpy python research/lib/idea_wide1_contagion.py
(card: cards/contagion-catchup.md)"""

from __future__ import annotations

import math
from datetime import timedelta

import common as c
import harness
import numpy as np
import wide1 as w
import wide1_rules as rules
from harness import OOU_COINS, OOU_ETFS, SECTORS

IDEA = "contagion-catchup"
ETF21 = ["SPY", "QQQ", "TLT", "GLD", *OOU_ETFS, *SECTORS]
COINS = ["BTC", "ETH", *OOU_COINS]
SIGNALS = ("catchup", "nbr", "rev7")


def week_signals(view: c.View) -> tuple[list[str], dict[str, np.ndarray], list[bool]]:
    """(eligible assets, signals, in-trend flags), from closes visible at the decision."""
    key = ("wide1-contagion", view.today)
    memo = view.panel.cache
    if key not in memo:
        held = c.live(view)
        z = np.full(len(held), np.nan)
        for k, s in enumerate(held):
            r7 = c.trailing_logret(view, s, 7)
            vol = c.vol_series(view, s, 60)
            if len(vol) and vol[-1] > 0 and not math.isnan(r7):
                z[k] = min(5.0, max(-5.0, r7 / (vol[-1] * math.sqrt(7 / 365))))
        cols = [view.syms.index(s) for s in held]
        daily = view.grid_logret(252)[:, cols]
        if len(daily) < 252:
            daily = np.full((2, len(held)), np.nan)
        lam, cu = rules.catchup(z, daily)
        sig = {"catchup": cu, "nbr": np.where(np.isfinite(z), lam, np.nan), "rev7": -z}
        memo[key] = (held, sig, [c.tsmom_signal(view, s) for s in held])
    return memo[key]  # type: ignore[return-value]


def top_ts(which: str) -> c.ResearchStrategy:
    def f(view: c.View) -> c.Weights:
        held, sig, up = week_signals(view)
        if not held:
            return {}
        k = max(1, int(len(held) / 3 + 0.5))
        return rules.top_slots(held, sig[which], up, k)

    return c.weekly(f)


def forward(panel: harness.Panel, s: str, d_ord: int) -> float:
    """Return from the first open after decision day `d` to the first open after `d + 7`."""
    days = panel.ord[s]
    i = int(np.searchsorted(days, d_ord, side="right"))
    j = int(np.searchsorted(days, d_ord + 7, side="right"))
    return float(panel.o[s][j] / panel.o[s][i] - 1) if j < len(days) and j > i else math.nan


def ic_rows(u: c.Ctx) -> tuple[list[str], dict[str, tuple[float, float, float, float]]]:
    """Weekly rank IC of each signal against the coming week's open-to-open return."""
    ics: dict[str, list[float]] = {k: [] for k in SIGNALS}
    d = u.start + timedelta(days=(4 - u.start.weekday()) % 7)
    while d <= u.end - timedelta(days=14):
        held, sig, _ = week_signals(u.panel.view(harness.decide_time(d)))
        fwd = np.array([forward(u.panel, s, d.toordinal()) for s in held])
        for k in SIGNALS:
            x = rules.rank_ic(sig[k], fwd) if len(held) >= 5 else math.nan
            if not math.isnan(x):
                ics[k].append(x)
        d += timedelta(days=7)
    lines = [
        "| Signal | Weeks | Mean rank IC | t | Share of weeks > 0 | First half | Second half |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    stats_: dict[str, tuple[float, float, float, float]] = {}
    for k in SIGNALS:
        x = np.array(ics[k])
        if len(x) < 10:
            lines.append(f"| `{k}` | {len(x)} | - | - | - | - | - |")
            stats_[k] = (math.nan, math.nan, math.nan, math.nan)
            continue
        h = len(x) // 2
        t = w.tstat(x)
        stats_[k] = (float(x.mean()), t, float(x[:h].mean()), float(x[h:].mean()))
        lines.append(
            f"| `{k}` | {len(x)} | {x.mean():+.3f} | {t:+.1f} | {(x > 0).mean():.0%} | "
            f"{x[:h].mean():+.3f} | {x[h:].mean():+.3f} |"
        )
    return lines, stats_


def main() -> None:
    out = ["# contagion-catchup: buy the assets a shock has not reached yet", ""]
    out += ["Card: `cards/contagion-catchup.md`. Protocol: `protocol.md`.", ""]
    u = w.book_ctx("etf21", ETF21, 10)
    ts = c.go(IDEA, "TS", c.weekly(c.slots(c.tsmom_signal)), u, "baseline")
    ew = c.go(IDEA, "EW", c.weekly(c.equal_weight), u, "baseline")
    rev = c.go(IDEA, "rev7", top_ts("rev7"), u, "baseline")
    cu = c.go(IDEA, "catchup", top_ts("catchup"), u, "variant")
    nb = c.go(IDEA, "nbr", top_ts("nbr"), u, "variant")
    runs = [cu, nb, rev, ts, ew]
    out += [f"## The 21 ETFs, from {u.start}", "", c.table(runs, ts), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    lines, ic = ic_rows(u)
    out += ["Weekly rank IC (signal against the return from the next open to the open a week "
            "later, across the eligible ETFs):", "", *lines, ""]  # fmt: skip
    vs, vs_rev = w.versus(cu, ts), w.versus(cu, rev)
    vs_nb = w.versus(nb, ts)

    k = w.book_ctx("coin8", COINS, 6)
    ts_k = c.go(IDEA, "TS", c.weekly(c.slots(c.tsmom_signal)), k, "baseline")
    ew_k = c.go(IDEA, "EW", c.weekly(c.equal_weight), k, "baseline")
    cu_k = c.go(IDEA, "catchup", top_ts("catchup"), k, "robustness")
    out += [f"## Out of universe: 8 coins (BTC, ETH and the six other coins), from {k.start}", ""]
    out += [c.table([cu_k, ts_k, ew_k], ts_k), ""]
    lines_k, _ = ic_rows(k)
    out += [*lines_k, ""]
    vs_k = w.versus(cu_k, ts_k)

    dv, dt, de = c.describe(cu), c.describe(ts), c.describe(ew)
    d = vs["diff"]
    m, t, h1, h2 = ic["catchup"]
    bars = [
        ("1. `catchup` beats `TS` with p < 0.10", d > 0 and vs["p"] < 0.10,
         f"difference {d:+.2f}, p = {vs['p']:.2f}"),
        (f"2. Ahead of `TS` in at least 3 of {vs['eras']:.0f} eras", vs["ahead"] >= 3,
         f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than `TS`",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Same sign on the coin set after 30 bps", d > 0 and vs_k["diff"] > 0,
         f"{vs_k['diff']:+.2f} (p = {vs_k['p']:.2f})"),
        ("5. Beats `EW` on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. Beats `rev7` (plain one-week reversal) on Sharpe", vs_rev["diff"] > 0,
         f"{vs_rev['diff']:+.2f} (p = {vs_rev['p']:.2f})"),
        ("7. Weekly rank IC of `catchup`: t >= 3, positive in both halves",
         t >= 3 and h1 > 0 and h2 > 0, f"mean {m:+.3f}, t {t:+.1f}, halves {h1:+.3f} / {h2:+.3f}"),
    ]  # fmt: skip
    out += ["## Pass bar (primary variant `catchup`)", "", *w.bars_report(bars)]
    out += [f"`nbr` against `TS`: {vs_nb['diff']:+.2f} (p = {vs_nb['p']:.2f}), ahead in "
            f"{vs_nb['ahead']:.0f} of {vs_nb['eras']:.0f} eras.", ""]  # fmt: skip
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
