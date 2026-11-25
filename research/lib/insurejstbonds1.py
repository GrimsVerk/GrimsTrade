"""insure-jstbonds-1: does trend's crash insurance hold on JST annual government-bond returns?
Card: research/cards/insure-jstbonds-1.md.

    uv run python -I research/lib/insurejstbonds1.py counts   # holding-index fall counts only
    uv run python -I research/lib/insurejstbonds1.py          # full run, writes the results

insure-1870-1's annual rule and scoring (`insure1870`, unchanged) applied to the JST R6 `bond_tr`
(cached by data-long-4, read-only, never committed): hold bonds in year t if the bond total
return of year t-1 beat the bill, else bills. The fall threshold comes from holding-index counts
alone (`counts`, run before any rule position). Timing is judged against AR-preserving nulls
(Gaussian AR(1) per country and a stationary block bootstrap per segment), as #204 requires
before 1966; rotations are description only. A year-older signal control as stale-checks-1 (b).
Ties: |I| < 1e-9 is set to 0 (insure-bonds-1's tie bug). Writes
research/results/insure-jstbonds-1.md (statistics only) and `insure-check` rows to tries.md
(once).
"""

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import insure1 as i1  # noqa: E402
import insure1870 as ins  # noqa: E402
import jstautocorr as ja  # noqa: E402
import jstautocorr2 as ja2  # noqa: E402

IDEA = "insure-jstbonds-1"
OUT = HERE.parent / "results" / "insure-jstbonds-1.md"
LADDER = (0.25, 0.20, 0.15, 0.10, 0.075, 0.05)
MIN_CLUSTERS = 10  # threshold rule: largest d with this many anchored and linked clusters
TOO_FEW = 8  # verdict "Too few falls" below this many anchored clusters with I != 0
TIE = 1e-9
WORLDS, SIM_ROT, OBS_ROT, SEED = 1_000, 50, 1_000, 0
BLOCK = 5.0  # mean block length of the stationary bootstrap, years
ERA_CUT = 1965
NAMES = {**ins.NAMES}

# Bond coverage already scored (datawide2.SEEN, the project's register) plus insure-bonds-1
# (monthly Norway 1823-1984 and UK consols 1867-1926). Inclusive year ranges.
SEEN_BOND: dict[str, list[tuple[int, int]]] = {
    "USA": [(1871, 2025)],
    "AUS": [(1969, 2025)], "CHE": [(1955, 2025)], "DEU": [(1956, 2025)], "GBR": [(1960, 2025)],
    "JPN": [(1989, 2025)], "NOR": [(1985, 2025)], "SWE": [(1986, 2025)],
}  # fmt: skip
INSURE_BONDS1: dict[str, list[tuple[int, int]]] = {"NOR": [(1823, 1984)], "GBR": [(1867, 1926)]}


def overlap(iso: str, y: int) -> bool:
    spans = SEEN_BOND.get(iso, []) + INSURE_BONDS1.get(iso, [])
    return any(a <= y <= b for a, b in spans)


# --- data and segments ---

Jst = dict[str, dict[str, dict[int, float]]]


def load_jst() -> Jst:
    import long_macro_build as lmb

    j = lmb._jst()
    return {
        v: {iso: {d.year: x for d, x in ser} for iso, ser in j[v].items()}
        for v in ("bond_tr", "bill_rate", "cpi")
    }


@dataclass(frozen=True)
class Config:
    key: str
    label: str
    rung: int = 0  # offset from the chosen rung on LADDER (+1 = next smaller d)
    with_overlap: bool = False
    keep_disrupted: bool = False
    real: bool = False
    cash0: bool = False
    era: str = ""  # "", "pre" (scored to 1965) or "post" (scored 1966-2020)


CONFIGS = [
    Config("primary", "Primary: non-overlapping country-years, undisrupted"),
    Config("overlap", "Check 1: overlapping years kept (all 16 countries)", with_overlap=True),
    Config("disrupted", "Check 2: disrupted years kept", keep_disrupted=True),
    Config("real", "Check 3: events on the real index", real=True),
    Config("cash0", "Check 4: cash at 0 when out", cash0=True),
    Config("larger", "Check 5a: next larger fall threshold", rung=-1),
    Config("smaller", "Check 5b: next smaller fall threshold", rung=+1),
    Config("pre", "Check 6a: primary, scored years to 1965", era="pre"),
    Config("post", "Check 6b: primary, scored years 1966-2020", era="post"),
]


