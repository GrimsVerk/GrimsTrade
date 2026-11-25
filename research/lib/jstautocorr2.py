"""jst-autocorr-2: where does the autocorrelation of early JST annual equity returns come from?
Card: research/cards/jst-autocorr-2.md.

    uv run python -I research/lib/jstautocorr2.py [--log] [--uk path/to/boe/monthly.csv]

Descriptive. Each equity source period of the JST Macrohistory R6 file gets three labels from the
source documentation (price timing, thin market, and year-level disruption), fixed in SOURCES /
TIMING / THIN / INTERP / DISRUPT below with the quote behind each label in research/
jst-autocorr-2.md. Then: lag-1 (and lag-2) autocorrelation of annual log equity returns over
bills, per source period (1870-2020) and pooled by label on insure-1870-1's decisive sample (US to
1926, others to 1965), with a permutation p for each flag and the card's "explained" reading.
Writes research/results/jst-autocorr-2.md (statistics only; JST is CC BY-NC-SA 4.0); `--log`
appends the `note` rows to research/tries.md once.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import insure1870 as ins  # noqa: E402
import jstautocorr as jac  # noqa: E402

IDEA = "jst-autocorr-2"
OUT = HERE.parent / "results" / "jst-autocorr-2.md"
TRIES = HERE.parent / "tries.md"
PERMS, SEED = 10_000, 0
Z = 1.645  # one-sided 5% noise line, 1.645 / sqrt(pairs)
MIN_FLAG_PAIRS = 50

# --- (1) labels (card rule; quotes in research/jst-autocorr-2.md) ---

YE, DAVG, AAVG, INTP, UNK = "year-end", "Dec-average", "annual-average", "interpolated", "unknown"
AVERAGED = frozenset({DAVG, AAVG, INTP})
THIN, BROAD = "thin", "broad"

# Equity price source periods of the RORE appendix (Tables 19-35): (first year, name).
SOURCES: dict[str, list[tuple[int, str]]] = {
    "AUS": [(1870, "IMM London listings"), (1882, "Brailsford et al. (to 1935)"),
            (1936, "Brailsford et al. (1936-)"), (2009, "NERA"),
            (2014, "ASX 200")],
    "BEL": [(1870, "Buelens SCOB (to 1914)"), (1915, "Buelens SCOB (1915-)")],
    "CHE": [(1900, "Moore Zurich microdata"), (1926, "Pictet"), (1960, "SBC (Pictet/SNB)"),
            (1984, "SPI")],
    "DEU": [(1870, "Ronge top-30"), (1890, "Eube all-share"), (1914, "Ronge top-30 (2)"),
            (1960, "Gielen"), (1991, "DAX"), (1996, "CDAX")],
    "DNK": [(1873, "Green microdata"), (1901, "yearbook selection"),
            (1914, "yearbook all-share price index"), (1923, "LoN/UN/IMF price index"),
            (2000, "MSCI"), (2002, "OMXCGI")],
    "ESP": [(1900, "Madrid microdata (Moore)"), (1927, "Madrid microdata (BdE archive)"),
            (1941, "IGBM")],
    "FIN": [(1895, "Poutvaara"), (1913, "Nyberg-Vaihekoski"), (1991, "OMX Helsinki")],
    "FRA": [(1870, "Le Bris-Hautcoeur"), (2011, "CAC-40")],
    "GBR": [(1870, "Grossman"), (1908, "Barclays top-30"), (1964, "FTSE all-share")],
    "ITA": [(1870, "Genova (Da Pozzo-Felloni)"), (1888, "Milan (Baia Curioni)"),
            (1913, "Rosania"), (1955, "Mondani + Mediobanca"), (1970, "Mediobanca index")],
    "JPN": [(1882, "Fujino-Akiyama"), (1941, "Bank of Japan"), (1948, "UN Monthly Bulletin"),
            (1949, "Bureau of Statistics (TSE)")],
    "NLD": [(1900, "Eichholtz-Koedijk-Otten"), (1996, "CBS"), (2004, "AEX")],
    "NOR": [(1881, "Oslo microdata (JST)"), (1921, "Klovland"), (2001, "OSEBX")],
    "PRT": [(1870, "Lisbon microdata (JST)"), (1988, "PSI")],
    "SWE": [(1871, "Waldenstrom (Aurell lists)"), (1891, "Waldenstrom (ten most traded)"),
            (1902, "Waldenstrom (1902-)"), (2003, "OMXSGI")],
    "USA": [(1870, "Shiller")],
}  # fmt: skip
# Price timing per source period (absent: UNK). Filled from the documentation only.
TIMING: dict[tuple[str, str], str] = {
    ("USA", "Shiller"): DAVG,  # Shiller: monthly averages of daily closes; JST = Dec-Dec
    ("NOR", "Klovland"): YE,  # Klovland 2004: latest bid price of the month (JST = Dec-Dec)
    # Brailsford-Handley-Maheswaran: "the average value of the index in December"
    ("AUS", "Brailsford et al. (to 1935)"): DAVG,
    ("AUS", "Brailsford et al. (1936-)"): DAVG,
    ("FRA", "Le Bris-Hautcoeur"): YE,  # first Friday of January, chained January to January
    ("CHE", "Moore Zurich microdata"): YE,  # JST footnote: December 1913 - July 1914 etc.
    ("CHE", "Pictet"): YE,  # "relevees a la fin des annees etudiees" (Pictet 1998 reprint)
    ("ESP", "Madrid microdata (BdE archive)"): YE,  # JST: "prices of securities in end-1936"
    ("DEU", "Ronge top-30"): YE,  # "Ultimo 1870 bis Ultimo 1959", weekly closes, year-end
    ("DEU", "Ronge top-30 (2)"): YE,
    ("SWE", "Waldenstrom (ten most traded)"): YE,  # "year-end market prices ... were collected"
    ("SWE", "Waldenstrom (1902-)"): YE,  # "market value of listed stocks at the end of the period"
}
# Thin-market label per source period (absent: UNK).
THINNESS: dict[tuple[str, str], str] = {
    ("DEU", "Ronge top-30"): BROAD,  # 30 blue chips by market cap
    ("DEU", "Ronge top-30 (2)"): BROAD,
    ("DEU", "Eube all-share"): BROAD,  # 415 shares; replaced (missing) prices at most 1%
    ("GBR", "Barclays top-30"): BROAD,
    ("GBR", "FTSE all-share"): BROAD,
    ("CHE", "Pictet"): BROAD,  # 50 Zurich shares chosen at random (Raetzer 1983 in Pictet)
    ("FIN", "Nyberg-Vaihekoski"): BROAD,  # on average 53 series a month
    ("AUS", "Brailsford et al. (1936-)"): BROAD,  # "forty seven in 1935"
    # stated: missing prices carried forward, 16% of 19th-century prices (Le Bris-Hautcoeur)
    ("FRA", "Le Bris-Hautcoeur"): THIN,
    ("AUS", "Brailsford et al. (to 1935)"): THIN,  # "five stocks ... in 1875, twelve in 1905"
    ("BEL", "Buelens SCOB (to 1914)"): THIN,  # Annaert-Van Hyfte: "did not trade very frequently"
    ("DNK", "yearbook selection"): THIN,
    ("ITA", "Genova (Da Pozzo-Felloni)"): THIN,  # "selected stocks"
    ("FIN", "Poutvaara"): THIN,  # "unofficial auction price quotations for three banks"
    ("NOR", "Oslo microdata (JST)"): THIN,  # Klovland 2004: 22 shares quoted monthly in 1881
    ("SWE", "Waldenstrom (Aurell lists)"): THIN,  # "Trading activity was quite low", 10-50 firms
    ("SWE", "Waldenstrom (ten most traded)"): THIN,  # ten stocks
}
# Year-level interpolated / non-calendar returns (documented closures; JST *_interp flags).
INTERP: dict[str, tuple[int, int]] = {
    "CHE": (1914, 1916), "NLD": (1944, 1946), "ESP": (1937, 1940), "PRT": (1975, 1977),
}  # fmt: skip
WARS = [(1914, 1918), (1939, 1945)]
# Documented closures, civil war, revolution and price controls beyond the world wars.
DISRUPT_EXTRA: dict[str, list[tuple[int, int]]] = {
    "ESP": [(1936, 1940)], "PRT": [(1974, 1977)], "JPN": [(1946, 1948)],
    "DEU": [(1943, 1948)], "NLD": [(1944, 1946)], "AUS": [(1941, 1947)],
}  # fmt: skip


def source(iso: str, y: int) -> str:
    return [s for a, s in SOURCES[iso] if a <= y][-1]


def timing(iso: str, y: int) -> str:
    a, b = INTERP.get(iso, (0, -1))
    if a <= y <= b:
        return INTP
    return TIMING.get((iso, source(iso, y)), UNK)


def thin(iso: str, y: int) -> str:
    return THINNESS.get((iso, source(iso, y)), UNK)


def disrupted(iso: str, y: int, hyper: frozenset[int]) -> bool:
    spans = WARS + DISRUPT_EXTRA.get(iso, [])
    return y in hyper or any(a <= y <= b for a, b in spans)


# --- pieces and pairs ---


@dataclass
class Piece:
    iso: str
    src: str
    seg: int  # index of its segment
    pos: np.ndarray  # positions of its years inside the segment's scored years
    years: np.ndarray
    x: np.ndarray  # demeaned log return over bills
    raw: np.ndarray  # demeaned log total return


def pieces(segs: Sequence[ins.Seg], sub: dict[int, float] | None = None) -> list[Piece]:
    """Each segment split into maximal runs of one source period; demeaned per run. With `sub`,
    the year's value in `sub` (e.g. the cross-country mean) is subtracted first."""
    out = []
    for j, s in enumerate(segs):
        ys = np.array(s.years[1:])
        w = np.array([sub[int(y)] for y in ys]) if sub is not None else np.zeros(len(ys))
        xb = np.log1p(s.r) - np.log1p(s.b) - w
        xr = np.log1p(s.r) - w
        srcs = [source(s.iso, int(y)) for y in ys]
        start = 0
        for i in range(1, len(ys) + 1):
            if i == len(ys) or srcs[i] != srcs[start]:
                sl = slice(start, i)
                out.append(
                    Piece(s.iso, srcs[start], j, np.arange(start, i), ys[sl],
                          xb[sl] - xb[sl].mean(), xr[sl] - xr[sl].mean())
                )  # fmt: skip
                start = i
    return out


