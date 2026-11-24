"""insure-4: put protection only while trend is in the market. Card: cards/insure-4.md.

    uv run python -I research/lib/insure4.py   # needs insure-3's raw files in the data cache

Rule: when `tsmom12` (the record's rule, on the S&P 500 total return) says in, hold CBOE's PPUT
(the index plus a 5% out-of-the-money monthly put) instead of the plain total return; when it says
out, bills. Switches at the decision Friday's close, at PPUT's index level; 2 bps a side.
Compared with holding, `tsmom12` and PPUT alone on insure-3's window and falls; paired Sharpe test
against `tsmom12` with a stationary block bootstrap. Raw levels stay in the cache (CBOE terms);
only statistics go to research/results/insure-4.md. Nothing after 2025-10-31 is parsed.
tries.md rows are written once.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import insure3 as i3  # noqa: E402
from stats import _stationary_indices  # noqa: E402

IDEA = "insure-4"
COST = i3.COST  # 2 bps a side, as tsmom12
COST_HI = 0.0010  # robustness: 10 bps a side
DRAWS, BLOCK, BLOCK_SIDE, SEED = 2000, 21, 63, 0
BAR_Z = 4.70  # research/register/BAR.md, rows through 2026-11-24 20:01
OUT = harness.RESEARCH / "results" / "insure-4.md"
TRIES = harness.RESEARCH / "tries.md"


def protected(pos: np.ndarray, r_in: np.ndarray, rf: np.ndarray, cost: float) -> np.ndarray:
    """Per-session return of the rule: r_in while in (pos 1), rf while out, `cost` a side on
    each switch. pos[i] is the position that earns session i's return (decided at an earlier
    close); index 0 is the base day (return 0)."""
    out = np.zeros(len(pos))
    flips = np.abs(np.diff(pos))
    out[1:] = pos[1:] * r_in[1:] + (1 - pos[1:]) * rf[1:] - cost * flips
    return out


def rule_from_level(days: Sequence[date], level: np.ndarray, r_in: np.ndarray, rf: np.ndarray,
                    cost: float = COST) -> tuple[np.ndarray, np.ndarray]:  # fmt: skip
    """The whole rule from the S&P 500 total-return level: positions from `tsmom12` on that
    level (insure-3's `trend`, the record's rule), returns from `protected`."""
    _, pos = i3.trend(days, level)
    return protected(pos, r_in, rf, cost), pos


def third_friday(d: date) -> bool:
    return d.weekday() == 4 and 15 <= d.day <= 21


def sharpe252(x: np.ndarray) -> float:
    sd = x.std()
    return float(x.mean() / sd * math.sqrt(252)) if sd > 0 else 0.0


def paired_test(
    a: np.ndarray,
    b: np.ndarray,
    rf: np.ndarray,
    block: float = BLOCK,
    draws: int = DRAWS,
    seed: int = SEED,
) -> tuple[float, float, float, float]:
    """Sharpe above bills of a minus b on the same sessions (index 0 dropped), with the SE of a
    paired stationary bootstrap of the daily excess returns. Returns (d, SE, z, p one-sided)."""
    xa, xb = (a - rf)[1:], (b - rf)[1:]
    d = sharpe252(xa) - sharpe252(xb)
    rng = np.random.default_rng(seed)
    diffs = np.empty(draws)
    for k in range(draws):
        i = _stationary_indices(len(xa), block, rng)
        diffs[k] = sharpe252(xa[i]) - sharpe252(xb[i])
    se = float(diffs.std(ddof=1))
    return d, se, d / se if se > 0 else math.nan, float((diffs <= 0).mean())


def verdict(z: float) -> str:
    if z >= BAR_Z:
        return "passes the bar"
    if z >= 1.645:
        return "better but not a pick"
    if z > -1.645:
        return "no Sharpe difference shown"
    return "worse than tsmom12"


def tries_rows(days: list[date], s: dict[str, np.ndarray], turn: float) -> list[str]:
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"
    spec = [
        ("tsmom12-pput-bills@insure4", "prot", "variant"),
        ("tsmom12-pput-bills-cost10@insure4", "prot@cost10", "robustness"),
        ("tsmom12-pput-cash0@insure4", "prot@cash0", "robustness"),
    ]
    out = []
    for var, key, kind in spec:
        x = s[key].copy()
        x[0] = 0.0
        out.append(
            f"| {now} | {IDEA} | {var} | {kind} | train | {days[0]} | {days[-1]} | "
            f"{i3.calendar_sharpe(x, days):.2f} | {np.prod(1 + x) - 1:+.1%} | {i3.mdd(x):.1%} | "
            f"{turn:.2f} |"
        )
    return out


def main() -> None:
    days, s3, rf, chk = i3.load()
    pos = chk["pos"]
    r_pp = s3["PPUT"]
    # check: the rule with the plain total return in place of PPUT is insure-3's tsmom12
    same = protected(pos, s3["hold"], rf, COST)
    assert np.allclose(same[1:], s3["trend"][1:], atol=1e-12), "rule != tsmom12 with r_in = hold"
    s = {
        "hold": s3["hold"], "trend": s3["trend"], "PPUT": r_pp,
        "prot": protected(pos, r_pp, rf, COST),
        "prot@cost10": protected(pos, r_pp, rf, COST_HI),
        "prot@cash0": protected(pos, r_pp, np.zeros(len(rf)), COST),
    }  # fmt: skip
    names = list(s)
    rows, ff = i3.stats_block(days, s, rf, names)
    main4 = ["hold", "trend", "PPUT", "prot"]
    sw = [i for i in range(1, len(pos)) if pos[i] != pos[i - 1]]
    sw_roll = sum(third_friday(days[i - 1]) for i in sw)
    yrs = (days[-1] - days[0]).days / 365.25
    share_in = float(pos[1:].mean())
    turn = len(sw) / yrs + 12 * share_in  # switches plus PPUT's monthly roll while in
    tests = []
    for other in ("trend", "PPUT", "hold"):
        for blk in (BLOCK, BLOCK_SIDE):
            tests.append((other, blk, *paired_test(s["prot"], s[other], rf, blk)))
    rob = [(k, *paired_test(s[k], s["trend"], rf)) for k in ("prot@cost10", "prot@cash0")]
    z_main = tests[0][4]
    named = [f for f in ff if any(lo <= f.trough <= hi for lo, hi in i3.NAMED_FAST.values())]
    md = [
        "# insure-4 results (generated by `research/lib/insure4.py`; do not edit)",
        "",
        f"Window {days[0]}..{days[-1]} ({len(days) - 1} sessions), insure-3's data and falls. "
        "`prot` = PPUT while `tsmom12` is in, bills while out (2 bps a side); `@cost10` 10 bps "
        "a side; `@cash0` idle cash at 0. Insurance cost = gap to hold (points a year) / mean "
        "loss avoided per fall (log points); premium P as insure-1.",
        "",
        "## Main table",
        "",
        i3.HEAD,
        *rows,
        "",
        "## Paired Sharpe test (above bills, daily, x sqrt(252)); stationary bootstrap, "
        f"{DRAWS} draws, seed {SEED}",
        "",
        "| prot minus | Mean block (sessions) | d | SE | z | p (one-sided, prot not better) |",
        "|---|---:|---:|---:|---:|---:|",
        *[
            f"| {o} | {b} | {d:+.3f} | {se:.3f} | {z:+.2f} | {p:.3f} |"
            for o, b, d, se, z, p in tests
        ],  # fmt: skip
        *[
            f"| ({k} minus trend) | {BLOCK} | {d:+.3f} | {se:.3f} | {z:+.2f} | {p:.3f} |"
            for k, d, se, z, p in rob
        ],  # fmt: skip
        "",
        f"Verdict (card rule, z vs `tsmom12`, block {BLOCK}): **{verdict(z_main)}** "
        f"(z {z_main:+.2f}; bar z >= {BAR_Z}).",
        "",
        "## Every 15% fall",
        "",
        *i3.fall_table(ff, main4),
        "",
        "## By kind of fall: mean share avoided / mean net of the next 365 days (log pts)",
        "",
        "| Subset | Falls | " + " | ".join(main4) + " |",
        "|---|---:|" + "---:|" * len(main4),
        i3.subset(named, main4, "named fast: 1987, 2020"),
        i3.subset([f for f in ff if f.days <= i3.FAST], main4, f"<= {i3.FAST} days"),
        i3.subset([f for f in ff if f.days > i3.FAST], main4, f"> {i3.FAST} days"),
        i3.subset(ff, main4, "all"),
        "",
        "Named fast falls, loss peak -> trough:",
        "",
        *[
            f"- {f.peak}..{f.trough} ({f.days} days): "
            + ", ".join(f"{n} {f.loss[n]:+.1%}" for n in main4)
            for f in named
        ],  # fmt: skip
        "",
        "## Diagnostics",
        "",
        f"- In the market {share_in:.1%} of sessions; {len(sw)} switches "
        f"({len(sw) / yrs:.2f} a year), {sw_roll} of them on a third Friday (PPUT's roll day).",
        "- Position at the peak of each fall: "
        + ", ".join(f"{f.peak.year} {pos[days.index(f.peak)]:.0f}" for f in ff)
        + ".",
        "- Check passed: the rule with the S&P 500 total return in place of PPUT equals "
        "insure-3's `tsmom12` (cash at bills) on every session.",
        "",
    ]
    OUT.write_text("\n".join(md))
    print("\n".join(md))
    text = TRIES.read_text()
    new = [r for r in tries_rows(days, s, turn) if f"| {r.split(' | ')[2]} |" not in text]
    if new:
        with TRIES.open("a") as f:
            f.write("\n".join(new) + "\n")
    print(f"{len(new)} tries rows appended")


if __name__ == "__main__":
    main()
