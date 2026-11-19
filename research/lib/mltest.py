"""The standard card test for fitted models: like `testkit.standard`, with the start of each
universe set by the first-model rule (protocol.md, "Machine-learning tests")."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence

import common as c
import ml
import stats

Extra = Callable[[c.Ctx, dict[str, c.Run]], list[str]]
Bar = tuple[str, bool, str]


def skill_table(u: c.Ctx, tags: Mapping[str, float], payoff: bool = False) -> list[str]:
    """Forecast skill of each tagged model on this universe (`tags`: name -> neutral forecast).
    `payoff`: also the hit rates with every month counted by the size of its move."""
    head = (
        "| Model | Forecasts | Share that went up | AUC | Hit rate | Said up | "
        "AUC of `up_12m` alone | Hit rate of `up_12m` alone |"
    )
    if payoff:
        head += " Size-weighted hit rate | ...of always up | ...of `up_12m` alone |"
    out = [head, "|---|" + "---:|" * (head.count("|") - 2)]
    for tag, neutral in tags.items():
        k = ml.skill(u.panel, tag, neutral)
        if "auc" not in k:
            continue
        row = (
            f"| {tag} | {k['n']:.0f} | {k['up_share']:.1%} | {k['auc']:.3f} | {k['hit']:.1%} | "
            f"{k['said_up']:.1%} | {c._f(k['auc_up12'], '.3f')} | {k['hit_up12']:.1%} |"
        )
        if payoff:
            row += f" {k['gain']:.1%} | {k['gain_always']:.1%} | {k['gain_up12']:.1%} |"
        out.append(row)
    return out


def standard(
    idea: str,
    title: str,
    variants: Mapping[str, c.ResearchStrategy],
    twins: Mapping[str, c.ResearchStrategy],
    *,
    sets: Sequence[str] = ("etf", "coin", "idx"),
    also: Mapping[str, c.ResearchStrategy] | None = None,
    extra: Extra | None = None,
    more_bars: Callable[[dict[str, c.Run]], list[Bar]] | None = None,
    skill_tags: Mapping[str, float] | None = None,
    payoff: bool = False,
    note: str = "",
) -> None:
    """`variants`: first is the primary. `twins`: first is THE twin. `also`: runs shown for
    comparison that are logged elsewhere. Twins and `also` are re-scored, not logged again."""
    primary, twin = next(iter(variants)), next(iter(twins))
    out = [f"# {title}", "", f"Card: `cards/{idea}.md`. Protocol: `protocol.md`. {note}".strip()]
    out += [""]

    six = c.ctx("six")
    start = max(six.start, ml.first_fit_day(six.panel, six.start)) if not c.DRY else six.start
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False,
              start=start)  # fmt: skip
    tw = [c.go("baselines", n, f, six, "baseline", log=False, start=start)
          for n, f in twins.items()]  # fmt: skip
    vs = [c.go(idea, n, f, six, "variant", start=start) for n, f in variants.items()]
    al = [c.go("shown", n, f, six, "baseline", log=False, start=start)
          for n, f in (also or {}).items()]  # fmt: skip
    runs = vs + al + tw + [ew]
    by_name = {r.variant: r for r in runs}
    out += [f"## The six live assets, train period, from {start}", "", c.table(runs, versus=tw[0])]
    out += ["", "Total return inside each stress window:", "", c.stress_table(runs), ""]
    out += ["Annualised log growth: " + ", ".join(f"{r.variant} {c.growth(r):+.1%}" for r in runs)]
    out += [""]
    if skill_tags:
        out += [
            f"## Forecast skill on the six assets (walk-forward forecasts, {ml.HORIZON} days ahead)"
        ]
        out += [""]
        out += skill_table(six, skill_tags, payoff) + [""]
    if extra:
        out += extra(six, by_name)

    p, t = vs[0], tw[0]
    a, b = c.align(p, t)
    diff, pval, _, _ = stats.sharpe_diff_boot(a, b)
    ep, et = c.era_sharpes(p), c.era_sharpes(t)
    both = [n for n in ep if not (math.isnan(ep[n]) or math.isnan(et[n]))]
    ahead = sum(ep[n] > et[n] for n in both)
    need = 4 if len(both) >= 5 else min(3, len(both))
    dp, dt = c.describe(p), c.describe(t)

    signs: dict[str, float] = {}
    for name in sets:
        u = c.ctx(name)
        try:
            s0 = max(u.start, ml.first_fit_day(u.panel, u.start)) if not c.DRY else u.start
        except ValueError:
            out += [f"## Out of universe: {name}", "", "Never reaches 1,000 rows: not run.", ""]
            continue
        tu = [c.go("baselines", n, f, u, "baseline", log=False, start=s0)
              for n, f in twins.items()]  # fmt: skip
        eu = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), u, "baseline", log=False,
                  start=s0)  # fmt: skip
        pu = c.go(idea, primary, variants[primary], u, "robustness", start=s0)
        out += [f"## Out of universe: {name}, from {s0}", "", c.table([pu, *tu, eu], versus=tu[0])]
        out += [""]
        if skill_tags:
            out += skill_table(u, {primary: skill_tags.get(primary, 0.5)}, payoff) + [""]
        x, y = c.align(pu, tu[0])
        signs[name] = stats.sharpe(x) - stats.sharpe(y)

    same = sum(1 for v in signs.values() if v * diff > 0) if diff != 0 else 0
    need_sets = min(2, len(signs))
    bars: list[Bar] = [
        (f"1. Sharpe beats twin `{twin}` with p < 0.10", diff > 0 and pval < 0.10,
         f"difference {diff:+.2f}, p = {pval:.2f}"),
        (f"2. Ahead of the twin in at least {need} of {len(both)} eras", ahead >= need,
         f"{ahead} of {len(both)}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dp["mdd"] <= dt["mdd"] + 0.05, f"{dp['mdd']:.1%} vs {dt['mdd']:.1%}"),
        (f"4. Same sign out of universe in at least {need_sets} of {len(signs)} sets",
         diff > 0 and same >= need_sets,
         ", ".join(f"{k} {v:+.2f}" for k, v in signs.items())),
        ("5. Beats equal weight on Sharpe", dp["sharpe"] > c.describe(ew)["sharpe"],
         f"{dp['sharpe']:.2f} vs {c.describe(ew)['sharpe']:.2f}"),
    ]  # fmt: skip
    if more_bars:
        bars += more_bars(by_name)
    out += [f"## Pass bar (primary variant `{primary}`)", ""]
    out += [f"- {'PASS' if ok else 'FAIL'}: {text} ({detail})" for text, ok, detail in bars]
    verdict = "PASSES train" if all(ok for _, ok, _ in bars) else "FAILS train"
    out += ["", f"**{verdict}.**", ""]
    c.write_result(idea, "\n".join(out))


def settings_section(u: c.Ctx, specs: Sequence[ml.Spec]) -> list[str]:
    """Which setting purged CV chose at each yearly fit."""
    out = []
    for spec in specs:
        used = ml.settings_used(u.panel, spec)
        if not used:
            continue
        counts: dict[str, int] = {}
        for _, _, text in used:
            counts[text] = counts.get(text, 0) + 1
        tally = "; ".join(f"{k}: {v} fits" for k, v in sorted(counts.items(), key=lambda t: -t[1]))
        out += [f"- `{spec.name}`: {len(used)} yearly fits, {used[0][1]} rows at the first, "
                f"{used[-1][1]} at the last. Chosen: {tally}."]  # fmt: skip
    return out
