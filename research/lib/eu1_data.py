"""eu-1 data: European-listed UCITS ETFs/ETCs, EUR rates, US twins in EUR. Stdlib only.

    uv run python -I research/lib/eu1_data.py fetch   # public Yahoo chart + ECB rate CSV
    uv run python -I research/lib/eu1_data.py build   # parse the saved files into research/data

`fetch` saves the raw responses under `<cache root>/eu-1/raw-<UTC date>/` (cache root from the
git-ignored `research/macro.local.json`). `build` reads the newest raw folder as data only
(json.loads / csv, never executed) and writes, in the git-ignored `research/data/`:

- `bars/<SYM>.csv`, `adj/<SYM>.csv`: each UCITS listing as quoted (EUR), raw and
  dividend-adjusted (total return), the same format as `fetch.py`.
- `bars|adj/<TWIN>-EUR.csv`: a US twin (SPY, QQQ, GLD, TLT, EEM, ...) or a USD coin (BTC, ETH)
  converted to EUR with the day's ECB euro reference rate (USD per EUR, set ~14:15 CET), the
  last rate carried over ECB holidays. The rate starts 1999-01-04, so do the EUR twins.
- `bars|adj/<SYM>-S.csv`: the UCITS listing, extended back before its first day with its twin in
  EUR, scaled to meet it on the listing's first day (a splice; see `research/eu-1.md`).

The US/coin sources must already be in `research/data` (run `research/lib/fetch.py` first).
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.request
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research"
DATA = RESEARCH / "data"
CONFIG = RESEARCH / "macro.local.json"
USER_AGENT = "Mozilla/5.0 (daily-bar research script)"
YAHOO_FROM = -631152000  # 1950-01-01
FIELDS = ["date", "open", "high", "low", "close", "volume"]

# Our symbol -> Yahoo ticker. All quoted in EUR (checked in `build`). Chosen in research/eu-1.md.
UCITS = {
    "IWDA": "IWDA.AS",  # iShares Core MSCI World (Acc), Euronext Amsterdam
    "EUNL": "EUNL.DE",  # same fund, Xetra
    "VWRL": "VWRL.AS",  # Vanguard FTSE All-World (Dist), Amsterdam
    "SXR8": "SXR8.DE",  # iShares Core S&P 500 (Acc), Xetra, EUR line of CSPX
    "CSPX": "CSPX.AS",  # same fund, Amsterdam
    "SXRV": "SXRV.DE",  # iShares Nasdaq 100 (Acc), Xetra
    "EQQQ": "EQQQ.DE",  # Invesco EQQQ Nasdaq-100 (Dist), Xetra
    "EXSA": "EXSA.DE",  # iShares STOXX Europe 600 (DE) (Dist), Xetra
    "MEUD": "MEUD.PA",  # Amundi STOXX Europe 600 (Acc), Paris
    "EMIM": "EMIM.AS",  # iShares Core MSCI EM IMI (Acc), Amsterdam
    "IS3N": "IS3N.DE",  # same fund, Xetra
    "IQQE": "IQQE.DE",  # iShares MSCI EM (Dist), Xetra (older)
    "IBGS": "IBGS.AS",  # iShares Euro Govt Bond 1-3yr (Dist), Amsterdam
    "IBGM": "IBGM.AS",  # iShares Euro Govt Bond 7-10yr (Dist), Amsterdam
    "IBGL": "IBGL.AS",  # iShares Euro Govt Bond 15-30yr (Dist), Amsterdam
    "EXHE": "EXHE.DE",  # iShares eb.rexx Govt Germany 10.5+ (DE), Xetra
    "4GLD": "4GLD.DE",  # Xetra-Gold (physically backed ETC), Xetra
    "EWG2": "EWG2.DE",  # EUWAX Gold II (ETC), Xetra
    "EXXY": "EXXY.DE",  # iShares Diversified Commodity Swap (DE), Xetra
    "IS04": "IS04.DE",  # iShares $ Treasury 20+yr EUR Hedged (Dist), Xetra
}
FX = {"EURUSD": "EURUSD=X"}  # Yahoo, a cross-check of the ECB rate only
ECB_URL = (
    "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"
    "?format=csvdata&startPeriod=1999-01-01"
)


def cache_root() -> Path:
    return Path(json.loads(CONFIG.read_text())["cache_root"]).expanduser()


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body: bytes = resp.read()
                return body
        except Exception as e:  # noqa: BLE001 - retry any transient failure
            if attempt == 4:
                raise
            print(f"  retry after {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def fetch(fx_only: bool = False) -> None:
    now = datetime.now(UTC)
    out = cache_root() / "eu-1" / f"raw-{now:%Y-%m-%d}"
    (out / "yahoo").mkdir(parents=True, exist_ok=True)
    (out / "ecb").mkdir(parents=True, exist_ok=True)
    p2 = int(now.timestamp()) + 86400
    for ticker in [] if fx_only else [*UCITS.values(), *FX.values()]:
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            f"?period1={YAHOO_FROM}&period2={p2}&interval=1d&events=history"
        )
        try:
            (out / "yahoo" / f"{ticker}.json").write_bytes(get(url))
            print("ok", ticker, flush=True)
        except Exception as e:  # noqa: BLE001 - a missing ticker is reported, not fatal
            print("FAILED", ticker, type(e).__name__, e, flush=True)
        time.sleep(0.5)
    (out / "ecb" / "USD-EUR.csv").write_bytes(get(ECB_URL))
    print("ok ECB USD per EUR", flush=True)
    (out / "fetched.txt").write_text(now.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")


# --- build ---

Row = tuple[date, float, float, float, float, float]  # date, open, high, low, close, volume


def newest_raw() -> Path:
    folders = sorted((cache_root() / "eu-1").glob("raw-*"))
    if not folders:
        raise FileNotFoundError("run `fetch` first")
    return folders[-1]


def parse_yahoo(payload: dict[str, Any]) -> tuple[str, list[Row], list[Row]]:
    """(currency, raw rows, dividend-adjusted rows); bars with a missing or zero field dropped."""
    res = payload["chart"]["result"][0]
    cur = str(res["meta"].get("currency"))
    q = res["indicators"]["quote"][0]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    offset = int(res["meta"].get("gmtoffset", 0))
    raw: dict[date, Row] = {}
    adjusted: dict[date, Row] = {}
    for i, ts in enumerate(res["timestamp"]):
        vals = [q["open"][i], q["high"][i], q["low"][i], q["close"][i], adj[i]]
        if any(v is None or v <= 0 for v in vals):
            continue
        d = datetime.fromtimestamp(ts + offset, tz=UTC).date()
        o, h, lo, c, a = (float(v) for v in vals)
        vol = float(q["volume"][i] or 0)
        k = a / c
        raw[d] = (d, o, h, lo, c, vol)
        adjusted[d] = (d, o * k, h * k, lo * k, a, vol)
    return cur, [raw[d] for d in sorted(raw)], [adjusted[d] for d in sorted(adjusted)]


def usd_per_eur(raw: Path) -> list[tuple[date, float]]:
    """Daily USD per EUR, ECB reference rate (SDMX csvdata: TIME_PERIOD, OBS_VALUE)."""
    rate = {}
    with (raw / "ecb" / "USD-EUR.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            if r["OBS_VALUE"] not in ("", "NaN"):
                rate[date.fromisoformat(r["TIME_PERIOD"])] = float(r["OBS_VALUE"])
    return sorted(rate.items())


def read_rows(path: Path) -> list[Row]:
    with path.open(newline="") as f:
        return [
            (date.fromisoformat(r["date"]), float(r["open"]), float(r["high"]), float(r["low"]),
             float(r["close"]), float(r["volume"]))
            for r in csv.DictReader(f)
        ]  # fmt: skip


def write_rows(path: Path, rows: list[Row]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(FIELDS)
        for d, o, h, lo, c, v in rows:
            w.writerow([d.isoformat(), o, h, lo, c, v])


def to_eur(rows: list[Row], fx: list[tuple[date, float]]) -> list[Row]:
    """USD prices / (USD per EUR) of the same date, the last known rate carried over holidays.
    Rows before the first rate are dropped."""
    out = []
    j = -1
    for d, o, h, lo, c, v in rows:
        while j + 1 < len(fx) and fx[j + 1][0] <= d:
            j += 1
        if j < 0:
            continue
        r = fx[j][1]
        out.append((d, o / r, h / r, lo / r, c / r, v))
    return out


def splice(listing: list[Row], twin: list[Row]) -> list[Row]:
    """Twin rows before the listing's first day, scaled to the listing's first close."""
    first = listing[0][0]
    before = [r for r in twin if r[0] < first]
    at = [r for r in twin if r[0] <= first]
    if not at:
        return listing
    k = listing[0][4] / at[-1][4]
    scaled = [(d, o * k, h * k, lo * k, c * k, v) for d, o, h, lo, c, v in before]
    return scaled + listing


# Yahoo's first bars of these Xetra lines are not EUR prices: both fall ~25% on 2010-11-01,
# the day's USD/EUR rate, on near-zero volume. They start on that day (research/eu-1.md).
TRIM = {"SXR8": date(2010, 11, 1), "SXRV": date(2010, 11, 1)}

# UCITS listing -> its twin (a US ETF or a coin, converted to EUR) for the spliced series.
SPLICE = {"SXR8": "SPY", "SXRV": "QQQ", "4GLD": "GLD", "IBGL": "TLT"}
TWINS_EUR = ["SPY", "QQQ", "GLD", "TLT", "EEM", "EFA", "IEF", "DBC", "BTC", "ETH"]


def build() -> None:
    raw = newest_raw()
    print("raw folder", raw.name)
    for sym, ticker in UCITS.items():
        path = raw / "yahoo" / f"{ticker}.json"
        if not path.exists():
            print("missing", sym)
            continue
        cur, rows, adj = parse_yahoo(json.loads(path.read_bytes()))
        if cur != "EUR":
            print("skip (not EUR)", sym, cur)
            continue
        if sym in TRIM:
            rows = [r for r in rows if r[0] >= TRIM[sym]]
            adj = [r for r in adj if r[0] >= TRIM[sym]]
        write_rows(DATA / "bars" / f"{sym}.csv", rows)
        write_rows(DATA / "adj" / f"{sym}.csv", adj)
        print(sym, cur, len(rows), rows[0][0], flush=True)
    fx = usd_per_eur(raw)
    print("USD per EUR", fx[0], len(fx))
    for s in TWINS_EUR:
        for kind in ("bars", "adj"):
            src = DATA / kind / f"{s}.csv"
            if src.exists():
                write_rows(DATA / kind / f"{s}-EUR.csv", to_eur(read_rows(src), fx))
    for sym, twin in SPLICE.items():
        for kind in ("bars", "adj"):
            listing = DATA / kind / f"{sym}.csv"
            tw = DATA / kind / f"{twin}-EUR.csv"
            if listing.exists() and tw.exists():
                write_rows(DATA / kind / f"{sym}-S.csv", splice(read_rows(listing), read_rows(tw)))


if __name__ == "__main__":
    if sys.argv[1] == "fetch-fx":  # the ECB rate alone, into today's raw folder
        fetch(fx_only=True)
    else:
        {"fetch": fetch, "build": build}[sys.argv[1]]()
