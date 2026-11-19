"""insure-2: is trend's crash insurance cheaper than holding less per era, and outside the US?

    uv run python -I research/lib/insure2.py

Step 1 (card `cards/insure-era.md`): insure-1's card 2 controls (fixed exposure, the rule's
own positions rotated to random dates) per era, on insure-1's episodes, clusters and calm mask,
reused through `insure1` (no replay).
Step 2 (card `cards/insure-geo.md`): the same episodes, metrics and controls on non-US stock
indices (Yahoo daily closes, local currency; Ken French regional daily, US dollars), files
fetched by `fetch_insure2.py` into the data cache. Clusters anchored on the US market's falls.
Writes research/results/insure-2.md; rows of kind `insure-check` go to research/tries.md once
(`--no-log` skips them). Nothing after 2025-10-31 is parsed. Needs insure-1's setup (saved
trend-1926 runs, macro.local.json).
"""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import trend_1926 as t  # noqa: E402
import trend_tune as tt  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade.data import ETF, UNIVERSE  # noqa: E402

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
        "Rule I > 0 (sign test) | Clusters where rule S > fixed S | Rule minus holding per "
        "series-year, log pts |",
        "|---|---:|---:|---:|---:|---:|---|---:|---|---|---:|",
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
            f"{sum(fx_s)} of {len(fx_s)} | "
            f"{(rule.sum_i + rule.sum_b + rule.calm) / (11 * (hi - lo).days / 365.25):+.2f} |"
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


# --- step 2: outside the US ---

RAW = "insure-2/raw-2026-11-18"
IDEA = "insure-2"
PRIMARY_GEO = {
    "N225": "Japan", "GSPTSE": "Canada", "FTSE": "UK", "AORD": "Australia", "HSI": "HongKong",
    "GDAXI": "Germany", "STI": "Singapore", "FCHI": "France", "SSMI": "Switzerland",
    "BFX": "Belgium", "AEX": "Netherlands", "ATX": "Austria", "IBEX": "Spain",
}  # fmt: skip
WIDER_GEO = {
    "FTSEMIB.MI": "Italy", "NZ50": "NewZealand", "TA125.TA": "Israel", "KS11": "Korea",
    "TWII": "Taiwan", "BSESN": "India", "BVSP": "Brazil", "MXX": "Mexico", "KLSE": "Malaysia",
    "JKSE": "Indonesia",
}  # fmt: skip
FRENCH_GEO = {
    "Europe_3_Factors_Daily_CSV.zip": "FF-Europe",
    "Japan_3_Factors_Daily_CSV.zip": "FF-Japan",
    "Asia_Pacific_ex_Japan_3_Factors_Daily_CSV.zip": "FF-AsiaPacExJapan",
}
FRENCH_DEVX = ("Developed_ex_US_3_Factors_Daily_CSV.zip", "FF-DevExUS")
GEO_ERAS = (("before 2002", date(1900, 1, 1), date(2001, 12, 31)),
            ("2002-2025", date(2002, 1, 1), i1.LAST))  # fmt: skip


def load_yahoo(path: Path) -> tuple[list[date], np.ndarray]:
    """Daily closes (local trading day) up to LAST -> days, simple returns (first 0)."""
    res = json.loads(path.read_text())["chart"]["result"][0]
    off = int(res["meta"].get("gmtoffset") or 0)
    closes: dict[date, float] = {}
    for ts, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"], strict=True):
        if c is None or c <= 0:
            continue
        d = datetime.fromtimestamp(ts + off, UTC).date()
        if d <= i1.LAST:
            closes[d] = float(c)
    days = sorted(closes)
    px = np.array([closes[d] for d in days])
    ret = np.zeros(len(px))
    ret[1:] = px[1:] / px[:-1] - 1
    return days, ret


def load_french_region(path: Path) -> tuple[list[date], np.ndarray]:
    fac = t.parse_factors(i1._lines(path), i1.LAST)
    days = sorted(fac)
    return days, np.array([fac[d][0] for d in days])


def build_geo(name: str, days: list[date], ret: np.ndarray) -> i1.Series:
    """insure-1's Series for one index: paper series of `tsmom12`, from its first decision."""
    sym = f"I2-{name}"
    UNIVERSE[sym] = ETF  # research process only; src/ is untouched
    bars = t.bars(days, ret)
    panel = harness.Panel({sym: bars})
    p = tt.paper(panel, sym, (12,))
    bdays = [b.date for b in bars]
    close = np.array([b.close for b in bars])
    bar = simple(close)
    pos = i1.infer_pos(p.ret[12], bar, COST)
    k = max(int(np.argmax(p.ok)) - 1, 0)  # session before the first one the rule may hold
    paper = p.ret[12][k:].copy()
    paper[0] = 0.0
    px = close[k:] / close[k]
    return i1.Series(name, bdays[k:], px, paper.copy(), paper, pos[k:], np.zeros(len(px)), 0.0)


