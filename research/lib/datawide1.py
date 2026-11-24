"""Loaders for the dose sources verified by research run data-wide-1 (research/data-wide-1.md).

Four sources whose series could be F1/F2 doses (wide-11 filters), each with an explicit
"available on" rule so a later card cannot read a value before it was public:

- USGS ComCat earthquakes (`parse_usgs_csv`, `load_quakes`, `daily_max_magnitude`).
- Caldara-Iacoviello daily geopolitical risk (`parse_gpr_rows`, `read_gpr_xls`,
  `gpr_available_on`).
- FDIC bank failures (`parse_fdic_failures`, `failure_available_on`).
- Japan MOF FX intervention (`parse_mof_csv`, `mof_quarter_totals`, `monthly_totals`,
  `mof_month_available_on`, `mof_daily_available_on`).

Raw files come from `scripts/fetch_datawide1.py` into the git-ignored cache
(`<cache_root>/data-wide-1/<source>/<YYYY-MM-DD>/`). They are untrusted downloads: parse them
as data only, from a process started with `python -I`. The parsers take text, bytes or rows,
so the tests run offline on small literal samples. No function here reads any price.
"""

from __future__ import annotations

import csv
import io
import json
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def cache_root() -> Path:
    cfg = ROOT / "research" / "macro.local.json"
    return Path(json.loads(cfg.read_text())["cache_root"]).expanduser()


def snapshot(source: str, root: Path | None = None) -> Path:
    """The latest dated snapshot folder of one source."""
    base = (root or cache_root()) / "data-wide-1" / source
    folders = sorted(p for p in base.iterdir() if p.is_dir())
    if not folders:
        raise FileNotFoundError(f"no snapshot of {source} under {base}")
    return folders[-1]


# ---------------------------------------------------------------- USGS earthquakes


@dataclass(frozen=True)
class Quake:
    id: str
    time: datetime  # UTC
    lat: float
    lon: float
    depth_km: float
    mag: float
    mag_type: str
    place: str
    updated: datetime  # UTC: last revision of the catalogue row


def _utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


def parse_usgs_csv(text: str) -> list[Quake]:
    """Rows of a ComCat CSV answer; only `type == earthquake` rows with a magnitude."""
    out = []
    for r in csv.DictReader(io.StringIO(text)):
        if r.get("type") != "earthquake" or not r.get("mag"):
            continue
        out.append(
            Quake(
                id=r["id"],
                time=_utc(r["time"]),
                lat=float(r["latitude"]),
                lon=float(r["longitude"]),
                depth_km=float(r["depth"]) if r["depth"] else float("nan"),
                mag=float(r["mag"]),
                mag_type=r["magType"],
                place=r["place"],
                updated=_utc(r["updated"]),
            )
        )
    return out


def merge_quakes(parts: Iterable[list[Quake]]) -> list[Quake]:
    """One row per event id (the most recently updated wins), in time order."""
    best: dict[str, Quake] = {}
    for part in parts:
        for q in part:
            if q.id not in best or q.updated > best[q.id].updated:
                best[q.id] = q
    return sorted(best.values(), key=lambda q: (q.time, q.id))


def load_quakes(folder: Path) -> list[Quake]:
    return merge_quakes(parse_usgs_csv(p.read_text()) for p in sorted(folder.glob("*.csv")))


def daily_max_magnitude(quakes: Iterable[Quake], min_mag: float) -> dict[date, float]:
    """Largest magnitude per UTC day among events >= min_mag. The magnitudes are the
    catalogue's reviewed ones: a real-time reader saw a first estimate (often 0.1-0.3 off), so
    a card should leave a margin around any threshold."""
    out: dict[date, float] = {}
    for q in quakes:
        if q.mag >= min_mag:
            d = q.time.date()
            out[d] = max(out.get(d, q.mag), q.mag)
    return out


# ---------------------------------------------------------------- geopolitical risk (daily)


@dataclass(frozen=True)
class GprDay:
    day: date
    gprd: float  # daily geopolitical risk index (1985-2019 mean = 100)
    act: float  # acts sub-index (war start, escalation, terror acts)
    threat: float  # threats sub-index
    articles: int  # N10D: articles searched that day (all topics)


