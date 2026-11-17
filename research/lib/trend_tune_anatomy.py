"""Part A of research run trend-tune: the anatomy of `tsmom12` (card: research/trend-tune.md).

    uv run python research/lib/trend_tune_anatomy.py

A description: no pass bar, no selection. Gym runs are logged in research/tries.md the first time
only (their equity curves are saved under research/data/runs/, and a rerun re-scores them
unlogged), so the tables can be rebuilt without logging tries twice. Hand-written text above the
marker line in the result file is kept.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import harness
import numpy as np
import stats
import trend_tune as tt

from grimstrade import gym, report
from grimstrade.data import CRYPTO, UNIVERSE

ANATOMY = "trend-tune-anatomy"
SURFACE = "trend-tune-surface"
MARK = "<!-- tables below this line are written by lib/trend_tune_anatomy.py -->"
ORDER = ["SPY", "QQQ", "TLT", "GLD", "BTC", "ETH"]
Y2003 = date(2003, 1, 1)
LOOKS = [*range(3, 17), 18, 20, 22, 24]
PAIRS = (3, 6, 9, 12, 18)
Z_LOOKS = (6, 12, 18)
CENTRES = (-0.25, 0.0, 0.25)
HALVES = (0.0, 0.25, 0.5)
BANDS = (0.0, 0.025, 0.05)
WINDOWS = [
    ("1994-2025", date(1994, 1, 1), date(2025, 12, 31)),
    ("2003-2025", Y2003, date(2025, 12, 31)),
    *[e for e in harness.ERAS if e[1].year >= 1994],
    ("dot-com bust", date(2000, 3, 24), date(2002, 10, 9)),
]


def tsmom12() -> c.ResearchStrategy:
    return c.weekly(c.slots(c.tsmom_signal))


def hold() -> c.ResearchStrategy:
    return c.weekly(c.equal_weight)


def go_once(idea: str, variant: str, strategy: c.ResearchStrategy, u: c.Ctx, kind: str) -> c.Run:
    """Run and log a configuration once; later calls re-score it without a new `tries.md` row."""
    tag = variant if u.name == "six" else f"{variant}@{u.name}"
    done = (harness.DATA / "runs" / idea / f"{tag}.train.csv").exists()
    return c.go(idea, variant, strategy, u, kind, log=not done)


def replay(strategy: c.ResearchStrategy, u: c.Ctx) -> gym.Result:
    """The same decisions through the gym again, keeping the fills (nothing logged)."""
    return gym.simulate(harness.decisions(strategy, u.panel, u.start, u.end), u.hist)


def pct(x: float, digits: int = 1) -> str:
    return "-" if math.isnan(x) else f"{x * 100:+.{digits}f}%"


def num(x: float, digits: int = 2) -> str:
    return "-" if math.isnan(x) else f"{x:.{digits}f}"


def since(run: c.Run, a: date) -> np.ndarray:
    return run.rets_between(max(a, run.days[0]), run.days[-1])


# --- one asset on its own: states, spells, bear windows ---


@dataclass
class Spell:
    sym: str
    out: date  # exit fill (or the day holding began, for a spell that starts out)
    back: date  # re-entry fill (or the last bar, if still out)
    days: int
    move: float  # log(asset price at re-entry / price at exit): positive = bought back higher
    closed: bool
    lead: bool


@dataclass
class Bear:
    sym: str
    hi: int
    lo: int
    settled: bool


@dataclass
class Solo:
    sym: str
    dates: list[date]
    o: np.ndarray
    cl: np.ndarray
    i0: int  # bar whose open is the hold run's entry fill
    state: np.ndarray  # True where the rule holds the asset during the bar's session
    gap: np.ndarray  # log(open / previous close), 0 at i0
    intr: np.ndarray  # log(close / open)
    spells: list[Spell]
    bears: list[Bear]
    bucket: np.ndarray  # 0 the rest, 1 bear window, 2 rebound window
    rule: c.Run
    hold: c.Run
    rule_fills: int

    @property
    def per_year(self) -> int:
        return c.bpy(self.sym)

    @property
    def years(self) -> float:
        return (len(self.cl) - self.i0) / self.per_year

    def in_log(self, mask: np.ndarray | None = None) -> float:
        """Log return earned while holding (gap belongs to the state before the open)."""
        m = np.ones(len(self.cl), bool) if mask is None else mask
        before = np.concatenate([[False], self.state[:-1]])
        return float((self.gap * before * m).sum() + (self.intr * self.state * m).sum())

    def all_log(self, mask: np.ndarray | None = None) -> float:
        m = np.ones(len(self.cl), bool) if mask is None else mask
        return float(((self.gap + self.intr) * m).sum())


def find_bears(sym: str, cl: np.ndarray, i0: int, thr: float) -> list[Bear]:
    """Card A5: from the highest close since the last bear low to the lowest close after it,
    once the fall reaches `thr`; the low is settled when the close has risen `thr` from it."""
    out: list[Bear] = []
    hi, lo, falling = i0, i0, False
    for i in range(i0 + 1, len(cl)):
        if not falling:
            if cl[i] > cl[hi]:
                hi = i
            elif cl[i] <= cl[hi] * (1 - thr):
                falling, lo = True, i
        elif cl[i] < cl[lo]:
            lo = i
        elif cl[i] >= cl[lo] * (1 + thr):
            out.append(Bear(sym, hi, lo, True))
            falling = False
            hi = lo + 1 + int(np.argmax(cl[lo + 1 : i + 1]))
    if falling:
        out.append(Bear(sym, hi, lo, False))
    return out


def solo(sym: str) -> Solo:
    u = c.ctx(sym)
    logged = ("crypto-alone", "baseline") if UNIVERSE[sym] == CRYPTO else (ANATOMY, "baseline")
    if UNIVERSE[sym] == CRYPTO:  # logged on 2026-11-12 by lib/crypto_alone.py: re-scored
        h = c.go(logged[0], "equal-weight", hold(), u, "baseline", log=False)
        r = c.go(logged[0], "tsmom12", tsmom12(), u, "baseline", log=False)
    else:
        h = go_once(ANATOMY, "equal-weight", hold(), u, "baseline")
        r = go_once(ANATOMY, "tsmom12", tsmom12(), u, "baseline")
    bars = u.hist[sym]
    dates = [b.date for b in bars]
    idx = {d: i for i, d in enumerate(dates)}
    o = np.array([b.open for b in bars])
    cl = np.array([b.close for b in bars])
    n = len(bars)
    hold_fills = replay(hold(), u).fills
    rule_fills = replay(tsmom12(), u).fills
    i0 = idx[hold_fills[0].time.date()]
    flip = {idx[f.time.date()]: f.qty > 0 for f in rule_fills}
    state = np.zeros(n, bool)
    cur = False
    for i in range(i0, n):
        cur = flip.get(i, cur)
        state[i] = cur
    gap = np.zeros(n)
    gap[i0 + 1 :] = np.log(o[i0 + 1 :] / cl[i0:-1])
    intr = np.zeros(n)
    intr[i0:] = np.log(cl[i0:] / o[i0:])
    spells: list[Spell] = []
    start, lead = (i0, True) if not state[i0] else (-1, False)
    for i in range(i0 + 1, n):
        if state[i - 1] and not state[i]:
            start, lead = i, False
        elif state[i] and not state[i - 1]:
            spells.append(Spell(sym, dates[start], dates[i], (dates[i] - dates[start]).days,
                                float(math.log(o[i] / o[start])), True, lead))  # fmt: skip
    if not state[-1]:
        spells.append(Spell(sym, dates[start], dates[-1], (dates[-1] - dates[start]).days,
                            float(math.log(cl[-1] / o[start])), False, lead))  # fmt: skip
    thr = 0.5 if UNIVERSE[sym] == CRYPTO else 0.2
    bears = find_bears(sym, cl, i0, thr)
    bucket = np.zeros(n, dtype=int)
    for k, b in enumerate(bears):
        bucket[b.hi + 1 : b.lo + 1] = 1
        stop = dates[b.lo] + timedelta(days=365)
        nxt = bears[k + 1].hi if k + 1 < len(bears) else n - 1
        j = b.lo + 1
        while j <= nxt and j < n and dates[j] <= stop:
            bucket[j] = 2
            j += 1
    return Solo(sym, dates, o, cl, i0, state, gap, intr, spells, bears, bucket, r, h,
                len(rule_fills))  # fmt: skip


def section_assets(solos: list[Solo]) -> list[str]:
    out = ["## 1. Each asset on its own: the rule against holding", ""]
    out += [
        "One asset, all of the account, from the day it has a year of bars. `hold` buys once; "
        "the rule is `tsmom12` on that asset alone. p is the paired bootstrap's one-sided "
        "p-value that the rule's Sharpe is higher.",
        "",
        "| Asset | From | Sharpe hold | Sharpe rule | Difference (p) | Growth/yr hold | "
        "Growth/yr rule | Worst loss hold | Worst loss rule | Time in |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for s in solos:
        a, b = c.align(s.rule, s.hold)
        d, p, _, _ = stats.sharpe_diff_boot(a, b)
        out.append(
            f"| {s.sym} | {s.rule.days[0]} | {stats.sharpe(b):.2f} | {stats.sharpe(a):.2f} | "
            f"{d:+.2f} ({p:.2f}) | {pct(stats.cagr(b))} | {pct(stats.cagr(a))} | "
            f"{stats.max_drawdown(b):.0%} | {stats.max_drawdown(a):.0%} | "
            f"{s.state[s.i0 :].mean():.0%} |"
        )
    out += ["", "Sharpe of the rule minus Sharpe of holding, by era (blank: under 250 days):", ""]
    names = [n for n, _, _ in harness.ERAS if n >= "1994"]
    out += ["| Asset |" + "".join(f" {n} |" for n in names) + " 2003-2025 |"]
    out += ["|---|" + "---:|" * (len(names) + 1)]
    for s in solos:
        er, eh = c.era_sharpes(s.rule), c.era_sharpes(s.hold)
        row = f"| {s.sym} |" + "".join(
            f" {'-' if math.isnan(er[n]) else format(er[n] - eh[n], '+.2f')} |" for n in names
        )
        a, b = since(s.rule, Y2003), since(s.hold, Y2003)
        out.append(row + f" {stats.sharpe(a) - stats.sharpe(b):+.2f} |")
    return out + [""]


def section_in_out(solos: list[Solo]) -> list[str]:
    out = ["## 2. In and out: what the asset did while the rule held it and while it did not", ""]
    out += [
        "Log points are sums of log returns (x100); a year's worth is shown. The asset's return "
        "is split at every fill: the overnight gap belongs to the position held before the open. "
        "`Asset while in` and `Asset while out` are annualised over the time spent in that "
        "state, so they compare the two kinds of days directly.",
        "",
        "| Asset | Time in | Asset while in (log pts/yr of in-time) | Asset while out (log pts/yr "
        "of out-time) | Volatility in | Volatility out | Of the 20 worst days, rule was out |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for s in solos:
        st = s.state[s.i0 :]
        lr = (s.gap + s.intr)[s.i0 :]
        n_in, n_out = int(st.sum()), int((~st).sum())
        tot_in = s.in_log()
        tot_out = s.all_log() - tot_in
        worst = np.argsort(lr)[:20]
        out.append(
            f"| {s.sym} | {st.mean():.0%} | {tot_in / (n_in / s.per_year) * 100:+.1f} | "
            f"{tot_out / (n_out / s.per_year) * 100:+.1f} | "
            f"{lr[st].std() * math.sqrt(s.per_year):.0%} | "
            f"{lr[~st].std() * math.sqrt(s.per_year):.0%} | {int((~st[worst]).sum())} |"
        )
    out += [
        "",
        "The identity, per year of the asset's history (log points a year): the rule's growth = "
        "holding's growth - what the asset did while the rule was out - costs.",
        "",
        "| Asset | Years | Holding | Asset while rule was out | Costs and slippage | Rule |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for s in solos:
        y = s.years
        rule = math.log(s.rule.equity[-1] / gym.START_CASH)
        held = math.log(s.hold.equity[-1] / gym.START_CASH)
        outside = s.all_log() - s.in_log()
        cost = rule - (held - outside)
        out.append(
            f"| {s.sym} | {y:.1f} | {held / y * 100:+.1f} | {outside / y * 100:+.1f} | "
            f"{cost / y * 100:+.2f} | {rule / y * 100:+.1f} |"
        )
    out += [
        "",
        "A negative `Asset while rule was out` means the asset fell on balance while the rule was "
        "out (the rule gained by being out); a positive one means it rose (the rule missed it).",
        "",
    ]
    return out


def scaled(r: np.ndarray, w: float) -> np.ndarray:
    return r * w


def section_invested(solos: list[Solo], book: c.Run, ew: c.Run) -> list[str]:
    out = ["## 3. Being invested against stepping aside", ""]
    out += [
        "`Constant` holds the rule's own average share of the asset all the time (the rest in "
        "cash at 0%), so it has the Sharpe of plain holding. The growth gap between the rule "
        "and `constant` is what choosing *when* to hold added or cost; the gaps in volatility "
        "and worst loss are what stepping aside bought.",
        "",
        "| What | Average share held | Growth/yr constant | Growth/yr rule | Timing gap | "
        "Volatility constant | Volatility rule | Worst loss constant | Worst loss rule | "
        "Sharpe constant | Sharpe rule |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    def row(label: str, rule: np.ndarray, held: np.ndarray, w: float) -> str:
        k = scaled(held, w)
        return (
            f"| {label} | {w:.0%} | {pct(stats.cagr(k))} | {pct(stats.cagr(rule))} | "
            f"{pct(stats.cagr(rule) - stats.cagr(k))} | {stats.vol(k):.1%} | "
            f"{stats.vol(rule):.1%} | {stats.max_drawdown(k):.0%} | "
            f"{stats.max_drawdown(rule):.0%} | {stats.sharpe(k):.2f} | {stats.sharpe(rule):.2f} |"
        )

    for s in solos:
        a, b = c.align(s.rule, s.hold)
        out.append(row(f"{s.sym} alone", a, b, float(s.state[s.i0 :].mean())))
    for label, a0 in (("1994-2025", book.days[0]), ("2003-2025", Y2003)):
        a, b = since(book, a0), since(ew, a0)
        i = max((a0 - book.days[0]).days, 0)
        w = float(np.mean([sum(d.weights.values()) for d in book.decisions[i:]]))
        out.append(row(f"Six-asset book, {label}", a, b, w))
    return out + [""]


BUCKETS = [(0, 28, "under 4 weeks"), (28, 91, "4-13 weeks"), (91, 182, "13-26 weeks"),
           (182, 10**6, "over 26 weeks")]  # fmt: skip


def section_spells(solos: list[Solo]) -> list[str]:
    out = ["## 4. Out-spells, flips and whipsaw", ""]
    out += [
        "A spell runs from the exit fill to the re-entry fill. It *saved* if the asset was "
        "cheaper at re-entry and was a *whipsaw* if it was dearer. Log points a year of the "
        "asset's history, on the asset's own slot (not the book). `Net` = saved - whipsaw - "
        "costs = the rule's growth minus holding's.",
        "",
        "| Asset | Fills/yr | Spells | Saved spells | Whipsaws | Saved (log pts/yr) | Whipsaw "
        "cost (log pts/yr) | Costs (log pts/yr) | Net (log pts/yr) | Median spell (days) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for s in solos:
        y = s.years
        good = [x for x in s.spells if x.move < 0]
        bad = [x for x in s.spells if x.move >= 0]
        saved = -sum(x.move for x in good)
        lost = sum(x.move for x in bad)
        rule = math.log(s.rule.equity[-1] / gym.START_CASH)
        held = math.log(s.hold.equity[-1] / gym.START_CASH)
        cost = (held - rule) - (lost - saved)
        med = float(np.median([x.days for x in s.spells])) if s.spells else math.nan
        out.append(
            f"| {s.sym} | {s.rule_fills / y:.1f} | {len(s.spells)} | {len(good)} | {len(bad)} | "
            f"{saved / y * 100:+.1f} | {-lost / y * 100:+.1f} | {-cost / y * 100:+.2f} | "
            f"{(rule - held) / y * 100:+.1f} | {med:.0f} |"
        )
    out += ["", "Spells by length, all six assets (net = saved minus whipsaw, in log points; "
            "summed over the assets' slots, not annualised):", ""]  # fmt: skip
    out += ["| Length | Spells | Whipsaws | Net log points | Per asset: spells (net) |",
            "|---|---:|---:|---:|---|"]  # fmt: skip
    every = [x for s in solos for x in s.spells]
    for lo, hi, label in BUCKETS:
        sub = [x for x in every if lo <= x.days < hi]
        per = ", ".join(
            f"{s.sym} {len(k)} ({-sum(x.move for x in k) * 100:+.0f})"
            for s in solos
            if (k := [x for x in s.spells if lo <= x.days < hi])
        )
        out.append(
            f"| {label} | {len(sub)} | {sum(x.move >= 0 for x in sub)} | "
            f"{-sum(x.move for x in sub) * 100:+.0f} | {per} |"
        )

    def listing(title: str, rows: list[Spell]) -> list[str]:
        t = ["", title, "", "| Asset | Out | Back in | Days | Asset's move while out |",
             "|---|---|---|---:|---:|"]  # fmt: skip
        for x in rows:
            end = str(x.back) if x.closed else f"{x.back} (still out)"
            start = f"{x.out} (start)" if x.lead else str(x.out)
            t.append(f"| {x.sym} | {start} | {end} | {x.days} | {math.expm1(x.move):+.0%} |")
        return t

    ranked = sorted(every, key=lambda x: x.move)
    out += listing("The ten spells that saved most:", ranked[:10])
    out += listing("The ten costliest whipsaws:", ranked[::-1][:10])
    return out + [""]


def section_bears(solos: list[Solo]) -> list[str]:
    out = ["## 5. Bear markets, rebounds and the rest", ""]
    out += [
        "Bear window: a fall of at least 20% (ETFs) or 50% (coins) from the highest close since "
        "the last bear low, to the lowest close after it. Rebound: the 365 days after that low. "
        "Log points summed inside each bucket; `Rule - hold` is what the rule gained or lost "
        "there against holding, before costs.",
        "",
        "| Asset | Bucket | Windows | Years | Holding (log pts) | Rule (log pts) | Rule - hold "
        "| Rule - hold per year of history | Time in |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    names = {1: "bear", 2: "rebound", 0: "the rest"}
    tot = {k: [0.0, 0.0, 0.0] for k in names}
    for s in solos:
        live = np.arange(len(s.cl)) >= s.i0
        for k in (1, 2, 0):
            m = (s.bucket == k) & live
            held, rule = s.all_log(m), s.in_log(m)
            yrs = m.sum() / s.per_year
            tot[k][0] += held
            tot[k][1] += rule
            tot[k][2] += (rule - held) / s.years
            out.append(
                f"| {s.sym} | {names[k]} | {len(s.bears) if k else '-'} | {yrs:.1f} | "
                f"{held * 100:+.0f} | {rule * 100:+.0f} | {(rule - held) * 100:+.0f} | "
                f"{(rule - held) / s.years * 100:+.1f} | {s.state[m].mean():.0%} |"
            )
    for k in (1, 2, 0):
        out.append(
            f"| all six | {names[k]} | | | {tot[k][0] * 100:+.0f} | {tot[k][1] * 100:+.0f} | "
            f"{(tot[k][1] - tot[k][0]) * 100:+.0f} | {tot[k][2] / len(solos) * 100:+.1f} "
            f"(average) | |"
        )
    out += [
        "",
        "Every bear window: how far below the high the rule sold, and how far above the low it "
        "bought back. `Held` and `rule` are the returns inside the window (high to low).",
        "",
        "| Asset | High | Low | Held | Rule | Sold at (from the high) | Bought back at (from the "
        "low) | Days from low to buy-back |",
        "|---|---|---|---:|---:|---|---|---:|",
    ]
    exits, entries, waits = [], [], []
    for s in solos:
        st = s.state
        for b in s.bears:
            m = np.zeros(len(s.cl), bool)
            m[b.hi + 1 : b.lo + 1] = True
            held, rule = math.expm1(s.all_log(m)), math.expm1(s.in_log(m))
            sold = "was out at the high"
            if st[b.hi]:
                i = next((i for i in range(b.hi + 1, len(st)) if not st[i]), None)
                if i is None:
                    sold = "never sold"
                elif i > b.lo:
                    sold = "held through the low"
                else:
                    x = s.o[i] / s.cl[b.hi] - 1
                    exits.append(x)
                    sold = f"{x:+.0%} on {s.dates[i]}"
            j = next(
                (j for j in range(b.lo + 1, len(st)) if st[j] and not st[j - 1]), None
            ) if not st[b.lo] else None  # fmt: skip
            if st[b.lo]:
                back = "was in at the low"
            elif j is None:
                back = "still out"
            else:
                y = s.o[j] / s.cl[b.lo] - 1
                entries.append(y)
                waits.append((s.dates[j] - s.dates[b.lo]).days)
                back = f"{y:+.0%} on {s.dates[j]}"
            wait = "-" if j is None else str((s.dates[j] - s.dates[b.lo]).days)
            low = f"{s.dates[b.lo]}" + ("" if b.settled else " (not settled)")
            out.append(
                f"| {s.sym} | {s.dates[b.hi]} | {low} | {held:+.0%} | {rule:+.0%} | {sold} | "
                f"{back} | {wait} |"
            )
    out += [
        "",
        f"Across the {sum(len(s.bears) for s in solos)} bear windows: the rule sold at a median "
        f"of {np.median(exits):+.0%} from the high ({len(exits)} sales inside a window) and "
        f"bought back at a median of {np.median(entries):+.0%} above the low, "
        f"{np.median(waits):.0f} days after it ({len(entries)} buy-backs).",
        "",
    ]
    return out


# --- the six-asset book: exact contribution of each asset ---


def attribute(res: gym.Result, u: c.Ctx) -> tuple[list[date], np.ndarray, dict[str, np.ndarray]]:
    """Each asset's share of every day's return: (value change - cash put in) / yesterday's
    equity. The shares sum to the book's daily return exactly (cash earns nothing)."""
    days = [d for d, _ in res.equity]
    eq = np.array([e for _, e in res.equity])
    pos = {d: k for k, d in enumerate(days)}
    out = {}
    total = np.zeros(len(days))
    ords = np.array([d.toordinal() for d in days])
    for s in u.hist:
        qty = np.zeros(len(days))
        paid = np.zeros(len(days))
        for f in res.fills:
            if f.symbol == s:
                k = pos[f.time.date()]
                qty[k:] += f.qty
                paid[k] += f.qty * f.price + f.fee
        i = np.searchsorted(u.panel.ord[s], ords, side="right") - 1
        px = np.where(i >= 0, u.panel.c[s][np.maximum(i, 0)], 0.0)
        value = qty * px
        pnl = np.diff(value, prepend=0.0) - paid
        out[s] = pnl
        total += pnl
    gain = np.diff(eq, prepend=gym.START_CASH)
    if np.abs(total - gain).max() > 1e-6 * eq.max():
        raise AssertionError("attribution does not add up to the book's equity")
    prev = np.concatenate([[gym.START_CASH], eq[:-1]])
    return days, eq, {s: v / prev for s, v in out.items()}


