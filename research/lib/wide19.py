"""wide-19: `tsmom12` with Buhlmann credibility-weighted drifts (`cred-xs`, `cred-lr`).

    DRY=1 uv run --with numpy python research/lib/wide19.py   # plumbing: last 120 days, no rows
    uv run --with numpy python research/lib/wide19.py         # the one real run

Card `research/cards/wide-19.md` (frozen before any number). Only the per-asset signal differs
from `tsmom12`; slots, Fridays, costs and band are the gym's. Every window ends on 2025-10-31
(the lane's train cut). Writes `results/wide-19.md`.
"""

from __future__ import annotations

import math
from datetime import date

import common as c
import harness
import numpy as np
import stats
from wide16 import bill_daily, boot

IDEA = "wide-19"
LAST = date(2025, 10, 31)  # the lane's train cut (card)
Z_BAR = 4.70  # BAR.md, N_eff 500 (rows through 2026-11-24 20:01)
Z_ONC = 3.25  # the bar at the ONC end of the count (reported, not a pass)
WEEKS = 52
V = 1 / WEEKS  # sampling variance of a year's drift in weekly risk units (card, step 3)
MIN_FRIDAYS = 52  # estimates of `a` need at least this many Fridays / pool points
LR_MIN_RETURNS = 156  # cred-lr: assets in the pool need three years of weekly returns
RULES = ("cred-xs", "cred-lr")


