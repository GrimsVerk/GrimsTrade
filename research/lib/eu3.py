"""eu-3: decision frequency and slot structure for a small coin-free EUR book (cards/eu-3.md).

    uv run --with numpy python research/lib/eu3.py check   # plumbing: no number printed
    uv run --with numpy python research/lib/eu3.py run     # all 81 rows and the result

Needs the CSVs from `eu1_data.py build`. Every run is a row in tries.md (idea `eu-3`); a run whose
equity file already exists under the git-ignored research/data/runs/eu-3/ is re-scored without a
new row. Train period only. Fixed fees reuse eu-2's in-process wrapper (`eu2.fixed_fees`); the
gym is not changed.

The rule's signal is `tsmom12`'s (365-day return > 0). What changes is when it is checked, when a
slot may switch, when trades are placed, and how many slots there are. A variant is a state
machine over Fridays: each Friday it may (or may not) look at the signal and update the set of
held slots; its weights then go to the gym either every day (the house: drift is topped up any
day) or only on its trade days.
"""

from __future__ import annotations

import csv
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import eu1
import eu2
import harness
import numpy as np
from harness import TRAIN_END, Run

from grimstrade import gym, report
from grimstrade.data import ETF, UNIVERSE

IDEA = "eu-3"
W_START = eu1.W_START  # 2012-01-02, a Monday
F0 = W_START - timedelta(days=(W_START.weekday() - 4) % 7)  # 2011-12-30, the Friday before
EUW = eu1.EUW
C4 = {"IWDA": 3 / 7, "IBGM": 2 / 7, "4GLD": 1 / 7, "EXXY": 1 / 7}  # class slots (card)
for _s in C4:
    UNIVERSE.setdefault(_s, ETF)

SIZES = [5_000, 10_000, 25_000]
SCHEDULES = eu2.SCHEDULES  # slip, dg1, tr2, dg3
COSTS = eu2.COSTS  # ETFs 0 fee + 0.05% slippage
BAND = 0.01
LOSS_MAX = 0.10
GAP_TOL = 0.15
SHARPE_TOL = 0.05
DD_TOL = 0.02


@dataclass(frozen=True)
class Spec:
    name: str
    monthly: bool = False  # signal checked on last Fridays only
    entries_monthly: bool = False  # a cash slot may be entered on last Fridays only
    hold_days: int = 0  # a slot may not be exited before this many days after its entry
    daily: bool = False  # weights repeated every day (house); else trades on check days only
    classes: bool = False  # 4 class slots (C4) instead of 7 equal slots

    @property
    def syms(self) -> list[str]:
        return list(C4) if self.classes else EUW


R = Spec("tsmom12", daily=True)
VARIANTS = [
    Spec("V0-w-fri"),
    Spec("V1-m", monthly=True),
    Spec("V2-m-in", entries_monthly=True),
    Spec("V3-hold4w", hold_days=28),
    Spec("V4-c4", classes=True),
    Spec("V5-c4-m", monthly=True, classes=True),
]


def last_friday(d: date) -> bool:
    return (d + timedelta(days=7)).month != d.month


def friday_weights(spec: Spec, pan: harness.Panel) -> list[tuple[date, dict[str, float]]]:
    """The state machine: (Friday, target weights) from F0 to the last Friday of train."""
    held: set[str] = set()
    entry: dict[str, date] = {}
    out = []
    f = F0
    while f <= TRAIN_END:
        view = pan.view(harness.decide_time(f))
        live = c.live(view)
        if not spec.monthly or last_friday(f):
            for s in live:
                sig = c.tsmom_signal(view, s)
                if s in held:
                    if not sig and (f - entry[s]).days >= spec.hold_days:
                        held.discard(s)
                elif sig and (not spec.entries_monthly or last_friday(f)):
                    held.add(s)
                    entry[s] = f
        if spec.classes:
            w = {s: C4[s] for s in live if s in held}
        else:
            w = {s: 1 / len(live) for s in live if s in held}
        out.append((f, w))
        f += timedelta(days=7)
    return out


