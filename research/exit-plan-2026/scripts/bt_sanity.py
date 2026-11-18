"""Print the range of every input series (no strategy numbers)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_data as d  # noqa: E402


def main() -> None:
    for sym in ["^GSPC", "^IXIC", "HYG", "LQD", "OSEBX.OL", "OBX.OL", "^VIX3M"]:
        try:
            s = d.yahoo(sym)
            print(f"{sym:9s} {s.index[0].date()} .. {s.index[-1].date()} n={len(s)}")
        except Exception as e:  # noqa: BLE001
            print(sym, "failed", type(e).__name__, e)
    v = d.vix()
    print("VIX", v.index[0].date(), v.index[-1].date(), len(v))
    v3 = d.vix3m()
    print("VIX3M", v3.index[0].date(), v3.index[-1].date(), len(v3))
    b = d.fred("BAA10Y")
    print("BAA10Y", b.index[0].date(), b.index[-1].date(), len(b))
    c = d.cape_lagged()
    print("CAPE lagged", c.index[0].date(), c.index[-1].date(), len(c))
    # gaps in GSPC
    g = d.yahoo("^GSPC")
    gaps = g.index.to_series().diff().dt.days
    print("GSPC gaps > 5 days:", gaps[gaps > 5].to_dict())


if __name__ == "__main__":
    main()
