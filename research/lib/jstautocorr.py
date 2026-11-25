"""jst-autocorr-1: is insure-1870-1's timing result an artefact of smoothed early indices? Card:
research/cards/jst-autocorr-1.md.

    uv run python -I research/lib/jstautocorr.py [path/to/norges-bank/stockprices.xlsx]

Descriptive. (1) labels each country-period of insure-1870-1's decisive sample from the JST
"Rate of Return on Everything" data appendix (RORE_documentation.pdf, macrohistory.net); (2)
lag-1 autocorrelation and per-episode share avoided S by label (and, as a description, by the
appendix's source periods); (3) JST US against Shiller's monthly file (cached) and JST Norway
against Norges Bank's monthly stock price index (Klovland; optional path, not committed);
(4) S of the rule under smoothing alone: AR(1) measured returns and annual averages of a monthly
random walk, on the same segments and bills. Writes research/results/jst-autocorr-1.md
(statistics only; JST is CC BY-NC-SA 4.0).
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import insure1 as i1  # noqa: E402
import insure1870 as ins  # noqa: E402

OUT = HERE.parent / "results" / "jst-autocorr-1.md"
DOWN = UP = 0.25
WORLDS, SIM_ROT, SEED = 1_000, 50, 0
WORKING = (2 * 12**2 + 1) / (3 * 12**2)  # variance ratio of 12-point averages of a random walk

# (1) Labels from the appendix text. Everything else: "year-end" by the paper's stated
# convention ("equity prices ... compare end-of-year prices of shares"), no per-country text.
YE, MAVG, NONCAL = "year-end (convention)", "monthly average (US)", "non-calendar / interpolated"
EXCEPTIONS: dict[str, list[tuple[int, int, str]]] = {
    # Shiller (2000), the JST US source: "monthly averages of daily closing prices"
    "USA": [(1870, 2020, MAVG)],
    # exchange closed mid-1914 to mid-1916: 1915 return = Jul 1914 - Jul 1916
    "CHE": [(1914, 1916, NONCAL)],
    # exchange closed Aug 1944 - Apr 1946: 1945 return covers that span
    "NLD": [(1945, 1945, NONCAL)],
    # civil war: end-1936 to end-1940 price change apportioned equally to 1937-1939
    "ESP": [(1937, 1939, NONCAL)],
}
# Source periods of the appendix (equity returns), for the descriptive split.
SOURCES: dict[str, list[tuple[int, str]]] = {
    "AUS": [(1870, "IMM London listings"), (1882, "Brailsford et al.")],
    "BEL": [(1870, "Buelens SCOB")],
    "CHE": [(1900, "Moore Zurich microdata"), (1926, "Pictet"), (1960, "SBC (Pictet/SNB)")],
    "DEU": [(1870, "Ronge top-30"), (1890, "Eube all-share"), (1914, "Ronge top-30"),
            (1960, "Gielen")],
    "DNK": [(1873, "Green microdata"), (1901, "yearbook selection"),
            (1923, "LoN/UN/IMF price index + Nielsen-Risager yields")],
    "ESP": [(1900, "Madrid microdata"), (1940, "IGBM")],
    "FIN": [(1895, "Poutvaara"), (1913, "Nyberg-Vaihekoski")],
    "FRA": [(1870, "Le Bris-Hautcoeur")],
    "GBR": [(1870, "Grossman"), (1908, "Barclays blue-chip"), (1964, "FTSE all-share")],
    "ITA": [(1870, "Genova (Da Pozzo-Felloni)"), (1888, "Milan (Baia Curioni)"),
            (1913, "Rosania"), (1955, "Mondani + Mediobanca")],
    "JPN": [(1882, "Fujino-Akiyama"), (1941, "Bank of Japan"), (1948, "UN / Bureau of Statistics")],
    "NLD": [(1900, "Eichholtz-Koedijk-Otten")],
    "NOR": [(1881, "Oslo microdata (JST)"), (1921, "Klovland price index + yearbook dividends")],
    "PRT": [(1870, "Lisbon microdata (JST)")],
    "SWE": [(1871, "Waldenstrom")],
    "USA": [(1870, "Shiller")],
}  # fmt: skip


def label(iso: str, y: int) -> str:
    return next((lab for a, b, lab in EXCEPTIONS.get(iso, []) if a <= y <= b), YE)


def source(iso: str, y: int) -> str:
    return [s for a, s in SOURCES[iso] if a <= y][-1]


# --- autocorrelation ---


def acf_pairs(
    xs: Sequence[np.ndarray], keep: Sequence[np.ndarray] | None = None, demean: bool = True
) -> tuple[float, int]:
    """Pooled lag-1 correlation over pairs (t-1, t) inside each series; `keep` marks the years a
    pair may use (both ends). Demeaned per series (over all its years) when `demean`."""
    a, b = [], []
    for j, x in enumerate(xs):
        z = x - x.mean() if demean else x
        k = np.ones(len(x), dtype=bool) if keep is None else keep[j]
        m = k[1:] & k[:-1]
        a.append(z[:-1][m])
        b.append(z[1:][m])
    u, v = np.concatenate(a), np.concatenate(b)
    if len(u) < 3:
        return math.nan, len(u)
    return float(np.corrcoef(u, v)[0, 1]), len(u)


def logx(seg: ins.Seg, over_bills: bool = False) -> np.ndarray:
    return np.log1p(seg.r) - (np.log1p(seg.b) if over_bills else 0.0)


# --- per-episode share avoided ---


@dataclass
class EpSet:
    segs: list[ins.Seg]
    pairs: list[list[tuple[int, int]]]  # per segment (peak, trough) indices on the hold index

    def years(self, j: int, a: int, b: int) -> list[int]:
        return self.segs[j].years[a + 1 : b + 1]


def episodes(segs: Sequence[ins.Seg], r: Sequence[np.ndarray] | None = None) -> EpSet:
    rr = [s.r for s in segs] if r is None else r
    out = []
    for x in rr:
        px = np.concatenate([[1.0], np.cumprod(1 + x)])
        out.append(i1.zigzag(px, DOWN, UP)[0])
    return EpSet(list(segs), out)


def shares(
    r: np.ndarray, b: np.ndarray, pos: np.ndarray, pairs: Sequence[tuple[int, int]],
    cost: float = ins.COST,
) -> np.ndarray:  # fmt: skip
    """S of each episode for each row of `pos` (K x n): rule minus holding over (peak, trough]
    in log points over |holding's log change|."""
    pos = np.atleast_2d(pos)
    flips = np.abs(np.diff(pos, axis=1, prepend=pos[:, :1]))
    rule = pos * r + (1 - pos) * b - cost * flips
    d = 100 * (np.log1p(rule) - np.log1p(r))
    cum = np.concatenate([np.zeros((len(pos), 1)), np.cumsum(d, axis=1)], axis=1)
    hold = np.concatenate([[0.0], np.cumsum(100 * np.log1p(r))])
    if not pairs:
        return np.zeros((len(pos), 0))
    a = np.array([p[0] for p in pairs])
    bb = np.array([p[1] for p in pairs])
    return (cum[:, bb] - cum[:, a]) / np.abs(hold[bb] - hold[a])


