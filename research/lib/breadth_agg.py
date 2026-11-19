"""Aggregate raw 1-minute downloads into hourly bars for research run breadth-1.

Reads (never runs) the shared cache (`macro.cache_root()`): Binance spot 1m klines (30 USDT
pairs), Binance USDT-perp funding and 1h premium index, Bitstamp 1m BTC/ETH. Writes one `.npz`
per series under `<cache_root>/derived/breadth-1/` (never committed). Bars after the train cut
(`TRAIN_LAST_BAR`) are dropped here, so nothing downstream can see them.

    uv run python -I research/lib/breadth_agg.py [binance|bitstamp|funding|all]

Hourly arrays: `t` (hour start, seconds since epoch, UTC), `o`, `h`, `l`, `c`, `v` (base
volume), `q` (quote volume, USD; Bitstamp: v x close).
"""

from __future__ import annotations

import io
import json
import sys
import zipfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro  # noqa: E402
from harness import TRAIN_LAST_BAR  # noqa: E402

CUT = int(
    datetime.combine(TRAIN_LAST_BAR + timedelta(days=1), datetime.min.time(), UTC).timestamp()
)


def out_dir() -> Path:
    d = macro.cache_root() / "derived" / "breadth-1"
    d.mkdir(parents=True, exist_ok=True)
    return d


def to_hourly(
    ts: np.ndarray,
    o: np.ndarray,
    h: np.ndarray,
    lo: np.ndarray,
    c: np.ndarray,
    v: np.ndarray,
    q: np.ndarray,
) -> dict[str, np.ndarray]:
    """Minute rows (any order, duplicates allowed) -> hourly OHLCV, hours with data only."""
    keep = ts < CUT
    ts, o, h, lo, c, v, q = (x[keep] for x in (ts, o, h, lo, c, v, q))
    order = np.lexsort((ts,))
    ts, o, h, lo, c, v, q = (x[order] for x in (ts, o, h, lo, c, v, q))
    ts, first = np.unique(ts, return_index=True)  # drop duplicate minutes
    o, h, lo, c, v, q = (x[first] for x in (o, h, lo, c, v, q))
    hr = ts // 3600 * 3600
    start = np.r_[0, np.flatnonzero(np.diff(hr)) + 1]
    end = np.r_[start[1:], len(hr)]
    return {
        "t": hr[start],
        "o": o[start],
        "h": np.maximum.reduceat(h, start),
        "l": np.minimum.reduceat(lo, start),
        "c": c[end - 1],
        "v": np.add.reduceat(v, start),
        "q": np.add.reduceat(q, start),
    }


def _kline_rows(path: Path) -> np.ndarray:
    with zipfile.ZipFile(path) as z:
        raw = z.read(z.namelist()[0])
    lines = [ln for ln in raw.splitlines() if ln[:1].isdigit()]  # skip a header if present
    if not lines:
        return np.empty((0, 12))
    return np.loadtxt(io.BytesIO(b"\n".join(lines)), delimiter=",", usecols=range(8), ndmin=2)


def binance_spot(sym: str) -> None:
    folder = macro.cache_root() / "binance" / "spot" / "monthly" / "klines" / sym / "1m"
    parts = [_kline_rows(p) for p in sorted(folder.glob("*.zip"))]
    a = np.concatenate([p for p in parts if len(p)])
    ts = a[:, 0].copy()
    ts[ts > 1e14] /= 1000.0  # 2025+ files are in microseconds
    ts = (ts // 1000).astype(np.int64)
    bars = to_hourly(ts, a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5], a[:, 7])
    np.savez(out_dir() / f"binance-{sym}-1h.npz", **bars)  # type: ignore[arg-type]


def binance_funding(sym: str) -> None:
    root = macro.cache_root() / "binance" / "futures" / "um" / "monthly"
    rows = []
    for p in sorted((root / "fundingRate" / sym).glob("*.zip")):
        with zipfile.ZipFile(p) as z:
            for ln in z.read(z.namelist()[0]).decode().splitlines():
                f = ln.split(",")
                if f[0].isdigit():
                    rows.append((int(f[0]) // 1000, float(f[-1])))
    prem = []
    for p in sorted((root / "premiumIndexKlines" / sym / "1h").glob("*.zip")):
        prem.append(_kline_rows(p))
    out: dict[str, np.ndarray] = {}
    if rows:
        f = np.array(sorted(set(rows)))
        f = f[f[:, 0] < CUT]
        out |= {"ft": f[:, 0].astype(np.int64), "fr": f[:, 1]}
    prem = [p for p in prem if len(p)]
    if prem:
        a = np.concatenate(prem)
        ts = a[:, 0].copy()
        ts[ts > 1e14] /= 1000.0
        t = (ts // 1000).astype(np.int64)
        t, i = np.unique(t, return_index=True)
        k = t < CUT
        out |= {"pt": t[k], "pc": a[i, 4][k]}  # premium at the bar's close; bar starts at pt
    if out:
        np.savez(out_dir() / f"binance-{sym}-funding.npz", **out)  # type: ignore[arg-type]


def bitstamp(pair: str) -> None:
    folder = macro.cache_root() / "bitstamp" / "1m" / pair
    cols: list[list[float]] = [[] for _ in range(6)]
    for p in sorted(folder.rglob("*.json")):
        for r in json.loads(p.read_text())["data"]["ohlc"]:
            for i, k in enumerate(("timestamp", "open", "high", "low", "close", "volume")):
                cols[i].append(float(r[k]))
    ts, o, h, lo, c, v = (np.array(x) for x in cols)
    bars = to_hourly(ts.astype(np.int64), o, h, lo, c, v, v * c)
    np.savez(out_dir() / f"bitstamp-{pair}-1h.npz", **bars)  # type: ignore[arg-type]


def main(what: str) -> None:
    syms = sorted(
        p.name for p in (macro.cache_root() / "binance/spot/monthly/klines").iterdir() if p.is_dir()
    )
    if what in ("bitstamp", "all"):
        for pair in ("btcusd", "ethusd"):
            bitstamp(pair)
            print("bitstamp", pair, flush=True)
    if what in ("funding", "all"):
        for s in syms:
            binance_funding(s)
        print("funding done", flush=True)
    if what in ("binance", "all"):
        for s in syms:
            binance_spot(s)
            print("binance", s, flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
