"""asset-ledger-1: what trend-timing buys and costs, per live asset. Card: cards/asset-ledger-1.md.

    uv run python -I research/lib/assetledger1.py

Descriptive re-score, no new rule. Per series (the six live assets and the long proxies the
project uses for them): fall gain I, late buy-back B, calm drag C (split by calm-drag-1's
`decompose`, unchanged) and the net N = I + B + C against holding, log points a year, by
gap-2002-1's labels. Per book (the gym twins `tsmom12` and `equal-weight` on the six): the
worst drawdown and each asset's contribution to it, rebuilt exactly from the gym's fills.
Nothing after 2025-10-31. Writes research/results/asset-ledger-1.md.
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calmdrag1 as cd  # noqa: E402
import harness  # noqa: E402

from grimstrade import gym  # noqa: E402
from grimstrade.data import UNIVERSE, Bar, close_time, open_time  # noqa: E402

LAST = cd.LAST
W02 = date(2002, 1, 1)
OUT = harness.RESEARCH / "results" / "asset-ledger-1.md"
ETF_COST = 0.0002


@dataclass
class Ledger:
    i: float  # fall sessions
    b: float  # rebound sessions
    c: float  # calm sessions
    n: float  # all window sessions
    falls: int  # 25% falls with the trough in the window
    yrs: float
    resid: float  # |n - i - b - c|
    k_all: float = 0.0  # trading cost over all window sessions (not on the card; a side column)


def window(s: cd.Ser, lo: date, hi: date) -> tuple[np.ndarray, float]:
    """calm-drag-1's window mask and divisor (from the first eligible session or `lo`)."""
    n = len(s.days)
    ords = np.array([d.toordinal() for d in s.days])
    win = s.ok & (ords >= lo.toordinal()) & (ords <= hi.toordinal())
    win[0] = False
    first_ok = s.days[int(np.argmax(s.ok & (np.arange(n) > 0)))]
    return win, (hi - max(lo, first_ok)).days / 365.25


def ledger(s: cd.Ser, lo: date, hi: date, part: np.ndarray, bills: bool) -> Ledger:
    win, yrs = window(s, lo, hi)
    rf = s.rf if bills else np.zeros(len(s.days))
    flip = np.abs(np.diff(s.pos, prepend=0.0))
    r = s.pos * s.hold - s.cost * flip + (1 - s.pos) * rf
    d = 100 * (np.log1p(r) - np.log1p(s.hold))
    i, b, c = (float(d[win & (part == k)].sum()) / yrs for k in (1, 2, 0))
    n_all = float(d[win].sum()) / yrs
    hl = np.zeros(len(s.hold))
    hl[1:] = np.log1p(s.hold[1:])
    px = np.exp(np.cumsum(hl))
    falls = sum(1 for _, tr in cd.zigzag(px) if win[tr])
    k_all = float((100 * (np.log1p(r) - np.log1p(r + s.cost * flip)))[win].sum()) / yrs
    return Ledger(i, b, c, n_all, falls, yrs, abs(n_all - i - b - c), k_all)


# --- long proxies ---


