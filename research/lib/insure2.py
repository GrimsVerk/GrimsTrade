"""insure-2: is trend's crash insurance cheaper than holding less per era, and outside the US?

    uv run python -I research/lib/insure2.py

Step 1 (card `cards/insure-era.md`): insure-1's card 2 controls (fixed exposure, the rule's
own positions rotated to random dates) per era, on insure-1's episodes, clusters and calm mask,
reused through `insure1` (no replay). Writes research/results/insure-2.md. Nothing after
2025-10-31 is parsed. Needs insure-1's setup (saved trend-1926 runs, macro.local.json).
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import trend_1926 as t  # noqa: E402

OUT = harness.RESEARCH / "results" / "insure-2.md"
COST = 0.0002
ROTATIONS = 1000
MIN_SIGN = 10  # no sign test on fewer clusters
WINDOWS = (
    ("1927-1961", date(1927, 7, 2), date(1961, 12, 31)),
    ("1962-2001", date(1962, 1, 1), date(2001, 12, 31)),
    ("2002-2025", date(2002, 1, 1), i1.LAST),
    ("1962-2025", date(1962, 1, 1), i1.LAST),
)


@dataclass
class Stat:
    s_mean: float  # mean over the window's clusters of the share avoided S
    n_mean: float  # mean over the window's clusters of N
    prem: float  # pooled premium P over the window
    sum_i: float
    sum_b: float
    calm: float
    s_vals: list[float]


def logret(px: np.ndarray) -> np.ndarray:
    h = np.zeros(len(px))
    h[1:] = np.log(px[1:] / px[:-1])
    return h


def simple(px: np.ndarray) -> np.ndarray:
    b = np.zeros(len(px))
    b[1:] = px[1:] / px[:-1] - 1
    return b


def window_stats(
    rets: Sequence[np.ndarray],
    hl: Sequence[np.ndarray],
    eps: Sequence[Sequence[i1.Episode]],
    calm_sel: Sequence[np.ndarray],
    clusters: Sequence[Sequence[i1.Episode]],
    lo: date,
    hi: date,
) -> Stat:
    """Rule-minus-holding stats of one set of return series on one window's episodes."""
    ins: dict[int, float] = {}
    net: dict[int, float] = {}
    sum_i = sum_b = calm = 0.0
    for r, h, ee, cs in zip(rets, hl, eps, calm_sel, strict=True):
        d = 100 * (np.log1p(r) - h)
        d[0] = 0.0
        cum = np.cumsum(d)
        calm += float(d[cs].sum())
        for e in ee:
            a, b, x = e.idx
            ins[id(e)] = float(cum[b] - cum[a])
            net[id(e)] = float(cum[x] - cum[a])
            if lo <= e.peak <= hi:  # the window's own episodes; others only fill clusters
                sum_i += ins[id(e)]
                sum_b += float(cum[x] - cum[b])
    s_vals = [np.mean([ins[id(e)] / abs(e.hold) for e in g]) for g in clusters]
    n_vals = [np.mean([net[id(e)] for e in g]) for g in clusters]
    prem = -(sum_b + calm) / sum_i if sum_i > 0 else np.inf
    return Stat(float(np.mean(s_vals)), float(np.mean(n_vals)), float(prem), sum_i, sum_b, calm,
                [float(v) for v in s_vals])  # fmt: skip


def q(a: np.ndarray, fmt: str = "+.2f") -> str:
    lo, mid, hi = np.quantile(a, [0.05, 0.5, 0.95])
    return f"{mid:{fmt}} ({lo:{fmt}} to {hi:{fmt}})"


