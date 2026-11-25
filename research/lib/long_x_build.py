"""data-long-3: coverage, validation and descriptive statistics of the new long series.

    uv run python -I research/lib/long_x_build.py

Reads only the cached files (`long_x_fetch.py`; datahub gold, Damodaran and Yahoo ETF closes
from earlier lanes), cut at 2025-10-31. Writes `research/results/data-long-3.md` and
`research/results/data-long-3.json` (statistics only: no prices, no return series). No trend
rule, signal or strategy statistic is computed here (research/data-long-3.md).

`panel()` is the entry point for the next lane: every monthly return series with its metadata.
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import long_x as lx  # noqa: E402
import long_x_fetch as fx  # noqa: E402

RESULTS = HERE.parents[0] / "results"
Series = list[tuple[date, float]]


def root() -> Path:
    return fx.cache_root()


def alfred(sid: str) -> Series:
    p = root() / f"data-long-3/alfred/{fx.VINTAGE}/{sid}.csv"
    return lx.parse_alfred(p.read_text())


def has(sid: str) -> bool:
    return (root() / f"data-long-3/alfred/{fx.VINTAGE}/{sid}.csv").exists()


def yahoo(path: Path) -> Series:
    return lx.yahoo_adjclose(json.loads(path.read_text()))


def yahoo_close(path: Path) -> Series:
    """Raw close (indices have no adjclose worth using)."""
    from datetime import UTC, datetime

    res = json.loads(path.read_text())["chart"]["result"][0]
    out: Series = []
    for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"], strict=True):
        d = datetime.fromtimestamp(t, UTC).date()
        if c is not None and d <= lx.LAST:
            out.append((d, float(c)))
    return out


YH = Path("yahoo-1d/2026-11-12")
YX = Path(f"data-long-3/yahoo/{fx.SNAP}")


# ---------------------------------------------------------------- panel


@dataclass
class Entry:
    name: str
    cls: str  # rates / fx / commodity
    returns: Series  # monthly simple returns, dated the first of the month they end in
    source: str
    averaged: bool  # built from monthly averages (needs the one-month gap, data-long-2)
    timing: str  # lx.available() kind of the inputs
    note: str = ""


US_BONDS = {
    "UST2": ("DGS2", 2.0),
    "UST5": ("DGS5", 5.0),
    "UST10": ("DGS10", 10.0),
    "UST30": ("DGS30", 30.0),
}
FX_LINES = ["JPY", "GBP", "CHF", "CAD", "EUR", "AUD", "NZD", "SEK", "NOK"]
FX_ID = {c: k for k, (c, _) in lx.FX_QUOTE.items()}
CC = {
    "JPY": "JP",
    "GBP": "GB",
    "CHF": "CH",
    "CAD": "CA",
    "AUD": "AU",
    "NZD": "NZ",
    "SEK": "SE",
    "NOK": "NO",
}
PPI = {
    "PPI-all": "PPIACO",
    "PPI-farm": "WPU01",
    "PPI-grains": "WPU012",
    "PPI-wheat": "WPU0121",
    "PPI-livestock": "WPU013",
    "PPI-coal": "WPU051",
    "PPI-natgas": "WPU0531",
    "PPI-crude": "WPU0561",
    "PPI-metals": "WPU10",
    "PPI-steel": "WPU101",
    "PPI-nonferrous": "WPU102",
    "PPI-prim-nonferrous": "WPU1022",
}
FOREIGN_10Y = ["JP", "GB", "CH", "CA", "DE", "AU", "NZ", "SE", "NO"]


def short_rate(cc: str) -> tuple[Series, list[tuple[str, date, date]]]:
    """Monthly 3-month rate by priority: OECD 3m interbank, OECD call money, IMF T-bill, IMF
    discount rate. Returns the merged series and which source covers which span."""
    ids = [f"IR3TIB01{cc}M156N", f"IRSTCI01{cc}M156N", f"INTGST{cc}M193N", f"INTDSR{cc}M193N"]
    parts = [alfred(i) if has(i) else [] for i in ids]
    merged = lx.first_available(*parts)
    used: list[tuple[str, date, date]] = []
    src = {d: next(i for i, p in zip(ids, parts, strict=True) if d in dict(p)) for d, _ in merged}
    for d, _ in merged:
        if used and used[-1][0] == src[d]:
            used[-1] = (src[d], used[-1][1], d)
        else:
            used.append((src[d], d, d))
    return merged, used


def us_short() -> Series:
    return lx.first_available(alfred("IR3TIB01USM156N"), alfred("TB3MS"))


def fx_spot_month_end(cur: str) -> tuple[Series, bool]:
    """Month-end USD per unit; EUR before 1999 is the mark's monthly AVERAGE (EXGEUS)."""
    if cur == "EUR":
        eur = lx.month_end(lx.usd_per_unit(alfred("DEXUSEU"), per_usd=False))
        dem = lx.usd_per_unit(alfred("EXGEUS"), per_usd=True)
        return lx.splice_eur(dem, eur), True
    sid = FX_ID[cur]
    return lx.month_end(lx.usd_per_unit(alfred(sid), lx.FX_QUOTE[sid][1])), False


