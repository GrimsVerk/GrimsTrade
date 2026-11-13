"""The three wide books of research run breadth-1 (card in research/breadth-1.md).

    uv run python -I research/lib/breadth_books.py [cm|binance|trad] [--log]

Builds each book's calendar-day panel (cached under `<cache_root>/derived/breadth-1/`), its
point-in-time universe and signals, then runs the card's IC and tilt measures weekly and daily.
Without `--log` nothing is written to tries.md.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_xs as xs  # noqa: E402
import macro  # noqa: E402
import stats  # noqa: E402
from harness import TRAIN_END, TRAIN_LAST_BAR, TRIES  # noqa: E402

EPOCH = date(1970, 1, 1)
CM_START = date(2010, 7, 1)
CM_SNAPSHOT = "2026-11-13"
ERAS_CRYPTO = [(2010, 2016), (2017, 2021), (2022, 2025)]
ERAS_TRAD = [(1994, 1999), (2000, 2009), (2010, 2016), (2017, 2021), (2022, 2025)]


def derived() -> Path:
    d = macro.cache_root() / "derived" / "breadth-1"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------- rolling helpers (NaN-aware)


def roll_mean(a: np.ndarray, w: int, min_frac: float = 0.8) -> np.ndarray:
    """Mean of the last `w` rows including the current one; NaN if fewer than min_frac*w known."""
    ok = np.isfinite(a)
    x = np.where(ok, a, 0.0)
    cs = np.cumsum(np.vstack([np.zeros((1, a.shape[1])), x]), axis=0)
    cn = np.cumsum(np.vstack([np.zeros((1, a.shape[1])), ok]), axis=0)
    s = cs[w:] - cs[:-w]
    n = cn[w:] - cn[:-w]
    out = np.full(a.shape, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        out[w - 1 :] = np.where(n >= min_frac * w, s / n, np.nan)
    return out


def roll_std(a: np.ndarray, w: int) -> np.ndarray:
    m = roll_mean(a, w)
    m2 = roll_mean(a * a, w)
    return np.sqrt(np.maximum(m2 - m * m, 0.0))


def roll_corr(a: np.ndarray, b: np.ndarray, w: int) -> np.ndarray:
    """Rolling correlation of each column of `a` with the vector `b` (same rows)."""
    bb = np.broadcast_to(b[:, None], a.shape)
    both = np.isfinite(a) & np.isfinite(bb)
    a2, b2 = np.where(both, a, np.nan), np.where(both, bb, np.nan)
    ma, mb = roll_mean(a2, w), roll_mean(b2, w)
    cov = roll_mean(a2 * b2, w) - ma * mb
    va, vb = roll_mean(a2 * a2, w) - ma * ma, roll_mean(b2 * b2, w) - mb * mb
    with np.errstate(invalid="ignore", divide="ignore"):
        return cov / np.sqrt(np.maximum(va, 1e-30) * np.maximum(vb, 1e-30))


def roll_median(a: np.ndarray, w: int, chunk: int = 64) -> np.ndarray:
    out = np.full(a.shape, np.nan, dtype=np.float32)
    for j in range(0, a.shape[1], chunk):
        v = np.lib.stride_tricks.sliding_window_view(a[:, j : j + chunk].astype(np.float32), w, 0)
        n = np.isfinite(v).sum(-1)
        with np.errstate(all="ignore"):
            import warnings

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                med = np.nanmedian(v, axis=-1)
        out[w - 1 :, j : j + chunk] = np.where(n >= 0.8 * w, med, np.nan)
    return out.astype(float)


def lag(a: np.ndarray, k: int) -> np.ndarray:
    out = np.full(a.shape, np.nan)
    if k < a.shape[0]:
        out[k:] = a[:-k] if k else a
    return out


def logret(px: np.ndarray, a: int, b: int) -> np.ndarray:
    """log(px[t - b] / px[t - a]) for every row t."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.log(lag(px, b) / lag(px, a))


# ---------------------------------------------------------------- Book A: Coin Metrics


