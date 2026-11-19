"""eu-5: two drift-only order cutters on `euw`, character test, fees by book (cards/eu-5.md).

    uv run --with numpy python research/lib/eu5.py check   # plumbing: no number printed
    uv run --with numpy python research/lib/eu5.py run     # 24 rows and the result

Needs the CSVs from `eu1_data.py build` and the saved runs of eu-1/eu-2/eu-3 under the
git-ignored research/data/runs/ (re-scored without new rows). Every new run is a row in
tries.md (idea `eu-5`); a run whose equity file already exists under research/data/runs/eu-5/
is re-scored without a new row. Train period only. Fee tiers are generic (EUR 1/2/3 per order,
eu-2's schedules unchanged).

Both rules keep `R`'s held set on every Friday (the signal is untouched). D1 `flipreb` sends
`R`'s target only on event days (the held set changes), so drift is traded only then. D2
`band25r` sends `R`'s target every day with a gym band of min(5%, 25% of the 1/n target).
"""

from __future__ import annotations

import csv
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date

import common as c
import eu1
import eu2
import eu3
import eu4_run as e4
import harness
import numpy as np
from harness import TRAIN_END, Run

from grimstrade import gym, report

IDEA = "eu-5"
W_START = eu1.W_START
EUW, EU6, USW = eu1.EUW, eu1.EU6, eu1.USW
SIZES = eu3.SIZES
TIERS = e4.TIERS
LOSS_MAX, GAP_TOL, SHARPE_TOL, DD_TOL = 0.10, 0.15, 0.05, 0.02
CORR_MIN, CRASH_PTS = 0.80, 0.03
N_FAMILY = 10
RULES = ["D1-flipreb", "D2-band25r"]


def band_525(n: int) -> float:
    """The 5/25 rule: off by 5 points or 25% of target, whichever is smaller."""
    return min(0.05, 0.25 / n)


def r_decisions(pan: harness.Panel) -> list[gym.Decision]:
    return e4.make_decisions(eu3.friday_weights(eu3.R, pan), pan)


def event_days(decs: list[gym.Decision], every: bool = False) -> list[gym.Decision]:
    """D1: keep a daily decision only when its target differs from the day before."""
    out = [decs[0]]
    for prev, d in zip(decs, decs[1:]):  # noqa: B905
        if every or d.weights != prev.weights:
            out.append(d)
    return out


def rule_setup(rule: str, pan: harness.Panel, n: int) -> tuple[list[gym.Decision], float]:
    decs = r_decisions(pan)
    if rule == "D1-flipreb":
        return event_days(decs), eu3.BAND
    return decs, band_525(n)


def weights_by_day(
    res: gym.Result, hist: Mapping[str, Sequence], syms: Sequence[str]
) -> tuple[list[date], np.ndarray, float]:
    """Realised end-of-day weights (days x syms) from fills and closes; also the worst relative
    gap between the replayed equity and the gym's (plumbing)."""
    closes = {s: {b.date: b.close for b in hist[s]} for s in syms}
    fills = sorted(res.fills, key=lambda f: f.time)
    pos = {s: 0.0 for s in syms}
    last = {s: 0.0 for s in syms}
    cash, k, worst = gym.START_CASH, 0, 0.0
    days, rows = [], []
    for d, eq in res.equity:
        while k < len(fills) and fills[k].time.date() <= d:
            f = fills[k]
            pos[f.symbol] += f.qty
            cash -= f.qty * f.price + f.fee
            k += 1
        for s in syms:
            last[s] = closes[s].get(d, last[s])
        vals = [pos[s] * last[s] for s in syms]
        mine = cash + sum(vals)
        worst = max(worst, abs(mine / eq - 1))
        days.append(d)
        rows.append([v / eq for v in vals])
    return days, np.array(rows), worst


@dataclass
class Out:
    run: Run
    res: gym.Result
    orders_yr: float
    entries_yr: float
    exits_yr: float
    drift_yr: float
    fees_yr: float


