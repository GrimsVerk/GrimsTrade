"""Lane wide-6, step 1: event-study gate for W11 `critical-slowing` (research/wide-6.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).

Run: `uv run python -I research/lib/wide6_csd.py`  (DRY=1: sample counts only, no statistics)
Output: research/results/critical-slowing.md
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide6_rules as r  # noqa: E402

from grimstrade.data import CRYPTO, UNIVERSE  # noqa: E402

ASSETS = ["SPY", "QQQ", "TLT", "GLD", "BTC", "ETH"]
SPLIT = date(2015, 12, 31)  # in-sample Fridays up to here; post-sample after
GATE_T = 2.24
LAGS = 13
OUT = Path(__file__).resolve().parents[1] / "results" / "critical-slowing.md"
DRY = bool(os.environ.get("DRY"))


@dataclass
class Obs:
    asset: str
    friday: date
    tau_ac1: float
    tau_var: float
    lsd21: float
    lsdw: float
    fdd: float
    large: float = math.nan


def sample(asset: str, closes: np.ndarray, days: list[date], detrend: bool) -> list[Obs]:
    crypto = UNIVERSE[asset] == CRYPTO
    w = 365 if crypto else 252
    h = 91 if crypto else 63
    logc = np.log(closes)
    ret = np.diff(logc, prepend=np.nan)  # ret[i] = log return into bar i
    if detrend:
        z = logc - r.trailing_mean(logc, 25)
        src = z
    else:
        src = ret.copy()
        src[0] = 0.0  # never inside a window used below (windows need 2w + 1 bars)
    ac1 = r.rolling_ac1(src, w)
    var = r.rolling_var(src, w)
    sd21 = np.sqrt(r.rolling_var(ret, 21))
    sdw = np.sqrt(r.rolling_var(ret, w))
    out: list[Obs] = []
    ords = np.array([d.toordinal() for d in days])
    f = days[0] + timedelta(days=(4 - days[0].weekday()) % 7)
    while f <= days[-1]:
        i = int(np.searchsorted(ords, f.toordinal(), side="right")) - 1
        f_next = f + timedelta(days=7)
        if i < 2 * w + 1 + (25 if detrend else 0):
            f = f_next
            continue
        fdd = r.forward_max_drawdown(logc, i, h)
        if math.isnan(fdd):
            break
        out.append(Obs(asset, f, r.kendall_trend(ac1, i, w), r.kendall_trend(var, i, w),
                       math.log(sd21[i]), math.log(sdw[i]), fdd))  # fmt: skip
        f = f_next
    return out


def label(obs: list[Obs]) -> None:
    """Large = FDD at or above the asset's 90th percentile over its own sampled Fridays."""
    for a in {o.asset for o in obs}:
        mine = [o for o in obs if o.asset == a]
        cut = float(np.quantile([o.fdd for o in mine], 0.9))
        for o in mine:
            o.large = 1.0 if o.fdd >= cut else 0.0


def design(obs: list[Obs], controls: bool, which: str = "both") -> np.ndarray:
    assets = sorted({o.asset for o in obs})
    cols = [np.array([1.0 if o.asset == a else 0.0 for o in obs]) for a in assets]
    if which in ("both", "ac1"):
        cols.append(np.array([o.tau_ac1 for o in obs]))
    if which in ("both", "var"):
        cols.append(np.array([o.tau_var for o in obs]))
    if controls:
        cols.append(np.array([o.lsd21 for o in obs]))
        cols.append(np.array([o.lsdw for o in obs]))
    return np.column_stack(cols)


def fit(obs: list[Obs], controls: bool, target: str = "large", which: str = "both"):  # type: ignore[no-untyped-def]
    obs = [o for o in obs if not (math.isnan(o.tau_ac1) or math.isnan(o.tau_var))]
    x = design(obs, controls, which)
    y = np.array([getattr(o, target) for o in obs])
    if target == "fdd":
        y = y * 100  # percent
    beta, t = r.ols_dk(y, x, [o.friday for o in obs], LAGS)
    k = len({o.asset for o in obs})
    return beta[k:], t[k:], len(obs), len({o.friday for o in obs})


def periods(obs: list[Obs]) -> list[tuple[str, list[Obs]]]:
    return [
        ("in-sample (Fridays to 2015-12)", [o for o in obs if o.friday <= SPLIT]),
        ("post-sample (2016-01 on)", [o for o in obs if o.friday > SPLIT]),
        ("all", obs),
    ]


def fmt(b: float, t: float) -> str:
    return f"{b:+.3f} ({t:+.2f})"


