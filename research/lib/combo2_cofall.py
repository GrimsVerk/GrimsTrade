"""combo-2, step 2: `cofall-dbc`, a DBC slot for the weeks stocks and bonds are both out.

    uv run --with numpy python research/lib/combo2_cofall.py          # the test (logs 1 try)
    COMBO_DRY=1 uv run --with numpy python research/lib/combo2_cofall.py  # nothing logged/written

Card: research/combo-2.md, "Step 2 card". `tsmom12` on the six live assets; when SPY and TLT
are both eligible and both out of trend (365-day return <= 0), and DBC is eligible and in trend,
DBC gets one slot (1/n of the six-asset slots) from cash. Both books earn T-bill interest on
cash (step 1's accounting), protocol costs. Writes research/results/combo-2-cofall.md.
"""

from __future__ import annotations

import bisect
import math
import os
from collections.abc import Callable
from datetime import date

import combo1_blend as cb
import combo1_map as cm
import combo2_cash as cc
import common as c
import deep1_atlas as da
import harness
import numpy as np
import stats
from harness import STRESS, SYMS

IDEA = "combo-2"
VARIANT = "cofall-dbc"
DRY = bool(os.environ.get("COMBO_DRY"))
FAMILY = 73
P_BAR = 0.10 / FAMILY
PARTNER = "DBC"


def gate_open(view: c.View) -> bool:
    held = [s for s in SYMS if c.eligible(view, s)]
    return (
        "SPY" in held
        and "TLT" in held
        and not c.tsmom_signal(view, "SPY")
        and not c.tsmom_signal(view, "TLT")
    )


def partner_ok(view: c.View) -> bool:
    return c.eligible(view, PARTNER) and c.tsmom_signal(view, PARTNER)


def cofall(view: c.View) -> c.Weights:
    held = [s for s in SYMS if c.eligible(view, s)]
    if not held:
        return {}
    w = {s: 1 / len(held) for s in held if c.tsmom_signal(view, s)}
    if gate_open(view) and partner_ok(view):
        w[PARTNER] = 1 / len(held)
    return w


def flag(test: Callable[[c.View], bool]) -> c.ResearchStrategy:
    """A yes/no per decision day, as weights, so it goes through the same weekly wrapper."""
    return c.weekly(lambda v: {"SPY": 1.0} if test(v) else {})


def ctx7(six: c.Ctx) -> c.Ctx:
    hist = harness.load_history("train", True, [*SYMS, PARTNER])
    return c.Ctx("six+dbc", "train", hist, harness.Panel(hist), six.start, six.end)


def sh(r: np.ndarray) -> float:
    return stats.sharpe(r) if len(r) > 250 else math.nan


def tot(r: np.ndarray) -> float:
    return float(np.prod(1 + r) - 1)


def spells(mask: np.ndarray, start: date) -> list[tuple[date, date, int, int]]:
    """Contiguous runs of True: (first day, last day, start index, end index exclusive)."""
    out = []
    k = 0
    n = len(mask)
    while k < n:
        if mask[k]:
            j = k
            while j < n and mask[j]:
                j += 1
            out.append((date.fromordinal(start.toordinal() + k),
                        date.fromordinal(start.toordinal() + j - 1), k, j))  # fmt: skip
            k = j
        else:
            k += 1
    return out


