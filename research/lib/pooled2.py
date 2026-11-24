"""pooled-2: `e4` and `vt-own-70-x` against `tsmom12` on non-equity series, and combined with
pooled-1's 41 equity markets. Card: research/cards/pooled-2.md. Engine: pooled2_core.py.

    uv run python -I research/lib/pooled2.py --random        # plumbing on random walks
    uv run python -I research/lib/pooled2.py --log           # the one real run (+ tries rows)

Data (read-only, nothing after 2025-10-31 parsed): the data-long-3 cache through
`long_x_build` (ALFRED daily yields, bills and H.10 rates; `panel()` for the monthly series),
datahub gold (`long_gold`), and pooled-1's equity inputs through `pooled1.load_all()` (Ken French,
insure-2's Yahoo indices, `research/data/adj/<ETF>.csv`, git-ignored). Cache root from
`research/macro.local.json` (git-ignored) or GRIMSTRADE_DATA.
"""

from __future__ import annotations

import json
import math
import sys
import time
from collections.abc import Iterator
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import long_x as lx  # noqa: E402
import pooled1_core as pc  # noqa: E402
import pooled2_core as qc  # noqa: E402

IDEA = "pooled-2"
LAST = date(2025, 10, 31)
FLOAT_FROM = date(1973, 3, 1)
GOLD_FROM = date(1971, 2, 1)  # first return on free-market prices (1971-01 on, data-long-1)
PRE = date(1994, 2, 1)
PRE_MIN = {"w": 260, "m": 60}
BLOCK, DRAWS, SEED = 12, 2000, 0
CHECK_BLOCKS = (3, 24)
NULL_REPS = 100
Z_BAR, Z_PROJ, KILL_HI = 2.50, 4.70, 0.03
COST = {"rates": 0.0002, "fx": 0.0003, "commodity": 0.0010}
RESET = {"rates": pc.RESET_COST, "fx": pc.RESET_COST, "commodity": 0.0010}
RAND_VOL = {"rates": 0.08, "fx": 0.10, "commodity": 0.25}
RESEARCH = Path(__file__).resolve().parents[1]
OUT = RESEARCH / "results" / "pooled-2.md"
OUT_PLUMB = RESEARCH / "results" / "pooled-2-plumbing.md"
JUDGED = ("USB3", "GOV9", "FX9")
GROUPS = (*JUDGED, "COM8")
US_BONDS = {"UST2": ("DGS2", 2.0), "UST10": ("DGS10", 10.0), "UST30": ("DGS30", 30.0)}
FX_DAILY = ["JPY", "GBP", "CHF", "CAD", "AUD", "NZD", "SEK", "NOK"]
GOV = ["JP", "GB", "CH", "CA", "DE", "AU", "NZ", "SE", "NO"]
PPI = [
    "PPI-grains",
    "PPI-livestock",
    "PPI-coal",
    "PPI-natgas",
    "PPI-crude",
    "PPI-steel",
    "PPI-prim-nonferrous",
]


@dataclass
class Spec:
    name: str
    group: str
    cls: str
    freq: str
    gap: int = 0  # monthly
    d: np.ndarray | None = None  # weekly: session ordinals
    av: np.ndarray | None = None  # weekly: ordinal each session's value was public
    px_ret: np.ndarray | None = None  # weekly: excess-return level
    px_sig: np.ndarray | None = None  # weekly: level the signal reads (check: FX spot)
    months: list[date] | None = None  # monthly: month each return ends in
    r_ret: np.ndarray | None = None  # monthly excess returns
    r_sig: np.ndarray | None = None


# --------------------------------------------------------------------------- data


def _prev_month(d: date) -> date:
    return (d.replace(day=1) - timedelta(days=1)).replace(day=1)


def _tail_after_gap(s: list[tuple[date, float]], days: int = 14) -> list[tuple[date, float]]:
    start = 0
    for i in range(1, len(s)):
        if (s[i][0] - s[i - 1][0]).days > days:
            start = i
    return s[start:]


def _ord(ds: list[date]) -> np.ndarray:
    return np.array([x.toordinal() for x in ds], dtype=np.int64)


