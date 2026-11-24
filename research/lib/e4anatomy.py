"""e4-anatomy-1: where `e4`'s lead over `tsmom12` comes from (regime, leg, mix against rates).
Card: research/cards/e4-anatomy-1.md. Engine: e4anatomy_core.py.

    uv run python -I research/lib/e4anatomy.py            # the one run (writes results)

Descriptive re-score of pooled-1 (#142) and pooled-2 (#159) on their own series and code:
`pooled1.load_all()` (41 equity markets) and `pooled2.load_nonequity()` (29 series), nothing
after 2025-10-31 parsed (their loaders stop there). Cache root from `research/macro.local.json`
(git-ignored) or GRIMSTRADE_DATA; the ETFs from `research/data/adj/` (git-ignored). Writes
research/results/e4-anatomy-1.md and .json. Logs nothing (the `note` row is written by hand).
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e4anatomy_core as ec  # noqa: E402
import pooled1_core as pc  # noqa: E402

RESEARCH = Path(__file__).resolve().parents[1]
OUT = RESEARCH / "results" / "e4-anatomy-1.md"
P2 = RESEARCH / "results" / "pooled-2.json"
BLOCK, DRAWS, SEED = 12, 2000, 0
VOL_K = 1.5
READINGS = ("A", "B", "C", "W", "VA", "VB")
LABELS = {"A": "A", "B": "B", "C": "C", "W": "W", "VA": "A", "VB": "B"}  # V: post hoc
READING_TXT = {
    "A": "A, primary: zigzag 25% / 25%, whipsaw +-13 weeks",
    "B": f"B: zigzag {VOL_K} x the series' annual volatility, whipsaw +-13 weeks",
    "C": "C: insure-3's zigzag 15% / 15%, whipsaw +-13 weeks",
    "W": "W: zigzag 25% / 25%, whipsaw +-26 weeks",
    "VA": "VA (post hoc, not on the card): against a volatility-matched `tsmom12`, labels A",
    "VB": "VB (post hoc, not on the card): against a volatility-matched `tsmom12`, labels B",
}
EQ_GROUPS = ("EQ-US10", "EQ-DEV13", "EQ-WIDE10", "EQ-ETF8")
NE_GROUPS = ("USB3", "GOV9", "FX9", "COM8")
POOLS = ("equity", "judged", "COM8", "combined")


def vol_of(level: np.ndarray, ppy: int) -> float:
    lr = np.diff(np.log(level))
    return float(lr.std() * math.sqrt(ppy))


def readings_for(level: np.ndarray, ppy: int) -> dict[str, tuple[float, int]]:
    return {
        "A": (0.25, 13),
        "B": (min(0.9, VOL_K * vol_of(level, ppy)), 13),
        "C": (0.15, 13),
        "W": (0.25, 26),
    }


def load() -> tuple[list[ec.Series], dict[str, float]]:
    import pooled1 as p1
    import pooled2 as p2

    out: list[ec.Series] = []
    thr: dict[str, float] = {}
    for n, g, days, px in p1.load_all():
        if days[-1] > p1.LAST:
            raise AssertionError(f"{n}: a day after {p1.LAST}")
        d = np.array([x.toordinal() for x in days], dtype=np.int64)
        rd = readings_for(px, 252)
        thr[n] = rd["B"][0]
        out.append(ec.run_weekly(n, "EQ-" + g, d, px, d, pc.COST, rd))
        print(f"  {n}", file=sys.stderr)
    for s in p2.load_nonequity():
        cost = p2.COST[s.cls]
        if s.freq == "w":
            assert s.d is not None and s.px_ret is not None and s.av is not None
            if int(s.d[-1]) > p2.LAST.toordinal():
                raise AssertionError(f"{s.name}: a day after {p2.LAST}")
            rd = readings_for(s.px_ret, 252)
            out.append(ec.run_weekly(s.name, s.group, s.d, s.px_ret, s.av, cost, rd))
        else:
            assert s.months is not None and s.r_ret is not None
            lv = np.concatenate([[1.0], np.cumprod(1.0 + s.r_ret)])
            rd = readings_for(lv, 12)
            out.append(ec.run_monthly(s.name, s.group, s.months, s.r_ret, s.gap, cost, rd))
        thr[s.name] = rd["B"][0]
        print(f"  {s.name}", file=sys.stderr)
    return out, thr


def masks(series: list[ec.Series]) -> dict[str, np.ndarray]:
    g = np.array([s.group for s in series])
    eq = np.array([x.startswith("EQ-") for x in g])
    judged = np.isin(g, ("USB3", "GOV9", "FX9"))
    out = {"equity": eq, "judged": judged, "COM8": g == "COM8", "combined": eq | judged}
    for k in EQ_GROUPS + NE_GROUPS:
        out[k] = g == k
    return out


def check(series: list[ec.Series], parts: list[ec.Parts]) -> float:
    """Largest |d - pooled-2's d| over the 70 series (card: must be <= 1e-9)."""
    ref = json.loads(P2.read_text())
    by = dict(zip(ref["names"], ref["d"]["e4"], strict=True))
    worst = 0.0
    for s, p in zip(series, parts, strict=True):
        worst = max(worst, abs(p.d - by[s.name]))
    return worst


