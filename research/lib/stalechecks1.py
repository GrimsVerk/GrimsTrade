"""stale-checks-1: are the pre-1926 insurance results artefacts of averaged or stale prices?
Card: research/cards/stale-checks-1.md.

    uv run python -I research/lib/stalechecks1.py [--log]   # cache root: macro.cache_root()

(a) US 1885-1925 monthly: Shiller's averaged (Cowles) prices against Schwert's (1990) appendix
    index, whose 1885-03..1925-12 price changes are those of his Dow Jones composite
    (end-of-month closes). The transcription `<cache_root>/stale-checks-1/schwert-appendix-
    1884-1926.csv` is not committed; `stalechecks1_ocr.py` rebuilds it from the cached PDF and
    the committed eye-read corrections.
(b) insure-1870-1's annual JST rule with the signal one year older.
(c) monthly `tsmom12` on AQR's 1877-1912 commodity aggregate, with and without a one-month
    execution delay.

Scoring is unchanged insure-1709-1 (monthly) and insure-1870-1 (annual) code; new here are the
loaders, the lagged null worlds and the report. Writes research/results/stale-checks-1.md
(statistics only) and, with --log, rows to tries.md (once).
"""

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402
import insure1709 as m9  # noqa: E402
import insure1870 as ins  # noqa: E402
import jstautocorr as ja  # noqa: E402

IDEA = "stale-checks-1"
OUT = harness.RESEARCH / "results" / "stale-checks-1.md"
WORLDS, SIM_WORLDS, SEED = 1_000, 1_000, 0
Levels = dict[int, float]
ym = m9.ym

# --- (a) data ---

SCHWERT_CSV = "schwert-appendix-1884-1926.csv"  # sha256 4ea58998...94cf3a78 (write-up)
A_FIRST, A_LAST = ym(1885, 2), ym(1925, 12)  # level months; returns 1885-03..1925-12
CLOSED = frozenset(ym(1914, k) for k in range(8, 12))  # NYSE closed Aug-Nov 1914


def load_schwert(path: Path) -> Levels:
    """year,month,index CSV transcribed from Schwert (1990), appendix 'Monthly Index of Common
    Stock Returns, 1802-1987'."""
    out: Levels = {}
    for line in path.read_text().splitlines()[1:]:
        y, mo, x = line.split(",")
        out[ym(int(y), int(mo))] = float(x)
    return out