def panel() -> list[Entry]:
    out: list[Entry] = []
    for name, (sid, m) in US_BONDS.items():
        ys = lx.month_end(alfred(sid))
        r = lx.bond_returns(lx.consecutive(ys), m, monthly=True)
        out.append(Entry(name, "rates", r, f"ALFRED {sid} month-end", False, "h15-daily"))
    gs = lx.bond_returns(lx.consecutive(alfred("GS10")), 10.0, monthly=True)
    out.append(
        Entry(
            "UST10-avg",
            "rates",
            gs,
            "ALFRED GS10 (monthly average)",
            True,
            "h15-monthly",
            "1953-04 on; check series for the averaging error",
        )
    )
    for cc in FOREIGN_10Y:
        ys = lx.consecutive(alfred(f"IRLTLT01{cc}M156N"))
        loc = lx.bond_returns(ys, 10.0, monthly=True)
        sr, _ = short_rate("DE" if cc == "DE" else cc)
        srd = dict(sr)
        prev = {lx._next_month(d): v for d, v in srd.items()}
        ex = [(d, r - prev[d] / 1200.0) for d, r in loc if d in prev]
        out.append(
            Entry(
                f"GOV10-{cc}",
                "rates",
                ex,
                f"ALFRED IRLTLT01{cc}M156N (OECD, average)",
                True,
                "oecd-monthly",
                "local-currency excess over the local 3m rate (a hedged return)",
            )
        )
    usr = us_short()
    for cur in FX_LINES:
        spot, avg = fx_spot_month_end(cur)
        if cur == "EUR":
            de, _ = short_rate("DE")
            ez, _ = short_rate("EZ")
            fr = [(d, v) for d, v in de if d < date(1999, 1, 1)] + [
                (d, v) for d, v in ez if d >= date(1999, 1, 1)
            ]
        else:
            fr, _ = short_rate(CC[cur])
        rows = lx.fx_excess_monthly(lx.consecutive(spot) if not avg else spot, fr, usr)
        out.append(
            Entry(
                f"FX-{cur}",
                "fx",
                [(d, x) for d, _, x in rows],
                f"ALFRED {'EXGEUS+DEXUSEU' if cur == 'EUR' else FX_ID[cur]}",
                avg,
                "h10-daily",
                "carry-inclusive excess return, long the currency, USD-funded"
                + ("; DEM monthly averages before 1999" if avg else ""),
            )
        )
    for name, sid in PPI.items():
        px = lx.consecutive(alfred(sid))
        out.append(
            Entry(
                name,
                "commodity",
                lx.simple_returns(px),
                f"ALFRED {sid} (BLS PPI)",
                False,
                "ppi",
                "spot price index, no roll or collateral",
            )
        )
    wti = lx.consecutive(alfred("WTISPLC"))
    out.append(
        Entry(
            "WTI-avg",
            "commodity",
            lx.simple_returns(wti),
            "ALFRED WTISPLC",
            True,
            "h15-monthly",
            "monthly average spot; no roll or collateral",
        )
    )
    return out


# ---------------------------------------------------------------- helpers


