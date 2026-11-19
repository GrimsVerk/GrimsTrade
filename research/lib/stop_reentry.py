"""stop-reentry: one pre-committed re-entry rule for the weekly coin stop (card:
research/cards/coin-cap.md, "Sixth reading"). `stop-cool-13` (13-week cool-off after a
stop-out, then the stop's reference high reset to the stop-out) on the coin book's 21 episodes
and on the six assets.

    uv run python -I research/lib/stop_reentry.py          # the real run: logs 4 tries rows
    DRY=1 uv run python -I research/lib/stop_reentry.py    # random coin prices / last 120 days

Writes `research/results/stop-reentry.md` (the real run only).
"""

from __future__ import annotations

import fcntl
import sys
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import coin_cap as cc  # noqa: E402
import coin_cap2 as cc2  # noqa: E402
import coin_cap2_core as k2  # noqa: E402
import coin_cap3 as cc3  # noqa: E402
import coin_cap3_core as k3  # noqa: E402
import coin_cap4_core as k4  # noqa: E402
import cointop1 as ct1  # noqa: E402
import cointop1_carry as ct  # noqa: E402
import cointop1_core as core  # noqa: E402
import common as c  # noqa: E402
import deep1_atlas as da  # noqa: E402
import harness  # noqa: E402
import stats  # noqa: E402
import stop_reentry_core as sr  # noqa: E402
from harness import RESEARCH, TRAIN_END, TRIES  # noqa: E402

from grimstrade import gym  # noqa: E402

IDEA = "stop-reentry"
DRY = c.DRY
M_PICKS = 16  # coin-cap 15 + this reading's 1
ALPHA = 0.10 / M_PICKS
NEED = 17  # of 21 episodes for p < ALPHA
WEEK_BEHIND = cc3.WEEK_BEHIND
WEEKLY = "stop-0.25"
COOL = f"stop-cool-{sr.COOL_WEEKS}"
NAMES = ("TS", WEEKLY, COOL)
COIN_START = date(2013, 1, 1)
AFTER = 182  # six months after a low
STOP_K = cc2.STOP_K


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


