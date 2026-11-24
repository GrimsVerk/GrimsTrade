"""Lane wide-15: event-study gates W27 `congress-workload` and W28 `refund-runoff`
(research/wide-15.md steps 3 and 4; rules pushed before this script's first run).

Descriptive only: no strategy, no backtest. Train bars only (load_history("train") cuts at
2025-11-10); roll calls and refund days dated after 2025-11-10 are never read. Dose files are
untrusted downloads in the shared cache: run with `python -I`.

Fetch the doses once:  `uv run python -I research/lib/wide15.py fetch`
Run:                   `uv run python -I research/lib/wide15.py`  (DRY=1: counts only)
Output: research/results/congress-workload.md and research/results/refund-runoff.md
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections.abc import Callable, Sequence
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as e13  # noqa: E402
import wide15_events as ev  # noqa: E402

from grimstrade import cache  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = harness.TRAIN_LAST_BAR
HS = (28, 91, 182, 364)  # control horizons, days
SNAP = "2026-11-24"
VOTEVIEW = "https://voteview.com/static/data/out/rollcalls/HSall_rollcalls.csv"
DTS = (
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/"
    "income_tax_refunds_issued?filter=record_date:lte:2025-11-10&sort=record_date"
    "&page[size]=10000&page[number]={n}"
)
UA = "Mozilla/5.0 (daily-bar research script)"

DoseFn = Callable[[date], float]


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        data: bytes = r.read()
    return data


def fetch() -> None:
    """Download both dose files into `<cache_root>/wide-15/` (write-once, manifest)."""
    root = dw.cache_root()
    rel = f"wide-15/voteview/{SNAP}/HSall_rollcalls.csv"
    if not (root / rel).exists():
        cache.write_once(root, rel, _get(VOTEVIEW), VOTEVIEW)
    n, pages = 1, 1
    while n <= pages:
        rel = f"wide-15/dts-refunds/{SNAP}/page-{n:02d}.json"
        url = DTS.format(n=n)
        path = root / rel
        if not path.exists():
            cache.write_once(root, rel, _get(url), url)
        pages = int(json.loads(path.read_text())["meta"]["total-pages"])
        n += 1
    print("fetched into", root / "wide-15")


def load_rollcalls() -> list[tuple[date, str, int, int]]:
    p = dw.cache_root() / f"wide-15/voteview/{SNAP}/HSall_rollcalls.csv"
    return ev.parse_rollcalls(p.read_text(encoding="utf-8", errors="replace"), LAST)


def load_refunds() -> dict[date, float]:
    folder = dw.cache_root() / f"wide-15/dts-refunds/{SNAP}"
    pages = [p.read_text() for p in sorted(folder.glob("page-*.json"))]
    return ev.parse_refund_pages(pages, LAST)


def week_index(ref: date) -> Callable[[date], int]:
    return lambda d: round((d - ref).days / 7)


class Design:
    """One gate design. `fit` is the one code path for the true dose, the placebos and every
    shown cell: y = asset intercepts + doses + optional past-return controls, DK t."""

    def __init__(self, px: dict[str, e13.Closes], ref: date, entry: int, exit_: int):
        self.px, self.week, self.entry, self.exit = px, week_index(ref), entry, exit_

    def fit(
        self,
        assets: Sequence[str],
        dates: Sequence[date],
        doses: Sequence[DoseFn],
        controls: bool,
        exit_: int | None = None,
        lags: int = 4,
        coef: int = 0,
    ) -> tuple[float, float, int]:
        """(b, t, rows) of dose number `coef`."""
        ex = self.exit if exit_ is None else exit_
        rs = [(a, t) for a in assets for t in dates]
        y = np.array([e13.window_return(self.px[a], t, self.entry, ex, 7, LAST) for a, t in rs])
        cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
        for dose in doses:
            cols.append(np.array([dose(t) for _, t in rs]))
        if controls:
            for h in HS:
                cols.append(np.array([e13.past_return(self.px[a], t, h) for a, t in rs]))
        wk = np.array([self.week(t) for _, t in rs])
        beta, tt, n = e11.ols_dk(cols, y, wk, lags)
        j = len(assets) + coef
        return float(beta[j]), float(tt[j]), n

    def feedback(
        self, assets: Sequence[str], dates: Sequence[date], dose: DoseFn, h: int
    ) -> tuple[float, float, int]:
        """Dose on the asset's own past h-day return alone (asset intercepts, DK 4 lags)."""
        rs = [(a, t) for a in assets for t in dates]
        y = np.array([dose(t) for _, t in rs])
        cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
        cols.append(np.array([e13.past_return(self.px[a], t, h) for a, t in rs]))
        beta, tt, n = e11.ols_dk(cols, y, np.array([self.week(t) for _, t in rs]), 4)
        j = len(assets)
        return float(beta[j]), float(tt[j]), n


