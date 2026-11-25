"""breadth-anatomy-1: why `breadth-book-1`'s broader `tsmom12` books have a lower Sharpe
(card `research/cards/breadth-anatomy-1.md`). Descriptive: no new rule, nothing selected.

    uv run python -I research/lib/banat1.py run    # writes research/results/breadth-anatomy-1.md

Needs `breadth-book-1`'s research cache (`research/data/{bars,adj}`, see its write-up). Train
only: no bar after 2025-10-31 is used.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

import banat1_core as ac
import bbook1
import bbook1_core as core
import common as c
import harness
import numpy as np
from harness import STRESS, Panel, View, Weights

from grimstrade import gym
from grimstrade.data import CRYPTO, UNIVERSE, Bar

IDEA = "breadth-anatomy-1"
END_BAR = date(2025, 10, 31)
W = (date(2008, 1, 2), END_BAR)
SPLIT = date(2010, 1, 1)
RESULT = harness.RESEARCH / "results" / f"{IDEA}.md"
COINS = set(core.LIVE_COINS)
MARKET_CRISES = ("2008 crisis", "covid crash", "2022 rate shock")

H: dict[str, list[Bar]] = {}
BILLS: gym.Rates = []


@dataclass
class B:
    name: str
    syms: list[str]
    days: list[date]
    ex: np.ndarray  # daily return above the bill, calendar days (days[1:])
    gross: np.ndarray  # cash earns 0
    decisions: list[gym.Decision]

    @property
    def sr(self) -> float:
        return core.sharpe(self.ex)


def load(syms: Sequence[str]) -> None:
    global BILLS
    bbook1.register(syms)
    hist = harness.load_history("train", True, list(syms))
    for s, bars in hist.items():
        H[s] = [b for b in bars if b.date <= END_BAR]
    assert all(b.date <= END_BAR for bars in H.values() for b in bars)
    BILLS = [(t, r) for t, r in harness.bill_rates() if t.date() <= END_BAR]


def book(name: str, syms: Sequence[str], strat: harness.ResearchStrategy) -> B:
    hist = {s: H[s] for s in syms}
    run = harness.run(IDEA, name, strat, kind="variant", panel=Panel(hist), history=hist,
                      start=W[0], end=W[1], log=False)  # fmt: skip
    res = gym.simulate(run.decisions, hist, rates=BILLS)
    return B(name, list(syms), run.days, bbook1.excess_calendar(res, run.days), run.rets,
             run.decisions)  # fmt: skip


def per_year(s: str) -> int:
    return 365 if UNIVERSE[s] == CRYPTO else 252


def vol_of(view: View, s: str) -> float:
    cl = view.close(s)
    return bbook1._ewma_vol(cl[1:] / cl[:-1] - 1, per_year(s))


def k_rule(view: View) -> Weights:
    el = c.live(view)
    on = {s for s in el if c.tsmom_signal(view, s)}
    return ac.coin_fixed_weights(el, on, core.SIX, COINS)


def rw_rule(view: View) -> Weights:
    el = c.live(view)
    on = {s for s in el if c.tsmom_signal(view, s)}
    return ac.inverse_vol_weights(el, on, {s: vol_of(view, s) for s in el})


def always(view: View, s: str) -> bool:
    return True


TSMOM = bbook1.tsmom12
K: Callable[[], harness.ResearchStrategy] = lambda: c.weekly(k_rule)  # noqa: E731
RW: Callable[[], harness.ResearchStrategy] = lambda: c.weekly(rw_rule)  # noqa: E731
HOLD: Callable[[], harness.ResearchStrategy] = lambda: c.weekly(c.slots(always))  # noqa: E731


# ---------------------------------------------------------------- helpers


def eligible_from(s: str) -> date:
    return H[s][0].date + timedelta(days=366)


def dmask(b: B, a: date, z: date) -> np.ndarray:
    d = np.array([x.toordinal() for x in b.days[1:]])
    return (d >= a.toordinal()) & (d <= z.toordinal())


def weekly(b: B) -> tuple[list[date], np.ndarray]:
    """Friday-to-Friday sums of the daily above-bill returns (week labelled by its Friday)."""
    out: dict[date, float] = {}
    for d, r in zip(b.days[1:], b.ex, strict=True):
        f = d + timedelta(days=(4 - d.weekday()) % 7)
        out[f] = out.get(f, 0.0) + float(r)
    ks = sorted(out)
    return ks, np.array([out[k] for k in ks])


def weight_sum(b: B, syms: Sequence[str]) -> float:
    return float(np.mean([sum(dc.weights.get(s, 0.0) for s in syms) for dc in b.decisions]))


def coin_var_share(b: B, sleeves: dict[str, B]) -> float:
    """cov(coin part, book) / var(book); coin part = slot size (1 / eligible assets that day) x
    the coin's own `tsmom12` sleeve return."""
    days = b.days[1:]
    n = np.array([sum(eligible_from(s) <= d for s in b.syms) for d in days], float)
    part = np.zeros(len(days))
    for s in b.syms:
        if s in COINS:
            el = np.array([eligible_from(s) <= d for d in days])
            part += np.where(el, sleeves[s].ex / np.maximum(n, 1), 0.0)
    return float(np.cov(part, b.ex)[0, 1] / b.ex.var())


