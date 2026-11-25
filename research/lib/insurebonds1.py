"""insure-bonds-1: trend's crash insurance on long government-bond histories.

    uv run python -I research/lib/insurebonds1.py before   # card's before-scoring table only
    uv run python -I research/lib/insurebonds1.py run [--log] [--worlds N]

Card: research/cards/insure-bonds-1.md. Data (read locally, nothing raw committed):
- Norges Bank Historical Monetary Statistics (cite Eitrheim, Klovland and Qvigstad 2004;
  Klovland 2004): `bond_yields.xlsx` sheet A4 (most actively traded long government bonds,
  1822-) and A1 (GOV, 1820-1920), cached by data-wide-2; `shortterm_ir.xlsx` sheet 1A1 (Norges
  Bank discount rate, end of month; Eitrheim and Klovland 2007), fetched by this lane.
- Bank of England, "A millennium of macroeconomic data" v3.1 (OGL v3): the spliced consol yield
  and the discount rate from the monthly long CSV (jst-autocorr-2's cache) and the M10 sheet of
  the workbook (insure-1709-1's cache) for the splice check.

Yields are turned into total returns (a 10-year par bond rebuilt monthly for Norway, a
perpetuity for consols). The rule, episodes, scores, tests, fixed/rotation controls and the
AR(1) / block-bootstrap worlds are `insure1709`'s and `insure1`'s code, unchanged; new here are
the loaders, the total-return rebuilds, the fall-threshold ladder, a threshold-aware world
scorer, AAFT surrogates and the report.
"""

from __future__ import annotations

import math
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import datawide2 as dw  # noqa: E402
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import insure1709 as i17  # noqa: E402

IDEA = "insure-bonds-1"
ym, ym_str = i17.ym, i17.ym_str
Levels = dict[int, float]

NOR_LO, NOR_HI = ym(1822, 1), ym(1984, 12)  # card: Norway's bond is scored from 1985 on
GOV_LO, GOV_HI = ym(1820, 5), ym(1920, 12)  # check 7
CON_LO, CON_HI = ym(1865, 12), ym(1926, 12)  # 1866 warms the signal up; scored 1867-01..
LADDER = (0.25, 0.20, 0.15, 0.10)
LADDER_A = (0.10, 0.075, 0.05)  # amendment A, after the before-scoring counts
MIN_FALLS = 8
MATURITY = 10.0
ROTATIONS, WORLDS, WORLD_ROT = i17.ROTATIONS, i17.WORLDS, i17.WORLD_ROT
OUT = harness.RESEARCH / "results" / "insure-bonds-1.md"
NB_BONDS = "data-wide-2/probe/nb-bond_yields.xlsx"
NB_SHORT = "insure-bonds-1/nb/shortterm_ir.xlsx"
A4, A1, D1A1 = "p1_c4_table_A4_Monthly", "p1_c4_table_A1_Monthly", "p2c1_table_1A1"
M10 = "M10. Mthly long-term rates"
# M10 columns (0-based) of the consol sources (header text of the workbook, card)
M10_COLS = {"NBER 1852-1888": 6, "Capie-Webber": 7, "Klovland 1870-1914": 8, "spliced": 10}


# --- total returns from yields (yields in % a year) ---


def par_return(y0: float, y1: float, maturity: float = MATURITY) -> float:
    """A par bond of `maturity` years (coupon y0, semiannual) bought at y0, repriced a month
    later at y1 with maturity - 1/12 years left (annuity formula, fractional periods), plus the
    coupon accrued over the month (data-long-3 / combo2_longrun's rebuild)."""
    c, y = y0 / 100, y1 / 100
    n = 2 * (maturity - 1 / 12)
    if y > 0:
        v = 1 / (1 + y / 2)
        price = (c / 2) * (1 - v**n) / (y / 2) + v**n
    else:
        price = 1 + c / 2 * n
    return price - 1 + c / 12


def perp_return(y0: float, y1: float) -> float:
    """A perpetuity paying 1 a year: price 1/y, coupon accrued monthly."""
    return y0 / y1 - 1 + y0 / 1200


def price_return(y0: float, y1: float) -> float:
    return y0 / y1 - 1


