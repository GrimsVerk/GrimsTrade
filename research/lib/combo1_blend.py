"""combo-1, step 2: the two carded blends (research/combo-1.md, "Step 2: card").

    uv run --with numpy python research/lib/combo1_blend.py          # the test (logs tries)
    COMBO_DRY=1 uv run --with numpy python research/lib/combo1_blend.py  # nothing logged/written

A: `blend-iv` = `tsmom12` + `inverse-vol`; B: `blend-ws` = `where-vol` + `stop-0.25`. Sleeve
shares are equal risk (1 / sd of the sleeve's weekly returns over the last 156 weeks before the
refit), refitted on the first Friday of each year from returns up to the day before. The
combined target weights go through `gym.simulate` as one account at the protocol's costs
(25 + 5 bps crypto, 2 bps ETFs; `main`'s gym default is 60 bps and is not used here).

Writes research/results/combo-1.md.
"""

from __future__ import annotations

import math
import os
from collections.abc import Callable
from datetime import date, timedelta

import cointop1_carry as ct
import combo1_map as cm
import common as c
import harness
import numpy as np
import stats
import trend_where as tw
from harness import ERAS

from grimstrade import gym, report
from grimstrade.data import CRYPTO, ETF

IDEA = "combo-1"
DRY = bool(os.environ.get("COMBO_DRY"))  # not `DRY`: common.DRY cuts the data to 120 days
PENDING: list[tuple[c.Run, str, date, date]] = []
PROTO: dict[str, gym.Costs] = {
    CRYPTO: gym.Costs(fee=0.0025, slip=0.0005),
    ETF: gym.Costs(fee=0.0, slip=0.0002),
}
LOOKBACK_WEEKS = 156
MIN_WEEKS = 26
FAMILY = 72
P_BAR = 0.10 / FAMILY
SINCE = date(2003, 1, 1)
ERA5 = [e for e in ERAS if e[1].year >= 1994]
SETS = {"etf": "8 other ETFs", "coin": "6 other coins", "idx": "4 indexes as one portfolio"}
LOGGED = {"tsmom12": 1.05, "inverse-vol": 0.85, "where-vol": 1.07, "stop-0.25": 1.09}

Make = Callable[[], c.ResearchStrategy]
SLEEVES: dict[str, Make] = {
    "tsmom12": lambda: c.weekly(c.slots(c.tsmom_signal)),
    "inverse-vol": lambda: c.weekly(c.inverse_vol),
    "where-vol": lambda: tw.Where("vol").strategy(),
    "stop-0.25": lambda: ct.rule(ct.stop_ok),
}
BLENDS = {"blend-iv": ("tsmom12", "inverse-vol"), "blend-ws": ("where-vol", "stop-0.25")}


def sleeve(name: str, u: c.Ctx) -> c.Run:
    """A logged configuration rebuilt at protocol costs, not logged again."""
    return harness.run(
        "combo-1-sleeve", name, SLEEVES[name](), period=u.period, panel=u.panel,
        history=u.hist, start=u.start, end=u.end, costs=PROTO, log=False,
    )  # fmt: skip


def weights(run: c.Run, syms: list[str]) -> np.ndarray:
    """Days x assets target weights, one row per daily decision from the run's first day."""
    w = np.zeros((len(run.decisions), len(syms)))
    for k, d in enumerate(run.decisions):
        for s, x in d.weights.items():
            w[k, syms.index(s)] = x
    return w


def first_friday(year: int) -> date:
    d = date(year, 1, 1)
    return d + timedelta(days=(4 - d.weekday()) % 7)


