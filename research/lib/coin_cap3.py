"""coin-cap-3: does reading `stop-0.25` every day fix its fast-crash losses against a cap of
matched cost, without whipsaw and fees eating the gain? (card: research/cards/coin-cap.md,
"Fourth reading").

    uv run python -I research/lib/coin_cap3.py          # the real run: logs 6 tries rows
    DRY=1 uv run python -I research/lib/coin_cap3.py    # plumbing on random prices, logs nothing

Writes `research/results/coin-cap-3.md` (the real run only).
"""

from __future__ import annotations

import fcntl
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import coin_cap2 as cc2  # noqa: E402
import coin_cap2_core as k2  # noqa: E402
import coin_cap3_core as k3  # noqa: E402
import cointop1 as ct1  # noqa: E402
import cointop1_core as core  # noqa: E402
import stats  # noqa: E402
from harness import RESEARCH, TRAIN_END, TRIES  # noqa: E402

IDEA = "coin-cap-3"
DRY = bool(os.environ.get("DRY"))
STOP_K = cc2.STOP_K
M_PICKS = 13  # coin-cap variant rows (9) + coin-cap-2 (2) + this reading's 2
ALPHA = 0.10 / M_PICKS
WEEK_BEHIND = ("market-0", "market-2", "own-0", "own-1", "own-3", "market-6")
NAMES = ("TS", "stop-0.25", "stop-0.25-d", "stop-0.25-dx")
VARIANTS = ("stop-0.25-d", "stop-0.25-dx")
WEEKLY = "stop-0.25"


@dataclass
class S:
    """One per-coin paper series at 0x, 1x and 2x costs."""

    name: str
    hold: np.ndarray
    dec: np.ndarray
    base: np.ndarray
    pos: np.ndarray
    r0: np.ndarray
    r1: np.ndarray
    r2: np.ndarray


def make(bk: cc2.Book2, name: str, hold: np.ndarray, dec: np.ndarray, base: np.ndarray) -> S:
    px, c = bk.book.px, float(bk.book.cost.max())
    r1, pos = core.paper(px, hold, base, c)
    r0, _ = core.paper(px, hold, base, 0.0)
    r2, _ = core.paper(px, hold, base, 2 * c)
    return S(name, hold, dec, base, pos, r0, r1, r2)


def portfolio(bk: cc2.Book2, s: S, scale: float, mult: float) -> tuple[np.ndarray, float]:
    """Equal-slot book of a series (slot 1 / universe coins of the Friday decision in force),
    from the first weekly set day, at `mult` x the book's costs; daily returns, turnover a year."""
    n_univ = bk.univ.sum(1)
    w_of = np.searchsorted(bk.d, s.dec, side="right") - 1
    n = np.where(w_of >= 0, n_univ[np.maximum(w_of, 0)], 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        targets = np.where(n[:, None] >= 1, s.hold / np.maximum(n, 1)[:, None], 0.0) * scale
    first = int(bk.b[0])
    r = xs.simulate(bk.book.px, targets, s.base, bk.book.cost * mult, first)
    turn = float(np.abs(np.diff(targets, axis=0)).sum() / (len(r) / 365))
    return r, turn


def log_row(variant: str, kind: str, first: date, r: np.ndarray, turn: float) -> None:
    eq = np.cumprod(1 + r)
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | {kind} | train | {first} | "
        f"{TRAIN_END} | {stats.sharpe(r):.2f} | {eq[-1] - 1:+.1%} | {stats.max_drawdown(r):.1%} | "
        f"{turn:.2f} |\n"
    )
    with TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row)