def simulate(
    variant: str | None, decs: list[gym.Decision], syms: Sequence[str],
    costs: Mapping[str, gym.Costs], band: float, st: eu2.FeeState, kind: str,
) -> Out:  # fmt: skip
    """variant None: run without logging or saving (plumbing / reference weights)."""
    hist, _ = eu1.panel_for(syms)
    with eu2.fixed_fees(st):
        res = gym.simulate(decs, hist, costs=costs, band=band)
    sc = report.score(f"{IDEA}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    expo = float(np.mean([sum(d.weights.values()) for d in decs]))
    run = Run(IDEA, variant or "-", "train", sc, days, equity, expo, decs)
    if variant is not None:
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
    return Out(run, res, st.orders / years, en / years, ex / years, ot / years, st.paid / years)


BOOKS: dict[str, tuple[list[str], Mapping[str, gym.Costs]]] = {
    "euw": (EUW, eu2.COSTS),
    "eu6": (EU6, eu2.COSTS),
    "usw": (USW, eu1.COSTS["gym"]),
}


def check() -> None:
    """D1 with every day an event is R; D2's path with band 1% is R; weight replay = equity."""
    for book, (syms, costs) in BOOKS.items():
        _, pan = eu1.panel_for(syms)
        decs = r_decisions(pan)
        ref = harness.decisions(eu1.TSMOM, pan, W_START, TRAIN_END)
        if [(d.time, d.weights) for d in decs] != [(d.time, d.weights) for d in ref]:
            raise AssertionError(f"R decisions differ on {book}")
        if event_days(decs, every=True) != decs:
            raise AssertionError(f"D1 with every day an event differs from R on {book}")
        a = simulate(None, decs, syms, costs, eu3.BAND, eu2.FeeState(0, 0), "")
        d2_decs, _ = rule_setup("D2-band25r", pan, len(syms))
        b = simulate(None, d2_decs, syms, costs, eu3.BAND, eu2.FeeState(0, 0), "")
        if not np.array_equal(a.run.equity, b.run.equity):
            raise AssertionError(f"D2 path with band 1% differs from R on {book}")
        hist, _ = eu1.panel_for(syms)
        _, _, worst = weights_by_day(a.res, hist, syms)
        if worst > 1e-9:
            raise AssertionError(f"weight replay misses the gym's equity on {book}")
    # R's run here must equal eu-3's saved house run on euw
    _, pan = eu1.panel_for(EUW)
    mine = simulate(None, r_decisions(pan), EUW, eu2.COSTS, eu3.BAND, eu2.FeeState(0, 0), "")
    saved = harness.DATA / "runs" / "eu-3" / "tsmom12@euw" / "slip.train.csv"
    if saved.exists():
        with saved.open() as f:
            eq = np.array([float(r["equity"]) for r in csv.DictReader(f)])
        if not np.allclose(eq, mine.run.equity, rtol=1e-12):
            raise AssertionError("R differs from eu-3's saved run")
    print("check ok", flush=True)


def weight_corr(a: Out, b: Out, syms: Sequence[str]) -> tuple[float, float]:
    """(pooled correlation of realised slot weights, mean |gap| per slot-day), over W."""
    hist, _ = eu1.panel_for(syms)
    da, wa, _ = weights_by_day(a.res, hist, syms)
    db, wb, _ = weights_by_day(b.res, hist, syms)
    ia = {d: i for i, d in enumerate(da)}
    idx = [(ia[d], j) for j, d in enumerate(db) if d in ia and d >= W_START]
    x = np.array([wa[i] for i, _ in idx]).ravel()
    y = np.array([wb[j] for _, j in idx]).ravel()
    return float(np.corrcoef(x, y)[0, 1]), float(np.mean(np.abs(x - y)))


def sh(run: Run) -> float:
    return c.describe(run)["sharpe"]


def yn(b: bool) -> str:
    return "yes" if b else "**no**"


def report_all() -> None:
    check()
    out = ["# eu-5 results: drift-only order cutters on `euw` (cards/eu-5.md)", ""]
    out += [
        "Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices; "
        "`euw` and `eu6` in EUR, `usw` in USD. Sharpe on calendar days, zero risk-free rate. "
        "`euw`/`eu6`: ETF slippage 0.05% a side (eu-2's costs; coins at the gym's); `usw`: the "
        "gym's costs. `R` = the house rule `tsmom12` (weights sent daily, 1% band). Both rules "
        "keep R's held set on every Friday. D1 `flipreb` = R's target sent only on days the held "
        "set changes (drift traded only then, 1% band); D2 `band25r` = R's daily target with a "
        "band of min(5%, 25% of the 1/n target) of the book (3.57% on `euw`/`usw`, 4.17% on "
        "`eu6`). Fee tiers: EUR 1, 2, 3 per ETF order on a constant book (eu-2's schedules; the "
        "EUR 1 and EUR 3 tiers also carry a EUR 2.50 yearly fee). `R`, V0 and equal weight on "
        "`euw` are eu-3's saved runs, re-scored.",
        "",
    ]
    _, pan = eu1.panel_for(EUW)
    zero = eu2.FeeState
    r_slip = eu3.simulate("tsmom12@euw/slip", eu3.make_decisions(eu3.R, pan), EUW, zero(0, 0),
                          "robustness")  # fmt: skip
    r_w = simulate(None, r_decisions(pan), EUW, eu2.COSTS, eu3.BAND, zero(0, 0), "")
    ew_decs = harness.decisions(eu1.EW, pan, W_START, TRAIN_END)
    ew_slip = eu3.simulate("equal-weight@euw/slip", ew_decs, EUW, zero(0, 0), "baseline")
    v0 = eu3.VARIANTS[0]
    v0_decs = eu3.make_decisions(v0, pan)
    v0_slip = eu3.simulate("V0-w-fri@euw/slip", v0_decs, EUW, zero(0, 0), "variant")
    setups = {r: rule_setup(r, pan, len(EUW)) for r in RULES}
    slip = {
        r: simulate(
            f"{r}@euw/slip", setups[r][0], EUW, eu2.COSTS, setups[r][1], zero(0, 0), "variant"
        )  # fmt: skip
        for r in RULES
    }
    ref_rets = e4.crash_rets(r_slip.run)
    ew_rets = e4.crash_rets(ew_slip.run)
    ref_signs = [np.sign(a - b) for a, b in zip(ref_rets, ew_rets)]  # noqa: B905
    dr = c.describe(r_slip.run)
    n_event = sum(1 for _ in setups["D1-flipreb"][0]) / ((TRAIN_END - W_START).days / 365)

    out += ["## 1. Character on `euw` at no fixed fee", ""]
    out += [
        "| Rule | Orders/yr | Entries | Exits | Drift | Sharpe | Max DD | 1. Realised-weight corr "
        "(mean gap; held-state corr) | 2. dSharpe | 3. dMax DD | 4. Crash signs match / worst "
        "window gap | Keeps character (euw) |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|---|---|---|",
        f"| R `tsmom12` | {r_slip.orders_yr:.1f} | {r_slip.entries_yr:.1f} | "
        f"{r_slip.exits_yr:.1f} | {r_slip.topups_yr:.1f} | {dr['sharpe']:.3f} | {dr['mdd']:.1%} "
        "| - | - | - | - | (reference) |",
        f"| V0 (eu-3) | {v0_slip.orders_yr:.1f} | {v0_slip.entries_yr:.1f} | "
        f"{v0_slip.exits_yr:.1f} | {v0_slip.topups_yr:.1f} | {sh(v0_slip.run):.3f} | "
        f"{c.describe(v0_slip.run)['mdd']:.1%} | - | {sh(v0_slip.run) - dr['sharpe']:+.3f} | - "
        "| - | yes (eu-3) |",
    ]
    keeps: dict[str, bool] = {}
    for r in RULES:
        o = slip[r]
        d = c.describe(o.run)
        corr, gap = weight_corr(o, r_w, EUW)
        cr = e4.crash_rets(o.run)
        match = sum(np.sign(a - b) == s for a, b, s in zip(cr, ew_rets, ref_signs))  # noqa: B905
        worst = max(abs(a - b) for a, b in zip(cr, ref_rets))  # noqa: B905
        t1 = corr >= CORR_MIN
        t2 = abs(d["sharpe"] - dr["sharpe"]) <= SHARPE_TOL
        t3 = abs(d["mdd"] - dr["mdd"]) <= DD_TOL
        t4 = match >= 3 and worst <= CRASH_PTS
        keeps[r] = t1 and t2 and t3 and t4
        out.append(
            f"| {r} | {o.orders_yr:.1f} | {o.entries_yr:.1f} | {o.exits_yr:.1f} | "
            f"{o.drift_yr:.1f} | {d['sharpe']:.3f} | {d['mdd']:.1%} | {corr:.2f} "
            f"({gap:.2%}; 1.00) {yn(t1)} | {d['sharpe'] - dr['sharpe']:+.3f} {yn(t2)} | "
            f"{(d['mdd'] - dr['mdd']) * 100:+.1f} pts {yn(t3)} | {match}/4, {worst * 100:.1f} "
            f"pts {yn(t4)} | {yn(keeps[r])} |"
        )
    out += [
        "",
        f"D1 event days (decisions sent): {n_event:.1f} a year. Entries/exits differ slightly "
        "from R's only through count rules (a fill is an entry when the slot was empty).",
        "",
        f"Family bar: {N_FAMILY} selectable variants (eu-3's V0-V5, eu-4's C1, C2, D1, D2); a "
        f"no-fee Sharpe difference counts as real only at p < {0.10 / N_FAMILY:.3f}.",
        "",
        c.table(
            [r_slip.run, v0_slip.run, *[slip[r].run for r in RULES], ew_slip.run], versus=r_slip.run
        ),  # fmt: skip
        "",
        "Crash windows (total return inside each, no fixed fee):",
        "",
        eu1.crash_table([r_slip.run, *[slip[r].run for r in RULES], ew_slip.run]),
        "",
    ]

    # ---- robustness books ----
    out += ["## 2. Robustness: the same rules on `eu6` (EUR, coins) and `usw` (USD)", ""]
    out += [
        "Tests 1 and 2 against `R` on the same book (a rule must pass both on at least one of "
        "the two books, else it is 'fragile'). Max DD and orders shown, not judged.",
        "",
        "| Book | Rule | Orders/yr (drift) | Sharpe | dSharpe vs R | Max DD | dMax DD | "
        "Realised-weight corr (mean gap) | Tests 1+2 |",
        "|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    robust = {r: 0 for r in RULES}
    rob_tables = []
    for book in ("eu6", "usw"):
        syms, costs = BOOKS[book]
        _, pan_b = eu1.panel_for(syms)
        rb = simulate(None, r_decisions(pan_b), syms, costs, eu3.BAND, zero(0, 0), "")
        drb = c.describe(rb.run)
        out.append(
            f"| {book} | R `tsmom12` | {rb.orders_yr:.1f} ({rb.drift_yr:.1f}) | "
            f"{drb['sharpe']:.3f} | - | {drb['mdd']:.1%} | - | - | (reference) |"
        )
        rb.run.variant = f"tsmom12@{book} (R)"
        runs_b = [rb.run]
        for r in RULES:
            decs_b, band_b = rule_setup(r, pan_b, len(syms))
            o = simulate(f"{r}@{book}/slip", decs_b, syms, costs, band_b, zero(0, 0),
                         "robustness")  # fmt: skip
            d = c.describe(o.run)
            corr, gap = weight_corr(o, rb, syms)
            ok = corr >= CORR_MIN and abs(d["sharpe"] - drb["sharpe"]) <= SHARPE_TOL
            robust[r] += int(ok)
            out.append(
                f"| {book} | {r} | {o.orders_yr:.1f} ({o.drift_yr:.1f}) | {d['sharpe']:.3f} | "
                f"{d['sharpe'] - drb['sharpe']:+.3f} | {d['mdd']:.1%} | "
                f"{(d['mdd'] - drb['mdd']) * 100:+.1f} pts | {corr:.2f} ({gap:.2%}) | {yn(ok)} |"
            )
            runs_b.append(o.run)
        rob_tables += [f"`{book}`:", "", c.table(runs_b, versus=rb.run), ""]
    out += ["", *rob_tables]
    same = {r: keeps[r] and robust[r] >= 1 for r in RULES}
    out += [
        "Keeps the character (euw tests 1-4 and robust on >= 1 other book): "
        + ", ".join(f"{r} **{'yes' if same[r] else 'no'}**" for r in RULES)
        + ".",
        "",
    ]
    passing = [r for r in RULES if same[r]]
    if passing:
        pick = min(passing, key=lambda r: slip[r].orders_yr)
        out += [
            f"Pick (fewest orders at no fee among those keeping the character): **{pick}**.",
            "",
        ]

    # ---- fees on euw ----
    s_ref = sh(r_slip.run)
    gap0 = s_ref - sh(ew_slip.run)
    vols = {"R": dr["vol"], "V0": c.describe(v0_slip.run)["vol"],
            **{r: c.describe(slip[r].run)["vol"] for r in RULES}}  # fmt: skip
    slip_sh = {"R": s_ref, "V0": sh(v0_slip.run), **{r: sh(slip[r].run) for r in RULES}}
    orders0 = {"R": r_slip.orders_yr, "V0": v0_slip.orders_yr,
               **{r: slip[r].orders_yr for r in RULES}}  # fmt: skip
    labels = [("R", True), ("V0", True), *[(r, same[r]) for r in RULES]]
    out += ["## 3. Fixed fees by book size on `euw`", ""]
    out += [
        f"R's Sharpe at no fee {s_ref:.3f}; R's gap to equal weight at no fee {gap0:+.2f}. Loss "
        "= max(own Sharpe at no fee, R's) minus Sharpe under the tier. Predicted = fixed fees "
        "per year / the rule's vol at no fee. Worth it = keeps the character, loss <= 0.10, gap "
        "to equal weight (same tier and book) within 0.15 of R's.",
        "",
        "| Rule | Tier | Book | Sharpe | Loss | Predicted | Gap (EW Sharpe) | Max DD | Orders/yr "
        "| Fixed fees/yr | Worth it |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    worth: dict[tuple[str, str, int], bool] = {}
    be_rows = []
    for label, ok_char in labels:
        for tname, ttag, sch in TIERS:
            losses = []
            for size in SIZES:
                st = eu2.FeeState(sch.per_order / size, sch.per_year / size)
                if label == "R":
                    r_decs = eu3.make_decisions(eu3.R, pan)
                    o3 = eu3.simulate(
                        f"tsmom12@euw/{sch.name}-{size // 1000}k", r_decs, EUW, st, "robustness"
                    )
                    run_o, ord_o, fees_o = o3.run, o3.orders_yr, o3.fees_yr
                elif label == "V0":
                    o3 = eu3.simulate(f"V0-w-fri@euw/{sch.name}-{size // 1000}k", v0_decs, EUW,
                                      st, "variant")  # fmt: skip
                    run_o, ord_o, fees_o = o3.run, o3.orders_yr, o3.fees_yr
                else:
                    o5 = simulate(f"{label}@euw/{ttag}-{size // 1000}k", setups[label][0], EUW,
                                  eu2.COSTS, setups[label][1], st, "variant")  # fmt: skip
                    run_o, ord_o, fees_o = o5.run, o5.orders_yr, o5.fees_yr
                e = eu3.simulate(f"equal-weight@euw/{sch.name}-{size // 1000}k", ew_decs, EUW,
                                 eu2.FeeState(sch.per_order / size, sch.per_year / size),
                                 "baseline")  # fmt: skip
                loss = max(slip_sh[label], s_ref) - sh(run_o)
                losses.append(loss)
                g = sh(run_o) - sh(e.run)
                w = ok_char and loss <= LOSS_MAX and abs(g - gap0) <= GAP_TOL
                worth[(label, tname, size)] = w
                out.append(
                    f"| {label} | {tname} | {size // 1000}k | {sh(run_o):.3f} | {loss:.3f} | "
                    f"{fees_o / vols[label]:.3f} | {g:+.2f} ({sh(e.run):.2f}) | "
                    f"{c.describe(run_o)['mdd']:.1%} | {ord_o:.1f} | {fees_o:.2%} | {yn(w)} |"
                )
            mech = (orders0[label] * sch.per_order + sch.per_year) / (LOSS_MAX * vols[label])
            be_rows.append(
                f"| {label} | {tname} | {eu3.break_even(losses)} | ~{mech / 1000:.1f}k | "
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
            ok = [lab for lab, _ in labels if worth[(lab, tname, size)]]
            cells.append(f"yes ({', '.join(ok)})" if ok else "**no**")
            base_ok = worth[("R", tname, size)] or worth[("V0", tname, size)]
            if size < 25_000 and not base_ok and any(worth[(r, tname, size)] for r in RULES):
                rescued.append(f"{tname} {size // 1000}k")
        out.append(f"| {tname} | " + " | ".join(cells) + " |")
    out += [
        "",
        "Rescued at EUR 5-10k where neither R nor V0 is worth it: "
        f"**{'yes (' + ', '.join(rescued) + ')' if rescued else 'no'}**.",
    ]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    {"check": check, "run": report_all}[sys.argv[1]]()
