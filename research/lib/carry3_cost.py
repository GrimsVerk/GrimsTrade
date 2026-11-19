"""Cost model of research run carry-3 (card in research/carry-3.md). Kept free of `harness` so
tests can import it.

Cost per side, as a fraction of the traded value, for a trade of `Q` USD:

    cost = taker_fee + m x stress x [ half_spread(ADV) + vol x sqrt(Q / ADV) ]

Fees are the venues' published lowest tier (checked 2026-11-17). The half-spread curve is fitted
on public order-book snapshots of today's book (`scripts/fetch_carry3.py book3`), which are read
here as JSON and never run.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np

# venue -> (maker, taker), lowest tier, no discounts (card)
FEES = {
    "binance": (0.00020, 0.00050),
    "bybit": (0.00020, 0.00055),
    "hyperliquid": (0.00015, 0.00045),
}
MIN_ORDER_USD = 10.0
ADV_FLOOR = 1e6  # the calibration's lower volume bound; a missing ADV is priced as this
FIT_MIN_VOL = 1e6
CHECK_MIN_VOL = 5e6
CHECK_SIZES = (300.0, 10_000.0)
MAKER_SHARE = 0.6


@dataclass(frozen=True)
class SpreadFit:
    """log(half-spread in bps) = a + b x log(ADV), ADV clipped to [lo, hi] USD."""

    a: float
    b: float
    lo: float
    hi: float

    def half_spread(self, adv: np.ndarray) -> np.ndarray:
        x = np.clip(np.nan_to_num(adv, nan=self.lo), self.lo, self.hi)
        bps = np.exp(self.a + self.b * np.log(x))
        out: np.ndarray = np.clip(bps, 0.1, 100.0) / 1e4
        return out


@dataclass(frozen=True)
class CostModel:
    venue: str
    fit: SpreadFit | None
    m: float = 1.0  # the card's book check (never below 1)
    stress: float = 1.0  # robustness: spread and impact multiplied
    account: float = 10_000.0
    maker_share: float = 0.0  # robustness: share of every trade filled as maker
    flat: float | None = None  # carry-2's flat cost per side instead of the model

    def parts(self, dw: np.ndarray, adv: np.ndarray, vol: np.ndarray, share: float) -> np.ndarray:
        """Cost of trading `dw` (weight changes, fractions of equity) as fractions of equity:
        [fee, spread, impact]. `share` = the venue's share of the account."""
        a = np.abs(dw)
        if self.flat is not None:
            return np.array([float(a.sum() * self.flat), 0.0, 0.0])
        if self.fit is None:
            raise ValueError("a model without a flat cost needs a spread fit")
        maker, taker = FEES[self.venue]
        q = a * self.account * share
        adv_eff = np.maximum(np.nan_to_num(adv, nan=ADV_FLOOR), ADV_FLOOR)
        k = self.m * self.stress * (1 - self.maker_share)
        fee = self.maker_share * maker + (1 - self.maker_share) * taker
        spread = k * self.fit.half_spread(adv_eff)
        impact = k * np.nan_to_num(vol) * np.sqrt(q / adv_eff)
        return np.array(
            [float(a.sum() * fee), float((a * spread).sum()), float((a * impact).sum())]
        )

    def per_side(self, q_usd: float, adv: float, vol: float) -> float:
        """Cost per side (fraction) of one trade of `q_usd`: for tables and tests."""
        if q_usd <= 0:
            return 0.0
        w = q_usd / self.account
        return float(self.parts(np.array([w]), np.array([adv]), np.array([vol]), 1.0).sum() / w)

    def min_dw(self, share: float) -> float:
        """Smallest weight change that is a tradable order (0 for flat-cost reference rows)."""
        return 0.0 if self.flat is not None else MIN_ORDER_USD / (self.account * share)

    def but(self, **kw: Any) -> CostModel:
        return replace(self, **kw)


# ---------------------------------------------------------------- order-book snapshots


def walk(levels: list[tuple[float, float]], q_usd: float) -> float | None:
    """Average price of a market order of `q_usd` against `levels` (price, size) from the best
    outwards; None if the visible book is too thin."""
    left = q_usd
    units = 0.0
    for p, s in levels:
        take = min(left, p * s)
        units += take / p
        left -= take
        if left <= 1e-9:
            return q_usd / units
    return None


def measure(bids: list[tuple[float, float]], asks: list[tuple[float, float]]) -> dict[str, float]:
    """Quoted half-spread and the measured cost of market orders, as fractions of the mid."""
    if not bids or not asks:
        return {}
    mid = (bids[0][0] + asks[0][0]) / 2
    if mid <= 0 or asks[0][0] <= bids[0][0]:
        return {}
    out = {"hs": (asks[0][0] - bids[0][0]) / (2 * mid)}
    for q in CHECK_SIZES:
        b, a = walk(bids, q), walk(asks, q)
        if b is not None and a is not None:
            out[f"slip{q:.0f}"] = ((mid - b) + (a - mid)) / (2 * mid)
    return out


def _levels(rows: list[Any]) -> list[tuple[float, float]]:
    return [(float(r[0]), float(r[1])) for r in rows]


