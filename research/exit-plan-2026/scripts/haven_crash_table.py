"""Crash table: what "safe havens" did while US stocks fell (descriptive history only).

Lane `haven` of the exit research (research/exit-plan-2026/lanes/haven.md). No strategy, no
fitting: for each crash episode it finds the S&P 500 closing peak and trough inside a fixed
search window, then reports each asset's return

- over the whole drawdown (peak close to trough close),
- over the first 1, 5 and 15 trading days of the worst leg (the 15-trading-day window with the
  worst S&P 500 price return inside the drawdown; day 0 is the close before it),
- on the single worst S&P 500 day of the drawdown,

in USD and, where an exchange rate exists, in EUR (DEM before 1999 is not available here).

Run (data paths are arguments, nothing machine-specific is committed):

    uv run --with xlrd --with openpyxl python -I \
        research/exit-plan-2026/scripts/haven_crash_table.py \
        --cache "$GRIMSTRADE_DATA" --dl <download dir> \
        > research/exit-plan-2026/lanes/haven-table.md

Sources (all public, fetched 2026-11-12 / 2026-11-18, raw files never committed):
- Yahoo chart API v8 daily: ^GSPC, ^IXIC, GC=F, GLD, SHY, IEF, TLT, UUP (cache), BRK-A, OBX.OL
  (OBX total return, NOK), EXX6.DE (iShares eb.rexx Govt Germany 10.5+yr, EUR), EUNH.DE
  (iShares Core EUR Govt Bond), XEON.DE (Xtrackers EUR Overnight Rate Swap 1C), DBXP.DE
  (Xtrackers Eurozone Govt Bond 1-3 1C), all three EUR and from 2008.
- FRED (https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>): DTB3, DGS2, DGS10, DGS30,
  DEXSZUS (CHF per USD), DEXJPUS (JPY per USD), DEXUSEU (USD per EUR), DEXNOUS (NOK per USD).
- Ken French data library, F-F_Research_Data_Factors_daily: RF (1-month T-bill, daily) and
  Mkt = Mkt-RF + RF (US market total return).
- ECB data API FM.M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA (3m Euribor monthly average, EUR cash proxy).
- Shiller ie_data.xls via research/lib/long_bond.py (monthly 10y bond total return, 1929-32).
- World Bank Pink Sheet CMO-Historical-Data-Monthly.xlsx (monthly average gold, 1960-):
  https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx

Approximations, stated in the output: Treasury returns are rebuilt from constant-maturity yields
as par bonds (coupon = yesterday's yield, semiannual, carry by calendar days); FX "cash" returns
are the currency move only, without its interest; gold is the front futures contract (GC=F) from
2000-08-30, spot not available before; BRK-A pays no dividend so price = total return; ^GSPC
and ^IXIC are price indices (no dividends).
"""

from __future__ import annotations

import argparse
import bisect
import csv
import importlib.util
import io
import json
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
YAHOO_CACHE = "yahoo-1d/2026-11-12"
FRENCH = "french/2026-11-12/F-F_Research_Data_Factors_daily_CSV.zip"


class Series:
    """Daily level series; value(d) = last observation on or before d."""

    def __init__(self, points: dict[date, float]) -> None:
        self.days = sorted(points)
        self.vals = [points[d] for d in self.days]

    def value(self, d: date) -> float | None:
        i = bisect.bisect_right(self.days, d) - 1
        if i < 0:
            return None
        # stale by more than 10 calendar days counts as missing (series not started / gap)
        if (d - self.days[i]).days > 10:
            return None
        return self.vals[i]

    def ret(self, a: date, b: date) -> float | None:
        va, vb = self.value(a), self.value(b)
        if va is None or vb is None:
            return None
        return vb / va - 1.0

    @property
    def first(self) -> date:
        return self.days[0]


def yahoo(path: Path, field: str = "adjclose") -> Series:
    r = json.loads(path.read_text())["chart"]["result"][0]
    off = timedelta(seconds=r["meta"].get("gmtoffset", 0))
    if field == "adjclose" and "adjclose" in r["indicators"]:
        vals = r["indicators"]["adjclose"][0]["adjclose"]
    else:
        vals = r["indicators"]["quote"][0]["close"]
    pts: dict[date, float] = {}
    for t, v in zip(r["timestamp"], vals, strict=True):
        if v is not None and v > 0:
            pts[(datetime.fromtimestamp(t, UTC) + off).date()] = float(v)
    return Series(pts)


