"""On-chain inputs for coins (run rl-2, card "On-chain variant" in research/rl-2.md).

Coin Metrics community daily metrics from the shared cache (`macro.cache_root()`), folder
`coinmetrics/full/2026-11-13/assets/<coin>/page-000.json`. As-of rule of the macro layer: a row
dated `d` is used from the day after, so a decision on day `d` sees rows dated before `d`.

Inputs (fixed on the card): `mvrv` = log(CapMVRVCur), the latest value; `adr_growth` and
`fee_growth` = log(30-day mean / 365-day mean) of AdrActCnt and FeeTotNtv. 0 when there are
fewer than 365 rows or the latest row is more than 7 days old. Exchange flows are not used
(revised attribution: look-ahead).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import date

import numpy as np

FEATS = ["mvrv", "adr_growth", "fee_growth"]
SNAPSHOT = "full/2026-11-13"
STALE_DAYS = 7


@dataclass
class Series:
    ords: np.ndarray  # date ordinals, ascending
    mvrv: np.ndarray  # NaN where missing
    adr: np.ndarray
    fee: np.ndarray


def from_rows(rows: list[dict[str, str | None]]) -> Series:
    def num(r: dict[str, str | None], k: str) -> float:
        v = r.get(k)
        return float(v) if v not in (None, "") else math.nan

    rows = sorted(rows, key=lambda r: str(r["time"]))
    return Series(
        np.array([date.fromisoformat(str(r["time"])[:10]).toordinal() for r in rows]),
        np.array([num(r, "CapMVRVCur") for r in rows]),
        np.array([num(r, "AdrActCnt") for r in rows]),
        np.array([num(r, "FeeTotNtv") for r in rows]),
    )


def load(coin: str) -> Series | None:
    import macro

    path = macro.cache_root() / "coinmetrics" / SNAPSHOT / "assets" / coin.lower() / "page-000.json"
    if not path.exists():
        return None
    return from_rows(json.loads(path.read_text())["data"])


def _growth(x: np.ndarray) -> float:
    long, short = np.nanmean(x[-365:]), np.nanmean(x[-30:])
    if not (long > 0 and short > 0):
        return 0.0
    return float(math.log(short / long))


def features_at(s: Series, d: date) -> list[float]:
    """The three inputs as a decision on day d may see them (rows dated before d)."""
    j = int(np.searchsorted(s.ords, d.toordinal()))  # rows 0..j-1 are dated before d
    if j < 365 or d.toordinal() - s.ords[j - 1] > STALE_DAYS:
        return [0.0, 0.0, 0.0]
    m = s.mvrv[:j]
    ok = np.flatnonzero(~np.isnan(m))
    mv = math.log(m[ok[-1]]) if len(ok) and m[ok[-1]] > 0 and j - 1 - ok[-1] <= STALE_DAYS else 0.0
    return [mv, _growth(s.adr[:j]), _growth(s.fee[:j])]
