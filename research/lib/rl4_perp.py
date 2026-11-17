# ruff: noqa: E501
"""Run rl-4, part 2: the gate-passing learner on carry-2's perpetual-futures cross-section
(card part 2 in research/rl-4.md). Train period only; the held-out year is never loaded.

    uv run python -I research/lib/rl4_perp.py --ic            # the input IC table, no training
    uv run python -I research/lib/rl4_perp.py --run [--log]   # the books (after the IC table)

Reads carry-2's daily venue panels (`<cache_root>/derived/carry-2/`, bars after the train cut
already dropped). Four inputs per coin, known at Friday's close; the target is the coming week's
total return of a long position (price change minus funding paid). Without `--log` nothing is
written to tries.md. The pure helpers (inputs, targets, ranks, folds) take arrays, for the tests.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rl4_sup  # noqa: E402
from breadth_xs import ffill, logret, roll_std, spearman  # noqa: E402

INPUTS = ("funding", "premium", "mom_12_1", "vol")
EQUAL_SIGNS = np.array([-1.0, -1.0, 1.0, -1.0])  # textbook: low funding/premium, winners, calm
MIN_COINS = 10
MIN_ROWS = 1000  # protocol: no model before this many labelled rows
EMBARGO = 7
IC_BAR, T_BAR = 0.04, 2.0  # card part 2: the screen an input must pass before any training
PERP_COST, HIGH_COST, TWIN_COST = 0.001, 0.003, 0.003
RESULTS = Path(__file__).resolve().parents[1] / "results"


# --- pure helpers ---


def raw_inputs(px: np.ndarray, fund7: np.ndarray, prem7: np.ndarray) -> np.ndarray:
    """[days, n, 4] inputs known at each day's close: 7-day mean funding, 7-day mean premium,
    the log return from 365 to 30 days ago, the log of the 30-day volatility of daily returns."""
    fp = ffill(px)
    with np.errstate(invalid="ignore", divide="ignore"):
        mom = logret(fp, 365, 30)
        vol = np.log(roll_std(logret(fp, 1, 0), 30))
    vol[~np.isfinite(vol)] = np.nan
    return np.stack([fund7, prem7, mom, vol], axis=2)


def week_total(px: np.ndarray, fund: np.ndarray, t: int) -> np.ndarray:
    """Total log return of a long position decided at the close of day t and held 7 days: price
    change (a missing last price falls back to the last known one) minus the funding paid on
    return days t + 1 .. t + 7. NaN where there is no price on day t."""
    fp = ffill(px)
    with np.errstate(invalid="ignore", divide="ignore"):
        out: np.ndarray = np.log(fp[t + 7] / px[t]) - np.nan_to_num(fund[t + 1 : t + 8]).sum(0)
    return out


def centred_rank(x: np.ndarray, m: np.ndarray) -> np.ndarray:
    """Rank of x among the finite values inside m, scaled to -0.5 .. 0.5; 0 elsewhere."""
    out = np.zeros(len(x))
    idx = np.flatnonzero(m & np.isfinite(x))
    if len(idx) > 1:
        out[idx] = (
            np.argsort(np.argsort(x[idx], kind="mergesort"), kind="mergesort") / (len(idx) - 1)
            - 0.5
        )
    return out


def decision_days(tradable: np.ndarray, weekday0: int, last: int) -> np.ndarray:
    """Fridays (day indices) from the first day with MIN_COINS tradable coins to `last`, that
    have a full week of days after them. `weekday0` = weekday of day 0."""
    n_days = tradable.shape[0]
    cnt = tradable.sum(1)
    if not (cnt >= MIN_COINS).any():
        return np.array([], dtype=np.int64)
    s0 = int(np.argmax(cnt >= MIN_COINS))
    d = np.arange(s0, n_days)
    return d[((d + weekday0) % 7 == 4) & (d <= last) & (d + 7 < n_days)]


@dataclass
class Rows:
    day: np.ndarray  # [W] decision day index
    m: np.ndarray  # [W, n] coins in the cross-section that Friday
    x: np.ndarray  # [W, n, 4] centred ranks of the inputs (0 = missing or outside m)
    y: np.ndarray  # [W, n] centred rank of the coming week's total return
    fwd: np.ndarray  # [W, n] that return itself
    yz: np.ndarray  # [W, n] the return in percent as a z-score across the coins (addendum)
    raw: np.ndarray  # [W, n, 4] the inputs before ranking


def build_rows(
    px: np.ndarray, fund: np.ndarray, tradable: np.ndarray, raw: np.ndarray, days: np.ndarray
) -> Rows:
    w, n = len(days), px.shape[1]
    m = np.zeros((w, n), bool)
    x = np.zeros((w, n, raw.shape[2]))
    y = np.zeros((w, n))
    yz = np.zeros((w, n))
    fwd = np.full((w, n), np.nan)
    for i, t in enumerate(days):
        fwd[i] = week_total(px, fund, int(t))
        m[i] = tradable[t] & np.isfinite(px[t]) & np.isfinite(fwd[i])
        for k in range(raw.shape[2]):
            x[i, :, k] = centred_rank(raw[t, :, k], m[i])
        y[i] = centred_rank(fwd[i], m[i])
        ret = np.expm1(fwd[i, m[i]])
        if len(ret) > 1 and ret.std() > 0:
            yz[i, m[i]] = (ret - ret.mean()) / ret.std()
    return Rows(days, m, x, y, fwd, yz, raw[days])


def weekly_ic(rows: Rows, k: int) -> np.ndarray:
    """[W] Spearman correlation of input k with the coming week's total return (NaN if fewer
    than MIN_COINS coins have the input)."""
    out = np.full(len(rows.day), np.nan)
    for i in range(len(rows.day)):
        ok = rows.m[i] & np.isfinite(rows.raw[i, :, k])
        if ok.sum() >= MIN_COINS:
            out[i] = spearman(rows.raw[i, ok, k], rows.fwd[i, ok])
    return out


def usable(day: np.ndarray, fit_day: int) -> np.ndarray:
    """Rows a fit on `fit_day` may use: the target week ended EMBARGO days before it."""
    ok: np.ndarray = day + 7 + EMBARGO <= fit_day
    return ok


def walk_forward_sign(day: np.ndarray, ic: np.ndarray, fits: list[int]) -> np.ndarray:
    """[W] the sign an input would have been given at each week: the sign of its mean IC over
    the weeks usable at the latest fit day on or before it (0 before the first fit)."""
    out = np.zeros(len(day))
    for f in fits:
        past = usable(day, f) & np.isfinite(ic)
        if past.any():
            out[day >= f] = np.sign(ic[past].mean())
    return out


def long_short(score: np.ndarray, m: np.ndarray) -> np.ndarray:
    """carry-2's book: +0.5 over the top third of m by score, -0.5 over the bottom third.
    No position when the score does not separate the coins (a forecaster that found nothing)."""
    import short_engine as se

    if not m.any() or np.ptp(score[m]) == 0:
        return np.zeros(len(m))
    return se.long_short(score, m)


# --- the run (needs the cache) ---


def _day0() -> date:
    from carry2_panel import DAY0

    return DAY0


def _date(i: int) -> date:
    return _day0() + timedelta(days=int(i))


def _idx(d: date) -> int:
    return (d - _day0()).days


def fit_days() -> list[int]:
    from ml import first_friday

    return [_idx(first_friday(y)) for y in range(2021, 2026)]


def load() -> dict[str, tuple[Any, Rows]]:
    """carry-2's three sets (B-out, Bybit, Hyperliquid) with their weekly rows."""
    import breadth_books as bb
    import carry2
    from harness import TRAIN_END

    p30 = {p.name.split("-")[1] for p in bb.derived().glob("binance-*-1h.npz")}
    out = {}
    for v in (
        carry2.Venue("B-out", "binance", drop=p30),
        carry2.Venue("Bybit", "bybit"),
        carry2.Venue("Hyperliquid", "hyperliquid"),
    ):
        raw = raw_inputs(v.px, -v.sig["funding"], -v.sig["premium"])
        days = decision_days(v.tradable, _day0().weekday(), _idx(TRAIN_END))
        out[v.label] = (v, build_rows(v.px, v.fund, v.tradable, raw, days))
    return out


