"""insure-1709-1: trend's crash insurance on UK monthly share and consol prices 1709-1866.

    uv run python -I research/lib/insure1709.py before   # card's before-scoring table only
    uv run python -I research/lib/insure1709.py run [--log]

Card: research/cards/insure-1709-1.md. Data: the Bank of England's "A millennium of
macroeconomic data" v3.1 (OGL v3), the monthly long CSV cached by jst-autocorr-2
(`<cache_root>/jst-autocorr-2/boe/monthly.csv`) and, for the splice month and the other indices
of check 4, the workbook's M13 sheet (`<cache_root>/insure-1709-1/boe/millennium.xlsx`, read with
a small stdlib reader: no formula or macro is evaluated). Nothing after 1866-12 is parsed.

The rule is the project's monthly `tsmom12` (`trend_where_long.signals`, unchanged); episodes,
scores, tests and the fixed/rotation controls are `insure1`'s code, unchanged. New here: the
loader, the AR-preserving nulls (Gaussian AR(1) and a stationary block bootstrap) and the report.
"""

from __future__ import annotations

import csv
import math
import re
import sys
import zipfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import trend_where_long as twl  # noqa: E402

IDEA = "insure-1709-1"
LAST_YM = 1866 * 12 + 11  # 1866-12: UK stocks are scored from 1867 on (card)
COST = 0.0002
MIN_SCORED = 60
ROTATIONS, WORLDS, WORLD_ROT = 1000, 1000, 200
BLOCK = 3.0  # mean block length of the stationary bootstrap, months
OUT = harness.RESEARCH / "results" / "insure-1709-1.md"
CSV_REL = "jst-autocorr-2/boe/monthly.csv"
XLSX_REL = "insure-1709-1/boe/millennium.xlsx"
SHARES = "spliced-monthly-share-price-index-weighted-by-market"
CONSOL = "long-term-consols-yield-1753-2015-corrected-for-goschen-s"
CASH = "spliced-series-for-discount-rate-on-prime-short-term-paper"
M13 = "M13. Mthly share prices 1709+ "
# M13 columns (0-based) of the source indices (card, workbook header text)
M13_COLS = {
    "Neal": 2,
    "GRS with mines": 3,
    "GRS without mines": 4,
    "Hayek": 5,
    "Acheson cap-weighted": 6,
    "Acheson paid-up weighted": 7,
    "Acheson unweighted": 8,
    "spliced": 23,
}
CONSOL_SPLIT = 1823 * 12  # Neal to 1823-01 (card: Neal 1753-1823, end month), Odlyzko/NBER after

Levels = dict[int, float]  # ym (year * 12 + month - 1) -> level


def ym(year: int, month: int) -> int:
    return year * 12 + month - 1


def ym_str(m: int) -> str:
    return f"{m // 12}-{m % 12 + 1:02d}"


def month_end(m: int) -> date:
    return date((m + 1) // 12, (m + 1) % 12 + 1, 1) - timedelta(days=1)


# --- data ---


def cache_root() -> Path:
    from macro import cache_root as cr

    return cr()


def read_csv(path: Path, ids: Sequence[str], last: int = LAST_YM) -> dict[str, Levels]:
    """The BoE monthly long CSV: variable_id -> {ym: value}, months <= `last` only."""
    out: dict[str, Levels] = {v: {} for v in ids}
    with path.open(newline="") as fh:
        for r in csv.DictReader(fh):
            v = r["variable_id"]
            if v in out and r["value"].strip():
                m = ym(int(r["year"]), int(r["month"]))
                if m <= last:
                    out[v][m] = float(r["value"])
    return out


def _col(ref: str) -> int:
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):  # type: ignore[union-attr]
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_sheet(path: Path, name: str) -> list[dict[int, str]]:
    """Rows of one sheet as {column: raw text} (shared strings resolved), stdlib only."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rid = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    sheet = next(s for s in wb.iterfind(".//m:sheet", ns) if s.get("name") == name)
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = next(r.get("Target") for r in rels if r.get("Id") == sheet.get(rid))
    target = str(target).lstrip("/")
    target = target if target.startswith("xl/") else "xl/" + target
    sst = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iterfind("m:si", ns):
            sst.append("".join(t.text or "" for t in si.iter(f"{{{ns['m']}}}t")))
    rows = []
    for _, el in ET.iterparse(z.open(target)):
        if el.tag != f"{{{ns['m']}}}row":
            continue
        row = {}
        for c in el.iterfind("m:c", ns):
            v = c.find("m:v", ns)
            if v is None or v.text is None:
                continue
            row[_col(c.get("r", "A"))] = sst[int(v.text)] if c.get("t") == "s" else v.text
        rows.append(row)
        el.clear()
    return rows


MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def m13_columns(rows: Sequence[dict[int, str]], last: int = LAST_YM) -> dict[str, Levels]:
    """M13's source columns as levels, months <= `last` (year in column 0, month name in 1)."""
    out: dict[str, Levels] = {k: {} for k in M13_COLS}
    for r in rows:
        y, mo = r.get(0, ""), r.get(1, "")
        if not (y.replace(".0", "").isdigit() and mo in MONTHS):
            continue
        m = ym(int(float(y)), MONTHS.index(mo) + 1)
        if m > last:
            continue
        for k, j in M13_COLS.items():
            x = r.get(j)
            if x is not None and re.fullmatch(r"-?[0-9.]+(E-?[0-9]+)?", x):
                out[k][m] = float(x)
    return out


