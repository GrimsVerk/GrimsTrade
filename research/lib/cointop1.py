"""cointop-1, Parts A and B: coin tops on breadth-1's top-100 coin book, and the choice of one
setting for each of three exit rules there (card in research/cointop-1.md).

    uv run python -I research/lib/cointop1.py [--log]      # the real run (once, with --log)
    uv run python -I research/lib/cointop1.py --synthetic  # plumbing check on random prices

Writes `research/results/cointop-1-coins.md` and `<cache_root>/derived/cointop-1/chosen.json`.
With `--log` every grid run, the twin and the controls get a row in tries.md.
"""

from __future__ import annotations

import fcntl
import json
import sys
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import cointop1_core as core  # noqa: E402
import macro  # noqa: E402
import stats  # noqa: E402
from harness import RESEARCH, TRAIN_END, TRIES  # noqa: E402

IDEA = "cointop-1-cm"
TEST_COINS = ("btc", "eth", "ltc", "xrp", "bch", "etc", "xlm", "dash")  # never used to choose
HALF = date(2022, 7, 1)
RULES: dict[str, tuple[float, ...]] = {
    "stop": core.STOP_GRID,
    "fade": tuple(float(x) for x in core.DAYS_GRID),
    "breadth": tuple(float(x) for x in core.DAYS_GRID),
}
HORIZONS = (7, 14, 28, 56, 91, 182, 365)


def derived() -> Path:
    d = macro.cache_root() / "derived" / "cointop-1"
    d.mkdir(parents=True, exist_ok=True)
    return d


def label(rule: str, v: float) -> str:
    return f"{rule}-{v:g}"


@dataclass
class Lab:
    """The coin book with everything the tables need, on the decision grid."""

    book: bb.Book
    sel: np.ndarray  # selection-set coins (bool per coin)
    d: np.ndarray  # decision rows (Fridays)
    b: np.ndarray  # set rows (decision + 1 day)
    univ: np.ndarray  # [decisions, coins] selection-set coins in the universe
    up: np.ndarray  # [decisions, coins] twin's condition
    mask: np.ndarray  # [days, coins] coin-days a pooled score counts
    logr: np.ndarray  # [days, coins] log return of the carried price
    filled: np.ndarray
    sig: dict[str, np.ndarray] = field(default_factory=dict)  # lagged signals [days, coins]
    share: dict[int, np.ndarray] = field(default_factory=dict)  # lagged breadth per horizon
    tops: dict[int, list[core.Top]] = field(default_factory=dict)  # per coin, all its tops
    open_high: dict[int, int] = field(default_factory=dict)

    @property
    def n_days(self) -> int:
        return int(self.book.px.shape[0])

    def day(self, row: int) -> date:
        return self.book.day0 + timedelta(days=int(row))

    def row(self, d: date) -> int:
        return (d - self.book.day0).days


def build(book: bb.Book, sel_names: tuple[str, ...] = TEST_COINS) -> Lab:
    px = book.px
    n_days, n = px.shape
    sel = np.array([nm not in sel_names for nm in book.names])
    dec, skip = bb.decisions(book, "weekly", bb.start_day(book))
    d = dec[dec + skip < n_days]
    b = d + skip
    univ = book.elig[d] & sel[None, :] & np.isfinite(px[b])
    up = book.up[d]
    filled = xs.ffill(px)
    with np.errstate(invalid="ignore", divide="ignore"):
        logr = np.zeros_like(filled)
        logr[1:] = np.log(filled[1:] / filled[:-1])
    logr[~np.isfinite(logr)] = 0.0
    lab = Lab(book, sel, d, b, univ, up, core.coin_days(univ, b, n_days), logr, filled)
    vol = core.ewma_vol(px, 60)
    vol10 = core.ewma_vol(px, 10)
    sh = book.shift
    for h in sorted({7, 28, 56, 91, 182, 365}):
        lab.sig[f"r{h}"] = xs.lag(xs.logret(px, h, 0), sh)
    for h in (7, 28, 91, 365):
        lab.sig[f"z{h}"] = xs.lag(core.zscore(px, vol, h), sh)
    lab.sig["dd_1y"] = xs.lag(core.dd_1y(px, vol), sh)
    with np.errstate(invalid="ignore", divide="ignore"):
        lab.sig["log_vol"] = xs.lag(np.log(vol), sh)
        lab.sig["vol_shock"] = xs.lag(np.log(vol10 / vol), sh)
    for h in sorted({*core.DAYS_GRID, 365}):
        lab.share[h] = core.breadth_share(lab.sig[f"r{h}"], book.elig)
    for j in range(n):
        lab.tops[j], lab.open_high[j] = core.find_tops(px[:, j])
    return lab


