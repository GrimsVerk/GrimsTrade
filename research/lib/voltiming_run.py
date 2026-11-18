"""vol-timing: is ls-trend-2's control b1 just volatility timing of `tsmom12`? (descriptive)
Card: research/cards/vol-timing.md.

    uv run --with openpyxl python -I research/lib/voltiming_run.py <cache_root>

Reuses `lstrend2_run.py` Part A (the wide book at gross 1, the `tsmom12` sleeve, the blend and
its control b1). Appends the card's 3 replication rows to `tries.md` (first run only) and writes
`research/results/vol-timing.md`. No day after 2025-10-31 is read.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cash_interest as ci  # noqa: E402
import common as c  # noqa: E402
import harness  # noqa: E402
import lstrend1_run as l1  # noqa: E402
import lstrend2_run as l2  # noqa: E402
import numpy as np  # noqa: E402
import rules  # noqa: E402
import stats  # noqa: E402
import survey5_live as s5  # noqa: E402

IDEA = "vol-timing"
P, LD, LAST_DAY = l2.P, l2.LD, l2.LAST_DAY


def tv40_series() -> tuple[dict[date, float], float]:
    """`trend-vol` (tv40) daily excess over bills (bill interest on cash), and turnover/yr."""
    six = c.ctx("six")
    run = c.go(IDEA, "tv40", c.weekly(rules.trend_vol(0.40)), six, "replication", log=False)
    days, ylds = ci.bill_yield()
    r, rf = ci.rescored(run, days, ylds)
    dd = run.days[1:]
    ex = {d: float(x - f_) for d, x, f_ in zip(dd, r, rf, strict=True) if d <= LAST_DAY}
    return ex, run.score.turnover


def vt_own(s1: l2.Sleeve, start: date, mean_share: float) -> tuple[dict, dict]:
    """`tsmom12` at share min(1, k / sigma52) set each month start, rest in bills; k solved so
    the mean share in P equals `mean_share`. Returns (daily excess, daily share)."""
    sig: dict[date, float] = {}
    d = start
    while d <= LAST_DAY:
        sig[d] = s1.sigma(d - timedelta(days=1))
        d = date(d.year + d.month // 12, d.month % 12 + 1, 1)

    def run(k: float) -> tuple[dict, dict]:
        ex: dict[date, float] = {}
        sh: dict[date, float] = {}
        v = 0.0
        for d in l2.cal_days(start, LAST_DAY):
            if d.day == 1:
                sg = sig[d]
                if sg > 0 and math.isfinite(sg):
                    v = min(1.0, k / sg)
            x = s1.ex.get(d, 0.0)
            sh[d], ex[d] = v, v * x
            v = v * (1 + x) / (v * (1 + x) + (1 - v)) if v > 0 else 0.0
        return ex, sh

    lo, hi = 0.0, 1.0
    for _ in range(60):
        k = (lo + hi) / 2
        m = float(np.mean([run(k)[1][d] for d in l2.cal_days(*P)]))
        lo, hi = (k, hi) if m < mean_share else (lo, k)
    return run((lo + hi) / 2)


def weekly(x: dict[date, float], a: date, b: date) -> np.ndarray:
    """Compounded Monday-Sunday weekly excess returns over complete weeks in [a, b]."""
    mon0 = a + timedelta(days=(7 - a.weekday()) % 7)
    out = []
    while mon0 + timedelta(days=6) <= b:
        g = 1.0
        for d in l2.cal_days(mon0, mon0 + timedelta(days=6)):
            g *= 1 + x.get(d, 0.0)
        out.append(g - 1)
        mon0 += timedelta(days=7)
    return np.array(out)


def resid(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    beta = np.cov(y, x)[0, 1] / x.var(ddof=1)
    return y - y.mean() - beta * (x - x.mean())


def row(variant: str, a: date, b: date, r: np.ndarray, turnover: float) -> str:
    return (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | replication | train | {a} | "
        f"{b} | {stats.sharpe(r):.2f} | {np.prod(1 + r) - 1:+.1%} | {l2.mdd(r):.1%} | "
        f"{turnover:.2f} |\n"
    )


def main(root: Path) -> None:
    rf_day = s5.bill_daily()
    g1 = l2.Book("wide-LS-g1", l1.WIDE, gross1=True)
    l2.run_books(l2.wide_prices(root), rf_day, [g1])
    s1, rf1, _drag, run = l2.tsmom12_sleeve()
    bl = l2.blend(s1, l2.wide_sleeve(g1), l1.COST)
    a_p = np.array([bl.a[d] for d in l2.cal_days(*P)])
    k = float(a_p.mean())
    const = {d: k * x for d, x in s1.ex.items()}
    vt, vt_sh = vt_own(s1, bl.start, k)
    tv, tv_turn = tv40_series()
    ser: dict[str, dict[date, float]] = {
        "`tsmom12`": s1.ex,
        "b1: split vs wide book (ls-trend-2 control)": bl.ctrl,
        f"const: {k:.2f} x `tsmom12` + bills": const,
        "vt-own: `tsmom12` / own sigma52 + bills": vt,
        "`trend-vol` tv40": tv,
    }
    share = {
        "`tsmom12`": 1.0,
        "b1: split vs wide book (ls-trend-2 control)": k,
        f"const: {k:.2f} x `tsmom12` + bills": k,
        "vt-own: `tsmom12` / own sigma52 + bills": float(
            np.mean([vt_sh[d] for d in l2.cal_days(*P)])
        ),
    }
    arr: Callable[[dict[date, float], tuple[date, date]], np.ndarray] = lambda x, w: l2.on_cal(  # noqa: E731
        x, *w
    )
    rf_cal = {w: l2.on_cal(rf1, *w) for w in (P, LD)}
    S = {
        n: {wn: stats.sharpe(arr(x, w)) for wn, w in (("P", P), ("L", LD))} for n, x in ser.items()
    }
    boot = {
        n: stats.sharpe_diff_boot(arr(x, P), arr(s1.ex, P), draws=l2.DRAWS, mean_block=20, seed=0)
        for n, x in ser.items()
        if n != "`tsmom12`"
    }

    out = [
        "# vol-timing: is ls-trend-2's control just volatility timing of `tsmom12`?",
        "",
        "Card: `cards/vol-timing.md` (committed before any number). Descriptive, no pick. Daily "
        "calendar excess returns over the 13-week T-bill, bill interest on idle cash, Sharpe a "
        "year in the repo's convention (daily, 365). P = 2007-04-01..2025-10-31, L = "
        "2010-02-01..2025-10-31. Nothing after 2025-10-31 read.",
        "",
        "## 1. Series",
        "",
        "| Series | Mean share P | Sharpe P | Sharpe L | Vol P | Max DD P (excess) | "
        "Max DD P (total) | dSharpe P vs `tsmom12` | boot p (better) | 5%..95% |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for n, x in ser.items():
        rp = arr(x, P)
        sh = share.get(n)
        b = boot.get(n)
        out.append(
            f"| {n} | {'-' if sh is None else f'{sh:.2f}'} | {S[n]['P']:.2f} | {S[n]['L']:.2f} | "
            f"{l2.vol_d(rp):.1%} | {l2.mdd(rp):.1%} | {l2.mdd(rp + rf_cal[P]):.1%} | "
            + (
                "- | - | - |"
                if b is None
                else f"{b[0]:+.3f} | {b[1]:.3f} | {b[2]:+.2f}..{b[3]:+.2f} |"
            )
        )
    nb1 = "b1: split vs wide book (ls-trend-2 control)"
    ncon = f"const: {k:.2f} x `tsmom12` + bills"
    nvt = "vt-own: `tsmom12` / own sigma52 + bills"
    ntv = "`trend-vol` tv40"
    nts = "`tsmom12`"
    out += [
        "",
        f"`trend-vol` mean exposure: see `results/trend-vol.md` (72% over 1994-2025); "
        f"turnover {tv_turn:.2f} a year. b1 and vt-own: no cost on the monthly share reset "
        "(as ls-trend-2's control); `tsmom12`'s and tv40's gym costs are inside.",
        "",
        "## 2. Decomposition of b1's Sharpe gain over `tsmom12`",
        "",
        "| Part | P | L |",
        "|---|---:|---:|",
    ]
    parts = [
        ("total: S(b1) - S(`tsmom12`)", nb1, nts),
        ("constant scaling: S(const) - S(`tsmom12`)", ncon, nts),
        ("time-varying: S(b1) - S(const)", nb1, ncon),
        ("  of which own-vol timing: S(vt-own) - S(const)", nvt, ncon),
        ("  of which the wide book's vol in the split: S(b1) - S(vt-own)", nb1, nvt),
        ("`trend-vol` for comparison: S(tv40) - S(`tsmom12`)", ntv, nts),
    ]
    for lab, a_, b_ in parts:
        out.append(f"| {lab} | {S[a_]['P'] - S[b_]['P']:+.3f} | {S[a_]['L'] - S[b_]['L']:+.3f} |")
    tot = S[nb1]["P"] - S[nts]["P"]
    if abs(tot) > 1e-9:
        cshare = (S[ncon]["P"] - S[nts]["P"]) / tot
        out += [
            "",
            f"Share of b1's P gain from constant scaling {cshare:.0%}, time-varying {1 - cshare:.0%}.",  # noqa: E501
        ]
    # correlations
    wk = {n: weekly(x, *P) for n, x in ser.items()}
    wl = {n: weekly(x, *LD) for n, x in ser.items()}
    cc = lambda u, v: float(np.corrcoef(u, v)[0, 1])  # noqa: E731
    out += [
        "",
        "## 3. Weekly correlation (Monday-Sunday, compounded)",
        "",
        "| Pair | P | L |",
        "|---|---:|---:|",
        f"| b1 vs `trend-vol` (raw) | {cc(wk[nb1], wk[ntv]):.2f} | {cc(wl[nb1], wl[ntv]):.2f} |",
        f"| vt-own vs `trend-vol` (raw) | {cc(wk[nvt], wk[ntv]):.2f} | {cc(wl[nvt], wl[ntv]):.2f} |",  # noqa: E501
        f"| b1 vs `tsmom12` (raw) | {cc(wk[nb1], wk[nts]):.2f} | {cc(wl[nb1], wl[nts]):.2f} |",
        f"| `trend-vol` vs `tsmom12` (raw) | {cc(wk[ntv], wk[nts]):.2f} | {cc(wl[ntv], wl[nts]):.2f} |",  # noqa: E501
        "| overlays: b1 vs `trend-vol`, residuals on `tsmom12` | "
        f"{cc(resid(wk[nb1], wk[nts]), resid(wk[ntv], wk[nts])):.2f} | "
        f"{cc(resid(wl[nb1], wl[nts]), resid(wl[ntv], wl[nts])):.2f} |",
        "| overlays: vt-own vs `trend-vol`, residuals on `tsmom12` | "
        f"{cc(resid(wk[nvt], wk[nts]), resid(wk[ntv], wk[nts])):.2f} | "
        f"{cc(resid(wl[nvt], wl[nts]), resid(wl[ntv], wl[nts])):.2f} |",
        "| overlays: b1 vs vt-own, residuals on `tsmom12` | "
        f"{cc(resid(wk[nb1], wk[nts]), resid(wk[nvt], wk[nts])):.2f} | "
        f"{cc(resid(wl[nb1], wl[nts]), resid(wl[nvt], wl[nts])):.2f} |",
        "",
        f"Weeks: P {len(wk[nts])}, L {len(wl[nts])}.",
    ]
    # crash windows
    out += ["", "## 4. Crash windows (excess over bills, compounded)", ""]
    out.append("| Series | 2008 | 2020-02..03 | 2022 |")
    out.append("|---|---:|---:|---:|")
    wins = [(date(2008, 1, 1), date(2008, 12, 31)), (date(2020, 2, 1), date(2020, 3, 31)),
            (date(2022, 1, 1), date(2022, 12, 31))]  # fmt: skip
    for n, x in ser.items():
        vals = [float(np.prod(1 + l2.on_cal(x, *w)) - 1) for w in wins]
        out.append(f"| {n} | " + " | ".join(f"{v:+.1%}" for v in vals) + " |")
    rows = [
        row("const-tsmom12@L07", *P, arr(const, P), k * run.score.turnover),
        row("vt-own-tsmom12@L07", *P, arr(vt, P), share[nvt] * run.score.turnover),
        row("tv40-ex@L07", *P, arr(tv, P), tv_turn),
    ]
    if f"| {IDEA} | const-tsmom12@L07 |" not in harness.TRIES.read_text():
        with harness.TRIES.open("a") as f:
            f.writelines(rows)
        print("logged 3 rows")
    path = harness.RESEARCH / "results" / "vol-timing.md"
    path.write_text("\n".join(out).rstrip() + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
