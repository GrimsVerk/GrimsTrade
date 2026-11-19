"""combo-1, step 1: the failure map of the most credible models against `tsmom12`.

    uv run --with numpy python research/lib/combo1_map.py

No backtest is run and nothing is logged: every series is a configuration already in a lane's
`tries.md`, read from saved output.

- deep-1's sleeve series (`<cache_root>/derived/deep-1/series/six/*.npz`): `tsmom12`,
  `trend-vol`, `inverse-vol`, `sixty-forty`, `equal-weight` (the market yardstick for the cuts).
- Saved equity curves of finished lanes, copied read-only to
  `<cache_root>/derived/combo-1/inputs/`: `where-vol` (trend-where), `stop-0.25` (cointop-1).
- carry-3's train series (`<cache_root>/derived/carry-3/train-series.npz`): the `band` carry
  book per venue; the map uses the mean of the venues that exist on a day.

Writes research/results/combo-1-map.md and `<cache_root>/derived/combo-1/map.json`.
"""

from __future__ import annotations

import csv
import json
import math
from collections.abc import Callable
from datetime import date, timedelta

import deep1_atlas as da
import deep1_models as dm
import numpy as np
import stats
from harness import ERAS, STRESS, TRAIN_END

OUT = dm.macro.cache_root() / "derived" / "combo-1"
INPUTS = OUT / "inputs"
CARRY = dm.macro.cache_root() / "derived" / "carry-3" / "train-series.npz"
CARRY_DAY0 = date(2019, 9, 1)  # carry3_panel.DAY0: index i of a venue is day DAY0 + b0 + 1 + i
RESULT = dm.harness.RESEARCH / "results" / "combo-1-map.md"

MODELS = ["trend-vol", "where-vol", "stop-0.25", "inverse-vol", "sixty-forty", "band"]
WHY = {
    "trend-vol": "deep-1's best risk shape: trend with volatility-sized slots (run 1, tv40)",
    "where-vol": "trend-where: filter kept only where days out were rougher (1.07)",
    "stop-0.25": "cointop-1/coin-cap: 25% stop on the coin slots (1.09, worst loss 28.9%)",
    "inverse-vol": "always invested, risk-sized: the opposite of stepping out",
    "sixty-forty": "the lowest loss-week correlation with `tsmom12` in deep-1's pool (0.44)",
    "band": "carry-3: funding carry on perps, another source of return (2021-25 only)",
}
ERA5 = [e for e in ERAS if e[1].year >= 1994]
REBOUND = 182
WEEK = 7


def equity_rets(path: str, days: np.ndarray) -> np.ndarray:
    """Daily returns of a saved equity curve on the atlas calendar (NaN where absent)."""
    n = len(days) - 1
    r = np.full(n, np.nan)
    with (INPUTS / path).open() as f:
        rows = [(date.fromisoformat(x["date"]), float(x["equity"])) for x in csv.DictReader(f)]
    off = rows[0][0].toordinal() - int(days[0])
    eq = np.array([e for _, e in rows])
    k = min(len(eq) - 1, n - off)
    r[off : off + k] = eq[1 : k + 1] / eq[:k] - 1
    return r


def carry_rets(days: np.ndarray) -> np.ndarray:
    """Mean over the venues that exist on a day of carry-3's `band` daily return."""
    z = np.load(CARRY, allow_pickle=False)
    n = len(days) - 1
    acc, cnt = np.zeros(n), np.zeros(n)
    for lab in ("B-out", "Bybit", "Hyperliquid"):
        x = z[f"{lab}|band"]
        first = (CARRY_DAY0 + timedelta(days=int(z[f"{lab}|b0"]) + 1)).toordinal()
        off = first - int(days[0]) - 1  # return index of that day
        k = min(len(x), n - off)
        acc[off : off + k] += x[:k]
        cnt[off : off + k] += 1
    return np.where(cnt > 0, acc / np.maximum(cnt, 1), np.nan)