def compound_by(rets: Sequence[tuple[date, float]], key: Callable[[date], date]) -> Series:
    acc: dict[date, float] = {}
    for d, r in rets:
        k = key(d)
        acc[k] = acc.get(k, 1.0) * (1.0 + r)
    return [(k, v - 1.0) for k, v in sorted(acc.items())]


def month_key(d: date) -> date:
    return d.replace(day=1)


def week_key(d: date) -> date:
    return d + timedelta(days=(4 - d.weekday()) % 7)  # the Friday ending the week


def pair(a: Series, b: Series, per_year: int, since: date | None = None) -> dict[str, float]:
    da, db = dict(a), dict(b)
    ks = sorted(k for k in set(da) & set(db) if since is None or k >= since)
    st = lx.stats_pair([da[k] for k in ks], [db[k] for k in ks], per_year)
    st["dd_a"] = lx.max_drawdown(da[k] for k in ks)
    st["dd_b"] = lx.max_drawdown(db[k] for k in ks)
    st["first"] = ks[0].isoformat()  # type: ignore[assignment]
    st["last"] = ks[-1].isoformat()  # type: ignore[assignment]
    return st


def daily_bond(sid: str, m: float) -> Series:
    return lx.bond_returns(alfred(sid), m)


def blend(*ss: Series) -> Series:
    maps = [dict(s) for s in ss]
    ks = sorted(set(maps[0]).intersection(*maps[1:]))
    return [(k, sum(mp[k] for mp in maps) / len(maps)) for k in ks]


def etf_returns(path: Path) -> Series:
    return lx.simple_returns(yahoo(path))


# ---------------------------------------------------------------- validation blocks


def validate_bonds() -> dict[str, Any]:
    r = root()
    syn = {m: daily_bond(f"DGS{m}", float(m)) for m in (1, 2, 5, 7, 10, 20, 30)}
    etfs = {t: etf_returns(r / YH / f"{t}.json") for t in ("IEF", "TLT", "SHY")}
    cases = {
        "IEF vs 10y": ("IEF", syn[10]),
        "IEF vs 7y": ("IEF", syn[7]),
        "IEF vs 7y/10y": ("IEF", blend(syn[7], syn[10])),
        "TLT vs 20y": ("TLT", syn[20]),
        "TLT vs 30y": ("TLT", syn[30]),
        "TLT vs 20y/30y": ("TLT", blend(syn[20], syn[30])),
        "SHY vs 2y": ("SHY", syn[2]),
        "SHY vs 1y/2y": ("SHY", blend(syn[1], syn[2])),
    }
    out: dict[str, Any] = {}
    for label, (t, s) in cases.items():
        e = etfs[t]
        out[label] = {
            "monthly": pair(compound_by(s, month_key), compound_by(e, month_key), 12),
            "weekly": pair(compound_by(s, week_key), compound_by(e, week_key), 52),
        }
    # exact repricing against the duration-convexity approximation, 10y month-end 1962-2025
    ys = lx.consecutive(lx.month_end(alfred("DGS10")))
    ex = lx.bond_returns(ys, 10.0, monthly=True)
    ap = [
        (d1, lx.bond_step_duration(y0, y1, 10.0, 1 / 12))
        for (_, y0), (d1, y1) in zip(ys, ys[1:], strict=False)
    ]
    out["exact vs duration-convexity, 10y monthly"] = pair(ex, ap, 12)
    # monthly-average yields (GS10) against month-end yields (DGS10): the averaging error
    gs = lx.bond_returns(lx.consecutive(alfred("GS10")), 10.0, monthly=True)
    out["GS10 average vs DGS10 month-end"] = pair(gs, ex, 12)
    # OECD US long rate (the input type of the foreign bonds) against DGS10 month-end
    oe = lx.bond_returns(lx.consecutive(alfred("IRLTLT01USM156N")), 10.0, monthly=True)
    out["OECD US 10y average vs DGS10 month-end"] = pair(oe, ex, 12)
    out["damodaran"] = damodaran_check(ex)
    return out


