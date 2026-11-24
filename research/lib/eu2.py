"""eu-2: `tsmom12` for a euro-area retail account (card cards/eu-2.md).

    uv run --with numpy python research/lib/eu2.py fees    # amendment 1: fixed fees, book, band
    uv run --with numpy python research/lib/eu2.py hedge   # amendment 2: EUR-hedged US equity

Needs the CSVs from `eu1_data.py build` (and `eu2_data.py build` for `hedge`). Every run is a row
in tries.md (idea `eu-2`); a run whose equity file already exists under the git-ignored
research/data/runs/eu-2/ is re-scored without a new row. Train period only.

Fixed per-order fees: the gym is not changed. `fixed_fees` wraps the gym's order step in-process
and, after each batch of fills, debits fee / book of the equity for every ETF fill (a constant
book of that size), plus a yearly fee / book on the first order step of each calendar year.
"""

from __future__ import annotations

import csv
import sys
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date, datetime

import common as c
import eu1
import harness
import numpy as np
from harness import TRAIN_END, Run

from grimstrade import gym, report
from grimstrade.data import CRYPTO, ETF, UNIVERSE

IDEA = "eu-2"
W_START = eu1.W_START
SLIP = 0.0005  # ETF half-spread + slippage a side, as eu-1's `retail`
CURRENCY_YEARLY = 2.50  # DEGIRO connectivity fee, Xetra, EUR per calendar year


@dataclass(frozen=True)
class Schedule:
    name: str
    per_order: float  # EUR per ETF order
    per_year: float  # EUR per calendar year


SCHEDULES = [
    Schedule("slip", 0.0, 0.0),
    Schedule("dg1", 1.0, CURRENCY_YEARLY),
    Schedule("tr2", 2.0, 0.0),
    Schedule("dg3", 3.0, CURRENCY_YEARLY),
]
SIZES = [5_000, 25_000, 100_000]
BANDS = [0.01, 0.05]
LOSS_MAX = 0.10  # card: fee loss <= 0.10 Sharpe
GAP_TOL = 0.15  # card: tsmom12 - EW gap within 0.15 of the gap at `slip`

COSTS = {ETF: gym.Costs(fee=0.0, slip=SLIP), CRYPTO: gym.COSTS[CRYPTO]}
RETAIL = eu1.COSTS["retail"]


@dataclass
class FeeState:
    per_order: float  # share of equity per ETF order (fee / book)
    per_year: float  # share of equity per calendar year
    orders: int = 0
    paid: float = 0.0  # sum of debits as shares of equity at the time
    years: set[int] = field(default_factory=set)


@contextmanager
def fixed_fees(st: FeeState) -> Iterator[None]:
    orig = gym._execute

    def wrapped(
        t: datetime, syms: list[str], pending: dict[str, float], res: gym.Result,
        price: Mapping[str, float], costs: Mapping[str, gym.Costs], band: float,
    ) -> None:  # fmt: skip
        eq = res.cash + sum(q * price.get(s, 0.0) for s, q in res.positions.items())
        n0 = len(res.fills)
        orig(t, syms, pending, res, price, costs, band)
        n_etf = sum(1 for f in res.fills[n0:] if UNIVERSE[f.symbol] == ETF)
        share = n_etf * st.per_order
        if st.per_year and t.year not in st.years and eq > 0:
            st.years.add(t.year)
            share += st.per_year
        st.orders += n_etf
        st.paid += share
        res.cash -= share * eq

    gym._execute = wrapped  # type: ignore[assignment]
    try:
        yield
    finally:
        gym._execute = orig  # type: ignore[assignment]


@dataclass
class Out:
    run: Run
    orders_yr: float  # ETF orders per year
    fees_yr: float  # fixed fees per year, share of the book


_decs: dict[tuple[int, tuple[str, ...]], list[gym.Decision]] = {}