def mean_dict(ds: list[dict[str, float]]) -> dict[str, float]:
    return {k: float(np.nanmean([d[k] for d in ds])) for k in ds[0]}


def summarise(series: list[ec.Series], key: str, mk: dict[str, np.ndarray]) -> dict[str, Any]:
    reading, vm = LABELS[key], key.startswith("V")
    ps = [ec.parts(s, reading, vm) for s in series]
    res: dict[str, Any] = {"pools": {}, "series": []}
    cal = ec.month_cells(series, reading, ps, vm)
    min_n = np.array([52 if s.freq == "w" else 12 for s in series], dtype=float)
    tot = ec.totals(cal)
    draws = ec.boot_draws(cal, min_n, BLOCK, DRAWS, SEED)

    def pool_point(m: np.ndarray) -> dict[str, Any]:
        sel = [p for p, ok in zip(ps, m, strict=True) if ok]
        sel_s = [x for x, ok in zip(series, m, strict=True) if ok]
        reg = mean_dict([ec.merge_slow(p.by_regime) for p in sel])
        share = mean_dict([ec.merge_slow(p.share) for p in sel])
        return {
            "n": len(sel),
            "D": float(np.mean([p.d for p in sel])),
            "ret": float(np.mean([p.ret for p in sel])),
            "risk": float(np.mean([p.risk for p in sel])),
            "regime": reg,
            "regime6": mean_dict([p.by_regime for p in sel]),
            "share": share,
            "leg": mean_dict([p.by_leg for p in sel]),
            "leg_regime": {
                r: mean_dict([ec.merge_slow_legs(p.leg_regime)[r] for p in sel]) for r in ec.MERGED
            },
            "gap": mean_dict([ec.merge_slow_gap(p) for p in sel]),
            "var_share": mean_dict([ec.merge_slow(p.var_share) for p in sel]),
            "d_pos": int(sum(p.d > 0 for p in sel)),
            "sr_ts": float(
                np.mean(
                    [
                        p.mu_ts / p.sd_ts * math.sqrt(ec.PPY[s.freq])
                        for p, s in zip(sel, sel_s, strict=True)
                    ]
                )
            ),
            "vol_ratio": float(np.mean([p.sd_ts / p.sd_e4 for p in sel])),
        }

    def merged_stats(X: dict[str, np.ndarray], m: np.ndarray) -> dict[str, Any]:
        st = ec.pool_stats(X, m, min_n)
        return {"S": ec.merge_slow(st["S"]), "C": ec.merge_slow(st["C"]), "risk": st["risk"]}

    for k, m in mk.items():
        pt = pool_point(m)
        lin = merged_stats(tot, m)
        bs = [merged_stats(dr, m) for dr in draws]
        se = {r: float(np.std([b["C"][r] for b in bs], ddof=1)) for r in ec.MERGED}
        se["risk"] = float(np.std([b["risk"] for b in bs], ddof=1))
        se["D"] = float(np.std([sum(b["C"].values()) + b["risk"] for b in bs], ddof=1))
        pt["se"] = se
        pt["lin_check"] = abs(sum(lin["C"].values()) + lin["risk"] - pt["D"])
        pt["_boot"] = bs
        pt["_lin"] = lin
        res["pools"][k] = pt
    for a, b in (("equity", "judged"), ("equity", "COM8")):
        la, lb = res["pools"][a]["_lin"], res["pools"][b]["_lin"]
        ms = ec.mix_split(la["S"], la["C"], lb["S"], lb["C"], la["risk"], lb["risk"])
        bd = [
            ec.mix_split(x["S"], x["C"], y["S"], y["C"], x["risk"], y["risk"])
            for x, y in zip(res["pools"][a]["_boot"], res["pools"][b]["_boot"], strict=True)
        ]
        ms_se = {key: float(np.std([z[key] for z in bd], ddof=1)) for key in ms}
        res[f"mix_{a}_{b}"] = {"point": ms, "se": ms_se, "reading": ec.mix_reading(ms)}
    for k in res["pools"]:
        del res["pools"][k]["_boot"], res["pools"][k]["_lin"]
    for s, p in zip(series, ps, strict=True):
        res["series"].append(
            {
                "name": s.name,
                "group": s.group,
                "freq": s.freq,
                "d": p.d,
                "ret": p.ret,
                "risk": p.risk,
                "regime": ec.merge_slow(p.by_regime),
                "share": ec.merge_slow(p.share),
                "leg": p.by_leg,
            }
        )
    res["_parts"] = ps
    return res