def splice_month(cols: dict[str, Levels], tol: float = 1e-6) -> tuple[int | None, int | None, str]:
    """First month whose spliced change equals the Acheson cap-weighted change, and the last
    month whose spliced change equals Neal's (card: identified after the card)."""
    sp, ne, ac = cols["spliced"], cols["Neal"], cols["Acheson cap-weighted"]

    def same(a: Levels, m: int) -> bool:
        return (
            all(k in a and k in sp for k in (m, m - 1))
            and abs(a[m] / a[m - 1] - sp[m] / sp[m - 1]) < tol
        )

    last_neal = max((m for m in sp if same(ne, m)), default=None)
    first_ach = min((m for m in sp if same(ac, m)), default=None)
    note = (
        f"last month matching Neal: {ym_str(last_neal) if last_neal else '-'}; "
        f"first matching Acheson: {ym_str(first_ach) if first_ach else '-'}"
    )
    if first_ach is None or (last_neal is not None and last_neal >= first_ach):
        return None, last_neal, note + " (ambiguous)"
    return first_ach, last_neal, note


def segments(lev: Levels) -> list[list[int]]:
    """Maximal runs of consecutive months with a value."""
    out: list[list[int]] = []
    for m in sorted(lev):
        if out and m == out[-1][-1] + 1:
            out[-1].append(m)
        else:
            out.append([m])
    return out


# --- before scoring: autocorrelation and stale prices ---