@dataclass
class Pairs:
    u: np.ndarray
    v: np.ndarray
    piece: np.ndarray
    seg: np.ndarray
    pos0: np.ndarray
    pos1: np.ndarray
    y0: np.ndarray
    y1: np.ndarray
    iso: np.ndarray


def pairs(ps: Sequence[Piece], lag: int = 1, raw: bool = False) -> Pairs:
    cols: list[list[np.ndarray]] = [[] for _ in range(9)]
    for k, p in enumerate(ps):
        x = p.raw if raw else p.x
        n = len(x) - lag
        if n <= 0:
            continue
        for c, a in zip(
            cols,
            [x[:-lag], x[lag:], np.full(n, k), np.full(n, p.seg), p.pos[:-lag], p.pos[lag:],
             p.years[:-lag], p.years[lag:], np.full(n, p.iso)],
            strict=True,
        ):  # fmt: skip
            c.append(a)
    arr = [np.concatenate(c) if c else np.zeros(0) for c in cols]
    return Pairs(*arr)


def corr(u: np.ndarray, v: np.ndarray) -> float:
    if len(u) < 3 or u.std() == 0 or v.std() == 0:
        return math.nan
    return float(np.corrcoef(u, v)[0, 1])


def acf(pr: Pairs, m: np.ndarray | None = None) -> tuple[float, int]:
    if m is None:
        return corr(pr.u, pr.v), len(pr.u)
    return corr(pr.u[m], pr.v[m]), int(m.sum())


