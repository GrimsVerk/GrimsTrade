"""vm-style-1: DMU (JF 2024) market-volatility management of xs-century-1's book, run once.

    GRIMSTRADE_DATA=<cache> uv run python -I research/lib/vm_style_run.py

Card: research/cards/vm-style-1.md. Reads only the cache (through xs_century_run's loaders plus
the Ken French daily factor files); nothing after 2025-10-31. Writes
research/results/vm-style-1.md (statistics only) and appends rows to research/tries.md the
moment the runs are scored.
"""

from __future__ import annotations

import math
import sys
import zipfile
from collections.abc import Mapping
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "src"))
import vm_style as vm  # noqa: E402
import xs_century as xc  # noqa: E402
import xs_century_run as xr  # noqa: E402
from macro import cache_root  # noqa: E402

IDEA = "vm-style-1"
LAST_DAY = date(2025, 10, 31)
PAPER = (date(1977, 1, 1), date(2021, 1, 1))  # DMU's out-of-sample window = in-paper
KAPPA_US, KAPPA_BF = 0.005, 0.0005
BAR, ONC = 4.70, 3.26
RESULT = REPO / "research" / "results" / "vm-style-1.md"
TRIES = REPO / "research" / "tries.md"
US = ("US-value(HML)", "US-mom(UMD)")

M = dict[date, float]
Full = dict[str, dict[date, tuple[float, float, float]]]


def french_daily(fname: str, cols: list[str]) -> dict[str, list[tuple[date, float]]]:
    with zipfile.ZipFile(cache_root() / xr.FRENCH / fname) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    out: dict[str, list[tuple[date, float]]] = {c: [] for c in cols}
    header: list[str] | None = None
    for line in text.splitlines():
        cells = [x.strip() for x in line.split(",")]
        if header is None:
            if len(cells) > 1 and cells[0] == "" and all(c in cells for c in cols):
                header = cells
            continue
        if len(cells[0]) != 8 or not cells[0].isdigit():
            if any(out[c] for c in cols):
                break
            continue
        d = date(int(cells[0][:4]), int(cells[0][4:6]), int(cells[0][6:]))
        if d > LAST_DAY:
            continue
        for c in cols:
            v = float(cells[header.index(c)])
            if v > -99.0:
                out[c].append((d, v / 100.0))
    return out


def full_sleeves(data: Mapping[str, object], *, gross: bool, umd_cost: float) -> Full:
    """xs-century-1's eight sleeves with (net, gross scaled, raw) kept: the same calls as
    xs_century_run.build (checked against it in main)."""
    out: Full = {}
    hml, umd = data["hml"], data["umd"]
    assert isinstance(hml, dict) and isinstance(umd, dict)
    b = 0.0 if gross else xr.BORROW
    out[US[0]] = xc.factor_sleeve(hml, 0.0 if gross else xr.HML_C, b)
    out[US[1]] = xc.factor_sleeve(umd, 0.0 if gross else umd_cost, b)
    br, y10, y3 = data["bonds"]  # type: ignore[misc]
    cb = 0.0 if gross else xr.COST["bond"]
    bsig = {
        "bond-value": lambda a, t: xc.yield_change_value(y10[a], t, xr.BOND_LAG),
        "bond-mom": lambda a, t: xc.momentum(br[a], t, max(2, xr.BOND_LAG)),
        "bond-carry": lambda a, t: xc.spread_value(y10[a], y3[a], t, xr.BOND_LAG),
    }
    for k, fn in bsig.items():
        out[k] = xc.constructed_sleeve(xr.signals(br, fn), br, cb)
    fr, spot, frate, usr = data["fx"]  # type: ignore[misc]
    cf = 0.0 if gross else xr.COST["fx"]
    fsig = {
        "fx-value": lambda a, t: xc.reversal_value(spot[a], t, xr.FX_SPOT_LAG),
        "fx-mom": lambda a, t: xc.momentum(fr[a], t, xr.FX_SPOT_LAG),
        "fx-carry": lambda a, t: xc.spread_value(frate[a], usr, t, xr.RATE_LAG),
    }
    for k, fn in fsig.items():
        out[k] = xc.constructed_sleeve(xr.signals(fr, fn), fr, cf)
    return {k: {t: v for t, v in s.items() if t <= xr.LAST} for k, s in out.items()}


def parts(full: Full, gross: bool) -> tuple[dict[str, M], dict[str, M], dict[str, M]]:
    """(return used, vol scale s, raw unscaled) per sleeve."""
    ret, scale, raw = {}, {}, {}
    for k, s in full.items():
        ret[k] = {t: (v[1] if gross else v[0]) for t, v in s.items()}
        raw[k] = {t: v[2] for t, v in s.items()}
        sc: M = {}
        prev = None
        for t in sorted(s):
            g, r = s[t][1], s[t][2]
            x = g / r if abs(r) > 1e-14 else prev
            sc[t] = float(x if x is not None else 1.0)
            prev = sc[t]
        scale[k] = sc
    return ret, scale, raw