def gate_block(
    title: str, b: float, t: float, n: int, placebo: list[float], shifts: Sequence[int], unit: str
) -> list[str]:
    rank = e11.rank_highest(t, placebo)
    sd, share = e11.null_spread(placebo)
    q5, med, q95 = e13.quantiles(placebo)
    met = [b > 0 and t >= 2, rank <= 2]
    return [
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| {title}, b (t), {n} rows | {b * 100:+.3f}% {unit} ({t:+.2f}) | > 0, t >= 2 |"
        f" {met[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {met[1]} |",
        "",
        f"**Gate: {'PASS (kill-only design: not dead yet)' if all(met) else 'fail'}.**"
        f" Empirical one-sided p = {rank}/41 = {rank / 41:.3f}. (t - placebo median) /"
        f" placebo sd = {(t - med) / sd:+.2f} (descriptive only).",
        "",
        "## Placebo null (dose calendar moved k weeks: placebo dose = dose at F - 7k days)",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {q5:+.2f}, 50% {med:+.2f}, 95% {q95:+.2f}; smallest"
        f" {min(placebo):+.2f}, largest {max(placebo):+.2f}.",
        "",
        "| k (weeks) | t |",
        "|---:|---:|",
        *[f"| {k:+d} | {v:+.2f} |" for k, v in zip(shifts, placebo, strict=True)],
        "",
        "## Shown (not gating)",
        "",
        "| Cut | b, % per unit (t) | Rows |",
        "|---|---:|---:|",
    ]


def cell(name: str, r: tuple[float, float, int]) -> str:
    return f"| {name} | {r[0] * 100:+.3f} ({r[1]:+.2f}) | {r[2]} |"


# ---------------------------------------------------------------- W27


