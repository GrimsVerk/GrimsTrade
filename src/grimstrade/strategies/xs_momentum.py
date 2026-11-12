"""Cross-sectional momentum (Jegadeesh & Titman 1993, "Returns to buying winners and selling
losers", JF).

The paper's headline strategy is J=6 / K=6: at each month end, rank assets by their past 6-month
return and buy the winners; hold each such cohort for 6 months, so 6 overlapping cohorts are held
at once, each with 1/6 of the money.

Adapted to us: winners are the top third of the universe (2 of 6 assets; a decile is impossible
with 6), long-only (the paper also shorts the losers; we hold cash instead), no skip week (the
paper's base case). A cohort whose month end predates our data stays in cash.

A month end counts as completed only once every crypto asset has a bar on or after it: crypto
bars close at 00:00 UTC, a day after the ETF bar of the same date, so a cohort formed on the ETF
bar alone would rank crypto on a stale close and change its picks the next day.
"""

import math
from datetime import date, timedelta

from grimstrade.data import CRYPTO, UNIVERSE, History
from grimstrade.signals import close_on_or_before

FORMATION_MONTHS = 6  # J
HOLDING_MONTHS = 6  # K
WINNER_SHARE = 1 / 3


def month_end(year: int, month: int) -> date:
    """Last day of `month` in `year`; months outside 1..12 roll over into other years."""
    year, month = year + (month - 1) // 12, (month - 1) % 12 + 1
    first_of_next = date(year + month // 12, month % 12 + 1, 1)
    return first_of_next - timedelta(days=1)


def winners(history: History, formed: date) -> list[str]:
    """Top third by return over the FORMATION_MONTHS ending at month end `formed`."""
    start = month_end(formed.year, formed.month - FORMATION_MONTHS)
    rets = {}
    for sym, bars in history.items():
        if not bars or bars[0].date > start:
            continue
        now, then = close_on_or_before(bars, formed), close_on_or_before(bars, start)
        if now is not None and then:
            rets[sym] = now / then - 1
    ranked = sorted(rets, key=lambda s: (-rets[s], s))
    return ranked[: math.ceil(len(ranked) * WINNER_SHARE)]


def decide(history: History) -> tuple[dict[str, float], str]:
    lasts = [b[-1].date for b in history.values() if b]
    if not lasts:
        return {}, "xs momentum: no data yet, stay in cash"
    crypto = [b[-1].date for s, b in history.items() if b and UNIVERSE.get(s) == CRYPTO]
    # Every asset has closed the day `latest` (crypto trades daily, so its slowest bar decides).
    latest = min(crypto) if crypto else max(lasts)
    # The last K completed month ends, newest first.
    last_end = month_end(latest.year, latest.month)
    if last_end > latest:
        last_end = month_end(latest.year, latest.month - 1)
    cohorts = [month_end(last_end.year, last_end.month - k) for k in range(HOLDING_MONTHS)]
    weights: dict[str, float] = {}
    notes = []
    for formed in cohorts:
        picks = winners(history, formed)
        for sym in picks:
            weights[sym] = weights.get(sym, 0.0) + 1 / HOLDING_MONTHS / len(picks)
        notes.append(f"{formed:%Y-%m}: {'+'.join(picks) or 'cash'}")
    return weights, "xs momentum 6/6, winners by cohort: " + ", ".join(notes)
