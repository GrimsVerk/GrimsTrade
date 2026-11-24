"""vix-call-1: a VIX-call overlay on `tsmom12`. Card: cards/vix-call-1.md.

    uv run python -I research/lib/vixcall1.py   # needs insure-3's raw files in the data cache

The overlay is CBOE VXTH's VIX-call sleeve, taken as VXTH's daily return minus the S&P 500 total
return's (the `leg`), added at full size every session on top of the record's `tsmom12` (V1),
or VXTH held while trend is in and bills while out (V2, insure-4's shape). Window: VXTH's
sessions 2006-03-31..2025-10-31. Compared with hold, `tsmom12`, VXTH, PPUT and insure-3's mix, and
with two alternatives set to V1's growth cost (less equity; trend mixed with PPUT). Raw levels
stay in the cache (CBOE terms); only statistics go to research/results/vix-call-1.md. Nothing
after 2025-10-31 is parsed. tries.md rows are written once.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable, Sequence
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import insure3 as i3  # noqa: E402
import insure4 as i4  # noqa: E402
from macro import cache_root  # noqa: E402

IDEA = "vix-call-1"
COST = i3.COST  # 2 bps a side, as tsmom12
DRAG = 0.005  # robustness: 0.50 points a year for VIX option bid-ask
BLOCK, BLOCK_SIDE = i4.BLOCK, i4.BLOCK_SIDE
BAR_Z = i4.BAR_Z  # research/register/BAR.md, rows through 2026-11-24 20:01
MISSED_SHARE = 0.5  # trend-missed fall: in at the peak and share avoided below this
VIX_FILE = ("cboe", "2026-11-12", "VIX_History.csv")
OUT = harness.RESEARCH / "results" / "vix-call-1.md"
TRIES = harness.RESEARCH / "tries.md"


# --- the overlay and the rules ---


def simple(level: np.ndarray) -> np.ndarray:
    """Per-session simple returns of a level series; index 0 (the base day) is 0."""
    out = np.zeros(len(level))
    out[1:] = level[1:] / level[:-1] - 1
    return out


def leg(r_vx: np.ndarray, r_hold: np.ndarray) -> np.ndarray:
    """The VIX-call overlay: VXTH's return minus the index's, per session (self-financed)."""
    out = r_vx - r_hold
    out[0] = 0.0
    return out


def overlay(r_base: np.ndarray, lg: np.ndarray, k: float = 1.0) -> np.ndarray:
    return r_base + k * lg


def trend_bills(days: Sequence[date], level: np.ndarray, rf: np.ndarray) -> np.ndarray:
    """insure-3's `tsmom12` on a total-return level, idle cash at bills."""
    ret, pos = i3.trend(days, level)
    out = ret + (1 - pos) * rf
    out[0] = 0.0
    return out


def v1_from_level(
    days: Sequence[date], level: np.ndarray, vx: np.ndarray, rf: np.ndarray, k: float = 1.0
) -> np.ndarray:
    """V1 from the index and VXTH levels: `tsmom12` (cash at bills) plus k x the leg."""
    return overlay(trend_bills(days, level, rf), leg(simple(vx), simple(level)), k)


