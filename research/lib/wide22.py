"""Lane wide-22: gate W36 `grid-load-premium` (research/cards/wide-22.md; rule pushed before
this script's first run).

Descriptive only: no strategy, no backtest. Train bars only, cut at 2025-10-31 (this night's
lane rule); usage and market months after 2025-10 are never read. The EIA file is an untrusted
download in the shared cache: run with `python -I`.

Run:  `uv run python -I research/lib/wide22.py`  (DRY=1: counts only)
R36:  `uv run python -I research/lib/wide22.py r36`  (cards/wide-22b.md; FRED files cached)
Post hoc: `uv run python -I research/lib/wide22.py posthoc`
Output: research/results/grid-load-premium.md, grid-load-premium-r36.md,
grid-load-premium-posthoc.md
"""

from __future__ import annotations

import math
import os
import sys
import zipfile
from collections.abc import Sequence
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as e13  # noqa: E402
import wide17_events as e17  # noqa: E402
import wide22_events as ev  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)  # lane rule: nothing after this date is read
EIA_REL = "wide-22/2026-11-25/eia/T07.06.csv"
FRENCH_REL = "french/2026-11-12/F-F_Research_Data_Factors_CSV.zip"
LAGS = 3
POST = 2011 * 12  # 2011-01: first usage month after the paper's sample


def ym(m: int) -> str:
    return f"{m // 12}-{m % 12 + 1:02d}"


def load() -> tuple[dict[int, float], dict[int, float], dict[int, float]]:
    root = dw.cache_root()
    text = (root / EIA_REL).read_text(encoding="utf-8", errors="replace")
    ind = ev.parse_mer(text, "ESICPUS", LAST)
    res = ev.parse_mer(text, "ESRCPUS", LAST)
    z = zipfile.ZipFile(root / FRENCH_REL)
    lines = z.read(z.namelist()[0]).decode("latin1").splitlines()
    mkt = {m: v[0] for m, v in ev.parse_french_monthly(lines, LAST).items()}
    return ind, res, mkt


def fit(
    months: Sequence[int],
    y: dict[int, float],
    x: dict[int, float],
    lags: int = LAGS,
    ctrl: Sequence[dict[int, float]] = (),
) -> tuple[float, float, int]:
    """(b, t, rows): OLS y = a + b x (+ controls), Newey-West t with `lags`. One code path for
    every cell, true and placebo."""
    nan = math.nan
    cols = [np.ones(len(months)), np.array([x.get(m, nan) for m in months])]
    cols += [np.array([c.get(m, nan) for m in months]) for c in ctrl]
    yy = np.array([y.get(m, nan) for m in months])
    beta, tt, n = e11.ols_dk(cols, yy, np.array(months), lags)
    return float(beta[1]), float(tt[1]), n


def null_block(t: float, placebo: list[float], labels: Sequence[str]) -> tuple[int, list[str]]:
    rank = ev.rank_lowest(t, placebo)  # predicted sign negative
    sd, share = e11.null_spread(placebo)
    q5, med, q95 = e13.quantiles(placebo)
    return rank, [
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {q5:+.2f}, 50% {med:+.2f}, 95% {q95:+.2f}; smallest"
        f" {min(placebo):+.2f}, largest {max(placebo):+.2f}.",
        "",
        "| placebo | t |",
        "|---|---:|",
        *[f"| {k} | {p:+.2f} |" for k, p in zip(labels, placebo, strict=True)],
        "",
    ]


def cell(name: str, r: tuple[float, float, int]) -> str:
    return f"| {name} | {r[0]:+.4f} | {r[1]:+.2f} | {r[2]} |"