def damodaran_check(ex: Series) -> dict[str, Any]:
    """Calendar-year 10y return from DGS10 month-end against Damodaran's T-bond, 1963-2024."""
    try:
        import long_check  # type: ignore[import-not-found]

        dam = long_check.damodaran()
    except Exception as e:  # noqa: BLE001 - optional cross-check
        return {"skipped": str(e)}
    yr: dict[int, float] = {}
    for d, x in ex:
        yr[d.year] = yr.get(d.year, 1.0) * (1.0 + x)
    years = [y for y in range(1963, 2025) if y in yr and y in dam]
    gaps = [(yr[y] - 1.0) - dam[y][0] for y in years]
    a = [yr[y] - 1.0 for y in years]
    b = [dam[y][0] for y in years]
    st = lx.stats_pair(a, b, 1)
    return {
        "years": f"{years[0]}-{years[-1]}",
        "corr": st["corr"],
        "mean_gap": st["gap"],
        "mean_abs_gap": sum(abs(g) for g in gaps) / len(gaps),
        "max_abs_gap": max(abs(g) for g in gaps),
        "years_over_1pt": sum(abs(g) > 0.01 for g in gaps),
    }


def validate_fx() -> dict[str, Any]:
    """CurrencyShares trusts (spot + the deposit rate they earn - 0.40% fee, unfunded)."""
    r = root()
    trust = {"EUR": "FXE", "JPY": "FXY", "GBP": "FXB", "CHF": "FXF", "CAD": "FXC", "AUD": "FXA"}
    out: dict[str, Any] = {}
    for cur, t in trust.items():
        etf = compound_by(etf_returns(r / YX / f"{t}.json"), month_key)
        etf = etf[1:]  # first month is partial
        spot, _ = fx_spot_month_end(cur)
        spot_r = lx.simple_returns(spot)
        if cur == "EUR":
            fr, _ = short_rate("EZ")
        else:
            fr, _ = short_rate(CC[cur])
        prev = {lx._next_month(d): v for d, v in fr}
        dep = [(d, (1 + s) * (1 + prev[d] / 1200.0) - 1) for d, s in spot_r if d in prev]
        out[f"{t} vs spot"] = pair(spot_r, etf, 12)
        out[f"{t} vs spot + 3m rate"] = pair(dep, etf, 12)
    return out


def validate_commodities() -> dict[str, Any]:
    r = root()
    out: dict[str, Any] = {}
    wti_d = alfred("DCOILWTICO")
    me = lx.simple_returns(lx.month_end(wti_d))
    # PPI prices refer to the Tuesday of the week with the 13th: last WTI quote on or before 13th
    mid: dict[date, float] = {}
    for d, v in wti_d:
        if d.day <= 13:
            mid[d.replace(day=1)] = v
    mid_r = lx.simple_returns(lx.consecutive(sorted(mid.items())))
    ppi = lx.simple_returns(lx.consecutive(alfred("WPU0561")))
    avg = lx.simple_returns(lx.consecutive(alfred("WTISPLC")))
    out["PPI crude vs WTI mid-month (day <= 13)"] = pair(ppi, mid_r, 12)
    out["PPI crude vs WTI month-end"] = pair(ppi, me, 12)
    out["WTI monthly average (WTISPLC) vs WTI month-end"] = pair(avg, me, 12)
    uso = compound_by(etf_returns(r / YH / "USO.json"), month_key)[1:]
    out["WTI month-end spot vs USO (front futures fund)"] = pair(me, uso, 12)
    imf_cu = lx.simple_returns(lx.consecutive(alfred("PCOPPUSDM")))
    out["PPI primary nonferrous vs IMF copper (average)"] = pair(
        lx.simple_returns(lx.consecutive(alfred("WPU1022"))), imf_cu, 12
    )
    imf_w = lx.simple_returns(lx.consecutive(alfred("PWHEAMTUSDM")))
    out["PPI wheat vs IMF wheat (average)"] = pair(
        lx.simple_returns(lx.consecutive(alfred("WPU0121"))), imf_w, 12
    )
    return out


# ---------------------------------------------------------------- description


