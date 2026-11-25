"""Fetch the data-long-4 raw files into the git-ignored cache (research/data-long-4.md).

    uv run python -I research/lib/long_macro_fetch.py            # everything not yet cached
    uv run python -I research/lib/long_macro_fetch.py --list     # print the plan only
    uv run python -I research/lib/long_macro_fetch.py --jst <path>   # register a JST download

Keyless public sources only. Every file is written once through `grimstrade.cache.write_once`
(manifest line with URL, time, size, SHA-256) under `<cache_root>/data-long-4/`. Nothing here is
committed: none of the licences below clearly allows redistribution inside an MIT repo
(BIS and JST: non-commercial only; French and OECD: no redistribution grant). The cache root is
`research/macro.local.json` (git-ignored, copy the `.example`) or GRIMSTRADE_DATA.

- BIS long consumer prices (WS_LONG_CPI, index 2010 = 100) and central-bank policy rates
  (WS_CBPOL), SDMX REST csv. The query's endPeriod keeps every period after the train window off
  the disk: monthly CPI to 2025-09 (the October 2025 prints were published after 2025-11-10),
  annual CPI to 2024, policy rates to 2025-10 (known on the day).
- Jorda-Schularick-Taylor Macrohistory Database, release 6 (annual 1870-2020, 18 countries),
  CC BY-NC-SA 4.0. NOT fetched by this script: the site answered 403 to urllib's default
  agent (2026-11-24). The cached copy is the lane's own plain curl download (curl's default
  agent), made during the source probes before the 403 was seen. To reproduce, download `JST`
  in a browser and register it with `--jst <path>` (`register_manual`: write-once copy into
  `<cache_root>/data-long-4/jst/JSTdatasetR6.xlsx` with a manifest line);
  `long_macro.parse_jst` reads it.
- Kenneth R. French, international country files with and without dividends (monthly
  value-weight market and B/M, E/P, CE/P, D/P sorted portfolios from 1975, plus annual
  value-weight averages of B/M, E/P, CE/P and dividend yield). The files run past the train
  window; the parser cuts at 2025-10.
- ALFRED vintage 2025-11-10: US CPI (BLS, public domain), OECD MEI CPI (cross-check) and OECD
  MEI share price indices.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import long_x_fetch as lxf  # noqa: E402

from grimstrade import cache  # noqa: E402

VINTAGE = lxf.VINTAGE
SNAP = "2026-11-24"
DIR = "data-long-4"

# ISO2 codes as BIS uses them; XM = euro area
BIS_AREAS = ["US", "JP", "GB", "CH", "CA", "DE", "XM", "AU", "NZ", "SE", "NO"]
_AREAS = "+".join(BIS_AREAS)
BIS = "https://stats.bis.org/api/v1/data/{flow}/{key}/all?format=csv&endPeriod={end}"
BIS_FILES = {
    "bis/cpi-monthly.csv": BIS.format(flow="WS_LONG_CPI", key=f"M.{_AREAS}.628", end="2025-09"),
    "bis/cpi-annual.csv": BIS.format(flow="WS_LONG_CPI", key=f"A.{_AREAS}.628", end="2024"),
    "bis/policy-monthly.csv": BIS.format(flow="WS_CBPOL", key=f"M.{_AREAS}", end="2025-10"),
}
JST = "https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx"
FRENCH = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/{f}"
FRENCH_FILES = ["F-F_International_Countries.zip", "F-F_International_Countries_Wout_Div.zip"]

# OECD MEI CPI (ISO3 ids on FRED; AU and NZ are quarterly) and share price indices
MEI_CPI = [
    "GBRCPIALLMINMEI", "JPNCPIALLMINMEI", "CHECPIALLMINMEI", "CANCPIALLMINMEI",
    "DEUCPIALLMINMEI", "AUSCPIALLQINMEI", "NZLCPIALLQINMEI", "SWECPIALLMINMEI",
    "NORCPIALLMINMEI", "USACPIALLMINMEI",
]  # fmt: skip
SHARES = [
    f"SPASTT01{c}M661N" for c in ("US", "JP", "GB", "CH", "CA", "DE", "EZ", "AU", "NZ", "SE", "NO")
]
ALFRED_IDS = ["CPIAUCNS", *MEI_CPI, *SHARES]


def plan() -> list[tuple[str, str]]:
    out = [(f"{DIR}/{rel}", url) for rel, url in BIS_FILES.items()]
    out += [(f"{DIR}/french/{SNAP}/{f}", FRENCH.format(f=f)) for f in FRENCH_FILES]
    out += [
        (f"{DIR}/alfred/{VINTAGE}/{s}.csv", lxf.ALFRED.format(id=s, v=VINTAGE)) for s in ALFRED_IDS
    ]
    return out


def _looks_right(rel: str, data: bytes) -> bool:
    if rel.endswith(".csv") and "/alfred/" in rel:
        return data.startswith(b"observation_date")
    if rel.endswith(".csv"):
        return data.startswith(b"FREQ,REF_AREA")
    return data[:2] == b"PK"  # xlsx and zip


def register_manual(src: Path, rel: str, url: str) -> None:
    """Copy a file downloaded by hand into the cache, write-once, with its manifest line."""
    data = src.read_bytes()
    if not _looks_right(rel, data):
        raise ValueError(f"unexpected content: {src}")
    cache.write_once(lxf.cache_root(), rel, data, url)


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--jst":  # register a hand download of JST
        register_manual(Path(sys.argv[2]), f"{DIR}/jst/JSTdatasetR6.xlsx", JST)
        return
    root = lxf.cache_root()
    failed = []
    for rel, url in plan():
        if "--list" in sys.argv:
            print(rel, url)
            continue
        if (root / rel).exists():
            continue
        try:
            data = lxf._get(url)
        except RuntimeError as e:
            failed.append(rel)
            print(e)
            continue
        if not _looks_right(rel, data):
            failed.append(rel)
            print(f"unexpected content: {rel} ({data[:60]!r})")
            continue
        cache.write_once(root, rel, data, url)
        print(f"ok {rel} {len(data)}", flush=True)
        time.sleep(1.0)
    print("failed:", failed)


if __name__ == "__main__":
    main()