def load_bonds() -> list[Spec]:
    import long_x_build as lb

    bill = lb.alfred("DTB3")
    bd = _ord([d for d, _ in bill])
    bv = np.array([v for _, v in bill])
    out = []
    for name, (sid, mat) in US_BONDS.items():
        y = _tail_after_gap(lb.alfred(sid))
        y = [(d, v) for d, v in y if d.toordinal() >= bd[0]]
        r = lx.bond_returns(y, mat)
        lv = [100.0]
        for (d0, _), (d1, x) in zip(y[:-1], r, strict=True):
            b = bv[int(np.searchsorted(bd, d0.toordinal(), side="right")) - 1]
            lv.append(lv[-1] * (1.0 + x - b / 100.0 * (d1 - d0).days / 365.0))
        days = [d for d, _ in y]
        out.append(
            Spec(
                name,
                "USB3",
                "rates",
                "w",
                d=_ord(days),
                av=_ord([lx.available("h15-daily", x) for x in days]),
                px_ret=np.array(lv),
                px_sig=np.array(lv),
            )
        )
    return out


def load_fx_daily() -> list[Spec]:
    import long_x_build as lb

    usr = dict(lb.us_short())
    out = []
    for cur in FX_DAILY:
        sid = lb.FX_ID[cur]
        spot = [(d, v) for d, v in lx.usd_per_unit(lb.alfred(sid), lx.FX_QUOTE[sid][1])]
        spot = [(d, v) for d, v in spot if d >= FLOAT_FROM]
        fr = dict(lb.short_rate(lb.CC[cur])[0])
        steps = []
        start = 0
        for i, ((d0, s0), (d1, s1)) in enumerate(zip(spot, spot[1:], strict=False)):
            pm = _prev_month(d1)
            if pm not in fr or pm not in usr or (d1 - d0).days > 14:
                start = i + 1
                steps.append(None)
                continue
            days = (d1 - d0).days
            carry = (1 + fr[pm] * days / 36500.0) / (1 + usr[pm] * days / 36500.0)
            steps.append((s1 / s0 * carry - 1.0, s1 / s0 - 1.0))
        kept = steps[start:]
        days_ = [d for d, _ in spot[start:]]
        ex = np.array([100.0, *np.cumprod([1 + a for a, _ in kept]) * 100.0])  # type: ignore[misc]
        sp = np.array([100.0, *np.cumprod([1 + b for _, b in kept]) * 100.0])  # type: ignore[misc]
        out.append(
            Spec(
                f"FX-{cur}",
                "FX9",
                "fx",
                "w",
                d=_ord(days_),
                av=_ord([lx.available("h10-daily", x) for x in days_]),
                px_ret=ex,
                px_sig=sp,
            )
        )
    return out


def _monthly(
    name: str,
    group: str,
    cls: str,
    rets: list[tuple[date, float]],
    gap: int,
    sig: list[tuple[date, float]] | None = None,
) -> Spec:
    rets = lx.consecutive([(d, x) for d, x in rets if d <= LAST])
    sig_r = None
    if sig is not None:
        sm = dict(sig)
        rets = lx.consecutive([(d, x) for d, x in rets if d in sm])
        sig_r = np.array([sm[d] for d, _ in rets])
    r = np.array([x for _, x in rets])
    return Spec(
        name,
        group,
        cls,
        "m",
        gap=gap,
        months=[d for d, _ in rets],
        r_ret=r,
        r_sig=r.copy() if sig_r is None else sig_r,
    )


def _gold_lines(path: Path) -> Iterator[str]:
    """Header and rows of the datahub file up to 2025-10; later rows are not parsed."""
    with path.open(newline="") as f:
        for i, line in enumerate(f):
            if i and line.strip() and line[:7] > "2025-10":
                return
            yield line


