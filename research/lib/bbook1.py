"""breadth-book-1: `tsmom12` unchanged on wider, mechanically chosen universes (card
`research/cards/breadth-book-1.md`).

    uv run python -I research/lib/bbook1.py prep    # bars into research/data, lists (no returns)
    uv run python -I research/lib/bbook1.py run     # the one logged run (tries.md rows)

`prep` converts the cached raw Yahoo responses of `ls-trend-1` and the Coin Metrics snapshot
into research/data/{bars,adj}/ (git-ignored) and prints the eligible ETFs, their order and the
coin list. `run` backtests every set of the card, logs one row each and writes
`research/results/breadth-book-1.md`. Train only: no bar after 2025-11-10 is read.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import bbook1_core as core
import common as c
import harness
import macro
import numpy as np
from harness import DATA, ERAS, STRESS, TRAIN_END, TRAIN_LAST_BAR, Panel, View, Weights

from grimstrade import gym, report
from grimstrade.data import CRYPTO, ETF, UNIVERSE, Bar
from grimstrade.strategies import ts_momentum

IDEA = "breadth-book-1"
CM_SNAPSHOT = "2026-11-13"
LS_YAHOO = Path("downloads") / "ls-trend-1" / "yahoo"
LONG = (date(2008, 1, 2), TRAIN_END)
COIN = (date(2020, 1, 1), TRAIN_END)
RESULT = harness.RESEARCH / "results" / f"{IDEA}.md"


def derived() -> Path:
    p = macro.cache_root() / "derived" / IDEA
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_bars(path: Path, bars: Sequence[Bar]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for b in bars:
            w.writerow([b.date.isoformat(), b.open, b.high, b.low, b.close, b.volume])


def yahoo_bars(body: bytes) -> tuple[list[Bar], list[Bar]]:
    """(raw, dividend-adjusted) bars from a Yahoo chart response, as `fetch.yahoo_all` builds
    them (exchange-local dates, rows with a missing or non-positive value dropped)."""
    res = json.loads(body)["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    offset = int(res["meta"].get("gmtoffset", 0))
    raw: dict[date, Bar] = {}
    adjusted: dict[date, Bar] = {}
    for i, ts in enumerate(res["timestamp"]):
        vals = [q["open"][i], q["high"][i], q["low"][i], q["close"][i], adj[i]]
        if any(v is None or v <= 0 for v in vals):
            continue
        d = datetime.fromtimestamp(ts + offset, tz=UTC).date()
        if d > TRAIN_LAST_BAR:
            continue
        o, h, lo, cl, a = (float(v) for v in vals)
        vol = float(q["volume"][i] or 0)
        raw[d] = Bar(d, o, h, lo, cl, vol)
        k = a / cl
        adjusted[d] = Bar(d, o * k, h * k, lo * k, a, vol)
    return [raw[d] for d in sorted(raw)], [adjusted[d] for d in sorted(adjusted)]


def coin_sym(cm_id: str) -> str:
    return cm_id.upper() if cm_id in ("btc", "eth") else f"{cm_id.upper()}-CM"


def register(syms: Sequence[str]) -> None:
    for s in syms:
        UNIVERSE.setdefault(s, CRYPTO if s.endswith("-CM") else ETF)


# ---------------------------------------------------------------- prep (no returns)


def prep_etfs() -> dict[str, float]:
    root = macro.cache_root() / LS_YAHOO
    for s in core.POOL:
        if (DATA / "bars" / f"{s}.csv").exists():
            continue
        p = root / f"{s}.json"
        if not p.exists():
            print(f"{s}: no cached response")
            continue
        raw, adjusted = yahoo_bars(p.read_bytes())
        write_bars(DATA / "bars" / f"{s}.csv", raw)
        write_bars(DATA / "adj" / f"{s}.csv", adjusted)
    return pool_volumes()


def raw_bars(s: str) -> list[core.RawBar]:
    path = DATA / "bars" / f"{s}.csv"
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return [(date.fromisoformat(r["date"]), float(r["close"]), float(r["volume"]))
                for r in csv.DictReader(f)]  # fmt: skip


def pool_volumes() -> dict[str, float]:
    return core.eligible_pool({s: raw_bars(s) for s in core.POOL})


def cm_rows(folder: Path) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    for p in sorted(folder.glob("page-*.json")):
        rows += json.loads(p.read_text())["data"]
    return rows


def prep_coins(k: int = 10) -> list[str]:
    """The coin list from 2019 data only (cached), then bars for the chosen coins."""
    cache = derived() / "cm2019.json"
    root = macro.cache_root() / "coinmetrics" / "full" / CM_SNAPSHOT / "assets"
    if not cache.exists():
        px: dict[str, dict[str, float]] = {}
        cap: dict[str, dict[str, float]] = {}
        for folder in sorted(root.iterdir()):
            p, m = {}, {}
            for r in cm_rows(folder):
                d = str(r["time"])[:10]
                if not "2019-01-01" <= d <= "2019-12-31":
                    continue
                if r.get("PriceUSD") is not None:
                    p[d] = float(str(r["PriceUSD"]))
                mc = r.get("CapMrktEstUSD") or r.get("CapMrktCurUSD")
                if mc is not None:
                    m[d] = float(mc)
            if len(p) >= 365:
                px[folder.name], cap[folder.name] = p, m
        cache.write_text(json.dumps({"px": px, "cap": cap}))
    blob = json.loads(cache.read_text())

    def dated(x: Mapping[str, Mapping[str, float]]) -> dict[str, dict[date, float]]:
        return {a: {date.fromisoformat(d): v for d, v in s.items()} for a, s in x.items()}

    coins = core.coin_list(dated(blob["px"]), dated(blob["cap"]), k)
    for a in coins:
        if a in ("btc", "eth"):
            continue
        series = sorted(
            (date.fromisoformat(str(r["time"])[:10]), float(str(r["PriceUSD"])))
            for r in cm_rows(root / a)
            if r.get("PriceUSD") is not None
        )
        series = [(d, p) for d, p in series if d <= TRAIN_LAST_BAR and p > 0]
        bars = [Bar(d, p0, max(p0, p), min(p0, p), p, 0.0)
                for (_, p0), (d, p) in zip(series, series[1:], strict=False)]  # fmt: skip
        write_bars(DATA / "bars" / f"{coin_sym(a)}.csv", bars)
    return [coin_sym(a) for a in coins]


def lists() -> tuple[dict[str, float], list[str], list[str]]:
    dv = pool_volumes()
    coins_path = derived() / "coins.json"
    if not coins_path.exists():
        coins_path.write_text(json.dumps(prep_coins()))
    coins: list[str] = json.loads(coins_path.read_text())
    return dv, core.round_robin(dv), coins


def prep() -> None:
    prep_etfs()
    dv, order, coins = lists()
    print("eligible ETFs (2006-H2 median dollar volume, USD m):")
    for s in core.POOL:
        v = core.dollar_volume_2006(raw_bars(s))
        tag = "in" if s in dv else "out"
        print(f"  {s:5s} {core.class_of(s):12s} {tag:3s} {'-' if v is None else f'{v / 1e6:.1f}'}")
    print("order (round-robin):", " ".join(order))
    print("order (volume):", " ".join(core.by_volume(dv)))
    print("coins (2019-12-31 caps):", " ".join(coins))


# ---------------------------------------------------------------- rules


def tsmom12() -> harness.ResearchStrategy:
    """The project's `tsmom12`, as on the bar (`baselines.twins()`)."""
    return c.weekly(c.slots(c.tsmom_signal))


