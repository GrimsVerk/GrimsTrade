"""ownvol-indep-1: `own_vol_70` (pooled-2's monthly `vt-own-70-x`) against `tsmom12` on the
independent stock data of e4-indep-1 (four markets before 1927-07; five Nordic/Irish markets
as a secondary pool).

Card: research/cards/ownvol-indep-1.md (pushed before any own-vol number). Data and segment
rule: `e4indep1` (`PRIMARY`, `SECONDARY`, `load_segs`, `scored`, `MIN_SCORED`), unchanged.
Rules and statistic: `pooled2_core.run_monthly`, `cells`, `bootstrap`, `pooled`, unchanged.

    uv run --with xlrd python research/lib/ownvolindep1.py run

writes results/ownvol-indep-1.{md,json} and prints the tries.md rows (`rows`).
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e4indep1 as ei  # noqa: E402
import e4indep1_data as ed  # noqa: E402
import long_bond  # noqa: E402
import pooled2_core as qc  # noqa: E402

RESEARCH = Path(__file__).resolve().parents[1]
OV = "vt-own-70-x"
RULES2 = ("tsmom12", OV)  # variant index 0 = own-vol
D41, SE41 = 0.022, 0.016  # pooled-1's 41 stock markets (#142)
D110 = 0.06  # risk-menu-3's usual size (#110), shown only
WARM = 60  # scored months of a segment before sizing (36 sigma months + 24 sigmas), + gap


def mean_share(r_ret: np.ndarray, gap: int, cost: float) -> tuple[float, float]:
    """(mean planned own-vol share over scored months, mean share while `tsmom12` holds),
    recomputed with the same frozen calls `run_monthly` makes."""
    pos, start = qc.decide_monthly(r_ret, gap)
    p = pos["tsmom12"]
    net = p * r_ret - cost * np.abs(np.diff(p, prepend=0.0))
    _, plan = qc.own_vol_monthly(net, p, start, gap, qc.TARGET, qc.pc.RESET_COST)
    sh = np.array([plan.get(t, qc.TARGET) for t in range(start, len(r_ret))])
    held = p[start:] > 0
    return float(sh.mean()), float(sh[held].mean()) if held.any() else math.nan


def build(
    root: Path,
    specs: Sequence[ei.Spec],
    cost: float = ei.COST,
    gap_all: int | None = None,
    skip_warm: bool = False,
) -> tuple[list[qc.Mkt], dict[str, dict[str, float]]]:
    """`e4indep1.build` for (`tsmom12`, own-vol): one `Mkt` per market, its counted segments
    run separately by `run_monthly` and concatenated. `skip_warm` drops each segment's first
    WARM + gap scored months (the shown "sized months only" cell). Also the share summary."""
    by: dict[str, list[qc.Mkt]] = {}
    groups: dict[str, str] = {}
    shares: dict[str, list[tuple[float, float, int]]] = {}
    for s in specs:
        for seg in ei.load_segs(root, s, gap_all):
            n = ei.scored(seg)
            if n < ei.MIN_SCORED:
                continue
            r = np.array(seg.r)
            m = qc.run_monthly(s.market, s.group, seg.months, r, seg.gap, cost)
            a, h = mean_share(r, seg.gap, cost)
            shares.setdefault(s.market, []).append((a, h, n))
            if skip_warm:
                k = WARM + seg.gap
                if n - k < 1:
                    continue
                m = qc.Mkt(m.name, m.group, "m", m.periods[k:], {x: m.rets[x][k:] for x in m.rets})
            by.setdefault(s.market, []).append(m)
            groups[s.market] = s.group
    out = []
    for name, ms in by.items():
        m = qc.Mkt(name, groups[name], "m", np.concatenate([x.periods for x in ms]))
        for rr in RULES2:
            m.rets[rr] = np.concatenate([x.rets[rr] for x in ms])
        out.append(m)
    sh = {
        k: {
            "share": sum(a * n for a, _, n in v) / sum(n for *_, n in v),
            "share_held": sum(h * n for _, h, n in v) / sum(n for *_, n in v),
        }
        for k, v in shares.items()
    }
    return out, sh


def pooled_of(
    ms: Sequence[qc.Mkt], block: int = ei.BLOCK, sel_years: tuple[int, int] | None = None
) -> dict[str, object]:
    c = qc.cells(ms, RULES2)
    sets = {"all": np.ones(len(ms), dtype=bool)}
    sel = None
    if sel_years is not None:
        yrs = c.cal // 12
        sel = (yrs >= sel_years[0]) & (yrs <= sel_years[1])
    bt = qc.bootstrap(c, sets, block, ei.DRAWS, ei.SEED, sel=sel)
    p = qc.pooled(bt, "all", 0)
    return {
        "D": p.D,
        "se": p.se,
        "z": p.z,
        "hi90": p.D + ei.Z_PASS * p.se,
        "n_pos": p.n_pos,
        "n": p.n,
        "per_market": {nm: float(bt.d[0, i]) for i, nm in enumerate(c.names)},
    }


def reading(p: dict[str, object]) -> str:
    """The card's rule: confirmed at z >= 1.645; contradicted when D + 1.645 SE < +0.022."""
    D, se, z = float(p["D"]), float(p["se"]), float(p["z"])  # type: ignore[arg-type]
    hi = D + ei.Z_PASS * se
    if z >= ei.Z_PASS:
        out = "confirmed (independent one-sided 5% test passed)"
    elif hi < D41:
        out = "contradicted (one-sided 95% upper bound below the 41-market +0.022)"
    else:
        out = "not confirmed, not contradicted (too little power to tell)"
    return out + ("; upper bound below #110's +0.06" if hi < D110 else "; +0.06 not excluded")


