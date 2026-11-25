"""xs-century-1: run the century style book once and score it against `tsmom12` (alpha form).

    uv run python -I research/lib/xs_century_run.py

Card: research/cards/xs-century-1.md. Reads only the cache (Ken French monthly factors, the
data-long-3 ALFRED files, the committed weekly returns store for R6); nothing after 2025-10-31.
Writes research/results/xs-century-1.md (statistics only) and appends rows to
research/tries.md the moment the run is scored.
"""

from __future__ import annotations

import math
import sys
import zipfile
from collections.abc import Callable, Mapping
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "src"))
import long_x as lx  # noqa: E402
import long_x_build as lb  # noqa: E402
import xs_century as xc  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade import returnstore as rs  # noqa: E402

IDEA = "xs-century-1"
LAST = date(2025, 10, 1)  # last month (October 2025)
FX_FLOAT = date(1973, 3, 1)
FRENCH = "french/2026-11-12"
BOND_LAG, FX_SPOT_LAG, RATE_LAG, PPI_LAG = 3, 2, 3, 3
COST = {"bond": 0.0005, "fx": 0.0005, "com": 0.0010}
HML_C, UMD_C, UMD_C_MIT, BORROW = 0.0005, 0.0065, 0.0034, 0.005
COMMODITIES = ["PPI-grains", "PPI-livestock", "PPI-coal", "PPI-natgas", "PPI-crude",
               "PPI-steel", "PPI-prim-nonferrous"]  # fmt: skip
HALF = date(1973, 1, 1)
POST = date(1994, 1, 1)
RESULT = REPO / "research" / "results" / "xs-century-1.md"
TRIES = REPO / "research" / "tries.md"

M = dict[date, float]


def ym(s: str) -> date:
    return date(int(s[:4]), int(s[4:6]), 1)


def french_monthly(fname: str, cols: list[str]) -> dict[str, M]:
    """First (monthly) block of a Ken French CSV, in decimals, cut at LAST."""
    with zipfile.ZipFile(cache_root() / FRENCH / fname) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    out: dict[str, M] = {c: {} for c in cols}
    header: list[str] | None = None
    for line in text.splitlines():
        cells = [x.strip() for x in line.split(",")]
        if header is None:
            if len(cells) > 1 and cells[0] == "" and all(c in cells for c in cols):
                header = cells
            continue
        if len(cells[0]) != 6 or not cells[0].isdigit():
            if any(out[c] for c in cols):
                break
            continue
        d = ym(cells[0])
        if d > LAST:
            continue
        for c in cols:
            out[c][d] = float(cells[header.index(c)]) / 100.0
    return out


def as_m(s: lx.Series) -> M:
    return {d: v for d, v in s if d <= LAST}


# ---------------------------------------------------------------- inputs


def us_stocks() -> tuple[M, M, M, M]:
    ff = french_monthly("F-F_Research_Data_Factors_CSV.zip", ["Mkt-RF", "HML", "RF"])
    mom = french_monthly("F-F_Momentum_Factor_CSV.zip", ["Mom"])["Mom"]
    return ff["Mkt-RF"], ff["RF"], ff["HML"], mom


def bonds() -> tuple[dict[str, M], dict[str, M], dict[str, M]]:
    """(excess returns, 10y yields, local 3m rates) per country, US included."""
    ret: dict[str, M] = {}
    y10: dict[str, M] = {}
    y3: dict[str, M] = {}
    us3 = dict(lb.us_short())
    gs = lx.consecutive(lb.alfred("GS10"))
    ret["US"] = {
        d: r - us3[xc.add_months(d, -1)] / 1200.0
        for d, r in lx.bond_returns(gs, 10.0, monthly=True)
        if xc.add_months(d, -1) in us3 and d <= LAST
    }
    y10["US"], y3["US"] = as_m(gs), as_m(list(us3.items()))
    panel = {e.name: e for e in lb.panel()}
    for cc in lb.FOREIGN_10Y:
        ret[cc] = as_m(panel[f"GOV10-{cc}"].returns)
        y10[cc] = as_m(lx.consecutive(lb.alfred(f"IRLTLT01{cc}M156N")))
        y3[cc] = as_m(lb.short_rate(cc)[0])
    return ret, y10, y3