def make_decisions(spec: Spec, pan: harness.Panel) -> list[gym.Decision]:
    fw = friday_weights(spec, pan)
    if spec.daily:
        # As `common.weekly`: day d repeats the Friday on or before the view's last grid day
        # (on a holiday Friday that is the Friday before, until the next trading day).
        by_day = dict(fw)
        out, d = [], W_START
        while d <= TRAIN_END:
            today = pan.view(harness.decide_time(d)).today
            f = max(today - timedelta(days=(today.weekday() - 4) % 7), F0)
            out.append(gym.Decision(harness.decide_time(d), harness.clean(by_day[f])))
            d += timedelta(days=1)
        return out
    out = [gym.Decision(harness.decide_time(W_START), harness.clean(fw[0][1]))]
    for f, w in fw[1:]:
        if not spec.monthly or last_friday(f):
            out.append(gym.Decision(harness.decide_time(f), harness.clean(w)))
    return out


def ew_c4_decisions(pan: harness.Panel) -> list[gym.Decision]:
    strat = c.weekly(lambda view: {s: C4[s] for s in c.live(view)})
    return harness.decisions(strat, pan, W_START, TRAIN_END)


@dataclass
class Out:
    run: Run
    orders_yr: float
    entries_yr: float
    exits_yr: float
    topups_yr: float
    fees_yr: float  # fixed fees per year, share of the book


def count_fills(fills: Sequence[gym.Fill]) -> tuple[int, int, int]:
    pos: dict[str, float] = {}
    entries = exits = other = 0
    for f in fills:
        if UNIVERSE[f.symbol] != ETF:
            continue
        before = pos.get(f.symbol, 0.0)
        after = before + f.qty
        pos[f.symbol] = after
        if before <= 1e-12:
            entries += 1
        elif after <= 1e-12:
            exits += 1
        else:
            other += 1
    return entries, exits, other


def simulate(
    variant: str, decs: list[gym.Decision], syms: Sequence[str], st: eu2.FeeState, kind: str
) -> Out:
    hist, _ = eu1.panel_for(syms)
    with eu2.fixed_fees(st):
        res = gym.simulate(decs, hist, costs=COSTS, band=BAND)
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
    en, ex, ot = count_fills(res.fills)
    return Out(run, st.orders / years, en / years, ex / years, ot / years, st.paid / years)


def check() -> None:
    """The state machine with daily trades must reproduce the house rule exactly."""
    _, pan = eu1.panel_for(EUW)
    mine = make_decisions(R, pan)
    ref = harness.decisions(eu1.TSMOM, pan, W_START, TRAIN_END)
    if [(d.time, d.weights) for d in mine] != [(d.time, d.weights) for d in ref]:
        raise AssertionError("state machine differs from eu1.TSMOM")
    eu2.plain_check(EUW)
    print("check ok", flush=True)


def tag(sch: eu2.Schedule, size: int) -> str:
    return "slip" if sch.name == "slip" else f"{sch.name}-{size // 1000}k"


Key = tuple[str, str, int]  # (rule, schedule, size); slip has size 0


def all_runs() -> dict[Key, Out]:
    out: dict[Key, Out] = {}
    rules: list[tuple[str, Spec | None, str]] = [
        ("tsmom12", R, "robustness"),
        ("equal-weight", None, "baseline"),
        *[(v.name, v, "variant") for v in VARIANTS],
    ]
    for name, spec, kind in rules:
        syms = spec.syms if spec else EUW
        _, pan = eu1.panel_for(syms)
        decs = make_decisions(spec, pan) if spec else harness.decisions(eu1.EW, pan, W_START,
                                                                        TRAIN_END)  # fmt: skip
        for sch in SCHEDULES:
            for size in [0] if sch.name == "slip" else SIZES:
                st = eu2.FeeState(sch.per_order / size, sch.per_year / size) if size else (
                    eu2.FeeState(0, 0))  # fmt: skip
                out[(name, sch.name, size)] = simulate(
                    f"{name}@euw/{tag(sch, size)}", decs, syms, st, kind
                )
    _, pan4 = eu1.panel_for(list(C4))
    out[("ew-c4", "slip", 0)] = simulate(
        "ew-c4@euw/slip", ew_c4_decisions(pan4), list(C4), eu2.FeeState(0, 0), "baseline"
    )
    return out


