"""ownvol-anatomy-1: where own-vol's lead (or loss) over `tsmom12` comes from (descriptive).
Card: research/cards/ownvol-anatomy-1.md. Engine: ownvolanatomy_core.py.

    GRIMSTRADE_DATA=<cache root> uv run python -I research/lib/ownvolanatomy.py [--log]

Data and rules: pooled-1's 41 stock markets (`pooled1.load_all`, `pooled1_core.run_market`),
pooled-2's 29 non-equity series (`pooled2.load_nonequity`, its costs, lags and engines) and
risk-menu-3's six-asset book (`riskmenu3_run.vt_expanding`, needs research/data/bars and adj).
Nothing after 2025-10-31 is parsed (the loaders stop there). Writes
results/ownvol-anatomy-1.md (+ .json); with `--log` appends one `note` row to tries.md once.
"""

from __future__ import annotations

import json
import math
import sys
import time
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ownvolanatomy_core as oc  # noqa: E402
import pooled1_core as pc  # noqa: E402
import pooled2_core as qc  # noqa: E402

IDEA = "ownvol-anatomy-1"
RESEARCH = Path(__file__).resolve().parents[1]
OUT = RESEARCH / "results" / "ownvol-anatomy-1.md"
FALLS = {"A": (0.25, 0.25), "C": (0.15, 0.15)}
B_MULT = 1.5
COMMODITY_FX = ("CAD", "AUD", "NZD", "NOK")
EQ_GROUPS = ("US10", "DEV13", "WIDE10", "ETF8")
NE_GROUPS = ("USB3", "GOV9", "FX9", "COM8")
POOLS = (
    "equity 41",
    *EQ_GROUPS,
    "judged 21",
    "USB3",
    "GOV9",
    "FX9",
    "FX commodity 4",
    "FX other 5",
    "COM8",
)


def month_index(o: int) -> int:
    x = date.fromordinal(int(o))
    return x.year * 12 + x.month - 1


def thresholds(lr: np.ndarray, ppy: int) -> dict[str, tuple[float, float]]:
    b = B_MULT * float(lr.std() * math.sqrt(ppy))
    return {**FALLS, "B": (b, b)}


# --------------------------------------------------------------------------- weekly series


def weekly_series(
    name: str,
    group: str,
    d: np.ndarray,
    px: np.ndarray,
    x: np.ndarray,
    g: np.ndarray,
    start: int,
    own_frozen: np.ndarray,
    skip: int,
    reset_cost: float,
) -> oc.Series:
    """One daily-data series: replay own-vol (checked against the frozen returns), build F,
    weekly returns, labels."""
    o_d, share, sized, sig_at = oc.book_weekly(d, x, g, start, skip=skip, reset_cost=reset_cost)
    if not np.array_equal(o_d, own_frozen):
        raise AssertionError(f"{name}: replay differs from the frozen own-vol")
    sb = oc.s_bar(share, g, start)
    f_d = oc.book_weekly(d, x, g, start, skip=skip, reset_cost=reset_cost, fixed=sb)[0]
    fri, o = pc.weekly(d, o_d, start)
    _, f = pc.weekly(d, f_d, start)
    _, s = pc.weekly(d, x, start)
    keys = np.array([pc.friday_of(int(v)) for v in d[start:]])
    first, last = oc.first_last(keys)
    first, last = first + start, last + start
    sr = oc.Series(name, group, "w", o, f, s, np.array([month_index(v) for v in fri]))
    sr.sbar = sb
    # regimes on the traded level over the whole loaded history
    lr = np.diff(np.log(px))
    pos_w = g[last]
    for rd, (dn, upx) in thresholds(lr, pc.BPY).items():
        fl = oc.fall_labels(d, px, dn, upx)[last]
        sr.labels[rd] = oc.regime_labels(fl, pos_w, "w")
    gs = np.concatenate([[0.0], np.cumsum(g)])
    out = (gs[last + 1] - gs[first]) == 0
    warm = first < sized
    sr.labels["vol"] = oc.vol_state(share[first], out, warm)
    ent = np.flatnonzero((g[1:] > 0) & (g[:-1] == 0)) + 1
    sr.labels["phase"] = oc.phase_labels(d[last], out, d[ent], lambda e, t: t - e < oc.ENTRY_DAYS)
    bar = np.zeros(len(px))
    bar[1:] = px[1:] / px[:-1] - 1
    sr.lev_corr = oc.lev_corr(pc.weekly(d, bar, start)[1], 4)
    sr.x_tercile = oc.tercile_mv(s, sr.labels["vol"], 52)
    sg, rv = [], []
    resets = [k for k, _ in sig_at] + [len(x)]
    for (k, v), k2 in zip(sig_at, resets[1:], strict=True):
        if k2 - k >= 10 and (g[k:k2] > 0).all():
            sg.append(v)
            rv.append(float(x[k:k2].std(ddof=1) * math.sqrt(pc.BPY)))
    sr.persist = oc.corr(sg, rv)
    for nm, r in (("tsmom12", s), ("fixed", f), ("own-vol", o)):
        sr.stats[nm] = oc.perf(r, 52)
    return sr


