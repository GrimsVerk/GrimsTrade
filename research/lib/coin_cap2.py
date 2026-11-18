"""coin-cap-2: does `stop-0.25` cut coin falls more than a cap of the same cost, across
independent coin falls on breadth-1's coin book? (card: research/cards/coin-cap.md, "Third
reading").

    uv run python -I research/lib/coin_cap2.py          # the real run: logs 4 tries rows
    DRY=1 uv run python -I research/lib/coin_cap2.py    # plumbing on random prices, logs nothing

Writes `research/results/coin-cap-2.md` (the real run only).
"""

from __future__ import annotations

import fcntl
import os
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import coin_cap2_core as k2  # noqa: E402
import cointop1 as ct1  # noqa: E402
import cointop1_core as core  # noqa: E402
import stats  # noqa: E402
from harness import RESEARCH, TRAIN_END, TRIES  # noqa: E402

IDEA = "coin-cap-2"
DRY = bool(os.environ.get("DRY"))
DEPTH = 0.60  # a coin fall: the low at least 60% below the top
STOP_K = 0.25
TEST_COINS = ct1.TEST_COINS
MIN_EPISODES = 8


@dataclass
class Book2:
    book: bb.Book
    d: np.ndarray  # decision rows
    b: np.ndarray  # set rows
    univ: np.ndarray  # [decisions, coins]
    mask: np.ndarray  # [days, coins] coin-days a pooled number counts
    filled: np.ndarray

    def day(self, row: int) -> date:
        return self.book.day0 + timedelta(days=int(row))


def build(book: bb.Book) -> Book2:
    """The book's own eligibility from its first eligible day, every coin."""
    n_days = book.px.shape[0]
    first = int(np.argmax(book.elig.any(1)))
    dec, skip = bb.decisions(book, "weekly", first)
    d = dec[dec + skip < n_days]
    b = d + skip
    univ = book.elig[d] & np.isfinite(book.px[b])
    return Book2(book, d, b, univ, core.coin_days(univ, b, n_days), xs.ffill(book.px))


@dataclass
class Series:
    name: str
    hold: np.ndarray
    ret: np.ndarray
    pos: np.ndarray


def series(bk: Book2) -> tuple[Series, Series]:
    px = bk.book.px
    twin = bk.univ & bk.book.up[bk.d]
    dd = xs.lag(core.dd_1y(px, core.ewma_vol(px, 60)), bk.book.shift)
    stop = twin & core.stop_cond(dd, STOP_K)[bk.d]
    out = []
    for nm, h in (("TS", twin), (f"stop-{STOP_K:g}", stop)):
        r, p = core.paper(px, h, bk.b)
        out.append(Series(nm, h, r, p))
    return out[0], out[1]


def portfolio(bk: Book2, hold: np.ndarray, scale: float) -> tuple[np.ndarray, float]:
    """Equal-slot book of the series (slot 1 / universe coins, at least one coin), `scale` of it
    held; daily returns from the first set day, and turnover a year."""
    n_univ = bk.univ.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        targets = np.where(n_univ[:, None] >= 1, hold / np.maximum(n_univ, 1)[:, None], 0.0)
    targets = targets * scale
    r = xs.simulate(bk.book.px, targets, bk.b, bk.book.cost, int(bk.b[0]))[int(bk.b[0]) + 1 :]
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


def coin_falls(bk: Book2, twin: Series) -> list[k2.Fall]:
    px, n_days = bk.book.px, bk.book.px.shape[0]
    last = min((TRAIN_END - bk.book.day0).days, n_days - 2)
    out = []
    for j in range(px.shape[1]):
        for t in core.find_tops(px[:, j])[0]:
            if not int(bk.b[0]) <= t.top <= last:
                continue
            if not bk.book.elig[t.top + 1, j] or twin.pos[t.top + 1, j] != 1:
                continue
            if bk.filled[t.low, j] / bk.filled[t.top, j] - 1 > -DEPTH:
                continue
            out.append(k2.Fall(j, t.top, t.low, t.settled))
    return out


def market_falls(bk: Book2) -> tuple[list[core.Top], np.ndarray]:
    member = core.in_force(bk.univ, bk.b, bk.book.px.shape[0])
    r = np.zeros_like(bk.filled)
    with np.errstate(invalid="ignore", divide="ignore"):
        r[1:] = bk.filled[1:] / bk.filled[:-1] - 1
    r[~np.isfinite(r)] = 0.0
    idx = k2.market_index(r, member)
    idx[: int(bk.b[0])] = np.nan  # the index starts with the first set day
    return core.find_tops(idx)[0], idx


