"""bear-legs: multi-leg bear markets, and can a bear-market rally be told from the bottom at the
time? Card: research/cards/bear-legs.md. Descriptive, no pick, no tries.md rows.

    uv run python -I research/lib/bearlegs.py

Step 1 catalogues the rallies inside insure-1/insure-2's 25% falls (US market + 10 industries,
1927-2025; 13 developed non-US price indices) and what the 3- and 12-month signals and the
three rules (`tsmom12`, `or3-12`, `arm3-12`, fast-reentry-2's paper series) did in them. Step 2
scores eight observables, known at the event close, on two real-time event sets (rally off the
low; 3-month re-entry moment): AUC for bottom vs bear rally, cluster bootstrap, and a stationary
block-bootstrap placebo. Writes research/results/bear-legs.md. Needs insure-2's setup (saved
trend-1926 runs, macro.local.json, insure-2's data cache). Nothing after 2025-10-31 is parsed.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastreentry as fr  # noqa: E402
import fastreentry2 as f2  # noqa: E402
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import trend_1926 as t  # noqa: E402

OUT = harness.RESEARCH / "results" / "bear-legs.md"
RALLY = 0.10
RALLY_SENS = (0.15, 0.20)
L3, L12 = 91, 365  # calendar days, as trend_tune (3 and 12 months)
NEXT_PEAK = 365  # a new 25% fall peaking this soon after a trough is a leg across episodes


# --- helpers ---


def ords_of(days: Sequence[date]) -> np.ndarray:
    return np.array([d.toordinal() for d in days])


def lookback(ords: np.ndarray, px: np.ndarray, days: int) -> np.ndarray:
    """Log return over `days` calendar days: last close on or before the date minus `days`."""
    j = np.searchsorted(ords, ords - days, side="right") - 1
    out = np.full(len(px), math.nan)
    ok = j >= 0
    out[ok] = np.log(px[ok] / px[j[ok]])
    return out


def rallies(px: np.ndarray, a: int, b: int, r: float) -> list[tuple[int, int]]:
    """(local low, rally top) session indices of the r / r zigzag inside one fall [a, b]."""
    seg = px[a : b + 1]
    pairs, open_pk = i1.zigzag(seg, r, r)
    out = []
    for j, (_, tr) in enumerate(pairs):
        if j + 1 < len(pairs):
            top = pairs[j + 1][0]
        elif open_pk is not None:
            top = open_pk
        else:
            top = tr + int(np.argmax(seg[tr:]))
        out.append((a + tr, a + top))
    return out


# --- step 1: catalogue ---


@dataclass
class Rally:
    low: int
    top: int
    size: float  # top / low - 1
    days: int
    next_low: float  # the next leg: lowest close after the top, to the fall's trough, / top - 1
    s3: bool  # 3-month signal on at the top
    s12: bool
    s3_turned: bool  # 3-month off at the low, on with 12-month off on some day of the rally
    s12_turned: bool  # 12-month off at the low, on on some day of the rally
    bought: dict[str, bool]  # rule out at the low, in on some session of the rally
    held: dict[str, bool]  # rule in at the top


@dataclass
class Leg:
    """One 25% episode with its rallies and the three rules' insurance."""

    ep: i1.Episode  # tsmom12's episode
    rl: list[Rally]
    n15: int
    n20: int
    d_or: float  # dI, or3-12 minus tsmom12
    d_arm: float
    cluster: int = -1
    follow: bool = False  # peak within NEXT_PEAK days of the same series' previous trough


@dataclass
class SetData:
    label: str
    trios: list[f2.Trio]
    legs: list[Leg]
    clusters: list[list[Leg]]


RULES = (("ts", "tsmom12"), ("orr", "or3-12"), ("arm", "arm3-12"))