def dropped(cfg: Config, iso: str, cpi: dict[int, float]) -> frozenset[int]:
    hyper = ins.hyper_years(cpi)
    out = set()
    for y in range(1860, 2021):
        if not cfg.keep_disrupted and ja2.disrupted(iso, y, hyper):
            out.add(y)
        if not cfg.with_overlap and overlap(iso, y):
            out.add(y)
        if cfg.real and (y not in cpi or y - 1 not in cpi):
            out.add(y)
        if cfg.era == "post" and y < ERA_CUT:
            out.add(y)  # 1965 stays as the signal year of the first post segment
    return frozenset(out)


def build(cfg: Config, jst: Jst, iso_only: str | None = None) -> list[ins.Seg]:
    out = []
    last = ERA_CUT if cfg.era == "pre" else 2020
    for iso in sorted(jst["bond_tr"]):
        if iso_only and iso != iso_only:
            continue
        cpi = jst["cpi"].get(iso, {})
        bill = jst["bill_rate"].get(iso, {})
        out += ins.segments(iso, jst["bond_tr"][iso], bill, cpi, last, dropped(cfg, iso, cpi))
    return out


def anchor_segs(cfg: Config, jst: Jst) -> list[ins.Seg]:
    """US bond segments for the anchors: all usable US years (labels only)."""
    us = replace(cfg, with_overlap=True, era="")
    return build(us, jst, "USA")


# --- holding-only episodes (threshold counts; no rule position used) ---


def hold_eps(seg: ins.Seg, d: float, real: bool = False) -> tuple[list[i1.Episode], int | None]:
    px = ins.hold_index(seg, real)
    pairs, open_pk = i1.zigzag(px, d, d)
    eps = [
        i1.Episode(seg.name, ins._ye(seg.years[a]), ins._ye(seg.years[b]), 1 - px[b] / px[a],
                   100 * math.log(px[b] / px[a]), 0.0, 0.0, 0.0, idx=(a, b, b))
        for a, b in pairs
    ]  # fmt: skip
    return eps, (seg.years[open_pk] if open_pk is not None else None)


@dataclass
class Count:
    d: float
    episodes: int
    anchored: int
    linked: int
    open_falls: int
    countries: int
    multi_year: int


def fall_counts(segs: Sequence[ins.Seg], anchors: Sequence[ins.Seg], real: bool = False,
                ladder: Sequence[float] = LADDER) -> list[Count]:  # fmt: skip
    out = []
    for d in ladder:
        eps, opens = [], 0
        for s in segs:
            e, op = hold_eps(s, d, real)
            eps += e
            opens += op is not None
        anc = [e for s in anchors for e in hold_eps(s, d, real)[0]]
        out.append(Count(d, len(eps), len(ins.anchored(anc, eps)), len(i1.link(eps)), opens,
                         len({e.series[:3] for e in eps}),
                         sum(1 for e in eps if e.trough.year - e.peak.year > 1)))  # fmt: skip
    return out


def choose(counts: Sequence[Count]) -> int:
    """Index on LADDER of the largest d with at least MIN_CLUSTERS anchored and linked clusters;
    the last rung (5%) if none."""
    for j, c in enumerate(counts):
        if c.anchored >= MIN_CLUSTERS and c.linked >= MIN_CLUSTERS:
            return j
    return len(counts) - 1


# --- scoring with the tie rule ---


def rescore(sc: ins.Scored, rule: np.ndarray) -> None:
    ins.rescore(sc, rule)
    for e in sc.eps:
        if abs(e.ins) < TIE:
            e.ins = 0.0
            e.rule = e.hold


# --- AR-preserving nulls (per-episode gap G) ---


def logx(s: ins.Seg) -> np.ndarray:
    return np.log1p(s.r) - np.log1p(s.b)