# --------------------------------------------------------------------------- report


def f3(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:+.3f}"


def carrying(v: float, se: float, D: float) -> str:
    return "**carrying**" if (se > 0 and v > 2 * se and D > 0 and v > D / 2) else ""


def legs_section(R: dict[str, Any], title: str, cols: tuple[str, ...]) -> list[str]:
    L = [
        f"## Legs (reading {title})",
        "",
        "Each leg = (h_L - h_12) / 4 x market return, i.e. what replacing a quarter of `tsmom12`",
        "by the L-month signal adds; cost = `e4`'s costs minus `tsmom12`'s; resid = weekly",
        "compounding (0 on monthly series); scale (post hoc readings only) = (1 - k) x the",
        "`tsmom12` return, k = sd(e4) / sd(tsmom12): what scaling `tsmom12` down to `e4`'s",
        "volatility removes.",
        "",
        "| Pool | " + " | ".join(cols) + " | Sum |",
        "|---|" + "---:|" * (len(cols) + 1),
    ]
    for k in POOLS + EQ_GROUPS + NE_GROUPS:
        p = R["pools"][k]
        lg = p["leg"]
        L.append(f"| {k} | " + " | ".join(f3(lg[x]) for x in cols) + f" | {f3(p['ret'])} |")
    L += ["", f"Leg x regime (reading {title}):", ""]
    for k in ("equity", "judged", "COM8"):
        L += [
            f"**{k}**",
            "",
            "| Regime | " + " | ".join(cols) + " |",
            "|---|" + "---:|" * len(cols),
        ]
        for r in ec.MERGED:
            lr = R["pools"][k]["leg_regime"][r]
            L.append(f"| {r} | " + " | ".join(f3(lr[x]) for x in cols) + " |")
        L.append("")
    return L


