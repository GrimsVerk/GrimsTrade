"""diversifier-1: a held 1/7 merger-arb slot next to `tsmom12` (card `cards/diversifier-1.md`).

    uv run python research/lib/diversifier1.py fetch          # MERFX, MNA from Yahoo (keyless)
    uv run --with numpy python research/lib/diversifier1.py   # the one run (logs 2 rows)

Book: each Friday 6/7 x `tsmom12`'s weights on the six + 1/7 in the diversifier, always held once
it has a year of bars. Primary `merfx7` (variant), `mna7@mna` (robustness, from MNA's first
eligible day). `tsmom12` and equal weight are re-scored with `log=False` (already logged).
"""

from __future__ import annotations

import math
import sys
from datetime import UTC, date, datetime, timedelta

import common as c
import harness
import numpy as np
import stats
from harness import SYMS, Panel, Run, View, Weights

from grimstrade.data import ETF, UNIVERSE

IDEA = "diversifier-1"
DIVS = ["MERFX", "MNA"]
UNIVERSE.update({s: ETF for s in DIVS})
SLOT = 1 / 7

# Crash windows scored by the card (the protocol's stress windows plus calendar 2020-Q1 and 2022).
CRASH = [
    ("2008 crisis", date(2007, 10, 9), date(2009, 3, 9), True),
    ("covid crash", date(2020, 2, 19), date(2020, 3, 23), True),
    ("2022 rate shock", date(2022, 1, 3), date(2022, 10, 12), True),
    ("2020-Q1", date(2019, 12, 31), date(2020, 3, 31), False),
    ("2022", date(2021, 12, 31), date(2022, 12, 31), False),
    ("dot-com bust", date(2000, 3, 24), date(2002, 10, 9), False),
]


def fetch() -> None:
    import fetch as f

    now = datetime.now(UTC)
    for s in DIVS:
        raw, adj = f.yahoo_all(s, now)
        f.write(f.DATA / "bars" / f"{s}.csv", raw)
        f.write(f.DATA / "adj" / f"{s}.csv", adj)
        f.report(s, raw, 5)


def book(div: str) -> c.ResearchStrategy:
    def w(view: View) -> Weights:
        held = [s for s in SYMS if c.eligible(view, s)]
        out = {s: (1 - SLOT) / len(held) for s in held if c.tsmom_signal(view, s)}
        if c.eligible(view, div):
            out[div] = SLOT
        return out

    return c.weekly(w)


def ctx_with(div: str, tag: str) -> c.Ctx:
    """The six plus the diversifier; `tag` names the universe in the variant (`six`: no tag)."""
    hist = harness.load_history("train", True, [*SYMS, div])
    six = c.ctx("six")
    return c.Ctx(tag, "train", hist, Panel(hist), six.start, six.end)


def first_eligible(ctx: c.Ctx, div: str) -> date:
    return ctx.hist[div][c.bpy(div) - 1].date + timedelta(days=1)


def window_return(run: Run, a: date, b: date) -> float:
    r = run.rets_between(a, b)
    return float(np.prod(1 + r) - 1) if len(r) > 5 and run.days[0] <= a else math.nan


def worst_year(run: Run) -> tuple[int, float]:
    years = range(run.days[0].year, run.days[-1].year + 1)
    rows = [(y, window_return(run, max(date(y - 1, 12, 31), run.days[0]), date(y, 12, 31)))
            for y in years]  # fmt: skip
    rows = [(y, x) for y, x in rows if not math.isnan(x)]
    return min(rows, key=lambda t: t[1])


def under_water(run: Run) -> tuple[int, float, date]:
    """Longest stretch below a prior peak (calendar days, to recovery or the end), its start,
    and the share of days below a prior peak."""
    eq = run.equity
    peak = np.maximum.accumulate(eq)
    below = eq < peak * (1 - 1e-9)
    best, cur, start, best_start = 0, 0, 0, 0
    for i, b in enumerate(below):
        if b:
            if cur == 0:
                start = i
            cur += 1
            if cur > best:
                best, best_start = cur, start
        else:
            cur = 0
    return best, float(below.mean()), run.days[max(best_start - 1, 0)]


