"""uv run --with numpy python research/lib/idea_dip_rsi2.py"""

from __future__ import annotations

from datetime import date

import common as c
import numpy as np
import timing

IDEA = "dip-rsi2"
SPLIT = date(2009, 1, 1)  # the rule was published in 2008


def state(view: c.View, sym: str) -> np.ndarray:
    """In-position flag after each close (entry i depends on closes 0..i only)."""
    key = ("rsi2", sym)
    cache = view.panel.cache
    if key not in cache:
        cl = view.panel.c[sym]
        n = len(cl)
        out = np.zeros(n, dtype=bool)
        up = dn = 0.0
        pos, age = False, 0
        for i in range(1, n):
            ch = cl[i] - cl[i - 1]
            up = (up + max(ch, 0.0)) / 2  # Wilder smoothing with period 2
            dn = (dn + max(-ch, 0.0)) / 2
            if i < 200:
                continue
            rsi = 100.0 if dn == 0 else 100 - 100 / (1 + up / dn)
            sma5 = cl[i - 4 : i + 1].mean()
            sma200 = cl[i - 199 : i + 1].mean()
            if pos:
                age += 1
                if cl[i] > sma5 or age >= 5:
                    pos = False
            if not pos and rsi < 5 and cl[i] < sma5 and cl[i] > sma200:
                pos, age = True, 0
            out[i] = pos
        cache[key] = out
    full: np.ndarray = cache[key]  # type: ignore[assignment]
    return full[: view.n[sym]]


def held(view: c.View, sym: str) -> bool:
    return bool(state(view, sym)[-1])


def close_fill(r: dict) -> str:
    """The same signals filled at the signal's own close (no costs): what the papers report."""
    u, sym = r["ctx"], r["sym"]
    cl = u.panel.c[sym]
    st = state(u.panel.view(u.panel.close_times[sym][-1]), sym)
    first = int(np.searchsorted(u.panel.ord[sym], u.start.toordinal()))
    x = np.array([cl[i + 1] / cl[i] - 1 for i in range(first, len(cl) - 1) if st[i]])
    return f"{sym}: {x.mean() * 1e4:+.1f} bps per day held at close fills ({len(x)} days)"


def main() -> None:
    out, res, signs = timing.run_all(
        IDEA, "dip-rsi2: buying short-term dips in stock indexes", "rsi2", held,
        ["SPY", "QQQ"],
        {"other ETFs": ["IWM", "EFA", "EEM"], "indexes": ["GSPC", "N225", "FTSE", "GDAXI"]},
        SPLIT,
        "Twin `constant` holds the same asset at the rule's average exposure. `equal-weight` "
        "is buy-and-hold of the asset.",
    )  # fmt: skip
    out += ["# What the next-open fill costs", "", "; ".join(close_fill(r) for r in res) + ".", ""]
    by = {r["sym"]: r for r in res}
    bars = [
        ("1. Sharpe beats the twin with p < 0.10 on SPY and QQQ both",
         all(r["diff"] > 0 and r["p"] < 0.10 for r in res),
         ", ".join(f"{s} {by[s]['diff']:+.2f} (p = {by[s]['p']:.2f})" for s in by)),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         all(r["mdd"] <= r["mdd_twin"] + 0.05 for r in res),
         ", ".join(f"{s} {by[s]['mdd']:.0%} vs {by[s]['mdd_twin']:.0%}" for s in by)),
        ("4. Same sign out of universe in both applicable sets",
         all(v > 0 for v in signs.values()), ", ".join(f"{k} {v:+.2f}" for k, v in signs.items())),
        ("5. (card) Return per day held above other days, t > 2, SPY and QQQ",
         all(r["t"] > 2 for r in res), ", ".join(f"{s} t = {by[s]['t']:.2f}" for s in by)),
        ("6. (card) Not behind the twin after publication, 2009-2025",
         all(r["post"] >= 0 for r in res), ", ".join(f"{s} {by[s]['post']:+.2f}" for s in by)),
    ]  # fmt: skip
    out += ["# Pass bar", "", "(Bar 2, eras ahead, is read from the tables above.)", ""]
    out += [f"- {'PASS' if ok else 'FAIL'}: {text} ({detail})" for text, ok, detail in bars]
    out += ["", f"**{'PASSES' if all(x for _, x, _ in bars) else 'FAILS'} train.**", ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
