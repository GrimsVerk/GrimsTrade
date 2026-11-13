"""Macro cards (run macro-1): `uv run --with numpy python research/lib/idea_macro.py <card>`.

Cards: fed-hiking, real-rate, yield-curve, liquidity, credit-spread, halving. `DRY=1` first.
Runs the standard test (testkit), then adds what protocol.md "Macro tests" asks for: the
2003-2025 window, card bar 6, and the hostile spells (independent episodes) of each gate.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from datetime import date

import common as c
import macro
import rules
import stats
import testkit

F = macro.features()
G = rules.macro_gate
CARDS: dict[str, tuple[str, dict[str, Callable[[date], bool]], dict[str, c.ResearchStrategy]]] = {}


def _card(name: str, title: str, gates: dict[str, Callable[[date], bool]], coins: bool = False):  # type: ignore[no-untyped-def]
    variants: dict[str, c.ResearchStrategy] = {}
    for tag, gate in gates.items():
        variants[f"{tag}-and"] = c.weekly(G(gate, trend=True, coins_only=coins))
        if tag != "walcl":
            variants[f"{tag}-alone"] = c.weekly(G(gate, trend=False, coins_only=coins))
    CARDS[name] = (title, gates, variants)


_card("fed-hiking", "fed-hiking: step aside while the Fed is hiking", {"hike": F.fed_hiking})
_card("real-rate", "real-rate: step aside while the real policy rate rises fast",
      {"real": F.real_rate_rising})  # fmt: skip
_card("yield-curve", "yield-curve: step aside for a year after an inversion",
      {"curve": F.curve_inverted})  # fmt: skip
_card("liquidity", "liquidity: step aside when real M2 shrinks (or the Fed runs QT)",
      {"m2": F.real_m2_negative, "walcl": F.qt})  # fmt: skip
_card("credit-spread", "credit-spread: step aside when corporate spreads widen",
      {"spread": F.spread_widening})  # fmt: skip
_card("halving", "halving: out of coins in the bear year after a halving",
      {"halving": F.halving_bear}, coins=True)  # fmt: skip

SINCE = date(2003, 1, 1)


def _window(runs: list[c.Run], twin: c.Run, a: date) -> str:
    lines = [
        "| Variant | Sharpe | CAGR | Max DD | dSharpe vs tsmom12 (p) |",
        "|---|---:|---:|---:|---:|",
    ]
    tb = twin.rets_between(a, twin.days[-1])
    for r in runs:
        x = r.rets_between(a, r.days[-1])
        n = min(len(x), len(tb))
        diff = ""
        if r is not twin:
            d, p, _, _ = stats.sharpe_diff_boot(x[-n:], tb[-n:])
            diff = f"{d:+.2f} ({p:.2f})"
        lines.append(f"| {r.variant} | {stats.sharpe(x):.2f} | {stats.cagr(x):+.1%} | "
                     f"{stats.max_drawdown(x):.1%} | {diff} |")  # fmt: skip
    return "\n".join(lines)


def main(name: str) -> None:
    title, gates, variants = CARDS[name]
    twins = {"tsmom12": c.weekly(c.slots(c.tsmom_signal))}
    sets = ("coin",) if name == "halving" else ("etf", "coin", "idx")
    res = testkit.standard(name, title, variants, twins, per_asset=True, sets=sets)
    vs: list[c.Run] = res["variants"]  # type: ignore[assignment]
    tw: list[c.Run] = res["twins"]  # type: ignore[assignment]
    ew: c.Run = res["ew"]  # type: ignore[assignment]
    twin, primary = tw[0], vs[0]
    out = [str(res["text"]), "## Since 2003 (the review's window)", ""]
    out += [_window(vs + [twin, ew], twin, SINCE), ""]
    x, y = primary.rets_between(SINCE, primary.days[-1]), twin.rets_between(SINCE, twin.days[-1])
    ok6 = stats.sharpe(x) >= stats.sharpe(y)
    out += [f"- {'PASS' if ok6 else 'FAIL'}: 6. Not behind `tsmom12` on Sharpe 2003-2025 "
            f"({stats.sharpe(x):.2f} vs {stats.sharpe(y):.2f})", ""]  # fmt: skip
    passed = res["passed"] == "PASSES train" and ok6
    out += [f"**Card verdict (bars 1-6): {'PASSES' if passed else 'FAILS'} train.**", ""]
    out += ["## Hostile spells (independent episodes)", ""]
    for tag, gate in gates.items():
        for lo, hi in ((date(1962, 1, 1), date(1993, 12, 31)), (c.TRAIN_START, c.TRAIN_END)):
            sp = macro.spells(gate, lo, hi)
            days = sum((b - a).days + 1 for a, b in sp)
            span = (hi - lo).days + 1
            when = ", ".join(f"{a:%Y-%m}..{b:%Y-%m}" for a, b in sp)
            share = days / span
            out.append(
                f"- `{tag}`, {lo.year}-{hi.year}: {len(sp)} spells, {share:.0%} of days: {when}"
            )
    out.append("")
    c.write_result(name, "\n".join(out))


if __name__ == "__main__":
    for card in sys.argv[1:] or list(CARDS):
        main(card)