def load_monthly() -> list[Spec]:
    import long_gold
    import long_x_build as lb

    p = {e.name: e for e in lb.panel()}
    out = [_monthly(f"GOV10-{c}", "GOV9", "rates", p[f"GOV10-{c}"].returns, 1) for c in GOV]
    eur = [(d, x) for d, x in p["FX-EUR"].returns if d > FLOAT_FROM]
    spot, _ = lb.fx_spot_month_end("EUR")
    out.append(_monthly("FX-EUR", "FX9", "fx", eur, 1, sig=lx.simple_returns(spot)))
    out += [_monthly(n, "COM8", "commodity", p[n].returns, 2) for n in PPI]
    gp = long_gold.parse(_gold_lines(long_gold.latest()))
    gr = [(d, x - 1.0) for d, x in long_gold.returns(gp, since=GOLD_FROM)]
    out.append(_monthly("GOLD", "COM8", "commodity", gr, 1))
    return out


def load_nonequity() -> list[Spec]:
    specs = load_bonds() + load_fx_daily() + load_monthly()
    order = {g: i for i, g in enumerate(GROUPS)}
    return sorted(specs, key=lambda s: order[s.group])


# --------------------------------------------------------------------------- engine runs


def run_specs(
    specs: list[Spec],
    cost_mult: float = 1.0,
    spot_signal: bool = False,
    gov_gap: int | None = None,
) -> list[qc.Mkt]:
    out = []
    for s in specs:
        cost, reset = COST[s.cls] * cost_mult, RESET[s.cls] * cost_mult
        use_sig = spot_signal and s.cls == "fx"
        if s.freq == "w":
            assert s.d is not None and s.px_ret is not None and s.av is not None
            if int(s.d[-1]) > LAST.toordinal():
                raise AssertionError(f"{s.name}: a day after {LAST}")
            out.append(
                qc.run_weekly(
                    s.name,
                    s.group,
                    s.d,
                    s.px_ret,
                    s.av,
                    cost,
                    reset,
                    px_sig=s.px_sig if use_sig else None,
                )
            )
        else:
            assert s.months is not None and s.r_ret is not None
            gap = gov_gap if (gov_gap is not None and s.group == "GOV9") else s.gap
            out.append(
                qc.run_monthly(
                    s.name,
                    s.group,
                    s.months,
                    s.r_ret,
                    gap,
                    cost,
                    reset,
                    r_sig=s.r_sig if use_sig else None,
                )
            )
    return out


def load_equity() -> list[qc.Mkt]:
    import pooled1 as p1

    return [qc.from_pooled1(m) for m in p1.run_all(p1.load_all(), quiet=True)]


def randomise(specs: list[Spec], seed: int = 12345, matched: bool = False) -> list[Spec]:
    """Plumbing: i.i.d. normal log returns, zero drift, class volatility (seed 12345).
    matched (drift-matched null): each series' own mean and sd of log excess returns."""
    rng = np.random.default_rng(seed)
    out = []
    for s in specs:
        if s.freq == "w":
            assert s.px_ret is not None
            if matched:
                real = np.diff(np.log(s.px_ret))
                lr = rng.normal(real.mean(), real.std(), len(s.px_ret))
            else:
                lr = rng.normal(0.0, RAND_VOL[s.cls] / math.sqrt(252), len(s.px_ret))
            lr[0] = 0.0
            px = 100 * np.exp(np.cumsum(lr))
            out.append(replace(s, px_ret=px, px_sig=px))
        else:
            assert s.r_ret is not None
            if matched:
                real = np.log1p(s.r_ret)
                lr = rng.normal(real.mean(), real.std(), len(s.r_ret))
            else:
                lr = rng.normal(0.0, RAND_VOL[s.cls] / math.sqrt(12), len(s.r_ret))
            r = np.expm1(lr)
            out.append(replace(s, r_ret=r, r_sig=r))
    return out


# --------------------------------------------------------------------------- analysis


def masks(c: qc.Cells) -> dict[str, np.ndarray]:
    g = np.array(c.groups)
    eq = np.array([x.startswith("EQ-") for x in c.groups])
    judged = np.isin(g, JUDGED)
    out = {"judged": judged, **{k: g == k for k in GROUPS}, "nonequity": ~eq}
    if eq.any():
        out |= {"equity": eq, "combined": eq | judged, "everything": np.ones(len(g), bool)}
    return out


