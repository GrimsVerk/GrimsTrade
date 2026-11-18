"""Research run trend-where: the walk-forward yes/no per asset against always-on `tsmom12` and
equal weight (card: research/trend-where.md).

    uv run python research/lib/trend_where_run.py

Each variant is one `variant` row in research/tries.md (idea `trend-where`), its out-of-universe
runs are `robustness` rows. Runs are logged the first time only; a rerun re-scores them. The
held-out year is not touched by this script.
"""

from __future__ import annotations

import common as c
import harness
import stats
import trend_tune as tt
import trend_where as tw
from trend_tune_anatomy import ORDER, Y2003, go_once, hold, since, tsmom12

IDEA = "trend-where"
VARIANTS = {"where-vol": "vol", "where-dd": "dd"}
P_BAR = 0.10 / len(VARIANTS)
SLACK = 0.05  # worst loss may be this much deeper than `tsmom12`'s


def answer_table(where: tw.Where, u: c.Ctx, order: list[str]) -> list[str]:
    out = ["| Refit (first Friday of) |" + "".join(f" {s} |" for s in order),
           "|---|" + "---|" * len(order)]  # fmt: skip
    prev = None
    for year in range(u.start.year, u.end.year + 1):
        ans = where.answers(u.panel, tt.first_friday(year))
        last = min(tt.first_friday(year + 1), u.end)
        view = u.panel.view(harness.decide_time(last))
        row = tuple("-" if not c.eligible(view, s) else ("yes" if ans[s] else "no") for s in order)
        if row != prev:
            out.append(f"| {year} |" + "".join(f" {x} |" for x in row))
        prev = row
    return out


def evidence_table(where: tw.Where, u: c.Ctx, order: list[str]) -> list[str]:
    unit = "volatility a year" if where.mode == "vol" else "worst chained fall"
    out = [f"| Asset | Years | Out bars | In bars | Out: {unit} | In: {unit} | Keep filter |",
           "|---|---:|---:|---:|---:|---:|---|"]  # fmt: skip
    refit = tt.refit_of(u.end)
    for s in order:
        e = where.evidence(u.panel, s, refit)
        k = c.bpy(s) ** 0.5 if where.mode == "vol" else 1.0
        out.append(f"| {s} | {e.years:.1f} | {e.n_out} | {e.n_in} | {e.out * k:.1%} | "
                   f"{e.inn * k:.1%} | {'yes' if e.keep else 'no'} |")  # fmt: skip
    return out


def main() -> None:
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", tsmom12(), six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", hold(), six, "baseline", log=False)
    wheres = {name: tw.Where(mode) for name, mode in VARIANTS.items()}
    runs = {n: go_once(IDEA, n, w.strategy(), six, "variant") for n, w in wheres.items()}
    every = [*runs.values(), twin, ew]

    out = [
        "# trend-where: keep the trend filter only where its days out were rougher",
        "",
        "Card: `trend-where.md`. Train period only (decisions to 2025-11-09), total-return "
        "prices, the gym's fills and costs. Each January every asset answers yes (keep the "
        "`tsmom12` filter) or no (just hold the slot) from its own past bars. Twin: always-on "
        "`tsmom12`. Benchmark: equal weight (buy and hold).",
        "",
        "## The six live assets, 1994-2025",
        "",
        c.table(every, versus=twin),
        "",
        "Total return inside each stress window:",
        "",
        c.stress_table(every),
        "",
        "## The same runs from 2003",
        "",
        "| Variant | Sharpe | Against `tsmom12` | Growth/yr | Worst loss |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in every:
        x = since(r, Y2003)
        d = stats.sharpe(x) - stats.sharpe(since(twin, Y2003))
        out.append(f"| {r.variant} | {stats.sharpe(x):.2f} | {'-' if r is twin else f'{d:+.2f}'} "
                   f"| {stats.cagr(x):+.1%} | {stats.max_drawdown(x):.1%} |")  # fmt: skip
    note = "A row is shown when an answer changed; `-` means not in the book yet."
    out += ["", "## The answers, year by year", "", note, ""]
    for name, w in wheres.items():
        out += [f"### `{name}`", "", *answer_table(w, six, ORDER), "",
                "What the last refit saw:", "", *evidence_table(w, six, ORDER), ""]  # fmt: skip

    out += ["## Out of universe (each set one book, refitted on its own history)", ""]
    oou: dict[str, dict[str, tuple[float, float, float]]] = {n: {} for n in VARIANTS}
    for set_name in ("etf", "coin", "idx"):
        u = c.ctx(set_name)
        tw_run = c.go("baselines", "tsmom12", tsmom12(), u, "baseline", log=False)
        ew_run = c.go("baselines", "equal-weight", hold(), u, "baseline", log=False)
        got = []
        for name, mode in VARIANTS.items():
            w = tw.Where(mode)
            run = go_once(IDEA, name, w.strategy(), u, "robustness")
            got.append(run)
            x, y = c.align(run, tw_run)
            oou[name][set_name] = (stats.sharpe(x) - stats.sharpe(y), c.describe(run)["mdd"],
                                   c.describe(tw_run)["mdd"])  # fmt: skip
            last = w.answers(u.panel, tt.refit_of(u.end))
            said = ", ".join(f"{s} {'yes' if a else 'no'}" for s, a in last.items())
            out += [f"`{name}` on {set_name}, answers at the last refit: {said}.", ""]
        out += [f"### {set_name}, from {u.start}", "", c.table([*got, tw_run, ew_run], tw_run), ""]

    out += ["## Pass bar (each variant judged alone)", ""]
    dt, de = c.describe(twin), c.describe(ew)
    for name, run in runs.items():
        a, b = c.align(run, twin)
        d, p, _, _ = stats.sharpe_diff_boot(a, b)
        dp = c.describe(run)
        x, y = since(run, Y2003), since(twin, Y2003)
        d03 = stats.sharpe(x) - stats.sharpe(y)
        m03, t03 = stats.max_drawdown(x), stats.max_drawdown(y)
        sets = oou[name]
        up = sum(v[0] > 0 for v in sets.values())
        shallow = sum(v[1] <= v[2] + SLACK for v in sets.values())
        bars = [
            (f"1. Sharpe beats `tsmom12` with p < {P_BAR:.2f}", d > 0 and p < P_BAR,
             f"difference {d:+.2f}, p = {p:.2f}"),
            ("2. Worst loss not more than 5 points worse", dp["mdd"] <= dt["mdd"] + SLACK,
             f"{dp['mdd']:.1%} vs {dt['mdd']:.1%}"),
            ("3. Since 2003: not behind on Sharpe, worst loss not more than 5 points worse",
             d03 >= 0 and m03 <= t03 + SLACK,
             f"difference {d03:+.2f}; {m03:.1%} vs {t03:.1%}"),
            ("4. Out of universe: Sharpe up in 2 of 3 sets, worst loss within 5 points in 2 of 3",
             up >= 2 and shallow >= 2,
             "; ".join(f"{k} {v[0]:+.2f}, {v[1]:.1%} vs {v[2]:.1%}" for k, v in sets.items())),
            ("5. Beats equal weight on Sharpe", dp["sharpe"] > de["sharpe"],
             f"{dp['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ]  # fmt: skip
        ok = all(flag for _, flag, _ in bars)
        out += [f"### `{name}`", ""]
        out += [f"- {'PASS' if flag else 'FAIL'}: {t} ({detail})" for t, flag, detail in bars]
        out += ["", f"**{'PASSES train' if ok else 'FAILS train'}.**", ""]
    out += ["## Held-out year", "", "Not looked at (the card: not in this run, pass or fail).", ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