def anchored(us: Sequence[i1.Episode], eps: Sequence[i1.Episode]) -> list[list[i1.Episode]]:
    """insure-1's market-anchored clusters with the US market's falls as anchors; a cluster
    holds non-US episodes only (the US episode is the label); empty anchors are dropped."""
    groups: list[tuple[i1.Episode, list[i1.Episode]]] = [(u, []) for u in us]
    rest = []
    for e in eps:
        home = next((g for u, g in groups if u.peak <= e.trough <= u.trough), None)
        if home is None:
            home = next((g for u, g in groups if u.peak <= e.peak <= u.trough), None)
        if home is None:
            rest.append(e)
        else:
            home.append(e)
    out = [g for _, g in groups if g] + i1.link(rest)
    return sorted(out, key=lambda g: min(x.peak for x in g))


def geo_tables(
    title: str, series: list[i1.Series], us: Sequence[i1.Episode], controls: bool
) -> tuple[list[str], str, str]:
    """Card 1's tables, the premium, and (optionally) card 2's controls for one set."""
    sc = [i1.score(s, *i1.PRIMARY) for s in series]
    eps = [e for x in sc for e in x.eps]
    anch, lnk = anchored(us, eps), i1.link(eps)
    out = [f"### {title}", ""]
    out += [
        "| Series | First decision | Sessions | Mean position | Episodes | Open fall (peak) | "
        "Sum I | Sum B | C | Premium P | Worst loss rule / hold |",
        "|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|",
    ]

    def prem(si: float, sb: float, c: float) -> str:
        return f"{-(sb + c) / si:.2f}" if si > 0 else "no insurance"

    for x in sc:
        si, sb = sum(e.ins for e in x.eps), sum(e.rebound for e in x.eps)
        out.append(
            f"| {x.s.name} | {x.s.days[1]} | {len(x.s.days)} | {x.s.pos[1:].mean():.0%} | "
            f"{len(x.eps)} | {x.open_peak or '-'} | {si:+.0f} | {sb:+.0f} | {x.calm:+.0f} | "
            f"{prem(si, sb, x.calm)} | {i1.maxdd(np.cumprod(1 + x.s.rule)):.0%} / "
            f"{i1.maxdd(x.s.px):.0%} |"
        )
    si, sb, c = (sum(e.ins for e in eps), sum(e.rebound for e in eps), sum(x.calm for x in sc))
    p_all = prem(si, sb, c)
    out += [f"| **pooled** | | | | {len(eps)} | | {si:+.0f} | {sb:+.0f} | {c:+.0f} | "
            f"**{p_all}** | |", ""]  # fmt: skip
    # eras: episodes by peak, calm by date
    era_bits = []
    for key, lo, hi in GEO_ERAS:
        ee = [e for e in eps if lo <= e.peak <= hi]
        cc = 0.0
        for x in sc:
            d = 100 * (np.log1p(x.s.rule) - logret(x.s.px))
            d[0] = 0.0
            m = np.array([lo <= dd <= hi for dd in x.s.days]) & ~x.in_mask
            cc += float(d[m].sum())
        a, b = sum(e.ins for e in ee), sum(e.rebound for e in ee)
        yrs = sum(max(0, (min(hi, x.s.days[-1]) - max(lo, x.s.days[0])).days) / 365.25 for x in sc)
        per_yr = (a + b + cc) / yrs if yrs else 0.0
        era_bits.append(
            f"{key} {prem(a, b, cc)} ({len(ee)} episodes; rule minus holding "
            f"{per_yr:+.2f} log pts per series-year)"
        )
    out += ["Premium by era (episodes by peak, calm by date): " + "; ".join(era_bits) + ".", ""]
    a_i = i1.test_line("I, anchored on US falls", anch, lambda e: e.ins)
    l_i = i1.test_line("I, linked (strict)", lnk, lambda e: e.ins)
    a_n = i1.test_line("N = I + B, anchored", anch, lambda e: e.net)
    v1 = i1.verdict(a_i, l_i, a_n)
    out += i1.TEST_HEAD + [
        a_i,
        l_i,
        a_n,
        i1.test_line("N = I + B, linked", lnk, lambda e: e.net),
        i1.test_line("Share avoided S, anchored", anch, lambda e: e.share),
        "",
        f"Episodes {len(eps)}; anchored clusters (effective episodes) {len(anch)}; linked "
        f"{len(lnk)}. Verdict by card 1's rule: **{v1}**.",
        "",
    ]
    # speed
    out += ["| Peak to trough | Episodes | Mean depth | Mean I | I > 0 | Mean S | Mean N | N > 0 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    for label, lo_d, hi_d in (("fast, <= 92 days", 0, i1.FAST),
                              ("medium, 93-365", i1.FAST + 1, i1.MEDIUM),
                              ("slow, > 365", i1.MEDIUM + 1, 10**6)):  # fmt: skip
        ee = [e for e in eps if lo_d <= e.days <= hi_d]
        if not ee:
            out.append(f"| {label} | 0 | | | | | | |")
            continue
        out.append(
            f"| {label} | {len(ee)} | {i1.cmean(ee, lambda e: e.depth):.0%} | "
            f"{i1.cmean(ee, lambda e: e.ins):+.1f} | {sum(e.ins > 0 for e in ee)} | "
            f"{i1.cmean(ee, lambda e: e.share):+.2f} | {i1.cmean(ee, lambda e: e.net):+.1f} | "
            f"{sum(e.net > 0 for e in ee)} |"
        )
    out.append("")
    # sensitivity
    sens = []
    for down, up in i1.SENS:
        ss = [i1.score(s, down, up) for s in series]
        ee = [e for x in ss for e in x.eps]
        us_s = us_market_eps(down, up)
        g = anchored(us_s, ee)
        k_i, n_i, p_i = i1.sign_test([i1.cmean(x, lambda e: e.ins) for x in g])
        net_m = float(np.mean([i1.cmean(x, lambda e: e.net) for x in g]))
        pp = prem(sum(e.ins for e in ee), sum(e.rebound for e in ee), sum(x.calm for x in ss))
        sens.append(f"{down:.0%} falls: {len(g)} clusters, I > 0 in {k_i} of {n_i} (p {p_i:.2g}), "
                    f"mean N {net_m:+.1f}, premium {pp}")  # fmt: skip
    out += ["Sensitivity (anchored): " + "; ".join(sens) + ".", ""]
    v2 = "-"
    if controls:
        ctl, v2 = geo_controls(series, sc, anch)
        out += ctl
    clus = ["| # | First peak | Last trough | Non-US episodes | Mean depth | Mean I | Mean S | "
            "Mean N | Series |", "|---:|---|---|---:|---:|---:|---:|---:|---|"]  # fmt: skip
    for i, g in enumerate(anch):
        names = ", ".join(sorted({e.series for e in g}))
        clus.append(
            f"| {i + 1} | {min(e.peak for e in g)} | {max(e.trough for e in g)} | {len(g)} | "
            f"{i1.cmean(g, lambda e: e.depth):.0%} | {i1.cmean(g, lambda e: e.ins):+.0f} | "
            f"{i1.cmean(g, lambda e: e.share):+.2f} | {i1.cmean(g, lambda e: e.net):+.0f} | "
            f"{names} |"
        )
    out += ["Anchored clusters:", "", *clus, ""]
    return out, v1, v2