def _stat(x: np.ndarray) -> tuple[float, float, float, int]:
    x = x[np.isfinite(x)]
    if len(x) < 10:
        return float("nan"), float("nan"), float("nan"), len(x)
    t = float(x.mean() / x.std(ddof=1) * np.sqrt(len(x)))
    return float(x.mean()), t, float((x > 0).mean()), len(x)


def ic_table() -> dict[str, Any]:
    """Each input's weekly cross-sectional IC, per venue and pooled over venue-weeks, in sample
    and walk-forward (sign fixed from the past at each yearly fit)."""
    sets = load()
    fits = fit_days()
    res: dict[str, Any] = {"inputs": {}, "sets": {}}
    for label, (_, r) in sets.items():
        res["sets"][label] = {
            "first": str(_date(r.day[0])),
            "weeks": len(r.day),
            "coins_per_week": float(r.m.sum(1).mean()),
        }
    for k, name in enumerate(INPUTS):
        ics = {label: weekly_ic(r, k) for label, (_, r) in sets.items()}
        day = np.concatenate([sets[s][1].day for s in sets])
        pooled = np.concatenate([ics[s] for s in sets])
        sign = walk_forward_sign(day, pooled, fits)
        wf = np.where(sign != 0, sign * pooled, np.nan)
        first_fit = min(
            (f for f in fits if (usable(day, f) & np.isfinite(pooled)).any()), default=0
        )
        row: dict[str, Any] = {
            "pooled": _stat(pooled),
            "pooled_from_first_fit": _stat(np.where(day >= first_fit, pooled, np.nan)),
            "walk_forward": _stat(wf),
            "signs": sorted({float(s) for s in sign if s != 0}),
        }
        for label in sets:
            row[label] = _stat(ics[label])
        res["inputs"][name] = row
    best = max(res["inputs"].values(), key=lambda r: r["walk_forward"][0])
    res["screen_passed"] = bool(
        any(
            r["walk_forward"][0] >= IC_BAR and r["walk_forward"][1] >= T_BAR
            for r in res["inputs"].values()
        )
    )
    res["best_walk_forward"] = best["walk_forward"][0]
    return res


