"""YouTube-rule cards (run ideas-1): `uv run --with numpy python research/lib/idea_yt.py <card>`.

Cards (all in `cards/yt-1.md`): bbwp, srsi, ath, gap, oil, y10, trend3, fng. `DRY=1` first.
Runs the standard test (testkit), then the 2003-2025 window, bar 6 and the hostile spells.

Per-asset price gates are precomputed once per panel as "date of the latest trigger at or
before bar i", each trigger computed from bars up to its own bar only; a decision reads entry
`n - 1` of what it can see, so nothing after the decision can reach it. A week's or month's close
is the last bar of that ISO week / calendar month, and a signal from it counts from the first
bar of the next period (when the period is known to be over): no calendar knowledge needed, and
`check` proves the decisions equal `gym.backtest`'s on visible bars only.
"""

from __future__ import annotations

import bisect
import json
import math
import sys
from collections.abc import Callable
from datetime import date, datetime, timedelta

import common as c
import harness
import macro
import numpy as np
import stats
import testkit
from harness import View, Weights

from grimstrade.data import CRYPTO, UNIVERSE

SAFE = {"TLT", "GLD", "IEF", "LQD"}
COMMODITY = {"DBC", "SLV"}
NONE = -(10**9)
SINCE = date(2003, 1, 1)


def is_coin(s: str) -> bool:
    return UNIVERSE[s] == CRYPTO


def is_stock(s: str) -> bool:
    return not is_coin(s) and s not in SAFE and s not in COMMODITY


def non_safe(s: str) -> bool:
    return s not in SAFE


# --- per-asset price triggers: arrays of booleans, one per bar, from bars <= that bar only ---


def _period_ends(dates: np.ndarray, key: Callable[[date], object]) -> np.ndarray:
    """Indexes of the last bar of each period (the final bar of the data is left out: its
    period may be incomplete)."""
    keys = [key(date.fromordinal(int(o))) for o in dates]
    return np.array([j for j in range(len(keys) - 1) if keys[j] != keys[j + 1]], dtype=np.int64)


def _week(d: date) -> object:
    return d.isocalendar()[:2]


def _month(d: date) -> object:
    return (d.year, d.month)


def trig_bbwp(dates: np.ndarray, close: np.ndarray, s: str) -> np.ndarray:
    ends = _period_ends(dates, _week)
    w = close[ends]
    out = np.zeros(len(close), dtype=bool)
    bbw = np.full(len(w), np.nan)
    for k in range(19, len(w)):
        x = w[k - 19 : k + 1]
        bbw[k] = 4 * x.std() / x.mean()
        prev = bbw[max(19, k - 252) : k]
        if len(prev) >= 104 and 100 * np.mean(prev < bbw[k]) >= 95 and w[k] > x.mean():
            out[ends[k] + 1] = True  # known from the first bar of the next week
    return out


def _rsi(x: np.ndarray, n: int = 14) -> np.ndarray:
    out = np.full(len(x), np.nan)
    if len(x) <= n:
        return out
    d = np.diff(x)
    g, lo = np.maximum(d, 0), np.maximum(-d, 0)
    ag, al = g[:n].mean(), lo[:n].mean()
    for k in range(n, len(x)):
        if k > n:
            ag = (ag * (n - 1) + g[k - 1]) / n
            al = (al * (n - 1) + lo[k - 1]) / n
        out[k] = 100.0 if al == 0 else 100 - 100 / (1 + ag / al)
    return out


def trig_srsi(dates: np.ndarray, close: np.ndarray, s: str) -> np.ndarray:
    ends = _period_ends(dates, _month)
    rsi = _rsi(close[ends])
    stoch = np.full(len(rsi), np.nan)
    for k in range(len(rsi)):
        win = rsi[k - 13 : k + 1] if k >= 13 else np.array([np.nan])
        if not np.isnan(win).any() and win.max() > win.min():
            stoch[k] = 100 * (rsi[k] - win.min()) / (win.max() - win.min())
    kk = np.full(len(rsi), np.nan)
    for k in range(2, len(rsi)):
        kk[k] = stoch[k - 2 : k + 1].mean()
    out = np.zeros(len(close), dtype=bool)
    for k in range(1, len(rsi)):
        if kk[k - 1] > 80 and kk[k] <= 80:  # NaN compares false
            out[ends[k] + 1] = True  # known from the first bar of the next month
    return out


