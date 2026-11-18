"""Parse the Daily Treasury Statement's operating cash balance (a download: read as data only)
into a small CSV for `tax-drain` (research/cards/tax-drain.md).

    uv run python -I research/lib/wide4_dts.py

Source: fiscaldata.treasury.gov `accounting/dts/operating_cash_balance` (public, keyless), JSON
pages saved under `<cache_root>/treasury/dts-2026-11-18/`. Output:
`<cache_root>/derived/wide-4/tga.csv` with `date,tga,ttl` (closing balances, $ billion; `ttl`
empty once the TT&L line is gone). Prints only row counts and the first and last date.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro  # noqa: E402

CUT = date(2025, 11, 10)
TGA = {
    "Federal Reserve Account": "close_today_bal",
    "Treasury General Account (TGA)": "close_today_bal",
    "Treasury General Account (TGA) Closing Balance": "open_today_bal",  # the API's column
}
TTL = ("Tax and Loan Note Accounts (Table V)", "Account Tax and Loan Note Accounts (Table V)")


def num(x: object) -> float | None:
    try:
        return float(str(x)) / 1000.0
    except ValueError:
        return None


def main() -> None:
    src = macro.cache_root() / "treasury" / "dts-2026-11-18"
    tga: dict[date, float] = {}
    ttl: dict[date, float] = {}
    for p in sorted(src.glob("ocb-p*.json")):
        for r in json.loads(p.read_text())["data"]:
            d = date.fromisoformat(str(r["record_date"]))
            if d > CUT:
                continue
            kind = str(r["account_type"])
            if kind in TGA:
                v = num(r[TGA[kind]])
                if v is not None:
                    tga[d] = v
            elif kind in TTL:
                v = num(r["close_today_bal"])
                if v is not None:
                    ttl[d] = v
    out = macro.cache_root() / "derived" / "wide-4"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "tga.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "tga", "ttl"])
        for d in sorted(tga):
            w.writerow([d.isoformat(), f"{tga[d]:.3f}", f"{ttl[d]:.3f}" if d in ttl else ""])
    days = sorted(tga)
    print(f"tga rows {len(days)}, {days[0]} .. {days[-1]}; ttl rows {len(ttl)}")


if __name__ == "__main__":
    main()