def cm_panel() -> dict[str, np.ndarray]:
    path = derived() / "cm-panel.npz"
    if path.exists():
        return dict(np.load(path, allow_pickle=False))
    root = macro.cache_root() / "coinmetrics" / "full" / CM_SNAPSHOT / "assets"
    n_days = (TRAIN_LAST_BAR - CM_START).days + 1
    cols: dict[str, list[np.ndarray]] = {k: [] for k in ("px", "mc", "vol", "addr")}
    names: list[str] = []
    for folder in sorted(root.iterdir()):
        rows = []
        for p in sorted(folder.glob("page-*.json")):
            rows += json.loads(p.read_text())["data"]
        m = {k: np.full(n_days, np.nan) for k in cols}
        for r in rows:
            d = date.fromisoformat(r["time"][:10])
            i = (d - CM_START).days
            if not 0 <= i < n_days:
                continue
            for k, key in (("px", "PriceUSD"), ("vol", "volume_reported_spot_usd_1d"),
                           ("addr", "AdrActCnt")):  # fmt: skip
                if r.get(key) is not None:
                    m[k][i] = float(r[key])
            mc = r.get("CapMrktEstUSD") or r.get("CapMrktCurUSD")
            if mc is not None:
                m["mc"][i] = float(mc)
        # keep a coin only if it ever passes the liquidity and size floors on some day
        if np.isfinite(m["px"]).sum() < 365:
            continue
        if not (np.nanmax(np.r_[m["mc"], 0]) >= 1e7 and np.nanmax(np.r_[m["vol"], 0]) >= 1e6):
            continue
        names.append(folder.name)
        for k in cols:
            cols[k].append(m[k])
    out = {k: np.stack(v, axis=1) for k, v in cols.items()}
    out["px"][out["px"] <= 0] = np.nan
    out["names"] = np.array(names)
    out["day0"] = np.array((CM_START - EPOCH).days)
    np.savez(path, **out)  # type: ignore[arg-type]
    return out


def history_days(px: np.ndarray) -> np.ndarray:
    """Days since the first known price, per row and column (NaN before it)."""
    known = np.isfinite(px)
    first = np.where(known.any(0), known.argmax(0), px.shape[0])
    days = np.arange(px.shape[0])[:, None] - first[None, :]
    return np.where(days >= 0, days, -1)


@dataclass
class Book:
    name: str
    day0: date
    names: list[str]
    px: np.ndarray
    elig: np.ndarray
    up: np.ndarray
    signals: dict[str, np.ndarray]
    cost: np.ndarray
    skip_week: int
    skip_day: int
    shift: int  # rows the signals and universe are lagged (as-of rule)
    weekdays_daily: tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6)
    eras: tuple[tuple[int, int], ...] = tuple(ERAS_CRYPTO)
    note: str = ""


def cm_book() -> Book:
    p = cm_panel()
    px, mc, vol, addr = p["px"], p["mc"], p["vol"], p["addr"]
    names = [str(x) for x in p["names"]]
    lr = np.vstack([np.full((1, px.shape[1]), np.nan), np.log(px[1:] / px[:-1])])
    vol90 = roll_std(lr, 90) * np.sqrt(365)
    mc30, v30 = roll_median(mc, 30), roll_median(vol, 30)
    ib, ie = names.index("btc"), names.index("eth")
    corr = np.fmax(roll_corr(lr, lr[:, ib], 90), roll_corr(lr, lr[:, ie], 90))
    corr[:, [ib, ie]] = 0.0
    hist = history_days(px)
    ok = (hist >= 365) & (v30 >= 1e6) & (mc30 >= 1e7) & (vol90 >= 0.20) & ~(corr > 0.95)
    ok &= np.isfinite(px)
    elig = np.zeros_like(ok)
    rank_mc = np.where(ok, mc30, -np.inf)
    for t in range(px.shape[0]):
        n = ok[t].sum()
        if n:
            elig[t, np.argsort(-rank_mc[t])[: min(100, n)]] = True
    with np.errstate(invalid="ignore", divide="ignore"):
        sig = {
            "mom_7": logret(px, 7, 0),
            "mom_28": logret(px, 28, 0),
            "mom_91": logret(px, 91, 7),
            "mom_365": logret(px, 365, 28),
            "rev_1": -logret(px, 1, 0),
            "size": -np.log(roll_mean(mc, 7)),
            "turnover": -np.log(roll_mean(vol, 30) / roll_mean(mc, 30)),
            "vol_growth": np.log(roll_mean(vol, 7) / roll_mean(vol, 91)),
            "low_vol": -vol90,
            "addr_growth": np.log(roll_mean(addr, 30) / roll_mean(addr, 365)),
        }
        up = logret(px, 365, 0) > 0
    sh = 1  # a value stamped x is usable from x + 1
    sig = {k: lag(v, sh) for k, v in sig.items()}
    elig = lag(elig.astype(float), sh) == 1
    up = lag(up.astype(float), sh) == 1
    cost = np.full(px.shape[1], 0.003)
    day0 = EPOCH + timedelta(days=int(p["day0"]))
    return Book("cm", day0, names, px, elig, up, sig, cost, 1, 1, sh)