def trig_ath(dates: np.ndarray, close: np.ndarray, s: str) -> np.ndarray:
    ends = _period_ends(dates, _week)
    w = close[ends]
    depth = 0.5 if is_coin(s) else 0.2
    out = np.zeros(len(close), dtype=bool)
    high, armed = -math.inf, False
    for k, x in enumerate(w):
        if armed and x > high:
            out[ends[k] + 1] = True  # known from the first bar of the next week
            armed = False
        high = max(high, x)
        if x <= (1 - depth) * high:
            armed = True
    return out


def _sent_low() -> macro.Step:
    def low(snap: dict[date, float], obs: list[date]) -> float:
        prev = [snap[o] for o in obs[-241:-1]]
        if len(prev) < 120:
            return math.nan
        return 1.0 if snap[obs[-1]] <= float(np.percentile(prev, 25)) else 0.0

    return macro.vintage_feature(macro.vintage_records("UMCSENT"), low)


_SENT: list[macro.Step] = []


def trig_gap(dates: np.ndarray, close: np.ndarray, s: str) -> np.ndarray:
    if not _SENT:
        _SENT.append(_sent_low())
    sent = _SENT[0]
    out = np.zeros(len(close), dtype=bool)
    for i in range(251, len(close)):
        if close[i] >= 0.95 * close[i - 251 : i + 1].max():
            out[i] = sent.at(date.fromordinal(int(dates[i])) + timedelta(days=1)) == 1.0
    return out


Trigger = Callable[[np.ndarray, np.ndarray, str], np.ndarray]


def price_gate(trig: Trigger, lo: int, hi: int, name: str) -> Callable[[View, str], bool]:
    """Hostile when today - (latest trigger date visible) is in [lo, hi] days."""

    def hostile(view: View, s: str) -> bool:
        n = view.n.get(s, 0)
        if n == 0:
            return False
        key = ("yt", name, s)
        cache = view.panel.cache
        if key not in cache:
            p = view.panel
            t = trig(p.ord[s], p.c[s], s)
            cache[key] = np.maximum.accumulate(np.where(t, p.ord[s], NONE))
        last: np.ndarray = cache[key]  # type: ignore[assignment]
        age = view.today.toordinal() - int(last[n - 1])
        return lo <= age <= hi

    return hostile


# --- macro and sentiment gates (the same for every gated asset on a day) ---


def _price_before(obs: list[date], vals: list[float], i: int, days: int) -> float:
    j = bisect.bisect_right(obs, obs[i] - timedelta(days=days)) - 1
    return vals[j] if j >= 0 else math.nan


def sticky(flag: macro.Step, days: int) -> Callable[[date], bool]:
    """True on a day the flag is 1 and for `days` days after the last such day."""
    on = [d for d, v in zip(flag.days, flag.values, strict=True) if v == 1.0]
    ords = [d.toordinal() for d in on]

    def f(d: date) -> bool:
        i = bisect.bisect_right(ords, d.toordinal())
        return bool(i) and d.toordinal() - ords[i - 1] <= days

    return f


def oil_shock() -> Callable[[date], bool]:
    def shock(obs: list[date], vals: list[float], i: int) -> float:
        a, b, x = _price_before(obs, vals, i, 182), _price_before(obs, vals, i, 365), vals[i]
        hit = (a > 0 and x >= 1.5 * a) or (b > 0 and x >= 2 * b)
        return 1.0 if hit else 0.0

    return sticky(macro.market_feature(macro.market_records("DCOILWTICO"), shock), 182)


def y10_change(rise: float = 0.75) -> Callable[[date], bool]:
    def chg(obs: list[date], vals: list[float], i: int) -> float:
        return vals[i] - _price_before(obs, vals, i, 91)

    step = macro.market_feature(macro.market_records("DGS10"), chg)
    return lambda d: step.at(d) > rise


def y10_level(level: float) -> Callable[[date], bool]:
    step = macro.market_feature(macro.market_records("DGS10"), macro.last_value)
    return lambda d: step.at(d) > level


def fng_step() -> macro.Step:
    path = macro.cache_root() / "fear-greed" / "2026-11-12" / "fng.json"
    rows = json.loads(path.read_text())["data"]
    pts = sorted(
        (datetime.fromtimestamp(int(r["timestamp"]), harness.UTC).date(), float(r["value"]))
        for r in rows
    )
    return macro.Step([d + timedelta(days=1) for d, _ in pts], [v for _, v in pts])


# --- rule shapes ---

AssetGate = Callable[[View, str], bool]


def gate_rule(
    hostile: AssetGate, applies: Callable[[str], bool], trend: bool
) -> c.ResearchStrategy:
    def f(view: View) -> Weights:
        held = c.live(view)
        out = {}
        for s in held:
            if not applies(s):
                on = c.tsmom_signal(view, s)
            elif hostile(view, s):
                on = False
            else:
                on = c.tsmom_signal(view, s) if trend else True
            if on:
                out[s] = 1 / len(held)
        return out

    return c.weekly(f)


