"""risk-menu-2: risk-menu's items 1-7 on 1994-02..2025-10 (descriptive, no pick).
Card: research/cards/risk-menu-2.md.

    uv run python -I research/lib/riskmenu2_run.py

Reuses `riskmenu_run.py` (gym re-scores, the monthly-reset mix, the risk measures) on window
W = 1994-02-01..2025-10-31 instead of P; no wide book, so no cache root is needed. Compares the
orders by worst loss, worst 12 months and time under water with risk-menu's (P, from
`results/risk-menu.json`). Appends the card's 4 replication rows (first run only) and writes
`research/results/risk-menu-2.md` (+ `.json`). No day after 2025-10-31 is read.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common as c  # noqa: E402
import harness  # noqa: E402
import lstrend2_run as l2  # noqa: E402
import numpy as np  # noqa: E402
import riskmenu_run as rm  # noqa: E402
import stats  # noqa: E402

IDEA = "risk-menu-2"
W = (date(1994, 2, 1), rm.LAST_DAY)
CRASH = {"2000-02": (date(2000, 1, 1), date(2002, 12, 31)), **rm.CRASH}
MEASURES = (("mdd", "worst loss", False), ("w12", "worst 12 months", True),
            ("uw", "longest under water", False))  # fmt: skip  # (key, name, higher is better)


def vt_target_w(s1: l2.Sleeve, mean_share: float, held: rm.Callable[[date], int]) -> rm.Mix:
    """risk-menu's vt-own, k solved on W; the fixed target share until sigma52 exists."""
    sig = {d: s1.sigma(d - timedelta(days=1)) for d in rm.months_in(*W)}

    def build(k: float) -> rm.Mix:
        def tgt(d: date, v: float) -> tuple[float, float]:
            sg = sig[d]
            if not math.isfinite(sg):
                return (mean_share, 0.0)
            return (min(1.0, k / sg), 0.0) if sg > 0 else (v, 0.0)

        return rm.mix(s1, None, tgt, W[0], held)

    lo, hi = 0.0, 2.0
    for _ in range(50):
        k = (lo + hi) / 2
        m = float(np.mean([v for d, v in build(k).share1.items() if W[0] <= d <= W[1]]))
        lo, hi = (k, hi) if m < mean_share else (lo, k)
    return build((lo + hi) / 2)


def kendall(a: list[float], b: list[float]) -> float:
    """Kendall's tau-b of two value lists (ties allowed)."""
    n = len(a)
    con = dis = ta = tb = 0
    for i in range(n):
        for j in range(i + 1, n):
            x, y = np.sign(a[i] - a[j]), np.sign(b[i] - b[j])
            if x == 0 and y == 0:
                continue
            if x == 0:
                ta += 1
            elif y == 0:
                tb += 1
            elif x == y:
                con += 1
            else:
                dis += 1
    den = math.sqrt((con + dis + ta) * (con + dis + tb))
    return (con - dis) / den if den else math.nan


