"""coin-cap-4, step 1: why the weekly coin stop trails a cap of matched cost in fast crashes and
on BTC. Descriptive and post-hoc by nature: the same series, coin falls and 21 episodes as
coin-cap-2/3 (`coin_cap2.py`), rebuilt in memory; no new rule, no bar, nothing logged.

    uv run python -I research/lib/coin_cap4_modes.py          # writes results/coin-cap-4-modes.md
    DRY=1 uv run python -I research/lib/coin_cap4_modes.py    # random prices, prints only

Per coin fall (prices as % of the top's close, days counted from the top):

- speed: the deepest price in the first 7 days; days to -25% and to -50%;
- gap: the largest one-day fall in the first 30 days;
- first leg: whether the weekly stop holds at the top, the day and price at which it stops
  earning (its exit), and the stop's summed return from the top to that exit;
- band: the stop's band in price terms, `exp(-0.25 x vol) - 1` (vol = the stop's own 60-day
  EWMA), at the top and at each re-entry after the first exit;
- re-entry: re-entries after the first exit inside the window, the price at re-entry, and the
  stop's summed return after the first exit;
- where M sits: the stop's deepest P&L fall (M) ends before the first exit (`first leg`), after
  a re-entry (`re-entry`), or does not include the top (`other`).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import coin_cap2 as cc2  # noqa: E402
import coin_cap2_core as k2  # noqa: E402
import coin_cap3_core as k3  # noqa: E402
import cointop1 as ct1  # noqa: E402
import cointop1_core as core  # noqa: E402
from harness import RESEARCH  # noqa: E402

DRY = bool(os.environ.get("DRY"))
WEEK_BEHIND = ("market-0", "market-2", "own-0", "own-1", "own-3", "market-6")


@dataclass
class F:
    ep: str
    coin: str
    top: int
    edge: float
    fall7: float
    d25: float
    d50: float
    gap: float
    held_top: bool
    exit_day: float
    exit_px: float
    leg1: float
    band_top: float
    n_re: int
    re_px: float
    band_re: float
    after: float
    where: str
    twin_exit: float


def first_le(x: np.ndarray, lvl: float) -> float:
    i = np.flatnonzero(x <= lvl)
    return float(i[0]) if len(i) else float("nan")


def main() -> None:
    book = ct1.synthetic_book(days=3000, n=40) if DRY else bb.cm_book()
    bk = cc2.build(book)
    n_days = book.px.shape[0]
    twin, stop = cc2.series(bk)
    f_star = float(stop.ret[bk.mask].mean() / twin.ret[bk.mask].mean())
    vol = core.ewma_vol(book.px, 60)
    falls = cc2.coin_falls(bk, twin)
    mkt, _ = cc2.market_falls(bk)
    keys, order = k2.episodes(falls, [(m.top, m.low) for m in mkt])
    names = book.names

    rows: list[F] = []
    for f, key in zip(falls, keys, strict=True):
        j, t0 = f.coin, f.top
        lo, hi = k2.window(f, n_days)
        px = bk.filled[:, j]
        rel = px[t0 : hi + 1] / px[t0] - 1  # index i = i days after the top
        pos = stop.pos[:, j]
        r = stop.ret[:, j]
        held = bool(pos[t0 + 1] == 1)
        ex = next((t for t in range(t0 + 1, hi + 1) if pos[t] == 0), -1)
        exit_day = float(ex - 1 - t0) if ex > 0 else float("nan")
        exit_px = float(px[ex - 1] / px[t0] - 1) if ex > 0 else float("nan")
        leg1 = float(r[t0 + 1 : ex].sum()) if ex > 0 else float(r[t0 + 1 : hi + 1].sum())
        re_rows = [t for t in range(max(ex, t0 + 1), hi + 1) if pos[t] == 1 and pos[t - 1] == 0]
        re_rows = re_rows if ex > 0 else []
        depth, pk, tr = k3.deepest_fall_span(r[lo + 1 : hi + 1])
        trough = lo + tr
        if lo + pk > t0 + 7 or trough <= t0:
            where = "other"
        elif ex < 0 or trough <= ex - 1:
            where = "first leg"
        elif re_rows and trough >= re_rows[0]:
            where = "re-entry"
        else:
            where = "first leg"
        tw_ex = next((t for t in range(t0 + 1, hi + 1) if twin.pos[t, j] == 0), -1)
        band = np.exp(-cc2.STOP_K * vol[:, j]) - 1
        rows.append(
            F(
                key, names[j], t0, f_star * k2.deepest_fall(twin.ret[lo + 1 : hi + 1, j]) - depth,
                float(rel[: 8].min()), first_le(rel, -0.25), first_le(rel, -0.50),
                float(np.min(px[t0 + 1 : t0 + 31] / px[t0 : t0 + 30] - 1)),
                held, exit_day, exit_px, leg1, float(band[t0]), len(re_rows),
                float(np.mean([px[t - 1] / px[t0] - 1 for t in re_rows])) if re_rows
                else float("nan"),
                float(np.mean([band[t - 1] for t in re_rows])) if re_rows else float("nan"),
                float(r[ex : hi + 1].sum()) if ex > 0 else 0.0,
                where, float(tw_ex - 1 - t0) if tw_ex > 0 else float("nan"),
            )
        )  # fmt: skip

    def mean(xs: list[float]) -> float:
        a = np.array(xs, dtype=float)
        a = a[np.isfinite(a)]
        return float(a.mean()) if len(a) else float("nan")

    def ep_mean(ep: str, attr: str) -> float:
        return mean([float(getattr(x, attr)) for x in rows if x.ep == ep])

    def pc(x: float) -> str:
        return "-" if not np.isfinite(x) else f"{x:+.0%}"

    def dy(x: float) -> str:
        return "-" if not np.isfinite(x) else f"{x:.0f}"

    out = [
        "# coin-cap-4, step 1: why the weekly coin stop fails in fast crashes and on BTC",
        "",
        "Generated by `research/lib/coin_cap4_modes.py` (descriptive, post-hoc by nature, nothing "
        "logged). Same book, weekly twin `TS`, weekly `stop-0.25`, 445 coin falls and 21 "
        f"episodes as `results/coin-cap-2.md`; matched cap `f*` {f_star:.3f}. Prices as change "
        "from the top's close; days from the top. Band: the stop's exit level in price terms, "
        "`exp(-0.25 x vol) - 1`, vol = its own 60-day EWMA (annualised). Exit: the last day "
        "the stop earns after the top. After exit: the stop's summed slot return from the "
        "first exit to the window's end (re-entries only; negative = re-entry losses). Where M "
        "sits: the stop's deepest P&L fall ends before its first exit (`first leg`), after a "
        "re-entry (`re-entry`), or does not start at the top (`other`).",
        "",
        "## Per episode (means over the episode's coin falls; `*` = the weekly stop trails)",
        "",
        "| Episode | Falls | Edge M | Worst 7 days | Days to -50% | Worst day (30 d) | "
        "Held at top | Exit day | Exit price | Leg-1 return | Band at top | Re-entries | "
        "Re-entry price | Band at re-entry | After exit | M: first leg / re-entry / other |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for ep in order:
        fs = [x for x in rows if x.ep == ep]
        star = " *" if ep in WEEK_BEHIND else ""
        cnt = {w: sum(x.where == w for x in fs) for w in ("first leg", "re-entry", "other")}
        out.append(
            f"| {ep}{star} | {len(fs)} | {pc(ep_mean(ep, 'edge'))} | {pc(ep_mean(ep, 'fall7'))} | "
            f"{dy(ep_mean(ep, 'd50'))} | {pc(ep_mean(ep, 'gap'))} | "
            f"{ep_mean(ep, 'held_top'):.0%} | {dy(ep_mean(ep, 'exit_day'))} | "
            f"{pc(ep_mean(ep, 'exit_px'))} | {pc(ep_mean(ep, 'leg1'))} | "
            f"{pc(ep_mean(ep, 'band_top'))} | {ep_mean(ep, 'n_re'):.1f} | "
            f"{pc(ep_mean(ep, 're_px'))} | {pc(ep_mean(ep, 'band_re'))} | "
            f"{pc(ep_mean(ep, 'after'))} | {cnt['first leg']} / {cnt['re-entry']} / "
            f"{cnt['other']} |"
        )

    def group(label: str, eps: list[str]) -> str:
        vals = {a: mean([ep_mean(e, a) for e in eps]) for a in (
            "edge", "fall7", "d50", "gap", "exit_day", "exit_px", "leg1", "band_top",
            "n_re", "re_px", "band_re", "after")}  # fmt: skip
        fs = [x for x in rows if x.ep in eps]
        share = {
            w: sum(x.where == w for x in fs) / max(len(fs), 1) for w in ("first leg", "re-entry")
        }
        return (
            f"| {label} | {len(eps)} | {pc(vals['edge'])} | {pc(vals['fall7'])} | "
            f"{dy(vals['d50'])} | {pc(vals['gap'])} | {dy(vals['exit_day'])} | "
            f"{pc(vals['exit_px'])} | {pc(vals['leg1'])} | {pc(vals['band_top'])} | "
            f"{vals['n_re']:.1f} | {pc(vals['re_px'])} | {pc(vals['band_re'])} | "
            f"{pc(vals['after'])} | {share['first leg']:.0%} / {share['re-entry']:.0%} |"
        )

    behind = [e for e in order if e in WEEK_BEHIND]
    ahead = [e for e in order if e not in WEEK_BEHIND]
    out += [
        "",
        "## Trailing against leading episodes (each episode counts once)",
        "",
        "| Group | Episodes | Edge M | Worst 7 days | Days to -50% | Worst day | Exit day | "
        "Exit price | Leg-1 return | Band at top | Re-entries | Re-entry price | "
        "Band at re-entry | After exit | Falls: M in first leg / after re-entry |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        group("weekly stop trails (6)", behind),
        group("weekly stop leads (15)", ahead),
    ]

    # every coin fall: does speed alone sort the edge?
    fall7 = np.array([x.fall7 for x in rows])
    edge = np.array([x.edge for x in rows])
    out += [
        "",
        "## All 445 coin falls by speed of the first week (each fall once)",
        "",
        "| Worst price in the first 7 days | Falls | Mean edge M | Edge > 0 | Mean exit price | "
        "Mean after exit |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    bins = ((-np.inf, -0.40, "-40% or worse"), (-0.40, -0.25, "-25% to -40%"),
            (-0.25, -0.10, "-10% to -25%"), (-0.10, np.inf, "better than -10%"))  # fmt: skip
    for a, b, lab in bins:
        m = (fall7 > a) & (fall7 <= b)
        sel = [x for x, k in zip(rows, m, strict=True) if k]
        out.append(
            f"| {lab} | {int(m.sum())} | {pc(float(edge[m].mean()) if m.any() else np.nan)} | "
            f"{int((edge[m] > 0).sum())} | {pc(mean([x.exit_px for x in sel]))} | "
            f"{pc(mean([x.after for x in sel]))} |"
        )
    nre = np.array([x.n_re for x in rows])
    out += [
        "",
        "| Re-entries after the first exit (inside the window) | Falls | Mean edge M | Edge > 0 |"
        " Mean after exit |",
        "|---|---:|---:|---:|---:|",
    ]
    for lab, m in (("none", nre == 0), ("one", nre == 1), ("two or more", nre >= 2)):
        sel = [x for x, k in zip(rows, m, strict=True) if k]
        out.append(
            f"| {lab} | {int(m.sum())} | {pc(float(edge[m].mean()) if m.any() else np.nan)} | "
            f"{int((edge[m] > 0).sum())} | {pc(mean([x.after for x in sel]))} |"
        )

    if "btc" in names:
        out += [
            "",
            "## BTC's five falls",
            "",
            "| Top | Edge M | Worst 7 days | Days to -50% | Worst day | Exit day | Exit price "
            "| Band at top | Re-entries | Re-entry price | Band at re-entry | After exit | "
            "Twin exit day | M sits |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
        for x in (x for x in rows if x.coin == "btc"):
            out.append(
                f"| {bk.day(x.top)} | {pc(x.edge)} | {pc(x.fall7)} | {dy(x.d50)} | {pc(x.gap)} | "
                f"{dy(x.exit_day)} | {pc(x.exit_px)} | {pc(x.band_top)} | {x.n_re} | "
                f"{pc(x.re_px)} | {pc(x.band_re)} | {pc(x.after)} | {dy(x.twin_exit)} | "
                f"{x.where} |"
            )
    text = "\n".join(out) + "\n"
    print(text)
    if not DRY:
        (RESEARCH / "results" / "coin-cap-4-modes.md").write_text(text)


if __name__ == "__main__":
    main()