def write_ic(res: dict[str, Any]) -> None:
    def cell(s: tuple[float, float, float, int]) -> str:
        return f"{s[0]:+.3f} ({s[1]:+.1f})" if np.isfinite(s[0]) else "-"

    sets = list(res["sets"])
    L = [
        "# RL 4, part 2: weekly IC of the four inputs on the perp cross-section (train only)",
        "",
        "Script `lib/rl4_perp.py --ic` (descriptive, no backtest, no training). IC = Spearman rank",
        "correlation, across the tradable coins of one venue on one Friday, between the input and the",
        "coming week's total return of a long position (price change minus funding paid); mean over",
        "weeks, t-statistic in brackets. Pooled = all venue-weeks. Walk-forward = the same, but the",
        "input's sign is set at each yearly fit from the weeks before it (7-day embargo), and only",
        "weeks after the first fit count. carry-2's sets, decisions to 2025-11-09.",
        "",
        "| Set | First decision | Weeks | Coins per week |",
        "|---|---|---:|---:|",
    ]
    for s in sets:
        i = res["sets"][s]
        L.append(f"| {s} | {i['first']} | {i['weeks']} | {i['coins_per_week']:.0f} |")
    L += [
        "",
        "| Input | Pooled IC (t) | Pooled, weeks after the first fit | **Walk-forward IC (t)** | Share of weeks > 0 | Sign used | "
        + " | ".join(sets)
        + " |",
        "|---|---:|---:|---:|---:|---|" + "---:|" * len(sets),
    ]
    for name, r in res["inputs"].items():
        sign = "/".join("+" if s > 0 else "-" for s in r["signs"]) or "-"
        L.append(
            f"| `{name}` | {cell(r['pooled'])} | {cell(r['pooled_from_first_fit'])} | **{cell(r['walk_forward'])}** "
            f"| {r['walk_forward'][2]:.0%} | {sign} | "
            + " | ".join(cell(r[s]) for s in sets)
            + " |"
        )
    L += [
        "",
        f"Screen (card part 2): an input passes with a walk-forward IC of at least {IC_BAR} and t of at"
        f" least {T_BAR:g}. **{'Passed' if res['screen_passed'] else 'Not passed'}**: the best"
        f" walk-forward IC is {res['best_walk_forward']:+.3f}.",
    ]
    (RESULTS / "rl-4-perp-ic.md").write_text("\n".join(L) + "\n")