def main() -> None:
    book = ct1.synthetic_book(days=3000, n=40) if DRY else bb.cm_book()
    bk = cc2.build(book)
    n_days = book.px.shape[0]
    twin_w, stop_w = cc2.series(bk)
    ok = k3.stop_ok(book.px, book.shift, STOP_K)
    assert (stop_w.hold == (twin_w.hold & ok[bk.d])).all(), "stop condition differs from run 3"
    first = int(np.argmax(book.elig.any(1)))
    dec, skip = bb.decisions(book, "daily", first)
    day_d = dec[dec + skip < n_days]
    day_b = day_d + skip
    ser = {
        "TS": make(bk, "TS", twin_w.hold, bk.d, bk.b),
        WEEKLY: make(bk, WEEKLY, stop_w.hold, bk.d, bk.b),
    }
    for mode in k3.MODES:
        nm = f"stop-0.25-{mode}"
        ser[nm] = make(bk, nm, k3.daily_hold(bk.d, twin_w.hold, day_d, ok, mode), day_d, day_b)
    assert np.allclose(ser[WEEKLY].r1, stop_w.ret) and np.allclose(ser["TS"].r1, twin_w.ret)
    # a daily variant is never in where the twin is out
    assert not ((ser["stop-0.25-d"].pos > 0) & (ser["TS"].pos == 0)).any()
    mask = bk.mask
    names = book.names

    def fstar(s: S, lvl: int) -> float:
        rt = getattr(ser["TS"], f"r{lvl}")[mask].mean()
        return float(getattr(s, f"r{lvl}")[mask].mean() / rt)

    fs = {nm: {lvl: fstar(ser[nm], lvl) for lvl in (1, 2)} for nm in NAMES}

    falls = cc2.coin_falls(bk, twin_w)
    mkt, _ = cc2.market_falls(bk)
    keys, order = k2.episodes(falls, [(m.top, m.low) for m in mkt])

    # M per fall, per series, at 1x and 2x costs
    m: dict[tuple[str, int], np.ndarray] = {}
    for nm in NAMES:
        for lvl in (1, 2):
            r = getattr(ser[nm], f"r{lvl}")
            vals = []
            for f in falls:
                lo, hi = k2.window(f, n_days)
                vals.append(k2.deepest_fall(r[lo + 1 : hi + 1, f.coin]))
            m[(nm, lvl)] = np.array(vals)

    def edge(nm: str, lvl: int) -> np.ndarray:
        return fs[nm][lvl] * m[("TS", lvl)] - m[(nm, lvl)]

    kk = np.array(keys)

    def by_ep(x: np.ndarray) -> np.ndarray:
        return np.array([float(x[kk == k].mean()) for k in order])

    n_ep = len(order)
    behind = [order.index(k) for k in WEEK_BEHIND if k in order]
    test_idx = {names.index(c) for c in cc2.TEST_COINS if c in names}
    is_test = np.array([f.coin in test_idx for f in falls], dtype=bool)

    @dataclass
    class Res:
        e1: np.ndarray  # per episode, 1x
        e2: np.ndarray  # per episode, 2x
        n_pos: int
        p: float
        fixed: int
        mean: float
        rest: float
        test_sum: float

    res: dict[str, Res] = {}
    for nm in (WEEKLY, *VARIANTS):
        e1, e2 = by_ep(edge(nm, 1)), by_ep(edge(nm, 2))
        n_pos = int((e1 > 0).sum())
        big = int(np.argmax(e1)) if n_ep else -1
        rest = np.delete(e1, big) if n_ep else e1
        res[nm] = Res(
            e1, e2, n_pos, k2.sign_p(n_pos, n_ep), int((e1[behind] > 0).sum()),
            float(e1.mean()) if n_ep else float("nan"),
            float(rest.mean()) if len(rest) else float("nan"),
            float(edge(nm, 1)[is_test].sum()),
        )  # fmt: skip
    wk = res[WEEKLY]
    verdicts: dict[str, tuple[list[bool], str]] = {}
    for nm in VARIANTS:
        x = res[nm]
        bars = [
            x.p < ALPHA and x.n_pos >= 2 * n_ep / 3,
            x.fixed >= 4,
            x.mean >= wk.mean and x.rest > 0,
            float(x.e2.mean()) >= float(wk.e2.mean()),
            x.test_sum > 0,
        ]
        if not 0 < fs[nm][1] < 1:
            v = "no cap matches its cost (f* outside 0..1): reported, no verdict"
        elif all(bars):
            v = "the daily check replaces the weekly one in the rule-PR recommendation"
        elif bars[1]:
            v = "fixes the fast crashes, not overall: the weekly stop stays the recommendation"
        else:
            v = "the daily check does not fix the fast crashes"
        verdicts[nm] = (bars, v)

    # turnover and fees, per series
    cy = mask.sum() / 365
    held_t = float(ser["TS"].pos[mask].sum())

    def trips(s: S) -> list[float]:
        out: list[float] = []
        for j in range(s.pos.shape[1]):
            out += k3.short_round_trips(s.pos[:, j], bk.filled[:, j])
        return out

    out = [
        "# coin-cap-3: the coin stop read every day, against a cap of matched cost",
        "",
        'Generated by `research/lib/coin_cap3.py`; card `research/cards/coin-cap.md` ("Fourth '
        f'reading"). Same book, coins, falls and episodes as `results/coin-cap-2.md`; Friday '
        f"twin decisions {bk.day(int(bk.d[0]))} .. {bk.day(int(bk.d[-1]))}, daily stop decisions "
        f"{bk.day(int(day_d[0]))} .. {bk.day(int(day_d[-1]))}; inputs stamped the day before the "
        "decision, position earns from the price stamped the day after (the book's as-of rule, "
        f"as the weekly stop); {float(book.cost.max()) * 1e4:.0f} bps a side; train only.",
        "",
        "## Cost match, turnover and fees",
        "",
        "Per counted coin-day (cointop-1's mask). `f*` = mean daily return over the twin's (the "
        "matched cap's fraction of the twin's slot). Switches: position changes per coin-year "
        "in the universe. Fee drag: mean (return after costs - before costs), bp per coin-day. "
        "Short trips: out and back in within 7 days, per coin-year; their mean price change "
        "from exit to re-entry (positive: bought back higher).",
        "",
        "| Series | `f*` | `f*` at 2x cost | Time held / twin | Pooled Sharpe | Switches / "
        "coin-yr | Fee drag bp/day | Short trips / coin-yr | Short trip re-entry vs exit |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for nm in NAMES:
        s = ser[nm]
        tr = trips(s)
        out.append(
            f"| `{nm}` | {fs[nm][1]:.3f} | {fs[nm][2]:.3f} | "
            f"{float(s.pos[mask].sum()) / held_t:.3f} | {core.pooled_sharpe(s.r1, mask):.2f} | "
            f"{float(k3.switches(s.pos)[mask].sum()) / cy:.2f} | "
            f"{float((s.r1 - s.r0)[mask].mean()) * 1e4:+.2f} | {len(tr) / cy:.3f} | "
            f"{float(np.mean(tr)) if tr else float('nan'):+.1%} ({len(tr)}) |"
        )
    out += [
        "",
        "## Per episode",
        "",
        "Edge M = matched cap's M (`f*` of the series x twin's M) minus the series' M, mean over "
        "the episode's coin falls, % of a slot; positive: the stop lost less at the same cost. "
        "W - d: weekly stop's M minus the daily series' M (raw; positive: daily lost less). "
        "`*` = an episode the weekly stop trailed.",
        "",
        "| Episode | Falls | Edge weekly | Edge `-d` | Edge `-dx` | W - d (`-d`) | W - d (`-dx`) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    wd = {nm: by_ep(m[(WEEKLY, 1)] - m[(nm, 1)]) for nm in VARIANTS}
    for i, k in enumerate(order):
        star = " *" if k in WEEK_BEHIND else ""
        out.append(
            f"| {k}{star} | {int((kk == k).sum())} | {wk.e1[i]:+.1%} | "
            f"{res['stop-0.25-d'].e1[i]:+.1%} | {res['stop-0.25-dx'].e1[i]:+.1%} | "
            f"{wd['stop-0.25-d'][i]:+.1%} | {wd['stop-0.25-dx'][i]:+.1%} |"
        )
    out += [
        "",
        "## Across episodes",
        "",
        "| | Weekly `stop-0.25` | `stop-0.25-d` | `stop-0.25-dx` |",
        "|---|---:|---:|---:|",
    ]

    def row(label: str, fn: Callable[[str], str]) -> str:
        return f"| {label} | " + " | ".join(str(fn(nm)) for nm in (WEEKLY, *VARIANTS)) + " |"

    out += [
        row("Edge M > 0 (episodes)", lambda nm: f"{res[nm].n_pos} of {n_ep}"),
        row("Sign test p", lambda nm: f"{res[nm].p:.4f}"),
        row("Of the 6 the weekly trailed, edge > 0", lambda nm: f"{res[nm].fixed} of 6"),
        row("Mean episode edge M", lambda nm: f"{res[nm].mean:+.1%}"),
        row("... without the largest episode", lambda nm: f"{res[nm].rest:+.1%}"),
        row("Mean episode edge M at 2x cost", lambda nm: f"{float(res[nm].e2.mean()):+.1%}"),
        row("Edge M > 0 at 2x cost", lambda nm: f"{int((res[nm].e2 > 0).sum())} of {n_ep}"),
        row("Held-aside coins, summed edge M", lambda nm: f"{res[nm].test_sum:+.0%}"),
        row(
            "Per coin fall, edge > 0",
            lambda nm: f"{int((edge(nm, 1) > 0).sum())} of {len(falls)}",
        ),
        row(
            "Mean W - d over episodes",
            lambda nm: "-" if nm == WEEKLY else f"{float(wd[nm].mean()):+.1%}",
        ),
        row(
            "Episodes daily lost less than weekly (raw M)",
            lambda nm: "-" if nm == WEEKLY else f"{int((wd[nm] > 0).sum())} of {n_ep}",
        ),
    ]
    fast = np.array([f.low - f.top <= 60 for f in falls])
    for nm in (WEEKLY, *VARIANTS):
        e = edge(nm, 1)
        out.append(
            f"- `{nm}`, coin falls with the low within 60 days of the top ({int(fast.sum())}): "
            f"mean edge {float(e[fast].mean()) if fast.any() else float('nan'):+.1%}, "
            f"positive in {int((e[fast] > 0).sum())}; slower falls: "
            f"{float(e[~fast].mean()) if (~fast).any() else float('nan'):+.1%}."
        )
    out += [
        "",
        f"## Bar (m = {M_PICKS} coin-cap picks; sign test p < {ALPHA:.4f})",
        "",
    ]
    labels = [
        "1. Edge M > 0 in at least 2/3 of episodes and corrected sign p",
        "2. Edge M > 0 in at least 4 of the 6 episodes the weekly stop trailed",
        "3. Mean episode edge at least the weekly's, and > 0 without the largest",
        "4. Mean episode edge at 2x cost at least the weekly's at 2x cost",
        "5. Held-aside coins, summed edge M > 0",
    ]
    out += ["| Bar | `stop-0.25-d` | `stop-0.25-dx` |", "|---|---|---|"]
    yes = lambda b: "holds" if b else "fails"  # noqa: E731
    for i, lab in enumerate(labels):
        out.append(
            f"| {lab} | {yes(verdicts['stop-0.25-d'][0][i])} | "
            f"{yes(verdicts['stop-0.25-dx'][0][i])} |"
        )
    weekly_ok = wk.p < ALPHA and wk.n_pos >= 2 * n_ep / 3
    out += [
        "",
        f"- **`stop-0.25-d`: {verdicts['stop-0.25-d'][1]}.**",
        f"- **`stop-0.25-dx`: {verdicts['stop-0.25-dx'][1]}.**",
        f"- Corrected sign test, weekly stop for reference: {wk.n_pos} of {n_ep}, p {wk.p:.4f}: "
        f"{'meets' if weekly_ok else 'does not meet'} it. Any stop meets it: "
        f"{'yes' if weekly_ok or any(verdicts[nm][0][0] for nm in VARIANTS) else 'no'}.",
    ]

    # BTC mechanism note (post-hoc, descriptive)
    out += [
        "",
        "## BTC mechanism note (post-hoc, descriptive; not in the bar)",
        "",
        "Each of BTC's coin falls: the window, every position change of each series inside it "
        "(`out`/`in`, the set day, the price as % of the top's), and where each series' deepest "
        "P&L fall starts and ends (with its depth, % of a slot).",
        "",
    ]
    if "btc" in names:
        j = names.index("btc")
        fl = bk.filled[:, j]
        for f in (f for f in falls if f.coin == j):
            lo, hi = k2.window(f, n_days)
            p_top = fl[f.top]
            out.append(
                f"### BTC top {bk.day(f.top)} (low {bk.day(f.low)}, "
                f"{fl[f.low] / p_top - 1:+.0%}; window {bk.day(lo)} .. {bk.day(hi)})"
            )
            out.append("")
            for nm in NAMES:
                s = ser[nm]
                ev = []
                for t in range(lo + 1, hi + 1):
                    if s.pos[t, j] != s.pos[t - 1, j]:
                        ev.append(
                            f"{'in' if s.pos[t, j] else 'out'} {bk.day(t - 1):%Y-%m-%d} "
                            f"({fl[t - 1] / p_top - 1:+.0%})"
                        )
                depth, pk, tr = k3.deepest_fall_span(s.r1[lo + 1 : hi + 1, j])
                shown = ", ".join(ev[:14]) + (f", ... ({len(ev)} in all)" if len(ev) > 14 else "")
                out.append(
                    f"- `{nm}`: M {depth:.0%} from {bk.day(lo + pk)} "
                    f"({fl[lo + pk] / p_top - 1:+.0%}) to {bk.day(lo + tr)} "
                    f"({fl[lo + tr] / p_top - 1:+.0%}). Changes: "
                    f"{shown if ev else 'none'}."
                )
            out.append(
                f"- Matched-cap M: weekly {fs[WEEKLY][1] * m[('TS', 1)][falls.index(f)]:.0%}, "
                + ", ".join(
                    f"`{nm}` {fs[nm][1] * m[('TS', 1)][falls.index(f)]:.0%}" for nm in VARIANTS
                )
                + "."
            )
            out.append("")
    text = "\n".join(out) + "\n"
    print(text)
    if DRY:
        return
    (RESEARCH / "results" / "coin-cap-3.md").write_text(text)
    first_day = bk.day(int(bk.b[0]) + 1)
    for nm in VARIANTS:
        r, t = portfolio(bk, ser[nm], 1.0, 1.0)
        log_row(f"{nm}, extended coin book", "variant", first_day, r, t)
    for nm in VARIANTS:
        r, t = portfolio(bk, ser[nm], 1.0, 2.0)
        log_row(f"{nm}, extended coin book, 2x cost", "robustness", first_day, r, t)
    r, t = portfolio(bk, ser[WEEKLY], 1.0, 2.0)
    log_row("stop-0.25 weekly, extended coin book, 2x cost", "robustness", first_day, r, t)
    r, t = portfolio(bk, ser["TS"], 1.0, 2.0)
    log_row("TS twin, extended coin book, 2x cost", "baseline", first_day, r, t)


if __name__ == "__main__":
    main()