# --- flags and the permutation ---


@dataclass
class Flag:
    name: str
    piece: np.ndarray  # bool per piece (source-level part)
    year: list[np.ndarray]  # bool per scored year of each segment (year-level part)

    def on(self, pr: Pairs, piece: np.ndarray | None = None,
           year: Sequence[np.ndarray] | None = None) -> np.ndarray:  # fmt: skip
        pf = self.piece if piece is None else piece
        yf = self.year if year is None else year
        y0 = np.array([yf[s][i] for s, i in zip(pr.seg, pr.pos0, strict=True)], dtype=bool)
        y1 = np.array([yf[s][i] for s, i in zip(pr.seg, pr.pos1, strict=True)], dtype=bool)
        return pf[pr.piece.astype(int)] | y0 | y1


def make_flag(
    name: str, segs: Sequence[ins.Seg], ps: Sequence[Piece],
    piece_rule: Callable[[Piece], bool], year_rule: Callable[[str, int], bool],
) -> Flag:  # fmt: skip
    pf = np.array([piece_rule(p) for p in ps], dtype=bool)
    yf = [np.array([year_rule(s.iso, y) for y in s.years[1:]], dtype=bool) for s in segs]
    return Flag(name, pf, yf)


@dataclass
class FlagTest:
    name: str
    a_flag: float
    n_flag: int
    a_rest: float
    n_rest: int
    p: float
    reading: str

    @property
    def line(self) -> float:
        return Z / math.sqrt(self.n_rest) if self.n_rest else math.nan