def day_gate(g: Callable[[date], bool]) -> AssetGate:
    return lambda view, s: g(view.today)


def fng_rule(kind: str) -> c.ResearchStrategy:
    fng = fng_step()
    fear = sticky(fng.map(lambda v: 1.0 if v <= 24 else 0.0), 29)

    def f(view: View) -> Weights:
        held = c.live(view)
        out = {}
        for s in held:
            on = c.tsmom_signal(view, s)
            if is_coin(s):
                # NaN (before 2018-02): no data, so the slot stays `tsmom12`'s
                greed = fng.at(view.today) >= 75
                on = (on or fear(view.today)) if kind == "fear" else on and not greed
            if on:
                out[s] = 1 / len(held)
        return out

    return c.weekly(f)


def ten_month(view: View, s: str) -> bool:
    cl, od = view.close(s), view.dates(s)
    ends = _period_ends(od, _month)
    if len(ends) < 10:
        return False
    return bool(cl[-1] > cl[ends[-10:]].mean())


# --- cards ---

Card = tuple[str, dict[str, c.ResearchStrategy], tuple[str, ...], dict[str, AssetGate]]


def cards(name: str) -> Card:
    if name in ("bbwp", "srsi", "ath", "gap"):
        trig, lo, hi, title, applies = {
            "bbwp": (trig_bbwp, 0, 56, "bbwp: weekly band width percentile tops", non_safe),
            "srsi": (trig_srsi, 0, 364, "srsi: monthly stochastic RSI leaves overbought", non_safe),
            "ath": (trig_ath, 100, 464, "ath: the clock after breaking the old high", non_safe),
            "gap": (trig_gap, 0, 182, "gap: stocks near highs, consumers gloomy", is_stock),
        }[name]  # fmt: skip
        g = price_gate(trig, lo, hi, name)
        vs = {
            f"{name}-and": gate_rule(g, applies, True),
            f"{name}-alone": gate_rule(g, applies, False),
        }
        sets = ("etf", "coin", "idx") if applies is non_safe else ("etf", "idx")
        return title, vs, sets, {name: g}
    if name == "oil":
        g = day_gate(oil_shock())
        vs = {"oil-and": gate_rule(g, is_stock, True), "oil-alone": gate_rule(g, is_stock, False)}
        return "oil: oil supply shock regime", vs, ("etf", "idx"), {"oil": g}
    if name == "y10":
        gates = {"y10chg": day_gate(y10_change())}
        gates |= {f"y10lvl{int(x * 10)}": day_gate(y10_level(x)) for x in (4.0, 4.7, 5.5)}

        def bonds(s: str) -> bool:
            return is_stock(s) or s == "TLT"

        vs = {f"{k}-and": gate_rule(g, bonds, True) for k, g in gates.items()}
        return "y10: 10-year yield stress", vs, ("etf", "idx"), gates
    if name == "fng":
        vs = {"fng-buyfear": fng_rule("fear"), "fng-sellgreed": fng_rule("greed")}
        return "fng: crypto Fear & Greed contrarian", vs, ("coin",), {}
    raise KeyError(name)


def _window(runs: list[c.Run], twin: c.Run, a: date) -> str:
    lines = [
        "| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |",
        "|---|---:|---:|---:|---:|",
    ]
    tb = twin.rets_between(a, twin.days[-1])
    for r in runs:
        x = r.rets_between(a, r.days[-1])
        n = min(len(x), len(tb))
        diff = ""
        if r is not twin:
            d, p, _, _ = stats.sharpe_diff_boot(x[-n:], tb[-n:])
            diff = f"{d:+.2f} ({p:.2f})"
        lines.append(f"| {r.variant} | {stats.sharpe(x):.2f} | {stats.cagr(x):+.1%} | "
                     f"{stats.max_drawdown(x):.1%} | {diff} |")  # fmt: skip
    return "\n".join(lines)


def _spells(gates: dict[str, AssetGate]) -> list[str]:
    out = ["## Hostile spells (independent episodes)", ""]
    six = c.ctx("six")
    for tag, g in gates.items():
        for s in ("SPY", "BTC"):
            first = date.fromordinal(int(six.panel.ord[s][0])) + timedelta(days=366)
            lo = max(c.TRAIN_START, first)

            def f(d: date, s: str = s, g: AssetGate = g) -> bool:
                return g(six.panel.view(harness.decide_time(d)), s)

            sp = macro.spells(f, lo, c.TRAIN_END)
            days = sum((b - a).days + 1 for a, b in sp)
            share = days / ((c.TRAIN_END - lo).days + 1)
            when = ", ".join(f"{a:%Y-%m}..{b:%Y-%m}" for a, b in sp)
            out.append(
                f"- `{tag}` on {s}, {lo.year}-2025: {len(sp)} spells, {share:.0%} of days: {when}"
            )
    return out + [""]