def describe(p: Sequence[Entry]) -> dict[str, Any]:
    gspc = compound_by(lx.simple_returns(yahoo_close(root() / YH / "^GSPC.json")), month_key)
    out: dict[str, Any] = {}
    for e in p:
        rs = e.returns
        xs = [x for _, x in rs]
        n = len(xs)
        mu = sum(xs) / n
        sd = math.sqrt(sum((x - mu) ** 2 for x in xs) / (n - 1))
        # worst drawdown and its dates
        lvl = peak = 1.0
        pk_d = rs[0][0]
        worst, w_from, w_to = 0.0, pk_d, pk_d
        for d, x in rs:
            lvl *= 1 + x
            if lvl > peak:
                peak, pk_d = lvl, d
            if 1 - lvl / peak > worst:
                worst, w_from, w_to = 1 - lvl / peak, pk_d, d
        g = dict(gspc)
        ks = [d for d, _ in rs if d in g]
        da = dict(rs)
        corr = lx.stats_pair([da[k] for k in ks], [g[k] for k in ks], 12)["corr"]
        out[e.name] = {
            "cls": e.cls,
            "first": rs[0][0].isoformat(),
            "last": rs[-1][0].isoformat(),
            "months": n,
            "mean_pa": mu * 12,
            "vol_pa": sd * math.sqrt(12),
            "max_dd": worst,
            "dd_from": w_from.isoformat(),
            "dd_to": w_to.isoformat(),
            "corr_spx": corr,
            "averaged": e.averaged,
            "source": e.source,
            "timing": e.timing,
            "note": e.note,
        }
    return out


def correlations(p: Sequence[Entry], since: date = date(1977, 3, 1)) -> dict[str, Any]:
    """Average pairwise monthly correlation within and between classes, common months."""
    keep = [e for e in p if not e.name.endswith("-avg") and e.name != "PPI-all"]
    maps = {e.name: dict(e.returns) for e in keep}
    common = sorted(k for k in set.intersection(*(set(m) for m in maps.values())) if k >= since)
    names = list(maps)
    cls = {e.name: e.cls for e in keep}
    acc: dict[str, list[float]] = {}
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            c = lx.stats_pair([maps[a][k] for k in common], [maps[b][k] for k in common], 12)
            key = "-".join(sorted((cls[a], cls[b])))
            acc.setdefault(key, []).append(c["corr"])
    every = [x for v in acc.values() for x in v]
    return {
        "window": f"{common[0].isoformat()}..{common[-1].isoformat()}",
        "months": len(common),
        "series": len(names),
        "mean_all": sum(every) / len(every),
        **{k: sum(v) / len(v) for k, v in sorted(acc.items())},
    }


def coverage() -> list[dict[str, Any]]:
    rows = []
    for p in sorted((root() / f"data-long-3/alfred/{fx.VINTAGE}").glob("*.csv")):
        s = lx.parse_alfred(p.read_text())
        rows.append(
            {
                "id": p.stem,
                "first": s[0][0].isoformat(),
                "last": s[-1][0].isoformat(),
                "obs": len(s),
            }
        )
    return rows


def carry_sources() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for cc in [*CC.values(), "DE", "EZ"]:
        _, used = short_rate(cc)
        out[cc] = [(i, a.isoformat(), b.isoformat()) for i, a, b in used]
    return out


# ---------------------------------------------------------------- report


def _f(x: float, spec: str = ".3f") -> str:
    return format(x, spec)


