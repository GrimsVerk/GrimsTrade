"""Build the Treasury's payment calendar for `coupon-dose` (research/cards/coupon-dose.md) from
the auction file (a download: read as data only).

    uv run python -I research/lib/wide4_coupons.py

Source: fiscaldata.treasury.gov `accounting/od/auctions_query` (public, keyless), saved under
`<cache_root>/downloads/wide-4/treasury-auctions/`. Output:
`<cache_root>/derived/wide-4/payments.csv` with `date,kind,amount,announced,issue,maturity`:
one row per coupon, principal repayment (amount > 0, $ billion) and settlement of a new issue
(amount < 0) of nominal fixed-rate notes and bonds. Prints only row counts and date ranges.
"""

from __future__ import annotations

import calendar
import csv
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro  # noqa: E402


@dataclass
class Tranche:
    announced: date
    issue: date
    amount: float  # $ billion


def last_day(y: int, m: int) -> int:
    return calendar.monthrange(y, m)[1]


def add_months(y: int, m: int, k: int) -> tuple[int, int]:
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


def coupon_dates(maturity: date, first_issue: date) -> list[date]:
    """Semiannual coupon dates after `first_issue` up to `maturity`, on the maturity's day of
    the month (the last day of the month if the maturity is on a month's last day)."""
    eom = maturity.day == last_day(maturity.year, maturity.month)
    out, k = [], 0
    while True:
        y, m = add_months(maturity.year, maturity.month, -6 * k)
        d = last_day(y, m) if eom else min(maturity.day, last_day(y, m))
        c = date(y, m, d)
        if c <= first_issue:
            break
        out.append(c)
        k += 1
    return sorted(out)


def payments(secs: dict[str, tuple[date, float, list[Tranche]]]) -> list[tuple]:
    """(date, kind, amount, announced, issue, maturity) rows for each security
    `cusip -> (maturity, rate in %, tranches)`."""
    rows: list[tuple] = []
    for maturity, rate, tr in secs.values():
        tr = sorted(tr, key=lambda t: t.issue)
        for t in tr:
            rows.append((t.issue, "settle", -t.amount, t.announced, tr[0].issue, maturity))
        for c in coupon_dates(maturity, tr[0].issue):
            held = [t for t in tr if t.issue < c]
            if held:
                amt = sum(t.amount for t in held) * rate / 200.0
                known = max(t.announced for t in held)
                rows.append((c, "coupon", amt, known, tr[0].issue, maturity))
        rows.append((maturity, "principal", sum(t.amount for t in tr),
                     max(t.announced for t in tr), tr[0].issue, maturity))  # fmt: skip
    return sorted(rows)


def main() -> None:
    src = macro.cache_root() / "downloads" / "wide-4" / "treasury-auctions"
    secs: dict[str, tuple[date, float, list[Tranche]]] = {}
    for p in sorted(src.glob("p*.json")):
        for r in json.loads(p.read_text())["data"]:
            if r["security_type"] not in ("Note", "Bond"):
                continue
            if r["floating_rate"] == "Yes" or r["inflation_index_security"] == "Yes":
                continue
            if r["total_accepted"] in (None, "null") or r["issue_date"] in (None, "null"):
                continue
            mat = date.fromisoformat(str(r["maturity_date"]))
            tr = Tranche(
                date.fromisoformat(str(r["announcemt_date"])),
                date.fromisoformat(str(r["issue_date"])),
                float(str(r["total_accepted"])) / 1e9,
            )
            cur = secs.get(str(r["cusip"]))
            rate = float(str(r["int_rate"])) if r["int_rate"] not in (None, "null") else None
            if cur is None:
                if rate is None:
                    continue
                secs[str(r["cusip"])] = (mat, rate, [tr])
            else:
                cur[2].append(tr)
    rows = payments(secs)
    out = macro.cache_root() / "derived" / "wide-4"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "payments.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "kind", "amount", "announced", "issue", "maturity"])
        for d, kind, amt, known, iss, mat in rows:
            w.writerow([d.isoformat(), kind, f"{amt:.6f}", known.isoformat(), iss.isoformat(),
                        mat.isoformat()])  # fmt: skip
    print(f"securities {len(secs)}, payment rows {len(rows)}, {rows[0][0]} .. {rows[-1][0]}")


if __name__ == "__main__":
    main()
