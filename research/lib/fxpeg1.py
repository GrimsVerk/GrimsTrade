"""fx-peg-1: a real-time peg filter for long FX histories, then trend on the floating spells.

    uv run python -I research/lib/fxpeg1.py before          # card's before-scoring table only
    uv run python -I research/lib/fxpeg1.py run [--log] [--worlds N]

Card: research/cards/fx-peg-1.md. Data (read locally, never committed):
- Bank of England, "A millennium of macroeconomic data" v3.1 (OGL v3), sheet M15 ($ per GBP,
  1791-), the workbook cached by insure-1709-1 (`<cache_root>/insure-1709-1/boe/millennium.xlsx`);
- Norges Bank Historical Monetary Statistics, exchange rates (Klovland 2004), Tables A1 (end of
  month, 1819-1914) and A2 (monthly averages, 1914-), cached by data-wide-2
  (`<cache_root>/data-wide-2/probe/nb-fx.xlsx`);
- Ilzetzki, Reinhart and Rogoff (2019, 2021) de facto classification (fine codes, monthly
  1940-2019) and anchors (monthly 1946-2019), stable versions, fetched by this lane into
  `<cache_root>/fx-peg-1/irr/` (agreement check only, never a rule input).

Step 1 is `classify` (trailing 24-month Reinhart-Rogoff band test) and the chronology check
(`CHRONOLOGY`, `irr_pair_labels`, `agreement`). Step 2 scores monthly `tsmom12` on the floating
spells with insure1 / insure1709 code (episodes, S, rotations) and new joint autocorrelation-
preserving nulls (`JointWorlds`). Nothing after 1970-12 is parsed.
"""

from __future__ import annotations

import math
import re
import sys
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import datawide2 as dw  # noqa: E402
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import insure1709 as i9  # noqa: E402

IDEA = "fx-peg-1"
LAST_YM = 1970 * 12 + 11  # 1970-12: scored FX coverage starts 1971 (card)
JOIN = 1915 * 12  # first month whose change comes from Table A2 for currencies in both tables
LOOKBACK = 12
WINDOW, BAND, SHARE = 24, 0.01, 0.80  # filter (card)
MIN_SEG = 12
FALL = (0.15, 0.15)
ROTATIONS, WORLDS, WORLD_ROT = 1000, 1000, 200
BLOCK = 3.0
BREAK = math.log(10.0)
BUFFER = 3  # months around a chronology switch that are ambiguous
OUT = harness.RESEARCH / "results" / "fx-peg-1.md"
BOE_REL = "insure-1709-1/boe/millennium.xlsx"
NB_REL = "data-wide-2/probe/nb-fx.xlsx"
IRR_REL = "fx-peg-1/irr"
M15 = "M15. Mthly $-£ 1791-2015"

PEG, FLOAT, UNKNOWN, AMBIG = "peg", "float", "unknown", "ambiguous"


def ym(year: int, month: int) -> int:
    return year * 12 + month - 1


def ym_str(m: int) -> str:
    return f"{m // 12:04d}-{m % 12 + 1:02d}"


def ym_parse(s: str) -> int:
    return ym(int(s[:4]), int(s[5:7]))


# --------------------------------------------------------------------------- loading


def label_month(x: object) -> int | None:
    """Month of a row label: an Excel serial (any value 1..1e5; Table A2 labels 1914-1927
    with serials below 10,000, which datawide2's parser also reads since #224), 'YYYY MM',
    'YYYYMmm' or an ISO date."""
    if isinstance(x, int | float) and 1 <= x < 1e5:
        d = dw.excel_serial(float(x))
        return ym(d.year, d.month)
    return dw._ym_label(x)


def table_columns(rows: Sequence[Sequence[object]], header: str) -> dict[str, dict[int, float]]:
    """{column name: {month: level}} from a Norges Bank table whose header row starts with
    `header` ('Year' for A1, 'Month' for A2); months after LAST_YM are not kept."""
    hi = next(i for i, r in enumerate(rows) if r and str(r[0]).strip() == header)
    names = [str(c).strip() if c is not None else "" for c in rows[hi]]
    out: dict[str, dict[int, float]] = {n: {} for n in names[1:] if n}
    for r in rows[hi + 1 :]:
        if not r:
            continue
        m = label_month(r[0])
        if m is None or m > LAST_YM:
            continue
        for j, n in enumerate(names[1:], start=1):
            v = dw._num(r[j]) if j < len(r) else None
            if n and v is not None and v > 0:
                out[n][m] = v
    return out


def boe_m15(path: Path) -> dict[int, float]:
    out: dict[int, float] = {}
    for r in i9.xlsx_sheet(path, M15):
        y, mo, v = r.get(0, ""), r.get(1, ""), r.get(2)
        if not (y.replace(".0", "").isdigit() and mo in i9.MONTHS) or v is None:
            continue
        m = ym(int(float(y)), i9.MONTHS.index(mo) + 1)
        if m <= LAST_YM and re.fullmatch(r"-?[0-9.]+(E-?[0-9]+)?", v) and float(v) > 0:
            out[m] = float(v)
    return out


def changes(levels: dict[int, float], lo: int = -(10**9), hi: int = 10**9) -> dict[int, float]:
    """Monthly log changes dated m (level m over level m-1, both present), lo <= m <= hi."""
    return {
        m: math.log(v / levels[m - 1])
        for m, v in levels.items()
        if lo <= m <= hi and m - 1 in levels and m <= LAST_YM
    }


@dataclass
class Market:
    """One market: log changes on a month grid (NaN = no change, i.e. a run break)."""

    name: str
    foreign: str  # currency held
    home: str  # quoting currency
    start: int  # month of x[0]
    x: np.ndarray  # log change dated start + i
    timing: list[str]  # 'end', 'avg' or 'unstated' per month
    breaks: int = 0  # changes dropped by the |change| > ln 10 rule

    @property
    def months(self) -> np.ndarray:
        return self.start + np.arange(len(self.x))


def make_market(
    name: str, foreign: str, home: str, pieces: Sequence[tuple[dict[int, float], str]]
) -> Market:
    """Join change pieces (disjoint months) into one grid; drop |change| > ln 10."""
    ch: dict[int, tuple[float, str]] = {}
    for d, t in pieces:
        for m, v in d.items():
            if m in ch:
                raise ValueError(f"{name}: two pieces give month {ym_str(m)}")
            ch[m] = (v, t)
    lo, hi = min(ch), max(ch)
    x = np.full(hi - lo + 1, np.nan)
    tim = ["" for _ in range(hi - lo + 1)]
    nb = 0
    for m, (v, t) in ch.items():
        tim[m - lo] = t
        if abs(v) > BREAK:
            nb += 1
            continue
        x[m - lo] = v
    return Market(name, foreign, home, lo, x, tim, nb)


