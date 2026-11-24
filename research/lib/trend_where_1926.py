"""trend-where follow-up: `where-vol`, unchanged, on Ken French's ten US industries 1926-1961
(card: research/trend-where.md, "Follow-up card").

    uv run python research/lib/trend_where_1926.py

Data and conventions are lane trend-1926's primary configuration (lib/trend_1926.py). One
`robustness` row in research/tries.md (idea `trend-where`), logged the first time only.
"""

from __future__ import annotations

from datetime import date

import common as c
import harness
import numpy as np
import stats
import trend_1926 as t26
import trend_tune as tt
import trend_where as tw

from grimstrade import gym
from grimstrade.data import ETF

IDEA = "trend-where"
COST = 0.0002
WINDOWS = [
    ("whole period", date(1927, 7, 2), date(1961, 12, 31)),
    ("1929-09-03 to 1932-07-08", date(1929, 9, 3), date(1932, 7, 8)),
    ("1937-03-10 to 1938-03-31", date(1937, 3, 10), date(1938, 3, 31)),
]


def run(variant: str, strategy: c.ResearchStrategy, u: c.Ctx, log: bool) -> c.Run:
    tag = f"{variant}@{u.name}"
    done = (harness.DATA / "runs" / IDEA / f"{tag}.train.csv").exists()
    costs = {**gym.COSTS, ETF: gym.Costs(fee=0.0, slip=COST)}
    return harness.run(
        IDEA if log else "baselines", tag, strategy, kind="robustness" if log else "baseline",
        period="train", panel=u.panel, history=u.hist, start=u.start, end=u.end, costs=costs,
        log=log and not done and not c.DRY,
    )  # fmt: skip


def main() -> None:
    raw = t26.load()
    u = t26.universe(raw, t26.INDUSTRIES, t26.BOOK)
    where = tw.Where("vol")
    got = run("where-vol", where.strategy(), u, log=True)
    twin = run("tsmom12", t26.rule(), u, log=False)
    ew = run("equal-weight", t26.hold(), u, log=False)
    every = [got, twin, ew]
    syms = [t26.sym(n) for n in t26.INDUSTRIES]

    out = [
        "## Follow-up: `where-vol` on ten US industries, 1926-1961",
        "",
        f"French cache snapshot `french/{raw.snapshot}`; decisions {u.start} to {u.end}; ten "
        "industries as one equal-slot book; 2 bps a side; cash earns 0. Twin: always-on "
        "`tsmom12`. Benchmark: equal weight.",
        "",
        "| Variant | Sharpe | Against `tsmom12` (p; 90% range) | Growth/yr | Worst loss | "
        "Trades a year | Avg exposure |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in every:
        d = c.describe(r)
        if r is twin:
            versus = "-"
        else:
            a, b = c.align(r, twin)
            diff, p, lo, hi = stats.sharpe_diff_boot(a, b)
            versus = f"{diff:+.2f} (p={p:.2f}; {lo:+.2f}..{hi:+.2f})"
        out.append(f"| {r.variant} | {d['sharpe']:.2f} | {versus} | {d['cagr']:+.1%} | "
                   f"{d['mdd']:.1%} | {d['turnover']:.1f} | {d['exposure']:.0%} |")  # fmt: skip
    out += ["", "Worst loss inside each window:", "",
            "| Window |" + "".join(f" {r.variant} |" for r in every),
            "|---|" + "---:|" * len(every)]  # fmt: skip
    for label, a, b in WINDOWS:
        cells = "".join(
            f" {stats.max_drawdown(r.rets_between(max(a, r.days[0]), min(b, r.days[-1]))):.1%} |"
            for r in every
        )
        out.append(f"| {label} |{cells}")

    out += ["", "Answers (yes = keep the filter), shown when one changed:", "",
            "| Refit |" + "".join(f" {n} |" for n in t26.INDUSTRIES),
            "|---|" + "---|" * len(syms)]  # fmt: skip
    prev = None
    no = total = 0
    for year in range(u.start.year, u.end.year + 1):
        ans = where.answers(u.panel, tt.first_friday(year))
        row = tuple("yes" if ans[s] else "no" for s in syms)
        if year > u.start.year:
            no += sum(not ans[s] for s in syms)
            total += len(syms)
        if row != prev:
            out.append(f"| {year} |" + "".join(f" {x} |" for x in row))
        prev = row
    out += ["", f"Industry-years answered no: {no} of {total} (refits 1928 to {u.end.year}).", ""]
    out += ["What the last refit saw:", "",
            "| Industry | Out bars | In bars | Volatility out | Volatility in | Keep filter |",
            "|---|---:|---:|---:|---:|---|"]  # fmt: skip
    last = tt.refit_of(u.end)
    for n, s in zip(t26.INDUSTRIES, syms, strict=True):
        e = where.evidence(u.panel, s, last)
        k = float(np.sqrt(c.bpy(s)))
        out.append(f"| {n} | {e.n_out} | {e.n_in} | {e.out * k:.1%} | {e.inn * k:.1%} | "
                   f"{'yes' if e.keep else 'no'} |")  # fmt: skip
    path = harness.RESEARCH / "results" / ("trend-where-1926.md" if not c.DRY else "tw26.dry.md")
    path.write_text("\n".join(out).rstrip() + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