def main() -> None:
    s1, rf1, _drag, run = l2.tsmom12_sleeve()
    six = c.ctx("six")
    held = rm.held_count(run)
    days, ylds = rm.ci.bill_yield()
    items: list[rm.Item] = []
    for key, name, f in (("hold six", "Hold the six (equal weight)", c.equal_weight),
                         ("60/40", "60/40 (SPY / TLT)", c.sixty_forty)):  # fmt: skip
        r = c.go(IDEA, key, c.weekly(f), six, "baseline", log=False)  # re-score, logged config
        rr, rf = rm.ci.rescored(r, days, ylds)
        exd = {d: float(x - y) for d, x, y in zip(r.days[1:], rr, rf, strict=True)}
        x = rm.Item(key, name, "hold", exd)
        x.expo = dict(rm_expo([(z.time.date(), sum(z.weights.values())) for z in r.decisions], W))
        items.append(x)
    dec = [(x.time.date(), sum(x.weights.values())) for x in run.decisions]
    it = rm.Item("tsmom12", "`tsmom12`, full size", "size", s1.ex)
    it.expo = dict(rm_expo(dec, W))
    items.append(it)
    shares: dict[str, float] = {"tsmom12": 1.0}
    for sh in (0.70, 0.26):
        mx = rm.mix(s1, None, lambda d, v, sh=sh: (sh, 0.0), W[0], held)
        key = f"tsmom12 {sh:.0%}"
        x = rm.Item(key, f"`tsmom12` {sh:.0%} + T-bills", "size", mx.ex)
        x.expo = {d: mx.expo[d] for d in l2.cal_days(*W)}
        shares[key] = float(np.mean([mx.share1[d] for d in l2.cal_days(*W)]))
        items.append(x)
    for sh in (0.26, 0.70):
        mx = vt_target_w(s1, sh, held)
        key = f"vt-own {sh:.0%}"
        x = rm.Item(key, f"Own-vol target, mean share {sh:.0%}", "vt", mx.ex)
        x.expo = {d: mx.expo[d] for d in l2.cal_days(*W)}
        shares[key] = float(np.mean([mx.share1[d] for d in l2.cal_days(*W)]))
        items.append(x)

    rf_w = l2.on_cal(rf1, *W)
    ex = {i.key: l2.on_cal(i.ex, *W) for i in items}
    m: dict[str, dict[str, float | str]] = {}
    for i in items:
        e = ex[i.key]
        tot = e + rf_w
        eq = np.concatenate([[1.0], np.cumprod(1 + tot)])
        cr = {}
        for n, (a_, b_) in CRASH.items():
            k0, k1 = (a_ - W[0]).days, (b_ - W[0]).days
            cr[n] = float(eq[k1 + 1] / eq[k0] - 1)
        peak = np.maximum.accumulate(eq)
        k_low = int(np.argmax(1 - eq / peak))
        k_high = int(np.argmax(eq[: k_low + 1]))
        w12 = eq[365:] / eq[:-365]
        k_w12 = int(np.argmin(w12))
        m[i.key] = {
            "sharpe": stats.sharpe(e), "se": stats.sharpe_se(e), "cagr": stats.cagr(tot),
            "vol": stats.vol(tot), "mdd": l2.mdd(tot), "w12": rm.worst_12m(eq),
            "uw": rm.underwater_years(eq), "expo": float(np.mean(list(i.expo.values()))),
            "mdd_from": str(W[0] + timedelta(days=k_high - 1)),
            "mdd_to": str(W[0] + timedelta(days=k_low - 1)),
            "w12_end": str(W[0] + timedelta(days=k_w12 + 365 - 1)), **cr,
        }  # fmt: skip
    p_json = json.loads((harness.RESEARCH / "results" / "risk-menu.json").read_text())

    def f(x: float | str) -> float:
        return float(x)

    out = [
        "# risk-menu-2: the menu's risk columns on 1994-2025 (descriptive, no pick)",
        "",
        "Card: `cards/risk-menu-2.md` (committed before any number). W = "
        f"{W[0]}..{W[1]}; items 1-7 of risk-menu (no wide book); definitions, costs and T-bill "
        "cash as risk-menu. Sharpe on daily excess returns over the 13-week T-bill (365-day "
        "convention); every other measure on the total-return curve. Own-vol target: k solved on "
        "W, fixed target share until `tsmom12` has 52 weeks. Before QQQ (1999-03) the six is SPY "
        "alone; before TLT (2002-07) 60/40 is 60% SPY and 40% bills. Nothing after 2025-10-31 "
        "read.",
        "",
        "## 1. Return and risk on W",
        "",
        "| Item | Sharpe W (SE) | Growth/yr | Vol | Worst loss | Worst 12 months | Longest "
        "under water | 2000-02 | 2008 | 2020 Q1 | 2022 | Mean share | Avg exposure |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for i in items:
        q = m[i.key]
        sh = shares.get(i.key)
        out.append(
            f"| {i.name} | {f(q['sharpe']):.2f} ({f(q['se']):.2f}) | {f(q['cagr']):.1%} | "
            f"{f(q['vol']):.1%} | {f(q['mdd']):.1%} | {f(q['w12']):+.1%} | {f(q['uw']):.1f} y | "
            f"{f(q['2000-02']):+.1%} | {f(q['2008']):+.1%} | {f(q['2020 Q1']):+.1%} | "
            f"{f(q['2022']):+.1%} | {'-' if sh is None else f'{sh:.2f}'} | {f(q['expo']):.2f} |"
        )
    out += [
        "",
        "## 2. When the worst came",
        "",
        "| Item | Worst loss: high | Worst loss: low | Worst 12 months: ending |",
        "|---|---|---|---|",
    ]
    for i in items:
        q = m[i.key]
        out.append(f"| {i.name} | {q['mdd_from']} | {q['mdd_to']} | {q['w12_end']} |")
    out += [
        "",
        "## 3. Do the risk rankings hold? (W against risk-menu's P = 2007-04..2025-10)",
        "",
        "Rank 1 = best (smallest worst loss, mildest worst 12 months, shortest time under water). "
        "Holds = same first item and Kendall's tau >= 0.7 (card).",
        "",
    ]
    verdict: dict[str, dict[str, object]] = {}
    for key, name, up in MEASURES:
        vw = [f(m[i.key][key]) for i in items]
        vp = [float(p_json[i.key][key]) for i in items]
        sgn = -1 if up else 1
        rw = [1 + sum(1 for y in vw if sgn * y < sgn * x - 1e-12) for x in vw]
        rp = [1 + sum(1 for y in vp if sgn * y < sgn * x - 1e-12) for x in vp]
        tau = kendall([sgn * x for x in vw], [sgn * x for x in vp])
        first_w = [i.key for i, r in zip(items, rw, strict=True) if r == 1]
        first_p = [i.key for i, r in zip(items, rp, strict=True) if r == 1]
        holds = first_w == first_p and tau >= 0.7
        verdict[key] = {"tau": tau, "first_w": first_w, "first_p": first_p, "holds": holds}
        fmt = (lambda x: f"{x:.1f} y") if key == "uw" else (
            (lambda x: f"{x:+.1%}") if up else (lambda x: f"{x:.1%}"))  # fmt: skip
        out += [
            f"### {name.capitalize()}: tau {tau:.2f}, first on W {', '.join(first_w)}, first on "
            f"P {', '.join(first_p)}: **{'holds' if holds else 'does not hold'}**",
            "",
            "| Item | P | rank P | W | rank W |",
            "|---|---:|---:|---:|---:|",
        ]
        for i, a, b, x, y in zip(items, vp, rp, vw, rw, strict=True):
            out.append(f"| {i.name} | {fmt(a)} | {b} | {fmt(x)} | {y} |")
        out.append("")
    path = harness.RESEARCH / "results" / "risk-menu-2.md"
    path.write_text("\n".join(out).rstrip() + "\n")
    dump = {"items": {i.key: {**m[i.key], "share1": shares.get(i.key)} for i in items},
            "verdict": verdict}  # fmt: skip
    (harness.RESEARCH / "results" / "risk-menu-2.json").write_text(
        json.dumps(dump, indent=1) + "\n"
    )
    new = ["tsmom12 70%", "tsmom12 26%", "vt-own 26%", "vt-own 70%"]
    tag = {k: k.replace(" ", "-").replace("%", "") + "@W94" for k in new}
    if f"| {IDEA} | {tag[new[0]]} |" not in harness.TRIES.read_text():
        with harness.TRIES.open("a") as fh:
            for k in new:
                r, to = ex[k], shares[k] * run.score.turnover
                fh.write(
                    f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {tag[k]} | replication | "
                    f"train | {W[0]} | {W[1]} | {stats.sharpe(r):.2f} | "
                    f"{np.prod(1 + r) - 1:+.1%} | {l2.mdd(r):.1%} | {to:.2f} |\n"
                )
        print("logged 4 rows")
    print("\n".join(out))


def rm_expo(dec: list[tuple[date, float]], win: tuple[date, date]) -> list[tuple[date, float]]:
    """Gross exposure of the last decision on or before each calendar day of win."""
    days = [d for d, _ in dec]
    out = []
    for d in l2.cal_days(*win):
        i = rm.bisect.bisect_right(days, d) - 1
        out.append((d, dec[i][1] if i >= 0 else 0.0))
    return out


if __name__ == "__main__":
    main()
