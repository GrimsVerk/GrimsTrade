# ruff: noqa: E501
"""Tables for research/results/rl-1.md from research/data/rl/eval-<variant>.json (no backtests).

uv run python research/lib/rl_report.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research" / "data" / "rl"
OUT = ROOT / "research" / "results" / "rl-1.md"
VARIANTS = ["ppo-lin", "ppo-mlp", "ppo-mlp-dd", "ppo-mlp-px", "es-lin"]
ERAS = ["2000-09", "2010-16", "2017-21", "2022-25"]


def f(x: float, spec: str = ".2f") -> str:
    return "-" if x is None or (isinstance(x, float) and math.isnan(x)) else format(x, spec)


def main() -> None:
    ev = {v: json.loads((DATA / f"eval-{v}.json").read_text()) for v in VARIANTS
          if (DATA / f"eval-{v}.json").exists()}  # fmt: skip
    first = next(iter(ev.values()))
    L = [
        "# RL 1: results (train period, out of sample 2000-01-07 to 2025-11-09)",
        "",
        "Script `lib/rl_eval.py` (tables by `lib/rl_report.py`). Walk-forward: a model retrained",
        "every two years on data before it trades. Every row is a replay through `gym.simulate`.",
        "Ensemble = the average of the ten seeds' weights each Friday (the selectable strategy).",
        "dSharpe and p against `tsmom12`: paired stationary bootstrap, one-sided. Baselines are",
        "re-scored from 2000-01-07.",
        "",
        "## Six assets",
        "",
        "| Strategy | Sharpe | Since 2003 | dSharpe vs tsmom12 (p) | Since 2003 d (p) | Worst loss "
        "| Growth/yr | Turnover/yr | Seeds: median Sharpe [min..max] | Seeds ahead | Bars passed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|",
    ]
    for k, b in first["baselines"].items():
        L.append(f"| `{k}` | {f(b['sharpe'])} | {f(b['since2003'])} | | | {f(b['mdd'], '.1%')} "
                 f"| {f(b['cagr'], '+.1%')} | {f(b['turnover'], '.1f')} | | | |")  # fmt: skip
    for v, e in ev.items():
        d, s = e["ensemble"], e["seeds"]["sharpe"]
        vt = e["vs_tsmom12"]
        passed = [k.split()[0] for k, ok in e["bars"].items() if ok]
        L.append(
            f"| `{v}` | {f(d['sharpe'])} | {f(d['since2003'])} | {vt['diff']:+.2f} "
            f"({vt['p']:.2f}) | {vt['since2003_diff']:+.2f} ({vt['since2003_p']:.2f}) | "
            f"{f(d['mdd'], '.1%')} | {f(d['cagr'], '+.1%')} | {f(d['turnover'], '.1f')} | "
            f"{sorted(s)[4] / 2 + sorted(s)[5] / 2:.2f} [{min(s):.2f}..{max(s):.2f}] | "
            f"{e['seeds']['ahead']}/10 | {', '.join(passed) or 'none'} |"
        )
    L += ["", "Eras (Sharpe):", "", "| Strategy | " + " | ".join(ERAS) + " |",
          "|---|" + "---:|" * len(ERAS)]  # fmt: skip
    for k, b in first["baselines"].items():
        L.append(f"| `{k}` | " + " | ".join(f(b.get(x, math.nan)) for x in ERAS) + " |")
    for v, e in ev.items():
        L.append(f"| `{v}` | " + " | ".join(f(e["ensemble"].get(x, math.nan)) for x in ERAS) + " |")
    L += ["", "## Out of universe (fold models unchanged, ensemble)", "",
          "| Strategy | Other ETFs | Other coins | Four indexes |", "|---|---:|---:|---:|"]  # fmt: skip
    L.append("| `tsmom12` | " + " | ".join(
        f"{f(first['oou'][k]['tsmom12'])} (from {first['oou'][k]['from']})"
        for k in ("etf", "coin", "idx")) + " |")  # fmt: skip
    for v, e in ev.items():
        L.append(f"| `{v}` | " + " | ".join(
            f"{f(e['oou'][k]['sharpe'])} ({e['oou'][k]['diff']:+.2f})"
            for k in ("etf", "coin", "idx")) + " |")  # fmt: skip
    L += ["", "## Overfitting: each fold model in sample against the two years it traded", "",
          "Weekly Sharpe, fresh account, batched simulator (same rules as the gym). In = the",
          "fold's own six-asset training window (1994 to the fold); out = its two traded years.",
          "", "| Fold | tsmom12 in / out | " + " | ".join(f"`{v}` in / out" for v in ev) + " |",
          "|---|---:|" + "---:|" * len(ev)]  # fmt: skip
    folds = [r["fold"] for r in first["overfit"]]
    for i, y in enumerate(folds):
        t = first["overfit"][i]
        row = f"| {y} | {t['in_tsmom']:.2f} / {t['out_tsmom']:.2f} |"
        for e in ev.values():
            r = e["overfit"][i]
            row += f" {r['in_ens']:.2f} / {r['out_ens']:.2f} |"
        L.append(row)
    mean = "| mean | "
    mean += (f"{sum(r['in_tsmom'] for r in first['overfit']) / len(folds):.2f} / "
             f"{sum(r['out_tsmom'] for r in first['overfit']) / len(folds):.2f} |")  # fmt: skip
    for e in ev.values():
        o = e["overfit"]
        mean += (f" {sum(r['in_ens'] for r in o) / len(o):.2f} / "
                 f"{sum(r['out_ens'] for r in o) / len(o):.2f} |")  # fmt: skip
    L.append(mean)
    L += ["", "## What the ensembles do (six assets, out of sample)", "",
          "Slot = weight as a multiple of an equal slot (1/number of eligible assets).", "",
          "| Strategy | Avg cash | Avg coins | Slot when 12m trend up | Slot when down | "
          "Corr(risk held, VIX) | Avg weekly change |", "|---|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    rows = [("tsmom12", first["behaviour_tsmom12"])] + [(v, e["behaviour"]) for v, e in ev.items()]
    for v, b in rows:
        L.append(f"| `{v}` | {b['cash']:.0%} | {b['coins']:.0%} | {b['slot_up']:.2f} | "
                 f"{b['slot_down']:.2f} | {b['corr_risk_vix']:+.2f} | {b['weekly_change']:.1%} |")  # fmt: skip
    L += ["", "## Pass bar", ""]
    for v, e in ev.items():
        L.append(f"- `{v}`: " + ("**passes**" if e["passed"] else "fails") + " ("
                 + "; ".join(f"{k}: {'yes' if ok else 'no'}" for k, ok in e["bars"].items())
                 + ")")  # fmt: skip
    OUT.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
