"""deep-1, Part A: the failure atlas (research/deep-1.md). No backtest is run here.

    uv run --with numpy python research/lib/deep1_atlas.py

Reads the series `deep1_models.py` saved and the equity curves earlier runs saved, cuts them as
the card says, and writes research/results/deep-1-atlas.md.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import date, timedelta

import deep1_models as dm
import harness
import numpy as np
import stats
from harness import ERAS, STRESS

SINCE = date(2003, 1, 1)
ERA5 = [e for e in ERAS if e[1].year >= 1994]
SAVED = {
    "rl-1": ["ppo-lin", "ppo-mlp", "ppo-mlp-dd", "ppo-mlp-px", "es-lin"],
    "rl-2": ["res-lin", "res-mlp", "res-pool", "res-mlp-chain"],
    "ideas-1": ["ath-and", "bbwp-and", "srsi-and", "gap-and", "oil-and", "y10chg-and",
                "fng-buyfear", "fng-sellgreed"],
}  # fmt: skip
REBOUND = 182
STATES = ("off", "mixed", "on")


@dataclass
class Atlas:
    days: np.ndarray  # ordinals, n + 1; return k belongs to day days[k + 1]
    syms: list[str]
    assets: np.ndarray  # n x m close-to-close asset returns
    rets: dict[str, np.ndarray]  # model -> n daily returns (NaN before it starts)
    w: dict[str, np.ndarray]  # model -> n x m target weights (models with positions)
    family: dict[str, str]

    def idx(self, d: date) -> int:
        """Index of the first return on or after day `d` (clipped)."""
        return int(np.clip(d.toordinal() - int(self.days[0]) - 1, 0, len(self.days) - 1))

    def cut(self, name: str, a: date, b: date) -> np.ndarray:
        """Returns of days a..b inclusive (NaN-free only if the model ran then)."""
        return self.rets[name][self.idx(a) : self.idx(b) + 1]

    def day(self, k: int) -> date:
        return date.fromordinal(int(self.days[k + 1]))


def load() -> Atlas:
    u = dm.c.ctx("six")
    base = dm.load("six", "tsmom12")
    n = len(base.rets)
    rets: dict[str, np.ndarray] = {}
    w: dict[str, np.ndarray] = {}
    fam: dict[str, str] = {}
    for m in dm.models_for("six"):
        s = dm.load("six", m.name)
        assert len(s.rets) == n and s.syms == base.syms
        rets[m.name], w[m.name], fam[m.name] = s.rets, s.w, m.family
    for m in dm.models_for("SPY"):
        s = dm.load("SPY", m.name)
        assert len(s.rets) == n
        full = np.zeros((n, len(base.syms)))
        full[:, base.syms.index("SPY")] = s.w[:, 0]
        rets[m.name], w[m.name], fam[m.name] = s.rets, full, "timing (SPY only)"
    for run, names in SAVED.items():
        for name in names:
            r = np.full(n, np.nan)
            with (dm.OUT / "saved" / run / f"{name}.train.csv").open() as f:
                rows = [(date.fromisoformat(x["date"]), float(x["equity"])) for x in
                        csv.DictReader(f)]  # fmt: skip
            off = rows[0][0].toordinal() - int(base.days[0])
            eq = np.array([e for _, e in rows])
            k = min(len(eq) - 1, n - off)
            r[off : off + k] = eq[1 : k + 1] / eq[:k] - 1
            rets[name], fam[name] = r, run
    return Atlas(base.days, base.syms, dm.asset_returns(u, base.days), rets, w, fam)


# --- small statistics on slices that may hold NaN ---


def ok(r: np.ndarray, need: int = 250) -> bool:
    return len(r) >= need and not np.isnan(r).any() and r.std() > 0


def sh(r: np.ndarray, need: int = 250) -> float:
    return stats.sharpe(r) if ok(r, need) else math.nan


def tot(r: np.ndarray) -> float:
    return float(np.prod(1 + r) - 1) if len(r) > 5 and not np.isnan(r).any() else math.nan


def f2(x: float, spec: str = "+.2f") -> str:
    return "-" if math.isnan(x) else format(x, spec)


def pc(x: float) -> str:
    return "-" if math.isnan(x) else f"{x * 100:+.0f}"


def weekly(r: np.ndarray) -> np.ndarray:
    """Compounded returns of consecutive 7-day blocks (NaN if a block has a NaN)."""
    k = len(r) // 7
    return np.prod(1 + r[: k * 7].reshape(k, 7), axis=1) - 1


def corr(a: np.ndarray, b: np.ndarray, need: int = 26) -> float:
    m = ~(np.isnan(a) | np.isnan(b))
    if m.sum() < need or a[m].std() == 0 or b[m].std() == 0:
        return math.nan
    return float(np.corrcoef(a[m], b[m])[0, 1])


def bold(text: str, on: bool) -> str:
    return f"**{text}**" if on else text


# --- cuts ---


@dataclass
class Episode:
    peak: int  # return index of the first day after the high-water mark
    trough: int  # return index of the lowest day
    end: int  # return index of the recovery day (or the last day)
    depth: float
    recovered: bool


def episodes(r: np.ndarray, top: int) -> list[Episode]:
    """Drawdown episodes (high-water mark to the next new high) of a NaN-free series, deepest
    first. Indices are into `r`."""
    eq = np.concatenate([[1.0], np.cumprod(1 + r)])
    out: list[Episode] = []
    hi, start, k = eq[0], None, 1
    low = lowk = 0.0
    while k < len(eq):
        if eq[k] >= hi:
            if start is not None:
                out.append(Episode(start, int(lowk) - 1, k - 1, 1 - low / hi, True))
                start = None
            hi = eq[k]
        else:
            if start is None:
                start, low, lowk = k - 1, eq[k], k
            if eq[k] < low:
                low, lowk = eq[k], k
        k += 1
    if start is not None:
        out.append(Episode(start, int(lowk) - 1, len(r) - 1, 1 - low / hi, False))
    return sorted(out, key=lambda e: -e.depth)[:top]


def contributions(a: Atlas, name: str) -> np.ndarray:
    """n x m: yesterday's target weight times the asset's close-to-close return."""
    w = a.w[name]
    prev = np.vstack([np.zeros((1, w.shape[1])), w[:-1]])
    return np.where(np.isnan(a.rets[name])[:, None], 0.0, prev * a.assets)


def trend_state(a: Atlas) -> np.ndarray:
    """0 off, 1 mixed, 2 on, per return day: `tsmom12`'s breadth at its decision in force."""
    b = a.w["tsmom12"].sum(axis=1)
    prev = np.concatenate([[0.0], b[:-1]])
    return np.where(prev <= 1 / 3 + 1e-9, 0, np.where(prev >= 2 / 3 - 1e-9, 2, 1))


