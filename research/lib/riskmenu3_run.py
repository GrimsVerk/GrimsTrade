"""risk-menu-3: own-vol targeting with an expanding-window k (no look-ahead), and the dates of
each item's longest under-water spell on 1994-2025 (descriptive, no pick).
Card: research/cards/risk-menu-3.md.

    uv run python -I research/lib/riskmenu3_run.py

Builds risk-menu-2's items 1-7 on W = 1994-02-01..2025-10-31 (same definitions) plus own-vol
targeting whose k on each 1st uses only the sigmas known then. Compares with the re-fitted
version on W (`results/risk-menu-2.json`) and on P (`results/risk-menu.json`). Appends the card's
2 replication rows (first run only), writes `research/results/risk-menu-3.md` (+ `.json`). No day
after 2025-10-31 is read.
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
import riskmenu2_run as r2  # noqa: E402
import riskmenu_run as rm  # noqa: E402
import stats  # noqa: E402

IDEA = "risk-menu-3"
W = r2.W
P = rm.P
WARMUP = 24  # monthly sigmas before k is solved from the expanding window (card)


def solve_k(sig: list[float], target: float) -> float:
    """k with mean(min(1, k / sigma)) = target over the given positive sigmas."""
    s = np.array(sig)
    lo, hi = 0.0, 10.0
    for _ in range(60):
        k = (lo + hi) / 2
        lo, hi = (k, hi) if np.minimum(1.0, k / s).mean() < target else (lo, k)
    return (lo + hi) / 2


def vt_expanding(
    s1: l2.Sleeve, target: float, held: rm.Callable[[date], int]
) -> tuple[rm.Mix, dict[date, float]]:
    """Own-vol target, k_d from the sigmas of months <= d only; fixed T during the warm-up."""
    seen: list[float] = []
    ks: dict[date, float] = {}
    plan: dict[date, float | None] = {}  # None: keep the drifted share (sigma 0)
    for d in rm.months_in(*W):
        sg = s1.sigma(d - timedelta(days=1))
        if math.isfinite(sg) and sg > 0:
            seen.append(sg)
        if len(seen) < WARMUP or not math.isfinite(sg):
            plan[d] = target
        elif sg == 0:
            plan[d] = None
        else:
            ks[d] = solve_k(seen, target)
            plan[d] = min(1.0, ks[d] / sg)

    def tgt(d: date, v: float) -> tuple[float, float]:
        a = plan[d]
        return (v if a is None else a, 0.0)

    return rm.mix(s1, None, tgt, W[0], held), ks


def measures(e: np.ndarray, rf: np.ndarray, a: date) -> dict[str, float | str]:
    tot = e + rf
    eq = np.concatenate([[1.0], np.cumprod(1 + tot)])
    return {
        "sharpe": stats.sharpe(e), "se": stats.sharpe_se(e), "cagr": stats.cagr(tot),
        "vol": stats.vol(tot), "mdd": l2.mdd(tot), "w12": rm.worst_12m(eq),
        "uw": rm.underwater_years(eq), **underwater_spell(eq, a),
    }  # fmt: skip


def underwater_spell(eq: np.ndarray, a: date) -> dict[str, float | str]:
    """Longest run of days below the running high (as `underwater_years`): its high, low, end.
    eq[k] is the value after day a + k - 1 (eq[0] the start, dated a - 1)."""
    peak = np.maximum.accumulate(eq)
    below = eq < peak * (1 - 1e-12)
    best = (0, 0)  # (length, first index below)
    cur, st = 0, 0
    for k, b in enumerate(below):
        if b:
            if cur == 0:
                st = k
            cur += 1
            if cur > best[0]:
                best = (cur, st)
        else:
            cur = 0
    n, st = best
    if n == 0:
        return {"uw_high": "-", "uw_low": "-", "uw_back": "-"}
    day = lambda k: str(a + timedelta(days=k - 1))  # noqa: E731
    low = st + int(np.argmin(eq[st : st + n]))
    back = st + n
    return {
        "uw_high": day(st - 1), "uw_low": day(low),
        "uw_back": day(back) if back < len(eq) else f"not back by {W[1]}",
    }  # fmt: skip


def main() -> None:
    s1, rf1, _drag, run = l2.tsmom12_sleeve()
    six = c.ctx("six")
    held = rm.held_count(run)
    days, ylds = rm.ci.bill_yield()
    series: dict[str, tuple[str, dict[date, float]]] = {}
    for key, name, f in (("hold six", "Hold the six (equal weight)", c.equal_weight),
                         ("60/40", "60/40 (SPY / TLT)", c.sixty_forty)):  # fmt: skip
        r = c.go(IDEA, key, c.weekly(f), six, "baseline", log=False)  # re-score, logged config
        rr, rf = rm.ci.rescored(r, days, ylds)
        series[key] = (name, {d: float(x - y) for d, x, y in zip(r.days[1:], rr, rf, strict=True)})
    series["tsmom12"] = ("`tsmom12`, full size", s1.ex)
    shares: dict[str, float] = {}
    for sh in (0.70, 0.26):
        mx = rm.mix(s1, None, lambda d, v, sh=sh: (sh, 0.0), W[0], held)
        series[f"tsmom12 {sh:.0%}"] = (f"`tsmom12` {sh:.0%} + T-bills", mx.ex)
    kinfo: dict[str, dict[str, float | str]] = {}
    for sh in (0.26, 0.70):
        mx = r2.vt_target_w(s1, sh, held)
        series[f"vt-own {sh:.0%}"] = (f"Own-vol target {sh:.0%}, k re-fitted on W", mx.ex)
        mx, ks = vt_expanding(s1, sh, held)
        key = f"vt-own {sh:.0%} x"
        series[key] = (f"Own-vol target {sh:.0%}, expanding k (no look-ahead)", mx.ex)
        for nm, win in (("W", W), ("P", P)):
            shares[f"{key} {nm}"] = float(np.mean([mx.share1[d] for d in l2.cal_days(*win)]))
        kv = list(ks.values())
        kinfo[key] = {"first_k": str(min(ks)), "k_min": min(kv), "k_max": max(kv), "k_last": kv[-1]}

    m: dict[str, dict[str, dict[str, float | str]]] = {"W": {}, "P": {}}
    for nm, (a, b) in (("W", W), ("P", P)):
        rf_ = l2.on_cal(rf1, a, b)
        for key, (_n, ex) in series.items():
            m[nm][key] = measures(l2.on_cal(ex, a, b), rf_, a)
    ref = {
        "W": json.loads((harness.RESEARCH / "results" / "risk-menu-2.json").read_text())["items"],
        "P": json.loads((harness.RESEARCH / "results" / "risk-menu.json").read_text()),
    }

    def f(x: float | str) -> float:
        return float(x)

    out = [
        "# risk-menu-3: own-vol targeting without look-ahead; under-water dates (descriptive)",
        "",
        "Card: `cards/risk-menu-3.md` (committed before any number). Footing as risk-menu-2: "
        "daily calendar returns, gym costs, 5 bps per monthly reset, idle cash at the 13-week "
        "T-bill; Sharpe on excess returns (365-day convention), other measures on the "
        f"total-return curve. W = {W[0]}..{W[1]}, P = {P[0]}..{P[1]} (the W-built series cut to "
        f"P). Expanding k: on each 1st, k solves mean(min(1, k / sigma_m)) = T over all monthly "
        f"sigmas known by then; share T for the first {WARMUP} sigmas (warm-up). Nothing after "
        f"{W[1]} read.",
        "",
        "## 1. Expanding k against the re-fitted k",
        "",
        "Re-fitted = risk-menu-2's numbers on W, risk-menu's on P (k solved on that window). "
        "This run's re-fitted W row is shown as a check against risk-menu-2.",
        "",
        "| Window | Item | Sharpe (SE) | Growth/yr | Vol | Worst loss | Worst 12 months | Longest "
        "under water | Mean share |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    delta: dict[str, dict[str, float]] = {}
    for nm in ("W", "P"):
        for sh in ("26%", "70%"):
            rk, xk = f"vt-own {sh}", f"vt-own {sh} x"
            q0, q1 = ref[nm][rk], m[nm][xk]
            rows = ((f"Own-vol {sh}, re-fitted k", q0, q0.get("share1")),
                    (f"Own-vol {sh}, expanding k", q1, shares[f"{xk} {nm}"]))  # fmt: skip
            for lab, q, s in rows:
                out.append(
                    f"| {nm} | {lab} | {f(q['sharpe']):.2f} ({f(q['se']):.2f}) | "
                    f"{f(q['cagr']):.1%} | {f(q['vol']):.1%} | {f(q['mdd']):.1%} | "
                    f"{f(q['w12']):+.1%} | {f(q['uw']):.1f} y | {f(s):.2f} |"
                )
            delta[f"{nm} {sh}"] = {
                k: f(q1[k]) - f(q0[k]) for k in ("sharpe", "cagr", "mdd", "w12", "uw")
            }
        for k_ in ("tsmom12", "tsmom12 26%", "tsmom12 70%"):
            q = m[nm][k_]
            out.append(
                f"| {nm} | {series[k_][0]} (context) | {f(q['sharpe']):.2f} ({f(q['se']):.2f}) | "
                f"{f(q['cagr']):.1%} | {f(q['vol']):.1%} | {f(q['mdd']):.1%} | "
                f"{f(q['w12']):+.1%} | {f(q['uw']):.1f} y | - |"
            )
    out += [
        "",
        "| Change, expanding minus re-fitted | Sharpe | Growth/yr | Worst loss | Worst 12 months "
        "| Under water |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for k_, dv in delta.items():
        out.append(
            f"| {k_} | {dv['sharpe']:+.2f} | {dv['cagr'] * 100:+.1f} pt | "
            f"{dv['mdd'] * 100:+.1f} pt | {dv['w12'] * 100:+.1f} pt | {dv['uw']:+.1f} y |"
        )
    chk = {sh: f(m["W"][f"vt-own {sh}"]["sharpe"]) - f(ref["W"][f"vt-own {sh}"]["sharpe"])
           for sh in ("26%", "70%")}  # fmt: skip
    out += [
        "",
        f"Check: this run's re-fitted W Sharpe minus risk-menu-2's: 26% {chk['26%']:+.3f}, "
        f"70% {chk['70%']:+.3f}.",
        "",
        "k (annual vol units; share = min(1, k / sigma52)):",
        "",
    ]
    for k_, ki in kinfo.items():
        out.append(
            f"- {k_}: first solved {ki['first_k']}, range {f(ki['k_min']):.3f}..."
            f"{f(ki['k_max']):.3f}, last {f(ki['k_last']):.3f}"
        )
    out += [
        "",
        f"## 2. Longest spell under water on W ({W[0]}..{W[1]})",
        "",
        "High = the last day at the old high before the spell; low = the spell's lowest day; "
        "back = the first day at or above the old high again. Calendar days: bills accrue on "
        "weekends and holidays, so a high can fall on one (2000-03-26 is the Sunday after the "
        "Friday 2000-03-24 close).",
        "",
        "| Item | Years | High | Low | Back |",
        "|---|---:|---|---|---|",
    ]
    for key, (name, _ex) in series.items():
        q = m["W"][key]
        out.append(
            f"| {name} | {f(q['uw']):.1f} | {q['uw_high']} | {q['uw_low']} | {q['uw_back']} |"
        )
    path = harness.RESEARCH / "results" / "risk-menu-3.md"
    path.write_text("\n".join(out).rstrip() + "\n")
    dump = {"measures": m, "delta": delta, "shares": shares, "k": kinfo}
    (harness.RESEARCH / "results" / "risk-menu-3.json").write_text(
        json.dumps(dump, indent=1) + "\n"
    )
    new = ["vt-own 26% x", "vt-own 70% x"]
    tag = {k: k.replace(" x", "-x").replace(" ", "-").replace("%", "") + "@W94" for k in new}
    if f"| {IDEA} | {tag[new[0]]} |" not in harness.TRIES.read_text():
        with harness.TRIES.open("a") as fh:
            for k in new:
                r = l2.on_cal(series[k][1], *W)
                to = shares[f"{k} W"] * run.score.turnover
                fh.write(
                    f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {tag[k]} | replication | "
                    f"train | {W[0]} | {W[1]} | {stats.sharpe(r):.2f} | "
                    f"{np.prod(1 + r) - 1:+.1%} | {l2.mdd(r):.1%} | {to:.2f} |\n"
                )
        print("logged 2 rows")
    print("\n".join(out))


if __name__ == "__main__":
    main()
