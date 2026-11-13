"""Download perpetual-futures history for research run carry-2 into the raw cache (resumable).

    uv run python -I scripts/fetch_carry2.py binance|bybit|hyperliquid

Cache root from `cache_root` in the git-ignored `research/macro.local.json` (copy the
`.example`). Every file is written once (temp file + rename); a rerun skips files already there.
One line per new file is appended to `<root>/manifest.jsonl` (path, fetched_at, url, bytes,
sha256), as ingest-1 does. Train data only: nothing after 2025-11-10 is requested, except that
Binance's monthly 2025-11 files hold the whole month (loaders cut at the train bar).
Downloaded files are data: parsed as CSV/JSON, never run. Never commit them.

Venues (keyless public market-data endpoints only; nothing here can reach an account):
- Binance USDT-M archive (data.binance.vision, keeps delisted contracts): 1d klines for every
  `*USDT` perpetual; funding and 1h premium index for those whose 30-day median quote volume
  ever reached 5M USD (the card's pre-filter).
- Bybit v5 linear: live symbols from instruments-info plus Binance's archive names (delisted
  contracts answer if Bybit still serves them); daily klines; funding and 1h premium index
  after the same pre-filter.
- Hyperliquid info endpoint: every perp in `meta` (delisted ones included), daily candles;
  hourly funding (with premium) after the pre-filter (volume = coin volume x close).
- Not fetched: OKX (public funding history covers only the last 3 months, checked
  2026-11-13), Bitget and dYdX (left out for the time budget).
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
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

UA = "grimstrade-research/0.1 (personal non-commercial research; python urllib)"
END_MS = int(datetime(2025, 11, 11, tzinfo=UTC).timestamp() * 1000)  # exclusive
START_MS = int(datetime(2019, 9, 1, tzinfo=UTC).timestamp() * 1000)
TODAY = datetime.now(UTC).date().isoformat()
MIN_VOL = 5e6
S3 = "https://s3-ap-northeast-1.amazonaws.com/data.binance.vision"
BVIS = "https://data.binance.vision/"
BYBIT = "https://api.bybit.com/v5/market/"
HL = "https://api.hyperliquid.xyz/info"
SAFE = re.compile(r"^[A-Za-z0-9]{1,40}$")
_lock = threading.Lock()


def cache_root() -> Path:
    cfg = Path(__file__).resolve().parents[1] / "research" / "macro.local.json"
    return Path(json.loads(cfg.read_text())["cache_root"]).expanduser()


ROOT = cache_root()


def http(url: str, body: dict[str, object] | None = None, tries: int = 4) -> bytes:
    data = None if body is None else json.dumps(body).encode()
    hdr = {"User-Agent": UA}
    if body is not None:
        hdr["Content-Type"] = "application/json"
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=hdr)
            with urllib.request.urlopen(req, timeout=60) as r:
                out = bytes(r.read())
            head = out[:512].lstrip().lower()
            if head.startswith(b"<!doctype html") or head.startswith(b"<html"):
                raise RuntimeError(f"HTML instead of data (bot check or login?): {url}")
            return out
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            if e.code in (403, 451):
                raise RuntimeError(f"refused {e.code} (skipped, not worked around): {url}") from e
            time.sleep(5 * 2**k)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(5 * 2**k)
    raise RuntimeError(f"gave up: {url}")


def save(rel: str, url: str, body: bytes) -> None:
    dst = ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".part")
    tmp.write_bytes(body)
    os.replace(tmp, dst)
    line = {
        "bytes": len(body),
        "fetched_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": rel,
        "sha256": hashlib.sha256(body).hexdigest(),
        "url": url,
    }
    with _lock, (ROOT / "manifest.jsonl").open("a") as f:
        f.write(json.dumps(line, sort_keys=True) + "\n")


def vol_ok(day_ms: np.ndarray, qv: np.ndarray, from_ms: float = 0) -> bool:
    """Did the 30-day median daily quote volume reach MIN_VOL on a train day >= from_ms?"""
    k = day_ms < END_MS
    order = np.argsort(day_ms[k])
    q, t = qv[k][order], day_ms[k][order]
    if len(q) < 30:
        return False
    med = np.median(np.lib.stride_tricks.sliding_window_view(q, 30), axis=1)
    return bool((med[t[29:] >= from_ms] >= MIN_VOL).any())


def pool(fn: object, items: list[str], workers: int) -> None:
    done = [0]

    def wrap(x: str) -> None:
        try:
            fn(x)  # type: ignore[operator]
        except Exception as e:  # noqa: BLE001  (log and keep going; a rerun retries)
            print(f"FAIL {x}: {e}", flush=True)
        with _lock:
            done[0] += 1
            if done[0] % 25 == 0:
                print(f"{done[0]}/{len(items)}", flush=True)

    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(wrap, items))


# ---------------------------------------------------------------- Binance archive


def s3_list(prefix: str, dirs: bool) -> list[str]:
    out: list[str] = []
    marker = ""
    while True:
        q = f"{S3}?delimiter=/&prefix={prefix}" + (f"&marker={marker}" if marker else "")
        x = http(q).decode()
        tag = "Prefix" if dirs else "Key"
        found = re.findall(rf"<{tag}>([^<]*)</{tag}>", x)
        found = [f for f in found if f != prefix]
        out += found
        time.sleep(0.3)
        if "<IsTruncated>true</IsTruncated>" not in x or not found:
            return out
        marker = re.findall(r"<NextMarker>([^<]*)</NextMarker>", x)
        marker = marker[0] if marker else found[-1]


def bn_symbols() -> list[str]:
    rel = f"binance/futures/um/listing/{TODAY}/fundingRate-symbols.json"
    if (ROOT / rel).exists():
        return list(json.loads((ROOT / rel).read_text()))
    pre = s3_list("data/futures/um/monthly/fundingRate/", True)
    syms = sorted({p.rstrip("/").split("/")[-1] for p in pre})
    save(rel, S3 + "?prefix=data/futures/um/monthly/fundingRate/", json.dumps(syms).encode())
    return syms


def bn_month_ok(key: str) -> bool:
    m = re.search(r"(\d{4})-(\d{2})\.zip$", key)
    return bool(m) and (m.group(1), m.group(2)) <= ("2025", "11")


def bn_fetch_dir(prefix: str) -> list[Path]:
    """Every monthly zip under `prefix` up to 2025-11, write-once."""
    paths = []
    for key in s3_list(prefix, False):
        if not key.endswith(".zip") or not bn_month_ok(key):
            continue
        rel = "binance/" + key.removeprefix("data/")
        if not (ROOT / rel).exists():
            save(rel, BVIS + key, http(BVIS + key))
            time.sleep(0.1)
        paths.append(ROOT / rel)
    return paths


def bn_kline_vol(paths: list[Path]) -> bool:
    rows = []
    for p in paths:
        with zipfile.ZipFile(p) as z:
            for ln in z.read(z.namelist()[0]).decode().splitlines():
                f = ln.split(",")
                if f[0].isdigit():
                    rows.append((float(f[0]), float(f[7])))
    if not rows:
        return False
    a = np.array(rows)
    return vol_ok(a[:, 0], a[:, 1])


def bn_one(sym: str) -> None:
    if not SAFE.match(sym):
        return
    kl = bn_fetch_dir(f"data/futures/um/monthly/klines/{sym}/1d/")
    if not bn_kline_vol(kl):
        return
    bn_fetch_dir(f"data/futures/um/monthly/fundingRate/{sym}/")
    bn_fetch_dir(f"data/futures/um/monthly/premiumIndexKlines/{sym}/1h/")


def binance() -> None:
    syms = [s for s in bn_symbols() if s.endswith("USDT") and "_" not in s]
    print(f"binance: {len(syms)} USDT perps in the archive", flush=True)
    pool(bn_one, syms, 10)  # a CDN of static files: ~10-15 requests a second


# ---------------------------------------------------------------- Bybit


def by_get(path: str) -> dict[str, object]:
    x = json.loads(http(BYBIT + path))
    time.sleep(0.4)
    return x  # type: ignore[no-any-return]


def by_pages(kind: str, sym: str, step_ms: int, extra: str, t0: int = START_MS) -> list[list[str]]:
    """Forward over fixed windows (klines, premium: rows are [start, ...])."""
    rows: list[list[str]] = []
    t = t0
    while t < END_MS:
        e = min(t + step_ms, END_MS) - 1
        x = by_get(f"{kind}?category=linear&symbol={sym}{extra}&start={t}&end={e}&limit=1000")
        if x.get("retCode") != 0:
            raise RuntimeError(f"bybit {kind} {sym}: {x.get('retMsg')}")
        rows += x["result"]["list"]  # type: ignore[index]
        t = e + 1
    return rows


def by_one(sym: str) -> None:
    if not SAFE.match(sym):
        return
    base = f"bybit/linear/to-2025-11-10/{sym}"
    rel = f"{base}/kline-D.json"
    if not (ROOT / rel).exists():
        x = by_get(f"kline?category=linear&symbol={sym}&interval=D&limit=2")
        if x.get("retCode") != 0 or not x["result"]["list"]:  # type: ignore[index]
            return  # Bybit does not serve this symbol
        rows = by_pages("kline", sym, 1000 * 86400_000, "&interval=D")
        save(
            rel, BYBIT + f"kline?category=linear&symbol={sym}&interval=D", json.dumps(rows).encode()
        )
    rows = json.loads((ROOT / rel).read_text())
    if not rows:
        return
    a = np.array([(float(r[0]), float(r[6])) for r in rows])  # start, turnover (USDT)
    if not vol_ok(a[:, 0], a[:, 1]):
        return
    rel = f"{base}/funding.json"
    if not (ROOT / rel).exists():
        out: list[dict[str, str]] = []
        end = END_MS - 1
        while True:
            x = by_get(f"funding/history?category=linear&symbol={sym}&endTime={end}&limit=200")
            got = x["result"]["list"]  # type: ignore[index]
            out += got
            if len(got) < 200:
                break
            end = min(int(g["fundingRateTimestamp"]) for g in got) - 1
        save(rel, BYBIT + f"funding/history?category=linear&symbol={sym}", json.dumps(out).encode())
    rel = f"{base}/premium-1h.json"
    if not (ROOT / rel).exists():
        first = int(a[:, 0].min()) // 86400_000 * 86400_000
        rows = by_pages("premium-index-price-kline", sym, 1000 * 3600_000, "&interval=60", first)
        url = BYBIT + f"premium-index-price-kline?category=linear&symbol={sym}&interval=60"
        save(rel, url, json.dumps(rows).encode())


def bybit() -> None:
    rel = f"bybit/linear/listing/{TODAY}/instruments.json"
    if not (ROOT / rel).exists():
        items: list[dict[str, str]] = []
        cur = ""
        while True:
            x = by_get(f"instruments-info?category=linear&limit=1000&cursor={cur}")
            items += x["result"]["list"]  # type: ignore[index]
            cur = x["result"].get("nextPageCursor", "")  # type: ignore[union-attr]
            if not cur:
                break
        save(rel, BYBIT + "instruments-info?category=linear", json.dumps(items).encode())
    items = json.loads((ROOT / rel).read_text())
    live = {
        i["symbol"]
        for i in items
        if i.get("contractType") == "LinearPerpetual" and i["symbol"].endswith("USDT")
    }
    bn = {s for s in bn_symbols() if s.endswith("USDT") and "_" not in s}
    syms = sorted(live | bn)
    print(f"bybit: {len(live)} live USDT perps, {len(syms)} names tried", flush=True)
    pool(by_one, syms, 2)


# ---------------------------------------------------------------- Hyperliquid


def hl_post(body: dict[str, object]) -> object:
    x = json.loads(http(HL, body))
    time.sleep(1.5)
    return x


def hl_one(coin: str) -> None:
    if not SAFE.match(coin):
        return
    base = f"hyperliquid/perp/to-2025-11-10/{coin}"
    rel = f"{base}/candles-1d.json"
    if not (ROOT / rel).exists():
        req = {"coin": coin, "interval": "1d", "startTime": START_MS, "endTime": END_MS - 1}
        rows = hl_post({"type": "candleSnapshot", "req": req})
        save(rel, HL + f" candleSnapshot {coin} 1d", json.dumps(rows).encode())
    rows = json.loads((ROOT / rel).read_text())
    if not rows:
        return
    a = np.array([(float(r["t"]), float(r["v"]) * float(r["c"])) for r in rows])
    # Hyperliquid's rate limit allows ~30 funding pages a minute, so only what the card can use:
    # a coin trades only after 365 days of bars, and its 7-day signal needs 7 days before that.
    first = float(a[:, 0].min())
    if not vol_ok(a[:, 0], a[:, 1], first + 365 * 86400_000):
        return
    rel = f"{base}/funding.json"
    if (ROOT / rel).exists():
        return
    out: list[dict[str, object]] = []
    t = int(first) + 350 * 86400_000
    while t < END_MS:
        got = hl_post(
            {"type": "fundingHistory", "coin": coin, "startTime": t, "endTime": END_MS - 1}
        )
        if not got:
            break
        out += got  # type: ignore[arg-type]
        last = max(int(g["time"]) for g in got)  # type: ignore[index, union-attr]
        if len(got) < 500:  # type: ignore[arg-type]
            break
        t = last + 1
    save(rel, HL + f" fundingHistory {coin}", json.dumps(out).encode())


def hyperliquid() -> None:
    rel = f"hyperliquid/listing/{TODAY}/meta.json"
    if not (ROOT / rel).exists():
        save(rel, HL + " meta", http(HL, {"type": "meta"}))
    meta = json.loads((ROOT / rel).read_text())
    coins = [u["name"] for u in meta["universe"]]
    print(f"hyperliquid: {len(coins)} perps in meta", flush=True)
    pool(hl_one, coins, 1)


if __name__ == "__main__":
    {"binance": binance, "bybit": bybit, "hyperliquid": hyperliquid}[sys.argv[1]]()
    print("done", flush=True)