def load_equity() -> list[oc.Series]:
    import pooled1 as p1

    out = []
    for n, grp, days, px in p1.load_all():
        d = np.array([v.toordinal() for v in days], dtype=np.int64)
        m = pc.run_market(n, grp, d, px)
        x, g = m.daily["tsmom12"], m.pos["tsmom12"]
        out.append(
            weekly_series(n, grp, d, px, x, g, m.start, m.daily["vt-own-70-x"], 0, pc.RESET_COST)
        )
        print(f"  {n}", file=sys.stderr)
    return out


def load_nonequity() -> list[oc.Series]:
    import pooled2 as p2

    out = []
    for sp in p2.load_nonequity():
        cost, reset = p2.COST[sp.cls], p2.RESET[sp.cls]
        if sp.freq == "w":
            assert sp.d is not None and sp.px_ret is not None and sp.av is not None
            if int(sp.d[-1]) > p2.LAST.toordinal():
                raise AssertionError(f"{sp.name}: a day after {p2.LAST}")
            dec = qc.decide_weekly(sp.d, sp.px_ret, sp.av)
            start = dec.first_ok + 1 + pc.LAG
            n = len(sp.px_ret)
            g = pc.held(n, dec.at["tsmom12"])
            x = pc.returns(sp.px_ret, g, cost)
            frozen, _ = qc.own_vol_weekly(sp.d, x, g, start, qc.TARGET, 1, reset)
            out.append(
                weekly_series(sp.name, sp.group, sp.d, sp.px_ret, x, g, start, frozen, 1, reset)
            )
        else:
            assert sp.months is not None and sp.r_ret is not None
            out.append(monthly_series(sp.name, sp.group, sp.months, sp.r_ret, sp.gap, cost, reset))
        print(f"  {sp.name}", file=sys.stderr)
    return out


# --------------------------------------------------------------------------- monthly series


