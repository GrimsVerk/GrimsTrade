"""The standard test every card goes through: six assets, twins, out-of-universe, pass bar."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import date

import common as c
import stats

SINGLES = ["GSPC", "N225", "FTSE", "GDAXI"]


def _twin_runs(twins: Mapping[str, c.ResearchStrategy], u: c.Ctx, start: date | None, fresh: bool):
    """Twins are already logged by baselines.py; `fresh` twins (a changed warm-up) are logged."""
    kind = "baseline"
    return [c.go("baselines", n, f, u, kind, log=fresh, start=start) for n, f in twins.items()]


def standard(
    idea: str,
    title: str,
    variants: Mapping[str, c.ResearchStrategy],
    twins: Mapping[str, c.ResearchStrategy],
    *,
    per_asset: bool,
    sets: Sequence[str] = ("etf", "coin", "idx"),
    fresh_twins: bool = False,
    start: date | None = None,
    note: str = "",
) -> dict[str, object]:
    """`variants`: first one is the primary. `twins`: first one is THE twin for the pass bar."""
    primary = next(iter(variants))
    twin = next(iter(twins))
    out = [
        f"# {title}",
        "",
        f"Card: `cards/{idea}.md`. Protocol: `protocol.md`. {note}".strip(),
        "",
    ]

    six = c.ctx("six")
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False,
              start=start)  # fmt: skip
    tw = _twin_runs(twins, six, start, fresh_twins)
    vs = [c.go(idea, n, f, six, "variant", start=start) for n, f in variants.items()]
    runs = vs + tw + ([] if "equal-weight" in twins else [ew])
    out += ["## The six live assets, train period", "", c.table(runs, versus=tw[0]), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    out += ["Annualised log growth: " + ", ".join(f"{r.variant} {c.growth(r):+.1%}" for r in runs)]
    out += [""]
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
        names = SINGLES if (name == "idx" and per_asset) else [name]
        diffs = []
        for nm in names:
            u = c.ctx(nm)
            tu = _twin_runs(twins, u, None, fresh_twins or nm in ("N225", "FTSE", "GDAXI"))
            eu = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), u, "baseline",
                      log=False)  # fmt: skip
            pu = c.go(idea, primary, variants[primary], u, "robustness")
            ru = [pu] + tu + ([] if "equal-weight" in twins else [eu])
            out += [f"## Out of universe: {nm}, from {u.start}", "", c.table(ru, versus=tu[0]), ""]
            x, y = c.align(pu, tu[0])
            diffs.append(stats.sharpe(x) - stats.sharpe(y))
        signs[name] = sum(diffs) / len(diffs)

    same = sum(1 for v in signs.values() if v * diff > 0) if diff != 0 else 0
    need_sets = min(2, len(signs))
    bars = [
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
    out += [f"## Pass bar (primary variant `{primary}`)", ""]
    out += [f"- {'PASS' if ok else 'FAIL'}: {text} ({detail})" for text, ok, detail in bars]
    verdict = "PASSES train" if all(ok for _, ok, _ in bars) else "FAILS train"
    out += ["", f"**{verdict}.**", ""]
    c.write_result(idea, "\n".join(out))
    return {"variants": vs, "twins": tw, "ew": ew, "text": "\n".join(out), "passed": verdict}
