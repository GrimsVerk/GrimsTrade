"""coin-drift-2's pure parts (card `research/cards/coin-drift-2.md`): the coin pick and the CM
bars. No `harness` import, so tests do not register research symbols in the gym's universe."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date

import numpy as np

from grimstrade.data import Bar

OOU_COINS = ("LTC", "XRP", "BCH", "ETC", "XLM", "DASH")  # wide-16's set (`harness.OOU_COINS`)
EXCLUDE = ("btc", "eth", "usdt", *(s.lower() for s in OOU_COINS))
CARD_COINS = ("xem", "xmr", "zec", "doge", "dcr", "rep")  # as the card lists them


def pick_coins(
    names: Sequence[str], elig: np.ndarray, cap30: np.ndarray, exclude: Sequence[str], k: int = 6
) -> list[str]:
    """The k largest by `cap30` among `elig` coins, skipping `exclude` (one day's rows)."""
    ok = [j for j, n in enumerate(names) if elig[j] and n not in exclude and np.isfinite(cap30[j])]
    ok.sort(key=lambda j: -float(cap30[j]))
    return [names[j] for j in ok[:k]]


def cm_bars(series: Sequence[tuple[date, float]], last: date) -> list[Bar]:
    """breadth-book-1's CM bars (`bbook1.prep_coins`): a bar opens at the previous known price
    and closes at the day's price; nothing after `last`, no non-positive price."""
    s = sorted((d, p) for d, p in series if d <= last and p > 0)
    return [
        Bar(d, p0, max(p0, p), min(p0, p), p, 0.0)
        for (_, p0), (d, p) in zip(s, s[1:], strict=False)
    ]