def main(name: str) -> None:
    title, variants, sets, gates = cards(name)
    twins = {"tsmom12": c.weekly(c.slots(c.tsmom_signal))}
    res = testkit.standard(name, title, variants, twins, per_asset=True, sets=sets,
                           note="Shared rules: `cards/yt-1.md`.")  # fmt: skip
    vs: list[c.Run] = res["variants"]  # type: ignore[assignment]
    tw: list[c.Run] = res["twins"]  # type: ignore[assignment]
    ew: c.Run = res["ew"]  # type: ignore[assignment]
    twin, primary = tw[0], vs[0]
    out = [str(res["text"]), "## Since 2003", "", _window(vs + [twin, ew], twin, SINCE), ""]
    x, y = primary.rets_between(SINCE, primary.days[-1]), twin.rets_between(SINCE, twin.days[-1])
    ok6 = stats.sharpe(x) >= stats.sharpe(y)
    out += [f"- {'PASS' if ok6 else 'FAIL'}: 6. Not behind `tsmom12` on Sharpe 2003-2025 "
            f"({stats.sharpe(x):.2f} vs {stats.sharpe(y):.2f})", ""]  # fmt: skip
    passed = res["passed"] == "PASSES train" and ok6
    out += [f"**Card verdict (bars 1-6): {'PASSES' if passed else 'FAILS'} train.**", ""]
    if name == "fng":
        ep, et = c.era_sharpes(primary), c.era_sharpes(twin)
        eras = ("2017-21", "2022-25")
        out += ["Information only (eras with Fear & Greed data): "
                + ", ".join(f"{e} {ep[e]:.2f} vs {et[e]:.2f}" for e in eras), ""]  # fmt: skip
    if gates:
        out += _spells(gates)
    c.write_result(name, "\n".join(out))


def main_trend3() -> None:
    """Card 10: the six-asset slot of the standard test is replaced by SPY, GLD, BTC."""
    syms = ["SPY", "GLD", "BTC"]
    hist = harness.load_history("train", True, syms)
    t3 = c.Ctx("trend3", "train", hist, harness.Panel(hist), c.TRAIN_START, c.TRAIN_END)
    if c.DRY:
        t3.start = t3.end - timedelta(days=120)
    orig = c.ctx
    c.ctx = lambda name="six", period="train", adjusted=True: (  # type: ignore[assignment]
        t3 if name == "six" else orig(name, period, adjusted)
    )
    variants = {"trend3-sma200": c.weekly(c.slots(c.sma_signal)),
                "trend3-10m": c.weekly(c.slots(ten_month))}  # fmt: skip
    twins = {"tsmom12": c.weekly(c.slots(c.tsmom_signal))}
    res = testkit.standard("trend3", "trend3: long SPY, GLD, BTC above the long average",
                           variants, twins, per_asset=True, fresh_twins=True,
                           note="Shared rules: `cards/yt-1.md`. 'six' = SPY, GLD, BTC here; "
                                "out of universe the variant is `sma200` itself.")  # fmt: skip
    c.ctx = orig  # type: ignore[assignment]
    vs: list[c.Run] = res["variants"]  # type: ignore[assignment]
    tw: list[c.Run] = res["twins"]  # type: ignore[assignment]
    ew: c.Run = res["ew"]  # type: ignore[assignment]
    out = [str(res["text"]), "## Since 2003", "", _window(vs + [tw[0], ew], tw[0], SINCE), ""]
    c.write_result("trend3", "\n".join(out))


def check() -> None:
    """Fast path == gym.backtest (which sees only visible bars) on sample days, every card."""
    hist = harness.load_history("train", True, harness.SYMS)
    days = [
        date(2014, 3, 7),
        date(2018, 2, 9),
        date(2021, 6, 4),
        date(2022, 6, 3),
        date(2024, 1, 5),
    ]
    for name in ("bbwp", "srsi", "ath", "gap", "oil", "y10", "fng"):
        for v, f in cards(name)[1].items():
            harness.check_against_gym(f, hist, days)
            print("ok", v)


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        check()
        sys.argv = sys.argv[:1]
    for card in sys.argv[1:]:
        main_trend3() if card == "trend3" else main(card)