def tr_levels(y: Levels, f: object = par_return) -> Levels:
    """Total-return index over each run of consecutive months with a yield (1 at a run's
    first month); a missing month starts a new run (never filled)."""
    fn = f if callable(f) else par_return
    out: Levels = {}
    for run_ in i17.segments({m: v for m, v in y.items() if v > 0}):
        lev = 1.0
        out[run_[0]] = lev
        for a, b in zip(run_, run_[1:], strict=False):
            lev *= 1 + fn(y[a], y[b])
            out[b] = lev
    return out


# --- loaders ---


def _year(x: object) -> int | None:
    if isinstance(x, int | float) and 1700 < x < 2100 and float(x).is_integer():
        return int(x)
    s = str(x).strip() if x is not None else ""
    return int(s) if re.fullmatch(r"1[7-9]\d\d|20\d\d", s) else None


def parse_wide_years(rows: Sequence[Sequence[object]], lo: int, hi: int) -> Levels:
    """A sheet with a year in column 0 and the 12 months in columns 1-12 (A4's layout)."""
    out: Levels = {}
    for r in rows:
        yr = _year(r[0]) if r else None
        if yr is None:
            continue
        for mo in range(1, 13):
            v = dw._num(r[mo]) if len(r) > mo else None
            m = ym(yr, mo)
            if v is not None and lo <= m <= hi:
                out[m] = v
    return out


def m10_columns(rows: Sequence[dict[int, str]], lo: int, hi: int) -> dict[str, Levels]:
    out: dict[str, Levels] = {k: {} for k in M10_COLS}
    for r in rows:
        y, mo = r.get(0, ""), r.get(1, "")
        if not (y.replace(".0", "").isdigit() and mo in i17.MONTHS):
            continue
        m = ym(int(float(y)), i17.MONTHS.index(mo) + 1)
        if not lo <= m <= hi:
            continue
        for k, j in M10_COLS.items():
            x = r.get(j)
            if x is not None and re.fullmatch(r"-?[0-9.]+(E-?[0-9]+)?", x):
                out[k][m] = float(x)
    return out


def match_runs(cols: dict[str, Levels], tol: float = 1e-6) -> list[tuple[str, int, int]]:
    """Runs of months by the source column whose monthly change equals the spliced column's
    ('none' where none does, 'tie' where several do)."""
    sp = cols["spliced"]
    lab = []
    for m in sorted(sp):
        if m - 1 not in sp:
            continue
        hit = [
            k
            for k, a in cols.items()
            if k != "spliced"
            and m in a
            and m - 1 in a
            and abs(a[m] / a[m - 1] - sp[m] / sp[m - 1]) < tol
        ]
        lab.append((m, hit[0] if len(hit) == 1 else ("tie" if hit else "none")))
    runs: list[tuple[str, int, int]] = []
    for m, k in lab:
        if runs and runs[-1][0] == k and runs[-1][2] == m - 1:
            runs[-1] = (k, runs[-1][1], m)
        else:
            runs.append((k, m, m))
    return runs


def consol_periods(runs: Sequence[tuple[str, int, int]]) -> tuple[list[i17.Period], str]:
    """C1 NBER, C2 Klovland, C3 Capie-Webber from the splice check (card default if the
    Klovland run is missing)."""
    kl = [r for r in runs if r[0] == "Klovland 1870-1914"]
    if kl:
        a, b = min(r[1] for r in kl), max(r[2] for r in kl)
        note = f"Klovland matches {ym_str(a)}..{ym_str(b)}"
        if a <= CON_LO + 1:  # no NBER month left in the window: C2 starts at the base month
            a = CON_LO
            note += f"; no NBER period in the window, C2 starts at {ym_str(CON_LO)}"
    else:
        a, b = ym(1870, 1), ym(1914, 12)
        note = "no Klovland match; card default 1870-01..1914-12 used"
    ps = [
        i17.Period("consols", "C1 NBER 1852-1888", CON_LO, a - 1, False, "not stated"),
        i17.Period("consols", "C2 Klovland (Goschen-corrected)", a, b, False, "last Friday"),
        i17.Period("consols", "C3 Capie-Webber", b + 1, CON_HI, False, "end month / averages"),
    ]
    return [p for p in ps if p.hi >= p.lo], note