def pooled_table(obs: list[Obs], controls: bool, target: str) -> list[str]:
    lines = [
        "| Period | obs | Fridays | tauAC1 slope (t) | tauVAR slope (t) | log sd21 (t) "
        "| log sdw (t) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, sub in periods(obs):
        b, t, n, nw = fit(sub, controls, target)
        extra = f"{fmt(b[2], t[2])} | {fmt(b[3], t[3])}" if controls else "- | -"
        lines.append(f"| {name} | {n} | {nw} | {fmt(b[0], t[0])} | {fmt(b[1], t[1])} | {extra} |")
    return lines


def main() -> None:
    hist = harness.load_history("train", syms=ASSETS)
    gspc = harness.load_history("train", syms=["GSPC"])["GSPC"]
    variants: dict[str, list[Obs]] = {}
    for detrend in (False, True):
        obs: list[Obs] = []
        for a in ASSETS:
            bars = hist[a]
            obs += sample(a, np.array([b.close for b in bars]), [b.date for b in bars], detrend)
        label(obs)
        variants["price" if detrend else "returns"] = obs
    g_all = sample("GSPC", np.array([b.close for b in gspc]), [b.date for b in gspc], False)
    g = [o for o in g_all if date(1962, 1, 1) <= o.friday <= SPLIT]
    label(g)

    main_obs = variants["returns"]
    if DRY:
        for name, sub in periods(main_obs):
            print(name, len(sub), {a: sum(o.asset == a for o in sub) for a in ASSETS})
        print("GSPC", len(g))
        return

    gate = {}
    for name, sub in periods(main_obs)[:2]:
        b, t, _, _ = fit(sub, True, "large")
        gate[name] = (b, t)
    passed = {
        k: all(gate[p][0][j] > 0 and gate[p][1][j] >= GATE_T for p in gate)
        for j, k in ((0, "tauAC1"), (1, "tauVAR"))
    }

    out = ["# Critical slowing down: event-study gate (wide-6, W11)", ""]
    out += [
        "Rule: `research/wide-6.md` (pushed before this ran). Script `research/lib/wide6_csd.py`.",
        "Linear probability of a large forward drawdown (asset's top decile of the maximum",
        "drawdown over the next quarter), pooled over SPY, QQQ, TLT, GLD, BTC, ETH with asset",
        f"intercepts; Driscoll-Kraay t ({LAGS} weekly lags). Slopes are per unit of Kendall tau",
        "(range -1 to +1) and per unit of log volatility; base rate 0.10.",
        "",
        "## Gate (with the two volatility controls)",
        "",
    ]
    out += pooled_table(main_obs, True, "large")
    out += [
        "",
        f"Gate (slope > 0 and t >= {GATE_T} in both periods): tauAC1 "
        f"**{'PASS' if passed['tauAC1'] else 'fail'}**, tauVAR "
        f"**{'PASS' if passed['tauVAR'] else 'fail'}**.",
        "",
        "## Shown: without the volatility controls (raw effect)",
        "",
    ]
    out += pooled_table(main_obs, False, "large")
    out += ["", "## Shown: continuous target (forward maximum drawdown, percent)", ""]
    out += pooled_table(main_obs, True, "fdd")
    out += [
        "",
        "## Shown: per asset, each tau alone with the controls (Newey-West t)",
        "",
        "| Asset | Period | obs | tauAC1 slope (t) | tauVAR slope (t) |",
        "|---|---|---:|---:|---:|",
    ]
    for a in ASSETS:
        for name, sub in periods([o for o in main_obs if o.asset == a])[:2]:
            sub = [o for o in sub if not (math.isnan(o.tau_ac1) or math.isnan(o.tau_var))]
            if len(sub) < 60:
                out.append(f"| {a} | {name} | {len(sub)} | - | - |")
                continue
            ba, ta, n, _ = fit(sub, True, "large", "ac1")
            bv, tv, _, _ = fit(sub, True, "large", "var")
            out.append(f"| {a} | {name} | {n} | {fmt(ba[0], ta[0])} | {fmt(bv[0], tv[0])} |")
    out += ["", "## Shown: S&P 500 index (GSPC) alone, Fridays 1962-2015 (the papers' years)", ""]
    out += [
        "| Spec | obs | tauAC1 slope (t) | tauVAR slope (t) |",
        "|---|---:|---:|---:|",
    ]
    for ctl in (True, False):
        b, t, n, _ = fit(g, ctl, "large")
        out.append(
            f"| {'with' if ctl else 'without'} vol controls | {n} | {fmt(b[0], t[0])} | "
            f"{fmt(b[1], t[1])} |"
        )
    out += [
        "",
        "## Shown: AC1 and variance of log price minus its trailing 25-bar mean "
        "(Guttal-style, causal)",
        "",
    ]
    out += pooled_table(variants["price"], True, "large")
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
