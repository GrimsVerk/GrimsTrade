"""Shared test for single-asset, in-or-out timing rules (month-end-liquidity, dip-rsi2)."""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from datetime import date

import common as c
import numpy as np
import stats
from harness import Run

Signal = Callable[[c.View, str], bool]


def in_out(run: Run, u: c.Ctx, sym: str) -> tuple[np.ndarray, np.ndarray, list[date]]:
    """Open-to-open returns of the asset on days the rule held it, and on days it did not.
    A decision after the close of bar i is held from the open of bar i+1 to the open of i+2."""
    bars = u.hist[sym]
    held = {d.time.date(): bool(d.weights) for d in run.decisions}
    ins, outs, days = [], [], []
    for i in range(len(bars) - 2):
        d = bars[i].date
        if d not in held:
            continue
        r = bars[i + 2].open / bars[i + 1].open - 1
        (ins if held[d] else outs).append(r)
        if held[d]:
            days.append(d)
    return np.array(ins), np.array(outs), days


def welch(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 2 or len(b) < 2:
        return math.nan
    return float((a.mean() - b.mean()) / math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)))


def one(idea: str, variant: str, signal: Signal, sym: str, kind: str, split: date) -> dict:
    u = c.ctx(sym)

    def rule(view: c.View) -> c.Weights:
        return {sym: 1.0} if c.eligible(view, sym) and signal(view, sym) else {}

    v = c.go(idea, variant, rule, u, kind)
    w = v.exposure

    def constant(view: c.View) -> c.Weights:
        return {sym: w} if c.eligible(view, sym) else {}

    t = c.go(idea, "constant", constant, u, "baseline")
    bh = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), u, "baseline", log=False)
    ins, outs, days = in_out(v, u, sym)
    pre_in = np.array([r for r, d in zip(ins, days, strict=True) if d < split])
    post_in = np.array([r for r, d in zip(ins, days, strict=True) if d >= split])
    a, b = c.align(v, t)
    diff, pval, _, _ = stats.sharpe_diff_boot(a, b)
    post = stats.sharpe(v.rets_between(split, v.days[-1])) - stats.sharpe(
        t.rets_between(split, t.days[-1])
    )
    text = [f"## {sym}, from {u.start}", "", c.table([v, t, bh], versus=t), ""]
    text += [
        f"Mean open-to-open return per day held {ins.mean() * 1e4:+.1f} bps ({len(ins)} days), "
        f"per day not held {outs.mean() * 1e4:+.1f} bps ({len(outs)} days), Welch t = "
        f"{welch(ins, outs):.2f}. Days held before {split}: "
        f"{pre_in.mean() * 1e4 if len(pre_in) else math.nan:+.1f} bps; from {split}: "
        f"{post_in.mean() * 1e4 if len(post_in) else math.nan:+.1f} bps. "
        f"Sharpe difference to the twin from {split}: {post:+.2f}.",
        "",
    ]
    return {
        "sym": sym, "text": text, "diff": diff, "p": pval, "post": post, "t": welch(ins, outs),
        "sharpe": c.describe(v)["sharpe"], "bh": c.describe(bh)["sharpe"],
        "mdd": c.describe(v)["mdd"], "mdd_twin": c.describe(t)["mdd"], "run": v, "ctx": u,
    }  # fmt: skip


def run_all(
    idea: str, title: str, variant: str, signal: Signal, main: Sequence[str],
    oou: dict[str, Sequence[str]], split: date, intro: str,
) -> tuple[list[str], list[dict], dict[str, float]]:  # fmt: skip
    out = [f"# {title}", "", f"Card: `cards/{idea}.md`. {intro}", ""]
    res = [one(idea, variant, signal, s, "variant", split) for s in main]
    for r in res:
        out += r["text"]
    signs = {}
    for name, syms in oou.items():
        out += [f"# Out of universe: {name}", ""]
        rs = [one(idea, variant, signal, s, "robustness", split) for s in syms]
        for r in rs:
            out += r["text"]
        signs[name] = sum(r["diff"] for r in rs) / len(rs)
    return out, res, signs
