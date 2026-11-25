"""e4-indep-1: `e4` against `tsmom12` on monthly stock data never used for `e4`.

Card: research/cards/e4-indep-1.md (pushed before any `e4` number on these series). Rules and
statistic are pooled-2's frozen monthly code, unchanged (`pooled2_core.run_monthly`, `cells`,
`bootstrap`, `pooled`). Data: `e4indep1_data`.

    GRIMSTRADE_DATA=~/data/grimstrade uv run --with xlrd python research/lib/e4indep1.py fetch
    ...                                                                         power
    ...                                                                         run

`power` uses only already-scored data (Shiller US 1927-2025, the US market of pooled-1) and
prints standard errors, never a difference. `run` writes results/e4-indep-1.{md,json}.
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e4indep1_data as ed  # noqa: E402
import long_bond  # noqa: E402
import pooled2_core as qc  # noqa: E402

RESEARCH = Path(__file__).resolve().parents[1]
RULES2 = ("tsmom12", "e4")  # only these two are read; run_monthly also builds vt-own (unread)
COST = 0.0002  # pooled-1's index cost, per side, share of the position changed
COST_HI = 0.0050  # check: 50 bps per side
MIN_SCORED = 48  # a segment counts with at least 48 scored months
BLOCK, DRAWS, SEED = 12, 2000, 0
Z_PASS = 1.645  # one-sided 5%
D41, SE41 = 0.063, 0.041  # pooled-1's 41 stock markets (#142)


@dataclass
class Spec:
    market: str
    group: str
    source: str  # "shiller", "shiller-tr", "nber:<id>", "french:<member>"
    gap: int
    lo: date | None = None
    hi: date | None = None


PRIMARY = [
    Spec("US", "P4", "shiller", 1, None, ed.CUT),
    Spec("GB", "P4", "nber:m11012a", 0, None, ed.CUT),
    Spec("GB", "P4", "nber:m11012b", 0, None, ed.CUT),
    Spec("GB", "P4", "nber:m11012c", 0, None, ed.CUT),
    Spec("DE", "P4", "nber:m11023a", 1, None, ed.CUT),
    Spec("DE", "P4", "nber:m11023b", 1, None, ed.CUT),
    Spec("FR", "P4", "nber:m11024", 0, None, date(1914, 7, 1)),
    Spec("FR", "P4", "nber:m11024", 1, date(1919, 1, 1), ed.CUT),
]
SECONDARY = [
    Spec("DK", "N5", "french:Denmark.Dat", 0),
    Spec("FI", "N5", "french:Finland.Dat", 0),
    Spec("IE", "N5", "french:Ireland.Dat", 0),
    Spec("NO", "N5", "french:Norway.Dat", 0),
    Spec("SE", "N5", "french:Sweden.Dat", 0),
]


def _k(x: date | None) -> int | None:
    return None if x is None else ed.mi(x.year, x.month)


def load_segs(root: Path, s: Spec, gap_all: int | None = None) -> list[ed.Seg]:
    gap = s.gap if gap_all is None else gap_all
    lo, hi = _k(s.lo), _k(s.hi)
    if s.source.startswith("french:"):
        rets = ed.french_country(root, s.source.split(":", 1)[1])
        return ed.returns_segments(s.market, rets, gap, lo, hi)
    if s.source == "shiller":
        lv = ed.shiller_prices(root, ed.month_of(hi) if hi is not None else ed.LAST)
    elif s.source == "shiller-tr":
        lv = ed.shiller_total(root, ed.month_of(hi) if hi is not None else ed.LAST)
    else:
        lv = ed.nber(root, s.source.split(":", 1)[1])
    # levels: the first return of a run needs the level of the month before `lo`
    lo_lv = None if lo is None else lo - 1
    return [
        ed.seg_returns(s.market, run, gap) for run in ed.segments(lv, lo_lv, hi) if len(run) > 1
    ]


def scored(seg: ed.Seg) -> int:
    return len(seg.r) - 12 - seg.gap


def build(
    root: Path, specs: Sequence[Spec], cost: float = COST, gap_all: int | None = None
) -> tuple[list[qc.Mkt], list[dict[str, object]]]:
    """One `Mkt` per market: its counted segments run separately and concatenated."""
    by: dict[str, list[qc.Mkt]] = {}
    groups: dict[str, str] = {}
    log: list[dict[str, object]] = []
    for s in specs:
        for seg in load_segs(root, s, gap_all):
            n = scored(seg)
            row: dict[str, object] = {
                "market": s.market,
                "source": s.source,
                "first": seg.months[0].isoformat()[:7],
                "last": seg.months[-1].isoformat()[:7],
                "returns": len(seg.r),
                "gap": seg.gap,
                "scored": max(n, 0),
                "counted": n >= MIN_SCORED,
            }
            log.append(row)
            if n < MIN_SCORED:
                continue
            m = qc.run_monthly(s.market, s.group, seg.months, np.array(seg.r), seg.gap, cost)
            by.setdefault(s.market, []).append(m)
            groups[s.market] = s.group
    out = []
    for name, ms in by.items():
        m = qc.Mkt(name, groups[name], "m", np.concatenate([x.periods for x in ms]))
        for r in RULES2:
            m.rets[r] = np.concatenate([x.rets[r] for x in ms])
        out.append(m)
    return out, log


def span_years(root: Path, specs: Sequence[Spec]) -> dict[str, float]:
    """Scored years per market from the spans alone (no rule is run)."""
    out: dict[str, float] = {}
    for s in specs:
        for seg in load_segs(root, s):
            if scored(seg) >= MIN_SCORED:
                out[s.market] = out.get(s.market, 0.0) + scored(seg) / 12
    return out


def sharpe(w: np.ndarray) -> float:
    sd = w.std()
    return float(w.mean() / sd * math.sqrt(12)) if sd > 0 else 0.0


def pooled_of(
    ms: Sequence[qc.Mkt], block: int = BLOCK, sel_years: tuple[int, int] | None = None
) -> dict[str, object]:
    c = qc.cells(ms, RULES2)
    sets = {"all": np.ones(len(ms), dtype=bool)}
    sel = None
    if sel_years is not None:
        yrs = c.cal // 12
        sel = (yrs >= sel_years[0]) & (yrs <= sel_years[1])
    bt = qc.bootstrap(c, sets, block, DRAWS, SEED, sel=sel)
    p = qc.pooled(bt, "all", 0)
    return {
        "D": p.D,
        "se": p.se,
        "z": p.z,
        "lo90": p.D - Z_PASS * p.se,
        "hi90": p.D + Z_PASS * p.se,
        "n_pos": p.n_pos,
        "n": p.n,
        "per_market": {nm: float(bt.d[0, i]) for i, nm in enumerate(c.names)},
    }


def reading(p: dict[str, object]) -> str:
    D, se, z = float(p["D"]), float(p["se"]), float(p["z"])  # type: ignore[arg-type]
    if z >= Z_PASS:
        return "confirmed (independent one-sided 5% test passed)"
    if D + Z_PASS * se < D41:
        return "contradicted (one-sided 95% upper bound below the 41-market +0.063)"
    return "not confirmed, not contradicted (too little power to tell)"


# ------------------------------------------------------------------- power (seen data only)


def power() -> None:
    from statistics import NormalDist

    root = long_bond.cache_root()
    spec = Spec("US-1927", "cal", "shiller", 1, date(1927, 7, 1), ed.LAST)
    ms, _ = build(root, [spec])
    m = ms[0]
    c = qc.cells(ms, RULES2)
    bt = qc.bootstrap(c, {"all": np.ones(1, dtype=bool)}, BLOCK, DRAWS, SEED)
    se_us = float(qc.pooled(bt, "all", 0).se)
    years = len(m.rets["e4"]) / 12
    rho = float(np.corrcoef(m.rets["e4"], m.rets["tsmom12"])[0, 1])
    sa, sb = sharpe(m.rets["e4"]), sharpe(m.rets["tsmom12"])
    jk = math.sqrt((2 - 2 * rho + (sa**2 + sb**2 - 2 * rho**2 * sa * sb) / 24) / years)
    print(f"calibration: Shiller US monthly, {years:.1f} years scored, gap 1, 2 bps")
    print(f"  bootstrap SE of d (12-month blocks): {se_us:.4f}; rho(e4, tsmom12) {rho:.3f}")
    print(f"  Jobson-Korkie-Memmel SE {jk:.4f}; k = {se_us / jk:.2f}")
    per_year = se_us * math.sqrt(years)
    nd = NormalDist()
    for pool, specs in (("P4 pre-1927", PRIMARY), ("N5 1975-2025", SECONDARY)):
        yrs = span_years(root, specs)
        print(f"  {pool}: scored years (spans only) { ({k: round(v, 1) for k, v in yrs.items()}) }")
        se_i = np.array([per_year / math.sqrt(y) for y in yrs.values()])
        M = len(se_i)
        for cc in (0.0, 0.3, 0.5):
            var = (np.sum(se_i**2) + cc * (np.sum(se_i) ** 2 - np.sum(se_i**2))) / M**2
            se = math.sqrt(var)
            pw = {dt: 1 - nd.cdf(Z_PASS - dt / se) for dt in (0.045, 0.063, 0.10)}
            print(
                f"  {pool}: c {cc:.1f}: SE {se:.4f}; power at D +0.045 {pw[0.045]:.2f}, "
                f"+0.063 {pw[0.063]:.2f}, +0.10 {pw[0.10]:.2f}; MDE80 {(Z_PASS + 0.8416) * se:.3f}"
            )


# ------------------------------------------------------------------- run


def run() -> None:
    root = long_bond.cache_root()
    res: dict[str, object] = {}
    ms, log = build(root, PRIMARY)
    res["segments"] = log
    res["years"] = {m.name: len(m.rets["e4"]) / 12 for m in ms}
    res["sharpe"] = {m.name: {r: sharpe(m.rets[r]) for r in RULES2} for m in ms}
    main = pooled_of(ms)
    main["reading"] = reading(main)
    res["primary"] = main
    checks: dict[str, object] = {}
    ms_g1, _ = build(root, PRIMARY, gap_all=1)
    checks["gap 1 everywhere"] = pooled_of(ms_g1)
    ms_c, _ = build(root, PRIMARY, cost=COST_HI)
    checks["cost 50 bps"] = pooled_of(ms_c)
    for b in (6, 24):
        checks[f"blocks {b}"] = pooled_of(ms, block=b)
    tr = [Spec("US", "P4", "shiller-tr", 1, None, ed.CUT)] + PRIMARY[1:]
    ms_tr, _ = build(root, tr)
    checks["US with dividends"] = pooled_of(ms_tr)
    for nm in [m.name for m in ms]:
        checks[f"without {nm}"] = pooled_of([m for m in ms if m.name != nm])
    checks["1867-1897"] = pooled_of(ms, sel_years=(1867, 1897))
    checks["1898-1927"] = pooled_of(ms, sel_years=(1898, 1927))
    res["checks"] = checks
    # meta (not deciding): inverse-variance with pooled-1's 41
    se = float(main["se"])  # type: ignore[arg-type]
    w1, w2 = 1 / SE41**2, 1 / se**2
    dm = (w1 * D41 + w2 * float(main["D"])) / (w1 + w2)  # type: ignore[arg-type]
    sm = math.sqrt(1 / (w1 + w2))
    res["meta_with_41"] = {"D": dm, "se": sm, "z": dm / sm}
    ms2, log2 = build(root, SECONDARY)
    sec = pooled_of(ms2)
    sec["reading"] = reading(sec)
    res["secondary"] = sec
    res["secondary_segments"] = log2
    res["secondary_years"] = {m.name: len(m.rets["e4"]) / 12 for m in ms2}
    res["secondary_sharpe"] = {m.name: {r: sharpe(m.rets[r]) for r in RULES2} for m in ms2}
    out = RESEARCH / "results" / "e4-indep-1.json"
    out.write_text(json.dumps(res, indent=1, default=str) + "\n")
    write_md(res)
    print(json.dumps({k: res[k] for k in ("primary", "meta_with_41", "secondary")}, indent=1))


def _row(name: str, p: dict[str, object]) -> str:
    f = {k: float(p[k]) for k in ("D", "se", "z", "lo90", "hi90")}  # type: ignore[arg-type]
    return (
        f"| {name} | {f['D']:+.3f} | {f['se']:.3f} | {f['z']:+.2f} | {f['hi90']:+.3f} | "
        f"{p['n_pos']}/{p['n']} |"
    )


def write_md(res: dict[str, object]) -> None:
    pr = res["primary"]
    assert isinstance(pr, dict)
    L = [
        "# e4-indep-1 results (generated by `research/lib/e4indep1.py run`; do not edit)",
        "",
        "D = equal-weight mean over markets of Sharpe(`e4`) - Sharpe(`tsmom12`), monthly, sqrt 12;",
        "SE = joint circular 12-month block bootstrap (2,000 draws, seed 0); hi90 = D + 1.645 SE.",
        "",
        "## Segments",
        "",
        "| Market | Source | First | Last | Returns | Gap | Scored | Counted |",
        "|---|---|---|---|---:|---:|---:|---|",
    ]
    for s in res["segments"] + res["secondary_segments"]:  # type: ignore[operator]
        L.append(
            f"| {s['market']} | {s['source']} | {s['first']} | {s['last']} | {s['returns']} | "
            f"{s['gap']} | {s['scored']} | {'yes' if s['counted'] else 'no'} |"
        )
    L += [
        "",
        "## Per market",
        "",
        "| Market | Years | tsmom12 | e4 | d |",
        "|---|---:|---:|---:|---:|",
    ]
    for key, pk in (("sharpe", "primary"), ("secondary_sharpe", "secondary")):
        sh = res[key]
        p = res[pk]
        yk = "years" if pk == "primary" else "secondary_years"
        assert isinstance(sh, dict) and isinstance(p, dict)
        for nm, v in sh.items():
            L.append(
                f"| {nm} | {res[yk][nm]:.1f} | {v['tsmom12']:+.3f} | {v['e4']:+.3f} | "  # type: ignore[index]
                f"{p['per_market'][nm]:+.3f} |"
            )
    L += [
        "",
        "## Pooled",
        "",
        "| Set | D | SE | z | hi90 | d > 0 |",
        "|---|---:|---:|---:|---:|---:|",
        _row("**P4 pre-1927 (deciding)**", pr),
    ]
    for k, v in res["checks"].items():  # type: ignore[attr-defined]
        L.append(_row(f"check: {k}", v))
    L.append(_row("N5 1975-2025 (secondary)", res["secondary"]))  # type: ignore[arg-type]
    mt = res["meta_with_41"]
    assert isinstance(mt, dict)
    L += [
        "",
        f"Primary reading: **{pr['reading']}**. Secondary reading: {res['secondary']['reading']}.",  # type: ignore[index]
        "",
        f"Meta with pooled-1's 41 (not deciding): D {mt['D']:+.3f}, SE {mt['se']:.3f}, "
        f"z {mt['z']:+.2f}.",
        "",
    ]
    (RESEARCH / "results" / "e4-indep-1.md").write_text("\n".join(L))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "fetch":
        ed.fetch(long_bond.cache_root())
    elif cmd == "power":
        power()
    else:
        run()
