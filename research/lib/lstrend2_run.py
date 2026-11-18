"""ls-trend-2: `tsmom12` + the wide long-short TSMOM book at gross <= 1 (Part A, a strategy
test), and the 1/3/12-month signal on the wide book (Part B, descriptive).
Card: research/cards/ls-trend-2.md.

    uv run --with openpyxl python -I research/lib/lstrend2_run.py <cache_root> A
    uv run --with openpyxl python -I research/lib/lstrend2_run.py <cache_root> B

Reads the ETF series written by `lstrend1_fetch.py`, survey-5's fund series and AQR workbook,
the repo's price cache (`research/data/`). Appends the card's rows to `tries.md` (first run of
each part only) and writes `research/results/ls-trend-2-blend.md` (A) or
`research/results/ls-trend-2-hop.md` (B). No day after 2025-10-31 is read.
"""

from __future__ import annotations

import bisect
import csv
import math
import sys
from collections import defaultdict
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cash_interest as ci  # noqa: E402
import common as c  # noqa: E402
import harness  # noqa: E402
import lstrend1_run as l1  # noqa: E402
import numpy as np  # noqa: E402
import stats  # noqa: E402
import survey5_live as s5  # noqa: E402
from survey5_live import Month, Series, compound, corr, cut, months  # noqa: E402

from grimstrade import gym  # noqa: E402

IDEA = "ls-trend-2"
LAST_DAY = l1.LAST_DAY
P = (date(2007, 4, 1), LAST_DAY)
LD = (date(2010, 2, 1), LAST_DAY)
CRASH = l1.CRASH
FAST: dict[str, tuple[Month, Month]] = {
    "2020-02..03": ((2020, 2), (2020, 3)),
    "2018-10..12": ((2018, 10), (2018, 12)),
    "2011-08..09": ((2011, 8), (2011, 9)),
    "2015-08..09": ((2015, 8), (2015, 9)),
    "2008": ((2008, 1), (2008, 12)),
    "2022": ((2022, 1), (2022, 12)),
}
DRAWS = 20_000
FAMILY_BAR = 0.10 / 68
PROJECT_N = 1_012


class Book(l1.Book):
    """A wide-book cell with a signal choice, an optional gross-1 rescaling and its own costs."""

    def __init__(
        self,
        name: str,
        assets: list[str],
        *,
        hop: bool = False,
        gross1: bool = False,
        cost: float = l1.COST,
        borrow: float = l1.BORROW,
    ) -> None:
        super().__init__(name, assets, True)
        self.hop, self.gross1, self.cost, self.borrow = hop, gross1, cost, borrow
        self.cost_d: list[float] = []
        self.borrow_d: list[float] = []
        self.traded_d: list[float] = []
        self.traded_today = 0.0


def bill_steps(cal: list[date], rf_day: dict[date, float]) -> dict[date, float]:
    rf_t: dict[date, float] = {}
    for a, b in zip(cal, cal[1:], strict=False):
        g, d = 1.0, a + timedelta(days=1)
        while d <= b:
            g *= 1 + rf_day.get(d, 0.0)
            d += timedelta(days=1)
        rf_t[b] = g - 1
    return rf_t