def monthly_series(
    name: str,
    group: str,
    months: Sequence[date],
    r: np.ndarray,
    gap: int,
    cost: float,
    reset: float,
) -> oc.Series:
    pos, start = qc.decide_monthly(r, gap)
    g = pos["tsmom12"]
    x = g * r - cost * np.abs(np.diff(g, prepend=0.0))
    frozen, _ = qc.own_vol_monthly(x, g, start, gap, qc.TARGET, reset)
    o_m, share, sized, sig_at = oc.book_monthly(x, g, start, gap, reset_cost=reset)
    if not np.array_equal(o_m, frozen):
        raise AssertionError(f"{name}: replay differs from the frozen own-vol")
    sb = oc.s_bar(share, g, start)
    f_m = oc.book_monthly(x, g, start, gap, reset_cost=reset, fixed=sb)[0]
    per = np.array([m.toordinal() for m in months], dtype=np.int64)
    sr = oc.Series(
        name,
        group,
        "m",
        o_m[start:],
        f_m[start:],
        x[start:],
        np.array([month_index(v) for v in per[start:]]),
    )
    sr.sbar = sb
    lv = qc.levels(r)  # lv[t + 1] = level after return t
    lv_ord = np.concatenate([[per[0] - 31], per])
    for rd, (dn, upx) in thresholds(np.log1p(r), 12).items():
        fl = oc.fall_labels(lv_ord, lv, dn, upx, rebound_n=12)[1:][start:]
        sr.labels[rd] = oc.regime_labels(fl, g[start:], "m")
    idx = np.arange(start, len(r))
    out = g[start:] == 0
    warm = idx < sized
    sr.labels["vol"] = oc.vol_state(share[start:], out, warm)
    ent = np.flatnonzero((g[1:] > 0) & (g[:-1] == 0)) + 1
    sr.labels["phase"] = oc.phase_labels(idx, out, ent, lambda e, t: t - e < oc.ENTRY_MONTHS)
    sr.lev_corr = oc.lev_corr(r[start:], 3)
    sr.x_tercile = oc.tercile_mv(sr.s, sr.labels["vol"], 12)
    pairs = [(v, abs(x[t]) * math.sqrt(12)) for t, v in sig_at if g[t] > 0]
    sr.persist = oc.corr([a for a, _ in pairs], [b for _, b in pairs])
    for nm, rr in (("tsmom12", sr.s), ("fixed", sr.f), ("own-vol", sr.o)):
        sr.stats[nm] = oc.perf(rr, 12)
    return sr


# --------------------------------------------------------------------------- the six


def load_six() -> oc.Series:
    import common as c
    import lstrend2_run as l2
    import riskmenu3_run as r3
    import riskmenu_run as rm

    s1, _rf, _drag, run = l2.tsmom12_sleeve()
    held = rm.held_count(run)
    mx, ks = r3.vt_expanding(s1, oc.TARGET, held)
    days = l2.cal_days(*r3.W)
    gross = np.array([s1.gross(v) for v in days])
    share = np.array([mx.share1[v] for v in days])
    sb = float((share * gross).sum() / gross.sum())
    fx = rm.mix(s1, None, lambda dd, v: (sb, 0.0), r3.W[0], held)
    o = l2.on_cal(mx.ex, *r3.W)
    f = l2.on_cal(fx.ex, *r3.W)
    s = l2.on_cal(s1.ex, *r3.W)
    ords = np.array([v.toordinal() for v in days], dtype=np.int64)
    sr = oc.Series("six", "SIX", "d", o, f, s, np.array([month_index(v) for v in ords]))
    sr.sbar = sb
    six = c.ctx("six")
    hr = c.go(IDEA, "hold six", c.weekly(c.equal_weight), six, "baseline", log=False)
    bdays, ylds = rm.ci.bill_yield()
    rr, rf = rm.ci.rescored(hr, bdays, ylds)
    hold = {dd: float(a - b) for dd, a, b in zip(hr.days[1:], rr, rf, strict=True)}
    h = l2.on_cal(hold, *r3.W)
    lvl = np.cumprod(1 + h)
    for rd, (dn, upx) in thresholds(np.log1p(h), 365).items():
        fl = oc.fall_labels(ords, lvl, dn, upx)
        sr.labels[rd] = oc.regime_labels(fl, gross, "d", reversals=True)
    out = gross == 0
    warm = ords < min(ks).toordinal()
    sr.labels["vol"] = oc.vol_state(share, out, warm)
    ent = np.flatnonzero((gross[1:] > 0) & (gross[:-1] == 0)) + 1
    sr.labels["phase"] = oc.phase_labels(ords, out, ords[ent], lambda e, t: t - e < oc.ENTRY_DAYS)
    sr.lev_corr = oc.lev_corr(h, 28)
    sr.x_tercile = oc.tercile_mv(s, sr.labels["vol"], 365)
    for nm, x in (("tsmom12", s), ("fixed", f), ("own-vol", o)):
        sr.stats[nm] = oc.perf(x, 365)
    return sr