def currencies() -> tuple[dict[str, M], dict[str, M], dict[str, M], M]:
    """(excess returns, month-end spot, foreign 3m rate) per currency, and the US 3m rate."""
    panel = {e.name: e for e in lb.panel()}
    ret, spot, rate = {}, {}, {}
    for cur in lb.FX_LINES:
        ret[cur] = {d: v for d, v in as_m(panel[f"FX-{cur}"].returns).items() if d >= FX_FLOAT}
        s, _ = lb.fx_spot_month_end(cur)
        spot[cur] = {d: v for d, v in as_m(s).items() if d >= add(FX_FLOAT, -1)}
        if cur == "EUR":
            de, _ = lb.short_rate("DE")
            ez, _ = lb.short_rate("EZ")
            fr = [(d, v) for d, v in de if d < date(1999, 1, 1)]
            fr += [(d, v) for d, v in ez if d >= date(1999, 1, 1)]
        else:
            fr, _ = lb.short_rate(lb.CC[cur])
        rate[cur] = as_m(fr)
    return ret, spot, rate, as_m(lb.us_short())


def commodities() -> tuple[dict[str, M], dict[str, M]]:
    ret, px = {}, {}
    for name in COMMODITIES:
        p = lx.consecutive(lb.alfred(lb.PPI[name]))
        px[name] = as_m(p)
        ret[name] = as_m(lx.simple_returns(p))
    return ret, px


def add(d: date, k: int) -> date:
    return xc.add_months(d, k)


# ---------------------------------------------------------------- the book


Sig = Callable[[str, date], float | None]


def signals(assets: Mapping[str, M], fn: Sig) -> dict[date, dict[str, float]]:
    allm = sorted({t for r in assets.values() for t in r})
    out: dict[date, dict[str, float]] = {}
    for t in allm:
        row = {}
        for a in assets:
            v = fn(a, t)
            if v is not None and t in assets[a]:
                row[a] = v
        out[t] = row
    return out


def net(sl: Mapping[date, tuple[float, float, float]], gross: bool) -> M:
    return {t: (v[1] if gross else v[0]) for t, v in sl.items()}


def build(
    data: dict[str, object],
    *,
    gross: bool = False,
    umd_cost: float = UMD_C,
    cost_mult: float = 1.0,
    with_com: bool = False,
    with_us: bool = True,
) -> tuple[dict[date, float], dict[str, M]]:
    """The card's book. Returns (book, every sleeve's net return)."""
    sleeves: dict[str, M] = {}
    classes: dict[str, list[M]] = {}
    if with_us:
        hml, umd = data["hml"], data["umd"]
        assert isinstance(hml, dict) and isinstance(umd, dict)
        b = 0.0 if gross else BORROW
        sleeves["US-value(HML)"] = net(xc.factor_sleeve(hml, 0.0 if gross else HML_C, b), gross)
        sleeves["US-mom(UMD)"] = net(xc.factor_sleeve(umd, 0.0 if gross else umd_cost, b), gross)
        classes["US stocks"] = [sleeves["US-value(HML)"], sleeves["US-mom(UMD)"]]
    br, y10, y3 = data["bonds"]  # type: ignore[misc]
    cb = 0.0 if gross else COST["bond"] * cost_mult
    bsig = {
        "bond-value": lambda a, t: xc.yield_change_value(y10[a], t, BOND_LAG),
        "bond-mom": lambda a, t: xc.momentum(br[a], t, max(2, BOND_LAG)),
        "bond-carry": lambda a, t: xc.spread_value(y10[a], y3[a], t, BOND_LAG),
    }
    classes["Bonds"] = []
    for k, fn in bsig.items():
        sleeves[k] = net(xc.constructed_sleeve(signals(br, fn), br, cb), gross)
        classes["Bonds"].append(sleeves[k])
    fr, spot, frate, usr = data["fx"]  # type: ignore[misc]
    cf = 0.0 if gross else COST["fx"] * cost_mult
    fsig = {
        "fx-value": lambda a, t: xc.reversal_value(spot[a], t, FX_SPOT_LAG),
        "fx-mom": lambda a, t: xc.momentum(fr[a], t, FX_SPOT_LAG),
        "fx-carry": lambda a, t: xc.spread_value(frate[a], usr, t, RATE_LAG),
    }
    classes["Currencies"] = []
    for k, fn in fsig.items():
        sleeves[k] = net(xc.constructed_sleeve(signals(fr, fn), fr, cf), gross)
        classes["Currencies"].append(sleeves[k])
    if with_com:
        cr, cpx = data["com"]  # type: ignore[misc]
        cc = 0.0 if gross else COST["com"] * cost_mult
        csig = {
            "com-value": lambda a, t: xc.reversal_value(cpx[a], t, PPI_LAG),
            "com-mom": lambda a, t: xc.momentum(cr[a], t, PPI_LAG),
        }
        classes["Commodities"] = []
        for k, fn in csig.items():
            sleeves[k] = net(xc.constructed_sleeve(signals(cr, fn), cr, cc), gross)
            classes["Commodities"].append(sleeves[k])
    bk = xc.book(classes)
    return {t: v for t, v in bk.items() if t <= LAST}, sleeves


