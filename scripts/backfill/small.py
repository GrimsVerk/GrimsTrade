"""Backfill the small keyless sources (each a few MB or less) into the local cache.

Whole-history files are saved under a dated folder, `<source>/<YYYY-MM-DD>/<name>`, so a later run
adds a new snapshot instead of editing one. Chunked series (Deribit, ALFRED vintages, GDELT days)
are saved one file per chunk and skipped once present. Resumable: re-run. About 1 request/second.
Sources: docs/data-sources.md sections 2, 4.3, 5, 6. Sizes and paths: docs/data-inventory.md.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import UTC, date, datetime, timedelta

from grimstrade.cache import cache_root, fetch_file, start_job
from grimstrade.sources import http_get

# FRED/ALFRED's CSV endpoints stall our (honest) User-Agent since 2026-11-12. We don't disguise
# the client; they are skipped until the owner decides (FRED's official API needs a free key).
SKIP_HOSTS = ("stlouisfed.org",)

TODAY = datetime.now(UTC).date()
NOW = int(time.time())
YAHOO = [
    "^GSPC",
    "^DJI",
    "^IXIC",
    "^RUT",
    "^NYA",
    "^VIX",
    "^VIX9D",
    "^VIX3M",
    "^VVIX",
    "^SKEW",
    "^IRX",
    "^FVX",
    "^TNX",
    "^TYX",
    "SPY",
    "QQQ",
    "GLD",
    "TLT",
    "IWM",
    "DIA",
    "EFA",
    "EEM",
    "VNQ",
    "IEF",
    "SHY",
    "LQD",
    "HYG",
    "SLV",
    "USO",
    "UUP",
    "XLE",
    "XLF",
    "XLK",
    "XLV",
    "BTC-USD",
    "ETH-USD",
    "GC=F",
    "CL=F",
    "DX-Y.NYB",
]
FRED = [
    "DFF",
    "FEDFUNDS",
    "DGS3MO",
    "DGS2",
    "DGS10",
    "DGS30",
    "T10Y2Y",
    "T10Y3M",
    "BAA10Y",
    "AAA10Y",
    "VIXCLS",
    "WALCL",
    "M2SL",
    "CPIAUCSL",
    "PAYEMS",
    "UNRATE",
    "INDPRO",
    "DTWEXBGS",
    "DCOILWTICO",
    "RRPONTSYD",
]
ALFRED = ["PAYEMS", "M2SL", "CPIAUCSL", "UNRATE", "INDPRO", "WALCL"]  # revised series
FRENCH = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
FRENCH_FILES = [
    "F-F_Research_Data_Factors_CSV.zip",
    "F-F_Research_Data_Factors_daily_CSV.zip",
    "F-F_Research_Data_5_Factors_2x3_daily_CSV.zip",
    "F-F_Momentum_Factor_daily_CSV.zip",
    "F-F_Momentum_Factor_CSV.zip",
    "10_Industry_Portfolios_daily_CSV.zip",
]
BLOCKCHAIN = "hash-rate miners-revenue transaction-fees-usd n-transactions n-unique-addresses"
COINMETRICS = "AdrActCnt,CapMVRVCur,CapMrktCurUSD,HashRate,TxCnt,FeeTotNtv,SplyCur,PriceUSD"


def whole_history() -> list[tuple[str, str]]:
    """(relative path, url) for single-file full histories, saved under today's date."""
    d = TODAY.isoformat()
    out = []
    for t in YAHOO:
        out.append(
            (
                f"yahoo-1d/{d}/{t}.json",
                f"https://query1.finance.yahoo.com/v8/finance/chart/{t}"
                f"?period1=-2208988800&period2={NOW}&interval=1d&events=div,split",
            )
        )
    for s in FRED:
        out.append((f"fred/{d}/{s}.csv", f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}"))
    out += [(f"french/{d}/{f}", FRENCH + f) for f in FRENCH_FILES]
    out.append((f"shiller/{d}/ie_data.xls", "http://www.econ.yale.edu/~shiller/data/ie_data.xls"))
    for y in range(1990, TODAY.year + 1):
        out.append(
            (
                f"treasury/{d}/yield-curve-{y}.csv",
                "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
                f"daily-treasury-rates.csv/{y}/all?type=daily_treasury_yield_curve"
                f"&field_tdr_date_value={y}&page&_format=csv",
            )
        )
    for f in ["routputqvqd.xlsx", "pcpiqvqd.xlsx", "ruc_qvmd.xlsx", "employmvmd.xlsx"]:
        out.append(
            (
                f"philly-rtdsm/{d}/{f}",
                "https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/"
                f"real-time-data/data-files/xlsx/{f}",
            )
        )
    for v in ["VIX", "VIX9D", "VIX3M", "VIX6M", "VVIX", "SKEW"]:
        out.append(
            (
                f"cboe/{d}/{v}_History.csv",
                f"https://cdn.cboe.com/api/global/us_indices/daily_prices/{v}_History.csv",
            )
        )
    for c in BLOCKCHAIN.split():
        out.append(
            (
                f"blockchain-com/{d}/{c}.json",
                f"https://api.blockchain.info/charts/{c}?timespan=all&format=json&sampled=false",
            )
        )
    out.append((f"fear-greed/{d}/fng.json", "https://api.alternative.me/fng/?limit=0&format=json"))
    return out


def chunked() -> list[tuple[str, str]]:
    """(relative path, url) for series fetched in pieces; each piece is final once saved."""
    out = []
    step = 30 * 86400
    deribit = "https://www.deribit.com/api/v2/public/"
    for cur, first in [("BTC", "2019-04-01"), ("ETH", "2019-04-01")]:
        t = int(datetime.fromisoformat(first).replace(tzinfo=UTC).timestamp())
        t -= t % step
        while t + step + 900 <= NOW:
            a, b = t * 1000, (t + step) * 1000 - 1
            out.append(
                (
                    f"deribit/funding/{cur}-PERPETUAL/{t}.json",
                    f"{deribit}get_funding_rate_history?instrument_name={cur}-PERPETUAL"
                    f"&start_timestamp={a}&end_timestamp={b}",
                )
            )
            if t >= 1614556800:  # DVOL starts 2021-03
                out.append(
                    (
                        f"deribit/dvol/{cur}/{t}.json",
                        f"{deribit}get_volatility_index_data?currency={cur}"
                        f"&start_timestamp={a}&end_timestamp={b}&resolution=3600",
                    )
                )
            t += step
    # ALFRED: the series as published on the 1st and 15th of each month since 2000.
    for s in ALFRED:
        y = 2000
        while y <= TODAY.year:
            for m in range(1, 13):
                for dd in (1, 15):
                    v = date(y, m, dd)
                    if v < TODAY:
                        out.append(
                            (
                                f"fred/alfred/{s}/{v}.csv",
                                "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
                                f"?id={s}&vintage_date={v}",
                            )
                        )
            y += 1
    # GDELT 1.0 daily event files: a 30-day sample, not the whole archive.
    for k in range(2, 32):
        d = TODAY - timedelta(days=k)
        out.append(
            (
                f"gdelt/events/{d:%Y%m%d}.export.CSV.zip",
                f"http://data.gdeltproject.org/events/{d:%Y%m%d}.export.CSV.zip",
            )
        )
    return out


def coinmetrics(root_rel: str) -> list[tuple[str, str]]:
    return [
        (
            root_rel,
            "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc,eth"
            f"&metrics={COINMETRICS}&frequency=1d&start_time=2009-01-01&page_size=10000",
        )
    ]


def main() -> int:
    root = cache_root()
    start_job(root, "small")
    errors = 0
    jobs = whole_history() + chunked()
    # Coin Metrics pages through next_page_url; each page is its own file.
    cm_dir = f"coinmetrics/{TODAY.isoformat()}"
    page, url = 0, coinmetrics("")[0][1]
    while url:
        rel = f"{cm_dir}/page-{page:03d}.json"
        try:
            fetch_file(root, rel, url, http_get)
            url = json.loads((root / rel).read_bytes()).get("next_page_url", "")
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {rel}: {e!r}", flush=True)
            errors += 1
            break
        page += 1
        time.sleep(1)
    for i, (rel, url) in enumerate(jobs):
        if (root / rel).exists() or any(h in url for h in SKIP_HOSTS):
            continue
        try:
            fetch_file(root, rel, url, http_get)
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {rel}: {e!r}", flush=True)
            errors += 1
        time.sleep(1)
        if i % 200 == 0:
            print(f"{time.strftime('%H:%M:%S')} {i}/{len(jobs)}", flush=True)
    print(f"DONE errors={errors}", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
