"""Rule of lane rp-1, exactly as on its card (research/rp-1.md, "Step 2 card: `where-rp`").

`where-vol` (lane trend-where) with one change: an eligible asset's slot is the protocol's
`inverse-vol` weight (1 / EWMA volatility, 60-bar half-life, normalised over all eligible assets)
instead of an equal share. The yes/no per asset, its refits and the `tsmom12` signals are
`where-vol`'s own. A slot that is not held sits in cash. Everything is causal.
"""

from __future__ import annotations

from typing import Protocol

import common as c
import trend_tune as tt
import trend_where as tw
from harness import Panel, ResearchStrategy, View, Weights


class Answers(Protocol):
    def answers(self, panel: Panel, refit: object) -> dict[str, bool]: ...


def where_rp(where: Answers | None = None) -> ResearchStrategy:
    """`where` gives the yes/no (keep the filter) per asset at a refit; default `Where("vol")`."""
    w = where if where is not None else tw.Where("vol")
    token = object()

    def f(view: View) -> Weights:
        day = tt.last_friday(view.today)
        key = (token, day)
        memo = view.panel.cache
        if key not in memo:
            v = view if day == view.today else view.at(day)
            keep = w.answers(view.panel, tt.refit_of(day))
            base = c.inverse_vol(v)
            memo[key] = {  # type: ignore[assignment]
                s: x for s, x in base.items() if (not keep[s]) or tt.signal(v, s, 12)
            }
        return memo[key]  # type: ignore[return-value]

    return f