def vol_state(a: Atlas) -> tuple[np.ndarray, tuple[float, float]]:
    """0 calm, 1 middle, 2 wild (-1 before 60 days exist): the equal-weight book's realised
    volatility over the 60 days to yesterday, in thirds of its whole distribution."""
    r = a.rets["equal-weight"]
    v = np.full(len(r), np.nan)
    for k in range(60, len(r)):
        v[k] = r[k - 60 : k].std() * math.sqrt(365)
    lo, hi = np.nanquantile(v, [1 / 3, 2 / 3])
    st = np.where(np.isnan(v), -1, np.where(v <= lo, 0, np.where(v <= hi, 1, 2)))
    return st, (float(lo), float(hi))


def names_in_order(a: Atlas) -> list[str]:
    fams = ["twin", "benchmark", "run1", "ml", "macro", "timing (SPY only)", "rl-1", "rl-2",
            "ideas-1"]  # fmt: skip
    out = ["tsmom12"]
    for f in fams:
        out += [n for n in a.rets if a.family[n] == f and n != "tsmom12"]
    return out


def section(title: str, note: str, head: str, rows: list[str]) -> list[str]:
    cols = head.count("|") - 1
    return [f"## {title}", "", note, "", head, "|---|" + "---:|" * (cols - 1), *rows, ""]