def risk_share(rets: list[np.ndarray], upto: int) -> np.ndarray:
    """Equal-risk shares from each sleeve's daily returns of the days before the refit:
    `rets[j][:upto]` are the returns of days start+1 .. refit-1 (nothing later is read)."""
    sd = []
    for r in rets:
        x = r[:upto]
        k = min(len(x) // 7, LOOKBACK_WEEKS)
        if k < MIN_WEEKS:
            return np.full(len(rets), 1 / len(rets))
        blocks = np.prod(1 + x[len(x) - k * 7 :].reshape(k, 7), axis=1) - 1
        sd.append(blocks.std())
    inv = 1 / np.maximum(np.array(sd), 1e-12)
    out: np.ndarray = inv / inv.sum()
    return out


def shares_by_day(rets: list[np.ndarray], start: date, n_dec: int) -> np.ndarray:
    """Per decision day: the shares of the refit in force (first Friday of each year)."""
    out = np.full((n_dec, len(rets)), 1 / len(rets))
    end = start + timedelta(days=n_dec - 1)
    for year in range(start.year, end.year + 1):
        r = first_friday(year)
        if r <= start:
            continue
        k = (r - start).days
        out[k:] = risk_share(rets, k - 1)  # returns of days start+1 .. r-1
    return out


def check_no_lookahead() -> None:
    """Scrambling every return on or after a refit day leaves that refit's shares unchanged."""
    rng = np.random.default_rng(1)
    start = date(2000, 1, 1)
    n = 2000
    a, b = rng.normal(0, 0.01, n), rng.normal(0, 0.02, n)
    base = shares_by_day([a, b], start, n + 1)
    for year in (2001, 2003, 2005):
        k = (first_friday(year) - start).days
        a2, b2 = a.copy(), b.copy()
        a2[k - 1 :] = rng.normal(0, 0.05, n - k + 1)
        b2[k - 1 :] = rng.normal(0, 0.001, n - k + 1)
        got = shares_by_day([a2, b2], start, n + 1)
        assert np.allclose(got[: k + 1], base[: k + 1]), year
    print("look-ahead check passed", flush=True)


def blend(name: str, u: c.Ctx, runs: dict[str, c.Run], kind: str) -> tuple[c.Run, np.ndarray]:
    parts = [runs[s] for s in BLENDS[name]]
    syms = u.panel.syms
    assert all(p.days[0] == u.start for p in parts)
    n_dec = len(parts[0].decisions)
    sh = shares_by_day([p.rets for p in parts], u.start, n_dec)
    w = sum(sh[:, [j]] * weights(p, syms) for j, p in enumerate(parts))
    decs = [
        gym.Decision(
            harness.decide_time(u.start + timedelta(days=k)),
            harness.clean({s: float(x) for s, x in zip(syms, w[k], strict=True)}),
        )
        for k in range(n_dec)
    ]
    res = gym.simulate(decs, u.hist, costs=PROTO)
    tag = name if u.name == "six" else f"{name}@{u.name}"
    cal, eq = harness._calendar(res.equity)
    run = c.Run(IDEA, tag, "train", report.score(f"{IDEA}/{tag}", res), cal, eq,
                float(np.mean([sum(d.weights.values()) for d in decs])), decs)  # fmt: skip
    PENDING.append((run, kind, u.start, u.end))  # logged once every run has finished
    return run, sh


def dist(run: c.Run, twin: c.Run, syms: list[str]) -> float:
    """Average half-sum of absolute weight differences to `tsmom12`'s targets."""
    a, b = weights(run, syms), weights(twin, syms)
    k = min(len(a), len(b))
    return float(np.abs(a[:k] - b[:k]).sum(axis=1).mean() / 2)


def era_sh(run: c.Run, a: date, b: date) -> float:
    r = run.rets_between(a, b)
    return stats.sharpe(r) if len(r) > 250 else math.nan


def f2(x: float, spec: str = ".2f") -> str:
    return "-" if math.isnan(x) else format(x, spec)


def main() -> None:
    check_no_lookahead()
    out = ["# combo-1, step 2: the two carded blends", ""]
    out += [
        'Card: `combo-1.md`, "Step 2: card". Train period, total-return prices, protocol '
        "costs (25 + 5 bps crypto, 2 bps ETFs). Sharpe on calendar days. p = paired stationary "
        f"bootstrap, one-sided, against `tsmom12`; bar p < 0.10 / {FAMILY} = {P_BAR:.4f}.",
        "",
    ]
    verdict: dict[str, dict[str, object]] = {b: {} for b in BLENDS}
    six_runs: dict[str, c.Run] = {}
    for uname in ("six", "etf", "coin", "idx"):
        u = c.ctx(uname)
        runs = {s: sleeve(s, u) for s in SLEEVES}
        ew = harness.run(
            "combo-1-sleeve", "equal-weight", c.weekly(c.equal_weight), period=u.period,
            panel=u.panel, history=u.hist, start=u.start, end=u.end, costs=PROTO, log=False,
        )  # fmt: skip
        if uname == "six":
            for s, want in LOGGED.items():
                got = stats.sharpe(runs[s].rets)
                assert abs(got - want) < 0.006, f"{s}: {got:.3f} vs logged {want}"
            print("sleeves reproduce their logged Sharpe", flush=True)
        else:
            if uname != "coin":  # the coin stop leaves ETF and index books untouched
                same = [d.weights for d in runs["stop-0.25"].decisions]
                assert same == [d.weights for d in runs["tsmom12"].decisions], uname
        twin = runs["tsmom12"]
        rows = []
        for b, kind in ((b, "variant" if uname == "six" else "robustness") for b in BLENDS):
            run, sh = blend(b, u, runs, kind)
            x, y = c.align(run, twin)
            d, p, lo, hi = stats.sharpe_diff_boot(x, y)
            dd, ddt = stats.max_drawdown(run.rets), stats.max_drawdown(twin.rets)
            mean_sh = sh.mean(axis=0)
            rows.append(
                f"| `{b}` | {stats.sharpe(x):.2f} | {d:+.2f} | {p:.3f} | {dd * 100:.1f} |"
                f" {stats.cagr(run.rets) * 100:+.1f} | {run.score.turnover:.2f} |"
                f" {' / '.join(f'{v:.2f}' for v in mean_sh)} |"
                f" {dist(run, twin, u.panel.syms) * 100:.0f}% |"
            )
            verdict[b][uname] = {"d": d, "p": p, "dd": dd, "ddt": ddt}
            if uname == "six":
                six_runs[b] = run
                verdict[b]["eras"] = [
                    (era_sh(run, lo_, hi_), era_sh(twin, lo_, hi_)) for _, lo_, hi_ in ERA5
                ]
                verdict[b]["since"] = (
                    stats.sharpe(run.rets_between(SINCE, u.end)),
                    stats.sharpe(twin.rets_between(SINCE, u.end)),
                    stats.sharpe(ew.rets_between(SINCE, u.end)),
                )
                verdict[b]["ew"] = stats.sharpe(ew.rets)
                verdict[b]["sh"] = stats.sharpe(run.rets)
        for s in ("tsmom12", "equal-weight"):
            r = twin if s == "tsmom12" else ew
            rows.append(
                f"| `{s}` | {stats.sharpe(r.rets):.2f} | | | {stats.max_drawdown(r.rets) * 100:.1f}"
                f" | {stats.cagr(r.rets) * 100:+.1f} | {r.score.turnover:.2f} | | |"
            )
        title = "Six live assets" if uname == "six" else SETS[uname]
        out += [
            f"## {title}, from {u.start}",
            "",
            "| Book | Sharpe | vs `tsmom12` | p | Worst loss % | Growth %/yr | Turnover |"
            " Mean shares (sleeve 1 / 2) | Distance from `tsmom12` |",
            "|---|---:|---:|---:|---:|---:|---:|---|---:|",
            *rows,
            "",
        ]
        if uname == "six":
            out += era_table(six_runs, twin, ew)
            out += regime_table(six_runs, twin)

    out += bar_table(verdict)
    text = "\n".join(out)
    print(text)
    if not DRY:
        for run, kind, a, b in PENDING:
            harness._log(run, kind, a, b)
        (harness.RESEARCH / "results" / "combo-1.md").write_text(text)


def era_table(runs: dict[str, c.Run], twin: c.Run, ew: c.Run) -> list[str]:
    wins = [("all", date(1994, 2, 1), date(2025, 11, 10)), ("2003-25", SINCE, date(2025, 11, 10))]
    wins += [(n, a, b) for n, a, b in ERA5]
    rows = []
    for nm, r in [*runs.items(), ("tsmom12", twin), ("equal-weight", ew)]:
        rows.append(f"| `{nm}` |" + "".join(f" {f2(era_sh(r, a, b))} |" for _, a, b in wins))
    return [
        "### Sharpe by era (six assets)",
        "",
        "| Book |" + "".join(f" {w[0]} |" for w in wins),
        "|---|" + "---:|" * len(wins),
        *rows,
        "",
    ]


def regime_table(runs: dict[str, c.Run], twin: c.Run) -> list[str]:
    a = cm.da.load()
    m = cm.masks(a)
    n = len(a.rets["tsmom12"])
    rows = []
    for nm, r in runs.items():
        x = r.rets - twin.rets
        assert len(x) == n, (len(x), n)
        rows.append(f"| `{nm}` |" + "".join(f" {cm.pc(cm.ann(x[m[k]]))} |" for k in m))
    return [
        "### Excess over `tsmom12` by the map's regimes (% a year, six assets)",
        "",
        "| Book |" + "".join(f" {k} |" for k in m),
        "|---|" + "---:|" * len(m),
        *rows,
        "",
    ]


def bar_table(v: dict[str, dict[str, object]]) -> list[str]:
    rows = []
    for b, d in v.items():
        six = d["six"]
        assert isinstance(six, dict)
        eras = d["eras"]
        assert isinstance(eras, list)
        ahead = sum(1 for x, y in eras if x > y)
        oou = [d[s] for s in SETS]
        pos = sum(1 for o in oou if isinstance(o, dict) and o["d"] > 0)
        since = d["since"]
        assert isinstance(since, tuple)
        ew = d["ew"]
        assert isinstance(ew, float)
        sh_six = d["sh"]
        assert isinstance(sh_six, float)
        bars = [
            (f"{six['d']:+.2f}, p {six['p']:.3f}", six["p"] < P_BAR),
            (f"{ahead} of 5", ahead >= 4),
            (f"{six['dd'] * 100:.1f}% vs {six['ddt'] * 100:.1f}%", six["dd"] <= six["ddt"] + 0.05),
            (
                ", ".join(f"{s} {o['d']:+.2f}" for s, o in zip(SETS, oou, strict=True)),  # type: ignore[index]
                pos >= 2,
            ),
            (f"{sh_six:.2f} vs EW {ew:.2f}", sh_six > ew),
            (
                f"{since[0]:.2f} vs {since[1]:.2f} / EW {since[2]:.2f}",
                since[0] >= since[1] and since[0] >= since[2],
            ),
        ]
        cells = " | ".join(f"{t} {'pass' if ok else 'FAIL'}" for t, ok in bars)
        rows.append(f"| `{b}` | {cells} | {'PASS' if all(ok for _, ok in bars) else 'fail'} |")
    return [
        "## Pass bar",
        "",
        f"| Blend | 1. p < {P_BAR:.4f} | 2. eras | 3. worst loss | 4. out of universe |"
        " 5. beats EW | 6. since 2003 | Verdict |",
        "|---|---|---|---|---|---|---|---|",
        *rows,
        "",
    ]


if __name__ == "__main__":
    main()