def signal(x_prev: np.ndarray) -> np.ndarray:
    return (x_prev > 0).astype(float)


@dataclass
class SStats:
    rule: np.ndarray  # per-episode S, rule
    fixed: np.ndarray  # per-episode S, fixed exposure
    rot: np.ndarray  # per-episode S, mean over rotations
    rot_means: np.ndarray  # mean episode S of each rotation


def s_stats(
    rs: Sequence[np.ndarray], bs: Sequence[np.ndarray], poss: Sequence[np.ndarray],
    pairs: Sequence[Sequence[tuple[int, int]]], ks: np.ndarray,
) -> SStats:  # fmt: skip
    rule, fix, rot, per_rot = [], [], [], []
    for r, b, pos, pr in zip(rs, bs, poss, pairs, strict=True):
        if not pr:
            per_rot.append(np.zeros((len(ks), 0)))
            continue
        rule.append(shares(r, b, pos, pr)[0])
        fix.append(shares(r, b, np.full(len(pos), pos.mean()), pr, cost=0.0)[0])
        rolled = np.array([np.roll(pos, int(k) % len(pos)) for k in ks])
        sh = shares(r, b, rolled, pr)
        rot.append(sh.mean(axis=0))
        per_rot.append(sh)
    allrot = np.concatenate(per_rot, axis=1)
    return SStats(
        np.concatenate(rule), np.concatenate(fix), np.concatenate(rot), allrot.mean(axis=1)
    )