def pairs_of(r: np.ndarray, d: float, pi: np.ndarray | None = None) -> list[tuple[int, int]]:
    g = 1 + r if pi is None else (1 + r) / (1 + pi)
    return i1.zigzag(np.concatenate([[1.0], np.cumprod(g)]), d, d)[0]


def ep_shares(r: np.ndarray, cash: np.ndarray, pos: np.ndarray, pairs: Sequence[tuple[int, int]],
              pi: np.ndarray | None = None, cost: float = ins.COST) -> np.ndarray:  # fmt: skip
    """S of each episode for each row of `pos` (K x n), as `jstautocorr.shares`, but with the
    denominator on the index the episodes were found on (real when `pi` is given)."""
    pos = np.atleast_2d(pos)
    flips = np.abs(np.diff(pos, axis=1, prepend=pos[:, :1]))
    rule = pos * r + (1 - pos) * cash - cost * flips
    d = 100 * (np.log1p(rule) - np.log1p(r))
    cum = np.concatenate([np.zeros((len(pos), 1)), np.cumsum(d, axis=1)], axis=1)
    g = np.log1p(r) - (np.log1p(pi) if pi is not None else 0.0)
    hold = np.concatenate([[0.0], np.cumsum(100 * g)])
    a = np.array([p[0] for p in pairs], dtype=int)
    b = np.array([p[1] for p in pairs], dtype=int)
    return (cum[:, b] - cum[:, a]) / np.abs(hold[b] - hold[a])


def gap_stats(rs: Sequence[np.ndarray], bs: Sequence[np.ndarray], poss: Sequence[np.ndarray],
              pairs: Sequence[Sequence[tuple[int, int]]], ks: np.ndarray,
              pis: Sequence[np.ndarray | None] | None = None
              ) -> tuple[float, float, float, int]:  # fmt: skip
    """Mean episode S of the rule, mean over rotations of the mean episode S, mean episode S of
    the fixed exposure, number of episodes (jst-autocorr-1's per-episode statistic)."""
    rule, fix, per_rot = [], [], []
    for j, (r, b, pos, pr) in enumerate(zip(rs, bs, poss, pairs, strict=True)):
        if not pr:
            continue
        pi = pis[j] if pis is not None else None
        rule.append(ep_shares(r, b, pos, pr, pi)[0])
        fix.append(ep_shares(r, b, np.full(len(pos), pos.mean()), pr, pi, cost=0.0)[0])
        rolled = np.array([np.roll(pos, int(k) % len(pos)) for k in ks])
        per_rot.append(ep_shares(r, b, rolled, pr, pi))
    if not rule:
        return math.nan, math.nan, math.nan, 0
    ru, fx = np.concatenate(rule), np.concatenate(fix)
    rot = np.concatenate(per_rot, axis=1).mean(axis=1)
    return float(ru.mean()), float(rot.mean()), float(fx.mean()), len(ru)


def cash_of(s: ins.Seg, cash0: bool) -> np.ndarray:
    return np.zeros(len(s.b)) if cash0 else s.b


def observed_gap(segs: Sequence[ins.Seg], d: float, real: bool, cash0: bool) -> tuple[float, ...]:
    rng_ks = np.random.default_rng(SEED).integers(1, max(len(s.pos) for s in segs), size=OBS_ROT)
    pairs = [pairs_of(s.r, d, s.pi if real else None) for s in segs]
    rule, rot, fix, n = gap_stats([s.r for s in segs], [cash_of(s, cash0) for s in segs],
                                  [s.pos for s in segs], pairs, rng_ks,
                                  [s.pi for s in segs] if real else None)  # fmt: skip
    return rule, rot, fix, rule - rot, n


def ar1_x(rng: np.random.Generator, s: ins.Seg, n: int, phi: float) -> np.ndarray:
    x = logx(s)
    return ja.ar1(rng, n, float(x.mean()), float(x.std(ddof=1)), phi)


