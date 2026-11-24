"""Price path of the stocks Burry's Scion held puts on at 2025-09-30 (lane inv).

Input: Yahoo chart-API JSON files, passed as arguments (label=path):
    python -I inv_burry_check.py PLTR=<pltr.json> NVDA=<nvda.json>
Prints the close on 2025-09-30 (13F date), the min and max close since, and the last close.
"""

import json
import sys
from datetime import UTC, date, datetime


def load(path: str) -> dict[date, float]:
    with open(path) as f:
        res = json.load(f)["chart"]["result"][0]
    return {
        datetime.fromtimestamp(t, UTC).date(): c
        for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"], strict=True)
        if c is not None
    }


def main() -> None:
    for arg in sys.argv[1:]:
        label, path = arg.split("=", 1)
        s = load(path)
        base_d = max(d for d in s if d <= date(2025, 9, 30))
        since = {d: v for d, v in s.items() if d >= base_d}
        lo = min(since, key=lambda d: since[d])
        hi = max(since, key=lambda d: since[d])
        last = max(s)
        b = s[base_d]
        print(
            f"{label}: 13F-date close {base_d} {b:.2f}; "
            f"max {hi} {s[hi]:.2f} ({s[hi] / b - 1:+.0%}); "
            f"min {lo} {s[lo]:.2f} ({s[lo] / b - 1:+.0%}); "
            f"last {last} {s[last]:.2f} ({s[last] / b - 1:+.0%})"
        )


if __name__ == "__main__":
    main()
