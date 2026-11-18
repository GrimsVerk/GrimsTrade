"""combo-2, step 2 (description only): what commodity proxies did when US stocks and bonds
were both out of trend, 1962-2025, monthly.

    uv run --with numpy python research/lib/combo2_longrun.py

Card: research/combo-2.md, "Step 2 card", "1970s-style co-falls". Nothing here is a test or a
try: no strategy is chosen, the gym is not used. Inputs from the data cache (`cache_root` in
research/macro.local.json), read as data only:

- US stocks: Fama-French market return (Mkt-RF + RF) and the 1-month T-bill (RF), monthly.
- 10-year Treasury: FRED DGS10 (daily, from 1962), month-end yield; the month's return of a
  10-year par bond bought at last month's yield (coupon carry plus the price change).
- Gold: datahub monthly gold price (a monthly average, no yield), from 1833.
- S&P GSCI: Yahoo `^SPGSCI` monthly closes (from 1985), fetched keyless into the cache.

Gate at the end of month t: the stock and the bond 12-month total returns both <= 0 (the step-2
rule's gate, monthly). Partner trend: the proxy's 12-month change > 0. Returns of month t + 1.
Writes research/results/combo-2-longrun.md.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from datetime import UTC, date, datetime

import macro
import numpy as np

ROOT = macro.cache_root()
RESULT = macro.RESEARCH / "results" / "combo-2-longrun.md"
Month = tuple[int, int]


def french() -> tuple[dict[Month, float], dict[Month, float]]:
    z = zipfile.ZipFile(ROOT / "french" / "2026-11-12" / "F-F_Research_Data_Factors_CSV.zip")
    text = z.read(z.namelist()[0]).decode("latin1")
    mkt: dict[Month, float] = {}
    rf: dict[Month, float] = {}
    for row in csv.reader(io.StringIO(text)):
        if len(row) == 5 and row[0].strip().isdigit() and len(row[0].strip()) == 6:
            ym = (int(row[0][:4]), int(row[0][4:6]))
            if ym in mkt:  # the annual block repeats years as 4-digit keys; 6-digit only
                break
            mkt[ym] = (float(row[1]) + float(row[4])) / 100
            rf[ym] = float(row[4]) / 100
    return mkt, rf


def dgs10() -> dict[Month, float]:
    """Month-end 10-year yield (fraction)."""
    path = sorted((ROOT / "fred" / "api" / "latest" / "DGS10").glob("*.json"))[-1]
    obs = json.loads(path.read_text())["observations"]
    out: dict[Month, float] = {}
    for o in obs:
        if o["value"] not in (".", ""):
            d = date.fromisoformat(o["date"])
            out[(d.year, d.month)] = float(o["value"]) / 100  # last one in the month wins
    return out


def bond_returns(y: dict[Month, float]) -> dict[Month, float]:
    """A 10-year par bond bought at last month's yield, repriced a month later."""
    ms = sorted(y)
    out = {}
    for a, b in zip(ms, ms[1:], strict=False):
        c, y1, n = y[a], y[b], 2 * (10 - 1 / 12)
        v = 1 / (1 + y1 / 2)
        price = (c / 2) * (1 - v**n) / (y1 / 2) + v**n if y1 > 0 else 1 + c / 2 * n
        out[b] = price - 1 + c / 12
    return out


def gold() -> dict[Month, float]:
    path = ROOT / "datahub-gold" / "2026-11-18" / "monthly.csv"
    with path.open() as f:
        return {
            (int(r["Date"][:4]), int(r["Date"][5:7])): float(r["Price"]) for r in csv.DictReader(f)
        }


def gsci() -> dict[Month, float]:
    path = ROOT / "yahoo-1d" / "combo2-spgsci" / "SPGSCI.json"
    r = json.loads(path.read_text())["chart"]["result"][0]
    out = {}
    for t, x in zip(r["timestamp"], r["indicators"]["quote"][0]["close"], strict=True):
        if x is not None:
            d = datetime.fromtimestamp(
                t + 86400, UTC
            ).date()  # Yahoo stamps month starts at 04-05 UTC
            out[(d.year, d.month)] = float(x)
    return out