# ---------------------------------------------------------------- Book A2: Binance 30


def binance_book() -> Book:
    d = derived()
    files = sorted(d.glob("binance-*-1h.npz"))
    syms = [f.name.split("-")[1] for f in files]
    day0 = date(2017, 7, 1)
    n_days = (TRAIN_LAST_BAR - day0).days + 1
    px = np.full((n_days, len(syms)), np.nan)
    qv = np.full_like(px, np.nan)
    fund = np.full_like(px, np.nan)
    prem = np.full_like(px, np.nan)
    t0 = int(datetime.combine(day0, datetime.min.time(), UTC).timestamp())
    for j, (s, f) in enumerate(zip(syms, files, strict=True)):
        b = np.load(f)
        day = (b["t"] - t0) // 86400
        k = (day >= 0) & (day < n_days)
        day, c, q = day[k], b["c"][k], b["q"][k]
        # daily close = close of the day's last hour (needs the 23:00 bar to be a full day)
        last = np.r_[np.flatnonzero(np.diff(day)), len(day) - 1]
        full = (b["t"][k][last] % 86400) == 23 * 3600
        px[day[last][full], j] = c[last][full]
        qsum = np.bincount(day, weights=q, minlength=n_days)
        has = np.bincount(day, minlength=n_days) > 0
        qv[has, j] = qsum[has]
        fp = d / f"binance-{s}-funding.npz"
        if fp.exists():
            fz = np.load(fp)
            if "ft" in fz:
                fd = (fz["ft"] - t0) // 86400  # funding paid at ft is known by the end of day fd
                kk = (fd >= 0) & (fd < n_days)
                num = np.bincount(fd[kk], weights=fz["fr"][kk], minlength=n_days)
                cnt = np.bincount(fd[kk], minlength=n_days)
                fund[cnt > 0, j] = (num / np.maximum(cnt, 1) * 3)[cnt > 0]  # per 8h, x3 per day
            if "pt" in fz:
                pdx = (fz["pt"] - t0) // 86400  # bar starts at pt, closes within that day
                kk = (pdx >= 0) & (pdx < n_days)
                num = np.bincount(pdx[kk], weights=fz["pc"][kk], minlength=n_days)
                cnt = np.bincount(pdx[kk], minlength=n_days)
                prem[cnt > 0, j] = (num / np.maximum(cnt, 1))[cnt > 0]
    lr = np.vstack([np.full((1, len(syms)), np.nan), np.log(px[1:] / px[:-1])])
    vol90 = roll_std(lr, 90) * np.sqrt(365)
    q30 = roll_median(qv, 30)
    hist = history_days(px)
    elig = (hist >= 365) & (q30 >= 5e6) & np.isfinite(px)
    cm = cm_panel()
    cm_names = [str(x) for x in cm["names"]]
    cm_day0 = EPOCH + timedelta(days=int(cm["day0"]))
    off = (day0 - cm_day0).days
    mc = np.full_like(px, np.nan)
    for j, s in enumerate(syms):
        base = s.removesuffix("USDT").lower()
        if base in cm_names:
            # Coin Metrics stamps lag one day (as-of rule): use the value stamped t - 1 at t
            col = cm["mc"][off - 1 : off - 1 + n_days, cm_names.index(base)]
            mc[: len(col), j] = col
    with np.errstate(invalid="ignore", divide="ignore"):
        sig = {
            "mom_7": logret(px, 7, 0),
            "mom_28": logret(px, 28, 0),
            "mom_91": logret(px, 91, 7),
            "mom_365": logret(px, 365, 28),
            "rev_1": -logret(px, 1, 0),
            "size": -np.log(roll_mean(mc, 7)),
            "turnover": -np.log(roll_mean(qv, 30) / roll_mean(mc, 30)),
            "vol_growth": np.log(roll_mean(qv, 7) / roll_mean(qv, 91)),
            "low_vol": -vol90,
            "funding": -roll_mean(fund, 7, 0.5),
            "premium": -roll_mean(prem, 7, 0.5),
        }
        up = logret(px, 365, 0) > 0
    cost = np.full(len(syms), 0.003)
    note = "survivors picked in 2026"
    return Book("binance", day0, syms, px, elig, up, sig, cost, 0, 0, 0, note=note)


