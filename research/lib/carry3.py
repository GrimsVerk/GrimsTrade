"""Research run carry-3: does the funding carry survive real costs? (card in
research/carry-3.md).

    uv run python -I research/lib/carry3.py --check          # the copy reproduces carry-2
    uv run python -I research/lib/carry3.py --calibrate      # cost model from the snapshots
    uv run python -I research/lib/carry3.py [--log]          # the train run
    uv run python -I research/lib/carry3.py --heldout        # once, only after a train pass
    uv run python -I research/lib/carry3.py --heldout-dry    # crash test on train bars, no output

Reads (never runs) the raw downloads of `scripts/fetch_carry2.py` and `scripts/fetch_carry3.py`
from the shared cache, builds one daily panel per venue (cached under
`<cache_root>/derived/carry-3/`; train panels drop every bar after the train cut), and runs the
card's five shapes with `carry3_engine.simulate`. Writes `research/results/carry-3.md` (and
`carry-3-heldout.md` for the one held-out run). Without `--log` nothing is written to tries.md.
carry-2's modules are imported for shared helpers, never edited.
"""

from __future__ import annotations

import json
import sys
import zipfile
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import carry3_cost as cc  # noqa: E402
import carry3_engine as ce  # noqa: E402
import carry3_panel as cp  # noqa: E402
import macro  # noqa: E402
import short1  # noqa: E402
import short_engine as se  # noqa: E402
import stats  # noqa: E402
from breadth_agg import _kline_rows  # noqa: E402
from breadth_xs import logret, roll_mean, roll_median, roll_std  # noqa: E402
from carry3_panel import DAY0  # noqa: E402
from harness import HELD_END, HELD_START, TRAIN_END, TRAIN_LAST_BAR, TRIES  # noqa: E402

assert TRAIN_LAST_BAR == cp.TRAIN_LAST_BAR
ERAS = [(2020, 2021), (2022, 2025)]
YEARS = list(range(2021, 2026))
RESULTS = Path(__file__).resolve().parents[1] / "results"
OUT = RESULTS / "carry-3.md"
OUT_HELD = RESULTS / "carry-3-heldout.md"
COST_JSON = RESULTS / "carry-3-cost.json"
VARIANTS = ("w1", "w2", "w4", "band", "f30")
PRIMARY = "band"
POOL = ("B-out", "Bybit", "Hyperliquid")
FILES = {"B-out": "binance", "B-all": "binance", "Bybit": "bybit", "Hyperliquid": "hyperliquid"}


def raw() -> Path:
    return macro.cache_root()


