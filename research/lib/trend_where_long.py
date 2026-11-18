"""trend-where-long: `where-vol` of lane trend-where on monthly long bonds and gold
(card: research/cards/trend-where-long.md; write-up: research/data-long-2.md, section 3).

    uv run --with xlrd python -I research/lib/trend_where_long.py

The rule is copied from `trend_where.py` (branch `trend-where`, PR #43) and translated to
monthly bars as the card fixes; nothing else changed. Pure numpy core (tested in
tests/test_trend_where_long.py); `main` loads the caches, writes
research/results/trend-where-long.md and appends the card's rows to research/tries.md once.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

MIN_YEARS = 5.0
MIN_BARS = 60
LOOKBACK = 12
COST = 0.0002  # a side, per unit of weight changed


def mnum(d: date) -> int:
    return d.year * 12 + d.month - 1


def mdate(n: int) -> date:
    return date(n // 12, n % 12 + 1, 1)


@dataclass
class Grid:
    """Monthly returns on one calendar grid: row i is the month `first + i`; `r[i, a]` is the
    simple return dated that month (NaN where the asset has none)."""

    first: int
    names: list[str]
    r: np.ndarray

    @classmethod
    def build(cls, series: dict[str, list[tuple[date, float]]]) -> Grid:
        names = list(series)
        lo = min(mnum(s[0][0]) for s in series.values())
        hi = max(mnum(s[-1][0]) for s in series.values())
        r = np.full((hi - lo + 1, len(names)), np.nan)
        for j, n in enumerate(names):
            for d, g in series[n]:
                r[mnum(d) - lo, j] = g - 1
        return cls(lo, names, r)


def signals(r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """At the end of month k: `valid[k]` if the 12 returns dated k-11..k exist, `on[k]` if they
    compound to more than 1 (12-month log return > 0)."""
    t, a = r.shape
    valid = np.zeros((t, a), dtype=bool)
    on = np.zeros((t, a), dtype=bool)
    lr = np.log1p(r)
    for k in range(LOOKBACK - 1, t):
        w = lr[k - LOOKBACK + 1 : k + 1]
        ok = np.isfinite(w).all(axis=0)
        valid[k] = ok
        on[k] = ok & (np.where(ok, w.sum(axis=0), 0.0) > 0)
    return valid, on


def decision_of(m: int, gap: int) -> int:
    """The decision month whose signal trades the return dated m."""
    return m - 1 - gap


@dataclass
class Labels:
    ok: np.ndarray  # return m had a signal
    inn: np.ndarray  # ... and it was on


def labels(valid: np.ndarray, on: np.ndarray, gap: int) -> Labels:
    t, a = valid.shape
    ok = np.zeros((t, a), dtype=bool)
    inn = np.zeros((t, a), dtype=bool)
    for m in range(t):
        k = decision_of(m, gap)
        if k >= 0:
            ok[m], inn[m] = valid[k], on[k]
    return Labels(ok, inn)


@dataclass
class Evidence:
    years: float
    n_out: int
    n_in: int
    out: float
    inn: float
    keep: bool


def evidence(
    r: np.ndarray, lab: Labels, j: int, upto: int, min_years: float, min_bars: int
) -> Evidence:
    """What a refit at the end of month `upto` sees for asset j: returns dated <= upto only."""
    x = r[: upto + 1, j]
    ok, inn = lab.ok[: upto + 1, j], lab.inn[: upto + 1, j]
    r_out, r_in = x[ok & ~inn], x[ok & inn]
    years = float(ok.sum()) / 12
    thin = years < min_years or min(len(r_out), len(r_in)) < min_bars
    a = float(r_out.std()) if len(r_out) else 0.0
    b = float(r_in.std()) if len(r_in) else 0.0
    return Evidence(years, len(r_out), len(r_in), a, b, thin or a > b)


def keep_table(
    g: Grid, lab: Labels, min_years: float = MIN_YEARS, min_bars: int = MIN_BARS
) -> np.ndarray:
    """`keep[k, a]`: the answer in force for a decision at the end of month k (the refit of the
    last December <= k; yes before the first December)."""
    t, a = g.r.shape
    keep = np.ones((t, a), dtype=bool)
    cur = np.ones(a, dtype=bool)
    for k in range(t):
        if (g.first + k) % 12 == 11:
            cur = np.array([evidence(g.r, lab, j, k, min_years, min_bars).keep for j in range(a)])
        keep[k] = cur
    return keep


def weights(
    g: Grid, kind: str, gap: int, keep: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """Target weights `w[m, a]` for the return dated m, and `live[m]`: every asset in the book
    eligible at that decision. kind: `hold`, `tsmom12` or `where`."""
    valid, on = signals(g.r)
    t, a = g.r.shape
    w = np.zeros((t, a))
    live = np.zeros(t, dtype=bool)
    for m in range(t):
        k = decision_of(m, gap)
        if k < 0:
            continue
        el = valid[k]
        live[m] = bool(el.all())
        if not el.any():
            continue
        if kind == "hold":
            held = el
        elif kind == "tsmom12":
            held = el & on[k]
        elif kind == "where":
            assert keep is not None
            held = el & (~keep[k] | on[k])
        else:
            raise ValueError(kind)
        w[m] = held / el.sum()
    return w, live


def book(g: Grid, w: np.ndarray, cost: float = COST) -> np.ndarray:
    """Monthly book return: weights times returns (cash earns 0), minus cost on weight changes."""
    gross = np.nansum(w * np.nan_to_num(g.r), axis=1)
    dw = np.abs(np.diff(w, axis=0, prepend=np.zeros((1, w.shape[1])))).sum(axis=1)
    return gross - cost * dw


def max_dd(r: np.ndarray) -> float:
    if len(r) == 0:
        return 0.0
    eq = np.concatenate([[1.0], np.cumprod(1 + r)])
    return float((1 - eq / np.maximum.accumulate(eq)).max())


def sharpe_m(r: np.ndarray) -> float:
    sd = r.std()
    return float(r.mean() / sd * math.sqrt(12)) if sd > 0 else 0.0


def cagr_m(r: np.ndarray) -> float:
    return float(np.exp(np.log1p(r).sum() * 12 / len(r)) - 1) if len(r) else 0.0


# ---------------------------------------------------------------------------------- the run

END = date(2025, 10, 1)  # last return used (held-out year from 2025-11-11)
BOND_FROM = date(1953, 4, 1)  # first non-interpolated Shiller label
SPLIT = date(2001, 12, 1)
WINDOWS = {
    "bond": (date(1965, 1, 1), date(1981, 9, 1)),
    "gold": (date(1980, 1, 1), date(2001, 12, 1)),
}
BOOKS = {"bond-m": ["bond"], "gold-m": ["gold"], "bondgold-m": ["bond", "gold"]}
IDEA = "trend-where"


@dataclass
class Variant:
    name: str
    kind: str  # hold / tsmom12 / where
    gap: int
    min_bars: int
    row_kind: str  # tries.md kind


VARIANTS = [
    Variant("where-vol", "where", 1, MIN_BARS, "robustness"),
    Variant("tsmom12", "tsmom12", 1, MIN_BARS, "baseline"),
    Variant("hold", "hold", 1, MIN_BARS, "baseline"),
    Variant("where-vol-min12", "where", 1, 12, "robustness"),
    Variant("where-vol-lag0", "where", 0, MIN_BARS, "robustness"),
    Variant("tsmom12-lag0", "tsmom12", 0, MIN_BARS, "robustness"),
]


def load_series() -> dict[str, list[tuple[date, float]]]:
    import long_bond as lb
    import long_gold as lg

    bond = [
        (mdate(mnum(d) + 1), x) for d, x in lb.load() if d >= BOND_FROM and mnum(d) + 1 <= mnum(END)
    ]
    gold = [(d, x) for d, x in lg.returns(lg.load(), lg.FREE_FROM) if d <= END]
    return {"bond": bond, "gold": gold}


@dataclass
class Result:
    variant: Variant
    book: str
    months: np.ndarray  # month numbers of the book's returns
    rets: np.ndarray
    w: np.ndarray
    keep: np.ndarray | None

    def between(self, a: date, b: date) -> np.ndarray:
        sel = (self.months >= mnum(a)) & (self.months <= mnum(b))
        return self.rets[sel]

    def turnover(self, a: date, b: date) -> float:
        sel = (self.months >= mnum(a)) & (self.months <= mnum(b))
        dw = np.abs(np.diff(self.w, axis=0, prepend=np.zeros((1, self.w.shape[1])))).sum(axis=1)
        return float(dw[sel][1:].sum() / max(sel.sum(), 1) * 12)


def run_book(series: dict[str, list[tuple[date, float]]], bk: str, v: Variant) -> Result:
    g = Grid.build({n: series[n] for n in BOOKS[bk]})
    keep = None
    if v.kind == "where":
        valid, on = signals(g.r)
        keep = keep_table(g, labels(valid, on, v.gap), MIN_YEARS, v.min_bars)
    w, live = weights(g, v.kind, v.gap, keep)
    start = int(np.argmax(live))
    rets = book(g, w)
    months = g.first + np.arange(len(rets))
    return Result(v, bk, months[start:], rets[start:], w[start:], keep)


def main() -> None:
    import stats

    series = load_series()
    res = {(bk, v.name): run_book(series, bk, v) for bk in BOOKS for v in VARIANTS}
    out = [
        "# trend-where-long: results",
        "",
        "Card `research/cards/trend-where-long.md`. Generated by "
        "`research/lib/trend_where_long.py`. Monthly bars; Sharpe = monthly x sqrt(12); cash 0; "
        "2 bps a side. Bond = Shiller TR re-dated (labels 1953-04 on), gold = datahub monthly "
        "average (1971-01 on); last return 2025-10.",
        "",
    ]
    rows: list[str] = []
    for bk in BOOKS:
        r0 = res[(bk, "where-vol")]
        first = mdate(int(r0.months[0]))
        out += [
            f"## Book `{bk}` (first traded return {first:%Y-%m})",
            "",
            "| Variant | Window | Sharpe | vs `tsmom12` (p) | Growth/yr | Worst loss | "
            "Turnover/yr |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
        for v in VARIANTS:
            r = res[(bk, v.name)]
            twin = res[(bk, "tsmom12-lag0" if v.gap == 0 else "tsmom12")]
            for lab, a, b in (("to 2001", first, SPLIT), ("2002-2025", date(2002, 1, 1), END)):
                x, y = r.between(a, b), twin.between(a, b)
                if v.name.startswith("tsmom12"):
                    vs = "-"
                else:
                    _, p, _, _ = stats.sharpe_diff_boot(x, y, mean_block=6)
                    vs = f"{sharpe_m(x) - sharpe_m(y):+.2f} ({p:.2f})"
                out.append(
                    f"| {v.name} | {lab} | {sharpe_m(x):.2f} | {vs} | {cagr_m(x):+.1%} | "
                    f"{max_dd(x):.1%} | {r.turnover(a, b):.2f} |"
                )
            x = r.between(first, SPLIT)
            total = float(np.prod(1 + x) - 1)
            rows.append(
                f"| {{now}} | {IDEA} | {v.name}@{bk} | {v.row_kind} | train | {first} | "
                f"{SPLIT:%Y-%m}-31 | {sharpe_m(x):.2f} | {total:+.1%} | {max_dd(x):.1%} | "
                f"{r.turnover(first, SPLIT):.2f} |"
            )
        out += ["", "Worst loss inside the card's windows:", "", "| Window |"]
        names = [v.name for v in VARIANTS]
        out[-1] += "".join(f" {n} |" for n in names)
        out.append("|---|" + "---:|" * len(names))
        for asset in BOOKS[bk]:
            a, b = WINDOWS[asset]
            cells = "".join(f" {max_dd(res[(bk, n)].between(a, b)):.1%} |" for n in names)
            out.append(f"| {asset} {a:%Y-%m} to {b:%Y-%m} |{cells}")
        out.append("")

    # answers per asset by refit year (single-asset books; same evidence in the pair book)
    for v in [x for x in VARIANTS if x.kind == "where"]:
        out += [f"## Answers of `{v.name}` (yes = keep the filter), by refit December", ""]
        for asset in ("bond", "gold"):
            g = Grid.build({asset: series[asset]})
            valid, on = signals(g.r)
            lab = labels(valid, on, v.gap)
            changes, n_no, n_no_pre, n_tot, n_tot_pre = [], 0, 0, 0, 0
            prev = None
            for k in range(len(g.r)):
                if (g.first + k) % 12 != 11 or not lab.ok[: k + 1, 0].any():
                    continue
                e = evidence(g.r, lab, 0, k, MIN_YEARS, v.min_bars)
                yr = mdate(g.first + k).year
                n_tot += 1
                n_no += not e.keep
                if yr <= 2000:
                    n_tot_pre += 1
                    n_no_pre += not e.keep
                if e.keep != prev or yr in (1981, 2000, 2024):  # changes, plus three snapshots
                    changes.append(
                        f"| {asset} | Dec {yr} | {'yes' if e.keep else 'no'} | {e.n_out} | "
                        f"{e.n_in} | {e.out * math.sqrt(12):.1%} | {e.inn * math.sqrt(12):.1%} |"
                    )
                prev = e.keep
            out += [
                f"{asset}: {n_no_pre} of {n_tot_pre} refits no for decisions to 2001; "
                f"{n_no} of {n_tot} through Dec {END.year - 1 if END.month < 12 else END.year}.",
                "",
                "| Asset | Refit | Answer from here | Out months | In months | Vol out | Vol in |",
                "|---|---|---|---:|---:|---:|---:|",
                *changes,
                "",
            ]

    path = HERE.parent / "results" / "trend-where-long.md"
    path.write_text("\n".join(out).rstrip() + "\n")
    print("\n".join(out))

    tries = HERE.parent / "tries.md"
    text = tries.read_text()
    if f"| {IDEA} | where-vol@bond-m |" in text:
        print("tries.md rows already logged; not appended again")
        return
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    with tries.open("a") as f:
        f.write("".join(row.replace("{now}", now) + "\n" for row in rows))
    print(f"appended {len(rows)} rows to tries.md")


if __name__ == "__main__":
    main()