def load_ust30(bill: Mapping[date, float]) -> cd.Ser:
    """pooled-2's 30-year Treasury (data-long-3's exact par-bond rebuild of `DGS30`), traded by
    insure-1's paper series (trend-1926 bars, `trend_tune.paper`, 2 bps a side)."""
    import insure1 as i1
    import insure3 as i3
    import long_x as lx
    import long_x_build as lb
    import pooled2 as p2
    import trend_1926 as t
    import trend_tune as tt

    from grimstrade.data import ETF

    y = p2._tail_after_gap(lb.alfred("DGS30"))
    rets = [(d, x) for d, x in lx.bond_returns(y, 30.0) if d <= LAST]
    sym = "AL1-UST30"
    UNIVERSE[sym] = ETF  # research process only; src/ is untouched
    bars = t.bars([d for d, _ in rets], np.array([x for _, x in rets]))
    p = tt.paper(harness.Panel({sym: bars}), sym, (12,))
    close = np.array([b.close for b in bars])
    hold = np.zeros(len(close))
    hold[1:] = close[1:] / close[:-1] - 1
    r0 = p.ret[12]
    pos = cd.repair(i1.infer_pos(r0, hold, ETF_COST), hold, r0, ETF_COST)
    back = pos * hold - ETF_COST * np.abs(np.diff(pos, prepend=0.0))
    if np.max(np.abs(back - r0)) > 1e-12:
        raise AssertionError("UST30: positions do not reproduce the paper series")
    days = [b.date for b in bars]
    rf = i3.bill_returns(days, bill)
    return cd.Ser("UST30 (TLT proxy)", days, hold, pos, np.asarray(p.ok, dtype=bool), rf,
                  ETF_COST, r0, r0 + (1 - pos) * rf)  # fmt: skip


def load_gold_monthly() -> cd.Ser:
    """trend-where-long's monthly gold (datahub, monthly averages, from 1971) and its monthly
    `tsmom12` (gap 1, 2 bps on weight changes, cash 0)."""
    import long_gold as lg
    import trend_where_long as twl

    gold = [(d, x) for d, x in lg.returns(lg.load(), lg.FREE_FROM) if d <= twl.END]
    g = twl.Grid.build({"gold": gold})
    w, live = twl.weights(g, "tsmom12", 1)
    hold = np.nan_to_num(g.r[:, 0])
    pos = w[:, 0]
    r0 = twl.book(g, w)
    back = pos * hold - twl.COST * np.abs(np.diff(pos, prepend=0.0))
    if np.max(np.abs(back - r0)) > 1e-12:
        raise AssertionError("gold: rebuilt rule differs from trend-where-long's book")
    days = [twl.mdate(g.first + k) for k in range(len(hold))]
    return cd.Ser("Gold, monthly avg (GLD proxy)", days, hold, pos, live.astype(bool),
                  np.zeros(len(hold)), twl.COST, r0, r0)  # fmt: skip


# --- book drawdown attribution ---


def attribute(res: gym.Result, hist: Mapping[str, Sequence[Bar]]
              ) -> tuple[list[date], np.ndarray, dict[str, np.ndarray], float]:  # fmt: skip
    """Per mark day of `res.equity`: each asset's dollar P&L (value change plus the cash its
    fills took or gave, fees and slippage included). Returns days, equity, P&L, and the
    largest |sum of P&L - equity change| relative to equity (cash 0, no dividends)."""
    days = [d for d, _ in res.equity]
    eq = np.array([e for _, e in res.equity])
    mk = np.array([d.toordinal() for d in days])
    pnl: dict[str, np.ndarray] = {}
    for sym, bars in hist.items():
        cls = UNIVERSE[sym]
        ev = sorted([(open_time(cls, b.date), 2, b.open) for b in bars]
                    + [(close_time(cls, b.date), 0, b.close) for b in bars])  # fmt: skip
        ev_day = np.array([((t - timedelta(microseconds=1)).date() if k == 0 else t.date())
                           .toordinal() for t, k, _ in ev])  # fmt: skip
        ev_px = np.array([p for _, _, p in ev])
        j = np.searchsorted(ev_day, mk, side="right") - 1
        price = np.where(j >= 0, ev_px[np.maximum(j, 0)], 0.0)
        fills = [f for f in res.fills if f.symbol == sym]
        fd = np.array([f.time.date().toordinal() for f in fills], dtype=np.int64)
        k = np.searchsorted(mk, fd, side="left")  # the mark day each fill lands in
        if len(fills) and (k >= len(mk)).any():
            raise AssertionError(f"{sym}: a fill after the last mark")
        dq = np.zeros(len(mk))
        cf = np.zeros(len(mk))
        np.add.at(dq, k, [f.qty for f in fills])
        np.add.at(cf, k, [-f.qty * f.price - f.fee for f in fills])
        val = np.cumsum(dq) * price
        pnl[sym] = np.diff(val, prepend=0.0) + cf
    tot = sum(pnl.values())
    de = np.diff(eq, prepend=res.start_cash)
    resid = float(np.max(np.abs(tot - de) / eq))
    return days, eq, pnl, resid