def simulate(
    variant: str, strategy: c.ResearchStrategy, syms: Sequence[str], costs: Mapping[str, gym.Costs],
    band: float, st: FeeState, kind: str, start: date = W_START,
) -> Out:  # fmt: skip
    hist, pan = eu1.panel_for(syms)
    if c.DRY:  # plumbing check: last two years, nothing logged
        start = date(2023, 11, 1)
    key = (id(strategy), tuple(syms))
    if key not in _decs:
        _decs[key] = harness.decisions(strategy, pan, start, TRAIN_END)
    decs = _decs[key]
    with fixed_fees(st):
        res = gym.simulate(decs, hist, costs=costs, band=band)
    sc = report.score(f"{IDEA}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    run = Run(
        IDEA, variant, "train", sc, days, equity,
        float(np.mean([sum(d.weights.values()) for d in decs])), decs,
    )  # fmt: skip
    path = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    if c.DRY:
        print("dry", variant, flush=True)
    elif not path.exists():
        harness._log(run, kind, start, TRAIN_END)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date", "equity"])
            w.writerows((d.isoformat(), repr(float(e))) for d, e in zip(days, equity))  # noqa: B905
        print("logged", variant, flush=True)
    else:
        print("re-scored", variant, flush=True)
    years = (days[-1] - days[0]).days / 365
    return Out(run, st.orders / years, st.paid / years)


def plain_check(syms: Sequence[str]) -> None:
    """With fee 0 the wrapper must give the plain gym's equity exactly."""
    hist, pan = eu1.panel_for(syms)
    decs = harness.decisions(eu1.TSMOM, pan, W_START, TRAIN_END)
    a = gym.simulate(decs, hist, costs=COSTS, band=0.05)
    with fixed_fees(FeeState(0.0, 0.0)):
        b = gym.simulate(decs, hist, costs=COSTS, band=0.05)
    if a.equity != b.equity:
        raise AssertionError("fee-0 wrapper differs from the plain gym")
    print("plain check ok", flush=True)


def band_tag(band: float) -> str:
    return f"b{band * 100:g}"


def fee_runs(book: str, syms: list[str]) -> dict[tuple[str, int, float, str], Out]:
    """(schedule, size, band, strategy) -> run. `slip` rows have size 0."""
    out: dict[tuple[str, int, float, str], Out] = {}
    strategies = [("tsmom12", eu1.TSMOM, "robustness"), ("equal-weight", eu1.EW, "baseline")]
    for band in BANDS:
        for name, strat, kind in strategies:
            v = f"{name}@{book}/slip-{band_tag(band)}"
            out[("slip", 0, band, name)] = simulate(
                v, strat, syms, COSTS, band, FeeState(0, 0), kind
            )
    for sch in SCHEDULES[1:]:
        for size in SIZES:
            for band in BANDS:
                for name, strat, kind in strategies:
                    v = f"{name}@{book}/{sch.name}-{size // 1000}k-{band_tag(band)}"
                    st = FeeState(sch.per_order / size, sch.per_year / size)
                    out[(sch.name, size, band, name)] = simulate(
                        v, strat, syms, COSTS, band, st, kind
                    )
    for size in SIZES:  # robustness: band 2.5% at dg3, tsmom12 only
        sch = SCHEDULES[3]
        v = f"tsmom12@{book}/dg3-{size // 1000}k-b2.5"
        st = FeeState(sch.per_order / size, sch.per_year / size)
        out[("dg3", size, 0.025, "tsmom12")] = simulate(
            v, eu1.TSMOM, syms, COSTS, 0.025, st, "robustness"
        )
    return out


def sharpe(o: Out) -> float:
    return c.describe(o.run)["sharpe"]


def break_even(losses: list[float]) -> str:
    """Smallest book with loss <= LOSS_MAX, linear in 1/size between tested sizes."""
    if losses[0] <= LOSS_MAX:
        return "<= 5k"
    for (b0, l0), (b1, l1) in zip(zip(SIZES, losses), zip(SIZES[1:], losses[1:])):  # noqa: B905
        if l1 <= LOSS_MAX < l0:
            x0, x1 = 1 / b0, 1 / b1
            x = x0 + (LOSS_MAX - l0) * (x1 - x0) / (l1 - l0)
            return f"~{1 / x / 1000:.0f}k"
    return "> 100k"


