"""coin-cap-4: the last coin risk candidates as one set (card: research/cards/coin-cap.md,
"Fifth reading"): `pstop` (a price-drawdown stop, band matched on time held) on the coin book's
21 episodes and on the six assets, `cap25+stop` on the six assets, time under water for all.

    uv run python -I research/lib/coin_cap4.py          # the real run: logs 6 tries rows
    DRY=1 uv run python -I research/lib/coin_cap4.py    # random coin prices / last 120 days, no log

Writes `research/results/coin-cap-4.md` (the real run only).
"""

from __future__ import annotations

import fcntl
import os
import sys
from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import coin_cap as cc  # noqa: E402
import coin_cap2 as cc2  # noqa: E402
import coin_cap2_core as k2  # noqa: E402
import coin_cap3 as cc3  # noqa: E402
import coin_cap3_core as k3  # noqa: E402
import coin_cap4_core as k4  # noqa: E402
import coin_cap_core as kc  # noqa: E402
import cointop1 as ct1  # noqa: E402
import cointop1_carry as ct  # noqa: E402
import cointop1_core as core  # noqa: E402
import common as c  # noqa: E402
import harness  # noqa: E402
import stats  # noqa: E402
from harness import RESEARCH, TRAIN_END, TRIES  # noqa: E402

from grimstrade import gym  # noqa: E402

IDEA = "coin-cap-4"
DRY = bool(os.environ.get("DRY"))
M_PICKS = 15  # coin-cap 9 + coin-cap-2 2 + coin-cap-3 2 + this reading's 2
ALPHA = 0.10 / M_PICKS
NEED = 17  # of 21 episodes for p < ALPHA
WEEK_BEHIND = cc3.WEEK_BEHIND
WEEKLY = "stop-0.25"
COIN_START = date(2013, 1, 1)
NAMES = ("TS", WEEKLY, "stop-0.25-d", "pstop")


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