# --------------------------------------------------------------------------- analysis


def masks(series: Sequence[oc.Series]) -> dict[str, np.ndarray]:
    g = np.array([s.group for s in series])
    nm = np.array([s.name for s in series])
    fxc = np.isin(nm, [f"FX-{c}" for c in COMMODITY_FX]) | np.isin(nm, COMMODITY_FX)
    out = {
        "equity 41": np.isin(g, EQ_GROUPS),
        **{k: g == k for k in EQ_GROUPS},
        "judged 21": np.isin(g, ("USB3", "GOV9", "FX9")),
        **{k: g == k for k in ("USB3", "GOV9", "FX9")},
        "FX commodity 4": (g == "FX9") & fxc,
        "FX other 5": (g == "FX9") & ~fxc,
        "COM8": g == "COM8",
    }
    return out


def class_measures(series: Sequence[oc.Series], m: np.ndarray) -> dict[str, float]:
    sel = [s for s, k in zip(series, m, strict=True) if k]

    def mean(f: Any) -> float:
        v = [f(s) for s in sel]
        v = [x for x in v if math.isfinite(x)]
        return float(np.mean(v)) if v else math.nan

    out = {
        "L": mean(lambda s: s.lev_corr),
        "persist": mean(lambda s: s.persist),
        "sbar": mean(lambda s: s.sbar),
    }
    for t in ("low share", "high share"):
        out[f"mu {t}"] = mean(lambda s, t=t: s.x_tercile[t][0])
        out[f"var {t}"] = mean(lambda s, t=t: s.x_tercile[t][1])
        out[f"mu/var {t}"] = out[f"mu {t}"] / out[f"var {t}"] if out[f"var {t}"] else math.nan
    for nm in ("tsmom12", "fixed", "own-vol"):
        for i, k in enumerate(("sharpe", "growth", "worst")):
            out[f"{nm} {k}"] = mean(lambda s, nm=nm, i=i: s.stats[nm][i])
    return out


def analyse(series: list[oc.Series], six: oc.Series, draws: int = 2000) -> dict[str, Any]:
    splits = [oc.split(s) for s in series]
    mk = masks(series)
    cal = oc.month_cells(series)
    bt = oc.boot(cal, mk, draws=draws)
    li = oc.label_index()
    res: dict[str, Any] = {"pools": {}, "series": [], "six": {}}
    for p in POOLS:
        pt = oc.pool_point(splits, mk[p])
        se = oc.ses(bt[p])
        pt["se"] = {f"{a}|{b}": v for (a, b), v in se.items()}
        tot = se[li[0]]
        pt["reading_a"] = oc.reading_a(pt["d"], pt["M"], pt["R"], tot["M"], tot["R"])
        pt["reading_b"] = oc.reading_b(pt["d"], pt["E"])
        carry, against = [], []
        for rd in oc.READINGS:
            for nm in oc.REGIMES:
                x = pt[rd][nm]["M"] + pt[rd][nm]["R"]
                if oc.big(pt["d"], x, se[(rd, nm)]["timing"]):
                    (carry if np.sign(x) == np.sign(pt["d"]) else against).append(f"{rd}:{nm}")
        pt["carrying_regimes"] = carry
        pt["carrying_against"] = against
        pt["class"] = class_measures(series, mk[p])
        res["pools"][p] = pt
    eq = res["pools"]["equity 41"]
    res["gaps"] = {}
    for other in ("FX9", "judged 21", "COM8", "FX commodity 4"):
        o = res["pools"][other]
        gap = {k: eq[k] - o[k] for k in ("d", *oc.TERMS)}
        gap["D"] = gap.pop("d")
        gap["reading"] = oc.reading_d(gap)  # type: ignore[assignment]
        res["gaps"][other] = gap
    for s, sp in zip(series, splits, strict=True):
        res["series"].append(
            {
                "name": s.name,
                "group": s.group,
                "freq": s.freq,
                "periods": len(s.o),
                "sbar": s.sbar,
                "L": s.lev_corr,
                "persist": s.persist,
                **{k: sp[k] for k in ("d", *oc.TERMS)},
                "parts": {p: sp[p] for p in oc.PARTS},
                "stats": s.stats,
            }
        )
    sx = oc.split(six)
    res["six"] = {
        **sx,
        "sbar": six.sbar,
        "L": six.lev_corr,
        "stats": six.stats,
        "x_tercile": six.x_tercile,
        "reading_b": oc.reading_b(sx["d"], sx["E"]),
    }
    return res