def read_snapshot(folder: Path) -> dict[str, dict[str, dict[str, float]]]:
    """One snapshot folder -> venue -> symbol -> {vol24, hs, slip300, slip10000}."""
    out: dict[str, dict[str, dict[str, float]]] = {"binance": {}, "bybit": {}, "hyperliquid": {}}
    b = folder / "binance"
    if (b / "ticker24h.json").exists():
        vol = {
            x["symbol"]: float(x["quoteVolume"])
            for x in json.loads((b / "ticker24h.json").read_text())
        }
        for p in sorted((b / "depth").glob("*.json")):
            d = json.loads(p.read_text())
            m = measure(_levels(d.get("bids", [])), _levels(d.get("asks", [])))
            if m and p.stem in vol:
                out["binance"][p.stem] = m | {"vol24": vol[p.stem]}
    b = folder / "bybit"
    if (b / "tickers.json").exists():
        rows = json.loads((b / "tickers.json").read_text())["result"]["list"]
        vol = {x["symbol"]: float(x["turnover24h"] or 0) for x in rows}
        for p in sorted((b / "orderbook").glob("*.json")):
            d = json.loads(p.read_text()).get("result") or {}
            m = measure(_levels(d.get("b", [])), _levels(d.get("a", [])))
            if m and p.stem in vol:
                out["bybit"][p.stem] = m | {"vol24": vol[p.stem]}
    b = folder / "hyperliquid"
    if (b / "metaAndAssetCtxs.json").exists():
        meta, ctxs = json.loads((b / "metaAndAssetCtxs.json").read_text())
        vol = {
            u["name"]: float(c.get("dayNtlVlm") or 0)
            for u, c in zip(meta["universe"], ctxs, strict=True)
        }
        for p in sorted((b / "l2Book").glob("*.json")):
            d = json.loads(p.read_text())
            lv = d.get("levels") or [[], []]
            bids = [(float(x["px"]), float(x["sz"])) for x in lv[0]]
            asks = [(float(x["px"]), float(x["sz"])) for x in lv[1]]
            m = measure(bids, asks)
            if m and p.stem in vol:
                out["hyperliquid"][p.stem] = m | {"vol24": vol[p.stem]}
    return out


def median_snapshots(
    snaps: list[dict[str, dict[str, dict[str, float]]]],
) -> dict[str, dict[str, dict[str, float]]]:
    """Per venue and symbol, the median over snapshots of every measured field."""
    out: dict[str, dict[str, dict[str, float]]] = {}
    for venue in ("binance", "bybit", "hyperliquid"):
        syms = sorted(set().union(*(s[venue].keys() for s in snaps)))
        out[venue] = {}
        for sym in syms:
            rows = [s[venue][sym] for s in snaps if sym in s[venue]]
            keys = sorted(set().union(*(r.keys() for r in rows)))
            out[venue][sym] = {
                k: float(np.median([r[k] for r in rows if k in r])) for k in keys
            } | {"n_slip10000": float(sum("slip10000" in r for r in rows)), "n": float(len(rows))}
    return out


def fit_spread(vol24: np.ndarray, hs: np.ndarray) -> SpreadFit | None:
    """Least squares of log half-spread (bps) on log 24-hour volume, coins >= FIT_MIN_VOL."""
    k = (vol24 >= FIT_MIN_VOL) & (hs > 0)
    if k.sum() < 30:
        return None
    x, y = np.log(vol24[k]), np.log(hs[k] * 1e4)
    b, a = np.polyfit(x, y, 1)
    return SpreadFit(float(a), float(b), float(vol24[k].min()), float(vol24[k].max()))


def calibrate(
    book: dict[str, dict[str, dict[str, float]]], vols: dict[str, dict[str, float]]
) -> dict[str, dict[str, Any]]:
    """The card's calibration. `book`: median_snapshots(); `vols`: venue -> symbol -> daily vol
    (the venue's median under the key "" for coins without one). Returns per venue the fit, the
    book check ratios and the multiplier `m`."""
    arr = {
        v: (
            np.array([r["vol24"] for r in rows.values()]),
            np.array([r["hs"] for r in rows.values()]),
        )
        for v, rows in book.items()
    }
    own = {v: fit_spread(*arr[v]) if len(arr[v][0]) else None for v in book}
    out: dict[str, dict[str, Any]] = {}
    for v, rows in book.items():
        fit, source = own[v], "own"
        if fit is None or fit.b > 0:
            others = [u for u in book if u != v and len(arr[u][0])]
            fit = fit_spread(
                np.concatenate([arr[u][0] for u in others]),
                np.concatenate([arr[u][1] for u in others]),
            )
            source = "other venues (card fallback)"
        if fit is None:
            raise RuntimeError(f"no spread fit possible for {v}")
        cm = CostModel(v, fit)
        ratios: dict[str, float] = {}
        counts: dict[str, int] = {}
        for q in CHECK_SIZES:
            rr = []
            thin = 0
            for sym, r in rows.items():
                if r["vol24"] < CHECK_MIN_VOL:
                    continue
                key = f"slip{q:.0f}"
                if key not in r:
                    thin += 1
                    continue
                sigma = vols.get(v, {}).get(sym, vols.get(v, {}).get("", 0.0))
                model = cm.per_side(q, r["vol24"], sigma) - FEES[v][1]
                rr.append(r[key] / model)
            ratios[f"{q:.0f}"] = float(np.median(rr)) if rr else float("nan")
            counts[f"{q:.0f}"] = len(rr)
            counts[f"thin{q:.0f}"] = thin
        worst = max((x for x in ratios.values() if math.isfinite(x)), default=1.0)
        m = math.ceil(worst * 2) / 2 if worst > 1.5 else 1.0
        n_fit = int(((arr[v][0] >= FIT_MIN_VOL) & (arr[v][1] > 0)).sum())
        out[v] = {
            "a": fit.a,
            "b": fit.b,
            "lo": fit.lo,
            "hi": fit.hi,
            "source": source,
            "coins": len(rows),
            "coins_fit": n_fit,
            "check_ratio": ratios,
            "check_counts": counts,
            "m": m,
        }
    return out


def model_from(params: dict[str, Any], venue: str) -> CostModel:
    p = params[venue]
    return CostModel(venue, SpreadFit(p["a"], p["b"], p["lo"], p["hi"]), m=float(p["m"]))
