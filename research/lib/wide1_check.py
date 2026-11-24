"""No-look-ahead check for the wide-1 rules: the fast path gives the same weights as
`gym.backtest`, which shows a strategy only the bars closed before the decision.

    uv run --with numpy python research/lib/wide1_check.py

(The trading calendar and the auction calendar are dates known in advance, by the cards.)"""

from __future__ import annotations

from datetime import date

import common as c
import harness
import idea_wide1_auction as auction
import idea_wide1_contagion as contagion
import idea_wide1_rebalance as rebalance
import idea_wide1_vol_echo as echo
import wide1 as w

DAYS = [
    date(2008, 10, 10),
    date(2011, 8, 8),  # inside a 30-year auction window
    date(2013, 5, 28),  # inside a month-end window
    date(2016, 7, 1),  # the first session of a month
    date(2020, 3, 12),
    date(2021, 5, 21),
    date(2022, 9, 28),
    date(2025, 2, 11),
]


def single(sym: str, signal) -> c.ResearchStrategy:  # type: ignore[no-untyped-def]
    return lambda view: {sym: 1.0} if c.eligible(view, sym) and signal(view, sym) else {}


def main() -> None:
    six = c.ctx("six")
    etf = c.ctx("etf")
    checks = [
        ("auction six", auction.gated("TLT"), six.hist),
        ("auction etf", auction.gated("IEF"), etf.hist),
        ("rebalance me", rebalance.rule(rebalance.SIX, False), six.hist),
        ("rebalance me-rebound", rebalance.rule(rebalance.SIX, True), six.hist),
        ("rebalance etf", rebalance.rule(rebalance.ETF, False), etf.hist),
    ]
    spy = c.ctx("SPY")
    tlt = c.ctx("TLT")
    checks += [
        ("auction tlt", single("TLT", auction.in_signal), tlt.hist),
        ("echo21 SPY", single("SPY", echo.signal(21, 0.20)), spy.hist),
        ("echo63 SPY", single("SPY", echo.signal(63, 0.10)), spy.hist),
    ]
    e21 = w.book_ctx("etf21", contagion.ETF21, 10)
    coins = w.book_ctx("coin8", contagion.COINS, 6)
    for name in contagion.SIGNALS:
        checks.append((f"contagion {name} etf21", contagion.top_ts(name), e21.hist))
    checks.append(("contagion catchup coin8", contagion.top_ts("catchup"), coins.hist))
    for name, strategy, hist in checks:
        first = min(b[0].date for b in hist.values())
        harness.check_against_gym(strategy, hist, [d for d in DAYS if d > first])
        print("ok", name, flush=True)


if __name__ == "__main__":
    main()
