"""ls-trend-1: download daily history of the wider ETF universe (Yahoo chart API, keyless) into
the git-ignored cache, and print each one's name and first bar. No returns are computed here
(the card comes before any number).

    python -I research/lib/lstrend1_fetch.py <cache_root> [TICKER ...]

Writes `<cache_root>/downloads/ls-trend-1/yahoo/<TICKER>.json` (raw response, untrusted data:
parsed as JSON only) and `<cache_root>/derived/ls-trend-1/<TICKER>.csv` (date, close, adjclose).
"""

from __future__ import annotations

import csv
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from survey5_fetch import URL, get  # noqa: E402

TICKERS = [
    # equity indexes: the nine developed markets of Moskowitz-Ooi-Pedersen 2012, as country ETFs
    "SPY", "EWA", "EWG", "EWP", "EWQ", "EWI", "EWJ", "EWN", "EWU",
    # US Treasury bonds along the curve
    "SHY", "IEI", "IEF", "TLT",
    # commodities: single-commodity ETFs and the two sector baskets without a single-commodity ETF
    "GLD", "SLV", "PPLT", "PALL", "CPER", "DBB", "USO", "BNO", "UGA", "UNG",
    "CORN", "WEAT", "SOYB", "CANE", "DBA",
    # currencies against the US dollar
    "FXE", "FXY", "FXB", "FXA", "FXC", "FXF",
    # the narrow set of tsmom12-c00
    "QQQ",
]  # fmt: skip


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    tickers = sys.argv[2:] or TICKERS
    raw_dir = root / "downloads" / "ls-trend-1" / "yahoo"
    out_dir = root / "derived" / "ls-trend-1"
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    now = int(datetime.now(UTC).timestamp())
    for t in tickers:
        try:
            body = get(URL.format(t=t, now=now))
        except Exception as e:  # noqa: BLE001
            print(f"{t}: FAILED {type(e).__name__}: {e}")
            continue
        (raw_dir / f"{t}.json").write_bytes(body)
        res = json.loads(body)["chart"]["result"]
        if not res:
            print(f"{t}: no result")
            continue
        r = res[0]
        meta = r["meta"]
        ts = r.get("timestamp") or []
        q = r["indicators"]["quote"][0]
        adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose") or [None] * len(ts)
        rows = [
            (datetime.fromtimestamp(x, UTC).date().isoformat(), c, a)
            for x, c, a in zip(ts, q["close"], adj, strict=True)
            if c is not None and a is not None
        ]
        with (out_dir / f"{t}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "close", "adjclose"])
            w.writerows(rows)
        name = meta.get("longName") or meta.get("shortName")
        print(f"{t}: {name} | first {rows[0][0]} | bars {len(rows)} | last {rows[-1][0]}")
        time.sleep(1)


if __name__ == "__main__":
    main()