def _cell_float(v: object) -> float:
    if v in ("", None):
        return float("nan")
    return float(str(v))


def _yyyymmdd(v: object) -> date:
    s = str(v).strip()
    if s.endswith(".0"):  # a numeric cell read as float
        s = s[:-2]
    return date(int(s[:4]), int(s[4:6]), int(s[6:8]))


def parse_gpr_rows(rows: Iterable[Sequence[object]]) -> list[GprDay]:
    """Rows of the daily file (`data_gpr_daily_recent.xls`), header first. Columns are found
    by name, so the extra columns (moving averages, events, labels) are ignored."""
    it = iter(rows)
    head = [str(h).strip() for h in next(it)]
    ix = {k: head.index(k) for k in ("DAY", "GPRD", "GPRD_ACT", "GPRD_THREAT", "N10D")}
    out = []
    for r in it:
        if not str(r[ix["DAY"]]).strip():
            continue
        n = _cell_float(r[ix["N10D"]])
        out.append(
            GprDay(
                day=_yyyymmdd(r[ix["DAY"]]),
                gprd=_cell_float(r[ix["GPRD"]]),
                act=_cell_float(r[ix["GPRD_ACT"]]),
                threat=_cell_float(r[ix["GPRD_THREAT"]]),
                articles=0 if n != n else int(n),
            )
        )
    return sorted(out, key=lambda g: g.day)


def read_gpr_xls(path: Path) -> list[GprDay]:  # pragma: no cover - needs xlrd and the file
    """Read with `uv run --with xlrd python -I ...` (xlrd is not a project dependency)."""
    import xlrd  # type: ignore[import-not-found]

    sh = xlrd.open_workbook(str(path)).sheet_by_index(0)
    return parse_gpr_rows(sh.row_values(i) for i in range(sh.nrows))


GPR_LAG_DAYS = 9


def gpr_available_on(day: date) -> date:
    """First date a decision may use the value for `day` when no vintage is at hand. The file
    is refreshed weekly on Mondays (the next business day after a federal holiday). Archived
    vintages (research/results/data-wide-1.md) show a Monday file carrying values through that
    Monday, the live file posted a day late (2026-11-16's on 2026-11-17, 18:00 UTC), and one
    Monday vintage still ending a week earlier (2026-11-09 ends 2026-11-02): a weekly update
    can slip. Rule: the first Wednesday at least GPR_LAG_DAYS days after `day` (9-15 days),
    which covers one slipped week for a Monday value. From 2022-02-24 on, a card should read
    the archived vintages instead (exact as-of, and values are revised between vintages)."""
    d = day + timedelta(days=GPR_LAG_DAYS)
    return d + timedelta(days=(2 - d.weekday()) % 7)


# ---------------------------------------------------------------- FDIC bank failures


@dataclass(frozen=True)
class Failure:
    day: date
    name: str
    cert: int | None
    assets_k: float  # total assets at failure, thousands of USD
    deposits_k: float
    cost_k: float  # estimated loss to the insurance fund, thousands of USD (nan if unknown)
    kind: str  # RESTYPE: FAILURE or ASSISTANCE
    resolution: str  # RESTYPE1: PA purchase and assumption, PO payout, ...
    fund: str  # SAVR: insurance fund (FDIC, BIF, SAIF, DIF, RTC, FSLIC)
    state: str


def _num(v: object) -> float:
    return float("nan") if v in (None, "") else float(str(v))


def parse_fdic_failures(text: str) -> list[Failure]:
    """The JSON answer of `banks.data.fdic.gov/api/failures` (fields as fetched)."""
    out = []
    for item in json.loads(text)["data"]:
        r = item["data"]
        m, d, y = (int(x) for x in str(r["FAILDATE"]).split("/"))
        cert = r.get("CERT")
        out.append(
            Failure(
                day=date(y, m, d),
                name=str(r.get("NAME", "")),
                cert=None if cert in (None, "") else int(cert),
                assets_k=_num(r.get("QBFASSET")),
                deposits_k=_num(r.get("QBFDEP")),
                cost_k=_num(r.get("COST")),
                kind=str(r.get("RESTYPE", "")),
                resolution=str(r.get("RESTYPE1", "")),
                fund=str(r.get("SAVR", "")),
                state=str(r.get("PSTALP", "")),
            )
        )
    return sorted(out, key=lambda f: (f.day, f.name))