@dataclass
class Draw:
    dd: float  # worst drawdown, fraction
    peak: date
    trough: date
    contrib: dict[str, float]  # fraction of peak equity (negative = lost)


def worst(days: Sequence[date], eq: np.ndarray, pnl: Mapping[str, np.ndarray], lo: date,
          hi: date, at: tuple[date, date] | None = None) -> Draw:  # fmt: skip
    """Worst peak-to-trough drawdown of `eq` over marks in [lo, hi] (or the given peak and
    trough dates) and each asset's P&L over (peak, trough] / equity at the peak."""
    idx = [k for k, d in enumerate(days) if lo <= d <= hi]
    a0 = idx[0]
    if at is None:
        e = eq[idx]
        run = np.maximum.accumulate(e)
        tr = int(np.argmax(1 - e / run))
        pk = int(np.argmax(e[: tr + 1]))
        p, t = a0 + pk, a0 + tr
    else:
        p, t = days.index(at[0]), days.index(at[1])
    c = {s: float(x[p + 1 : t + 1].sum()) / float(eq[p]) for s, x in pnl.items()}
    return Draw(1 - float(eq[t] / eq[p]), days[p], days[t], c)


# --- report ---

HEAD = ("| Series | For | Window | Falls | Fall gain I | Buy-back B | Calm C | Cost K | Premium P "
        "| Timing T | Net N (cash 0) | Net (bills) | Out share of calm "
        "| Cost, all sessions |")  # fmt: skip


def line(nm: str, for_: str, lo: date, s: cd.Ser, part: np.ndarray, bills_ok: bool
         ) -> tuple[str, Ledger, cd.Parts, float]:  # fmt: skip
    lg0 = ledger(s, lo, LAST, part, False)
    lgb = ledger(s, lo, LAST, part, True) if bills_ok else None
    p0 = cd.decompose(s, lo, LAST, False, part)
    first = s.days[int(np.argmax(s.ok & (np.arange(len(s.days)) > 0)))]
    w = f"{max(lo, first).year}-{LAST.year}"
    nb = f"{lgb.n:+.2f}" if lgb else "-"
    txt = (f"| {nm} | {for_} | {w} | {lg0.falls} | {lg0.i:+.2f} | {lg0.b:+.2f} | {lg0.c:+.2f} | "
           f"{p0.k:+.2f} | {p0.p:+.2f} | {p0.t:+.2f} | **{lg0.n:+.2f}** | {nb} | "
           f"{p0.out_share:.3f} | {lg0.k_all:+.2f} |")  # fmt: skip
    return txt, lg0, p0, max(lg0.resid, abs(lg0.c - p0.c), p0.resid)


