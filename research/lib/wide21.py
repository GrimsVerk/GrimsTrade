"""Lane wide-21: gate W35 `solar-max-recession` (research/cards/wide-21.md; rule pushed before
this script's first run).

Descriptive only: no strategy, no backtest. Train bars only, cut at 2025-10-31 (this night's
lane rule); sunspot months after 2025-10 are never read. The sunspot file is an untrusted
download in the shared cache: run with `python -I`.

Fetch once:  `uv run python -I research/lib/wide21.py fetch`
Run:         `uv run python -I research/lib/wide21.py`  (DRY=1: counts only)
Output: research/results/solar-max-recession.md
"""

from __future__ import annotations

import math
import os
import subprocess
import sys
from collections.abc import Callable, Sequence
from datetime import date
from pathlib import Path

import numpy as np
import xlrd  # type: ignore[import-untyped]

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as e13  # noqa: E402
import wide17_events as e17  # noqa: E402
import wide21_events as ev  # noqa: E402

from grimstrade import cache  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)  # lane rule: nothing after this date is read
SNAP = "2026-11-25"
SILSO = "https://www.sidc.be/SILSO/INFO/snmtotcsv.php"
SILSO_REL = f"wide-21/silso/{SNAP}/SN_m_tot_V2.0.csv"
SHILLER = "shiller/2026-11-12/ie_data.xls"

XFn = Callable[[int], float]
YFn = Callable[[int], float]


def fetch() -> None:
    root = dw.cache_root()
    if not (root / SILSO_REL).exists():
        out = subprocess.run(
            ["curl", "-sS", "-f", "-m", "120", "-A", "Mozilla/5.0 (research script)", SILSO],
            check=True,
            capture_output=True,
        )
        cache.write_once(root, SILSO_REL, out.stdout, SILSO)
    print("fetched", root / SILSO_REL)


def load() -> tuple[dict[int, float], dict[int, tuple[float, float]]]:
    root = dw.cache_root()
    sn = ev.parse_silso((root / SILSO_REL).read_text(encoding="utf-8", errors="replace"), LAST)
    sheet = xlrd.open_workbook(str(root / SHILLER)).sheet_by_name("Data")
    sh = ev.parse_shiller((sheet.row_values(i) for i in range(sheet.nrows)), LAST)
    return sn, sh


def fit(months: Sequence[int], y: YFn, x: XFn, lags: int) -> tuple[float, float, int]:
    """(b, t, rows): OLS y = a + b x, Newey-West t with `lags`. One code path for every cell,
    true and placebo."""
    yy = np.array([y(m) for m in months])
    xx = np.array([x(m) for m in months])
    one = np.ones(len(months))
    beta, tt, n = e11.ols_dk([one, xx], yy, np.array(months), lags)
    return float(beta[1]), float(tt[1]), n


def null_lines(t: float, placebo: list[float], shifts: Sequence[int]) -> tuple[int, list[str]]:
    """Rank of the true t from the lowest (predicted b < 0) and the null block."""
    rank = e11.rank_highest(-t, [-p for p in placebo])
    sd, share = e11.null_spread(placebo)
    q5, med, q95 = e13.quantiles(placebo)
    lines = [
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {q5:+.2f}, 50% {med:+.2f}, 95% {q95:+.2f}; smallest"
        f" {min(placebo):+.2f}, largest {max(placebo):+.2f}.",
        "",
        "| k (months; > 0 an earlier dose) | t |",
        "|---:|---:|",
        *[f"| {k:+d} | {v:+.2f} |" for k, v in zip(shifts, placebo, strict=True)],
        "",
    ]
    return rank, lines


def cell(name: str, r: tuple[float, float, int], scale: float = 100.0, unit: str = "%") -> str:
    return f"| {name} | {r[0] * scale:+.3f}{unit} ({r[1]:+.2f}) | {r[2]} |"