def window_sum(days: list[date], x: np.ndarray, a: date, b: date) -> float:
    """Sum of daily contributions inside [a, b], per year of that window (x365 / days)."""
    lo, hi = max(a, days[0]), min(b, days[-1])
    if hi <= lo:
        return math.nan
    m = np.array([lo <= d <= hi for d in days])
    return float(x[m].sum() * 365 / ((hi - lo).days + 1))


def section_book(six: c.Ctx, book: c.Run, ew: c.Run) -> list[str]:
    out = ["## 6. The six-asset book: where the return comes from", ""]
    out += [
        "Both books replayed through the gym with every fill kept. An asset's contribution on a "
        "day is its change in value minus the cash put into it, over the book's equity the day "
        "before; the six add up to the book's daily return to the cent. Shown as the sum of "
        "daily returns per year of the window (percent a year; these add across assets, growth "
        "rates do not).",
        "",
    ]
    d1, _, c1 = attribute(replay(tsmom12(), six), six)
    d2, _, c2 = attribute(replay(hold(), six), six)
    head = "| Window |" + "".join(f" {s} |" for s in ORDER) + " Book |"
    sep = "|---|" + "---:|" * (len(ORDER) + 1)

    def block(title: str, f) -> list[str]:  # type: ignore[no-untyped-def]
        t = [title, "", head, sep]
        for name, a, b in WINDOWS:
            vals = [f(s, a, b) for s in ORDER]
            t.append(
                f"| {name} |" + "".join(f" {pct(v)} |" for v in vals)
                + f" {pct(float(np.nansum(vals)))} |"
            )  # fmt: skip
        return t + [""]

    out += block("`tsmom12`:", lambda s, a, b: window_sum(d1, c1[s], a, b))
    out += block("Equal weight (hold everything):", lambda s, a, b: window_sum(d2, c2[s], a, b))
    out += block(
        "`tsmom12` minus equal weight (positive: the rule earned more from that asset):",
        lambda s, a, b: window_sum(d1, c1[s], a, b) - window_sum(d2, c2[s], a, b),
    )
    out += ["Sharpe, growth and worst loss of the two books in the same windows:", ""]
    out += ["| Window | Sharpe rule | Sharpe equal weight | Growth/yr rule | Growth/yr equal "
            "weight | Worst loss rule | Worst loss equal weight | Average share held by the rule |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    for name, a, b in WINDOWS:
        ra, rb = book.rets_between(a, b), ew.rets_between(a, b)
        i = max((a - book.days[0]).days, 0)
        j = min((b - book.days[0]).days, len(book.decisions) - 1)
        w = float(np.mean([sum(d.weights.values()) for d in book.decisions[i : j + 1]]))
        out.append(
            f"| {name} | {stats.sharpe(ra):.2f} | {stats.sharpe(rb):.2f} | {pct(stats.cagr(ra))} "
            f"| {pct(stats.cagr(rb))} | {stats.max_drawdown(ra):.0%} | "
            f"{stats.max_drawdown(rb):.0%} | {w:.0%} |"
        )
    out += ["", "Calendar years since 2003, the rule's return minus equal weight's, with the "
            "asset that moved the gap most (its contribution to the rule minus to equal weight):",
            "", "| Year | Rule | Equal weight | Gap | Largest part of the gap |",
            "|---|---:|---:|---:|---|"]  # fmt: skip
    rows = []
    for y in range(2003, 2026):
        a, b = date(y, 1, 1), date(y, 12, 31)
        ra, rb = book.rets_between(date(y - 1, 12, 31), b), ew.rets_between(date(y - 1, 12, 31), b)
        ya, yb = float(np.prod(1 + ra) - 1), float(np.prod(1 + rb) - 1)
        m1 = np.array([a <= d <= b for d in d1])
        m2 = np.array([a <= d <= b for d in d2])
        part = {s: float(c1[s][m1].sum() - c2[s][m2].sum()) for s in ORDER}
        top = max(part, key=lambda s: abs(part[s]))
        rows.append((ya - yb, f"| {y} | {pct(ya)} | {pct(yb)} | {pct(ya - yb)} | {top} "
                              f"{pct(part[top])} |"))  # fmt: skip
    out += [r for _, r in rows]
    behind = sum(g < 0 for g, _ in rows)
    out += ["", f"The rule finished behind equal weight in {behind} of {len(rows)} years and "
            f"ahead in {len(rows) - behind}.", ""]  # fmt: skip
    return out


# --- the sensitivity surface ---


@dataclass
class Cell:
    name: str
    run: c.Run
    sharpe: float
    sharpe03: float
    mdd: float
    mdd03: float
    cagr: float
    turnover: float
    diff: float


def cell(name: str, run: c.Run, twin: c.Run) -> Cell:
    r, r3 = run.rets, since(run, Y2003)
    return Cell(name, run, stats.sharpe(r), stats.sharpe(r3), stats.max_drawdown(r),
                stats.max_drawdown(r3), stats.cagr(r), run.score.turnover,
                stats.sharpe(r) - stats.sharpe(twin.rets))  # fmt: skip


def band_run(six: c.Ctx, band: float) -> c.Run:
    """`tsmom12` with another rebalance band in the gym (`harness.run` has no band argument)."""
    name = f"tsmom12-band{band * 100:g}"
    path = harness.DATA / "runs" / SURFACE / f"{name}.train.csv"
    decs = harness.decisions(tsmom12(), six.panel, six.start, six.end)
    res = gym.simulate(decs, six.hist, band=band)
    days, equity = harness._calendar(res.equity)
    run = c.Run(SURFACE, name, "train", report.score(f"{SURFACE}/{name}", res), days, equity,
                float(np.mean([sum(d.weights.values()) for d in decs])), decs)  # fmt: skip
    if not path.exists() and not c.DRY:
        harness._log(run, "robustness", six.start, six.end)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("logged\n")
    return run


def spearman(a: list[float], b: list[float]) -> float:
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def matrix(title: str, rows: list[str], cols: list[str], f) -> list[str]:  # type: ignore[no-untyped-def]
    t = [title, "", "| |" + "".join(f" {x} |" for x in cols), "|---|" + "---:|" * len(cols)]
    for r in rows:
        t.append(f"| {r} |" + "".join(f" {f(r, x)} |" for x in cols))
    return t + [""]


def section_surface(six: c.Ctx, twin: c.Run, warm: dict[str, tt.Warm]) -> list[str]:
    out = ["## 7. Sensitivity surface (train, IN SAMPLE: a description, nothing is selected)", ""]
    out += [
        "Every cell is a rule on the six assets, 1994-2025, through the gym, and a row in "
        "`tries.md`. Sharpe ratios. `tsmom12` is the 12-month, weekly, no-threshold cell: "
        f"{stats.sharpe(twin.rets):.2f} over 1994-2025 and "
        f"{stats.sharpe(since(twin, Y2003)):.2f} over 2003-2025.",
        "",
    ]
    cells: dict[str, Cell] = {}
    freq = {"daily": lambda f: f, "weekly": c.weekly, "monthly": c.monthly}
    grid1: dict[tuple[int, str], Cell] = {}
    for m in LOOKS:
        for fname, wrap in freq.items():
            name = f"L{m:02d}-{fname[0]}"
            if m == 12 and fname == "weekly":
                run = twin
            else:
                run = go_once(SURFACE, name, wrap(tt.fixed(m)), six, "variant")
            grid1[(m, fname)] = cells[name] = cell(name, run, twin)
    fnames = list(freq)

    def neigh1(m: int, fname: str) -> float:
        i, j = LOOKS.index(m), fnames.index(fname)
        near = [(LOOKS[i + di], fname) for di in (-1, 1) if 0 <= i + di < len(LOOKS)]
        near += [(m, fnames[j + dj]) for dj in (-1, 1) if 0 <= j + dj < len(fnames)]
        return float(np.mean([grid1[k].sharpe for k in near]))

    rows = [str(m) for m in LOOKS]
    out += ["### Lookback (months) by decision frequency", ""]
    out += matrix("Sharpe 1994-2025:", rows, fnames,
                  lambda r, x: num(grid1[(int(r), x)].sharpe))  # fmt: skip
    out += matrix("Sharpe 2003-2025:", rows, fnames,
                  lambda r, x: num(grid1[(int(r), x)].sharpe03))  # fmt: skip
    out += matrix("Worst loss 1994-2025:", rows, fnames,
                  lambda r, x: f"{grid1[(int(r), x)].mdd:.0%}")  # fmt: skip
    out += matrix("Trades a year (turnover):", rows, fnames,
                  lambda r, x: f"{grid1[(int(r), x)].turnover:.1f}")  # fmt: skip
    out += matrix("Sharpe 1994-2025 minus the average of the cell's grid neighbours "
                  "(a spike is above +0.10):", rows, fnames,
                  lambda r, x: f"{grid1[(int(r), x)].sharpe - neigh1(int(r), x):+.2f}")  # fmt: skip

    # fast and slow together
    grid2: dict[tuple[int, int], Cell] = {}
    for a in PAIRS:
        for b in PAIRS:
            if a == b:
                grid2[(a, b)] = grid1[(a, "weekly")]
            elif a < b:
                name = f"and-{a:02d}-{b:02d}"
                run = go_once(SURFACE, name, c.weekly(tt.both(a, b)), six, "variant")
                grid2[(a, b)] = cells[name] = cell(name, run, twin)
            else:
                name = f"or-{b:02d}-{a:02d}"
                run = go_once(SURFACE, name, c.weekly(tt.either(b, a)), six, "variant")
                grid2[(a, b)] = cells[name] = cell(name, run, twin)
    prs = [str(p) for p in PAIRS]
    out += ["### Two lookbacks together (weekly)", ""]
    out += [
        "Above the diagonal (row < column): AND, held only if both are positive (the fast one "
        "takes you out, both must agree to get back in). Below the diagonal: OR, held if either "
        "is positive (slow to leave, quick to return). On the diagonal: the single lookback.",
        "",
    ]
    out += matrix("Sharpe 1994-2025:", prs, prs, lambda r, x: num(grid2[(int(r), int(x))].sharpe))
    out += matrix("Sharpe 2003-2025:", prs, prs,
                  lambda r, x: num(grid2[(int(r), int(x))].sharpe03))  # fmt: skip
    out += matrix("Worst loss 1994-2025:", prs, prs,
                  lambda r, x: f"{grid2[(int(r), int(x))].mdd:.0%}")  # fmt: skip
    out += matrix("Trades a year:", prs, prs,
                  lambda r, x: f"{grid2[(int(r), int(x))].turnover:.1f}")  # fmt: skip

    # thresholds
    out += ["### Entry and exit thresholds on the trend's z-score (weekly)", ""]
    out += [
        "z = the L-month return in units of the asset's own volatility. Enter above c + h, "
        "leave below c - h. Rows: centre c (negative = lenient, stays in through small losses; "
        "positive = strict). Columns: half-width h of the no-trade band. c = 0, h = 0 is the "
        "plain rule.",
        "",
    ]
    grid3: dict[tuple[int, float, float], Cell] = {}
    for m in Z_LOOKS:
        for ce in CENTRES:
            for hw in HALVES:
                if ce == 0 and hw == 0:
                    grid3[(m, ce, hw)] = grid1[(m, "weekly")]
                    continue
                name = f"z{m:02d}-c{ce:+.2f}-h{hw:.2f}"
                run = go_once(SURFACE, name, tt.threshold(m, ce, hw), six, "variant")
                grid3[(m, ce, hw)] = cells[name] = cell(name, run, twin)
        cs, hs = [f"c = {x:+.2f}" for x in CENTRES], [f"h = {x:.2f}" for x in HALVES]

        def at(r: str, x: str, m: int = m) -> Cell:
            return grid3[(m, float(r[4:]), float(x[4:]))]

        out += matrix(f"{m}-month lookback, Sharpe 1994-2025 / 2003-2025 (worst loss; trades a "
                      "year):", cs, hs,
                      lambda r, x, at=at: f"{at(r, x).sharpe:.2f} / {at(r, x).sharpe03:.2f} "
                      f"({at(r, x).mdd:.0%}; {at(r, x).turnover:.1f})")  # fmt: skip

    # the gym's rebalance band
    out += ["### The gym's rebalance band, `tsmom12` unchanged otherwise", ""]
    out += ["| Band | Sharpe 1994-2025 | Sharpe 2003-2025 | Growth/yr | Worst loss | Trades a year "
            "|", "|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    for band in (*BANDS[:1], 0.01, *BANDS[1:]):
        k = cell("", twin if band == 0.01 else band_run(six, band), twin)
        label = f"{band:.1%}" + (" (the gym's rule)" if band == 0.01 else "")
        out.append(f"| {label} | {k.sharpe:.2f} | {k.sharpe03:.2f} | {pct(k.cagr)} | {k.mdd:.0%} "
                   f"| {k.turnover:.1f} |")  # fmt: skip
    out += [""]

    # hindsight ceiling
    tuner = tt.Tuner("asset", warm)
    sc = tuner.scores(six.panel, harness.TRAIN_END)
    best = {s: tt.pick(sc[s][1]) for s in six.panel.syms}
    pool_best = tt.pick(sc["*"][1])
    h_asset = go_once(SURFACE, "hindsight-asset", c.weekly(tt.per_asset(best)), six, "variant")
    cells["hindsight-asset"] = ka = cell("hindsight-asset", h_asset, twin)
    kp = grid1[(pool_best, "weekly")]  # the pooled pick is a grid lookback: the same cell
    out += ["### Hindsight ceiling (the best lookbacks chosen with all of train in view)", ""]
    out += [
        "The tuner's own score (paper series, full train) picks, with hindsight: "
        + ", ".join(f"{s} {best[s]}" for s in ORDER)
        + f" months per asset; {pool_best} months for the pool. Run as fixed rules:",
        "",
        "| Rule | Sharpe 1994-2025 | Sharpe 2003-2025 | Against `tsmom12` (p) | Worst loss |",
        "|---|---:|---:|---:|---:|",
    ]
    labels = [
        (f"hindsight per asset ({', '.join(str(best[s]) for s in ORDER)})", ka),
        (f"hindsight pooled ({pool_best} months; the `L{pool_best:02d}-w` cell)", kp),
    ]
    for label, k in labels:
        if k.run is twin:
            out.append(f"| {label} | {k.sharpe:.2f} | {k.sharpe03:.2f} | it is `tsmom12` | "
                       f"{k.mdd:.0%} |")  # fmt: skip
            continue
        a, b = c.align(k.run, twin)
        d, p, _, _ = stats.sharpe_diff_boot(a, b)
        out.append(f"| {label} | {k.sharpe:.2f} | {k.sharpe03:.2f} | {d:+.2f} ({p:.2f}) | "
                   f"{k.mdd:.0%} |")  # fmt: skip
    out += ["", "Paper-series Sharpe by lookback over all of train (what the tuner sees at the "
            "end; SPY includes the S&P 500 index 1962-1993):", ""]  # fmt: skip
    out += ["| |" + "".join(f" {m} |" for m in tt.GRID) + " Best |",
            "|---|" + "---:|" * (len(tt.GRID) + 1)]  # fmt: skip
    for s in [*ORDER, "*"]:
        row = sc[s][1]
        out.append(f"| {'pool' if s == '*' else s} |" + "".join(f" {row[m]:.2f} |" for m in tt.GRID)
                   + f" {tt.pick(row)} |")  # fmt: skip
    out += [""]

    # summary of the whole surface
    every = list(cells.values())
    ahead = [k for k in every if k.diff > 0]
    ahead03 = [k for k in every if k.sharpe03 > stats.sharpe(since(twin, Y2003))]
    top = sorted(every, key=lambda k: -k.sharpe)[:8]
    ses = []
    for k in top:
        a, b = c.align(k.run, twin)
        _, _, lo, hi = stats.sharpe_diff_boot(a, b, draws=500)
        ses.append((hi - lo) / 3.29)
    se = float(np.median(ses))
    luck = stats.expected_max_sharpe(len(every), se**2)
    out += ["### Reading the surface", ""]
    out += [
        f"- Cells logged besides `tsmom12`: {len(every)}. Ahead of `tsmom12` on Sharpe over "
        f"1994-2025: {len(ahead)}; over 2003-2025: {len(ahead03)}.",
        f"- If none of the {len(every)} cells had any edge over `tsmom12`, the best would still "
        f"be expected to show about {luck:+.2f} (expected maximum, standard error of a "
        f"difference about {se:.2f} among the top cells; the cells are far from independent, "
        f"so this overstates luck).",
        "- The eight best cells by Sharpe 1994-2025 (in sample):",
        "",
        "| Cell | Sharpe 1994-2025 | Against `tsmom12` | Sharpe 2003-2025 | Against `tsmom12` "
        "2003-2025 | Worst loss | Trades a year |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    t03 = stats.sharpe(since(twin, Y2003))
    for k in top:
        out.append(f"| {k.name} | {k.sharpe:.2f} | {k.diff:+.2f} | {k.sharpe03:.2f} | "
                   f"{k.sharpe03 - t03:+.2f} | {k.mdd:.0%} | {k.turnover:.1f} |")  # fmt: skip
    spikes = [(m, f) for (m, f), k in grid1.items() if k.sharpe - neigh1(m, f) > 0.10]
    out += ["", "- Spikes in the lookback-by-frequency map (a cell more than 0.10 above its "
            "neighbours): " + (", ".join(f"{m} months {f}" for m, f in spikes) or "none") + ".",
            ""]  # fmt: skip
    return out


# --- does the best lookback persist? ---


def section_persist(six: c.Ctx, warm: dict[str, tt.Warm]) -> list[str]:
    out = ["## 8. Does the best lookback persist from one era to the next?", ""]
    out += [
        "From the paper series the tuner scores on (gym-free, costs charged; no `tries.md` "
        "rows). Sharpe of each grid lookback in each era, for eras with at least two years of "
        "that asset. `Rank corr.` is the Spearman rank correlation of the seven lookbacks with "
        "the previous era (+1: same order, 0: unrelated). `Last best, now` is the rank (1 = "
        "best of 7) that the previous era's best lookback has in this era; 4 is what chance "
        "gives.",
        "",
        "| Asset | Era |"
        + "".join(f" {m} |" for m in tt.GRID)
        + " Best | Rank corr. | Last best, now | Last best minus 12 months, now |",
        "|---|---|" + "---:|" * (len(tt.GRID) + 4),
    ]
    n_all = {s: len(six.panel.c[s]) for s in six.panel.syms}
    corr, ranks, edges = [], [], []
    for s in [*ORDER, "*"]:
        prev: dict[int, float] | None = None
        for name, a, b in harness.ERAS:
            row = {}
            for m in tt.GRID:
                if s == "*":
                    d, r = tt.pooled_dated(six.panel, n_all, m, warm, tt.GRID)
                    per = 365
                else:
                    d, r = tt.asset_series(six.panel, s, n_all[s], m, warm, tt.GRID)
                    per = c.bpy(s)
                keep = (d >= a.toordinal()) & (d <= b.toordinal())
                if keep.sum() < 2 * per:
                    break
                row[m] = tt.sharpe_of(r[keep], per)
            if len(row) < len(tt.GRID):
                continue
            best = tt.pick(row)
            extra = " - | - | - |"
            if prev is not None:
                rc = spearman([prev[m] for m in tt.GRID], [row[m] for m in tt.GRID])
                last = tt.pick(prev)
                rank = 1 + sum(row[m] > row[last] for m in tt.GRID)
                edge = row[last] - row[12]
                if s != "*":
                    corr.append(rc)
                    ranks.append(rank)
                    edges.append(edge)
                extra = f" {rc:+.2f} | {rank} ({last} months) | {edge:+.2f} |"
            vals = "".join(f" {row[m]:.2f} |" for m in tt.GRID)
            out.append(f"| {'pool' if s == '*' else s} | {name} |{vals} {best} |{extra}")
            prev = row
    out += [
        "",
        f"Over the {len(corr)} era-to-era steps of the six assets: average rank correlation "
        f"{np.mean(corr):+.2f}; the previous era's best lookback ranked {np.mean(ranks):.1f} of 7 "
        f"on average in the next era, was the best again in {sum(r == 1 for r in ranks)} steps, "
        f"and beat the 12-month rule in {sum(e > 0 for e in edges)} of them (average Sharpe "
        f"difference to 12 months {np.mean(edges):+.2f}).",
        "",
    ]
    return out


def main() -> None:
    six = c.ctx("six")
    gspc = c.ctx("GSPC")
    warm = {"SPY": tt.warm_from(gspc.panel, "GSPC", date(1993, 1, 28))}
    twin = c.go("baselines", "tsmom12", tsmom12(), six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", hold(), six, "baseline", log=False)
    solos = [solo(s) for s in ORDER]
    body = [
        MARK,
        "",
        "Train period only (decisions to 2025-11-09), total-return prices, the gym's fills and "
        "costs. `tsmom12`: each asset's equal slot is held while its 365-day return is "
        "positive, else cash; decided on Fridays. Everything here is in sample and descriptive.",
        "",
    ]
    body += section_assets(solos)
    body += section_in_out(solos)
    body += section_invested(solos, twin, ew)
    body += section_spells(solos)
    body += section_bears(solos)
    body += section_book(six, twin, ew)
    body += section_surface(six, twin, warm)
    body += section_persist(six, warm)
    path = harness.RESEARCH / "results" / ("trend-tune-anatomy.md" if not c.DRY
                                           else "trend-tune-anatomy.dry.md")  # fmt: skip
    head = "# trend-tune, Part A: anatomy of `tsmom12`\n\nCard: `trend-tune.md`.\n"
    if path.exists() and MARK in path.read_text():
        head = path.read_text().split(MARK)[0].rstrip() + "\n"
    path.write_text(head + "\n" + "\n".join(body).rstrip() + "\n")
    print("\n".join(body))


if __name__ == "__main__":
    main()
