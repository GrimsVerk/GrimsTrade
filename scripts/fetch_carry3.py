"""Downloads for research run carry-3 (card in research/carry-3.md). Resumable, write-once.

    uv run python -I scripts/fetch_carry3.py book [name]          # one order-book snapshot
    uv run python -I scripts/fetch_carry3.py book3 <prefix>       # the card's three, 61 min apart
    uv run python -I scripts/fetch_carry3.py heldout binance|bybit|hyperliquid

Everything is written under `<cache_root>/carry-3/` only (files and `manifest.jsonl`); the
train downloads of carry-2 are read, never touched.

`book`: today's public order books and 24-hour volumes of every live USDT/USD perpetual on
Binance USDT-M, Bybit linear and Hyperliquid, for calibrating the cost model only (the card
takes three snapshots at least an hour apart). Saved under `carry-3/book/<name>/`.

`heldout`: bars and funding for 2025-11-11 .. 2026-11-10, under `carry-3/heldout/` (kept out of
the shared venue folders so no other loader can pick them up). **Run it only after the card's
train bar passed** (the card: if train fails the held-out bars are not even downloaded).
Loaders read these files only through `carry3.py --heldout`, which is guarded.

Keyless public market-data endpoints only; nothing here can reach an account. Downloaded files
are data: parsed as CSV/JSON, never run. Never commit them. Helpers come from
`scripts/fetch_carry2.py` (imported, not edited).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import threading
import time
import urllib.error
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_carry2 as f2  # noqa: E402
from fetch_carry2 import BVIS, BYBIT, HL, ROOT, SAFE, http, pool  # noqa: E402

f2.UA = "research-client/0.1 (python urllib)"  # generic client name for every request here
MINE = ROOT / "carry-3"  # the only folder this script writes to
FAPI = "https://fapi.binance.com/fapi/v1/"
HELD_FROM_MS = int(datetime(2025, 11, 11, tzinfo=UTC).timestamp() * 1000)
HELD_END_MS = int(datetime(2026, 11, 11, tzinfo=UTC).timestamp() * 1000)  # exclusive
BN_TRAIN = ROOT / "binance" / "futures" / "um" / "monthly"
BY_TRAIN = ROOT / "bybit" / "linear" / "to-2025-11-10"
HL_TRAIN = ROOT / "hyperliquid" / "perp" / "to-2025-11-10"
_lock = threading.Lock()


def save(rel: str, url: str, body: bytes) -> None:
    """Write-once under `carry-3/`, with a line in `carry-3/manifest.jsonl`."""
    dst = MINE / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".part")
    tmp.write_bytes(body)
    os.replace(tmp, dst)
    line = {
        "bytes": len(body),
        "fetched_at": _now(),
        "path": f"carry-3/{rel}",
        "sha256": hashlib.sha256(body).hexdigest(),
        "url": url,
    }
    with _lock, (MINE / "manifest.jsonl").open("a") as f:
        f.write(json.dumps(line, sort_keys=True) + "\n")


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- order-book snapshots


def book_binance(base: str) -> None:
    info = json.loads(http(FAPI + "exchangeInfo"))
    syms = sorted(
        s["symbol"]
        for s in info["symbols"]
        if s.get("contractType") == "PERPETUAL"
        and s.get("quoteAsset") == "USDT"
        and s.get("status") == "TRADING"
        and SAFE.match(s["symbol"])
    )
    save(f"{base}/binance/symbols.json", FAPI + "exchangeInfo", json.dumps(syms).encode())
    save(f"{base}/binance/ticker24h.json", FAPI + "ticker/24hr", http(FAPI + "ticker/24hr"))

    def one(sym: str) -> None:
        rel = f"{base}/binance/depth/{sym}.json"
        if not (MINE / rel).exists():
            url = FAPI + f"depth?symbol={sym}&limit=500"
            save(rel, url, http(url))
            time.sleep(0.35)  # weight 10 a call, limit 2400 a minute

    print(f"book binance: {len(syms)} perps", flush=True)
    pool(one, syms, 1)


def book_bybit(base: str) -> None:
    url = BYBIT + "tickers?category=linear"
    body = http(url)
    save(f"{base}/bybit/tickers.json", url, body)
    syms = sorted(
        x["symbol"]
        for x in json.loads(body)["result"]["list"]
        if x["symbol"].endswith("USDT") and SAFE.match(x["symbol"])
    )

    def one(sym: str) -> None:
        rel = f"{base}/bybit/orderbook/{sym}.json"
        if not (MINE / rel).exists():
            u = BYBIT + f"orderbook?category=linear&symbol={sym}&limit=200"
            save(rel, u, http(u))
            time.sleep(0.25)

    print(f"book bybit: {len(syms)} perps", flush=True)
    pool(one, syms, 1)


def book_hyperliquid(base: str) -> None:
    body = http(HL, {"type": "metaAndAssetCtxs"})
    save(f"{base}/hyperliquid/metaAndAssetCtxs.json", HL + " metaAndAssetCtxs", body)
    meta = json.loads(body)[0]
    coins = [
        u["name"] for u in meta["universe"] if not u.get("isDelisted") and SAFE.match(u["name"])
    ]

    def one(coin: str) -> None:
        rel = f"{base}/hyperliquid/l2Book/{coin}.json"
        if not (MINE / rel).exists():
            save(rel, HL + f" l2Book {coin}", http(HL, {"type": "l2Book", "coin": coin}))
            time.sleep(0.5)

    print(f"book hyperliquid: {len(coins)} perps", flush=True)
    pool(one, coins, 1)


def book(name: str) -> None:
    base = f"book/{name}"
    started = _now()

    def run(fn: object) -> None:
        try:
            fn(base)  # type: ignore[operator]
        except Exception as e:  # noqa: BLE001  (the card has a fallback for a missing venue)
            print(f"FAIL {fn.__name__}: {e}", flush=True)  # type: ignore[attr-defined]

    with ThreadPoolExecutor(3) as ex:  # the three venues at the same time
        list(ex.map(run, (book_binance, book_bybit, book_hyperliquid)))
    done = {"started": started, "finished": _now()}
    save(f"{base}/done.json", "local", json.dumps(done).encode())


def book3(prefix: str) -> None:
    """The card's three snapshots `<prefix>-s1..3`, starts at least 61 minutes apart. A snapshot
    that is already complete is kept, and the next one waits 61 minutes from its start."""
    last = 0.0
    for k in (1, 2, 3):
        name = f"{prefix}-s{k}"
        done = MINE / "book" / name / "done.json"
        if done.exists():
            started = json.loads(done.read_text())["started"]
            last = datetime.strptime(started, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).timestamp()
            continue
        wait = last + 3660 - time.time()
        if wait > 0:
            time.sleep(wait)
        last = time.time()
        book(name)
        print(f"snapshot {k} done", flush=True)


# ---------------------------------------------------------------- held-out year: Binance


def _bn_fetch_dir(prefix: str, first_month: str) -> None:
    """Monthly archive zips under `prefix` from `first_month` to 2026-10, into carry-3/heldout."""
    for key in f2.s3_list(prefix, False):
        m = re.search(r"(\d{4}-\d{2})\.zip$", key)
        if not m or not first_month <= m.group(1) <= "2026-10":
            continue
        rel = "heldout/binance/" + key.removeprefix("data/futures/um/")
        if not (MINE / rel).exists():
            save(rel, BVIS + key, http(BVIS + key))
            time.sleep(0.1)


def _bn_daily_klines(sym: str) -> None:
    """Archive daily files for 2026-11-01 .. 2026-11-10 (the month has no monthly file yet)."""
    d = date(2026, 11, 1)
    while d <= date(2026, 11, 10):
        key = f"data/futures/um/daily/klines/{sym}/1d/{sym}-1d-{d}.zip"
        rel = "heldout/binance/" + key.removeprefix("data/futures/um/")
        if not (MINE / rel).exists():
            try:
                save(rel, BVIS + key, http(BVIS + key))
            except urllib.error.HTTPError:
                return  # 404: the contract stopped trading (later days are missing too)
            time.sleep(0.05)
        d += timedelta(days=1)


def _bn_vol_ok(sym: str) -> bool:
    held = MINE / "heldout" / "binance"
    paths = sorted((BN_TRAIN / "klines" / sym / "1d").glob("*.zip"))
    paths += sorted((held / "monthly" / "klines" / sym / "1d").glob("*.zip"))
    paths += sorted((held / "daily" / "klines" / sym / "1d").glob("*.zip"))
    rows = []
    for p in paths:
        with zipfile.ZipFile(p) as z:
            for ln in z.read(z.namelist()[0]).decode().splitlines():
                f = ln.split(",")
                if f[0].isdigit():
                    t = float(f[0])
                    rows.append((t / 1000 if t > 1e14 else t, float(f[7])))
    if len(rows) < 30:
        return False
    a = np.array(sorted(set(rows)))
    med = np.median(np.lib.stride_tricks.sliding_window_view(a[:, 1], 30), axis=1)
    return bool((med >= f2.MIN_VOL).any())


def _bn_rest_funding(sym: str) -> None:
    """Funding events of 2026-11-01 .. 2026-11-10 (not in the monthly archive yet)."""
    rel = f"heldout/binance/rest/fundingRate-2026-11/{sym}.json"
    if (MINE / rel).exists():
        return
    start = int(datetime(2026, 11, 1, tzinfo=UTC).timestamp() * 1000)
    out: list[dict[str, object]] = []
    while start < HELD_END_MS:
        url = FAPI + (
            f"fundingRate?symbol={sym}&startTime={start}&endTime={HELD_END_MS - 1}&limit=1000"
        )
        try:
            got = json.loads(http(url, tries=2))
        except (RuntimeError, urllib.error.HTTPError):
            got = []  # delisted symbols are not served: no events
        time.sleep(0.7)  # 500 requests per 5 minutes
        out += got
        if len(got) < 1000:
            break
        start = max(int(g["fundingTime"]) for g in got) + 1
    save(rel, FAPI + f"fundingRate?symbol={sym}", json.dumps(out).encode())


def bn_one(sym: str) -> None:
    if not SAFE.match(sym):
        return
    _bn_fetch_dir(f"data/futures/um/monthly/klines/{sym}/1d/", "2025-12")
    _bn_daily_klines(sym)
    if not _bn_vol_ok(sym):
        return
    # train already holds funding to 2025-11 for coins that passed its pre-filter; a coin that
    # first passes in the held-out year needs all its funding
    had = (BN_TRAIN / "fundingRate" / sym).exists()
    _bn_fetch_dir(f"data/futures/um/monthly/fundingRate/{sym}/", "2025-12" if had else "2019-01")
    _bn_rest_funding(sym)


def heldout_binance() -> None:
    root = BN_TRAIN / "klines"
    syms = sorted(p.name for p in root.iterdir() if p.name.endswith("USDT") and "_" not in p.name)
    print(f"heldout binance: {len(syms)} symbols with train klines", flush=True)
    pool(bn_one, syms, 6)


# ---------------------------------------------------------------- held-out year: Bybit


def _by_get(path: str) -> dict[str, object]:
    x = json.loads(http(BYBIT + path))
    time.sleep(0.4)
    return x  # type: ignore[no-any-return]


def _by_funding(sym: str, start_ms: int, end_ms: int) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    end = end_ms - 1
    while end >= start_ms:
        x = _by_get(
            f"funding/history?category=linear&symbol={sym}&startTime={start_ms}"
            f"&endTime={end}&limit=200"
        )
        got = x["result"]["list"]  # type: ignore[index]
        out += got
        if len(got) < 200:
            break
        end = min(int(g["fundingRateTimestamp"]) for g in got) - 1
    return out


def by_one(sym: str) -> None:
    if not SAFE.match(sym):
        return
    train = BY_TRAIN / sym
    if not (train / "kline-D.json").exists():
        return  # no train bars: cannot have 365 days of history inside the held-out year
    base = f"heldout/bybit/{sym}"
    rel = f"{base}/kline-D.json"
    if not (MINE / rel).exists():
        x = _by_get(
            f"kline?category=linear&symbol={sym}&interval=D&start={HELD_FROM_MS}"
            f"&end={HELD_END_MS - 1}&limit=1000"
        )
        if x.get("retCode") != 0:
            return
        url = BYBIT + f"kline?category=linear&symbol={sym}&interval=D"
        save(rel, url, json.dumps(x["result"]["list"]).encode())  # type: ignore[index]
    rows = json.loads((train / "kline-D.json").read_text()) + json.loads((MINE / rel).read_text())
    if len(rows) < 30:
        return
    a = np.array(sorted({(float(r[0]), float(r[6])) for r in rows}))
    med = np.median(np.lib.stride_tricks.sliding_window_view(a[:, 1], 30), axis=1)
    if not (med >= f2.MIN_VOL).any():
        return
    rel = f"{base}/funding.json"
    if not (MINE / rel).exists():
        # all history if train has none (the coin first passed the pre-filter after train)
        start = HELD_FROM_MS if (train / "funding.json").exists() else f2.START_MS
        out = _by_funding(sym, start, HELD_END_MS)
        url = BYBIT + f"funding/history?category=linear&symbol={sym}"
        save(rel, url, json.dumps(out).encode())


def heldout_bybit() -> None:
    syms = sorted(p.name for p in BY_TRAIN.iterdir())
    print(f"heldout bybit: {len(syms)} symbols with train klines", flush=True)
    pool(by_one, syms, 2)


# ---------------------------------------------------------------- held-out year: Hyperliquid


def _hl_post(body: dict[str, object]) -> object:
    x = json.loads(http(HL, body))
    time.sleep(1.5)
    return x


def hl_one(coin: str) -> None:
    if not SAFE.match(coin):
        return
    train = HL_TRAIN / coin
    if not (train / "candles-1d.json").exists():
        return
    base = f"heldout/hyperliquid/{coin}"
    rel = f"{base}/candles-1d.json"
    if not (MINE / rel).exists():
        req = {
            "coin": coin,
            "interval": "1d",
            "startTime": HELD_FROM_MS,
            "endTime": HELD_END_MS - 1,
        }
        rows = _hl_post({"type": "candleSnapshot", "req": req})
        save(rel, HL + f" candleSnapshot {coin} 1d", json.dumps(rows).encode())
    rows = json.loads((train / "candles-1d.json").read_text()) + json.loads(
        (MINE / rel).read_text()
    )
    if len(rows) < 30:
        return
    a = np.array(sorted({(float(r["t"]), float(r["v"]) * float(r["c"])) for r in rows}))
    first = float(a[:, 0].min())
    med = np.median(np.lib.stride_tricks.sliding_window_view(a[:, 1], 30), axis=1)
    if not (med[a[29:, 0] >= first + 365 * 86400_000] >= f2.MIN_VOL).any():
        return
    rel = f"{base}/funding.json"
    if (MINE / rel).exists():
        return
    # train funding starts at the coin's day 350; continue from the train cut, or from day 350
    # if train fetched none (the coin first passed the pre-filter after train)
    t = HELD_FROM_MS if (train / "funding.json").exists() else int(first) + 350 * 86400_000
    out: list[dict[str, object]] = []
    while t < HELD_END_MS:
        got = _hl_post(
            {"type": "fundingHistory", "coin": coin, "startTime": t, "endTime": HELD_END_MS - 1}
        )
        if not got:
            break
        out += got  # type: ignore[arg-type]
        last = max(int(g["time"]) for g in got)  # type: ignore[index, union-attr]
        if len(got) < 500:  # type: ignore[arg-type]
            break
        t = last + 1
    save(rel, HL + f" fundingHistory {coin}", json.dumps(out).encode())


def heldout_hyperliquid() -> None:
    coins = sorted(p.name for p in HL_TRAIN.iterdir())
    print(f"heldout hyperliquid: {len(coins)} coins with train candles", flush=True)
    pool(hl_one, coins, 1)


if __name__ == "__main__":
    if sys.argv[1] == "book":
        book(sys.argv[2] if len(sys.argv) > 2 else _now().replace(":", ""))
    elif sys.argv[1] == "book3":
        book3(sys.argv[2])
    elif sys.argv[1] == "heldout":
        {
            "binance": heldout_binance,
            "bybit": heldout_bybit,
            "hyperliquid": heldout_hyperliquid,
        }[sys.argv[2]]()
    else:
        raise SystemExit(__doc__)
    print("done", flush=True)