NOR_PERIODS = [
    i17.Period("norway", "N1 quotations abroad", NOR_LO, ym(1842, 12), False, "end month"),
    i17.Period("norway", "N2 interpolated", ym(1843, 1), ym(1844, 12), False, "interpolated"),
    i17.Period("norway", "N3 quotations abroad", ym(1845, 1), ym(1914, 12), False, "end month"),
    i17.Period("norway", "N4 Oslo", ym(1915, 1), ym(1939, 12), False, "end month"),
    i17.Period("norway", "N5 Oslo, occupation", ym(1940, 1), ym(1945, 12), False, "end month"),
    i17.Period("norway", "N6 Oslo, regulated", ym(1946, 1), NOR_HI, False, "end month"),
]


@dataclass
class Data:
    nor_y: Levels  # A4 yield, %
    gov_y: Levels  # A1 GOV yield, %
    nor_cash: Levels  # Norges Bank discount rate, %
    con_y: Levels  # BoE spliced consol yield, %
    con_cash: Levels  # BoE discount rate on prime paper, %
    m10: dict[str, Levels]
    runs: list[tuple[str, int, int]]
    csv_vs_xlsx: float


def load(root: Path | None = None) -> Data:
    root = root or i17.cache_root()
    b = root / NB_BONDS
    nor = parse_wide_years(dw.read_xlsx_rows(b, A4), NOR_LO, NOR_HI)
    a1 = dw.read_xlsx_rows(b, A1)
    gov = {m: v for m, v in dw.parse_labelled_columns(a1, dw.find_col(a1, "GOV"))}
    gov = {m: v for m, v in gov.items() if GOV_LO <= m <= GOV_HI}
    s = dw.read_xlsx_rows(root / NB_SHORT, D1A1)
    cash = dict(dw.parse_labelled_columns(s, dw.find_col(s, "NB discount rate")))
    cash = {m: v for m, v in cash.items() if m <= NOR_HI}
    c = i17.read_csv(root / i17.CSV_REL, [i17.CONSOL, i17.CASH], last=CON_HI)
    con = {m: v for m, v in c[i17.CONSOL].items() if m >= CON_LO and v > 0}
    con_cash = {m: v for m, v in c[i17.CASH].items() if m >= CON_LO - 1}
    cols = m10_columns(i17.xlsx_sheet(root / i17.XLSX_REL, M10), CON_LO, CON_HI)
    common = [m for m in con if m in cols["spliced"]]
    gap = max(abs(con[m] / cols["spliced"][m] - 1) for m in common) if common else math.nan
    return Data(nor, gov, cash, con, con_cash, cols, match_runs(cols), gap)


# --- before scoring ---


def zero_share(y: Levels, p: i17.Period) -> float:
    ms = [m for m in y if p.lo <= m <= p.hi and m - 1 in y and m - 1 >= p.lo]
    return float(np.mean([y[m] == y[m - 1] for m in ms])) if ms else math.nan


def stats_of(y: Levels, lev: Levels, ps: Sequence[i17.Period]) -> list[i17.PStat]:
    return [replace(i17.period_stats(lev, p), zero=zero_share(y, p)) for p in ps]


def make_segs(
    name: str,
    lev: Levels,
    cash: Levels | None = None,
    lag: int = 0,
    lo: int = 0,
    hi: int = 10**9,
) -> list[i17.Seg]:
    lev = {m: x for m, x in lev.items() if lo <= m <= hi}
    out = []
    for run_ in i17.segments(lev):
        s = i17.build_seg(name, run_, i17.holding_returns(lev, run_), lag, cash)
        if s is not None:
            out.append(s)
    return out


def fall_counts(segs: Sequence[i17.Seg], ladder: Sequence[float] = LADDER) -> dict[float, int]:
    """Confirmed falls of the holding level (positions not read) per rung of the ladder."""
    return {d: sum(len(i17.pairs_of(s.r, d, d)) for s in segs) for d in ladder}


def pick_threshold(counts: dict[float, int], ladder: Sequence[float] = LADDER) -> float:
    return next((d for d in ladder if counts[d] >= MIN_FALLS), ladder[-1])


def neighbours(d: float, ladder: Sequence[float] = LADDER) -> list[float]:
    j = list(ladder).index(d)
    return [ladder[k] for k in (j - 1, j + 1) if 0 <= k < len(ladder)]