def legs_of(trio: f2.Trio, eps: Sequence[i1.Episode], tw_or: dict[int, i1.Episode],
            tw_arm: dict[int, i1.Episode]) -> list[Leg]:  # fmt: skip
    s = trio.ts
    ords = ords_of(s.days)
    r3, r12 = lookback(ords, s.px, L3), lookback(ords, s.px, L12)
    pos = {k: getattr(trio, k).pos for k, _ in RULES}
    out = []
    for e in eps:
        a, b, _ = e.idx
        rl = []
        for lo, top in rallies(s.px, a, b, RALLY):
            span = slice(lo + 1, top + 1)
            nxt = float(s.px[top : b + 1].min() / s.px[top] - 1)
            on3 = (r3[span] > 0) & ~(r12[span] > 0)
            rl.append(Rally(
                lo, top, float(s.px[top] / s.px[lo] - 1), (s.days[top] - s.days[lo]).days, nxt,
                bool(r3[top] > 0), bool(r12[top] > 0),
                bool(not r3[lo] > 0 and on3.any()),
                bool(not r12[lo] > 0 and (r12[span] > 0).any()),
                {k: bool(p[lo] == 0 and p[span].max() > 0) for k, p in pos.items()},
                {k: bool(p[top] > 0) for k, p in pos.items()},
            ))  # fmt: skip
        n15 = len(rallies(s.px, a, b, RALLY_SENS[0]))
        n20 = len(rallies(s.px, a, b, RALLY_SENS[1]))
        out.append(Leg(e, rl, n15, n20, tw_or[id(e)].ins - e.ins, tw_arm[id(e)].ins - e.ins))
    return out


def set_data(label: str, trios: list[f2.Trio], anchor: Sequence[i1.Episode] | None) -> SetData:
    ss_or = fr.score_set(label, f2.as_pairs(trios, "orr"), anchor)
    ss_arm = fr.score_set(label, f2.as_pairs(trios, "arm"), anchor)
    legs: list[Leg] = []
    by_id: dict[int, Leg] = {}
    tw_arm = _twin_by_idx(ss_or, ss_arm)
    for x, sc in zip(trios, ss_or.sc_ts, strict=True):
        for lg in legs_of(x, sc.eps, ss_or.twin, tw_arm):
            legs.append(lg)
            by_id[id(lg.ep)] = lg
    for x in trios:
        mine = sorted((lg for lg in legs if lg.ep.series == x.ts.name), key=lambda v: v.ep.peak)
        for g0, g1 in zip(mine, mine[1:], strict=False):
            g1.follow = (g1.ep.peak - g0.ep.trough).days <= NEXT_PEAK
    clusters = []
    for k, g in enumerate(ss_or.clusters):
        cl = [by_id[id(e)] for e in g]
        for lg in cl:
            lg.cluster = k
        clusters.append(cl)
    return SetData(label, trios, legs, clusters)


def _twin_by_idx(ss_or: fr.SetScore, ss_arm: fr.SetScore) -> dict[int, i1.Episode]:
    """arm3-12's episode keyed by the id of or-score-set's tsmom12 episode (same episodes)."""
    out = {}
    for a, b in zip(ss_or.sc_ts, ss_arm.sc_ts, strict=True):
        for x, y in zip(a.eps, b.eps, strict=True):
            if x.idx != y.idx:
                raise AssertionError("episodes differ")
            out[id(x)] = ss_arm.twin[id(y)]
    return out


def rep(cl: Sequence[Leg]) -> Leg:
    """The cluster's representative fall: the US market's episode, else the deepest."""
    mk = [lg for lg in cl if lg.ep.series == t.MKT]
    return mk[0] if mk else max(cl, key=lambda lg: lg.ep.depth)


def pct(x: float) -> str:
    return f"{x:.0%}"


