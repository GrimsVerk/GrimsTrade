"""wide-16 `cost-band`: `tsmom12` with a cost-sized rebalance band (card `cards/cost-band.md`).

    DRY=1 uv run --with numpy python research/lib/wide16.py   # plumbing: last 120 days, no rows
    uv run --with numpy python research/lib/wide16.py         # the one real run

The rule is `tsmom12`'s weights, unchanged; only `gym.simulate(band=...)` differs. Train period
only (`common.ctx` loads bars through 2025-11-10). Writes `results/cost-band.md`.
"""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import date

import common as c
import harness
import numpy as np
import stats

from grimstrade import gym
from grimstrade.data import CRYPTO, UNIVERSE

IDEA = "cost-band"
BANDS = {"band05": 0.05, "band02": 0.02}  # frozen in the card
COIN_ERA = date(2015, 1, 1)  # reporting split only


def rule() -> c.ResearchStrategy:
    """The rule's weights: exactly `tsmom12`'s (the band lives in the gym, not here)."""
    return c.weekly(c.slots(c.tsmom_signal))


def boot(a: np.ndarray, b: np.ndarray, draws: int = 2000) -> tuple[float, float, float]:
    """dSharpe, paired stationary-bootstrap SE and one-sided p (20-day blocks, seed 0)."""
    rng = np.random.default_rng(0)
    diffs = np.empty(draws)
    for k in range(draws):
        i = stats._stationary_indices(len(a), 20, rng)
        diffs[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
    return stats.sharpe(a) - stats.sharpe(b), float(diffs.std()), float((diffs <= 0).mean())


def bill_daily(days: list[date], rates: gym.Rates) -> np.ndarray:
    """What a dollar of cash earned on each calendar day after the first (the gym's rule)."""
    known = [t for t, _ in rates]
    return np.array([gym.cash_rate(rates, d, known) / gym.DAYS_PER_YEAR for d in days[1:]])


def coin_drift(run: harness.Run, ctx: c.Ctx, band: float) -> tuple[float, float]:
    """Coin drift fills a year and their fee + slip as a share of equity a year, from 2015 (or
    the set's start): fills that neither open nor close a position."""
    res = gym.simulate(run.decisions, ctx.hist, band=band)
    eq = dict(res.equity)
    pos: dict[str, float] = defaultdict(float)
    n, cost = 0, 0.0
    first = max(COIN_ERA, ctx.start)
    for f in res.fills:
        before = pos[f.symbol]
        pos[f.symbol] += f.qty
        d = f.time.date()
        if UNIVERSE[f.symbol] != CRYPTO or d < first or before <= 1e-12 or pos[f.symbol] <= 1e-9:
            continue
        e = eq.get(d) or next(v for k, v in reversed(res.equity) if k <= d)
        n += 1
        cost += (f.fee + abs(f.qty) * f.price * gym.COSTS[CRYPTO].slip) / e
    years = (ctx.end - first).days / 365.25
    return n / years, cost / years


def compare(rule_run: harness.Run, base: harness.Run, rf: np.ndarray | None) -> dict[str, float]:
    a, b = rule_run.rets, base.rets
    if rf is not None:
        a, b = a - rf, b - rf
    d, se, p = boot(a, b)
    g = rule_run.rets - base.rets
    return {
        "d": d, "se": se, "z": d / se if se > 0 else math.nan, "p": p,
        "te": float(g.std() * math.sqrt(365)), "corr": float(np.corrcoef(a, b)[0, 1]),
        "sharpe": stats.sharpe(a), "base": stats.sharpe(b),
    }  # fmt: skip


def run_set(name: str) -> tuple[list[str], dict[str, dict[str, float]]]:
    ctx = c.ctx(name)
    kind = "variant" if name == "six" else "robustness"
    rates = harness.bill_rates() if name == "six" else ()
    out: dict[str, dict[str, float]] = {}
    lines: list[str] = []

    def go(variant: str, band: float, with_bills: bool, log: bool) -> harness.Run:
        tag = variant if name == "six" else f"{variant}@{name}"
        tag += "/bills" if with_bills else ""
        return harness.run(
            IDEA, tag, rule(), kind=kind if not with_bills else "robustness", period="train",
            panel=ctx.panel, history=ctx.hist, start=ctx.start, end=ctx.end,
            log=log and not c.DRY, rates=rates if with_bills else (), band=band,
        )  # fmt: skip

    base0 = go("tsmom12", gym.BAND, False, log=False)  # the logged baseline, re-scored
    conventions = [(False, None)]
    if name == "six":
        base1 = go("tsmom12", gym.BAND, True, log=False)
        conventions.append((True, bill_daily(base1.days, rates)))
    n0, k0 = coin_drift(base0, ctx, gym.BAND)
    eras0 = c.era_sharpes(base0)
    lines.append(
        f"| `tsmom12` (b = 0.01) | {stats.sharpe(base0.rets):.3f} | - | - | - | - | "
        f"{stats.max_drawdown(base0.rets):.1%} | {base0.score.turnover:.2f} | {n0:.1f} | "
        f"{k0:.3%} | - |"
    )
    for variant, band in BANDS.items():
        for with_bills, rf in conventions:
            r = go(variant, band, with_bills, log=True)
            base = base1 if with_bills else base0
            m = compare(r, base, rf)
            key = variant + ("/bills" if with_bills else "")
            out[key] = m
            if with_bills:
                lines.append(
                    f"| `{key}` (above bills) | {m['sharpe']:.3f} | {m['d']:+.4f} | "
                    f"{m['se']:.4f} | **{m['z']:+.2f}** | {m['p']:.3f} | - | - | - | - | - |"
                )
                continue
            n1, k1 = coin_drift(r, ctx, band)
            m["mdd"], m["mdd0"] = stats.max_drawdown(r.rets), stats.max_drawdown(base0.rets)
            m["drift_n"], m["drift_cost"] = n1, k1
            er = c.era_sharpes(r)
            eras = " ".join(
                f"{e} {er[e] - eras0[e]:+.3f}" for e in er if not math.isnan(er[e] - eras0[e])
            )
            lines.append(
                f"| `{key}` | {m['sharpe']:.3f} | {m['d']:+.4f} | {m['se']:.4f} | "
                f"**{m['z']:+.2f}** | {m['p']:.3f} | {m['mdd']:.1%} | {r.score.turnover:.2f} | "
                f"{n1:.1f} | {k1:.3%} | TE {m['te']:.2%}, corr {m['corr']:.4f}; eras: {eras} |"
            )
    return lines, out


HEAD = (
    "| Rule | Sharpe | dSharpe | Paired SE | z | p (one-sided) | Max DD | Turnover/yr | "
    "Coin drift fills/yr | Their cost/yr | Notes |\n"
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"
)


def main() -> None:
    text = [f"# {IDEA}: results (card `cards/cost-band.md`)", ""]
    verdict: dict[str, dict[str, dict[str, float]]] = {}
    sets = (("six", "Primary test: the six, 1994-2025"), ("coin", "Out of universe: 6 other coins"))
    for name, title in sets:
        lines, out = run_set(name)
        verdict[name] = out
        text += [f"## {title}", "", HEAD, *lines, ""]
    text += ["## Pass bar (card)", ""]
    for v in BANDS:
        six, bills, coin = verdict["six"][v], verdict["six"][v + "/bills"], verdict["coin"][v]
        ok = [six["z"] >= 4.69, bills["z"] >= 4.69, coin["d"] > 0, six["mdd"] <= six["mdd0"] + 0.01]
        text.append(
            f"- `{v}`: z {six['z']:+.2f} (cash 0) {'>=' if ok[0] else '<'} 4.69; z "
            f"{bills['z']:+.2f} (above bills) {'>=' if ok[1] else '<'} 4.69; coin dSharpe "
            f"{coin['d']:+.4f} ({'> 0' if ok[2] else '<= 0'}); max DD {six['mdd']:.1%} vs "
            f"{six['mdd0']:.1%} ({'ok' if ok[3] else 'worse by > 1 point'}). "
            f"**{'PASS' if all(ok) else 'FAIL'}**"
        )
    c.write_result(IDEA, "\n".join(text))


if __name__ == "__main__":
    main()
