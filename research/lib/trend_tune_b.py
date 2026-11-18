"""Part B of research run trend-tune: three walk-forward tuning procedures against fixed
`tsmom12` (card: research/trend-tune.md).

    uv run python research/lib/trend_tune_b.py

Each procedure is one `variant` row in research/tries.md (idea `trend-tune`), its out-of-universe
runs are `robustness` rows. Runs are logged the first time only; a rerun re-scores them from the
same configuration, so the tables can be rebuilt. Hand-written text above the marker line in the
result file is kept. The held-out year is not touched by this script.
"""

from __future__ import annotations

import math
from datetime import date

import common as c
import harness
import numpy as np
import stats
import trend_tune as tt
from trend_tune_anatomy import ORDER, Y2003, go_once, hold, since, tsmom12

from grimstrade import gym

IDEA = "trend-tune"
MARK = "<!-- tables below this line are written by lib/trend_tune_b.py -->"
PROCS = {"wf-asset": "asset", "wf-pooled": "pooled", "wf-shrunk": "shrunk"}
SINGLES = ["GSPC", "N225", "FTSE", "GDAXI"]
P_BAR = 0.10 / len(PROCS)


def twin_on(u: c.Ctx) -> c.Run:
    return c.go("baselines", "tsmom12", tsmom12(), u, "baseline", log=False)


def active_share(run: c.Run, twin: c.Run) -> float:
    """Average distance of the weights from the twin's: half the sum of absolute differences."""
    out = []
    for a, b in zip(run.decisions, twin.decisions, strict=True):
        keys = set(a.weights) | set(b.weights)
        out.append(0.5 * sum(abs(a.weights.get(k, 0.0) - b.weights.get(k, 0.0)) for k in keys))
    return float(np.mean(out))


def diff_stats(run: c.Run, twin: c.Run, start: date | None = None) -> tuple[float, float, float]:
    """Sharpe difference to the twin, one-sided bootstrap p, and its standard error."""
    a, b = c.align(run, twin)
    if start is not None:
        a, b = since(run, start), since(twin, start)
    d, p, lo, hi = stats.sharpe_diff_boot(a, b)
    return d, p, (hi - lo) / 3.29


def oou(name: str, mode: str) -> tuple[dict[str, float], list[str]]:
    """Sharpe difference to `tsmom12` on each out-of-universe set, the procedure refitted on the
    set's own history. Per-asset procedures: each index alone, averaged. Pooled: one index book."""
    text: list[str] = []
    signs: dict[str, float] = {}
    for set_name in ("etf", "coin", "idx"):
        names = SINGLES if (set_name == "idx" and mode != "pooled") else [set_name]
        diffs = []
        for nm in names:
            u = c.ctx(nm)
            tw = twin_on(u)
            ew = c.go("baselines", "equal-weight", hold(), u, "baseline", log=False)
            tuner = tt.Tuner(mode)
            run = go_once(IDEA, name, tuner.strategy(), u, "robustness")
            text += [f"#### `{name}` on {nm}, from {u.start}", "", c.table([run, tw, ew], tw), ""]
            last = tuner.choices(u.panel, tt.refit_of(u.end))
            text += ["Lookbacks in force at the end: "
                     + ", ".join(f"{s} {m}" for s, m in last.items()) + ".", ""]  # fmt: skip
            x, y = c.align(run, tw)
            diffs.append(stats.sharpe(x) - stats.sharpe(y))
        signs[set_name] = float(np.mean(diffs))
    return signs, text


def choice_table(tuner: tt.Tuner, six: c.Ctx) -> list[str]:
    out = ["| Refit (first Friday of) |" + "".join(f" {s} |" for s in ORDER),
           "|---|" + "---:|" * len(ORDER)]  # fmt: skip
    prev = None
    for year in range(six.start.year, six.end.year + 1):
        refit = tt.first_friday(year)
        ch = tuner.choices(six.panel, refit)
        # an asset that joins the book during the year trades on this refit's choice
        last = min(tt.first_friday(year + 1), six.end)
        view = six.panel.view(harness.decide_time(last))
        row = tuple("-" if not c.eligible(view, s) else str(ch[s]) for s in ORDER)
        if row != prev:
            out.append(f"| {year} |" + "".join(f" {x} |" for x in row))
        prev = row
    return out


