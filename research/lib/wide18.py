"""wide-18: `tsmom12` read in variance time (`vclock12`) and through a robust filter (`huber52`).

    DRY=1 uv run --with numpy python research/lib/wide18.py   # plumbing: last 120 days, no rows
    uv run --with numpy python research/lib/wide18.py         # the one real run

Card `research/cards/wide-18.md` (frozen before any number). Only the per-asset signal differs
from `tsmom12`; slots, Fridays, costs and band are the gym's. Every window ends on 2025-10-31
(the lane's train cut). Writes `results/wide-18.md`.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from datetime import date

import common as c
import harness
import numpy as np
import stats
from wide16 import bill_daily, boot

from grimstrade.data import CRYPTO, UNIVERSE

IDEA = "wide-18"
LAST = date(2025, 10, 31)  # the lane's train cut (card)
Z_BAR = 4.70  # BAR.md, N_eff 500 (rows through 2026-11-24 20:01)
Z_ONC = 3.25  # the bar at the ONC end of the count (reported, not a pass)
HUBER_K = 1.345
WEEKS = 52


def bars_per_year(s: str) -> int:
    return 365 if UNIVERSE[s] == CRYPTO else 252


def vclock_window(lr: np.ndarray, b: int) -> int:
    """Bars of the most recent stretch holding one median year of variance (card, step 1-2).
    0 when fewer than `b` returns are visible (the caller falls back to `tsmom12`)."""
    if len(lr) < b:
        return 0
    sq = lr * lr
    cs = np.concatenate(([0.0], np.cumsum(sq)))
    v = float(np.median(cs[b:] - cs[:-b]))  # every window of b consecutive returns
    rc = np.cumsum(sq[::-1])
    k = int(np.searchsorted(rc, v * (1 - 1e-9), side="left")) + 1  # first k, sum >= v (float tol.)
    return int(min(max(k, b // 4), 2 * b, len(lr)))


def vclock_signal(view: harness.View, s: str) -> bool:
    lr = view.logret(s)
    k = vclock_window(lr, bars_per_year(s))
    if k == 0:
        return c.tsmom_signal(view, s)
    return float(lr[-k:].sum()) > 0


def huber_drift(x: np.ndarray, k: float = HUBER_K) -> float:
    """One-step Huber location: clip at k robust sd (1.4826 MAD) around the median, then mean.
    NaN when the MAD is zero (the caller falls back to `tsmom12`)."""
    m = float(np.median(x))
    sd = 1.4826 * float(np.median(np.abs(x - m)))
    if sd <= 0:
        return math.nan
    return float(np.clip(x, m - k * sd, m + k * sd).mean())


def huber_signal(view: harness.View, s: str) -> bool:
    cl = view.close(s)
    w = 7 if UNIVERSE[s] == CRYPTO else 5
    if len(cl) < WEEKS * w + 1:
        return c.tsmom_signal(view, s)
    x = np.diff(np.log(cl[-1 - WEEKS * w :: w]))
    d = huber_drift(x)
    if math.isnan(d):
        return c.tsmom_signal(view, s)
    return d > 0


RULES: dict[str, Callable[[harness.View, str], bool]] = {
    "vclock12": vclock_signal,
    "huber52": huber_signal,
}


def rule(name: str) -> c.ResearchStrategy:
    return c.weekly(c.slots(RULES[name]))


def baseline() -> c.ResearchStrategy:
    return c.weekly(c.slots(c.tsmom_signal))


def compare(a: harness.Run, b: harness.Run, rf: np.ndarray | None) -> dict[str, float]:
    x, y = a.rets, b.rets
    if rf is not None:
        x, y = x - rf, y - rf
    d, se, p = boot(x, y)
    return {
        "d": d, "se": se, "z": d / se if se > 0 else math.nan, "p": p,
        "corr": float(np.corrcoef(x, y)[0, 1]), "sharpe": stats.sharpe(x),
        "base": stats.sharpe(y), "te": float((a.rets - b.rets).std() * math.sqrt(365)),
        "mdd": stats.max_drawdown(a.rets), "mdd0": stats.max_drawdown(b.rets),
        "expo": a.exposure, "expo0": b.exposure,
    }  # fmt: skip


def flips(run: harness.Run) -> float:
    """Slot switches (in -> out or out -> in) a year, from the decisions."""
    held = [frozenset(d.weights) for d in run.decisions]
    n = sum(len(p ^ q) for p, q in zip(held, held[1:], strict=False))
    years = max(len(run.rets) / 365.25, 1e-9)
    return n / years


def run_set(name: str) -> dict[str, dict[str, float]]:
    ctx = c.ctx(name)
    end = min(ctx.end, LAST)
    kind = "variant" if name == "six" else "robustness"
    rates = harness.bill_rates() if name == "six" else ()

    def go(variant: str, strat: c.ResearchStrategy, bills: bool, log: bool) -> harness.Run:
        tag = variant if name == "six" else f"{variant}@{name}"
        tag += "/bills" if bills else ""
        return harness.run(
            IDEA, tag, strat, kind="robustness" if bills else kind, period="train",
            panel=ctx.panel, history=ctx.hist, start=ctx.start, end=end,
            log=log and not c.DRY, rates=rates if bills else (),
        )  # fmt: skip

    base = {False: go("tsmom12", baseline(), False, log=False)}
    rf: dict[bool, np.ndarray | None] = {False: None}
    if name == "six":
        base[True] = go("tsmom12", baseline(), True, log=False)
        rf[True] = bill_daily(base[True].days, rates)
    out: dict[str, dict[str, float]] = {}
    out["tsmom12"] = {"sharpe": stats.sharpe(base[False].rets), "flips": flips(base[False]),
                      "mdd": stats.max_drawdown(base[False].rets),
                      "expo": base[False].exposure}  # fmt: skip
    for v in RULES:
        for bills in base:
            r = go(v, rule(v), bills, log=True)
            m = compare(r, base[bills], rf[bills])
            m["flips"] = flips(r)
            if not bills:
                er, e0 = c.era_sharpes(r), c.era_sharpes(base[False])
                for e in er:
                    m[f"era {e}"] = er[e] - e0[e]
            out[v + ("/bills" if bills else "")] = m
    out["_window"] = {"start": ctx.start.toordinal(), "end": end.toordinal()}
    return out


def fmt_set(title: str, res: dict[str, dict[str, float]]) -> list[str]:
    w = res["_window"]
    a, b = date.fromordinal(int(w["start"])), date.fromordinal(int(w["end"]))
    t = res["tsmom12"]
    lines = [
        f"## {title} ({a} .. {b})", "",
        "| Rule | Sharpe | dSharpe | Paired SE | z | p (one-sided) | corr with `tsmom12` | "
        "Edge needed (4.70 x SE) | Tracking error | Max DD | Exposure | Slot flips/yr |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        f"| `tsmom12` | {t['sharpe']:.3f} | - | - | - | - | - | - | - | {t['mdd']:.1%} | "
        f"{t['expo']:.2f} | {t['flips']:.1f} |",
    ]  # fmt: skip
    for k, m in res.items():
        if k in ("tsmom12", "_window"):
            continue
        dd = f"{m['mdd']:.1%}" if "/bills" not in k else "-"
        fl = f"{m['flips']:.1f}" if "/bills" not in k else "-"
        lines.append(
            f"| `{k}` | {m['sharpe']:.3f} | {m['d']:+.4f} | {m['se']:.4f} | **{m['z']:+.2f}** | "
            f"{m['p']:.3f} | {m['corr']:.3f} | {Z_BAR * m['se']:+.3f} | {m['te']:.2%} | {dd} | "
            f"{m['expo']:.2f} | {fl} |"
        )
    eras = [
        f"- `{k}` minus `tsmom12` by era: "
        + ", ".join(
            f"{e[4:]} {x:+.3f}" for e, x in m.items() if e.startswith("era ") and not math.isnan(x)
        )  # fmt: skip
        for k, m in res.items()
        if k in RULES
    ]
    return [*lines, "", *eras, ""]


def main() -> None:
    sets = (
        ("six", "Primary test: the six"),
        ("etf", "Out of universe: 8 ETFs"),
        ("idx", "Out of universe: 4 price indexes"),
    )
    text = [f"# {IDEA}: results (card `cards/wide-18.md`)", ""]
    res: dict[str, dict[str, dict[str, float]]] = {}
    for name, title in sets:
        res[name] = run_set(name)
        text += fmt_set(title, res[name])
    text += ["## Pass bar (card)", ""]
    for v in RULES:
        six, bills = res["six"][v], res["six"][v + "/bills"]
        etf, idx = res["etf"][v], res["idx"][v]
        ok = [six["z"] >= Z_BAR, bills["z"] >= Z_BAR, etf["d"] > 0, idx["d"] > 0]
        onc = ""
        if min(six["z"], bills["z"]) >= Z_ONC:
            onc = " (z >= 3.25: the counting method decides)"
        text.append(
            f"- `{v}`: z {six['z']:+.2f} (cash 0), {bills['z']:+.2f} (above bills) against "
            f"{Z_BAR}; dSharpe `etf` {etf['d']:+.4f}, `idx` {idx['d']:+.4f}{onc}. "
            f"**{'PASS' if all(ok) else 'FAIL'}**"
        )
    c.write_result(IDEA, "\n".join(text))


if __name__ == "__main__":
    main()
