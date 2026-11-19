"""rp-1 step 2: the one carded run of `where-rp` (card: research/rp-1.md, "Step 2 card").

    uv run python -I research/lib/rp1_run.py

Logs one `variant` row (six assets) and three `robustness` rows (8 other ETFs, 6 other coins,
4 indexes) under idea `rp-1` in research/tries.md, the first time only; a rerun re-scores
without logging. Twins and context books are re-scores of logged configurations. Train period
only; the held-out year is not touched. Writes research/results/rp-1.md.
"""

from __future__ import annotations

import math
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common as c  # noqa: E402
import harness  # noqa: E402
import numpy as np  # noqa: E402
import rp1_diag as dg  # noqa: E402
import stats  # noqa: E402
import trend_where as tw  # noqa: E402
from rp1_rule import where_rp  # noqa: E402

IDEA = "rp-1"
FAMILY = 74
P_BAR = 0.10 / FAMILY
P_PROJECT = 0.05 / 1012  # register-1 BAR.md, N 1,012 for a new pick
SLACK = 0.05
Y2003 = date(2003, 1, 1)
TRIES = harness.RESEARCH / "tries.md"


def logged(variant: str) -> bool:
    return f"| {IDEA} | {variant} |" in TRIES.read_text()


def go_once(name: str, f: c.ResearchStrategy, u: c.Ctx, kind: str) -> c.Run:
    tag = name if u.name == "six" else f"{name}@{u.name}"
    return c.go(IDEA, name, f, u, kind, log=not logged(tag))


def since(run: c.Run, a: date) -> np.ndarray:
    return run.rets_between(max(a, run.days[0]), run.days[-1])


def window(run: c.Run, a: date, b: date) -> float:
    return float(np.prod(1 + run.rets_between(a - timedelta(days=1), b)) - 1)