def bb_x(rng: np.random.Generator, s: ins.Seg, n: int, block: float = BLOCK) -> np.ndarray:
    """Stationary bootstrap (Politis-Romano) of the segment's own log excess returns: n draws
    in blocks of mean length `block`, circular."""
    x = logx(s)
    m = len(x)
    out = np.empty(n)
    j = int(rng.integers(m))
    for t in range(n):
        if t and rng.random() < 1 / block:
            j = int(rng.integers(m))
        elif t:
            j = (j + 1) % m
        out[t] = x[j]
    return out


def null_gaps(segs: Sequence[ins.Seg], d: float, kind: str, lag: int = 1, real: bool = False,
              cash0: bool = False, worlds: int = WORLDS, seed: int = SEED,
              phis: dict[str, float] | None = None) -> np.ndarray:  # fmt: skip
    """Gap G of the rule (signal lag `lag` years) in `worlds` synthetic worlds: log excess returns
    over bills from AR(1) ('ar', each country's own lag-1 acf) or a block bootstrap ('bb');
    bills (and CPI) as observed; episodes re-detected at d."""
    rng = np.random.default_rng(seed)
    phis = phis if phis is not None else ja.country_phi(list(segs))
    lmax = max(len(s.pos) for s in segs)
    out = np.full(worlds, np.nan)
    for w in range(worlds):
        rs, bs, poss, pairs = [], [], [], []
        for s in segs:
            n = len(s.r)
            if kind == "ar":
                x = ar1_x(rng, s, n + lag, float(np.clip(phis[s.iso], -0.9, 0.9)))
            else:
                x = bb_x(rng, s, n + lag)
            r = (1 + s.b) * np.exp(x[lag:]) - 1
            rs.append(r)
            bs.append(cash_of(s, cash0))
            poss.append(ja.signal(x[:n]))
            pairs.append(pairs_of(r, d, s.pi if real else None))
        ks = rng.integers(1, lmax, size=SIM_ROT)
        rule, rot, _, k = gap_stats(rs, bs, poss, pairs, ks, [s.pi for s in segs] if real else None)
        if k:
            out[w] = rule - rot
    return out


def p_ge(g: np.ndarray, obs: float) -> float:
    v = g[~np.isnan(g)]
    return float((v >= obs).mean()) if len(v) else math.nan


# --- one configuration ---


@dataclass
class Result:
    label: str
    d: float
    scs: list[ins.Scored]
    eps: list[i1.Episode]
    anch: list[list[i1.Episode]]
    linked: list[list[i1.Episode]]
    lines: dict[str, str]
    s_rule: float
    p_rule: float
    s_fix: float
    p_fix: float
    s_rot: np.ndarray
    p_rot_dist: np.ndarray
    gap: tuple[float, ...]
    g_ar: np.ndarray
    g_bb: np.ndarray
    drag: float
    acf: float
    verdict: str = ""
    quals: list[str] = field(default_factory=list)

    @property
    def p_rot(self) -> float:
        return float((self.s_rot >= self.s_rule).mean())

    @property
    def p_ar(self) -> float:
        return p_ge(self.g_ar, self.gap[3])

    @property
    def p_bb(self) -> float:
        return p_ge(self.g_bb, self.gap[3])

    @property
    def p_null(self) -> float:
        return max(self.p_ar, self.p_bb)

    @property
    def head(self) -> tuple[int, int]:
        iv = ins.cvals(self.anch, lambda e: e.ins)
        return sum(1 for v in iv if v > 0), len(iv)

    @property
    def per_ep(self) -> tuple[int, int, int]:
        e = self.eps
        return sum(1 for x in e if x.ins > 0), sum(1 for x in e if x.ins == 0), len(e)


