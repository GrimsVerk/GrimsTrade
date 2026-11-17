"""Parse the Treasury auction calendar (a download: read as data only) into a small CSV.

    uv run python -I research/lib/wide1_auctions.py

Source: fiscaldata.treasury.gov `accounting/od/auctions_query` (public, keyless), every JSON
page saved under `<cache_root>/downloads/wide-1/treasury-auctions/`. Output:
`<cache_root>/derived/wide-1/auctions.csv` with `group,announced,auction,term` for the nominal
fixed-rate bonds and notes the card `auction-concession` names. Dates only: no prices, yields
or auction results are kept.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro  # noqa: E402
import wide1_rules as rules  # noqa: E402


def derived() -> Path:
    d = macro.cache_root() / "derived" / "wide-1"
    d.mkdir(parents=True, exist_ok=True)
    return d


def main() -> None:
    src = macro.cache_root() / "downloads" / "wide-1" / "treasury-auctions"
    rows: dict[tuple[str, date], tuple[date, str]] = {}
    for p in sorted(src.glob("*.json")):
        for r in json.loads(p.read_text())["data"]:
            g = rules.auction_group(
                str(r["security_type"]),
                str(r["original_security_term"]),
                str(r["inflation_index_security"]),
                str(r["floating_rate"]),
            )
            if g is None:
                continue
            try:
                auction = date.fromisoformat(str(r["auction_date"]))
                announced = date.fromisoformat(str(r["announcemt_date"]))
            except ValueError:
                continue
            key = (g, auction)
            if key not in rows or announced < rows[key][0]:
                rows[key] = (announced, str(r["original_security_term"]))
    out = derived() / "auctions.csv"
    with out.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["group", "announced", "auction", "term"])
        for (g, auction), (announced, term) in sorted(rows.items()):
            w.writerow([g, announced.isoformat(), auction.isoformat(), term])
    for g in ("long", "mid"):
        ds = [a for (gg, a) in rows if gg == g]
        print(g, len(ds), min(ds), max(ds))


if __name__ == "__main__":
    main()