def flag_test(flag: Flag, pr: Pairs, a0: float, perms: int = PERMS, seed: int = SEED) -> FlagTest:
    m = flag.on(pr)
    af, nf = acf(pr, m)
    ar, nr = acf(pr, ~m)
    obs = af - ar
    rng = np.random.default_rng(seed)
    hits, done = 0, 0
    for _ in range(perms):
        pf = rng.permutation(flag.piece)
        yf = [np.roll(v, int(rng.integers(0, len(v)))) for v in flag.year]
        mm = flag.on(pr, pf, yf)
        if mm.sum() < 3 or (~mm).sum() < 3:
            continue
        d = acf(pr, mm)[0] - acf(pr, ~mm)[0]
        if math.isnan(d):
            continue
        done += 1
        hits += d >= obs
    p = (hits + 1) / (done + 1)
    return FlagTest(flag.name, af, nf, ar, nr, p, reading(af, nf, ar, nr, p, a0))


def reading(af: float, nf: int, ar: float, nr: int, p: float, a0: float) -> str:
    """The card's rule."""
    if nf < MIN_FLAG_PAIRS:
        return "not decidable (fewer than 50 flagged pairs)"
    if ar <= Z / math.sqrt(nr) and p <= 0.05:
        return "explains it"
    if ar <= a0 / 2 or p <= 0.05:
        return "partly explains it"
    return "not explained by this flag"


# --- usability (card rule) ---


def usability(tim: str, th: str, a_ex: float, n_ex: int) -> str:
    if tim in AVERAGED:
        return "not usable (averaged / interpolated)"
    if n_ex < 5 or math.isnan(a_ex):
        return "too short to judge: AR-preserving null only"
    above = a_ex > Z / math.sqrt(n_ex)
    if above:
        return "AR-preserving null only (acf above noise line)"
    if th in (THIN, UNK) or tim == UNK:
        return f"AR-preserving null only ({'thin' if th == THIN else 'labels unknown'})"
    return "usable"


# --- output ---


def f2(x: float) -> str:
    return "-" if math.isnan(x) else f"{x:+.2f}"