# --- data ---


def decisive() -> tuple[list[ins.Seg], dict[str, dict[str, dict[int, float]]]]:
    import long_macro_build as lmb

    jst = ins.load_jst()
    cg = lmb._jst()["eq_capgain"]
    jst["eq_capgain"] = {iso: {d.year: x for d, x in ser} for iso, ser in cg.items()}
    return ins.build(ins.CONFIGS[0], jst), jst


def rot_offsets(segs: Sequence[ins.Seg], n: int, seed: int = ins.SEED) -> np.ndarray:
    lmax = max(len(s.pos) for s in segs)
    return np.random.default_rng(seed).integers(1, lmax, size=n)


# --- (4) simulation ---


def ar1(rng: np.random.Generator, n: int, m: float, s: float, phi: float) -> np.ndarray:
    e = rng.standard_normal(n) * s * math.sqrt(1 - phi**2)
    x = np.empty(n)
    x[0] = m + rng.standard_normal() * s
    for t in range(1, n):
        x[t] = m + phi * (x[t - 1] - m) + e[t]
    return x


def averaged(rng: np.random.Generator, n: int, m: float, s: float) -> tuple[np.ndarray, np.ndarray]:
    """n + 1 annual log excess returns from a monthly random walk: measured = log change of the
    mean of the 12 month-end price levels; true = December-to-December. Scaled so the measured
    sd is about s (Working's variance ratio)."""
    sm = s / math.sqrt(12 * WORKING)
    steps = m / 12 + sm * rng.standard_normal(12 * (n + 2))
    lev = np.concatenate([[0.0], np.cumsum(steps)])[1:].reshape(n + 2, 12)
    avg = np.log(np.exp(lev - lev[0, -1]).mean(axis=1))
    return np.diff(avg), np.diff(lev[:, -1])


@dataclass
class Scenario:
    key: str
    label: str
    phi: float | None = None  # AR(1); None with own=False means time averaging
    own: bool = False
    true_scoring: bool = False


SCENARIOS = [
    Scenario("ar0", "AR(1) phi 0 (random walk)", 0.0),
    Scenario("ar10", "AR(1) phi 0.10", 0.10),
    Scenario("ar19", "AR(1) phi 0.19", 0.19),
    Scenario("ar30", "AR(1) phi 0.30", 0.30),
    Scenario("own", "AR(1) each country's own observed phi", own=True),
    Scenario("avg", "Annual averages of a monthly random walk (measured)"),
    Scenario("avgtrue", "Same signal, scored on true year-end returns", true_scoring=True),
]


def country_phi(segs: Sequence[ins.Seg]) -> dict[str, float]:
    out = {}
    for iso in sorted({s.iso for s in segs}):
        out[iso] = acf_pairs([logx(s, True) for s in segs if s.iso == iso])[0]
    return out


@dataclass
class SimOut:
    s_rule: np.ndarray
    s_fix: np.ndarray
    s_rot: np.ndarray
    acf: np.ndarray
    n_eps: np.ndarray

    @property
    def gap(self) -> np.ndarray:
        return self.s_rule - self.s_rot