def _ewma_vol(simple: np.ndarray, per_year: int, com: float = 60, tail: int = 1500) -> float:
    """`grimstrade.signals.ewma_vol` in numpy (weights past `tail` returns are < 1e-10)."""
    if len(simple) < 2:
        return math.nan
    x = simple[-tail:][::-1]
    d = com / (com + 1)
    w = (1 - d) * d ** np.arange(len(x))
    mean = (w * x).sum() / w.sum()
    return float(math.sqrt((w * (x - mean) ** 2).sum() / w.sum() * per_year))


def live_form(view: View) -> Weights:
    """The live runner's `ts_momentum.decide` on a View: daily, slot min(1, 40% / vol) / N with
    N = assets with 12 months of history."""
    sig: dict[str, float] = {}
    for s in view.syms:
        d, cl = view.dates(s), view.close(s)
        if len(cl) == 0:
            continue
        target = int(d[-1]) - 365
        if d[0] > target:
            continue
        i = int(np.searchsorted(d, target, side="right")) - 1
        sig[s] = cl[-1] / cl[i] - 1
    out: Weights = {}
    for s, r in sig.items():
        if r <= 0:
            continue
        cl = view.close(s)
        vol = _ewma_vol(cl[1:] / cl[:-1] - 1, 365 if UNIVERSE[s] == CRYPTO else 252)
        if vol and math.isfinite(vol):
            out[s] = min(1.0, 0.40 / vol) / len(sig)
    return out