def main() -> None:
    six = c.ctx("six")
    u7 = ctx7(six)
    strat = c.weekly(cofall)
    gday = [date(2008, 11, 14), date(2018, 12, 14), date(2022, 6, 17), date(2022, 10, 14)]
    harness.check_against_gym(strat, u7.hist, gday)
    print("fast path equals gym.backtest on the check days", flush=True)

    run = harness.run(
        IDEA, VARIANT, strat, period="train", panel=u7.panel, history=u7.hist,
        start=u7.start, end=u7.end, costs=cb.PROTO, log=False, rates=cc.RATES,
    )  # fmt: skip
    twin = cc.cash_run("tsmom12", six)
    ew = cc.cash_run("equal-weight", six)
    rf = cc.bill_rets(six)
    assert run.days == twin.days, (run.days[0], run.days[-1], twin.days[-1])

    gate = np.array([bool(d.weights) for d in harness.decisions(flag(gate_open), u7.panel,
                                                                u7.start, u7.end)])  # fmt: skip
    held = np.array([PARTNER in d.weights for d in run.decisions])
    # identity: with the gate closed the book is the twin, and DBC is held only in the gate
    for k, (a, b) in enumerate(zip(run.decisions, twin.decisions, strict=True)):
        six_part = {s: x for s, x in a.weights.items() if s != PARTNER}
        assert six_part == b.weights, (k, a.weights, b.weights)
        assert not held[k] or gate[k], k
    print("identity check passed: off the gate the book is the twin", flush=True)

    n = len(run.rets)
    g = gate[:n]  # decision k sets the holdings behind return k
    hh = held[:n]
    ex = run.rets - twin.rets
    first_held = date.fromordinal(u7.start.toordinal() + int(np.argmax(hh))) if hh.any() else None
    x_run, x_twin, x_ew = cc.above(run, rf), cc.above(twin, rf), cc.above(ew, rf)
    d0, p0, lo0, hi0 = stats.sharpe_diff_boot(run.rets, twin.rets)
    d1, p1, lo1, hi1 = stats.sharpe_diff_boot(x_run.rets, x_twin.rets)
    dd, ddt = stats.max_drawdown(run.rets), stats.max_drawdown(twin.rets)
    wins = [("all", six.start, date(2025, 11, 10)), ("2003-25", cb.SINCE, date(2025, 11, 10))]
    wins += [(nm, a, b) for nm, a, b in cb.ERA5]

    out = ["# combo-2, step 2: `cofall-dbc`", ""]
    out += [
        'Card: `combo-2.md`, "Step 2 card". Six live assets plus DBC, train period, total-return '
        "prices, protocol costs (25 + 5 bps crypto, 2 bps ETFs), T-bill interest on cash for "
        "every book. Sharpe on calendar days. p = paired stationary bootstrap, one-sided, "
        f"against the `tsmom12` twin; bar p < 0.10 / {FAMILY} = {P_BAR:.5f}.",
        "",
        f"Gate open (SPY and TLT both out of trend): {g.sum()} of {n} days ({g.mean():.1%}), "
        f"{g.sum() / 7:.0f} weeks; DBC held {hh.sum()} days ({hh.sum() / 7:.0f} weeks). "
        f"First day DBC was held: {first_held}.",
        "",
        "## Full train",
        "",
        "| Book | Sharpe | vs twin | p | 90% range | Sharpe above bills | vs twin | p |"
        " Worst loss % | Growth %/yr |",
        "|---|---:|---:|---:|---|---:|---:|---:|---:|---:|",
        f"| `{VARIANT}` | {sh(run.rets):.2f} | {d0:+.3f} | {p0:.3f} | {lo0:+.3f}..{hi0:+.3f} |"
        f" {sh(x_run.rets):.2f} | {d1:+.3f} | {p1:.3f} | {dd * 100:.1f} |"
        f" {stats.cagr(run.rets) * 100:+.2f} |",
        f"| `tsmom12` (twin) | {sh(twin.rets):.2f} | | | | {sh(x_twin.rets):.2f} | | |"
        f" {ddt * 100:.1f} | {stats.cagr(twin.rets) * 100:+.2f} |",
        f"| `equal-weight` | {sh(ew.rets):.2f} | | | | {sh(x_ew.rets):.2f} | | |"
        f" {stats.max_drawdown(ew.rets) * 100:.1f} | {stats.cagr(ew.rets) * 100:+.2f} |",
        "",
        "## Sharpe by era (against 0 / above bills)",
        "",
        "| Book |" + "".join(f" {w[0]} |" for w in wins),
        "|---|" + "---:|" * len(wins),
    ]
    eras: dict[str, list[tuple[float, float]]] = {}
    for nm, r0, r1 in (
        (VARIANT, run, x_run),
        ("tsmom12", twin, x_twin),
        ("equal-weight", ew, x_ew),
    ):
        eras[nm] = [(cb.era_sh(r0, a, b), cb.era_sh(r1, a, b)) for _, a, b in wins]
        out.append(f"| `{nm}` |" + "".join(f" {cb.f2(u)} / {cb.f2(v)} |" for u, v in eras[nm]))
    out.append("")

    # spells of the gate and what the partner did in them
    out += [
        "## Gate spells (SPY and TLT both out of trend)",
        "",
        "Points of total return in the spell (book minus twin; decision days, holdings from the "
        "next open). DBC weeks = weeks the partner was held.",
        "",
        "| Spell | Days | DBC weeks | Twin % | Book % | Book minus twin (points) | DBC own % |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    j_dbc = u7.panel.syms.index(PARTNER) if PARTNER in u7.panel.syms else -1
    assert j_dbc >= 0
    pan = u7.panel
    dbc_close = {
        date.fromordinal(int(o)): float(x)
        for o, x in zip(pan.ord[PARTNER], pan.c[PARTNER], strict=True)
    }
    dbc_days = sorted(dbc_close)

    def dbc_ret(a: date, b: date) -> float:
        i = bisect.bisect_right(dbc_days, a) - 1
        k = bisect.bisect_right(dbc_days, b) - 1
        if i < 0 or k < 0:
            return math.nan
        return dbc_close[dbc_days[k]] / dbc_close[dbc_days[i]] - 1

    for a, b, i, k in spells(g, u7.start):
        out.append(
            f"| {a} .. {b} | {k - i} | {hh[i:k].sum() / 7:.0f} | {tot(twin.rets[i:k]) * 100:+.1f} |"
            f" {tot(run.rets[i:k]) * 100:+.1f} |"
            f" {(tot(run.rets[i:k]) - tot(twin.rets[i:k])) * 100:+.1f} |"
            f" {cb.f2(dbc_ret(a, b) * 100, '+.1f')} |"
        )
    out.append("")

    # 2022 and the map's regimes
    def window(a: date, b: date) -> tuple[float, float]:
        return tot(run.rets_between(a, b)), tot(twin.rets_between(a, b))

    rows = []
    for nm, a, b in [("calendar 2022", date(2021, 12, 31), date(2022, 12, 31)),
                     *[(s, a, b) for s, a, b in STRESS if s == "2022 rate shock"],
                     ("2022-25", date(2021, 12, 31), date(2025, 11, 10))]:  # fmt: skip
        x, y = window(a, b)
        rows.append(f"| {nm} | {y * 100:+.1f} | {x * 100:+.1f} | {(x - y) * 100:+.1f} |")
    out += [
        "## 2022",
        "",
        "| Window | Twin % | Book % | Points |",
        "|---|---:|---:|---:|",
        *rows,
        "",
    ]
    a = da.load()
    M = cm.masks(a)
    assert len(a.rets["tsmom12"]) == n, (len(a.rets["tsmom12"]), n)
    M = {"gate open (own weeks)": g, **M}
    out += [
        "## Excess over the twin by regime (% a year)",
        "",
        "| Book |" + "".join(f" {k} |" for k in M),
        "|---|" + "---:|" * len(M),
        f"| `{VARIANT}` |" + "".join(f" {cm.pc(cm.ann(ex[m]))} |" for m in M.values()),
        "| *share of days* |" + "".join(f" *{m.mean() * 100:.1f}%* |" for m in M.values()),
        "",
    ]

    # the bar
    e = eras[VARIANT]
    t = eras["tsmom12"]
    era_idx = {w[0]: i for i, w in enumerate(wins)}
    five = [w[0] for w in wins[2:]]
    ahead22 = e[era_idx["2022-25"]][0] > t[era_idx["2022-25"]][0]
    ahead22x = e[era_idx["2022-25"]][1] > t[era_idx["2022-25"]][1]
    not_behind = all(
        e[era_idx[k]][0] >= t[era_idx[k]][0] - 0.01 and e[era_idx[k]][1] >= t[era_idx[k]][1] - 0.01
        for k in five
        if not math.isnan(e[era_idx[k]][0])
    )
    mech_gate = cm.ann(ex[g]) > 0
    mech_sb = cm.ann(ex[M["stock-bond corr > 0 (1y)"]]) > 0
    since = (
        stats.sharpe(run.rets_between(cb.SINCE, six.end)),
        stats.sharpe(twin.rets_between(cb.SINCE, six.end)),
        stats.sharpe(ew.rets_between(cb.SINCE, six.end)),
    )
    bars = [
        (f"vs 0 {d0:+.3f} p {p0:.3f}; above bills {d1:+.3f} p {p1:.3f}", p0 < P_BAR and p1 < P_BAR),
        (
            f"2022-25 ahead {ahead22 and ahead22x}; none behind {not_behind}",
            ahead22 and ahead22x and not_behind,
        ),  # fmt: skip
        (f"{dd * 100:.1f}% vs {ddt * 100:.1f}%", dd <= ddt + 0.05),
        (
            f"gate {cm.pc(cm.ann(ex[g]))}, stock-bond+ "
            f"{cm.pc(cm.ann(ex[M['stock-bond corr > 0 (1y)']]))} %/yr",
            mech_gate and mech_sb,
        ),  # fmt: skip
        (f"{sh(run.rets):.2f} vs EW {sh(ew.rets):.2f}", sh(run.rets) > sh(ew.rets)),
        (
            f"{since[0]:.2f} vs {since[1]:.2f} / EW {since[2]:.2f}",
            since[0] >= since[1] and since[0] >= since[2],
        ),  # fmt: skip
    ]
    cells = " | ".join(f"{txt} {'pass' if ok else 'FAIL'}" for txt, ok in bars)
    out += [
        "## Pass bar",
        "",
        f"| Book | 1. p < {P_BAR:.5f} (both) | 2. eras | 3. worst loss | 4. mechanism |"
        " 5. beats EW | 6. since 2003 | Verdict |",
        "|---|---|---|---|---|---|---|---|",
        f"| `{VARIANT}` | {cells} | {'PASS' if all(ok for _, ok in bars) else 'fail'} |",
        "",
    ]
    text = "\n".join(out)
    print(text)
    if not DRY:
        harness._log(run, "variant", u7.start, u7.end)
        (harness.RESEARCH / "results" / "combo-2-cofall.md").write_text(text + "\n")


if __name__ == "__main__":
    main()