def main() -> None:
    import baselines as bl
    import common as c

    bill = cd.irx()
    six = cd.load_six(bill)
    fr = cd.load_french()
    spx = cd.load_spx(bill)
    ust = load_ust30(bill)
    gold = load_gold_monthly()
    hitec = next(s for s in fr if s.name == "HiTec")
    fmkt = fr[0]
    series: list[tuple[str, str, cd.Ser, list[date]]] = [
        (s.name, s.name, s, [s.days[0], W02] if s.days[0] < W02 else [s.days[0]]) for s in six
    ]
    series += [
        ("French US market", "SPY", fmkt, [fmkt.days[0], W02]),
        ("S&P 500 TR", "SPY", spx, [spx.days[0], W02]),
        ("French HiTec (loose)", "QQQ", hitec, [hitec.days[0], W02]),
        ("UST30 rebuild", "TLT", ust, [ust.days[0], W02]),
        ("Gold, monthly averages", "GLD", gold, [gold.days[0], W02, date(2005, 11, 1)]),
    ]
    rows, checks, store = [], 0.0, {}
    for nm, for_, s, starts in series:
        part = cd.labels(s.days, s.hold)
        for lo in starts:
            txt, lg0, p0, ck = line(nm, for_, lo, s, part, nm != "Gold, monthly averages")
            rows.append(txt)
            checks = max(checks, ck)
            store[(nm, lo.year)] = (lg0, p0)
    # books
    ctx = c.ctx("six")
    hist = {k: [b for b in v if b.date <= LAST] for k, v in ctx.hist.items()}
    tw = bl.twins()
    books = {}
    for nm in ("tsmom12", "equal-weight"):
        run = c.go(bl.IDEA, nm, tw[nm], ctx, "baseline", log=False)
        decs = [d for d in run.decisions if d.time.date() <= LAST]
        res = gym.simulate(decs, hist)
        days, eq, pnl, resid = attribute(res, hist)
        known = dict(zip(run.days, run.equity, strict=True))
        gap = max(abs(known[d] - e) / e for d, e in zip(days, eq, strict=True) if d in known
                  and d < LAST)  # fmt: skip
        books[nm] = (days, eq, pnl, resid, gap)
    syms = list(hist)
    bk_rows = []
    for lo in (harness.TRAIN_START, W02):
        dh = worst(*books["equal-weight"][:3], lo, LAST)
        dt = worst(*books["tsmom12"][:3], lo, LAST)
        dx = worst(*books["tsmom12"][:3], lo, LAST, at=(dh.peak, dh.trough))
        for lab, dr in (("without timing (`equal-weight`)", dh), ("with timing (`tsmom12`)", dt),
                        ("`tsmom12` over the `equal-weight` dates", dx)):  # fmt: skip
            tot = sum(dr.contrib.values())
            cells = " | ".join(
                f"{100 * dr.contrib[s]:+.1f} ({dr.contrib[s] / tot:.0%})" if tot else "0"
                for s in syms
            )
            bk_rows.append(f"| {lo.year}-{LAST.year} | {lab} | {100 * dr.dd:.1f}% | {dr.peak} .. "
                           f"{dr.trough} | {cells} |")  # fmt: skip
    md = [
        "# asset-ledger-1 results (generated by `research/lib/assetledger1.py`; do not edit)",
        "",
        "## A. Per series: `tsmom12` minus holding, log points a year",
        "",
        "Labels: gap-2002-1's (25% / 25% zigzag on the series' own total-return index, rebound = "
        "365 days after the trough or the next peak). N = I + B + C; C = K + P + T "
        "(calm-drag-1's `decompose`). Cash 0 unless marked. Falls: 25% falls with the trough in "
        "the window. Negative = costs the rule. Cost, all sessions: trading cost over every "
        "window session (in I, B and C; a side column, not on the card).",
        "",
        HEAD,
        "|---|---|---|" + "---:|" * 11,
        *rows,
        "",
        f"Checks: largest |N - I - B - C|, |C - calm-drag-1's C| and calm-split residual over "
        f"all rows {checks:.1e}.",
        "",
        "## B. Six-asset book: worst drawdown and each asset's share (gym, cash 0)",
        "",
        "Contribution: the asset's dollar P&L over (peak, trough] / equity at the peak, in "
        "percent of peak equity (share of the total in brackets). Rows sum to minus the "
        "drawdown.",
        "",
        "| Window | Book | Worst drawdown | Peak .. trough | " + " | ".join(syms) + " |",
        "|---|---|---:|---|" + "---:|" * len(syms),
        *bk_rows,
        "",
        "Checks: largest |sum of asset P&L - equity change| / equity: "
        + ", ".join(f"{k} {v[3]:.1e}" for k, v in books.items())
        + "; largest gap to the harness run's equity: "
        + ", ".join(f"{k} {v[4]:.1e}" for k, v in books.items())
        + ".",
        "",
    ]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