def masks(a: da.Atlas) -> dict[str, np.ndarray]:
    """The regime cuts, one boolean per return day. Descriptions on the full train sample: the
    thresholds may use the whole period (nothing here is traded)."""
    ts = a.rets["tsmom12"]
    ew = a.rets["equal-weight"]
    n = len(ts)
    out: dict[str, np.ndarray] = {}
    eq_ew = np.concatenate([[1.0], np.cumprod(1 + ew)])
    # trend state (deep-1's): tsmom12's book share at the decision in force
    tstate = da.trend_state(a)
    for k, nm in enumerate(da.STATES):
        out[f"trend {nm}"] = tstate == k
    # chop: tsmom12 slot changes (entries + exits) over the trailing 91 days >= 3
    held = a.w["tsmom12"] > 0
    flips = np.concatenate([[0], (held[1:] != held[:-1]).sum(axis=1)])
    c91 = np.convolve(flips, np.ones(91), mode="full")[:n]
    out["chop (>=3 flips/13 wk)"] = c91 >= 3
    # crash speed on the always-invested book: fast = the trailing 21-day fall is in its worst
    # 5% of days; slow bear = the trailing 365-day return is below zero
    r21 = np.full(n, np.nan)
    r365 = np.full(n, np.nan)
    r21[21:] = eq_ew[22:] / eq_ew[1:-21] - 1
    r365[365:] = eq_ew[366:] / eq_ew[1:-365] - 1
    cut = np.nanquantile(r21, 0.05)
    out["fast fall (21-day, worst 5%)"] = np.nan_to_num(r21, nan=1.0) <= cut
    out["slow bear (12-mo below 0)"] = np.nan_to_num(r365, nan=1.0) < 0
    # rate regime: stocks and bonds moving together (trailing ~1 year of SPY/TLT daily returns)
    j_s, j_t = a.syms.index("SPY"), a.syms.index("TLT")
    s, t = a.assets[:, j_s], a.assets[:, j_t]
    both = (s != 0) & (t != 0)
    sb = np.full(n, np.nan)
    for k in range(365, n):
        m = both[k - 365 : k]
        if m.sum() > 200:
            sb[k] = np.corrcoef(s[k - 365 : k][m], t[k - 365 : k][m])[0, 1]
    out["stock-bond corr > 0 (1y)"] = np.nan_to_num(sb, nan=-1.0) > 0
    # tsmom12's ten deepest drawdowns: into the fall, and the six months after the low
    down = np.zeros(n, bool)
    back = np.zeros(n, bool)
    for e in da.episodes(ts, 10):
        down[e.peak : e.trough + 1] = True
        back[e.trough + 1 : min(n, e.trough + 1 + REBOUND)] = True
    out["tsmom12 top-10 falls (peak to low)"] = down
    out["6 months after those lows"] = back
    # tsmom12 losing weeks, as days
    wk = n // WEEK
    tw = da.weekly(ts)
    lose = np.zeros(n, bool)
    lose[: wk * WEEK] = np.repeat(tw < 0, WEEK)
    out["tsmom12 losing weeks"] = lose
    return out


def ann(x: np.ndarray) -> float:
    return float(np.nanmean(x) * 365) if np.isfinite(x).sum() > 30 else math.nan


def pc(x: float, spec: str = "+.1f") -> str:
    return "-" if math.isnan(x) else format(x * 100, spec)


def f2(x: float, spec: str = "+.2f") -> str:
    return "-" if math.isnan(x) else format(x, spec)


def wk_mask(m: np.ndarray) -> np.ndarray:
    """A week belongs to a regime if at least four of its seven days do."""
    k = len(m) // WEEK
    return m[: k * WEEK].reshape(k, WEEK).sum(axis=1) >= 4