def check_reproduction(series: Sequence[oc.Series]) -> dict[str, float]:
    """Max |d - published d| per source (pooled-1 / pooled-2 json)."""
    p1 = json.loads((RESEARCH / "results" / "pooled-1.json").read_text())
    p2 = json.loads((RESEARCH / "results" / "pooled-2.json").read_text())
    ref = {m["name"]: m["d"]["vt-own-70-x"] for m in p1["markets"]}
    ref2 = {m["name"]: m["d"]["vt-own-70-x"] for m in p2["markets"]}
    e1 = e2 = 0.0
    for s in series:
        d = oc.sharpe(s.o, s.P) - oc.sharpe(s.s, s.P)
        if s.name in ref and s.group in EQ_GROUPS:
            e1 = max(e1, abs(d - ref[s.name]))
        elif s.name in ref2:
            e2 = max(e2, abs(d - ref2[s.name]))
        else:
            raise AssertionError(f"{s.name}: no published d")
    if max(e1, e2) > 1e-9:
        raise AssertionError(f"reproduction failed: pooled-1 {e1:.2e}, pooled-2 {e2:.2e}")
    return {"pooled-1 max |diff|": e1, "pooled-2 max |diff|": e2}


# --------------------------------------------------------------------------- report


def f3(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:+.3f}"


def ws(x: float, se: float) -> str:
    return f"{f3(x)} ({se:.3f})"


