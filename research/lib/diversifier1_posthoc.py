"""diversifier-1, post-hoc (not on the card): is the Sharpe gain more than T-bill interest?

    uv run --with numpy python research/lib/diversifier1_posthoc.py

The gym pays 0 on cash and Sharpe is measured against 0, so any always-held slot that earns
about the T-bill rate (merger arb is close to a bond-like, low-vol return) lifts a book whose
cash earns nothing. Here both logged books are re-scored (`log=False`, no new configuration)
the `cash_interest.py` way: cash earns the 13-week T-bill yield and Sharpe is measured above it.
Under that convention a 1/7 slot of plain bills adds exactly nothing (6/7 of the excess return).
"""

from __future__ import annotations

import cash_interest as ci
import common as c
import diversifier1 as d1
import stats


def main() -> None:
    days, yields = ci.bill_yield()
    six = c.ctx("six")
    base = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline",
                log=False)  # fmt: skip
    out = ["# diversifier-1 post-hoc: Sharpe above T-bills (not on the card)", ""]
    out += [
        "Same runs as `results/diversifier-1.md`, re-scored (`log=False`): cash earns the 13-week "
        "T-bill yield, Sharpe on daily returns above that yield. Descriptive, no new try.",
        "",
        "| Window | Book | Sharpe above bills | tsmom12 above bills | dSharpe | boot SE | z | p |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for div, tag in (("MERFX", "six"), ("MNA", "mna")):
        ctx = d1.ctx_with(div, tag)
        start = d1.first_eligible(ctx, div) if div == "MNA" else None
        name = "merfx7" if div == "MERFX" else "mna7"
        test = c.go(d1.IDEA, name, d1.book(div), ctx, log=False, start=start)
        ref = base
        if start is not None:
            ref = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six,
                       "baseline", log=False, start=start)  # fmt: skip
        assert test.days[0] == ref.days[0]
        rt, rft = ci.rescored(test, days, yields)
        rb, _ = ci.rescored(ref, days, yields)
        n = min(len(rt), len(rb))
        a, b = (rt - rft)[:n], (rb - rft)[:n]
        dd, p, se = d1.boot(a, b)
        out.append(
            f"| {test.days[0]}..{test.days[-1]} | {test.variant} | {stats.sharpe(a):.2f} | "
            f"{stats.sharpe(b):.2f} | {dd:+.3f} | {se:.3f} | {dd / se:+.2f} | {p:.3f} |"
        )
    c.write_result("diversifier-1-posthoc", "\n".join(out))


if __name__ == "__main__":
    main()