def congress_workload(px: dict[str, e13.Closes]) -> None:
    rolls = load_rollcalls()
    weeks = e13.fridays(date(1960, 1, 1), LAST)
    dose = ev.workload_dose(ev.weekly_counts(rolls, weeks))
    gate_dates = e13.fridays(date(1994, 2, 4), date(2025, 10, 3))
    d = Design(px, date(1994, 2, 4), 3, 31)

    def pair(src: dict[date, tuple[float, float]], k: int = 0) -> list[DoseFn]:
        return [
            lambda t: ev.shifted_pair(src, t, k)[0],
            lambda t: ev.shifted_pair(src, t, k)[1],
        ]

    if DRY:
        n = ev.weekly_counts(rolls, gate_dates)
        print("W27 roll calls read", len(rolls), "last dated", max(r[0] for r in rolls))
        print("W27 gate Fridays", len(gate_dates), "session weeks", sum(v > 0 for v in n.values()))
        for a in ("SPY", "QQQ", "IWM"):
            ok = sum(
                not np.isnan(
                    e13.window_return(px[a], t, 3, 31, 7, LAST)
                    + sum(e13.past_return(px[a], t, h) for h in HS)
                )
                for t in gate_dates
            )
            print("W27", a, "rows with outcome and controls", ok)
        ns = [
            sum(not np.isnan(ev.shifted_pair(dose, t, k)[0]) for t in gate_dates)
            for k in ev.SHIFTS_EARLY
        ]
        print("W27 placebos", len(ev.SHIFTS_EARLY), "dose weeks min", min(ns), "max", max(ns))
        return

    b, t, n = d.fit(["SPY"], gate_dates, pair(dose), controls=True)
    placebo = [d.fit(["SPY"], gate_dates, pair(dose, k), controls=True)[1] for k in ev.SHIFTS_EARLY]
    out = [
        "# Congress workload and SPY over the next 4 weeks (wide-15, W27 `congress-workload`)",
        "",
        "Rule: `research/wide-15.md` step 3 (pushed before this ran). Script",
        "`research/lib/wide15.py`. Dose x = 2 sqrt(n + 3/8), n = House + Senate roll calls dated",
        "Saturday..Friday F (Voteview); in-session dummy s = 1 if n > 0 also in the fit.",
        "y = log return of SPY from the close of the first bar >= F + 3 to the first bar",
        ">= F + 31.",
        "Controls: SPY's past 4/13/26/52-week returns. Newey-West t, 4 lags (one row a week).",
        "",
        *gate_block(
            "Fridays 1994-02-04..2025-10-03", b, t, n, placebo, ev.SHIFTS_EARLY, "per unit of x"
        ),
    ]

    def variant(**kw: object) -> dict[date, tuple[float, float]]:
        return ev.workload_dose(ev.weekly_counts(rolls, weeks, **kw))  # type: ignore[arg-type]

    late = [f for f in gate_dates if f >= date(2011, 1, 7)]
    out += [
        cell("Without the controls", d.fit(["SPY"], gate_dates, pair(dose), False)),
        cell("QQQ instead of SPY", d.fit(["QQQ"], gate_dates, pair(dose), True)),
        cell("IWM instead of SPY", d.fit(["IWM"], gate_dates, pair(dose), True)),
        cell(
            "Close votes only (margin < 10%)",
            d.fit(["SPY"], gate_dates, pair(variant(close_only=True)), True),
        ),
        cell("House only", d.fit(["SPY"], gate_dates, pair(variant(chamber="House")), True)),
        cell("Senate only", d.fit(["SPY"], gate_dates, pair(variant(chamber="Senate")), True)),
        cell(
            "Fridays 2011-01-07..2025-10-03 (after Pastor-Veronesi)",
            d.fit(["SPY"], late, pair(dose), True),
        ),
        cell(
            "1-week horizon (exit >= F + 10, 1 lag)",
            d.fit(["SPY"], gate_dates, pair(dose), True, exit_=10, lags=1),
        ),
        cell(
            "Calendar cell: c, the in-session dummy, % per 4 weeks (gate fit)",
            d.fit(["SPY"], gate_dates, pair(dose), True, coef=1),
        ),
        "",
        "F2 feedback check: x on SPY's own past return alone, session weeks only (NW 4 lags;",
        "negative = more votes after falls):",
        "",
        "| Past return | Slope, x per unit of log return (t) | Rows |",
        "|---|---:|---:|",
    ]
    sess = [f for f in gate_dates if dose[f][1] > 0]
    for h in HS:
        fb = d.feedback(["SPY"], sess, lambda t: dose[t][0], h)
        out.append(f"| {h // 7} weeks | {fb[0]:+.2f} ({fb[1]:+.2f}) | {fb[2]} |")
    out.append("")
    (RESULTS / "congress-workload.md").write_text("\n".join(out))
    print("\n".join(out))


# ---------------------------------------------------------------- W28