@dataclass
class Series:
    name: str
    y: Levels
    lev: Levels
    cash: Levels
    periods: list[i17.Period]
    stats: list[i17.PStat]
    segs: list[i17.Seg]
    counts: dict[float, int]
    d: float


def make_series(
    name: str,
    y: Levels,
    lev: Levels,
    cash: Levels,
    ps_all: Sequence[i17.Period],
    ladder: Sequence[float] = LADDER,
) -> tuple[Series, list[str]]:
    ps = [p for p in ps_all if any(p.lo <= m <= p.hi for m in lev)]
    dropped = [p.label for p in ps_all if p not in ps]
    segs = make_segs(name, lev, cash)
    cnt = fall_counts(segs, ladder)
    s = Series(name, y, lev, cash, ps, stats_of(y, lev, ps), segs, cnt,
               pick_threshold(cnt, ladder))  # fmt: skip
    return s, dropped


def series(d: Data, ladder: Sequence[float] = LADDER) -> tuple[Series, Series, str]:
    cps, note = consol_periods(d.runs)
    nor, dn = make_series(
        "norway", d.nor_y, tr_levels(d.nor_y, par_return), d.nor_cash, NOR_PERIODS, ladder
    )
    con, dc = make_series(
        "consols", d.con_y, tr_levels(d.con_y, perp_return), d.con_cash, cps, ladder
    )
    for name, dr in (("norway", dn), ("consols", dc)):
        if dr:
            note += f"; {name}: no data in {', '.join(dr)}"
    return nor, con, note


def amended(d: Data) -> list[tuple[str, Series]]:
    """Amendment A (card): the ladder extended to 7.5% and 5% for the two primary series, and
    Norway with a perpetuity total return on the card's ladder."""
    nor, con, _ = series(d, LADDER_A)
    perp, _ = make_series(
        "norway", d.nor_y, tr_levels(d.nor_y, perp_return), d.nor_cash, NOR_PERIODS
    )
    return [
        ("Norway, 10-year par bond, extended ladder", nor),
        ("Consols, perpetuity, extended ladder", con),
        ("Norway, perpetuity, card ladder", perp),
    ]