def shiller_tr(mon: dict[tuple[int, int], tuple[float, float]], lo: int, hi: int) -> Levels:
    """Total-return levels from Shiller's monthly P and D: r_t = (P_t + D_t / 12) / P_{t-1} - 1."""
    out: Levels = {lo: 1.0}
    for m in range(lo + 1, hi + 1):
        p0, _ = mon[(m - 1) // 12, (m - 1) % 12 + 1]
        p1, d1 = mon[m // 12, m % 12 + 1]
        out[m] = out[m - 1] * (p1 + d1 / 12) / p0
    return out


def window(lev: Levels, lo: int = A_FIRST, hi: int = A_LAST) -> Levels:
    return {m: x for m, x in lev.items() if lo <= m <= hi and m not in CLOSED}


# --- (a) Working (1960) ---


def working_rho(m: int) -> float:
    """Lag-1 acf of changes of m-point averages of a random walk (Working 1960)."""
    return (m * m - 1) / (2 * (2 * m * m + 1))


def sim_rho(n_months: int, steps: int = 25, seed: int = SEED) -> tuple[float, float, float]:
    """Simulated lag-1 acf of monthly changes of (mean, midrange, last) of a Gaussian random walk
    with `steps` daily closes a month."""
    rng = np.random.default_rng(seed)
    px = np.cumsum(rng.standard_normal(n_months * steps)).reshape(n_months, steps)
    out = []
    for v in (px.mean(axis=1), (px.max(axis=1) + px.min(axis=1)) / 2, px[:, -1]):
        d = np.diff(v)
        d = d - d.mean()
        out.append(float((d[1:] * d[:-1]).sum() / (d * d).sum()))
    return out[0], out[1], out[2]


# --- monthly machinery (insure-1709-1, unchanged) ---


def segs_of(name: str, lev: Levels, lag: int = 0) -> list[m9.Seg]:
    out = []
    for run_ in m9.segments(lev):
        s = m9.build_seg(name, run_, m9.holding_returns(lev, run_), lag)
        if s is not None:
            out.append(s)
    return out


def one_period(name: str, lev: Levels, label: str) -> m9.PStat:
    return m9.period_stats(lev, m9.Period(name, label, min(lev), max(lev), False, "-"))


def null_gaps(lev: Levels, st: m9.PStat, kind: str, lag: int, worlds: int, seed: int) -> np.ndarray:
    """Gap G in synthetic worlds on the same month runs: Gaussian AR(1) with the series' own mean,
    sd and lag-1 acf ('ar1'), or a stationary block bootstrap of its own returns ('bb'); the
    rule with the same signal lag. insure-1709-1's world_gap with a lag."""
    rng = np.random.default_rng(seed)
    runs = m9.segments(lev)
    per = [np.zeros(len(r), dtype=int) for r in runs]
    m, sd = np.array([st.mean]), np.array([st.sd])
    phi = np.array([float(np.clip(st.acf1, -0.9, 0.9))])
    pool = [m9.logrets(lev, sorted(lev))[1]]
    out = np.full(worlds, np.nan)
    for w in range(worlds):
        segs, prs = [], []
        for run_, p in zip(runs, per, strict=True):
            x = (
                m9.bb_path(rng, p[1:], pool)
                if kind == "bb"
                else m9.ar1_path(rng, p[1:], m, sd, phi)
            )
            s = m9.build_seg(st.p.series, run_, np.concatenate([[np.nan], np.expm1(x)]), lag)
            if s is not None:
                segs.append(s)
                prs.append(m9.pairs_of(s.r))
        if segs and any(prs):
            out[w] = m9.timing(segs, prs, m9.offsets(segs, m9.WORLD_ROT, rng)).gap
    return out


def p_ge(g: np.ndarray, obs: float) -> float:
    g = g[np.isfinite(g)]
    return float((g >= obs - 1e-12).mean()) if len(g) else math.nan


def hold_sharpe(ev: m9.Eval) -> float:
    r = np.concatenate([s.r[1:] for s in ev.segs])
    return float(r.mean() / r.std() * math.sqrt(12)) if r.std() > 0 else 0.0


@dataclass
class Run:
    key: str
    label: str
    ev: m9.Eval
    nulls: dict[str, np.ndarray]

    @property
    def gap(self) -> float:
        return self.ev.t.gap


def run_row(r: Run) -> str:
    ev, t = r.ev, r.ev.t
    k, n, p, _, bp = ev.tests(lambda e: e.ins)
    nl = "; ".join(
        f"{kind.upper()} {p_ge(g, r.gap):.3f} (median {np.nanmedian(g):+.3f})"
        for kind, g in r.nulls.items()
    )
    return (
        f"| {r.label} | {ev.n} | {k} of {n} | {p:.3g} / {bp:.3f} | "
        f"{t.rule.s_mean[0]:+.2f} / {t.fixed.s_mean[0]:+.2f} / "
        f"{float(np.median(t.rot.s_mean)):+.2f} ({t.p_rot:.3f}) | {t.gap:+.3f} | "
        f"{nl or '-'} | {t.rule.prem[0]:.2f} / {t.fixed.prem[0]:.2f} | "
        f"{m9.sharpe_row(ev)[2]:.2f} / {hold_sharpe(ev):.2f} | {m9.verdict(ev, 1.0)} |"
    )


RUN_HEAD = [
    "| Run | Falls | I > 0 | Sign p / boot p | S rule / fixed / random (p_rot) | Gap G | "
    "Null p (worlds with G >= observed) | P rule / fixed | Sharpe rule / hold | Verdict words "
    "(no AR null) |",
    "|---|---:|---|---|---|---:|---|---|---|---|",
]


def eps_rows(r: Run) -> list[str]:
    out = []
    for e in sorted(r.ev.eps, key=lambda x: x.peak):
        out.append(
            f"| {r.label} | {e.peak:%Y-%m} | {e.trough:%Y-%m} | {e.depth:.0%} | {e.hold:+.0f} | "
            f"{e.ins:+.1f} | {e.share:+.2f} | {e.rebound:+.1f} |"
        )
    return out


EPS_HEAD = [
    "| Run | Peak | Trough | Depth | Hold | I | S | B |",
    "|---|---|---|---:|---:|---:|---:|---:|",
]


def stat_row(label: str, st: m9.PStat) -> str:
    return (
        f"| {label} | {st.months} | {st.acf1:+.3f} ({st.n1}) | {st.acf2:+.3f} | {st.noise:.3f} | "
        f"{st.mean * 1200:+.1f} | {st.sd * math.sqrt(12) * 100:.1f} |"
    )


STAT_HEAD = [
    "| Series | Months | Lag-1 acf (pairs) | Lag-2 acf | Noise line 1.645/sqrt(n) | "
    "Mean log return, % a year | Sd, % a year |",
    "|---|---:|---:|---:|---:|---:|---:|",
]


# --- (a) ---


@dataclass
class PartA:
    stats: dict[str, m9.PStat]
    runs: dict[str, Run]
    rho: tuple[float, float, float]
    corr: float

    @property
    def dg(self) -> float:
        return self.runs["A1"].gap - self.runs["A2"].gap


def reading_a(dg: float) -> str:
    if dg >= 0.10:
        return "averaging inflates the timing statistic"
    if abs(dg) < 0.05:
        return "no measurable averaging effect on the 12-month timing statistic"
    return "small, not separable from noise on so few falls"


def part_a(sh: Levels, dj: Levels, worlds: int = WORLDS) -> PartA:
    sh, dj = window(sh), window(dj)
    if sorted(sh) != sorted(dj):
        raise ValueError("(a): the two series must cover the same months")
    stats = {
        "sh": one_period("shiller", sh, "Shiller (Cowles averages)"),
        "dj": one_period("schwert", dj, "Schwert / Dow Jones month-end"),
    }
    ms, xs = m9.logrets(sh, sorted(sh))
    _, xd = m9.logrets(dj, sorted(dj))
    corr = float(np.corrcoef(xs, xd)[0, 1])
    runs: dict[str, Run] = {}
    spec = [
        ("A1", "A1 Shiller (averaged), lag 0", sh, "sh", 0),
        ("A2", "A2 Schwert / Dow Jones (month-end), lag 0", dj, "dj", 0),
        ("A3", "A3 Shiller, signal a month older", sh, "sh", 1),
        ("A4", "A4 Schwert / Dow Jones, signal a month older", dj, "dj", 1),
    ]
    for key, label, lev, sk, lag in spec:
        ev = m9.evaluate(label, segs_of(sk, lev, lag))
        nl = {"ar1": null_gaps(lev, stats[sk], "ar1", 0, worlds, 0)} if lag == 0 else {}
        runs[key] = Run(key, label, ev, nl)
    # A5: Shiller's positions traded on Dow Jones returns, scored on Dow Jones falls
    mixed = []
    for a, b in zip(segs_of("sh", sh), segs_of("dj", dj), strict=True):
        if a.months != b.months:
            raise ValueError("(a): segment months differ")
        mixed.append(m9.Seg("sh-on-dj", b.months, b.r, a.pos, b.cash))
    runs["A5"] = Run("A5", "A5 Shiller's signal traded on Dow Jones", m9.evaluate("A5", mixed), {})
    return PartA(stats, runs, sim_rho(200_000), corr)


# --- (b) ---


def trimmed(segs: Sequence[ins.Seg], lag: int) -> list[ins.Seg]:
    """Drop each segment's first scored year; lag 1 keeps the rule's positions, lag 2 uses the
    signal of the year before (position of year t = 1 if eq(t-2) > bill(t-2))."""
    out = []
    for s in segs:
        pos = s.pos[1:] if lag == 1 else s.pos[:-1]
        out.append(ins.Seg(s.iso, s.years[1:], s.r[1:], s.b[1:], s.pi[1:], pos))
    return out


def ep_gap(segs: Sequence[ins.Seg], ks: np.ndarray) -> tuple[float, float, float]:
    """Per-episode mean S of the rule, mean over rotations, gap (jst-autocorr-1's statistic)."""
    pairs = ja.episodes(segs).pairs
    st = ja.s_stats([s.r for s in segs], [s.b for s in segs], [s.pos for s in segs], pairs, ks)
    return (
        float(st.rule.mean()),
        float(st.rot_means.mean()),
        float(st.rule.mean() - st.rot_means.mean()),
    )


def sim_gaps(
    segs: Sequence[ins.Seg], lag: int, own: bool, worlds: int = SIM_WORLDS, seed: int = SEED
) -> np.ndarray:
    """Per-episode gap of the rule with signal lag `lag` (years) in Gaussian AR(1) worlds of log
    excess returns over bills (each segment's mean and sd; phi = the country's own acf, or 0)."""
    rng = np.random.default_rng(seed)
    ms = [float(ja.logx(s, True).mean()) for s in segs]
    ss = [float(ja.logx(s, True).std(ddof=1)) for s in segs]
    phis = ja.country_phi(segs)
    lmax = max(len(s.pos) for s in segs)
    out = np.full(worlds, np.nan)
    for w in range(worlds):
        rs, bs, poss = [], [], []
        for s, m, sd in zip(segs, ms, ss, strict=True):
            n = len(s.r)
            phi = float(np.clip(phis[s.iso], -0.9, 0.9)) if own else 0.0
            x = ja.ar1(rng, n + lag, m, sd, phi)
            rs.append((1 + s.b) * np.exp(x[lag:]) - 1)
            bs.append(s.b)
            poss.append(ja.signal(x[:n]))
        pairs = ja.episodes(segs, rs).pairs
        st = ja.s_stats(rs, bs, poss, pairs, rng.integers(1, lmax, size=ja.SIM_ROT))
        if len(st.rule):
            out[w] = float(st.rule.mean() - st.rot_means.mean())
    return out


@dataclass
class PartB:
    full: ins.Result
    l1: ins.Result
    l2: ins.Result
    ep: dict[str, tuple[float, float, float]]
    sims: dict[str, np.ndarray]


def reading_b(b: PartB) -> str:
    p1, p2 = ins.p_s(b.l1), ins.p_s(b.l2)
    if p2 < 0.05 and ins.ok(ins.cvals(b.l2.anch, lambda e: e.ins)):
        return "timing does not rest on the last year alone"
    if p2 >= 0.10 and p1 < 0.05:
        return (
            "timing rests on the last year's return (artefact and real persistence not separated)"
        )
    return "in between / not read"


def part_b(sims: int = SIM_WORLDS) -> PartB:
    jst = ins.load_jst()
    cfg = ins.CONFIGS[0]
    base = ins.build(cfg, jst)
    full = ins.run(cfg, jst)
    l1s, l2s = trimmed(base, 1), trimmed(base, 2)
    l1, l2 = ins.run(cfg, jst, l1s), ins.run(cfg, jst, l2s)
    ks = ja.rot_offsets(l1s, ins.ROTATIONS)
    ep = {"L1": ep_gap(l1s, ks), "L2": ep_gap(l2s, ks)}
    sm = {
        f"{lab}-{kind}": sim_gaps(l1s, lag, kind == "own", sims)
        for lab, lag in (("L1", 1), ("L2", 2))
        for kind in ("own", "rw")
    }
    return PartB(full, l1, l2, ep, sm)


# --- (c) ---

C_FIRST, C_LAST = ym(1877, 1), ym(1912, 12)


def aqr_levels(rows: Sequence[Sequence[object]]) -> Levels:
    """Excess-return levels of AQR's equal-weight commodity futures portfolio (column 1,
    `datawide2.parse_aqr_comlr`), level months up to C_LAST (the first level is 1877-02, so the
    first return is 1877-03)."""
    import datawide2 as dw

    mo = dw.parse_aqr_comlr(rows)
    return {m: x for m, x in zip(mo.months, mo.level, strict=True) if C_FIRST <= m <= C_LAST}


@dataclass
class PartC:
    stat: m9.PStat
    runs: dict[str, Run]

    @property
    def ratio(self) -> float:
        g0 = self.runs["C0"].gap
        return self.runs["C1"].gap / g0 if g0 > 0.05 else math.nan


def reading_c(c: PartC) -> str:
    g0 = c.runs["C0"].gap
    if g0 <= 0.05:
        return "no timing to test; the delay check is moot"
    r = c.ratio
    if r >= 0.75:
        return "the timing survives a one-month delay"
    if r < 0.50:
        return "the timing rests largely on one-month dependence"
    return "partly"


def part_c(lev: Levels, worlds: int = WORLDS) -> PartC:
    st = one_period("aqr", lev, "AQR EW commodity excess return")
    runs = {}
    for key, lag, d, label in (
        ("C0", 0, 0.25, "C0 AQR commodities, lag 0"),
        ("C1", 1, 0.25, "C1 AQR commodities, one-month delay"),
        ("C0-20", 0, 0.20, "C0 at 20% / 20%"),
        ("C1-20", 1, 0.20, "C1 at 20% / 20%"),
    ):
        ev = m9.evaluate(label, segs_of("aqr", lev, lag), d, d)
        nl = (
            {
                k: null_gaps(lev, st, k, lag, worlds, 10 * lag + j)
                for j, k in enumerate(("ar1", "bb"))
            }
            if d == 0.25
            else {}
        )
        runs[key] = Run(key, label, ev, nl)
    return PartC(st, runs)


# --- report and tries ---


def q(a: np.ndarray) -> str:
    a = a[np.isfinite(a)]
    lo, mid, hi = np.quantile(a, [0.05, 0.5, 0.95])
    return f"{mid:+.3f} ({lo:+.3f} to {hi:+.3f})"


def report(a: PartA, b: PartB, c: PartC) -> list[str]:
    L = [
        "# stale-checks-1: are the pre-1926 insurance results artefacts of averaged or stale "
        "prices?\n",
        "Generated by `uv run python -I research/lib/stalechecks1.py`. Card: "
        "`research/cards/stale-checks-1.md`. Statistics only. Log points = 100 x ln. "
        "S = share of a fall's log loss the rule avoided; G = S rule minus mean S of 1,000 "
        "rotations; null p = share of synthetic worlds with G at least the observed one.\n",
        "## (a) Averaged against point prices, US 1885-1925\n",
        "Shiller monthly total return (Cowles monthly averages before 1926) against Schwert "
        "(1990)'s appendix index (Dow Jones end-of-month price changes plus Cowles dividends), "
        "returns 1885-03..1925-12, Aug-Nov 1914 (exchange closed) dropped from both, so two "
        "segments.\n",
        *STAT_HEAD,
        stat_row("Shiller (averaged)", a.stats["sh"]),
        stat_row("Schwert / Dow Jones month-end", a.stats["dj"]),
        "",
        f"Correlation of the two monthly log returns: {a.corr:.3f}. Working (1960), m-point "
        f"average of a random walk: rho(25) = {working_rho(25):.3f}, limit 0.25. Simulated, "
        f"200,000 months of 25 daily steps: mean {a.rho[0]:+.3f}, midrange (high-low average, "
        f"Cowles' construction) {a.rho[1]:+.3f}, last close {a.rho[2]:+.3f}.\n",
        *RUN_HEAD,
        *[run_row(r) for r in a.runs.values()],
        "",
        f"**dG = G(A1) - G(A2) = {a.dg:+.3f}: {reading_a(a.dg)}.** "
        f"|G(A3) - G(A2)| = {abs(a.runs['A3'].gap - a.runs['A2'].gap):.3f}.\n",
        *EPS_HEAD,
        *[x for k in ("A1", "A2") for x in eps_rows(a.runs[k])],
        "",
        "## (b) A one-year-older signal on insure-1870-1 (annual JST)\n",
        f"Reproduction of #186 (untrimmed): S {b.full.s_rule:.2f}, random "
        f"{np.median(b.full.s_rot):.2f}, p_S {ins.p_s(b.full):.3f}, {b.full.share_head[0]} of "
        f"{b.full.share_head[1]}.\n",
        "| Run (trimmed: first scored year dropped) | Episodes | Anchored I > 0 | S rule / fixed / "
        "random | p_S | P rule / fixed / random | p_P | Verdict (#186 rule) |",
        "|---|---:|---|---|---:|---|---:|---|",
    ]
    for lab, r in (("L1: signal year t-1 (#186)", b.l1), ("L2: signal year t-2", b.l2)):
        k, n = r.share_head
        L.append(
            f"| {lab} | {len(r.eps)} | {k} of {n} | {r.s_rule:.2f} / {r.s_fix:.2f} / "
            f"{np.median(r.s_rot):.2f} | {ins.p_s(r):.3f} | {r.p_rule:.2f} / {r.p_fix:.2f} / "
            f"{np.median(r.p_rot):.2f} | {ins.p_p(r):.3f} | {r.verdict} ({'; '.join(r.quals)}) |"
        )
    L += [
        "",
        "Per-episode statistic (jst-autocorr-1) against Gaussian AR(1) worlds "
        f"({SIM_WORLDS:,} each; median and 5-95%):\n",
        "| Rule | Observed S / random / gap | AR(1) own-country phi: gap | p | Random walk: gap "
        "| p |",
        "|---|---|---|---:|---|---:|",
    ]
    for lab in ("L1", "L2"):
        s, rr, g = b.ep[lab]
        own, rw = b.sims[f"{lab}-own"], b.sims[f"{lab}-rw"]
        L.append(
            f"| {lab} | {s:.2f} / {rr:.2f} / {g:+.3f} | {q(own)} | {p_ge(own, g):.3f} | {q(rw)} | "
            f"{p_ge(rw, g):.3f} |"
        )
    L += [
        "",
        f"**Reading (card): {reading_b(b)}.**\n",
        "## (c) One-month delay on AQR's 1877-1912 commodity aggregate\n",
        *STAT_HEAD,
        stat_row("AQR EW commodity excess return", c.stat),
        "",
        *RUN_HEAD,
        *[run_row(r) for r in c.runs.values()],
        "",
        f"**G(C1) / G(C0) = {c.ratio:.2f}: {reading_c(c)}.**\n",
        *EPS_HEAD,
        *[x for k in ("C0", "C1") for x in eps_rows(c.runs[k])],
        "",
    ]
    return L


def _row(
    v: str, a: str, b: str, sh: str = "-", tot: str = "-", mdd: str = "-", fl: str = "-"
) -> str:
    return (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | insure-check | train | {a} | "
        f"{b} | {sh} | {tot} | {mdd} | {fl} |\n"
    )


def tries_rows(a: PartA, b: PartB, c: PartC) -> list[str]:
    rows = []
    for key, r in [*a.runs.items(), *c.runs.items()]:
        f, l_, sh, tot, mdd, fl = m9.sharpe_row(r.ev)
        t = r.ev.t
        v = (
            f"tsmom12m@{IDEA}-{key}: {r.label}; I > 0 in {r.ev.k} of {r.ev.n}, S "
            f"{t.rule.s_mean[0]:.2f} vs random {float(np.median(t.rot.s_mean)):.2f} "
            f"(p_rot {t.p_rot:.3f}), G {t.gap:+.3f}"
        )
        rows.append(_row(v, f, l_, f"{sh:.2f}", f"{tot:+.1%}", f"{mdd:.1%}", f"{fl:.2f}"))
    for key, r in (("L1", b.l1), ("L2", b.l2)):
        k, n = r.share_head
        segs = [s.seg for s in r.scs]
        v = (
            f"tsmom12a@{IDEA}-{key}: insure-1870-1 decisive sample, first year dropped, signal "
            f"{'t-1' if key == 'L1' else 't-2'}; {r.verdict}; I > 0 in {k} of {n} anchored falls, "
            f"S {r.s_rule:.2f} vs random {np.median(r.s_rot):.2f} (p {ins.p_s(r):.3f}), "
            f"P {r.p_rule:.2f}"
        )
        rows.append(
            _row(
                v,
                f"{min(s.years[1] for s in segs)}-12-31",
                f"{max(s.years[-1] for s in segs)}-12-31",
            )
        )
    return rows


def log_tries(rows: Sequence[str]) -> int:
    text = harness.TRIES.read_text()
    new = [x for x in rows if x.split(" | ")[2].split(":")[0] not in text]
    with harness.TRIES.open("a") as f:
        f.writelines(new)
    return len(new)


def main(argv: Sequence[str]) -> None:
    root = m9.cache_root()
    dj_path = root / IDEA / SCHWERT_CSV
    if not dj_path.exists():
        raise SystemExit(
            f"missing {dj_path}: rebuild it with `uv run python -I "
            f"research/lib/stalechecks1_ocr.py <cache_root>/survey-9/schwert/w2985.pdf "
            f"{dj_path}` (needs pdftoppm, magick, "
            "tesseract; the PDF is NBER WP 2985 from www.nber.org)"
        )
    sh = shiller_tr(
        ja.shiller_monthly(root / "shiller" / "2026-11-12" / "ie_data.xls"), A_FIRST, A_LAST
    )
    dj = load_schwert(dj_path)
    a = part_a(sh, dj)
    b = part_b()
    import datawide2 as dw

    c = part_c(
        aqr_levels(dw.read_xlsx_rows(root / "data-wide-2" / "probe" / "aqr-comlr-monthly.xlsx", 0))
    )
    OUT.write_text("\n".join(report(a, b, c)) + "\n")
    msg = f"wrote {OUT}"
    if "--log" in argv:
        msg += f"; tries rows added: {log_tries(tries_rows(a, b, c))}"
    print(msg)


if __name__ == "__main__":
    main(sys.argv[1:])
