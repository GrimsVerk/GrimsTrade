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
import warnings
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
    db_or: float = 0.0  # dB (year after the low), or3-12 minus tsmom12
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
        o = tw_or[id(e)]
        out.append(Leg(e, rl, n15, n20, o.ins - e.ins, tw_arm[id(e)].ins - e.ins,
                       o.rebound - e.rebound))  # fmt: skip
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
        "Added after the card (description, not a test): the follow-on flag is known when a fall "
        "starts, the rally count is not. `or3-12` minus `tsmom12` by that flag alone, episode "
        "level (dB = year after the low; the rebound of a follow-on leg can overlap the next "
        "fall's peak, as in insure-1):",
        "",
        "| Episodes | Count | Clusters touched | dI | dB | dN = dI + dB |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for lab, fol in (("first leg", False), ("follow-on leg", True)):
        g = [lg for lg in sd.legs if lg.follow == fol]
        di, db = np.mean([lg.d_or for lg in g]), np.mean([lg.db_or for lg in g])
        out.append(f"| {lab} | {len(g)} | {len({lg.cluster for lg in g})} | {di:+.1f} | "
                   f"{db:+.1f} | {di + db:+.1f} |")  # fmt: skip
    out += [""]

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


# --- step 2: bear-market rally or bottom, with information at the time ---

FEATS = (
    ("fall", "Prior fall, log(peak / L)"),
    ("retr", "Retracement, log(close / L) / log(peak / L)"),
    ("fall_days", "Fall duration, days peak -> L"),
    ("rally_days", "Rally speed, days L -> event"),
    ("vol", "Volatility, 21 sessions, annualized"),
    ("vol_ratio", "Volatility ratio, 21 / 252 sessions"),
    ("r12", "12-month log return"),
    ("breadth", "Breadth, share of the set with 3-month return > 0"),
)
A_FEATS = tuple(k for k, _ in FEATS if k != "retr")
DOWN, UP = i1.PRIMARY
BOOT, SEED = 10_000, 0
PLACEBO, BLOCK = 500, 21


@dataclass
class Panel:
    """A set on one calendar: closes forward-filled inside each series' span, NaN outside."""

    ords: np.ndarray
    px: np.ndarray  # series x sessions
    names: list[str]
    breadth_rows: list[int]  # rows counted in breadth
    week_last: np.ndarray  # last session of each calendar week


def panel_of(sd: SetData, breadth_rows: list[int]) -> Panel:
    cal = sorted({d for x in sd.trios for d in x.ts.days})
    ords = ords_of(cal)
    px = np.full((len(sd.trios), len(cal)), math.nan)
    for r, x in enumerate(sd.trios):
        o = ords_of(x.ts.days)
        j = np.searchsorted(o, ords, side="right") - 1
        ok = (j >= 0) & (ords <= o[-1])
        px[r, ok] = x.ts.px[j[ok]]
    wk = (ords - 1) // 7
    week_last = np.append(wk[1:] != wk[:-1], True)
    return Panel(ords, px, [x.ts.name for x in sd.trios], breadth_rows, week_last)


def roll_std(lr: np.ndarray, w: int) -> np.ndarray:
    """Std of lr[i-w+1 .. i] (NaN-free spans only), NaN where fewer than w values."""
    out = np.full(len(lr), math.nan)
    x = np.nan_to_num(lr)
    ok = (~np.isnan(lr)).astype(float)
    c1, c2, cn = (np.concatenate(([0.0], np.cumsum(v))) for v in (x, x * x, ok))
    i = np.arange(w - 1, len(lr))
    n = cn[i + 1] - cn[i + 1 - w]
    s1, s2 = c1[i + 1] - c1[i + 1 - w], c2[i + 1] - c2[i + 1 - w]
    var = (s2 - s1 * s1 / w) / (w - 1)
    out[i] = np.where(n == w, np.sqrt(np.maximum(var, 0.0)), math.nan)
    return out


@dataclass
class Events:
    kind: str  # "A" or "B"
    row: np.ndarray  # series row
    pk_ord: np.ndarray  # episode peak (ordinal), to find the cluster
    bottom: np.ndarray  # bool
    x: dict[str, np.ndarray]