# ---------------------------------------------------------------- Book B: 33 markets


def trad_book() -> Book:
    import ml
    from harness import CRYPTO, UNIVERSE

    hist = ml.pool_history()
    syms: list[str] = []
    series = []
    for _set, h in hist.items():
        for s, bars in h.items():
            if s in syms:
                continue
            syms.append(s)
            series.append(bars)
    day0 = min(b[0].date for b in series)
    n_days = (TRAIN_LAST_BAR - day0).days + 1
    raw = np.full((n_days, len(syms)), np.nan)
    for j, bars in enumerate(series):
        for b in bars:
            raw[(b.date - day0).days, j] = b.close
    hist_d = history_days(raw)
    last_real = np.where(np.isfinite(raw), np.arange(n_days)[:, None], -10**9)
    np.maximum.accumulate(last_real, axis=0, out=last_real)
    stale = (np.arange(n_days)[:, None] - last_real) > 5
    px = xs.ffill(raw)
    px[hist_d < 0] = np.nan
    lr = np.vstack([np.zeros((1, len(syms))), np.log(px[1:] / px[:-1])])
    lr[~np.isfinite(lr)] = np.nan
    # EWMA vol, 60-day half-life, on calendar days (closed days add a zero return)
    lam = 0.5 ** (1 / 60)
    var = np.full_like(lr, np.nan)
    v = np.full(len(syms), np.nan)
    for t in range(n_days):
        x = lr[t]
        f = np.isfinite(x)
        v = np.where(f & np.isnan(v), x**2, v)
        v = np.where(f, lam * v + (1 - lam) * np.nan_to_num(x) ** 2, v)
        var[t] = v
    vol = np.sqrt(var * 365)
    vol[hist_d < 60] = np.nan

    def z(a: int, b: int) -> np.ndarray:
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.clip(logret(px, a, b) / (vol * np.sqrt((a - b) / 365)), -5, 5)

    with np.errstate(invalid="ignore", divide="ignore"):
        hi = np.fmax.reduce(np.lib.stride_tricks.sliding_window_view(
            np.nan_to_num(px, nan=-np.inf), 365, 0), axis=-1)  # fmt: skip
        high = np.full_like(px, np.nan)
        high[364:] = np.log(px[364:] / hi)
        sig = {
            "mom_7": z(7, 0),
            "mom_28": z(28, 0),
            "mom_91": z(91, 7),
            "mom_365": z(365, 28),
            "low_vol": -vol,
            "high_52w": high,
        }
        up = logret(px, 365, 0) > 0
    elig = (hist_d >= 365) & ~stale & np.isfinite(px)
    cost = np.array([0.003 if UNIVERSE[s] == CRYPTO else 0.0002 for s in syms])
    return Book("trad", day0, syms, px, elig, up, sig, cost, 3, 1, 0, (0, 1, 2, 3),
                tuple(ERAS_TRAD), "S&P 500 index and SPY both in after 1993")  # fmt: skip


