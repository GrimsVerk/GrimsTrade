"""Lane coin-drift-2: wide-16's `band05@coin`, unchanged, on six coins and years it never saw.
Card `research/cards/coin-drift-2.md`; write-up `research/coin-drift-2.md`.

    DRY=1 uv run python -I research/lib/coindrift2.py   # plumbing: last 120 days, no numbers
    uv run python -I research/lib/coindrift2.py --log   # the one real run (tries.md rows)

The coins: the six largest by 30-day median cap on 2017-12-31 among breadth-1 book A's
eligible coins on 2018-01-01, without BTC, ETH, wide-16's `OOU_COINS` and USDT. Their Coin
Metrics prices, cut after 2019-03-31 (coin-drift-1 traded them from 2019-04-07), go through
the gym exactly as wide-16's `run_set("coin")`: `tsmom12` with band 0.05 against band 0.01.
Writes `research/results/coin-drift-2.md`.
"""

from __future__ import annotations

import fcntl
import math
import os
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import coindrift2_core as core  # noqa: E402
import harness  # noqa: E402
import stats  # noqa: E402
from coindrift2_core import CARD_COINS, EXCLUDE, cm_bars, pick_coins  # noqa: E402
from harness import OOU_COINS, TRAIN_START, Panel  # noqa: E402

from grimstrade import gym  # noqa: E402
from grimstrade.data import CRYPTO, ETF, UNIVERSE, Bar  # noqa: E402

assert tuple(OOU_COINS) == core.OOU_COINS

IDEA = "coin-drift-run"
PICK_DAY = date(2018, 1, 1)  # wide-16's set rule: "large caps of January 2018"
LAST = date(2019, 3, 31)  # last bar: coin-drift-1's first return day is 2019-04-07
BAND05 = 0.05
SUFFIX = "-CD2"
DRY = os.environ.get("DRY") == "1"
SPLIT = date(2018, 1, 1)  # reporting only: the part after the pick


def load_coins() -> dict[str, list[Bar]]:
    import bbook1
    import breadth_books as bb
    import macro

    book = bb.cm_book()
    panel = bb.cm_panel()
    cap30 = bb.roll_median(panel["mc"], 30)
    i = (PICK_DAY - book.day0).days
    coins = pick_coins(book.names, book.elig[i], cap30[i - 1], EXCLUDE)
    assert tuple(coins) == CARD_COINS, f"pick differs from the card: {coins}"
    root = macro.cache_root() / "coinmetrics" / "full" / bb.CM_SNAPSHOT / "assets"
    hist: dict[str, list[Bar]] = {}
    for a in coins:
        series = [
            (date.fromisoformat(str(r["time"])[:10]), float(str(r["PriceUSD"])))
            for r in bbook1.cm_rows(root / a)
            if r.get("PriceUSD") is not None
        ]
        sym = a.upper() + SUFFIX
        UNIVERSE[sym] = CRYPTO
        hist[sym] = cm_bars(series, LAST)
    assert max(b.date for bars in hist.values() for b in bars) <= LAST
    return hist


def boot(a: np.ndarray, b: np.ndarray, draws: int = 2000) -> tuple[float, float, float]:
    """wide-16's `boot`: dSharpe, paired stationary-bootstrap SE, one-sided p (20-day, seed 0)."""
    rng = np.random.default_rng(0)
    diffs = np.empty(draws)
    for k in range(draws):
        i = stats._stationary_indices(len(a), 20, rng)
        diffs[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
    return stats.sharpe(a) - stats.sharpe(b), float(diffs.std()), float((diffs <= 0).mean())


def bill_daily(days: list[date], rates: gym.Rates) -> np.ndarray:
    known = [t for t, _ in rates]
    return np.array([gym.cash_rate(rates, d, known) / gym.DAYS_PER_YEAR for d in days[1:]])


def fill_stats(res: gym.Result, years: float) -> tuple[float, float, float]:
    """Coin fills a year, fee and slip as a share of equity a year."""
    eq = dict(res.equity)
    fee = slip = 0.0
    for f in res.fills:
        d = f.time.date()
        e = eq.get(d) or next(v for k, v in reversed(res.equity) if k <= d)
        fee += f.fee / e
        slip += abs(f.qty) * f.price * gym.COSTS[CRYPTO].slip / e
    return len(res.fills) / years, fee / years, slip / years


def note_row(text: str, first: date, last: date) -> None:
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {text} | note | train | {first} | "
        f"{last} | - | - | - | - |\n"
    )
    with harness.TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row)