def report(all_res: dict[str, dict[str, Any]], worst: float, thr: dict[str, float]) -> str:
    A = all_res["A"]
    L = [
        "# e4-anatomy-1: where `e4`'s lead over `tsmom12` comes from",
        "",
        "Card: `cards/e4-anatomy-1.md`. Code: `lib/e4anatomy.py`, `lib/e4anatomy_core.py` (rules:",
        "`lib/pooled1_core.py`, `lib/pooled2_core.py`; series: `pooled1.load_all()`,",
        "`pooled2.load_nonequity()`). Descriptive re-score: no new rule, nothing selected.",
        "",
        "Units: Sharpe points, `e4` minus `tsmom12`, per series, then the equal-weight mean over",
        "the pool (adds up to the pool's D exactly). D = return part + risk part; the return part",
        "= the sum of the regime columns = the sum of the leg columns. SE: joint circular",
        f"bootstrap of {BLOCK}-month blocks on one monthly calendar ({DRAWS} draws, seed {SEED}),",
        "sigmas held at full-sample values (a linearisation; a description, not a test).",
        "",
        f"**Reproduction check:** largest |d - pooled-2's d| over the 70 series = {worst:.1e}"
        f" ({'passes' if worst <= 1e-9 else 'FAILS'} the card's 1e-9).",
        "",
    ]
    for rd in READINGS:
        R = all_res[rd]
        L += [
            f"## Reading {READING_TXT[rd]}",
            "",
            "| Pool | n | D (SE) | Risk part (SE) | Return part | Fast crash | Slow bear | "
            "Rebound | Whipsaw | Calm |",
            "|---|---:|---|---|---:|---|---|---|---|---|",
        ]
        for k in POOLS:
            p = R["pools"][k]
            se = p["se"]
            cells = [
                f"{f3(p['regime'][r])} ({se[r]:.3f}) {carrying(p['regime'][r], se[r], p['D'])}"
                for r in ec.MERGED
            ]
            L.append(
                f"| {k} | {p['n']} | {f3(p['D'])} ({se['D']:.3f}) | {f3(p['risk'])} "
                f"({se['risk']:.3f}) | {f3(p['ret'])} | " + " | ".join(cells) + " |"
            )
        if rd == "A":
            L += [
                "",
                "Risk part = Sharpe(`tsmom12`) x (sd(`tsmom12`) / sd(`e4`) - 1) per series:",
                "",
            ]
            L += ["| Pool | mean Sharpe `tsmom12` | mean sd ratio |", "|---|---:|---:|"]
            for k in POOLS + EQ_GROUPS + NE_GROUPS:
                p = R["pools"][k]
                L.append(f"| {k} | {p['sr_ts']:.3f} | {p['vol_ratio']:.3f} |")
        L += ["", "Time shares (mean over series):", ""]
        L += ["| Pool | " + " | ".join(ec.MERGED) + " |", "|---|" + "---:|" * len(ec.MERGED)]
        for k in POOLS:
            sh = R["pools"][k]["share"]
            L.append(f"| {k} | " + " | ".join(f"{sh[r]:.2f}" for r in ec.MERGED) + " |")
        L += ["", "Mix against rates (exact; SE from the same draws):", ""]
        L += [
            "| Gap | Gap value | Mix at other's rates | Rates at equity mix | Mix at equity rates"
            " | Rates at other's mix | Risk part | Reading (card) |",
            "|---|---:|---|---|---|---|---|---|",
        ]
        for b in ("judged", "COM8"):
            m = R[f"mix_equity_{b}"]
            pt, se = m["point"], m["se"]
            L.append(
                f"| equity - {b} | {f3(pt['gap'])} | "
                + " | ".join(
                    f"{f3(pt[x])} ({se[x]:.3f})"
                    for x in (
                        "mix_at_b_rates",
                        "rates_at_a_mix",
                        "mix_at_a_rates",
                        "rates_at_b_mix",
                        "risk",
                    )
                )
                + f" | {m['reading'] if b == 'judged' else '(shown)'} |"
            )
        L.append("")
        if rd in ("A", "VA"):
            L += [f"Groups (reading {rd}):", ""]
            L += [
                "| Group | n | D | Risk | Return | " + " | ".join(ec.MERGED) + " |",
                "|---|---:|---:|---:|---:|" + "---:|" * len(ec.MERGED),
            ]
            for g in EQ_GROUPS + NE_GROUPS:
                p = R["pools"][g]
                L.append(
                    f"| {g} | {p['n']} | {f3(p['D'])} | {f3(p['risk'])} | {f3(p['ret'])} | "
                    + " | ".join(f3(p["regime"][r]) for r in ec.MERGED)
                    + " |"
                )
            L += [
                "",
                "Slow bears split (reading A, insure-1's medium 93-365 / long > 365 days):",
                "",
            ]
            L += ["| Pool | medium | long |", "|---|---:|---:|"]
            for k in POOLS:
                r6 = R["pools"][k]["regime6"]
                L.append(f"| {k} | {f3(r6['slow-medium'])} | {f3(r6['slow-long'])} |")
            L.append("")
    L += legs_section(A, "A", ("1m", "3m", "6m", "cost", "resid"))
    L += legs_section(all_res["VA"], "VA, post hoc", ("1m", "3m", "6m", "cost", "resid", "scale"))
    L += [
        "## Exposure and variance by regime (reading A)",
        "",
        "Mean position gap `e4` - `tsmom12` (negative = `e4` holds less), and each regime's share",
        "of var(`e4`) - var(`tsmom12`) (mean over series).",
        "",
        "| Pool | "
        + " | ".join(f"gap {r}" for r in ec.MERGED)
        + " | "
        + " | ".join(f"var {r}" for r in ec.MERGED)
        + " |",
        "|---|" + "---:|" * (2 * len(ec.MERGED)),
    ]
    for k in POOLS:
        p = A["pools"][k]
        L.append(
            f"| {k} | "
            + " | ".join(f3(p["gap"][r]) for r in ec.MERGED)
            + " | "
            + " | ".join(f"{p['var_share'][r]:.2f}" for r in ec.MERGED)
            + " |"
        )
    L += [
        "",
        "## Per series (reading A)",
        "",
        "| Series | Group | B threshold | d | Risk | Return | "
        + " | ".join(ec.MERGED)
        + " | 1m | 3m | 6m | cost |",
        "|---|---|---:|---:|---:|---:|" + "---:|" * (len(ec.MERGED) + 4),
    ]
    for s in A["series"]:
        L.append(
            f"| {s['name']} | {s['group']} | {thr[s['name']]:.2f} | {f3(s['d'])} | "
            f"{f3(s['risk'])} | {f3(s['ret'])} | "
            + " | ".join(f3(s["regime"][r]) for r in ec.MERGED)
            + " | "
            + " | ".join(f3(s["leg"][x]) for x in ("1m", "3m", "6m", "cost"))
            + " |"
        )
    return "\n".join(L) + "\n"


def main() -> None:
    t0 = time.time()
    series, thr = load()
    mk = masks(series)
    all_res = {rd: summarise(series, rd, mk) for rd in READINGS}
    worst = check(series, all_res["A"]["_parts"])
    if worst > 1e-9:
        print(f"REPRODUCTION FAILS: {worst}", file=sys.stderr)
    for r in all_res.values():
        del r["_parts"]
    OUT.write_text(report(all_res, worst, thr))
    payload = {
        "readings": all_res,
        "check_max_abs": worst,
        "thresholds_B": thr,
        "written": datetime.now(UTC).isoformat(timespec="seconds"),
        "runtime_s": round(time.time() - t0, 1),
    }
    OUT.with_suffix(".json").write_text(json.dumps(payload, indent=1) + "\n")
    print(f"wrote {OUT} ({payload['runtime_s']} s)", file=sys.stderr)


if __name__ == "__main__":
    main()
