"""uv run --with numpy python research/lib/idea_month_end_liquidity.py"""

from __future__ import annotations

import bisect
from datetime import date

import common as c
import harness
import timing

from grimstrade import data

IDEA = "month-end-liquidity"
SPLIT = date(2014, 1, 1)  # the paper's sample ends December 2013
_calendar: dict[str, list[date]] = {}


def calendar(sym: str) -> list[date]:
    """All trading dates of the symbol, including future ones: dates only, known in advance."""
    if sym not in _calendar:
        _calendar[sym] = [b.date for b in data.load(harness.RESEARCH, sym)]
    return _calendar[sym]


def in_window(view: c.View, sym: str) -> bool:
    """True on decision days T-4 .. T+2 (held from the open of T-3 to the open of T+4)."""
    cal = calendar(sym)
    d = date.fromordinal(int(view.dates(sym)[-1]))  # the last closed trading day
    i = bisect.bisect_left(cal, d)
    left = sum(1 for x in cal[i + 1 : i + 8] if (x.year, x.month) == (d.year, d.month))
    if i + 8 >= len(cal):  # the calendar's end: count weekdays instead
        return False
    done = sum(1 for x in cal[max(i - 8, 0) : i] if (x.year, x.month) == (d.year, d.month)) + 1
    return left <= 4 or done <= 2


def main() -> None:
    out, res, signs = timing.run_all(
        IDEA, "month-end-liquidity: the turn-of-month window", "window", in_window,
        ["SPY", "QQQ", "TLT"],
        {"other ETFs": ["IWM", "EFA", "EEM", "IEF", "LQD"],
         "indexes": ["GSPC", "N225", "FTSE", "GDAXI"]},
        SPLIT,
        "Twin `constant` holds the same asset at the rule's average exposure. `equal-weight` "
        "is buy-and-hold of the asset.",
    )  # fmt: skip
    by = {r["sym"]: r for r in res}
    bars = [
        ("1. Sharpe beats the twin with p < 0.10 on SPY and TLT both",
         all(by[s]["diff"] > 0 and by[s]["p"] < 0.10 for s in ("SPY", "TLT")),
         ", ".join(f"{s} {by[s]['diff']:+.2f} (p = {by[s]['p']:.2f})" for s in by)),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         all(by[s]["mdd"] <= by[s]["mdd_twin"] + 0.05 for s in ("SPY", "TLT")),
         ", ".join(f"{s} {by[s]['mdd']:.0%} vs {by[s]['mdd_twin']:.0%}" for s in by)),
        ("4. Same sign out of universe in both applicable sets",
         all(v > 0 for v in signs.values()), ", ".join(f"{k} {v:+.2f}" for k, v in signs.items())),
        ("5. (card) Sharpe above buy-and-hold of the same asset, SPY and TLT",
         all(by[s]["sharpe"] > by[s]["bh"] for s in ("SPY", "TLT")),
         ", ".join(f"{s} {by[s]['sharpe']:.2f} vs {by[s]['bh']:.2f}" for s in by)),
        ("6. (card) Not behind the twin after the paper's sample, 2014-2025, SPY and TLT",
         all(by[s]["post"] >= 0 for s in ("SPY", "TLT")),
         ", ".join(f"{s} {by[s]['post']:+.2f}" for s in by)),
    ]  # fmt: skip
    out += ["# Pass bar", "", "(Bar 2, eras ahead, is read from the tables above.)", ""]
    out += [f"- {'PASS' if ok else 'FAIL'}: {text} ({detail})" for text, ok, detail in bars]
    out += ["", f"**{'PASSES' if all(x for _, x, _ in bars) else 'FAILS'} train.**", ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