def check_live_form(hist: Mapping[str, Sequence[Bar]], days: Sequence[date]) -> None:
    """`live_form` gives the live `ts_momentum.decide` weights on sample days."""
    panel = Panel(hist)
    for d in days:
        t = harness.decide_time(d)
        fast = harness.clean(live_form(panel.view(t)))
        seen = {s: [b for b in bars if harness.data.close_time(UNIVERSE[s], b.date) <= t]
                for s, bars in hist.items()}  # fmt: skip
        ref = harness.clean(ts_momentum.decide({s: b for s, b in seen.items() if b})[0])
        if set(fast) != set(ref) or any(abs(fast[s] - ref[s]) > 1e-7 for s in fast):
            raise AssertionError(f"{d}: live form {fast} != ts_momentum {ref}")


# ---------------------------------------------------------------- scoring


class Book:
    def __init__(self, name: str, syms: list[str], window: tuple[date, date], kind: str,
                 rule: str = "tsmom12", log: bool = True) -> None:  # fmt: skip
        self.name, self.syms, self.window, self.kind, self.rule = name, syms, window, kind, rule
        register(syms)
        hist = harness.load_history("train", True, syms)
        assert all(b.date <= TRAIN_LAST_BAR for bars in hist.values() for b in bars)
        self.hist = hist
        self.panel = Panel(hist)
        strat = tsmom12() if rule == "tsmom12" else live_form
        variant = f"{name}@{window[0].year}" + ("" if rule == "tsmom12" else "/ts_momentum")
        self.run = harness.run(IDEA, variant, strat, kind=kind, panel=self.panel, history=hist,
                               start=window[0], end=window[1], log=log)  # fmt: skip
        res = gym.simulate(self.run.decisions, hist, rates=harness.bill_rates())
        self.bills = report.score(name, res)
        self.ex = excess_calendar(res, self.run.days)

    @property
    def gross(self) -> np.ndarray:
        return self.run.rets


def excess_calendar(res: gym.Result, days: Sequence[date]) -> np.ndarray:
    """Daily return above the bill on every calendar day of `days` (0 on days without a bar),
    aligned with `Run.rets` (whose first return ends on days[1])."""
    eq = [e for _, e in res.equity]
    rets = [b / a - 1 for a, b in zip([res.start_cash, *eq], eq, strict=False)]
    ex = {d: r - f for (d, _), r, f in zip(res.equity, rets, res.cash_growth, strict=True)}
    return np.array([ex.get(d, 0.0) for d in days[1:]])


def years(days: Sequence[date]) -> np.ndarray:
    return np.array([d.year for d in days[1:]])


def worst_year(b: Book) -> tuple[int, float]:
    y = years(b.run.days)
    out = {int(k): float(np.prod(1 + b.gross[y == k]) - 1) for k in np.unique(y)}
    k = min(out, key=lambda x: out[x])
    return k, out[k]


def window_ret(b: Book, a: date, z: date) -> float | None:
    if a < b.run.days[0] or z > b.run.days[-1]:
        return None
    r = b.run.rets_between(a, z)
    return float(np.prod(1 + r) - 1)


def era_sharpes(b: Book) -> dict[str, float]:
    d = np.array([x.toordinal() for x in b.run.days[1:]])
    out = {}
    for name, a, z in ERAS:
        m = (d >= a.toordinal()) & (d <= z.toordinal())
        if m.sum() > 300:
            out[name] = core.sharpe(b.ex[m])
    return out


def weekly_closes(hist: Mapping[str, Sequence[Bar]], syms: Sequence[str],
                  fridays: Sequence[date]) -> np.ndarray:  # fmt: skip
    out = np.full((len(fridays), len(syms)), np.nan)
    for j, s in enumerate(syms):
        ds = [b.date for b in hist[s]]
        cl = [b.close for b in hist[s]]
        k = 0
        for i, f in enumerate(fridays):
            while k < len(ds) and ds[k] <= f:
                k += 1
            if k and (f - ds[k - 1]).days <= 7:
                out[i, j] = cl[k - 1]
    return out


