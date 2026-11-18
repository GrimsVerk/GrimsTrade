"""survey-6: download keyless live histories of long-running funds and ETFs per strategy family,
plain holdings to match them, and published paper factors, into the git-ignored cache. Prints
each Yahoo series' name, type and first and last bar only: **no return is computed here** (the
card comes before any number).

    python -I research/lib/survey6_fetch.py <cache_root>            # everything
    python -I research/lib/survey6_fetch.py <cache_root> TICKER ...  # some Yahoo tickers again
    python -I research/lib/survey6_fetch.py <cache_root> --files     # the non-Yahoo files only

Writes (raw files are untrusted data: parsed as JSON / CSV / zip only, never executed):
- `<cache_root>/downloads/survey-6/yahoo/<TICKER>.json`, parsed to
  `<cache_root>/derived/survey-6/<TICKER>.csv` (date, close, adjclose);
- `<cache_root>/downloads/survey-6/french/<name>.zip` (Ken French data library);
- `<cache_root>/downloads/survey-6/aqr/<name>.xlsx` (AQR data sets);
- `<cache_root>/downloads/survey-6/cboe/<name>.csv` (CBOE strategy benchmark indexes).
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

# Family -> live funds / ETFs. Picked by name before any return was seen (survey-6.md says how).
FAMILIES: dict[str, list[str]] = {
    "value": ["DFLVX", "DFSVX", "DFIVX", "VIVAX", "IWD", "IWN", "VTV", "RPV"],
    "momentum": ["AMOMX", "ASMOX", "AIMOX", "PDP", "MTUM"],
    "quality": ["SPHQ", "QUAL"],
    "low-vol": ["SPLV", "USMV", "ACWV", "EEMV"],
    "multi-factor": ["DFEOX", "DFQTX", "LRGF", "GSLC", "QSPIX"],
    "dividend": ["DVY", "SDY", "VIG", "VYM", "SCHD", "VDIGX"],
    "fx-carry": ["CEW", "DBV"],
    "merger-arb": ["MERFX", "ARBFX", "MNA"],
    "option-writing": ["GATEX", "PBP", "XYLD", "QYLD"],
    "tail-hedge": ["TAIL", "SWAN", "VIXY", "BTAL"],
    "gold-miners": ["INIVX", "FSAGX", "VGPMX", "GDX", "GDXJ"],
    "defensive-sectors": ["XLP", "XLU", "XLV", "SECT"],
}
# Plain holdings to match the families against (and the market for context).
HOLDINGS = ["SPY", "VFINX", "NAESX", "IWB", "IWM", "VTSMX", "EFA", "EEM", "ACWI", "VBMFX",
            "AGG", "QQQ", "GLD", "VGTSX"]  # fmt: skip

FRENCH = {
    "ff3": "F-F_Research_Data_Factors_CSV.zip",
    "ff5": "F-F_Research_Data_5_Factors_2x3_CSV.zip",
    "mom": "F-F_Momentum_Factor_CSV.zip",
}
FRENCH_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{f}"
AQR = {
    "bab": "Betting-Against-Beta-Equity-Factors-Monthly.xlsx",
    "qmj": "Quality-Minus-Junk-Factors-Monthly.xlsx",
}
AQR_URL = "https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/{f}"
CBOE = ["BXM", "PUT"]
CBOE_URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{n}_History.csv"


def yahoo(root: Path, tickers: list[str]) -> None:
    raw_dir = root / "downloads" / "survey-6" / "yahoo"
    out_dir = root / "derived" / "survey-6"
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
        if "close" not in q:
            print(f"{t}: no price bars (meta only)")
            continue
        adj = r["indicators"].get("adjclose", [{}])[0].get("adjclose") or [None] * len(ts)
        rows = [
            (datetime.fromtimestamp(x, UTC).date().isoformat(), c, a)
            for x, c, a in zip(ts, q["close"], adj, strict=True)
            if c is not None and a is not None
        ]
        if not rows:
            print(f"{t}: no bars")
            continue
        with (out_dir / f"{t}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["date", "close", "adjclose"])
            w.writerows(rows)
        first = datetime.fromtimestamp(meta.get("firstTradeDate") or ts[0], UTC).date()
        name = meta.get("longName") or meta.get("shortName")
        kind = meta.get("instrumentType")
        print(
            f"{t}: {kind} | {name} | first {first} | bars {len(rows)} | {rows[0][0]}..{rows[-1][0]}"
        )
        time.sleep(1)


def files(root: Path) -> None:
    jobs = [("french", n, FRENCH_URL.format(f=f), ".zip") for n, f in FRENCH.items()]
    jobs += [("aqr", n, AQR_URL.format(f=f), ".xlsx") for n, f in AQR.items()]
    jobs += [("cboe", n, CBOE_URL.format(n=n), ".csv") for n in CBOE]
    for sub, name, url, ext in jobs:
        d = root / "downloads" / "survey-6" / sub
        d.mkdir(parents=True, exist_ok=True)
        try:
            body = get(url)
        except Exception as e:  # noqa: BLE001
            print(f"{sub}/{name}: FAILED {type(e).__name__}: {e}")
            continue
        (d / f"{name}{ext}").write_bytes(body)
        print(f"{sub}/{name}: {len(body)} bytes")
        time.sleep(1)


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    if sys.argv[2:] == ["--files"]:
        files(root)
        return
    if sys.argv[2:]:
        yahoo(root, sys.argv[2:])
        return
    yahoo(root, [t for ts in FAMILIES.values() for t in ts] + HOLDINGS)
    files(root)


if __name__ == "__main__":
    main()