def condition(lab: Lab, rule: str, v: float) -> np.ndarray:
    """The rule's extra condition at every decision, `[decisions, coins]`."""
    if rule == "stop":
        return core.stop_cond(lab.sig["dd_1y"], v)[lab.d]
    if rule == "fade":
        return core.fade_cond(lab.sig[f"r{int(v)}"])[lab.d]
    if rule == "breadth":
        return core.breadth_cond(lab.share[int(v)], len(lab.sel))[lab.d]
    raise ValueError(rule)


@dataclass
class Res:
    name: str
    hold: np.ndarray  # [decisions, coins]
    ret: np.ndarray  # paper series [days, coins]
    pos: np.ndarray  # position earning each day's return
    book: np.ndarray  # daily returns of the equal-slot portfolio
    turnover: float
    pooled: float = 0.0


def run(lab: Lab, name: str, cond: np.ndarray | None) -> Res:
    hold = lab.univ & lab.up
    if cond is not None:
        hold = hold & cond
    ret, pos = core.paper(lab.book.px, hold, lab.b)
    n_univ = lab.univ.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        targets = np.where(n_univ[:, None] >= 10, hold / np.maximum(n_univ, 1)[:, None], 0.0)
    port = xs.simulate(lab.book.px, targets, lab.b, lab.book.cost, int(lab.b[0]))
    years = (lab.n_days - lab.b[0]) / 365
    turn = float(np.abs(np.diff(targets, axis=0)).sum() / years)
    return Res(name, hold, ret, pos, port, turn, core.pooled_sharpe(ret, lab.mask))


# ---------------------------------------------------------------- tops


@dataclass
class Event:
    coin: int
    top: core.Top
    near_btc: bool


def study_tops(lab: Lab, first_row: int | None = None, last_row: int | None = None) -> list[Event]:
    """Tops of selection-set coins that were in the book's universe on the top day."""
    lo = int(lab.b[0]) if first_row is None else first_row
    hi = lab.n_days - 1 if last_row is None else last_row
    names = lab.book.names
    btc = [t.top for t in lab.tops[names.index("btc")]] if "btc" in names else []
    out = []
    for j in np.flatnonzero(lab.sel):
        for t in lab.tops[int(j)]:
            if not lo <= t.top <= hi:
                continue
            if not lab.book.elig[min(t.top + 1, lab.n_days - 1), j]:
                continue
            out.append(Event(int(j), t, any(abs(t.top - x) <= 30 for x in btc)))
    return out


def qs(x: list[float] | np.ndarray, spec: str = ".0f", scale: float = 1.0) -> str:
    a = np.asarray(x, float) * scale
    a = a[np.isfinite(a)]
    if len(a) == 0:
        return "-"
    q1, q2, q3 = np.quantile(a, [0.25, 0.5, 0.75])
    return f"{q2:{spec}} ({q1:{spec}} to {q3:{spec}})"


@dataclass
class TopStat:
    n: int
    in_at_top: float
    exit_days: str
    exit_rel: str
    in_when_halved: float
    sat_median: float
    sat_total: float


def top_stats(lab: Lab, events: list[Event], pos: np.ndarray, base_pos: np.ndarray) -> TopStat:
    """How a position series went through the tops at which `base_pos` (the twin) held the coin."""
    days, rel, sat, halved, at_top = [], [], [], [], []
    num = den = 0.0
    n = 0
    for e in events:
        j, t = e.coin, e.top
        if t.top + 1 >= lab.n_days or base_pos[t.top + 1, j] != 1:
            continue
        n += 1
        fall = float(np.log(lab.filled[t.low, j] / lab.filled[t.top, j]))
        took = float((pos[t.top + 1 : t.low + 1, j] * lab.logr[t.top + 1 : t.low + 1, j]).sum())
        sat.append(took / fall)
        num += took
        den += fall
        inn = pos[t.top + 1, j] == 1
        at_top.append(inn)
        halved.append(pos[t.halved, j] == 1)
        if inn:
            out_rows = np.flatnonzero(pos[t.top + 1 :, j] == 0)
            if len(out_rows):
                ex = t.top + int(out_rows[0])  # the set day: the row before the first day out
                days.append(ex - t.top)
                rel.append(lab.filled[ex, j] / lab.filled[t.top, j] - 1)
    if n == 0:
        return TopStat(0, np.nan, "-", "-", np.nan, np.nan, np.nan)
    return TopStat(
        n,
        float(np.mean(at_top)),
        qs(days),
        qs(rel, "+.0f", 100),
        float(np.mean(halved)),
        float(np.median(sat)),
        num / den if den else np.nan,
    )


