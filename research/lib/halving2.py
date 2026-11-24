"""halving-2: the frozen `halving-alone` rule on other halving coins (card `research/halving-2.md`).

    DRY=1 GRIMSTRADE_DATA=<cache root> uv run python -I research/lib/halving2.py   # counts only
    GRIMSTRADE_DATA=<cache root> uv run python -I research/lib/halving2.py         # the one run

Coin Metrics daily prices (keyless, shared cache), cut at 2025-11-10. The judged test is `LZ`
(LTC + ZEC, equal slots): own clocks against BTC's clock, 40 shifted-calendar placebos each.
"""

from __future__ import annotations

import math
import os
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common as c  # noqa: E402
import halving2_core as h  # noqa: E402
import harness  # noqa: E402
import macro  # noqa: E402
import numpy as np  # noqa: E402
import stats  # noqa: E402

from grimstrade.data import CRYPTO, UNIVERSE, Bar  # noqa: E402

IDEA = "halving-2"
DRY = bool(os.environ.get("DRY"))
COINS = ["LTC", "ZEC", "BCH", "BSV", "ETC"]
JUDGED = ["LTC", "ZEC"]
for _s in [*COINS, "BTC"]:
    UNIVERSE.setdefault(_s, CRYPTO)  # research-only registration, as harness.UNIVERSE_EXTRA

Cals = Mapping[str, Sequence[date]]


def alone(cals: Cals, trend: bool = False) -> c.ResearchStrategy:
    """Each eligible coin's equal slot, held unless today is in its window (and, with `trend`,
    only while its 365-day return is positive)."""

    def f(view: harness.View) -> c.Weights:
        held = c.live(view)
        out = {}
        for s in held:
            if h.in_window(cals[s], view.today):
                continue
            if trend and not c.tsmom_signal(view, s):
                continue
            out[s] = 1 / len(held)
        return out

    return c.weekly(f)


def ctx(name: str, hist: dict[str, list[Bar]]) -> c.Ctx:
    first = min(b[0].date for b in hist.values())
    start = first + timedelta(days=366)
    end = min(harness.TRAIN_END, max(b[-1].date for b in hist.values()) - timedelta(days=1))
    return c.Ctx(name, "train", hist, harness.Panel(hist), start, end)


def sharpe(run: harness.Run) -> float:
    return float(stats.sharpe(run.rets))


def z_vs(a: harness.Run, b: harness.Run) -> tuple[float, float, float]:
    x, y = c.align(a, b)
    diff, p, lo, hi = stats.sharpe_diff_boot(x, y)
    se = (hi - lo) / 3.29
    return diff, p, diff / se if se > 0 else math.nan


def screen_row(variant: str, start: date, end: date) -> None:
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | screen | train | "
        f"{start} | {end} | - | - | - | - |\n"
    )
    with harness.TRIES.open("a") as f:
        f.write(row)


def window_days(cal: Sequence[date], a: date, b: date) -> int:
    return sum(h.in_window(cal, a + timedelta(days=k)) for k in range((b - a).days + 1))