def neff(b: Book) -> tuple[float, float, float]:
    """Mean over month ends in the window of (N_eff of the eligible set, mean pairwise
    correlation, N_eff of the assets held at that month end)."""
    a, z = b.window
    first = a - timedelta(days=7 * 110)
    fr = [first + timedelta(days=(4 - first.weekday()) % 7 + 7 * i) for i in range(2000)]
    fr = [f for f in fr if f <= z]
    lr = np.diff(np.log(weekly_closes(b.hist, b.syms, fr)), axis=0)
    fr = fr[1:]
    held_at = {dc.time.date(): dc.weights for dc in b.run.decisions}
    pe, pr, ph = [], [], []
    for i, f in enumerate(fr):
        if f < a or (i + 1 < len(fr) and fr[i + 1].month == f.month):
            continue  # month ends only: the last Friday of each month in the window
        e, rho = core.neff_at(lr, i, range(len(b.syms)))
        w = held_at.get(f, {})
        cols = [j for j, s in enumerate(b.syms) if w.get(s, 0) > 0]
        h = core.neff_at(lr, i, cols)[0] if cols else math.nan
        pe.append(e)
        pr.append(rho)
        ph.append(h)

    def m(x: list[float]) -> float:
        v = [y for y in x if math.isfinite(y)]
        return float(np.mean(v)) if v else math.nan

    return m(pe), m(pr), m(ph)


# ---------------------------------------------------------------- the run


def f2(x: float | None) -> str:
    return "-" if x is None or not math.isfinite(x) else f"{x:+.2f}" if x < 0 else f"{x:.2f}"


def pct(x: float | None) -> str:
    return "-" if x is None else f"{x:+.1%}"


def table(books: Sequence[Book], ref: Book, label: str) -> list[str]:
    out = [f"### {label}: window {ref.window[0]} .. {ref.window[1]}, compared with `{ref.name}`",
           "",
           "| Set | N | Sharpe above bills | Edge (SE, z, p) | Gym Sharpe | Gym edge | CAGR | "
           "Max DD | Worst year | Turnover/yr | Exposure | N_eff (rho) | N_eff held | Eras ahead |",
           "|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|---:|---|"]  # fmt: skip
    ref_era = era_sharpes(ref)
    for b in books:
        d, se, z, p = core.paired(b.ex, ref.ex)
        dg = core.sharpe(b.gross) - core.sharpe(ref.gross)
        e, rho, h = neff(b)
        era = era_sharpes(b)
        ahead = sum(era[k] > ref_era[k] for k in era if k in ref_era)
        wy, wr = worst_year(b)
        edge = "-" if b is ref else f"{d:+.3f} ({se:.3f}, {z:+.2f}, {p:.3f})"
        out.append(
            f"| `{b.name}` | {len(b.syms)} | {b.bills.sharpe:.2f} | {edge} | "
            f"{core.sharpe(b.gross):.2f} | {'-' if b is ref else f'{dg:+.3f}'} | "
            f"{pct(cagr(b))} | {b.run.score.max_drawdown:.1%} | "
            f"{wy} {wr:+.1%} | {b.run.score.turnover:.2f} | {b.run.exposure:.2f} | "
            f"{e:.1f} ({rho:.2f}) | {h:.1f} | {ahead}/{len([k for k in era if k in ref_era])} |"
        )
    out += ["", "Return inside the stress windows (gym convention):", "",
            "| Set | " + " | ".join(n for n, _, _ in STRESS) + " |",
            "|---|" + "---:|" * len(STRESS)]  # fmt: skip
    for b in books:
        out.append(f"| `{b.name}` | " + " | ".join(pct(window_ret(b, a, z)) for _, a, z in STRESS)
                   + " |")  # fmt: skip
    out += ["", "Sharpe above bills per era:", "",
            "| Set | " + " | ".join(ref_era) + " |", "|---|" + "---:|" * len(ref_era)]  # fmt: skip
    for b in books:
        era = era_sharpes(b)
        out.append(f"| `{b.name}` | " + " | ".join(f2(era.get(k)) for k in ref_era) + " |")
    return out + [""]


def cagr(b: Book) -> float:
    span = (b.run.days[-1] - b.run.days[0]).days + 1
    return float(b.run.equity[-1] / b.run.equity[0]) ** (365 / span) - 1