def buckets(lab: Lab, events: list[Event]) -> np.ndarray:
    """Per coin-day: 1 inside a fall (top to lowest price), 2 in the 365 days after that low
    (cut at the coin's next top), 0 elsewhere."""
    out = np.zeros(lab.book.px.shape, dtype=np.int8)
    by_coin: dict[int, list[core.Top]] = {}
    for e in events:
        by_coin.setdefault(e.coin, []).append(e.top)
    for j, tops in by_coin.items():
        tops = sorted(tops, key=lambda t: t.top)
        for i, t in enumerate(tops):
            nxt = tops[i + 1].top if i + 1 < len(tops) else lab.n_days
            out[t.low + 1 : min(t.low + 366, nxt + 1), j] = 2
        for t in tops:
            out[t.top + 1 : t.low + 1, j] = 1
    return out


def decompose(lab: Lab, r: Res, twin: Res, bucket: np.ndarray) -> dict[str, float]:
    """Where the rule's log growth differs from the twin's, in % per coin a year."""
    years = lab.mask.sum() / 365
    gross = (r.pos - twin.pos) * lab.logr
    out = {}
    for k, nm in ((1, "falls"), (2, "rebounds"), (0, "rest")):
        out[nm] = float(gross[lab.mask & (bucket == k)].sum() / years * 100)
    with np.errstate(invalid="ignore", divide="ignore"):
        total = np.log1p(r.ret) - np.log1p(twin.ret)
    out["costs"] = float(total[lab.mask].sum() / years * 100) - sum(out.values())
    out["total"] = float(total[lab.mask].sum() / years * 100)
    return out


# ---------------------------------------------------------------- Part A tables


def table_a1(lab: Lab, ev: list[Event], twin: Res) -> list[str]:
    names = lab.book.names
    trend_on = [e for e in ev if e.top.top + 1 < lab.n_days and twin.pos[e.top.top + 1, e.coin]]
    ever = int(lab.univ.any(0).sum())
    coins_with = len({e.coin for e in ev})
    stopped = sum(1 for j in {e.coin for e in ev} if not np.isfinite(lab.book.px[-30:, j]).any())
    months: dict[tuple[int, int], int] = {}
    for e in ev:
        dd = lab.day(e.top.top)
        months[(dd.year, dd.month)] = months.get((dd.year, dd.month), 0) + 1
    shares = np.array(list(months.values())) / max(len(ev), 1)
    eff = 1 / (shares**2).sum() if len(ev) else float("nan")
    tmonths: dict[tuple[int, int], int] = {}
    for e in trend_on:
        dd = lab.day(e.top.top)
        tmonths[(dd.year, dd.month)] = tmonths.get((dd.year, dd.month), 0) + 1
    tsh = np.array(list(tmonths.values())) / max(len(trend_on), 1)
    teff = 1 / (tsh**2).sum() if len(trend_on) else float("nan")
    open_high = sum(
        1
        for j in np.flatnonzero(lab.sel & lab.univ[-1])
        if lab.open_high[int(j)] >= 0 and lab.open_high[int(j)] >= lab.b[0]
    )
    open_low = sum(1 for e in ev if e.top.settled < 0)
    near = np.mean([e.near_btc for e in ev]) if ev else float("nan")
    tnear = np.mean([e.near_btc for e in trend_on]) if trend_on else float("nan")
    per_coin = np.bincount([e.coin for e in ev], minlength=len(names))
    out = [
        "### A1. How many tops, and how many separate episodes",
        "",
        f"- Selection-set coins ever in the universe: {ever}. Coins with at least one study top: "
        f"{coins_with} (of which {stopped} have no price in the last 30 days of train: dead or "
        f"dropped).",
        f"- **Study tops: {len(ev)}; trend-on tops (the twin held the coin at the top): "
        f"{len(trend_on)}.** Tops per coin with any: median "
        f"{np.median(per_coin[per_coin > 0]) if coins_with else 0:.0f}, most "
        f"{per_coin.max() if coins_with else 0}.",
        f"- Study tops whose low is still open at the end of train (the fall may not be over): "
        f"{open_low}. Coins in the universe on the last decision that end train below a high "
        f"that has not lost 50% (open highs, not tops): {open_high}.",
        f"- **Effective number of top months** (1 / sum of squared monthly shares): "
        f"{eff:.1f} for study tops, {teff:.1f} for trend-on tops. That is roughly how many "
        f"separate episodes the choice of settings rests on.",
        f"- Share of study tops within 30 days of a BTC top: {near:.0%} (trend-on tops: "
        f"{tnear:.0%}).",
    ]
    if "btc" in names:
        ib = names.index("btc")
        bt = [
            f"{lab.day(t.top)} ({lab.filled[t.low, ib] / lab.filled[t.top, ib] - 1:+.0%})"
            for t in lab.tops[ib]
            if t.top >= lab.b[0] - 365
        ]
        out.append(f"- BTC's own tops by the same definition, from a year before the book: "
                   f"{', '.join(bt) if bt else 'none'}.")  # fmt: skip
    out += ["", "Tops per calendar quarter (study tops / of which trend-on):", ""]
    quarters: dict[str, list[int]] = {}
    for e in ev:
        dd = lab.day(e.top.top)
        k = f"{dd.year}Q{(dd.month - 1) // 3 + 1}"
        quarters.setdefault(k, [0, 0])
        quarters[k][0] += 1
        quarters[k][1] += int(e in trend_on)
    out += ["| Quarter | Study tops | Trend-on |", "|---|---:|---:|"]
    out += [f"| {k} | {v[0]} | {v[1]} |" for k, v in sorted(quarters.items())]
    return out + [""]