def run() -> None:
    ind, res, mkt = load()
    g = ev.yoy(ind)
    gr = ev.yoy(res)
    y = {m - ev.LAG: v for m, v in mkt.items()}  # y(m) = Mkt-RF of month m + 3
    months = [m for m in sorted(g) if m in y]
    lo, hi = months[0], months[-1]
    allm = list(range(lo, hi + 1))

    if DRY:
        print("industrial months", len(ind), ym(min(ind)), "..", ym(max(ind)))
        print("residential months", len(res), "market months", len(mkt), ym(min(mkt)), ym(max(mkt)))
        print("gate rows", len(months), ym(lo), "..", ym(hi))
        ns = [len([m for m in allm if m in ev.shifted(g, k) and m in y]) for k in ev.SHIFTS]
        print("placebo rows min", min(ns), "max", max(ns))
        print("post-sample rows", len([m for m in months if m >= POST]))
        print("surrogate run", len(ev.contiguous(g)))
        return

    b, t, n = fit(allm, y, g)
    sd_g = float(np.std([g[m] for m in months]))
    placebo = [fit(allm, y, ev.shifted(g, k))[1] for k in ev.SHIFTS]
    rank, null = null_block(t, placebo, [f"k = {k}" for k in ev.SHIFTS])
    post = [m for m in allm if m >= POST]
    bp, tp, np_ = fit(post, y, g)
    passed = b < 0 and t <= -2 and rank <= 2 and bp < 0

    c1 = {m - 2: v for m, v in mkt.items()}  # Mkt-RF of month m + 2
    c12 = ev.window_sum(mkt, -9, 12)  # months m-9 .. m+2
    y12 = ev.window_sum(mkt, 3, 12)  # months m+3 .. m+14
    r12 = ev.window_sum(mkt, -11, 12)  # months m-11 .. m
    r24 = ev.window_sum(mkt, -23, 24)
    common = [m for m in allm if all(m - k in g for k in ev.SHIFTS) and m in y]
    tc = fit(common, y, g)
    pc = [fit(common, y, ev.shifted(g, k))[1] for k in ev.SHIFTS]
    rank_c = ev.rank_lowest(tc[1], pc)
    surr = ev.phase_surrogates(g)
    ps = [fit(allm, y, s)[1] for s in surr]
    rank_s, null_s = null_block(t, ps, [f"surrogate {i + 1}" for i in range(len(ps))])
    inside = [m for m in allm if m < POST]

    fb = [m for m in allm if m in g]
    beta, tf, nf = e11.ols_dk(
        [np.ones(len(fb)), np.array([r12.get(m, math.nan) for m in fb]),
         np.array([r24.get(m, math.nan) for m in fb])],
        np.array([g[m] for m in fb]), np.array(fb), 12,
    )  # fmt: skip

    hist = harness.load_history("train", syms=["SPY", "TLT", "GLD", "BTC"])
    live = []
    for s, bars in hist.items():
        px = e13.Closes({x.date: x.close for x in bars if x.date <= LAST})
        ys = {m: e17.month_return(px, m + 2, m + 3, LAST) * 100 for m in allm}
        ys = {m: v for m, v in ys.items() if not math.isnan(v)}
        live.append(cell(f"(h) {s} log return, month m+3", fit(allm, ys, g)))

    shown = [
        cell("(a) with controls: Mkt-RF of m+2, of m-9..m+2", fit(allm, y, g, LAGS, [c1, c12])),
        cell("(b) paper's horizon: Mkt-RF m+3..m+14, NW 18", fit(allm, y12, g, 18)),
        cell(f"(c) inside the paper's sample, {ym(lo)} .. 2010-12", fit(inside, y, g)),
        cell(f"(c) after it, 2011-01 .. {ym(hi)} (gate condition 4)", (bp, tp, np_)),
        cell(f"(d) common rows {ym(common[0])} .. {ym(common[-1])}", tc),
        cell("(e) negative control: residential sales growth", fit(allm, y, gr)),
        *live,
    ]
    lines = [
        "# W36 `grid-load-premium`: result",
        "",
        "Card: `research/cards/wide-22.md`. Script: `research/lib/wide22.py`. Data: EIA Monthly"
        " Energy Review Table 7.6 (ESICPUS, industrial retail sales of electricity; ESRCPUS"
        " residential), Ken French's monthly `Mkt-RF`. Only statistics are committed.",
        "",
        f"**Gate (usage months {ym(lo)} .. {ym(hi)}, {n} rows; outcome Mkt-RF of month m+3):**"
        f" b = {b:+.4f}% a month per point of year-on-year growth ({b * sd_g:+.3f}% per sd of"
        f" g, sd {sd_g:.2f} points), Newey-West t {t:+.2f}; rank {rank} of 41 (lowest = 1);"
        f" post-sample b {bp:+.4f} (t {tp:+.2f}, {np_} rows)."
        f" **{'PASS (kill-only)' if passed else 'FAIL'}.**",
        "",
        "Conditions: b < 0 "
        + ("yes" if b < 0 else "no")
        + "; t <= -2 "
        + ("yes" if t <= -2 else "no")
        + f"; rank <= 2 {'yes' if rank <= 2 else 'no'}"
        + f"; post-sample b < 0 {'yes' if bp < 0 else 'no'}.",
        "",
        "## Placebo null: earlier doses, k = 25..103 months (odd)",
        "",
        *null,
        "## Shown (not gating)",
        "",
        "| Cell | b (% a month per point) | t | rows |",
        "|---|---:|---:|---:|",
        *shown,
        "",
        f"(d) on the common rows the true t ranks {rank_c} of 41 against the same 40 shifts.",
        "",
        f"(f) feedback, g(m) on the market's 12- and 24-month excess returns ending at m"
        f" ({nf} rows, NW 12): 12-month {beta[1]:+.4f} (t {tf[1]:+.2f}), 24-month"
        f" {beta[2]:+.4f} (t {tf[2]:+.2f}).",
        "",
        f"(g) phase-randomised surrogates of g (seed {ev.SEED}): the true t ranks {rank_s} of 41.",
        "",
        *null_s,
    ]
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "grid-load-premium.md").write_text("\n".join(lines))
    print("\n".join(lines))