def why_table() -> None:
    """Post-hoc, descriptive: what a long-short third-against-third book on each input earns a
    week before costs, next to the input's rank IC. Written after the books had been seen."""
    sets = load()
    L = [
        "# RL 4, part 2: why a good rank forecast made no money (post-hoc, descriptive)",
        "",
        "Script `lib/rl4_perp.py --why`, written after `results/rl-4-perp.md` had been seen; no",
        "backtest, no costs. For each input, every venue-week (at least 10 coins with the input): the",
        "coins are split into thirds by the input. Long third = the side the rank IC favours. Return",
        "= the week's total return of a long position in plain percent (price change minus funding),",
        "equal weight inside a third. Spread = long third minus short third: what the book's two",
        "legs earn together per unit of gross exposure x 2. All venue-weeks from 2021-02 to 2025-11.",
        "",
        "| Input | Long side | Rank IC | Mean return, long third | Mean return, short third | **Mean spread per week (t)** | Median coin, long third | Median coin, short third | Weeks spread > 0 | Worst week's spread | Best week's spread |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for k, name in enumerate(INPUTS):
        ics, lo, hi, mlo, mhi = [], [], [], [], []
        for _, r in sets.values():
            for i in range(len(r.day)):
                ok = r.m[i] & np.isfinite(r.raw[i, :, k])
                if ok.sum() < MIN_COINS:
                    continue
                x = r.raw[i, ok, k]
                ret = np.expm1(r.fwd[i, ok])  # log total return -> percent (funding is small)
                order = np.argsort(x, kind="mergesort")
                n3 = max(1, round(len(x) / 3))
                ics.append(spearman(x, ret))
                lo.append(ret[order[:n3]].mean())
                hi.append(ret[order[-n3:]].mean())
                mlo.append(float(np.median(ret[order[:n3]])))
                mhi.append(float(np.median(ret[order[-n3:]])))
        ic = float(np.mean(ics))
        a, b, ma, mb = (np.array(v) for v in ((lo, hi, mlo, mhi) if ic < 0 else (hi, lo, mhi, mlo)))
        sp = a - b
        t = float(sp.mean() / sp.std(ddof=1) * np.sqrt(len(sp)))
        L.append(
            f"| `{name}` | {'low' if ic < 0 else 'high'} | {ic:+.3f} | {a.mean():+.2%} | {b.mean():+.2%} "
            f"| **{sp.mean():+.2%} ({t:+.1f})** | {ma.mean():+.2%} | {mb.mean():+.2%} | {(sp > 0).mean():.0%} "
            f"| {sp.min():+.1%} | {sp.max():+.1%} |"
        )
    (RESULTS / "rl-4-perp-why.md").write_text("\n".join(L) + "\n")
    print((RESULTS / "rl-4-perp-why.md").read_text())


def fold_models(
    sets: dict[str, tuple[Any, Rows]], kind: str, target: str = "rank"
) -> dict[int, rl4_sup.Fit]:
    """One pooled model per yearly fit day that has MIN_ROWS usable rows. Target: the week's
    return as a rank (card part 2) or as a z-score of the return itself (the addendum)."""
    out = {}
    for f in fit_days():
        xs, ys, ds = [], [], []
        for _, r in sets.values():
            ok = usable(r.day, f)
            mm = r.m[ok]
            xs.append(r.x[ok][mm])
            ys.append((r.y if target == "rank" else r.yz)[ok][mm])
            ds.append(np.repeat(r.day[ok][:, None], r.m.shape[1], 1)[mm])
        x, y, d = np.concatenate(xs), np.concatenate(ys), np.concatenate(ds)
        if len(y) >= MIN_ROWS:
            out[f] = rl4_sup.fit(kind, x, y / y.std(), d)
    return out


def summary(r: np.ndarray, first: date) -> dict[str, Any]:
    import stats

    yrs = np.array([(first + timedelta(days=i)).year for i in range(len(r))])
    eq = np.cumprod(1 + r)
    return {
        "sharpe": stats.sharpe(r),
        "cagr": stats.cagr(r),
        "mdd": stats.max_drawdown(r),
        "worst_week": float((eq[7:] / eq[:-7] - 1).min()) if len(r) > 7 else float("nan"),
        "years": {
            int(y): stats.sharpe(r[yrs == y]) for y in np.unique(yrs) if (yrs == y).sum() >= 180
        },
    }


def compare(series: dict[str, np.ndarray], rows: dict[str, dict[str, Any]]) -> None:
    """Adds p(S>0), the blend with the twin, and `ls-ml` against the two long-short baselines."""
    import stats

    tw = series["tsmom12 twin"]
    for key, r in series.items():
        rows[key]["corr_twin"] = float(np.corrcoef(r, tw)[0, 1]) if r.std() > 0 else 0.0
        if key.startswith("ls-"):
            blend = 0.5 * tw + 0.5 * r
            d, p, _, _ = stats.sharpe_diff_boot(blend, tw)
            _, p0, _, _ = stats.sharpe_diff_boot(r, np.zeros_like(r))
            rows[key] |= {"p_zero": p0, "blend_sharpe": stats.sharpe(blend), "blend_diff": d,
                          "blend_p": p, "blend_mdd": stats.max_drawdown(blend)}  # fmt: skip
    for key in [k for k in series if k.startswith("ls-ml")]:
        tail = key[len("ls-ml") :]
        for other in ("ls-funding", "ls-equal"):
            d, p, _, _ = stats.sharpe_diff_boot(series[key], series[other + tail])
            rows[key] |= {f"vs_{other}": d, f"vs_{other}_p": p}


def run_books(kind: str, log: bool, target: str = "rank") -> dict[str, Any]:
    import breadth_books as bb
    import short_engine as se

    tag = "" if target == "rank" else f"-{target}"  # the addendum logs only its own book
    sets = load()
    models = fold_models(sets, kind, target)
    fits = sorted(models)
    out: dict[str, Any] = {"sets": {}, "models": {}}
    for f in fits:
        m = models[f]
        out["models"][str(_date(f))] = {
            "penalty": m.penalty,
            "beta": dict(zip(INPUTS, m.beta.tolist(), strict=True)),
        }
    for label, (v, r) in sets.items():
        dw = r.day[r.day >= fits[0]]
        if len(dw) < 2:
            continue
        sel = np.searchsorted(r.day, dw)
        fc = np.zeros((len(dw), v.px.shape[1]))
        for i, (j, t) in enumerate(zip(sel, dw, strict=True)):
            fc[i] = models[max(f for f in fits if f <= t)].score(r.x[j])
        ics = [
            spearman(fc[i][r.m[j]], r.fwd[j][r.m[j]])
            for i, j in enumerate(sel)
            if r.m[j].sum() >= MIN_COINS and np.ptp(fc[i][r.m[j]]) > 0
        ]
        up = v.up
        targets = {
            "ls-ml": np.array([long_short(fc[i], r.m[j]) for i, j in enumerate(sel)]),
            "ls-funding": np.array(
                [long_short(-r.raw[j, :, 0], r.m[j] & np.isfinite(r.raw[j, :, 0])) for j in sel]
            ),
            "ls-equal": np.array([long_short(r.x[j] @ EQUAL_SIGNS, r.m[j]) for j in sel]),
            "tsmom12 twin": np.array(
                [
                    np.where(r.m[j] & up[t], 1.0 / max(r.m[j].sum(), 1), 0.0)
                    for j, t in zip(sel, dw, strict=True)
                ]
            ),
        }
        b0 = int(dw[0])
        first = _date(b0 + 1)
        years = (v.px.shape[0] - b0) / 365
        series: dict[str, np.ndarray] = {}
        rows: dict[str, dict[str, Any]] = {}
        for name, tg in targets.items():
            twin = name == "tsmom12 twin"
            turn = float(np.abs(np.diff(tg, axis=0)).sum() / years)
            for cost in [TWIN_COST] if twin else [PERP_COST, HIGH_COST]:
                run = se.simulate(v.px, None if twin else v.fund, tg, dw, cost, b0)
                key = name if cost != HIGH_COST or twin else f"{name} @30"
                series[key] = run.r
                rows[key] = summary(run.r, first) | {
                    "funding_yr": float(run.funding.sum() / years),
                    "turn_yr": turn,
                }
                if log and (not tag or name == "ls-ml"):
                    kd = (
                        "robustness"
                        if key.endswith("@30")
                        else ("variant" if name == "ls-ml" else "baseline")
                    )
                    cd = (
                        "perp close as spot, 30 bps"
                        if twin
                        else f"perp {cost * 1e4:.0f} bps + funding"
                    )
                    bb.log_row(f"rl-4-perp-{label}", f"{name}{tag}, {cd}", kd, first, run.r, turn)
        compare(series, rows)
        out["sets"][label] = {"first": str(first), "years": years, "weeks": len(dw), "b0": b0,
                              "coins": float(r.m[sel].sum(1).mean()), "rows": rows, "series": series,
                              "forecast_ic": _stat(np.array(ics))}  # fmt: skip
    # pooled: equal capital per venue book on each day it exists
    outs = list(out["sets"].values())
    start = min(o["b0"] for o in outs) + 1
    n = len(next(iter(sets.values()))[0].px) - start
    series = {}
    for k in outs[0]["series"]:
        tot, cnt = np.zeros(n), np.zeros(n)
        for o in outs:
            off = o["b0"] + 1 - start
            tot[off:] += o["series"][k]
            cnt[off:] += 1
        series[k] = tot / cnt
    first = _date(start)
    rows = {
        k: summary(s, first) | {"funding_yr": float("nan"), "turn_yr": float("nan")}
        for k, s in series.items()
    }
    if log:
        for k, s in series.items():
            if tag and not k.startswith("ls-ml"):
                continue
            kd = "robustness" if k.endswith("@30") else ("variant" if k == "ls-ml" else "baseline")
            nm = k.replace("ls-ml", f"ls-ml{tag}")
            bb.log_row(
                "rl-4-perp-pooled", f"{nm}, equal capital per venue", kd, first, s, float("nan")
            )
    compare(series, rows)
    out["pooled"] = {"first": str(first), "years": n / 365, "rows": rows}
    out["bars"] = bars(out)
    for o in outs:
        o.pop("series")
    return out


def bars(out: dict[str, Any]) -> dict[str, bool]:
    """Card part 2, `ls-ml` at 10 bps + funding."""
    p = out["pooled"]["rows"]["ls-ml"]
    s = out["sets"]
    other = [
        s[k]["rows"]["ls-ml"]["sharpe"] > 0
        for k in ("Bybit", "Hyperliquid")
        if k in s and s[k]["weeks"] >= 52
    ]
    return {
        "1 pooled Sharpe > 0, p < 0.10": p["sharpe"] > 0 and p["p_zero"] < 0.10,
        "2 beats ls-funding, p < 0.10": p["vs_ls-funding"] > 0 and p["vs_ls-funding_p"] < 0.10,
        "3 not behind ls-equal": p["vs_ls-equal"] >= 0,
        "4 B-out > 0 and Bybit or Hyperliquid > 0": s["B-out"]["rows"]["ls-ml"]["sharpe"] > 0
        and any(other),
        "5 pooled blend beats the twin, p < 0.10": p["blend_diff"] > 0 and p["blend_p"] < 0.10,
    }


def f(x: Any, fmt: str) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else format(x, fmt)


def write_books(out: dict[str, Any], kind: str, target: str = "rank") -> Path:
    tag = "" if target == "rank" else f"-{target}"
    L = [
        "# RL 4, part 2: the gate-passing learner on the perp cross-section (train only)",
        "",
        *(
            []
            if not tag
            else [
                "**Addendum run (`ls-ml-ret`, post-hoc):** here `ls-ml` is trained on the week's return",
                "itself (percent, as a z-score across the venue's coins), not on its rank. Everything",
                "else is as in `results/rl-4-perp.md`.",
                "",
            ]
        ),
        f"Script `lib/rl4_perp.py --run`; card part 2 in `research/rl-4.md`. `ls-ml`: {kind} on the four",
        "ranked inputs, refitted on the first Friday of each year on every earlier venue-week (7-day",
        "embargo); long the top third of its forecast, short the bottom third, per venue. `ls-funding`:",
        "carry-2's book on the same days. `ls-equal`: the four inputs averaged with fixed signs, no",
        "fitting. 10 bps a side plus every funding event; `@30` the same at 30 bps. `tsmom12 twin`:",
        "long-only, 30 bps, no funding. Sharpe on daily returns, 365 days. p: one-sided stationary",
        "bootstrap. Pooled: equal capital per venue book on each day it exists.",
        "",
        "## Verdict (card part 2 bars, `ls-ml`)",
        "",
    ]
    L += [f"- bar {k}: {'yes' if ok else 'no'}" for k, ok in out["bars"].items()]
    L += ["", f"**{'PASSES' if all(out['bars'].values()) else 'does not pass'}**", "", "## The models", "",
          "| Fitted on | Penalty | " + " | ".join(f"`{k}`" for k in INPUTS) + " |", "|---|---:|" + "---:|" * len(INPUTS)]  # fmt: skip
    for d, m in out["models"].items():
        L.append(
            f"| {d} | {f(m['penalty'], 'g')} | "
            + " | ".join(f(m["beta"][k], "+.3f") for k in INPUTS)
            + " |"
        )
    L += ["", "Weights are on ranked, standardised inputs, for a target with unit spread: a weight is roughly",
          "that input's own IC after the penalty."]  # fmt: skip
    for label, o in [("Pooled", out["pooled"]), *out["sets"].items()]:
        yrs = sorted({y for r in o["rows"].values() for y in r["years"]})
        head = f"### {label}\n\nFirst return day {o['first']}, {o['years']:.1f} years."
        if "coins" in o:
            ic = o["forecast_ic"]
            head += (f" Weekly decisions {o['weeks']}, coins per week {o['coins']:.0f}. Forecast's weekly IC out of"
                     f" sample {f(ic[0], '+.3f')} (t {f(ic[1], '+.1f')}).")  # fmt: skip
        cols = ["Book", "Sharpe", "CAGR", "Max DD", "Worst week", *[str(y) for y in yrs], "Funding/yr", "Turn/yr",
                "Corr twin", "p(S>0)", "vs ls-funding (p)", "vs ls-equal (p)", "Blend", "Blend - twin (p)"]  # fmt: skip
        L += ["", head, "", "| " + " | ".join(cols) + " |", "|---|" + "---:|" * (len(cols) - 1)]
        for k, r in o["rows"].items():
            cells = [
                k,
                f(r["sharpe"], ".2f"),
                f(r["cagr"], "+.1%"),
                f(r["mdd"], ".0%"),
                f(r["worst_week"], "+.0%"),
            ]
            cells += [f(r["years"].get(y), "+.2f") for y in yrs]
            cells += [
                f(r["funding_yr"], "+.1%"),
                f(r["turn_yr"], ".0f"),
                f(r["corr_twin"], "+.2f"),
                f(r.get("p_zero"), ".3f"),
            ]
            for o2 in ("ls-funding", "ls-equal"):
                cells.append(
                    f"{r[f'vs_{o2}']:+.2f} ({r[f'vs_{o2}_p']:.2f})" if f"vs_{o2}" in r else ""
                )
            cells += [
                f(r.get("blend_sharpe"), ".2f"),
                f"{r['blend_diff']:+.2f} ({r['blend_p']:.2f})" if "blend_p" in r else "",
            ]
            L.append("| " + " | ".join(cells) + " |")
    path = RESULTS / f"rl-4-perp{tag}.md"
    path.write_text("\n".join(L) + "\n")
    return path


def main() -> None:
    import macro

    d = macro.cache_root() / "derived" / "rl-4"
    d.mkdir(parents=True, exist_ok=True)
    if "--ic" in sys.argv:
        res = ic_table()
        (d / "ic.json").write_text(json.dumps(res, indent=1))
        write_ic(res)
        print((RESULTS / "rl-4-perp-ic.md").read_text())
    elif "--why" in sys.argv:
        why_table()
    elif "--smoke" in sys.argv:  # plumbing check: runs everything, logs and prints no number
        out = run_books("lasso", False, "ret")
        print("ok", sorted(out["sets"]), len(out["models"]), "models")
    elif "--run" in sys.argv:
        kind = next((a.split("=")[1] for a in sys.argv if a.startswith("--fit=")), "lasso")
        target = next((a.split("=")[1] for a in sys.argv if a.startswith("--target=")), "rank")
        out = run_books(kind, "--log" in sys.argv, target)
        tag = "" if target == "rank" else f"-{target}"
        (d / f"books{tag}.json").write_text(json.dumps(out, indent=1, default=str))
        print(write_books(out, kind, target).read_text())


if __name__ == "__main__":
    main()