def table_a2(lab: Lab, ev: list[Event], title: str) -> list[str]:
    out = [title, ""]
    out += ["| Days after the top | Price against the top, % (median, quartiles) | Tops |"]
    out += ["|---:|---|---:|"]
    for h in HORIZONS:
        v = [
            lab.filled[e.top.top + h, e.coin] / lab.filled[e.top.top, e.coin] - 1
            for e in ev
            if e.top.top + h < lab.n_days
        ]
        out.append(f"| {h} | {qs(v, '+.0f', 100)} | {len(v)} |")
    to_half = [e.top.halved - e.top.top for e in ev]
    depth = [lab.filled[e.top.low, e.coin] / lab.filled[e.top.top, e.coin] - 1 for e in ev]
    to_low = [e.top.low - e.top.top for e in ev]
    settled = np.mean([e.top.settled >= 0 for e in ev]) if ev else float("nan")
    out += [
        "",
        f"Days from the top to -50%: {qs(to_half)}. Lowest price against the top: "
        f"{qs(depth, '+.0f', 100)}%, reached {qs(to_low)} days after the top. Lows settled by a "
        f"doubling before the end of train: {settled:.0%}.",
        "",
    ]
    return out


A3_HEAD = [
    "| Rule | Tops | In at the top | Days from top to exit | Price at exit against the top, % | "
    "Still in when the coin has halved | Share of the fall sat through: median | all tops "
    "together |",
    "|---|---:|---:|---|---|---:|---:|---:|",
]


def a3_row(name: str, s: TopStat) -> str:
    if s.n == 0:
        return f"| {name} | 0 | - | - | - | - | - | - |"
    return (
        f"| {name} | {s.n} | {s.in_at_top:.0%} | {s.exit_days} | {s.exit_rel} | "
        f"{s.in_when_halved:.0%} | {s.sat_median:.0%} | {s.sat_total:.0%} |"
    )


FEATURES = [
    "z7", "z28", "z91", "z365", "decay", "dd_1y", "log_vol", "vol_shock", "vol_growth",
    "turnover", "cap_rank", "breadth_28", "breadth_91", "breadth_365", "btc_z28", "funding_7",
]  # fmt: skip


def funding(lab: Lab) -> np.ndarray:
    """7-day mean funding rate (per day) of breadth-1's Binance pairs, on the coin book's rows,
    lagged a day. NaN for coins without a perp in that set or before its funding starts."""
    out = np.full(lab.book.px.shape, np.nan)
    src = macro.cache_root() / "derived" / "breadth-1"
    t0 = int(datetime.combine(lab.book.day0, datetime.min.time(), UTC).timestamp())
    for f in sorted(src.glob("binance-*-funding.npz")):
        base = f.name.split("-")[1].removesuffix("USDT").lower()
        if base not in lab.book.names:
            continue
        fz = np.load(f)
        if "ft" not in fz:
            continue
        day = (fz["ft"] - t0) // 86400
        k = (day >= 0) & (day < lab.n_days)
        num = np.bincount(day[k], weights=fz["fr"][k], minlength=lab.n_days)
        cnt = np.bincount(day[k], minlength=lab.n_days)
        col = np.full(lab.n_days, np.nan)
        col[cnt > 0] = (num / np.maximum(cnt, 1) * 3)[cnt > 0]
        out[:, lab.book.names.index(base)] = col
    return xs.lag(xs.roll_mean(out, 7, 0.5), 1)