def run_books(
    prices: dict[str, dict[date, float]], rf_day: dict[date, float], books: list[Book]
) -> dict[date, float]:
    """ls-trend-1's `run_books`, with the 1/3/12 signal, gross-1 rescaling and per-book costs.
    Returns the per-trading-day bill return."""
    cal = sorted(set().union(*(p.keys() for p in prices.values())))
    first = {t: min(p) for t, p in prices.items()}
    pdates = {t: sorted(p) for t, p in prices.items()}
    rets: dict[str, dict[date, float]] = {}
    for t, ds in pdates.items():
        p = prices[t]
        rets[t] = {b: p[b] / p[a] - 1 for a, b in zip(ds, ds[1:], strict=False)}
    rf_t = bill_steps(cal, rf_day)
    month_end = {
        a for a, b in zip(cal, cal[1:], strict=False) if (a.year, a.month) != (b.year, b.month)
    }
    m1: dict[str, float] = {}
    m2: dict[str, float] = {}
    nret: dict[str, int] = defaultdict(int)
    bill = [1.0]
    for b in cal[1:]:
        bill.append(bill[-1] * (1 + rf_t[b]))

    def past(t: str, back: date) -> float:
        ds = pdates[t]
        return prices[t][ds[bisect.bisect_right(ds, back) - 1]]

    def bill_at(back: date) -> float:
        return bill[max(bisect.bisect_right(cal, back) - 1, 0)]

    weights = {bk.name: dict.fromkeys(bk.assets, 0.0) for bk in books}
    pending: dict[str, tuple[int, dict[str, float]]] = {}
    for i, d in enumerate(cal):
        for bk in books:
            if bk.name in pending and pending[bk.name][0] == i:
                new = pending.pop(bk.name)[1]
                old = weights[bk.name]
                turn = sum(abs(new.get(t, 0.0) - old.get(t, 0.0)) for t in bk.assets)
                bk.traded += turn
                bk.traded_today = turn
                weights[bk.name] = new
                bk.cost_paid += turn * bk.cost
                bk.cost_today = turn * bk.cost
        if i > 0:
            days = (d - cal[i - 1]).days
            for bk in books:
                w = weights[bk.name]
                tot, bor = 0.0, 0.0
                for t in bk.assets:
                    x = rets[t].get(d)
                    e = (x - rf_t[d]) if x is not None else 0.0
                    wt = w.get(t, 0.0)
                    cc = wt * e
                    if wt < 0:
                        fee = -wt * bk.borrow * days / 365
                        cc -= fee
                        bor += fee
                    bk.contrib[t].append(cc)
                    bk.sign[t].append(float(np.sign(wt)))
                    tot += cc
                bk.borrow_paid += bor
                tot -= bk.cost_today
                bk.cost_d.append(bk.cost_today)
                bk.borrow_d.append(bor)
                bk.traded_d.append(bk.traded_today)
                bk.cost_today = bk.traded_today = 0.0
                bk.days.append(d)
                bk.ret.append(tot)
                bk.gross.append(sum(abs(v) for v in w.values()))
                bk.net.append(sum(w.values()))
        for t in prices:
            x = rets[t].get(d)
            if x is None:
                continue
            if t not in m1:
                m1[t], m2[t] = x, x * x
            else:
                m1[t] = l1.DELTA * m1[t] + (1 - l1.DELTA) * x
                m2[t] = l1.DELTA * m2[t] + (1 - l1.DELTA) * x * x
            nret[t] += 1
        if d in month_end and i + 2 < len(cal):
            for bk in books:
                alive = []
                for t in bk.assets:
                    if first[t] > d - timedelta(days=365) or nret[t] < 60:
                        continue
                    if d not in prices[t]:
                        continue  # no close today (a delisted or not yet started asset)
                    looks = (30, 91, 365) if bk.hop else (365,)
                    sig = 0.0
                    for k in looks:
                        back = d - timedelta(days=k)
                        ex = (prices[t][d] / past(t, back)) / (bill[i] / bill_at(back)) - 1
                        sig += (1.0 if ex > 0 else -1.0) / len(looks)
                    sigma = math.sqrt(max(m2[t] - m1[t] ** 2, 1e-12) * 261)
                    alive.append((t, sig, sigma))
                n = len(alive)
                new = {t: sig * l1.TARGET_VOL / sigma / n for t, sig, sigma in alive}
                if bk.gross1:
                    g = sum(abs(v) for v in new.values())
                    new = {t: v / g for t, v in new.items()} if g > 0 else new
                pending[bk.name] = (i + 2, new)
    return rf_t


# --- helpers ---


def cal_days(a: date, b: date) -> list[date]:
    return [a + timedelta(days=i) for i in range((b - a).days + 1)]


def on_cal(x: dict[date, float], a: date, b: date) -> np.ndarray:
    return np.array([x.get(d, 0.0) for d in cal_days(a, b)])


def mdd(r: np.ndarray) -> float:
    eq = np.cumprod(1 + r)
    return float((1 - eq / np.maximum.accumulate(eq)).max())


def vol_d(r: np.ndarray) -> float:
    return float(r.std(ddof=1) * math.sqrt(365))


def monthly_ex(ex: dict[date, float], rf: dict[date, float]) -> Series:
    acc: dict[Month, list[float]] = defaultdict(lambda: [1.0, 1.0])
    for d, x in ex.items():
        f = rf.get(d, 0.0)
        a = acc[(d.year, d.month)]
        a[0] *= 1 + x + f
        a[1] *= 1 + f
    return {k: a[0] - a[1] for k, a in acc.items()}


def worst_year(s: Series, y0: int, y1: int) -> tuple[float, int]:
    ys = {y: compound(s, months((y, 1), (y, 12))) for y in range(y0, y1 + 1)}
    return min((v, y) for y, v in ys.items() if math.isfinite(v))


def f2(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:.2f}"


def pct(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:+.1%}"


def row(variant: str, kind: str, a: date, b: date, r: np.ndarray, turnover: float) -> str:
    return (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | {kind} | train | {a} | "
        f"{b} | {stats.sharpe(r):.2f} | {np.prod(1 + r) - 1:+.1%} | {mdd(r):.1%} | "
        f"{turnover:.2f} |\n"
    )