def sh(o: Out) -> float:
    return c.describe(o.run)["sharpe"]


def crash_signs(run: Run, ew: Run) -> list[float]:
    inside = [(a, b) for _, a, b in eu1.CRASHES if a >= W_START]
    return [float(np.sign(eu1.crash_ret(run, a, b) - eu1.crash_ret(ew, a, b))) for a, b in inside]


def character(o: Out, ref: Out, ew: Out) -> tuple[bool, str]:
    d, dr = c.describe(o.run), c.describe(ref.run)
    dsh, ddd = d["sharpe"] - dr["sharpe"], d["mdd"] - dr["mdd"]
    match = sum(a == b for a, b in zip(crash_signs(o.run, ew.run), crash_signs(ref.run, ew.run)))  # noqa: B905
    ok = abs(dsh) <= SHARPE_TOL and abs(ddd) <= DD_TOL and match >= 3
    yn = lambda b: "yes" if b else "**no**"  # noqa: E731
    txt = (
        f"{dsh:+.2f} ({yn(abs(dsh) <= SHARPE_TOL)}) | {ddd * 100:+.1f} pts "
        f"({yn(abs(ddd) <= DD_TOL)}) | {match}/4 ({yn(match >= 3)}) | {yn(ok)}"
    )
    return ok, txt


def break_even(losses: list[float]) -> str:
    if losses[0] <= LOSS_MAX:
        return "<= 5k"
    for (b0, l0), (b1, l1) in zip(zip(SIZES, losses), zip(SIZES[1:], losses[1:])):  # noqa: B905
        if l1 <= LOSS_MAX < l0:
            x0, x1 = 1 / b0, 1 / b1
            x = x0 + (LOSS_MAX - l0) * (x1 - x0) / (l1 - l0)
            return f"~{1 / x / 1000:.0f}k"
    return "> 25k"