def run(label: str, segs: list[ins.Seg], anchors: list[ins.Seg], d: float, real: bool = False,
        cash0: bool = False, lag: int = 1, worlds: int = WORLDS) -> Result:  # fmt: skip
    scs = [ins.episodes(s, d, d, real) for s in segs]
    for s in scs:
        rescore(s, ins.strat(s.seg, s.seg.pos, cash0))
    eps = [e for s in scs for e in s.eps]
    anc = [e for u in anchors for e in hold_eps(u, d, real)[0]]

    def groups() -> list[list[i1.Episode]]:
        return ins.anchored(anc, eps)

    anch, linked = groups(), i1.link(eps)
    lines = {
        "I anchored": i1.test_line("I, anchored clusters", anch, lambda e: e.ins),
        "I linked": i1.test_line("I, linked clusters", linked, lambda e: e.ins),
        "N anchored": i1.test_line("N, anchored clusters", anch, lambda e: e.net),
        "I episodes": i1.test_line("I, episodes", [[e] for e in eps], lambda e: e.ins),
    }
    s_rule = float(np.mean(ins.cvals(anch, lambda e: e.share))) if anch else math.nan
    p_rule = ins.premium(scs)
    if anch:
        s_fix, p_fix = ins.fixed(scs, groups, cash0)
        s_rot, p_rot = ins.rotations(scs, groups, cash0)
    else:
        s_fix, p_fix, s_rot, p_rot = math.nan, math.nan, np.full(1, np.nan), np.full(1, np.nan)
    for s in scs:  # back to the rule, with the tie rule
        rescore(s, ins.strat(s.seg, s.seg.pos, cash0))
    gap = observed_gap(segs, d, real, cash0)
    phis = ja.country_phi(segs)
    g_ar = null_gaps(segs, d, "ar", lag, real, cash0, worlds, phis=phis)
    g_bb = null_gaps(segs, d, "bb", lag, real, cash0, worlds)
    n_calm = sum(s.calm_years for s in scs)
    drag = sum(s.calm for s in scs) / n_calm if n_calm else math.nan
    acf = ja.acf_pairs([logx(s) for s in segs])[0]
    res = Result(label, d, scs, eps, anch, linked, lines, s_rule, p_rule, s_fix, p_fix, s_rot,
                 p_rot, gap, g_ar, g_bb, drag, acf)  # fmt: skip
    judge(res)
    return res


def judge(r: Result) -> None:
    nonzero = sum(1 for v in ins.cvals(r.anch, lambda e: e.ins) if v != 0)
    ins_ok = (
        bool(r.anch)
        and ins.ok(ins.cvals(r.anch, lambda e: e.ins))
        and ins.ok(ins.cvals(r.linked, lambda e: e.ins))
    )
    pn = r.p_null
    if nonzero < TOO_FEW:
        r.verdict = "Too few falls"
    elif not ins_ok:
        r.verdict = "Does not hold"
    elif pn < 0.05:
        r.verdict = "Holds"
    elif pn < 0.10:
        r.verdict = "In between"
    else:
        r.verdict = "Holds only as lower exposure"
    k, n = r.head
    r.quals = [
        "at the claimed strength" if n and k / n >= 0.80 else "weaker than claimed",
        "kept after the rebound" if r.anch and ins.ok(ins.cvals(r.anch, lambda e: e.net))
        else "handed back in the rebound",
        "cheaper than holding less" if r.p_rule < r.p_fix else "not cheaper than holding less",
    ]  # fmt: skip


def trimmed(segs: Sequence[ins.Seg], lag: int) -> list[ins.Seg]:
    """stale-checks-1's trim: drop each segment's first scored year; lag 1 keeps the rule's
    positions, lag 2 uses the signal of the year before."""
    out = []
    for s in segs:
        pos = s.pos[1:] if lag == 1 else s.pos[:-1]
        out.append(ins.Seg(s.iso, s.years[1:], s.r[1:], s.b[1:], s.pi[1:], pos))
    return out


def reading_l2(l1: Result, l2: Result) -> str:
    l2_ins = ins.ok(ins.cvals(l2.anch, lambda e: e.ins)) and ins.ok(
        ins.cvals(l2.linked, lambda e: e.ins)
    )
    if l2.p_null < 0.05 and l2_ins:
        return "timing does not rest on the last year alone"
    if l2.p_null >= 0.10 and l1.p_null < 0.05:
        return "timing rests on the last year's return"
    return "in between / not read"


# --- per country (description) ---


@dataclass
class CountryRow:
    iso: str
    years: str
    n_years: int
    acf: float
    eps: int
    wins: int
    ties: int
    s_rule: float
    s_fix: float
    s_rot: float
    gap: float
    p_ar: float