# Norges Bank currencies: (market currency, A1 column or None, A2 column)
A2_ONLY = ["USD", "SEK", "DKK", "CHF", "ITL", "ESP", "FIM", "CAD", "ISK", "PTE", "ATS"]


def build_markets(
    boe: dict[int, float], a1: dict[str, dict[int, float]], a2: dict[str, dict[int, float]]
) -> list[Market]:
    hi1 = JOIN - 1

    def both(c1: str, c2: str) -> list[tuple[dict[int, float], str]]:
        return [(changes(a1[c1], hi=hi1), "end"), (changes(a2[c2], lo=JOIN), "avg")]

    mk = [make_market("GBP in USD", "GBP", "USD", [(changes(boe), "unstated")])]
    mk.append(make_market("GBP in NOK", "GBP", "NOK", both("LONDON", "GBP")))
    hamburg = [(changes(a1["HAMBURG"], hi=hi1), "end")]
    mk.append(make_market("Mark in NOK", "DEM", "NOK", hamburg + both("REICHMARKS", "DEM")))
    for cur, col in (("FRF", "PARIS"), ("NLG", "AMSTERDAM")):
        mk.append(make_market(f"{cur} in NOK", cur, "NOK", both(col, cur)))
    belga = [(changes(a2["BEF"], lo=JOIN), "avg")]
    mk.append(make_market("BEF in NOK", "BEF", "NOK", both("ANTWERP", "BEF_OLD") + belga))
    mk.append(make_market("NOK in DKK", "NOK", "DKK", [(changes(a1["SPECIEDALER"]), "end")]))
    for cur in A2_ONLY:
        mk.append(make_market(f"{cur} in NOK", cur, "NOK", [(changes(a2[cur]), "avg")]))
    return mk


@dataclass
class Data:
    markets: list[Market]
    irr_fine: dict[str, dict[int, int]]
    irr_anchor: dict[str, dict[int, str]]


def load(root: Path | None = None) -> Data:
    root = root or i9.cache_root()
    boe = boe_m15(root / BOE_REL)
    nb = root / NB_REL
    a1 = table_columns(dw.read_xlsx_rows(nb, "p1_c7_Table_A1"), "Year")
    a2 = table_columns(dw.read_xlsx_rows(nb, "p1_c7_Table_A2"), "Month")
    fine, anch = load_irr(root / IRR_REL)
    return Data(build_markets(boe, a1, a2), fine, anch)


# --------------------------------------------------------------------------- step 1: filter