def refund_runoff(px: dict[str, e13.Closes]) -> None:
    daily = load_refunds()
    weeks = e13.fridays(date(2005, 10, 7), LAST)
    surprise = ev.refund_surprise(ev.weekly_sums(daily, weeks), ev.year_totals(daily))
    u = ev.runoff(surprise, weeks)
    gate_dates = e13.fridays(date(2008, 1, 4), date(2025, 10, 3))
    d = Design(px, date(2008, 1, 4), 5, 33)
    gate = ["QQQ", "IWM", "BTC", "ETH"]

    def at(src: dict[date, float], k: int = 0) -> list[DoseFn]:
        return [lambda t: e13.shifted(src, t, k)]

    if DRY:
        print(
            "W28 refund days read",
            len(daily),
            "first",
            min(daily),
            "last",
            max(daily),
            "years with a total",
            sorted(ev.year_totals(daily)),
        )
        print("W28 surprise weeks", len(surprise), "runoff weeks", len(u))
        print("W28 gate Fridays", len(gate_dates), "with u", sum(f in u for f in gate_dates))
        for a in [*gate, "SPY"]:
            ok = sum(
                not np.isnan(e13.window_return(px[a], t, 5, 33, 7, LAST)) and t in u
                for t in gate_dates
            )
            print("W28", a, "rows with outcome and dose", ok)
        ns = [sum(not np.isnan(e13.shifted(u, t, k)) for t in gate_dates) for k in e13.SHIFTS]
        print("W28 placebos", len(e13.SHIFTS), "dose weeks min", min(ns), "max", max(ns))
        return

    b, t, n = d.fit(gate, gate_dates, at(u), controls=False)
    placebo = [d.fit(gate, gate_dates, at(u, k), controls=False)[1] for k in e13.SHIFTS]
    out = [
        "# Tax-refund runoff and retail-heavy assets over the next 4 weeks (wide-15, W28",
        "`refund-runoff`)",
        "",
        "Rule: `research/wide-15.md` step 4 (pushed before this ran). Script",
        "`research/lib/wide15.py`. Dose u = Nash-cascade runoff (gamma 2, mean 2 weeks) of the",
        "weekly individual-refund surprise d (Daily Treasury Statement, same-ISO-week median of",
        "three earlier years as baseline, % of last year's refunds).",
        "y = log return from the close of the first bar >= F + 5 to the first bar >= F + 33;",
        "QQQ, IWM, BTC, ETH pooled with asset intercepts, Driscoll-Kraay t, 4 lags.",
        "Placebo k > 0 uses an earlier dose, k < 0 a later one (allowed: refunds do not answer",
        "prices).",
        "",
        *gate_block(
            "Fridays 2008-01-04..2025-10-03", b, t, n, placebo, e13.SHIFTS, "per unit of u"
        ),
    ]
    late = [f for f in gate_dates if f >= date(2017, 1, 6)]
    out += [
        cell("SPY alone", d.fit(["SPY"], gate_dates, at(u), False)),
        cell("QQQ and IWM", d.fit(["QQQ", "IWM"], gate_dates, at(u), False)),
        cell("BTC and ETH", d.fit(["BTC", "ETH"], gate_dates, at(u), False)),
        cell("Raw weekly surprise d instead of u", d.fit(gate, gate_dates, at(surprise), False)),
        cell("Seasons from 2017 (PATH Act hold)", d.fit(gate, late, at(u), False)),
        cell("With past 4/13/26/52-week returns", d.fit(gate, gate_dates, at(u), True)),
        cell(
            "1-week horizon (exit >= F + 12, 1 lag)",
            d.fit(gate, gate_dates, at(u), False, exit_=12, lags=1),
        ),
        "",
        "F2 feedback check: u on each asset's own past return alone (pooled, DK 4 lags):",
        "",
        "| Past return | Slope, u per unit of log return (t) | Rows |",
        "|---|---:|---:|",
    ]
    for h in HS:
        fb = d.feedback(gate, gate_dates, lambda t: u.get(t, np.nan), h)
        out.append(f"| {h // 7} weeks | {fb[0]:+.3f} ({fb[1]:+.2f}) | {fb[2]} |")
    out.append("")
    (RESULTS / "refund-runoff.md").write_text("\n".join(out))
    print("\n".join(out))


def main() -> None:
    if sys.argv[1:] == ["fetch"]:
        fetch()
        return
    syms = ["SPY", "QQQ", "IWM", "BTC", "ETH"]
    hist = harness.load_history("train", syms=syms)
    px = {a: e13.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    which = os.environ.get("GATE", "both")
    if which in ("both", "W27"):
        congress_workload(px)
    if which in ("both", "W28"):
        refund_runoff(px)


if __name__ == "__main__":
    main()