def r36() -> None:
    root = dw.cache_root()
    p1 = ev.parse_fred((root / "wide-22/2026-11-25/fred/M01128USM247NNBR.csv").read_text(), LAST)
    p2 = ev.parse_fred((root / "wide-22/2026-11-25/fred/M0128AUSM247NNBR.csv").read_text(), LAST)
    _, _, mkt = load()
    g = ev.splice_r36(p1, p2)
    y = {m - ev.LAG: v for m, v in mkt.items()}
    lo, hi = 1926 * 12 + 3, 1955 * 12 + 11
    allm = list(range(lo, hi + 1))
    if DRY:
        print("P1", len(p1), ym(min(p1)), ym(max(p1)), "P2", len(p2), ym(min(p2)), ym(max(p2)))
        print("rows", len([m for m in allm if m in g and m in y]))
        ns = [len([m for m in allm if m - k in g and m in y]) for k in ev.SHIFTS]
        print("placebo rows min", min(ns), "max", max(ns))
        return
    b, t, n = fit(allm, y, g)
    placebo = [fit(allm, y, ev.shifted(g, k))[1] for k in ev.SHIFTS]
    rank, null = null_block(t, placebo, [f"k = {k}" for k in ev.SHIFTS])
    passed = b < 0 and t <= -2 and rank <= 2
    gs = {m: v for m, v in g.items() if lo - 200 <= m <= hi}
    ps = [fit(allm, y, s)[1] for s in ev.phase_surrogates(gs)]
    rank_s, null_s = null_block(t, ps, [f"surrogate {i + 1}" for i in range(len(ps))])
    shown = [
        cell("without the Depression, 1934-01 .. 1955-12", fit(allm[(1934 * 12) - lo :], y, g)),
        cell("P1 alone, 1926-04 .. 1938-12", fit([m for m in allm if m <= 1938 * 12 + 11], y, g)),
        cell("P2 alone, 1939-01 .. 1955-12", fit([m for m in allm if m > 1938 * 12 + 11], y, g)),
    ]
    sd_g = float(np.std([g[m] for m in allm if m in g]))
    lines = [
        "# R36: replication of W36 `grid-load-premium` on 1926-1955",
        "",
        "Card: `research/cards/wide-22b.md` (pushed after the W36 number, before this one)."
        " Script: `research/lib/wide22.py r36`. Data: NBER Macrohistory electric power"
        " production (FRED `M01128USM247NNBR` to 1938, `M0128AUSM247NNBR` from 1939, spliced on"
        " year-on-year growth); French monthly `Mkt-RF`.",
        "",
        f"**R36 (usage months {ym(lo)} .. {ym(hi)}, {n} rows; outcome Mkt-RF of month m+3):**"
        f" b = {b:+.4f}% a month per point ({b * sd_g:+.3f}% per sd of g, sd {sd_g:.2f}),"
        f" Newey-West t {t:+.2f}; rank {rank} of 41 (lowest = 1)."
        f" **{'PASS (kill-only)' if passed else 'FAIL: W36 is killed'}.**",
        "",
        "## Placebo null: earlier doses, k = 25..103 months (odd)",
        "",
        *null,
        "## Shown (not deciding)",
        "",
        "| Cell | b (% a month per point) | t | rows |",
        "|---|---:|---:|---:|",
        *shown,
        "",
        f"Phase-randomised surrogates of g (seed {ev.SEED}): the true t ranks {rank_s} of 41.",
        "",
        *null_s,
    ]
    (RESULTS / "grid-load-premium-r36.md").write_text("\n".join(lines))
    print("\n".join(lines))


def posthoc() -> None:
    """Diagnostics added after both numbers (labelled post hoc in research/wide-22.md)."""
    ind, _, mkt = load()
    g = ev.yoy(ind)
    y = {m - ev.LAG: v for m, v in mkt.items()}
    allm = [m for m in sorted(g) if m in y]
    covid = set(range(2020 * 12, 2021 * 12 + 12))
    cells = [
        ("2011-01 .. 2025-07 without usage months 2020-2021", [m for m in allm
         if m >= POST and m not in covid]),
        ("1974-01 .. 2025-07 without usage months 2020-2021", [m for m in allm
         if m not in covid]),
        ("Mkt-RF on SPY's rows (usage months 1993-01 .. 2025-07)", [m for m in allm
         if m >= 1993 * 12]),
        ("1993-01 .. 2010-12", [m for m in allm if 1993 * 12 <= m < POST]),
    ]  # fmt: skip
    lines = [
        "# W36 `grid-load-premium`: post-hoc diagnostics",
        "",
        "Added after the W36 and R36 numbers; not part of any rule. Script:"
        " `research/lib/wide22.py posthoc` (first run 2026-11-25 21:15 UTC). Outcome and dose as"
        " the gate (`grid-load-premium.md`): French Mkt-RF of month m+3 on yoy growth of EIA"
        " industrial electricity sales, NW 3.",
        "",
        "| Cell (post hoc) | b | t | rows |",
        "|---|---:|---:|---:|",
        *[cell(name, fit(ms, y, g)) for name, ms in cells],
        "",
    ]
    (RESULTS / "grid-load-premium-posthoc.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    if sys.argv[1:] == ["posthoc"]:
        posthoc()
    elif sys.argv[1:] == ["r36"]:
        r36()
    else:
        run()