def tsmom_market(mkt_rf: M, rf: M) -> M:
    """`tsmom12`'s rule on the US market, monthly, above bills."""
    tot = {d: mkt_rf[d] + rf[d] for d in mkt_rf}
    out: M = {}
    for t in sorted(tot):
        past = [tot.get(add(t, -k)) for k in range(1, 13)]
        if any(v is None for v in past):
            continue
        g = math.prod(1.0 + v for v in past if v is not None)
        out[t] = mkt_rf[t] if g > 1.0 else 0.0
    return out


def tsmom_six(rf: M) -> M:
    """R6: the store's six-asset `tsmom12` (weekly), compounded to calendar months by the
    Friday's month, above the French RF. Only complete months from 1994-02 to 2025-10."""
    rows = [
        r
        for r in rs.read(REPO / "research" / "register" / "returns")
        if r.idea == "baselines" and r.variant == "tsmom12" and r.start == "1994-02-01"
    ]
    rows.sort(key=lambda r: not r.source.startswith("harness"))
    row = rows[0]
    f0 = date.fromisoformat(row.first_friday)
    acc: dict[date, float] = {}
    for i, r in enumerate(row.rets):
        d = f0 + timedelta(days=7 * i)
        if d > date(2025, 10, 31):
            break
        m = d.replace(day=1)
        acc[m] = (1.0 + acc.get(m, 0.0)) * (1.0 + r) - 1.0
    return {m: v - rf[m] for m, v in acc.items() if date(1994, 3, 1) <= m <= LAST and m in rf}


# ---------------------------------------------------------------- scoring and output


def aligned(b: M, t: M, lo: date | None = None, hi: date | None = None) -> tuple[np.ndarray, ...]:
    ms = sorted(m for m in set(b) & set(t) if (lo is None or m >= lo) and (hi is None or m < hi))
    return np.array([b[m] for m in ms]), np.array([t[m] for m in ms]), np.array(ms)


def total_dd(r: np.ndarray) -> tuple[float, float]:
    eq = np.cumprod(1.0 + r)
    return float(eq[-1] - 1.0), float(1.0 - (eq / np.maximum.accumulate(eq)).min())