def era_section(primary: list[i1.Series]) -> tuple[str, dict[str, str]]:
    if any(s.days != primary[0].days for s in primary):
        raise ValueError("needs one session calendar for the 11 series")
    sc = [i1.score(s, *i1.PRIMARY) for s in primary]
    anch = i1.market_anchored([e for x in sc for e in x.eps], t.MKT)
    hl = [logret(s.px) for s in primary]
    bar = [simple(s.px) for s in primary]
    ords = np.array([d.toordinal() for d in primary[0].days])
    x_full = [float(s.pos[1:].mean()) for s in primary]
    out = [
        "## Step 1, insure-era: card 2's controls per era",
        "",
        "Card: `cards/insure-era.md`. Same 11 series, insure-1's 25% episodes, market-anchored "
        "clusters and calm mask, cash at 0, the rule as its paper series. Episodes by peak, "
        "clusters by first peak, calm by date. Fixed exposure: x = the rule's mean position in "
        "the window (whole-span x as second reading). Rotations: the 11-series block of the "
        "rule's positions rotated within the window, 1,000 per window, median (5-95%). p = share "
        "of rotations at least as good as the rule.",
        "",
        "| Window | Clusters | Episodes | Rule S | Fixed S | Rotations S | p (S) | Rule P | "
        "Fixed P | Fixed P (whole-span x) | Rotations P | p (P) | Mean x | Verdict |",
        "|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|",
    ]
    detail = [
        "",
        "Detail per window: the rule's sums (log points, paper series), the net N, and a sign "
        f"test of the rule's cluster I (only with at least {MIN_SIGN} clusters).",
        "",
        "| Window | Sum I | Sum B | C | Rule N | Fixed N | Rotations N | p (N) | "
        "Rule I > 0 (sign test) | Clusters where rule S > fixed S |",
        "|---|---:|---:|---:|---:|---:|---|---:|---|---|",
    ]
    verdicts: dict[str, str] = {}
    for key, lo, hi in WINDOWS:
        lo_o, hi_o = lo.toordinal(), hi.toordinal()
        in_win = (ords >= lo_o) & (ords <= hi_o)
        own = [[e for e in x.eps if lo <= e.peak <= hi] for x in sc]
        eps = [x.eps for x in sc]
        clusters = [g for g in anch if lo <= min(e.peak for e in g) <= hi]
        calm_sel = [in_win & ~x.in_mask for x in sc]
        a0 = int(np.argmax(in_win))
        ends = [e.idx[2] for ee in own for e in ee] + [e.idx[2] for g in clusters for e in g]
        a1 = max([int(np.nonzero(in_win)[0][-1]), *ends])
        rule = window_stats([s.paper for s in primary], hl, eps, calm_sel, clusters, lo, hi)
        xs = [float(s.pos[in_win].mean()) for s in primary]
        fixed = window_stats([x * b for x, b in zip(xs, bar, strict=True)], hl, eps, calm_sel,
                             clusters, lo, hi)  # fmt: skip
        fixed_full = window_stats(
            [x * b for x, b in zip(x_full, bar, strict=True)], hl, eps, calm_sel, clusters, lo, hi
        )
        n = a1 - a0 + 1
        rng = np.random.default_rng(i1.SEED)
        rots = []
        for _ in range(ROTATIONS):
            k = int(rng.integers(365, n - 365))
            rr = []
            for s, b in zip(primary, bar, strict=True):
                p = s.pos.copy()
                p[a0 : a1 + 1] = np.roll(s.pos[a0 : a1 + 1], k)
                flips = np.abs(np.diff(p, prepend=p[0]))
                r = p * b - COST * flips
                r[0] = 0.0
                rr.append(r)
            rots.append(window_stats(rr, hl, eps, calm_sel, clusters, lo, hi))
        rs = np.array([c.s_mean for c in rots])
        rp = np.array([c.prem for c in rots])
        rn = np.array([c.n_mean for c in rots])
        p_s = float((rs >= rule.s_mean).mean())
        p_p = float((rp <= rule.prem).mean())
        p_n = float((rn >= rule.n_mean).mean())
        if p_s < 0.05 and p_p < 0.05 and rule.prem < fixed.prem:
            v = "Timing, not just exposure"
        elif p_s >= 0.10 and p_p >= 0.10:
            v = "Exposure, not timing"
        else:
            v = "In between"
        verdicts[key] = v
        n_eps = sum(len(ee) for ee in own)
        out.append(
            f"| {key} | {len(clusters)} | {n_eps} | {rule.s_mean:.2f} | {fixed.s_mean:.2f} | "
            f"{q(rs)} | {p_s:.3f} | {rule.prem:.2f} | {fixed.prem:.2f} | {fixed_full.prem:.2f} | "
            f"{q(rp)} | {p_p:.3f} | {np.mean(xs):.0%} | {v} |"
        )
        ci = [float(np.mean([e.ins for e in g])) for g in clusters]
        if len(clusters) >= MIN_SIGN:
            k_, n_, p_ = i1.sign_test(ci)
            sign = f"{k_} of {n_} (p {p_:.2g})"
        else:
            sign = f"{sum(c > 0 for c in ci)} of {len(ci)} (no test)"
        fx_s = [a > b for a, b in zip(rule.s_vals, fixed.s_vals, strict=True)]
        detail.append(
            f"| {key} | {rule.sum_i:+.0f} | {rule.sum_b:+.0f} | {rule.calm:+.0f} | "
            f"{rule.n_mean:+.1f} | {fixed.n_mean:+.1f} | {q(rn, '+.1f')} | {p_n:.3f} | {sign} | "
            f"{sum(fx_s)} of {len(fx_s)} |"
        )
    head = verdicts["1962-2025"]
    ans = {"Timing, not just exposure": "Yes", "In between": "Partly"}.get(head, "No")
    out += detail + [
        "",
        "Fixed exposure's S is about 1 - x in every episode (it holds x of each fall); the "
        "last column counts clusters where the rule's S beats it.",
        "",
        f"**Headline by the card (1962-2025 window): {head} -> {ans}.** Per era: "
        + "; ".join(f"{k} {v}" for k, v in verdicts.items() if k != "1962-2025")
        + ".",
        "",
    ]
    return "\n".join(out) + "\n", verdicts


def main() -> None:
    primary = i1.load_primary()
    sec1, _ = era_section(primary)
    head = [
        "# insure-2: crash insurance of `tsmom12` per era and outside the US",
        "",
        "Written by `lib/insure2.py`. Log points = 100 x natural log; every number is rule minus "
        "holding unless said otherwise. Cash earns 0.",
        "",
    ]
    OUT.write_text("\n".join(head) + "\n" + sec1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