def geo_controls(
    series: list[i1.Series], sc: list[i1.Scored], anch: list[list[i1.Episode]]
) -> tuple[list[str], str]:
    eps = [x.eps for x in sc]
    clusters = [[(0, e) for e in g] for g in anch]
    hl = [logret(s.px) for s in series]
    bar = [simple(s.px) for s in series]
    rule = i1.control_stats([s.paper for s in series], hl, eps, clusters)
    xs = [float(s.pos[1:].mean()) for s in series]
    fixed = i1.control_stats([x * b for x, b in zip(xs, bar, strict=True)], hl, eps, clusters)
    ords = [np.array([d.toordinal() for d in s.days]) for s in series]
    span = min(int(o[-1] - o[0]) + 1 for o in ords)
    rng = np.random.default_rng(i1.SEED)
    rots = []
    for _ in range(ROTATIONS):
        dd = int(rng.integers(365, span - 365))
        rr = []
        for s, b, o in zip(series, bar, ords, strict=True):
            f, n_days = int(o[0]), int(o[-1] - o[0]) + 1
            shifted = f + np.mod(o - dd - f, n_days)
            idx = np.searchsorted(o, shifted, side="right") - 1
            p = s.pos[idx]
            flips = np.abs(np.diff(p, prepend=p[0]))
            r = p * b - COST * flips
            r[0] = 0.0
            rr.append(r)
        rots.append(i1.control_stats(rr, hl, eps, clusters))
    rs = np.array([c.s_mean for c in rots])
    rn = np.array([c.n_mean for c in rots])
    rp = np.array([c.prem for c in rots])
    p_s = float((rs >= rule.s_mean).mean())
    p_p = float((rp <= rule.prem).mean())
    p_n = float((rn >= rule.n_mean).mean())
    if p_s < 0.05 and p_p < 0.05 and rule.prem < fixed.prem:
        v = "Timing, not just exposure"
    elif p_s >= 0.10 and p_p >= 0.10:
        v = "Exposure, not timing"
    else:
        v = "In between"
    out = [
        "Card 2's controls (rotations by one common calendar offset, 1,000, median and 5-95%):",
        "",
        "| | Mean cluster S | Mean cluster N | Pooled premium P |",
        "|---|---:|---:|---:|",
        f"| `tsmom12` | {rule.s_mean:+.2f} | {rule.n_mean:+.1f} | {rule.prem:.2f} |",
        f"| Fixed exposure (mean x {np.mean(xs):.0%}) | {fixed.s_mean:+.2f} | "
        f"{fixed.n_mean:+.1f} | {fixed.prem:.2f} |",
        f"| Random timing | {q(rs)} | {q(rn, '+.1f')} | {q(rp)} |",
        f"| p: rotations at least as good | {p_s:.3f} | {p_n:.3f} | {p_p:.3f} |",
        "",
        f"Verdict by card 2's rule: **{v}**.",
        "",
    ]
    return out, v