def feature_rows(lab: Lab, twin: Res, synthetic: bool) -> dict[str, np.ndarray]:
    """One row per (Friday, coin the twin holds): features, both labels, the decision index."""
    book = lab.book
    kk, jj = np.nonzero(twin.hold)
    rows = lab.d[kk]
    f: dict[str, np.ndarray] = {}
    for nm in ("z7", "z28", "z91", "z365", "dd_1y", "log_vol", "vol_shock"):
        f[nm] = lab.sig[nm][rows, jj]
    f["decay"] = f["z28"] - f["z91"]
    f["vol_growth"] = book.signals["vol_growth"][rows, jj]
    f["turnover"] = -book.signals["turnover"][rows, jj]
    size = -book.signals["size"]  # log of the 7-day mean market cap, lagged
    rank = np.full(size.shape, np.nan)
    for r in np.unique(rows):
        m = book.elig[r] & np.isfinite(size[r])
        if m.sum() > 1:
            order = np.argsort(np.argsort(size[r, m]))
            rank[r, np.flatnonzero(m)] = order / (m.sum() - 1)
    f["cap_rank"] = rank[rows, jj]
    for h in (28, 91, 365):
        f[f"breadth_{h}"] = lab.share[h][rows]
    f["btc_z28"] = (
        lab.sig["z28"][rows, book.names.index("btc")]
        if "btc" in book.names
        else np.full(len(rows), np.nan)
    )
    f["funding_7"] = np.full(len(rows), np.nan) if synthetic else funding(lab)[rows, jj]
    topday = np.zeros(book.px.shape, dtype=np.int32)
    for j, tops in lab.tops.items():
        for t in tops:
            topday[t.top, j] = 1
    cum = np.vstack([np.zeros((1, topday.shape[1]), np.int32), np.cumsum(topday, axis=0)])

    def count(lo: np.ndarray, hi: np.ndarray) -> np.ndarray:  # tops in rows lo..hi inclusive
        lo = np.clip(lo, 0, lab.n_days)
        hi = np.clip(hi + 1, 0, lab.n_days)
        return cum[hi, jj] - cum[lo, jj]

    s = rows - 1  # the last price the decision sees
    f["before"] = count(s + 1, s + 14) > 0
    f["after"] = count(s - 14, s) > 0
    f["k"] = kk
    return f


def auc_boot(
    x: np.ndarray, y: np.ndarray, k: np.ndarray, draws: int = 500, seed: int = 0
) -> tuple[float, float, float]:
    ok = np.isfinite(x)
    x, y, k = x[ok], y[ok], k[ok]
    point = core.auc(x, y)
    if not np.isfinite(point) or draws == 0:
        return point, np.nan, np.nan
    uniq, inv = np.unique(k, return_inverse=True)
    order = np.argsort(inv, kind="mergesort")
    bounds = np.r_[0, np.cumsum(np.bincount(inv, minlength=len(uniq)))]
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(draws):
        pick = stats._stationary_indices(len(uniq), 4, rng)
        idx = np.concatenate([order[bounds[i] : bounds[i + 1]] for i in pick])
        v = core.auc(x[idx], y[idx])
        if np.isfinite(v):
            vals.append(v)
    if len(vals) < draws // 2:
        return point, np.nan, np.nan
    return point, float(np.quantile(vals, 0.05)), float(np.quantile(vals, 0.95))


def table_a4(lab: Lab, twin: Res, synthetic: bool, draws: int) -> list[str]:
    f = feature_rows(lab, twin, synthetic)
    k = f["k"]
    first = lab.d[k] < lab.row(HALF)
    out = [
        "### A4. What precedes a top, and what shows just after",
        "",
        f"Rows: every Friday on which the twin holds a selection-set coin ({len(k):,} coin-weeks). "
        f"`before`: a top of that coin in the next 14 days ({int(f['before'].sum()):,} rows). "
        f"`after`: a top in the last 14 days ({int(f['after'].sum()):,} rows). AUC 0.50 = no "
        "information; above 0.50 = the feature is higher on labelled rows. 90% interval from a "
        "bootstrap over weeks. **Marks tops** = the interval excludes 0.50 and both halves are "
        "on the same side.",
        "",
    ]
    for lab_name in ("before", "after"):
        y = f[lab_name]
        out += [
            f"**Label `{lab_name}`**",
            "",
            "| Feature | Mean on labelled rows | Mean on the rest | AUC (90% interval) | "
            "First half | Second half | Marks tops |",
            "|---|---:|---:|---|---:|---:|---|",
        ]
        for nm in FEATURES:
            x = f[nm]
            ok = np.isfinite(x)
            if ok.sum() < 100 or y[ok].sum() < 10:
                out.append(f"| `{nm}` | - | - | too few rows | - | - | - |")
                continue
            a, lo, hi = auc_boot(x, y, k, draws)
            a1, _, _ = auc_boot(x[first], y[first], k[first], 0)
            a2, _, _ = auc_boot(x[~first], y[~first], k[~first], 0)
            marks = (
                np.isfinite(lo)
                and (lo > 0.5 or hi < 0.5)
                and np.sign(a1 - 0.5) == np.sign(a2 - 0.5) == np.sign(a - 0.5)
            )
            out.append(
                f"| `{nm}` | {np.nanmean(x[ok & y]):+.2f} | {np.nanmean(x[ok & ~y]):+.2f} | "
                f"{a:.2f} ({lo:.2f} to {hi:.2f}) | {a1:.2f} | {a2:.2f} | "
                f"{'**yes**' if marks else 'no'} |"
            )
        out.append("")
    return out


