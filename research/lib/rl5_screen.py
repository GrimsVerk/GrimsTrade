# ruff: noqa: E501
"""Run rl-5: perp inputs screened by their weekly net return spread (card in research/rl-5.md).
Train period only; the held-out year is never loaded.

    uv run python -I research/lib/rl5_screen.py --screen [--log]

Reuses rl-4's loader (`rl4_perp.load`: carry-2's three sets, decisions to the train cut). Nine
inputs per coin; for each, a third-against-third book, 10 bps a side, pooled over venues, with a
Holm correction over the nine. Without `--log` nothing is written to tries.md. The pure helpers
take arrays, for the tests.
"""

from __future__ import annotations

import fcntl
import sys
from datetime import UTC, datetime
from math import erf, sqrt
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rl4_perp  # noqa: E402
from breadth_xs import ffill, logret, roll_mean, roll_median  # noqa: E402

NEW_INPUTS = ("rev_1w", "mom_1m", "fund_30", "max_30", "log_qv")
INPUTS = rl4_perp.INPUTS + NEW_INPUTS
COST = 0.001  # 10 bps a side
LEVEL = 0.10  # family-wise
MIN_COINS = rl4_perp.MIN_COINS
RESULTS = rl4_perp.RESULTS
TRIES = RESULTS.parent / "tries.md"


# --- pure helpers ---


def extra_inputs(px: np.ndarray, fund: np.ndarray, qv: np.ndarray) -> np.ndarray:
    """[days, n, 5] inputs known at each day's close: the log return of the last 7 days, of the
    last 30 days, the mean daily funding of the last 30 days, the largest daily log return of the
    last 30 days, the log of the 30-day median dollar volume."""
    fp = ffill(px)
    with np.errstate(invalid="ignore", divide="ignore"):
        rev = logret(fp, 7, 0)
        mom = logret(fp, 30, 0)
        r1 = logret(fp, 1, 0)
        lqv = np.log(roll_median(qv, 30))
    f30 = roll_mean(fund, 30)
    mx = np.full(px.shape, np.nan)
    if px.shape[0] >= 30:
        v = np.lib.stride_tricks.sliding_window_view(np.where(np.isfinite(r1), r1, -np.inf), 30, 0)
        n = np.isfinite(v).sum(-1)
        mx[29:] = np.where(n >= 24, v.max(-1), np.nan)
    out = np.stack([rev, mom, f30, mx, lqv], axis=2)
    out[~np.isfinite(out)] = np.nan
    return out


def third_book(x: np.ndarray, ok: np.ndarray) -> np.ndarray:
    """Weights of carry-2's book on input x among the coins in `ok`: +0.5 of equity spread
    equally over the top third, -0.5 over the bottom third. Zeros if fewer than MIN_COINS."""
    w = np.zeros(len(x))
    idx = np.flatnonzero(ok & np.isfinite(x))
    if len(idx) < MIN_COINS:
        return w
    order = idx[np.argsort(x[idx], kind="mergesort")]
    n3 = max(1, round(len(idx) / 3))
    w[order[-n3:]] = 0.5 / n3
    w[order[:n3]] = -0.5 / n3
    return w


def venue_weeks(
    raw: np.ndarray, m: np.ndarray, fwd: np.ndarray, cost: float = COST
) -> tuple[np.ndarray, np.ndarray]:
    """Per decision week of one venue: the gross return of the high-minus-low book on the input
    (NaN if there is no book) and the cost of getting from last week's weights to this week's.
    raw, m, fwd: [W, n] input, cross-section mask, coming week's log total return."""
    w_n = raw.shape[0]
    gross = np.full(w_n, np.nan)
    paid = np.zeros(w_n)
    prev = np.zeros(raw.shape[1])
    for i in range(w_n):
        w = third_book(raw[i], m[i])
        paid[i] = cost * np.abs(w - prev).sum()
        if np.any(w != 0):
            gross[i] = float((w * np.nan_to_num(np.expm1(fwd[i]))).sum())
        prev = w
    return gross, paid


def pool(days: list[np.ndarray], series: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """Equal capital per venue: for each decision day, the mean over the venues that have a
    finite number that day. Returns (sorted days, pooled series)."""
    acc: dict[int, list[float]] = {}
    for d, s in zip(days, series, strict=True):
        for di, si in zip(d, s, strict=True):
            if np.isfinite(si):
                acc.setdefault(int(di), []).append(float(si))
    ds = np.array(sorted(acc), dtype=np.int64)
    return ds, np.array([float(np.mean(acc[int(d)])) for d in ds])


def tstat(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    if len(x) < 10 or x.std(ddof=1) == 0:
        return float("nan")
    return float(x.mean() / x.std(ddof=1) * np.sqrt(len(x)))


def p_two_sided(t: float) -> float:
    """The sign was picked from the same data: 2 x (1 - Phi(t)); 1 if t is not above 0."""
    if not np.isfinite(t) or t <= 0:
        return 1.0
    return float(2 * (1 - 0.5 * (1 + erf(t / sqrt(2)))))


def holm(p: list[float]) -> list[float]:
    """Holm step-down adjusted p-values (reject where adjusted < level)."""
    n = len(p)
    order = sorted(range(n), key=lambda i: p[i])
    adj = [1.0] * n
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (n - rank) * p[i]))
        adj[i] = run
    return adj


