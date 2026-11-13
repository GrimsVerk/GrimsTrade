"""How sharp is the halving window? (run macro-1, after `halving` was judged)

    uv run --with numpy python research/lib/halving_shift.py

The card's window (days 548-912 after a halving) moved six months earlier and six months later,
`halving-and` form, six assets. Logged as `robustness`: the card's choice was made before, these
only show whether the result needs that exact window (a fitted folklore would).
"""

from __future__ import annotations

from datetime import date

import common as c
import macro
import rules


def window(lo: int, hi: int):  # type: ignore[no-untyped-def]
    def hostile(d: date) -> bool:
        return lo <= macro.days_since_halving(d) < hi

    return hostile


if __name__ == "__main__":
    six = c.ctx("six")
    tw = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline", log=False)
    runs = [tw]
    for tag, lo, hi in (("m12-24", 365, 730), ("m18-30", 548, 913), ("m24-36", 730, 1095)):
        log = tag != "m18-30"  # the card's own window is already logged as halving-and
        runs.append(c.go("halving", f"halving-and-{tag}",
                         c.weekly(rules.macro_gate(window(lo, hi), coins_only=True)), six,
                         "robustness", log=log))  # fmt: skip
    text = ["# halving: the window moved six months either way", "",
            "Script `lib/halving_shift.py`, run after the card was judged. Months after the last",
            "halving during which coins are out; `m18-30` is the card's window.", "",
            c.table(runs, versus=tw), "", c.stress_table(runs)]  # fmt: skip
    c.write_result("halving-shift", "\n".join(text))