_US: dict[tuple[float, float], list[i1.Episode]] = {}
_US_SERIES: list[i1.Series] = []


def us_market_eps(down: float, up: float) -> list[i1.Episode]:
    """The US market's (French daily market) episodes at a threshold: the anchors."""
    if (down, up) not in _US:
        _US[(down, up)] = i1.score(_US_SERIES[0], down, up).eps
    return _US[(down, up)]


def geo_section(us_market: i1.Series) -> tuple[str, list[i1.Series]]:
    _US_SERIES[:] = [us_market]
    root = cache_root() / RAW
    prim = [build_geo(n, *load_yahoo(root / "yahoo" / f"{tk}.json"))
            for tk, n in PRIMARY_GEO.items()]  # fmt: skip
    wide = [build_geo(n, *load_yahoo(root / "yahoo" / f"{tk}.json"))
            for tk, n in WIDER_GEO.items()]  # fmt: skip
    ff = [build_geo(n, *load_french_region(root / "french" / f)) for f, n in FRENCH_GEO.items()]
    devx = build_geo(FRENCH_DEVX[1], *load_french_region(root / "french" / FRENCH_DEVX[0]))
    us = us_market_eps(*i1.PRIMARY)
    out = [
        "## Step 2, insure-geo: outside the US",
        "",
        "Card: `cards/insure-geo.md`. `tsmom12` paper series (Friday decisions, 12-month "
        "lookback, 2 bps a side, cash at 0) on each index's closes, from its first decision to "
        "2025-10-31; insure-1's 25% / 25% episodes and metrics. Clusters anchored on the US "
        "market's 25% falls (French daily market); a cluster's value is the mean over its "
        "non-US episodes. Yahoo indices: price indices in local currency (DAX: total return); "
        "French regions: total return in US dollars.",
        "",
    ]
    t1, v1, v2 = geo_tables("Primary: 13 developed markets (Yahoo)", prim, us, True)
    t2, w1, w2 = geo_tables("Total-return check: French regions (USD)", ff, us, True)
    t3, x1, x2 = geo_tables("Wider set: 10 more indices (Yahoo)", wide, us, True)
    t4, y1, _ = geo_tables("Developed ex US as one series (French, USD)", [devx], us, False)
    out += t1 + t2 + t3 + t4
    out += [
        "### Verdicts",
        "",
        "| Set | Card 1 rule (insurance) | Card 2 rule (cheaper than holding less) |",
        "|---|---|---|",
        f"| Primary, 13 developed (decides) | {v1} | {v2} |",
        f"| French regions, total return | {w1} | {w2} |",
        f"| Wider set, 10 | {x1} | {x2} |",
        f"| Developed ex US, one series | {y1} | - |",
        "",
    ]
    return "\n".join(out) + "\n", prim + ff + wide + [devx]


def log_geo_tries(series: Sequence[i1.Series]) -> int:
    text = harness.TRIES.read_text()
    rows = []
    for s in series:
        v = f"tsmom12@insure-geo-{s.name}"
        if f"| {IDEA} | {v} |" in text:
            continue
        sh, tot, mdd, fl = i1.sharpe_row(s)
        rows.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | insure-check | train | "
            f"{s.days[0]} | {s.days[-1]} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(rows)
    return len(rows)


def main() -> None:
    primary = i1.load_primary()
    sec1, _ = era_section(primary)
    sec2, geo = geo_section(primary[0])
    head = [
        "# insure-2: crash insurance of `tsmom12` per era and outside the US",
        "",
        "Written by `lib/insure2.py`. Log points = 100 x natural log; every number is rule minus "
        "holding unless said otherwise. Cash earns 0.",
        "",
    ]
    OUT.write_text("\n".join(head) + "\n" + sec1 + "\n" + sec2)
    n = 0 if "--no-log" in sys.argv else log_geo_tries(geo)
    print(f"wrote {OUT}; {n} new tries.md rows")


if __name__ == "__main__":
    main()