def v2_from_level(
    days: Sequence[date], level: np.ndarray, vx: np.ndarray, rf: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """V2: VXTH while `tsmom12` is in, bills while out (insure-4's rule with VXTH for PPUT)."""
    return i4.rule_from_level(days, level, simple(vx), rf, COST)


def drag(days: Sequence[date], rate: float) -> np.ndarray:
    """A cost of `rate` a year, per session by calendar days elapsed (index 0 is 0)."""
    out = np.zeros(len(days))
    for i in range(1, len(days)):
        out[i] = rate * (days[i] - days[i - 1]).days / 365
    return out


def delever(r: np.ndarray, rf: np.ndarray, e: float) -> np.ndarray:
    """Exposure e to r, the rest in bills, rebalanced every session."""
    out = e * r + (1 - e) * rf
    out[0] = 0.0
    return out


def solve(
    f: Callable[[float], float], target: float, lo: float = 0.0, hi: float = 1.0, iters: int = 60
) -> tuple[float, bool]:
    """x in [lo, hi] with f(x) = target for a monotone f, by bisection; (x, clipped)."""
    flo, fhi = f(lo), f(hi)
    up = fhi >= flo
    if (target <= flo) if up else (target >= flo):
        return lo, target != flo
    if (target >= fhi) if up else (target <= fhi):
        return hi, target != fhi
    a, b = lo, hi
    for _ in range(iters):
        m = (a + b) / 2
        if (f(m) < target) == up:
            a = m
        else:
            b = m
    return (a + b) / 2, False


def keep_mask(n: int, a: int, b: int) -> np.ndarray:
    """All sessions but (a, b]: the sessions of a fall from its peak to its trough."""
    m = np.ones(n, dtype=bool)
    m[a + 1 : b + 1] = False
    return m


def log_gap(x: np.ndarray, y: np.ndarray, mask: np.ndarray | None = None) -> float:
    """100 x (total log growth of x - of y), index 0 dropped, over the kept sessions."""
    m = np.ones(len(x), dtype=bool) if mask is None else mask.copy()
    m[0] = False
    return 100 * float(np.log1p(x[m]).sum() - np.log1p(y[m]).sum())


def sharpe_diff(x: np.ndarray, y: np.ndarray, rf: np.ndarray, mask: np.ndarray) -> float:
    m = mask.copy()
    m[0] = False
    return i4.sharpe252((x - rf)[m]) - i4.sharpe252((y - rf)[m])


def premium_vs(g: float, s: float) -> float:
    """P_T = -(G - S) / S: log points given up against trend outside the falls per point
    gained inside them (below 1: paid back more than it cost)."""
    return -(g - s) / s if s > 0 else math.inf


def vix_band(v: float) -> str:
    """VXTH's weight band for a VIX level: 0% at 15 or below, 1% to 30, 0.5% to 50, else 0%."""
    if v <= 15:
        return "<=15"
    if v <= 30:
        return "15-30"
    if v <= 50:
        return "30-50"
    return ">50"


# --- run ---


def vix_closes() -> dict[date, float]:
    text = cache_root().joinpath(*VIX_FILE).read_text()
    out: dict[date, float] = {}
    for line in text.splitlines()[1:]:
        cells = line.split(",")
        try:
            d = datetime.strptime(cells[0].strip(), "%m/%d/%Y").date()
            v = float(cells[4])
        except (ValueError, IndexError):
            continue
        if d <= i3.LAST:
            out[d] = v
    return out


def tries_rows(days: list[date], s: dict[str, np.ndarray], turns: dict[str, float]) -> list[str]:
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"
    spec = [
        ("tsmom12+vxth-leg@vixcall1", "V1", "variant"),
        ("tsmom12-in-vxth-bills@vixcall1", "V2", "variant"),
        ("tsmom12+vxth-leg-x2@vixcall1", "V1@x2", "robustness"),
        ("tsmom12+vxth-leg-cost50@vixcall1", "V1@cost50", "robustness"),
        ("tsmom12-cash0+vxth-leg@vixcall1", "V1@cash0", "robustness"),
        ("tsmom12-delever-matched@vixcall1", "A1", "control"),
        ("mix-tsmom12-pput-matched@vixcall1", "A2", "control"),
    ]
    out = []
    for var, key, kind in spec:
        if key not in s:
            continue
        x = s[key].copy()
        x[0] = 0.0
        out.append(
            f"| {now} | {IDEA} | {var} | {kind} | train | {days[0]} | {days[-1]} | "
            f"{i3.calendar_sharpe(x, days):.2f} | {np.prod(1 + x) - 1:+.1%} | {i3.mdd(x):.1%} | "
            f"{turns.get(key, math.nan):.2f} |"
        )
    return out


def main() -> None:
    full_days, s3, rf_full, chk = i3.load()
    lo = full_days.index(chk["VXTH_start"])
    days = full_days[lo:]
    rf = rf_full[lo:].copy()
    rf[0] = 0.0
    pos = chk["pos"][lo:]
    cut = {}
    for k in ("hold", "trend", "trend@cash0", "PPUT", "mix", "VXTH"):
        v = s3[k][lo:].copy()
        v[0] = 0.0
        cut[k] = v
    hold, trend, vx = cut["hold"], cut["trend"], cut["VXTH"]
    lg = leg(vx, hold)
    v2 = i4.protected(pos, vx, rf, COST)
    # check: V2 with the index in place of VXTH is tsmom12 (cash at bills)
    same = i4.protected(pos, hold, rf, COST)
    assert np.allclose(same[1:], trend[1:], atol=1e-12), "V2 != tsmom12 with VXTH = index"
    v1 = overlay(trend, lg)
    s: dict[str, np.ndarray] = {
        "hold": hold,
        "trend": trend,
        "VXTH": vx,
        "PPUT": cut["PPUT"],
        "mix": cut["mix"],
        "V1": v1,
        "V2": v2,
        "V1@x2": overlay(trend, lg, 2.0),
        "V1@cost50": v1 - drag(days, DRAG),
        "V1@cash0": overlay(cut["trend@cash0"], lg),
    }
    cg = {k: i3.cagr(v, days) for k, v in s.items()}
    c = 100 * (cg["trend"] - cg["V1"])
    matched: dict[str, tuple[float, bool]] = {}
    if c > 0:
        t = cg["V1"]
        e, ce = solve(lambda x: i3.cagr(delever(trend, rf, x), days), t)
        w, cw = solve(lambda x: i3.cagr(i3.mix(days, trend, cut["PPUT"], x), days), t)
        s["A1"] = delever(trend, rf, e)
        s["A2"] = i3.mix(days, trend, cut["PPUT"], w)
        matched = {"A1": (e, ce), "A2": (w, cw)}
    names = list(s)
    rows, ff = i3.stats_block(days, s, rf, names)
    idx = {d: i for i, d in enumerate(days)}
    lo20, hi20 = i3.NAMED_FAST["2020"]
    f20 = [f for f in ff if lo20 <= f.trough <= hi20]
    assert len(f20) == 1, "expected one 2020 fall"
    f20_ = f20[0]
    missed = [f for f in ff if pos[idx[f.peak]] == 1 and f.share["trend"] < MISSED_SHARE]
    fast = [f for f in ff if f.days <= i3.FAST]
    # paired Sharpe tests against trend
    tests = []
    for k in ("V1", "V2"):
        for blk in (BLOCK, BLOCK_SIDE):
            tests.append((k, "trend", blk, *i4.paired_test(s[k], trend, rf, blk)))
    for k in ("V1@x2", "V1@cost50", "V1@cash0"):
        tests.append((k, "trend", BLOCK, *i4.paired_test(s[k], trend, rf, BLOCK)))
    tests.append(("VXTH", "hold", BLOCK, *i4.paired_test(vx, hold, rf, BLOCK)))
    z = {(a, blk): zz for a, b, blk, d, se, zz, p in tests if b == "trend"}
    # premium against trend, all window and with 2020 left out
    keep = keep_mask(len(days), idx[f20_.peak], idx[f20_.trough])
    full_mask = np.ones(len(days), dtype=bool)
    prem = {}
    for k in ("V1", "V2", "V1@x2", "V1@cost50", "V1@cash0", "A1", "A2", "VXTH"):
        if k not in s:
            continue
        g = log_gap(s[k], trend)
        sm = sum(f.ins[k] - f.ins["trend"] for f in ff)
        g_ex = log_gap(s[k], trend, keep)
        sm_ex = sm - (f20_.ins[k] - f20_.ins["trend"])
        prem[k] = (
            g,
            sm,
            premium_vs(g, sm),
            g_ex,
            premium_vs(g_ex, sm_ex),
            sharpe_diff(s[k], trend, rf, full_mask),
            sharpe_diff(s[k], trend, rf, keep),
        )
    z_ex = {}
    for k in ("V1", "V2"):
        m = keep.copy()
        m[0] = False
        a = np.concatenate([[0.0], s[k][m]])
        b = np.concatenate([[0.0], trend[m]])
        r0 = np.concatenate([[0.0], rf[m]])
        z_ex[k] = i4.paired_test(a, b, r0, BLOCK)
    # leave each fall out (descriptive): V1's log gap to trend
    loo = []
    for f in ff:
        m = keep_mask(len(days), idx[f.peak], idx[f.trough])
        loo.append((f, log_gap(v1, trend, m), sharpe_diff(v1, trend, rf, m)))

    def mean_ins(k: str, fs: Sequence[i3.Fall]) -> float:
        return float(np.mean([f.ins[k] for f in fs])) if fs else math.nan

    def kills(k: str) -> list[tuple[str, bool, str]]:
        out = [
            (
                "1 loses less than trend in 2020",
                f20_.loss[k] > f20_.loss["trend"],
                f"{f20_.loss[k]:+.1%} vs trend {f20_.loss['trend']:+.1%}",
            ),
            (
                "2 more loss avoided than trend over trend-missed falls",
                mean_ins(k, missed) > mean_ins("trend", missed),
                f"mean I {mean_ins(k, missed):+.1f} vs trend {mean_ins('trend', missed):+.1f} "
                f"log pts ({len(missed)} falls)",
            ),
            ("3 paired Sharpe z > -1.645", z[(k, BLOCK)] > -1.645, f"z {z[(k, BLOCK)]:+.2f}"),
            (
                "4 not resting on 2020 alone (G or d > 0 without 2020)",
                prem[k][3] > 0 or prem[k][6] > 0,
                f"G without 2020 {prem[k][3]:+.1f} log pts, d {prem[k][6]:+.3f}",
            ),
        ]
        # each entry: (test, killed?, numbers); out[i][1] above is "passes the test"
        res = [(t, not ok, txt) for t, ok, txt in out]
        if k == "V1":
            if c > 0:
                best = max(mean_ins(a, missed) for a in ("A1", "A2"))
                res.append(
                    (
                        "5 matched cost: no alternative covers the trend-missed falls better",
                        best > mean_ins("V1", missed),
                        f"V1 {mean_ins('V1', missed):+.1f}, A1 {mean_ins('A1', missed):+.1f}, "
                        f"A2 {mean_ins('A2', missed):+.1f} log pts",
                    )
                )
            else:
                res.append(("5 matched cost", False, f"c = {c:+.2f} <= 0: trend itself"))
        return res

    def verdict(k: str) -> str:
        kk = kills(k)
        if any(killed for _, killed, _ in kk):
            if all(not killed for t, killed, _ in kk if not t.startswith("4")):
                return "rests on one crash (kill 4)"
            return "killed (" + ", ".join(t.split()[0] for t, killed, _ in kk if killed) + ")"
        if z[(k, BLOCK)] >= BAR_Z:
            return "passes"
        return "not killed, not shown"

    vix = vix_closes()

    def vix_at(d: date) -> str:
        """VIX close on or before d, as VXTH's weight band only (CBOE terms: no raw levels)."""
        ks = [x for x in vix if x <= d]
        return vix_band(vix[max(ks)]) if ks else "-"

    show = ["hold", "trend", "VXTH", "PPUT", "mix", "V1", "V2"] + [
        a for a in ("A1", "A2") if a in s
    ]
    yrs = (days[-1] - days[0]).days / 365.25
    flips = float(np.abs(np.diff(pos)).sum() / yrs)
    share_in = float(pos[1:].mean())
    turns = {
        "V1": flips + 12,
        "V2": flips + 12 * share_in,
        "V1@x2": flips + 12,
        "V1@cost50": flips + 12,
        "V1@cash0": flips + 12,
        "A1": flips,
        "A2": flips + 12,
    }
    vix_le15 = float(np.mean([vix[d] <= 15 for d in days if d in vix]))
    md = [
        "# vix-call-1 results (generated by `research/lib/vixcall1.py`; do not edit)",
        "",
        f"Window {days[0]}..{days[-1]} ({len(days) - 1} sessions), VXTH's sessions in insure-3's "
        "data. leg = VXTH's daily return minus the S&P 500 total return's. V1 = `tsmom12` (cash at "
        "bills) + leg; V2 = VXTH while trend is in, bills while out (2 bps a side); @x2 double "
        "leg; @cost50 V1 minus 0.50 pts a year; @cash0 trend's idle cash at 0. A1 = trend at "
        "exposure e (rest bills), A2 = w trend + (1 - w) PPUT (monthly), each set to V1's CAGR. "
        "Insurance cost = gap to hold (points a year) / mean loss avoided per fall (log points).",
        "",
        "## Main table",
        "",
        i3.HEAD,
        *rows,
        "",
        f"V1's growth cost against trend c = {c:+.2f} points a year."
        + (
            "".join(
                f" {a}: {'e' if a == 'A1' else 'w'} = {x:.3f}{' (clipped)' if cl else ''}."
                for a, (x, cl) in matched.items()
            )
            if matched
            else " No matched alternative needed."
        ),
        "",
        "## Paired Sharpe test (above bills, daily, x sqrt(252)); stationary bootstrap, "
        f"{i4.DRAWS} draws, seed {i4.SEED}",
        "",
        "| Series | minus | Mean block | d | SE | z | p (one-sided, not better) |",
        "|---|---|---:|---:|---:|---:|---:|",
        *[
            f"| {a} | {b} | {blk} | {d:+.3f} | {se:.3f} | {zz:+.2f} | {p:.3f} |"
            for a, b, blk, d, se, zz, p in tests
        ],
        *[
            f"| {k}, 2020 fall left out | trend | {BLOCK} | {d:+.3f} | {se:.3f} | {zz:+.2f} | "
            f"{p:.3f} |"
            for k, (d, se, zz, p) in z_ex.items()
        ],
        "",
        "## Against trend: growth given up outside the falls per point gained inside them",
        "",
        "G = total log growth minus trend's (log pts); S = sum over falls of loss avoided minus "
        "trend's; P_T = -(G - S) / S (below 1: paid back more than it cost). Without 2020: the "
        "sessions of the 2020 fall (peak, trough] dropped from every series.",
        "",
        "| Series | G | S | P_T | G without 2020 | P_T without 2020 | Sharpe d | d without 2020 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        *[
            f"| {k} | {g:+.1f} | {sm:+.1f} | {p:.2f} | {gx:+.1f} | {px:.2f} | "
            f"{d:+.3f} | {dx:+.3f} |"
            for k, (g, sm, p, gx, px, d, dx) in prem.items()
        ],
        "",
        "## Every 15% fall",
        "",
        *i3.fall_table(ff, show),
        "",
        "Trend in at the peak, VIX close at the peak as VXTH's band (diagnostic): "
        + ", ".join(f"{f.peak} {pos[idx[f.peak]]:.0f} / {vix_at(f.peak)}" for f in ff)
        + ".",
        "",
        f"Trend-missed falls (in at the peak, trend's share avoided < {MISSED_SHARE}): "
        + (", ".join(f"{f.peak}..{f.trough}" for f in missed) or "none")
        + ".",
        "",
        "## By kind of fall: mean share avoided / mean net of the next 365 days (log pts)",
        "",
        "| Subset | Falls | " + " | ".join(show) + " |",
        "|---|---:|" + "---:|" * len(show),
        i3.subset(f20, show, "named fast: 2020"),
        i3.subset(missed, show, "trend-missed"),
        i3.subset(fast, show, f"<= {i3.FAST} days"),
        i3.subset([f for f in ff if f.days > i3.FAST], show, f"> {i3.FAST} days"),
        i3.subset(ff, show, "all"),
        "",
        "Mean loss avoided over the trend-missed falls (log pts): "
        + ", ".join(f"{k} {mean_ins(k, missed):+.1f}" for k in show)
        + ".",
        "",
        "## Leave one fall out (V1 minus trend, descriptive)",
        "",
        "| Fall left out | Days | V1 log gap to trend without it | Sharpe d without it |",
        "|---|---:|---:|---:|",
        *[f"| {f.peak}..{f.trough} | {f.days} | {g:+.1f} | {d:+.3f} |" for f, g, d in loo],
        "",
        "## Verdicts (card's kill bars)",
        "",
    ]
    for k in ("V1", "V2"):
        md += [
            f"**{k}: {verdict(k)}** (Sharpe label: {i4.verdict(z[(k, BLOCK)])}, bar z >= {BAR_Z}).",
            "",
        ]
        md += [f"- kill {t}: {'KILLED' if killed else 'ok'} ({txt})" for t, killed, txt in kills(k)]
        md.append("")
    md += [
        "## Diagnostics",
        "",
        f"- Trend in the market {share_in:.1%} of the window's sessions, {flips:.2f} flips a year.",
        f"- VIX close at 15 or below (VXTH holds no calls) on {vix_le15:.0%} of the sessions.",
        f"- VXTH sessions carried (no level): {chk['VXTH_miss']}.",
        "- Check passed: V2 with the S&P 500 total return in place of VXTH equals `tsmom12`.",
        "",
    ]
    OUT.write_text("\n".join(md))
    print("\n".join(md))
    text = TRIES.read_text()
    new = [r for r in tries_rows(days, s, turns) if f"| {r.split(' | ')[2]} |" not in text]
    if new:
        with TRIES.open("a") as f:
            f.write("\n".join(new) + "\n")
    print(f"{len(new)} tries rows appended")


if __name__ == "__main__":
    main()
