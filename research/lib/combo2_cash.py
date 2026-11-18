"""combo-2, step 1 (`combo-cash`): combo-1's map and blends rerun with T-bill interest on cash.

    uv run --with numpy python research/lib/combo2_cash.py          # the rerun (logs tries)
    COMBO_DRY=1 uv run --with numpy python research/lib/combo2_cash.py  # nothing logged/written

Card: research/combo-2.md, "Step 1 card". Nothing new is chosen: the same models, blends,
shares, costs and regime masks as combo-1; only the gym now pays idle cash the 13-week T-bill
rate (`gym.simulate(rates=...)`, PR #61, merged into this branch).

Writes research/results/combo-2-cash.md.
"""

from __future__ import annotations

import dataclasses
import math
import os
from datetime import date, timedelta

import combo1_blend as cb
import combo1_map as cm
import common as c
import deep1_atlas as da
import deep1_models as dm
import harness
import numpy as np
import stats

from grimstrade import gym, report

IDEA = "combo-2"
DRY = bool(os.environ.get("COMBO_DRY"))
RATES = harness.bill_rates("train")
PENDING: list[tuple[c.Run, str, date, date]] = []
MAP_GYM = ["tsmom12", "trend-vol", "where-vol", "stop-0.25", "inverse-vol", "sixty-forty"]


def make(name: str, u: c.Ctx) -> c.ResearchStrategy:
    if name in cb.SLEEVES:
        return cb.SLEEVES[name]()
    return dm.BY_NAME[name].make(u)


def cash_run(name: str, u: c.Ctx, tag: str | None = None) -> c.Run:
    """A logged configuration replayed with T-bill cash at protocol costs."""
    return harness.run(
        IDEA, tag or name, make(name, u), period=u.period, panel=u.panel, history=u.hist,
        start=u.start, end=u.end, costs=cb.PROTO, log=False, rates=RATES,
    )  # fmt: skip


def bill_rets(u: c.Ctx) -> np.ndarray:
    """What one dollar of cash earned each calendar day from u.start, in the same gym (an
    all-cash book), so `run.rets - bill_rets(u)` is aligned day for day."""
    res = gym.simulate([gym.Decision(harness.decide_time(u.start), {})], u.hist, rates=RATES)
    _, eq = harness._calendar(res.equity)
    out: np.ndarray = eq[1:] / eq[:-1] - 1
    return out


def above(run: c.Run, rf: np.ndarray) -> c.Run:
    """The run's returns above the bill rate, as a Run (for era cuts and drawdowns)."""
    r = run.rets
    assert len(r) == len(rf), (len(r), len(rf))
    eq = run.equity[0] * np.concatenate([[1.0], np.cumprod(1 + r - rf)])
    return dataclasses.replace(run, equity=eq)


# --- the map ---


