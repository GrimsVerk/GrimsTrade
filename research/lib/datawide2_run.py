# ruff: noqa: E501  (report table strings)
"""data-wide-2: count new market-years and falls of 25%+ per cached keyless source.

    uv run python -I research/lib/datawide2_run.py

Reads the git-ignored cache (`<cache_root>/data-wide-2/...` and the BoE / Norges Bank stock
copies cached by jst-autocorr-2), writes `research/results/data-wide-2.md` and `.json`.
Descriptive data counts only: no rule, no strategy, no return statistic.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide2 as dw  # noqa: E402

OUT = dw.ROOT / "research" / "results"


def splice(a: dw.Monthly, b: dw.Monthly, name: str) -> dw.Monthly:
    """a, then b rescaled at a's last month (b must contain that month)."""
    last = a.months[-1]
    if last not in b.months:
        return a
    k = a.level[-1] / b.level[b.months.index(last)]
    pts = list(zip(a.months, a.level, strict=True))
    pts += [(m, v * k) for m, v in zip(b.months, b.level, strict=True) if m > last]
    return dw.from_points(name, a.asset, a.market, pts, timing=a.timing)


def load_all() -> dict[str, list[dw.Monthly]]:
    root = dw.cache_root()
    w2 = root / "data-wide-2"
    src: dict[str, list[dw.Monthly]] = {}

    # Yale ICF
    y = w2 / "yale" / "2026-11-25"
    with zipfile.ZipFile(y / "Totaldata.zip") as z:
        text = z.read("Totaldata.csv").decode("utf-8", errors="replace")
    rows = list(csv.DictReader(io.StringIO(text)))
    src["Yale IMM government bonds 1869-1929"] = dw.parse_imm_rows(rows, "Government Bond")
    src["Yale IMM common stocks 1869-1929 (file truncated)"] = dw.parse_imm_rows(
        rows, "Common Stock"
    )
    src["Yale IMM government bonds, 3+ quotes a month"] = dw.parse_imm_rows(
        rows, "Government Bond", min_pairs=3
    )
    src["Yale IMM common stocks, 3+ quotes a month"] = dw.parse_imm_rows(
        rows, "Common Stock", min_pairs=3
    )
    import xlrd  # dev dependency

    sh = xlrd.open_workbook(str(y / "SPSENYSE18651917ind.xls")).sheet_by_index(0)
    spse = dw.parse_spse_nyse([sh.row_values(i) for i in range(sh.nrows)])
    src["Yale St Petersburg SE 1865-1917"] = [spse[1]]
    nyse = dw.parse_yale_nyse((y / "Price-Weighted-Index-Returns-2020-08-20.xls").read_text())
    src["Yale NYSE 1815-1925"] = [nyse]

    # Norges Bank HMS
    p = w2 / "probe"
    stock_rows = dw.read_xlsx_rows(root / "jst-autocorr-2" / "nb" / "stockprices.xlsx", 1)
    src["Norges Bank stocks 1914-2001"] = [
        dw.from_points(
            "Norges Bank stock index, total",
            "stock",
            "NOR",
            dw.parse_labelled_columns(stock_rows, 1),
            timing="mixed",
        )
    ]
    b1 = dw.read_xlsx_rows(p / "nb-bond_yields.xlsx", "p1_c4_table_A1_Monthly")
    gov = dw.parse_labelled_columns(b1, dw.find_col(b1, "GOV"))
    src["Norges Bank government bond yields 1820-"] = [
        dw.from_points(
            "Norges Bank long govt bond (price 1/y)",
            "bond",
            "NOR",
            dw.yields_to_price(gov),
            timing="month-end",
        )
    ]
    f1 = dw.read_xlsx_rows(p / "nb-fx.xlsx", "p1_c7_Table_A1")
    lon = [(m, 1 / v) for m, v in dw.parse_labelled_columns(f1, dw.find_col(f1, "LONDON"))]
    f2 = dw.read_xlsx_rows(p / "nb-fx.xlsx", "p1_c7_Table_A2")
    usd = [(m, 1 / v) for m, v in dw.parse_labelled_columns(f2, dw.find_col(f2, "USD"))]
    src["Norges Bank exchange rates 1819-"] = [
        dw.from_points(
            "NOK in GBP 1819-1914 (Oslo, end of month)", "fx", "NOR", lon, timing="month-end"
        ),
        dw.from_points(
            "NOK in USD 1914- (monthly average)", "fx", "NOR-USD", usd, timing="average"
        ),
    ]

    # SNB historical capital-market tables
    bk = xlrd.open_workbook(str(p / "snb-histz_km.xls"))

    def snb(sheet: str, col: int = 1) -> list[tuple[int, float]]:
        s = bk.sheet_by_name(sheet)
        return dw.parse_labelled_columns([s.row_values(i) for i in range(s.nrows)], col)

    eq = dw.from_points(
        "SNB equity index 1924-1968", "stock", "CHE", snb("T 8.1 p.m."), timing="month-end"
    )
    eq2 = dw.from_points(
        "SBC equity index 1959-1997", "stock", "CHE", snb("T 8.3 p.m."), timing="month-end"
    )
    src["SNB Swiss equity 1924-1997"] = [
        splice(eq, eq2, "SNB 1924-1968 + SBC 1968-1997 equity index")
    ]
    src["SNB Swiss bond price index 1943-1981"] = [
        dw.from_points(
            "SNB bond index, price", "bond", "CHE", snb("T 10.2 p.m."), timing="month-end"
        )
    ]

    # DBnomics mirrors (trimmed to 2025-10 at fetch)
    d = w2 / "dbnomics" / "2026-11-25"
    src["OECD MEI share prices (DBnomics)"] = dw.parse_dbnomics(
        (d / "oecd-finmark-share-m.json").read_text(), "stock"
    )
    src["OECD MEI share prices (DBnomics)"] = [
        s for s in src["OECD MEI share prices (DBnomics)"] if not s.market.startswith("EA")
    ]
    src["IMF IFS share prices (DBnomics)"] = dw.parse_dbnomics(
        (d / "imf-ifs-FPE_IX-m.json").read_text(), "stock", iso2=True
    )
    fx = dw.parse_dbnomics(
        (d / "imf-ifs-ENDA_XDC_USD_RATE-m.json").read_text(), "fx", invert=True, iso2=True
    )
    src["IMF IFS exchange rates vs USD (DBnomics)"] = [
        s
        for s in fx
        if s.market.isalpha() and s.market not in ("US", "USA") and s.market[0] not in "1234567"
    ]
    by = dw.parse_dbnomics((d / "imf-ifs-FIGB_PA-m.json").read_text(), "bond", iso2=True)
    src["IMF IFS government bond yields (DBnomics)"] = [
        dw.from_points(
            s.name + " (price 1/y)",
            "bond",
            s.market,
            dw.yields_to_price(zip(s.months, s.level, strict=True)),
            timing="average",
        )
        for s in by
    ]

    # AQR
    aq = dw.read_xlsx_rows(p / "aqr-comlr-monthly.xlsx", 0)
    src["AQR Commodities for the Long Run 1877-"] = [dw.parse_aqr_comlr(aq)]

    # BoE millennium monthly sheet (long CSV, cached by jst-autocorr-2)
    t = (root / "jst-autocorr-2" / "boe" / "monthly.csv").read_text()
    src["BoE millennium monthly sheet"] = [
        dw.parse_boe_long_csv(t, "spliced-monthly-share-price-index", "stock"),
        dw.parse_boe_long_csv(t, "long-term-consols-yield", "bond", yield_=True),
        dw.parse_boe_long_csv(t, "monthly-corporate-bond-yields", "bond", "GBR-corp", yield_=True),
        dw.parse_boe_long_csv(t, "usd-gbp-exchange-rate", "fx", "GBR"),
    ]
    return src


