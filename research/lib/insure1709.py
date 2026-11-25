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
    "Neal": 2, "GRS with mines": 3, "GRS without mines": 4, "Hayek": 5,
    "Acheson cap-weighted": 6, "Acheson paid-up weighted": 7, "Acheson unweighted": 8,
    "spliced": 23,
}  # fmt: skip
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
            if x is not None:
                try:
                    out[k][m] = float(x)
                except ValueError:
                    pass
    return out


def splice_month(
    cols: dict[str, Levels], tol: float = 1e-6
) -> tuple[int | None, int | None, str]:
    """First month whose spliced change equals the Acheson cap-weighted change, and the last
    month whose spliced change equals Neal's (card: identified after the card)."""
    sp, ne, ac = cols["spliced"], cols["Neal"], cols["Acheson cap-weighted"]

    def same(a: Levels, m: int) -> bool:
        return all(k in a and k in sp for k in (m, m - 1)) and abs(
            a[m] / a[m - 1] - sp[m] / sp[m - 1]
        ) < tol

    last_neal = max((m for m in sp if same(ne, m)), default=None)
    first_ach = min((m for m in sp if same(ac, m)), default=None)
    note = (f"last month matching Neal: {ym_str(last_neal) if last_neal else '-'}; "
            f"first matching Acheson: {ym_str(first_ach) if first_ach else '-'}")  # fmt: skip
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
        Period("shares", "Gayer-Rostow-Schwartz excl. mines (63 companies)", neal_end + 1,
               splice - 1, False, "not stated"),  # fmt: skip
        Period("shares", "Acheson et al. (681 companies, cap-weighted)", splice, LAST_YM, False,
               "end month"),  # fmt: skip
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
    return PStat(p, len(ms_all), hi - lo + 1 - len(ms_all), a1, n1, a2, n2, zero,
                 float(x.mean()), float(x.std(ddof=1)))  # fmt: skip


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


def build_seg(series: str, months: Sequence[int], r_all: np.ndarray, lag: int = 0,
              cash: Levels | None = None) -> Seg | None:  # fmt: skip
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
    return i1.Series(f"{s.series}-{j}", [month_end(m) for m in s.months], px, rule, rule.copy(),
                     s.pos, s.cash)  # fmt: skip


# --- scoring on a set of segments ---


def pairs_of(r: np.ndarray, down: float = 0.25, up: float = 0.25) -> list[tuple[int, int]]:
    return i1.zigzag(np.cumprod(1 + r), down, up)[0]


@dataclass
class Book:
    """Per-episode S and pooled premium of K position sets on fixed episodes."""

    s_mean: np.ndarray  # (K,) mean S over all episodes
    prem: np.ndarray  # (K,) pooled premium
    s_eps: np.ndarray  # (K, episodes)


def book(segs: Sequence[Seg], poss: Sequence[np.ndarray], pairs: Sequence[Sequence[tuple[int, int]]],
         cost: bool = True) -> Book:  # fmt: skip
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


def timing(segs: Sequence[Seg], pairs: Sequence[Sequence[tuple[int, int]]], ks: np.ndarray) -> Timing:
    rule = book(segs, [s.pos for s in segs], pairs)
    xs = [float(s.pos[1:].mean()) for s in segs]
    fixed = book(segs, [np.full(len(s.pos), x) for s, x in zip(segs, xs, strict=True)], pairs,
                 cost=False)  # fmt: skip
    rot = book(segs, rotated(segs, ks), pairs)
    return Timing(rule, fixed, rot, xs)


# --- AR-preserving worlds ---


@dataclass
class Raw:
    """A segment before the rule: its months, the period index of each month's return."""

    series: str
    months: list[int]
    per: np.ndarray  # period index of the return dated months[i] (i >= 1)


def ar1_path(rng: np.random.Generator, per: np.ndarray, m: np.ndarray, sd: np.ndarray,
             phi: np.ndarray) -> np.ndarray:  # fmt: skip
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


def bb_path(rng: np.random.Generator, per: np.ndarray, pools: Sequence[np.ndarray],
            block: float = BLOCK) -> np.ndarray:  # fmt: skip
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


def world_gap(raws: Sequence[Raw], paths: Sequence[np.ndarray], rng: np.random.Generator,
              n_rot: int = WORLD_ROT) -> tuple[float, float, int]:  # fmt: skip
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


def null_gaps(raws: Sequence[Raw], kind: str, stats: Sequence[PStat], pools: Sequence[np.ndarray],
              worlds: int, seed: int) -> np.ndarray:  # fmt: skip
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
    return Data(c[SHARES], {m: 1 / y for m, y in yld.items()}, yld, c[CASH], cols, sp, ne, note,
                gap)  # fmt: skip


def series_levels(d: Data, name: str) -> Levels:
    return d.shares if name == "shares" else d.consols


def before_rows(d: Data) -> list[str]:
    out = [
        "## Before scoring (card): sampling, splice and autocorrelation",
        "",
        f"Splice of the share index (M13, monthly changes matched to 1e-6): {d.splice_note}. "
        f"So Neal to {ym_str(d.neal_end)}, Gayer-Rostow-Schwartz without mines (the only M13 "
        f"column whose changes match in between) {ym_str(d.neal_end + 1)} to "
        f"{ym_str(d.splice - 1)}, Acheson et al. from {ym_str(d.splice)}. Cached CSV against the workbook's spliced "
        f"column: largest relative difference {d.csv_vs_xlsx:.1e} "
        f"({len([m for m in d.shares if m in d.cols['spliced']])} common months).",
        "",
    ]
    for name in ("shares", "consols"):
        lev = series_levels(d, name)
        segs = segments(lev)
        out.append(f"{name}: {len(lev)} months {ym_str(min(lev))} to {ym_str(max(lev))}, "
                   f"{len(segs)} runs of consecutive months: "
                   + ", ".join(f"{ym_str(s[0])}..{ym_str(s[-1])} ({len(s)})" for s in segs)
                   + ".")  # fmt: skip
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


def main(argv: Sequence[str]) -> None:
    d = load()
    if argv and argv[0] == "before":
        text = "\n".join(before_rows(d)) + "\n"
        print(text)
        return
    run(d, "--log" in argv)


if __name__ == "__main__":
    main(sys.argv[1:])