# ---------------------------------------------------------------- measures and report


def decisions(book: Book, freq: str, start_day: int) -> tuple[np.ndarray, int]:
    days = np.arange(start_day, book.px.shape[0])
    wd = np.array([(book.day0 + timedelta(days=int(i))).weekday() for i in days])
    last = (TRAIN_END - book.day0).days
    days, wd = days[days <= last], wd[days <= last]
    if freq == "weekly":
        return days[wd == 4], book.skip_week
    return days[np.isin(wd, book.weekdays_daily)], book.skip_day


def mdd(r: np.ndarray) -> float:
    return stats.max_drawdown(r)


def era_ahead(book: Book, first: int, a: np.ndarray, b: np.ndarray) -> tuple[int, int]:
    yrs = np.array([(book.day0 + timedelta(days=int(first + i))).year for i in range(len(a))])
    ahead = n = 0
    for y0, y1 in book.eras:
        m = (yrs >= y0) & (yrs <= y1)
        if m.sum() < 180:
            continue
        n += 1
        ahead += stats.sharpe(a[m]) > stats.sharpe(b[m])
    return ahead, n


def start_day(book: Book) -> int:
    n = (book.elig & np.isfinite(book.px)).sum(1)
    return int(np.argmax(n >= 30 if book.name == "cm" else n >= 10))


def run(book: Book, log: bool) -> list[dict[str, object]]:
    s0 = start_day(book)
    rows: list[dict[str, object]] = []
    base_logged: set[str] = set()
    for freq in ("weekly", "daily"):
        dec, skip = decisions(book, freq, s0)
        for name, sig in book.signals.items():
            if name == "rev_1" and freq == "weekly":
                continue
            ic = xs.ic_stats(book.px, book.elig, sig, dec, skip)
            tl = xs.tilt(book.px, book.elig, sig, book.up, dec, skip, book.cost)
            gross = xs.tilt(book.px, book.elig, sig, book.up, dec, skip, book.cost * 0)
            d_ts, p_ts, _, _ = stats.sharpe_diff_boot(tl.top_ts, tl.ts)
            d_ew, p_ew, _, _ = stats.sharpe_diff_boot(tl.top, tl.ew)
            g_ts = stats.sharpe(gross.top_ts) - stats.sharpe(gross.ts)
            ahead, n_eras = era_ahead(book, tl.first, tl.top_ts, tl.ts)
            # breakeven cost per side: Sharpe gain is ~linear in cost
            be = float("nan")
            c0 = float(book.cost.max())
            if g_ts > 0 and g_ts != d_ts:
                be = c0 * g_ts / (g_ts - d_ts) if d_ts < g_ts else float("inf")
            passed = (
                ic.t >= 3 and np.sign(ic.first) == np.sign(ic.second) == 1
                and d_ts > 0 and p_ts < 0.10 and ahead * 2 > n_eras and d_ew > 0
                and mdd(tl.top_ts) <= mdd(tl.ts) + 0.05
            )  # fmt: skip
            weak = ic.t >= 3 and g_ts > 0 and not passed
            first_date = book.day0 + timedelta(days=tl.first)
            row: dict[str, object] = {
                "book": book.name, "freq": freq, "signal": name, "ic": ic, "first": first_date,
                "sh_ew": stats.sharpe(tl.ew), "sh_top": stats.sharpe(tl.top),
                "sh_ts": stats.sharpe(tl.ts), "sh_top_ts": stats.sharpe(tl.top_ts),
                "d_ts": d_ts, "p_ts": p_ts, "d_ew": d_ew, "p_ew": p_ew, "g_ts": g_ts,
                "g_ew": stats.sharpe(gross.top) - stats.sharpe(gross.ew),
                "ahead": f"{ahead}/{n_eras}", "mdd_ts": mdd(tl.ts), "mdd_top_ts": mdd(tl.top_ts),
                "turn": tl.turnover["top_ts"], "be": be,
                "verdict": "PASS" if passed else ("weak-but-real" if weak else "no"),
                "cagr_top_ts": stats.cagr(tl.top_ts),
            }  # fmt: skip
            rows.append(row)
            print(fmt_row(row), flush=True)
            if log:
                for b_name, r in (("ew", tl.ew), ("ts", tl.ts)):
                    key = f"{freq}-{b_name}-{tl.first}"
                    if key not in base_logged:
                        base_logged.add(key)
                        log_row(f"breadth-1-{book.name}", f"{freq} {b_name.upper()} baseline",
                                "baseline", first_date, r, tl.turnover[b_name])  # fmt: skip
                log_row(f"breadth-1-{book.name}",
                        f"{freq} {name} TOP-TS (IC {ic.mean:+.3f} t {ic.t:+.1f}, "
                        f"vs TS {d_ts:+.2f} p {p_ts:.2f}) {row['verdict']}",
                        "variant", first_date, tl.top_ts, tl.turnover["top_ts"])  # fmt: skip
    return rows


