"""insure-1870-1: does trend's crash insurance hold on 1870-1965 annual data? Card:
research/cards/insure-1870-1.md.

    uv run python -I research/lib/insure1870.py

Annual analogue of `tsmom12` on the Jorda-Schularick-Taylor Macrohistory Database R6 (cached by
data-long-4, read-only, never committed): hold equities in year t if the equity total return of
year t-1 beat the bill, else bills. Falls of 25%+ on year-end closes (insure-1's zigzag), the
insurance I, rebound B, calm C and premium P of insure-1, clusters and tests of insure-2, a
random-date rotation placebo and a fixed-exposure control. Decisive sample: US years to 1926,
other countries to 1965 (data the insurance claim never saw). Writes
research/results/insure-1870-1.md (statistics only) and `insure-check` rows to tries.md (once).
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import insure1 as i1  # noqa: E402

IDEA = "insure-1870-1"
COST = 0.0002  # a side
MIN_YEARS = 10  # scored years a segment needs
US_LAST, OTHER_LAST = 1926, 1965  # decisive sample: before insure-1 (US) and insure-2 (others)
ROTATIONS, SEED = 1_000, 0
OUT = HERE.parent / "results" / "insure-1870-1.md"
NAMES = {
    "AUS": "Australia", "BEL": "Belgium", "CHE": "Switzerland", "DEU": "Germany",
    "DNK": "Denmark", "ESP": "Spain", "FIN": "Finland", "FRA": "France", "GBR": "UK",
    "ITA": "Italy", "JPN": "Japan", "NLD": "Netherlands", "NOR": "Norway", "PRT": "Portugal",
    "SWE": "Sweden", "USA": "US",
}  # fmt: skip


# --- segments and the rule ---


@dataclass
class Seg:
    iso: str
    years: list[int]  # base (signal) year first, then the scored years
    r: np.ndarray  # equity total return of each scored year
    b: np.ndarray  # bill return of each scored year
    pi: np.ndarray  # CPI inflation of each scored year
    pos: np.ndarray  # rule position of each scored year (1 equities, 0 bills)

    @property
    def name(self) -> str:
        return f"{self.iso}-{self.years[0]}"


def segments(
    iso: str,
    eq: dict[int, float],
    bill: dict[int, float],
    cpi: dict[int, float],
    last: int,
    drop: frozenset[int] = frozenset(),
) -> list[Seg]:
    """Maximal runs of consecutive usable years (eq_tr and bill_rate present, not dropped, up to
    `last`); the first year of a run is the signal year only. Position in year t: 1 if
    eq(t-1) > bill(t-1). Runs with fewer than MIN_YEARS scored years are dropped."""
    ok = sorted(y for y in eq if y in bill and y <= last and y not in drop)
    runs: list[list[int]] = []
    for y in ok:
        if runs and y == runs[-1][-1] + 1:
            runs[-1].append(y)
        else:
            runs.append([y])
    out = []
    for run in runs:
        if len(run) - 1 < MIN_YEARS:
            continue
        sc = run[1:]
        pos = np.array([1.0 if eq[y - 1] > bill[y - 1] else 0.0 for y in sc])
        pi = np.array(
            [cpi[y] / cpi[y - 1] - 1 if y in cpi and y - 1 in cpi else math.nan for y in sc]
        )
        out.append(
            Seg(iso, run, np.array([eq[y] for y in sc]), np.array([bill[y] for y in sc]), pi, pos)
        )
    return out


def strat(seg: Seg, pos: np.ndarray, cash0: bool = False, cost: float = COST) -> np.ndarray:
    """pos x eq + (1 - pos) x bill - cost x |change of pos| (no cost in the first year)."""
    flips = np.abs(np.diff(pos, prepend=pos[0]))
    return pos * seg.r + (1 - pos) * (0.0 if cash0 else seg.b) - cost * flips


def hold_index(seg: Seg, real: bool = False) -> np.ndarray:
    g = (1 + seg.r) / (1 + seg.pi) if real else 1 + seg.r
    return np.concatenate([[1.0], np.cumprod(g)])


# --- episodes and scoring ---


@dataclass
class Scored:
    seg: Seg
    eps: list[i1.Episode]
    calm: float
    calm_years: int
    open_peak: int | None
    mask: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=bool))


def _ye(y: int) -> date:
    return date(y, 12, 31)


def episodes(seg: Seg, down: float, up: float, real: bool = False) -> Scored:
    """Zigzag on the year-end holding index; I over (peak, trough], B the year after the trough
    (bounded by the next peak and the segment end), C the rest; scored with the rule."""
    px = hold_index(seg, real)
    pairs, open_pk = i1.zigzag(px, down, up)
    n = len(px)
    tri = [(a, b, min(b + 1, n - 1, pairs[j + 1][0] if j + 1 < len(pairs) else n - 1))
           for j, (a, b) in enumerate(pairs)]  # fmt: skip
    eps = []
    for a, b, e in tri:
        hold = 100 * math.log(px[b] / px[a])
        eps.append(i1.Episode(seg.name, _ye(seg.years[a]), _ye(seg.years[b]),
                              1 - px[b] / px[a], hold, 0.0, 0.0, 0.0, idx=(a, b, e)))  # fmt: skip
    mask = np.zeros(n, dtype=bool)
    for a, _, e in tri:
        mask[a + 1 : e + 1] = True
    sc = Scored(seg, eps, 0.0, int((~mask[1:]).sum()),
                seg.years[open_pk] if open_pk is not None else None, mask)  # fmt: skip
    rescore(sc, strat(seg, seg.pos))
    return sc


def diff_cum(seg: Seg, rule: np.ndarray) -> np.ndarray:
    d = np.zeros(len(rule) + 1)
    d[1:] = 100 * (np.log1p(rule) - np.log1p(seg.r))
    return np.cumsum(d)


def rescore(sc: Scored, rule: np.ndarray) -> None:
    """Fill I, B, C (and the rule's log change) for a rule return vector; checks the identity."""
    cum = diff_cum(sc.seg, rule)
    for e in sc.eps:
        a, b, x = e.idx
        e.ins = float(cum[b] - cum[a])
        e.rebound = float(cum[x] - cum[b])
        e.rule = e.hold + e.ins
    d = np.diff(cum)
    sc.calm = float(d[~sc.mask[1:]].sum())
    total = sum(e.ins + e.rebound for e in sc.eps) + sc.calm
    if abs(total - cum[-1]) > 1e-6:
        raise AssertionError(f"{sc.seg.name}: decomposition {total} != {cum[-1]}")


def premium(scs: Sequence[Scored]) -> float:
    si = sum(e.ins for s in scs for e in s.eps)
    sb = sum(e.rebound for s in scs for e in s.eps)
    return -(sb + sum(s.calm for s in scs)) / si if si else math.nan


# --- clusters ---


def anchored(anchors: Sequence[i1.Episode], eps: Sequence[i1.Episode]) -> list[list[i1.Episode]]:
    """insure-geo's anchoring: an episode joins the anchor whose [peak, trough] holds its trough,
    else its peak; the rest are linked. Anchors are labels: a group holds only `eps`."""
    groups: dict[int, list[i1.Episode]] = {}
    rest = []
    for e in eps:
        j = next((k for k, g in enumerate(anchors) if g.peak <= e.trough <= g.trough), None)
        if j is None:
            j = next((k for k, g in enumerate(anchors) if g.peak <= e.peak <= g.trough), None)
        if j is None:
            rest.append(e)
        else:
            groups.setdefault(j, []).append(e)
    return sorted([*groups.values(), *i1.link(rest)], key=lambda g: min(x.peak for x in g))


def cvals(groups: Sequence[Sequence[i1.Episode]], f: Callable[[i1.Episode], float]) -> list[float]:
    return [i1.cmean(g, f) for g in groups]


# --- placebo ---


def rotations(scs: Sequence[Scored], groups_of: Callable[[], list[list[i1.Episode]]],
              cash0: bool = False) -> tuple[np.ndarray, np.ndarray]:  # fmt: skip
    """Mean anchored-cluster S and pooled P under 1,000 common rotations of the positions."""
    lmax = max(len(s.seg.pos) for s in scs)
    ks = np.random.default_rng(SEED).integers(1, lmax, size=ROTATIONS)
    s_out, p_out = np.zeros(ROTATIONS), np.zeros(ROTATIONS)
    for j, k in enumerate(ks):
        for s in scs:
            rolled = np.roll(s.seg.pos, int(k) % len(s.seg.pos))
            rescore(s, strat(s.seg, rolled, cash0))
        s_out[j] = float(np.mean(cvals(groups_of(), lambda e: e.share)))
        p_out[j] = premium(scs)
    for s in scs:
        rescore(s, strat(s.seg, s.seg.pos, cash0))
    return s_out, p_out


def fixed(scs: Sequence[Scored], groups_of: Callable[[], list[list[i1.Episode]]],
          cash0: bool = False) -> tuple[float, float]:  # fmt: skip
    for s in scs:
        x = np.full(len(s.seg.pos), s.seg.pos.mean())
        rescore(s, strat(s.seg, x, cash0, cost=0.0))
    out = float(np.mean(cvals(groups_of(), lambda e: e.share))), premium(scs)
    for s in scs:
        rescore(s, strat(s.seg, s.seg.pos, cash0))
    return out


# --- data ---


def load_jst() -> dict[str, dict[str, dict[int, float]]]:
    import long_macro_build as lmb

    j = lmb._jst()
    return {
        v: {iso: {d.year: x for d, x in ser} for iso, ser in j[v].items()}
        for v in ("eq_tr", "bill_rate", "cpi")
    }


def hyper_years(cpi: dict[int, float]) -> frozenset[int]:
    return frozenset(y for y in cpi if y - 1 in cpi and cpi[y] / cpi[y - 1] > 1.5)


@dataclass
class Config:
    key: str
    label: str
    down: float = 0.25
    up: float = 0.25
    real: bool = False
    cash0: bool = False
    full: bool = False
    drop_hyper: bool = False


CONFIGS = [
    Config("primary", "Decisive: US to 1926, others to 1965 (25%, nominal, cash at bills)"),
    Config("full", "Check 1: full span 1870-2020", full=True),
    Config("real", "Check 2: events on the real index", real=True),
    Config("t20", "Check 3a: 20% fall / 20% rise", down=0.20, up=0.20),
    Config("t40", "Check 3b: 40% fall / 25% rise", down=0.40, up=0.25),
    Config("cash0", "Check 4: cash at 0 when out", cash0=True),
    Config("nohyper", "Check 5: years with CPI > 50% dropped", drop_hyper=True),
]


def build(cfg: Config, jst: dict[str, dict[str, dict[int, float]]]) -> list[Seg]:
    out = []
    for iso in sorted(jst["eq_tr"]):
        cpi = jst["cpi"].get(iso, {})
        last = 2020 if cfg.full else (US_LAST if iso == "USA" else OTHER_LAST)
        drop = hyper_years(cpi) if cfg.drop_hyper else frozenset()
        out += segments(iso, jst["eq_tr"][iso], jst["bill_rate"][iso], cpi, last, drop)
    return out


# --- one configuration ---


@dataclass
class Result:
    cfg: Config
    scs: list[Scored]
    eps: list[i1.Episode]
    anch: list[list[i1.Episode]]
    linked: list[list[i1.Episode]]
    lines: dict[str, str]
    share_head: tuple[int, int]
    share_ep: tuple[int, int, int]
    s_rule: float
    p_rule: float
    s_fix: float
    p_fix: float
    s_rot: np.ndarray
    p_rot: np.ndarray
    drag: dict[str, float]
    verdict: str = ""
    quals: list[str] = field(default_factory=list)


def ok(vals: Sequence[float]) -> bool:
    _, _, p = i1.sign_test(vals)
    _, bp, _, _ = i1.boot(vals)
    return p < 0.05 and bp < 0.05


def run(
    cfg: Config, jst: dict[str, dict[str, dict[int, float]]], segs: list[Seg] | None = None
) -> Result:
    """`segs` (optional, stale-checks-1): score these segments instead of `build(cfg, jst)`."""
    segs = build(cfg, jst) if segs is None else segs
    scs = [episodes(s, cfg.down, cfg.up, cfg.real) for s in segs]
    for s in scs:
        rescore(s, strat(s.seg, s.seg.pos, cfg.cash0))
    eps = [e for s in scs for e in s.eps]
    us_last = 2020 if cfg.full else OTHER_LAST
    us = segments("USA", jst["eq_tr"]["USA"], jst["bill_rate"]["USA"], jst["cpi"]["USA"], us_last)
    anchors = [e for u in us for e in episodes(u, cfg.down, cfg.up, cfg.real).eps]

    def groups() -> list[list[i1.Episode]]:
        return anchored(anchors, eps)

    anch, linked = groups(), i1.link(eps)
    lines = {
        "I anchored": i1.test_line("I, anchored clusters", anch, lambda e: e.ins),
        "I linked": i1.test_line("I, linked clusters", linked, lambda e: e.ins),
        "N anchored": i1.test_line("N, anchored clusters", anch, lambda e: e.net),
        "I episodes": i1.test_line(
            "I, episodes (no clustering)", [[e] for e in eps], lambda e: e.ins
        ),  # fmt: skip
    }
    iv = cvals(anch, lambda e: e.ins)
    s_rule = float(np.mean(cvals(anch, lambda e: e.share)))
    p_rule = premium(scs)
    s_fix, p_fix = fixed(scs, groups, cfg.cash0)
    s_rot, p_rot = rotations(scs, groups, cfg.cash0)
    calm_us = [s for s in scs if s.seg.iso == "USA"]
    calm_ot = [s for s in scs if s.seg.iso != "USA"]

    def drag(ss: Sequence[Scored]) -> float:
        n = sum(s.calm_years for s in ss)
        return sum(s.calm for s in ss) / n if n else math.nan

    res = Result(
        cfg, scs, eps, anch, linked, lines,
        (sum(1 for v in iv if v > 0), len(iv)),
        (sum(1 for e in eps if e.ins > 0), sum(1 for e in eps if e.ins == 0), len(eps)),
        s_rule, p_rule, s_fix, p_fix, s_rot, p_rot,
        {"all": drag(scs), "US": drag(calm_us), "other": drag(calm_ot)},
    )  # fmt: skip
    judge(res)
    return res


def p_s(r: Result) -> float:
    return float((r.s_rot >= r.s_rule).mean())


def p_p(r: Result) -> float:
    return float((r.p_rot <= r.p_rule).mean())


def judge(r: Result) -> None:
    ins = ok(cvals(r.anch, lambda e: e.ins)) and ok(cvals(r.linked, lambda e: e.ins))
    ps, pp = p_s(r), p_p(r)
    if not ins:
        r.verdict = "Does not hold"
    elif ps < 0.05:
        r.verdict = "Holds"
    elif ps < 0.10:
        r.verdict = "In between"
    else:
        r.verdict = "Holds only as lower exposure"
    k, n = r.share_head
    r.quals = [
        "at the claimed strength" if n and k / n >= 0.80 else "weaker than claimed",
        "kept after the rebound" if ok(cvals(r.anch, lambda e: e.net)) else
        "handed back in the rebound",
        "timing, not just exposure" if ps < 0.05 and pp < 0.05 and r.p_rule < r.p_fix else
        "exposure, not timing" if ps >= 0.10 and pp >= 0.10 else "in between (vs holding less)",
    ]  # fmt: skip


# --- report ---


def fmt_result(r: Result, detail: bool) -> list[str]:
    k, n = r.share_head
    pk, pz, pn = r.share_ep
    segs = [s.seg for s in r.scs]
    L = [f"### {r.cfg.label}\n"]
    L.append(
        f"Segments {len(segs)} in {len({s.iso for s in segs})} countries, "
        f"{sum(len(s.pos) for s in segs)} country-years; episodes {len(r.eps)}, "
        f"anchored clusters {len(r.anch)}, linked clusters {len(r.linked)}. Mean position "
        f"{np.mean(np.concatenate([s.pos for s in segs])):.2f}.\n"
    )
    L += [*i1.TEST_HEAD, *r.lines.values(), ""]
    L.append(
        f"- **Verdict: {r.verdict}** ({'; '.join(r.quals)}).\n"
        f"- Lost less than holding (I > 0) in **{k} of {n}** anchored effective falls "
        f"({k / n:.2f}; ties count against); per episode {pk} of {pn}, {pz} ties (I = 0, "
        f"fully in).\n"
        f"- Share avoided (mean anchored cluster S): rule **{r.s_rule:.2f}**, fixed exposure "
        f"{r.s_fix:.2f}, random dates {np.median(r.s_rot):.2f} (median; 5-95% "
        f"{np.quantile(r.s_rot, 0.05):.2f} to {np.quantile(r.s_rot, 0.95):.2f}), p_S "
        f"{p_s(r):.3f}.\n"
        f"- Premium P: rule **{r.p_rule:.2f}**, fixed {r.p_fix:.2f}, random dates "
        f"{np.median(r.p_rot):.2f} (median), p_P {p_p(r):.3f}.\n"
        f"- Calm-year drag (C per calm year, rule minus holding, log points): all "
        f"{r.drag['all']:+.2f}, US {r.drag['US']:+.2f}, other {r.drag['other']:+.2f}.\n"
    )
    if detail:
        L += [
            "| Country | Peak | Trough | Depth | Years | Hold | I | S | B | N |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for e in sorted(r.eps, key=lambda x: (x.peak, x.series)):
            L.append(
                f"| {NAMES[e.series[:3]]} | {e.peak.year} | {e.trough.year} | {e.depth:.0%} | "
                f"{e.trough.year - e.peak.year} | {e.hold:+.0f} | {e.ins:+.1f} | "
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
        L += ["| Segment | Years | Mean position | Episodes | Calm years | C | Open fall from |",
              "|---|---|---:|---:|---:|---:|---|"]  # fmt: skip
        for s in r.scs:
            L.append(
                f"| {NAMES[s.seg.iso]} | {s.seg.years[1]}-{s.seg.years[-1]} | "
                f"{s.seg.pos.mean():.2f} | {len(s.eps)} | {s.calm_years} | {s.calm:+.0f} | "
                f"{s.open_peak or '-'} |"
            )
        L.append("")
    return L


def country_rows(r: Result) -> list[str]:
    rows = []
    for iso in sorted({s.seg.iso for s in r.scs}):
        ss = [s.seg for s in r.scs if s.seg.iso == iso]
        rr = np.concatenate([strat(s, s.pos) for s in ss])
        eq = np.cumprod(1 + rr)
        sh = rr.mean() / rr.std() if rr.std() > 0 else 0.0
        mdd = i1.maxdd(np.concatenate([[1.0], eq]))
        flips = sum(float(np.abs(np.diff(s.pos)).sum()) for s in ss) / len(rr)
        rows.append((f"tsmom12a@insure-1870-{iso}", ss[0].years[1], ss[-1].years[-1],
                     f"{sh:.2f}", f"{eq[-1] - 1:+.1%}", f"{mdd:.1%}", f"{flips:.2f}"))  # fmt: skip
    return [_row(*x) for x in rows]


def _row(v: str, lo: int, hi: int, sh: str, tot: str, mdd: str, fl: str) -> str:
    return (f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | insure-check | train | "
            f"{lo}-12-31 | {hi}-12-31 | {sh} | {tot} | {mdd} | {fl} |\n")  # fmt: skip


def check_row(r: Result) -> str:
    k, n = r.share_head
    v = (f"tsmom12a@insure-1870-check-{r.cfg.key}: {r.cfg.label}; {r.verdict}; I > 0 in {k} of "
         f"{n} anchored falls, S {r.s_rule:.2f} vs random {np.median(r.s_rot):.2f} "
         f"(p {p_s(r):.3f}), P {r.p_rule:.2f}")  # fmt: skip
    segs = [s.seg for s in r.scs]
    return _row(v, min(s.years[1] for s in segs), max(s.years[-1] for s in segs),
                "-", "-", "-", "-")  # fmt: skip


def log_tries(res: Sequence[Result]) -> int:
    import harness

    text = harness.TRIES.read_text()
    rows = country_rows(res[0]) + [check_row(r) for r in res[1:]]
    new = [x for x in rows if f"| {IDEA} | {x.split(' | ')[2].split(':')[0]}" not in text]
    with harness.TRIES.open("a") as f:
        f.writelines(new)
    return len(new)


def main() -> None:
    jst = load_jst()
    res = [run(c, jst) for c in CONFIGS]
    L = [
        "# insure-1870-1: trend's crash insurance on 1870-1965 annual data (JST R6)\n",
        "Generated by `uv run python -I research/lib/insure1870.py`. Card: "
        "`research/cards/insure-1870-1.md`. Statistics only (JST R6, CC BY-NC-SA 4.0; cite Jorda, "
        "Schularick and Taylor 2017). Log points = 100 x ln; I, B, N, C are rule minus holding. "
        f"Rotations {ROTATIONS}, seed {SEED}; bootstrap {i1.DRAWS:,} draws.\n",
        "## Summary\n",
        "| Run | Episodes | Anchored / linked clusters | I > 0 (anchored, ties against) | "
        "Share avoided: rule / fixed / random | p_S | Premium: rule / fixed / random | p_P | "
        "Calm drag a year | Verdict |",
        "|---|---:|---|---|---|---:|---|---:|---:|---|",
    ]
    for r in res:
        k, n = r.share_head
        L.append(
            f"| {r.cfg.label} | {len(r.eps)} | {len(r.anch)} / {len(r.linked)} | {k} of {n} | "
            f"{r.s_rule:.2f} / {r.s_fix:.2f} / {np.median(r.s_rot):.2f} | {p_s(r):.3f} | "
            f"{r.p_rule:.2f} / {r.p_fix:.2f} / {np.median(r.p_rot):.2f} | {p_p(r):.3f} | "
            f"{r.drag['all']:+.2f} | {r.verdict} ({'; '.join(r.quals)}) |"
        )
    L.append("")
    for j, r in enumerate(res):
        L += fmt_result(r, detail=j in (0, 1))
    OUT.write_text("\n".join(L) + "\n")
    print(f"wrote {OUT}; tries rows added: {log_tries(res)}")


if __name__ == "__main__":
    main()
