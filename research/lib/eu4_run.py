"""eu-4 step 2-3: two whipsaw reducers on `euw`, character test, fees by book (cards/eu-4.md).

    uv run --with numpy python research/lib/eu4_run.py check   # plumbing: no number printed
    uv run --with numpy python research/lib/eu4_run.py run     # 24 rows and the result

Needs the CSVs from `eu1_data.py build` and the saved runs of eu-1/eu-2/eu-3 under the
git-ignored research/data/runs/ (re-scored without new rows). Every new run is a row in
tries.md (idea `eu-4`); a run whose equity file already exists under research/data/runs/eu-4/
is re-scored without a new row. Train period only. Fee tiers are generic (EUR 1/2/3 per order,
eu-2's schedules unchanged).
"""

from __future__ import annotations

import csv
import math
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import eu1
import eu2
import eu3
import harness
import numpy as np
from eu4 import z_score
from harness import TRAIN_END, Run

from grimstrade import gym, report

IDEA = "eu-4"
W_START = eu1.W_START
F0 = eu3.F0
EUW, EU6, USW = eu1.EUW, eu1.EU6, eu1.USW
SIZES = eu3.SIZES  # 5k, 10k, 25k
TIERS = [("EUR 1", "eur1", eu2.SCHEDULES[1]), ("EUR 2", "eur2", eu2.SCHEDULES[2]),
         ("EUR 3", "eur3", eu2.SCHEDULES[3])]  # fmt: skip
LOSS_MAX, GAP_TOL, SHARPE_TOL, DD_TOL = 0.10, 0.15, 0.05, 0.02
CORR_MIN, CRASH_PTS = 0.80, 0.03
N_FAMILY = 8


@dataclass(frozen=True)
class Red:
    name: str
    confirm: bool = False  # switch only after two Fridays in a row with the new sign
    h: float = 0.0  # dead zone half-width in z


PLAIN = Red("plain")
C1 = Red("C1-confirm2", confirm=True)
C2 = Red("C2-dz25", h=0.25)
REDS = [C1, C2]


def friday_weights(red: Red, pan: harness.Panel) -> list[tuple[date, dict[str, float]]]:
    held: set[str] = set()
    prev: dict[str, bool] = {}
    out = []
    f = F0
    while f <= TRAIN_END:
        view = pan.view(harness.decide_time(f))
        live = c.live(view)
        for s in live:
            sig = c.tsmom_signal(view, s)
            if s not in prev:  # first live Friday: the house rule's state
                state = sig
            elif red.confirm:
                state = sig if sig == prev[s] else s in held
            elif red.h > 0:
                z = z_score(view, s)
                state = (s in held) if math.isnan(z) else (
                    z > red.h or (s in held and z >= -red.h))  # fmt: skip
            else:
                state = sig
            prev[s] = sig
            if state:
                held.add(s)
            else:
                held.discard(s)
        out.append((f, {s: 1 / len(live) for s in live if s in held}))
        f += timedelta(days=7)
    return out


def make_decisions(
    fw: list[tuple[date, dict[str, float]]], pan: harness.Panel
) -> list[gym.Decision]:
    """As eu-3's house rule: day d repeats the Friday on or before the view's last grid day."""
    by_day = dict(fw)
    out, d = [], W_START
    while d <= TRAIN_END:
        today = pan.view(harness.decide_time(d)).today
        f = max(today - timedelta(days=(today.weekday() - 4) % 7), F0)
        out.append(gym.Decision(harness.decide_time(d), harness.clean(by_day[f])))
        d += timedelta(days=1)
    return out


@dataclass
class Out:
    run: Run
    orders_yr: float
    entries_yr: float
    exits_yr: float
    drift_yr: float
    fees_yr: float