def country_rows(r: Result, worlds: int = WORLDS) -> list[CountryRow]:
    out = []
    for iso in sorted({s.seg.iso for s in r.scs}):
        segs = [s.seg for s in r.scs if s.seg.iso == iso]
        eps = [e for s in r.scs if s.seg.iso == iso for e in s.eps]
        rule, rot, fix, g, n = observed_gap(segs, r.d, False, False)
        p = p_ge(null_gaps(segs, r.d, "ar", worlds=worlds), g) if n else math.nan
        out.append(CountryRow(
            iso, f"{segs[0].years[1]}-{segs[-1].years[-1]}", sum(len(s.pos) for s in segs),
            ja.acf_pairs([logx(s) for s in segs])[0], len(eps),
            sum(1 for e in eps if e.ins > 0), sum(1 for e in eps if e.ins == 0), rule, fix, rot,
            g, p,
        ))  # fmt: skip
    return out


# --- report ---


def q(a: np.ndarray) -> str:
    v = a[~np.isnan(a)]
    if not len(v):
        return "-"
    return f"{np.median(v):+.3f} ({np.quantile(v, 0.05):+.3f} to {np.quantile(v, 0.95):+.3f})"


SUM_HEAD = [
    "| Run | d | Episodes | Anchored / linked | I > 0 (anchored, ties against) | Per episode: "
    "I > 0 / ties / n | S anchored: rule / fixed / rotations (p_rot) | Gap G per episode | "
    "p AR(1) / BB | Premium rule / fixed | Calm drag a year | Verdict |",
    "|---|---:|---:|---|---|---|---|---:|---|---|---:|---|",
]


def sum_row(r: Result) -> str:
    k, n = r.head
    pk, pz, pn = r.per_ep
    return (
        f"| {r.label} | {r.d:.1%} | {len(r.eps)} | {len(r.anch)} / {len(r.linked)} | {k} of {n} "
        f"| {pk} / {pz} / {pn} | {r.s_rule:.2f} / {r.s_fix:.2f} / {np.nanmedian(r.s_rot):.2f} "
        f"({r.p_rot:.3f}) | {r.gap[3]:+.3f} | {r.p_ar:.3f} / {r.p_bb:.3f} | {r.p_rule:.2f} / "
        f"{r.p_fix:.2f} | {r.drag:+.2f} | {r.verdict} ({'; '.join(r.quals)}) |"
    )