def table_a5(book: bb.Book) -> list[str]:
    """Tops before the book starts, every panel coin with a year of prices at the top."""
    px = book.px
    n_days = px.shape[0]
    hist = bb.history_days(px)
    elig = xs.lag(((hist >= 365) & np.isfinite(px)).astype(float), 1) == 1
    early = bb.Book("early", book.day0, book.names, px, elig, book.up, {}, book.cost, 1, 1, 1)
    first = int(np.argmax(elig.any(1)))
    days = np.arange(first, n_days)
    wd = np.array([(book.day0 + timedelta(days=int(i))).weekday() for i in days])
    d = days[(wd == 4) & (days + 1 < n_days)]
    b = d + 1
    univ = elig[d] & np.isfinite(px[b])
    filled = xs.ffill(px)
    with np.errstate(invalid="ignore", divide="ignore"):
        logr = np.zeros_like(filled)
        logr[1:] = np.log(filled[1:] / filled[:-1])
    logr[~np.isfinite(logr)] = 0.0
    lab = Lab(early, np.ones(px.shape[1], bool), d, b, univ, book.up[d],
              core.coin_days(univ, b, n_days), logr, filled)  # fmt: skip
    for j in range(px.shape[1]):
        lab.tops[j], lab.open_high[j] = core.find_tops(px[:, j])
    cut = bb.start_day(book)
    ev = study_tops(lab, first_row=int(b[0]), last_row=cut - 1)
    twin = run(lab, "twin", None)
    hold_all = univ.copy()
    bh_ret, bh_pos = core.paper(px, hold_all, b)
    out = [
        "### A5. Early tops (before the coin book starts; description only)",
        "",
        f"Every panel coin with a year of prices at its top, tops before "
        f"{book.day0 + timedelta(days=cut)}: {len(ev)} tops on {len({e.coin for e in ev})} coins "
        "(no size or volume filter: Coin Metrics has too few market caps that early).",
        "",
    ]
    out += table_a2(lab, ev, "Shape of the fall:")
    out += A3_HEAD
    out.append(a3_row("twin (12-month rule)", top_stats(lab, ev, twin.pos, twin.pos)))
    out.append(a3_row("buy and hold", top_stats(lab, ev, bh_pos, twin.pos)))
    return out + [""]


# ---------------------------------------------------------------- Part B


def halves(lab: Lab, ret: np.ndarray) -> tuple[float, float]:
    cut = lab.row(HALF)
    m1 = lab.mask.copy()
    m1[cut:] = False
    m2 = lab.mask.copy()
    m2[:cut] = False
    return core.pooled_sharpe(ret, m1), core.pooled_sharpe(ret, m2)


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


