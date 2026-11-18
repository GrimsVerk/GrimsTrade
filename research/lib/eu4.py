"""eu-4: where the coin-free EUR book's orders go, and whipsaw reducers (cards/eu-4.md).

    uv run --with numpy python research/lib/eu4.py diag    # step 1: descriptive note, no row

Needs the CSVs from `eu1_data.py build`. Train period only. Fees are described as generic
tiers: EUR 1, 2 or 3 per ETF order on a constant book (eu-2's three schedules,
reused unchanged so numbers compare with eu-2 and eu-3).

`diag` replays the house rule `tsmom12` on `euw` at no fixed fee (the configuration eu-3 logged
as `tsmom12@euw/slip`; replaying it adds no row) and sorts every ETF order by cause.
"""

from __future__ import annotations

import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import eu1
import eu2
import eu3
import harness
import numpy as np

from grimstrade import gym
from grimstrade.data import ETF, UNIVERSE

IDEA = "eu-4"
EUW = eu1.EUW
W_START = eu1.W_START
TIERS = [("EUR 1", eu2.SCHEDULES[1]), ("EUR 2", eu2.SCHEDULES[2]), ("EUR 3", eu2.SCHEDULES[3])]
NS = [4, 8, 13, 26]  # whipsaw horizons in weeks


@dataclass
class Spell:
    sym: str
    held: bool  # True = an in-spell (entry .. exit), False = an out-spell (exit .. re-entry)
    start: date  # Friday of the flip that opened it
    end: date | None  # Friday of the flip that closed it (None = still open at the end)
    weeks: int
    peak_z: float  # largest |z| (12-month log return / one-year vol) inside the spell
    move: float  # the asset's log return from the opening flip to the closing flip


def z_score(view: harness.View, s: str) -> float:
    """12-month log return in units of the asset's own volatility (60-bar half-life EWMA)."""
    r = c.trailing_logret(view, s, 365)
    v = c.asset_vol(view, s, 60)
    return r / v if v > 0 and not math.isnan(r) else math.nan


def friday_series(
    syms: list[str],
) -> tuple[list[date], dict[str, list[bool]], dict[str, list[float]], dict[str, list[float]]]:
    """Per Friday from F0: the house rule's held state, z, and the 12-month log return."""
    _, pan = eu1.panel_for(syms)
    fw = eu3.friday_weights(eu3.R, pan)
    fridays = [f for f, _ in fw]
    held = {s: [s in w for _, w in fw] for s in syms}
    zs: dict[str, list[float]] = {s: [] for s in syms}
    r12: dict[str, list[float]] = {s: [] for s in syms}
    for f in fridays:
        view = pan.view(harness.decide_time(f))
        for s in syms:
            ok = s in c.live(view)
            zs[s].append(z_score(view, s) if ok else math.nan)
            r12[s].append(c.trailing_logret(view, s, 365) if ok else math.nan)
    return fridays, held, zs, r12


def close_on(pan: harness.Panel, s: str, f: date) -> float:
    return float(pan.view(harness.decide_time(f)).close(s)[-1])


def spells(
    syms: list[str], fridays: list[date], held: dict[str, list[bool]],
    zs: dict[str, list[float]],
) -> list[Spell]:  # fmt: skip
    _, pan = eu1.panel_for(syms)
    out = []
    for s in syms:
        h = held[s]
        flips = [i for i in range(1, len(h)) if h[i] != h[i - 1]]
        for a, b in zip([0, *flips], [*flips, None]):  # noqa: B905
            if a == 0:
                continue  # the state before the first flip is the start-up build, not a spell
            end = len(h) - 1 if b is None else b
            seg = [abs(x) for x in zs[s][a:end] if not math.isnan(x)]
            move = math.log(close_on(pan, s, fridays[end]) / close_on(pan, s, fridays[a]))
            out.append(
                Spell(
                    s,
                    h[a],
                    fridays[a],
                    None if b is None else fridays[b],
                    end - a,
                    max(seg) if seg else math.nan,
                    move,
                )  # fmt: skip
            )
    return out


def classify_fills(fills: list[gym.Fill]) -> dict[str, list[tuple[date, str]]]:
    """Per symbol, (fill date, 'entry' | 'exit' | 'drift') for every ETF fill."""
    pos: dict[str, float] = defaultdict(float)
    out: dict[str, list[tuple[date, str]]] = defaultdict(list)
    for f in fills:
        if UNIVERSE[f.symbol] != ETF:
            continue
        before = pos[f.symbol]
        pos[f.symbol] = before + f.qty
        kind = "entry" if before <= 1e-12 else ("exit" if pos[f.symbol] <= 1e-12 else "drift")
        out[f.symbol].append((f.time.date(), kind))
    return out