def weekly_returns(dates: np.ndarray, closes: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Weekly log returns on a chronological Friday grid (ordinals): the close at each grid date
    is the last close on or before it; NaN before the first close. Length len(grid) - 1."""
    i = np.searchsorted(dates, grid, side="right") - 1
    px = np.where(i >= 0, closes[np.maximum(i, 0)], np.nan)
    return np.diff(np.log(px))


def rolling_x(r: np.ndarray, n: int = WEEKS) -> np.ndarray:
    """x at each grid return: mean / sample sd of the n returns ending there (NaN when fewer
    than n valid returns or sd 0). Same length as r."""
    ok = ~np.isnan(r)
    z = np.where(ok, r, 0.0)
    cs = np.concatenate(([0.0], np.cumsum(z)))
    cq = np.concatenate(([0.0], np.cumsum(z * z)))
    cn = np.concatenate(([0], np.cumsum(ok)))
    out = np.full(len(r), np.nan)
    if len(r) < n:
        return out
    s = cs[n:] - cs[:-n]
    q = cq[n:] - cq[:-n]
    k = cn[n:] - cn[:-n]
    var = (q - s * s / n) / (n - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        x = np.where((k == n) & (var > 1e-18), (s / n) / np.sqrt(np.maximum(var, 1e-300)), np.nan)
    out[n - 1 :] = x
    return out


def z_of(a: float) -> float:
    a = max(a, 0.0)
    return a / (a + V)


def xs_z(xm: np.ndarray) -> float:
    """cred-xs: Z from the mean over Fridays (columns) with >= 2 assets (rows) of the
    cross-sectional variance minus V; 1.0 with fewer than MIN_FRIDAYS such Fridays."""
    cnt = (~np.isnan(xm)).sum(axis=0)
    cols = xm[:, cnt >= 2]
    if cols.shape[1] < MIN_FRIDAYS:
        return 1.0
    s2 = np.nanvar(cols, axis=0, ddof=1)
    return z_of(float(np.mean(s2 - V)))


def lr_z(xm: np.ndarray, mu: np.ndarray, nret: np.ndarray) -> float:
    """cred-lr: Z from the pooled squared deviation of x from each asset's long-run mu minus V,
    over assets with >= LR_MIN_RETURNS weekly returns; 1.0 with fewer than MIN_FRIDAYS points."""
    rows = nret >= LR_MIN_RETURNS
    dev = xm[rows] - mu[rows, None]
    dev = dev[~np.isnan(dev)]
    if len(dev) < MIN_FRIDAYS:
        return 1.0
    return z_of(float(np.mean(dev * dev) - V))


class State:
    """Everything the two rules need on one decision Friday, from visible bars only."""

    def __init__(self, view: harness.View) -> None:
        d = view.today.toordinal()
        syms = [s for s in view.syms if view.n.get(s, 0) >= 2]
        first = min(int(view.dates(s)[0]) for s in syms)
        k = (d - first) // 7 + 1
        grid = d - 7 * np.arange(k, -1, -1)  # chronological, ends on d
        self.syms = syms
        xm, mu, nret = [], [], []
        for s in syms:
            r = weekly_returns(view.dates(s), view.close(s), grid)
            xm.append(rolling_x(r))
            v = r[~np.isnan(r)]
            nret.append(len(v))
            sd = float(v.std(ddof=1)) if len(v) >= 2 else 0.0
            mu.append(float(v.mean()) / sd if sd > 0 else math.nan)
        self.xm = np.array(xm)
        self.mu = np.array(mu)
        self.x = {s: float(self.xm[i, -1]) for i, s in enumerate(syms)}
        now = [v for v in self.x.values() if not math.isnan(v)]
        self.xbar = float(np.mean(now)) if now else math.nan
        self.z = {"cred-xs": xs_z(self.xm), "cred-lr": lr_z(self.xm, self.mu, np.array(nret))}

    def signal(self, name: str, s: str) -> bool | None:
        """None when the asset has no x on this Friday (the caller uses `tsmom12`)."""
        x = self.x.get(s, math.nan)
        if math.isnan(x):
            return None
        z = self.z[name]
        comp = self.xbar if name == "cred-xs" else self.mu[self.syms.index(s)]
        if math.isnan(comp):
            comp = x
        return z * x + (1 - z) * comp > 0


def rule(name: str, zlog: dict[date, float] | None = None) -> c.ResearchStrategy:
    def f(view: harness.View) -> c.Weights:
        st = State(view)
        if zlog is not None:
            zlog[view.today] = st.z[name]
        held = c.live(view)
        out = {}
        for s in held:
            sig = st.signal(name, s)
            if sig is None:
                sig = c.tsmom_signal(view, s)
            if sig:
                out[s] = 1 / len(held)
        return out

    return c.weekly(f)


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
    return n / max(len(run.rets) / 365.25, 1e-9)


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
            zlog: dict[date, float] = {}
            r = go(v, rule(v, zlog), bills, log=True)
            m = compare(r, base[bills], rf[bills])
            m["flips"] = flips(r)
            zs = [zlog[k] for k in sorted(zlog)]
            m["z_end"], m["z_med"] = zs[-1], float(np.median(zs))
            m["z_min"], m["z_max"] = min(zs), max(zs)
            m["same"] = sum(p.weights == q.weights for p, q in
                            zip(r.decisions, base[bills].decisions, strict=False)
                            ) / max(len(r.decisions), 1)  # fmt: skip
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
        "Edge needed (4.70 x SE) | Tracking error | Max DD | Exposure | Slot flips/yr | "
        "Z end | Z median (min-max) | Same decision as `tsmom12` |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        f"| `tsmom12` | {t['sharpe']:.3f} | - | - | - | - | - | - | - | {t['mdd']:.1%} | "
        f"{t['expo']:.2f} | {t['flips']:.1f} | - | - | - |",
    ]  # fmt: skip
    for k, m in res.items():
        if k in ("tsmom12", "_window"):
            continue
        dd = f"{m['mdd']:.1%}" if "/bills" not in k else "-"
        fl = f"{m['flips']:.1f}" if "/bills" not in k else "-"
        lines.append(
            f"| `{k}` | {m['sharpe']:.3f} | {m['d']:+.4f} | {m['se']:.4f} | **{m['z']:+.2f}** | "
            f"{m['p']:.3f} | {m['corr']:.3f} | {Z_BAR * m['se']:+.3f} | {m['te']:.2%} | {dd} | "
            f"{m['expo']:.2f} | {fl} | {m['z_end']:.2f} | {m['z_med']:.2f} "
            f"({m['z_min']:.2f}-{m['z_max']:.2f}) | {m['same']:.0%} |"
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
    text = [f"# {IDEA}: results (card `cards/wide-19.md`)", ""]
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