def detect(px: np.ndarray, week_on: np.ndarray) -> tuple[list[tuple], list[tuple], list]:
    """insure-1's zigzag run forward; A and B events (i, peak, L, episode no.) and the pairs."""
    lp = px.tolist()
    wl = week_on.tolist()
    ev_a: list[tuple] = []
    ev_b: list[tuple] = []
    pairs: list[tuple[int, int]] = []
    falling, pk, tr, fired = False, 0, 0, False
    for i in range(1, len(lp)):
        v = lp[i]
        if not falling:
            if v > lp[pk]:
                pk = i
            elif v <= lp[pk] * (1 - DOWN):
                falling, tr, fired = True, i, False
        elif v < lp[tr]:
            tr, fired = i, False
        elif v >= lp[tr] * (1 + UP):
            pairs.append((pk, tr))
            falling, pk = False, i
        else:
            if not fired and v >= lp[tr] * (1 + RALLY):
                ev_a.append((i, pk, tr, len(pairs)))
                fired = True
            if wl[i]:
                ev_b.append((i, pk, tr, len(pairs)))
    return ev_a, ev_b, pairs


def events_of(p: Panel) -> tuple[Events, Events, list[list[tuple[int, int]]]]:
    """Both event sets with the eight observables, every series of the panel."""
    nser, n = p.px.shape
    r3 = np.full((nser, n), math.nan)
    rows_a: list[list] = []
    rows_b: list[list] = []
    all_pairs = []
    per: list[dict[str, np.ndarray]] = []
    spans = []
    for r in range(nser):
        ok = np.nonzero(~np.isnan(p.px[r]))[0]
        a, b = int(ok[0]), int(ok[-1]) + 1
        spans.append(a)
        o, x = p.ords[a:b], p.px[r, a:b]
        r3[r, a:b] = lookback(o, x, L3)
        r12 = lookback(o, x, L12)
        lr = np.concatenate(([math.nan], np.diff(np.log(x))))
        v21, v252 = roll_std(lr, 21), roll_std(lr, 252)
        per.append({"r12": r12, "vol": v21 * math.sqrt(252), "vol_ratio": v21 / v252})
        wl = p.week_last[a:b]
        w_idx = np.nonzero(wl)[0]
        on = np.zeros(b - a, dtype=bool)
        s3 = r3[r, a:b] > 0
        s12 = r12 > 0
        on[w_idx[1:]] = s3[w_idx[1:]] & ~s3[w_idx[:-1]] & ~s12[w_idx[1:]]
        ev_a, ev_b, pairs = detect(x, on)
        all_pairs.append([(a + u, a + w) for u, w in pairs])
        for ev, rows in ((ev_a, rows_a), (ev_b, rows_b)):
            for i, pk, tr, k in ev:
                if k >= len(pairs):
                    continue  # unfinished fall at the end
                rows.append([r, a + i, a + pk, a + tr, tr == pairs[k][1]])
    pos3 = np.where(np.isnan(r3), math.nan, (r3 > 0).astype(float))
    br_rows = pos3[p.breadth_rows]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # sessions where no series has a value
        breadth = np.nanmean(br_rows, axis=0)

    def build(kind: str, rows: list[list]) -> Events:
        if not rows:
            z = np.zeros(0)
            return Events(kind, z.astype(int), z, z.astype(bool), {k: z for k, _ in FEATS})
        m = np.array(rows, dtype=np.int64)
        row, i, pk, tr = m[:, 0], m[:, 1], m[:, 2], m[:, 3]
        xs = p.px[row, i]
        lpk, ltr = np.log(p.px[row, pk]), np.log(p.px[row, tr])
        fall = lpk - ltr
        out = {
            "fall": fall,
            "retr": (np.log(xs) - ltr) / fall,
            "fall_days": (p.ords[tr] - p.ords[pk]).astype(float),
            "rally_days": (p.ords[i] - p.ords[tr]).astype(float),
            "breadth": breadth[i],
        }
        for k in ("r12", "vol", "vol_ratio"):
            out[k] = np.array([per[rr][k][ii - spans[rr]] for rr, ii in zip(row, i, strict=True)])
        return Events(kind, row, p.ords[pk].astype(float), m[:, 4].astype(bool), out)

    return build("A", rows_a), build("B", rows_b), all_pairs


