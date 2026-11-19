"""Download the Wikipedia page views of card `attention-peak` (research/cards/attention-peak.md).

    uv run python research/lib/wide3_pageviews.py

Wikimedia REST API, en.wikipedia, all-access, agent `user`, daily, 2015-07-01 .. 2025-11-10
(the train cut: nothing later is requested). No key; a generic user agent. One CSV per title
in the git-ignored research/data/pageviews/ (date,views). A title with no data gets no file.
"""

from __future__ import annotations

import csv
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "pageviews"
FIRST, LAST = "20150701", "20251110"
API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user"
UA = "grimstrade-research/0.1 (research script; public page view statistics)"

# coin -> titles whose views are summed (card: renamed articles are added together)
TITLES: dict[str, tuple[str, ...]] = {
    "BTC": ("Bitcoin",),
    "ETH": ("Ethereum",),
    "LTC": ("Litecoin",),
    "XRP": ("Ripple_(payment_protocol)", "XRP_Ledger"),
    "BCH": ("Bitcoin_Cash",),
    "ETC": ("Ethereum_Classic",),
    "XLM": ("Stellar_(payment_network)",),
    "DASH": ("Dash_(cryptocurrency)",),
}


def fetch(title: str) -> list[tuple[date, int]]:
    url = f"{API}/{urllib.parse.quote(title, safe='')}/daily/{FIRST}/{LAST}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            items = json.load(r)["items"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return []
        raise
    out = []
    for it in items:
        ts = it["timestamp"]
        d = date(int(ts[:4]), int(ts[4:6]), int(ts[6:8]))
        if d <= date(2025, 11, 10):
            out.append((d, int(it["views"])))
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for titles in TITLES.values():
        for t in titles:
            rows = fetch(t)
            print(f"{t}: {len(rows)} days, {rows[0][0] if rows else '-'} .. "
                  f"{rows[-1][0] if rows else '-'}")  # fmt: skip
            if rows:
                with (OUT / f"{t}.csv").open("w", newline="") as f:
                    w = csv.writer(f, lineterminator="\n")
                    w.writerow(["date", "views"])
                    w.writerows((d.isoformat(), v) for d, v in rows)


if __name__ == "__main__":
    main()