def detail(r: Result, full: bool) -> list[str]:
    segs = [s.seg for s in r.scs]
    pos = np.concatenate([s.pos for s in segs]) if segs else np.zeros(0)
    L = [f"### {r.label} (d {r.d:.1%})\n"]
    L.append(
        f"Segments {len(segs)} in {len({s.iso for s in segs})} countries, "
        f"{sum(len(s.pos) for s in segs)} country-years; mean position {pos.mean():.2f}; "
        f"pooled lag-1 acf of log excess returns over bills {r.acf:+.3f}.\n"
    )
    L += [*i1.TEST_HEAD, *r.lines.values(), ""]
    L.append(
        f"- Per-episode S: rule {r.gap[0]:.3f}, fixed {r.gap[2]:.3f}, rotations {r.gap[1]:.3f}; "
        f"gap G {r.gap[3]:+.3f}. AR(1) worlds G median (5-95%) {q(r.g_ar)}, p {r.p_ar:.3f}; "
        f"block bootstrap {q(r.g_bb)}, p {r.p_bb:.3f}. **p_null {r.p_null:.3f}.**\n"
    )
    if full:
        L += ["| Country | Peak | Trough | Depth | Years | Hold | I | S | B | N |",
              "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
        for e in sorted(r.eps, key=lambda x: (x.peak, x.series)):
            L.append(
                f"| {NAMES[e.series[:3]]} | {e.peak.year} | {e.trough.year} | {e.depth:.1%} | "
                f"{e.trough.year - e.peak.year} | {e.hold:+.1f} | {e.ins:+.1f} | "
                f"{e.share:+.2f} | {e.rebound:+.1f} | {e.net:+.1f} |"
            )
        L.append("")
        L += ["| Anchored cluster | Episodes | Countries | Mean I | Mean S | Mean N |",
              "|---|---:|---|---:|---:|---:|"]  # fmt: skip
        for g in r.anch:
            lo, hi = min(x.peak.year for x in g), max(x.trough.year for x in g)
            L.append(
                f"| {lo}-{hi} | {len(g)} | {', '.join(sorted({x.series[:3] for x in g}))} | "
                f"{i1.cmean(g, lambda e: e.ins):+.1f} | {i1.cmean(g, lambda e: e.share):+.2f} | "
                f"{i1.cmean(g, lambda e: e.net):+.1f} |"
            )
        L.append("")
    return L


def tries_row(v: str, lo: int, hi: int, sh: str, tot: str, mdd: str, fl: str) -> str:
    return (f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | insure-check | train | "
            f"{lo}-12-31 | {hi}-12-31 | {sh} | {tot} | {mdd} | {fl} |\n")  # fmt: skip


def per_country_tries(r: Result) -> list[str]:
    rows = []
    for iso in sorted({s.seg.iso for s in r.scs}):
        ss = [s.seg for s in r.scs if s.seg.iso == iso]
        rr = np.concatenate([ins.strat(s, s.pos) for s in ss])
        eq = np.cumprod(1 + rr)
        sh = rr.mean() / rr.std() if rr.std() > 0 else 0.0
        mdd = i1.maxdd(np.concatenate([[1.0], eq]))
        flips = sum(float(np.abs(np.diff(s.pos)).sum()) for s in ss) / len(rr)
        rows.append(
            tries_row(
                f"tsmom12a@insure-jstbonds-{iso}",
                ss[0].years[1],
                ss[-1].years[-1],
                f"{sh:.2f}",
                f"{eq[-1] - 1:+.1%}",
                f"{mdd:.1%}",
                f"{flips:.2f}",
            )
        )
    return rows  # fmt: skip


def check_tries(key: str, r: Result) -> str:
    k, n = r.head
    v = (f"tsmom12a@insure-jstbonds-{key}: {r.label}; d {r.d:.1%}; {r.verdict}; I > 0 in {k} of "
         f"{n} anchored falls, S {r.s_rule:.2f} vs fixed {r.s_fix:.2f}, G {r.gap[3]:+.3f} "
         f"(p AR {r.p_ar:.3f}, BB {r.p_bb:.3f}), P {r.p_rule:.2f}")  # fmt: skip
    segs = [s.seg for s in r.scs]
    return tries_row(v, min(s.years[1] for s in segs), max(s.years[-1] for s in segs),
                     "-", "-", "-", "-")  # fmt: skip


def log_tries(rows: Sequence[str]) -> int:
    import harness

    text = harness.TRIES.read_text()
    new = [x for x in rows if f"| {IDEA} | {x.split(' | ')[2].split(':')[0]}" not in text]
    with harness.TRIES.open("a") as f:
        f.writelines(new)
    return len(new)


# --- main ---


def counts_table(jst: Jst) -> list[str]:
    L = [
        "| Sample | d | Episodes | Multi-year | Anchored clusters | Linked clusters | "
        "Unfinished falls | Countries with a fall |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for cfg in (CONFIGS[0], CONFIGS[1]):
        segs = build(cfg, jst)
        cs = fall_counts(segs, anchor_segs(cfg, jst))
        for c in cs:
            L.append(f"| {cfg.key} | {c.d:.1%} | {c.episodes} | {c.multi_year} | {c.anchored} | "
                     f"{c.linked} | {c.open_falls} | {c.countries} |")  # fmt: skip
        if cfg.key == "primary":
            j = choose(cs)
            n_years = sum(len(s.pos) for s in segs)
            L.insert(
                0,
                f"Primary: {len(segs)} segments, {len({s.iso for s in segs})} countries, "
                f"{n_years} scored country-years. **Chosen d = {LADDER[j]:.1%}.**\n",
            )
    return L  # fmt: skip


def main(argv: Sequence[str]) -> None:
    jst = load_jst()
    if argv and argv[0] == "counts":
        print("\n".join(counts_table(jst)))
        return
    base = CONFIGS[0]
    j0 = choose(fall_counts(build(base, jst), anchor_segs(base, jst)))
    res: dict[str, Result] = {}
    for cfg in CONFIGS:
        j = j0 + cfg.rung
        if not 0 <= j < len(LADDER):
            continue
        segs = build(cfg, jst)
        res[cfg.key] = run(cfg.label, segs, anchor_segs(cfg, jst), LADDER[j], cfg.real, cfg.cash0)
        print(sum_row(res[cfg.key]), flush=True)
    stale: dict[str, tuple[Result, Result, str]] = {}
    for key in ("primary", "overlap"):
        cfg = next(c for c in CONFIGS if c.key == key)
        segs, anc = build(cfg, jst), anchor_segs(cfg, jst)
        l1 = run(f"{key}: L1 signal year t-1 (trimmed)", trimmed(segs, 1), anc, LADDER[j0])
        l2 = run(f"{key}: L2 signal year t-2 (trimmed)", trimmed(segs, 2), anc, LADDER[j0], lag=2)
        stale[key] = (l1, l2, reading_l2(l1, l2))
        print(sum_row(l1), sum_row(l2), stale[key][2], sep="\n", flush=True)
    crow = {k: country_rows(res[k]) for k in ("primary", "overlap")}
    L = [
        "# insure-jstbonds-1: trend's crash insurance on JST annual government-bond returns\n",
        "Generated by `uv run python -I research/lib/insurejstbonds1.py`. Card: "
        "`research/cards/insure-jstbonds-1.md`. Statistics only (JST R6, CC BY-NC-SA 4.0; cite "
        "Jorda, Schularick and Taylor 2017). Log points = 100 x ln; I, B, N, C are rule minus "
        f"holding. Rotations {ins.ROTATIONS} (anchored S), {OBS_ROT} (observed G), {SIM_ROT} "
        f"per world; {WORLDS} worlds per null, seed {SEED}; block bootstrap mean block "
        f"{BLOCK:.0f} years; ties |I| < {TIE:g} set to 0.\n",
        "## Fall counts on the holding index (threshold rule)\n",
        *counts_table(jst), "",
        "## Summary\n", *SUM_HEAD, *[sum_row(r) for r in res.values()], "",
        "## Year-older signal control (stale-checks-1 (b))\n", *SUM_HEAD,
    ]  # fmt: skip
    for l1, l2, _ in stale.values():
        L += [sum_row(l1), sum_row(l2)]
    L.append("")
    for key, (_, _, rd) in stale.items():
        L.append(f"- {key}: **{rd}**.")
    L.append("")
    for key, rows in crow.items():
        L += [
            f"## Per country ({key}, description; AR(1) p from the country's own worlds)\n",
            "| Country | Years | Scored years | Lag-1 acf | Episodes | I > 0 | Ties | "
            "S rule / fixed / rotations (per episode) | Gap G | p AR(1) |",
            "|---|---|---:|---:|---:|---:|---:|---|---:|---:|",
        ]
        for c in rows:
            ss = f"{c.s_rule:.2f} / {c.s_fix:.2f} / {c.s_rot:.2f}" if c.eps else "-"
            L.append(f"| {NAMES[c.iso]} | {c.years} | {c.n_years} | {c.acf:+.2f} | {c.eps} | "
                     f"{c.wins} | {c.ties} | {ss} | {c.gap:+.3f} | {c.p_ar:.3f} |")  # fmt: skip
        L.append("")
    L.append("## Detail\n")
    for key, r in res.items():
        L += detail(r, full=key in ("primary", "overlap"))
    for l1, l2, _ in stale.values():
        L += detail(l1, False) + detail(l2, False)
    OUT.write_text("\n".join(L) + "\n")
    rows = per_country_tries(res["primary"])
    rows += [check_tries(k, r) for k, r in res.items() if k != "primary"]
    rows += [check_tries(f"{k}-{lab}", r) for k, (l1, l2, _) in stale.items()
             for lab, r in (("L1", l1), ("L2", l2))]  # fmt: skip
    print(f"wrote {OUT}; tries rows added: {log_tries(rows)}")


if __name__ == "__main__":
    main(sys.argv[1:])