def tries_row(variant: str, kind: str, ms: np.ndarray, r: np.ndarray, now: str) -> str:
    tot, dd = total_dd(r)
    sr = float(r.mean() / r.std(ddof=1)) * math.sqrt(12)
    to = date(ms[-1].year + ms[-1].month // 12, ms[-1].month % 12 + 1, 1) - timedelta(days=1)
    return (f"| {now} | {IDEA} | {variant} | {kind} | train | {ms[0].isoformat()} | "
            f"{to.isoformat()} | {sr:.2f} | {tot * 100:+.1f}% | {dd * 100:.1f}% | - |")  # fmt: skip


def fmt(v: float, d: int = 2) -> str:
    return f"{v:+.{d}f}"


def main() -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    mkt_rf, rf, hml, umd = us_stocks()
    data: dict[str, object] = {
        "hml": hml,
        "umd": umd,
        "bonds": bonds(),
        "fx": currencies(),
        "com": commodities(),
    }
    tm = tsmom_market(mkt_rf, rf)
    primary, sleeves = build(data)
    runs: dict[str, tuple[str, dict[date, float], M, date | None, date | None]] = {
        "primary": ("book (primary)", primary, tm, None, None),
        "R1": ("R1 gross", build(data, gross=True)[0], tm, None, None),
        "R2": ("R2 UMD cost 0.34%/mo", build(data, umd_cost=UMD_C_MIT)[0], tm, None, None),
        "R3": ("R3 bond/FX costs x2", build(data, cost_mult=2.0)[0], tm, None, None),
        "R4": ("R4 + commodity spot", build(data, with_com=True)[0], tm, None, None),
        "R5": ("R5 1994-01..2025-10", primary, tm, POST, None),
        "R6": ("R6 vs six-asset tsmom12", primary, tsmom_six(rf), None, None),
        "R7": ("R7 bonds + FX only", build(data, with_us=False)[0], tm, None, None),
    }
    scores = {}
    for key, (_, b, t, lo, hi) in runs.items():
        r, x, ms = aligned(b, t, lo, hi)
        scores[key] = (xc.score(r, x), ms, r, x)
    s0, ms0, r0, x0 = scores["primary"]
    halves = {}
    for nm, lo, hi in [("1928..1972", None, HALF), ("1973..2025", HALF, None)]:
        r, x, ms = aligned(primary, tm, lo, hi)
        halves[nm] = (xc.alpha(r, x), ms)
    bar, onc = 4.70, 3.29
    both = all(h[0]["a"] > 0 for h in halves.values())
    verdict = (
        "PASS (informational)" if s0["z"] >= bar and both else "NEAR" if s0["z"] >= onc else "FAIL"
    )
    # tries rows first (the moment the run is scored)
    rows = [
        tries_row(
            "tsmom12@us-mkt-monthly (comparator, above bills, monthly x sqrt12)",
            "baseline",
            ms0,
            x0,
            now,
        ),  # fmt: skip
    ]
    for key, (label, *_rest) in runs.items():
        s, ms, r, _ = scores[key]
        kind = "variant" if key == "primary" else "robustness"
        v = (f"{label}: alpha vs tsmom12 IR {s['ir']:+.2f} z {s['z']:+.2f} "
             f"(monthly excess x sqrt12)")  # fmt: skip
        rows.append(tries_row(v, kind, ms, r, now))
    with TRIES.open("a") as fh:
        fh.write("\n".join(rows) + "\n")

    L: list[str] = []
    L.append("# xs-century-1 results (generated by research/lib/xs_century_run.py)\n")
    L.append(f"Run {now} UTC. Card: `research/cards/xs-century-1.md`. Monthly, excess returns. "
             "Statistics only.\n")  # fmt: skip
    L.append(f"**Verdict (card's rules): {verdict}.** Primary z {s0['z']:.2f} "
             f"(bar 4.70; ONC end 3.29); IR {s0['ir']:+.2f} against power-map-1's 0.51 / 0.60; "
             f"alpha > 0 in both halves: {'yes' if both else 'no'}.\n")  # fmt: skip
    L.append("## Alpha against the `tsmom12` proxy\n")
    L.append("| Run | Months | From | Years | Book Sharpe | Book vol | rho | beta | alpha %/yr | "
             "IR | NW z | boot z | z (decides) | mix w | mix gain |")  # fmt: skip
    L.append("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for key, (label, *_rest) in runs.items():
        s, ms, _, _ = scores[key]
        L.append(
            f"| {label} | {s['n']} | {ms[0]:%Y-%m} | {s['years']:.1f} | {s['sr_r']:.2f} | "
            f"{s['vol_r'] * 100:.1f}% | {s['rho']:+.2f} | {s['b']:+.3f} | "
            f"{s['a'] * 1200:+.2f} | {s['ir']:+.2f} | {s['z_nw']:.2f} | {s['z_boot']:.2f} | "
            f"**{s['z']:.2f}** | {s['mix_w']:.2f} | {s['mix_gain']:+.3f} |"
        )
    L.append(f"\nComparator Sharpe (primary window): {s0['mix_sr_t']:.2f}; NW lag {s0['lag']}; "
             "bootstrap 2,000 draws, 12-month blocks, seed 20261124.\n")  # fmt: skip
    L.append("## Halves (primary book; NW only)\n")
    L.append("| Half | Months | alpha %/yr | IR | NW z |")
    L.append("|---|---:|---:|---:|---:|")
    for nm, (a, _ms) in halves.items():
        L.append(f"| {nm} | {a['n']} | {a['a'] * 1200:+.2f} | {a['ir']:+.2f} | {a['z_nw']:.2f} |")
    L.append("\n## Sleeves (net, own Sharpe; alpha vs the same comparator)\n")
    L.append("| Sleeve | From | Months | Sharpe | IR vs tsmom12 | NW z |")
    L.append("|---|---|---:|---:|---:|---:|")
    for k, sl in sleeves.items():
        r, x, ms = aligned(sl, tm)
        if len(r) < 24:
            L.append(f"| {k} | - | {len(r)} | - | - | - |")
            continue
        a = xc.alpha(r, x)
        sr = float(r.mean() / r.std(ddof=1)) * math.sqrt(12)
        L.append(f"| {k} | {ms[0]:%Y-%m} | {len(r)} | {sr:.2f} | {a['ir']:+.2f} | "
                 f"{a['z_nw']:.2f} |")  # fmt: skip
    L.append("\n## By decade (primary book, net)\n")
    L.append("| Decade | Book Sharpe | Book return %/yr | alpha %/yr |")
    L.append("|---|---:|---:|---:|")
    for dec in range(1920, 2030, 10):
        r, x, ms = aligned(primary, tm, date(dec, 1, 1), date(dec + 10, 1, 1))
        if len(r) < 24:
            continue
        a = xc.alpha(r, x)
        sr = float(r.mean() / r.std(ddof=1)) * math.sqrt(12)
        L.append(f"| {dec}s | {sr:.2f} | {r.mean() * 1200:+.2f} | {a['a'] * 1200:+.2f} |")
    RESULT.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