def auc(x: np.ndarray, y: np.ndarray) -> float:
    """P(value of a bottom > value of a bear rally), ties half; NaNs dropped."""
    ok = ~np.isnan(x)
    x, y = x[ok], y[ok]
    n1, n0 = int(y.sum()), int((~y).sum())
    if n1 == 0 or n0 == 0:
        return math.nan
    order = np.argsort(x, kind="mergesort")
    xs = x[order]
    rk = np.empty(len(x))
    rk[order] = np.arange(1, len(x) + 1)
    _, inv, cnt = np.unique(xs, return_inverse=True, return_counts=True)
    if (cnt > 1).any():  # average ranks for ties
        start = np.concatenate(([0], np.cumsum(cnt)[:-1]))
        avg = start + (cnt + 1) / 2
        rk[order] = avg[inv]
    return float((rk[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def cluster_ids(ev: Events, sd: SetData) -> np.ndarray:
    key = {(lg.ep.series, lg.ep.peak.toordinal()): lg.cluster for lg in sd.legs}
    names = [x.ts.name for x in sd.trios]
    return np.array([key[(names[r], int(o))] for r, o in zip(ev.row, ev.pk_ord, strict=True)])


def boot_auc(x: np.ndarray, y: np.ndarray, cl: np.ndarray) -> tuple[float, float, float]:
    """Cluster bootstrap over effective falls: 90% range and two-sided p of AUC vs 0.5."""
    ok = ~np.isnan(x)
    x, y, cl = x[ok], y[ok], cl[ok]
    pos, neg = np.nonzero(y)[0], np.nonzero(~y)[0]
    cmp = (x[pos][:, None] > x[neg][None, :]) + 0.5 * (x[pos][:, None] == x[neg][None, :])
    ids = np.unique(cl)
    rng = np.random.default_rng(SEED)
    draws = np.zeros((BOOT, len(ids)))
    for k in range(BOOT):
        draws[k] = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))
    col = np.searchsorted(ids, cl)
    w1, w0 = draws[:, col[pos]], draws[:, col[neg]]
    den = w1.sum(axis=1) * w0.sum(axis=1)
    num = ((w1 @ cmp) * w0).sum(axis=1)
    a = num[den > 0] / den[den > 0]
    lo, hi = np.quantile(a, [0.05, 0.95])
    p = min(1.0, 2 * min(float((a <= 0.5).mean()), float((a >= 0.5).mean())))
    return float(lo), float(hi), p


def synth(p: Panel, rng: np.random.Generator) -> Panel:
    """Stationary block bootstrap (mean block BLOCK), the same draws for every series."""
    n = len(p.ords)
    idx = np.empty(n - 1, dtype=np.int64)
    k = 0
    while k < n - 1:
        ln = int(rng.geometric(1 / BLOCK))
        s = int(rng.integers(1, n))
        take = (s - 1 + np.arange(min(ln, n - 1 - k))) % (n - 1) + 1
        idx[k : k + len(take)] = take
        k += len(take)
    lr = np.diff(np.log(p.px), axis=1)  # series x (n - 1), NaN outside spans
    out = np.full(p.px.shape, math.nan)
    for r in range(p.px.shape[0]):
        ok = np.nonzero(~np.isnan(p.px[r]))[0]
        a, b = int(ok[0]), int(ok[-1])
        src = lr[r, idx[a:b] - 1]
        bad = np.isnan(src)
        if bad.any():  # source outside this series' span: its own return at a random session
            pool = lr[r, a:b]
            src[bad] = pool[rng.integers(0, len(pool), int(bad.sum()))]
        out[r, a] = 1.0
        out[r, a + 1 : b + 1] = np.exp(np.cumsum(src))
    return Panel(p.ords, out, p.names, p.breadth_rows, p.week_last)


@dataclass
class Step2:
    real: dict[str, Events]
    clusters: dict[str, np.ndarray]
    placebo: dict[str, dict[str, np.ndarray]]  # kind -> feature -> AUCs
    base: dict[str, np.ndarray]  # kind -> placebo share of bottoms
    pairs_ok: bool


def step2(sd: SetData, breadth_rows: list[int], draws: int) -> Step2:
    p = panel_of(sd, breadth_rows)
    ea, eb, pairs = events_of(p)
    # the forward zigzag must give insure-1's episodes
    want = sorted((lg.ep.series, lg.ep.peak, lg.ep.trough) for lg in sd.legs)
    got = sorted(
        (p.names[r], date.fromordinal(int(p.ords[u])), date.fromordinal(int(p.ords[w])))
        for r, pr in enumerate(pairs)
        for u, w in pr
    )
    real = {"A": ea, "B": eb}
    cls = {k: cluster_ids(v, sd) for k, v in real.items()}
    rng = np.random.default_rng(SEED)
    plc: dict[str, dict[str, list[float]]] = {"A": {}, "B": {}}
    base: dict[str, list[float]] = {"A": [], "B": []}
    for _ in range(draws):
        sa, sb, _ = events_of(synth(p, rng))
        for kind, ev in (("A", sa), ("B", sb)):
            base[kind].append(float(ev.bottom.mean()) if len(ev.bottom) else math.nan)
            for f, _ in FEATS:
                plc[kind].setdefault(f, []).append(auc(ev.x[f], ev.bottom))
    return Step2(real, cls,
                 {k: {f: np.array(v) for f, v in d.items()} for k, d in plc.items()},
                 {k: np.array(v) for k, v in base.items()}, want == got)  # fmt: skip


def step2_table(label: str, st: Step2, other: Step2 | None) -> tuple[list[str], dict]:
    out = [f"### {label}", ""]
    out.append(
        f"Forward zigzag reproduces insure-1/insure-2's episodes: {'yes' if st.pairs_ok else 'NO'}."
    )
    out.append("")
    res: dict[tuple[str, str], tuple] = {}
    for kind, title in (("A", "A, rally of 10% off the low"), ("B", "B, 3-month re-entry moment")):
        ev, cl = st.real[kind], st.clusters[kind]
        nb, nr = int(ev.bottom.sum()), int((~ev.bottom).sum())
        bs = st.base[kind]
        out += [
            f"**Set {title}:** {len(ev.bottom)} events ({nb} bottoms, {nr} bear rallies) from "
            f"{len(np.unique(cl))} effective falls; share bottoms {ev.bottom.mean():.2f} "
            f"(placebo median {np.nanmedian(bs):.2f}, 5-95% {np.nanquantile(bs, 0.05):.2f} - "
            f"{np.nanquantile(bs, 0.95):.2f}).",
            "",
            "| Observable | Median, bottoms | Median, bear rallies | AUC | Bootstrap 90% | "
            "Bootstrap p | Placebo AUC median (5-95%) | Placebo p | AUC minus placebo median | "
            "Reading |",
            "|---|---:|---:|---:|---|---:|---|---:|---:|---|",
        ]
        for f, name in FEATS:
            if kind == "A" and f == "retr":
                continue
            x = ev.x[f]
            if np.all(np.isnan(x)):
                continue
            a = auc(x, ev.bottom)
            lo, hi, bp = boot_auc(x, ev.bottom, cl)
            pl = st.placebo[kind][f]
            pl = pl[~np.isnan(pl)]
            pp = float((np.abs(pl - 0.5) >= abs(a - 0.5)).mean())
            reading = ""
            if kind == "A" and other is not None:
                oa = auc(other.real["A"].x[f], other.real["A"].bottom)
                same = (a - 0.5) * (oa - 0.5) > 0
                ok = bp < 0.05 and pp < 0.05 and same
                reading = ("distinguishes, in sample" if ok else "not shown") + (
                    f" (non-US AUC {oa:.2f})"
                )
            res[(kind, f)] = (a, bp, pp)
            b1, b0 = np.nanmedian(x[ev.bottom]), np.nanmedian(x[~ev.bottom])
            fmt = ".0f" if "days" in f else ".2f"
            out.append(
                f"| {name} | {b1:{fmt}} | {b0:{fmt}} | {a:.2f} | {lo:.2f} - {hi:.2f} | {bp:.3f} | "
                f"{np.median(pl):.2f} ({np.quantile(pl, 0.05):.2f} - {np.quantile(pl, 0.95):.2f})"
                f" | {pp:.3f} | {a - np.median(pl):+.2f} | {reading} |"
            )
        out.append("")
    return out, res


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
    draws = int(sys.argv[sys.argv.index("--draws") + 1]) if "--draws" in sys.argv else PLACEBO
    st_us = step2(sd_us, list(range(1, len(sd_us.trios))), draws)
    st_dev = step2(sd_dev, list(range(len(sd_dev.trios))), draws)
    t_us, _ = step2_table("US: market + 10 industries (set A decides)", st_us, st_dev)
    t_dev, _ = step2_table("Non-US: 13 developed price indices (replication)", st_dev, None)
    s2 = [
        "## Step 2: bear-market rally or bottom, with information at the time",
        "",
        "Events per the card: A = first close 10% above the lowest close L since the peak, inside "
        "a confirmed 25% fall; B = last session of a week where the 3-month signal turns on with "
        "the 12-month off, inside a confirmed 25% fall. Bottom = L is the episode's trough. AUC = "
        "P(observable of a bottom > that of a bear rally). Bootstrap: "
        f"{BOOT:,} draws over effective falls. Placebo: {draws} stationary block-bootstrap "
        f"histories (mean block {BLOCK} sessions, same draws for all series of a set); placebo p "
        "= share of placebo AUCs at least as far from 0.5; the column AUC minus placebo median "
        "(not on the card, description) shows what is left once the placebo's mechanical "
        "AUC is taken out. Breadth: US over the 10 industries, "
        "non-US over the 13 indices. Looks: 7 observables in A + 8 in B, two regions = 30 AUCs "
        "(the card's count of 31 was an arithmetic slip; 30 were computed).",
        "",
    ]
    if draws != PLACEBO:
        s2.insert(2, f"**Test run with {draws} placebo draws, not the card's {PLACEBO}.**\n")
    OUT.write_text("\n".join(head + body + s2 + t_us + t_dev))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