def coin_book() -> tuple[list[str], float, dict[str, bool], cc2.Book2, cc3.S]:
    """Part A on the coin book. Returns the report lines, the frozen band, A1-A4 and the book
    with `pstop`'s series (for the tries rows)."""
    book = ct1.synthetic_book(days=3000, n=40) if DRY else bb.cm_book()
    bk = cc2.build(book)
    n_days = book.px.shape[0]
    twin_w, stop_w = cc2.series(bk)
    mask = bk.mask

    # 1. the band, from positions only, frozen before any return of `pstop` exists
    held_t = float(core.in_force(twin_w.hold, bk.b, n_days)[mask].sum())
    target = float(core.in_force(stop_w.hold, bk.b, n_days)[mask].sum()) / held_t
    dd = k4.price_dd(book.px, book.shift)

    def hold_x(x: float) -> np.ndarray:
        return twin_w.hold & k4.pstop_ok(dd, x)[bk.d]

    def time_held(x: float) -> float:
        return float(core.in_force(hold_x(x), bk.b, n_days)[mask].sum()) / held_t

    x_star = k4.match_x(time_held, target)
    print(f"band frozen: X = {x_star:.2f} (time held {time_held(x_star):.3f}, target {target:.3f})")

    # 2. the series
    ok = k3.stop_ok(book.px, book.shift, cc2.STOP_K)
    first = int(np.argmax(book.elig.any(1)))
    dec, skip = bb.decisions(book, "daily", first)
    day_d = dec[dec + skip < n_days]
    ser = {
        "TS": cc3.make(bk, "TS", twin_w.hold, bk.d, bk.b),
        WEEKLY: cc3.make(bk, WEEKLY, stop_w.hold, bk.d, bk.b),
        "stop-0.25-d": cc3.make(
            bk, "stop-0.25-d", k3.daily_hold(bk.d, twin_w.hold, day_d, ok, "d"), day_d,
            day_d + skip,
        ),
        "pstop": cc3.make(bk, "pstop", hold_x(x_star), bk.d, bk.b),
    }  # fmt: skip
    assert np.allclose(ser[WEEKLY].r1, stop_w.ret) and np.allclose(ser["TS"].r1, twin_w.ret)
    assert not ((ser["pstop"].pos > 0) & (ser["TS"].pos == 0)).any()

    def fstar(nm: str, lvl: int) -> float:
        rt = getattr(ser["TS"], f"r{lvl}")[mask].mean()
        return float(getattr(ser[nm], f"r{lvl}")[mask].mean() / rt)

    fs = {nm: {lvl: fstar(nm, lvl) for lvl in (1, 2)} for nm in NAMES}

    falls = cc2.coin_falls(bk, twin_w)
    mkt, _ = cc2.market_falls(bk)
    keys, order = k2.episodes(falls, [(m.top, m.low) for m in mkt])
    kk = np.array(keys)
    n_ep = len(order)

    m: dict[tuple[str, int], np.ndarray] = {}
    tw: dict[str, np.ndarray] = {}
    for nm in NAMES:
        for lvl in (1, 2):
            r = getattr(ser[nm], f"r{lvl}")
            m[(nm, lvl)] = np.array(
                [k2.deepest_fall(r[slice(*_w(f, n_days)), f.coin]) for f in falls]
            )
        tw[nm] = np.array([k4.tuw(ser[nm].r1[slice(*_w(f, n_days)), f.coin]) for f in falls])

    def edge(nm: str, lvl: int) -> np.ndarray:
        return fs[nm][lvl] * m[("TS", lvl)] - m[(nm, lvl)]

    def by_ep(x: np.ndarray) -> np.ndarray:
        return np.array([float(x[kk == k].mean()) for k in order])

    e1 = {nm: by_ep(edge(nm, 1)) for nm in NAMES[1:]}
    e2 = {nm: by_ep(edge(nm, 2)) for nm in NAMES[1:]}
    raw = by_ep(m[(WEEKLY, 1)] - m[("pstop", 1)])  # positive: pstop lost less than weekly
    names = book.names
    test_idx = {names.index(s) for s in cc2.TEST_COINS if s in names}
    is_test = np.array([f.coin in test_idx for f in falls], dtype=bool)
    behind = [order.index(k) for k in WEEK_BEHIND if k in order]

    n_pos = {nm: int((e1[nm] > 0).sum()) for nm in NAMES[1:]}
    a = {
        "A1": n_pos["pstop"] >= NEED and k2.sign_p(n_pos["pstop"], n_ep) < ALPHA,
        "A2": int((raw > 0).sum()) >= 14,
        "A3": float(e2["pstop"].mean()) >= float(e2[WEEKLY].mean()),
        "A4": float(edge("pstop", 1)[is_test].sum()) > 0,
    }

    out = [
        "## A. `pstop` on the coin book (21 episodes)",
        "",
        f"Band frozen from positions only: **X = {x_star:.2f}** (pooled time held over the "
        f"twin's {time_held(x_star):.3f}, target = the weekly stop's {target:.3f}). `pstop` "
        f"holds a coin while the twin does and its price is within {x_star:.0%} of its "
        "one-year high (read on Fridays, inputs stamped the day before).",
        "",
        "| Series | `f*` | `f*` 2x cost | Time held / twin | Pooled Sharpe | Switches / coin-yr "
        "| Edge M > 0 (sign p) | Mean episode edge M | ... 2x cost | Of the 6 the weekly "
        "trailed | Held-aside coins, summed edge | Mean episode TUW, days |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    cy = mask.sum() / 365
    held_pos = float(ser["TS"].pos[mask].sum())
    for nm in NAMES:
        s = ser[nm]
        if nm == "TS":
            cells = "- | - | - | - | -"
        else:
            cells = (
                f"{n_pos[nm]} of {n_ep} ({k2.sign_p(n_pos[nm], n_ep):.4f}) | "
                f"{float(e1[nm].mean()):+.1%} | {float(e2[nm].mean()):+.1%} | "
                f"{int((e1[nm][behind] > 0).sum())} of {len(behind)} | "
                f"{float(edge(nm, 1)[is_test].sum()):+.0%}"
            )
        out.append(
            f"| `{nm}` | {fs[nm][1]:.3f} | {fs[nm][2]:.3f} | "
            f"{float(s.pos[mask].sum()) / held_pos:.3f} | {core.pooled_sharpe(s.r1, mask):.2f} | "
            f"{float(k3.switches(s.pos)[mask].sum()) / cy:.2f} | {cells} | "
            f"{float(by_ep(tw[nm].astype(float)).mean()):.0f} |"
        )
    out += [
        "",
        "The twin's TUW is every cap's (a cap scales the P&L path, so its time under water is "
        "the twin's). `stop-0.25-d` is coin-cap-3's daily-checked stop, for reference.",
        "",
        "Per episode (edge M in % of a slot, means over the episode's coin falls; raw W - p: "
        "the weekly stop's M minus `pstop`'s, positive = `pstop` lost less; TUW in days; `*` = "
        "an episode the weekly stop trailed):",
        "",
        "| Episode | Falls | Edge weekly | Edge `pstop` | Raw W - p | TUW twin/cap | TUW weekly "
        "| TUW `-d` | TUW `pstop` |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    tw_ep = {nm: by_ep(tw[nm].astype(float)) for nm in NAMES}
    for i, k in enumerate(order):
        star = " *" if k in WEEK_BEHIND else ""
        out.append(
            f"| {k}{star} | {int((kk == k).sum())} | {e1[WEEKLY][i]:+.1%} | "
            f"{e1['pstop'][i]:+.1%} | {raw[i]:+.1%} | {tw_ep['TS'][i]:.0f} | "
            f"{tw_ep[WEEKLY][i]:.0f} | {tw_ep['stop-0.25-d'][i]:.0f} | {tw_ep['pstop'][i]:.0f} |"
        )
    out += [
        "",
        f"- Raw M: `pstop` lost less than the weekly stop in {int((raw > 0).sum())} of {n_ep} "
        f"episodes, mean {float(raw.mean()):+.1%} of a slot.",
        f"- TUW shorter than the twin's (and every cap's), episodes: weekly "
        f"{int((tw_ep[WEEKLY] < tw_ep['TS']).sum())}, `-d` "
        f"{int((tw_ep['stop-0.25-d'] < tw_ep['TS']).sum())}, `pstop` "
        f"{int((tw_ep['pstop'] < tw_ep['TS']).sum())} of {n_ep}.",
    ]
    if "btc" in names:
        j = names.index("btc")
        bi = [i for i, f in enumerate(falls) if f.coin == j]
        out += [
            "",
            "BTC's five falls (edge M against each series' own pooled matched cap; TUW days):",
            "",
            "| Top | Edge weekly | Edge `-d` | Edge `pstop` | TUW twin | TUW weekly | "
            "TUW `pstop` |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
        for i in bi:
            out.append(
                f"| {bk.day(falls[i].top)} | {edge(WEEKLY, 1)[i]:+.0%} | "
                f"{edge('stop-0.25-d', 1)[i]:+.0%} | {edge('pstop', 1)[i]:+.0%} | "
                f"{tw['TS'][i]} | {tw[WEEKLY][i]} | {tw['pstop'][i]} |"
            )
    return out, x_star, a, bk, ser["pstop"]


def _w(f: k2.Fall, n_days: int) -> tuple[int, int]:
    lo, hi = k2.window(f, n_days)
    return lo + 1, hi + 1


def pstop_rule(x: float) -> ct.Extra:
    def ok(view: c.View, s: str) -> bool:
        cl, d = view.close(s), view.dates(s)
        if len(cl) == 0:
            return False
        hi = cl[d > d[-1] - 365].max()
        return bool(cl[-1] / hi - 1 >= -x)

    return ok


def cap_stop() -> c.ResearchStrategy:
    inner = ct.rule(ct.stop_ok, weekly=False)
    return c.weekly(lambda view: kc.cap_coins(inner(view), cc.COINS, 0.25, "cash"))


def six_assets(x: float) -> tuple[list[str], dict[str, bool]]:
    six = c.ctx("six")
    pstop_f = ct.rule(pstop_rule(x))
    cs_f = cap_stop()
    for f in (pstop_f, cs_f):
        harness.check_against_gym(f, six.hist, ct.CHECK_DAYS)
    print("look-ahead checks passed", flush=True)
    costs2 = {k: gym.Costs(fee=v.fee * 2, slip=v.slip * 2) for k, v in gym.COSTS.items()}

    def at2(idea: str, name: str, f: c.ResearchStrategy, kind: str, log: bool) -> c.Run:
        return harness.run(
            idea, name, f, kind=kind, panel=six.panel, history=six.hist, start=six.start,
            end=six.end, costs=costs2, log=log and not c.DRY,
        )  # fmt: skip

    pname = f"pstop-{x:.2f}"
    runs = {
        "tsmom12": c.go("baselines", "tsmom12", c.weekly(cc.TSMOM), six, "baseline", log=False),
        "cap25-cash": c.go("coin-cap", "cap25-cash", cc.capped(0.25, "cash"), six, log=False),
        WEEKLY: c.go("cointop-1-stop", WEEKLY, ct.rule(ct.stop_ok), six, log=False),
        "cap25+stop": c.go(IDEA, "cap25+stop", cs_f, six, "variant"),
        pname: c.go(IDEA, pname, pstop_f, six, "variant"),
    }
    runs2 = {
        WEEKLY: at2("cointop-1-stop", f"{WEEKLY}-2xcost", ct.rule(ct.stop_ok), "robustness", False),
        "cap25+stop": at2(IDEA, "cap25+stop-2xcost", cs_f, "robustness", True),
        pname: at2(IDEA, f"{pname}-2xcost", pstop_f, "robustness", True),
    }

    def yrs(run: c.Run) -> dict[str, float]:
        y = run.rets_between(COIN_START, six.end)
        eq = np.concatenate([[1.0], np.cumprod(1 + y)])
        longest, deep = k4.equity_tuw(eq)
        return {
            "mdd": stats.max_drawdown(y), "cagr": stats.cagr(y), "sharpe": stats.sharpe(y),
            "tuw": float(longest), "deep": deep, "full_mdd": c.describe(run)["mdd"],
        }  # fmt: skip

    st = {n: yrs(r) for n, r in runs.items()}
    st2 = {n: yrs(r) for n, r in runs2.items()}
    s, cs, ps = st[WEEKLY], st["cap25+stop"], st[pname]
    s2, cs2 = st2[WEEKLY], st2["cap25+stop"]
    b = {
        "B1": cs["mdd"] <= s["mdd"] - 0.02,
        "B2": cs["cagr"] >= s["cagr"] - 0.01,
        "B3": cs["tuw"] <= s["tuw"],
        "B4": cs2["mdd"] <= s2["mdd"] - 0.02 and cs2["cagr"] >= s2["cagr"] - 0.01,
        "A5": ps["mdd"] <= s["mdd"] and ps["cagr"] >= s["cagr"] - 0.01,
    }
    out = [
        "## Six assets through the gym (coin years 2013-01-01 .. "
        f"{six.end}, equity re-based; full train worst loss beside it)",
        "",
        "| Series | Worst loss | CAGR | Sharpe | CAGR vs stop | Longest under water, days | "
        "Days 10%+ under | Full-train worst loss |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for n, v in st.items():
        out.append(
            f"| `{n}` | {v['mdd']:.1%} | {v['cagr']:+.2%} | {v['sharpe']:.2f} | "
            f"{v['cagr'] - s['cagr']:+.2%} | {v['tuw']:.0f} | {v['deep']:.0%} | "
            f"{v['full_mdd']:.1%} |"
        )
    out += ["", "At double costs:", "", "| Series | Worst loss | CAGR | Sharpe | Longest under "
            "water |", "|---|---:|---:|---:|---:|"]  # fmt: skip
    for n, v in st2.items():
        out.append(
            f"| `{n}` | {v['mdd']:.1%} | {v['cagr']:+.2%} | {v['sharpe']:.2f} | {v['tuw']:.0f} |"
        )
    return out, b


def main() -> None:
    lines_a, x_star, a, bk, ps = coin_book()
    lines_six, b = six_assets(x_star)
    a["A5"] = b.pop("A5")
    yes: Callable[[bool], str] = lambda v: "holds" if v else "fails"  # noqa: E731
    if all(a.values()):
        va = "`pstop` meets the family bar and replaces the weekly stop"
    elif a["A1"]:
        va = "`pstop` meets the sign bar, not the rest: reported, not acted on"
    else:
        va = "no candidate meets the family bar: the weekly stop stays a risk preference"
    vb = (
        "a 25% cap on top of the stop is an optional size choice (not provable on episodes)"
        if all(b.values())
        else "a 25% cap adds nothing worth its cost to the stop"
    )
    labels = {
        "A1": f"A1. Edge M > 0 in at least {NEED} of 21 episodes (p < {ALPHA:.4f})",
        "A2": "A2. Raw M below the weekly stop's in at least 14 of 21 episodes",
        "A3": "A3. Mean episode edge at 2x cost at least the weekly stop's",
        "A4": "A4. Held-aside coins, summed edge M > 0",
        "A5": "A5. Six assets, coin years: worst loss <= stop's, CAGR >= stop's - 1 point",
        "B1": "B1. Worst loss at least 2 points below the stop's",
        "B2": "B2. CAGR at most 1 point a year below the stop's",
        "B3": "B3. Longest stretch under water no longer than the stop's",
        "B4": "B4. B1 and B2 at double costs",
    }
    out = [
        "# coin-cap-4: the last coin risk candidates as one set",
        "",
        'Generated by `research/lib/coin_cap4.py`; card `research/cards/coin-cap.md` ("Fifth '
        "reading\"). Coin book: breadth-1's Coin Metrics book, every coin, Friday decisions, 30 "
        "bps a side, the third reading's 445 coin falls and 21 episodes. Six assets: `tsmom12` "
        "through the gym, gym costs. Train only; held-out year unspent. Family bar: m = "
        f"{M_PICKS} coin-cap picks, sign test p < {ALPHA:.4f} (at least {NEED} of 21).",
        "",
        *lines_a,
        "",
        *lines_six,
        "",
        "## Decision (one rule for the set)",
        "",
        "| Bar | Result |",
        "|---|---|",
        *[f"| {labels[k]} | {yes(v)} |" for k, v in {**a, **b}.items()],
        "",
        f"- **A: {va}.**",
        f"- **B: {vb}.**",
        "- For reference (coin-cap-3, not retested): the weekly stop's 15 of 21 (p 0.039) does "
        "not meet the family bar; `stop-0.25-d`'s 18 of 21 does, but failed its own card.",
    ]
    text = "\n".join(out) + "\n"
    print(text)
    if DRY:
        return
    (RESEARCH / "results" / "coin-cap-4.md").write_text(text)
    first_day = bk.day(int(bk.b[0]) + 1)
    for mult, kind, tag in ((1.0, "variant", ""), (2.0, "robustness", ", 2x cost")):
        r, t = cc3.portfolio(bk, ps, 1.0, mult)
        log_row(f"pstop-{x_star:.2f}, extended coin book{tag}", kind, first_day, r, t)


if __name__ == "__main__":
    main()