def fees_report() -> None:
    plain_check(eu1.EUW)
    out = ["# eu-2 results, amendment 1: fixed per-order fees, book size, rebalance band", ""]
    out += [
        "Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices, "
        "EUR. Sharpe on calendar days, zero risk-free rate. ETF slippage 0.05% a side in every "
        "schedule; coins 0.25% + 0.05%. Fixed fees on a constant book (fee / book of equity per "
        "ETF order). Schedules: `slip` no fee; `dg1` DEGIRO core selection EUR 1/order + EUR "
        "2.50/yr; `tr2` Trade Republic Direct Price EUR 2/order; `dg3` DEGIRO other ETFs EUR "
        "3/order + EUR 2.50/yr. `b1`/`b5` = rebalance band 1% (house) / 5% (mitigation). Fee loss "
        "= tsmom12's Sharpe at `slip` (same band) minus under the schedule. Card: `cards/eu-2.md`.",
        "",
    ]
    verdict_lines = []
    for book, syms in (("eu6", eu1.EU6), ("euw", eu1.EUW)):
        r = fee_runs(book, syms)
        out += [f"## {book}", ""]
        out += [
            "| Schedule | Book | Band | tsmom12 Sharpe | EW Sharpe | Gap (gap at slip) | "
            "Fee loss | tsmom12 CAGR | Max DD | ETF orders/yr | Fixed fees/yr | Worth it |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
        for band in BANDS:
            t0, e0 = r[("slip", 0, band, "tsmom12")], r[("slip", 0, band, "equal-weight")]
            gap0 = sharpe(t0) - sharpe(e0)
            d0 = c.describe(t0.run)
            out.append(
                f"| slip | any | {band:.0%} | {sharpe(t0):.2f} | {sharpe(e0):.2f} | {gap0:+.2f} | "
                f"- | {d0['cagr']:+.1%} | {d0['mdd']:.1%} | {t0.orders_yr:.0f} (EW "
                f"{e0.orders_yr:.0f}) | - | - |"
            )
        for sch in SCHEDULES[1:]:
            for band in BANDS:
                gap0 = sharpe(r[("slip", 0, band, "tsmom12")]) - sharpe(
                    r[("slip", 0, band, "equal-weight")]
                )
                losses = []
                for size in SIZES:
                    t, e = (
                        r[(sch.name, size, band, "tsmom12")],
                        r[(sch.name, size, band, "equal-weight")],
                    )
                    loss = sharpe(r[("slip", 0, band, "tsmom12")]) - sharpe(t)
                    losses.append(loss)
                    gap = sharpe(t) - sharpe(e)
                    ok = loss <= LOSS_MAX and abs(gap - gap0) <= GAP_TOL
                    d = c.describe(t.run)
                    out.append(
                        f"| {sch.name} | {size // 1000}k | {band:.0%} | {sharpe(t):.2f} | "
                        f"{sharpe(e):.2f} | {gap:+.2f} ({gap0:+.2f}) | {loss:.2f} | "
                        f"{d['cagr']:+.1%} | {d['mdd']:.1%} | {t.orders_yr:.0f} (EW "
                        f"{e.orders_yr:.0f}) | {t.fees_yr:.2%} | {'yes' if ok else '**no**'} |"
                    )
                verdict_lines.append(
                    f"| {book} | {sch.name} | {band:.0%} | {break_even(losses)} | "
                    + " | ".join(f"{x:.2f}" for x in losses)
                    + " |"
                )
        out.append("")
        out += ["Band 2.5% (robustness), `dg3`, tsmom12:", ""]
        out += ["| Book size | Sharpe | Fee loss vs slip b1 | ETF orders/yr | Fixed fees/yr |"]
        out += ["|---:|---:|---:|---:|---:|"]
        s1 = sharpe(r[("slip", 0, 0.01, "tsmom12")])
        for size in SIZES:
            o = r[("dg3", size, 0.025, "tsmom12")]
            out.append(
                f"| {size // 1000}k | {sharpe(o):.2f} | {s1 - sharpe(o):.2f} | {o.orders_yr:.0f} | "
                f"{o.fees_yr:.2%} |"
            )
        out.append("")
        # Band test (card): at dg3 the 5% band at least halves the fee loss at every size, and at
        # slip moves Sharpe by <= 0.05 and max DD by <= 2 points.
        s_b1, s_b5 = r[("slip", 0, 0.01, "tsmom12")], r[("slip", 0, 0.05, "tsmom12")]
        halves = []
        for size in SIZES:
            l1 = sharpe(s_b1) - sharpe(r[("dg3", size, 0.01, "tsmom12")])
            l5 = sharpe(s_b5) - sharpe(r[("dg3", size, 0.05, "tsmom12")])
            halves.append(l5 <= l1 / 2)
        dsh = sharpe(s_b5) - sharpe(s_b1)
        ddd = c.describe(s_b5.run)["mdd"] - c.describe(s_b1.run)["mdd"]
        works = all(halves) and abs(dsh) <= 0.05 and abs(ddd) <= 0.02
        out += [
            f"Band test ({book}): 5% band halves the `dg3` fee loss at 5k/25k/100k: "
            f"{', '.join('yes' if h else 'no' for h in halves)}; at `slip` it moves Sharpe by "
            f"{dsh:+.2f} and max DD by {ddd * 100:+.1f} points. **The band "
            f"{'works' if works else 'does not pass'}.**",
            "",
        ]
        out += ["Crash windows, tsmom12 (total return inside each):", ""]
        crash_runs = []
        for key in [("slip", 0, 0.01), ("slip", 0, 0.05), ("dg3", 5000, 0.01), ("dg3", 5000, 0.05)]:
            crash_runs.append(r[(*key, "tsmom12")].run)
        out += [eu1.crash_table(crash_runs), ""]
    out += ["## Break-even book size (fee loss <= 0.10 Sharpe)", ""]
    out += ["| Book | Schedule | Band | Break-even | Loss 5k | Loss 25k | Loss 100k |"]
    out += ["|---|---|---:|---|---:|---:|---:|", *verdict_lines, ""]
    c.write_result(f"{IDEA}-fees", "\n".join(out))


# --- amendment 2: EUR-hedged US equity ---

IUSE = "IUSEL"  # iShares S&P 500 EUR Hedged (Acc), London EUR line (research/eu-2.md)
XAD1 = "XAD1"  # Xtrackers Physical Gold EUR Hedged ETC, Xetra
for _s in (IUSE, XAD1):
    UNIVERSE.setdefault(_s, ETF)
EUW_H = [IUSE if s == "SXR8" else s for s in eu1.EUW]
EUW_HH = [XAD1 if s == "4GLD" else s for s in EUW_H]
EU6_H = [IUSE if s == "SXR8" else s for s in eu1.EU6]
DRAG = 0.06  # eu-1's currency part of euw's gap (usw-eur -0.10 vs usw -0.04)


def go2(
    variant: str, strategy: c.ResearchStrategy, syms: Sequence[str], kind: str
) -> Run:  # the eu-1 path (`retail` percentage costs, house band), logged under eu-2
    hist, pan = eu1.panel_for(syms)
    saved = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    log = not saved.exists() and not c.DRY
    start = date(2023, 11, 1) if c.DRY else W_START
    run = harness.run(
        IDEA, variant, strategy, kind=kind, period="train", panel=pan, history=hist,
        start=start, end=TRAIN_END, costs=RETAIL, log=log,
    )  # fmt: skip
    print(f"{'logged' if log else 're-scored'} {variant}", flush=True)
    return run


def hedge_pair(name: str, syms: list[str]) -> tuple[Run, Run]:
    return (
        go2(f"tsmom12@{name}", eu1.TSMOM, syms, "robustness"),
        go2(f"equal-weight@{name}", eu1.EW, syms, "baseline"),
    )


def gap(p: tuple[Run, Run]) -> float:
    return c.describe(p[0])["sharpe"] - c.describe(p[1])["sharpe"]


def hedge_report() -> None:
    out = ["# eu-2 results, amendment 2: EUR-hedged US equity", ""]
    out += [
        "Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices; "
        "EUR books at percentage costs (`retail`: ETFs 0.10% + 0.05%), US books at the gym's, "
        "coins 0.25% + 0.05%; house band 1%. Sharpe on calendar days, zero risk-free rate. "
        "`IUSEL` = IUSE, iShares S&P 500 EUR Hedged (London EUR line); `XAD1` = Xtrackers "
        "Physical Gold EUR Hedged. Rows from eu-1 are re-scored from its saved runs (no new "
        "rows). Card: `cards/eu-2.md`.",
        "",
    ]
    books = {k: b for k, b in [
        ("usw", eu1.Book("usw", eu1.USW, "gym")),
        ("usw-eur", eu1.Book("usw-eur", eu1.USW_EUR, "gym")),
        ("euw", eu1.Book("euw", eu1.EUW, "retail")),
        ("us6", eu1.Book("us6", eu1.US6, "gym")),
        ("eu6", eu1.Book("eu6", eu1.EU6, "retail")),
    ]}  # fmt: skip
    old = {k: eu1.pair(b, W_START) for k, b in books.items()}
    new = {
        "euw-h": hedge_pair("euw-h", EUW_H),
        "euw-hh": hedge_pair("euw-hh", EUW_HH),
        "eu6-h": hedge_pair("eu6-h", EU6_H),
    }
    singles = {}
    for sym in (IUSE, XAD1):
        singles[sym] = (
            go2(f"tsmom12@{sym}", eu1.TSMOM, [sym], "robustness"),
            go2(f"hold@{sym}", c.weekly(c.hold(sym)), [sym], "baseline"),
        )
    for sym, costs in (("SPY", "gym"), ("SXR8", "retail"), ("4GLD", "retail"), ("GLD", "gym")):
        singles[sym] = (
            eu1.go(f"tsmom12@{sym}", eu1.TSMOM, [sym], costs, "robustness", W_START),
            eu1.go(f"hold@{sym}", c.weekly(c.hold(sym)), [sym], costs, "baseline", W_START),
        )
    allp = {**old, **new}

    out += ["## 1. Coin-free asset classes: does hedging remove the currency drag?", ""]
    keys = ["usw", "usw-eur", "euw", "euw-h", "euw-hh"]
    out += [c.table([r for k in keys for r in allp[k]]), ""]
    out += ["| Book | tsmom12 - EW Sharpe | Change vs euw |", "|---|---:|---:|"]
    for k in keys:
        out.append(f"| {k} | {gap(allp[k]):+.2f} | {gap(allp[k]) - gap(allp['euw']):+.2f} |")
    out.append("")
    verdicts = {}
    for k in ("euw-h", "euw-hh"):
        d = gap(allp[k]) - gap(allp["euw"])
        verdicts[k] = "removes" if d >= DRAG else "in part" if d >= DRAG / 2 else "no"
        out.append(
            f"- `{k}`: gap change {d:+.2f} (card: >= +{DRAG:.2f} removes, >= +{DRAG / 2:.2f} in "
            f"part): **{verdicts[k]}**"
        )
    out.append("")

    out += ["## 2. The live six with a hedged S&P 500 slot", ""]
    out += [c.table([r for k in ["us6", "eu6", "eu6-h"] for r in allp[k]]), ""]

    out += ["## 3. eu-1's character tests on the hedged books", ""]
    for name, eu, us in [("eu6-h vs us6", "eu6-h", "us6"), ("euw-h vs usw", "euw-h", "usw")]:
        lines, v = eu1.criteria(allp[eu], allp[us])
        out += [f"### {name}: **{v}**", "", *lines, ""]

    out += ["## 4. Single slots: the filter against holding", ""]
    srun = [r for s in (IUSE, "SXR8", "SPY", XAD1, "4GLD", "GLD") for r in singles[s]]
    out += [c.table(srun, eras=False), ""]
    out += ["| Slot | tsmom12 - hold Sharpe |", "|---|---:|"]
    for s in (IUSE, "SXR8", "SPY", XAD1, "4GLD", "GLD"):
        out.append(f"| {s} | {gap(singles[s]):+.2f} |")
    us_like = abs(gap(singles[IUSE]) - gap(singles["SPY"])) <= 0.05
    out += [
        "",
        f"US slot behaves as in USD (IUSE's gap within 0.05 of SPY's): "
        f"**{'yes' if us_like else 'no'}** ({gap(singles[IUSE]):+.2f} vs "
        f"{gap(singles['SPY']):+.2f}; SXR8 {gap(singles['SXR8']):+.2f}).",
        "",
    ]
    out += ["Crash windows (total return inside each):", ""]
    crash = [*allp["euw"], *allp["euw-h"], *allp["euw-hh"], *srun]
    out += [eu1.crash_table(crash), ""]
    out += ["## Verdicts", ""] + [f"- `{k}`: currency drag {v}" for k, v in verdicts.items()]
    out.append(f"- US slot as in USD: {'yes' if us_like else 'no'}")
    c.write_result(f"{IDEA}-hedge", "\n".join(out))


if __name__ == "__main__":
    {"fees": fees_report, "hedge": hedge_report}[sys.argv[1]]()
