"""data-long-4: coverage and cross-checks of the long CPI, equity-yield and policy-rate series.

    uv run python -I research/lib/long_macro_build.py

Reads only cached files (`long_macro_fetch.py`; data-long-3's ALFRED files and spot rates;
Shiller's file of 2026-11-12), cut at 2025-10-31. Writes `research/results/data-long-4.md` and
`.json` (statistics only: no index levels, yields or rates). No signal, rule or strategy
statistic is computed (research/data-long-4.md).

Entry points for a next lane: `cpi`, `policy_rate`, `dividend_yield`, `french_ratios`, `jst`,
`us_yields`, `real_fx_series`.
"""

from __future__ import annotations

import json
import math
import statistics as st
import sys
from collections.abc import Sequence
from datetime import date
from functools import cache
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import long_macro as lm  # noqa: E402
import long_macro_fetch as mf  # noqa: E402
import long_x as lx  # noqa: E402
import long_x_build as lxb  # noqa: E402

RESULTS = HERE.parents[0] / "results"
Series = list[tuple[date, float]]
AREAS = mf.BIS_AREAS
MEI_ID = {
    "GB": "GBRCPIALLMINMEI", "JP": "JPNCPIALLMINMEI", "CH": "CHECPIALLMINMEI",
    "CA": "CANCPIALLMINMEI", "DE": "DEUCPIALLMINMEI", "AU": "AUSCPIALLQINMEI",
    "NZ": "NZLCPIALLQINMEI", "SE": "SWECPIALLMINMEI", "NO": "NORCPIALLMINMEI",
    "US": "USACPIALLMINMEI",
}  # fmt: skip
CUR_AREA = {
    "JPY": "JP", "GBP": "GB", "CHF": "CH", "CAD": "CA", "EUR": "XM", "AUD": "AU",
    "NZD": "NZ", "SEK": "SE", "NOK": "NO",
}  # fmt: skip
FRENCH_CC = ["JP", "GB", "CH", "CA", "DE", "AU", "NZ", "SE", "NO"]
JST_VARS = ["cpi", "stir", "ltrate", "eq_dp", "eq_tr", "eq_capgain", "bill_rate", "bond_tr"]


def root() -> Path:
    return mf.lxf.cache_root() / mf.DIR


# ---------------------------------------------------------------- loaders


@cache
def _bis(name: str) -> dict[str, Series]:
    return lm.parse_bis((root() / "bis" / name).read_text())


def cpi(area: str, annual: bool = False) -> Series:
    """BIS long CPI (2010 = 100). Monthly; AU/NZ repeat the quarter (`lm.QUARTERLY`)."""
    return _bis("cpi-annual.csv" if annual else "cpi-monthly.csv").get(area, [])


def policy_rate(area: str) -> Series:
    return _bis("policy-monthly.csv").get(area, [])


def alfred4(sid: str) -> Series:
    return lx.parse_alfred((root() / f"alfred/{mf.VINTAGE}/{sid}.csv").read_text())


@cache
def _french(with_div: bool) -> dict[str, dict[str, object]]:
    f = mf.FRENCH_FILES[0 if with_div else 1]
    return lm.read_french_zip(root() / f"french/{mf.SNAP}/{f}")


def _mkt(cc: str, with_div: bool, currency: str = "Local") -> Series:
    m: Any = _french(with_div)[cc]["monthly"]
    out: Series = m[(currency, "Not Reqd")]["Mkt"]
    return out


def dividend_yield(cc: str) -> Series:
    """Monthly trailing 12-month dividend yield (percent) of French's value-weight country
    market, local currency, all firms ('Not Reqd')."""
    return lm.dividend_yield(_mkt(cc, True), _mkt(cc, False))


def french_ratios(cc: str) -> dict[str, Series]:
    """Annual value-weight B/M, E/P, CE/P, Yld (percent) and Firms; row t = December t-1."""
    r: Any = _french(True)[cc]["annual_ratios"]
    out: dict[str, Series] = r["Not Reqd"]
    return out