def f2(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:+.2f}" if x < 0 else f"{x:.2f}"


def edge(a: B, ref: B) -> str:
    d, se, z, _ = core.paired(a.ex, ref.ex)
    return f"{d:+.3f} ({se:.3f}, z {z:+.2f})"


def sub_sr(b: B, a: date, z: date) -> float:
    return core.sharpe(b.ex[dmask(b, a, z)])


# ---------------------------------------------------------------- the run


def run() -> None:
    _, order, _ = bbook1.lists()
    six, four = core.SIX, core.LIVE_ETFS
    n_all = len(order) + 2
    lsets = {k: core.nested(order, n, six) for k, n in (("12", 12), ("20", 20), ("all", n_all))}
    added = {k: [s for s in v if s not in six] for k, v in lsets.items()}
    allsyms = lsets["all"]
    load(allsyms)
    harness.check_against_gym(TSMOM(), {s: H[s] for s in allsyms},
                              [date(2009, 3, 6), date(2018, 6, 1)])  # fmt: skip

    out = [f"# breadth-anatomy-1 results ({datetime.now(UTC):%Y-%m-%d %H:%M} UTC)", "",
           "Card `research/cards/breadth-anatomy-1.md`. Window: decisions 2008-01-02 .. "
           "2025-10-31, no bar after 2025-10-31. Sharpe = daily return above the 13-week bill, "
           "calendar days, 365-day year. Edges: paired stationary bootstrap (block 20, 2,000 "
           "draws), (SE, z). Descriptive: nothing here is a candidate book.", "",
           "Added sets (the six's added ETFs, round-robin order): "
           + "; ".join(f"A-{len(v)}: {' '.join(v)}" for v in added.values()), ""]  # fmt: skip

    # step 0
    bs = {"six": book("six", six, TSMOM()), "four": book("four", four, TSMOM())}
    for k, v in lsets.items():
        bs[f"L-{k}"] = book(f"L-{k}", v, TSMOM())
    bs["E-all"] = book("E-all", [s for s in allsyms if s not in COINS], TSMOM())
    out += ["## Step 0: reproduction (breadth-book-1 to 2025-11-09: six 1.19, L-12 0.96, "
            "L-20 0.83, L-all 0.65, four 0.82, E-all 0.37)", "",
            "| Set | N | Sharpe above bills | Cash-0 Sharpe | Edge vs ref |",
            "|---|---:|---:|---:|---|"]  # fmt: skip
    for n, b in bs.items():
        ref = bs["four"] if n in ("four", "E-all") else bs["six"]
        e = "-" if b is ref else f"{edge(b, ref)} vs `{ref.name}`"
        out.append(f"| `{n}` | {len(b.syms)} | {b.sr:.2f} | {core.sharpe(b.gross):.2f} | {e} |")
    out.append("")

    # sleeves (b)
    sl = {s: book(f"{s}-sleeve", [s], TSMOM()) for s in allsyms}
    hold = {s: book(f"{s}-hold", [s], HOLD()) for s in allsyms}

    def own(b: B, s: str) -> np.ndarray:
        return b.ex[dmask(b, eligible_from(s), W[1])]

    srs = {s: core.sharpe(own(sl[s], s)) for s in allsyms}

    # (a)
    for k in ("12", "20", "all"):
        bs[f"X-{len(added[k]) + 4}"] = book(f"X-{len(added[k]) + 4}", four + added[k], TSMOM())
        bs[f"K-{k}"] = book(f"K-{k}", lsets[k], K())
    out += ["## (a) Coin share", "",
            "| Set | N | Mean coin weight | Coin share of variance | Sharpe |",
            "|---|---:|---:|---:|---:|"]  # fmt: skip
    for n in ("six", "L-12", "L-20", "L-all", "K-12", "K-20", "K-all"):
        b = bs[n]
        out.append(f"| `{n}` | {len(b.syms)} | {weight_sum(b, list(COINS)):.3f} | "
                   f"{coin_var_share(b, sl):.2f} | {b.sr:.2f} |")  # fmt: skip
    out += ["", "Coins excluded from both (vs `four`):", "",
            "| Set | N | Sharpe | Edge vs `four` |", "|---|---:|---:|---|"]  # fmt: skip
    for n in ("X-10", "X-18", "X-33"):
        b = bs[n]
        out.append(f"| `{n}` | {len(b.syms)} | {b.sr:.2f} | {edge(b, bs['four'])} |")
    out += ["", "Split of the gap (coins held at the six's weight = `K`):", "",
            "| k | SR(L) - SR(six) | ETF breadth, coins fixed: K - six | Coin dilution: L - K | "
            "Coin share of the gap |", "|---|---|---|---|---:|"]  # fmt: skip
    for k in ("12", "20", "all"):
        lb, kb, s6 = bs[f"L-{k}"], bs[f"K-{k}"], bs["six"]
        share = (lb.sr - kb.sr) / (lb.sr - s6.sr)
        out.append(f"| {k} | {edge(lb, s6)} | {edge(kb, s6)} | {edge(lb, kb)} | {share:.0%} |")
    out.append("")

    # (b)
    out += ["## (b) Each asset's own tsmom12 sleeve (from its first eligible day in the window)",
            "", "| Asset | Class | Group | Sleeve Sharpe | Sleeve vol | Exposure | Hold Sharpe |",
            "|---|---|---|---:|---:|---:|---:|"]  # fmt: skip

    def group(s: str) -> str:
        if s in six:
            return "six"
        return next(f"A-{len(added[k])}" for k in ("12", "20", "all") if s in added[k])

    for s in allsyms:
        e = own(sl[s], s)
        ex = weight_sum(sl[s], [s])
        cls = "crypto" if s in COINS else core.class_of(s)
        out.append(f"| {s} | {cls} | {group(s)} | {srs[s]:.2f} | {e.std() * math.sqrt(365):.1%} "
                   f"| {ex:.2f} | {core.sharpe(own(hold[s], s)):.2f} |")  # fmt: skip
    out += ["", "| Group | n | Mean sleeve Sharpe | Median | Mean hold Sharpe |",
            "|---|---:|---:|---:|---:|"]  # fmt: skip
    groups: dict[str, list[str]] = {"six": six, "four": four, "C (BTC, ETH)": ["BTC", "ETH"]}
    groups.update({f"A-{len(v)}": v for v in added.values()})
    for cl in core.CLASS_ORDER:
        groups[f"A-29 {cl}"] = [s for s in added["all"] if core.class_of(s) == cl]
    for g, v in groups.items():
        if not v:
            continue
        x = [srs[s] for s in v]
        h = [core.sharpe(own(hold[s], s)) for s in v]
        out.append(f"| {g} | {len(v)} | {np.mean(x):.2f} | {np.median(x):.2f} | "
                   f"{np.mean(h):.2f} |")  # fmt: skip
    a_books = {k: book(f"A-{len(v)}", v, TSMOM()) for k, v in added.items()}
    out += ["", "Books on the added ETFs alone: "
            + ", ".join(f"`{b.name}` {b.sr:.2f}" for b in a_books.values()), ""]  # fmt: skip

    # (c)
    fr, _ = weekly(sl[allsyms[0]])
    wk = np.column_stack([weekly(sl[s])[1] for s in allsyms])
    valid = np.column_stack([np.array([f >= eligible_from(s) + timedelta(7) for f in fr])
                             for s in allsyms])  # fmt: skip
    i6 = [allsyms.index(s) for s in six]
    ia = [allsyms.index(s) for s in added["all"]]
    i4 = [allsyms.index(s) for s in four]

    def in_windows(names: Sequence[str] | None) -> np.ndarray:
        ws = [(a, z) for n, a, z in STRESS if names is None or n in names]
        ws = [(max(a, W[0]), min(z, W[1])) for a, z in ws if z >= W[0] and a <= W[1]]
        return np.array([any(a <= f <= z + timedelta(6) for a, z in ws) for f in fr])

    six_w = weekly(bs["six"])[1]
    four_w = weekly(bs["four"])[1]
    a29_w = weekly(a_books["all"])[1]
    out += ["## (c) Correlation of the weekly above-bill sleeve returns", "",
            "| Weeks | n weeks | Within six | Within A-29 | Six x A-29 | Four x A-29 | "
            "rho(A-29 book, six book) | N_eff six | N_eff all 35 |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    crisis_m = in_windows(MARKET_CRISES)
    crisis_all = in_windows(None)
    allw = np.ones(len(fr), bool)
    spans = [("all", allw), ("market crises", crisis_m), ("not market crises", ~crisis_m),
             ("all 7 stress windows", crisis_all), ("outside them", ~crisis_all)]  # fmt: skip
    for lab, rows in spans:
        cm = ac.pairwise_corr(wk, valid, rows)
        ne6 = core.participation(np.nan_to_num(cm[np.ix_(i6, i6)]))
        ne = core.participation(np.nan_to_num(cm))
        rho = ac.corr_masked(a29_w, six_w, rows)
        out.append(f"| {lab} | {int(rows.sum())} | {f2(ac.mean_offdiag(cm, i6))} | "
                   f"{f2(ac.mean_offdiag(cm, ia))} | {f2(ac.mean_offdiag(cm, i6, ia))} | "
                   f"{f2(ac.mean_offdiag(cm, i4, ia))} | {f2(rho)} | {ne6:.1f} | "
                   f"{ne:.1f} |")  # fmt: skip
    out += ["", "Two-book blend (static daily mix; weight w on the added book; rho = daily "
            "correlation; test = SR_A - rho x SR_ref, > 0 means a small weight on A helps):", "",
            "| Ref | Added | SR_ref | SR_A | rho | rho x SR_ref | Test | w* | SR(w*) | "
            "SR at L-weight (actual L) | SR(1) |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|"]  # fmt: skip
    pairs = [("six", k, bs["six"]) for k in ("12", "20", "all")] + [("four", "all", bs["four"])]
    for rn, k, ref in pairs:
        a = a_books[k]
        rho = float(np.corrcoef(a.ex, ref.ex)[0, 1])
        w_l = len(added[k]) / len(lsets[k])
        ws, srw = ac.best_weight(a.ex, ref.ex)
        actual = bs[f"L-{k}"].sr if rn == "six" else bs["X-33"].sr
        out.append(f"| `{rn}` | `{a.name}` | {ref.sr:.2f} | {a.sr:.2f} | {rho:.2f} | "
                   f"{rho * ref.sr:.2f} | {ac.marginal_gain(a.sr, ref.sr, rho):+.2f} | {ws:.2f} | "
                   f"{srw:.2f} | {ac.mix_sharpe(a.ex, ref.ex, w_l):.2f} at w {w_l:.2f} "
                   f"({actual:.2f}) | {a.sr:.2f} |")  # fmt: skip
    # per added sleeve
    out += ["", "Per added sleeve, marginal test against the six and the four books (weekly rho):",
            "", "| Asset | SR_i | rho_i six | SR_i - rho x SR_six | rho_i four | "
            "SR_i - rho x SR_four |", "|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    pass6 = pass4 = 0
    sr6, sr4 = bs["six"].sr, bs["four"].sr
    for s in added["all"]:
        j = allsyms.index(s)
        r6 = ac.corr_masked(wk[:, j], six_w, valid[:, j])
        r4 = ac.corr_masked(wk[:, j], four_w, valid[:, j])
        g6, g4 = ac.marginal_gain(srs[s], sr6, r6), ac.marginal_gain(srs[s], sr4, r4)
        pass6 += g6 > 0
        pass4 += g4 > 0
        out.append(f"| {s} | {srs[s]:.2f} | {r6:.2f} | {g6:+.2f} | {r4:.2f} | {g4:+.2f} |")
    out += ["", f"Pass the marginal test: {pass6} of {len(ia)} against `six`, {pass4} of "
            f"{len(ia)} against `four`.", ""]  # fmt: skip

    # (d)
    rw = {n: book(f"{n}-rw", bs[n].syms, RW()) for n in ("six", "four", "L-12", "L-20", "L-all",
                                                        "E-all")}  # fmt: skip
    out += ["## (d) Equal weight vs inverse-vol weight", "",
            "| Set | SR equal | SR rw | Coin weight equal | Coin weight rw | Gap equal | Gap rw |",
            "|---|---:|---:|---:|---:|---|---|"]  # fmt: skip
    for n, b in rw.items():
        ref = "four" if n in ("four", "E-all") else "six"
        ge = "-" if n == ref else edge(bs[n], bs[ref])
        gr = "-" if n == ref else edge(b, rw[ref])
        out.append(f"| `{n}` | {bs[n].sr:.2f} | {b.sr:.2f} | {weight_sum(bs[n], list(COINS)):.3f}"
                   f" | {weight_sum(b, list(COINS)):.3f} | {ge} | {gr} |")  # fmt: skip
    out.append("")

    # (e)
    out += ["## (e) Period (one row; the asset-class view is tick-tier-1's)", "",
            "| Span | six | four | L-all | E-all | A-29 | K-all | L-all - six |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    for lab, a, z in (("2008-2009", W[0], SPLIT - timedelta(1)), ("2010-2025-10", SPLIT, W[1])):
        v = [sub_sr(bs[n], a, z) for n in ("six", "four", "L-all", "E-all")]
        v += [sub_sr(a_books["all"], a, z), sub_sr(bs["K-all"], a, z)]
        out.append(f"| {lab} | " + " | ".join(f2(x) for x in v) + f" | {v[2] - v[0]:+.2f} |")
    RESULT.write_text("\n".join(out).rstrip() + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    if (sys.argv[1] if len(sys.argv) > 1 else "") == "run":
        run()
    else:
        raise SystemExit(__doc__)
