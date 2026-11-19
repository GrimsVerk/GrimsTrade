"""uv run --with numpy python research/lib/idea_wide1_vol_echo.py   (card: cards/vol-echo.md)"""

from __future__ import annotations

from datetime import date

import common as c
import numpy as np
import timing
import wide1_rules as rules

IDEA = "vol-echo"
SPLIT = date(2010, 1, 1)  # the start of the volatility-control era
VARIANTS = {"echo21": (21, 0.20), "echo63": (63, 0.10)}


def signal(n: int, theta: float) -> timing.Signal:
    def f(view: c.View, s: str) -> bool:
        key = ("echo", s, n, theta)
        cache = view.panel.cache
        if key not in cache:
            cache[key] = rules.echo_in(view.panel.lr[s], n, theta)  # entry m uses lr[:m] only
        held: np.ndarray = cache[key]  # type: ignore[assignment]
        return bool(held[len(view.logret(s))])

    return f


def split_line(r: dict) -> str:
    """Mean open-to-open return per day held / not held, before and from SPLIT."""
    run, u, sym = r["run"], r["ctx"], r["sym"]
    bars = u.hist[sym]
    held = {d.time.date(): bool(d.weights) for d in run.decisions}
    cells: dict[str, tuple[list[float], list[float]]] = {"pre": ([], []), "post": ([], [])}
    for i in range(len(bars) - 2):
        d = bars[i].date
        if d in held:
            x = bars[i + 2].open / bars[i + 1].open - 1
            cells["pre" if d < SPLIT else "post"][0 if held[d] else 1].append(x)
    parts = []
    for name, label in (("pre", f"before {SPLIT.year}"), ("post", f"from {SPLIT.year}")):
        a, b = np.array(cells[name][0]), np.array(cells[name][1])
        if len(a) < 2 or len(b) < 2:
            parts.append(f"| {sym} | {label} | - | - | - | - | - |")
            continue
        parts.append(
            f"| {sym} | {label} | {len(a)} | {a.mean() * 1e4:+.1f} | {len(b)} | "
            f"{b.mean() * 1e4:+.1f} | {timing.welch(a, b):+.2f} |"
        )
    return "\n".join(parts)


SPLIT_HEAD = (
    "| Asset | Period | Days held | bps a day held | Days not held | bps a day not held | "
    "Welch t |\n|---|---|---:|---:|---:|---:|---:|"
)


def main() -> None:
    sig = signal(*VARIANTS["echo21"])
    out, res, signs = timing.run_all(
        IDEA, "vol-echo: the day a shock leaves other people's volatility window", "echo21", sig,
        ["SPY", "QQQ"],
        {"other stock ETFs": ["IWM", "EFA", "EEM"], "foreign indexes": ["N225", "FTSE", "GDAXI"]},
        SPLIT,
        "Twin `constant` holds the same asset at the rule's average exposure. `equal-weight` "
        "is buy-and-hold of the asset.",
    )  # fmt: skip
    by = {r["sym"]: r for r in res}
    out += ["# Placebo: the S&P 500 index 1962-1993 (before volatility-control funds)", ""]
    placebo = timing.one(IDEA, "echo21", sig, "GSPC", "robustness", SPLIT)
    out += placebo["text"]
    out += ["# Variant `echo63` (63-day window, a tenth of its variance)", ""]
    res63 = [
        timing.one(IDEA, "echo63", signal(*VARIANTS["echo63"]), s, "variant", SPLIT)
        for s in ("SPY", "QQQ")
    ]
    for r in res63:
        out += r["text"]
    out += ["# Before and after 2010 (the mechanism should be absent before)", "", SPLIT_HEAD]
    out += [split_line(r) for r in [*res, placebo]]
    out += ["", "`echo63`:", "", SPLIT_HEAD]
    out += [split_line(r) for r in res63]
    out += [""]
    bars = [
        ("1. `echo21` beats the twin with p < 0.10 on SPY and QQQ both",
         all(by[s]["diff"] > 0 and by[s]["p"] < 0.10 for s in by),
         ", ".join(f"{s} {by[s]['diff']:+.2f} (p = {by[s]['p']:.2f})" for s in by)),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         all(by[s]["mdd"] <= by[s]["mdd_twin"] + 0.05 for s in by),
         ", ".join(f"{s} {by[s]['mdd']:.0%} vs {by[s]['mdd_twin']:.0%}" for s in by)),
        ("4. Same sign in both out-of-universe sets",
         all(v > 0 for v in signs.values()), ", ".join(f"{k} {v:+.2f}" for k, v in signs.items())),
        ("5. Sharpe above buy-and-hold of the same asset, SPY and QQQ",
         all(by[s]["sharpe"] > by[s]["bh"] for s in by),
         ", ".join(f"{s} {by[s]['sharpe']:.2f} vs {by[s]['bh']:.2f}" for s in by)),
        ("6. From 2010: not behind the twin, SPY and QQQ",
         all(by[s]["post"] >= 0 for s in by),
         ", ".join(f"{s} {by[s]['post']:+.2f}" for s in by)),
    ]  # fmt: skip
    out += ["# Pass bar (primary variant `echo21`)", ""]
    out += ["(Bar 2, eras ahead, is read from the tables above.)", ""]
    out += [f"- {'PASS' if ok else 'FAIL'}: {text} ({detail})" for text, ok, detail in bars]
    out += ["", f"**{'PASSES' if all(x for _, x, _ in bars) else 'FAILS'} train.**", ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