def report(res: dict[str, Any]) -> str:
    P = res["pools"]
    L = [
        "# ownvol-anatomy-1: where own-vol's lead over `tsmom12` comes from (descriptive)",
        "",
        "Card: `cards/ownvol-anatomy-1.md`. Code: `lib/ownvolanatomy.py`, "
        "`lib/ownvolanatomy_core.py`. d = SR(own-vol) - SR(`tsmom12`) per series = E + M + R: E "
        "exposure (fixed-share twin at own-vol's average invested share minus `tsmom12`), M mean "
        "channel, R risk channel (M + R = volatility timing). Pool = equal-weight mean over "
        "series. SE (in brackets) from a joint 12-month block bootstrap of calendar months, "
        "2,000 draws, seed 0, means and sds held at full-sample values (linearised; descriptive, "
        "not a test).",
        "",
        f"Reproduction: {res['repro']}.",
        "",
        "## Pools: d = E + M + R",
        "",
        "| Pool | n | d | E exposure | M mean channel | R risk channel | Timing M + R | "
        "Avg share | Reading (a) | Reading (b) | Carrying regimes (with D) | "
        "Carrying (against D) |",
        "|---|---:|---|---|---|---|---|---:|---|---|---|---|",
    ]
    for p in POOLS:
        x = P[p]
        se = x["se"]["total|total"]
        L.append(
            f"| {p} | {x['n']} | {ws(x['d'], se['d'])} | {ws(x['E'], se['E'])} | "
            f"{ws(x['M'], se['M'])} | {ws(x['R'], se['R'])} | "
            f"{ws(x['M'] + x['R'], se['timing'])} | {x['class']['sbar']:.2f} | "
            f"{x['reading_a']} | {x['reading_b']} | {', '.join(x['carrying_regimes']) or '-'} | "
            f"{', '.join(x['carrying_against']) or '-'} |"
        )
    s6 = res["six"]
    L.append(
        f"| the six (#110 book, daily) | 1 | {f3(s6['d'])} | {f3(s6['E'])} | {f3(s6['M'])} | "
        f"{f3(s6['R'])} | {f3(s6['M'] + s6['R'])} | {s6['sbar']:.2f} | - | {s6['reading_b']} "
        "| - | - |"
    )
    L += [
        "",
        "## Holding less: Sharpe, growth a year, worst loss (pool means)",
        "",
        "| Pool | `tsmom12` | Fixed twin | Own-vol |",
        "|---|---|---|---|",
    ]

    def trip(c: dict[str, float], nm: str) -> str:
        return f"{c[nm + ' sharpe']:.3f} / {c[nm + ' growth']:.1%} / {c[nm + ' worst']:.0%}"

    for p in POOLS:
        c = P[p]["class"]
        L.append(f"| {p} | {trip(c, 'tsmom12')} | {trip(c, 'fixed')} | {trip(c, 'own-vol')} |")
    st = s6["stats"]
    L.append(
        "| the six | "
        + " | ".join(
            f"{st[k][0]:.3f} / {st[k][1]:.1%} / {st[k][2]:.0%}"
            for k in ("tsmom12", "fixed", "own-vol")
        )
        + " |"
    )
    for part, title in (
        ("A", "Regimes, reading A (25% / 25% zigzag)"),
        ("B", "Regimes, reading B (1.5 x the series' volatility)"),
        ("C", "Regimes, reading C (15% / 15%)"),
        ("vol", "Volatility state (own-vol's share at the period's start)"),
        ("phase", "Trend phase (entry = first 26 weeks / 6 months after a `tsmom12` entry)"),
    ):
        names = oc.PARTS[part]
        L += [
            "",
            f"## {title}: M + R by label (SE), time share",
            "",
            "| Pool | " + " | ".join(names) + " |",
            "|---|" + "---|" * len(names),
        ]
        for p in (*POOLS, "six"):
            if p == "six":
                cells = [
                    f"{f3(s6[part][nm]['M'] + s6[part][nm]['R'])}, {s6[part][nm]['share']:.0%}"
                    for nm in names
                ]
            else:
                x = P[p]
                cells = [
                    f"{ws(x[part][nm]['M'] + x[part][nm]['R'], x['se'][part + '|' + nm]['timing'])}"
                    f", {x[part][nm]['share']:.0%}"
                    for nm in names
                ]
            L.append(f"| {p} | " + " | ".join(cells) + " |")
        L += [
            "",
            "Split into channels (M / R):",
            "",
            "| Pool | " + " | ".join(names) + " |",
            "|---|" + "---|" * len(names),
        ]
        for p in (*POOLS, "six"):
            x = s6 if p == "six" else P[p]
            L.append(
                f"| {p} | "
                + " | ".join(f"{f3(x[part][nm]['M'])} / {f3(x[part][nm]['R'])}" for nm in names)
                + " |"
            )
    L += [
        "",
        "## Volatility and return by class (pool means over series)",
        "",
        "| Pool | Leverage corr. L | Vol persistence | Sleeve mean, low / high share | "
        "Sleeve variance, low / high share | mean / var, low / high share |",
        "|---|---:|---:|---|---|---|",
    ]
    for p in POOLS:
        c = P[p]["class"]
        L.append(
            f"| {p} | {f3(c['L'])} | {f3(c['persist'])} | {c['mu low share']:+.1%} / "
            f"{c['mu high share']:+.1%} | {c['var low share']:.4f} / {c['var high share']:.4f} | "
            f"{c['mu/var low share']:+.2f} / {c['mu/var high share']:+.2f} |"
        )
    xt = s6["x_tercile"]
    L.append(
        f"| the six | {f3(s6['L'])} | - | {xt['low share'][0]:+.1%} / {xt['high share'][0]:+.1%}"
        f" | {xt['low share'][1]:.4f} / {xt['high share'][1]:.4f} | "
        f"{xt['low share'][0] / xt['low share'][1]:+.2f} / "
        f"{xt['high share'][0] / xt['high share'][1]:+.2f} |"
    )
    L += [
        "",
        "## The gap: equity 41 minus each pool",
        "",
        "| Other pool | Gap in d | E | M | R | Reading (d) |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for k, g in res["gaps"].items():
        L.append(
            f"| {k} | {f3(g['D'])} | {f3(g['E'])} | {f3(g['M'])} | {f3(g['R'])} | {g['reading']} |"
        )
    L += [
        "",
        "## Per series",
        "",
        "| Series | Group | Avg share | d | E | M | R | L | Vol persistence | "
        "M + R in rebounds (A) | M + R entry phase | M + R low-share tercile |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for s in res["series"]:
        pa = s["parts"]

        def mr(part: str, nm: str, pa: dict[str, Any] = pa) -> str:
            return f3(pa[part][nm]["M"] + pa[part][nm]["R"])

        L.append(
            f"| {s['name']} | {s['group']} | {s['sbar']:.2f} | {f3(s['d'])} | {f3(s['E'])} | "
            f"{f3(s['M'])} | {f3(s['R'])} | {f3(s['L'])} | {f3(s['persist'])} | "
            f"{mr('A', 'rebound')} | {mr('phase', 'entry')} | {mr('vol', 'low share')} |"
        )
    return "\n".join(L) + "\n"


def log_note(res: dict[str, Any]) -> int:
    tries = RESEARCH / "tries.md"
    if f"| {IDEA} |" in tries.read_text():
        return 0
    P = res["pools"]
    e, f9, j21, c8 = (P[k] for k in ("equity 41", "FX9", "judged 21", "COM8"))
    s6 = res["six"]
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"

    def emr(x: dict[str, Any]) -> str:
        return f"d {x['d']:+.3f} = E {x['E']:+.3f} + M {x['M']:+.3f} + R {x['R']:+.3f}"

    text = (
        f"re-score (not a try): vt-own-70-x minus tsmom12 split into exposure E (fixed-share "
        f"twin), mean channel M and risk channel R; equity 41 {emr(e)}; judged 21 {emr(j21)}; "
        f"FX9 {emr(f9)}; COM8 {emr(c8)}; six {emr(s6)} (research/ownvol-anatomy-1.md)"
    )
    row = f"| {now} | {IDEA} | {text} | note | train | 1913-01-01 | 2025-10-31 | - | - | - | - |\n"
    with tries.open("a") as fh:
        fh.write(row)
    return 1


def main() -> None:
    t0 = time.time()
    quick = "--quick" in sys.argv
    six = load_six()
    print(f"six d {oc.split(six)['d']:+.4f}", file=sys.stderr)
    series = load_equity() + load_nonequity()
    repro = check_reproduction(series)
    res = analyse(series, six, draws=200 if quick else 2000)
    res["repro"] = (
        f"per-series d equals pooled-1's and pooled-2's published d (max |diff| "
        f"{repro['pooled-1 max |diff|']:.1e} / {repro['pooled-2 max |diff|']:.1e}); the six "
        f"d {res['six']['d']:+.4f}"
    )
    res["runtime_s"] = time.time() - t0
    OUT.write_text(report(res))
    OUT.with_suffix(".json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(f"wrote {OUT} in {time.time() - t0:.0f}s")
    if "--log" in sys.argv:
        print(f"tries.md: {log_note(res)} rows")


if __name__ == "__main__":
    main()