def run() -> None:
    if any(IDEA in line for line in harness.TRIES.read_text().splitlines()):
        raise SystemExit(f"{IDEA} already logged: the card allows one real run")
    dv, order, coins = lists()
    six = core.SIX
    etf_all = len(order)
    lines = [f"# breadth-book-1 results ({datetime.now(UTC):%Y-%m-%d %H:%M} UTC)", "",
             "Card `research/cards/breadth-book-1.md`. Train only (no bar after 2025-11-10). "
             "Sharpe above bills: cash earns the 13-week bill, Sharpe of the return above it. "
             "Gym Sharpe: cash earns 0 (the `tries.md` rows). Edge: paired stationary bootstrap "
             "(block 20 days, 2,000 draws), one-sided p. N_eff: participation ratio of the "
             "trailing 104-week correlation matrix, mean over month ends.", "",
             f"Eligible ETFs ({etf_all}), round-robin order: {' '.join(order)}", "",
             f"Coin list (2019-12-31 caps): {' '.join(coins)}", ""]  # fmt: skip

    # the long window: ETFs (and the six) from 2008
    b_six = Book("six", six, LONG, "baseline")
    b_four = Book("four", core.LIVE_ETFS, LONG, "baseline")
    sizes = [n for n in (6, 12, 20) if n < etf_all] + [etf_all]
    e_books = [Book(f"E-{'all' if n == etf_all else n}", core.nested(order, n), LONG, "variant")
               for n in sizes]  # fmt: skip
    l_sizes = [n for n in (12, 20) if n < etf_all + 2] + [etf_all + 2]
    l_books = [Book(f"L-{'all' if n == etf_all + 2 else n}", core.nested(order, n, six), LONG,
                    "variant") for n in l_sizes]  # fmt: skip
    l_all = l_books[-1]
    harness.check_against_gym(tsmom12(), l_all.hist, [date(2009, 3, 6), date(2018, 6, 1)])
    check_live_form(l_all.hist, [date(2009, 3, 6), date(2021, 6, 1)])
    six_v = Book("six-live-form", six, LONG, "robustness", "live")
    l_all_v = Book("L-all-live-form", l_all.syms, LONG, "robustness", "live")
    lines += table([b_six, *l_books, six_v, l_all_v], b_six, "Candidate books: the six plus ETFs")
    lines += table([b_four, *e_books], b_four, "Clean ETF breadth: ETF-only sets")
    lines += table([b_six, b_four, *e_books], b_six, "ETF-only sets against the six")
    vol_order = core.by_volume(dv)
    if set(core.nested(vol_order, etf_all + 2, six)) != set(l_all.syms):
        lines += ["`L-all-vol` differs from `L-all`: not expected (all eligible are in both)."]
    else:
        lines += ["`L-all-vol` holds the same assets as `L-all` (all eligible ETFs are in both "
                  "orders), so it was not run (card).", ""]  # fmt: skip

    # the coin window: from 2020
    coin_syms = ["BTC", "ETH"] + [s for s in coins if s not in ("BTC", "ETH")]
    c_books = [Book(f"C-{k}", coin_syms[:k], COIN, "baseline" if k == 2 else "variant")
               for k in (2, 5, 10)]  # fmt: skip
    b_six20 = Book("six", six, COIN, "baseline")
    lc = Book("LC-all", l_all.syms + coin_syms[2:10], COIN, "variant")
    lc_v = Book("LC-all-live-form", lc.syms, COIN, "robustness", "live")
    six20_v = Book("six-live-form", six, COIN, "robustness", "live")
    l_all20 = Book("L-all", l_all.syms, COIN, "robustness")
    lines += table(c_books, c_books[0], "Clean coin breadth: coin-only sets")
    lines += table([b_six20, l_all20, lc, six20_v, lc_v], b_six20, "Candidate books from 2020")
    dead = [s for s in coin_syms[2:10] if lc.hist[s][-1].date < TRAIN_LAST_BAR - timedelta(7)]
    lines += [f"Coins whose price stops before the end of the window: {dead or 'none'}.", ""]
    RESULT.write_text("\n".join(lines).rstrip() + "\n")
    print("\n".join(lines))


def smoke() -> None:
    """Plumbing check before the logged run: two short windows, nothing logged or printed but
    "ok" (the output tables are built and discarded)."""
    _, order, coins = lists()
    w1, w2 = (date(2008, 1, 2), date(2008, 3, 31)), (date(2020, 1, 1), date(2020, 3, 31))
    a = Book("six", core.SIX, w1, "baseline", log=False)
    b = Book("L-all", core.nested(order, 99, core.SIX), w1, "variant", "live", log=False)
    table([a, b], a, "smoke")
    d = Book("C-10", ["BTC", "ETH", *coins[2:10]], w2, "variant", log=False)
    table([d], d, "smoke")
    check_live_form(b.hist, [date(2009, 3, 6)])
    print("ok")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prep":
        prep()
    elif cmd == "smoke":
        smoke()
    elif cmd == "run":
        run()
    else:
        raise SystemExit(__doc__)