def main() -> None:
    six = c.ctx("six")
    gspc = c.ctx("GSPC")
    warm = {"SPY": tt.warm_from(gspc.panel, "GSPC", date(1993, 1, 28))}
    twin = twin_on(six)
    ew = c.go("baselines", "equal-weight", hold(), six, "baseline", log=False)
    tuners = {name: tt.Tuner(mode, warm) for name, mode in PROCS.items()}
    runs = {name: go_once(IDEA, name, t.strategy(), six, "variant") for name, t in tuners.items()}
    every = [*runs.values(), twin, ew]

    out = [MARK, ""]
    out += [
        "Train period only (decisions to 2025-11-09), total-return prices, the gym's fills and "
        "costs. Each procedure picks lookbacks from 3, 6, 9, 12, 15, 18, 24 months on the first "
        "Friday of every year, from bars visible at that moment only, then trades like "
        "`tsmom12`. Twin: fixed `tsmom12`.",
        "",
        "## The six live assets, 1994-2025",
        "",
        c.table(every, versus=twin),
        "",
        "Total return inside each stress window:",
        "",
        c.stress_table(every),
        "",
        "## The same runs from 2003 (the review's window)",
        "",
        "| Variant | Sharpe | Against `tsmom12` (p) | Growth/yr | Worst loss |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in every:
        x = since(r, Y2003)
        if r is twin:
            versus = "-"
        else:
            d, p, _ = diff_stats(r, twin, Y2003)
            versus = f"{d:+.2f} ({p:.2f})"
        out.append(f"| {r.variant} | {stats.sharpe(x):.2f} | {versus} | {stats.cagr(x):+.1%} | "
                   f"{stats.max_drawdown(x):.1%} |")  # fmt: skip
    out += [""]

    out += ["## What each procedure chose", ""]
    out += ["A row is shown when the choice changed; `-` means the asset was not in the book "
            "yet; 12 is `tsmom12`'s own setting.", ""]  # fmt: skip
    for name, t in tuners.items():
        share = active_share(runs[name], twin)
        out += [f"### `{name}`", "", *choice_table(t, six), ""]
        out += [f"Average distance from `tsmom12`'s weights (active share): {share:.1%} of the "
                f"book. Trades a year: {runs[name].score.turnover:.1f} against "
                f"{twin.score.turnover:.1f}.", ""]  # fmt: skip

    out += ["## Out of universe", ""]
    verdicts = {}
    oou_text: list[str] = []
    bar_text: list[str] = []
    ev = c.era_sharpes(twin)
    dt = c.describe(twin)
    de = c.describe(ew)
    for name, mode in PROCS.items():
        run = runs[name]
        signs, text = oou(name, mode)
        oou_text += text
        d, p, se = diff_stats(run, twin)
        d03 = stats.sharpe(since(run, Y2003)) - stats.sharpe(since(twin, Y2003))
        es = c.era_sharpes(run)
        both = [n for n in es if not (math.isnan(es[n]) or math.isnan(ev[n]))]
        ahead = sum(es[n] > ev[n] for n in both)
        dp = c.describe(run)
        same = sum(1 for v in signs.values() if v * d > 0)
        luck3 = stats.expected_max_sharpe(3, se**2)
        luck21 = stats.expected_max_sharpe(21, se**2)
        bars = [
            (f"1. Sharpe beats `tsmom12` with p < {P_BAR:.3f}", d > 0 and p < P_BAR,
             f"difference {d:+.2f}, p = {p:.2f}"),
            ("2. Ahead of `tsmom12` in at least 4 of 5 eras", ahead >= 4,
             f"{ahead} of {len(both)}"),
            ("3. Max drawdown not more than 5 points worse", dp["mdd"] <= dt["mdd"] + 0.05,
             f"{dp['mdd']:.1%} vs {dt['mdd']:.1%}"),
            ("4. Same sign out of universe in at least 2 of 3 sets", d > 0 and same >= 2,
             ", ".join(f"{k} {v:+.2f}" for k, v in signs.items())),
            ("5. Beats equal weight on Sharpe", dp["sharpe"] > de["sharpe"],
             f"{dp['sharpe']:.2f} vs {de['sharpe']:.2f}"),
            ("6. Not behind `tsmom12` since 2003", d03 >= 0, f"difference {d03:+.2f}"),
            ("7. Deflation: the difference beats the best of 3 unskilled tries", d > luck3,
             f"{d:+.2f} against {luck3:+.2f} for 3 tries and {luck21:+.2f} for 21; standard "
             f"error of the difference {se:.2f}"),
        ]  # fmt: skip
        ok = all(b for _, b, _ in bars)
        weak = ok and d <= luck21
        verdicts[name] = (ok, d)
        bar_text += [f"### `{name}`", ""]
        bar_text += [f"- {'PASS' if b else 'FAIL'}: {t} ({detail})" for t, b, detail in bars]
        label = "PASSES train" + (" (weak: clears 3 tries, not 21)" if weak else "")
        bar_text += ["", f"**{label if ok else 'FAILS train'}.**", ""]
    out += oou_text
    out += ["## Pass bar (each procedure judged alone)", "", *bar_text]

    best = max(verdicts, key=lambda n: verdicts[n][1])
    out += [f"## Robustness of the procedure with the largest train difference (`{best}`)", ""]
    raw = c.ctx("six", adjusted=False)
    raw_twin = c.go("robustness", "tsmom12-raw", tsmom12(), raw, "robustness", log=False)
    raw_run = go_once(IDEA, f"{best}-raw", tt.Tuner(PROCS[best], warm).strategy(), raw,
                      "robustness")  # fmt: skip
    out += ["Raw prices (no dividends, what the live scoreboard shows):", "",
            c.table([raw_run, raw_twin], versus=raw_twin), ""]  # fmt: skip
    double = {k: gym.Costs(fee=2 * v.fee, slip=2 * v.slip) for k, v in gym.COSTS.items()}
    done = (harness.DATA / "runs" / IDEA / f"{best}-2xcost.train.csv").exists()
    cost_run = harness.run(IDEA, f"{best}-2xcost", tt.Tuner(PROCS[best], warm).strategy(),
                           kind="robustness", panel=six.panel, history=six.hist, start=six.start,
                           end=six.end, costs=double, log=not (done or c.DRY))  # fmt: skip
    cost_twin = harness.run("robustness", "tsmom12-2xcost", tsmom12(), kind="robustness",
                            panel=six.panel, history=six.hist, start=six.start, end=six.end,
                            costs=double, log=False)  # fmt: skip
    out += ["Double costs (120 bps a round trip in coins, 8 bps in ETFs):", "",
            c.table([cost_run, cost_twin], versus=cost_twin), ""]  # fmt: skip

    passed = [n for n, (ok, _) in verdicts.items() if ok]
    out += ["## Held-out year", ""]
    out += [
        "Not looked at: no procedure passed train."
        if not passed
        else f"Train passed by: {', '.join(passed)}. The card allows one held-out look, for "
        f"`{max(passed, key=lambda n: verdicts[n][1])}`; it is run separately and logged.",
        "",
    ]
    path = harness.RESEARCH / "results" / ("trend-tune.md" if not c.DRY else "trend-tune.dry.md")
    head = (
        "# trend-tune, Part B: walk-forward tuning of the lookback against fixed `tsmom12`\n\n"
        "Card: `trend-tune.md`.\n"
    )
    if path.exists() and MARK in path.read_text():
        head = path.read_text().split(MARK)[0].rstrip() + "\n"
    path.write_text(head + "\n" + "\n".join(out).rstrip() + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