def before_rows(
    d: Data, nor: Series, con: Series, note: str, amend: Sequence[tuple[str, Series]] = ()
) -> list[str]:
    out = [
        "## Before scoring (card): sources, splice, autocorrelation and the fall threshold",
        "",
        "Consol splice (BoE M10, monthly changes of the spliced column matched to 1e-6 against "
        "the NBER 1852-1888, Klovland 1870-1914 and Capie-Webber columns): "
        + "; ".join(f"{k} {ym_str(a)}..{ym_str(b)}" for k, a, b in d.runs)
        + f". {note}. Cached CSV against the workbook's spliced column: largest relative "
        f"difference {d.csv_vs_xlsx:.1e}.",
        "",
    ]
    for s in (nor, con):
        runs = i17.segments(s.y)
        out += [
            f"{s.name}: yields for {len(s.y)} months {ym_str(min(s.y))} to {ym_str(max(s.y))}, "
            f"{len(runs)} runs: "
            + ", ".join(f"{ym_str(r[0])}..{ym_str(r[-1])} ({len(r)})" for r in runs)
            + f". Scored segments: {len(s.segs)}, "
            + ", ".join(f"{ym_str(g.months[1])}..{ym_str(g.months[-1])}" for g in s.segs)
            + ".",
            "",
        ]
    out += [
        "| Series | Source period | Timing (documented) | Months | Missing inside | "
        "Lag-1 acf (pairs) | Noise line | Lag-2 acf | Zero yield changes | Stale-suspect |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for s in (nor, con):
        for st in s.stats:
            p = st.p
            out.append(
                f"| {s.name} | {p.label} {ym_str(p.lo)}-{ym_str(p.hi)} | {p.timing} | "
                f"{st.months} | {st.missing} | {st.acf1:+.3f} ({st.n1}) | {st.noise:.3f} | "
                f"{st.acf2:+.3f} | {st.zero:.1%} | {'yes' if st.stale_suspect else 'no'} |"
            )
    out += [
        "",
        "Monthly log total returns (Norway: 10-year par bond; consols: perpetuity), demeaned "
        "per source period, pairs inside the period. Noise line 1.645/sqrt(pairs). Zero yield "
        "changes: months whose yield equals the month before. Stale-suspect: acf1 above the "
        "noise line or zero changes above 20% (card).",
        "",
        "| Series | Falls at 25% | 20% | 15% | 10% | Threshold (largest with >= 8) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for s in (nor, con):
        out.append(
            f"| {s.name} | " + " | ".join(str(s.counts[x]) for x in LADDER) + f" | {s.d:.0%} |"
        )
    out += [
        "",
        "Confirmed falls of the total-return holding level, fall d and rise d, scored window "
        "(rule positions not read).",
        "",
    ]
    if amend:
        out += [
            "**Amendment A (card, after the counts above, before any rule position was read):** "
            'with 2 and 4 falls at 10%, both card verdicts are fixed as "Too few falls". The '
            "readings below are added, with the same tests, nulls and verdict table, reported "
            "next to (not instead of) the card's verdicts.",
            "",
            "| Reading | Falls per rung | Threshold (largest with >= 8) |",
            "|---|---|---:|",
        ]
        for lab, a in amend:
            out.append(
                f"| {lab} | "
                + ", ".join(f"{x:.1%}: {a.counts[x]}" for x in a.counts)
                + f" | {a.d:.1%} |"
            )
        perp = amend[-1][1]
        out += [
            "",
            "Norway with a perpetuity total return, lag-1 acf by period (AR-null input): "
            + ", ".join(f"{st.p.label.split(' ')[0]} {st.acf1:+.3f} ({st.n1})" for st in perp.stats)
            + ".",
            "",
        ]
    return out


TIE = 1e-9  # log points; |I| below this is floating-point noise of a cumulative sum


def evaluate(label: str, segs: Sequence[i17.Seg], down: float, up: float) -> i17.Eval:
    """`insure1709.evaluate`, with I, the rebound B and the cash-rate I and N set to exactly 0
    where they are floating-point noise (the rule held throughout): insure1's sum of log
    differences leaves ~1e-14 there, which its sign test and headline count would otherwise
    score as a win (or loss) instead of a tie. N = I + B then inherits exact zeros."""
    ev = i17.evaluate(label, segs, down, up)
    for e in ev.eps:
        for f in ("ins", "rebound", "ins_tb", "net_tb"):
            if abs(getattr(e, f)) < TIE:
                setattr(e, f, 0.0)
    return ev


# --- null worlds at a given threshold ---


@dataclass
class Raw:
    series: str
    months: list[int]
    per: np.ndarray  # period index of each month (index 0 unused)
    x: np.ndarray  # observed log returns dated months[1:]


def raws_of(s: Series) -> tuple[list[Raw], list[np.ndarray]]:
    raws = []
    for run_ in i17.segments(s.lev):
        per = np.array(
            [next(i for i, p in enumerate(s.periods) if p.lo <= m <= p.hi) for m in run_]
        )
        raws.append(Raw(s.name, run_, per, i17.logrets(s.lev, run_)[1]))
    pools = []
    for p in s.periods:
        ms = [m for m in s.lev if p.lo <= m <= p.hi and m - 1 >= p.lo]
        pools.append(i17.logrets(s.lev, ms)[1])
    return raws, pools


def aaft_path(rng: np.random.Generator, x: np.ndarray) -> np.ndarray:
    """Amplitude-adjusted Fourier-transform surrogate (Theiler et al. 1992): Gaussianise by
    rank, randomise the Fourier phases, map back to the series' own values by rank."""
    n = len(x)
    order = np.argsort(np.argsort(x))
    g = np.sort(rng.standard_normal(n))[order]
    f = np.fft.rfft(g)
    ph = rng.uniform(0, 2 * np.pi, len(f))
    ph[0] = 0.0
    if n % 2 == 0:
        ph[-1] = 0.0
    s = np.fft.irfft(np.abs(f) * np.exp(1j * ph), n)
    return np.sort(x)[np.argsort(np.argsort(s))]


def world_gap(
    raws: Sequence[Raw], paths: Sequence[np.ndarray], rng: np.random.Generator, d: float
) -> float:
    segs, prs = [], []
    for raw, x in zip(raws, paths, strict=True):
        r_all = np.concatenate([[np.nan], np.expm1(x)])
        s = i17.build_seg(raw.series, raw.months, r_all)
        if s is None:
            continue
        segs.append(s)
        prs.append(i17.pairs_of(s.r, d, d))
    if not segs or not any(prs):
        return math.nan
    return i17.timing(segs, prs, i17.offsets(segs, WORLD_ROT, rng)).gap


def null_gaps(s: Series, kind: str, worlds: int, seed: int) -> np.ndarray:
    raws, pools = raws_of(s)
    rng = np.random.default_rng(seed)
    m = np.array([st.mean for st in s.stats])
    sd = np.array([st.sd for st in s.stats])
    phi = np.array([0.0 if kind == "iid" else float(np.clip(st.acf1, -0.9, 0.9)) for st in s.stats])
    out = np.full(worlds, np.nan)
    for w in range(worlds):
        if kind == "bb":
            paths = [i17.bb_path(rng, raw.per[1:], pools) for raw in raws]
        elif kind == "aaft":
            paths = [aaft_path(rng, raw.x) for raw in raws]
        else:
            paths = [i17.ar1_path(rng, raw.per[1:], m, sd, phi) for raw in raws]
        out[w] = world_gap(raws, paths, rng, s.d)
    return out


NULL_LABELS = {
    "ar1": "AR1: Gaussian AR(1), each source period's own mean, sd, lag-1 acf",
    "bb": "BB: stationary block bootstrap of each period's returns, mean block 3 m",
    "iid": "Reference: iid Gaussian (phi 0)",
    "aaft": "Description: AAFT phase-randomised surrogates (whole spectrum, own values)",
}
SEEDS = {"ar1": 0, "bb": 1, "iid": 2, "aaft": 3}


def nulls(s: Series, obs: float, worlds: int) -> i17.Nulls:
    return i17.Nulls({k: null_gaps(s, k, worlds, SEEDS[k]) for k in NULL_LABELS}, obs)


def null_rows(nl: i17.Nulls, worlds: int) -> list[str]:
    out = [
        f"| Null ({worlds:,} worlds) | Median gap G (5-95%) | p: worlds with G >= observed | "
        "Worlds without a fall |",
        "|---|---:|---:|---:|",
    ]
    for k, lab in NULL_LABELS.items():
        out.append(f"| {lab} | {i17.q(nl.gaps[k], '+.3f')} | {nl.p(k):.3f} | {nl.dropped(k)} |")
    return out + [
        "",
        f"Observed G {nl.obs:+.3f}; p_AR (larger of AR1 and BB) = {nl.p_ar:.3f}.",
        "",
    ]


# --- rows and report ---


def sharpe_cash(ev: i17.Eval) -> tuple[str, str, float, float, float, float]:
    """`insure1709.sharpe_row` with cash at the discount rate while out (card check 1)."""
    rule = np.concatenate([i17.rule_returns(s.pos, s.r, s.cash)[1:] for s in ev.segs])
    a, b, _, _, _, fl = i17.sharpe_row(ev)
    sh = float(rule.mean() / rule.std() * math.sqrt(12)) if rule.std() > 0 else 0.0
    eq = np.cumprod(1 + rule)
    return a, b, sh, float(eq[-1] - 1), float((1 - eq / np.maximum.accumulate(eq)).max()), fl


def log_rows(
    evs: Sequence[tuple[str, i17.Eval]],
    note: str | None = None,
    cash_evs: Sequence[tuple[str, i17.Eval]] = (),
) -> int:
    text = harness.TRIES.read_text()
    rows = []
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"
    if note and f"| {IDEA} | before scoring" not in text:
        rows.append(f"| {now} | {IDEA} | {note} | note | train | - | - | - | - | - | - |\n")
    for v, ev in evs:
        if f"| {IDEA} | {v} |" in text:
            continue
        a, b, sh, tot, mdd, fl = i17.sharpe_row(ev)
        rows.append(
            f"| {now} | {IDEA} | {v} | insure-check | train | {a} | {b} | {sh:.2f} | "
            f"{tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
        )
    for v, ev in cash_evs:
        if f"| {IDEA} | {v} |" in text:
            continue
        a, b, sh, tot, mdd, fl = sharpe_cash(ev)
        rows.append(
            f"| {now} | {IDEA} | {v} | insure-check | train | {a} | {b} | {sh:.2f} | "
            f"{tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(rows)
    return len(rows)


def before_note(nor: Series, con: Series) -> str:
    def part(s: Series) -> str:
        acfs = ", ".join(f"{st.p.label.split(' ')[0]} {st.acf1:+.2f}" for st in s.stats)
        cnt = "/".join(str(s.counts[x]) for x in LADDER)
        return f"{s.name} lag-1 acf {acfs}; falls 25/20/15/10% {cnt}, threshold {s.d:.0%}"

    return (
        "before scoring (card), monthly log total returns: "
        + "; ".join(part(s) for s in (nor, con))
        + " (research/results/insure-bonds-1.md)"
    )


def run(d: Data, log: bool, worlds: int = WORLDS) -> None:
    nor, con, note = series(d)
    text = [
        "# insure-bonds-1: crash insurance of monthly `tsmom12` on Norwegian government bonds "
        "1822-1984 and UK consols 1867-1926",
        "",
        "Card: `cards/insure-bonds-1.md`. Written by `lib/insurebonds1.py`. Log points = 100 x "
        "natural log, rule minus holding unless said otherwise. Total returns rebuilt from "
        "yields (Norway: 10-year par bond; consols: perpetuity). Cash earns 0 unless the row "
        "says otherwise.",
        "",
    ]
    amend = amended(d)
    text += before_rows(d, nor, con, note, amend)
    evs: list[tuple[str, i17.Eval]] = []
    verdicts = {}
    readings = [
        ("card", s.name, s, f"{'Norway (primary)' if s.name == 'norway' else 'UK consols'}")
        for s in (nor, con)
    ] + [(f"A{j + 1}", lab, a, lab) for j, (lab, a) in enumerate(amend)]
    amend_evs = []
    for tag, _, s, title in readings:
        ev = evaluate(s.name, s.segs, s.d, s.d)
        if sum(e.ins != 0 for e in ev.eps) < 5:
            nl = None
            v = "Too few falls"
        else:
            nl = nulls(s, ev.t.gap, worlds)
            v = i17.verdict(ev, nl.p_ar)
        key = s.name if tag == "card" else tag
        verdicts[key] = v
        head = "Card" if tag == "card" else f"Amendment {tag}"
        text += [f"## {head}: {title}, falls of {s.d:.1%} (rise {s.d:.1%})", ""]
        text += i17.episode_rows(ev, s.stats) + i17.test_rows(ev) + i17.control_rows(ev)
        text += (
            null_rows(nl, worlds)
            if nl
            else ["Nulls not run: fewer than 5 falls with I != 0 (the verdict is fixed).", ""]
        )
        text += [
            f"**Verdict ({head.lower()}, {title}): {v}** ({i17.qualifiers(ev)}). Headline: "
            f"lost less in {ev.k} of {ev.n} falls (ties against).",
            "",
        ]
        if tag == "card":
            evs.append((f"tsmom12m@insure-bonds-{s.name}", ev))
        else:
            v_name = {"A1": "norway-5pct", "A2": "consols-5pct", "A3": "norway-perpetuity-15pct"}
            evs.append((f"tsmom12m@insure-bonds-{v_name[tag]}", ev))
            amend_evs.append(ev)

    groups = i1.link(amend_evs[0].eps + amend_evs[1].eps)
    text += [
        "## Pooled description: Norway and consols at 5% (A1 + A2), linked clusters",
        "",
        "| # | First peak | Last trough | Series | Mean I | Mean S | Mean N |",
        "|---:|---|---|---|---:|---:|---:|",
    ]
    for j, g in enumerate(groups):
        text.append(
            f"| {j + 1} | {ym_str(i17.ym_of(min(e.peak for e in g)))} | "
            f"{ym_str(i17.ym_of(max(e.trough for e in g)))} | "
            f"{', '.join(sorted({e.series.split('-')[0] for e in g}))} | "
            f"{i1.cmean(g, lambda e: e.ins):+.0f} | {i1.cmean(g, lambda e: e.share):+.2f} | "
            f"{i1.cmean(g, lambda e: e.net):+.0f} |"
        )
    vals = [i1.cmean(g, lambda e: e.ins) for g in groups]
    k, n, p = i1.sign_test(vals)
    text += [
        "",
        f"Clusters with mean I > 0: {k} of {n} non-zero (sign p {p:.3g}), bootstrap p "
        f"{i1.boot(vals)[1]:.3f}."
        if vals
        else "No clusters.",
        "",
    ]

    # checks
    checks: list[tuple[str, i17.Eval]] = []
    nd, cd = amend[0][1].d, amend[1][1].d  # checks at A1/A2's 5% (at 10% they are empty)
    checks.append((
        "norway perpetuity",
        evaluate("Norway, perpetuity total return, 10%", make_segs(
            "norway", tr_levels(d.nor_y, perp_return), d.nor_cash), nor.d, nor.d),
    ))  # fmt: skip
    checks.append((
        "consols price only",
        evaluate("consols, price only (1/y), 5%", make_segs(
            "consols", tr_levels(d.con_y, price_return), d.con_cash), cd, cd),
    ))  # fmt: skip
    for s in (nor, con):
        for x in neighbours(s.d) + [0.075]:
            checks.append(
                (f"{s.name} {x:.1%}", evaluate(f"{s.name}, falls of {x:.1%}", s.segs, x, x))
            )
    for lab, lo, hi in (
        ("1822-1914", NOR_LO, ym(1914, 12)),
        ("1915-1984", ym(1913, 12), NOR_HI),
    ):
        segs = make_segs("norway", nor.lev, d.nor_cash, lo=lo, hi=hi)
        if segs:
            checks.append((f"norway {lab}", evaluate(f"Norway {lab} alone, 5%", segs, nd, nd)))
    checks.append((
        "norway A1 GOV 1820-1920",
        evaluate("Norway A1 GOV 1820-1920 (overlapping), 5%", make_segs(
            "norway", tr_levels(d.gov_y, par_return), d.nor_cash), nd, nd),
    ))  # fmt: skip
    for s, a in ((nor, amend[0][1]), (con, amend[1][1])):
        checks.append((
            f"{s.name} lag 1",
            evaluate(f"{s.name}, signal one month older (stale check), 5%",
                         make_segs(s.name, s.lev, s.cash, lag=1), a.d, a.d),
        ))  # fmt: skip

    text += ["## Checks (description)", ""] + i17.CHECK_HEAD
    for _, ev in evs:
        text.append(i17.check_line(ev))
    for _, ev in evs:
        text.append(i17.tb_eval(ev))
    text += [i17.check_line(ev) for _, ev in checks]
    text += [
        "",
        "p_rot: share of 1,000 rotations with mean S at least the rule's. Fixed exposure: the "
        "rule's mean position, no costs. The first rows are the card and amendment readings, "
        "then the same with cash at the discount rate (Norges Bank's for Norway, the BoE "
        "prime-paper rate for consols), then the checks at the threshold in their label.",
        "",
    ]
    for key, ev in checks:
        if key.endswith("lag 1") or key.startswith("norway 1") or key == "norway perpetuity":
            text += [f"### Episodes: {ev.label}", ""]
            stats = nor.stats if ev.segs[0].series == "norway" else con.stats
            text += i17.episode_rows(ev, stats)
    OUT.write_text("\n".join(text) + "\n")
    n_rows = (
        log_rows(
            evs + [(f"tsmom12m@insure-bonds-check-{k.replace(' ', '-')}", ev) for k, ev in checks],
            before_note(nor, con),
            [
                (f"tsmom12m@insure-bonds-check-{n}-cash-discount-rate", ev)
                for n, ev in (("norway", evs[0][1]), ("consols", evs[1][1]))
            ],  # fmt: skip
        )
        if log
        else 0
    )
    print(f"wrote {OUT}; verdicts {verdicts}; {n_rows} tries rows")


def main(argv: Sequence[str]) -> None:
    d = load()
    if argv and argv[0] == "before":
        nor, con, note = series(d)
        OUT.write_text(
            "# insure-bonds-1: before scoring\n\n"
            + "\n".join(before_rows(d, nor, con, note, amended(d)))
            + "\n"
        )
        print(OUT.read_text())
        return
    worlds = int(argv[argv.index("--worlds") + 1]) if "--worlds" in argv else WORLDS
    run(d, "--log" in argv, worlds)


if __name__ == "__main__":
    main(sys.argv[1:])