def log_row(idea: str, variant: str, kind: str, first: date, r: np.ndarray, turn: float) -> None:
    eq = np.cumprod(1 + r)
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {idea} | {variant} | {kind} | train | {first} | "
        f"{TRAIN_END} | {stats.sharpe(r):.2f} | {eq[-1] - 1:+.1%} | {mdd(r):.1%} | {turn:.2f} |\n"
    )
    with TRIES.open("a") as f:
        f.write(row)


def fmt_row(r: dict[str, object]) -> str:
    ic = r["ic"]
    assert isinstance(ic, xs.IC)
    return (
        f"| {r['freq']} | `{r['signal']}` | {ic.mean:+.3f} | {ic.t:+.1f} | {ic.pos:.0%} | "
        f"{ic.first:+.3f} / {ic.second:+.3f} | {ic.breadth:.0f} | {r['sh_ew']:.2f} | "
        f"{r['sh_top']:.2f} | {r['sh_ts']:.2f} | {r['sh_top_ts']:.2f} | {r['d_ts']:+.2f} "
        f"({r['p_ts']:.2f}) | {r['g_ts']:+.2f} | {r['g_ew']:+.2f} | {r['ahead']} | "
        f"{r['mdd_ts']:.0%} / {r['mdd_top_ts']:.0%} | {r['turn']:.0f} | {r['verdict']} |"
    )


HEADER = (
    "| Freq | Signal | IC | t | IC>0 | IC halves | Assets | EW | TOP | TS | TOP-TS | "
    "TOP-TS - TS (p) | gross | TOP-EW gross | Eras ahead | Max DD TS / TOP-TS | Turn/yr | "
    "Verdict |\n|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---|"
)

BOOKS: dict[str, Callable[[], Book]] = {"cm": cm_book, "binance": binance_book, "trad": trad_book}


def main() -> None:
    which = sys.argv[1]
    log = "--log" in sys.argv
    book = BOOKS[which]()
    n = (book.elig & np.isfinite(book.px)).sum(1)
    s0 = start_day(book)
    print(f"book {which}: {len(book.names)} assets ever, start {book.day0 + timedelta(s0)}, "
          f"eligible per day median {np.median(n[s0:]):.0f} max {n.max()}", flush=True)  # fmt: skip
    if "--panel" in sys.argv:  # coverage only: no measure is computed
        return
    print(HEADER)
    rows = run(book, log)
    out = derived() / f"results-{which}.json"
    out.write_text(json.dumps([{k: (v.__dict__ if isinstance(v, xs.IC) else str(v)
                                    if isinstance(v, date) else v) for k, v in r.items()}
                               for r in rows], default=float))  # fmt: skip


if __name__ == "__main__":
    main()