def pre_masks(c: qc.Cells, sel: np.ndarray, base: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    n = c.S[0][0][:, sel].sum(-1)
    need = np.array([PRE_MIN[f] for f in c.freq])
    ok = n >= need
    return {k: v & ok for k, v in base.items() if k in ("judged", "combined", "equity")}


def summarise(c: qc.Cells, quick: bool = False) -> dict[str, Any]:
    base = masks(c)
    bt = qc.bootstrap(c, base, BLOCK, DRAWS, SEED)
    sel = c.cal < qc.month_index(PRE.toordinal())
    pm = pre_masks(c, sel, base)
    bt_pre = qc.bootstrap(c, pm, BLOCK, DRAWS, SEED, sel=sel)
    chk = (
        {}
        if quick
        else {
            b: qc.bootstrap(
                c, {k: base[k] for k in base if k in ("judged", "combined")}, b, DRAWS, SEED
            )
            for b in CHECK_BLOCKS
        }
    )
    res: dict[str, Any] = {"variants": {}}
    for v, name in enumerate(qc.VARIANTS):
        sets = {k: vars(qc.pooled(bt, k, v)) for k in base}
        pre = {k: vars(qc.pooled(bt_pre, k, v)) for k in pm}
        r: dict[str, Any] = {
            "sets": sets,
            "pre1994": pre,
            "pre1994_markets": {k: int(m.sum()) for k, m in pm.items()},
            "se_block": {
                str(b): {k: qc.pooled(x, k, v).se for k in x.sets} for b, x in chk.items()
            },
            "corr_d": {k: qc.mean_pair_corr(bt, v, base[k]) for k in ("judged", *GROUPS)},
        }
        gpos = sum(1 for g in JUDGED if sets[g]["D"] > 0)
        r["groups_pos"] = gpos
        r["verdict"] = qc.verdict(
            qc.pooled(bt, "judged", v), gpos, pre["judged"]["D"] > 0, Z_BAR, Z_PROJ, KILL_HI
        )
        com_pos = int(sets["COM8"]["n_pos"])
        r["verdict_com"] = qc.verdict(qc.pooled(bt, "COM8", v), 2, True, Z_BAR, Z_PROJ, KILL_HI)
        r["com_pos"] = com_pos
        r["mde80"] = (Z_BAR + 0.8416) * sets["judged"]["se"]
        r["mde80_proj"] = (Z_PROJ + 0.8416) * sets["judged"]["se"]
        if "combined" in base:
            r["balanced"] = qc.balanced(bt, "equity", "judged", v)
            r["combined_mde80"] = (Z_BAR + 0.8416) * sets["combined"]["se"]
            r["reading"] = combined_reading(r)
        res["variants"][name] = r
    res["d"] = {name: [float(x) for x in bt.d[v]] for v, name in enumerate(qc.VARIANTS)}
    res["names"], res["groups"], res["freq"] = c.names, c.groups, c.freq
    return res


def combined_reading(r: dict[str, Any]) -> str:
    s = r["sets"]
    c, dn, de = s["combined"], s["judged"]["D"], s["equity"]["D"]
    if c["z"] >= Z_BAR and de > 0 and dn > 0 and r["pre1994"]["combined"]["D"] > 0:
        return (
            "selectable candidate (own card first)"
            if c["z"] >= Z_PROJ
            else "real small edge across asset classes"
        )
    if r["verdict"] == "killed":
        return "equity-only at best"
    if dn <= 0:
        return "lean not confirmed"
    return "unsettled, leaning positive"


def point_D(markets: list[qc.Mkt]) -> dict[str, dict[str, float]]:
    c = qc.cells(markets)
    d = qc.diffs(c, [x.sum(-1) for x in c.S])
    base = masks(c)
    return {
        name: {k: float(np.nanmean(d[v, m])) for k, m in base.items()}
        for v, name in enumerate(qc.VARIANTS)
    }


def market_rows(markets: list[qc.Mkt], d: dict[str, list[float]]) -> list[dict[str, Any]]:
    rows = []
    for i, m in enumerate(markets):
        rows.append(
            {
                "name": m.name,
                "group": m.group,
                "freq": m.freq,
                "from": str(date.fromordinal(int(m.periods[0]))),
                "to": str(date.fromordinal(int(m.periods[-1]))),
                "periods": len(m.periods),
                "stats": {r: qc.stats(m, r) for r in qc.RULES},
                "d": {v: d[v][i] for v in qc.VARIANTS},
            }
        )
    return rows


# --------------------------------------------------------------------------- report


def f3(x: float) -> str:
    return f"{x:+.3f}"


def cell(p: dict[str, Any]) -> str:
    return f"{f3(p['D'])} ({p['se']:.3f}, z {p['z']:+.2f})"


def report(res: dict[str, Any], title: str) -> str:
    combined = "combined" in next(iter(res["variants"].values()))["sets"]
    L = [
        f"# {title}",
        "",
        "Card: `cards/pooled-2.md`. Code: `lib/pooled2.py`, `lib/pooled2_core.py` (rules from "
        "`lib/pooled1_core.py`). d = Sharpe(variant) - Sharpe(`tsmom12`) on the same series and "
        "periods (weekly Sharpe x sqrt 52 for daily series, monthly x sqrt 12 otherwise), excess "
        "over the US bill (commodities: spot); D = equal-weight mean over markets; SE from a joint "
        f"circular block bootstrap of calendar months ({BLOCK}-month blocks, {DRAWS} draws, seed "
        f"{SEED}). Costs a side: bonds 2 bps, currencies 3, commodities 10. Bars: z >= {Z_BAR} "
        f"(real small edge, with D > 0 in 2 of 3 judged groups and before 1994); project z >= "
        f"{Z_PROJ}; killed if the 95% upper end < +{KILL_HI} or z <= -{Z_BAR}.",
        "",
        "## Judged pool: bonds and currencies (21 markets)",
        "",
        "| Variant | D | SE | z | 95% (normal) | 95% (percentile) | d > 0 | USB3 | GOV9 | FX9 | "
        "Before 1994 (markets) | SE 3 / 24-month blocks | Edge seen 80% (z 2.50 / 4.70) | "
        "Mean corr of d | Verdict |",
        "|---|---:|---:|---:|---|---|---:|---|---|---|---|---|---|---:|---|",
    ]
    for v, r in res["variants"].items():
        a = r["sets"]["judged"]
        pre = r["pre1994"]["judged"]
        sb = r["se_block"]
        sbs = f"{sb['3']['judged']:.3f} / {sb['24']['judged']:.3f}" if sb else "-"
        L.append(
            f"| `{v}` | {f3(a['D'])} | {a['se']:.3f} | {a['z']:+.2f} | {f3(a['lo'])}..{f3(a['hi'])}"
            f" | {f3(a['plo'])}..{f3(a['phi'])} | {a['n_pos']} of {a['n']} | "
            + " | ".join(cell(r["sets"][g]) for g in JUDGED)
            + f" | {cell(pre)}; {r['pre1994_markets']['judged']} | {sbs} | +{r['mde80']:.2f} / "
            f"+{r['mde80_proj']:.2f} | {r['corr_d']['judged']:+.2f} | **{r['verdict']}** |"
        )
    L += [
        "",
        "## Commodities, spot (8 markets; shown, not judged)",
        "",
        "| Variant | D (SE, z) | 95% | d > 0 | Verdict by the same bars |",
        "|---|---|---|---:|---|",
    ]
    for v, r in res["variants"].items():
        a = r["sets"]["COM8"]
        L.append(
            f"| `{v}` | {cell(a)} | {f3(a['lo'])}..{f3(a['hi'])} | {a['n_pos']} of {a['n']} "
            f"| {r['verdict_com']} |"
        )
    L += [
        "",
        "All 29 non-equity: "
        + "; ".join(f"`{v}` {cell(r['sets']['nonequity'])}" for v, r in res["variants"].items()),
        "",
    ]
    if combined:
        L += [
            "## Combined with pooled-1's 41 equity markets (re-run with pooled-1's code)",
            "",
            "| Variant | Equity (41) | Non-equity judged (21) | Combined (62) | Combined 95% | "
            "Combined before 1994 (markets) | Class-balanced (D, SE) | Edge seen 80% (z 2.50) | "
            "Everything (70) | Reading |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for v, r in res["variants"].items():
            s = r["sets"]
            bd, bs = r["balanced"]
            L.append(
                f"| `{v}` | {cell(s['equity'])} | {cell(s['judged'])} | {cell(s['combined'])} | "
                f"{f3(s['combined']['lo'])}..{f3(s['combined']['hi'])} | "
                f"{cell(r['pre1994']['combined'])}; {r['pre1994_markets']['combined']} | "
                f"{f3(bd)} ({bs:.3f}, z {bd / bs:+.2f}) | +{r['combined_mde80']:.2f} | "
                f"{cell(s['everything'])} | **{r['reading']}** |"
            )
        L.append("")
    L += checks_table(res)
    L += [
        "## Per market",
        "",
        "| Market | Group | Freq | Scored from | Periods | `tsmom12` Sharpe | `e4` | `vt-own-70-x` "
        "| d `e4` | d `vt-own-70-x` | `tsmom12` max DD | Turnover `tsmom12` / `e4` |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for m in res["markets"]:
        st = m["stats"]
        L.append(
            f"| {m['name']} | {m['group']} | {m['freq']} | {m['from']} | {m['periods']} | "
            f"{st['tsmom12'][0]:.2f} | {st['e4'][0]:.2f} | {st['vt-own-70-x'][0]:.2f} | "
            f"{f3(m['d']['e4'])} | {f3(m['d']['vt-own-70-x'])} | {st['tsmom12'][2]:.0%} | "
            f"{st['tsmom12'][3]:.1f} / {st['e4'][3]:.1f} |"
        )
    return "\n".join(L) + "\n"


def checks_table(res: dict[str, Any]) -> list[str]:
    ck = res.get("checks")
    if not ck:
        return []
    L = [
        "## Checks (reported, not deciding; point D)",
        "",
        "| Check | Set | " + " | ".join(f"`{v}`" for v in qc.VARIANTS) + " |",
        "|---|---|" + "---:|" * len(qc.VARIANTS),
    ]
    for label, (setname, vals) in ck.items():
        L.append(f"| {label} | {setname} | " + " | ".join(f3(vals[v]) for v in qc.VARIANTS) + " |")
    nl = res.get("null")
    if nl:
        L += [
            "",
            f"## Drift-matched null ({NULL_REPS} i.i.d. walks with each series' own mean and sd)",
            "",
            "| Variant | Set | D | Null mean | Null 5% / 95% | D beyond drift | Reading |",
            "|---|---|---:|---:|---|---:|---|",
        ]
        for v in qc.VARIANTS:
            for s in ("judged", "COM8"):
                x = nl[v][s]
                L.append(
                    f"| `{v}` | {s} | {f3(x['D'])} | {f3(x['mean'])} | {f3(x['q5'])} / "
                    f"{f3(x['q95'])} | {f3(x['D'] - x['mean'])} | {x['reading']} |"
                )
    return [*L, ""]


# --------------------------------------------------------------------------- logging


def log_tries(res: dict[str, Any]) -> int:
    tries = RESEARCH / "tries.md"
    text = tries.read_text()
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"
    rows = []
    mk = res["markets"]
    allm = res["markets"] + res.get("equity_markets", [])
    tests = (
        ("nonequity-21", "judged", JUDGED),
        ("com-8", "COM8", ("COM8",)),
        ("combined-62", "combined", (*JUDGED, "EQ")),
    )
    for v, r in res["variants"].items():
        for tag, setname, groups in tests:
            if setname not in r["sets"]:
                continue
            a = r["sets"][setname]
            ms = [
                m
                for m in allm
                if m["group"] in groups or ("EQ" in groups and m["group"].startswith("EQ-"))
            ]
            verdict = {
                "judged": r["verdict"],
                "COM8": r["verdict_com"] + " (shown, not judged)",
                "combined": r.get("reading", "-"),
            }[setname]
            name = (
                f"{v}@pooled2-{tag} (pooled dSharpe vs tsmom12 {a['D']:+.3f}, SE {a['se']:.3f}"
                f", z {a['z']:+.2f}; {verdict})"
            )
            if f"| {IDEA} | {v}@pooled2-{tag} " in text:
                continue
            sh = float(np.mean([m["stats"][v][0] for m in ms]))
            first = min(m["from"] for m in ms)
            last = max(m["to"] for m in ms)
            rows.append(
                f"| {now} | {IDEA} | {name} | variant | train | {first} | {last} | "
                f"{sh:.2f} | - | - | - |\n"
            )
    for m in mk:
        for r in qc.RULES:
            tag = f"{r}@{m['group']}-{m['name']}"
            if f"| {IDEA} | {tag} |" in text:
                continue
            sh, tot, mdd, turn = m["stats"][r]
            ts = "-" if math.isnan(turn) else f"{turn:.2f}"
            rows.append(
                f"| {now} | {IDEA} | {tag} | robustness | train | {m['from']} | "
                f"{m['to']} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {ts} |\n"
            )
    with tries.open("a") as f:
        f.writelines(rows)
    return len(rows)


# --------------------------------------------------------------------------- main


def null_D(specs: list[Spec], reps: int) -> np.ndarray:
    out = np.zeros((len(qc.VARIANTS), 2, reps))
    for b in range(reps):
        pd = point_D(run_specs(randomise(specs, 1000 + b, matched=True)))
        for v, name in enumerate(qc.VARIANTS):
            out[v, 0, b], out[v, 1, b] = pd[name]["judged"], pd[name]["COM8"]
        print(f"  null {b + 1}/{reps}", file=sys.stderr, flush=True)
    return out


def main() -> None:
    t0 = time.time()
    specs = load_nonequity()
    for s in specs:
        print(f"  {s.name} ({s.group}, {s.freq})", file=sys.stderr)
    if "--random" in sys.argv:
        mk = run_specs(randomise(specs))
        c = qc.cells(mk)
        res = summarise(c)
        res["markets"] = market_rows(mk, res["d"])
        OUT_PLUMB.write_text(report(res, "pooled-2 plumbing run: random walks (not data)"))
        print(f"wrote {OUT_PLUMB} in {time.time() - t0:.0f}s")
        return
    mk = run_specs(specs)
    eq = load_equity()
    c = qc.cells(mk + eq)
    res = summarise(c)
    allrows = market_rows(mk + eq, res["d"])
    res["markets"], res["equity_markets"] = allrows[: len(mk)], allrows[len(mk) :]
    pt = point_D(mk)
    checks: dict[str, tuple[str, dict[str, float]]] = {}
    for label, kw, sets in (
        ("costs x2", {"cost_mult": 2.0}, ("judged", "COM8")),
        ("FX signal on spot only", {"spot_signal": True}, ("judged", "FX9")),
        ("GOV10 gap 3 (strict OECD publication)", {"gov_gap": 3}, ("judged", "GOV9")),
    ):
        pdx = point_D(run_specs(specs, **kw))
        for s in sets:
            checks[f"{label}" + ("" if s == sets[0] else f" ({s})")] = (
                s,
                {v: pdx[v][s] for v in qc.VARIANTS},
            )
    res["checks"] = checks
    reps = NULL_REPS if "--quick-null" not in sys.argv else 5
    nd = null_D(specs, reps)
    res["null"] = {}
    for v, name in enumerate(qc.VARIANTS):
        res["null"][name] = {}
        for k, s in enumerate(("judged", "COM8")):
            q5, q95 = (float(x) for x in np.percentile(nd[v, k], [5, 95]))
            D = pt[name][s]
            verdict = res["variants"][name]["verdict" if s == "judged" else "verdict_com"]
            if verdict in ("real small edge", "selectable candidate") and q95 >= D:
                reading = "exposure, not timing"
            elif verdict == "killed" and q5 <= D <= q95:
                reading = "no timing effect either way"
            else:
                reading = "-"
            res["null"][name][s] = {
                "D": D,
                "mean": float(nd[v, k].mean()),
                "q5": q5,
                "q95": q95,
                "reading": reading,
            }
    res["runtime_s"] = time.time() - t0
    OUT.write_text(report(res, "pooled-2: e4 and vt-own-70-x vs tsmom12 outside equities"))
    OUT.with_suffix(".json").write_text(json.dumps(res, indent=1) + "\n")
    print(f"wrote {OUT} in {time.time() - t0:.0f}s")
    if "--log" in sys.argv:
        print(f"tries.md: {log_tries(res)} rows")


if __name__ == "__main__":
    main()