def per_source_rows(
    segs: Sequence[ins.Seg], decisive_keys: set[tuple[str, str]], hyper: dict[str, frozenset[int]]
) -> tuple[list[str], dict[str, int]]:
    ps = pieces(segs)
    p1, p2 = pairs(ps), pairs(ps, 2)
    keys = sorted({(p.iso, p.src) for p in ps},
                  key=lambda k: (k[0], [s for _, s in SOURCES[k[0]]].index(k[1])))  # fmt: skip
    head = [
        "| Country | Source | Years | Timing | Thin | In decisive | Pairs | Lag-1 acf | Noise line"
        " | Lag-1, undisrupted pairs | Pairs | Lag-2 acf | Usability (card rule) |",
        "|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    rows, tally = [], {}
    for iso, src in keys:
        kk = [i for i, p in enumerate(ps) if (p.iso, p.src) == (iso, src)]
        yrs = np.concatenate([ps[i].years for i in kk])
        m1 = np.isin(p1.piece, kk)
        m2 = np.isin(p2.piece, kk)
        a1, n1 = acf(p1, m1)
        h = hyper.get(iso, frozenset())
        dis = np.array([disrupted(iso, int(a), h) or disrupted(iso, int(b), h)
                        for a, b in zip(p1.y0, p1.y1, strict=True)], dtype=bool)  # fmt: skip
        ax, nx = acf(p1, m1 & ~dis)
        a2, _ = acf(p2, m2)
        tims = {timing(iso, int(y)) for y in yrs}
        tim = TIMING.get((iso, src), UNK)
        tl = tim + (" (some years interpolated)" if INTP in tims else "")
        th = THINNESS.get((iso, src), UNK)
        us = usability(tim, th, ax, nx)
        tally[us] = tally.get(us, 0) + len(yrs)
        line = Z / math.sqrt(n1) if n1 else math.nan
        rows.append(
            f"| {iso} | {src} | {int(yrs.min())}-{int(yrs.max())} | {tl} | {th} | "
            f"{'yes' if (iso, src) in decisive_keys else 'no'} | {n1} | {f2(a1)} | "
            f"{line:.2f} | {f2(ax)} | {nx} | {f2(a2)} | {us} |"
        )
    return head + rows, tally


def group_table(pr: Pairs, pr2: Pairs, groups: dict[str, np.ndarray],
                groups2: dict[str, np.ndarray], prr: Pairs) -> list[str]:  # fmt: skip
    out = [
        "| Group | Pairs | Lag-1 acf, over bills | Lag-1 acf, log return | Lag-2 pairs "
        "| Lag-2 acf |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for g, m in groups.items():
        a, n = acf(pr, m)
        ar, _ = acf(prr, m)
        a2, n2 = acf(pr2, groups2[g])
        out.append(f"| {g} | {n} | {f2(a)} | {f2(ar)} | {n2} | {f2(a2)} |")
    return out


def pair_label(pr: Pairs, f: Callable[[str, int], str]) -> np.ndarray:
    a = np.array([f(i, int(y)) for i, y in zip(pr.iso, pr.y0, strict=True)])
    b = np.array([f(i, int(y)) for i, y in zip(pr.iso, pr.y1, strict=True)])
    return np.where(a == b, a, "mixed")


def world_mean(segs: Sequence[ins.Seg]) -> dict[int, float]:
    """Equal-weighted cross-country mean log return over bills, by year."""
    by: dict[int, list[float]] = {}
    for s in segs:
        for y, r, b in zip(s.years[1:], s.r, s.b, strict=True):
            by.setdefault(y, []).append(math.log1p(r) - math.log1p(b))
    return {y: float(np.mean(v)) for y, v in by.items()}


def world_acf(segs: Sequence[ins.Seg], y0: int, y1: int) -> tuple[float, int]:
    """Lag-1 acf of the equal-weighted cross-country mean log return over bills, by year."""
    wm = world_mean(segs)
    ys = [y for y in sorted(wm) if y0 <= y <= y1]
    x = np.array([wm[y] for y in ys])
    ok = np.array([ys[i] == ys[i - 1] + 1 for i in range(1, len(ys))])
    u, v = (x[:-1] - x.mean())[ok], (x[1:] - x.mean())[ok]
    return corr(u, v), len(u)


def uk_monthly(path: Path) -> dict[tuple[int, int], float]:
    """Bank of England 'A millennium of macroeconomic data' v3.1, monthly sheet in long CSV form
    (datahub mirror, OGL v3): spliced monthly share price index weighted by market cap."""
    import csv

    out = {}
    with path.open() as fh:
        for r in csv.DictReader(fh):
            if r["variable_id"].startswith("spliced-monthly-share-price-index") and r["value"]:
                out[(int(r["year"]), int(r["month"]))] = float(r["value"])
    return out


def uk_rows(path: Path) -> list[str]:
    import long_macro_build as lmb

    cg = {d.year: x for d, x in lmb._jst()["eq_capgain"]["GBR"]}
    mon = uk_monthly(path)
    alt = jac.norway_annual(mon)  # Dec-Dec and annual-average changes of a monthly index
    jj = {}
    for y in {y for y, _ in mon}:
        if (y, 1) in mon and (y + 1, 1) in mon:  # January y to January y+1
            jj[y] = mon[(y + 1, 1)] / mon[(y, 1)] - 1
    alts = {"Dec-Dec": alt["Dec-Dec"], "Jan-Jan": jj, "annual average": alt["annual average"]}
    out = []
    for y0, y1, lab in [(1871, 1907, "Grossman"), (1908, 1963, "Barclays top-30"),
                        (1964, 2016, "FTSE all-share")]:  # fmt: skip
        out += [f"UK {y0}-{y1} ({lab}), JST `eq_capgain` against the Bank of England's spliced "
                "monthly share price index:\n",
                "| Series | Years | Corr. with JST | Mean abs. diff, log pts | Lag-1 acf |",
                "|---|---:|---:|---:|---:|"]  # fmt: skip
        for name, n, c, d, a in jac.compare(cg, alts, y0, y1):
            out.append(f"| {name} | {n} | {c:.3f} | {d:.1f} | {a:+.2f} |")
        out.append("")
    return out


def main(argv: Sequence[str]) -> None:
    jst = ins.load_jst()
    hyper = {iso: ins.hyper_years(c) for iso, c in jst["cpi"].items()}
    segs = ins.build(ins.CONFIGS[0], jst)
    full = ins.build(ins.CONFIGS[1], jst)
    ps = pieces(segs)
    pr, pr2, prr = pairs(ps), pairs(ps, 2), pairs(ps, raw=True)
    a0, n0 = acf(pr)
    a2_0, n2_0 = acf(pr2)

    def dis(iso: str, y: int) -> bool:
        return disrupted(iso, y, hyper.get(iso, frozenset()))

    f_avg = make_flag("averaged / interpolated", segs, ps,
                      lambda p: TIMING.get((p.iso, p.src), UNK) in AVERAGED,
                      lambda iso, y: timing(iso, y) == INTP)  # fmt: skip
    f_thin = make_flag("thin", segs, ps, lambda p: THINNESS.get((p.iso, p.src)) == THIN,
                       lambda iso, y: False)  # fmt: skip
    f_dis = make_flag("disrupted (war, closure, hyperinflation)", segs, ps, lambda p: False, dis)
    f_all = Flag("union of the three", f_avg.piece | f_thin.piece,
                 [a | b for a, b in zip(f_avg.year, f_dis.year, strict=True)])  # fmt: skip
    tests = [flag_test(f, pr, a0) for f in (f_avg, f_thin, f_dis, f_all)]

    # descriptive groups (lag-1 and lag-2 on the same rule)
    lt1, lt2 = pair_label(pr, timing), pair_label(pr2, timing)
    lh1, lh2 = pair_label(pr, thin), pair_label(pr2, thin)
    d1, d2 = f_dis.on(pr), f_dis.on(pr2)
    g1: dict[str, np.ndarray] = {"all pairs": np.ones(len(pr.u), dtype=bool)}
    g2: dict[str, np.ndarray] = {"all pairs": np.ones(len(pr2.u), dtype=bool)}
    for lab in (YE, DAVG, AAVG, INTP, UNK, "mixed"):
        g1[f"timing: {lab}"], g2[f"timing: {lab}"] = lt1 == lab, lt2 == lab
    for lab in (THIN, BROAD, UNK):
        g1[f"market: {lab}"], g2[f"market: {lab}"] = lh1 == lab, lh2 == lab
    g1["disrupted"], g2["disrupted"] = d1, d2
    g1["undisrupted"], g2["undisrupted"] = ~d1, ~d2
    for lab, (y0, y1) in {"1872-1913": (1872, 1913), "1919-1938": (1919, 1938),
                          "1946-1965": (1946, 1965)}.items():  # fmt: skip
        g1[f"era {lab}, undisrupted"] = (pr.y0 >= y0) & (pr.y1 <= y1) & ~d1
        g2[f"era {lab}, undisrupted"] = (pr2.y0 >= y0) & (pr2.y1 <= y1) & ~d2
    clean1 = ~f_all.on(pr) & (lt1 != UNK) & (lh1 == BROAD)
    clean2 = ~f_all.on(pr2) & (lt2 != UNK) & (lh2 == BROAD)
    g1["documented year-end, broad, undisrupted"] = clean1
    g2["documented year-end, broad, undisrupted"] = clean2
    nonflag1, nonflag2 = ~f_all.on(pr), ~f_all.on(pr2)
    g1["no flag (rest after the union)"], g2["no flag (rest after the union)"] = nonflag1, nonflag2

    # 1966-2020 reference, same pairing on the full-span segments
    fps = pieces(full)
    fpr = pairs(fps)
    late = fpr.y0 >= 1966
    a_late, n_late = acf(fpr, late)

    dkeys = {(p.iso, p.src) for p in ps}
    src_rows, tally = per_source_rows(full, dkeys, hyper)
    w1, wn1 = world_acf(segs, 1872, 1965)
    w2, wn2 = world_acf(full, 1966, 2020)
    weras = {
        lab: world_acf(segs, a, b)
        for lab, (a, b) in {
            "1872-1913": (1872, 1913),
            "1919-1938": (1919, 1938),
            "1946-1965": (1946, 1965),
        }.items()
    }
    # common vs idiosyncratic: subtract the year's cross-country mean before pairing
    ipr = pairs(pieces(segs, world_mean(segs)))
    ia, ina = acf(ipr)
    ia_u, ina_u = acf(ipr, ~f_dis.on(ipr))
    ia_t, ina_t = acf(ipr, f_thin.on(ipr))
    ia_r, ina_r = acf(ipr, ~f_all.on(ipr))

    L = [
        "# jst-autocorr-2: where does the autocorrelation of early JST annual equity returns "
        "come from?\n",
        "Generated by `uv run python -I research/lib/jstautocorr2.py`. Card: "
        "`research/cards/jst-autocorr-2.md`. Statistics only (JST R6, CC BY-NC-SA 4.0; cite "
        "Jorda, Schularick and Taylor 2017; Jorda, Knoll, Kuvshinov, Schularick and Taylor 2019). "
        "Returns: annual log equity total return over bills. Pairs: consecutive scored years of "
        "one insure-1870-1 segment and one source period, demeaned per (segment, source) run. "
        "Labels and the quotes behind them: `research/jst-autocorr-2.md`.\n",
        "## Decisive sample (US to 1926, others to 1965)\n",
        f"- Lag-1 acf over bills A0 {a0:+.3f} ({n0} pairs); lag-2 {a2_0:+.3f} ({n2_0} pairs). "
        f"1966-2020 on the same pairing: {a_late:+.3f} ({n_late} pairs).",
        f"- Equal-weighted cross-country mean return, lag-1 acf: 1872-1965 {w1:+.2f} ({wn1} "
        f"pairs), 1966-2020 {w2:+.2f} ({wn2} pairs); by era (description): "
        + ", ".join(f"{k} {a:+.2f} ({n})" for k, (a, n) in weras.items())
        + ".",
        "- Idiosyncratic part (each country's return minus the year's cross-country mean, same "
        f"pairing; description, not on the card): all {ia:+.3f} ({ina} pairs), undisrupted "
        f"{ia_u:+.3f} ({ina_u}), thin {ia_t:+.3f} ({ina_t}), no flag {ia_r:+.3f} ({ina_r}).\n",
        "### Flag tests (card rule)\n",
        f"Permutation: {PERMS:,} draws, seed {SEED}; source-level flags shuffled across the "
        f"{len(ps)} source runs, year-level flags circularly shifted within each segment. "
        "One-sided: flagged acf minus rest acf at least the observed.\n",
        "| Flag | Flagged pairs | Acf flagged | Rest pairs | Acf rest | Noise line of rest | "
        "Difference | Perm. p | Reading |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for t in tests:
        L.append(
            f"| {t.name} | {t.n_flag} | {f2(t.a_flag)} | {t.n_rest} | {f2(t.a_rest)} | "
            f"{t.line:.3f} | {f2(t.a_flag - t.a_rest)} | {t.p:.4f} | {t.reading} |"
        )
    L += ["", "### Groups (description)\n", *group_table(pr, pr2, g1, g2, prr), ""]
    L += ["## Per source period, 1870-2020 (full-span segments)\n",
          "Noise line = 1.645 / sqrt(pairs). Undisrupted = pairs with neither year in a war, "
          "closure or hyperinflation year (the card drops those years). Usability by the card "
          "rule, on the undisrupted acf.\n", *src_rows, ""]  # fmt: skip
    L.append("Scored years per usability class (full span): " + "; ".join(
        f"{k} {v}" for k, v in sorted(tally.items())) + ".\n")  # fmt: skip
    if "--uk" in argv:
        L += ["## Independent series: UK (description)\n",
              *uk_rows(Path(argv[list(argv).index("--uk") + 1]).expanduser())]  # fmt: skip
    OUT.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    if "--log" in argv:
        log_rows(tests, a0, n0, tally)


def log_rows(tests: Sequence[FlagTest], a0: float, n0: int, tally: dict[str, int]) -> None:
    text = TRIES.read_text()
    if f"| {IDEA} |" in text:
        print("tries.md already has rows for", IDEA)
        return
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    tail = "| note | train | 1871-12-31 | 1965-12-31 | - | - | - | - |"
    rows = [
        f"| {now} | {IDEA} | descriptive note (not a try): pooled lag-1 acf over bills "
        f"{a0:+.3f} ({n0} pairs) on insure-1870-1's decisive sample, source-period pairing "
        f"(research/jst-autocorr-2.md) {tail}"
    ]
    for t in tests:
        rows.append(
            f"| {now} | {IDEA} | flag split '{t.name}' (descriptive): acf flagged "
            f"{t.a_flag:+.2f} ({t.n_flag} pairs) vs rest {t.a_rest:+.2f} ({t.n_rest}), "
            f"permutation p {t.p:.3f}: {t.reading} {tail}"
        )
    rows.append(
        f"| {now} | {IDEA} | usability per JST source period (descriptive, card rule), scored "
        "years 1871-2020: "
        + "; ".join(f"{k} {v}" for k, v in sorted(tally.items()))
        + " | note | train | 1871-12-31 | 2020-12-31 | - | - | - | - |"
    )
    with TRIES.open("a") as fh:
        fh.write("\n".join(rows) + "\n")
    print(f"appended {len(rows)} rows to tries.md")


if __name__ == "__main__":
    main(sys.argv[1:])