def coin_book() -> tuple[list[str], dict[str, bool], dict[str, float], cc2.Book2, cc3.S]:
    book = ct1.synthetic_book(days=3000, n=40) if DRY else bb.cm_book()
    bk = cc2.build(book)
    n_days = book.px.shape[0]
    twin_w, stop_w = cc2.series(bk)
    mask = bk.mask
    pl = xs.lag(book.px, book.shift)
    vl = xs.lag(core.ewma_vol(book.px, 60), book.shift)
    cool_h, outs = sr.cool_hold(pl, vl, bk.d, twin_w.hold, STOP_K)
    ser = {
        "TS": cc3.make(bk, "TS", twin_w.hold, bk.d, bk.b),
        WEEKLY: cc3.make(bk, WEEKLY, stop_w.hold, bk.d, bk.b),
        COOL: cc3.make(bk, COOL, cool_h, bk.d, bk.b),
    }
    assert np.allclose(ser[WEEKLY].r1, stop_w.ret) and np.allclose(ser["TS"].r1, twin_w.ret)
    assert not (cool_h & ~twin_w.hold).any()
    # before a coin's first stop-out the rule is the weekly stop
    seen = np.cumsum(outs, axis=0) > 0
    assert (cool_h[~seen] == stop_w.hold[~seen]).all()

    def fstar(nm: str, lvl: int) -> float:
        rt = getattr(ser["TS"], f"r{lvl}")[mask].mean()
        return float(getattr(ser[nm], f"r{lvl}")[mask].mean() / rt)

    fs = {nm: {lvl: fstar(nm, lvl) for lvl in (1, 2)} for nm in NAMES}
    falls = cc2.coin_falls(bk, twin_w)
    mkt, _ = cc2.market_falls(bk)
    keys, order = k2.episodes(falls, [(m.top, m.low) for m in mkt])
    kk = np.array(keys)
    n_ep = len(order)

    def win(f: k2.Fall) -> slice:
        lo, hi = k2.window(f, n_days)
        return slice(lo + 1, hi + 1)

    m: dict[tuple[str, int], np.ndarray] = {}
    tw: dict[str, np.ndarray] = {}
    aft: dict[tuple[str, int], np.ndarray] = {}
    nre: dict[str, np.ndarray] = {}
    for nm in NAMES:
        for lvl in (1, 2):
            r = getattr(ser[nm], f"r{lvl}")
            m[(nm, lvl)] = np.array([k2.deepest_fall(r[win(f), f.coin]) for f in falls])
            aft[(nm, lvl)] = np.array([sr.after_low(r[:, f.coin], f.low, AFTER) for f in falls])
        tw[nm] = np.array([k4.tuw(ser[nm].r1[win(f), f.coin]) for f in falls], dtype=float)
        nre[nm] = np.array(
            [sr.reentries(ser[nm].pos[:, f.coin], f.top, k2.window(f, n_days)[1]) for f in falls],
            dtype=float,
        )

    def edge(nm: str, lvl: int) -> np.ndarray:
        return fs[nm][lvl] * m[("TS", lvl)] - m[(nm, lvl)]

    def by_ep(x: np.ndarray) -> np.ndarray:
        return np.array([float(x[kk == k].mean()) for k in order])

    e1 = {nm: by_ep(edge(nm, 1)) for nm in NAMES[1:]}
    e2 = {nm: by_ep(edge(nm, 2)) for nm in NAMES[1:]}
    raw = by_ep(m[(WEEKLY, 1)] - m[(COOL, 1)])  # positive: stop-cool lost less than weekly
    aft_ep = {nm: by_ep(aft[(nm, 1)]) for nm in NAMES}
    names = book.names
    test_idx = {names.index(s) for s in cc2.TEST_COINS if s in names}
    is_test = np.array([f.coin in test_idx for f in falls], dtype=bool)
    behind = [order.index(k) for k in WEEK_BEHIND if k in order]
    bounce = nre[WEEKLY] >= 2  # fixed by the weekly stop's positions
    n_pos = {nm: int((e1[nm] > 0).sum()) for nm in NAMES[1:]}
    mean_b = {nm: float(edge(nm, 1)[bounce].mean()) if bounce.any() else 0.0 for nm in NAMES[1:]}
    a = {
        "1": n_pos[COOL] >= NEED and k2.sign_p(n_pos[COOL], n_ep) < ALPHA,
        "2a": float(aft_ep[COOL].mean()) >= float(aft_ep[WEEKLY].mean()),
        "3": mean_b[COOL] > mean_b[WEEKLY],
        "4b": float(e2[COOL].mean()) >= float(e2[WEEKLY].mean()),
        "5": float(edge(COOL, 1)[is_test].sum()) > 0,
    }
    info = {"x_n_pos": float(n_pos[COOL]), "x_p": k2.sign_p(n_pos[COOL], n_ep), "n_ep": n_ep}

    cy = mask.sum() / 365
    held_pos = float(ser["TS"].pos[mask].sum())
    out = [
        f"## A. `{COOL}` on the coin book ({n_ep} episodes, {len(falls)} coin falls)",
        "",
        f"Stop-outs that started a cool-off: {int(outs.sum())} ({float(outs.sum()) / cy:.2f} per "
        "coin-year of the universe).",
        "",
        "| Series | `f*` | `f*` 2x cost | Time held / twin | Pooled Sharpe | Switches / coin-yr "
        "| Edge M > 0 (sign p) | Mean episode edge M | ... 2x cost | Of the 6 the weekly "
        "trailed | Held-aside coins, summed edge | Mean episode TUW, days | Six months after "
        "the low, mean episode | Re-entries per fall |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
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
            f"{float(by_ep(tw[nm]).mean()):.0f} | {float(aft_ep[nm].mean()):+.1%} | "
            f"{float(nre[nm].mean()):.2f} |"
        )
    out += [
        "",
        "Six months after the low: the slot's summed daily return (after costs) over the 182 "
        "days after each fall's low; the matched cap's is `f*` x the twin's. TUW of every cap is "
        "the twin's.",
        "",
        f"- Bounce falls (the weekly stop re-entered two or more times; {int(bounce.sum())} "
        f"falls): mean edge M weekly {mean_b[WEEKLY]:+.1%}, `{COOL}` {mean_b[COOL]:+.1%}; "
        f"re-entries per fall there {float(nre[WEEKLY][bounce].mean()):.2f} against "
        f"{float(nre[COOL][bounce].mean()):.2f}.",
        f"- Raw M: `{COOL}` lost less than the weekly stop in {int((raw > 0).sum())} of {n_ep} "
        f"episodes, mean {float(raw.mean()):+.1%} of a slot.",
        f"- Six months after the low, `{COOL}` above the weekly stop in "
        f"{int((aft_ep[COOL] > aft_ep[WEEKLY]).sum())} of {n_ep} episodes; at double costs "
        f"mean episode {float(by_ep(aft[(COOL, 2)]).mean()):+.1%} against "
        f"{float(by_ep(aft[(WEEKLY, 2)]).mean()):+.1%}.",
        "",
        "Per episode (edge M in % of a slot, means over the episode's coin falls; raw W - c: the "
        f"weekly stop's M minus `{COOL}`'s, positive = it lost less; `*` = an episode the weekly "
        "stop trailed):",
        "",
        "| Episode | Falls | Edge weekly | Edge cool | Raw W - c | TUW twin | TUW weekly | "
        "TUW cool | 6 mo after low: twin | weekly | cool |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    tw_ep = {nm: by_ep(tw[nm]) for nm in NAMES}
    for i, k in enumerate(order):
        star = " *" if k in WEEK_BEHIND else ""
        out.append(
            f"| {k}{star} | {int((kk == k).sum())} | {e1[WEEKLY][i]:+.1%} | {e1[COOL][i]:+.1%} | "
            f"{raw[i]:+.1%} | {tw_ep['TS'][i]:.0f} | {tw_ep[WEEKLY][i]:.0f} | "
            f"{tw_ep[COOL][i]:.0f} | {aft_ep['TS'][i]:+.0%} | {aft_ep[WEEKLY][i]:+.0%} | "
            f"{aft_ep[COOL][i]:+.0%} |"
        )
    if "btc" in names:
        j = names.index("btc")
        bi = [i for i, f in enumerate(falls) if f.coin == j]
        out += [
            "",
            "BTC's falls (edge M against each series' own pooled matched cap; six months after "
            "the low; re-entries):",
            "",
            "| Top | Edge weekly | Edge cool | 6 mo after: twin | weekly | cool | Re-entries "
            "weekly | cool |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for i in bi:
            out.append(
                f"| {bk.day(falls[i].top)} | {edge(WEEKLY, 1)[i]:+.0%} | {edge(COOL, 1)[i]:+.0%} "
                f"| {aft[('TS', 1)][i]:+.0%} | {aft[(WEEKLY, 1)][i]:+.0%} | "
                f"{aft[(COOL, 1)][i]:+.0%} | {nre[WEEKLY][i]:.0f} | {nre[COOL][i]:.0f} |"
            )
    return out, a, info, bk, ser[COOL]


State = tuple[bool, int | None, date | None]  # held, latest stop-out close (ordinal), cool until


class CoolStop:
    """`stop-cool-13` as a gym extra for the coin slots: the state at a Friday is replayed from
    the views of earlier Fridays only (`view.at`), memoised per panel."""

    def __init__(self, k: float = STOP_K, cool_days: int = sr.COOL_DAYS) -> None:
        self.k = k
        self.cool = timedelta(days=cool_days)
        self.token = object()

    def step(self, v: c.View, s: str, day: date, st: State) -> State:
        held_prev, s_ord, until = st
        if until is not None and day < until:
            return False, s_ord, until
        twin = c.eligible(v, s) and c.tsmom_signal(v, s)
        cl, d = v.close(s), v.dates(s)
        vol = c.vol_series(v, s, 60)
        known = ok = False
        if len(cl) and len(vol) >= 20:
            keep = d > d[-1] - 365
            if s_ord is not None:
                keep &= d >= s_ord
            known, ok = sr.stop_state(float(cl[-1]), float(vol[-1]), float(cl[keep].max()), self.k)
        if held_prev and twin and known and not ok:
            return False, int(d[-1]), day + self.cool
        return bool(twin and ok), s_ord, until

    def __call__(self, view: c.View, s: str) -> bool:
        today = view.today
        fri = today - timedelta(days=(today.weekday() - 4) % 7)
        first = date.fromordinal(int(view.panel.ord[s][0]))
        cache = view.panel.cache
        todo: list[date] = []
        st: State = (False, None, None)
        day = fri
        while day >= first:
            key = (self.token, s, day)
            if key in cache:
                st = cache[key]  # type: ignore[assignment]
                break
            todo.append(day)
            day -= timedelta(days=7)
        for day in reversed(todo):
            st = self.step(view if day == today else view.at(day), s, day, st)
            cache[(self.token, s, day)] = st
        return st[0]


def turn_excess(runs: dict[str, c.Run], base: str) -> dict[str, float]:
    """combo-1's turn: mean daily excess over `base` x 365 in the 182 days after each of the
    base's ten deepest lows (overlaps counted once)."""
    rb = runs[base].rets
    back = np.zeros(len(rb), dtype=bool)
    for e in da.episodes(rb, 10):
        back[e.trough + 1 : min(len(rb), e.trough + 1 + AFTER)] = True
    out = {}
    for n, run in runs.items():
        r = run.rets
        assert len(r) == len(rb), n
        out[n] = float((r - rb)[back].mean() * 365) if back.any() else float("nan")
    return out


def six_assets() -> tuple[list[str], dict[str, bool]]:
    six = c.ctx("six")
    cool_f = ct.rule(CoolStop())
    harness.check_against_gym(cool_f, six.hist, ct.CHECK_DAYS)
    print("look-ahead check passed", flush=True)
    costs2 = {k: gym.Costs(fee=v.fee * 2, slip=v.slip * 2) for k, v in gym.COSTS.items()}

    def at2(idea: str, name: str, f: c.ResearchStrategy, kind: str, log: bool) -> c.Run:
        return harness.run(
            idea, name, f, kind=kind, panel=six.panel, history=six.hist, start=six.start,
            end=six.end, costs=costs2, log=log and not DRY,
        )  # fmt: skip

    runs = {
        "tsmom12": c.go("baselines", "tsmom12", c.weekly(cc.TSMOM), six, "baseline", log=False),
        WEEKLY: c.go("cointop-1-stop", WEEKLY, ct.rule(ct.stop_ok), six, log=False),
        COOL: c.go(IDEA, COOL, ct.rule(CoolStop()), six, "variant"),
    }
    runs2 = {
        "tsmom12": at2("robustness", "tsmom12-2xcost", c.weekly(cc.TSMOM), "robustness", False),
        WEEKLY: at2("cointop-1-stop", f"{WEEKLY}-2xcost", ct.rule(ct.stop_ok), "robustness", False),
        COOL: at2(IDEA, f"{COOL}-2xcost", ct.rule(CoolStop()), "robustness", True),
    }
    turn = turn_excess(runs, "tsmom12")
    turn2 = turn_excess(runs2, "tsmom12")

    def yrs(run: c.Run, a: date) -> dict[str, float]:
        y = run.rets_between(a, six.end)
        eq = np.concatenate([[1.0], np.cumprod(1 + y)])
        longest, deep = k4.equity_tuw(eq)
        return {
            "mdd": stats.max_drawdown(y), "cagr": stats.cagr(y), "sharpe": stats.sharpe(y),
            "tuw": float(longest), "deep": deep,
        }  # fmt: skip

    first = runs["tsmom12"].days[0]
    full = {n: yrs(r, first) for n, r in runs.items()}
    coin = {n: yrs(r, COIN_START) for n, r in runs.items()}
    full2 = {n: yrs(r, first) for n, r in runs2.items()}
    coin2 = {n: yrs(r, COIN_START) for n, r in runs2.items()}
    b = {
        "2b": turn[COOL] > turn[WEEKLY],
        "4a": coin[COOL]["mdd"] <= coin[WEEKLY]["mdd"] + 0.01,
    }
    out = [
        f"## B. Six assets through the gym (full train from {first}, and coin years "
        f"{COIN_START} .. {six.end}, equity re-based)",
        "",
        "| Series | Period | Worst loss | CAGR | Sharpe | Longest under water, days | "
        "Days 10%+ under | Turn: excess over `tsmom12`, % a year |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for lab, st, tn in (("full", full, turn), ("coin yrs", coin, None)):
        for n, v in st.items():
            t_cell = f"{tn[n] * 100:+.1f}" if tn is not None else "-"
            out.append(
                f"| `{n}` | {lab} | {v['mdd']:.1%} | {v['cagr']:+.2%} | {v['sharpe']:.2f} | "
                f"{v['tuw']:.0f} | {v['deep']:.0%} | {t_cell} |"
            )
    out += ["", "At double costs:", "", "| Series | Period | Worst loss | CAGR | Sharpe | Longest "
            "under water | Turn |", "|---|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    for lab, st, tn in (("full", full2, turn2), ("coin yrs", coin2, None)):
        for n, v in st.items():
            t_cell = f"{tn[n] * 100:+.1f}" if tn is not None else "-"
            out.append(
                f"| `{n}` | {lab} | {v['mdd']:.1%} | {v['cagr']:+.2%} | {v['sharpe']:.2f} | "
                f"{v['tuw']:.0f} | {t_cell} |"
            )
    out += [
        "",
        "Turn: combo-1's measure, the 182 days after each of `tsmom12`'s ten deepest lows "
        "(this run's `tsmom12`, full train), mean daily excess x 365.",
    ]
    return out, b


def main() -> None:
    lines_a, a, info, bk, cool_s = coin_book()
    lines_b, b = six_assets()
    bars = {**a, **b}
    yes: Callable[[bool], str] = lambda v: "holds" if v else "fails"  # noqa: E731
    two = bars["2a"] and bars["2b"]
    four = bars["4a"] and bars["4b"]
    rest = two and bars["3"] and four and bars["5"]
    if bars["1"] and rest:
        verdict = f"`{COOL}` meets the family bar and replaces the weekly stop"
    elif rest:
        verdict = (
            f"fixes the re-entry costs without proof: if a coin stop is wanted, `{COOL}` is the "
            "better risk preference, still not a proven rule"
        )
    else:
        verdict = "the re-entry rule does not fix the stop: the weekly stop stays the (unproven) " \
            "risk preference"  # fmt: skip
    labels = {
        "1": f"1. Edge M > 0 in at least {NEED} of 21 episodes (p < {ALPHA:.5f})",
        "2a": "2a. Coin book: six months after the low, mean episode at least the weekly stop's",
        "2b": "2b. Six assets: turn excess (full train) above the weekly stop's",
        "3": "3. Weekly stop's bounce falls (2+ re-entries): mean edge M above the weekly stop's",
        "4a": "4a. Six assets, coin years: worst loss at most 1.0 point above the weekly stop's",
        "4b": "4b. Mean episode edge M at 2x cost at least the weekly stop's",
        "5": "5. Held-aside coins, summed edge M > 0",
    }
    out = [
        "# stop-reentry: one re-entry rule for the weekly coin stop",
        "",
        'Generated by `research/lib/stop_reentry.py`; card `research/cards/coin-cap.md` ("Sixth '
        f'reading"). `{COOL}`: after a stop-out, out for 13 weeks, then the stop reads its band '
        "against the highest close since the stop-out instead of the one-year high. Coin book: "
        "breadth-1's Coin Metrics book, every coin, Friday decisions, 30 bps a side, the third "
        "reading's coin falls and episodes. Six assets: `tsmom12` through the gym, gym costs. "
        f"Train only; held-out year unspent. Family bar: m = {M_PICKS} coin-cap picks, sign test "
        f"p < {ALPHA:.5f} (at least {NEED} of 21).",
        "",
        *lines_a,
        "",
        *lines_b,
        "",
        "## Decision (one rule)",
        "",
        "| Bar | Result |",
        "|---|---|",
        *[f"| {labels[k]} | {yes(bars[k])} |" for k in labels],
        "",
        f"- **{verdict}.**",
        f"- Sign test: {int(info['x_n_pos'])} of {int(info['n_ep'])} (p {info['x_p']:.4f}). "
        + (
            "Meets the family bar."
            if bars["1"]
            else "Does not meet the family bar: the coin line stays parked (no rule PR from this "
            "lane; held-out year unspent)."
        ),
    ]
    text = "\n".join(out) + "\n"
    print(text)
    if DRY:
        return
    (RESEARCH / "results" / "stop-reentry.md").write_text(text)
    first_day = bk.day(int(bk.b[0]) + 1)
    for mult, kind, tag in ((1.0, "variant", ""), (2.0, "robustness", ", 2x cost")):
        r, t = cc3.portfolio(bk, cool_s, 1.0, mult)
        log_row(f"{COOL}, extended coin book{tag}", kind, first_day, r, t)


if __name__ == "__main__":
    main()