def boot(a: np.ndarray, b: np.ndarray, draws: int = 2000) -> tuple[float, float, float]:
    """Sharpe difference, one-sided p, bootstrap SE (same draws as stats.sharpe_diff_boot)."""
    rng = np.random.default_rng(0)
    diffs = np.empty(draws)
    for k in range(draws):
        i = stats._stationary_indices(len(a), 20, rng)
        diffs[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
    return stats.sharpe(a) - stats.sharpe(b), float((diffs <= 0).mean()), float(diffs.std())


def weekly_corr(ctx: c.Ctx, div: str, run: Run, start: date) -> tuple[float, float]:
    """Correlation of the diversifier's Friday-to-Friday returns with SPY's and with the run's."""
    eq = dict(zip(run.days, run.equity, strict=True))
    fridays = [d for d in run.days if d.weekday() == 4 and d >= start]

    def last_close(s: str, d: date) -> float:
        bars = ctx.hist[s]
        lo, hi = 0, len(bars)
        while lo < hi:
            mid = (lo + hi) // 2
            if bars[mid].date <= d:
                lo = mid + 1
            else:
                hi = mid
        return bars[lo - 1].close

    dv = np.array([last_close(div, d) for d in fridays])
    sp = np.array([last_close("SPY", d) for d in fridays])
    bk = np.array([eq[d] for d in fridays])
    r = [np.diff(x) / x[:-1] for x in (dv, sp, bk)]
    return float(np.corrcoef(r[0], r[1])[0, 1]), float(np.corrcoef(r[0], r[2])[0, 1])


def block(title: str, runs: list[Run], base: Run, ew: Run, ctx: c.Ctx, div: str) -> list[str]:
    test = runs[0]
    out = [f"## {title}", "", c.table([test, base, ew], versus=base), ""]
    d, p, se = boot(*c.align(test, base))
    de, pe, _ = boot(*c.align(test, ew))
    out += [
        f"vs `tsmom12`: dSharpe {d:+.3f}, bootstrap SE {se:.3f}, z {d / se:+.2f}, one-sided "
        f"p {p:.3f}. vs equal weight: {de:+.3f} (p {pe:.3f}).",
        "",
        "| Book | Max DD | Worst year | Longest under water (from) | Share of days under water |"
        + "".join(f" {n}{'' if s else ' (info)'} |" for n, _, _, s in CRASH),
        "|---|---:|---:|---:|---:|" + "---:|" * len(CRASH),
    ]
    for r in (test, base):
        y, wy = worst_year(r)
        lw, share, since = under_water(r)
        row = (
            f"| {r.variant} | {stats.max_drawdown(r.rets):.1%} | {wy:+.1%} ({y}) | "
            f"{lw} d ({since}) | {share:.0%} |"
        )
        row += "".join(
            f" {x:+.1%} |" if not math.isnan(x := window_return(r, a, b)) else " - |"
            for _, a, b, _ in CRASH
        )
        out.append(row)
    cs, cb = weekly_corr(ctx, div, base, test.days[0])
    out += ["", f"Weekly correlation of {div} with SPY {cs:+.2f}, with `tsmom12` {cb:+.2f}.", ""]
    # risk preference (card): (a) smaller max DD, (b) better in >= 2 of 3 named crash windows,
    # (c) longest time under water not longer.
    a_ok = stats.max_drawdown(test.rets) < stats.max_drawdown(base.rets)
    wins = sum(window_return(test, a, b) > window_return(base, a, b) for _, a, b, s in CRASH if s)
    c_ok = under_water(test)[0] <= under_water(base)[0]
    verdict = "preferred on risk" if a_ok and wins >= 2 and c_ok else "no risk case"
    out += [
        f"Risk preference (card): smaller max DD {a_ok}; better in {wins} of 3 crash windows; "
        f"under water not longer {c_ok} -> **{verdict}** (a preference, not an edge).",
        "",
    ]
    return out


def main() -> None:
    six = c.ctx("six")
    base = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline",
                log=False)  # fmt: skip
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    out = ["# diversifier-1: a held 1/7 merger-arb slot next to `tsmom12`", ""]
    out += [
        "Card: `cards/diversifier-1.md`. Train only, total-return prices, gym costs. Sharpe "
        "daily, 365 days, zero risk-free rate. Era columns are Sharpe ratios. Under water: "
        "calendar days below a prior peak.",
        "",
    ]
    mx = ctx_with("MERFX", "six")
    merfx = c.go(IDEA, "merfx7", book("MERFX"), mx)
    out += block("Primary: MERFX, 1994-2025", [merfx], base, ew, mx, "MERFX")
    mn = ctx_with("MNA", "mna")
    s = first_eligible(mn, "MNA")
    mna = c.go(IDEA, "mna7", book("MNA"), mn, "robustness", start=s)
    base_m = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline",
                  log=False, start=s)  # fmt: skip
    ew_m = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline",
                log=False, start=s)  # fmt: skip
    out += block(f"Robustness: MNA, from {s}", [mna], base_m, ew_m, mn, "MNA")
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else main()