def main() -> None:
    book = ct1.synthetic_book(days=3000, n=40) if DRY else bb.cm_book()
    bk = build(book)
    n_days = book.px.shape[0]
    twin, stop = series(bk)
    mu_t, mu_s = float(twin.ret[bk.mask].mean()), float(stop.ret[bk.mask].mean())
    f_star = mu_s / mu_t if mu_t != 0 else float("nan")
    f_time = float(stop.hold.sum() / max(twin.hold.sum(), 1))
    matched = 0 < f_star < 1
    names = book.names

    falls = coin_falls(bk, twin)
    mkt, idx = market_falls(bk)
    keys, order = k2.episodes(falls, [(m.top, m.low) for m in mkt])

    @dataclass
    class Row:
        fall: k2.Fall
        key: str
        m_twin: float
        m_stop: float
        s_twin: float
        s_stop: float

    rows = []
    for f, key in zip(falls, keys, strict=True):
        lo, hi = k2.window(f, n_days)
        j = f.coin
        rows.append(
            Row(
                f, key,
                k2.deepest_fall(twin.ret[lo + 1 : hi + 1, j]),
                k2.deepest_fall(stop.ret[lo + 1 : hi + 1, j]),
                float(twin.ret[f.top + 1 : f.low + 1, j].sum()),
                float(stop.ret[f.top + 1 : f.low + 1, j].sum()),
            )
        )  # fmt: skip
    edge_m = {r.fall: f_star * r.m_twin - r.m_stop for r in rows}
    edge_s = {r.fall: r.s_stop - f_star * r.s_twin for r in rows}
    edge_t = {r.fall: f_time * r.m_twin - r.m_stop for r in rows}
    ep: dict[str, list[Row]] = {k: [r for r in rows if r.key == k] for k in order}
    e_m = np.array([np.mean([edge_m[r.fall] for r in ep[k]]) for k in order])
    e_s = np.array([np.mean([edge_s[r.fall] for r in ep[k]]) for k in order])
    e_t = np.array([np.mean([edge_t[r.fall] for r in ep[k]]) for k in order])

    n_ep = len(order)
    n_pos = int((e_m > 0).sum())
    p_sign = k2.sign_p(n_pos, n_ep)
    boot = k2.boot_mean(e_m)
    big = int(np.argmax(e_m)) if n_ep else -1
    rest = np.delete(e_m, big) if n_ep else e_m
    test_idx = {names.index(c) for c in TEST_COINS if c in names}
    test_sum = float(sum(edge_m[r.fall] for r in rows if r.fall.coin in test_idx))
    n_test = sum(1 for r in rows if r.fall.coin in test_idx)
    bar1 = n_ep >= MIN_EPISODES
    bar2 = n_ep > 0 and n_pos >= 2 * n_ep / 3 and p_sign < 0.10
    bar3 = len(rest) > 0 and float(rest.mean()) > 0
    bar4 = n_test > 0 and test_sum > 0
    if not matched:
        verdict = "no cap matches the stop's cost (f* outside 0..1): reported, no verdict"
    elif not bar1:
        verdict = "close: too few independent coin falls to tell"
    elif not bar3:
        verdict = "close: one-episode effect"
    elif not (bar2 and bar4):
        verdict = "close: no edge across episodes"
    else:
        verdict = "rule PR candidate, for the owner"

    months = [f"{bk.day(r.fall.top):%Y-%m}" for r in rows]
    yes = lambda x: "holds" if x else "fails"  # noqa: E731
    out = [
        "# coin-cap-2: the stop against a cap of matched cost, across independent coin falls",
        "",
        'Generated by `research/lib/coin_cap2.py`; card `research/cards/coin-cap.md` ("Third '
        f"reading\"). breadth-1's Coin Metrics book, every coin, the book's own eligibility from "
        f"its first eligible day; Friday decisions {bk.day(int(bk.d[0]))} .. "
        f"{bk.day(int(bk.d[-1]))}; 30 bps a side; train only. Per-coin paper series (cointop-1).",
        "",
        "## Cost match",
        "",
        f"- Mean daily return per counted coin-day: twin `TS` {mu_t * 1e4:+.2f} bp, "
        f"`stop-0.25` {mu_s * 1e4:+.2f} bp. **Matched cap `f*` = {f_star:.3f}** of the twin's "
        f"slot. Time held: stop / twin = **`f_time` {f_time:.3f}**.",
        f"- Pooled single-coin Sharpe: twin {core.pooled_sharpe(twin.ret, bk.mask):.2f}, stop "
        f"{core.pooled_sharpe(stop.ret, bk.mask):.2f} (a cap has the twin's Sharpe).",
        "",
        "## Coin falls and episodes",
        "",
        f"- Coin falls (trend-on cointop-1 tops, low at least {DEPTH:.0%} below the top): "
        f"**{len(falls)}** on {len({f.coin for f in falls})} coins; unsettled at the end of train: "
        f"{sum(f.settled < 0 for f in falls)}.",
        f"- Market falls of the equal-weight index (high, then -50%, settled by a doubling): "
        f"{len(mkt)}: "
        + ", ".join(
            f"{bk.day(m.top)} .. low {bk.day(m.low)} ({idx[m.low] / idx[m.top] - 1:+.0%})"
            for m in mkt
        )
        + ".",
        f"- **Episodes: {n_ep}** ({sum(k.startswith('market') for k in order)} common to a market "
        f"fall, {sum(k.startswith('own') for k in order)} coin-own runs). Effective number "
        f"(1 / sum of squared shares of falls): **{k2.effective_number(keys):.1f}**. Beside it, "
        f"cointop-1's effective number of top months: {k2.effective_number(months):.1f}.",
        "",
        "Per episode. M = deepest fall of the slot's P&L (summed daily returns, % of a slot) "
        "inside the window (91 days before the top to the settled day, at most a year after the "
        "low); the matched cap's M is `f*` x the twin's. Edge M = cap's M minus the stop's "
        "(positive: the stop lost less at the same cost). Edge S = stop's summed return top to "
        "low minus `f*` x the twin's. Edge M (time) uses `f_time` instead of `f*`. Means over the "
        "episode's coin falls.",
        "",
        "| Episode | First top .. last low | Falls | Coins (first five) | Twin M | Cap M | "
        "Stop M | Edge M | Edge S | Edge M (time) |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for i, k in enumerate(order):
        rs = ep[k]
        tops = [r.fall.top for r in rs]
        lows = [r.fall.low for r in rs]
        coins = sorted({names[r.fall.coin] for r in rs})
        tw = float(np.mean([r.m_twin for r in rs]))
        sp = float(np.mean([r.m_stop for r in rs]))
        out.append(
            f"| {k} | {bk.day(min(tops))} .. {bk.day(max(lows))} | {len(rs)} | "
            f"{', '.join(coins[:5])}{' ...' if len(coins) > 5 else ''} | {tw:.0%} | "
            f"{f_star * tw:.0%} | {sp:.0%} | {e_m[i]:+.1%} | {e_s[i]:+.1%} | {e_t[i]:+.1%} |"
        )
    out += [
        "",
        "## Across episodes",
        "",
        f"- Edge M positive in **{n_pos} of {n_ep}** episodes (sign test p = {p_sign:.3f}). Mean "
        f"episode edge {float(e_m.mean()) if n_ep else float('nan'):+.1%} of a slot (bootstrap "
        f"over episodes: p {boot[0]:.3f}, 90% range {boot[1]:+.1%} .. {boot[2]:+.1%}); without "
        f"the episode of the largest edge ({order[big] if n_ep else '-'}): "
        f"{float(rest.mean()) if len(rest) else float('nan'):+.1%}.",
        f"- Weighted by falls instead (every coin fall once): mean edge M "
        f"{float(np.mean(list(edge_m.values()))) if rows else float('nan'):+.1%}, positive in "
        f"{sum(v > 0 for v in edge_m.values())} of {len(rows)}.",
        f"- Edge S positive in {int((e_s > 0).sum())} of {n_ep} episodes (mean "
        f"{float(e_s.mean()) if n_ep else float('nan'):+.1%}). Edge M against the time-matched "
        f"cap positive in {int((e_t > 0).sum())} of {n_ep} (mean "
        f"{float(e_t.mean()) if n_ep else float('nan'):+.1%}).",
        f"- The eight coins kept out of choosing the stop ({', '.join(TEST_COINS)}): {n_test} "
        f"coin falls, summed edge M {test_sum:+.1%} of a slot.",
        "",
        "## Bar",
        "",
        f"1. At least {MIN_EPISODES} episodes: {n_ep}, {yes(bar1)}.",
        f"2. Edge M positive in at least two thirds, sign p < 0.10: {n_pos}/{n_ep}, p "
        f"{p_sign:.3f}, {yes(bar2)}.",
        f"3. Mean edge M positive without the largest episode: {yes(bar3)}.",
        f"4. Summed edge M of the eight held-aside coins positive: {yes(bar4)}.",
        "",
        f"**Verdict: {verdict}.**",
        "",
        "Every coin fall (top, low, settled; M and edges in % of a slot):",
        "",
        "| Episode | Coin | Top | Low | Settled | Fall | Twin M | Stop M | Edge M | Edge S |",
        "|---|---|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in sorted(rows, key=lambda r: (order.index(r.key), r.fall.top)):
        f = r.fall
        out.append(
            f"| {r.key} | {names[f.coin]} | {bk.day(f.top)} | {bk.day(f.low)} | "
            f"{bk.day(f.settled) if f.settled >= 0 else 'open'} | "
            f"{bk.filled[f.low, f.coin] / bk.filled[f.top, f.coin] - 1:+.0%} | {r.m_twin:.0%} | "
            f"{r.m_stop:.0%} | {edge_m[f]:+.1%} | {edge_s[f]:+.1%} |"
        )
    text = "\n".join(out) + "\n"
    print(text)
    if DRY:
        return
    (RESEARCH / "results" / "coin-cap-2.md").write_text(text)
    first = bk.day(int(bk.b[0]) + 1)
    r, t = portfolio(bk, twin.hold, 1.0)
    log_row("TS twin, extended coin book (all coins, 2013 on)", "baseline", first, r, t)
    r, t = portfolio(bk, stop.hold, 1.0)
    log_row("stop-0.25, extended coin book", "robustness", first, r, t)
    r, t = portfolio(bk, twin.hold, f_star)
    log_row(f"cap matched cost f*={f_star:.3f}, extended coin book", "variant", first, r, t)
    r, t = portfolio(bk, twin.hold, f_time)
    log_row(f"cap matched time f_time={f_time:.3f}, extended coin book", "variant", first, r, t)


if __name__ == "__main__":
    main()