def mstats(ms: Sequence[qc.Mkt]) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for m in ms:
        row: dict[str, object] = {
            "first": date.fromordinal(int(m.periods[0])).isoformat(),
            "last": date.fromordinal(int(m.periods[-1])).isoformat(),
            "years": len(m.periods) / 12,
        }
        for rr in RULES2:
            sh, tot, mdd, _ = qc.stats(m, rr)
            vol = float(m.rets[rr].std() * math.sqrt(12))
            row[rr] = {"sharpe": sh, "total": tot, "mdd": mdd, "vol": vol}
        out[m.name] = row
    return out


def run() -> dict[str, object]:
    root = long_bond.cache_root()
    res: dict[str, object] = {}
    ms, shares = build(root, ei.PRIMARY)
    res["stats"] = mstats(ms)
    res["shares"] = shares
    main = pooled_of(ms)
    main["reading"] = reading(main)
    res["primary"] = main
    checks: dict[str, dict[str, object]] = {}
    for nm in [m.name for m in ms]:
        checks[f"without {nm}"] = pooled_of([m for m in ms if m.name != nm])
    ms_w, _ = build(root, ei.PRIMARY, skip_warm=True)
    checks["sized months only"] = pooled_of(ms_w)
    ms_g1, _ = build(root, ei.PRIMARY, gap_all=1)
    checks["gap 1 everywhere"] = pooled_of(ms_g1)
    ms_c, _ = build(root, ei.PRIMARY, cost=ei.COST_HI)
    checks["cost 50 bps"] = pooled_of(ms_c)
    for b in (6, 24):
        checks[f"blocks {b}"] = pooled_of(ms, block=b)
    tr = [ei.Spec("US", "P4", "shiller-tr", 1, None, ed.CUT)] + ei.PRIMARY[1:]
    ms_tr, _ = build(root, tr)
    checks["US with dividends"] = pooled_of(ms_tr)
    checks["1867-1897"] = pooled_of(ms, sel_years=(1867, 1897))
    checks["1898-1927"] = pooled_of(ms, sel_years=(1898, 1927))
    res["checks"] = checks
    se = float(main["se"])  # type: ignore[arg-type]
    w1, w2 = 1 / SE41**2, 1 / se**2
    dm = (w1 * D41 + w2 * float(main["D"])) / (w1 + w2)  # type: ignore[arg-type]
    sm = math.sqrt(1 / (w1 + w2))
    res["meta_with_41"] = {"D": dm, "se": sm, "z": dm / sm}
    ms2, shares2 = build(root, ei.SECONDARY)
    sec = pooled_of(ms2)
    sec["reading"] = reading(sec)
    res["secondary"] = sec
    res["secondary_stats"] = mstats(ms2)
    res["secondary_shares"] = shares2
    (RESEARCH / "results" / "ownvol-indep-1.json").write_text(
        json.dumps(res, indent=1, default=str) + "\n"
    )
    write_md(res)
    return res


def _row(name: str, p: dict[str, object]) -> str:
    f = {k: float(p[k]) for k in ("D", "se", "z", "hi90")}  # type: ignore[arg-type]
    return (
        f"| {name} | {f['D']:+.3f} | {f['se']:.3f} | {f['z']:+.2f} | {f['hi90']:+.3f} | "
        f"{p['n_pos']}/{p['n']} |"
    )