def simulate(
    sc: Scenario, segs: Sequence[ins.Seg], worlds: int = WORLDS, n_rot: int = SIM_ROT,
    seed: int = SEED,
) -> SimOut:  # fmt: skip
    rng = np.random.default_rng(seed)
    ms = [float(logx(s, True).mean()) for s in segs]
    ss = [float(logx(s, True).std(ddof=1)) for s in segs]
    phis = country_phi(segs)
    lmax = max(len(s.pos) for s in segs)
    res = np.zeros((5, worlds))
    for w in range(worlds):
        rs, bs, poss, xs = [], [], [], []
        for s, m, sd in zip(segs, ms, ss, strict=True):
            n = len(s.r)
            if sc.phi is not None or sc.own:
                phi = float(np.clip(phis[s.iso], -0.9, 0.9)) if sc.own else float(sc.phi or 0.0)
                x = ar1(rng, n + 1, m, sd, phi)
                xt = x
            else:
                x, xt = averaged(rng, n, m, sd)
            pos = signal(x[:-1])
            use = xt if sc.true_scoring else x
            rs.append((1 + s.b) * np.exp(use[1:]) - 1)
            bs.append(s.b)
            poss.append(pos)
            xs.append(x[1:])
        pairs = episodes(segs, rs).pairs
        ks = rng.integers(1, lmax, size=n_rot)
        st = s_stats(rs, bs, poss, pairs, ks)
        n_e = len(st.rule)
        res[:, w] = [
            st.rule.mean() if n_e else math.nan,
            st.fixed.mean() if n_e else math.nan,
            st.rot_means.mean() if n_e else math.nan,
            acf_pairs(xs)[0],
            n_e,
        ]
    return SimOut(*res)


# --- (3) independent series ---


def shiller_monthly(path: Path) -> dict[tuple[int, int], tuple[float, float]]:
    import xlrd  # type: ignore[import-untyped]

    sh = xlrd.open_workbook(str(path)).sheet_by_name("Data")
    out = {}
    for i in range(sh.nrows):
        v = sh.row_values(i)
        if not isinstance(v[0], float) or not isinstance(v[1], float):
            continue
        y = int(v[0])
        mo = round((v[0] - y) * 100)
        if 1 <= mo <= 12 and v[1] > 0 and isinstance(v[2], float) and y <= 2024:
            out[(y, mo)] = (float(v[1]), float(v[2]))
    return out


def shiller_annual(mon: dict[tuple[int, int], tuple[float, float]]) -> dict[str, dict[int, float]]:
    """Annual nominal total returns of year y: Dec-Dec, Jan(y+1)-Jan(y) and annual-average price
    (dividends: the year's 12 monthly D/12 over the starting price)."""
    years = sorted({y for y, _ in mon})
    dd, jj, av = {}, {}, {}
    for y in years:
        try:
            div = sum(mon[(y, m)][1] for m in range(1, 13)) / 12
            p0, p1 = mon[(y - 1, 12)][0], mon[(y, 12)][0]
            dd[y] = (p1 + div) / p0 - 1
            j0, j1 = mon[(y, 1)][0], mon[(y + 1, 1)][0]
            jj[y] = (j1 + div) / j0 - 1
            a0 = np.mean([mon[(y - 1, m)][0] for m in range(1, 13)])
            a1 = np.mean([mon[(y, m)][0] for m in range(1, 13)])
            av[y] = (a1 + div) / a0 - 1
        except KeyError:
            continue
    return {"Dec-Dec": dd, "Jan-Jan": jj, "annual average": av}


def norway_monthly(path: Path) -> dict[tuple[int, int], float]:
    import long_x as lx

    out = {}
    for row in lx.xlsx_rows(path, "p1c8_table_a1"):
        if len(row) > 1 and len(row[0]) == 7 and row[0][4] == ":" and row[1]:
            try:
                out[(int(row[0][:4]), int(row[0][5:]))] = float(row[1])
            except ValueError:
                continue
    return out


def norway_annual(mon: dict[tuple[int, int], float]) -> dict[str, dict[int, float]]:
    years = sorted({y for y, _ in mon})
    dd, av = {}, {}
    for y in years:
        if (y - 1, 12) in mon and (y, 12) in mon:
            dd[y] = mon[(y, 12)] / mon[(y - 1, 12)] - 1
        a0 = [mon[(y - 1, m)] for m in range(1, 13) if (y - 1, m) in mon]
        a1 = [mon[(y, m)] for m in range(1, 13) if (y, m) in mon]
        if len(a0) == 12 and len(a1) == 12:
            av[y] = float(np.mean(a1) / np.mean(a0) - 1)
    return {"Dec-Dec": dd, "annual average": av}