def main() -> None:
    import wide16

    log = "--log" in sys.argv and not DRY
    hist = load_coins()
    pan = Panel(hist)
    first = min(b[0].date for b in hist.values())
    start = max(TRAIN_START, first + timedelta(days=366))
    end = max(b[-1].date for b in hist.values()) - timedelta(days=1)
    if DRY:
        start = end - timedelta(days=120)
    rates = harness.bill_rates()
    assert rates, "no bill rates (research/data/bars/IRX.csv missing)"
    free = {CRYPTO: gym.Costs(fee=0.0, slip=0.0), ETF: gym.COSTS[ETF]}

    def go(variant: str, band: float, logged: bool, kind: str, **kw: object) -> harness.Run:
        return harness.run(
            IDEA, variant, wide16.rule(), kind=kind, period="train", panel=pan, history=hist,
            start=start, end=end, log=logged and log, band=band, **kw,  # type: ignore[arg-type]
        )  # fmt: skip

    base = go("tsmom12@cd2 (band 0.01; coin-drift-2's six coins to 2019-03)", gym.BAND, True,
              "baseline")  # fmt: skip
    rule = go("band05@cd2 (band 0.05 of equity)", BAND05, True, "robustness")
    base_b = go("-", gym.BAND, False, "robustness", rates=rates)
    rule_b = go("-", BAND05, False, "robustness", rates=rates)
    base_f = go("-", gym.BAND, False, "robustness", costs=free)
    rule_f = go("-", BAND05, False, "robustness", costs=free)
    if DRY:
        print(f"DRY: {len(base.rets)} / {len(rule.rets)} daily returns, {base.days[0]} .. "
              f"{base.days[-1]}; coins {sorted(hist)}; no numbers printed")  # fmt: skip
        return

    d, se, p = boot(rule.rets, base.rets)
    rf = bill_daily(base_b.days, rates)
    db, seb, pb = boot(rule_b.rets - rf, base_b.rets - rf)
    df, sef, pf = boot(rule_f.rets, base_f.rets)
    z, zb, zf = d / se, db / seb, df / sef
    years = len(base.rets) / 365
    gap = rule.rets - base.rets
    te, corr = float(gap.std() * math.sqrt(365)), float(np.corrcoef(rule.rets, base.rets)[0, 1])
    fs = {
        n: fill_stats(gym.simulate(r.decisions, hist, band=b), years)
        for n, r, b in (("base", base, gym.BAND), ("rule", rule, BAND05))
    }

    out = [
        f"# {IDEA}: coin-drift-2 results (card `cards/coin-drift-2.md`)",
        "",
        "Generated by `research/lib/coindrift2.py`. `tsmom12` through the gym on the Coin Metrics "
        f"prices of {', '.join(c.upper() for c in CARD_COINS)}, bars cut after {LAST}; returns "
        f"{base.days[0]} .. {base.days[-1]} ({years:.1f} years). Gym costs, start 10,000 USD.",
        "",
        "| Book | Sharpe (cash 0) | Above bills | Coin fills free | Growth/yr | Max DD | "
        "Fills/yr | Fee/yr | Slip/yr |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, r, rb, rf_, key in (
        ("`tsmom12` (band 0.01)", base, base_b, base_f, "base"),
        ("`band05` (band 0.05)", rule, rule_b, rule_f, "rule"),
    ):
        n, fee, sl = fs[key]
        out.append(
            f"| {name} | {stats.sharpe(r.rets):.3f} | {stats.sharpe(rb.rets - rf):.3f} | "
            f"{stats.sharpe(rf_.rets):.3f} | {stats.cagr(r.rets):.1%} | "
            f"{stats.max_drawdown(r.rets):.1%} | {n:.0f} | {fee:.2%} | {sl:.2%} |"
        )
    out += [
        "",
        "| `band05` minus `tsmom12` | dSharpe | SE | z | p (one-sided) |",
        "|---|---:|---:|---:|---:|",
        f"| net, cash 0 (**scored**) | {d:+.4f} | {se:.4f} | **{z:+.2f}** | {p:.3f} |",
        f"| net, above bills | {db:+.4f} | {seb:.4f} | {zb:+.2f} | {pb:.3f} |",
        f"| coin fills free (the drift part) | {df:+.4f} | {sef:.4f} | {zf:+.2f} | {pf:.3f} |",
        "",
        f"Tracking error {te:.2%} a year, correlation {corr:.4f}.",
        "",
        "| Window | Days | `tsmom12` Sharpe | dSharpe net | dSharpe, fills free |",
        "|---|---:|---:|---:|---:|",
    ]
    windows = [(f"{y}", date(y, 1, 1), date(y, 12, 31)) for y in range(2015, 2020)]
    windows.append((f"after the pick ({SPLIT} ..)", SPLIT, end))
    for label, a, b in windows:
        r0, r1 = base.rets_between(a, b), rule.rets_between(a, b)
        g0, g1 = base_f.rets_between(a, b), rule_f.rets_between(a, b)
        if len(r0) < 60 or r0.std() == 0:
            continue
        out.append(
            f"| {label} | {len(r0)} | {stats.sharpe(r0):.2f} | "
            f"{stats.sharpe(r1) - stats.sharpe(r0):+.3f} | "
            f"{stats.sharpe(g1) - stats.sharpe(g0):+.3f} |"
        )
    if z >= 2.5 and d > 0:
        reading = "small effect supported" if df > 0 else "fees, not drift: not supported"
    elif d > 0 and z >= 1.0:
        reading = "not confirmed"
    else:
        reading = "killed: no support on unseen data"
    out += [
        "",
        "## Bars (card)",
        "",
        f"- Project bar z >= 4.70: z {z:+.2f}, {'met' if z >= 4.70 else 'not met'} "
        "(not a pick in any case).",
        f"- Real small effect, z >= 2.5 with dSharpe > 0: z {z:+.2f}, "
        f"{'met' if z >= 2.5 and d > 0 else 'not met'}; coin fills free dSharpe {df:+.4f}.",
        f"- **Reading: {reading}.**",
    ]
    text = "\n".join(out) + "\n"
    print(text)
    (harness.RESEARCH / "results" / "coin-drift-2.md").write_text(text)
    if log:
        note_row(
            f"coin-drift-2 split (same run, not a try): band05@cd2 net {d:+.3f} (z {z:.2f}); "
            f"above bills {db:+.3f} (z {zb:.2f}); coin fills free {df:+.3f} (z {zf:.2f}); "
            f"reading: {reading}",
            base.days[0],
            base.days[-1],
        )


if __name__ == "__main__":
    main()