def in_paper(m: date) -> bool:
    return PAPER[0] <= m < PAPER[1]


def arrays(b: M, t: M, keep: object = None) -> tuple[np.ndarray, np.ndarray, list[date]]:
    ms = sorted(m for m in set(b) & set(t) if keep is None or keep(m))  # type: ignore[operator]
    return np.array([b[m] for m in ms]), np.array([t[m] for m in ms]), ms


def tries_row(variant: str, kind: str, ms: list[date], r: np.ndarray, now: str) -> str:
    eq = np.cumprod(1.0 + r)
    tot, dd = float(eq[-1] - 1.0), float(1.0 - (eq / np.maximum.accumulate(eq)).min())
    last = xc.add_months(ms[-1], 1)
    to = date.fromordinal(last.toordinal() - 1)
    return (
        f"| {now} | {IDEA} | {variant} | {kind} | train | {ms[0].isoformat()} | "
        f"{to.isoformat()} | {vm.sharpe(r):.2f} | {tot * 100:+.1f}% | {dd * 100:.1f}% | - |"
    )


def main() -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    mkt_rf, rf, hml, umd = xr.us_stocks()
    data: dict[str, object] = {"hml": hml, "umd": umd, "bonds": xr.bonds(), "fx": xr.currencies()}
    tm = xr.tsmom_market(mkt_rf, rf)
    book, xs_sleeves = xr.build(data)

    d3 = french_daily("F-F_Research_Data_Factors_daily_CSV.zip", ["Mkt-RF", "HML", "RF"])
    dm = french_daily("F-F_Momentum_Factor_daily_CSV.zip", ["Mom"])
    rfd = dict(d3["RF"])
    mkt_sd = vm.realised_sd([(d, r + rfd[d]) for d, r in d3["Mkt-RF"] if d in rfd])
    own_sd_us = {US[0]: vm.realised_sd(d3["HML"]), US[1]: vm.realised_sd(dm["Mom"])}

    def run(
        gross: bool = False, umd_cost: float = xr.UMD_C, k_us: float = KAPPA_US, mode: str = "cmv"
    ) -> tuple[M, dict[date, tuple[float, float, float]], dict[date, dict[str, float]]]:
        full = full_sleeves(data, gross=gross, umd_cost=umd_cost)
        ret, scale, raw = parts(full, gross)
        if not gross and umd_cost == xr.UMD_C:
            for k in ret:  # same sleeves as xs-century-1's primary
                assert all(abs(ret[k][t] - xs_sleeves[k][t]) < 1e-15 for t in ret[k]), k
        kap = {k: (0.0 if gross else (k_us if k in US else KAPPA_BF)) for k in ret}
        cond: dict[str, M] | None
        if mode == "umv":
            cond = None
        elif mode == "own":
            cond = {}
            for k in ret:
                sd = own_sd_us[k] if k in US else vm.trailing_sd(raw[k], 6)
                cond[k] = vm.conditioner(sd, 1.0)
        else:
            z = vm.conditioner(mkt_sd, 2.0 if mode == "var" else 1.0)
            cond = dict.fromkeys(ret, z)
        out, th = vm.walk(ret, scale, kap, cond)
        return {t: v[0] for t, v in out.items()}, out, th

    specs = {
        "CMV": ("CMV (primary: theta = a + b / market vol)", "variant", {}),
        "UMV": ("UMV (control: b = 0)", "variant", {"mode": "umv"}),
        "OWN": ("own-vol twin (theta = a + b / own vol)", "variant", {"mode": "own"}),
        "R1": ("R1 CMV gross", "robustness", {"gross": True}),
        "R1u": ("R1 UMV gross", "robustness", {"gross": True, "mode": "umv"}),
        "R2": ("R2 CMV UMD 0.34%/mo", "robustness", {"umd_cost": xr.UMD_C_MIT}),
        "R2u": ("R2 UMV UMD 0.34%/mo", "robustness", {"umd_cost": xr.UMD_C_MIT, "mode": "umv"}),
        "R3a": ("R3a CMV kappa US 0.25%", "robustness", {"k_us": 0.0025}),
        "R3b": ("R3b CMV kappa US 1.0%", "robustness", {"k_us": 0.01}),
        "R4": ("R4 CMV market variance (1 / sigma^2)", "robustness", {"mode": "var"}),
    }
    res: dict[str, tuple[M, dict[date, tuple[float, float, float]], dict]] = {}  # type: ignore[type-arg]
    for key, (_, _, kw) in specs.items():
        res[key] = run(**kw)  # type: ignore[arg-type]
    cmv = res["CMV"][0]
    first = min(cmv)
    oos = {m for m in cmv}
    series: dict[str, M] = {k: v[0] for k, v in res.items()}
    series["BOOK"] = {m: v for m, v in book.items() if m in oos}
    samples = {
        "full": lambda m: m >= first,
        "out-of-paper": lambda m: m >= first and not in_paper(m),
        "in-paper 1977-2020": in_paper,
        "pre 1939-1976": lambda m: first <= m < PAPER[0],
        "post 2021-2025": lambda m: m >= PAPER[1],
    }
    sc: dict[tuple[str, str], dict[str, float]] = {}
    for key in ["CMV", "UMV", "OWN", "BOOK", *[k for k in specs if k.startswith("R")]]:
        for sn, f in samples.items():
            r, x, ms = arrays(series[key], tm, f)
            draws = xc.DRAWS if sn in ("full", "out-of-paper") else 200
            sc[(key, sn)] = xc.score(r, x, draws) | {"n_m": len(ms)}
    # the paper's own test: CMV on UMV (NW, xs-century lag rule) by sample
    paper_t = {}
    for sn, f in samples.items():
        r, x, _ = arrays(series["CMV"], series["UMV"], f)
        paper_t[sn] = xc.alpha(r, x)

    s_full, s_oop = sc[("CMV", "full")], sc[("CMV", "out-of-paper")]
    shp = {k: {sn: sc[(k, sn)]["sr_r"] for sn in samples} for k in ["CMV", "UMV", "OWN", "BOOK"]}
    c3 = shp["CMV"]["out-of-paper"] > shp["UMV"]["out-of-paper"]
    c4 = shp["CMV"]["out-of-paper"] > shp["OWN"]["out-of-paper"]
    if s_oop["z"] >= BAR and s_full["z"] >= BAR and c3 and c4:
        verdict = "PASS (informational)"
    elif ONC <= s_oop["z"] < BAR and c3:
        verdict = "NEAR"
    else:
        verdict = "FAIL"
    kills = {
        "K1 (CMV net Sharpe <= UMV, out of paper)": not c3,
        "K2 (CMV alpha z < unmanaged book's, out of paper)": s_oop["z"]
        < sc[("BOOK", "out-of-paper")]["z"],
        "K3 (own-vol twin Sharpe >= CMV, out of paper)": not c4,
    }

    # tries rows first
    rows = []
    r, x, ms = arrays(tm, tm, samples["full"])
    rows.append(
        tries_row(
            "tsmom12@us-mkt-monthly (comparator, above bills, monthly x sqrt12)",
            "baseline",
            ms,
            r,
            now,
        )
    )
    for key, label, kind in [
        ("BOOK", "xs-century-1 book (unmanaged, same months)", "baseline"),
        *[(k, v[0], v[1]) for k, v in specs.items()],
    ]:
        f, o = sc[(key, "full")], sc[(key, "out-of-paper")]
        v = (
            f"{label}: alpha vs tsmom12 full IR {f['ir']:+.2f} z {f['z']:+.2f}; out-of-paper "
            f"IR {o['ir']:+.2f} z {o['z']:+.2f} (monthly excess x sqrt12)"
        )
        rr, _, mm = arrays(series[key], tm, samples["full"])
        rows.append(tries_row(v, kind, mm, rr, now))
    for sn in ["out-of-paper", "in-paper 1977-2020", "pre 1939-1976", "post 2021-2025"]:
        s = sc[("CMV", sn)]
        rr, _, mm = arrays(series["CMV"], tm, samples[sn])
        v = (
            f"CMV sample {sn}: alpha vs tsmom12 IR {s['ir']:+.2f} z {s['z']:+.2f}; CMV-UMV "
            f"Sharpe {shp['CMV'][sn] - shp['UMV'][sn]:+.2f} (monthly excess x sqrt12)"
        )
        rows.append(tries_row(v, "robustness", mm, rr, now))
    with TRIES.open("a") as fh:
        fh.write("\n".join(rows) + "\n")

    L: list[str] = ["# vm-style-1 results (generated by research/lib/vm_style_run.py)\n"]
    L.append(
        f"Run {now} UTC. Card: `research/cards/vm-style-1.md`. Monthly excess returns, "
        "statistics only. Out of sample from "
        f"{first:%Y-%m} (first month after 120 months of HML/UMD history).\n"
    )
    L.append(
        f"**Verdict (card's rules): {verdict}.** Out-of-paper z {s_oop['z']:.2f}, full z "
        f"{s_full['z']:.2f} (bar {BAR}; ONC end {ONC}); out of paper CMV net Sharpe "
        f"{shp['CMV']['out-of-paper']:.2f} vs UMV {shp['UMV']['out-of-paper']:.2f} vs "
        f"own-vol twin {shp['OWN']['out-of-paper']:.2f}.\n"
    )
    L.append(
        "Kill rules: "
        + "; ".join(f"{k}: {'HIT' if v else 'not hit'}" for k, v in kills.items())
        + ".\n"
    )
    L.append("## Alpha against the `tsmom12` proxy\n")
    L.append(
        "| Portfolio | Sample | Months | Sharpe | vol %/yr | rho | alpha %/yr | IR | NW z | "
        "boot z | z (decides) |"
    )
    L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    names = {"BOOK": "xs-century-1 book (unmanaged)"} | {k: v[0] for k, v in specs.items()}
    for key in ["CMV", "UMV", "OWN", "BOOK", *[k for k in specs if k.startswith("R")]]:
        for sn in samples if key in ("CMV", "UMV", "OWN", "BOOK") else ["full", "out-of-paper"]:
            s = sc[(key, sn)]
            L.append(
                f"| {names[key]} | {sn} | {s['n_m']} | {s['sr_r']:.2f} | "
                f"{s['vol_r'] * 100:.1f} | {s['rho']:+.2f} | {s['a'] * 1200:+.2f} | "
                f"{s['ir']:+.2f} | {s['z_nw']:.2f} | {s['z_boot']:.2f} | **{s['z']:.2f}** |"
            )
    L.append(
        "\nSub-period rows (in-paper, pre, post) use 200 bootstrap draws; full and out-of-paper "
        "2,000 (seed 20261124).\n"
    )
    L.append("## The paper's own test: CMV against UMV (net)\n")
    L.append(
        "| Sample | CMV Sharpe | UMV Sharpe | CMV / UMV - 1 | own-vol twin Sharpe | book Sharpe | "
        "alpha of CMV on UMV, NW t |"
    )
    L.append("|---|---:|---:|---:|---:|---:|---:|")
    for sn in samples:
        a = paper_t[sn]
        u = shp["UMV"][sn]
        rel = f"{shp['CMV'][sn] / u - 1:+.0%}" if u > 0 else "-"
        L.append(
            f"| {sn} | {shp['CMV'][sn]:.2f} | {u:.2f} | {rel} | {shp['OWN'][sn]:.2f} | "
            f"{shp['BOOK'][sn]:.2f} | {a['z_nw']:.2f} |"
        )
    L.append("\n## Weights and costs (CMV, UMV, twin; out-of-sample months)\n")
    L.append(
        "| Portfolio | mean gross notional (sum 2 s theta) | scaling cost %/yr | "
        "mean theta per sleeve (HML, UMD, bond v/m/c, FX v/m/c; months held) |"
    )
    L.append("|---|---:|---:|---|")
    order = [US[0], US[1], "bond-value", "bond-mom", "bond-carry", "fx-value", "fx-mom", "fx-carry"]
    full0 = parts(full_sleeves(data, gross=False, umd_cost=xr.UMD_C), False)[1]
    for key in ["CMV", "UMV", "OWN"]:
        _, out, th = res[key]
        gn = np.mean([sum(2 * full0[k][t] * abs(v) for k, v in th[t].items()) for t in th])
        cost = np.mean([v[2] for v in out.values()]) * 1200
        mt = []
        for k in order:
            vals = [th[t][k] for t in th if k in th[t]]
            mt.append(f"{np.mean(vals):.2f} ({len(vals)})" if vals else "-")
        L.append(f"| {key} | {gn:.2f} | {cost:.2f} | {', '.join(mt)} |")
    L.append("\n## By decade (net Sharpe)\n")
    L.append("| Decade | CMV | UMV | own-vol | book |")
    L.append("|---|---:|---:|---:|---:|")
    for dec in range(1930, 2030, 10):
        lo, hi = date(dec, 1, 1), date(dec + 10, 1, 1)
        cells = []
        for key in ["CMV", "UMV", "OWN", "BOOK"]:
            r_ = np.array([v for m, v in sorted(series[key].items()) if lo <= m < hi])
            cells.append(f"{vm.sharpe(r_):.2f}" if len(r_) >= 24 else "-")
        L.append(f"| {dec}s | " + " | ".join(cells) + " |")
    L.append(
        f"\nMarket-vol months: {len(mkt_sd)} ({min(mkt_sd):%Y-%m}..{max(mkt_sd):%Y-%m}); "
        f"median monthly sigma {np.median(list(mkt_sd.values())) * 100:.2f}% a day.\n"
    )
    RESULT.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    print(math.nan if not cmv else "done")


if __name__ == "__main__":
    main()