def fred(path: Path) -> dict[date, float]:
    out: dict[date, float] = {}
    with path.open() as f:
        rows = csv.reader(f)
        next(rows)
        for d, v in rows:
            if v not in ("", "."):
                out[date.fromisoformat(d)] = float(v)
    return out


def inverse(points: dict[date, float]) -> Series:
    """FRED quotes 'foreign units per USD'; the USD value of one foreign unit is 1/x."""
    return Series({d: 1.0 / v for d, v in points.items()})


def bond_index(yields: dict[date, float], maturity: float) -> Series:
    """Total-return index of a constant-maturity par bond rebuilt from daily yields (%)."""
    days = sorted(yields)
    level, pts = 1.0, {days[0]: 1.0}
    n = int(round(maturity * 2))
    for prev, cur in zip(days, days[1:], strict=False):
        c, y = yields[prev] / 100.0, yields[cur] / 100.0
        dt = (cur - prev).days / 365.0
        disc = (1 + y / 2) ** -n
        price = (c / y) * (1 - disc) + disc if y > 0 else 1 + c / 2 * n
        level *= price + c * dt
        pts[cur] = level
    return Series(pts)


def bill_index(yields: dict[date, float]) -> Series:
    days = sorted(yields)
    level, pts = 1.0, {days[0]: 1.0}
    for prev, cur in zip(days, days[1:], strict=False):
        level *= 1 + yields[prev] / 100.0 * (cur - prev).days / 365.0
        pts[cur] = level
    return Series(pts)


def french(path: Path) -> tuple[Series, Series]:
    text = zipfile.ZipFile(path).read("F-F_Research_Data_Factors_daily.csv").decode()
    rf_level, mkt_level = 1.0, 1.0
    rf_pts: dict[date, float] = {}
    mkt_pts: dict[date, float] = {}
    for row in csv.reader(io.StringIO(text)):
        if len(row) != 5 or not row[0].strip().isdigit() or len(row[0].strip()) != 8:
            continue
        d = datetime.strptime(row[0].strip(), "%Y%m%d").date()
        mkt_rf, rf = float(row[1]) / 100, float(row[4]) / 100
        rf_level *= 1 + rf
        mkt_level *= 1 + mkt_rf + rf
        rf_pts[d], mkt_pts[d] = rf_level, mkt_level
    return Series(rf_pts), Series(mkt_pts)


def euribor_cash(path: Path) -> Series:
    """EUR cash proxy: accrue the monthly-average 3m Euribor day by day (calendar days)."""
    rates: dict[tuple[int, int], float] = {}
    with path.open() as f:
        for row in csv.DictReader(f):
            y, m = row["TIME_PERIOD"].split("-")
            rates[(int(y), int(m))] = float(row["OBS_VALUE"])
    start = date(min(rates)[0], min(rates)[1], 1)
    end = date(2026, 11, 1)
    level, d, pts = 1.0, start, {}
    while d <= end:
        r = rates.get((d.year, d.month))
        if r is None:
            break
        pts[d] = level
        level *= 1 + r / 100 / 365
        d += timedelta(days=1)
    return Series(pts)