def derived() -> Path:
    d = macro.cache_root() / "derived" / "carry-3"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ts(a: np.ndarray) -> np.ndarray:
    t = a.astype(float).copy()
    t[t > 1e14] /= 1000.0  # some 2025+ Binance files are in microseconds
    return (t // 1000).astype(np.int64)


# ---------------------------------------------------------------- panels


def held_raw() -> Path:
    """The held-out downloads (`scripts/fetch_carry3.py heldout`), kept apart from train's."""
    return raw() / "carry-3" / "heldout"


def load_binance(grid: cp.Grid) -> None:
    root = raw() / "binance" / "futures" / "um" / "monthly"
    held = grid.tag == "heldout"
    extra = held_raw() / "binance"
    acc = cp.Acc(grid)
    for d in sorted((root / "klines").iterdir()):
        files = [p for p in sorted((d / "1d").glob("*.zip")) if p.stem[-7:] <= "2025-11"]
        fz = [
            p
            for p in sorted((root / "fundingRate" / d.name).glob("*.zip"))
            if p.stem[-7:] <= "2025-11"
        ]
        if held:
            files += sorted((extra / "monthly" / "klines" / d.name / "1d").glob("*.zip"))
            files += sorted((extra / "daily" / "klines" / d.name / "1d").glob("*.zip"))
            fz += sorted((extra / "monthly" / "fundingRate" / d.name).glob("*.zip"))
        if not files or not fz:
            continue  # never passed the volume pre-filter (or no funding history)
        k = np.concatenate([a for a in (_kline_rows(p) for p in files) if len(a)])
        rows = []
        for p in fz:
            with zipfile.ZipFile(p) as z:
                for ln in z.read(z.namelist()[0]).decode().splitlines():
                    f = ln.split(",")
                    if f[0].isdigit():
                        rows.append((int(f[0]) // 1000, float(f[-1])))
        rest = extra / "rest" / "fundingRate-2026-11" / f"{d.name}.json"
        if held and rest.exists():
            for x in json.loads(rest.read_text()):
                rows.append((int(x["fundingTime"]) // 1000, float(x["fundingRate"])))
        f = np.array(sorted(set(rows)))
        ft, fr = f[:, 0].astype(np.int64), f[:, 1]
        acc.add(d.name, _ts(k[:, 0]), k[:, 2], k[:, 3], k[:, 4], k[:, 7], ft, fr)
    acc.save(derived(), "binance")


def _json(paths: list[Path]) -> list[Any]:
    out: list[Any] = []
    for p in paths:
        if p.exists():
            out += json.loads(p.read_text())
    return out


def load_bybit(grid: cp.Grid) -> None:
    dirs = [raw() / "bybit" / "linear" / "to-2025-11-10"]
    if grid.tag == "heldout":
        dirs.append(held_raw() / "bybit")
    acc = cp.Acc(grid)
    for d in sorted(dirs[0].iterdir()):
        fl = _json([x / d.name / "funding.json" for x in dirs])
        kl = _json([x / d.name / "kline-D.json" for x in dirs])
        if not fl or not kl:
            continue
        k = np.array(kl, dtype=float)
        ft = np.array([int(x["fundingRateTimestamp"]) // 1000 for x in fl], dtype=np.int64)
        fr = np.array([float(x["fundingRate"]) for x in fl])
        ft, i = np.unique(ft, return_index=True)
        day = (k[:, 0] // 1000).astype(np.int64)
        acc.add(d.name, day, k[:, 2], k[:, 3], k[:, 4], k[:, 6], ft, fr[i])
    acc.save(derived(), "bybit")


def load_hyperliquid(grid: cp.Grid) -> None:
    dirs = [raw() / "hyperliquid" / "perp" / "to-2025-11-10"]
    if grid.tag == "heldout":
        dirs.append(held_raw() / "hyperliquid")
    acc = cp.Acc(grid)
    for d in sorted(dirs[0].iterdir()):
        fl = _json([x / d.name / "funding.json" for x in dirs])
        c = _json([x / d.name / "candles-1d.json" for x in dirs])
        if not fl or not c:
            continue
        t = np.array([int(x["t"]) // 1000 for x in c], dtype=np.int64)
        hi = np.array([float(x["h"]) for x in c])
        lo = np.array([float(x["l"]) for x in c])
        close = np.array([float(x["c"]) for x in c])
        qv = np.array([float(x["v"]) * float(x["c"]) for x in c])
        ft = np.array([int(x["time"]) // 1000 for x in fl], dtype=np.int64)
        fr = np.array([float(x["fundingRate"]) for x in fl])
        ft, i = np.unique(ft, return_index=True)
        acc.add(d.name, t, hi, lo, close, qv, ft, fr[i])
    acc.save(derived(), "hyperliquid")


LOADERS = {"binance": load_binance, "bybit": load_bybit, "hyperliquid": load_hyperliquid}


def ensure_panels(grid: cp.Grid) -> None:
    for venue, fn in LOADERS.items():
        if not (derived() / f"{venue}-{grid.tag}.npz").exists():
            fn(grid)
            print("panel", venue, grid.tag, flush=True)


class Venue:
    def __init__(
        self,
        label: str,
        grid: cp.Grid,
        last_decision: date,
        keep: list[str] | None = None,
        drop: set[str] | None = None,
    ) -> None:
        z = np.load(derived() / f"{FILES[label]}-{grid.tag}.npz")
        names = [str(x) for x in z["names"]]
        cols = [
            j
            for j, s in enumerate(names)
            if (keep is None or s in keep) and s not in (drop or set())
        ]
        self.label = label
        self.venue = FILES[label]
        self.grid = grid
        self.names = [names[j] for j in cols]
        self.px = z["px"][:, cols]
        self.hi = z["hi"][:, cols]
        self.lo = z["lo"][:, cols]
        qv = z["qv"][:, cols]
        self.fund = z["fsim"][:, cols]
        cnt = z["fcnt"][:, cols]
        n_days, n = self.px.shape
        alive = (cnt > 0) | (np.vstack([np.zeros((1, n)), cnt[:-1]]) > 0)
        hist = bb.history_days(self.px)
        self.adv = roll_median(qv, 30)
        elig = (hist >= 365) & (self.adv >= 5e6) & np.isfinite(self.px)
        self.tradable = elig & alive
        with np.errstate(invalid="ignore", divide="ignore"):
            fsig = z["fsig"][:, cols]
            self.sig = {"f7": -roll_mean(fsig, 7, 0.5), "f30": -roll_mean(fsig, 30, 0.5)}
            self.up = logret(self.px, 365, 0) > 0
            lr = np.vstack([np.full((1, n), np.nan), np.log(self.px[1:] / self.px[:-1])])
        vol = roll_std(lr, 30)
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            med = np.nanmedian(np.where(self.tradable, vol, np.nan), axis=1)
        med = np.nan_to_num(med, nan=float(np.nanmedian(vol)))
        self.vol = np.where(np.isfinite(vol), vol, med[:, None])
        last_px = np.where(
            np.isfinite(self.px).any(0), n_days - 1 - np.isfinite(self.px[::-1]).argmax(0), -1
        )
        self.delisted = last_px < n_days - 31
        cnt_t = self.tradable.sum(1)
        self.ok = bool((cnt_t >= 10).any())
        s0 = int(np.argmax(cnt_t >= 10))
        days = np.arange(s0, n_days)
        wd = np.array([(DAY0 + timedelta(days=int(i))).weekday() for i in days])
        dec = days[(wd == 4) & (days <= (last_decision - DAY0).days)]
        self.dw, _, _ = xs.schedule(n_days, dec, 0)
        self.b0 = int(self.dw[0]) if len(self.dw) else n_days
        self.years = (n_days - self.b0) / 365
        self.tradable_median = float(np.median(cnt_t[self.b0 :])) if self.ok else 0.0

    def mask(self, t: int, sig: str = "f7") -> np.ndarray:
        m: np.ndarray = self.tradable[t] & np.isfinite(self.px[t]) & np.isfinite(self.sig[sig][t])
        return m

    def first(self) -> date:
        return DAY0 + timedelta(days=self.b0 + 1)


# ---------------------------------------------------------------- books


def book(
    v: Venue, base: np.ndarray, decide: ce.Decide, cm: cc.CostModel, share: np.ndarray, fund: bool
) -> ce.Run:
    def charge(t: int, dw: np.ndarray) -> np.ndarray:
        return cm.parts(dw, v.adv[t], v.vol[t], float(share[t]))

    min_dw = None if cm.flat is not None else cc.MIN_ORDER_USD / (cm.account * share)
    return ce.simulate(v.px, v.fund if fund else None, base, decide, charge, v.b0, min_dw)


def mean_runs(runs: list[ce.Run]) -> ce.Run:
    def m(k: str) -> np.ndarray:
        out: np.ndarray = np.mean([getattr(r, k) for r in runs], axis=0)
        return out

    return ce.Run(m("r"), m("funding"), m("gross"), m("net"), m("traded"), m("cost"))


def venue_rows(
    v: Venue, cm: cc.CostModel, share: np.ndarray, only: tuple[str, ...] | None = None
) -> dict[str, tuple[ce.Run, str]]:
    """Every row of the card for one venue: name -> (run, kind). `only`: just those shapes at
    the realistic cost (plus the twin)."""
    dw = v.dw
    tg7 = np.array([ce.long_short(v.sig["f7"][t], v.mask(t)) for t in dw])
    tg30 = np.array([ce.long_short(v.sig["f30"][t], v.mask(t, "f30")) for t in dw])

    def ts(t: int) -> np.ndarray:
        m = v.tradable[t] & np.isfinite(v.px[t])
        return np.where(m & v.up[t], 1.0 / max(m.sum(), 1), 0.0)

    tw = np.array([ts(t) for t in dw])

    def fixed(tg: np.ndarray) -> ce.Decide:
        return lambda k, t, w: tg[k]

    def band(top: int | None = None, store: list[np.ndarray] | None = None) -> ce.Decide:
        def decide(k: int, t: int, w: np.ndarray) -> np.ndarray:
            m = v.mask(t)
            if top is not None:
                m = ce.top_n(v.adv[t], m, top)
            new = ce.band_weights(v.sig["f7"][t], m, w)
            if store is not None:
                store.append(new)
            return new

        return decide

    def tranche(k_parts: int, model: cc.CostModel) -> list[ce.Run]:
        return [
            book(v, dw[j::k_parts], fixed(tg7[j::k_parts]), model, share / k_parts, True)
            for j in range(k_parts)
        ]

    def shape(name: str, model: cc.CostModel) -> ce.Run:
        if name == "w1":
            return book(v, dw, fixed(tg7), model, share, True)
        if name == "f30":
            return book(v, dw, fixed(tg30), model, share, True)
        if name == "band":
            return book(v, dw, band(), model, share, True)
        return mean_runs(tranche(int(name[1:]), model))

    out: dict[str, tuple[ce.Run, str]] = {}
    twin_cm = cc.CostModel(v.venue, None, flat=0.003)
    out["tsmom12 twin"] = (book(v, dw, fixed(tw), twin_cm, share, False), "baseline")
    names = only or VARIANTS
    for name in names:
        out[name] = (shape(name, cm), "variant")
    if only is not None:
        return out
    for name in VARIANTS:
        out[f"{name} nocost"] = (shape(name, cm.but(flat=0.0)), "robustness")
    out["w1 flat10"] = (shape("w1", cm.but(flat=0.001)), "robustness")
    for kp in (2, 4):
        for j, r in enumerate(tranche(kp, cm)):
            out[f"w{kp} phase {j + 1}"] = (r, "robustness")
    for label, model in (
        ("flat10", cm.but(flat=0.001)),
        ("flat30", cm.but(flat=0.003)),
        ("x2", cm.but(stress=2.0)),
        ("A100k", cm.but(account=100_000.0)),
        ("A1M", cm.but(account=1_000_000.0)),
        ("maker", cm.but(maker_share=cc.MAKER_SHARE)),
    ):
        out[f"band {label}"] = (shape("band", model), "robustness")
    out["band top50"] = (book(v, dw, band(top=50), cm, share, True), "robustness")
    store: list[np.ndarray] = []
    book(v, dw, band(store=store), cm, share, True)
    for sign, leg in ((1, "long"), (-1, "short")):
        lt = np.array([np.where(sign * s > 0, s, 0.0) for s in store])
        out[f"band {leg} leg"] = (book(v, dw, fixed(lt), cm, share, True), "robustness")
    return out


def pad(r: ce.Run, b0: int, start: int, n_days: int) -> dict[str, np.ndarray]:
    """A venue run on the pooled day axis (zeros before the venue starts)."""
    off = b0 + 1 - start
    out = {}
    for k in ("r", "funding", "gross", "net", "traded"):
        a = np.zeros(n_days - start)
        a[off:] = getattr(r, k)
        out[k] = a
    c = np.zeros((n_days - start, 3))
    c[off:] = r.cost
    out["cost"] = c
    return out


def pool_runs(parts: list[tuple[ce.Run, int]], start: int, n_days: int) -> ce.Run:
    """Equal capital per venue book on each day it exists."""
    n = n_days - start
    cnt = np.zeros(n)
    for _, b0 in parts:
        cnt[b0 + 1 - start :] += 1
    padded = [pad(r, b0, start, n_days) for r, b0 in parts]

    def m(k: str) -> np.ndarray:
        tot = sum(p[k] for p in padded)
        out: np.ndarray = tot / (cnt[:, None] if k == "cost" else cnt)
        return out

    return ce.Run(m("r"), m("funding"), m("gross"), m("net"), m("traded"), m("cost"))


def shares(venues: dict[str, Venue], n_days: int) -> np.ndarray:
    """1 / (number of pooled venue books trading that day), per day."""
    cnt = np.zeros(n_days)
    for lab in POOL:
        if lab in venues:
            cnt[venues[lab].b0 :] += 1
    out: np.ndarray = 1.0 / np.maximum(cnt, 1)
    return out


# ---------------------------------------------------------------- statistics


def summary(run: ce.Run, first: date, years: float) -> dict[str, Any]:
    r = run.r
    yrs = np.array([(first + timedelta(days=i)).year for i in range(len(r))])

    def sub(y0: int, y1: int) -> float | None:
        m = (yrs >= y0) & (yrs <= y1)
        return stats.sharpe(r[m]) if m.sum() >= 180 else None

    eq = np.cumprod(1 + r)
    traded = float(run.traded.sum())
    cost = run.cost.sum(0)
    return {
        "sharpe": stats.sharpe(r),
        "cagr": stats.cagr(r),
        "mdd": stats.max_drawdown(r),
        "worst_week": float((eq[7:] / eq[:-7] - 1).min()) if len(r) > 7 else float("nan"),
        "eras": [sub(a, b) for a, b in ERAS],
        "years": [sub(y, y) for y in YEARS],
        "funding_yr": float(run.funding.sum() / years),
        "turn_yr": traded / years,
        "cost_yr": [float(c / years) for c in cost],
        "cost_side_bps": float(cost.sum() / traded * 1e4) if traded > 0 else 0.0,
        "gross": float(run.gross.mean()),
        "abs_net": float(np.abs(run.net).mean()),
    }


def add_tests(
    rows: dict[str, dict[str, Any]],
    series: dict[str, np.ndarray],
    btc: np.ndarray | None,
    keys: tuple[str, ...],
) -> None:
    tw = series["tsmom12 twin"]
    for key in keys:
        r = series[key]
        row = rows[key]
        row["corr_twin"] = float(np.corrcoef(r, tw)[0, 1]) if r.std() > 0 else 0.0
        blend = 0.5 * tw + 0.5 * r
        d, p, _, _ = stats.sharpe_diff_boot(blend, tw)
        _, p0, _, _ = stats.sharpe_diff_boot(r, np.zeros_like(r))
        row |= {
            "p_zero": p0,
            "blend_sharpe": stats.sharpe(blend),
            "blend_diff": d,
            "blend_p": p,
            "blend_mdd": stats.max_drawdown(blend),
        }
        if btc is not None:
            b2 = 0.5 * btc + 0.5 * r
            d2, p2, _, _ = stats.sharpe_diff_boot(b2, btc)
            row |= {
                "btc_blend_sharpe": stats.sharpe(b2),
                "btc_blend_diff": d2,
                "btc_blend_p": p2,
                "btc_blend_mdd": stats.max_drawdown(b2),
                "btc_mdd": stats.max_drawdown(btc),
                "corr_btc": float(np.corrcoef(r, btc)[0, 1]) if r.std() > 0 else 0.0,
            }


def btc_eth_spot(start: int, n_days: int) -> np.ndarray:
    """The paper system's rule on short-1's data: `tsmom12` long-only on BTC/ETH spot, 30 bps,
    on the pooled day axis (train only)."""
    b = bb.binance_book()
    _, alive = short1.funding_panel(b)
    two = [b.names.index("BTCUSDT"), b.names.index("ETHUSDT")]
    shapes, b0 = short1.build(b, b.elig & alive, two, 1)
    sh = next(s for s in shapes if s.name == "tsmom12 spot")
    run = se.simulate(b.px, None, sh.targets, sh.base, short1.SPOT_COST, b0)
    first = (b.day0 - DAY0).days + b0 + 1  # index of run.r[0] on carry-3's day axis
    out = np.zeros(n_days - start)
    lo = max(start, first)
    out[lo - start :] = run.r[lo - first : lo - first + n_days - lo]
    return out


def btc_eth_perp(grid: cp.Grid, last_decision: date, start: int) -> np.ndarray:
    """The same rule on Binance perp closes standing in for spot (30 bps, no funding): the only
    BTC/ETH series the held-out download has."""
    v = Venue("B-all", grid, last_decision, keep=["BTCUSDT", "ETHUSDT"])
    n_days = v.px.shape[0]
    days = np.arange(start - 1, n_days)
    wd = np.array([(DAY0 + timedelta(days=int(i))).weekday() for i in days])
    dec = days[(wd == 4) & (days <= (last_decision - DAY0).days)]
    dw, _, _ = xs.schedule(n_days, dec, 0)
    hist = bb.history_days(v.px)
    tg = np.array([np.where((hist[t] >= 365) & v.up[t], 0.5, 0.0) for t in dw])
    run = se.simulate(v.px, None, tg, dw, 0.003, start - 1)
    out: np.ndarray = run.r
    return out


def verdict(
    key: str, pool: dict[str, dict[str, Any]], per: dict[str, dict[str, dict[str, Any]]]
) -> dict[str, Any]:
    p = pool[key]
    eras = [e for e in p["eras"] if e is not None]
    bars = {
        "1 pooled Sharpe > 0, p < 0.10": p["sharpe"] > 0 and p["p_zero"] < 0.10,
        "2 Sharpe > 0 on every venue": all(per[lab][key]["sharpe"] > 0 for lab in POOL),
        "3 pooled blend beats the twin, p < 0.10": p["blend_p"] < 0.10,
        "4 pooled Sharpe > 0 in both eras": bool(eras) and all(e > 0 for e in eras),
    }
    extra = {
        "(5) blend with BTC/ETH spot tsmom12 beats it, p < 0.10, drawdown within 5 points": (
            p.get("btc_blend_p", 1.0) < 0.10
            and p.get("btc_blend_mdd", 1.0) <= p.get("btc_mdd", 0.0) + 0.05
        )
    }
    if f"{key} x2" in pool:
        extra["(6) pooled Sharpe > 0 at x2 slippage and at 100,000 USD"] = (
            pool[f"{key} x2"]["sharpe"] > 0 and pool[f"{key} A100k"]["sharpe"] > 0
        )
    return {
        "key": key,
        "bars": bars,
        "extra": extra,
        "train_pass": all(bars.values()),
        "p": p["p_zero"],
        "p_x5": min(1.0, p["p_zero"] * 5),
        "p_x7": min(1.0, p["p_zero"] * 7),
    }


def log_row(
    idea: str, variant: str, kind: str, period: str, first: date, last: date, run: ce.Run | None
) -> None:
    if run is None:
        cells = "- | - | - | -"
    else:
        r = run.r
        eq = np.cumprod(1 + r)
        years = len(r) / 365
        cells = (
            f"{stats.sharpe(r):.2f} | {eq[-1] - 1:+.1%} | {stats.max_drawdown(r):.1%} | "
            f"{run.traded.sum() / years:.2f}"
        )
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {idea} | {variant} | {kind} | {period} | "
        f"{first} | {last} | {cells} |\n"
    )
    PENDING.append(row)


PENDING: list[str] = []  # rows are written together, only once the whole run has succeeded


def flush_log() -> None:
    with TRIES.open("a") as f:
        f.writelines(PENDING)
    PENDING.clear()


# ---------------------------------------------------------------- descriptive extras


def ic_rows(v: Venue) -> list[dict[str, Any]]:
    """Weekly cross-sectional Spearman IC of the funding signal against next week's price
    return and against the return of a long position including funding."""
    n_days = v.px.shape[0]
    d, b, e = xs.schedule(n_days, v.dw, 0)
    price = xs.fwd_logret(v.px, b, e)
    cf = np.cumsum(np.nan_to_num(v.fund), axis=0)
    total = price - (cf[e] - cf[b])
    out = []
    for sig in ("f7", "f30"):
        for label, fr in (("price", price), ("price + funding", total)):
            ics, ns = [], []
            for k in range(len(d)):
                m = v.tradable[d[k]] & np.isfinite(v.sig[sig][d[k]]) & np.isfinite(fr[k])
                if m.sum() >= 10:
                    x = xs.spearman(v.sig[sig][d[k], m], fr[k, m])
                    if np.isfinite(x):
                        ics.append(x)
                        ns.append(int(m.sum()))
            x = np.array(ics)
            h = len(x) // 2
            out.append(
                {
                    "venue": v.label,
                    "signal": "7-day funding" if sig == "f7" else "30-day funding",
                    "target": label,
                    "ic": float(x.mean()),
                    "t": float(x.mean() / x.std(ddof=1) * np.sqrt(len(x))),
                    "pos": float((x > 0).mean()),
                    "halves": [float(x[:h].mean()), float(x[h:].mean())],
                    "weeks": len(x),
                    "coins": float(np.mean(ns)),
                }
            )
    return out


def ar_spread(v: Venue, cm: cc.CostModel) -> list[dict[str, Any]]:
    """Abdi-Ranaldo (2017) spread from daily close, high, low, pooled over tradable coin-days by
    year and ADV third, next to the model's full spread. Descriptive (card)."""
    with np.errstate(invalid="ignore", divide="ignore"):
        c = np.log(v.px)
        eta = (np.log(v.hi) + np.log(v.lo)) / 2
    x = np.full_like(c, np.nan)
    x[:-1] = (c[:-1] - eta[:-1]) * (c[:-1] - eta[1:])
    ok = v.tradable & np.isfinite(x)
    third = np.full(c.shape, -1)
    for t in range(c.shape[0]):
        idx = np.flatnonzero(v.tradable[t] & np.isfinite(v.adv[t]))
        if len(idx) >= 3:
            order = idx[np.argsort(v.adv[t, idx])]
            for j, part in enumerate(np.array_split(order, 3)):
                third[t, part] = j
    yrs = np.array([(DAY0 + timedelta(days=i)).year for i in range(c.shape[0])])
    out = []
    for y in sorted(set(yrs[v.b0 :])):
        for j, name in enumerate(("low ADV", "mid ADV", "high ADV")):
            m = ok & (third == j) & (yrs == y)[:, None]
            if m.sum() < 500:
                continue
            mom = float(x[m].mean())
            out.append(
                {
                    "venue": v.label,
                    "year": int(y),
                    "third": name,
                    "coin_days": int(m.sum()),
                    "ar_bps": 2 * np.sqrt(max(mom, 0.0)) * 1e4,
                    "ar_moment_sign": "+" if mom > 0 else "-",
                    "model_bps": float(2 * cm.fit.half_spread(v.adv[m]).mean() * 1e4)  # type: ignore[union-attr]
                    * cm.m,
                    "adv_median": float(np.median(v.adv[m])),
                }
            )
    return out


# ---------------------------------------------------------------- calibration


def calibrate() -> None:
    folders = sorted(
        p for p in (raw() / "carry-3" / "book").iterdir() if (p / "done.json").exists()
    )
    if len(folders) < 3:
        raise SystemExit(f"the card needs three snapshots, found {len(folders)}")
    folders = folders[:3]
    times = [json.loads((p / "done.json").read_text()) for p in folders]
    snaps = [cc.read_snapshot(p) for p in folders]
    book_med = cc.median_snapshots(snaps)
    ensure_panels(cp.Grid())
    vols: dict[str, dict[str, float]] = {}
    for lab in ("B-all", "Bybit", "Hyperliquid"):
        v = Venue(lab, cp.Grid(), TRAIN_END)
        last = v.vol[-1]
        vols[v.venue] = {s: float(last[j]) for j, s in enumerate(v.names)}
        vols[v.venue][""] = float(np.median(last[v.tradable[-1]]))
    params = cc.calibrate(book_med, vols)
    for venue, rows in book_med.items():
        vol = np.array([r["vol24"] for r in rows.values()])
        hs = np.array([r["hs"] for r in rows.values()]) * 1e4
        cm = cc.model_from(params, venue)
        buckets = []
        for lo, hi in ((1e6, 5e6), (5e6, 2e7), (2e7, 1e8), (1e8, 1e9), (1e9, 1e13)):
            k = (vol >= lo) & (vol < hi)
            if not k.any():
                continue
            slip = {
                f"slip{q:.0f}": float(
                    np.median(
                        [
                            r[f"slip{q:.0f}"]
                            for r in rows.values()
                            if lo <= r["vol24"] < hi and f"slip{q:.0f}" in r
                        ]
                        or [np.nan]
                    )
                    * 1e4
                )
                for q in cc.CHECK_SIZES
            }
            buckets.append(
                {
                    "vol24": [lo, hi],
                    "coins": int(k.sum()),
                    "hs_median_bps": float(np.median(hs[k])),
                    "hs_model_bps": float(np.median(cm.fit.half_spread(vol[k])) * 1e4),  # type: ignore[union-attr]
                }
                | slip
            )
        params[venue]["buckets"] = buckets
        params[venue]["fees"] = list(cc.FEES[venue])
    out = {"snapshots": [{"name": p.name} | t for p, t in zip(folders, times, strict=True)]}
    COST_JSON.write_text(json.dumps(out | {"venues": params}, indent=1) + "\n")
    print(COST_JSON.read_text())


def models() -> dict[str, cc.CostModel]:
    if not COST_JSON.exists():
        raise SystemExit("no cost model: run --calibrate first (needs the three snapshots)")
    params = json.loads(COST_JSON.read_text())["venues"]
    return {v: cc.model_from(params, v) for v in cc.FEES}


# ---------------------------------------------------------------- report


def f(x: Any, fmt: str) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else format(x, fmt)


def table(title: str, rows: dict[str, dict[str, Any]], note: str = "") -> str:
    cols = ["Row", "Sharpe", "p(S>0)", "CAGR", "Max DD", "Worst week", "2020-21", "2022-25"]
    cols += [str(y) for y in YEARS]
    cols += ["Turn/yr", "Cost/side", "Fee/yr", "Spread/yr", "Impact/yr", "Funding/yr"]
    cols += ["Gross", "Blend", "Blend - twin (p)", "Blend DD", "BTC/ETH blend - alone (p)"]
    lines = [f"### {title}", ""]
    if note:
        lines += [note, ""]
    lines += ["| " + " | ".join(cols) + " |", "|---|" + "---:|" * (len(cols) - 1)]
    for k, r in rows.items():
        cells = [k, f(r["sharpe"], ".2f"), f(r.get("p_zero"), ".3f"), f(r["cagr"], "+.1%")]
        cells += [f(r["mdd"], ".0%"), f(r["worst_week"], "+.0%")]
        cells += [f(e, "+.2f") for e in r["eras"]] + [f(e, "+.2f") for e in r["years"]]
        cells += [f(r["turn_yr"], ".1f"), f(r["cost_side_bps"], ".1f") + " bps"]
        cells += [f(-c, "+.1%") for c in r["cost_yr"]] + [f(r["funding_yr"], "+.1%")]
        cells += [f(r["gross"], ".2f")]
        if "blend_p" in r:
            cells += [
                f(r["blend_sharpe"], ".2f"),
                f"{r['blend_diff']:+.2f} ({r['blend_p']:.3f})",
                f(r["blend_mdd"], ".0%"),
            ]
        else:
            cells += ["", "", ""]
        if "btc_blend_p" in r:
            cells.append(
                f"{r['btc_blend_sharpe']:.2f}: {r['btc_blend_diff']:+.2f} ({r['btc_blend_p']:.3f})"
            )
        else:
            cells.append("")
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def cost_section() -> str:
    j = json.loads(COST_JSON.read_text())
    snaps = ", ".join(f"{s['name']} ({s['started']} to {s['finished']})" for s in j["snapshots"])
    lines = [
        "## Cost model (calibrated on order-book snapshots, card)",
        "",
        f"Snapshots: {snaps}. Half-spread in bps = exp(a + b x log ADV); `R` = median measured"
        " cost of a market order / model (spread + impact, no fee) over coins with 24-hour volume"
        " >= 5M; `m` = the card's multiplier (1 unless a ratio is above 1.5).",
        "",
        "| Venue | Maker | Taker | Coins | In fit | a | b | Fit from | R(300 USD) | R(10,000 USD)"
        " | Too thin for 10,000 | m |",
        "|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|",
    ]
    for v, p in j["venues"].items():
        lines.append(
            f"| {v} | {p['fees'][0]:.3%} | {p['fees'][1]:.3%} | {p['coins']} | {p['coins_fit']} |"
            f" {p['a']:.2f} | {p['b']:.3f} | {p['source']} | {p['check_ratio']['300']:.2f} |"
            f" {p['check_ratio']['10000']:.2f} | {p['check_counts']['thin10000']} | {p['m']:.1f} |"
        )
    lines += [
        "",
        "Measured in the snapshots, by 24-hour volume (medians over coins, bps of the mid):",
        "",
        "| Venue | 24h volume | Coins | Half-spread measured | Half-spread model | Market order"
        " 300 USD | Market order 10,000 USD |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for v, p in j["venues"].items():
        for b in p["buckets"]:
            lo, hi = b["vol24"]
            rng = f"{lo / 1e6:.0f}M-{hi / 1e6:.0f}M" if hi < 1e12 else f">{lo / 1e6:.0f}M"
            lines.append(
                f"| {v} | {rng} | {b['coins']} | {b['hs_median_bps']:.2f} |"
                f" {b['hs_model_bps']:.2f} | {f(b['slip300'], '.2f')} |"
                f" {f(b['slip10000'], '.2f')} |"
            )
    return "\n".join(lines) + "\n"


def verdict_text(vd: dict[str, Any], defl: float | None = None) -> list[str]:
    out = [
        f"**`{vd['key']}`: {'PASSES train (bars 1-4)' if vd['train_pass'] else 'fails train'}**"
        f" (pooled p {vd['p']:.3f}; x5 {vd['p_x5']:.3f}; x7 {vd['p_x7']:.3f}"
        + (f"; deflated Sharpe probability {defl:.2f}" if defl is not None else "")
        + ")"
    ]
    out += [f"- bar {k}: {'yes' if ok else 'no'}" for k, ok in (vd["bars"] | vd["extra"]).items()]
    return out + [""]


# ---------------------------------------------------------------- runs


def run_all(
    grid: cp.Grid, last_decision: date, only: tuple[str, ...] | None
) -> tuple[dict[str, Venue], dict[str, dict[str, tuple[ce.Run, str]]], np.ndarray]:
    cms = models()
    p30 = [p.name.split("-")[1] for p in bb.derived().glob("binance-*-1h.npz")]
    venues = {
        "B-out": Venue("B-out", grid, last_decision, drop=set(p30)),
        "Bybit": Venue("Bybit", grid, last_decision),
        "Hyperliquid": Venue("Hyperliquid", grid, last_decision),
    }
    share = shares(venues, grid.n_days)
    runs = {}
    for lab, v in venues.items():
        runs[lab] = venue_rows(v, cms[v.venue], share, only)
        print("ran", lab, flush=True)
    return venues, runs, share


def train(log: bool) -> None:
    grid = cp.Grid()
    ensure_panels(grid)
    cms = models()
    venues, runs, share = run_all(grid, TRAIN_END, None)
    n_days = grid.n_days
    start = min(v.b0 for v in venues.values()) + 1
    first = DAY0 + timedelta(days=start)
    years = (n_days - start) / 365
    # B-all in place of B-out (robustness, band only)
    ball = Venue("B-all", grid, TRAIN_END)
    ball_runs = venue_rows(ball, cms["binance"], share, (PRIMARY,))
    keys = list(runs["B-out"])
    pooled = {
        k: pool_runs([(runs[lab][k][0], venues[lab].b0) for lab in POOL], start, n_days)
        for k in keys
    }
    alt = "band (B-all for B-out)"
    start2 = min(start, ball.b0 + 1)
    pooled[alt] = pool_runs(
        [(ball_runs[PRIMARY][0], ball.b0)]
        + [(runs[lab][PRIMARY][0], venues[lab].b0) for lab in POOL[1:]],
        start2,
        n_days,
    )
    kinds = {k: runs["B-out"][k][1] for k in keys} | {alt: "robustness"}
    btc = btc_eth_spot(start, n_days)
    btc_perp = btc_eth_perp(grid, TRAIN_END, start)
    tested = tuple(k for k in keys if k != "tsmom12 twin")
    # per venue
    per: dict[str, dict[str, dict[str, Any]]] = {}
    for lab, v in venues.items():
        rows = {k: summary(r, v.first(), v.years) for k, (r, _) in runs[lab].items()}
        add_tests(rows, {k: r.r for k, (r, _) in runs[lab].items()}, None, tested)
        per[lab] = rows
    pool_rows = {}
    for k, r in pooled.items():
        s0 = start2 if k == alt else start
        pool_rows[k] = summary(r, DAY0 + timedelta(days=s0), (n_days - s0) / 365)
    add_tests(pool_rows, {k: pooled[k].r for k in keys}, btc, tested)
    ball_rows = {k: summary(r, ball.first(), ball.years) for k, (r, _) in ball_runs.items()}
    add_tests(ball_rows, {k: r.r for k, (r, _) in ball_runs.items()}, None, (PRIMARY,))
    verdicts = {k: verdict(k, pool_rows, per) for k in VARIANTS}
    sh_var = float(np.var([pool_rows[k]["sharpe"] for k in VARIANTS], ddof=1))
    defl = stats.deflated_sharpe(pooled[PRIMARY].r, len(VARIANTS), sh_var)
    # the paper system's rule on the same days
    twin_btc = {
        "sharpe_spot": stats.sharpe(btc),
        "mdd_spot": stats.max_drawdown(btc),
        "sharpe_perp_close": stats.sharpe(btc_perp),
        "corr_spot_perp": float(np.corrcoef(btc, btc_perp)[0, 1]),
    }
    if log:
        last = TRAIN_END
        for lab, v in venues.items():
            for k, (r, kind) in runs[lab].items():
                log_row(f"carry-3-{lab}", k, kind, "train", v.first(), last, r)
        for k, r in pooled.items():
            log_row(
                "carry-3-pooled", f"{k}, equal capital per venue", kinds[k], "train", first, last, r
            )
        log_row(
            "carry-3-B-all",
            f"{PRIMARY} (robustness set)",
            "robustness",
            "train",
            ball.first(),
            last,
            ball_runs[PRIMARY][0],
        )
    # descriptive extras
    ics = [row for v in (*venues.values(), ball) for row in ic_rows(v)]
    ars = [row for v in venues.values() for row in ar_spread(v, cms[v.venue])]
    if log:
        for row in ics:
            log_row(
                f"carry-3-{row['venue']}",
                f"weekly cross-sectional IC, {row['signal']} vs next week's {row['target']}:"
                f" {row['ic']:+.3f} (t {row['t']:+.1f}, {row['weeks']} weeks)",
                "robustness",
                "train",
                venues.get(row["venue"], ball).first(),
                TRAIN_END,
                None,
            )
    # report
    vtxt: list[str] = []
    for k in (PRIMARY, *[x for x in VARIANTS if x != PRIMARY]):
        vtxt += verdict_text(verdicts[k], defl if k == PRIMARY else None)
    head = (
        "# Carry 3: raw tables (train, decisions to 2025-11-09)\n\n"
        "Script `lib/carry3.py`; card and reading in `research/carry-3.md`. Rows without a suffix"
        " are at the realistic cost: taker fee + modelled half-spread + square-root impact for a"
        " 10,000 USD account, smallest order 10 USD, plus every funding event. `nocost`: no"
        " trading cost; `flat10`/`flat30`: carry-2's flat 10/30 bps a side; `x2`: spread and impact"
        " doubled; `A100k`/`A1M`: account 100,000 / 1,000,000 USD; `maker`: 60% of each trade at"
        " the maker fee without spread; `top50`: only the 50 highest-ADV tradable coins per venue."
        " `Turn/yr`: traded value per year in multiples of the account. `Cost/side`: average cost"
        " per unit traded. `Fee/yr`, `Spread/yr`, `Impact/yr`, `Funding/yr`: share of equity per"
        " year. `Gross`: mean gross exposure. `p(S>0)`: one-sided stationary-bootstrap p. Blend:"
        " 50% twin + 50% the row. `tsmom12 twin`: long-only on the venue's perp closes, 30 bps,"
        " no funding. Last column (pooled only): 50% `tsmom12` on BTC/ETH spot (30 bps) + 50% the"
        " row: blend Sharpe, difference to BTC/ETH `tsmom12` alone, p.\n\n"
        f"BTC/ETH spot `tsmom12` on the pooled days ({first} on): Sharpe"
        f" {twin_btc['sharpe_spot']:.2f}, max drawdown {twin_btc['mdd_spot']:.0%} (the same rule"
        f" on Binance perp closes: {twin_btc['sharpe_perp_close']:.2f}, daily correlation"
        f" {twin_btc['corr_spot_perp']:.3f}).\n\n"
        "## Verdict (card bars)\n\n" + "\n".join(vtxt) + "\n"
    )

    def pick(rows: dict[str, dict[str, Any]], names: list[str]) -> dict[str, dict[str, Any]]:
        return {k: rows[k] for k in names if k in rows}

    main_rows = ["tsmom12 twin", *VARIANTS]
    rob = [k for k in pool_rows if k not in main_rows]
    body = [
        cost_section(),
        "## Pooled (B-out, Bybit, Hyperliquid; equal capital per venue)\n",
        table(
            f"Pooled: the five shapes at the realistic cost (first return day {first},"
            f" {years:.1f} years)",
            pick(pool_rows, main_rows),
        ),
        table("Pooled: robustness rows", pick(pool_rows, rob)),
    ]
    for lab, v in venues.items():
        note = (
            f"First return day {v.first()}, {v.years:.1f} years; coins with data {len(v.names)}"
            f" ({int(v.delisted.sum())} delisted); tradable per day median"
            f" {v.tradable_median:.0f}; weekly decisions {len(v.dw)}."
        )
        body.append(f"## {lab}\n")
        body.append(
            table(f"{lab}: the five shapes at the realistic cost", pick(per[lab], main_rows), note)
        )
        body.append(
            table(
                f"{lab}: robustness rows",
                pick(per[lab], [k for k in per[lab] if k not in main_rows]),
            )
        )
    body.append("## B-all (all Binance USDT-M perps; robustness, not part of the bars)\n")
    body.append(table("B-all", ball_rows))
    ic_lines = [
        "## Funding as an ML/RL input: weekly cross-sectional IC (train, descriptive)",
        "",
        "Spearman rank correlation across the tradable coins of a venue, each Friday, between the"
        " signal (minus the mean funding rate: high = cheap funding) and the coming week's return."
        " `price + funding` = the return of a long position including the funding it pays or"
        " receives.",
        "",
        "| Venue | Signal | Target | Mean IC | t | Weeks > 0 | First half / second half | Weeks"
        " | Coins |",
        "|---|---|---|---:|---:|---:|---|---:|---:|",
    ]
    for r in ics:
        ic_lines.append(
            f"| {r['venue']} | {r['signal']} | {r['target']} | {r['ic']:+.3f} | {r['t']:+.1f} |"
            f" {r['pos']:.0%} | {r['halves'][0]:+.3f} / {r['halves'][1]:+.3f} | {r['weeks']} |"
            f" {r['coins']:.0f} |"
        )
    body.append("\n".join(ic_lines) + "\n")
    ar_lines = [
        "## Did spreads drift? Abdi-Ranaldo estimate from daily bars (descriptive)",
        "",
        "Full spread in bps, pooled over tradable coin-days; `-` in the sign column means the"
        " pooled moment was negative (the estimate is then 0: noise larger than the spread)."
        " Model = twice the modelled half-spread on the same coin-days.",
        "",
        "| Venue | Year | ADV third | Coin-days | Median ADV | AR spread | Moment sign"
        " | Model spread |",
        "|---|---:|---|---:|---:|---:|---|---:|",
    ]
    for r in ars:
        ar_lines.append(
            f"| {r['venue']} | {r['year']} | {r['third']} | {r['coin_days']} |"
            f" {r['adv_median'] / 1e6:.0f}M | {r['ar_bps']:.0f} | {r['ar_moment_sign']} |"
            f" {r['model_bps']:.1f} |"
        )
    body.append("\n".join(ar_lines) + "\n")
    text = head + "\n".join(body)
    if log:
        flush_log()
    OUT.write_text(text)
    dump = {
        "verdicts": verdicts,
        "deflated": defl,
        "sharpe_var": sh_var,
        "twin_btc": twin_btc,
        "pool": pool_rows,
        "per": per,
        "ball": ball_rows,
        "ic": ics,
        "first": str(first),
    }
    (derived() / "results-train.json").write_text(json.dumps(dump, indent=1, default=str))
    np.savez(
        derived() / "train-series.npz",
        start=np.array(start),
        **{f"{lab}|{PRIMARY}": runs[lab][PRIMARY][0].r for lab in POOL},
        **{f"{lab}|b0": np.array(venues[lab].b0) for lab in POOL},
    )
    print(OUT.read_text())


def heldout(dry: bool = False) -> None:
    """The one held-out run. `dry`: the same code on the train panels, scoring train's last
    year, with no claim, no log row, no file and no number printed (a crash test only)."""
    res = derived() / "results-train.json"
    if not dry:
        if not res.exists():
            raise SystemExit("no train run found")
        vd = json.loads(res.read_text())["verdicts"][PRIMARY]
        if not vd["train_pass"]:
            raise SystemExit("the primary failed train: the held-out year stays unspent (card)")
        ce.claim_heldout(TRIES, f"{datetime.now(UTC):%Y-%m-%d %H:%M}")
    grid = cp.Grid() if dry else cp.Grid(cp.HELD_LAST_BAR)
    ensure_panels(grid)
    cms = models()
    venues, runs, share = run_all(grid, TRAIN_END if dry else HELD_END, (PRIMARY,))
    n_days = grid.n_days
    # look-ahead check: the train part of this run equals the train run
    stop = (date(2025, 11, 6) - DAY0).days  # the train run drops its last Friday (2025-11-07)
    if not dry:
        saved = np.load(derived() / "train-series.npz")
        for lab in POOL:
            b0 = venues[lab].b0
            assert b0 == int(saved[f"{lab}|b0"]), f"{lab}: start moved"
            a, b = runs[lab][PRIMARY][0].r[: stop - b0], saved[f"{lab}|{PRIMARY}"][: stop - b0]
            assert np.allclose(a, b, rtol=0, atol=1e-12), f"{lab}: train part differs"
    h0 = (date(2024, 11, 11) - DAY0).days if dry else (HELD_START - DAY0).days
    h1 = n_days - 1
    first, last = DAY0 + timedelta(days=h0), DAY0 + timedelta(days=h1)
    years = (h1 - h0 + 1) / 365

    def cut(r: ce.Run, b0: int) -> ce.Run:
        s = slice(h0 - b0 - 1, h1 - b0)
        return ce.Run(r.r[s], r.funding[s], r.gross[s], r.net[s], r.traded[s], r.cost[s])

    held: dict[str, dict[str, ce.Run]] = {}
    for lab, v in venues.items():
        cm = cms[v.venue]
        rows = {k: cut(r, v.b0) for k, (r, _) in runs[lab].items()}
        for label, model in (
            ("nocost", cm.but(flat=0.0)),
            ("flat10", cm.but(flat=0.001)),
            ("x2", cm.but(stress=2.0)),
        ):
            rr = venue_rows(v, model, share, (PRIMARY,))[PRIMARY][0]
            rows[f"{PRIMARY} {label}"] = cut(rr, v.b0)
        held[lab] = rows
    keys = list(held["B-out"])
    pooled = {k: mean_runs([held[lab][k] for lab in POOL]) for k in keys}
    start = min(v.b0 for v in venues.values()) + 1
    btc = btc_eth_perp(grid, TRAIN_END if dry else HELD_END, start)[h0 - start : h1 - start + 1]
    tested = tuple(k for k in keys if k != "tsmom12 twin")
    per = {}
    for lab in POOL:
        rows = {k: summary(r, first, years) for k, r in held[lab].items()}
        add_tests(rows, {k: r.r for k, r in held[lab].items()}, None, tested)
        per[lab] = rows
        for k, r in held[lab].items():
            kind = "variant" if k == PRIMARY else ("baseline" if "twin" in k else "robustness")
            log_row(f"carry-3-{lab}", k, kind, "heldout", first, last, r)
    pool_rows = {k: summary(r, first, years) for k, r in pooled.items()}
    add_tests(pool_rows, {k: r.r for k, r in pooled.items()}, btc, tested)
    for k, r in pooled.items():
        kind = "variant" if k == PRIMARY else ("baseline" if "twin" in k else "robustness")
        log_row("carry-3-pooled", f"{k}, equal capital per venue", kind, "heldout", first, last, r)
    p = pool_rows[PRIMARY]
    ok = p["sharpe"] > 0 and p["blend_diff"] >= 0
    lines = [
        f"# Carry 3: the one held-out run ({first} .. {last})",
        "",
        "Script `lib/carry3.py --heldout`; card in `research/carry-3.md`. The primary (`band`)"
        " only,"
        " at the realistic cost, simulated from the start of train so the band's state carries"
        " over; only the held-out days are scored. Same columns as `carry-3.md`'s tables; the"
        " per-year columns are empty (one year). The BTC/ETH `tsmom12` here is on Binance perp"
        f" closes standing in for spot (30 bps): Sharpe {stats.sharpe(btc):.2f} over the year.",
        "",
        f"**Held-out verdict: {'PASSES' if ok else 'FAILS'}** (pooled Sharpe {p['sharpe']:.2f} > 0:"
        f" {'yes' if p['sharpe'] > 0 else 'no'}; pooled blend not behind the twin:"
        f" {'yes' if p['blend_diff'] >= 0 else 'no'}, {p['blend_diff']:+.2f}).",
        "",
        table("Pooled (B-out, Bybit, Hyperliquid)", pool_rows),
    ]
    for lab, v in venues.items():
        m = v.tradable[h0 : h1 + 1].sum(1)
        note = (
            f"Tradable per day median {np.median(m):.0f}; coins delisted by the end"
            f" {int(v.delisted.sum())}."
        )
        lines.append(table(lab, per[lab], note))
    if dry:
        PENDING.clear()
        print(f"dry run ok: {len(lines)} blocks, {len(btc)} days scored, nothing written")
        return
    flush_log()  # result rows first: from here on the guard refuses any further run
    OUT_HELD.write_text("\n".join(lines))
    dump = {"pass": ok, "pool": pool_rows, "per": per, "btc_sharpe": stats.sharpe(btc)}
    (derived() / "results-heldout.json").write_text(json.dumps(dump, indent=1, default=str))
    print(OUT_HELD.read_text())


def check() -> None:
    """The copied code must be carry-2's book: `w1` at flat 10 bps and the twin, per venue and
    pooled, against `results/carry-2.md` (numbers already seen; nothing new is computed)."""
    grid = cp.Grid()
    ensure_panels(grid)
    p30 = [p.name.split("-")[1] for p in bb.derived().glob("binance-*-1h.npz")]
    venues = {
        "B-out": Venue("B-out", grid, TRAIN_END, drop=set(p30)),
        "Bybit": Venue("Bybit", grid, TRAIN_END),
        "Hyperliquid": Venue("Hyperliquid", grid, TRAIN_END),
    }
    share = shares(venues, grid.n_days)
    start = min(v.b0 for v in venues.values()) + 1
    want = {"B-out": (0.57, 0.07), "Bybit": (0.31, 0.20), "Hyperliquid": (0.47, 0.52)}
    parts: dict[str, list[tuple[ce.Run, int]]] = {"w1": [], "twin": []}
    for lab, v in venues.items():
        dw = v.dw
        tg = np.array([ce.long_short(v.sig["f7"][t], v.mask(t)) for t in dw])
        ref = se.simulate(v.px, v.fund, tg, dw, 0.001, v.b0)
        flat = cc.CostModel(v.venue, None, flat=0.001)
        mine = book(v, dw, lambda k, t, w, tg=tg: tg[k], flat, share, True)
        assert np.allclose(ref.r, mine.r, rtol=0, atol=1e-12), lab
        rows = venue_rows(v, flat, share, ("w1",))
        got = (stats.sharpe(rows["w1"][0].r), stats.sharpe(rows["tsmom12 twin"][0].r))
        print(
            f"{lab}: w1 flat10 {got[0]:.2f} (carry-2 {want[lab][0]}), twin {got[1]:.2f}"
            f" (carry-2 {want[lab][1]}), first {v.first()}, tradable {v.tradable_median:.0f}"
        )
        assert abs(got[0] - want[lab][0]) < 0.006 and abs(got[1] - want[lab][1]) < 0.006, lab
        parts["w1"].append((rows["w1"][0], v.b0))
        parts["twin"].append((rows["tsmom12 twin"][0], v.b0))
    for k, w in (("w1", 0.69), ("twin", 0.20)):
        got_p = stats.sharpe(pool_runs(parts[k], start, grid.n_days).r)
        print(f"pooled {k}: {got_p:.2f} (carry-2 {w})")
        assert abs(got_p - w) < 0.006, k
    print("check passed: the copy reproduces carry-2")


def main() -> None:
    if "--check" in sys.argv:
        check()
    elif "--heldout-dry" in sys.argv:
        heldout(dry=True)
    elif "--calibrate" in sys.argv:
        calibrate()
    elif "--heldout" in sys.argv:
        heldout()
    else:
        train("--log" in sys.argv)


if __name__ == "__main__":
    main()