def run() -> None:
    sn, sh = load()
    x = ev.trailing_dose(sn)
    mi = e17.month_index
    lo = mi(date(1871, 1, 1))
    y1: YFn = lambda m: ev.shiller_return(sh, m, 1)  # noqa: E731
    months = [m for m in range(lo, max(sh) + 1) if not math.isnan(y1(m))]
    hi = max(months)

    def at(src: dict[int, float], k: int = 0) -> XFn:
        return lambda m: ev.shifted(src, m, k)

    syms = ["GSPC", "SPY", "QQQ", "TLT", "GLD", "BTC", "ETH"]
    hist = harness.load_history("train", syms=syms)
    px = {
        s: e13.Closes({b.date: b.close for b in bars if b.date <= LAST}) for s, bars in hist.items()
    }

    def me(s: str) -> YFn:
        return lambda m: e17.month_return(px[s], m, m + 1, LAST)

    def me_months(s: str, start: int = 0) -> list[int]:
        return [
            m for m in range(max(start, mi(px[s].days[0])), mi(LAST)) if not math.isnan(me(s)(m))
        ]

    if DRY:
        print("sunspot months", len(sn), e17.month_last_day(min(sn)), "..",
              e17.month_last_day(max(sn)))  # fmt: skip
        print("shiller months", len(sh), e17.month_last_day(min(sh)), "..",
              e17.month_last_day(max(sh)))  # fmt: skip
        print("gate rows", len(months), e17.month_last_day(months[0]), "..",
              e17.month_last_day(hi), "dose defined", sum(m in x for m in months))  # fmt: skip
        ns = [sum(not math.isnan(ev.shifted(x, m, k)) for m in months) for k in ev.SHIFTS]
        print("placebos", len(ev.SHIFTS), "rows min", min(ns), "max", max(ns))
        peaks = ev.maxima(ev.smoothed13(sn))
        print("maxima", [e17.month_last_day(p).isoformat()[:7] for p in peaks])
        for s in syms:
            ms = me_months(s)
            print(s, "month-end rows", len(ms), e17.month_last_day(ms[0]), "..",
                  e17.month_last_day(ms[-1]))  # fmt: skip
        return

    b, t, n = fit(months, y1, at(x), 12)
    placebo = [fit(months, y1, at(x, k), 12)[1] for k in ev.SHIFTS]
    rank, null = null_lines(t, placebo, ev.SHIFTS)
    met = [b < 0 and t <= -2, rank <= 2]
    passed = all(met)

    peaks = ev.maxima(ev.smoothed13(sn))
    win = ev.window_indicator(range(lo - 200, mi(LAST) + 1), peaks)
    ph = ev.phase_dose(x)
    y12: YFn = lambda m: ev.shiller_return(sh, m, 12)  # noqa: E731
    fall: YFn = lambda m: ev.fall_within(sh, m, 12)  # noqa: E731
    gspc = me_months("GSPC")
    post = me_months("GSPC", mi(date(2012, 1, 1)))
    shown = [
        cell(
            "Gorbanev window (max -12..+24 months), indicator, look-ahead",
            fit(months, y1, at(win), 12),
        ),
        cell("Phase: x(m) - x(m-12)", fit(months, y1, at(ph), 12)),
        cell("12-month horizon P(m+1)..P(m+13), NW 18", fit(months, y12, at(x), 18)),
        cell(
            "Crash: 20% fall within 12 months (LPM, pp per unit; predicted > 0), NW 18",
            fit(months, fall, at(x), 18),
            unit=" pp",
        ),
        cell(
            f"GSPC month-end, {e17.month_last_day(gspc[0]):%Y-%m}.."
            f"{e17.month_last_day(gspc[-1]):%Y-%m}",
            fit(gspc, me("GSPC"), at(x), 12),
        ),
        cell(
            "GSPC month-end, post-Gorbanev dose months 2012-01..", fit(post, me("GSPC"), at(x), 12)
        ),
        *[
            cell(
                f"{s} month-end, from {e17.month_last_day(me_months(s)[0]):%Y-%m}",
                fit(me_months(s), me(s), at(x), 12),
            )  # fmt: skip
            for s in ("SPY", "QQQ", "TLT", "GLD", "BTC", "ETH")
        ],
    ]
    xs = np.array([x[m] for m in months])
    out = [
        "# Solar activity and next-month US stock returns (wide-21, W35 `solar-max-recession`)",
        "",
        "Rule: `research/cards/wide-21.md` (pushed before this ran). Script",
        "`research/lib/wide21.py`. Dose x(m) = trailing 12-month mean SILSO total sunspot number",
        "/ 100. y = ln((P(m+2) + D(m+2)/12) / P(m+1)), Shiller's monthly S&P 500 (P = monthly",
        "average of daily closes). Newey-West t, 12 lags, one row a dose month.",
        f"Dose over the gate rows: mean {xs.mean():.2f}, sd {xs.std(ddof=1):.2f}.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Dose months {e17.month_last_day(months[0]):%Y-%m}..{e17.month_last_day(hi):%Y-%m},"
        f" b (t), {n} rows | {b * 100:+.3f}% a month per 100 sunspots ({t:+.2f}) | < 0,"
        f" t <= -2 | {met[0]} |",
        f"| Rank of true t among 41 calendars (1 = lowest) | {rank} | <= 2 | {met[1]} |",
        "",
        f"**Gate: {'PASS (kill-only design: not dead yet)' if passed else 'fail'}.**"
        f" Empirical one-sided p = {rank}/41 = {rank / 41:.3f}.",
        "",
        "## Placebo null (sunspot calendar moved k months, both ways)",
        "",
        *null,
        "## Shown (not gating)",
        "",
        "Solar maxima used by the window cell (peaks of the 13-month smoothed series; look-ahead):",
        ", ".join(e17.month_last_day(p).isoformat()[:7] for p in peaks if p >= lo - 24) + ".",
        "",
        "| Cut | b per 100 sunspots (t) | Rows |",
        "|---|---:|---:|",
        *shown,
        "",
    ]
    if passed:
        out += ["R35 replication: run `GATE=R35` (card: run at once after a pass).", ""]
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "solar-max-recession.md").write_text("\n".join(out))
    print("\n".join(out))


def main() -> None:
    if sys.argv[1:] == ["fetch"]:
        fetch()
        return
    run()


if __name__ == "__main__":
    main()