def logrets(lev: Levels, months: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
    """Monthly log returns dated m (m-1 to m) for months whose predecessor exists."""
    ms = [m for m in months if m - 1 in lev and m in lev]
    return np.array(ms, dtype=int), np.array([math.log(lev[m] / lev[m - 1]) for m in ms])


def acf(ms: np.ndarray, x: np.ndarray, lag: int) -> tuple[float, int]:
    """Lag-k acf, demeaned, pairs of months exactly k apart."""
    if len(x) < 3:
        return math.nan, 0
    d = x - x.mean()
    pos = {int(m): i for i, m in enumerate(ms)}
    pr = [(pos[int(m)], pos[int(m) + lag]) for m in ms if int(m) + lag in pos]
    if not pr:
        return math.nan, 0
    a, b = np.array([p[0] for p in pr]), np.array([p[1] for p in pr])
    return float((d[a] * d[b]).sum() / (d * d).sum()), len(pr)


@dataclass(frozen=True)
class Period:
    series: str
    label: str
    lo: int
    hi: int  # inclusive ym
    thin: bool
    timing: str


def periods(splice: int, neal_end: int) -> list[Period]:
    """Source periods. The middle share period (Gayer-Rostow-Schwartz without mines) was found
    by the splice check after the card, which had expected Neal to run to the Acheson splice."""
    return [
        Period("shares", "Neal (3 shares, unweighted)", 0, neal_end, True, "end month"),
        Period(
            "shares",
            "Gayer-Rostow-Schwartz excl. mines (63 companies)",
            neal_end + 1,
            splice - 1,
            False,
            "not stated",
        ),
        Period(
            "shares",
            "Acheson et al. (681 companies, cap-weighted)",
            splice,
            LAST_YM,
            False,
            "end month",
        ),
        Period("consols", "Neal (3% consols)", 0, CONSOL_SPLIT - 1, False, "end month"),
        Period("consols", "Odlyzko / NBER", CONSOL_SPLIT, LAST_YM, False, "not stated"),
    ]


@dataclass
class PStat:
    p: Period
    months: int
    missing: int
    acf1: float
    n1: int
    acf2: float
    n2: int
    zero: float
    mean: float
    sd: float

    @property
    def noise(self) -> float:
        return 1.645 / math.sqrt(self.n1) if self.n1 else math.nan

    @property
    def stale_suspect(self) -> bool:
        return self.acf1 > self.noise or self.zero > 0.20


def period_stats(lev: Levels, p: Period) -> PStat:
    ms_all = [m for m in lev if p.lo <= m <= p.hi]
    lo, hi = min(ms_all), max(ms_all)
    ms, x = logrets(lev, [m for m in ms_all if m - 1 >= p.lo])
    a1, n1 = acf(ms, x, 1)
    a2, n2 = acf(ms, x, 2)
    zero = float((np.abs(x) < 1e-12).mean()) if len(x) else math.nan
    return PStat(
        p,
        len(ms_all),
        hi - lo + 1 - len(ms_all),
        a1,
        n1,
        a2,
        n2,
        zero,
        float(x.mean()),
        float(x.std(ddof=1)),
    )


# --- rule and series ---


@dataclass
class Seg:
    """One segment: monthly levels and the rule's positions; index 0 = first decision month."""

    series: str
    months: list[int]  # scored months, months[0] = base (first decision month)
    r: np.ndarray  # holding's simple return dated months[i] (r[0] = 0)
    pos: np.ndarray  # position earning r[i] (pos[0] = pos[1])
    cash: np.ndarray  # cash simple return dated months[i] (0 unless check 1)


def holding_returns(lev: Levels, months: Sequence[int], income: Levels | None = None) -> np.ndarray:
    r = np.full(len(months), np.nan)
    for i in range(1, len(months)):
        r[i] = lev[months[i]] / lev[months[i - 1]] - 1
        if income is not None:
            r[i] += income[months[i - 1]]
    return r


def build_seg(
    series: str, months: Sequence[int], r_all: np.ndarray, lag: int = 0, cash: Levels | None = None
) -> Seg | None:
    """Signals by `trend_where_long.signals` on the segment's returns; the signal at the end of
    month k trades the return dated k + 1 + lag."""
    valid, on = twl.signals(r_all.reshape(-1, 1))
    first = int(np.argmax(valid[:, 0])) if valid[:, 0].any() else len(months)
    base = first + lag  # the month before the first scored month
    if len(months) - 1 - base < MIN_SCORED:
        return None
    idx = np.arange(base, len(months))
    pos = np.zeros(len(idx))
    pos[1:] = on[idx[1:] - 1 - lag, 0].astype(float)
    pos[0] = pos[1]
    r = r_all[idx].copy()
    r[0] = 0.0
    ms = [months[i] for i in idx]
    c = np.zeros(len(idx))
    if cash is not None:
        c[1:] = [cash.get(m - 1, 0.0) / 1200 for m in ms[1:]]
    return Seg(series, ms, r, pos, c)


def rule_returns(pos: np.ndarray, r: np.ndarray, cash: np.ndarray | None = None) -> np.ndarray:
    flips = np.abs(np.diff(pos, prepend=pos[:1]))
    out = pos * r - COST * flips
    if cash is not None:
        out = out + (1 - pos) * cash
    out[0] = 0.0
    return out


def to_series(s: Seg, j: int) -> i1.Series:
    px = np.cumprod(1 + s.r)
    rule = rule_returns(s.pos, s.r)
    return i1.Series(
        f"{s.series}-{j}", [month_end(m) for m in s.months], px, rule, rule.copy(), s.pos, s.cash
    )


# --- scoring on a set of segments ---


def pairs_of(r: np.ndarray, down: float = 0.25, up: float = 0.25) -> list[tuple[int, int]]:
    return i1.zigzag(np.cumprod(1 + r), down, up)[0]


@dataclass
class Book:
    """Per-episode S and pooled premium of K position sets on fixed episodes."""

    s_mean: np.ndarray  # (K,) mean S over all episodes
    prem: np.ndarray  # (K,) pooled premium
    s_eps: np.ndarray  # (K, episodes)


def book(
    segs: Sequence[Seg],
    poss: Sequence[np.ndarray],
    pairs: Sequence[Sequence[tuple[int, int]]],
    cost: bool = True,
) -> Book:
    """`poss[j]` is a (K, n_j) array of positions for segment j (K the same for all)."""
    s_cols, sum_i, total = [], 0.0, 0.0
    for s, pos, pr in zip(segs, poss, pairs, strict=True):
        pos = np.atleast_2d(pos)
        flips = np.abs(np.diff(pos, axis=1, prepend=pos[:, :1]))
        rule = pos * s.r - (COST * flips if cost else 0.0)
        rule[:, 0] = 0.0
        d = 100 * (np.log1p(rule) - np.log1p(s.r))
        cum = np.cumsum(d, axis=1)
        total = total + cum[:, -1]
        if pr:
            a = np.array([p[0] for p in pr])
            b = np.array([p[1] for p in pr])
            px = np.cumprod(1 + s.r)
            ins = cum[:, b] - cum[:, a]
            s_cols.append(ins / np.abs(100 * np.log(px[b] / px[a])))
            sum_i = sum_i + ins.sum(axis=1)
    k = np.atleast_2d(poss[0]).shape[0]
    s_eps = np.concatenate(s_cols, axis=1) if s_cols else np.zeros((k, 0))
    si = np.broadcast_to(np.asarray(sum_i, dtype=float), (k,))
    tot = np.broadcast_to(np.asarray(total, dtype=float), (k,))
    with np.errstate(divide="ignore", invalid="ignore"):
        prem = np.where(si > 0, -(tot - si) / si, np.inf)
    sm = s_eps.mean(axis=1) if s_eps.shape[1] else np.full(k, np.nan)
    return Book(sm, prem, s_eps)


def offsets(segs: Sequence[Seg], n: int, rng: np.random.Generator) -> np.ndarray:
    lmax = max(len(s.pos) for s in segs)
    return rng.integers(12, max(lmax - 12, 13), size=n)


def rotated(segs: Sequence[Seg], ks: np.ndarray) -> list[np.ndarray]:
    return [np.array([np.roll(s.pos, int(k) % len(s.pos)) for k in ks]) for s in segs]


@dataclass
class Timing:
    rule: Book
    fixed: Book
    rot: Book
    xs: list[float]

    @property
    def gap(self) -> float:
        return float(self.rule.s_mean[0] - self.rot.s_mean.mean())

    @property
    def p_rot(self) -> float:
        return float((self.rot.s_mean >= self.rule.s_mean[0] - 1e-12).mean())

    @property
    def p_prem(self) -> float:
        return float((self.rot.prem <= self.rule.prem[0] + 1e-12).mean())


def timing(
    segs: Sequence[Seg], pairs: Sequence[Sequence[tuple[int, int]]], ks: np.ndarray
) -> Timing:
    rule = book(segs, [s.pos for s in segs], pairs)
    xs = [float(s.pos[1:].mean()) for s in segs]
    fixed = book(
        segs, [np.full(len(s.pos), x) for s, x in zip(segs, xs, strict=True)], pairs, cost=False
    )
    rot = book(segs, rotated(segs, ks), pairs)
    return Timing(rule, fixed, rot, xs)


# --- AR-preserving worlds ---


@dataclass
class Raw:
    """A segment before the rule: its months, the period index of each month's return."""

    series: str
    months: list[int]
    per: np.ndarray  # period index of the return dated months[i] (i >= 1)


def ar1_path(
    rng: np.random.Generator, per: np.ndarray, m: np.ndarray, sd: np.ndarray, phi: np.ndarray
) -> np.ndarray:
    """Gaussian AR(1) log returns with period-specific mean, sd and lag-1 coefficient
    (standardised AR(1) z, x = m + sd z)."""
    n = len(per)
    z = np.empty(n)
    e = rng.standard_normal(n)
    z[0] = e[0]
    for t in range(1, n):
        ph = phi[per[t]]
        z[t] = ph * z[t - 1] + math.sqrt(1 - ph * ph) * e[t]
    return m[per] + sd[per] * z


def bb_path(
    rng: np.random.Generator, per: np.ndarray, pools: Sequence[np.ndarray], block: float = BLOCK
) -> np.ndarray:
    """Stationary bootstrap (Politis-Romano): each period's months drawn in blocks of mean
    length `block` from that period's own returns (circular)."""
    out = np.empty(len(per))
    cur, cur_p = -1, -1
    for t, p in enumerate(per):
        pool = pools[p]
        if p != cur_p or rng.random() < 1 / block:
            cur = int(rng.integers(len(pool)))
        else:
            cur = (cur + 1) % len(pool)
        cur_p = p
        out[t] = pool[cur]
    return out


def world_gap(
    raws: Sequence[Raw],
    paths: Sequence[np.ndarray],
    rng: np.random.Generator,
    n_rot: int = WORLD_ROT,
) -> tuple[float, float, int]:
    """(rule S, gap, episodes) on one synthetic world (log returns per segment)."""
    segs, prs = [], []
    for raw, x in zip(raws, paths, strict=True):
        r_all = np.concatenate([[np.nan], np.expm1(x)])
        s = build_seg(raw.series, raw.months, r_all)
        if s is None:
            continue
        segs.append(s)
        prs.append(pairs_of(s.r))
    if not segs or not any(prs):
        return math.nan, math.nan, 0
    t = timing(segs, prs, offsets(segs, n_rot, rng))
    return float(t.rule.s_mean[0]), t.gap, sum(len(p) for p in prs)


def null_gaps(
    raws: Sequence[Raw],
    kind: str,
    stats: Sequence[PStat],
    pools: Sequence[np.ndarray],
    worlds: int,
    seed: int,
) -> np.ndarray:
    """Gap G of `worlds` synthetic worlds; kind 'ar1', 'iid' or 'bb'. NaN where no fall."""
    rng = np.random.default_rng(seed)
    m = np.array([s.mean for s in stats])
    sd = np.array([s.sd for s in stats])
    phi = np.array([0.0 if kind == "iid" else float(np.clip(s.acf1, -0.9, 0.9)) for s in stats])
    out = np.full(worlds, np.nan)
    for w in range(worlds):
        if kind == "bb":
            paths = [bb_path(rng, raw.per[1:], pools) for raw in raws]
        else:
            paths = [ar1_path(rng, raw.per[1:], m, sd, phi) for raw in raws]
        out[w] = world_gap(raws, paths, rng)[1]
    return out


# --- loading ---


@dataclass
class Data:
    shares: Levels
    consols: Levels  # perpetuity price 1 / y
    yld: Levels  # consol yield, % a year
    cash: Levels  # discount rate, % a year
    cols: dict[str, Levels]  # M13 source columns
    splice: int
    neal_end: int
    splice_note: str
    csv_vs_xlsx: float  # largest abs. relative gap, CSV spliced against workbook spliced


def load(root: Path | None = None) -> Data:
    root = root or cache_root()
    c = read_csv(root / CSV_REL, [SHARES, CONSOL, CASH])
    cols = m13_columns(xlsx_sheet(root / XLSX_REL, M13))
    sp, ne, note = splice_month(cols)
    if sp is None:
        sp, note = ym(1825, 3), note + "; card default 1825-03 used"
    ne = sp - 1 if ne is None else ne
    common = [m for m in c[SHARES] if m in cols["spliced"]]
    gap = max(abs(c[SHARES][m] / cols["spliced"][m] - 1) for m in common) if common else math.nan
    yld = {m: y for m, y in c[CONSOL].items() if y > 0}
    return Data(
        c[SHARES], {m: 1 / y for m, y in yld.items()}, yld, c[CASH], cols, sp, ne, note, gap
    )


def series_levels(d: Data, name: str) -> Levels:
    return d.shares if name == "shares" else d.consols


def before_rows(d: Data) -> list[str]:
    out = [
        "## Before scoring (card): sampling, splice and autocorrelation",
        "",
        f"Splice of the share index (M13, monthly changes matched to 1e-6): {d.splice_note}. "
        f"So Neal to {ym_str(d.neal_end)}, Gayer-Rostow-Schwartz without mines (the only M13 "
        f"column whose changes match in between) {ym_str(d.neal_end + 1)} to "
        f"{ym_str(d.splice - 1)}, Acheson et al. from {ym_str(d.splice)}. Cached CSV against "
        f"the workbook's spliced column: largest relative difference {d.csv_vs_xlsx:.1e} "
        f"({len([m for m in d.shares if m in d.cols['spliced']])} common months).",
        "",
    ]
    for name in ("shares", "consols"):
        lev = series_levels(d, name)
        segs = segments(lev)
        out.append(
            f"{name}: {len(lev)} months {ym_str(min(lev))} to {ym_str(max(lev))}, "
            f"{len(segs)} runs of consecutive months: "
            + ", ".join(f"{ym_str(s[0])}..{ym_str(s[-1])} ({len(s)})" for s in segs)
            + "."
        )
        out.append("")
    out += [
        "| Series | Source period | Timing (documented) | Thin | Months | Missing inside | "
        "Lag-1 acf (pairs) | Noise line | Lag-2 acf | Zero-change months | Stale-suspect |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for st in all_stats(d):
        p = st.p
        out.append(
            f"| {p.series} | {p.label} {ym_str(max(p.lo, min(series_levels(d, p.series))))}-"
            f"{ym_str(min(p.hi, LAST_YM))} | {p.timing} | {'yes' if p.thin else 'no'} | "
            f"{st.months} | {st.missing} | {st.acf1:+.3f} ({st.n1}) | {st.noise:.3f} | "
            f"{st.acf2:+.3f} | {st.zero:.1%} | {'yes' if st.stale_suspect else 'no'} |"
        )
    out += [
        "",
        "Monthly log returns, demeaned per source period, pairs exactly 1 (2) months apart within "
        "the period. Noise line 1.645/sqrt(pairs). Stale-suspect: lag-1 acf above its noise "
        "line or more than 20% zero-change months (card).",
        "",
    ]
    return out


def all_stats(d: Data) -> list[PStat]:
    return [period_stats(series_levels(d, p.series), p) for p in periods(d.splice, d.neal_end)]


# --- evaluation ---


@dataclass
class Eval:
    label: str
    segs: list[Seg]
    scored: list[i1.Scored]
    eps: list[i1.Episode]
    t: Timing
    ks: np.ndarray

    @property
    def n(self) -> int:
        return len(self.eps)

    @property
    def k(self) -> int:
        return sum(e.ins > 0 for e in self.eps)

    def tests(self, f: Callable[[i1.Episode], float]) -> tuple[int, int, float, float, float]:
        vals = [f(e) for e in self.eps]
        k, n, p = i1.sign_test(vals)
        m, bp, _, _ = i1.boot(vals) if vals else (math.nan, 1.0, 0.0, 0.0)
        return k, n, p, m, bp

    @property
    def calm_drag(self) -> float:
        months = sum(int((~x.in_mask[1:]).sum()) for x in self.scored)
        return sum(x.calm for x in self.scored) / (months / 12) if months else math.nan

    @property
    def prem(self) -> float:
        si = sum(e.ins for e in self.eps)
        sb = sum(e.rebound for e in self.eps)
        c = sum(x.calm for x in self.scored)
        return -(sb + c) / si if si > 0 else math.inf


def evaluate(
    label: str, segs: Sequence[Seg], down: float = 0.25, up: float = 0.25, n_rot: int = ROTATIONS
) -> Eval:
    ser = [to_series(s, j) for j, s in enumerate(segs)]
    sc = [i1.score(x, down, up) for x in ser]
    prs = [pairs_of(s.r, down, up) for s in segs]
    ks = offsets(segs, n_rot, np.random.default_rng(i1.SEED))
    t = timing(segs, prs, ks)
    eps = [e for x in sc for e in x.eps]
    # the vectorised S must equal insure1's episode shares
    if eps and abs(float(np.mean([e.share for e in eps])) - float(t.rule.s_mean[0])) > 1e-9:
        raise AssertionError(f"{label}: S mismatch")
    return Eval(label, list(segs), sc, eps, t, ks)


def make_segs(
    d: Data,
    name: str,
    lev: Levels | None = None,
    lag: int = 0,
    lo: int = 0,
    hi: int = LAST_YM,
    income: bool = False,
) -> list[Seg]:
    lev = series_levels(d, name) if lev is None else lev
    lev = {m: x for m, x in lev.items() if lo <= m <= hi}
    inc = {m: y / 1200 for m, y in d.yld.items()} if income else None
    out = []
    for run_ in segments(lev):
        r_all = holding_returns(lev, run_, inc)
        s = build_seg(name, run_, r_all, lag, d.cash)  # cash fills insure1's T-bill reading
        if s is not None:
            out.append(s)
    return out


def raws_of(d: Data, name: str, stats: Sequence[PStat]) -> tuple[list[Raw], list[np.ndarray]]:
    """Segments as raw month runs with the period index of each month, and per-period pools
    of observed log returns (all periods of all series, indexed like `stats`)."""
    lev = series_levels(d, name)
    raws = []
    for run_ in segments(lev):
        per = np.array(
            [
                next(
                    i
                    for i, st in enumerate(stats)
                    if st.p.series == name and st.p.lo <= m <= st.p.hi
                )
                for m in run_
            ]
        )
        raws.append(Raw(name, run_, per))
    pools = []
    for st in stats:
        lv = series_levels(d, st.p.series)
        ms = [m for m in lv if st.p.lo <= m <= st.p.hi]
        pools.append(logrets(lv, [m for m in ms if m - 1 >= st.p.lo])[1])
    return raws, pools


def q(a: np.ndarray, fmt: str = "+.2f") -> str:
    a = a[np.isfinite(a)]
    lo, mid, hi = np.quantile(a, [0.05, 0.5, 0.95])
    return f"{mid:{fmt}} ({lo:{fmt}} to {hi:{fmt}})"


def verdict(ev: Eval, p_ar: float) -> str:
    _, n_i, p_i, _, bp_i = ev.tests(lambda e: e.ins)
    if n_i < 5:
        return "Too few falls"
    if not (p_i < 0.05 and bp_i < 0.05):
        return "Does not hold"
    if ev.t.p_rot < 0.05:
        return (
            "Holds, timing beyond autocorrelation"
            if p_ar < 0.05
            else "Holds, timing not separable from autocorrelation"
        )
    return "In between" if ev.t.p_rot < 0.10 else "Holds only as lower exposure"


def qualifiers(ev: Eval) -> str:
    _, _, p_n, _, bp_n = ev.tests(lambda e: e.net)
    share = ev.k / ev.n if ev.n else math.nan
    return "; ".join(
        [
            "at the claimed strength" if share >= 0.80 else "weaker than claimed",
            "kept" if p_n < 0.05 and bp_n < 0.05 else "handed back in the rebound",
            "cheaper than holding less"
            if ev.t.rule.prem[0] < ev.t.fixed.prem[0]
            else "not cheaper than holding less",
        ]
    )


def period_of(stats: Sequence[PStat], series: str, m: int) -> str:
    return next(
        (
            st.p.label.split(" (")[0]
            for st in stats
            if st.p.series == series and st.p.lo <= m <= st.p.hi
        ),
        "-",
    )


def ym_of(d: date) -> int:
    return ym(d.year, d.month)


def episode_rows(ev: Eval, stats: Sequence[PStat]) -> list[str]:
    out = [
        "| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B "
        "(12 m) | N | Source at peak |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for j, e in enumerate(ev.eps):
        a, b = ym_of(e.peak), ym_of(e.trough)
        out.append(
            f"| {j + 1} | {ym_str(a)} | {ym_str(b)} | {b - a} | {e.depth:.0%} | {e.hold:+.0f} | "
            f"{e.rule:+.0f} | {e.ins:+.0f} | {e.share:+.2f} | {e.rebound:+.0f} | {e.net:+.0f} | "
            f"{period_of(stats, ev.segs[0].series, a)} |"
        )
    open_ = [x.open_peak for x in ev.scored if x.open_peak]
    out += ["", f"Unfinished fall at the end (peak): {', '.join(map(str, open_)) or 'none'}.", ""]
    return out


def test_rows(ev: Eval) -> list[str]:
    out = [
        "| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | "
        "Bootstrap p |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for lab, f in (
        ("I (insurance)", lambda e: e.ins),
        ("N = I + B (net of rebound)", lambda e: e.net),
        ("I with cash at the discount rate", lambda e: e.ins_tb),
    ):
        k, n, p, m, bp = ev.tests(f)
        out.append(f"| {lab} | {n} | {k} | {p:.3g} | {m:+.1f} | {bp:.3f} |")
    return out + [""]


def control_rows(ev: Eval) -> list[str]:
    t = ev.t
    return [
        "| | Mean S (share avoided) | Pooled premium P |",
        "|---|---:|---:|",
        f"| `tsmom12` monthly | {t.rule.s_mean[0]:+.2f} | {t.rule.prem[0]:.2f} |",
        f"| Fixed exposure (x = {', '.join(f'{x:.0%}' for x in t.xs)}) | "
        f"{t.fixed.s_mean[0]:+.2f} | {t.fixed.prem[0]:.2f} |",
        f"| Random dates (1,000 rotations, median, 5-95%) | {q(t.rot.s_mean)} | "
        f"{q(t.rot.prem[np.isfinite(t.rot.prem)])} |",
        f"| p: rotations at least as good | {t.p_rot:.3f} | {t.p_prem:.3f} |",
        "",
        f"Timing gap G = rule S minus mean rotation S: {t.gap:+.3f}. Calm drag (rule minus "
        f"holding per calm year): {ev.calm_drag:+.2f} log points. Premium from insure1's "
        f"decomposition: {ev.prem:.2f}.",
        "",
    ]


@dataclass
class Nulls:
    gaps: dict[str, np.ndarray]
    obs: float

    def p(self, kind: str) -> float:
        g = self.gaps[kind]
        g = g[np.isfinite(g)]
        return float((g >= self.obs - 1e-12).mean()) if len(g) else math.nan

    def dropped(self, kind: str) -> int:
        return int((~np.isfinite(self.gaps[kind])).sum())

    @property
    def p_ar(self) -> float:
        return max(self.p("ar1"), self.p("bb"))


def nulls(d: Data, name: str, stats: Sequence[PStat], obs: float, worlds: int) -> Nulls:
    raws, pools = raws_of(d, name, stats)
    gaps = {
        "ar1": null_gaps(raws, "ar1", stats, pools, worlds, 0),
        "bb": null_gaps(raws, "bb", stats, pools, worlds, 1),
        "iid": null_gaps(raws, "iid", stats, pools, worlds, 2),
    }
    return Nulls(gaps, obs)


def null_rows(nl: Nulls) -> list[str]:
    lab = {
        "ar1": "AR1: Gaussian AR(1), each source period's own mean, sd, lag-1 acf",
        "bb": f"BB: stationary block bootstrap of each period's returns, mean block {BLOCK:.0f} m",
        "iid": "Reference: iid Gaussian (phi 0), the event definition alone",
    }
    out = [
        "| Null (1,000 worlds) | Median gap G (5-95%) | p: worlds with G >= observed | "
        "Worlds without a fall |",
        "|---|---:|---:|---:|",
    ]
    for k in ("ar1", "bb", "iid"):
        out.append(f"| {lab[k]} | {q(nl.gaps[k], '+.3f')} | {nl.p(k):.3f} | {nl.dropped(k)} |")
    return out + ["", f"Observed G {nl.obs:+.3f}; p_AR (larger of AR1 and BB) = {nl.p_ar:.3f}.", ""]


def check_line(ev: Eval) -> str:
    k, n, p, m, bp = ev.tests(lambda e: e.ins)
    kn, nn, pn, _, _ = ev.tests(lambda e: e.net)
    t = ev.t
    return (
        f"| {ev.label} | {ev.n} | {ev.k} of {ev.n} | {p:.3g} / {bp:.3f} | {kn} of {nn} | "
        f"{t.rule.s_mean[0]:+.2f} / {t.fixed.s_mean[0]:+.2f} / "
        f"{float(np.median(t.rot.s_mean)):+.2f} ({t.p_rot:.3f}) | {t.gap:+.3f} | "
        f"{t.rule.prem[0]:.2f} / {t.fixed.prem[0]:.2f} | {ev.calm_drag:+.2f} |"
    )


CHECK_HEAD = [
    "| Run | Falls | I > 0 (ties against) | Sign p / boot p | N > 0 | S rule / fixed / random "
    "(p_rot) | Gap G | P rule / fixed | Calm drag a year |",
    "|---|---:|---|---|---|---|---:|---|---:|",
]


def tb_eval(ev: Eval) -> str:
    """Check 1: the same run with cash at the discount rate (insure1's T-bill reading)."""
    eps = ev.eps
    k = sum(e.ins_tb > 0 for e in eps)
    p = i1.sign_test([e.ins_tb for e in eps])[2]
    bp = i1.boot([e.ins_tb for e in eps])[1] if eps else 1.0
    kn = sum(e.net_tb > 0 for e in eps)
    s_tb = float(np.mean([e.ins_tb / abs(e.hold) for e in eps])) if eps else math.nan
    si = sum(e.ins_tb for e in eps)
    rest = sum(e.net_tb - e.ins_tb for e in eps) + sum(x.calm_tb for x in ev.scored)
    months = sum(int((~x.in_mask[1:]).sum()) for x in ev.scored)
    return (
        f"| {ev.label}, cash at the discount rate | {len(eps)} | {k} of {len(eps)} | "
        f"{p:.3g} / {bp:.3f} | {kn} of {len(eps)} | {s_tb:+.2f} / - / - | - | "
        f"{-rest / si if si > 0 else math.inf:.2f} / - | "
        f"{sum(x.calm_tb for x in ev.scored) / (months / 12):+.2f} |"
    )


def sharpe_row(ev: Eval) -> tuple[str, str, float, float, float, float]:
    rule = np.concatenate([rule_returns(s.pos, s.r)[1:] for s in ev.segs])
    pos = np.concatenate([s.pos for s in ev.segs])
    sh = float(rule.mean() / rule.std() * math.sqrt(12)) if rule.std() > 0 else 0.0
    eq = np.cumprod(1 + rule)
    mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
    years = len(rule) / 12
    flips = float(np.abs(np.diff(pos)).sum()) / years
    first = month_end(ev.segs[0].months[1]).isoformat()
    last = month_end(ev.segs[-1].months[-1]).isoformat()
    return first, last, sh, float(eq[-1] - 1), mdd, flips


def log_rows(evs: Sequence[tuple[str, Eval]]) -> int:
    text = harness.TRIES.read_text()
    rows = []
    for v, ev in evs:
        if f"| {IDEA} | {v} |" in text:
            continue
        a, b, sh, tot, mdd, fl = sharpe_row(ev)
        rows.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | insure-check | "
            f"train | {a} | {b} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(rows)
    return len(rows)


def run(d: Data, log: bool, worlds: int = WORLDS) -> None:
    stats = all_stats(d)
    text = [
        "# insure-1709-1: crash insurance of monthly `tsmom12` on UK shares and consols, 1709-1866",
        "",
        "Card: `cards/insure-1709-1.md`. Written by `lib/insure1709.py`. Log points = 100 x "
        "natural log, rule minus holding unless said otherwise. Cash earns 0 unless the row "
        "says otherwise. Price indices (no dividends, no coupons unless stated).",
        "",
    ]
    text += before_rows(d)
    evs: list[tuple[str, Eval]] = []
    verdicts = {}
    for name, title in (("shares", "UK shares (primary)"), ("consols", "Consols (secondary)")):
        ev = evaluate(name, make_segs(d, name))
        nl = nulls(d, name, stats, ev.t.gap, worlds)
        v = verdict(ev, nl.p_ar)
        verdicts[name] = v
        text += [f"## {title}: 25% falls", ""]
        text += episode_rows(ev, stats) + test_rows(ev) + control_rows(ev) + null_rows(nl)
        text += [
            f"**Verdict by the card ({name}): {v}** ({qualifiers(ev)}). Headline: lost less "
            f"in {ev.k} of {ev.n} falls (ties against).",
            "",
        ]
        evs.append((f"tsmom12m@insure-1709-{name}", ev))

    # pooled description: linked clusters across shares and consols
    pooled = evs[0][1].eps + evs[1][1].eps
    groups = i1.link(pooled)
    text += [
        "## Pooled description: shares and consols, linked clusters",
        "",
        "| # | First peak | Last trough | Series | Mean I | Mean S | Mean N |",
        "|---:|---|---|---|---:|---:|---:|",
    ]
    for j, g in enumerate(groups):
        text.append(
            f"| {j + 1} | {ym_str(ym_of(min(e.peak for e in g)))} | "
            f"{ym_str(ym_of(max(e.trough for e in g)))} | "
            f"{', '.join(sorted({e.series.split('-')[0] for e in g}))} | "
            f"{i1.cmean(g, lambda e: e.ins):+.0f} | {i1.cmean(g, lambda e: e.share):+.2f} | "
            f"{i1.cmean(g, lambda e: e.net):+.0f} |"
        )
    vals = [i1.cmean(g, lambda e: e.ins) for g in groups]
    k, n, p = i1.sign_test(vals)
    text += [
        "",
        f"Clusters with mean I > 0: {k} of {n} non-zero (sign p {p:.3g}), "
        f"bootstrap p {i1.boot(vals)[1]:.3f}.",
        "",
    ]

    # checks
    sh = evs[0][1]
    checks: list[tuple[str, Eval]] = []
    text += ["## Checks (description)", ""] + CHECK_HEAD
    text.append(check_line(sh))
    text.append(tb_eval(sh))
    text.append(tb_eval(evs[1][1]))
    for down, up in ((0.20, 0.20), (0.40, 0.25)):
        checks.append(
            (
                f"shares {down:.0%}/{up:.0%}",
                evaluate(
                    f"shares, {down:.0%} fall / {up:.0%} rise", make_segs(d, "shares"), down, up
                ),
            )
        )
    for st in stats:
        if st.p.series != "shares":
            continue
        lab = st.p.label.split(" (")[0]
        segs = make_segs(d, "shares", lo=st.p.lo, hi=st.p.hi)
        if segs:
            checks.append((f"shares {lab} alone", evaluate(f"shares, {lab} alone", segs)))
    for col, lo, hi in (
        ("Acheson paid-up weighted", ym(1825, 3), LAST_YM),
        ("Acheson unweighted", ym(1825, 3), LAST_YM),
        ("GRS with mines", 0, LAST_YM),
        ("GRS without mines", 0, LAST_YM),
        ("Hayek", 0, LAST_YM),
    ):
        segs = make_segs(d, "shares", lev=d.cols[col], lo=lo, hi=hi)
        if segs:
            checks.append((f"index {col}", evaluate(f"index: {col}", segs)))
    checks.append(
        (
            "shares lag 1",
            evaluate("shares, signal one month older (stale check)", make_segs(d, "shares", lag=1)),
        )
    )
    checks.append(
        (
            "consols lag 1",
            evaluate("consols, signal one month older", make_segs(d, "consols", lag=1)),
        )
    )
    checks.append(
        (
            "consols total return",
            evaluate("consols with coupon accrual", make_segs(d, "consols", income=True)),
        )
    )
    text += [check_line(ev) for _, ev in checks]
    text += [
        "",
        "p_rot: share of 1,000 rotations with mean S at least the rule's. Fixed "
        "exposure: the rule's mean position, no costs. Check 4's indices overlap the "
        "primary's calendar (not independent).",
        "",
    ]
    # per-check episode lists for the stale check and per-period runs
    for key, ev in checks:
        if key in ("shares lag 1",) or key.endswith("alone"):
            text += [f"### Episodes: {ev.label}", ""] + episode_rows(ev, stats)
    OUT.write_text("\n".join(text) + "\n")
    n_rows = (
        log_rows(
            evs + [(f"tsmom12m@insure-1709-check-{k.replace(' ', '-')}", ev) for k, ev in checks]
        )
        if log
        else 0
    )
    print(f"wrote {OUT}; verdicts {verdicts}; {n_rows} tries rows")


def main(argv: Sequence[str]) -> None:
    d = load()
    if argv and argv[0] == "before":
        text = "\n".join(before_rows(d)) + "\n"
        print(text)
        return
    worlds = int(argv[argv.index("--worlds") + 1]) if "--worlds" in argv else WORLDS
    run(d, "--log" in argv, worlds)


if __name__ == "__main__":
    main(sys.argv[1:])
