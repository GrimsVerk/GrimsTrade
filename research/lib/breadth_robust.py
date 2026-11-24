"""Checks on the one book-A survivor of breadth-1 (`turnover`, weekly), run after its result
was seen (kind `robustness` in tries.md), and its one held-out look.

    uv run python -I research/lib/breadth_robust.py [--log]       # train-period checks
    uv run python -I research/lib/breadth_robust.py --heldout --log  # once only

Checks: 100 bps a side; the top 50 coins instead of 100; a placebo (100 random fixed scores per
coin, the same test) giving the chance spread of TOP-TS minus TS; the share of zero-return
days (stale prices) in the top third; rank overlap with `low_vol` and `size`.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import stats  # noqa: E402
from harness import HELD_END, HELD_START, TRIES  # noqa: E402

SIG = "turnover"


def weekly(book: bb.Book) -> tuple[np.ndarray, int]:
    return bb.decisions(book, "weekly", bb.start_day(book))


def line(label: str, t: xs.Tilt) -> str:
    d, p, _, _ = stats.sharpe_diff_boot(t.top_ts, t.ts)
    return (
        f"| {label} | {stats.sharpe(t.ts):.2f} | {stats.sharpe(t.top_ts):.2f} | {d:+.2f} ({p:.2f})"
        f" | {stats.sharpe(t.top) - stats.sharpe(t.ew):+.2f} | {stats.max_drawdown(t.ts):.0%} / "
        f"{stats.max_drawdown(t.top_ts):.0%} |"
    )


def train(log: bool) -> None:
    book = bb.cm_book()
    dec, skip = weekly(book)
    sig = book.signals[SIG]
    print("| Check | TS | TOP-TS | TOP-TS - TS (p) | TOP - EW | Max DD TS / TOP-TS |")
    print("|---|---:|---:|---:|---:|---|")
    runs = {
        "as run (30 bps, top 100)": xs.tilt(book.px, book.elig, sig, book.up, dec, skip, book.cost),
        "100 bps a side": xs.tilt(book.px, book.elig, sig, book.up, dec, skip, book.cost * 10 / 3),
    }
    b50 = bb.cm_book(top_n=50)
    d50, s50 = weekly(b50)
    runs["top 50 coins"] = xs.tilt(b50.px, b50.elig, b50.signals[SIG], b50.up, d50, s50, b50.cost)
    for k, t in runs.items():
        print(line(k, t), flush=True)
        if log and k != "as run (30 bps, top 100)":
            first = book.day0 + timedelta(days=t.first)
            bb.log_row(
                "breadth-1-cm",
                f"weekly turnover TOP-TS, {k}",
                "robustness",
                first,
                t.top_ts,
                t.turnover["top_ts"],
            )
    # placebo: fixed random score per coin
    rng = np.random.default_rng(0)
    diffs = []
    for _ in range(100):
        score = np.broadcast_to(rng.random(book.px.shape[1]), book.px.shape)
        t = xs.tilt(book.px, book.elig, score, book.up, dec, skip, book.cost)
        diffs.append(stats.sharpe(t.top_ts) - stats.sharpe(t.ts))
    q = np.quantile(diffs, [0.5, 0.9, 0.95, 0.99])
    print(
        f"\nPlacebo (100 fixed random scores): TOP-TS - TS median {q[0]:+.2f}, 90th pct "
        f"{q[1]:+.2f}, 95th {q[2]:+.2f}, 99th {q[3]:+.2f}, max {max(diffs):+.2f}"
    )
    # stale prices and overlap
    lr = np.vstack([np.full((1, book.px.shape[1]), np.nan), np.diff(np.log(book.px), axis=0)])
    zero_top, zero_all, ov_lv, ov_sz = [], [], [], []
    for d in dec:
        m = book.elig[d] & np.isfinite(sig[d])
        if m.sum() < 10:
            continue
        top = xs.top_mask(sig[d], m)
        win = lr[d + 1 : d + 8]
        zero_top.append(np.mean(win[:, top] == 0))
        zero_all.append(np.mean(win[:, m] == 0))
        for out, other in ((ov_lv, "low_vol"), (ov_sz, "size")):
            o = book.signals[other][d]
            k = m & np.isfinite(o)
            out.append(xs.spearman(sig[d, k], o[k]))
    print(f"Zero-return days: top third {np.mean(zero_top):.1%}, universe {np.mean(zero_all):.1%}")
    print(
        f"Rank correlation of turnover with low_vol {np.mean(ov_lv):+.2f}, with size "
        f"{np.mean(ov_sz):+.2f}"
    )
    if log:
        with TRIES.open("a") as f:
            f.write(
                f"| {bb.datetime.now(bb.UTC):%Y-%m-%d %H:%M} | breadth-1-cm | weekly turnover "
                f"placebo, 100 random fixed scores (95th pct of TOP-TS - TS {q[2]:+.2f}) | "
                f"control | train | {book.day0 + timedelta(days=int(dec[0]))} | "
                f"{bb.TRAIN_END} | - | - | - | - |\n"
            )


def heldout(log: bool) -> None:
    book = bb.cm_book(last=HELD_END + timedelta(days=1))
    dec, skip = bb.decisions(book, "weekly", 0)  # decisions() stops at TRAIN_END: redo
    days = np.arange(book.px.shape[0])
    wd = np.array([(book.day0 + timedelta(days=int(i))).weekday() for i in days])
    first, last = (HELD_START - book.day0).days, (HELD_END - book.day0).days
    dec = days[(wd == 4) & (days >= first) & (days <= last)]
    t = xs.tilt(book.px, book.elig, book.signals[SIG], book.up, dec, 1, book.cost)
    print(f"Held-out {HELD_START}..{HELD_END}, {len(dec)} Fridays")
    print("| Book | Sharpe | Return | Max DD |\n|---|---:|---:|---:|")
    for k, r in (("EW", t.ew), ("TOP", t.top), ("TS", t.ts), ("TOP-TS", t.top_ts)):
        print(
            f"| {k} | {stats.sharpe(r):.2f} | {np.prod(1 + r) - 1:+.1%} | "
            f"{stats.max_drawdown(r):.0%} |"
        )
    if log:
        first_d = book.day0 + timedelta(days=t.first)
        with TRIES.open("a") as f:
            for k, r, kind in (("TS", t.ts, "baseline"), ("TOP-TS", t.top_ts, "variant")):
                f.write(
                    f"| {bb.datetime.now(bb.UTC):%Y-%m-%d %H:%M} | breadth-1-cm | weekly "
                    f"turnover {k} held-out | {kind} | heldout | {first_d} | {HELD_END} | "
                    f"{stats.sharpe(r):.2f} | {np.prod(1 + r) - 1:+.1%} | "
                    f"{stats.max_drawdown(r):.1%} | {t.turnover['top_ts']:.2f} |\n"
                )


if __name__ == "__main__":
    if "--heldout" in sys.argv:
        marker = bb.derived() / "heldout-turnover-used"
        if marker.exists():
            sys.exit("held-out year already looked at for this survivor")
        marker.write_text(str(date.today()))
        heldout("--log" in sys.argv)
    else:
        train("--log" in sys.argv)