def diag() -> None:
    hist, pan = eu1.panel_for(EUW)
    decs = eu3.make_decisions(eu3.R, pan)
    res = gym.simulate(decs, hist, costs=eu2.COSTS, band=eu3.BAND)
    days, equity = harness._calendar(res.equity)
    years = (days[-1] - days[0]).days / 365
    lr = np.diff(np.log(np.asarray(equity)))
    vol = float(np.std(lr) * math.sqrt(365))
    fills = classify_fills(res.fills)
    start_build = {s: sum(1 for d, k in v if k == "entry" and d <= W_START + timedelta(days=7))
                   for s, v in fills.items()}  # fmt: skip

    fridays, held, zs, r12 = friday_series(EUW)
    sp = spells(EUW, fridays, held, zs)
    closed = [x for x in sp if x.end is not None]

    out = ["# eu-4 step 1: where `euw` spends its order budget (descriptive)", ""]
    out += [
        "Train period only, window W (decisions 2012-01-02 .. 2025-11-09), the house rule "
        "`tsmom12` on `euw` (SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY; 7 equal slots, Friday "
        "signal, weights repeated daily, 1% band), EUR, total-return prices, ETF slippage 0.05% "
        "a side, no fixed fee. This replays eu-3's `tsmom12@euw/slip` (no new `tries.md` row). "
        "Fee tiers are generic: EUR 1, 2 or 3 per ETF order on a constant book (eu-2's schedules; "
        "the EUR 1 and EUR 3 tiers also carry a EUR 2.50 yearly fee, the EUR 2 tier none). "
        f"Book vol at no fee: {vol:.1%}. Fee drag in Sharpe = fees per year / vol.",
        "",
    ]

    # 1. orders by cause
    tot: dict[str, int] = defaultdict(int)
    for v in fills.values():
        for _, k in v:
            tot[k] += 1
    n_build = sum(start_build.values())
    flip_in, flip_out, drift = tot["entry"] - n_build, tot["exit"], tot["drift"]
    n_all = sum(tot.values())

    # whipsaw: orders that belong to a spell (in or out) closed within N weeks
    def whip(n: int, held_side: bool | None = None) -> list[Spell]:
        return [x for x in closed if x.weeks <= n and (held_side is None or x.held == held_side)]

    out += ["## 1. Orders by cause", ""]
    out += [
        "A spell is the time between two signal flips of one slot, counted in Fridays. A "
        "**whipsaw** is a spell that the next flip closes within N weeks: an in-spell (bought, "
        "sold again) or an out-spell (sold, bought back); its two flips are two orders that "
        "cancel each other. Drift = top-ups and trims of held slots back to 1/7 once they "
        "stray by 1% of the book.",
        "",
        "| Cause | Orders | Per year | Share | Fee/yr EUR 1 tier, 5k / 10k book | EUR 2 | EUR 3 | "
        "Sharpe drag at 10k (EUR 1 / 2 / 3) |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]

    def fee_cells(n_yr: float) -> str:
        cells = []
        for _, sch in TIERS:
            cells.append(f"EUR {n_yr * sch.per_order:.0f} ({n_yr * sch.per_order / 5000:.2%}"
                         f" / {n_yr * sch.per_order / 10000:.2%})")  # fmt: skip
        drag = " / ".join(f"{n_yr * sch.per_order / 10000 / vol:.3f}" for _, sch in TIERS)
        return " | ".join(cells) + f" | {drag} |"

    rows = [
        ("Start-up build (2012-01)", n_build),
        ("Signal flip in (entry)", flip_in),
        ("Signal flip out (exit)", flip_out),
        ("Drift top-up / trim", drift),
        ("All", n_all),
    ]
    for name, n in rows:
        if name.startswith("Start"):
            out.append(f"| {name} | {n} | - | {n / n_all:.0%} | - | - | - | - |")
        else:
            head = f"| {name} | {n} | {n / years:.1f} | {n / n_all:.0%} | "
            out.append(head + fee_cells(n / years))
    out += [
        "",
        "(The yearly EUR 2.50 of two tiers is not an order and is left out of these columns; "
        "at 5k / 10k it is 0.05% / 0.025% of the book a year.)",
        "",
    ]

    # whipsaw by horizon
    out += [
        "Flip orders that sit in whipsaw spells (both orders of each short spell; a flip can "
        "close one spell and open the next, so each spell is charged its two flips once):",
        "",
        "| N weeks | Short in-spells | Short out-spells | Orders in them / yr | Share of flip "
        "orders | Share of all orders | Fee/yr at 10k, EUR 1 / 2 / 3 | Sharpe drag at 10k "
        "(EUR 1 / 2 / 3) | Asset move inside (log pts/yr; in-spells / out-spells) |",
        "|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    flip_orders = flip_in + flip_out
    for n in NS:
        wi, wo = whip(n, True), whip(n, False)
        # orders: each short spell = the flip that opened it + the flip that closed it; flips
        # shared by two adjacent short spells are counted once
        flips_set = set()
        for x in [*wi, *wo]:
            flips_set.add((x.sym, x.start))
            if x.end is not None:
                flips_set.add((x.sym, x.end))
        k = len(flips_set) / years
        fee = " / ".join(f"EUR {k * sch.per_order:.0f}" for _, sch in TIERS)
        drag = " / ".join(f"{k * sch.per_order / 10000 / vol:.3f}" for _, sch in TIERS)
        mi = sum(x.move for x in wi) / years * 100 / len(EUW)
        mo = sum(x.move for x in wo) / years * 100 / len(EUW)
        out.append(
            f"| {n} | {len(wi)} | {len(wo)} | {k:.1f} | {len(flips_set) / flip_orders:.0%} | "
            f"{len(flips_set) / n_all:.0%} | {fee} | {drag} | {mi:+.2f} / {mo:+.2f} |"
        )
    out += [
        "",
        "Asset move inside = the asset's own log return from the opening to the closing flip, "
        "summed over spells, per year, divided by 7 (one slot's share of the book). For an "
        "in-spell a negative number is money lost while held; for an out-spell a positive "
        "number is the move missed while out. Fills are at the next open; these are Friday "
        "closes, so the size is approximate. These moves are selected by hindsight (a spell is a "
        "whipsaw *because* the asset turned), so they are not a cost any rule could avoid; "
        "they show only that whipsaws are not free of market loss either.",
        "",
    ]

    # 2. per asset
    out += ["## 2. Which assets whipsaw", ""]
    out += [
        "| Asset | Flips/yr | Spells | Median spell (wk) | Whipsaw spells <= 4 wk | <= 13 wk | "
        "Share of all <= 13 wk whipsaw | Drift orders/yr | Weekly noise of z (sd of weekly "
        "change) | Median |z| at a flip |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    all13 = len(whip(13))
    for s in EUW:
        mine = [x for x in closed if x.sym == s]
        flips_n = sum(1 for i in range(1, len(held[s])) if held[s][i] != held[s][i - 1])
        dz = np.diff(np.array([x for x in zs[s] if not math.isnan(x)]))
        zf = [abs(zs[s][i]) for i in range(1, len(held[s])) if held[s][i] != held[s][i - 1]
              and not math.isnan(zs[s][i])]  # fmt: skip
        w4 = sum(1 for x in mine if x.weeks <= 4)
        w13 = sum(1 for x in mine if x.weeks <= 13)
        dr = sum(1 for _, k in fills.get(s, []) if k == "drift") / years
        med = float(np.median([x.weeks for x in mine])) if mine else math.nan
        out.append(
            f"| {s} | {flips_n / years:.1f} | {len(mine)} | {med:.0f} | {w4} | {w13} | "
            f"{w13 / all13:.0%} | {dr:.1f} | {float(np.std(dz)):.2f} | "
            f"{float(np.median(zf)) if zf else math.nan:.2f} |"
        )
    out += [""]

    # 3. spell length distribution and peak |z|
    out += ["## 3. How short and how shallow are the whipsaws", ""]
    out += [
        "Closed spells by length (Fridays), and the largest |z| reached inside each "
        "(z = 12-month log return / the asset's one-year EWMA vol, 60-bar half-life; the "
        "signal is the sign of z). A dead zone of half-width h (enter above +h, leave below -h) "
        "would have removed a spell whose |z| never got past h, other things equal; a "
        "confirmation rule (two Fridays in a row) removes every 1-Friday spell and delays the "
        "rest by a week.",
        "",
        "| Length | Spells | In / out | Median peak \\|z\\| | Share with peak \\|z\\| < 0.25 "
        "| < 0.5 | Median move inside (log pts, in / out) |",
        "|---|---:|---|---:|---:|---:|---|",
    ]
    buckets = [
        (1, 1, "1 week"), (2, 2, "2 weeks"), (3, 4, "3-4 weeks"), (5, 8, "5-8 weeks"),
        (9, 13, "9-13 weeks"), (14, 26, "14-26 weeks"), (27, 10_000, "> 26 weeks"),
    ]  # fmt: skip
    for lo, hi, name in buckets:
        b = [x for x in closed if lo <= x.weeks <= hi]
        if not b:
            continue
        pk = [x.peak_z for x in b if not math.isnan(x.peak_z)]
        bi = [x.move for x in b if x.held]
        bo = [x.move for x in b if not x.held]
        mi = f"{float(np.median(bi)) * 100:+.1f}" if bi else "-"
        mo = f"{float(np.median(bo)) * 100:+.1f}" if bo else "-"
        out.append(
            f"| {name} | {len(b)} | {len(bi)} / {len(bo)} | {float(np.median(pk)):.2f} | "
            f"{np.mean([p < 0.25 for p in pk]):.0%} | {np.mean([p < 0.5 for p in pk]):.0%} | "
            f"{mi} / {mo} |"
        )
    pk_long = [x.peak_z for x in closed if x.weeks > 26]
    pooled_dz = float(
        np.std(np.concatenate([np.diff([v for v in zs[s] if not math.isnan(v)]) for s in EUW]))
    )
    out += [
        "",
        f"All weekly z changes, pooled over the 7 assets: sd {pooled_dz:.2f}"
        f". Long spells (> 26 weeks) reach a median peak |z| of {float(np.median(pk_long)):.2f}.",
        "",
    ]
    c.write_result(f"{IDEA}-diag", "\n".join(out))


if __name__ == "__main__":
    {"diag": diag}[sys.argv[1]]()