def main() -> None:
    a = load()
    names = names_in_order(a)
    ts = a.rets["tsmom12"]
    n = len(ts)
    last = a.day(n - 1)
    out = ["# deep-1, Part A: the failure atlas", ""]
    out += [
        "Card: `deep-1.md`. Six live assets, train period, total-return prices, gym costs. "
        "Sharpe on calendar days. Families: twin and benchmark (protocol), run1 (the "
        "literature cards), ml (run 2), macro (macro-1), timing (the two SPY-only cards), rl-1 "
        "and rl-2 (ensembles, from 2000-01-07), ideas-1 (the YouTube rules). The last three "
        "families are read from saved equity curves and have no positions. Nothing here was "
        "selected or tuned; every row is a configuration already in `tries.md`. **Bold** = "
        "ahead of `tsmom12` on the same days.",
        "",
    ]

    # 1. eras
    rows = []
    wins = [("all", date(1994, 1, 1), last), ("2003-25", SINCE, last)] + ERA5
    for nm in names:
        row = f"| {nm} | {a.family[nm]} |"
        for _, lo, hi in wins:
            x, y = a.cut(nm, lo, hi), a.cut("tsmom12", lo, hi)
            m = ~np.isnan(x)
            if nm != "tsmom12" and 0 < m.sum() < len(x):
                x, y = x[m], y[m]  # a model that starts late: its own span, twin on the same
            s = sh(x)
            row += f" {bold(f2(s, '.2f'), nm != 'tsmom12' and s > sh(y))} |"
        x = a.rets[nm]
        m = ~np.isnan(x)
        row += f" {f2(stats.cagr(x[m]) * 100, '+.1f')} | {stats.max_drawdown(x[m]) * 100:.0f} |"
        rows.append(row)
    head = "| Model | Family |" + "".join(f" {w[0]} |" for w in wins) + " Growth %/yr | Worst % |"
    out += section(
        "1. Sharpe by era",
        "`all` is the model's own span (rl from 2000, `absorption` from 2002; the fear-and-greed "
        "rules are `tsmom12` until their data starts in 2018). Growth and worst loss are over "
        "that span too.",
        head, rows,
    )  # fmt: skip

    # 2. trend state and volatility state
    tstate = trend_state(a)
    vstate, (vlo, vhi) = vol_state(a)
    share_t = [float((tstate == k).mean()) for k in range(3)]
    share_v = [float((vstate == k).sum() / (vstate >= 0).sum()) for k in range(3)]
    rows = []
    for nm in names:
        x = a.rets[nm]
        row = f"| {nm} |"
        for st in (tstate, vstate):
            for k in range(3):
                m = (st == k) & ~np.isnan(x)
                y = ts[m]
                mean = x[m].mean() * 365 if m.sum() > 100 else math.nan
                row += f" {bold(pc(mean), nm != 'tsmom12' and mean > y.mean() * 365)} |"
        if nm in a.w:
            ex = a.w[nm].sum(axis=1)
            prev = np.concatenate([[0.0], ex[:-1]])
            row += "".join(
                f" {prev[(tstate == k) & ~np.isnan(x)].mean() * 100:.0f} |" for k in range(3)
            )
        else:
            row += " - | - | - |"
        rows.append(row)
    head = (
        "| Model | trend off | mixed | on | calm | middle | wild | invested % when off | "
        "when mixed | when on |"
    )
    out += section(
        "2. Return by trend state and by volatility state (% a year, simple average)",
        f"Trend state: the share of eligible assets `tsmom12` holds (off: a third or less, "
        f"{share_t[0]:.0%} of days; mixed {share_t[1]:.0%}; on: two thirds or more, "
        f"{share_t[2]:.0%}). Volatility state: the equal-weight book's 60-day volatility to "
        f"yesterday, in thirds (cut-offs {vlo:.0%} and {vhi:.0%} a year; "
        f"{share_v[0]:.0%} / {share_v[1]:.0%} / {share_v[2]:.0%} of days). The last three "
        "columns are the model's average share of the book invested in each trend state.",
        head, rows,
    )  # fmt: skip

    # 2b. what the slots `tsmom12` leaves empty earn, by trend state
    groups = {"stocks": ["SPY", "QQQ"], "bonds and gold": ["TLT", "GLD"], "coins": ["BTC", "ETH"]}
    w_ts, w_ew = a.w["tsmom12"], a.w["equal-weight"]
    lag = lambda w: np.vstack([np.zeros((1, w.shape[1])), w[:-1]])  # noqa: E731
    held, empty = lag(w_ts), lag(np.clip(w_ew - w_ts, 0, None))
    rows = []
    for k, st in enumerate(STATES):
        m = tstate == k
        yrs = m.sum() / 365
        row = f"| {st} | {m.mean():.0%} |"
        for wgt in (held, empty):
            c_k = (wgt[m] * a.assets[m]).sum() / yrs * 100
            per = c_k / (wgt[m].sum(axis=1).mean() * 100) * 100 if wgt[m].sum() > 0 else math.nan
            row += f" {wgt[m].sum(axis=1).mean() * 100:.0f} | {c_k:+.1f} | {f2(per, '+.0f')} |"
        for g in groups.values():
            j = [a.syms.index(x) for x in g]
            wg = empty[m][:, j]
            per = (wg * a.assets[m][:, j]).sum() / yrs / wg.sum(axis=1).mean() if wg.sum() else \
                math.nan  # fmt: skip
            row += f" {f2(per * 100, '+.0f')} |"
        eras = ", ".join(
            f"{nm} {(m[a.idx(lo) : a.idx(hi) + 1]).sum() / max(m.sum(), 1):.0%}"
            for nm, lo, hi in ERA5
        )
        rows.append(row + f" {eras} |")
    head = ("| Trend state | Days | Held: share of book % | points a year | per unit held, %/yr | "
            "Empty: share of book % | points a year | per unit, %/yr | Empty stocks, per unit | "
            "Empty bonds and gold | Empty coins | Where the days are |")  # fmt: skip
    out += section(
        "2b. What the slots `tsmom12` leaves empty would have earned, by trend state",
        "`Held` is what `tsmom12` holds, `empty` the slots it keeps in cash (equal weight minus "
        "`tsmom12`). `Per unit` divides the points by the average share of the book, so it reads "
        "as the yearly return of those assets while they were in that group. Before costs. This "
        "is the gap between equal weight and `tsmom12`, taken apart; it is a description found "
        "after looking, not a test.",
        head, rows,
    )  # fmt: skip

    # 3. stress windows and the rebounds after them
    rows, rows2 = [], []
    for nm in names:
        row, row2 = f"| {nm} |", f"| {nm} |"
        for _, lo, hi in STRESS:
            x, y = tot(a.cut(nm, lo, hi)), tot(a.cut("tsmom12", lo, hi))
            row += f" {bold(pc(x), nm != 'tsmom12' and x > y)} |"
            lo2, hi2 = hi + timedelta(days=1), hi + timedelta(days=REBOUND)
            x, y = tot(a.cut(nm, lo2, hi2)), tot(a.cut("tsmom12", lo2, hi2))
            row2 += f" {bold(pc(x), nm != 'tsmom12' and x > y)} |"
        rows.append(row)
        rows2.append(row2)
    head = "| Model |" + "".join(f" {s[0]} |" for s in STRESS)
    out += section("3a. Total return inside each stress window (%)",
                   "The protocol's seven windows, peak to trough of the named sell-off.",
                   head, rows)  # fmt: skip
    out += section(f"3b. Total return in the {REBOUND} days after each stress window (%)",
                   "The rebound: where a rule that stepped out has to get back in.",
                   head, rows2)  # fmt: skip

    # 6. tsmom12's ten deepest drawdown episodes
    eps = episodes(ts, 10)
    eps.sort(key=lambda e: e.peak)
    con = contributions(a, "tsmom12")
    rows = []
    for j, e in enumerate(eps, 1):
        c_as = con[e.peak : e.trough + 1].sum(axis=0)
        drivers = ", ".join(
            f"{a.syms[i]} {c_as[i] * 100:+.0f}" for i in np.argsort(c_as)[:3] if c_as[i] < -0.005
        )
        rec = str(a.day(e.end)) if e.recovered else "not yet"
        rows.append(
            f"| E{j} | {a.day(e.peak - 1) if e.peak else a.day(0)} | {a.day(e.trough)} | {rec} | "
            f"{e.depth * 100:.0f} | {e.trough - e.peak + 1} | {e.end - e.trough} | {drivers} |"
        )
    head = ("| Episode | Peak | Trough | New high | Depth % | Days down | Days back | "
            "Assets that cost most (points) |")  # fmt: skip
    out += section("4a. `tsmom12`'s ten deepest drawdown episodes",
                   "High-water mark to the next new high, in date order. Asset points: weight "
                   "times the asset's return, summed from peak to trough.", head, rows)  # fmt: skip
    rows = []
    for nm in names:
        row = f"| {nm} |"
        for e in eps:
            x, y = tot(a.rets[nm][e.peak : e.trough + 1]), tot(ts[e.peak : e.trough + 1])
            hi = min(e.trough + REBOUND, n - 1)
            x2, y2 = tot(a.rets[nm][e.trough + 1 : hi + 1]), tot(ts[e.trough + 1 : hi + 1])
            row += (f" {bold(pc(x), nm != 'tsmom12' and x > y)} / "
                    f"{bold(pc(x2), nm != 'tsmom12' and x2 > y2)} |")  # fmt: skip
        rows.append(row)
    head = "| Model |" + "".join(f" E{j} |" for j in range(1, len(eps) + 1))
    out += section(
        "4b. Every model inside those episodes (% from peak to trough / % in the 182 days after "
        "the trough)", "The same dates for every model: `tsmom12`'s peak and trough.", head, rows,
    )  # fmt: skip

    # 7. correlation with tsmom12, weekly
    wk = {nm: weekly(a.rets[nm]) for nm in names}
    wt = wk["tsmom12"]
    in_ep = np.zeros(n, dtype=bool)
    for e in eps:
        in_ep[e.peak : e.trough + 1] = True
    wk_ep = in_ep[: len(wt) * 7].reshape(len(wt), 7).mean(axis=1) > 0.5
    lose = wt < 0
    rows = []
    for nm in names:
        x = wk[nm]
        m = lose & ~np.isnan(x)
        cap = x[m].mean() / wt[m].mean() if m.sum() > 26 else math.nan
        m2 = ~lose & ~np.isnan(x)
        upc = x[m2].mean() / wt[m2].mean() if m2.sum() > 26 else math.nan
        rows.append(
            f"| {nm} | {f2(corr(x, wt), '.2f')} | {f2(corr(x[lose], wt[lose]), '.2f')} | "
            f"{f2(corr(x[wk_ep], wt[wk_ep]), '.2f')} | {f2(x[m].mean() * 100, '+.2f')} | "
            f"{f2(cap, '.2f')} | {f2(upc, '.2f')} | {f2(upc - cap, '+.2f')} |"
        )
    head = ("| Model | Corr., all weeks | in weeks `tsmom12` lost | inside its ten episodes | "
            "Avg week when `tsmom12` lost, % | Share of its losing weeks' loss taken | "
            "Share of its other weeks' gain taken | Gain share minus loss share |")  # fmt: skip
    out += section(
        "5. How each model moves with `tsmom12` (weekly returns)",
        f"`tsmom12` lost money in {lose.mean():.0%} of weeks. A good complement has a low "
        "correlation in those weeks, takes a small share of the loss and a large share of the "
        "gain (`tsmom12` itself is 1.00 and 1.00). The last column is the second minus the "
        "first: above zero, the model keeps more of the good weeks than of the bad ones.",
        head, rows,
    )  # fmt: skip

    # 8. rolling three-year windows
    starts = []
    d = date(1994, 4, 1)
    while d + timedelta(days=1096) <= last:
        starts.append(d)
        d = date(d.year + (d.month + 3 > 12), (d.month + 3 - 1) % 12 + 1, 1)
    rows = []
    for nm in names[1:]:
        diffs, when = [], []
        for s0 in starts:
            x = a.cut(nm, s0, s0 + timedelta(days=1095))
            y = a.cut("tsmom12", s0, s0 + timedelta(days=1095))
            if ok(x) and ok(y):
                diffs.append(stats.sharpe(x) - stats.sharpe(y))
                when.append(s0)
        if len(diffs) < 8:
            rows.append(f"| {nm} | {len(diffs)} | - | - | - | - | - |")
            continue
        dd = np.array(diffs)
        lo_i, hi_i = int(dd.argmin()), int(dd.argmax())
        rows.append(
            f"| {nm} | {len(dd)} | {(dd > 0).mean():.0%} | {dd.min():+.2f} "
            f"({when[lo_i]:%Y-%m}) | {np.median(dd):+.2f} | {dd.max():+.2f} ({when[hi_i]:%Y-%m}) |"
            f" {(dd < -0.25).mean():.0%} |"
        )
    head = ("| Model | Windows | Ahead of `tsmom12` | Worst (window from) | Median | "
            "Best (window from) | Behind by 0.25 or more |")  # fmt: skip
    out += section("6. Rolling three-year windows: Sharpe minus `tsmom12`'s",
                   "A new three-year window every quarter.", head, rows)  # fmt: skip

    # 2 (asset). contribution by asset
    rows, rows2 = [], []
    base_c = con.sum(axis=0) * 365 / n * 100
    for nm in [x for x in names if x in a.w]:
        c_m = contributions(a, nm)
        x = a.rets[nm]
        days_m = (~np.isnan(x)).sum()
        per = c_m.sum(axis=0) * 365 / days_m * 100
        gap = (np.nansum(x) - c_m.sum()) * 365 / days_m * 100
        rows.append(f"| {nm} |" + "".join(f" {v:+.1f} |" for v in per) +
                    f" {gap:+.1f} | {np.nansum(x) * 365 / days_m * 100:+.1f} |")  # fmt: skip
        ep_c = c_m[in_ep].sum(axis=0) * 100
        rows2.append(f"| {nm} |" + "".join(f" {v:+.0f} |" for v in ep_c) +
                     f" {np.nansum(x[in_ep]) * 100:+.0f} |")  # fmt: skip
    head = ("| Model |" + "".join(f" {s} |" for s in a.syms) +
            " Costs and fills | Total (simple, %/yr) |")  # fmt: skip
    out += section(
        "7a. Where the return comes from: contribution by asset (% a year, simple)",
        "Yesterday's target weight times the asset's close-to-close return, summed and "
        "annualised over the model's own span. `Costs and fills` is the gap to the gym's "
        "return (rough for the two SPY rules, which trade daily: their fills move return "
        "between the two columns). Reference: `tsmom12` earns " +
        ", ".join(f"{s} {v:+.1f}" for s, v in zip(a.syms, base_c, strict=True)) + ".",
        head, rows,
    )  # fmt: skip
    head = "| Model |" + "".join(f" {s} |" for s in a.syms) + " Total |"
    out += section(
        "7b. Which assets cost what inside `tsmom12`'s ten episodes (points, summed over all "
        f"ten falls; {in_ep.sum()} days)",
        "Simple sums of daily contributions from each peak to its trough.", head, rows2,
    )  # fmt: skip

    # 9. each model's own three deepest drawdowns
    rows = []
    for nm in names:
        x = a.rets[nm]
        m = ~np.isnan(x)
        off = int(np.argmax(m))
        cells = []
        for e in episodes(x[m], 3):
            p, t = e.peak + off, e.trough + off
            txt = f"{e.depth * 100:.0f}% {a.day(max(p - 1, 0)):%Y-%m} to {a.day(t):%Y-%m}"
            if nm in a.w:
                c_as = contributions(a, nm)[p : t + 1].sum(axis=0)
                i = int(np.argmin(c_as))
                txt += f" ({a.syms[i]} {c_as[i] * 100:+.0f})"
            cells.append(txt)
        rows.append(f"| {nm} | " + " | ".join(cells + ["-"] * (3 - len(cells))) + " |")
    out += [
        "## 8. Each model's own three deepest drawdowns", "",
        "Depth, peak month to trough month, and the asset that cost most (points).", "",
        "| Model | Deepest | Second | Third |", "|---|---|---|---|", *rows, "",
    ]  # fmt: skip

    (harness.RESEARCH / "results" / "deep-1-atlas.md").write_text("\n".join(out).rstrip() + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
