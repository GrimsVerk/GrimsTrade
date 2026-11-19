"""Parse the Treasury's auction file for the wide-5 cards (research/cards/dealer-backlog.md,
research/cards/extension-dose.md). The file is a download: read as data only.

    uv run python -I research/lib/wide5_auctions.py

Source: fiscaldata.treasury.gov `accounting/od/auctions_query` (public, keyless), notes and
bonds, saved under `<cache_root>/downloads/wide-5/treasury-auctions/`. Output:
`<cache_root>/derived/wide-5/auctions.csv`, one row per nominal fixed-rate auction (originals
and reopenings): `cusip,years,announced,auction,issue,maturity,accepted,comp,dealer` with
amounts in $ billion (`comp` and `dealer` empty where the file has none). Prints only row
counts and date ranges.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro  # noqa: E402


def term_years(term: str) -> int | None:
    """The leading number of years of an `original_security_term` such as '29-Year 9-Month'."""
    m = re.match(r"\s*(\d+)-Year", term or "")
    return int(m.group(1)) if m else None


def _num(x: object) -> str:
    if x in (None, "null", ""):
        return ""
    return f"{float(str(x)) / 1e9:.6f}"


def main() -> None:
    src = macro.cache_root() / "downloads" / "wide-5" / "treasury-auctions"
    rows = []
    for p in sorted(src.glob("p*.json")):
        for r in json.loads(p.read_text())["data"]:
            if r["security_type"] not in ("Note", "Bond"):
                continue
            if r["floating_rate"] == "Yes" or r["inflation_index_security"] == "Yes":
                continue
            yrs = term_years(str(r["original_security_term"]))
            need = ("announcemt_date", "auction_date", "issue_date", "maturity_date")
            if yrs is None or any(r[k] in (None, "null") for k in need):
                continue
            if r["total_accepted"] in (None, "null"):
                continue
            rows.append((
                str(r["cusip"]), yrs, str(r["announcemt_date"]), str(r["auction_date"]),
                str(r["issue_date"]), str(r["maturity_date"]), _num(r["total_accepted"]),
                _num(r["comp_accepted"]), _num(r["primary_dealer_accepted"]),
            ))  # fmt: skip
    rows.sort(key=lambda x: (x[3], x[0]))
    out = macro.cache_root() / "derived" / "wide-5"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "auctions.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cusip", "years", "announced", "auction", "issue", "maturity", "accepted",
                    "comp", "dealer"])  # fmt: skip
        w.writerows(rows)
    with_dealer = sum(1 for x in rows if x[7] and x[8])
    print(f"auctions {len(rows)} ({rows[0][3]} .. {rows[-1][3]}), with dealer data {with_dealer}")


if __name__ == "__main__":
    main()
