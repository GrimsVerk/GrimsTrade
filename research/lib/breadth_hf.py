"""Book C of research run breadth-1: hourly BTC/ETH (card in research/breadth-1.md).

    uv run python -I research/lib/breadth_hf.py [--log]

Hourly bars from `breadth_agg.py` (Bitstamp and Binance). Features at the close of hour h use
bars closed by h; a position decided at that close fills at the next hour's open (= that close)
and earns the following hour's return. Also the hourly cross-sectional screen of the 30
Binance pairs (IC only, with the break-even IC the costs imply).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_xs as xs  # noqa: E402
import macro  # noqa: E402
import stats  # noqa: E402
from breadth_books import log_row  # noqa: E402
from harness import TRAIN_END, TRIES  # noqa: E402

SERIES = {
    "btc-bitstamp": "bitstamp-btcusd-1h.npz",
    "btc-binance": "binance-BTCUSDT-1h.npz",
    "eth-bitstamp": "bitstamp-ethusd-1h.npz",
    "eth-binance": "binance-ETHUSDT-1h.npz",
}
FEATURES = ["r_1h", "r_4h", "r_24h", "r_168h", "vol_shock", "volu_shock", "hour_mean"]
HL = 720  # 30-day half-life in hours
END = int(datetime(TRAIN_END.year, TRAIN_END.month, TRAIN_END.day, 23, tzinfo=UTC).timestamp())


def derived() -> Path:
    return macro.cache_root() / "derived" / "breadth-1"


@dataclass
class Hourly:
    t: np.ndarray  # hour start (s)
    lc: np.ndarray  # log close
    v: np.ndarray  # quote volume


def load(name: str) -> Hourly:
    b = np.load(derived() / SERIES[name])
    t0, t1 = int(b["t"][0]), min(int(b["t"][-1]), END)
    t = np.arange(t0, t1 + 1, 3600)
    c = np.full(len(t), np.nan)
    v = np.zeros(len(t))
    i = (b["t"] - t0) // 3600
    k = i < len(t)
    c[i[k]] = b["c"][k]
    v[i[k]] = b["q"][k]
    c = xs.ffill(c[:, None])[:, 0]
    return Hourly(t, np.log(c), v)


def ewma_var(r: np.ndarray, hl: float) -> np.ndarray:
    lam = 0.5 ** (1 / hl)
    out = np.empty_like(r)
    v = r[:200].var()
    for i, x in enumerate(r):
        v = lam * v + (1 - lam) * x * x
        out[i] = v
    return out


def roll_sum(x: np.ndarray, w: int) -> np.ndarray:
    cs = np.r_[0.0, np.cumsum(x)]
    out = np.full(len(x), np.nan)
    out[w - 1 :] = cs[w:] - cs[:-w]
    return out


def features(h: Hourly) -> tuple[dict[str, np.ndarray], np.ndarray, np.ndarray, np.ndarray]:
    lc = h.lc
    r1 = np.r_[0.0, np.diff(lc)]
    var = ewma_var(r1, HL)
    vol = np.sqrt(var)
    vol[:HL] = np.nan  # a month of warm-up
    f: dict[str, np.ndarray] = {}
    for k in (1, 4, 24, 168):
        rk = np.full(len(lc), np.nan)
        rk[k:] = lc[k:] - lc[:-k]
        f[f"r_{k}h"] = np.clip(rk / (vol * np.sqrt(k)), -5, 5)
    with np.errstate(divide="ignore", invalid="ignore"):
        f["vol_shock"] = np.log(np.sqrt(roll_sum(r1 * r1, 24) / 24) / vol)
        v24 = roll_sum(h.v, 24)
        f["volu_shock"] = np.log(v24 / (roll_sum(h.v, HL) / 30))
    f["volu_shock"][~np.isfinite(f["volu_shock"])] = np.nan
    f["vol_shock"][~np.isfinite(f["vol_shock"])] = np.nan
    y1 = np.full(len(lc), np.nan)
    y1[:-1] = lc[1:] - lc[:-1]
    y24 = np.full(len(lc), np.nan)
    y24[:-24] = lc[24:] - lc[:-24]
    years = np.array([datetime.fromtimestamp(int(x), UTC).year for x in h.t])
    hod = (h.t // 3600) % 24
    hm = np.full(len(lc), np.nan)
    for y in np.unique(years)[1:]:
        past = (years < y) & np.isfinite(y1)
        means = np.array([y1[past & (hod == k)].mean() for k in range(24)])
        cur = years == y
        hm[cur] = means[hod[cur]] / np.nanmedian(vol[past])
    f["hour_mean"] = hm
    return f, y1, y24, vol


def spearman_nan(a: np.ndarray, b: np.ndarray) -> tuple[float, int]:
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 100:
        return float("nan"), int(m.sum())
    return xs.spearman(a[m], b[m]), int(m.sum())


def walk_forward(
    f: dict[str, np.ndarray], y24: np.ndarray, vol: np.ndarray, t: np.ndarray
) -> np.ndarray:
    """Forecast of the next-24h log return; OLS refitted each 1 January on earlier hours."""
    x = np.column_stack([f[k] for k in FEATURES])
    x = np.where(np.isfinite(x), x, 0.0)  # hour_mean is 0 (no seasonal view) in year one
    target = np.clip(y24 / (vol * np.sqrt(24)), -5, 5)
    years = np.array([datetime.fromtimestamp(int(s), UTC).year for s in t])
    fc = np.full(len(t), np.nan)
    first_year = years[0] + 2 + (1 if datetime.fromtimestamp(int(t[0]), UTC).month > 1 else 0)
    for y in range(first_year, years[-1] + 1):
        fit_t = datetime(y, 1, 1, tzinfo=UTC).timestamp()
        tr = (t + 24 * 3600 < fit_t) & np.isfinite(target) & np.isfinite(vol)
        cols = np.column_stack([np.ones(tr.sum()), x[tr]])
        beta, *_ = np.linalg.lstsq(cols, target[tr], rcond=None)
        cur = years == y
        fc[cur] = (np.column_stack([np.ones(cur.sum()), x[cur]]) @ beta) * vol[cur] * np.sqrt(24)
    return fc


def band_positions(fc: np.ndarray, b: float) -> np.ndarray:
    pos = np.zeros(len(fc))
    p = 0.0
    for i, v in enumerate(fc):
        if v > b:
            p = 1.0
        elif v < -b:
            p = 0.0
        pos[i] = p
    return pos


def daily_returns(t: np.ndarray, pos: np.ndarray, y1: np.ndarray, cost: float) -> np.ndarray:
    """Hourly P&L of holding `pos[i]` over hour i+1, costs on each change, compounded per UTC
    day."""
    r = np.nan_to_num(np.expm1(y1))
    prev = np.r_[0.0, pos[:-1]]
    hourly = (1 - cost * np.abs(pos - prev)) * (1 + pos * r) - 1
    day = (t - t[0]) // 86400
    lg = np.bincount(day, weights=np.log1p(hourly))
    out: np.ndarray = np.expm1(lg)
    return out


def tsmom_daily(h: Hourly) -> np.ndarray:
    """1 while the 365-day return at the last UTC midnight close is positive."""
    hod = (h.t // 3600) % 24
    out = np.zeros(len(h.t))
    cur = 0.0
    for i in range(len(h.t)):
        if hod[i] == 23 and i >= 365 * 24:  # the 23:00 bar closes at midnight
            cur = 1.0 if h.lc[i] > h.lc[i - 365 * 24] else 0.0
        out[i] = cur
    return out


def eras(t: np.ndarray, a: np.ndarray, b: np.ndarray) -> tuple[int, int]:
    days = t[0] // 86400 + np.arange(len(a))
    yrs = np.array([date.fromordinal(date(1970, 1, 1).toordinal() + int(d)).year for d in days])
    ahead = n = 0
    for y0, y1 in ((2010, 2016), (2017, 2021), (2022, 2025)):
        m = (yrs >= y0) & (yrs <= y1)
        if m.sum() >= 180:
            n += 1
            ahead += stats.sharpe(a[m]) > stats.sharpe(b[m])
    return ahead, n


def main() -> None:
    log = "--log" in sys.argv
    print("## IC (Spearman, whole span)\n")
    print("| Series | Feature | IC next 1h | IC next 24h | n days | chance 24h | chance 1h |")
    print("|---|---|---:|---:|---:|---:|---:|")
    res = {}
    for name in SERIES:
        h = load(name)
        f, y1, y24, vol = features(h)
        midnight = (h.t // 3600) % 24 == 23
        for k in FEATURES:
            ic1, n1 = spearman_nan(f[k], y1)
            ic24, nd = spearman_nan(f[k][midnight], y24[midnight])
            print(
                f"| {name} | `{k}` | {ic1:+.4f} | {ic24:+.3f} | {nd} | {1.96 / np.sqrt(nd):.3f}"
                f" | {1.96 / np.sqrt(n1):.4f} |",
                flush=True,
            )
            if log:
                first = datetime.fromtimestamp(int(h.t[0]), UTC).date()
                with TRIES.open("a") as fh:
                    fh.write(
                        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | breadth-1-hf | {name} {k} "
                        f"(IC 1h {ic1:+.4f}, 24h {ic24:+.3f}) | screen | train | {first} | "
                        f"{TRAIN_END} | - | - | - | - |\n"
                    )
        fc = walk_forward(f, y24, vol, h.t)
        start = int(np.argmax(np.isfinite(fc)))
        sl = slice(start, None)
        ts = tsmom_daily(h)
        res[name] = (h, f, y1, fc, ts, start)
        del sl
    print("\n## Rules (daily Sharpe, from the first walk-forward fit)\n")
    print(
        "| Series | From | Cost | Buy-hold | tsmom12 | hf-band | hf-band-ts | band - ts (p) | "
        "band-ts - ts (p) | Eras ahead (band-ts) | Trades/yr band | Max DD ts / band-ts |"
    )
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|")
    for cost in (0.003, 0.001):
        for name, (h, _f, y1, fc, ts, s) in res.items():
            t, y, f2, tsv = h.t[s:], y1[s:], fc[s:], ts[s:]
            bh = daily_returns(t, np.ones(len(t)), y, cost)
            tsr = daily_returns(t, tsv, y, cost)
            pos = band_positions(f2, 0.003)
            band = daily_returns(t, pos, y, cost)
            band_ts = daily_returns(t, pos * tsv, y, cost)
            d1, p1, _, _ = stats.sharpe_diff_boot(band, tsr)
            d2, p2, _, _ = stats.sharpe_diff_boot(band_ts, tsr)
            ah, ne = eras(t, band_ts, tsr)
            yrs = len(bh) / 365
            trades = np.abs(np.diff(pos)).sum() / yrs
            first = datetime.fromtimestamp(int(t[0]), UTC).date()
            print(
                f"| {name} | {first} | {cost * 1e4:.0f} bps | {stats.sharpe(bh):.2f} | "
                f"{stats.sharpe(tsr):.2f} | {stats.sharpe(band):.2f} | "
                f"{stats.sharpe(band_ts):.2f} | {d1:+.2f} ({p1:.2f}) | {d2:+.2f} ({p2:.2f}) | "
                f"{ah}/{ne} | {trades:.0f} | {stats.max_drawdown(tsr):.0%} / "
                f"{stats.max_drawdown(band_ts):.0%} |",
                flush=True,
            )
            if log:
                kind = "variant" if cost == 0.003 else "robustness"
                c = f"{cost * 1e4:.0f}bps"
                if cost == 0.003:
                    log_row("breadth-1-hf", f"{name} buy-hold", "baseline", first, bh, 0.0)
                    log_row("breadth-1-hf", f"{name} tsmom12 daily", "baseline", first, tsr, 0.0)
                log_row(
                    "breadth-1-hf",
                    f"{name} hf-band {c} (vs ts {d1:+.2f} p {p1:.2f})",
                    kind,
                    first,
                    band,
                    trades,
                )
                log_row(
                    "breadth-1-hf",
                    f"{name} hf-band-ts {c} (vs ts {d2:+.2f} p {p2:.2f})",
                    kind,
                    first,
                    band_ts,
                    trades,
                )
    xs_hourly_screen(log)


def xs_hourly_screen(log: bool) -> None:
    """Hourly IC of rev_1h and mom_24h across the 30 Binance pairs, with the break-even IC."""
    files = sorted(derived().glob("binance-*-1h.npz"))
    t0 = int(datetime(2020, 1, 1, tzinfo=UTC).timestamp())
    n = (END - t0) // 3600 + 1
    lc = np.full((n, len(files)), np.nan)
    for j, fp in enumerate(files):
        b = np.load(fp)
        i = (b["t"] - t0) // 3600
        k = (i >= 0) & (i < n)
        lc[i[k], j] = np.log(b["c"][k])
    nxt = np.full_like(lc, np.nan)
    nxt[:-1] = lc[1:] - lc[:-1]
    sigs = {
        "rev_1h": np.r_[np.full((1, lc.shape[1]), np.nan), -(lc[1:] - lc[:-1])],
        "mom_24h": np.r_[np.full((24, lc.shape[1]), np.nan), lc[24:] - lc[:-24]],
    }
    print("\n## Hourly cross-section, 30 Binance pairs, 2020-2025 (IC only)\n")
    print(
        "| Signal | mean IC | t | hours | cross-sectional sd of next hour | top-third renewed "
        "per hour | break-even IC at 30 bps |"
    )
    print("|---|---:|---:|---:|---:|---:|---:|")
    rows = np.arange(0, n - 1, 1)
    for name, s in sigs.items():
        ics, sds, renew = [], [], []
        prev: set[int] = set()
        for i in rows[::3]:  # every third hour keeps it quick; independent enough
            m = np.isfinite(s[i]) & np.isfinite(nxt[i])
            if m.sum() < 10:
                continue
            ics.append(xs.spearman(s[i, m], nxt[i, m]))
            sds.append(nxt[i, m].std())
            top = set(np.flatnonzero(m)[np.argsort(-s[i, m])[: m.sum() // 3]].tolist())
            if prev:
                renew.append(len(top - prev) / max(len(top), 1))
            prev = top
        x = np.array(ics)
        sd, rn = float(np.mean(sds)), float(np.mean(renew))
        # top third beats the average by ~1.09 cross-sectional sd x IC; costs 2 x 30 bps x renew
        be = 2 * 0.003 * rn / (1.09 * sd)
        tstat = x.mean() / x.std(ddof=1) * np.sqrt(len(x))
        print(
            f"| `{name}` | {x.mean():+.4f} | {tstat:+.1f} | {len(x)} | {sd:.4f} | {rn:.0%} | "
            f"{be:.2f} |",
            flush=True,
        )
        if log:
            with TRIES.open("a") as fh:
                fh.write(
                    f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | breadth-1-binance | hourly "
                    f"{name} (IC {x.mean():+.4f} t {tstat:+.1f}, break-even {be:.2f}) | "
                    f"screen | train | 2020-01-01 | {TRAIN_END} | - | - | - | - |\n"
                )


if __name__ == "__main__":
    main()