def report_all() -> None:
    check()
    r = all_runs()
    names = ["tsmom12", *[v.name for v in VARIANTS]]
    ref, ew = r[("tsmom12", "slip", 0)], r[("equal-weight", "slip", 0)]
    s_ref = sh(ref)
    gap0 = s_ref - sh(ew)
    out = ["# eu-3 results: decision frequency and slot structure on `euw`", ""]
    out += [
        "Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices, "
        "EUR. Sharpe on calendar days, zero risk-free rate. ETF slippage 0.05% a side; 1% band. "
        "Fixed fees on a constant book (fee / book of equity per ETF order), as in eu-2: `dg1` "
        "DEGIRO core EUR 1/order + EUR 2.50/yr, `tr2` Trade Republic EUR 2/order, `dg3` DEGIRO "
        "other ETFs EUR 3/order + EUR 2.50/yr. `tsmom12` = the house rule (R); V0-V5 as on the "
        "card (`cards/eu-3.md`). Orders = ETF fills per year at `slip`.",
        "",
        "## 1. At no fixed fee (`slip`): orders and character",
        "",
        "| Rule | Sharpe | CAGR | Vol | Max DD | Exposure | Orders/yr | Entries | Exits | "
        "Top-ups/trims | dSharpe vs R | dMax DD vs R | Crash signs vs EW match R | "
        "Same character |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    same: dict[str, bool] = {"tsmom12": True}
    for n in [*names, "equal-weight", "ew-c4"]:
        o = r[(n, "slip", 0)]
        d = c.describe(o.run)
        row = (
            f"| {n} | {d['sharpe']:.2f} | {d['cagr']:+.1%} | {d['vol']:.1%} | {d['mdd']:.1%} | "
            f"{d['exposure']:.0%} | {o.orders_yr:.1f} | {o.entries_yr:.1f} | {o.exits_yr:.1f} | "
            f"{o.topups_yr:.1f} |"
        )
        if n in names[1:]:
            ok, txt = character(o, ref, ew)
            same[n] = ok
            row += f" {txt} |"
        else:
            row += " - | - | - | - |" if n != "tsmom12" else " - | - | - | (reference) |"
        out.append(row)
    out += ["", c.table([r[(n, "slip", 0)].run for n in [*names, "equal-weight", "ew-c4"]]), ""]
    out += ["Crash windows (total return inside each, `slip`):", ""]
    out += [eu1.crash_table([r[(n, "slip", 0)].run for n in [*names, "equal-weight"]]), ""]

    out += [
        "## 2. Fixed fees by book size",
        "",
        "Fee loss = min(own Sharpe at `slip`, R's at `slip` "
        f"{s_ref:.2f}) minus Sharpe under the schedule (card). Predicted = fixed fees per year / "
        "the rule's vol at `slip` (the mechanical part). Gap = Sharpe minus house equal weight's "
        f"under the same schedule and size; R's gap at `slip` is {gap0:+.2f}. Worth it = same "
        "character, fee loss <= 0.10 and gap within 0.15 of R's.",
        "",
        "| Rule | Schedule | Book | Sharpe | Fee loss | Predicted | Gap (EW Sharpe) | Max DD | "
        "Orders/yr | Fixed fees/yr | Worth it |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    worth: dict[Key, bool] = {}
    be_lines = []
    for n in names:
        base = min(sh(r[(n, "slip", 0)]), s_ref)
        vol = c.describe(r[(n, "slip", 0)].run)["vol"]
        for sch in SCHEDULES[1:]:
            losses = []
            for size in SIZES:
                o, e = r[(n, sch.name, size)], r[("equal-weight", sch.name, size)]
                loss = base - sh(o)
                losses.append(loss)
                g = sh(o) - sh(e)
                ok = same[n] and loss <= LOSS_MAX and abs(g - gap0) <= GAP_TOL
                worth[(n, sch.name, size)] = ok
                d = c.describe(o.run)
                out.append(
                    f"| {n} | {sch.name} | {size // 1000}k | {sh(o):.2f} | {loss:.2f} | "
                    f"{o.fees_yr / vol:.2f} | {g:+.2f} ({sh(e):.2f}) | {d['mdd']:.1%} | "
                    f"{o.orders_yr:.1f} | {o.fees_yr:.2%} | {'yes' if ok else '**no**'} |"
                )
            be_lines.append(
                f"| {n} | {sch.name} | {break_even(losses)} | "
                + " | ".join(f"{x:.2f}" for x in losses)
                + f" | {'yes' if same[n] else 'no'} |"
            )
    out += ["", "## 3. Break-even book (fee loss <= 0.10)", ""]
    out += ["| Rule | Schedule | Break-even | Loss 5k | Loss 10k | Loss 25k | Same character |"]
    out += ["|---|---|---|---:|---:|---:|---|", *be_lines, ""]

    out += ["## 4. Verdict grid: is `euw` worth running?", ""]
    out += ["| Schedule | " + " | ".join(f"EUR {s // 1000}k" for s in SIZES) + " |"]
    out += ["|---|" + "---|" * len(SIZES)]
    for sch in SCHEDULES[1:]:
        cells = []
        for size in SIZES:
            if worth[("tsmom12", sch.name, size)]:
                cells.append("yes (R)")
                continue
            ok = [n for n in names[1:] if worth[(n, sch.name, size)]]
            cells.append(f"yes ({', '.join(ok)}; R no)" if ok else "**no**")
        out.append(f"| {sch.name} | " + " | ".join(cells) + " |")
    out.append("")
    rescued = [
        (sch.name, size)
        for sch in SCHEDULES[1:]
        for size in SIZES[:2]
        if not worth[("tsmom12", sch.name, size)]
        and any(worth[(n, sch.name, size)] for n in names[1:])
    ]
    out.append(
        "Lane test (a same-character variant makes `euw` worth running at EUR 5-10k on a "
        f"schedule where R is not): **{'yes' if rescued else 'no'}**"
        + (f" ({', '.join(f'{a} {b // 1000}k' for a, b in rescued)})" if rescued else "")
        + "."
    )
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    {"check": check, "run": report_all}[sys.argv[1]]()