def rolling_count_sum(x: np.ndarray, w: int, f: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """For each k: number of finite x in [k-w+1, k] and the sum of f over those."""
    ok = np.isfinite(x)
    c = np.concatenate([[0], np.cumsum(ok)])
    s = np.concatenate([[0.0], np.cumsum(np.where(ok, f, 0.0))])
    k = np.arange(len(x))
    lo = np.maximum(k - w + 1, 0)
    n = c[k + 1] - c[lo]
    n = np.where(k - w + 1 < 0, 0, n)
    return n, s[k + 1] - s[lo]


def classify(
    x: np.ndarray, window: int = WINDOW, band: float = BAND, share: float = SHARE
) -> np.ndarray:
    """State at the end of each month k from the `window` changes dated k-window+1..k only:
    'unknown' if any is missing, 'peg' if a share >= `share` has |change| < band, else 'float'
    (Reinhart and Rogoff 2004's de facto peg band test on a trailing window)."""
    small = (np.abs(np.nan_to_num(x, nan=np.inf)) < band).astype(float)
    n, s = rolling_count_sum(x, window, small)
    out = np.full(len(x), UNKNOWN, dtype=object)
    full = n == window
    out[full & (s >= share * window - 1e-9)] = PEG
    out[full & (s < share * window - 1e-9)] = FLOAT
    return out


def trailing_sd(x: np.ndarray, w: int = 12) -> np.ndarray:
    out = np.full(len(x), np.nan)
    for k in range(w - 1, len(x)):
        seg = x[k - w + 1 : k + 1]
        if np.isfinite(seg).all():
            out[k] = float(seg.std(ddof=1))
    return out


def signals(x: np.ndarray, lookback: int = LOOKBACK) -> tuple[np.ndarray, np.ndarray]:
    """`trend_where_long.signals` on one series of log changes, vectorised: valid[k] if the
    `lookback` changes dated k-lookback+1..k exist, on[k] if they sum to more than 0."""
    n, s = rolling_count_sum(x, lookback, np.nan_to_num(x))
    valid = n == lookback
    return valid, valid & (s > 0)


# --------------------------------------------------------------------------- chronology

# Per currency: (first month, state). States: 'gold', 'silver', 'float', 'peg:XXX' (pegged to
# currency XXX), 'trans' (transition), 'control' (exchange control), 'war' (war, occupation).
# Approximate month dates from standard secondary sources (card); a state runs to the next.
# Description only: never an input of the filter, the books or the verdict.
CHRONOLOGY: dict[str, list[tuple[str, str]]] = {
    # Officer (1996); Bank Restriction 1797-1821; 1916-19 'pegged' at 4.765; EEA float 1931-39
    "GBP": [("1791-01", "gold"), ("1797-03", "float"), ("1821-05", "gold"), ("1914-08", "float"),
            ("1916-01", "peg:USD"), ("1919-04", "float"), ("1925-05", "gold"), ("1931-10", "float"),
            ("1939-09", "peg:USD")],
    # Friedman and Schwartz (1963); de facto silver to 1834, greenbacks 1862-1878, embargo 1917-19
    "USD": [("1791-01", "silver"), ("1834-08", "gold"), ("1862-01", "float"), ("1879-01", "gold"),
            ("1917-09", "control"), ("1919-07", "gold"), ("1933-04", "float"), ("1934-02", "gold")],
    # Klovland (2004): inconvertible speciedaler notes to 1842, silver, gold from 1874 (SMU 1875)
    "NOK": [("1816-01", "float"), ("1842-01", "silver"), ("1874-01", "gold"), ("1914-08", "float"),
            ("1928-05", "gold"), ("1931-10", "float"), ("1933-05", "peg:GBP"), ("1939-09", "war")],
    # Hamburg mark banco (silver bank money) to the Reichsmark; gold from 1876
    "DEM": [("1816-01", "silver"), ("1872-01", "trans"), ("1876-01", "gold"), ("1914-08", "float"),
            ("1923-11", "trans"), ("1924-10", "gold"), ("1931-07", "control")],
    # bimetallic to the limping gold standard (1876); de facto stabilisation 1926-12
    "FRF": [("1816-01", "trans"), ("1876-01", "gold"), ("1914-08", "float"), ("1926-12", "gold"),
            ("1936-10", "float"), ("1939-09", "war")],
    "NLG": [("1875-06", "gold"), ("1914-08", "float"), ("1925-05", "gold"), ("1936-10", "float"),
            ("1939-09", "war")],
    "BEF": [("1878-01", "gold"), ("1914-08", "float"), ("1926-10", "gold"), ("1935-04", "gold"),
            ("1939-09", "war")],
    "DKK": [("1816-01", "float"), ("1845-01", "silver"), ("1873-01", "trans"), ("1875-01", "gold"),
            ("1914-08", "float"), ("1927-01", "gold"), ("1931-10", "float"), ("1933-02", "peg:GBP"),
            ("1939-09", "war")],
    "SEK": [("1873-01", "gold"), ("1914-08", "float"), ("1924-04", "gold"), ("1931-10", "float"),
            ("1933-07", "peg:GBP"), ("1939-09", "war")],
    "CHF": [("1878-01", "gold"), ("1914-08", "float"), ("1925-01", "gold"), ("1936-10", "float"),
            ("1939-09", "war")],
    "ITL": [("1914-08", "float"), ("1927-12", "gold"), ("1934-05", "control")],
    "ESP": [("1883-01", "float"), ("1936-07", "war")],
    "FIM": [("1878-01", "gold"), ("1914-08", "float"), ("1926-01", "gold"), ("1931-10", "float"),
            ("1933-01", "peg:GBP"), ("1939-09", "war")],
}  # fmt: skip
IRR_FROM = ym(1946, 1)


def chrono_state(cur: str, m: int) -> tuple[str | None, bool]:
    """(state of `cur` at month m or None, whether m is within BUFFER months of a switch)."""
    lst = CHRONOLOGY.get(cur)
    if not lst:
        return None, False
    starts = [ym_parse(s) for s, _ in lst]
    if m < starts[0]:
        return None, False
    i = max(j for j, s in enumerate(starts) if s <= m)
    near = any(abs(m - s) <= BUFFER for s in starts[1:])
    return lst[i][1], near


def resolve(cur: str, state_of: dict[str, str | None], depth: int = 0) -> str | None:
    """Final anchor: 'gold'/'silver', 'float:XXX' for a floating currency, None if ambiguous."""
    st = state_of.get(cur)
    if st is None or depth > 5:
        return None
    if st in ("gold", "silver"):
        return st
    if st == "float":
        return f"float:{cur}"
    if st.startswith("peg:"):
        return resolve(st[4:], state_of, depth + 1)
    return None  # trans, control, war


def pair_label(foreign: str, home: str, state_of: dict[str, str | None]) -> str:
    a, b = resolve(foreign, state_of), resolve(home, state_of)
    if a is None or b is None:
        return AMBIG
    if a == b:
        return PEG
    if {a, b} == {"gold", "silver"}:
        return AMBIG
    return FLOAT


def chrono_pair(foreign: str, home: str, m: int) -> str:
    """Bilateral label before 1946 from CHRONOLOGY (both currencies and their anchors)."""
    curs = {foreign, home}
    for c in list(curs):
        st, _ = chrono_state(c, m)
        if st and st.startswith("peg:"):
            curs.add(st[4:])
    state_of: dict[str, str | None] = {}
    for c in curs:
        st, near = chrono_state(c, m)
        if near:
            return AMBIG
        state_of[c] = st
    return pair_label(foreign, home, state_of)


IRR_NAMES = {
    "GBP": "United Kingdom", "USD": "United States", "NOK": "Norway", "SEK": "Sweden",
    "DKK": "Denmark", "DEM": "Germany", "FRF": "France", "NLG": "Netherlands",
    "CHF": "Switzerland", "BEF": "Belgium", "ITL": "Italy", "ESP": "Spain", "FIM": "Finland",
    "CAD": "Canada", "ISK": "Iceland", "PTE": "Portugal", "ATS": "Austria",
}  # fmt: skip
IRR_ISO = {
    "GBP": "GBR", "USD": "USA", "NOK": "NOR", "SEK": "SWE", "DKK": "DNK", "DEM": "DEU",
    "FRF": "FRA", "NLG": "NLD", "CHF": "CHE", "BEF": "BEL", "ITL": "ITA", "ESP": "ESP",
    "FIM": "FIN", "CAD": "CAN", "ISK": "ISL", "PTE": "PRT", "ATS": "AUT",
}  # fmt: skip


def _irr_month(s: str) -> int | None:
    mt = re.fullmatch(r"\s*(\d{4})M(\d{1,2})\s*", s or "")
    return ym(int(mt.group(1)), int(mt.group(2))) if mt else None


def parse_irr_fine(rows: Sequence[dict[int, str]]) -> dict[str, dict[int, int]]:
    """{currency: {month: fine code}} from the 'Fine' sheet (country name split over the two
    rows above the data; month label 'YYYYMm' in column 1)."""
    name_rows = [i for i, r in enumerate(rows[:12]) if r.get(1, "").strip() == "Country"]
    hi = name_rows[0]
    names = {
        k: re.sub(r"\s+", " ", (rows[hi].get(k, "") + " " + rows[hi + 1].get(k, "")).strip())
        for k in set(rows[hi]) | set(rows[hi + 1])
        if k >= 2
    }
    col = {c: next((k for k, v in names.items() if v == n), None) for c, n in IRR_NAMES.items()}
    out: dict[str, dict[int, int]] = {c: {} for c in IRR_NAMES}
    for r in rows:
        m = _irr_month(r.get(1, ""))
        if m is None or m > LAST_YM:
            continue
        for c, k in col.items():
            v = r.get(k) if k is not None else None
            if v is not None and re.fullmatch(r"\d+(\.0)?", v.strip()):
                out[c][m] = int(float(v))
    return out


def parse_irr_anchor(rows: Sequence[dict[int, str]]) -> dict[str, dict[int, str]]:
    """{currency: {month: anchor code}} from the anchor file's 'Master' sheet."""
    hi = next(i for i, r in enumerate(rows[:20]) if r.get(0, "").strip() == "ISO3 Code")
    iso = {v.strip(): k for k, v in rows[hi].items() if k >= 1}
    out: dict[str, dict[int, str]] = {c: {} for c in IRR_ISO}
    for r in rows:
        m = _irr_month(r.get(0, ""))
        if m is None or m > LAST_YM:
            continue
        for c, code in IRR_ISO.items():
            k = iso.get(code)
            v = r.get(k, "").strip() if k is not None else ""
            if v and v != "n.a.":
                out[c][m] = v
    return out


def load_irr(d: Path) -> tuple[dict[str, dict[int, int]], dict[str, dict[int, str]]]:
    fine = parse_irr_fine(i9.xlsx_sheet(d / "ERA_Classification_Monthly_1940-2019.xlsx", "Fine"))
    anch = parse_irr_anchor(i9.xlsx_sheet(d / "Anchor_monthly_1946-2019.xlsx", "Master"))
    return fine, anch


def irr_state(cur: str, m: int, fine: dict[str, dict[int, int]],
              anch: dict[str, dict[int, str]]) -> str | None:  # fmt: skip
    """CHRONOLOGY-style state from IRR: USD is the system's final anchor ('gold' here, i.e.
    the common terminal); fine 1-4 -> 'peg:<anchor>'; 9-14 -> 'float'; else None."""
    if cur == "USD":
        return "gold"
    f = fine.get(cur, {}).get(m)
    if f is None:
        return None
    if 1 <= f <= 4:
        a = anch.get(cur, {}).get(m)
        if a is None or a == cur:
            return None
        return f"peg:{a}"
    if 9 <= f <= 14:
        return "float"
    return None


def irr_pair(foreign: str, home: str, m: int, fine: dict[str, dict[int, int]],
             anch: dict[str, dict[int, str]]) -> str:  # fmt: skip
    state_of: dict[str, str | None] = {}
    todo = [foreign, home]
    while todo:
        c = todo.pop()
        if c in state_of:
            continue
        st = irr_state(c, m, fine, anch)
        state_of[c] = st
        if st and st.startswith("peg:"):
            todo.append(st[4:])
    return pair_label(foreign, home, state_of)


def reference(mk: Market, m: int, d: Data) -> str:
    if m >= IRR_FROM:
        return irr_pair(mk.foreign, mk.home, m, d.irr_fine, d.irr_anchor)
    return chrono_pair(mk.foreign, mk.home, m)


@dataclass
class Agreement:
    n: int
    agree: float
    kappa: float
    ff_cp: int  # filter float, chronology peg
    fp_cf: int  # filter peg, chronology float
    fp_cp: int
    ff_cf: int


def agreement(pairs: Sequence[tuple[str, str]]) -> Agreement:
    """(filter state, reference label) pairs; only peg/float on both sides count."""
    pp = [(a, b) for a, b in pairs if a in (PEG, FLOAT) and b in (PEG, FLOAT)]
    n = len(pp)
    if n == 0:
        return Agreement(0, math.nan, math.nan, 0, 0, 0, 0)
    c = {(a, b): sum(1 for x in pp if x == (a, b)) for a in (PEG, FLOAT) for b in (PEG, FLOAT)}
    po = (c[(PEG, PEG)] + c[(FLOAT, FLOAT)]) / n
    pa = (c[(PEG, PEG)] + c[(PEG, FLOAT)]) / n
    pb = (c[(PEG, PEG)] + c[(FLOAT, PEG)]) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = (po - pe) / (1 - pe) if pe < 1 else math.nan
    return Agreement(n, po, kappa, c[(FLOAT, PEG)], c[(PEG, FLOAT)], c[(PEG, PEG)],
                     c[(FLOAT, FLOAT)])  # fmt: skip


# --------------------------------------------------------------------------- step 2: books


@dataclass
class Spec:
    """One book configuration (card: primary = filtered, 24/1%/0.80, 15%/15%, 2 bps, lag 0)."""

    book: str = "filtered"  # filtered, unfiltered, pegonly
    window: int = WINDOW
    band: float = BAND
    down: float = FALL[0]
    up: float = FALL[1]
    cost: float = i9.COST
    lag: int = 0
    markets: str = "all"  # all, end (BoE + A1 months), nok (no BoE), boe


def scored_mask(mk: Market, sp: Spec, x: np.ndarray | None = None) -> np.ndarray:
    """Months k scored by the book: signal valid at k-1-lag, change at k, and the filter
    state at k-1 (filtered: float; pegonly: not float)."""
    x = mk.x if x is None else x
    valid, _ = signals(x)
    st = classify(x, sp.window, sp.band)
    n = len(x)
    ok = np.zeros(n, dtype=bool)
    d = 1 + sp.lag
    ok[d:] = valid[: n - d] & np.isfinite(x[d:])
    fl = np.zeros(n, dtype=bool)
    fl[1:] = st[:-1] == FLOAT
    if sp.book == "filtered":
        ok &= fl
    elif sp.book == "pegonly":
        ok &= ~fl
    if sp.markets == "end":
        ok &= np.array([t in ("end", "unstated") for t in mk.timing])
    return ok


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    """[a, b) index runs where mask is True."""
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


@dataclass
class SegRef:
    market: int
    a: int  # first scored index in the market grid
    b: int  # one past the last


def seg_refs(markets: Sequence[Market], sp: Spec) -> tuple[list[SegRef], int]:
    refs, dropped = [], 0
    for j, mk in enumerate(markets):
        for a, b in runs(scored_mask(mk, sp)):
            if b - a >= MIN_SEG:
                refs.append(SegRef(j, a, b))
            else:
                dropped += 1
    return refs, dropped


def make_seg(mk: Market, ref: SegRef, x: np.ndarray, lag: int) -> i9.Seg:
    _, on = signals(x)
    idx = np.arange(ref.a, ref.b)
    pos = np.empty(len(idx) + 1)
    pos[1:] = on[idx - 1 - lag].astype(float)
    pos[0] = pos[1]
    r = np.concatenate([[0.0], np.expm1(x[idx])])
    months = [int(mk.start + ref.a - 1)] + [int(mk.start + i) for i in idx]
    return i9.Seg(mk.name, months, r, pos, np.zeros(len(idx) + 1))


@contextmanager
def cost_of(c: float) -> Iterator[None]:
    old = i9.COST
    i9.COST = c
    try:
        yield
    finally:
        i9.COST = old


def ls_mean(segs: Sequence[i9.Seg]) -> tuple[float, int, float]:
    """Equal-weight monthly long/short book: mean log return a month, months, t-stat."""
    by: dict[int, list[float]] = {}
    for s in segs:
        lr = np.log1p(s.r[1:])
        ls = (2 * s.pos[1:] - 1) * lr
        for m, v in zip(s.months[1:], ls, strict=True):
            by.setdefault(m, []).append(float(v))
    if not by:
        return math.nan, 0, math.nan
    b = np.array([np.mean(v) for _, v in sorted(by.items())])
    t = float(b.mean() / b.std(ddof=1) * math.sqrt(len(b))) if len(b) > 1 and b.std() > 0 else 0.0
    return float(b.mean()), len(b), t


@dataclass
class Eval:
    spec: Spec
    names: list[str]
    refs: list[SegRef]
    segs: list[i9.Seg]
    dropped: int
    eps: list[i1.Episode] = field(default_factory=list)
    clusters: list[list[i1.Episode]] = field(default_factory=list)
    calm: float = 0.0
    total: float = 0.0
    tim: i9.Timing | None = None
    ls: tuple[float, int, float] = (math.nan, 0, math.nan)
    open_falls: int = 0

    @property
    def c_ins(self) -> list[float]:
        return [i1.cmean(g, lambda e: e.ins) for g in self.clusters]

    @property
    def c_net(self) -> list[float]:
        return [i1.cmean(g, lambda e: e.net) for g in self.clusters]


def select(markets: Sequence[Market], sp: Spec) -> list[Market]:
    if sp.markets == "nok":
        return [m for m in markets if m.name != "GBP in USD"]
    if sp.markets == "boe":
        return [m for m in markets if m.name == "GBP in USD"]
    return list(markets)


def evaluate(markets: Sequence[Market], sp: Spec, rotations: int = ROTATIONS) -> Eval:
    mks = select(markets, sp)
    refs, dropped = seg_refs(mks, sp)
    segs = [make_seg(mks[r.market], r, mks[r.market].x, sp.lag) for r in refs]
    ev = Eval(sp, [m.name for m in mks], refs, segs, dropped)
    with cost_of(sp.cost):
        prs = []
        for j, s in enumerate(segs):
            sc = i1.score(i9.to_series(s, j), sp.down, sp.up)
            ev.eps += sc.eps
            ev.calm += sc.calm
            ev.total += sc.total
            ev.open_falls += sc.open_peak is not None
            prs.append(i9.pairs_of(s.r, sp.down, sp.up))
        ev.clusters = i1.link(ev.eps)
        if segs and any(prs):
            rng = np.random.default_rng(0)
            ev.tim = i9.timing(segs, prs, i9.offsets(segs, rotations, rng))
    ev.ls = ls_mean(segs)
    return ev


# --------------------------------------------------------------------------- joint worlds


@dataclass
class JointWorlds:
    """Synthetic worlds that replace the scored months' changes of every segment, drawn jointly
    across segments by calendar month inside each epoch (card)."""

    markets: list[Market]
    refs: list[SegRef]
    lag: int = 0
    seg_x: list[np.ndarray] = field(default_factory=list)
    seg_m: list[np.ndarray] = field(default_factory=list)
    epochs: list[tuple[int, int, list[int]]] = field(default_factory=list)

    def __post_init__(self) -> None:
        for r in self.refs:
            mk = self.markets[r.market]
            self.seg_x.append(mk.x[r.a : r.b].copy())
            self.seg_m.append(mk.start + np.arange(r.a, r.b))
        spans = sorted((int(m[0]), int(m[-1]), j) for j, m in enumerate(self.seg_m))
        for a, b, j in spans:
            if self.epochs and a <= self.epochs[-1][1] + 1:
                lo, hi, js = self.epochs[-1]
                self.epochs[-1] = (lo, max(hi, b), js + [j])
            else:
                self.epochs.append((a, b, [j]))

    def draw(self, rng: np.random.Generator, kind: str, demean: bool) -> list[np.ndarray]:
        """New changes per segment. kind: 'bb' (stationary blocks, mean BLOCK), 'ar1' (AR(1)
        sieve with jointly drawn residuals) or 'iid' (joint single months)."""
        out: list[np.ndarray] = [np.empty(0)] * len(self.refs)
        for lo, hi, js in self.epochs:
            n = hi - lo + 1
            tau = np.empty(n, dtype=int)
            if kind == "bb":
                cur = int(rng.integers(n))
                for t in range(n):
                    cur = (
                        int(rng.integers(n))
                        if (t == 0 or rng.random() < 1 / BLOCK)
                        else (cur + 1) % n
                    )
                    tau[t] = cur
            else:
                tau = rng.integers(n, size=n)
            for j in js:
                v = self.seg_x[j]
                mu = float(v.mean())
                dev = v - mu
                m0 = int(self.seg_m[j][0]) - lo
                L = len(v)
                own = tau[m0 : m0 + L] - m0  # drawn calendar month as an index into the segment
                miss = (own < 0) | (own >= L)
                if kind == "ar1":
                    phi = (
                        float(np.clip(np.corrcoef(dev[:-1], dev[1:])[0, 1], -0.9, 0.9))
                        if L > 2
                        else 0.0
                    )
                    e = np.empty(L)
                    e[1:] = dev[1:] - phi * dev[:-1]
                    e[0] = math.nan
                    pick = np.where(miss | (own == 0), rng.integers(1, L, size=L), own)
                    z = np.empty(L)
                    z[0] = dev[int(rng.integers(L))]
                    ee = e[pick]
                    for t in range(1, L):
                        z[t] = phi * z[t - 1] + ee[t]
                    out[j] = z + (0.0 if demean else mu)
                else:
                    pick = np.where(miss, rng.integers(L, size=L), own)
                    out[j] = dev[pick] + (0.0 if demean else mu)
        return out

    def world(self, xs: Sequence[np.ndarray]) -> list[i9.Seg]:
        full = {i: mk.x.copy() for i, mk in enumerate(self.markets)}
        for r, v in zip(self.refs, xs, strict=True):
            full[r.market][r.a : r.b] = v
        return [make_seg(self.markets[r.market], r, full[r.market], self.lag) for r in self.refs]


def world_stats(segs: Sequence[i9.Seg], sp: Spec, rng: np.random.Generator,
                timing_too: bool) -> tuple[float, float]:  # fmt: skip
    """(gap G or NaN, LS mean) on one world."""
    ls = ls_mean(segs)[0]
    if not timing_too:
        return math.nan, ls
    prs = [i9.pairs_of(s.r, sp.down, sp.up) for s in segs]
    if not any(prs):
        return math.nan, ls
    with cost_of(sp.cost):
        t = i9.timing(segs, prs, i9.offsets(segs, WORLD_ROT, rng))
    return t.gap, ls


def null_run(jw: JointWorlds, sp: Spec, kind: str, demean: bool, worlds: int, seed: int,
             timing_too: bool) -> tuple[np.ndarray, np.ndarray]:  # fmt: skip
    rng = np.random.default_rng(seed)
    g, ls = np.full(worlds, np.nan), np.full(worlds, np.nan)
    for w in range(worlds):
        segs = jw.world(jw.draw(rng, kind, demean))
        g[w], ls[w] = world_stats(segs, sp, rng, timing_too)
    return g, ls


def p_ge(null: np.ndarray, obs: float) -> tuple[float, int]:
    v = null[np.isfinite(null)]
    return (float((v >= obs - 1e-12).mean()) if len(v) else math.nan), int(len(v))


# --------------------------------------------------------------------------- verdicts


def verdict(ev: Eval, p_ar: float) -> str:
    vals = [v for v in ev.c_ins if v != 0]
    if len(vals) < 5 or ev.tim is None:
        return "Too few falls"
    _, _, p_sign = i1.sign_test(ev.c_ins)
    _, p_boot, _, _ = i1.boot(ev.c_ins)
    if not (p_sign < 0.05 and p_boot < 0.05):
        return "Does not hold"
    pr = ev.tim.p_rot
    if pr >= 0.10:
        return "Holds only as lower exposure"
    if pr >= 0.05:
        return "In between"
    return ("Holds, timing beyond autocorrelation" if p_ar < 0.05
            else "Holds, timing not separable from autocorrelation")  # fmt: skip


def qualifiers(ev: Eval) -> str:
    if not ev.clusters or ev.tim is None:
        return "-"
    k = sum(1 for v in ev.c_ins if v > 0)
    q = ["at the claimed strength" if k / len(ev.clusters) >= 0.80 else "weaker than claimed"]
    _, _, ps = i1.sign_test(ev.c_net)
    _, pb, _, _ = i1.boot(ev.c_net)
    q.append("kept" if ps < 0.05 and pb < 0.05 else "handed back in the rebound")
    if ev.tim.rule.prem[0] < ev.tim.fixed.prem[0]:
        q.append("cheaper than holding less")
    return "; ".join(q)


def premium_verdict(mean: float, p_iid: float, p_ar: float) -> str:
    if mean > 0 and p_ar < 0.05:
        return "Trend premium beyond autocorrelation"
    if mean > 0 and p_iid < 0.05:
        return "Premium not separable from autocorrelation"
    return "No trend premium shown"


# --------------------------------------------------------------------------- report


def acf1(x: np.ndarray) -> tuple[float, int]:
    ok = np.isfinite(x[1:]) & np.isfinite(x[:-1])
    a, b = x[:-1][ok], x[1:][ok]
    if len(a) < 3:
        return math.nan, int(len(a))
    a, b = a - a.mean(), b - b.mean()
    return float((a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum())), int(len(a))


def before_rows(d: Data) -> list[str]:
    out = [
        "| Market | Source | Changes | Lag-1 acf (pairs) | noise line | share abs change < 1% "
        "| Filter float / peg / unknown | Chronology agreement (n, kappa) |",
        "|---|---|---:|---|---:|---:|---|---|",
    ]
    allp: list[tuple[str, str]] = []
    for mk in d.markets:
        st = classify(mk.x)
        refs = [reference(mk, int(m), d) for m in mk.months]
        prs = list(zip(st, refs, strict=True))
        allp += prs
        ag = agreement(prs)
        for t in ("end", "avg", "unstated"):
            sel = np.array([u == t for u in mk.timing])
            if not sel.any():
                continue
            xx = np.where(sel, mk.x, np.nan)
            a, n = acf1(xx)
            fin = np.isfinite(xx)
            sh = float((np.abs(xx[fin]) < BAND).mean()) if fin.any() else math.nan
            ss = st[sel]
            first, last = int(mk.months[sel][0]), int(mk.months[sel][-1])
            out.append(
                f"| {mk.name} | {t} {ym_str(first)}..{ym_str(last)} | {int(fin.sum())} | "
                f"{a:+.3f} ({n}) | {1.645 / math.sqrt(max(n, 1)):.3f} | {sh:.2f} | "
                f"{(ss == FLOAT).mean():.2f} / {(ss == PEG).mean():.2f} / "
                f"{(ss == UNKNOWN).mean():.2f} | "
                f"{ag.agree:.2f} ({ag.n}, {ag.kappa:+.2f}) |"
            )
    ag = agreement(allp)
    out += [
        "",
        f"All markets: agreement {ag.agree:.3f} on {ag.n} market-months, kappa {ag.kappa:+.3f}; "
        f"filter float / chronology peg {ag.ff_cp}, filter peg / chronology float {ag.fp_cf}, "
        f"both peg {ag.fp_cp}, both float {ag.ff_cf}. Card reading: "
        + (
            "the filter matches the chronology."
            if ag.agree >= 0.85
            else "filter disagrees with the chronology (caveat on the verdict)."
        ),  # fmt: skip
        "Breaks dropped by the ln 10 rule: "
        + (", ".join(f"{m.name} {m.breaks}" for m in d.markets if m.breaks) or "none")
        + ".",
    ]
    return out


def sharpe_row(ev: Eval) -> tuple[str, str, float, float, float, float]:
    with cost_of(ev.spec.cost):
        rule = np.concatenate([i9.rule_returns(s.pos, s.r)[1:] for s in ev.segs])
    sh = float(rule.mean() / rule.std() * math.sqrt(12)) if rule.std() > 0 else 0.0
    eq = np.cumprod(1 + rule)
    mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
    flips = float(sum(np.abs(np.diff(s.pos)).sum() for s in ev.segs)) / (len(rule) / 12)
    first = min(s.months[1] for s in ev.segs)
    last = max(s.months[-1] for s in ev.segs)
    return (i9.month_end(first).isoformat(), i9.month_end(last).isoformat(), sh,
            float(eq[-1] - 1), mdd, flips)  # fmt: skip


def log_rows(evs: Sequence[tuple[str, Eval]]) -> int:
    text = harness.TRIES.read_text()
    rows = []
    for v, ev in evs:
        if f"| {IDEA} | {v} |" in text or not ev.segs:
            continue
        a, b, sh, tot, mdd, fl = sharpe_row(ev)
        rows.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | insure-check | "
            f"train | {a} | {b} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(rows)
    return len(rows)


def summary_line(label: str, ev: Eval) -> str:
    if ev.tim is None:
        ls = f"{ev.ls[0] * 1200:+.2f} ({ev.ls[2]:+.2f})"
        return f"| {label} | {len(ev.segs)} | 0 | - | - | - | - | - | {ls} |"
    k = sum(1 for v in ev.c_ins if v > 0)
    _, _, ps = i1.sign_test(ev.c_ins)
    _, pb, _, _ = i1.boot(ev.c_ins)
    t = ev.tim
    months = sum(len(s.r) - 1 for s in ev.segs)
    return (
        f"| {label} | {len(ev.segs)} ({months} mo) | {len(ev.eps)} / {len(ev.clusters)} | "
        f"{k} of {len(ev.clusters)} (sign {ps:.3f}, boot {pb:.3f}) | "
        f"{t.rule.s_mean[0]:.2f} / {t.fixed.s_mean[0]:.2f} / {t.rot.s_mean.mean():.2f} | "
        f"{t.gap:+.2f} (p_rot {t.p_rot:.3f}) | {t.rule.prem[0]:.2f} / {t.fixed.prem[0]:.2f} | "
        f"{np.mean([e.ins for e in ev.eps]):+.1f} | {ev.ls[0] * 1200:+.2f} ({ev.ls[2]:+.2f}) |"
    )


HEAD = [
    "| Book | Segments | Falls / clusters | Clusters lost less (p) | S rule / fixed / random | "
    "Gap G | Premium P rule / fixed | mean I per fall (log pts) | LS % a year (t) |",
    "|---|---|---|---|---|---|---|---:|---|",
]


def episode_rows(ev: Eval) -> list[str]:
    out = [
        "| Cluster | Market | Peak | Trough | Depth | Hold (log pts) | I | B | N | S |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for ci, g in enumerate(ev.clusters, start=1):
        for e in g:
            out.append(
                f"| {ci} | {e.series.rsplit('-', 1)[0]} | {e.peak:%Y-%m} | {e.trough:%Y-%m} | "
                f"{e.depth:.0%} | {e.hold:+.1f} | {e.ins:+.1f} | {e.rebound:+.1f} | {e.net:+.1f} | "
                f"{e.share:+.2f} |"
            )
    return out


def open_falls(ev: Eval) -> list[tuple[str, int, int, int, float, float, float]]:
    """Falls still unfinished at a segment end (not counted by the card): market, peak month,
    the lowest month after it, segment end, depth, holding's log change and I to that low."""
    out = []
    with cost_of(ev.spec.cost):
        for s in ev.segs:
            px = np.cumprod(1 + s.r)
            _, pk = i1.zigzag(px, ev.spec.down, ev.spec.up)
            if pk is None:
                continue
            lo = pk + int(np.argmin(px[pk:]))
            rule = i9.rule_returns(s.pos, s.r)
            d = np.log1p(rule) - np.log1p(s.r)
            ins = 100 * float(d[pk + 1 : lo + 1].sum())
            hold = 100 * math.log(px[lo] / px[pk])
            out.append((s.series, s.months[pk], s.months[lo], s.months[-1],
                        float(1 - px[lo] / px[pk]), hold, ins))  # fmt: skip
    return out


def open_rows(ev: Eval) -> list[str]:
    out = [
        "| Market | Peak | Low | Segment end | Depth | Hold (log pts) | I | S |",
        "|---|---|---|---|---:|---:|---:|---:|",
    ]
    for name, a, lo, end, depth, hold, ins in open_falls(ev):
        out.append(
            f"| {name} | {ym_str(a)} | {ym_str(lo)} | {ym_str(end)} | {depth:.0%} | "
            f"{hold:+.1f} | {ins:+.1f} | {ins / abs(hold):+.2f} |"
        )
    return out


SPIKE = (ym(1857, 10), ym(1857, 11))  # BoE M15: 4.876, 8.924, 4.843 $/GBP in 1857-09..11


def all_pairs(d: Data, split: int | None = None) -> dict[str, list[tuple[str, str]]]:
    """(filter state, reference) pairs for every market-month; keys 'all', or 'before' and
    'after' the month `split`."""
    out: dict[str, list[tuple[str, str]]] = {}
    for mk in d.markets:
        st = classify(mk.x)
        for m, s in zip(mk.months, st, strict=True):
            k = "all" if split is None else ("before" if m < split else "after")
            out.setdefault(k, []).append((s, reference(mk, int(m), d)))
    return out


def caveat(d: Data) -> str:
    ag = agreement(all_pairs(d)["all"])
    if ag.agree >= 0.85:
        return ""
    return f"; caveat: filter disagrees with the chronology (agreement {ag.agree:.3f} < 0.85)"


def spike_rows(d: Data) -> list[str]:
    """Data note: the one-month spike in BoE M15 (1857-10) and what it does (description)."""
    mk = next(m for m in d.markets if m.name == "GBP in USD")
    i = [s - mk.start for s in SPIKE]
    x = mk.x.copy()
    a0, n0 = acf1(x)
    x[i] = np.nan
    a1, n1 = acf1(x)
    return [
        f"- BoE M15 ($/GBP) has a one-month spike: 4.876 (1857-09), 8.924 (1857-10), 4.843 "
        f"(1857-11), i.e. monthly log changes {mk.x[i[0]]:+.3f} and {mk.x[i[1]]:+.3f}. It "
        f"sets the GBP-in-USD lag-1 acf in the before-scoring table at {a0:+.3f} ({n0} pairs); "
        f"without those two changes it is {a1:+.3f} ({n1} pairs). It also makes the spurious "
        "48% fall 1857-10..1861-01 of the unfiltered and peg-only books (it starts at the "
        "spike). The filtered (primary) book never scores 1857, so no verdict changes. The "
        "card's data rules are unchanged (the spike is below the ln 10 break rule).",
    ]


def posthoc_rows(d: Data, prim: Eval) -> list[str]:
    sp = all_pairs(d, IRR_FROM)
    b, a = agreement(sp["before"]), agreement(sp["after"])
    s = [ins / abs(hold) for *_, hold, ins in open_falls(prim)]
    return [
        f"- Agreement split at 1946: hand-coded list before 1946 {b.agree:.3f} on {b.n} "
        f"market-months (kappa {b.kappa:+.2f}; filter float / list peg {b.ff_cp}, filter peg / "
        f"list float {b.fp_cf}); IRR 1946-1970 {a.agree:.3f} on {a.n} (kappa {a.kappa:+.2f}; "
        f"{a.ff_cp} / {a.fp_cf}).",
        f"- Falls unfinished at a segment end, primary book: {len(s)}; the rule's S to the low "
        f"median {float(np.median(s)):.2f}, range {min(s):.2f}..{max(s):.2f}.",
    ]


def spell_rows(ev: Eval) -> list[str]:
    by: dict[str, list[str]] = {}
    for s in ev.segs:
        by.setdefault(s.series, []).append(f"{ym_str(s.months[1])}..{ym_str(s.months[-1])}")
    return [f"- {k}: {', '.join(v)}" for k, v in by.items()]


CHECKS: list[tuple[str, Spec]] = [
    ("check-falls-10/10", Spec(down=0.10, up=0.10)),
    ("check-falls-25/25", Spec(down=0.25, up=0.25)),
    ("check-window-12", Spec(window=12)),
    ("check-window-60", Spec(window=60)),
    ("check-band-2%", Spec(band=0.02)),
    ("check-end-month-only", Spec(markets="end")),
    ("check-nok-only", Spec(markets="nok")),
    ("check-boe-only", Spec(markets="boe")),
    ("check-cost-25bps", Spec(cost=0.0025)),
    ("check-stale-lag1", Spec(lag=1)),
]


def run(d: Data, log: bool, worlds: int = WORLDS) -> None:
    prim = evaluate(d.markets, Spec())
    unf = evaluate(d.markets, Spec(book="unfiltered"))
    peg = evaluate(d.markets, Spec(book="pegonly"))
    jw = JointWorlds(select(d.markets, prim.spec), prim.refs)
    assert prim.tim is not None
    obs_g, obs_ls = prim.tim.gap, prim.ls[0]
    g_ar, ls_ar = null_run(jw, prim.spec, "ar1", False, worlds, 2, True)
    g_bb, ls_bb = null_run(jw, prim.spec, "bb", False, worlds, 3, True)
    _, d_ar = null_run(jw, prim.spec, "ar1", True, worlds, 4, False)
    _, d_bb = null_run(jw, prim.spec, "bb", True, worlds, 5, False)
    _, d_iid = null_run(jw, prim.spec, "iid", True, worlds, 6, False)
    p_g_ar, n_g_ar = p_ge(g_ar, obs_g)
    p_g_bb, n_g_bb = p_ge(g_bb, obs_g)
    p_ar = max(p_g_ar, p_g_bb)
    pp_ar, _ = p_ge(d_ar, obs_ls)
    pp_bb, _ = p_ge(d_bb, obs_ls)
    pp_iid, _ = p_ge(d_iid, obs_ls)
    pp_drift = max(p_ge(ls_ar, obs_ls)[0], p_ge(ls_bb, obs_ls)[0])
    v_ins = verdict(prim, p_ar)
    v_prem = premium_verdict(obs_ls, pp_iid, max(pp_ar, pp_bb))
    checks = [(n, evaluate(d.markets, sp)) for n, sp in CHECKS]
    cav = caveat(d)

    def q(a: np.ndarray) -> str:
        v = a[np.isfinite(a)]
        lo, hi = np.quantile(v, [0.05, 0.95])
        return f"median {np.median(v):+.4f}, 5-95% {lo:+.4f}..{hi:+.4f}"

    lines = [
        "# fx-peg-1 results",
        "",
        f"Generated {datetime.now(UTC):%Y-%m-%d %H:%M} UTC by `research/lib/fxpeg1.py run` "
        "(card `research/cards/fx-peg-1.md`). Months to 1970-12. Holding = the foreign "
        "currency as quoted, price only, cash at 0.",
        "",
        "## Before scoring: sources, autocorrelation, filter and chronology",
        "",
        *before_rows(d),
        "",
        "## Primary (filtered, 15%/15%) and the filter effect",
        "",
        *HEAD,
        summary_line("**Filtered (primary)**", prim),
        summary_line("Unfiltered", unf),
        summary_line("Peg-only", peg),
        "",
        f"Segments dropped (< {MIN_SEG} months): filtered {prim.dropped}, unfiltered "
        f"{unf.dropped}, peg-only {peg.dropped}. Unfinished falls at a segment end: "
        f"{prim.open_falls} / {unf.open_falls} / {peg.open_falls}.",
        "",
        "## Nulls (primary)",
        "",
        f"- Timing gap G observed {obs_g:+.4f}. AR1 sieve (joint residuals): p {p_g_ar:.3f} "
        f"({n_g_ar} worlds with a fall; {q(g_ar)}). Joint block bootstrap: p {p_g_bb:.3f} "
        f"({n_g_bb}; {q(g_bb)}). **p_AR = {p_ar:.3f}.**",
        f"- LS mean observed {obs_ls:+.5f} a month ({obs_ls * 1200:+.2f}% a year, t "
        f"{prim.ls[2]:+.2f}, {prim.ls[1]} months). Demeaned worlds: AR1 p {pp_ar:.3f} "
        f"({q(d_ar)}), BB p {pp_bb:.3f} ({q(d_bb)}), iid p {pp_iid:.3f} ({q(d_iid)}). "
        f"**p_AR_prem = {max(pp_ar, pp_bb):.3f}.** With own means kept (beyond drift, not "
        f"decisive): p {pp_drift:.3f}.",
        "",
        f"**Insurance verdict: {v_ins}** ({qualifiers(prim)}{cav}).",
        "",
        f"**Premium verdict: {v_prem}**{cav}.",
        "",
        f"Unfiltered book by the same rules (description): {verdict(unf, math.nan)} "
        f"({qualifiers(unf)}); peg-only: {verdict(peg, math.nan)}.",
        "",
        "## Data note",
        "",
        *spike_rows(d),
        "",
        "## Post hoc (not on the card; description)",
        "",
        *posthoc_rows(d, prim),
        "",
        "## Checks (description)",
        "",
        *HEAD,
        *[summary_line(n, ev) for n, ev in checks],
        "",
        "## Episodes, primary",
        "",
        *episode_rows(prim),
        "",
        "## Falls unfinished at a segment end, primary (not counted; description)",
        "",
        *open_rows(prim),
        "",
        "## Floating spells scored by the primary book",
        "",
        *spell_rows(prim),
        "",
        "## Episodes, unfiltered",
        "",
        *episode_rows(unf),
        "",
        "## Months scored per market",
        "",
        "| Market | Filtered | Unfiltered |",
        "|---|---:|---:|",
    ]
    for name in prim.names:
        f_ = sum(len(s.r) - 1 for s in prim.segs if s.series == name)
        u_ = sum(len(s.r) - 1 for s in unf.segs if s.series == name)
        lines.append(f"| {name} | {f_} | {u_} |")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))
    print(v_ins, "|", v_prem)
    if log:
        n = log_rows(
            [("tsmom12m@fx-peg-1-filtered", prim), ("tsmom12m@fx-peg-1-unfiltered", unf),
             ("tsmom12m@fx-peg-1-pegonly", peg)]
            + [(f"tsmom12m@fx-peg-1-{k}", ev) for k, ev in checks]
        )  # fmt: skip
        print(f"logged {n} rows")


def main(argv: Sequence[str]) -> None:
    d = load()
    if argv and argv[0] == "before":
        print("\n".join(before_rows(d)))
        return
    worlds = WORLDS
    if "--worlds" in argv:
        worlds = int(argv[argv.index("--worlds") + 1])
    run(d, "--log" in argv, worlds)


if __name__ == "__main__":
    main(sys.argv[1:])