def screen(
    sets: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]],
) -> dict[str, Any]:
    """sets: label -> (day [W], m [W, n], fwd [W, n], raw [W, n, K]). The card's screen."""
    k_n = next(iter(sets.values()))[3].shape[2]
    rows: list[dict[str, Any]] = []
    for k in range(k_n):
        per = {lab: venue_weeks(raw[:, :, k], m, fwd) for lab, (_, m, fwd, raw) in sets.items()}
        days = [sets[lab][0] for lab in sets]
        d, g = pool(days, [per[lab][0] for lab in sets])
        s = 1.0 if g.mean() >= 0 else -1.0
        nets = {lab: s * per[lab][0] - per[lab][1] for lab in sets}
        d2, net = pool(days, [nets[lab] for lab in sets])
        t = tstat(net)
        turn = float(np.mean([np.nanmean(per[lab][1][1:]) / COST for lab in sets]))
        rows.append(
            {
                "sign": s,
                "weeks": len(net),
                "first": int(d2[0]),
                "last": int(d2[-1]),
                "gross": float(s * g.mean()),
                "gross_t": tstat(s * g),
                "net": float(net.mean()),
                "net_t": t,
                "p": p_two_sided(t),
                "sharpe": float(net.mean() / net.std(ddof=1) * np.sqrt(52)),
                "turnover": turn * 52,
                "venues": {lab: float(np.nanmean(v)) for lab, v in nets.items()},
                "venue_t": {lab: tstat(v) for lab, v in nets.items()},
                "series": net,
            }
        )
    adj = holm([r["p"] for r in rows])
    for r, a in zip(rows, adj, strict=True):
        r["holm"] = a
        r["venues_ahead"] = sum(v > 0 for v in r["venues"].values())
        r["pass"] = bool(a < LEVEL and r["venues_ahead"] >= 2)
    return {"rows": rows}


# --- data and report ---


def load() -> dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    import carry2

    files = {"B-out": "binance", "Bybit": "bybit", "Hyperliquid": "hyperliquid"}
    out = {}
    for lab, (v, r) in rl4_perp.load().items():
        z = np.load(carry2.derived() / f"{files[lab]}.npz")
        col = {str(s): j for j, s in enumerate(z["names"])}
        qv = z["qv"][:, [col[s] for s in v.names]]
        extra = extra_inputs(v.px, v.fund, qv)[r.day]
        out[lab] = (r.day, r.m, r.fwd, np.concatenate([r.raw, extra], axis=2))
    return out


def log_rows(res: dict[str, Any]) -> None:
    with TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        for name, r in zip(INPUTS, res["rows"], strict=True):
            eq = np.cumprod(1 + r["series"])
            mdd = float((1 - eq / np.maximum.accumulate(np.maximum(eq, 1.0))).max())
            f.write(
                f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | rl-5-screen | {name} | screen | train | "
                f"{rl4_perp._date(r['first'])} | {rl4_perp._date(r['last'])} | {r['sharpe']:.2f} | "
                f"{eq[-1] - 1:+.1%} | {mdd:.1%} | {r['turnover']:.2f} |\n"
            )


def write(res: dict[str, Any], labels: list[str]) -> Path:
    rows = res["rows"]
    L = [
        "# RL 5: perp inputs screened by weekly net return spread (train only)",
        "",
        "Script `lib/rl5_screen.py --screen`, run once (card `research/rl-5.md`). Per input and",
        "venue-week: +0.5 of equity in the top third of coins by the input, -0.5 in the bottom third;",
        "week = total return (price change minus funding), cost 10 bps on every change of weight.",
        "Pooled = mean over the venues with a book that Friday. Sign = the side that earned gross",
        "over all train weeks (picked in sample, so p is two-sided). Holm = adjusted p over the nine",
        "inputs. Pass = Holm p < 0.10 and net above 0 on at least two venues. Sharpe = pooled net",
        "weeks, annualised with sqrt(52). Turnover = sum of absolute weight changes a year.",
        "",
        "| Input | Long side | Weeks | Gross per week (t) | **Net per week (t)** | p | **Holm p** | Net Sharpe | Turnover | "
        + " | ".join(labels)
        + " | Venues > 0 | Pass |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|" + "---:|" * len(labels) + "---:|---|",
    ]
    for name, r in zip(INPUTS, rows, strict=True):
        ven = " | ".join(f"{r['venues'][lab]:+.2%} ({r['venue_t'][lab]:+.1f})" for lab in labels)
        L.append(
            f"| `{name}` | {'high' if r['sign'] > 0 else 'low'} | {r['weeks']} | {r['gross']:+.2%} ({r['gross_t']:+.1f}) "
            f"| **{r['net']:+.2%} ({r['net_t']:+.1f})** | {r['p']:.3f} | **{r['holm']:.3f}** | {r['sharpe']:.2f} "
            f"| {r['turnover']:.0f}x | {ven} | {r['venues_ahead']} | {'**yes**' if r['pass'] else 'no'} |"
        )
    passed = [n for n, r in zip(INPUTS, rows, strict=True) if r["pass"]]
    L += [
        "",
        f"Passed: {', '.join(f'`{n}`' for n in passed) if passed else '**none**'}. "
        "Bar for a book on survivors: pooled Sharpe above `ls-funding`'s 0.57 (rl-4's days).",
    ]
    path = RESULTS / "rl-5-screen.md"
    path.write_text("\n".join(L) + "\n")
    return path


def main() -> None:
    if "--screen" in sys.argv:
        sets = load()
        res = screen(sets)
        if "--log" in sys.argv:
            log_rows(res)
        print(write(res, list(sets)).read_text())


if __name__ == "__main__":
    main()
