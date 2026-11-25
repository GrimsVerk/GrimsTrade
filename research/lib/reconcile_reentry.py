"""reentry-reconcile-1: why `e4` gains in the year after the low when the fast re-entry rules
did not. Card: research/cards/reentry-reconcile-1.md. Engine: reconcile_reentry_core.py.

    uv run python -I research/lib/reconcile_reentry.py      # the one run (writes results)

Descriptive re-score of pooled-1's (#142) logged rules `e4`, `or3-12`, `arm3-12` on its 41
equity series (`pooled1.load_all()`, nothing after 2025-10-31 parsed), with e4-anatomy-1's
(#168) regimes, plus ten diagnostic sleeves (mechanism checks, not candidates). Cache root from
`research/macro.local.json` (git-ignored) or GRIMSTRADE_DATA; the ETFs from
`research/data/adj/` (git-ignored). Writes research/results/reentry-reconcile-1.md and .json.
Logs nothing (the two `note` rows are written by hand).
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
import e4anatomy as ea  # noqa: E402
import e4anatomy_core as ec  # noqa: E402
import pooled1_core as pc  # noqa: E402
import reconcile_reentry_core as rc  # noqa: E402

RESEARCH = Path(__file__).resolve().parents[1]
OUT = RESEARCH / "results" / "reentry-reconcile-1.md"
P1 = RESEARCH / "results" / "pooled-1.json"
GROUPS = ("EQ-US10", "EQ-DEV13", "EQ-WIDE10", "EQ-ETF8")
POOLS = ("equity", *GROUPS)
SPLITS = {"A": ("A", False), "B": ("B", False), "VA": ("A", True)}
TH = 0.02  # the card's Sharpe threshold
KTH = 0.10  # the card's kept-share threshold


def rules_for(wstar: dict[str, float]) -> list[str]:
    out = ["e4", "or3-12", "arm3-12", "e4-re", "e4-trim"]
    for r in ("or3-12", "arm3-12"):
        out += [f"{r} x {w}" for w in rc.WS] + [f"{r} x w*"]
    del wstar
    return out


def positions(m: rc.Market, wstar: dict[str, float]) -> dict[str, np.ndarray]:
    h12 = m.h["tsmom12"]
    out = {r: m.h[r] for r in rc.LOGGED}
    out.update(rc.e4_parts(m.h["e4"], h12))
    for r in ("or3-12", "arm3-12"):
        for w in rc.WS:
            out[f"{r} x {w}"] = rc.sleeve(m.h[r], h12, w)
        out[f"{r} x w*"] = rc.sleeve(m.h[r], h12, wstar[r])
    return out


def mean_dict(ds: list[dict[str, float]]) -> dict[str, float]:
    return {k: float(np.nanmean([d[k] for d in ds])) for k in ds[0]}


def load() -> list[rc.Market]:
    import pooled1 as p1

    out = []
    for n, g, days, px in p1.load_all():
        if days[-1] > p1.LAST:
            raise AssertionError(f"{n}: a day after {p1.LAST}")
        d = np.array([x.toordinal() for x in days], dtype=np.int64)
        rd = ea.readings_for(px, 252)
        out.append(rc.market(n, "EQ-" + g, d, px, {"A": rd["A"], "B": rd["B"]}))
        print(f"  {n}", file=sys.stderr)
    return out


def check(markets: list[rc.Market], dd: dict[str, list[float]]) -> float:
    ref = json.loads(P1.read_text())
    by = {x["name"]: x["stats"] for x in ref["markets"]}
    worst = 0.0
    for i, m in enumerate(markets):
        st = by[m.name]
        for r in rc.LOGGED:
            worst = max(worst, abs(dd[r][i] - (st[r][0] - st["tsmom12"][0])))
    return worst


def run() -> dict[str, Any]:
    t0 = time.time()
    markets = load()
    groups = np.array([m.group for m in markets])
    masks = {"equity": np.ones(len(markets), dtype=bool)}
    masks.update({g: groups == g for g in GROUPS})

    # w*: size-matched sleeves (card: equal-weight means over the 41 markets)
    size = {
        "e4-re": float(np.mean([rc.buyback_size(m, m.h["e4"]) for m in markets])),
        "or3-12": float(np.mean([rc.buyback_size(m, m.h["or3-12"]) for m in markets])),
        "arm3-12": float(np.mean([rc.buyback_size(m, m.h["arm3-12"]) for m in markets])),
    }
    wstar = {r: size["e4-re"] / size[r] for r in ("or3-12", "arm3-12")}
    rules = rules_for(wstar)
    pos = [positions(m, wstar) for m in markets]

    # measure 1 and 2: regime anatomy and component split
    anat: dict[str, Any] = {}
    dd: dict[str, list[float]] = {}
    for r in rules:
        ser = [rc.series(m, r, p[r]) for m, p in zip(markets, pos, strict=True)]
        anat[r] = {}
        for key, (rd, vm) in SPLITS.items():
            ps = [ec.parts(s, rd, vm) for s in ser]
            if key == "A":
                dd[r] = [p.d for p in ps]
            pools: dict[str, Any] = {}
            for pn, mk in masks.items():
                sel = [p for p, ok in zip(ps, mk, strict=True) if ok]
                sel_m = [(m, p) for m, p, ok in zip(markets, pos, mk, strict=True) if ok]
                pools[pn] = {
                    "n": len(sel),
                    "D": float(np.mean([p.d for p in sel])),
                    "ret": float(np.mean([p.ret for p in sel])),
                    "risk": float(np.mean([p.risk for p in sel])),
                    "regime": mean_dict([ec.merge_slow(p.by_regime) for p in sel]),
                    "share": mean_dict([ec.merge_slow(p.share) for p in sel]),
                    "gap": mean_dict([ec.merge_slow_gap(p) for p in sel]),
                    "comp": mean_dict([p.by_leg for p in sel]),
                    "comp_regime": {
                        g: mean_dict([ec.merge_slow_legs(p.leg_regime)[g] for p in sel])
                        for g in ec.MERGED
                    },
                    "d_pos": int(sum(p.d > 0 for p in sel)),
                }
                if not vm:
                    cs = [rc.comp_size_by_regime(m, p[r], rd) for m, p in sel_m]
                    pools[pn]["comp_size"] = {k: mean_dict([c[k] for c in cs]) for k in rc.COMPS}
            anat[r][key] = pools
        print(f"  anatomy {r}", file=sys.stderr)
    worst = check(markets, dd)
    if worst > 1e-9:
        raise AssertionError(f"reproduction check fails: {worst:.2e} > 1e-9")

    # measure 3: episodes
    eps: dict[str, Any] = {}
    for r in rules:
        allep = [e for m, p in zip(markets, pos, strict=True) for e in rc.episodes(m, p[r])]
        eps[r] = {pn: rc.episode_pool([e for e in allep if pn == "equity" or e.group == pn])
                  for pn in POOLS}  # fmt: skip
        if r in rc.LOGGED:
            by_speed = {
                "fast": rc.episode_pool([e for e in allep if e.days <= ec.FAST]),
                "slow": rc.episode_pool([e for e in allep if e.days > ec.FAST]),
            }
            eps[r]["speed"] = by_speed

    # measure 4: pooled D and paired SE (pooled-1's bootstrap)
    allr = ["tsmom12", *rules]
    lo = min(pc.friday_of(int(m.d[m.start])) for m in markets)
    hi = max(pc.friday_of(int(m.d[-1])) for m in markets)
    cal = np.arange(lo, hi + 1, 7)
    R = np.full((len(allr), len(markets), len(cal)), np.nan)
    for i, (m, p) in enumerate(zip(markets, pos, strict=True)):
        for a, r in enumerate(allr):
            h = m.h["tsmom12"] if r == "tsmom12" else p[r]
            f, w = pc.weekly(m.d, pc.returns(m.px, h), m.start)
            R[a, i, (f - lo) // 7] = w
    bt = pc.bootstrap(pc.Panel(cal, [m.name for m in markets], list(groups), R), masks)
    boot: dict[str, Any] = {}
    for pn in masks:
        si = list(bt.sets).index(pn)
        boot[pn] = {}
        for v, r in enumerate(rules):
            q = pc.pooled(bt, pn, v)
            boot[pn][r] = {"D": q.D, "se": q.se, "z": q.z, "n_pos": q.n_pos, "n": q.n}
        diffs = {}
        for base in ("e4", "e4-re"):
            b = rules.index(base)
            for v, r in enumerate(rules):
                if r == base:
                    continue
                x = bt.draws[si, b] - bt.draws[si, v]
                x = x[np.isfinite(x)]
                diffs[f"{base} - {r}"] = {
                    "diff": boot[pn][base]["D"] - boot[pn][r]["D"],
                    "se": float(x.std(ddof=1)),
                }
        boot[pn]["diffs"] = diffs
    res = {
        "generated": datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        "n_markets": len(markets),
        "names": [m.name for m in markets],
        "groups": list(groups),
        "repro_worst": worst,
        "size": size,
        "wstar": wstar,
        "rules": rules,
        "d": dd,
        "anatomy": anat,
        "episodes": eps,
        "boot": boot,
        "seconds": round(time.time() - t0, 1),
    }
    res["verdicts"] = verdicts(res)
    return res


# --------------------------------------------------------------------------- verdicts


def verdicts(res: dict[str, Any]) -> dict[str, Any]:
    b = res["boot"]["equity"]
    ep = res["episodes"]
    A = res["anatomy"]
    D = {r: b[r]["D"] for r in res["rules"]}
    dif = b["diffs"]

    def noise(key: str) -> str:
        x = dif[key]
        return "within noise" if abs(x["diff"]) < 2 * x["se"] else "beyond 2 SE"

    K = {r: ep[r]["equity"]["K"] for r in rc.LOGGED}
    kbest = max(K["or3-12"], K["arm3-12"])
    e = ep["e4"]["equity"]
    no_conflict = e["dB"] > 0 and e["dI"] < 0 and K["e4"] <= kbest + KTH
    out: dict[str, Any] = {
        "conflict": "no conflict" if no_conflict else "conflict stands",
        "K": K,
    }
    # (a) part size
    a1, a2, notes = True, True, []
    for r in ("or3-12", "arm3-12"):
        sl = [f"{r} x {w}" for w in rc.WS] + [f"{r} x w*"]
        best = max(sl, key=lambda x: D[x])
        a1 &= D[best] - D[r] >= TH
        a2 &= D[f"{r} x w*"] >= D["e4-re"] - TH
        notes.append(
            f"{r}: best sleeve {best} {D[best]:+.3f} vs w=1 {D[r]:+.3f}; w* {D[r + ' x w*']:+.3f}"
            f" vs e4-re {D['e4-re']:+.3f} (diff {dif['e4-re - ' + r + ' x w*']['diff']:+.3f},"
            f" SE {dif['e4-re - ' + r + ' x w*']['se']:.3f}, {noise('e4-re - ' + r + ' x w*')})"
        )
    out["a"] = {"verdict": "supported" if a1 and a2 else ("partly" if a1 else "rejected"),
                "notes": notes}  # fmt: skip
    # (b) sample
    rej, sup, nb = True, True, []
    sup_k = all(K[r] > 0.5 for r in ("or3-12", "arm3-12"))
    sup_d = all(D["e4"] - D[r] < TH for r in ("or3-12", "arm3-12"))
    for r in ("or3-12", "arm3-12"):
        x = ep[r]["equity"]
        rej &= x["dB"] > 0 and x["dI"] < 0 and K[r] <= 0.5 and D["e4"] - D[r] >= TH
        nb.append(
            f"{r}: dB {x['dB']:+.2f}, dI {x['dI']:+.2f}, K {K[r]:.2f};"
            f" D(e4) - D {D['e4'] - D[r]:+.3f}"
            f" (SE {dif['e4 - ' + r]['se']:.3f}, {noise('e4 - ' + r)})"
        )
    sup = sup_k or sup_d
    out["b"] = {"verdict": "rejected" if rej else ("supported" if sup else "mixed"), "notes": nb}
    # (c) definitions / metric
    if no_conflict:
        cv = "carries"
    elif K["e4"] > kbest + KTH:
        cv = "does not carry"
    else:
        cv = "does not carry (shape differs)"
    out["c"] = {
        "verdict": cv,
        "notes": [f"K: e4 {K['e4']:.2f}, or3-12 {K['or3-12']:.2f}, arm3-12 {K['arm3-12']:.2f}"],
    }
    # (d) exits and signals
    ca = A["e4"]["A"]["equity"]["comp_regime"]
    trim_falls = ca["fast"]["trim"] + ca["slow"]["trim"]
    bb_slow = ca["slow"]["buyback"]
    d_exit = D["e4-trim"] >= 0.5 * D["e4"] or trim_falls > -bb_slow

    def eff(r: str) -> float:
        c = A[r]["A"]["equity"]["comp_regime"]
        x = rc.efficiency(c["rebound"]["buyback"], c["slow"]["buyback"])
        return math.inf if math.isnan(x) else x

    effs = {r: eff(r) for r in rc.LOGGED}
    d_sig = all(D["e4-re"] - D[f"{r} x w*"] >= TH for r in ("or3-12", "arm3-12")) and all(
        effs["e4"] > effs[r] for r in ("or3-12", "arm3-12")
    )
    out["d"] = {
        "exit": "carries" if d_exit else "does not carry",
        "signals": "carry" if d_sig else "do not carry",
        "notes": [
            f"D(e4-trim) {D['e4-trim']:+.3f} vs 0.5 x D(e4) {0.5 * D['e4']:+.3f}"
            f" (e4 - e4-trim {dif['e4 - e4-trim']['diff']:+.3f},"
            f" SE {dif['e4 - e4-trim']['se']:.3f})",
            f"e4 trim terms in falls {trim_falls:+.3f} vs minus buy-back slow-bear term"
            f" {-bb_slow:+.3f}",
            "efficiency (rebound / -slow, buy-back component): "
            + ", ".join(f"{r} {v:.2f}" for r, v in effs.items()),
        ],
    }
    return out


# --------------------------------------------------------------------------- report


def f3(x: float) -> str:
    return "n/a" if x is None or not math.isfinite(x) else f"{x:+.3f}"


def f2(x: float) -> str:
    return "n/a" if x is None or not math.isfinite(x) else f"{x:+.2f}"


def report(res: dict[str, Any]) -> str:
    A, ep, bt, V = res["anatomy"], res["episodes"], res["boot"], res["verdicts"]
    L = [
        "# reentry-reconcile-1: results",
        "",
        f"Generated {res['generated']} by `research/lib/reconcile_reentry.py` "
        f"({res['seconds']} s). Card: `research/cards/reentry-reconcile-1.md`. "
        f"{res['n_markets']} equity markets (pooled-1). Reproduction check: per-market d of "
        f"`e4`, `or3-12`, `arm3-12` vs pooled-1: worst {res['repro_worst']:.1e} (must be <= 1e-9).",
        "",
        "Units: Sharpe points per market, rule minus `tsmom12`, equal-weight means over markets. "
        "Episode tables: log points per 25% fall, rule minus `tsmom12`, net of costs.",
        "",
        "## Verdicts (card rules)",
        "",
        f"- Conflict: **{V['conflict']}** (K = mean dN / mean dB: "
        + ", ".join(f"{r} {v:.2f}" for r, v in V["K"].items())
        + ")",
        f"- (a) part size: **{V['a']['verdict']}**. " + "; ".join(V["a"]["notes"]),
        f"- (b) sample: **{V['b']['verdict']}**. " + "; ".join(V["b"]["notes"]),
        f"- (c) definitions / metric: **{V['c']['verdict']}**. " + "; ".join(V["c"]["notes"]),
        f"- (d) exit (trims): **{V['d']['exit']}**; signals: **{V['d']['signals']}**. "
        + "; ".join(V["d"]["notes"]),
        "",
        f"Size-matched w*: or3-12 {res['wstar']['or3-12']:.3f}, arm3-12 "
        f"{res['wstar']['arm3-12']:.3f} (mean buy-back size: "
        + ", ".join(f"{k} {v:.3f}" for k, v in res["size"].items())
        + ").",
        "",
        "## Pooled D and paired SE (measure 4; joint 52-week blocks, 2,000 draws, seed 0)",
        "",
        "| Rule | "
        + " | ".join(POOLS)
        + " | SE (equity) | z | > 0 | D(e4) - D (SE) | D(e4-re) - D (SE) |",
        "|---|" + "---:|" * (len(POOLS) + 5),
    ]
    for r in res["rules"]:
        dfs = bt["equity"]["diffs"]
        a = dfs.get(f"e4 - {r}")
        b = dfs.get(f"e4-re - {r}")
        L.append(
            f"| `{r}` | "
            + " | ".join(f3(bt[p][r]["D"]) for p in POOLS)
            + f" | {bt['equity'][r]['se']:.3f} | {bt['equity'][r]['z']:+.2f} | "
            f"{bt['equity'][r]['n_pos']} of {bt['equity'][r]['n']} | "
            + (f"{a['diff']:+.3f} ({a['se']:.3f})" if a else "-")
            + " | "
            + (f"{b['diff']:+.3f} ({b['se']:.3f})" if b else "-")
            + " |"
        )
    for key, txt in (
        ("A", "card split, reading A (25% zigzag)"),
        ("B", "card split, reading B (1.5 x volatility)"),
        ("VA", "against a volatility-matched `tsmom12`, labels A (no risk part)"),
    ):
        L += [
            "",
            f"## Regime anatomy, {txt} (measure 1)",
            "",
            "| Rule | Pool | D | Risk part | Return part | Fast | Slow bear | Rebound | Whipsaw"
            " | Calm |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for r in res["rules"]:
            for p in ("equity", "EQ-US10"):
                x = A[r][key][p]
                L.append(
                    f"| `{r}` | {p} | {f3(x['D'])} | {f3(x['risk'])} | {f3(x['ret'])} | "
                    + " | ".join(f3(x["regime"][g]) for g in ec.MERGED)
                    + " |"
                )
        x = A["e4"][key]["equity"]["share"]
        L.append(
            "| Time share | equity | | | | " + " | ".join(f"{x[g]:.2f}" for g in ec.MERGED) + " |"
        )
    L += [
        "",
        "## Component split, reading A, equity 41 (measure 2)",
        "",
        "Return terms (card split, Sharpe points) and mean component position, by regime. "
        "Buy-back = (1 - h12) x h; trim = h12 x (h - 1).",
        "",
        "| Rule | Component | Total | Fast | Slow bear | Rebound | Whipsaw | Calm |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in res["rules"]:
        x = A[r]["A"]["equity"]
        for k in (*rc.COMPS, "cost", "resid"):
            L.append(
                f"| `{r}` | {k} | {f3(x['comp'][k])} | "
                + " | ".join(f3(x["comp_regime"][g][k]) for g in ec.MERGED)
                + " |"
            )
        for k in rc.COMPS:
            L.append(
                f"| `{r}` | {k} size | | "
                + " | ".join(f2(x["comp_size"][k][g]) for g in ec.MERGED)
                + " |"
            )
    L += [
        "",
        "## Episodes: 25% falls in the earlier lanes' units (measure 3)",
        "",
        "Per fall, rule minus `tsmom12`, log points net of costs; means over episodes (equal "
        "weight, no clustering). K = mean dN / mean dB. Component columns: simple points before "
        "costs.",
        "",
        "| Rule | Pool | Falls | dI | dB | dN | K | dN > 0 | buy-back I | buy-back B | trim I"
        " | trim B |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in res["rules"]:
        for p in (*POOLS, "fast", "slow"):
            if p in ("fast", "slow"):
                if "speed" not in ep[r]:
                    continue
                x = ep[r]["speed"][p]
                p = f"equity, {p} falls"
            else:
                x = ep[r][p]
            if not x["n"]:
                continue
            L.append(
                f"| `{r}` | {p} | {x['n']} | {f2(x['dI'])} | {f2(x['dB'])} | {f2(x['dN'])} | "
                f"{x['K']:.2f} | {x['share_dN_pos']:.2f} | {f2(x['buyback_I'])} | "
                f"{f2(x['buyback_B'])} | {f2(x['trim_I'])} | {f2(x['trim_B'])} |"
            )
    return "\n".join(L) + "\n"


def main() -> None:
    res = run()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(report(res))
    OUT.with_suffix(".json").write_text(json.dumps(res, indent=1, default=float) + "\n")
    print(f"wrote {OUT} in {res['seconds']} s", file=sys.stderr)


if __name__ == "__main__":
    main()