def log_once(marker: str, lines: list[str]) -> bool:
    if f"| {IDEA} | {marker} |" in harness.TRIES.read_text():
        return False  # logged by the first run; a rerun only rewrites the tables
    with harness.TRIES.open("a") as f:
        f.writelines(lines)
    return True


def wide_prices(root: Path) -> dict[str, dict[date, float]]:
    return {t: l1.load_prices(root, t) for t in l1.WIDE}


def book_ex(bk: Book) -> dict[date, float]:
    return dict(zip(bk.days, bk.ret, strict=True))


def first_pos(bk: Book) -> date:
    return next(d for d, g in zip(bk.days, bk.gross, strict=True) if g > 0)


# --- Part A ---


class Sleeve:
    """Daily excess returns of a sleeve on its own days, with its gross and net."""

    def __init__(
        self,
        ex: dict[date, float],
        start: date,
        gross: Callable[[date], float],
        net: Callable[[date], float],
    ) -> None:
        self.ex, self.start, self.gross, self.net = ex, start, gross, net

    def sigma(self, end: date) -> float:
        """Std of the trailing 52 complete Monday-Sunday weeks of excess returns, x sqrt 52;
        nan if those weeks do not all lie after the sleeve's start."""
        last_sun = end - timedelta(days=(end.weekday() + 1) % 7)
        mon0 = last_sun - timedelta(days=52 * 7 - 1)
        if mon0 < self.start:
            return math.nan
        wk = np.zeros(52)
        for d in cal_days(mon0, last_sun):
            wk[(d - mon0).days // 7] += self.ex.get(d, 0.0)
        return float(wk.std(ddof=1) * math.sqrt(52))


class Blend:
    def __init__(self) -> None:
        self.ex: dict[date, float] = {}
        self.ctrl: dict[date, float] = {}  # tsmom12 at the same split, rest in bills
        self.a: dict[date, float] = {}
        self.gross: dict[date, float] = {}
        self.net: dict[date, float] = {}
        self.reset_cost: dict[date, float] = {}
        self.reset_traded: dict[date, float] = {}
        self.start = LAST_DAY
        self.held_split = 0  # months the split was kept because a sleeve's vol was 0


def blend(s1: Sleeve, s2: Sleeve, cost: float) -> Blend:
    out = Blend()
    m = (s1.start.year, s1.start.month)
    while True:  # first month with both sleeves' 52 weeks at the previous month end
        prev_end = date(m[0], m[1], 1) - timedelta(days=1)
        if math.isfinite(s1.sigma(prev_end)) and math.isfinite(s2.sigma(prev_end)):
            break
        m = (m[0] + m[1] // 12, m[1] % 12 + 1)
    out.start = date(m[0], m[1], 1)
    v1, v2 = 0.0, 0.0  # sleeve shares of the book (start in cash)
    a = 0.5
    for d in cal_days(out.start, LAST_DAY):
        today_cost = 0.0
        if d.day == 1:
            e = d - timedelta(days=1)
            sg1, sg2 = s1.sigma(e), s2.sigma(e)
            if sg1 > 0 and sg2 > 0:  # else keep the previous split (a sleeve all in cash)
                a = (1 / sg1) / (1 / sg1 + 1 / sg2)
            else:
                out.held_split += 1
            t1, t2 = abs(a - v1), abs(1 - a - v2)
            today_cost = cost * (t1 * s1.gross(d) + t2 * s2.gross(d))
            out.reset_traded[d] = t1 * s1.gross(d) + t2 * s2.gross(d)
            v1, v2 = a, 1 - a
        x1, x2 = s1.ex.get(d, 0.0), s2.ex.get(d, 0.0)
        out.a[d] = v1
        out.gross[d] = v1 * s1.gross(d) + v2 * s2.gross(d)
        out.net[d] = v1 * s1.net(d) + v2 * s2.net(d)
        out.reset_cost[d] = today_cost
        out.ex[d] = v1 * x1 + v2 * x2 - today_cost
        out.ctrl[d] = v1 * x1
        v1, v2 = v1 * (1 + x1), v2 * (1 + x2)
        v1, v2 = v1 / (v1 + v2), v2 / (v1 + v2)
    return out


def tsmom12_sleeve() -> tuple[Sleeve, dict[date, float], dict[date, float], harness.Run]:
    """(sleeve, daily bill, daily gym cost drag, run): `tsmom12` re-scored as survey-5 did."""
    six = c.ctx("six")
    f = c.weekly(c.slots(c.tsmom_signal))
    run = c.go(IDEA, "tsmom12", f, six, "baseline", log=False)  # re-score of a logged config
    free = {k: gym.Costs(0.0, 0.0) for k in gym.COSTS}
    run0 = harness.run(
        IDEA, "tsmom12", f, kind="baseline", period=six.period, panel=six.panel,
        history=six.hist, start=six.start, end=six.end, costs=free, log=False,
    )  # fmt: skip  # cost attribution only: the same config without costs
    days, ylds = ci.bill_yield()
    r, rf = ci.rescored(run, days, ylds)
    r0, _ = ci.rescored(run0, days, ylds)
    dd = run.days[1:]
    ex = {d: float(x - f_) for d, x, f_ in zip(dd, r, rf, strict=True) if d <= LAST_DAY}
    rfd = {d: float(f_) for d, f_ in zip(dd, rf, strict=True) if d <= LAST_DAY}
    drag = {d: float(b - a) for d, a, b in zip(dd, r, r0, strict=True) if d <= LAST_DAY}
    dec_days = [x.time.date() for x in run.decisions]
    dec_expo = [sum(x.weights.values()) for x in run.decisions]

    def gross(d: date) -> float:
        i = bisect.bisect_right(dec_days, d) - 1
        return dec_expo[i] if i >= 0 else 0.0

    start = next(d for d in dd if gross(d) > 0)  # first day invested (cash before)
    return Sleeve(ex, start, gross, gross), rfd, drag, run


def wide_sleeve(bk: Book) -> Sleeve:
    days = bk.days

    def at(xs: list[float]) -> Callable[[date], float]:
        def f(d: date) -> float:
            i = bisect.bisect_right(days, d) - 1
            return xs[i] if i >= 0 else 0.0

        return f

    return Sleeve(book_ex(bk), first_pos(bk), at(bk.gross), at(bk.net))


def part_a(root: Path) -> None:
    rf_day = s5.bill_daily()
    books = [
        Book("wide-LS", l1.WIDE),
        Book("wide-LS-g1", l1.WIDE, gross1=True),
        Book("wide-LS-g1-cost2", l1.WIDE, gross1=True, cost=0.0010, borrow=0.03),
    ]
    rf_t = run_books(wide_prices(root), rf_day, books)
    raw, g1, g1c = books
    s1, rf1, drag, run = tsmom12_sleeve()
    s2, s2c = wide_sleeve(g1), wide_sleeve(g1c)
    bl = blend(s1, s2, l1.COST)
    blc = blend(s1, s2c, 0.0010)
    F = (bl.start, LAST_DAY)

    # daily calendar excess arrays per window
    def arr(x: dict[date, float], w: tuple[date, date]) -> np.ndarray:
        return on_cal(x, *w)

    b_p, t_p = arr(bl.ex, P), arr(s1.ex, P)
    k_eq = vol_d(b_p) / vol_d(t_p)
    eqvol = {d: k_eq * x for d, x in s1.ex.items()}
    ser = {
        "blend-er": bl.ex, "tsmom12": s1.ex, "tsmom12-split-bills (b1)": bl.ctrl,
        f"tsmom12 at the blend's vol, k {k_eq:.2f} (b2)": eqvol, "wide-LS-g1": s2.ex,
        "wide-LS raw (ls-trend-1)": book_ex(raw), "blend-er-cost2": blc.ex,
    }  # fmt: skip
    mon = {n: monthly_ex(x, rf1) for n, x in ser.items()}
    for n, bk in (("wide-LS-g1", g1), ("wide-LS raw (ls-trend-1)", raw)):
        mon[n] = l1.monthly(bk.days, bk.ret, rf_t)
    # Sharpe tests (decides: P)
    test = {}
    for wn, w in (("P", P), ("L", LD)):
        test[wn] = stats.sharpe_diff_boot(
            arr(bl.ex, w), arr(s1.ex, w), draws=DRAWS, mean_block=20, seed=0
        )
    # turnover a year (blend: sleeves at their weights + resets)
    yrs_p = ((P[1] - P[0]).days + 1) / 365.25
    a_p = np.array([bl.a[d] for d in cal_days(*P)])
    g1_traded = dict(zip(g1.days, g1.traded_d, strict=True))
    b_turn = (
        float(a_p.mean()) * run.score.turnover
        + sum((1 - bl.a[d]) * g1_traded.get(d, 0.0) for d in cal_days(*P)) / yrs_p
        + sum(v for d, v in bl.reset_traded.items() if P[0] <= d) / yrs_p
    )
    g1_turn = sum(v for d, v in g1_traded.items() if P[0] <= d <= P[1]) / yrs_p
    rows = [
        row("blend-er@L07", "variant", *P, b_p, b_turn),
        row("blend-er@L", "robustness", *LD, arr(bl.ex, LD), b_turn),
        row("blend-er@F", "robustness", *F, arr(bl.ex, F), b_turn),
        row("blend-er-cost2@L07", "robustness", *P, arr(blc.ex, P), b_turn),
        row("tsmom12-split-bills@L07", "baseline", *P, arr(bl.ctrl, P),
            float(a_p.mean()) * run.score.turnover),
        row("wide-LS-g1@L07", "replication", *P, arr(s2.ex, P), g1_turn),
    ]  # fmt: skip
    logged = log_once("blend-er@L07", rows)

    # ---- report ----
    pa, pl = test["P"], test["L"]
    out = [
        "# ls-trend-2 Part A: `tsmom12` + wide long-short TSMOM at gross <= 1",
        "",
        "Card: `cards/ls-trend-2.md` (committed before any number). One blend, equal risk "
        "between `tsmom12` and wide-LS rescaled to gross 1, split from trailing 52-week "
        "volatility only, reset monthly. Daily calendar excess returns over the 13-week T-bill; "
        "Sharpe a year in the repo's convention (daily, 365). P = 2007-04-01..2025-10-31 "
        f"(decides), L = 2010-02-01..2025-10-31, F = {F[0]}..2025-10-31. Nothing after "
        "2025-10-31 read.",
        "",
        "## 1. The test (a): Sharpe of the blend minus `tsmom12`",
        "",
        "| Window | Blend | `tsmom12` | Difference | Bootstrap p (blend better) | 5%..95% |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for wn, w in (("P (decides)", P), ("L", LD)):
        t = pa if wn.startswith("P") else pl
        out.append(
            f"| {wn} | {f2(stats.sharpe(arr(bl.ex, w)))} | {f2(stats.sharpe(arr(s1.ex, w)))} | "
            f"{t[0]:+.2f} | {t[1]:.4f} | {t[2]:+.2f}..{t[3]:+.2f} |"
        )
    passed = pa[1] < FAMILY_BAR and pa[0] > 0
    out += [
        "",
        f"Paired stationary bootstrap, mean block 20 days, {DRAWS:,} draws, seed 0. Family bar "
        f"p < {FAMILY_BAR:.5f}; project-wide (N {PROJECT_N:,} + this card's rows) p <= "
        f"{0.05 / (PROJECT_N + 2):.1e}. **(a) {'passes' if passed else 'fails'}.**",
        "",
        "## 2. Sharpe, risk, split, gross",
        "",
        "| Series | Sharpe P | Sharpe L | Sharpe F | Vol P | Max DD P | Worst year P |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for n, x in ser.items():
        rp = arr(x, P)
        wy = worst_year(mon[n], 2008, 2024)
        out.append(
            f"| {n} | {f2(stats.sharpe(rp))} | {f2(stats.sharpe(arr(x, LD)))} | "
            f"{f2(stats.sharpe(arr(x, F)))} | {vol_d(rp):.1%} | {mdd(rp):.1%} | "
            f"{wy[0]:+.1%} ({wy[1]}) |"
        )
    gp = np.array([bl.gross[d] for d in cal_days(*P)])
    npn = np.array([bl.net[d] for d in cal_days(*P)])
    out += [
        "",
        f"Split to `tsmom12` in P: mean {a_p.mean():.2f}, min {a_p.min():.2f}, max "
        f"{a_p.max():.2f} (the rest in wide-LS-g1). Combined gross: mean {gp.mean():.2f}, max "
        f"{gp.max():.3f} (card: <= 1); net exposure mean {npn.mean():+.2f}. wide-LS-g1 alone: "
        f"net mean {np.mean([n for d, n in zip(g1.days, g1.net, strict=True) if d >= P[0]]):+.2f}"
        f"; wide-LS raw gross mean {np.mean([x for d, x in zip(raw.days, raw.gross, strict=True) if d >= P[0]]):.2f}.",  # noqa: E501
        "",
        "## 3. Costs a year in P",
        "",
        "| Item | In the sleeve (own capital) | In the blend (at its weights) |",
        "|---|---:|---:|",
    ]

    def per_year(x: dict[date, float], wt: Callable[[date], float]) -> float:
        return sum(v * wt(d) for d, v in x.items() if P[0] <= d <= P[1]) / yrs_p

    one: Callable[[date], float] = lambda d: 1.0  # noqa: E731
    bw: Callable[[date], float] = lambda d: 1 - bl.a.get(d, 0.0)  # noqa: E731
    aw: Callable[[date], float] = lambda d: bl.a.get(d, 0.0)  # noqa: E731
    g1c_ = dict(zip(g1.days, g1.cost_d, strict=True))
    g1b_ = dict(zip(g1.days, g1.borrow_d, strict=True))
    rc_ = {d: c_ for d, c_ in g1c_.items()}
    items = [
        ("wide-LS-g1 trading (5 bps a side)", rc_, bw),
        ("wide-LS-g1 borrow (1% a year on shorts)", g1b_, bw),
        ("`tsmom12` gym costs (with-cost vs no-cost re-score)", drag, aw),
    ]
    tot_b = 0.0
    for lab, x, wt in items:
        tb = per_year(x, wt)
        tot_b += tb
        out.append(f"| {lab} | {per_year(x, one):.2%} | {tb:.2%} |")
    rc = per_year(bl.reset_cost, one)
    tot_b += rc
    out.append(f"| split reset (5 bps a side) | - | {rc:.2%} |")
    out.append(f"| **total** | | **{tot_b:.2%}** |")
    rw = [x for d, x in zip(raw.days, raw.cost_d, strict=True) if P[0] <= d]
    rb = [x for d, x in zip(raw.days, raw.borrow_d, strict=True) if P[0] <= d]
    out += [
        "",
        f"For scale, wide-LS raw (3.7x gross) in P: trading {sum(rw) / yrs_p:.2%}, borrow "
        f"{sum(rb) / yrs_p:.2%} a year. Cost stress (10 bps, 3% borrow): blend Sharpe P "
        f"{f2(stats.sharpe(arr(blc.ex, P)))}.",
        "",
        "## 4. Crash windows (compounded monthly excess)",
        "",
        "| Series | " + " | ".join(CRASH) + " |",
        "|---|" + "---:|" * len(CRASH),
    ]
    for n in ser:
        out.append(
            f"| {n} | "
            + " | ".join(pct(compound(mon[n], months(*w))) for w in CRASH.values())
            + " |"
        )
    cr = {n: [compound(mon[n], months(*w)) for w in CRASH.values()] for n in mon}
    bt, tt = cr["blend-er"], cr["tsmom12"]
    b1, b2 = cr["tsmom12-split-bills (b1)"], cr[next(n for n in mon if n.endswith("(b2)"))]
    surv = [g / r for g, r in zip(cr["wide-LS-g1"], cr["wide-LS raw (ls-trend-1)"], strict=True)]
    rule_b = all(x > y for x, y in zip(bt, tt, strict=True))
    rule_b1 = all(x > y for x, y in zip(bt, b1, strict=True))
    rule_b2 = [x > y for x, y in zip(bt, b2, strict=True)]
    out += [
        "",
        "How much of the crash help survives at <= 1x: wide-LS-g1 / wide-LS raw = "
        + ", ".join(f"{k} {s:.0%}" for k, s in zip(CRASH, surv, strict=True))
        + ". The blend's gain over the dilution control (b1), in points: "
        + ", ".join(f"{k} {100 * (x - y):+.1f}" for k, x, y in zip(CRASH, bt, b1, strict=True))
        + ".",
        "",
        f"- (b) blend above `tsmom12` in all three: **{'yes' if rule_b else 'no'}** "
        "(a risk preference, not an edge).",
        f"- (b1) blend above the dilution control in all three: {'yes' if rule_b1 else 'no'}.",
        "- (b2) blend above `tsmom12` at equal vol: "
        + ", ".join(f"{k} {'yes' if v else 'no'}" for k, v in zip(CRASH, rule_b2, strict=True))
        + ".",
        "",
        "## 5. Correlation of monthly excess returns in L",
        "",
    ]
    rf_m = s5.bill_monthly(rf_day)
    funds = {t: s5.fund_monthly(root, t, rf_m) for t in s5.TREND}
    refs = {"TC": s5.composite(funds), "SPY": s5.spy_monthly(rf_m), "tsmom12": mon["tsmom12"],
            "wide-LS-g1": mon["wide-LS-g1"]}  # fmt: skip
    out += ["| Series | " + " | ".join(refs) + " |", "|---|" + "---:|" * len(refs)]
    for n in ("blend-er", "tsmom12", "wide-LS-g1"):
        cs = [corr(cut(mon[n], s5.L), cut(s, s5.L)) for s in refs.values()]
        out.append(f"| {n} | " + " | ".join(f"{f2(r)} ({k})" for r, k in cs) + " |")
    verdict = (
        "edge at the family bar"
        if passed
        else ("a risk choice, not an edge" if rule_b else "neither an edge nor crash insurance")
    )
    out += ["", f"## Verdict (card's wording): **{verdict}**.", ""]
    out.append(f"Months the split was kept (a sleeve's trailing vol 0): {bl.held_split}.")
    out.append(f"Rows logged this run: {'6' if logged else '0 (already logged)'}.")
    text = "\n".join(out) + "\n"
    (harness.RESEARCH / "results" / "ls-trend-2-blend.md").write_text(text)
    print(text)


# --- Part B ---


def gspc_prices() -> dict[str, dict[date, float]]:
    out = {}
    with (harness.RESEARCH / "data" / "bars" / "GSPC.csv").open() as f:
        for r in csv.DictReader(f):
            d = date.fromisoformat(r["date"])
            if date(1960, 1, 4) <= d <= LAST_DAY:
                out[d] = float(r["close"])
    return {"GSPC": out}


def part_b(root: Path) -> None:
    rf_day = s5.bill_daily()
    books = [
        Book("wide-LS", l1.WIDE),
        Book("hop-wide-LS", l1.WIDE, hop=True),
        Book("wide-LS-g1", l1.WIDE, gross1=True),
        Book("hop-wide-LS-g1", l1.WIDE, hop=True, gross1=True),
    ]
    rf_t = run_books(wide_prices(root), rf_day, books)
    gb = [Book("gspc-12m", ["GSPC"]), Book("gspc-hop", ["GSPC"], hop=True)]
    rf_g = run_books(gspc_prices(), rf_day, gb)
    mon = {bk.name: l1.monthly(bk.days, bk.ret, rf_t) for bk in books}
    gmon = {bk.name: l1.monthly(bk.days, bk.ret, rf_g) for bk in gb}
    L07 = (date(2007, 4, 1), LAST_DAY)

    def turn(bk: Book, w: tuple[date, date]) -> float:
        yrs = ((w[1] - w[0]).days + 1) / 365.25
        return sum(x for d, x in zip(bk.days, bk.traded_d, strict=True) if w[0] <= d <= w[1]) / yrs

    g0 = (date(1961, 1, 1), LAST_DAY)
    rows = [row(f"{bk.name}@live-L", "replication", *LD, on_cal(book_ex(bk), *LD), turn(bk, LD))
            for bk in books if bk.hop]  # fmt: skip
    rows += [row(f"{bk.name}@1961", "replication", *g0, on_cal(book_ex(bk), *g0), turn(bk, g0))
             for bk in gb]  # fmt: skip
    logged = log_once("hop-wide-LS@live-L", rows)

    rf_m = s5.bill_monthly(rf_day)
    funds = {t: s5.fund_monthly(root, t, rf_m) for t in s5.TREND}
    tc = s5.composite(funds)
    _, s5_ours = s5.ours()
    vol10 = {n: l1.vol_m(cut(s, s5.L07)) for n, s in mon.items()}
    out = [
        "# ls-trend-2 Part B: the 1/3/12-month signal on the wide long-short book",
        "",
        "Card: `cards/ls-trend-2.md` Part B (committed before any number). Descriptive, no "
        "pick. Signal = mean of the signs of the 1-, 3- and 12-month excess returns "
        "(Hurst-Ooi-Pedersen 2017), otherwise ls-trend-1's wide-LS unchanged (40% / sigma / N, "
        "monthly, 5 bps, 1% borrow). Raw = leverage at the bill; g1 = rescaled to gross 1. "
        "Monthly excess returns over the T-bill; nothing after 2025-10 read.",
        "",
        "## 1. Sharpe, cost, correlation",
        "",
        "| Cell | Sharpe L | Sharpe L07 | Vol L07 | Mean gross L | Turnover/yr L | "
        "Costs/yr L | Borrow/yr L | Corr. TC (L) | Corr. tsmom12 (L) | Corr. wide-LS (L) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    yl = ((LD[1] - LD[0]).days + 1) / 365.25
    for bk in books:
        s = mon[bk.name]
        ins = [i for i, d in enumerate(bk.days) if LD[0] <= d]
        out.append(
            f"| {bk.name} | {f2(stats.sharpe(on_cal(book_ex(bk), *LD)))} | "
            f"{f2(stats.sharpe(on_cal(book_ex(bk), *L07)))} | {vol10[bk.name]:.1%} | "
            f"{np.mean([bk.gross[i] for i in ins]):.2f} | {turn(bk, LD):.1f} | "
            f"{sum(bk.cost_d[i] for i in ins) / yl:.2%} | "
            f"{sum(bk.borrow_d[i] for i in ins) / yl:.2%} | "
            f"{f2(corr(cut(s, s5.L), cut(tc, s5.L))[0])} | "
            f"{f2(corr(cut(s, s5.L), cut(s5_ours['tsmom12'], s5.L))[0])} | "
            f"{f2(corr(cut(s, s5.L), cut(mon['wide-LS'], s5.L))[0])} |"
        )
    out += [
        "",
        "(Daily Sharpe, calendar days, 365, on excess returns; the repo's row convention. "
        "ls-trend-1's monthly Sharpe for wide-LS was 0.15 in L.)",
        "",
        "## 2. Fast crashes (and the slow ones, for the cost of speed)",
        "",
        "Compounded monthly excess; at 10% vol = x 10% / the cell's monthly vol in L07 "
        "(display scaling, ex post).",
        "",
        "| Window | "
        + " | ".join(bk.name for bk in books)
        + " | "
        + " | ".join(f"{bk.name} at 10%" for bk in books if not bk.gross1)
        + " | TC |",
        "|---|" + "---:|" * (len(books) + 3),
    ]
    for wn, w in FAST.items():
        raw = {bk.name: compound(mon[bk.name], months(*w)) for bk in books}
        sc = [raw[bk.name] * 0.10 / vol10[bk.name] for bk in books if not bk.gross1]
        out.append(
            f"| {wn} | "
            + " | ".join(pct(x) for x in raw.values())
            + " | "
            + " | ".join(pct(x) for x in sc)
            + f" | {pct(compound(tc, months(*w)))} |"
        )
    w20 = FAST["2020-02..03"]
    d20 = (compound(mon["hop-wide-LS"], months(*w20)) * 0.10 / vol10["hop-wide-LS"]
           - compound(mon["wide-LS"], months(*w20)) * 0.10 / vol10["wide-LS"])  # fmt: skip
    sl = {bk.name: stats.sharpe(on_cal(book_ex(bk), *LD)) for bk in books}
    out += [
        "",
        f"Card's reading: 2020-02..03 at 10% vol, hop minus 12-month = {100 * d20:+.1f} points "
        f"-> {'helps' if d20 > 0.02 else 'does not help'} in the fast crash (rule: > 2 points); "
        f"Sharpe L {f2(sl['hop-wide-LS'])} vs {f2(sl['wide-LS'])} -> "
        f"{'costs' if sl['hop-wide-LS'] < sl['wide-LS'] else 'does not cost'}.",
        "",
        "## 3. Where the 2020-02..03 result came from (hop-wide-LS, additive daily P&L)",
        "",
        "| Class | Long legs | Short legs | Total |",
        "|---|---:|---:|---:|",
    ]
    hb = books[1]
    a20, b20 = date(2020, 2, 1), date(2020, 3, 31)
    ii = [i for i, d in enumerate(hb.days) if a20 <= d <= b20]
    for k, ts in l1.CLASSES.items():
        lo = sum(hb.contrib[t][i] for t in ts for i in ii if hb.sign[t][i] > 0)
        sh = sum(hb.contrib[t][i] for t in ts for i in ii if hb.sign[t][i] < 0)
        out.append(f"| {k} | {pct(lo)} | {pct(sh)} | {pct(lo + sh)} |")
    out += [
        "",
        "## 4. 1987 on the S&P 500 alone (price index, no dividends; long-short, 40% / sigma)",
        "",
        "| Cell | 1987-10 | 1987-10..12 | Cell's 1987-09 | Sharpe 1961..2025-10 | "
        "Position held 1987-10-02..10-30 (x capital) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for bk in gb:
        s = gmon[bk.name]
        i = bisect.bisect_left(bk.days, date(1987, 10, 2))
        out.append(
            f"| {bk.name} | {pct(compound(s, months((1987, 10), (1987, 10))))} | "
            f"{pct(compound(s, months((1987, 10), (1987, 12))))} | "
            f"{pct(compound(s, months((1987, 9), (1987, 9))))} | "
            f"{f2(stats.sharpe(on_cal(book_ex(bk), *g0)))} | {bk.net[i]:+.2f} |"
        )
    gp = gspc_prices()["GSPC"]

    def lvl(d: date) -> float:
        return gp[max(x for x in gp if x <= d)]

    out += [
        "",
        f"S&P 500 price index: 1987-09 {lvl(date(1987, 9, 30)) / lvl(date(1987, 8, 31)) - 1:+.1%},"
        f" 1987-07..09 {lvl(date(1987, 9, 30)) / lvl(date(1987, 6, 30)) - 1:+.1%}, 1987-10 "
        f"{lvl(date(1987, 10, 31)) / lvl(date(1987, 9, 30)) - 1:+.1%}. The cells size one market "
        "at 40% / sigma, so a calm September means about 2-3x leverage; divide by 4 for a 10% "
        "volatility reading.",
    ]
    out += ["", f"Rows logged this run: {len(rows) if logged else 0}."]
    text = "\n".join(out) + "\n"
    (harness.RESEARCH / "results" / "ls-trend-2-hop.md").write_text(text)
    print(text)


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    part = sys.argv[2] if len(sys.argv) > 2 else "A"
    if part == "A":
        part_a(root)
    elif part == "B":
        part_b(root)
    else:
        raise SystemExit("part must be A or B")


if __name__ == "__main__":
    main()