def main() -> None:
    root = macro.cache_root()
    px: dict[str, dict[date, float]] = {}
    hist: dict[str, list[Bar]] = {}
    for s in [*COINS, "BTC"]:
        rows = h.load_rows(root, s)
        px[s] = h.prices_from_rows(rows)
        hist[s] = h.bars(px[s], h.volumes_from_rows(rows))
        assert hist[s][-1].date <= harness.TRAIN_LAST_BAR
    own = {s: h.CALENDARS[s] for s in [*COINS, "BTC"]}
    btc_on = {s: h.CALENDARS["BTC"] for s in [*COINS, "BTC"]}
    shifts = h.draw_shifts(JUDGED)
    btc_shifts = h.draw_shifts(["BTC"], seed=h.SEED + 1)

    if DRY:
        print("DRY: counts only, no return computed, nothing logged")
        for s in [*COINS, "BTC"]:
            b = hist[s]
            st = b[0].date + timedelta(days=366)
            print(f"{s}: {len(b)} bars {b[0].date}..{b[-1].date}; test from {st}; "
                  f"own-window days {window_days(own[s], st, harness.TRAIN_END)}, "
                  f"BTC-window days {window_days(btc_on[s], st, harness.TRAIN_END)}")  # fmt: skip
        for s in JUDGED:
            lo, hi = h.shift_bounds(h.CALENDARS[s])
            mags = sorted(abs(r[s]) for r in shifts)
            print(f"{s} placebo shifts in +-[{lo}, {hi}]: {sum(r[s] > 0 for r in shifts)} forward, "
                  f"magnitudes {mags[0]}..{mags[-1]}")  # fmt: skip
        lo, hi = h.shift_bounds(h.CALENDARS["BTC"])
        print(f"BTC placebo shifts in +-[{lo}, {hi}]: {len(btc_shifts)}")
        # plumbing on a random walk with the same dates: decision and fill counts only
        rng = np.random.default_rng(0)
        fake = {}
        for s in JUDGED:
            ds = [b.date for b in hist[s]]
            p = np.exp(np.cumsum(rng.normal(0, 0.04, len(ds))))
            fake[s] = h.bars(dict(zip(ds, (float(x) for x in p), strict=True)))
        k = ctx("LZ", fake)
        run = harness.run(IDEA, "dry", alone(own), panel=k.panel, history=k.hist,
                          start=k.start, end=k.end, kind="robustness", log=False)  # fmt: skip
        held = sum(bool(d.weights) for d in run.decisions)
        print(f"plumbing (random prices): {len(run.decisions)} decisions, {held} with a holding, "
              f"{len(run.score.__dict__)} score fields")  # fmt: skip
        print(f"real run would make {5 + 4 * len(COINS) + 3} logged runs and "
              f"{40 * 3 + 40 * len(JUDGED)} placebo runs")  # fmt: skip
        return

    out: list[str] = []
    logged: list[str] = []

    def go(name: str, syms: Sequence[str], variant: str, strat: c.ResearchStrategy,
           kind: str) -> harness.Run:  # fmt: skip
        k = ctx(name, {s: hist[s] for s in syms})
        logged.append(f"{variant}@{name}")
        return c.go(IDEA, variant, strat, k, kind)

    def placebo(name: str, syms: Sequence[str], strat: c.ResearchStrategy) -> harness.Run:
        k = ctx(name, {s: hist[s] for s in syms})
        return harness.run(IDEA, "placebo", strat, panel=k.panel, history=k.hist, start=k.start,
                           end=k.end, kind="robustness", log=False)  # fmt: skip

    # --- the judged test: LZ ---
    lz = {
        "bh": go("LZ", JUDGED, "bh", c.equal_weight, "baseline"),
        "tsmom12": go("LZ", JUDGED, "tsmom12", c.weekly(c.slots(c.tsmom_signal)), "baseline"),
        "alone-own": go("LZ", JUDGED, "alone-own", alone(own), "robustness"),
        "alone-btc": go("LZ", JUDGED, "alone-btc", alone(btc_on), "robustness"),
        "and-own": go("LZ", JUDGED, "and-own", alone(own, trend=True), "robustness"),
    }
    k0 = ctx("LZ", {s: hist[s] for s in JUDGED})
    s1 = sharpe(lz["alone-own"])
    s2 = sharpe(lz["alone-btc"])
    p1, p1_exp = [], []
    pc = {s: [] for s in JUDGED}  # per-coin placebo Sharpes (shown)
    c2p = []
    starts = {s: hist[s][0].date + timedelta(days=366) for s in JUDGED}
    for row in shifts:
        cal = {s: h.placebo_calendar(h.CALENDARS[s], row[s]) for s in JUDGED}
        r = placebo("LZ", JUDGED, alone(cal))
        p1.append(sharpe(r))
        p1_exp.append(r.exposure)
        for s in JUDGED:
            pc[s].append(sharpe(placebo(s, [s], alone(cal))))
        c2p.append(h.relative_gap({s: px[s] for s in JUDGED}, px["BTC"], cal, starts,
                                  harness.TRAIN_END)[0])  # fmt: skip
    p2, p2_exp = [], []
    for row in btc_shifts:
        cal_b = h.placebo_calendar(h.CALENDARS["BTC"], row["BTC"])
        r = placebo("LZ", JUDGED, alone({s: cal_b for s in JUDGED}))
        p2.append(sharpe(r))
        p2_exp.append(r.exposure)
    c2, n_in, n_out = h.relative_gap({s: px[s] for s in JUDGED}, px["BTC"], own, starts,
                                     harness.TRAIN_END)  # fmt: skip
    rank1, rank2 = h.rank_high(s1, p1), h.rank_high(s2, p2)
    rank_c2 = h.rank_low(c2, c2p)
    d_bh, p_bh, z_bh = z_vs(lz["alone-own"], lz["bh"])
    d_ts, p_ts, z_ts = z_vs(lz["alone-own"], lz["tsmom12"])
    d_ob, p_ob, z_ob = z_vs(lz["alone-own"], lz["alone-btc"])
    db_bh, pb_bh, zb_bh = z_vs(lz["alone-btc"], lz["bh"])
    db_ts, _, zb_ts = z_vs(lz["alone-btc"], lz["tsmom12"])

    bar = [
        ("1. S1 ranks 1-2 of 41", rank1 <= 2, f"rank {rank1} of 41"),
        ("2. alone-own beats bh, z >= 2", d_bh > 0 and z_bh >= 2, f"{d_bh:+.2f}, z {z_bh:.2f}"),
        ("3. alone-own beats tsmom12", d_ts > 0, f"{d_ts:+.2f}, z {z_ts:.2f}"),
        ("4. alone-own beats alone-btc, C2 < 0 and rank 1-2 (most negative)",
         d_ob > 0 and c2 < 0 and rank_c2 <= 2,
         f"{d_ob:+.2f} (z {z_ob:.2f}); C2 {c2 * 365:+.3f}/yr, rank {rank_c2} of 41"),
    ]  # fmt: skip
    h1 = all(ok for _, ok, _ in bar)
    btc_beta = (not h1) and rank2 <= 2 and db_bh > 0 and zb_bh >= 2

    runs = list(lz.values())
    out += ["# halving-2: the frozen halving rule on Litecoin and Zcash (and shown coins)", "",
            "Script `lib/halving2.py`; card `halving-2.md`. Coin Metrics daily prices, train "
            "only. Cash earns 0.", "", f"## LZ = LTC + ZEC, equal slots, from {k0.start}", "",
            c.table(runs, versus=lz["bh"]), "", "Against the coins' own `tsmom12`:", "",
            c.table(runs, versus=lz["tsmom12"], eras=False), "",
            "## Placebos (40 each, gate-null)", "",
            "| Statistic | True | Rank | Placebo null | Mean exposure true / placebos |",
            "|---|---:|---:|---|---:|",
            f"| S1: Sharpe of alone-own@LZ, own calendars shifted | {s1:.3f} | {rank1} of 41 | "
            f"{h.null_summary(p1)} | {lz['alone-own'].exposure:.0%} / {np.mean(p1_exp):.0%} |",
            f"| S2: Sharpe of alone-btc@LZ, BTC calendar shifted | {s2:.3f} | {rank2} of 41 | "
            f"{h.null_summary(p2)} | {lz['alone-btc'].exposure:.0%} / {np.mean(p2_exp):.0%} |",
            f"| C2: alt/BTC log return per year, own window minus outside (predicted < 0) | "
            f"{c2 * 365:+.3f} | {rank_c2} of 41 (most negative) | "
            f"{h.null_summary([x * 365 for x in c2p])} | {n_in} days in / {n_out} out |",
            "", "Differences (paired stationary bootstrap; z = diff / ((q95 - q05) / 3.29)):", "",
            f"- alone-own vs bh {d_bh:+.2f} (p {p_bh:.2f}, z {z_bh:.2f}); vs tsmom12 {d_ts:+.2f} "
            f"(p {p_ts:.2f}, z {z_ts:.2f}); vs alone-btc {d_ob:+.2f} (p {p_ob:.2f}, z {z_ob:.2f})",
            f"- alone-btc vs bh {db_bh:+.2f} (p {pb_bh:.2f}, z {zb_bh:.2f}); vs tsmom12 "
            f"{db_ts:+.2f} (z {zb_ts:.2f})", "",
            "## Pass bar (card)", ""]  # fmt: skip
    out += [f"- {'PASS' if ok else 'FAIL'}: {name} ({txt})" for name, ok, txt in bar]
    verdict = ("H1 holds: transfers on own clocks (kill-only gate: not dead)" if h1
               else "BTC-beta: H1 fails, the BTC clock works on the alts" if btc_beta
               else "no transfer: H1 fails and the BTC clock does not pass either")  # fmt: skip
    out += ["", f"**Verdict: {verdict}.**", "", c.stress_table(runs), ""]

    # --- shown: each coin alone, and BTC ---
    out += ["## Shown: each coin alone (own clock and BTC clock)", ""]
    for s in COINS:
        rs = [go(s, [s], "bh", c.equal_weight, "baseline"),
              go(s, [s], "tsmom12", c.weekly(c.slots(c.tsmom_signal)), "baseline"),
              go(s, [s], "alone-own", alone(own), "robustness"),
              go(s, [s], "alone-btc", alone(btc_on), "robustness")]  # fmt: skip
        extra = ""
        if s in JUDGED:
            extra = (
                f" Own-clock placebo rank on {s} alone (the LZ shifts): "
                f"{h.rank_high(sharpe(rs[2]), pc[s])} of 41; null {h.null_summary(pc[s])}."
            )
        out += [f"### {s} (cuts {', '.join(str(d) for d in h.CALENDARS[s])}){extra}", "",
                c.table(rs, versus=rs[0]), ""]  # fmt: skip
    rb = [go("BTC", ["BTC"], "bh", c.equal_weight, "baseline"),
          go("BTC", ["BTC"], "tsmom12", c.weekly(c.slots(c.tsmom_signal)), "baseline"),
          go("BTC", ["BTC"], "alone-own", alone(own), "robustness")]  # fmt: skip
    pbtc = [sharpe(placebo("BTC", ["BTC"],
                           alone({"BTC": h.placebo_calendar(h.CALENDARS["BTC"], r["BTC"])})))
            for r in btc_shifts]  # fmt: skip
    rank_b = h.rank_high(sharpe(rb[2]), pbtc)
    out += ["### BTC alone, BTC clock (in-sample replication on this data source)", "",
            c.table(rb, versus=rb[0]), "",
            f"Placebo rank of alone-own on BTC: {rank_b} of 41; null {h.null_summary(pbtc)}.", "",
            "Placebo shifts (days): " + "; ".join(f"{r['LTC']:+d}/{r['ZEC']:+d}" for r in shifts)
            + " (LTC/ZEC); BTC: "
            + ", ".join(f"{r['BTC']:+d}" for r in btc_shifts) + "."]  # fmt: skip

    end = harness.TRAIN_END
    screen_row(
        f"S1 alone-own@LZ own-calendar placebos (Sharpe {s1:.2f}, rank {rank1}/41, "
        f"null SD {np.std(p1, ddof=1):.2f}, {'pass' if rank1 <= 2 else 'fail'})",
        k0.start,
        end,
    )
    screen_row(
        f"S2 alone-btc@LZ BTC-calendar placebos (Sharpe {s2:.2f}, rank {rank2}/41, "
        f"null SD {np.std(p2, ddof=1):.2f})",
        k0.start,
        end,
    )
    screen_row(f"C2 LZ alt/BTC own window minus outside ({c2 * 365:+.3f}/yr, rank {rank_c2}/41 "
               f"most negative; gate {'pass' if h1 else 'fail'}: {verdict.split(':')[0]})",
               k0.start, end)  # fmt: skip
    screen_row(f"BTC alone-own placebos (rank {rank_b}/41, shown)",
               hist["BTC"][0].date + timedelta(days=366), end)  # fmt: skip
    c.write_result(IDEA, "\n".join(out))
    print(f"logged runs: {len(logged)}")


if __name__ == "__main__":
    main()