def map_section(u: c.Ctx) -> list[str]:
    a = da.load()
    rf_six = bill_rets(u)
    r: dict[str, np.ndarray] = {}
    sh_rf: dict[str, list[float]] = {}
    wins = [
        ("all", date(1994, 2, 1), date(2025, 11, 10)),
        ("2003-25", cb.SINCE, date(2025, 11, 10)),
    ]
    wins += [(nm, lo, hi) for nm, lo, hi in cb.ERA5]
    for name in [*MAP_GYM, "equal-weight"]:
        run = cash_run(name, u)
        s = dm.to_series(run, u, name)
        assert len(s.rets) == len(a.days) - 1 and int(s.days[0]) == int(a.days[0]), name
        r[name] = s.rets
        if name in MAP_GYM:
            PENDING.append((dataclasses.replace(run, variant=f"{name} cash"), "robustness",
                            u.start, u.end))  # fmt: skip
        ex = above(run, rf_six)
        sh_rf[name] = [cb.era_sh(ex, lo, hi) for _, lo, hi in wins]
        old = stats.sharpe(a.rets[name][np.isfinite(a.rets[name])]) if name in a.rets else math.nan
        print(
            f"map {name}: Sharpe {stats.sharpe(run.rets):.3f} (atlas, no interest {old:.3f})",
            flush=True,
        )
    # tsmom12 without interest must be the atlas series (plumbing check)
    plain = harness.run(
        IDEA, "check", make("tsmom12", u), period=u.period, panel=u.panel, history=u.hist,
        start=u.start, end=u.end, costs=cb.PROTO, log=False,
    )  # fmt: skip
    got = dm.to_series(plain, u, "tsmom12").rets
    assert np.allclose(got, a.rets["tsmom12"], equal_nan=True), "tsmom12 rebuild differs"
    print("tsmom12 without interest reproduces the atlas series", flush=True)
    r["band"] = cm.carry_rets(a.days)
    note = (
        "Card: `combo-2.md`, step 1. combo-1's map with idle cash earning the 13-week T-bill "
        "rate (gym PR #61): the six gym models rebuilt from their logged configurations at "
        "protocol costs (25 + 5 bps crypto, 2 bps ETFs), regime masks unchanged from combo-1 "
        "(computed without interest). Sharpe on calendar days, against 0 (the carded "
        "statistic); Sharpe above T-bills in the extra table at the end. Excess = model's "
        "daily return minus `tsmom12`'s (both with interest), annualised, % a year."
    )
    out, _ = cm.tables(a, r, cm.masks(a), "## A. The failure map with T-bill cash", note)
    out = [x.replace("## ", "### ", 1) if x.startswith("## ") and i > 0 else x
           for i, x in enumerate(out)]  # fmt: skip
    out += [
        "### 6. Sharpe above T-bills by era (gym models, #61's convention)",
        "",
        "| Model |" + "".join(f" {w[0]} |" for w in wins),
        "|---|" + "---:|" * len(wins),
        *[f"| `{m}` |" + "".join(f" {cb.f2(x)} |" for x in v) for m, v in sh_rf.items()],
        "",
    ]
    return out


# --- the blends ---


def blend(name: str, u: c.Ctx, runs: dict[str, c.Run]) -> tuple[c.Run, np.ndarray]:
    parts = [runs[s] for s in cb.BLENDS[name]]
    syms = u.panel.syms
    assert all(p.days[0] == u.start for p in parts)
    n_dec = len(parts[0].decisions)
    sh = cb.shares_by_day([p.rets for p in parts], u.start, n_dec)
    w = sum(sh[:, [j]] * cb.weights(p, syms) for j, p in enumerate(parts))
    decs = [
        gym.Decision(
            harness.decide_time(u.start + timedelta(days=k)),
            harness.clean({s: float(x) for s, x in zip(syms, w[k], strict=True)}),
        )
        for k in range(n_dec)
    ]
    res = gym.simulate(decs, u.hist, costs=cb.PROTO, rates=RATES)
    tag = f"{name} cash" if u.name == "six" else f"{name} cash@{u.name}"
    cal, eq = harness._calendar(res.equity)
    run = c.Run(IDEA, tag, "train", report.score(f"{IDEA}/{tag}", res), cal, eq,
                float(np.mean([sum(d.weights.values()) for d in decs])), decs)  # fmt: skip
    PENDING.append((run, "robustness", u.start, u.end))
    return run, sh


def verdict_for(
    run: c.Run, twin: c.Run, ew: c.Run, u: c.Ctx, v: dict[str, object], uname: str
) -> str:
    x, y = c.align(run, twin)
    d, p, _, _ = stats.sharpe_diff_boot(x, y)
    dd, ddt = stats.max_drawdown(run.rets), stats.max_drawdown(twin.rets)
    v[uname] = {"d": d, "p": p, "dd": dd, "ddt": ddt}
    if uname == "six":
        v["eras"] = [(cb.era_sh(run, lo, hi), cb.era_sh(twin, lo, hi)) for _, lo, hi in cb.ERA5]
        v["since"] = (
            stats.sharpe(run.rets_between(cb.SINCE, u.end)),
            stats.sharpe(twin.rets_between(cb.SINCE, u.end)),
            stats.sharpe(ew.rets_between(cb.SINCE, u.end)),
        )
        v["ew"] = stats.sharpe(ew.rets)
        v["sh"] = stats.sharpe(run.rets)
    return f"{d:+.2f} | {p:.3f}"