def simulate(
    variant: str, decs: list[gym.Decision], syms: Sequence[str], costs: Mapping[str, gym.Costs],
    st: eu2.FeeState, kind: str,
) -> Out:  # fmt: skip
    hist, _ = eu1.panel_for(syms)
    with eu2.fixed_fees(st):
        res = gym.simulate(decs, hist, costs=costs, band=eu3.BAND)
    sc = report.score(f"{IDEA}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    expo = float(np.mean([sum(d.weights.values()) for d in decs]))
    run = Run(IDEA, variant, "train", sc, days, equity, expo, decs)
    path = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    if not path.exists():
        harness._log(run, kind, W_START, TRAIN_END)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date", "equity"])
            w.writerows((d.isoformat(), repr(float(e))) for d, e in zip(days, equity))  # noqa: B905
        print("logged", variant, flush=True)
    else:
        print("re-scored", variant, flush=True)
    years = (days[-1] - days[0]).days / 365
    en, ex, ot = eu3.count_fills(res.fills)
    return Out(run, st.orders / years, en / years, ex / years, ot / years, st.paid / years)


def check() -> None:
    """No confirmation and h = 0 must reproduce the house rule's weights on all three books."""
    for syms in (EUW, EU6, USW):
        _, pan = eu1.panel_for(syms)
        mine = make_decisions(friday_weights(PLAIN, pan), pan)
        ref = harness.decisions(eu1.TSMOM, pan, W_START, TRAIN_END)
        if [(d.time, d.weights) for d in mine] != [(d.time, d.weights) for d in ref]:
            raise AssertionError(f"plain reducer differs from eu1.TSMOM on {syms}")
    print("check ok", flush=True)


def held_matrix(fw: list[tuple[date, dict[str, float]]], syms: Sequence[str]) -> np.ndarray:
    return np.array([[1.0 if s in w else 0.0 for s in syms] for _, w in fw])


def flips_yr(fw: list[tuple[date, dict[str, float]]], syms: Sequence[str]) -> float:
    m = held_matrix(fw, syms)
    return float(np.abs(np.diff(m, axis=0)).sum()) / ((fw[-1][0] - W_START).days / 365)


def positions(fa: list, fb: list, syms: Sequence[str], pan: harness.Panel) -> tuple[float, ...]:
    """(pooled 0/1 correlation, share agreeing, correlation of book exposure), live slots only."""
    a, b = held_matrix(fa, syms), held_matrix(fb, syms)
    live = np.array([[1.0 if s in c.live(pan.view(harness.decide_time(f))) else 0.0
                      for s in syms] for f, _ in fa])  # fmt: skip
    k = live.ravel() > 0
    x, y = a.ravel()[k], b.ravel()[k]
    return (
        float(np.corrcoef(x, y)[0, 1]),
        float(np.mean(x == y)),
        float(np.corrcoef(a.sum(1), b.sum(1))[0, 1]),
    )


def inside_crashes() -> list[tuple[str, date, date]]:
    return [(n, a, b) for n, a, b in eu1.CRASHES if a >= W_START]


def crash_rets(run: Run) -> list[float]:
    return [eu1.crash_ret(run, a, b) for _, a, b in inside_crashes()]


def sh(run: Run) -> float:
    return c.describe(run)["sharpe"]


def break_even(losses: list[float]) -> str:
    return eu3.break_even(losses)


def report_all() -> None:
    check()
    out = ["# eu-4 results: whipsaw reducers on `euw` (cards/eu-4.md)", ""]
    out += [
        "Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices; "
        "`euw` and `eu6` in EUR, `usw` in USD. Sharpe on calendar days, zero risk-free rate. "
        "`euw`/`eu6`: ETF slippage 0.05% a side (eu-2's costs; coins at the gym's); `usw`: the "
        "gym's costs (as eu-1). 1% band. `R` = the house rule `tsmom12`; C1 `confirm2` = switch "
        "only after two Fridays in a row with the new sign; C2 `dz25` = dead zone, enter above "
        "z = +0.25, leave below z = -0.25 (z = 12-month log return / one-year EWMA vol). Fee "
        "tiers: EUR 1, 2, 3 per ETF order on a constant book (eu-2's schedules; the EUR 1 and "
        "EUR 3 tiers also carry a EUR 2.50 yearly fee). `R`, V0 and equal weight on `euw` are "
        "eu-3's saved runs, re-scored.",
        "",
    ]
    # ---- euw at no fee ----
    _, pan = eu1.panel_for(EUW)
    fw_r = eu3.friday_weights(eu3.R, pan)
    zero = eu2.FeeState(0, 0)
    r_slip = eu3.simulate("tsmom12@euw/slip", eu3.make_decisions(eu3.R, pan), EUW, zero,
                          "robustness")  # fmt: skip
    ew_decs = harness.decisions(eu1.EW, pan, W_START, TRAIN_END)
    ew_slip = eu3.simulate("equal-weight@euw/slip", ew_decs, EUW, eu2.FeeState(0, 0), "baseline")
    v0 = eu3.VARIANTS[0]
    v0_decs = eu3.make_decisions(v0, pan)
    v0_slip = eu3.simulate("V0-w-fri@euw/slip", v0_decs, EUW, eu2.FeeState(0, 0), "variant")
    fws = {red.name: friday_weights(red, pan) for red in REDS}
    decs = {red.name: make_decisions(fws[red.name], pan) for red in REDS}
    slip: dict[str, Out] = {}
    for red in REDS:
        slip[red.name] = simulate(
            f"{red.name}@euw/slip", decs[red.name], EUW, eu2.COSTS, eu2.FeeState(0, 0), "variant"
        )
    ref_rets = crash_rets(r_slip.run)
    ew_rets = crash_rets(ew_slip.run)
    ref_signs = [np.sign(a - b) for a, b in zip(ref_rets, ew_rets)]  # noqa: B905
    dr = c.describe(r_slip.run)

    out += ["## 1. Character on `euw` at no fixed fee", ""]
    out += [
        "| Rule | Orders/yr | Entries | Exits | Drift | Signal flips/yr | Sharpe | Max DD | "
        "1. Position corr (agree; exposure corr) | 2. dSharpe | 3. dMax DD | 4. Crash signs "
        "match / worst window gap | Keeps character (euw) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|",
    ]
    flips_r = flips_yr(fw_r, EUW)
    out.append(
        f"| R `tsmom12` | {r_slip.orders_yr:.1f} | {r_slip.entries_yr:.1f} | {r_slip.exits_yr:.1f} "
        f"| {r_slip.topups_yr:.1f} | {flips_r:.1f} | {dr['sharpe']:.3f} | {dr['mdd']:.1%} | - | - "
        "| - | - | (reference) |"
    )
    out.append(
        f"| V0 (eu-3) | {v0_slip.orders_yr:.1f} | {v0_slip.entries_yr:.1f} | "
        f"{v0_slip.exits_yr:.1f} | {v0_slip.topups_yr:.1f} | {flips_r:.1f} | {sh(v0_slip.run):.3f} "
        f"| {c.describe(v0_slip.run)['mdd']:.1%} | 1.00 | "
        f"{sh(v0_slip.run) - dr['sharpe']:+.3f} | - | - | yes (eu-3) |"
    )
    keeps: dict[str, bool] = {}
    for red in REDS:
        o = slip[red.name]
        d = c.describe(o.run)
        corr, agree, ecorr = positions(fws[red.name], fw_r, EUW, pan)
        cr = crash_rets(o.run)
        match = sum(np.sign(a - b) == s for a, b, s in zip(cr, ew_rets, ref_signs))  # noqa: B905
        worst = max(abs(a - b) for a, b in zip(cr, ref_rets))  # noqa: B905
        t1 = corr >= CORR_MIN
        t2 = abs(d["sharpe"] - dr["sharpe"]) <= SHARPE_TOL
        t3 = abs(d["mdd"] - dr["mdd"]) <= DD_TOL
        t4 = match >= 3 and worst <= CRASH_PTS
        keeps[red.name] = t1 and t2 and t3 and t4
        yn = lambda b: "yes" if b else "**no**"  # noqa: E731
        out.append(
            f"| {red.name} | {o.orders_yr:.1f} | {o.entries_yr:.1f} | {o.exits_yr:.1f} | "
            f"{o.drift_yr:.1f} | {flips_yr(fws[red.name], EUW):.1f} | {d['sharpe']:.3f} | "
            f"{d['mdd']:.1%} | {corr:.2f} ({agree:.0%}; {ecorr:.2f}) {yn(t1)} | "
            f"{d['sharpe'] - dr['sharpe']:+.3f} {yn(t2)} | {(d['mdd'] - dr['mdd']) * 100:+.1f} pts "
            f"{yn(t3)} | {match}/4, {worst * 100:.1f} pts {yn(t4)} | {yn(keeps[red.name])} |"
        )
    out += [
        "",
        f"Family bar: 8 selectable variants (eu-3's V0-V5, C1, C2); a no-fee Sharpe difference "
        f"counts as real only at p < {0.10 / N_FAMILY:.4f}.",
        "",
        c.table(
            [r_slip.run, v0_slip.run, *[slip[r.name].run for r in REDS], ew_slip.run],
            versus=r_slip.run,
        ),  # fmt: skip
        "",
        "Crash windows (total return inside each, no fixed fee):",
        "",
        eu1.crash_table([r_slip.run, *[slip[r.name].run for r in REDS], ew_slip.run]),
        "",
    ]

    # ---- robustness books ----
    out += ["## 2. Robustness: the same reducers on `eu6` (EUR, coins) and `usw` (USD)", ""]
    out += [
        "Tests 1 and 2 against `R` on the same book (a reducer must pass both on at least one "
        "of the two books, else it is 'fragile').",
        "",
        "| Book | Rule | Signal flips/yr | Orders/yr | Sharpe | dSharpe vs R | Max DD | dMax DD "
        "| Position corr (agree) | Tests 1+2 |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    robust: dict[str, int] = {r.name: 0 for r in REDS}
    books = [
        ("eu6", EU6, eu2.COSTS, lambda: eu2.simulate("tsmom12@eu6/slip-b1", eu1.TSMOM, EU6,
         eu2.COSTS, 0.01, eu2.FeeState(0, 0), "robustness").run),
        ("usw", USW, eu1.COSTS["gym"], lambda: eu1.go("tsmom12@usw", eu1.TSMOM, USW, "gym",
         "robustness", W_START)),
    ]  # fmt: skip
    rob_tables = []
    for book, syms, costs, ref_fn in books:
        _, pan_b = eu1.panel_for(syms)
        ref_run = ref_fn()
        fw_rb = eu3.friday_weights(eu3.R, pan_b)
        drb = c.describe(ref_run)
        out.append(
            f"| {book} | R `tsmom12` | {flips_yr(fw_rb, syms):.1f} | - | {drb['sharpe']:.3f} | - | "
            f"{drb['mdd']:.1%} | - | - | (reference) |"
        )
        runs_b = [ref_run]
        for red in REDS:
            fw_b = friday_weights(red, pan_b)
            o = simulate(f"{red.name}@{book}/slip", make_decisions(fw_b, pan_b), syms, costs,
                         eu2.FeeState(0, 0), "robustness")  # fmt: skip
            d = c.describe(o.run)
            corr, agree, _ = positions(fw_b, fw_rb, syms, pan_b)
            ok = corr >= CORR_MIN and abs(d["sharpe"] - drb["sharpe"]) <= SHARPE_TOL
            robust[red.name] += int(ok)
            out.append(
                f"| {book} | {red.name} | {flips_yr(fw_b, syms):.1f} | {o.orders_yr:.1f} | "
                f"{d['sharpe']:.3f} | {d['sharpe'] - drb['sharpe']:+.3f} | {d['mdd']:.1%} | "
                f"{(d['mdd'] - drb['mdd']) * 100:+.1f} pts | {corr:.2f} ({agree:.0%}) | "
                f"{'yes' if ok else '**no**'} |"
            )
            runs_b.append(o.run)
        rob_tables += [f"`{book}`:", "", c.table(runs_b, versus=ref_run), ""]
    out += ["", *rob_tables]
    same = {r.name: keeps[r.name] and robust[r.name] >= 1 for r in REDS}
    out += [
        "Keeps the character (euw tests 1-4 and robust on >= 1 other book): "
        + ", ".join(f"{r.name} **{'yes' if same[r.name] else 'no'}**" for r in REDS)
        + ".",
        "",
    ]

    # ---- fees on euw ----
    s_ref = sh(r_slip.run)
    gap0 = s_ref - sh(ew_slip.run)
    rules: list[tuple[str, list[gym.Decision], bool, str]] = [
        ("R", eu3.make_decisions(eu3.R, pan), True, "tsmom12"),
        ("V0", v0_decs, True, "V0-w-fri"),
        *[(r.name, decs[r.name], same[r.name], r.name) for r in REDS],
    ]
    slip_sh = {"R": s_ref, "V0": sh(v0_slip.run), **{r.name: sh(slip[r.name].run) for r in REDS}}
    vols = {"R": dr["vol"], "V0": c.describe(v0_slip.run)["vol"],
            **{r.name: c.describe(slip[r.name].run)["vol"] for r in REDS}}  # fmt: skip
    out += ["## 3. Fixed fees by book size on `euw`", ""]
    out += [
        f"R's Sharpe at no fee {s_ref:.3f}; R's gap to equal weight at no fee {gap0:+.2f}. Loss "
        "= max(own Sharpe at no fee, R's) minus Sharpe under the tier (eu-3's strict reading). "
        "Predicted = fixed fees per year / the rule's vol at no fee. Worth it = keeps the "
        "character, loss <= 0.10, gap to equal weight (same tier and book) within 0.15 of R's.",
        "",
        "| Rule | Tier | Book | Sharpe | Loss | Predicted | Gap (EW Sharpe) | Max DD | Orders/yr "
        "| Fixed fees/yr | Worth it |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    worth: dict[tuple[str, str, int], bool] = {}
    be_rows = []
    for label, rdecs, ok_char, base in rules:
        for tname, ttag, sch in TIERS:
            losses = []
            for size in SIZES:
                st = eu2.FeeState(sch.per_order / size, sch.per_year / size)
                if label in ("R", "V0"):
                    o = eu3.simulate(f"{base}@euw/{sch.name}-{size // 1000}k", rdecs, EUW, st,
                                     "robustness" if label == "R" else "variant")  # fmt: skip
                    fees_yr = o.fees_yr
                else:
                    o2 = simulate(f"{base}@euw/{ttag}-{size // 1000}k", rdecs, EUW, eu2.COSTS,
                                  st, "variant")  # fmt: skip
                    o, fees_yr = o2, o2.fees_yr  # type: ignore[assignment]
                e = eu3.simulate(f"equal-weight@euw/{sch.name}-{size // 1000}k", ew_decs, EUW,
                                 eu2.FeeState(sch.per_order / size, sch.per_year / size),
                                 "baseline")  # fmt: skip
                loss = max(slip_sh[label], s_ref) - sh(o.run)
                losses.append(loss)
                g = sh(o.run) - sh(e.run)
                w = ok_char and loss <= LOSS_MAX and abs(g - gap0) <= GAP_TOL
                worth[(label, tname, size)] = w
                out.append(
                    f"| {label} | {tname} | {size // 1000}k | {sh(o.run):.3f} | {loss:.3f} | "
                    f"{fees_yr / vols[label]:.3f} | {g:+.2f} ({sh(e.run):.2f}) | "
                    f"{c.describe(o.run)['mdd']:.1%} | {o.orders_yr:.1f} | {fees_yr:.2%} | "
                    f"{'yes' if w else '**no**'} |"
                )
            # mechanical minimum book: orders x fee + yearly fee = 0.10 x vol x book
            o_slip = {"R": r_slip, "V0": v0_slip, **slip}[label]
            mech = (o_slip.orders_yr * sch.per_order + sch.per_year) / (LOSS_MAX * vols[label])
            be_rows.append(
                f"| {label} | {tname} | {break_even(losses)} | ~{mech / 1000:.1f}k | "
                + " | ".join(f"{x:.3f}" for x in losses)
                + f" | {'yes' if ok_char else 'no'} |"
            )
    out += ["", "## 4. Minimum book (fee loss <= 0.10)", ""]
    out += [
        "Interpolated linearly in 1/size between the tested books (eu-2's method); mechanical "
        "= (orders a year x fee per order + yearly fee) / (0.10 x the rule's vol at no fee).",
        "",
        "| Rule | Tier | Minimum book (tested) | Mechanical | Loss 5k | 10k | 25k | Keeps "
        "character |",
        "|---|---|---|---|---:|---:|---:|---|",
        *be_rows,
        "",
    ]
    out += ["## 5. Verdict grid: is `euw` worth running?", ""]
    out += ["| Tier | " + " | ".join(f"EUR {s // 1000}k" for s in SIZES) + " |"]
    out += ["|---|" + "---|" * len(SIZES)]
    rescued = []
    for tname, _, _ in TIERS:
        cells = []
        for size in SIZES:
            ok = [lab for lab, *_ in rules if worth[(lab, tname, size)]]
            cells.append(f"yes ({', '.join(ok)})" if ok else "**no**")
            base_ok = worth[("R", tname, size)] or worth[("V0", tname, size)]
            red_ok = any(worth[(r.name, tname, size)] for r in REDS)
            if size < 25_000 and not base_ok and red_ok:
                rescued.append(f"{tname} {size // 1000}k")
        out.append(f"| {tname} | " + " | ".join(cells) + " |")
    out += [
        "",
        f"Rescued at EUR 5-10k where neither R nor V0 is worth it: "
        f"**{'yes (' + ', '.join(rescued) + ')' if rescued else 'no'}**.",
    ]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    {"check": check, "run": report_all}[sys.argv[1]]()