def compare(
    ref: dict[int, float], alts: dict[str, dict[int, float]], y0: int, y1: int
) -> list[tuple[str, int, float, float, float]]:
    """(name, years, correlation with ref, mean |diff| in log points, lag-1 acf) per series."""
    out = []
    ys = [y for y in range(y0, y1 + 1) if y in ref and all(y in a for a in alts.values())]
    ys = [y for y in ys if y - 1 in ys or y + 1 in ys]
    series = {"JST": ref, **alts}
    for name, s in series.items():
        x = np.log1p(np.array([s[y] for y in ys]))
        xr = np.log1p(np.array([ref[y] for y in ys]))
        keep = np.array([y - 1 in ys for y in ys])
        u, v = x[:-1][keep[1:]], x[1:][keep[1:]]
        ac = float(np.corrcoef(u - x.mean(), v - x.mean())[0, 1])
        out.append((name, len(ys), float(np.corrcoef(x, xr)[0, 1]),
                    float(np.mean(np.abs(x - xr)) * 100), ac))  # fmt: skip
    return out


# --- report ---


def pct(x: np.ndarray, q: float) -> float:
    return float(np.nanpercentile(x, q))


def group_rows(
    segs: Sequence[ins.Seg], eps: EpSet, st: SStats, key: Callable[[str, int], str]
) -> list[str]:
    xs = [logx(s) for s in segs]
    xe = [logx(s, True) for s in segs]
    groups = sorted({key(s.iso, y) for s in segs for y in s.years[1:]})
    # episode group: the common key of its (peak, trough] years, else "mixed"
    ep_key = []
    for j, pr in enumerate(eps.pairs):
        for a, b in pr:
            ks = {key(segs[j].iso, y) for y in eps.years(j, a, b)}
            ep_key.append(ks.pop() if len(ks) == 1 else "mixed")
    ek = np.array(ep_key)
    L = []
    for g in [*groups, "mixed"]:
        keep = [np.array([key(s.iso, y) == g for y in s.years[1:]]) for s in segs]
        n_years = int(sum(k.sum() for k in keep))
        ac, npair = acf_pairs(xs, keep) if g != "mixed" else (math.nan, 0)
        ac2, _ = acf_pairs(xe, keep) if g != "mixed" else (math.nan, 0)
        m = ek == g
        if g == "mixed" and not m.any():
            continue
        ne = int(m.sum())
        s_txt = "- | - | - | -"
        if ne:
            sr, sf, so = st.rule[m].mean(), st.fixed[m].mean(), st.rot[m].mean()
            s_txt = f"{sr:.2f} | {sf:.2f} | {so:.2f} | {sr - so:+.2f}"
        ac_txt = f"{ac:+.2f} | {ac2:+.2f} | {npair}" if npair else "- | - | 0"
        L.append(f"| {g} | {n_years} | {ac_txt} | {ne} | {s_txt} |")
    return L


GROUP_HEAD = [
    "| Group | Scored years | Lag-1 acf, log return | Lag-1 acf, over bills | Pairs | "
    "Episodes | S rule | S fixed | S random | Gap rule - random |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
]


def by_source_key(iso: str, y: int) -> str:
    return f"{iso} {source(iso, y)}"