def write_md(res: dict[str, object]) -> None:
    pr, sec = res["primary"], res["secondary"]
    assert isinstance(pr, dict) and isinstance(sec, dict)
    L = [
        "# ownvol-indep-1 results (generated by `research/lib/ownvolindep1.py run`; do not edit)",
        "",
        "D = equal-weight mean over markets of Sharpe(own-vol, `vt-own-70-x` monthly) -",
        "Sharpe(`tsmom12`), monthly, sqrt 12; SE = joint circular 12-month block bootstrap",
        "(2,000 draws, seed 0); hi90 = D + 1.645 SE (one-sided 95% upper bound).",
        "",
        "## Per market",
        "",
        "| Market | Years | tsmom12 Sharpe | own-vol Sharpe | d | tsmom12 vol / maxDD | "
        "own-vol vol / maxDD | Mean share (held) |",
        "|---|---:|---:|---:|---:|---|---|---:|",
    ]
    for sk, pk, hk in (
        ("stats", "primary", "shares"),
        ("secondary_stats", "secondary", "secondary_shares"),
    ):
        st, p, sh = res[sk], res[pk], res[hk]
        assert isinstance(st, dict) and isinstance(p, dict) and isinstance(sh, dict)
        for nm, v in st.items():
            a, b = v["tsmom12"], v[OV]
            L.append(
                f"| {nm} | {v['years']:.1f} | {a['sharpe']:+.3f} | {b['sharpe']:+.3f} | "
                f"{p['per_market'][nm]:+.3f} | {a['vol']:.1%} / {a['mdd']:.1%} | "
                f"{b['vol']:.1%} / {b['mdd']:.1%} | {sh[nm]['share']:.2f} "
                f"({sh[nm]['share_held']:.2f}) |"
            )
    L += [
        "",
        "## Pooled",
        "",
        "| Set | D | SE | z | hi90 | d > 0 |",
        "|---|---:|---:|---:|---:|---:|",
        _row("**P4 pre-1927 (deciding)**", pr),
    ]
    ch = res["checks"]
    assert isinstance(ch, dict)
    for k, v in ch.items():
        L.append(_row(f"check: {k}", v))
    L.append(_row("N5 1975-2025 (secondary)", sec))
    mt = res["meta_with_41"]
    assert isinstance(mt, dict)
    L += [
        "",
        f"Primary reading: **{pr['reading']}**. Secondary reading: {sec['reading']}.",
        "",
        f"Meta with pooled-1's 41 (not deciding): D {mt['D']:+.3f}, SE {mt['se']:.3f}, "
        f"z {mt['z']:+.2f}.",
        "",
    ]
    (RESEARCH / "results" / "ownvol-indep-1.md").write_text("\n".join(L))


def rows(res: dict[str, object], stamp: str) -> list[str]:
    """tries.md rows in e4-indep-1's format."""
    out: list[str] = []
    for pk, sk, tag, desc, lo in (
        (
            "primary",
            "stats",
            "P4",
            "P4 pre-1927 stock markets US/GB/DE/FR, monthly, never scored for own-vol, DECIDING",
            "1868-08-01",
        ),
        (
            "secondary",
            "secondary_stats",
            "N5",
            "N5 DK/FI/IE/NO/SE French country files 1975-2025, new markets but years overlap "
            "the 41, secondary",
            "1976-01-01",
        ),
    ):
        p, st = res[pk], res[sk]
        assert isinstance(p, dict) and isinstance(st, dict)
        hi = "2025-10-01" if tag == "N5" else "1927-06-01"
        sh = float(np.mean([v[OV]["sharpe"] for v in st.values()]))
        out.append(
            f"| {stamp} | ownvol-indep-1 | own_vol_70@indep-{tag} ({desc}; pooled dSharpe vs "
            f"tsmom12 {p['D']:+.3f}, SE {p['se']:.3f}, z {p['z']:+.2f}, one-sided 95% upper "
            f"{p['hi90']:+.3f}, d>0 in {p['n_pos']}/{p['n']}; {p['reading']}) | variant | train | "
            f"{lo} | {hi} | {sh:.2f} | - | - | - |"
        )
        for nm, v in st.items():
            for rr, lab in (("tsmom12", "tsmom12"), (OV, "own_vol_70")):
                x = v[rr]
                out.append(
                    f"| {stamp} | ownvol-indep-1 | {lab}@indep-{tag}-{nm} | robustness | train | "
                    f"{v['first']} | {v['last']} | {x['sharpe']:.2f} | {x['total']:+.1%} | "
                    f"{x['mdd']:.1%} | - |"
                )
        if tag == "P4":
            ch = res["checks"]
            assert isinstance(ch, dict)
            for k, c in ch.items():
                out.append(
                    f"| {stamp} | ownvol-indep-1 | own_vol_70@indep-P4-check-"
                    f"{k.replace(' ', '-')} (pooled dSharpe vs tsmom12 {c['D']:+.3f}, SE "
                    f"{c['se']:.3f}, z {c['z']:+.2f}, one-sided 95% upper {c['hi90']:+.3f}, "
                    f"d>0 in {c['n_pos']}/{c['n']}) | robustness | train | 1868-08-01 | "
                    f"1927-06-30 | - | - | - | - |"
                )
    return out


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: r[k] for k in ("primary", "meta_with_41", "secondary")}, indent=1))
    if len(sys.argv) > 1 and sys.argv[1] == "rows":
        print("\n".join(rows(r, sys.argv[2] if len(sys.argv) > 2 else "")))
