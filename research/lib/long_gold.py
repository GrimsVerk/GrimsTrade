"""Monthly gold price in USD from datahub.io core/gold-prices (research/data-long-1.md).

Source: https://datahub.io/core/gold-prices/r/monthly.csv (ODC PDDL, public domain). Download
it by hand into `<cache_root>/datahub-gold/<YYYY-MM-DD>/monthly.csv` (the download date); never
commit it. Cache root: GRIMSTRADE_DATA or `research/macro.local.json` (git-ignored, copy the
`.example`). The newest dated folder is read unless a path is given.

File: header `Date,Price`, one row per month `YYYY-MM,price`. The copy fetched 2026-11-18
(sha256 f20720f3...a9608) has 2,326 months, 1833-01 to 2026-10, no gaps. The price is a monthly
figure (World Bank / Bundesbank lineage, most likely the average of the month's London fixings,
not a month-end close) and is whole dollars through the early 1970s. The US price was fixed
(20.67, then 35.00 from 1934) until the two-tier market of 1968 and the end of convertibility in
1971-08: gold before `FREE_FROM` is not market risk and must not be read as gold history.
"""

from __future__ import annotations

import csv
import json
import os
from collections.abc import Iterable, Sequence
from datetime import date
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[1]
CONFIG = RESEARCH / "macro.local.json"
FOLDER = "datahub-gold"
FREE_FROM = date(1971, 1, 1)  # data-long-1: "use gold only from 1971"


def cache_root() -> Path:
    env = os.environ.get("GRIMSTRADE_DATA")
    if env:
        return Path(env).expanduser()
    if CONFIG.exists():
        return Path(json.loads(CONFIG.read_text())["cache_root"]).expanduser()
    raise FileNotFoundError(f"set GRIMSTRADE_DATA or copy {CONFIG.name}.example to {CONFIG.name}")


def _month(text: str) -> date:
    y, m = text.strip().split("-")
    return date(int(y), int(m), 1)


def _next(d: date) -> date:
    return date(d.year + d.month // 12, d.month % 12 + 1, 1)


def parse(lines: Iterable[str]) -> list[tuple[date, float]]:
    """(first of month, USD price) from the csv text; months must be consecutive."""
    rows = csv.reader(lines)
    header = [h.strip() for h in next(rows)]
    if header != ["Date", "Price"]:
        raise ValueError(f"unexpected header {header}")
    out: list[tuple[date, float]] = []
    for row in rows:
        if not row or not row[0].strip():
            continue
        d, px = _month(row[0]), float(row[1])
        if not px > 0:
            raise ValueError(f"bad price {row!r}")
        if out and d != _next(out[-1][0]):
            raise ValueError(f"gap or disorder: {out[-1][0]} then {d}")
        out.append((d, px))
    if not out:
        raise ValueError("no rows")
    return out


def returns(
    prices: Sequence[tuple[date, float]], since: date | None = None
) -> list[tuple[date, float]]:
    """Gross monthly returns, dated by the month they end in (price[m] / price[m-1])."""
    out = [(d, p / q) for (_, q), (d, p) in zip(prices, prices[1:], strict=False)]
    return [x for x in out if since is None or x[0] >= since]


def latest(root: Path | None = None) -> Path:
    base = (root or cache_root()) / FOLDER
    snaps = sorted(p for p in base.iterdir() if (p / "monthly.csv").exists())
    if not snaps:
        raise FileNotFoundError(f"no {FOLDER}/<date>/monthly.csv under {base.parent}")
    return snaps[-1] / "monthly.csv"


def load(path: Path | None = None) -> list[tuple[date, float]]:
    path = path or latest()
    with path.open(newline="") as f:
        return parse(f)