def shiller_bond(cache: Path) -> Series:
    spec = importlib.util.spec_from_file_location("long_bond", ROOT / "research/lib/long_bond.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rets = mod.load(cache / "shiller" / "ie_data.xls")
    # month m's return runs from the start of month m to the start of month m+1
    level, pts = 1.0, {}
    for d, r in rets:
        pts[d] = level
        level *= r
    return Series(pts)


def wb_gold(path: Path) -> dict[tuple[int, int], float]:
    """World Bank Pink Sheet monthly average gold price ($/toz), sheet 'Monthly Prices'."""
    openpyxl = importlib.import_module("openpyxl")
    ws = openpyxl.load_workbook(path, read_only=True)["Monthly Prices"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = next(r for r in rows if r and "Gold" in [str(c) for c in r])
    col = [str(c) for c in hdr].index("Gold")
    out: dict[tuple[int, int], float] = {}
    for r in rows:
        k = r[0]
        if isinstance(k, str) and len(k) == 7 and k[4] == "M" and isinstance(r[col], int | float):
            out[(int(k[:4]), int(k[5:]))] = float(r[col])
    return out


@dataclass
class Episode:
    name: str
    search_from: date
    search_to: date
    note: str = ""


EPISODES = [
    Episode("1929-32 Great Crash", date(1929, 8, 1), date(1932, 12, 31), "monthly bonds"),
    Episode("1973-74 stagflation", date(1973, 1, 1), date(1974, 12, 31)),
    Episode("1987 Black Monday", date(1987, 8, 1), date(1987, 12, 31)),
    Episode("2000-02 dot-com", date(2000, 3, 1), date(2002, 12, 31)),
    Episode("2007-09 GFC", date(2007, 10, 1), date(2009, 3, 31)),
    Episode("2008 Lehman leg", date(2008, 9, 12), date(2008, 11, 30), "sub-leg of GFC"),
    Episode("2020 Covid", date(2020, 2, 1), date(2020, 3, 31)),
    Episode("2022 inflation", date(2022, 1, 1), date(2022, 10, 31)),
    Episode("2024 Aug carry unwind", date(2024, 7, 1), date(2024, 8, 9)),
    Episode("2025 tariff shock", date(2025, 2, 1), date(2025, 4, 30)),
]


def peak_trough(spx: Series, ep: Episode) -> tuple[date, date]:
    idx = [i for i, d in enumerate(spx.days) if ep.search_from <= d <= ep.search_to]
    # trough first (lowest close), then the highest close before it
    t = min(idx, key=lambda i: spx.vals[i])
    p = max((i for i in idx if i <= t), key=lambda i: spx.vals[i])
    if ep.name.startswith("2008 Lehman"):
        p = idx[0]  # fixed start: close of Fri 2008-09-12, before the Lehman weekend
    return spx.days[p], spx.days[t]


def worst_leg(spx: Series, p: date, t: date, n: int = 15) -> tuple[date, int]:
    i0, i1 = spx.days.index(p), spx.days.index(t)
    n = min(n, i1 - i0)
    best = min(range(i0, i1 - n + 1), key=lambda i: spx.vals[i + n] / spx.vals[i])
    return spx.days[best], best


def fmt(x: float | None) -> str:
    return "n/a" if x is None else f"{x * 100:+.1f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, required=True, help="GRIMSTRADE_DATA root")
    ap.add_argument("--dl", type=Path, required=True, help="lane download dir")
    a = ap.parse_args()
    yc, dl = a.cache / YAHOO_CACHE, a.dl

    spx = yahoo(yc / "^GSPC.json", "close")
    rf, mkt = french(a.cache / FRENCH)
    usd_per_eur = Series(fred(dl / "fred_DEXUSEU.csv"))
    eur_cash = euribor_cash(dl / "ecb_estr_like_eonia.csv")
    nok = fred(dl / "fred_DEXNOUS.csv")

    def gold_usd() -> Series:
        return yahoo(yc / "GC=F.json", "close")

    usd_assets: dict[str, Callable[[], Series]] = {
        "US stocks TR (French Mkt)": lambda: mkt,
        "Nasdaq Comp.": lambda: yahoo(yc / "^IXIC.json", "close"),
        "T-bills (French RF)": lambda: rf,
        "UST 2y (DGS2)": lambda: bond_index(fred(dl / "fred_DGS2.csv"), 2),
        "UST 10y (DGS10)": lambda: bond_index(fred(dl / "fred_DGS10.csv"), 10),
        "UST 30y (DGS30)": lambda: bond_index(fred(dl / "fred_DGS30.csv"), 30),
        "Gold (GC=F)": gold_usd,
        "CHF": lambda: inverse(fred(dl / "fred_DEXSZUS.csv")),
        "JPY": lambda: inverse(fred(dl / "fred_DEXJPUS.csv")),
        "EUR": lambda: usd_per_eur,
        "Berkshire (BRK-A)": lambda: yahoo(dl / "y_BRK-A.json", "close"),
        "SHY ETF": lambda: yahoo(yc / "SHY.json"),
        "IEF ETF": lambda: yahoo(yc / "IEF.json"),
        "TLT ETF": lambda: yahoo(yc / "TLT.json"),
        "GLD ETF": lambda: yahoo(yc / "GLD.json"),
    }
    loaded = {k: f() for k, f in usd_assets.items()}
    loaded["US 10y (Shiller, monthly)"] = shiller_bond(a.cache)

    # EUR investor: USD asset converted at USD/EUR; EUR assets as they are.
    def in_eur(s: Series) -> Callable[[date, date], float | None]:
        def f(x: date, y: date) -> float | None:
            r, fx = s.ret(x, y), usd_per_eur.ret(x, y)
            if r is None or fx is None:
                return None
            return (1 + r) / (1 + fx) - 1

        return f

    obx_nok = yahoo(dl / "y_OBX.OL.json", "close")
    # NOK per EUR = (NOK per USD) * (USD per EUR). Fixed 2026-11-18 (review round 1): this
    # used to divide, which gave EUR/NOK near 4 in 2007-08 and overstated OBX losses in EUR.
    nok_per_eur = Series(
        {d: v * fx for d, v in nok.items() if (fx := usd_per_eur.value(d)) is not None}
    )
    pairs = zip(nok_per_eur.days, nok_per_eur.vals, strict=True)
    bad = [(d, x) for d, x in pairs if not 6.0 <= x <= 15.0]
    assert not bad, f"EUR/NOK outside 6-15, conversion is wrong: {bad[:3]}"

    def obx_eur(x: date, y: date) -> float | None:
        r, fx = obx_nok.ret(x, y), nok_per_eur.ret(x, y)
        return None if r is None or fx is None else (1 + r) / (1 + fx) - 1

    eur_cols: dict[str, Callable[[date, date], float | None]] = {
        "S&P 500 in EUR": in_eur(spx),
        "EUR cash (3m Euribor)": eur_cash.ret,
        "EUR o/n swap ETF (XEON.DE)": yahoo(dl / "y_XEON.DE.json").ret,
        "EZ govt 1-3y (DBXP.DE)": yahoo(dl / "y_DBXP.DE.json").ret,
        "Bund 10.5y+ (EXX6.DE)": yahoo(dl / "y_EXX6.DE.json").ret,
        "EUR govt all (EUNH.DE)": yahoo(dl / "y_EUNH.DE.json").ret,
        "UST 10y in EUR": in_eur(loaded["UST 10y (DGS10)"]),
        "T-bills in EUR": in_eur(rf),
        "Gold in EUR": in_eur(loaded["Gold (GC=F)"]),
        "CHF in EUR": in_eur(loaded["CHF"]),
        "JPY in EUR": in_eur(loaded["JPY"]),
        "Berkshire in EUR": in_eur(loaded["Berkshire (BRK-A)"]),
        "OBX TR (Oslo) in EUR": obx_eur,
    }

    print("# Crash table (generated by scripts/haven_crash_table.py; descriptive only)\n")
    print("Returns in percent. 'n/a' = no data for that asset on those dates. Day 0 of the")
    print("worst leg is the close before the worst 15-trading-day S&P 500 fall inside the")
    print("drawdown. Treasuries rebuilt from constant-maturity yields; FX = currency move only.")
    print("'worst point' = the asset's lowest cumulative return, measured from the equity peak,")
    print("at any close up to the trough (how far under water a holder was at the worst moment).")
    print("'own max drawdown' = the asset's own largest peak-to-trough fall inside the window.")
    print("Oslo (OBX) closes before New York, so its 1-day numbers are not the same session.\n")
    print("Correction 2026-11-18 (review round 1): the OBX-in-EUR column used EUR/NOK =")
    print("(NOK per USD) / (USD per EUR), which is wrong; it is now (NOK per USD) * (USD per EUR),")
    print("checked to lie in 6-15. Every OBX-in-EUR cell changed; no other column did.\n")

    rows: list[tuple[Episode, date, date, date, int]] = []
    print("## Episodes (S&P 500 closes, ^GSPC price index)\n")
    print("| Episode | Peak | Trough | Trading days | S&P 500 | Worst leg start | Worst 15d |")
    print("|---|---|---|---|---|---|---|")
    for ep in EPISODES:
        p, t = peak_trough(spx, ep)
        ls, li = worst_leg(spx, p, t)
        n = spx.days.index(t) - spx.days.index(p)
        leg15 = spx.days[min(li + 15, spx.days.index(t))]
        rows.append((ep, p, t, ls, li))
        print(
            f"| {ep.name} | {p} | {t} | {n} | {fmt(spx.ret(p, t))} | {ls} | "
            f"{fmt(spx.ret(ls, leg15))} |"
        )

    def windows(p: date, t: date, ls: date, li: int) -> list[tuple[str, date, date]]:
        ti = spx.days.index(t)
        wd_i = min(
            range(spx.days.index(p) + 1, ti + 1), key=lambda i: spx.vals[i] / spx.vals[i - 1]
        )
        return [
            ("whole drawdown", p, t),
            ("leg 1d", ls, spx.days[min(li + 1, ti)]),
            ("leg 5d", ls, spx.days[min(li + 5, ti)]),
            ("leg 15d", ls, spx.days[min(li + 15, ti)]),
            (f"worst day {spx.days[wd_i]}", spx.days[wd_i - 1], spx.days[wd_i]),
            ("worst point", p, t),
            ("own max drawdown", p, t),
        ]

    def own_mdd(f: Callable[[date, date], float | None], p: date, t: date) -> float | None:
        """The asset's own largest peak-to-trough fall between the equity peak and trough."""
        days = spx.days[spx.days.index(p) : spx.days.index(t) + 1]
        lv = [(1 + r) for r in (f(p, d) for d in days) if r is not None]
        if not lv:
            return None
        hi, worst = lv[0], 0.0
        for v in lv:
            hi = max(hi, v)
            worst = min(worst, v / hi - 1)
        return worst

    def worst_point(f: Callable[[date, date], float | None], p: date, t: date) -> float | None:
        """Lowest cumulative return from the equity peak at any close up to the trough."""
        days = spx.days[spx.days.index(p) : spx.days.index(t) + 1]
        vals = [r for r in (f(p, d) for d in days) if r is not None]
        return min(vals) if vals else None

    print("\n## USD view (asset return in USD, %)\n")
    names = ["S&P 500"] + list(loaded)
    print("| Episode | Window | " + " | ".join(names) + " |")
    print("|---|---|" + "---|" * len(names))
    for ep, p, t, ls, li in rows:
        for label, x, y in windows(p, t, ls, li):
            if label in ("worst point", "own max drawdown"):
                stat = worst_point if label == "worst point" else own_mdd
                cells = [fmt(stat(spx.ret, x, y))]
                for k, s in loaded.items():
                    monthly = k.startswith("US 10y (Shiller")
                    cells.append("n/a" if monthly else fmt(stat(s.ret, x, y)))
                print(f"| {ep.name} | {label} | " + " | ".join(cells) + " |")
                continue
            cells = [fmt(spx.ret(x, y))]
            for k, s in loaded.items():
                if k.startswith("US 10y (Shiller") and label != "whole drawdown":
                    cells.append("n/a")
                    continue
                if k.startswith("US 10y (Shiller"):
                    # monthly: from the month of the peak to the month of the trough
                    cells.append(fmt(s.ret(x.replace(day=1), y.replace(day=1))))
                    continue
                cells.append(fmt(s.ret(x, y)))
            print(f"| {ep.name} | {label} | " + " | ".join(cells) + " |")

    print("\n## EUR view (return to a euro-based holder, %; 1999 onwards)\n")
    en = list(eur_cols)
    print("| Episode | Window | " + " | ".join(en) + " |")
    print("|---|---|" + "---|" * len(en))
    for ep, p, t, ls, li in rows:
        if p.year < 1999:
            continue
        for label, x, y in windows(p, t, ls, li):
            if label == "worst point":
                cells = [fmt(worst_point(f, x, y)) for f in eur_cols.values()]
            elif label == "own max drawdown":
                cells = [fmt(own_mdd(f, x, y)) for f in eur_cols.values()]
            else:
                cells = [fmt(f(x, y)) for f in eur_cols.values()]
            print(f"| {ep.name} | {label} | " + " | ".join(cells) + " |")

    gold_m = wb_gold(dl / "wb_cmo_monthly.xlsx")
    print("\n## Gold from monthly averages (World Bank Pink Sheet), peak month to trough month\n")
    print("Covers the episodes before GC=F starts; a monthly average blurs the short run.\n")
    print("| Episode | From | To | Gold USD |")
    print("|---|---|---|---|")
    for ep, p, t, _, _ in rows:
        a0, b0 = gold_m.get((p.year, p.month)), gold_m.get((t.year, t.month))
        r = None if a0 is None or b0 is None else b0 / a0 - 1
        print(f"| {ep.name} | {p:%Y-%m} | {t:%Y-%m} | {fmt(r)} |")

    print("\n## Data starts\n")
    for k, s in loaded.items():
        print(f"- {k}: {s.first}")
    print(f"- EUR/USD (DEXUSEU): {usd_per_eur.first}; Euribor cash: {eur_cash.first}")
    print(f"- OBX TR: {obx_nok.first}")


if __name__ == "__main__":
    main()