@cache
def _jst() -> dict[str, dict[str, Series]]:
    rows = lx.xlsx_rows(root() / "jst" / "JSTdatasetR6.xlsx", "Sheet1")
    return lm.parse_jst(rows, JST_VARS)


def jst(var: str, area: str) -> Series:
    iso3 = {v: k for k, v in lm.JST_ISO.items()}[area]
    return _jst()[var].get(iso3, [])


def us_yields() -> dict[str, Series]:
    """Shiller monthly: dividend yield D/P and earnings yield E/P (percent), US, 1871 on."""
    import xlrd  # type: ignore[import-untyped]

    p = mf.lxf.cache_root() / "shiller" / "2026-11-12" / "ie_data.xls"
    sheet = xlrd.open_workbook(str(p)).sheet_by_name("Data")
    dp: Series = []
    ep: Series = []
    for i in range(sheet.nrows):
        v = sheet.row_values(i)
        if not isinstance(v[0], float) or not isinstance(v[1], float):
            continue
        y = int(v[0])
        m = round((v[0] - y) * 100)
        if not 1 <= m <= 12 or v[1] <= 0:
            continue
        d = date(y, m, 1)
        if d > lm.LAST:
            break
        if isinstance(v[2], float) and v[2] > 0:
            dp.append((d, 100.0 * v[2] / v[1]))
        if isinstance(v[3], float) and v[3] > 0:
            ep.append((d, 100.0 * v[3] / v[1]))
    return {"D/P": dp, "E/P": ep}


def real_fx_series(cur: str, as_known: bool = True) -> Series:
    """ln(S x P_f / P_us), monthly, from data-long-3's month-end spot and BIS CPI. The euro
    before 1999 is the mark (monthly average) with German CPI.

    as_known=True (default, the only form a signal may use): each CPI as known at the end of the
    spot's month (`lm.real_fx_known`). AUD and NZD use the quarter's CPI (`lm.quarter_ends`)
    only from `lm.available("cpi-quarterly", quarter start)`, not the m+2 monthly rule: BIS's
    AU/NZ "monthly" CPI repeats the quarter's value, so 2025-07 already holds Q3 2025, which
    was published in late October. as_known=False pairs spot and CPI of the same month
    (descriptive only: it looks ahead)."""
    spot, _ = lxb.fx_spot_month_end(cur)
    area = CUR_AREA[cur]
    pf = cpi(area)
    if cur == "EUR":
        xm = dict(pf)
        pf = [(d, v) for d, v in cpi("DE") if d < date(1999, 1, 1)]
        # rescale the euro-area index to continue the German one at 1999-01
        k = dict(cpi("DE"))[date(1999, 1, 1)] / xm[date(1999, 1, 1)]
        pf += [(d, v * k) for d, v in sorted(xm.items()) if d >= date(1999, 1, 1)]
    if as_known:
        return lm.real_fx_known(spot, pf, cpi("US"), quarterly_foreign=area in lm.QUARTERLY)
    return lm.real_fx(spot, pf, cpi("US"))


# ---------------------------------------------------------------- statistics


def span(s: Sequence[tuple[date, float]], fmt: str = "%Y-%m") -> dict[str, Any]:
    if not s:
        return {"start": None, "end": None, "n": 0}
    return {"start": s[0][0].strftime(fmt), "end": s[-1][0].strftime(fmt), "n": len(s)}