def failure_available_on(day: date) -> date:
    """Closures are announced the evening of the closing day, after the US close (mostly on
    Fridays), so the first decision that may use one is the next calendar day."""
    return day + timedelta(days=1)


# ---------------------------------------------------------------- Japan MOF FX intervention

_MONTHS = {
    m: i + 1
    for i, m in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
}


@dataclass(frozen=True)
class Intervention:
    day: date  # Tokyo date of the operation
    amount: int  # 100 million yen, as published (always positive)
    pair: str  # English description, e.g. "the US dollar (sold) the Japanese yen (bought)"
    yen_sign: int  # +1 yen bought (support), -1 yen sold, 0 yen not involved


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).strip()


def _yen_sign(pair: str) -> int:
    if "Japanese yen (bought)" in pair:
        return 1
    if "Japanese yen (sold)" in pair:
        return -1
    return 0


def _mof_rows(raw: bytes) -> list[list[str]]:
    text = raw.decode("shift_jis", errors="replace")
    return [[_norm(c) for c in r] for r in csv.reader(io.StringIO(text))]


def parse_mof_csv(raw: bytes) -> list[Intervention]:
    """Daily operations from the MOF CSV (Shift-JIS). A daily row has the day in column 5 and
    the amount in column 6; year (column 3) and month (column 4) are blank when they repeat
    the row above. Quarter-total and note rows are skipped."""
    out = []
    year = month = None
    for r in _mof_rows(raw):
        if len(r) < 9:
            continue
        if r[3].isdigit() and len(r[3]) == 4:
            year = int(r[3])
        if r[4] in _MONTHS:
            month = _MONTHS[r[4]]
        if not r[5].isdigit() or not r[6]:
            continue
        if year is None or month is None:
            raise ValueError(f"daily row before any year or month: {r}")
        out.append(
            Intervention(
                day=date(year, month, int(r[5])),
                amount=int(r[6].replace(",", "")),
                pair=r[8],
                yen_sign=_yen_sign(r[8]),
            )
        )
    return out


def mof_quarter_totals(raw: bytes) -> dict[tuple[int, int], int]:
    """Published quarter totals, {(year, quarter): 100 million yen}, to check the daily rows
    against (they may differ by rounding)."""
    out = {}
    starts = {"January": 1, "April": 2, "July": 3, "October": 4}
    for r in _mof_rows(raw):
        if len(r) < 7 or r[5] or not r[6]:
            continue
        words = r[3].replace("-", " ").split()
        if len(words) >= 3 and words[0] in starts and words[-1].isdigit():
            out[(int(words[-1]), starts[words[0]])] = int(r[6].replace(",", ""))
    return out


def monthly_totals(ops: Iterable[Intervention], signed: bool = True) -> dict[tuple[int, int], int]:
    """{(year, month): total}; signed by yen_sign (operations without the yen count 0)."""
    out: dict[tuple[int, int], int] = {}
    for o in ops:
        k = (o.day.year, o.day.month)
        out[k] = out.get(k, 0) + (o.amount * o.yen_sign if signed else o.amount)
    return out


def _month_end(year: int, month: int) -> date:
    nxt = date(year + month // 12, month % 12 + 1, 1)
    return nxt - timedelta(days=1)


def mof_month_available_on(year: int, month: int) -> date:
    """The month's total is published on its last business day (Tokyo, after the market);
    the first decision that may use it is the day after the calendar month end."""
    return _month_end(year, month) + timedelta(days=1)


MOF_DAILY_LAG_DAYS = 45


def mof_daily_available_on(day: date) -> date:
    """Daily detail is published once a quarter, early in the month after the quarter ends
    (exact dates not checked: research/data-wide-1.md). Default: quarter end + 45 days."""
    q_end_month = ((day.month - 1) // 3 + 1) * 3
    return _month_end(day.year, q_end_month) + timedelta(days=MOF_DAILY_LAG_DAYS)