def catalogue(sd: SetData) -> list[str]:
    out = [f"### {sd.label}", ""]
    allr = [r for lg in sd.legs for r in lg.rl]
    n_ep = len(sd.legs)
    multi = sum(1 for lg in sd.legs if lg.rl)
    sizes = np.array([r.size for r in allr]) if allr else np.zeros(1)
    durs = np.array([r.days for r in allr]) if allr else np.zeros(1)
    out += [
        f"Episodes {n_ep} in {len(sd.clusters)} effective falls. Multi-leg (at least one 10% "
        f"rally inside the fall): {multi} of {n_ep} episodes ({multi / n_ep:.0%}); at 15%: "
        f"{sum(1 for lg in sd.legs if lg.n15)}; at 20%: {sum(1 for lg in sd.legs if lg.n20)}. "
        f"Rallies (10%): {len(allr)}, mean legs per episode {1 + len(allr) / n_ep:.2f}.",
        "",
        f"Rally size: median {np.median(sizes):.0%} (quartiles {np.quantile(sizes, 0.25):.0%} - "
        f"{np.quantile(sizes, 0.75):.0%}, largest {sizes.max():.0%}); duration median "
        f"{np.median(durs):.0f} days (quartiles {np.quantile(durs, 0.25):.0f} - "
        f"{np.quantile(durs, 0.75):.0f}). Next leg after a rally top: median "
        f"{np.median([r.next_low for r in allr]):.0%} to the fall's trough.",
        "",
        "At the rally tops (all rallies inside falls, every series):",
        "",
        "| | Share of rallies |",
        "|---|---:|",
        f"| 3-month signal on at the top | {np.mean([r.s3 for r in allr]):.0%} |",
        f"| 12-month signal on at the top | {np.mean([r.s12 for r in allr]):.0%} |",
        f"| 3-month turned on during the rally with 12-month off | "
        f"{np.mean([r.s3_turned for r in allr]):.0%} |",
        f"| 12-month turned on during the rally | {np.mean([r.s12_turned for r in allr]):.0%} |",
    ]
    for k, name in RULES:
        out.append(f"| `{name}` out at the low, bought during the rally | "
                   f"{np.mean([r.bought[k] for r in allr]):.0%} |")  # fmt: skip
    for k, name in RULES:
        out.append(f"| `{name}` holding at the top | {np.mean([r.held[k] for r in allr]):.0%} |")
    out += [""]

    # by the representative fall's leg count
    out += [
        "Effective falls by the representative episode's 10% rallies (the US market's episode "
        "where the cluster has one, else the deepest). dI = rule minus `tsmom12`, cluster mean "
        "over member episodes, log pts (negative = less insurance):",
        "",
        "| Rallies inside the fall | Falls | Mean depth | Mean days | `tsmom12` mean S | "
        "dI `or3-12` | dI `arm3-12` |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for lab, ok in (("0 (one leg)", lambda n: n == 0), ("1", lambda n: n == 1),
                    ("2 or more", lambda n: n >= 2)):  # fmt: skip
        g = [cl for cl in sd.clusters if ok(len(rep(cl).rl))]
        if not g:
            out.append(f"| {lab} | 0 | | | | | |")
            continue
        out.append(
            f"| {lab} | {len(g)} | {np.mean([rep(c).ep.depth for c in g]):.0%} | "
            f"{np.mean([rep(c).ep.days for c in g]):.0f} | "
            f"{np.mean([np.mean([lg.ep.share for lg in c]) for c in g]):+.2f} | "
            f"{np.mean([np.mean([lg.d_or for lg in c]) for c in g]):+.1f} | "
            f"{np.mean([np.mean([lg.d_arm for lg in c]) for c in g]):+.1f} |"
        )
    xs = [len(rep(cl).rl) for cl in sd.clusters]
    for key, lab in (("d_or", "or3-12"), ("d_arm", "arm3-12")):
        ys = [float(np.mean([getattr(lg, key) for lg in cl])) for cl in sd.clusters]
        rho = spearman(np.array(xs, float), np.array(ys))
        out.append("")
        out.append(f"Spearman correlation, representative rallies vs cluster dI `{lab}`: "
                   f"{rho:+.2f} ({len(xs)} falls).")  # fmt: skip
    out += [
        "",
        "Episode level (all member episodes; not independent, description): the fall's own "
        "rallies against whether it is a follow-on leg (it began within "
        f"{NEXT_PEAK} days of the same series' previous 25% trough, i.e. after a 25%+ "
        "bear-market rally):",
        "",
        "| Episodes | Count | Clusters touched | `tsmom12` mean S | dI `or3-12` | dI `arm3-12` |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for lab, fol, many in (("first leg, no 10% rally inside", False, False),
                           ("first leg, 10% rallies inside", False, True),
                           ("follow-on leg, no 10% rally inside", True, False),
                           ("follow-on leg, 10% rallies inside", True, True)):  # fmt: skip
        g = [lg for lg in sd.legs if lg.follow == fol and bool(lg.rl) == many]
        if not g:
            continue
        out.append(
            f"| {lab} | {len(g)} | {len({lg.cluster for lg in g})} | "
            f"{np.mean([lg.ep.share for lg in g]):+.2f} | {np.mean([lg.d_or for lg in g]):+.1f} | "
            f"{np.mean([lg.d_arm for lg in g]):+.1f} |"
        )
    tot_or = sum(lg.d_or for lg in sd.legs)
    tot_fo = sum(lg.d_or for lg in sd.legs if lg.follow)
    tot_ml = sum(lg.d_or for lg in sd.legs if lg.rl)
    out += [
        "",
        f"Share of the summed episode dI of `or3-12` ({tot_or:+.0f} log pts) in follow-on "
        f"legs: {tot_fo / tot_or:.0%}; in falls with 10% rallies inside: {tot_ml / tot_or:.0%}.",
        "",
    ]

    # legs across episodes
    pairs = lows = 0
    for x in sd.trios:
        eps = sorted((lg.ep for lg in sd.legs if lg.ep.series == x.ts.name), key=lambda e: e.peak)
        for e0, e1 in zip(eps, eps[1:], strict=False):
            if (e1.peak - e0.trough).days <= NEXT_PEAK:
                pairs += 1
                lows += x.ts.px[e1.idx[1]] < x.ts.px[e0.idx[1]]
    out += [
        f"Legs across episodes: {pairs} times a series began a new 25% fall within "
        f"{NEXT_PEAK} days of a trough (the 25%+ rally that ended the episode was a bear-market "
        f"rally in the wider sense); in {lows} of them the new trough was below the old.",
        "",
    ]

    # per effective fall
    out += [
        "| # | Representative | Peak | Trough | Depth | Days | Rallies 10% / 15% / 20% | "
        "Largest rally (days) | Tops with 3m on / 12m on | `or3-12` / `arm3-12` / `tsmom12` "
        "bought | Episodes multi-leg | dI or / arm |",
        "|---:|---|---|---|---:|---:|---|---|---|---|---|---|",
    ]
    for k, cl in enumerate(sd.clusters):
        r = rep(cl)
        big = max(r.rl, key=lambda x: x.size) if r.rl else None
        out.append(
            f"| {k + 1} | {r.ep.series} | {r.ep.peak} | {r.ep.trough} | {r.ep.depth:.0%} | "
            f"{r.ep.days} | {len(r.rl)} / {r.n15} / {r.n20} | "
            + (f"{big.size:.0%} ({big.days})" if big else "")
            + f" | {sum(x.s3 for x in r.rl)} / {sum(x.s12 for x in r.rl)} | "
            f"{sum(x.bought['orr'] for x in r.rl)} / {sum(x.bought['arm'] for x in r.rl)} / "
            f"{sum(x.bought['ts'] for x in r.rl)} | "
            f"{sum(1 for lg in cl if lg.rl)} of {len(cl)} | "
            f"{np.mean([lg.d_or for lg in cl]):+.0f} / {np.mean([lg.d_arm for lg in cl]):+.0f} |"
        )
    return out + [""]


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    def rank(v: np.ndarray) -> np.ndarray:
        o = np.argsort(v, kind="mergesort")
        rk = np.empty(len(v))
        rk[o] = np.arange(len(v))
        for u in np.unique(v):  # average ties
            m = v == u
            rk[m] = rk[m].mean()
        return rk

    rx, ry = rank(x), rank(y)
    if rx.std() == 0 or ry.std() == 0:
        return math.nan
    return float(np.corrcoef(rx, ry)[0, 1])


# --- main ---


def load() -> tuple[SetData, SetData]:
    us = f2.load_us()
    dev, _ = f2.load_geo()
    sd_us = set_data("US: market + 10 industries, 1927-2025", us, None)
    us_mkt = [lg.ep for lg in sd_us.legs if lg.ep.series == t.MKT]
    sd_dev = set_data("Non-US: 13 developed price indices", dev, us_mkt)
    return sd_us, sd_dev


def main() -> None:
    sd_us, sd_dev = load()
    head = [
        "# bear-legs: multi-leg bear markets, and bear-market rally vs bottom",
        "",
        "Card: `cards/bear-legs.md`. Written by `lib/bearlegs.py`. Descriptive, no pick, no "
        "`tries.md` rows. Episodes and clusters as insure-1 (US) and insure-2 (non-US); rules "
        "as fast-reentry-2's paper series. Rally = 10% / 10% zigzag inside a 25% fall's "
        "[peak, trough]; signals on daily closes (3-month = 91 days, 12-month = 365 days).",
        "",
        "## Step 1: catalogue of multi-leg bears",
        "",
    ]
    body = catalogue(sd_us) + catalogue(sd_dev)
    OUT.write_text("\n".join(head + body))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
