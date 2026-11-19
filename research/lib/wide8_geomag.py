"""Lane wide-8, step 2: event-study gate for W16 `geomagnetic-storm` (research/wide-8.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).
Needs GFZ's keyless Kp/Ap file in research/data/kp/ (CC BY 4.0; see wide-8.md).

Run: `uv run python -I research/lib/wide8_geomag.py`  (DRY=1: counts only)
Output: research/results/geomagnetic-storm.md
"""

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide6_rules as r6  # noqa: E402
import wide8_events as ev  # noqa: E402

KP = harness.DATA / "kp" / "Kp_ap_Ap_SN_F107_since_1932.txt"
OUT = Path(__file__).resolve().parents[1] / "results" / "geomagnetic-storm.md"
DRY = bool(os.environ.get("DRY"))
POST = (date(2003, 1, 1), date(2025, 11, 10))
SHIFTS = [k * 61 for k in range(-15, 16) if k != 0]
LAGS = 5


class Series:
    def __init__(self, sym: str):
        bars = harness.load_history("train", syms=[sym])[sym]
        self.days = [b.date for b in bars]
        self.logc = np.log(np.array([b.close for b in bars]))
        self.ret = np.r_[np.nan, np.diff(self.logc)]

    def mask(self, a: date, b: date) -> np.ndarray:
        d = np.array(self.days)
        return (d >= a) & (d <= b)


def fit(
    s: Series, ap: dict[date, int], a: date, b: date, shift: int = 0, severe: int = ev.SEVERE
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(coefficients, t, M) of r on [1, Sev, Min] over sessions in [a, b]."""
    m = ev.storm_max(s.days, ap, shift)
    keep = s.mask(a, b) & ~np.isnan(m) & ~np.isnan(s.ret)
    x = ev.storm_design(m[keep], severe=severe)
    beta, t = r6.ols_dk(s.ret[keep], x, list(range(int(keep.sum()))), LAGS)
    return beta, t, m[keep]


def fit_cont(s: Series, ap: dict[date, int], a: date, b: date) -> tuple[float, float]:
    m = ev.storm_max(s.days, ap)
    keep = s.mask(a, b) & ~np.isnan(m) & ~np.isnan(s.ret)
    x = np.column_stack([np.ones(int(keep.sum())), np.log1p(m[keep])])
    beta, t = r6.ols_dk(s.ret[keep], x, list(range(int(keep.sum()))), LAGS)
    return float(beta[1]), float(t[1])


def raw_after(s: Series, ap: dict[date, int], a: date, b: date) -> tuple[float, int]:
    """Mean log return over the first six sessions after each severe UT day in [a, b]."""
    out = []
    for d, v in ap.items():
        if v >= ev.SEVERE and a <= d <= b:
            i = int(np.searchsorted(np.array(s.days), d, side="right"))  # first session > d
            if i >= 1 and i + ev.STORM_SESSIONS - 1 < len(s.days):
                out.append(s.logc[i + ev.STORM_SESSIONS - 1] - s.logc[i - 1])
    return (float(np.mean(out)) if out else float("nan")), len(out)


def counts(ap: dict[date, int], m: np.ndarray, a: date, b: date) -> str:
    sev_d = sum(v >= ev.SEVERE for d, v in ap.items() if a <= d <= b)
    min_d = sum(ev.MINOR <= v < ev.SEVERE for d, v in ap.items() if a <= d <= b)
    return (
        f"severe days {sev_d}, minor days {min_d}, sessions {len(m)}, "
        f"severe sessions {int((m >= ev.SEVERE).sum())}, minor sessions "
        f"{int(((m >= ev.MINOR) & (m < ev.SEVERE)).sum())}"
    )


def bp(x: float) -> str:
    return f"{x * 1e4:+.1f}"


def main() -> None:
    ap = ev.parse_ap(KP.read_text())
    spy, gspc = Series("SPY"), Series("GSPC")
    samples = {
        "SPY 2003-2025 (gate)": (spy, *POST),
        "GSPC 1950-2002 (gate, in-sample)": (gspc, date(1950, 1, 1), date(2002, 12, 31)),
        "GSPC 2003-2025": (gspc, *POST),
        "SPY 1993-2002": (spy, date(1993, 1, 1), date(2002, 12, 31)),
    }
    if DRY:
        for k, (s, a, b) in samples.items():
            _, _, m = fit(s, ap, a, b)
            print(k, counts(ap, m, a, b))
        return
    res = {k: fit(s, ap, a, b) for k, (s, a, b) in samples.items()}
    bs, ts, _ = res["SPY 2003-2025 (gate)"]
    bi = res["GSPC 1950-2002 (gate, in-sample)"][0]
    shifted = [float(fit(spy, ap, *POST, shift=sh)[0][1]) for sh in SHIFTS]
    rank = ev.rank_most_negative(float(bs[1]), shifted)
    g = [
        bs[1] < 0 and ts[1] <= -2,
        bs[1] < bs[2],
        bi[1] < 0,
        rank <= 2,
    ]
    out = [
        "# Geomagnetic storms: event-study gate (wide-8, W16)",
        "",
        "Rule: `research/wide-8.md` step 2 (pushed before this ran). Script",
        "`research/lib/wide8_geomag.py`. Daily Ap: GFZ Potsdam (CC BY 4.0). Daily log returns,",
        "bps a day over calm sessions; Newey-West t, 5 lags. Severe: the largest Ap of the UT",
        "days whose six-session window holds the session is >= 100; minor: 30-99.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| SPY 2003-2025 b_sev (t) | {bp(bs[1])} ({ts[1]:+.2f}) | < 0, t <= -2 | {g[0]} |",
        f"| SPY 2003-2025 b_sev vs b_min | {bp(bs[1])} vs {bp(bs[2])} | b_sev < b_min | {g[1]} |",
        f"| GSPC 1950-2002 b_sev | {bp(bi[1])} | < 0 | {g[2]} |",
        f"| Rank of true b_sev among 31 calendars (1 = most negative) | {rank} | <= 2 | {g[3]} |",
        "",
        f"**Gate: {'PASS' if all(g) else 'fail'}.**",
        "",
        "## Shown",
        "",
        "| Sample | b_sev (t) | b_min (t) | Sev at Ap >= 50 (t) | log(1+M) slope (t) |"
        " Raw 6-session mean after severe days (n) | Counts |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for k, (s, a, b) in samples.items():
        beta, t, m = res[k]
        b50, t50, _ = fit(s, ap, a, b, severe=50)
        bc, tc = fit_cont(s, ap, a, b)
        raw, n = raw_after(s, ap, a, b)
        out.append(
            f"| {k} | {bp(beta[1])} ({t[1]:+.2f}) | {bp(beta[2])} ({t[2]:+.2f}) | "
            f"{bp(b50[1])} ({t50[1]:+.2f}) | {bp(bc)} ({tc:+.2f}) | {raw * 100:+.2f}% ({n}) | "
            f"{counts(ap, m, a, b)} |"
        )
    out += [
        "",
        "## Shifted calendars, SPY 2003-2025 b_sev (bps a day)",
        "",
        "| Shift (days) | b_sev |",
        "|---:|---:|",
    ]
    out += [f"| {sh:+d} | {bp(v)} |" for sh, v in zip(SHIFTS, shifted, strict=True)]
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