def gaps(s: Sequence[tuple[date, float]], step_months: int = 1) -> int:
    """Number of missing steps inside the span."""
    n = 0
    for (a, _), (b, _) in zip(s, s[1:], strict=False):
        k = (b.year - a.year) * 12 + b.month - a.month
        n += max(0, k // step_months - 1)
    return n


def compare(a: Sequence[tuple[date, float]], b: Sequence[tuple[date, float]]) -> dict[str, Any]:
    mb = dict(b)
    pairs = [(v, mb[d]) for d, v in a if d in mb and math.isfinite(v) and math.isfinite(mb[d])]
    if len(pairs) < 3:
        return {"n": len(pairs)}
    x, y = [p[0] for p in pairs], [p[1] for p in pairs]
    return {
        "n": len(pairs),
        "corr": round(st.correlation(x, y), 4),
        "mean_gap": round(st.mean(x) - st.mean(y), 3),
        "mean_abs_gap": round(st.mean(abs(p - q) for p, q in pairs), 3),
        "max_abs_gap": round(max(abs(p - q) for p, q in pairs), 3),
        "from": min(d for d, _ in a if d in mb).strftime("%Y-%m"),
        "to": max(d for d, _ in a if d in mb).strftime("%Y-%m"),
    }


def shift_years(s: Sequence[tuple[date, float]], k: int) -> Series:
    return [(date(d.year + k, d.month, 1), v) for d, v in s]


def decembers(s: Sequence[tuple[date, float]]) -> Series:
    """December values re-dated 1 January of the same year (to meet annual series)."""
    return [(date(d.year, 1, 1), v) for d, v in s if d.month == 12]


def cpi_checks() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for a in AREAS:
        m = cpi(a)
        q = a in lm.QUARTERLY
        row: dict[str, Any] = {
            "monthly": span(m),
            "annual": span(cpi(a, annual=True), "%Y"),
            "quarterly": q,
            "gaps": gaps(lm.quarter_ends(m) if q else m, 3 if q else 1),
            "unbroken_from": span(lx.consecutive(m))["start"],
        }
        if a in MEI_ID:
            mei = alfred4(MEI_ID[a])
            row["mei"] = span(mei)
            if q:  # MEI quarterly is dated the quarter's first month, as BIS's repeats
                row["vs_mei_yoy"] = compare(lm.yoy(lm.quarter_ends(m)), lm.yoy(mei))
            else:
                row["vs_mei_yoy"] = compare(lm.yoy(m), lm.yoy(mei))
        if a == "US":
            row["vs_bls_yoy"] = compare(lm.yoy(m), lm.yoy(alfred4("CPIAUCNS")))
        if a in lm.JST_ISO.values():
            ann = cpi(a, annual=True)
            row["vs_jst_yoy"] = compare(_annual_change(ann), _annual_change(jst("cpi", a)))
        out[a] = row
    return out


def _annual_change(s: Sequence[tuple[date, float]]) -> Series:
    return [
        (d1, 100.0 * (v1 / v0 - 1.0)) for (_, v0), (d1, v1) in zip(s, s[1:], strict=False) if v0 > 0
    ]


def policy_checks() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for a in AREAS:
        p = policy_rate(a)
        row: dict[str, Any] = {
            "span": span(p),
            "gaps": gaps(p),
            "unbroken_from": span(lx.consecutive(p))["start"],
        }
        cc = "EZ" if a == "XM" else a
        sid = f"IR3TIB01{cc}M156N"
        if lxb.has(sid):
            o = lxb.alfred(sid)
            row["oecd3m"] = span(o)
            row["vs_oecd3m"] = compare(p, o)
        if a in lm.JST_ISO.values():
            row["jst_stir"] = span(jst("stir", a), "%Y")
        out[a] = row
    return out


def yield_checks() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for cc in FRENCH_CC:
        dy = dividend_yield(cc)
        r = french_ratios(cc)
        row: dict[str, Any] = {
            "dy_monthly": span(dy),
            "dy_gaps": gaps(dy),
            "ratios": {k: span(v, "%Y") for k, v in r.items() if k != "Firms"},
            "firms_first_last": [r["Firms"][0][1], r["Firms"][-1][1]] if r.get("Firms") else None,
            # French's annual Yld of row t against the derived yield at December t-1 (and t)
            "vs_french_annual_dec_tm1": compare(r["Yld"], shift_years(decembers(dy), 1)),
            "vs_french_annual_dec_t": compare(r["Yld"], decembers(dy)),
        }
        if cc in lm.JST_ISO.values():
            j = [(d, 100.0 * v) for d, v in jst("eq_dp", cc)]
            row["jst_eq_dp"] = span(j, "%Y")
            row["vs_jst_dec_t"] = compare(decembers(dy), j)
            row["vs_jst_dec_tm1"] = compare(shift_years(decembers(dy), 1), j)
            row["french_yld_vs_jst_t"] = compare(r["Yld"], j)
            row["french_yld_vs_jst_tm1"] = compare(shift_years(r["Yld"], -1), j)
        out[cc] = row
    us = us_yields()
    j = [(d, 100.0 * v) for d, v in jst("eq_dp", "US")]
    out["US"] = {
        "shiller_dp": span(us["D/P"]),
        "shiller_ep": span(us["E/P"]),
        "jst_eq_dp": span(j, "%Y"),
        "vs_jst_dec_t": compare(decembers(us["D/P"]), j),
        "vs_jst_dec_tm1": compare(shift_years(decembers(us["D/P"]), 1), j),
    }
    return out


def jst_coverage() -> dict[str, Any]:
    return {v: {a: span(jst(v, a), "%Y") for a in sorted(lm.JST_ISO.values())} for v in JST_VARS}


def share_coverage() -> dict[str, Any]:
    return {s: span(alfred4(s)) for s in mf.SHARES}


def real_fx_coverage() -> dict[str, Any]:
    return {c: span(real_fx_series(c)) for c in CUR_AREA}


# ---------------------------------------------------------------- report


def _c(x: dict[str, Any] | None, key: str = "corr", spec: str = ".3f") -> str:
    if not x or key not in x:
        return "-"
    return format(x[key], spec)


def render(res: dict[str, Any]) -> str:
    L: list[str] = []
    L.append("# data-long-4 results (statistics only)\n")
    L.append("Generated by `research/lib/long_macro_build.py` from the cached files (cut at")
    L.append("2025-10-31). Method and caveats: `research/data-long-4.md`.\n")
    L.append("## Consumer prices (BIS long CPI)\n")
    L.append(
        "| Area | Monthly from | Unbroken from | to | Months | Quarterly? | Gaps | Annual from | "
        "vs OECD MEI 12m infl. corr / mean abs gap (n) | vs JST annual infl. corr / mean abs gap |"
    )
    L.append("|---|---|---|---|---:|---|---:|---|---|---|")
    for a, r in res["cpi"].items():
        m = r.get("vs_mei_yoy")
        j = r.get("vs_jst_yoy")
        mei = f"{_c(m)} / {_c(m, 'mean_abs_gap', '.2f')} ({m['n']})" if m else "-"
        jj = f"{_c(j)} / {_c(j, 'mean_abs_gap', '.2f')}" if j else "-"
        L.append(
            f"| {a} | {r['monthly']['start']} | {r['unbroken_from']} | {r['monthly']['end']} | "
            f"{r['monthly']['n']} | "
            f"{'yes' if r['quarterly'] else 'no'} | {r['gaps']} | {r['annual']['start']} | "
            f"{mei} | {jj} |"
        )
    us = res["cpi"]["US"].get("vs_bls_yoy")
    L.append(
        f"\nUS against BLS `CPIAUCNS`: 12-month inflation corr {_c(us)}, mean abs gap "
        f"{_c(us, 'mean_abs_gap', '.3f')} points, n {us['n'] if us else 0}.\n"
    )
    L.append("## Policy rates (BIS)\n")
    L.append(
        "| Area | From | Unbroken from | to | Months | Gaps | OECD 3m from | "
        "vs OECD 3m: corr / mean gap (n) | JST short rate |"
    )
    L.append("|---|---|---|---|---:|---:|---|---|---|")
    for a, r in res["policy"].items():
        v = r.get("vs_oecd3m")
        o = r.get("oecd3m", {}).get("start", "-")
        js = r.get("jst_stir")
        jt = f"{js['start']}-{js['end']}" if js else "-"
        vv = f"{_c(v)} / {_c(v, 'mean_gap', '+.2f')} ({v['n']})" if v else "-"
        sp = r["span"]
        L.append(
            f"| {a} | {sp['start']} | {r['unbroken_from']} | {sp['end']} | {sp['n']} | "
            f"{r['gaps']} | {o} | {vv} | {jt} |"
        )
    L.append("\n## Equity yields\n")
    L.append(
        "Monthly trailing dividend yield derived from French's returns with and without "
        "dividends; annual ratios as French publishes them (row t = December t-1).\n"
    )
    L.append(
        "| Country | Monthly DY from | to | vs French annual Yld at Dec t-1: corr / mean gap | "
        "(at Dec t) | Annual E/P, B/M from | vs JST eq_dp (Dec t): corr / mean gap (n) | "
        "(Dec t-1) |"
    )
    L.append("|---|---|---|---|---|---|---|---|")
    for cc, r in res["yields"].items():
        if cc == "US":
            continue
        f1, f0 = r["vs_french_annual_dec_tm1"], r["vs_french_annual_dec_t"]
        j0, j1 = r.get("vs_jst_dec_t"), r.get("vs_jst_dec_tm1")
        jt0 = f"{_c(j0)} / {_c(j0, 'mean_gap', '+.2f')} ({j0['n']})" if j0 else "- (not in JST)"
        L.append(
            f"| {cc} | {r['dy_monthly']['start']} | {r['dy_monthly']['end']} | "
            f"{_c(f1)} / {_c(f1, 'mean_gap', '+.2f')} | {_c(f0)} | {r['ratios']['E/P']['start']} | "
            f"{jt0} | {_c(j1)} |"
        )
    u = res["yields"]["US"]
    L.append(
        f"\nUS (Shiller, monthly D/P {u['shiller_dp']['start']}..{u['shiller_dp']['end']}, "
        f"E/P {u['shiller_ep']['start']}..{u['shiller_ep']['end']}): December D/P against JST "
        f"eq_dp of the same year corr {_c(u['vs_jst_dec_t'])} (mean gap "
        f"{_c(u['vs_jst_dec_t'], 'mean_gap', '+.2f')}), of the year before "
        f"{_c(u['vs_jst_dec_tm1'])}.\n"
    )
    L.append("## JST Macrohistory R6 coverage (annual, years)\n")
    areas = sorted(lm.JST_ISO.values())
    L.append("| Variable | " + " | ".join(areas) + " |")
    L.append("|---|" + "---|" * len(areas))
    for v, row in res["jst"].items():
        cells = [f"{row[a]['start']}-{row[a]['end']}" if row[a]["n"] else "-" for a in areas]
        L.append(f"| {v} | " + " | ".join(cells) + " |")
    L.append("\n## OECD MEI share price indices (monthly averages, ALFRED vintage 2025-11-10)\n")
    L.append("| Series | From | to | Months |")
    L.append("|---|---|---|---:|")
    for s, sp in res["shares"].items():
        L.append(f"| `{s}` | {sp['start']} | {sp['end']} | {sp['n']} |")
    L.append(
        "\n## Real exchange rate inputs (month-end spot x BIS CPI ratio, each CPI as known at"
        " the month's end; AUD, NZD by quarter)\n"
    )
    L.append("| Currency | From | to | Months |")
    L.append("|---|---|---|---:|")
    for c, sp in res["real_fx"].items():
        L.append(f"| {c} | {sp['start']} | {sp['end']} | {sp['n']} |")
    return "\n".join(L) + "\n"


def main() -> None:
    res = {
        "cpi": cpi_checks(),
        "policy": policy_checks(),
        "yields": yield_checks(),
        "jst": jst_coverage(),
        "shares": share_coverage(),
        "real_fx": real_fx_coverage(),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "data-long-4.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
    (RESULTS / "data-long-4.md").write_text(render(res))
    print(render(res))


if __name__ == "__main__":
    main()