def blend_section() -> list[str]:
    out = [
        "## B. The two blends with T-bill cash",
        "",
        "combo-1's card unchanged (equal-risk shares refitted yearly, protocol costs); every "
        "book (sleeves, blend, `tsmom12` twin, equal weight) earns the T-bill rate on idle "
        f"cash. p = paired stationary bootstrap, one-sided; bar p < {cb.P_BAR:.4f} (family "
        f"{cb.FAMILY}). Left: Sharpe against 0 (the card); right: above T-bills.",
        "",
    ]
    v0: dict[str, dict[str, object]] = {b: {} for b in cb.BLENDS}
    v1: dict[str, dict[str, object]] = {b: {} for b in cb.BLENDS}
    six: dict[str, c.Run] = {}
    six_x: dict[str, c.Run] = {}
    twin_six = ew_six = twin_six_x = ew_six_x = None
    for uname in ("six", "etf", "coin", "idx"):
        u = c.ctx(uname)
        rf = bill_rets(u)
        runs = {s: cash_run(s, u) for s in cb.SLEEVES}
        ew = cash_run("equal-weight", u)
        twin = runs["tsmom12"]
        rows = []
        for b in cb.BLENDS:
            run, sh = blend(b, u, runs)
            run_x, twin_x, ew_x = above(run, rf), above(twin, rf), above(ew, rf)
            s0 = verdict_for(run, twin, ew, u, v0[b], uname)
            s1 = verdict_for(run_x, twin_x, ew_x, u, v1[b], uname)
            rows.append(
                f"| `{b}` | {stats.sharpe(run.rets):.2f} | {s0} | {stats.sharpe(run_x.rets):.2f}"
                f" | {s1} | {stats.max_drawdown(run.rets) * 100:.1f} |"
                f" {stats.cagr(run.rets) * 100:+.1f} |"
                f" {' / '.join(f'{x:.2f}' for x in sh.mean(axis=0))} |"
            )
            if uname == "six":
                six[b], six_x[b] = run, run_x
                twin_six, ew_six, twin_six_x, ew_six_x = twin, ew, twin_x, ew_x
        for nm, r0 in (("tsmom12", twin), ("equal-weight", ew)):
            rows.append(
                f"| `{nm}` | {stats.sharpe(r0.rets):.2f} | | | {stats.sharpe(r0.rets - rf):.2f}"
                f" | | | {stats.max_drawdown(r0.rets) * 100:.1f} |"
                f" {stats.cagr(r0.rets) * 100:+.1f} | |"
            )
        title = "Six live assets" if uname == "six" else cb.SETS[uname]
        out += [
            f"### {title}, from {u.start} (average bill rate {rf.mean() * 365 * 100:.1f}%)",
            "",
            "| Book | Sharpe | vs `tsmom12` | p | Sharpe above bills | vs `tsmom12` | p |"
            " Worst loss % | Growth %/yr | Mean shares |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
            *rows,
            "",
        ]
    assert twin_six is not None and ew_six is not None
    assert twin_six_x is not None and ew_six_x is not None
    era0 = cb.era_table(six, twin_six, ew_six)
    era1 = cb.era_table(six_x, twin_six_x, ew_six_x)
    era0[0] = "### Sharpe by era (six assets, against 0)"
    era1[0] = "### Sharpe by era (six assets, above T-bills)"
    reg = cb.regime_table(six, twin_six)
    reg[0] = "### Excess over `tsmom12` by the map's regimes (% a year, six assets, with cash)"
    bar0, bar1 = cb.bar_table(v0), cb.bar_table(v1)
    bar0[0] = "### Pass bar, Sharpe against 0 (the card)"
    bar1[0] = "### Pass bar, Sharpe above T-bills (#61's convention)"
    return [*out, *era0, *era1, *reg, *bar0, *bar1]


def main() -> None:
    out = ["# combo-2, step 1: combo-1 rerun with T-bill cash", ""]
    out += map_section(c.ctx("six"))
    out += blend_section()
    text = "\n".join(out)
    print(text)
    if not DRY:
        for run, kind, a, b in PENDING:
            harness._log(run, kind, a, b)
        (harness.RESEARCH / "results" / "combo-2-cash.md").write_text(text + "\n")


if __name__ == "__main__":
    assert not math.isnan(RATES[-1][1])
    main()