def main() -> None:
    a = da.load()
    days = a.days
    n = len(days) - 1
    r: dict[str, np.ndarray] = {
        "tsmom12": a.rets["tsmom12"],
        "trend-vol": a.rets["trend-vol"],
        "where-vol": equity_rets("where-vol.train.csv", days),
        "stop-0.25": equity_rets("stop-0.25.train.csv", days),
        "inverse-vol": a.rets["inverse-vol"],
        "sixty-forty": a.rets["sixty-forty"],
        "band": carry_rets(days),
    }
    ts = r["tsmom12"]
    ex = {m: r[m] - ts for m in MODELS}
    last = date.fromordinal(int(days[-1]))
    assert last <= TRAIN_END + timedelta(days=1)
    M = masks(a)

    def idx(d: date) -> int:
        return int(np.clip(d.toordinal() - int(days[0]) - 1, 0, n - 1))

    def span(m: str) -> np.ndarray:
        return np.isfinite(r[m])

    out = ["# combo-1, step 1: the failure map", ""]
    out += [
        "Plan and reading: `combo-1.md`. Six live assets, train period (decisions 1994-02-01 .. "
        "2025-11-09), total-return prices, protocol costs (30 bps crypto, 2 bps ETFs). Sharpe on "
        "calendar days. Excess = model's daily return minus `tsmom12`'s on the same day, "
        "annualised (x 365), in percent a year. Nothing here was run anew or selected: every "
        "series is a logged configuration read from saved output. `band` (perp funding carry) "
        f"exists only from {date.fromordinal(int(days[0]) + 1 + int(np.argmax(span('band'))))}; "
        "its cells cover its own span.",
        "",
        "| Model | Why it is on the map |",
        "|---|---|",
        *[f"| `{m}` | {WHY[m]} |" for m in MODELS],
        "",
    ]

    # 1. eras
    wins = [("all", date(1994, 2, 1), last), ("2003-25", date(2003, 1, 1), last)] + ERA5
    rows = []
    for m in ["tsmom12", *MODELS]:
        row = f"| `{m}` |"
        for _, lo, hi in wins:
            x = r[m][idx(lo) : idx(hi) + 1]
            ok = np.isfinite(x)
            row += f" {f2(stats.sharpe(x[ok]), '.2f') if ok.sum() > 250 else '-'} |"
        x = r[m][span(m)]
        row += f" {pc(stats.cagr(x))} | {stats.max_drawdown(x) * 100:.1f} |"
        rows.append(row)
    out += [
        "## 1. Sharpe by era",
        "",
        "| Model |" + "".join(f" {w[0]} |" for w in wins) + " Growth %/yr | Worst loss % |",
        "|---|" + "---:|" * (len(wins) + 2),
        *rows,
        "",
    ]

    # 2. excess by regime
    order = list(M)
    rows = []
    share = {k: float(M[k].mean()) for k in order}
    for m in MODELS:
        row = f"| `{m}` |"
        for k in order:
            sel = M[k] & span(m)
            row += f" {pc(ann(ex[m][sel]))} |" if sel.sum() > 30 else " - |"
        rows.append(row)
    rows.append("| *`tsmom12` own return* |" + "".join(f" *{pc(ann(ts[M[k]]))}* |" for k in order))
    rows.append("| *share of days* |" + "".join(f" *{share[k] * 100:.0f}%* |" for k in order))
    out += [
        "## 2. Where each model loses to `tsmom12`: excess return by regime (% a year)",
        "",
        "Negative = the model earns less than `tsmom12` in that regime. Regimes (descriptions "
        "on the whole sample): trend state = share of eligible assets `tsmom12` holds (off <= "
        "1/3, on >= 2/3, deep-1's cut); chop = `tsmom12` changed at least 3 slots in the last "
        "13 weeks; fast fall = the always-invested equal-weight book's 21-day return in its worst "
        "5% of days; slow bear = that book's 12-month return below zero; stock-bond corr > 0 = "
        "SPY and TLT daily returns positively correlated over the past year (the 2022 kind of "
        "rate regime); `tsmom12`'s ten deepest falls (peak to low) and the six months after "
        "each low (the turn); `tsmom12`'s losing weeks.",
        "",
        "| Model |" + "".join(f" {k} |" for k in order),
        "|---|" + "---:|" * len(order),
        *rows,
        "",
    ]

    # 3. stress windows and their rebounds: total return, model minus tsmom12
    rows = []
    for nm, lo, hi in STRESS:
        a0, b0 = idx(lo) + 1, idx(hi) + 1
        c0, d0 = b0, min(n, b0 + REBOUND)
        row = f"| {nm} | {pc(da.tot(ts[a0:b0]), '+.0f')} / {pc(da.tot(ts[c0:d0]), '+.0f')} |"
        for m in MODELS:
            x, y = r[m][a0:b0], r[m][c0:d0]
            row += (
                f" {pc(da.tot(x) - da.tot(ts[a0:b0]), '+.0f')} /"
                f" {pc(da.tot(y) - da.tot(ts[c0:d0]), '+.0f')} |"
            )
        rows.append(row)
    out += [
        "## 3. Stress windows: in the window / in the 6 months after (points, model minus "
        "`tsmom12`)",
        "",
        "First column: `tsmom12`'s own total return in the window / after it. `-` = the model "
        "did not exist then.",
        "",
        "| Window | `tsmom12` |" + "".join(f" `{m}` |" for m in MODELS),
        "|---|---:|" + "---:|" * len(MODELS),
        *rows,
        "",
    ]

    # 4. coverage of tsmom12's losses
    tw = da.weekly(ts)
    wr = {m: da.weekly(np.nan_to_num(r[m], nan=np.nan)) for m in MODELS}
    wx = {m: da.weekly(r[m]) - tw for m in MODELS}
    lose = tw < 0
    worst = tw <= np.quantile(tw, 0.10)
    rows = []
    cover: dict[str, dict[str, float]] = {}
    for m in MODELS:
        ok = np.isfinite(wr[m])
        cl = da.corr(wr[m][lose & ok], tw[lose & ok])
        call = da.corr(wr[m][ok], tw[ok])
        hit = float((wx[m][lose & ok] > 0).mean())
        mw = float(np.nanmean(wr[m][worst & ok])) if (worst & ok).sum() > 5 else math.nan
        tw_w = float(tw[worst & ok].mean())
        cover[m] = {"corr_all": call, "corr_lose": cl, "hit_lose": hit, "mean_worst": mw}
        rows.append(
            f"| `{m}` | {f2(call)} | {f2(cl)} | {hit * 100:.0f}% | {pc(mw, '+.2f')} |"
            f" {pc(tw_w, '+.2f')} | {int((lose & ok).sum())} |"
        )
    out += [
        "## 4. Does the model cover `tsmom12`'s losses? (weekly, 7-day blocks)",
        "",
        "Corr = correlation of the model's weekly return with `tsmom12`'s (all weeks; weeks "
        "`tsmom12` lost). Ahead = share of `tsmom12`'s losing weeks in which the model lost "
        "less. Worst 10% = mean weekly return (%) in `tsmom12`'s worst tenth of weeks, model "
        "and `tsmom12` on the same weeks.",
        "",
        "| Model | Corr, all | Corr, losing weeks | Ahead in losing weeks | Worst 10%: model |"
        " Worst 10%: `tsmom12` | Losing weeks |",
        "|---|---:|---:|---:|---:|---:|---:|",
        *rows,
        "",
    ]

    # 5. pairs: do their excess returns fail at the same time?
    regimes: list[tuple[str, Callable[[], np.ndarray]]] = [
        ("all weeks", lambda: np.ones(len(tw), bool)),
        ("tsmom12 losing", lambda: lose),
        ("chop", lambda: wk_mask(M["chop (>=3 flips/13 wk)"])),
        ("fast fall", lambda: wk_mask(M["fast fall (21-day, worst 5%)"])),
        ("slow bear", lambda: wk_mask(M["slow bear (12-mo below 0)"])),
        ("stock-bond +", lambda: wk_mask(M["stock-bond corr > 0 (1y)"])),
        ("turn (6 mo after low)", lambda: wk_mask(M["6 months after those lows"])),
    ]
    pairs = [(x, y) for i, x in enumerate(MODELS) for y in MODELS[i + 1 :]]
    rows = []
    pair_corr: dict[str, dict[str, float]] = {}
    for x, y in pairs:
        row = f"| `{x}` + `{y}` |"
        pc_: dict[str, float] = {}
        for lab, fm in regimes:
            sel = fm()
            v = da.corr(wx[x][sel], wx[y][sel], need=26)
            pc_[lab] = v
            row += f" {f2(v)} |"
        pair_corr[f"{x}+{y}"] = pc_
        rows.append(row)
    out += [
        "## 5. Pairs: correlation of weekly excess returns (each minus `tsmom12`) by regime",
        "",
        "Low or negative = the two models lose to `tsmom12` at different times, so a blend of "
        "them (or of either with `tsmom12`) could cover one with the other. `-` = fewer than 26 "
        "common weeks.",
        "",
        "| Pair |" + "".join(f" {lab} |" for lab, _ in regimes),
        "|---|" + "---:|" * len(regimes),
        *rows,
        "",
    ]

    RESULT.write_text("\n".join(out))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "map.json").write_text(
        json.dumps({"cover": cover, "pairs": pair_corr, "share": share}, indent=1)
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