def main() -> None:
    synthetic = "--synthetic" in sys.argv
    log = "--log" in sys.argv and not synthetic
    book = synthetic_book() if synthetic else bb.cm_book()
    lab = build(book)
    first = lab.day(int(lab.b[0]) + 1)
    twin = run(lab, "TS (twin)", None)
    bh = run(lab, "buy and hold", np.ones_like(lab.univ))
    bh.hold = lab.univ.copy()
    bh.ret, bh.pos = core.paper(book.px, bh.hold, lab.b)
    ev = study_tops(lab)
    bucket = buckets(lab, ev)
    draws = 50 if synthetic else 500

    out = [
        "# cointop-1: coin tops on the top-100 coin book, and the choice of settings",
        "",
        "Generated by `research/lib/cointop1.py`; card and reading in `research/cointop-1.md`. "
        f"Coin Metrics book of breadth-1 (dead coins included), decisions on Fridays from "
        f"{lab.day(int(lab.d[0]))} to {lab.day(int(lab.d[-1]))}, 30 bps a side. Selection set: "
        f"the book without {', '.join(c.upper() for c in TEST_COINS)}. A top is a high followed "
        "by a fall of at least 50%; it is found with hindsight and is never a rule input.",
        "",
        "## Part A: the event study",
        "",
    ]
    out += table_a1(lab, ev, twin)
    out += table_a2(lab, ev, "### A2. The shape of a fall (study tops)")

    # Part B runs (needed for A3 as well)
    results: dict[str, list[Res]] = {}
    chosen: dict[str, float] = {}
    smooth: dict[str, list[float]] = {}
    half_pick: dict[str, tuple[float, float]] = {}
    for rule, grid in RULES.items():
        rs = [run(lab, label(rule, v), condition(lab, rule, v)) for v in grid]
        results[rule] = rs
        i, sm = core.choose([r.pooled for r in rs])
        chosen[rule], smooth[rule] = grid[i], sm
        h = [halves(lab, r.ret) for r in rs]
        half_pick[rule] = (
            grid[core.choose([x[0] for x in h])[0]],
            grid[core.choose([x[1] for x in h])[0]],
        )

    out += ["### A3. How slow the twin is, and what each rule does at the same tops", ""]
    out += [
        "Trend-on tops only. `In at the top`: the rule held the coin on the day after the top. "
        "Exit columns: tops at which the rule was in. `Share of the fall sat through`: the log "
        "loss the rule took between the top and the lowest price, over the coin's whole fall "
        "(re-entries count).",
        "",
    ]
    out += A3_HEAD
    out.append(a3_row("twin (12-month rule)", top_stats(lab, ev, twin.pos, twin.pos)))
    out.append(a3_row("buy and hold", top_stats(lab, ev, bh.pos, twin.pos)))
    for rule, rs in results.items():
        for r in rs:
            mark = " (chosen)" if r.name == label(rule, chosen[rule]) else ""
            out.append(a3_row(f"`{r.name}`{mark}", top_stats(lab, ev, r.pos, twin.pos)))
    out.append("")
    for nm, sub in (
        ("near a BTC top (within 30 days)", [e for e in ev if e.near_btc]),
        ("not near a BTC top", [e for e in ev if not e.near_btc]),
    ):
        out.append(f"The twin at tops {nm}:")
        out.append("")
        out += A3_HEAD
        out.append(a3_row("twin (12-month rule)", top_stats(lab, sub, twin.pos, twin.pos)))
        out.append("")
    out += table_a4(lab, twin, synthetic, draws)
    if not synthetic:
        out += table_a5(book)

    out += [
        "## Part B: three exit rules, one setting each",
        "",
        "`Pooled` = pooled single-coin Sharpe (the selection score: one coin slot run by the "
        "rule, for the average coin). `Smoothed` = its mean with the grid neighbours'. "
        "`vs twin (p)`: difference with a one-sided bootstrap p (dates resampled for the pooled "
        "score; the protocol's paired bootstrap for the book). `Book` = the equal-slot "
        "portfolio of the selection set.",
        "",
        "| Rule | Pooled | Smoothed | Pooled vs twin (p; 90% range) | First half | Second half | "
        "Book Sharpe | Book vs twin (p) | Book worst loss | Time held | Turnover/yr |",
        "|---|---:|---:|---|---:|---:|---:|---|---:|---:|---:|",
    ]
    th = halves(lab, twin.ret)
    held = lambda r: float(r.hold.sum() / max(lab.univ.sum(), 1))  # noqa: E731
    out.append(
        f"| twin `TS` | {twin.pooled:.2f} | - | - | {th[0]:.2f} | {th[1]:.2f} | "
        f"{stats.sharpe(twin.book):.2f} | - | {stats.max_drawdown(twin.book):.0%} | "
        f"{held(twin):.0%} | {twin.turnover:.1f} |"
    )
    verdicts: dict[str, dict[str, object]] = {}
    twin_top = top_stats(lab, ev, twin.pos, twin.pos)
    for rule, rs in results.items():
        for r, sm in zip(rs, smooth[rule], strict=True):
            d, p, lo, hi = core.pooled_boot(r.ret, twin.ret, lab.mask)
            h = halves(lab, r.ret)
            bd, bp, _, _ = stats.sharpe_diff_boot(r.book, twin.book)
            is_chosen = r.name == label(rule, chosen[rule])
            nm = f"**`{r.name}` (chosen)**" if is_chosen else f"`{r.name}`"
            out.append(
                f"| {nm} | {r.pooled:.2f} | {sm:.2f} | {d:+.2f} (p={p:.2f}; {lo:+.2f}..{hi:+.2f})"
                f" | {h[0]:.2f} | {h[1]:.2f} | {stats.sharpe(r.book):.2f} | {bd:+.2f} "
                f"(p={bp:.2f}) | {stats.max_drawdown(r.book):.0%} | {held(r):.0%} | "
                f"{r.turnover:.1f} |"
            )
            if log:
                log_row(
                    f"{r.name} on the coin book (pooled single-coin {r.pooled:.2f}, vs TS "
                    f"{d:+.2f} p {p:.2f})",
                    "variant",
                    first,
                    r.book,
                    r.turnover,
                )
            if is_chosen:
                ts = top_stats(lab, ev, r.pos, twin.pos)
                works = (
                    d > 0
                    and p < 0.10
                    and h[0] > th[0]
                    and h[1] > th[1]
                    and bd >= 0
                    and ts.sat_median < twin_top.sat_median
                )
                verdicts[rule] = {
                    "setting": chosen[rule], "pooled_diff": d, "p": p, "book_diff": bd,
                    "halves_ahead": [bool(h[0] > th[0]), bool(h[1] > th[1])],
                    "sat_median": ts.sat_median, "twin_sat_median": twin_top.sat_median,
                    "works": bool(works),
                }  # fmt: skip
    if log:
        log_row(f"TS twin on the selection set (pooled single-coin {twin.pooled:.2f})",
                "baseline", first, twin.book, twin.turnover)  # fmt: skip
    out.append("")
    out += ["Chosen settings, and what each half of the sample would have chosen alone:", ""]
    out += ["| Rule | Chosen | First half alone | Second half alone | Works on the coin book? |"]
    out += ["|---|---|---|---|---|"]
    for rule in RULES:
        v = verdicts[rule]
        why = (
            f"pooled {v['pooled_diff']:+.2f} (p {v['p']:.2f}), halves ahead "
            f"{sum(v['halves_ahead'])}/2, book {v['book_diff']:+.2f}, fall sat through "  # type: ignore[arg-type]
            f"{v['sat_median']:.0%} vs twin {v['twin_sat_median']:.0%}"
        )
        out.append(
            f"| `{rule}` | `{label(rule, chosen[rule])}` | `{label(rule, half_pick[rule][0])}` | "
            f"`{label(rule, half_pick[rule][1])}` | {'**yes**' if v['works'] else 'no'}: {why} |"
        )
    out += [
        "",
        "Where each rule's result differs from the twin's, % per coin a year (log). `Falls`: "
        "between a study top and its lowest price. `Rebounds`: the 365 days after that low. "
        "Positive = the rule did better than the twin there.",
        "",
        "| Rule | Falls | Rebounds | Rest | Costs | Total |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for _rule, rs in results.items():
        for r in rs:
            dc = decompose(lab, r, twin, bucket)
            out.append(
                f"| `{r.name}` | {dc['falls']:+.1f} | {dc['rebounds']:+.1f} | {dc['rest']:+.1f} | "
                f"{dc['costs']:+.1f} | {dc['total']:+.1f} |"
            )
    dc = decompose(lab, bh, twin, bucket)
    out.append(
        f"| buy and hold (for scale) | {dc['falls']:+.1f} | {dc['rebounds']:+.1f} | "
        f"{dc['rest']:+.1f} | {dc['costs']:+.1f} | {dc['total']:+.1f} |"
    )
    out += [
        "",
        "Control: the chosen setting with its extra condition read 26 weeks late (the same "
        "time out of the market, at the wrong moments).",
        "",
        "| Rule | Pooled | Control pooled | Rule vs its control (p) | Book: rule / control |",
        "|---|---:|---:|---|---|",
    ]
    for rule, grid in RULES.items():
        r = results[rule][grid.index(chosen[rule])]
        cond = condition(lab, rule, chosen[rule])
        late = np.ones_like(cond)
        late[26:] = cond[:-26]
        ctl = run(lab, f"{r.name} 26 weeks late", late)
        d, p, _, _ = core.pooled_boot(r.ret, ctl.ret, lab.mask)
        out.append(
            f"| `{r.name}` | {r.pooled:.2f} | {ctl.pooled:.2f} | {d:+.2f} (p={p:.2f}) | "
            f"{stats.sharpe(r.book):.2f} / {stats.sharpe(ctl.book):.2f} |"
        )
        if log:
            log_row(f"{r.name} control: condition read 26 weeks late (pooled {ctl.pooled:.2f})",
                    "control", first, ctl.book, ctl.turnover)  # fmt: skip
    text = "\n".join(out).rstrip() + "\n"
    if synthetic:
        print(text)
        return
    (RESEARCH / "results" / "cointop-1-coins.md").write_text(text)
    (derived() / "chosen.json").write_text(json.dumps({"chosen": chosen, "verdicts": verdicts}))
    print(text)


def synthetic_book(days: int = 1500, n: int = 60, seed: int = 0) -> bb.Book:
    """Random-walk coins for a plumbing check: no real number can come out of this."""
    rng = np.random.default_rng(seed)
    mkt = rng.normal(0, 0.03, (days, 1))
    px = np.exp(np.cumsum(mkt + rng.normal(0, 0.05, (days, n)), axis=0))
    names = ["btc", "eth"] + [f"c{i}" for i in range(n - 2)]
    elig = xs.lag((np.arange(days)[:, None] >= 365) & np.ones((1, n), bool), 1) == 1
    up = xs.lag((xs.logret(px, 365, 0) > 0).astype(float), 1) == 1
    vol = np.exp(rng.normal(15, 1, (days, n)))
    sig = {
        "vol_growth": xs.lag(np.log(xs.roll_mean(vol, 7) / xs.roll_mean(vol, 91)), 1),
        "turnover": xs.lag(-np.log(xs.roll_mean(vol, 30)), 1),
        "size": xs.lag(-np.log(px), 1),
    }
    day0 = TRAIN_END - timedelta(days=days - 2)
    return bb.Book("cm", day0, names, px, elig, up, sig, np.full(n, 0.003), 1, 1, 1)


if __name__ == "__main__":
    main()
