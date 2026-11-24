"""survey-5: download daily price history of public LIVE funds and ETFs (Yahoo chart API,
keyless) into the git-ignored cache, and print each one's first bar and name. No returns are
computed here (the card comes before any number).

    python -I research/lib/survey5_fetch.py <cache_root> [TICKER ...]

Writes `<cache_root>/downloads/survey-5/yahoo/<TICKER>.json` (raw response, untrusted data:
parsed as JSON only) and `<cache_root>/derived/survey-5/<TICKER>.csv` (date, close, adjclose).
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (daily-bar research script)"
URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/{t}"
    "?period1=-631152000&period2={now}&interval=1d&events=div%2Csplit&includeAdjustedClose=true"
)
TICKERS = [
    # trend following / managed futures
    "AQMIX", "PQTIX", "ASFYX", "RYMFX", "WTMF", "DBMF", "KMLM", "CTA", "ABYIX", "LCSIX",
    # risk parity / balanced risk
    "ABRZX", "AQRIX", "RPAR",
    # defensive / low volatility
    "USMV", "SPLV",
    # carry / multi-style premia
    "DBV", "QSPIX",
]  # fmt: skip


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body: bytes = resp.read()
                return body
        except Exception as e:  # noqa: BLE001 - retry any transient failure
            if attempt == 3:
                raise
            print(f"  retry after {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise AssertionError("unreachable")


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    tickers = sys.argv[2:] or TICKERS
    raw_dir = root / "downloads" / "survey-5" / "yahoo"
    out_dir = root / "derived" / "survey-5"
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
        first = datetime.fromtimestamp(meta.get("firstTradeDate") or ts[0], UTC).date()
        name = meta.get("longName") or meta.get("shortName")
        kind = meta.get("instrumentType")
        print(f"{t}: {kind} | {name} | first {first} | bars {len(rows)} | last {rows[-1][0]}")
        time.sleep(1)


if __name__ == "__main__":
    main()