def main() -> None:
    src = load_all()
    table, union, union_falls, detail = [], defaultdict(set), defaultdict(set), {}
    for name, series in src.items():
        cs = [dw.count_new(s) for s in series if len(s.months) >= 24]
        tot = {
            "source": name,
            "series": len(cs),
            "months": sum(c.months for c in cs),
            "new_market_years": sum(c.new_years for c in cs),
            "new_calendar_years": len(
                {
                    y
                    for s in series
                    for y in dw.years_covered(s.months)
                    if not dw.seen_calendar(s.asset, y) and not dw.seen(s.asset, s.market, y)
                }
            ),
            "falls_new": sum(c.falls_new for c in cs),
            "falls_all": sum(c.falls_all for c in cs),
        }
        table.append(tot)
        detail[name] = [asdict(c) for c in cs]
        if "3+" in name:
            continue  # a cleaner variant of a source already in the union
        for s in series:
            if len(s.months) < 24:
                continue
            new = {y for y in dw.years_covered(s.months) if not dw.seen(s.asset, s.market, y)}
            base = s.market[:3]
            union[s.asset] |= {(base, y) for y in new}
            for f in dw.falls(s.months, s.level):
                if f[1] // 12 in new:
                    union_falls[s.asset].add((base, f[1] // 12))
    table.sort(key=lambda r: -r["new_market_years"])
    lines = [
        "# data-wide-2: new market-years and falls of 25%+ per source",
        "",
        "Generated by `research/lib/datawide2_run.py` from the local cache; descriptive counts only (no rule,",
        "no strategy). A market-year counts with at least 6 monthly points; 'new' = not in `SEEN`",
        "(`research/lib/datawide2.py`); falls are peak-to-trough >= 25% of the monthly level, one per",
        "episode, counted when the trough falls in a new year. Months after 2025-10 are dropped.",
        "",
        "| Source | Series | Months | New market-years | New calendar years | Falls 25%+ in new years | Falls 25%+ all years |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in table:
        lines.append(
            f"| {r['source']} | {r['series']} | {r['months']:,} | {r['new_market_years']:,} | {r['new_calendar_years']} | {r['falls_new']} | {r['falls_all']} |"
        )
    lines += [
        "",
        "Union across sources (a country-year counted once per asset class; markets by first 3 letters):",
        "",
    ]
    lines += ["| Asset | New market-years | Falls 25%+ in new years |", "|---|---:|---:|"]
    for a in sorted(union):
        lines.append(f"| {a} | {len(union[a]):,} | {len(union_falls[a])} |")
    lines += ["", "## Per series (sources with up to 60 series; the full list is in the .json)", ""]
    for name, cs in detail.items():
        if len(cs) > 60:
            continue
        lines += [
            f"### {name}",
            "",
            "| Series | Market | First | Last | Months | New years | Falls new / all |",
            "|---|---|---|---|---:|---:|---:|",
        ]
        for c in sorted(cs, key=lambda c: -c["new_years"]):
            lines.append(
                f"| {c['name']} | {c['market']} | {c['first']} | {c['last']} | {c['months']} | {c['new_years']} | {c['falls_new']} / {c['falls_all']} |"
            )
        lines.append("")
    OUT.mkdir(exist_ok=True)
    (OUT / "data-wide-2.md").write_text("\n".join(lines) + "\n")
    (OUT / "data-wide-2.json").write_text(
        json.dumps({"table": table, "detail": detail}, indent=1) + "\n"
    )
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()