def chg(level: dict[Month, float], m: Month, k: int) -> float | None:
    y, mo = m
    back = (y + (mo - 1 - k) // 12, (mo - 1 - k) % 12 + 1)
    if m in level and back in level:
        return level[m] / level[back] - 1
    return None


def nxt(m: Month) -> Month:
    return (m[0] + m[1] // 12, m[1] % 12 + 1)


def main() -> None:
    mkt, rf = french()
    bond = bond_returns(dgs10())
    au, gs = gold(), gsci()
    months = sorted(set(mkt) & set(bond))
    # cumulative levels for 12-month returns
    lv_s: dict[Month, float] = {}
    lv_b: dict[Month, float] = {}
    s = b = 1.0
    for m in months:
        s *= 1 + mkt[m]
        b *= 1 + bond[m]
        lv_s[m], lv_b[m] = s, b
    rows: list[tuple[Month, bool, float, float, float | None, float | None, bool, bool]] = []
    for m in months:
        n1 = nxt(m)
        if n1 not in mkt or n1 not in bond:
            continue
        s12, b12 = chg(lv_s, m, 12), chg(lv_b, m, 12)
        if s12 is None or b12 is None:
            continue
        g_au = chg(au, n1, 1)
        g_gs = chg(gs, n1, 1)
        au_on = (chg(au, m, 12) or 0) > 0
        gs_on = (chg(gs, m, 12) or 0) > 0
        rows.append((n1, s12 <= 0 and b12 <= 0, mkt[n1], rf[n1], g_au, g_gs, au_on, gs_on))

    def spans(sel: list[Month]) -> str:
        if not sel:
            return "none"
        out, a, p = [], sel[0], sel[0]
        for m in sel[1:]:
            if m != nxt(p):
                out.append((a, p))
                a = m
            p = m
        out.append((a, p))
        return ", ".join(f"{x[0]}-{x[1]:02d}..{y[0]}-{y[1]:02d}" for x, y in out)

    def stats_for(lo: int, hi: int) -> list[str]:
        sel = [r for r in rows if lo <= r[0][0] <= hi and r[1]]
        if not sel:
            return [f"| {lo}-{hi} | 0 | | | | | | | |"]

        def ann(xs: list[float]) -> str:
            return f"{np.mean(xs) * 1200:+.1f}" if xs else "-"

        au_x = [r[4] for r in sel if r[4] is not None]
        au_t = [r[4] if r[6] else r[3] for r in sel if r[4] is not None]
        gs_x = [r[5] for r in sel if r[5] is not None]
        gs_t = [r[5] + r[3] if r[7] else r[3] for r in sel if r[5] is not None]
        return [
            f"| {lo}-{hi} | {len(sel)} | {ann([r[2] for r in sel])} | {ann([r[3] for r in sel])} |"
            f" {ann(au_x)} | {ann(au_t)} | {ann(gs_x)} | {ann(gs_t)} |"
            f" {spans([r[0] for r in sel])} |"
        ]

    out = [
        "# combo-2, step 2: commodity proxies in US stock-bond co-falls, 1962-2025 (description)",
        "",
        'Card: `combo-2.md`, step 2, "1970s-style co-falls". Not a test and not a try: monthly '
        "data, no gym, no costs. Gate at month end: US stocks' (Fama-French market) and a "
        "10-year Treasury's (from FRED DGS10, par bond) 12-month total returns both <= 0; "
        "returns of the next month, % a year (mean monthly x 12). Gold: monthly average price, "
        "no yield. GSCI: Yahoo `^SPGSCI` (from 1985), a price index; the trend-gated column adds "
        "the T-bill to it as the collateral a futures fund earns (DBC's construction), and holds "
        "T-bills when the proxy's 12-month change is <= 0. None of these is what DBC earned.",
        "",
        "| Years | Gate months | Stocks | T-bill | Gold | Gold if in trend, else bill |"
        " GSCI | GSCI + bill if in trend, else bill | Spells |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for lo, hi in [(1962, 1979), (1980, 1993), (1994, 2005), (2006, 2025), (1962, 2025)]:
        out += stats_for(lo, hi)
    out.append("")
    text = "\n".join(out)
    print(text)
    RESULT.write_text(text + "\n")


if __name__ == "__main__":
    main()