def main(argv: Sequence[str]) -> None:
    segs, jst = decisive()
    eps = episodes(segs)
    ks = rot_offsets(segs, ins.ROTATIONS)
    st = s_stats([s.r for s in segs], [s.b for s in segs], [s.pos for s in segs], eps.pairs, ks)
    # cross-check against insure-1870-1's own scoring
    ref = [e.share for s in segs for e in ins.episodes(s, DOWN, UP).eps]
    assert np.allclose(ref, st.rule), "per-episode S differs from insure1870"
    obs_gap = float(st.rule.mean() - st.rot.mean())
    ac_all, n_all = acf_pairs([logx(s) for s in segs])
    ac_raw, _ = acf_pairs([logx(s) for s in segs], demean=False)
    ac_ex, _ = acf_pairs([logx(s, True) for s in segs])
    p_gap = float((st.rot_means >= st.rule.mean()).mean())

    L = [
        "# jst-autocorr-1: is insure-1870-1's timing result a smoothed-index artefact?\n",
        "Generated by `uv run python -I research/lib/jstautocorr.py`. Card: "
        "`research/cards/jst-autocorr-1.md`. Statistics only (JST R6, CC BY-NC-SA 4.0; cite "
        "Jorda, Schularick and Taylor 2017; Jorda, Knoll, Kuvshinov, Schularick and Taylor 2019). "
        "Decisive sample of insure-1870-1 (US to 1926, others to 1965, 25% zigzag). S = share "
        "avoided per episode (rule minus holding over (peak, trough], over |holding|), pooled "
        "over episodes, no clustering. Random = mean over insure-1870-1's 1,000 rotations "
        "(seed 0). Acf = pooled lag-1 correlation of annual log returns, pairs of consecutive "
        "scored years inside a segment, demeaned per segment.\n",
        "## Whole decisive sample\n",
        f"- Scored years in {len(segs)} segments; lag-1 pairs {n_all}. Acf of log returns "
        f"{ac_all:+.3f} (not demeaned {ac_raw:+.3f}), over bills {ac_ex:+.3f}.",
        f"- Episodes {len(st.rule)}. Per-episode S: rule {st.rule.mean():.3f}, fixed "
        f"{st.fixed.mean():.3f}, random {st.rot.mean():.3f}; gap rule - random {obs_gap:+.3f} "
        f"(share of rotations with mean S at least the rule's: {p_gap:.3f}). insure-1870-1's "
        "headline (mean over anchored clusters): 0.73 / 0.51 / 0.47.\n",
        "## (2) By documented label\n",
        "Labels from the JST appendix (`RORE_documentation.pdf`): the paper states the "
        "year-end convention for all equity returns; the appendix tables name sources but say "
        "nothing per country about year-end vs averaged prices, except the US (Shiller: monthly "
        "averages of daily closes), the exchange closures (Switzerland 1914-16, Netherlands 1945) "
        "and Spain 1937-39 (interpolated). Episodes are grouped by the label of all their "
        "(peak, trough] years.\n",
        *GROUP_HEAD,
        *group_rows(segs, eps, st, label),
        "",
        "## (2b) By source period of the appendix (description, not on the card)\n",
        *GROUP_HEAD,
        *group_rows(segs, eps, st, by_source_key),
        "",
    ]

    # (3) independent series
    L += ["## (3) Independent series\n"]
    root = ins.HERE.parent.parent
    try:
        import long_macro_build as lmb

        sp = lmb.mf.lxf.cache_root() / "shiller" / "2026-11-12" / "ie_data.xls"
        sa = shiller_annual(shiller_monthly(sp))
        us = jst["eq_tr"]["USA"]
        for y0, y1 in ((1872, 1926), (1927, 1965), (1966, 2020)):
            L += [f"US {y0}-{y1}, JST `eq_tr` against Shiller's monthly file (nominal total "
                  "return; Shiller prices are monthly averages of daily closes):\n",
                  "| Series | Years | Corr. with JST | Mean abs. diff, log pts | Lag-1 acf |",
                  "|---|---:|---:|---:|---:|"]  # fmt: skip
            for name, n, c, dfn, ac in compare(us, sa, y0, y1):
                L.append(f"| {name} | {n} | {c:.3f} | {dfn:.1f} | {ac:+.2f} |")
            L.append("")
    except (OSError, ImportError) as err:
        L.append(f"Shiller comparison skipped ({type(err).__name__}).\n")
    nb = Path(argv[0]) if argv else None
    if nb and nb.exists():
        na = norway_annual(norway_monthly(nb))
        cg = jst["eq_capgain"]["NOR"]
        for y0, y1 in ((1915, 1920), (1921, 1965), (1966, 2000)):
            L += [f"Norway {y0}-{y1}, JST `eq_capgain` against Norges Bank's monthly total "
                  "stock price index (Klovland 2004; latest bid of the month):\n",
                  "| Series | Years | Corr. with JST | Mean abs. diff, log pts | Lag-1 acf |",
                  "|---|---:|---:|---:|---:|"]  # fmt: skip
            for name, n, c, dfn, ac in compare(cg, na, y0, y1):
                L.append(f"| {name} | {n} | {c:.3f} | {dfn:.1f} | {ac:+.2f} |")
            L.append("")
        L += norway_redo(segs, jst, na, ks)
    else:
        L.append("Norway comparison skipped (Norges Bank file not given).\n")
    del root

    # (4) simulation
    L += [
        "## (4) Simulation: S under smoothing alone\n",
        f"{WORLDS:,} worlds per scenario (seed 0), same {len(segs)} segments, actual bills, "
        "per-segment mean and sd of the log excess return, Gaussian; per world: pooled "
        f"per-episode S of the rule, fixed exposure, mean of {SIM_ROT} rotations, and the "
        "measured acf (pairs as above, over bills). Observed: gap "
        f"{obs_gap:+.3f}, S rule {st.rule.mean():.3f}, acf over bills {ac_ex:+.3f}.\n",
        "| Scenario | Mean acf | Episodes | S rule (median) | S random | Gap: median | "
        "Gap: 95th pct | Share of worlds with gap >= observed | Share with S rule >= observed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    sims = {}
    for sc in SCENARIOS:
        so = simulate(sc, segs)
        sims[sc.key] = so
        L.append(
            f"| {sc.label} | {np.nanmean(so.acf):+.3f} | {np.nanmean(so.n_eps):.0f} | "
            f"{pct(so.s_rule, 50):.3f} | {np.nanmedian(so.s_rot):.3f} | {pct(so.gap, 50):+.3f} | "
            f"{pct(so.gap, 95):+.3f} | {np.nanmean(so.gap >= obs_gap):.3f} | "
            f"{np.nanmean(so.s_rule >= st.rule.mean()):.3f} |"
        )
    q19, qavg = pct(sims["ar19"].gap, 95), pct(sims["avg"].gap, 95)
    if obs_gap < q19 or obs_gap < qavg:
        reading = "smoothing could explain it"
    else:
        reading = "smoothing alone does not explain it"
    L += [
        "",
        f"Card reading: observed gap {obs_gap:+.3f} against the 95th percentile "
        f"{q19:+.3f} (phi 0.19) and {qavg:+.3f} (annual averages): **{reading}**.",
        "",
        "Country phi used in the 'own' scenario (over bills): "
        + ", ".join(f"{k} {v:+.2f}" for k, v in country_phi(segs).items())
        + ".",
        "",
    ]
    OUT.write_text("\n".join(L) + "\n")
    print("\n".join(L))


def norway_redo(
    segs: Sequence[ins.Seg], jst: dict[str, dict[str, dict[int, float]]],
    na: dict[str, dict[int, float]], ks: np.ndarray,
) -> list[str]:  # fmt: skip
    """Norway 1921-1965 with JST's capital gain replaced by Klovland Dec-Dec (dividend part of
    JST kept): acf and per-episode S of Norway's segments (description)."""
    out = ["Norway's decisive segments with 1921-1965 capital gains replaced by the "
           "December-to-December change of the monthly index (JST dividend return kept):\n",
           "| Norway series | Acf log return | Episodes | S rule | S fixed | S random |",
           "|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    nor = [s for s in segs if s.iso == "NOR"]
    tr, cg = jst["eq_tr"]["NOR"], jst["eq_capgain"]["NOR"]
    for name in ("JST", "Dec-Dec", "annual average"):
        new = []
        for s in nor:
            ys = s.years
            r = {y: tr[y] for y in ys}
            if name != "JST":
                for y in ys:
                    if 1921 <= y <= 1965 and y in na[name] and y in cg:
                        r[y] = tr[y] - cg[y] + na[name][y]
            eq = {y: r[y] for y in ys}
            bill = {y: jst["bill_rate"]["NOR"][y] for y in ys}
            new += ins.segments("NOR", eq, bill, jst["cpi"]["NOR"], ys[-1])
        e = episodes(new)
        st = s_stats([s.r for s in new], [s.b for s in new], [s.pos for s in new], e.pairs, ks)
        ac = acf_pairs([logx(s) for s in new])[0]
        out.append(f"| {name} | {ac:+.2f} | {len(st.rule)} | {st.rule.mean():.2f} | "
                   f"{st.fixed.mean():.2f} | {st.rot.mean():.2f} |")  # fmt: skip
    return [*out, ""]


if __name__ == "__main__":
    main(sys.argv[1:])