def main() -> None:
    six = c.ctx("six")
    twin_f = c.weekly(c.slots(c.tsmom_signal))
    rp = go_once("where-rp", where_rp(), six, "variant")
    twin = c.go("baselines", "tsmom12", twin_f, six, "baseline", log=False)
    wv = c.go("trend-where", "where-vol", tw.Where("vol").strategy(), six, "baseline", log=False)
    iv = c.go("baselines", "inverse-vol", c.weekly(c.inverse_vol), six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    every = [rp, twin, wv, iv, ew]

    out = [
        "# rp-1: `where-rp` (`where-vol` with inverse-vol slot sizes)",
        "",
        "Card: `rp-1.md`, step 2 (pushed before any number). Train period only (decisions to "
        "2025-11-09), total-return prices, the gym's fills and protocol costs, cash 0. Twin: "
        "`tsmom12`. Context (re-scores of logged configurations): `where-vol`, `inverse-vol`, "
        "equal weight. Held-out year not touched.",
        "",
        "## Six assets, 1994-2025",
        "",
        c.table(every, versus=twin),
        "",
        "Total return inside each stress window:",
        "",
        c.stress_table(every),
        "",
    ]

    # 2022, the reason for the card
    out += ["## 2022 (the reason for the card)", ""]
    out += ["| Book | Calendar 2022 | Rate shock 2022-01-03..10-12 |", "|---|---:|---:|"]
    for r in (rp, wv, twin, iv, ew):
        a = window(r, date(2022, 1, 1), date(2022, 12, 31))
        b = window(r, *dg.SHOCK)
        out.append(f"| {r.variant} | {a:+.1%} | {b:+.1%} |")
    days = dg.cal_days(date(2022, 1, 1), date(2022, 12, 31))
    R = np.column_stack([dg.asset_rets(six.panel, s, days) for s in dg.SIX])
    out += ["", "Slot contributions, calendar 2022 (points, arithmetic, as in step 1):", ""]
    out += ["| Book | " + " | ".join(dg.SIX) + " | Sum |", "|---|" + "---:|" * (len(dg.SIX) + 1)]
    for r in (rp, wv, twin):
        contrib = (dg.weights_by_day(r, days) * R).sum(axis=0)
        out.append(
            f"| {r.variant} | "
            + " | ".join(f"{100 * x:+.1f}" for x in contrib)
            + f" | {100 * contrib.sum():+.1f} |"
        )
    all_days = dg.cal_days(rp.days[1], rp.days[-1])
    wr = dg.weights_by_day(rp, all_days)
    coins = wr[:, 4] + wr[:, 5]
    eligible_btc = [i for i, d in enumerate(all_days) if d >= date(2013, 1, 1)]
    out += [
        "",
        f"`where-rp` mean invested share {wr.sum(axis=1).mean():.0%}; mean coin weight "
        f"{coins[eligible_btc].mean():.1%} from 2013 (`where-vol`: up to 33%).",
        "",
    ]

    # out of universe
    out += ["## Out of universe (rule unchanged, each set one book)", ""]
    oou: dict[str, float] = {}
    for name in ("etf", "coin", "idx"):
        u = c.ctx(name)
        r = go_once("where-rp", where_rp(), u, "robustness")
        t = c.go("baselines", "tsmom12", twin_f, u, "baseline", log=False)
        w = c.go("trend-where", "where-vol", tw.Where("vol").strategy(), u, "baseline", log=False)
        x, y = c.align(r, t)
        oou[name] = stats.sharpe(x) - stats.sharpe(y)
        out += [f"### {name}, from {u.start}", "", c.table([r, t, w], t, eras=False), ""]

    # the bar
    a, b = c.align(rp, twin)
    d, p, lo, hi = stats.sharpe_diff_boot(a, b)
    es, et = c.era_sharpes(rp), c.era_sharpes(twin)
    both = [n for n in es if not (math.isnan(es[n]) or math.isnan(et[n]))]
    ahead = sum(es[n] > et[n] for n in both)
    dr, dt, de = c.describe(rp), c.describe(twin), c.describe(ew)
    s03 = stats.sharpe(since(rp, Y2003))
    t03, e03 = stats.sharpe(since(twin, Y2003)), stats.sharpe(since(ew, Y2003))
    bars = [
        (
            f"1. Sharpe beats `tsmom12`, one-sided p < {P_BAR:.5f} (family {FAMILY})",
            d > 0 and p < P_BAR,
            f"{dr['sharpe']:.2f} vs {dt['sharpe']:.2f}, difference {d:+.3f}, p = {p:.4f}, "
            f"90% range {lo:+.2f}..{hi:+.2f}; project-wide bar p <= {P_PROJECT:.1e}: "
            f"{'met' if d > 0 and p <= P_PROJECT else 'not met'}",
        ),
        (
            "2. Ahead of `tsmom12` in at least 4 of 5 eras",
            ahead >= 4,
            f"{ahead} of {len(both)}: "
            + ", ".join(f"{n} {es[n]:.2f} vs {et[n]:.2f}" for n in both),
        ),
        (
            "3. Worst loss not more than 5 points deeper",
            dr["mdd"] <= dt["mdd"] + SLACK,
            f"{dr['mdd']:.1%} vs {dt['mdd']:.1%}",
        ),
        (
            "4. Out of universe: Sharpe up in 2 of 3 sets",
            sum(v > 0 for v in oou.values()) >= 2,
            ", ".join(f"{k} {v:+.2f}" for k, v in oou.items()),
        ),
        (
            "5. Beats equal weight on Sharpe",
            dr["sharpe"] > de["sharpe"],
            f"{dr['sharpe']:.2f} vs {de['sharpe']:.2f}",
        ),
        (
            "6. Since 2003 not behind `tsmom12` nor equal weight",
            s03 >= t03 and s03 >= e03,
            f"{s03:.2f} vs {t03:.2f} and {e03:.2f}",
        ),
    ]
    ok = all(flag for _, flag, _ in bars)
    out += ["## Pass bar", ""]
    out += [f"- {'PASS' if flag else 'FAIL'}: {t} ({detail})" for t, flag, detail in bars]
    out += ["", f"**`where-rp` {'PASSES' if ok else 'FAILS'} train.**", ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