def render(res: dict[str, Any]) -> str:
    L: list[str] = ["# data-long-3 results (generated by `research/lib/long_x_build.py`)", ""]
    L += [
        "Statistics only, train window (nothing after 2025-10-31). Method and reading:",
        "`research/data-long-3.md`.",
        "",
    ]

    def vt(title: str, block: dict[str, Any], per: str = "monthly") -> None:
        L.extend(
            [
                f"## {title}",
                "",
                "| Pair (synthetic vs real) | Window | n | Corr | TE a year | Mean gap a year |"
                " Vol a / b | Max DD a / b |",
                "|---|---|---:|---:|---:|---:|---|---|",
            ]
        )
        for k, v in block.items():
            if "corr" not in v and per in v:
                v = v[per]
            if "corr" not in v or "first" not in v:
                continue
            L.append(
                f"| {k} | {v['first'][:7]}..{v['last'][:7]} | {int(v['n'])} | {_f(v['corr'])} |"
                f" {_f(v['te'] * 100, '.2f')}% | {_f(v['gap'] * 100, '+.2f')}% |"
                f" {_f(v['vol_a'] * 100, '.1f')}% / {_f(v['vol_b'] * 100, '.1f')}% |"
                f" {_f(v['dd_a'] * 100, '.1f')}% / {_f(v['dd_b'] * 100, '.1f')}% |"
            )
        L.append("")

    vt("Bonds, monthly", res["bonds"], "monthly")
    vt(
        "Bonds, weekly (Friday weeks)",
        {k: v for k, v in res["bonds"].items() if "weekly" in v},
        "weekly",
    )
    d = res["bonds"]["damodaran"]
    if "corr" in d:
        L += [
            "Damodaran cross-check (calendar-year 10y return from DGS10 month-end against",
            f"Damodaran's T-bond return, {d['years']}): corr {_f(d['corr'])}, mean gap",
            f"{_f(d['mean_gap'] * 100, '+.2f')} pts, mean abs gap "
            f"{_f(d['mean_abs_gap'] * 100, '.2f')} pts, largest {_f(d['max_abs_gap'] * 100, '.2f')}"
            f" pts, {d['years_over_1pt']} years more than 1 pt apart.",
            "",
        ]
    vt("Currencies against the CurrencyShares trusts, monthly", res["fx"])
    vt("Commodities, monthly", res["commodities"])
    L += [
        "## The panel (monthly series for the next lane)",
        "",
        "| Series | Class | From | To | Months | Mean a year | Vol a year | Max DD | DD from..to |"
        " Corr S&P 500 | Averages? |",
        "|---|---|---|---|---:|---:|---:|---:|---|---:|---|",
    ]
    for k, v in res["panel"].items():
        L.append(
            f"| {k} | {v['cls']} | {v['first'][:7]} | {v['last'][:7]} | {v['months']} |"
            f" {_f(v['mean_pa'] * 100, '+.1f')}% | {_f(v['vol_pa'] * 100, '.1f')}% |"
            f" {_f(v['max_dd'] * 100, '.1f')}% | {v['dd_from'][:7]}..{v['dd_to'][:7]} |"
            f" {_f(v['corr_spx'], '+.2f')} | {'yes' if v['averaged'] else 'no'} |"
        )
    c = res["correlations"]
    L += [
        "",
        f"## Average pairwise correlation of monthly returns ({c['window']}, "
        f"{c['months']} months, {c['series']} series)",
        "",
        "| Pair of classes | Mean corr |",
        "|---|---:|",
    ]
    for k, v in c.items():
        if k not in ("window", "months", "series"):
            L.append(f"| {k} | {_f(v, '+.3f')} |")
    L += [
        "",
        "## Short-rate sources used for carry (priority: OECD 3m, OECD call money, IMF "
        "T-bill, IMF discount rate)",
        "",
        "| Country | Source: span |",
        "|---|---|",
    ]
    for cc, used in res["carry_sources"].items():
        L.append(f"| {cc} | " + "; ".join(f"{i}: {a[:7]}..{b[:7]}" for i, a, b in used) + " |")
    L += [
        "",
        "## Coverage of the cached ALFRED files (vintage 2025-11-10, cut at 2025-10-31)",
        "",
        "| Series | First | Last | Observations |",
        "|---|---|---|---:|",
    ]
    for row in res["coverage"]:
        L.append(f"| {row['id']} | {row['first']} | {row['last']} | {row['obs']} |")
    return "\n".join(L) + "\n"


def main() -> None:
    p = panel()
    res = {
        "bonds": validate_bonds(),
        "fx": validate_fx(),
        "commodities": validate_commodities(),
        "panel": describe(p),
        "correlations": correlations(p),
        "carry_sources": carry_sources(),
        "coverage": coverage(),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "data-long-3.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    (RESULTS / "data-long-3.md").write_text(render(res))
    print(render(res))


if __name__ == "__main__":
    main()
