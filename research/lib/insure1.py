"""insure-1: is "trend = crash insurance" solid over 1927-2025? Card: cards/crash-insurance.md.

    uv run python -I research/lib/insure1.py

Descriptive check of `tsmom12` exactly as trend-1926 ran it, no new rule. The rule's returns are
trend-1926's saved primary gym runs (research/data/runs/trend-1926/, git-ignored, copied from the
trend-1926 worktree) where they exist, and trend-tune's gym-free paper series elsewhere (the turn
of 1961/1962 and 2002-2025); the 30-industry set is paper series only. Every fall of 25% or more
(zigzag, 25% down / 25% up) is an episode; insurance = rule minus holding over peak -> trough,
rebound = the 365 days after the trough, calm = the rest. Episodes are clustered across series
(effective episodes) and tested with a sign test and a cluster bootstrap. Writes
research/results/insure-1.md. Nothing after 2025-10-31 is parsed. Rows of kind `insure-check`
go to research/tries.md once (a variant already in the file is not logged again).
"""

from __future__ import annotations

import math
import sys
import zipfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import trend_1926 as t  # noqa: E402
import trend_tune as tt  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade.data import ETF, UNIVERSE  # noqa: E402

IDEA = "insure-1"
FIRST, LAST = date(1926, 7, 1), date(2025, 10, 31)  # nothing later is parsed
START = date(1927, 7, 2)  # trend-1926's first decision
PRIMARY = (0.25, 0.25)  # fall, rise of the zigzag
SENS = ((0.20, 0.20), (0.40, 0.25))
FAST, MEDIUM = 92, 365  # calendar days peak -> trough
REBOUND = 365
DRAWS, SEED = 10_000, 0
RUNS = harness.DATA / "runs" / "trend-1926"
OUT = harness.RESEARCH / "results" / "insure-1.md"
ERAS = (
    ("1927-1961", date(1927, 7, 2), date(1961, 12, 31)),
    ("1962-2001", date(1962, 1, 1), date(2001, 12, 31)),
    ("2002-2025", date(2002, 1, 1), LAST),
)
IND30_ZIP = "french-gsy/2026-11-18/30d/30_Industry_Portfolios_daily_CSV.zip"
VW = "Average Value Weighted Returns -- Daily"


# --- data ---


@dataclass
class Series:
    name: str
    days: list[date]  # sessions with a return, from START on
    px: np.ndarray  # total-return index (holding)
    rule: np.ndarray  # rule's simple return per session (index 0: 0)
    paper: np.ndarray  # paper series' simple return per session
    pos: np.ndarray  # paper series' position earning that session's return
    rf: np.ndarray  # T-bill simple return per session
    gym_share: float = 0.0  # share of sessions taken from a saved gym run


def _lines(path: Path) -> list[str]:
    z = zipfile.ZipFile(path)
    return z.read(z.namelist()[0]).decode("latin1").splitlines()


def parse_vw(lines: Sequence[str], last: date = LAST) -> tuple[list[str], dict[date, list[float]]]:
    """The value-weighted daily block of an industry file: names, date -> returns (NaN missing)."""
    head = next(i for i, x in enumerate(lines) if x.strip() == VW)
    names = [x.strip() for x in lines[head + 1].split(",")][1:]
    rows = {
        d: [math.nan if x <= -99 else x / 100 for x in v]
        for d, v in t._rows(lines[head + 2 :], len(names) + 1, last)
    }
    return names, rows


def infer_pos(ret: np.ndarray, bar: np.ndarray, cost: float) -> np.ndarray:
    """The paper series' position from its returns: ret = pos * bar - cost * flip."""
    pos = np.zeros(len(ret))
    for i in range(1, len(ret)):
        fit1 = min(abs(ret[i] - bar[i]), abs(ret[i] - bar[i] + cost)) < 1e-12
        fit0 = min(abs(ret[i]), abs(ret[i] + cost)) < 1e-12
        pos[i] = pos[i - 1] if fit1 == fit0 else (1.0 if fit1 else 0.0)
    return pos


def gym_runs(name: str) -> list[tuple[dict[date, float], date]]:
    """Both eras' saved gym equity (calendar days) and the first day to use each from: 14 days
    in (the gym starts in cash and needs a Friday to buy; a continuous rule would already hold)."""
    out = []
    for prefix in ("F", "F62"):
        path = RUNS / f"tsmom12@{prefix}-{name}.train.csv"
        if not path.exists():
            raise FileNotFoundError(f"{path}: copy trend-1926's saved runs (see docstring)")
        rows = [x.split(",") for x in path.read_text().splitlines()[1:]]
        eq = {date.fromisoformat(a): float(b) for a, b in rows}
        out.append((eq, min(eq) + timedelta(days=14)))
    return out


def build(name: str, days: list[date], ret: np.ndarray, rf: dict[date, float],
          gym: list[tuple[dict[date, float], date]] | None) -> Series:  # fmt: skip
    sym = f"I1-{name}"
    UNIVERSE[sym] = ETF  # research process only; src/ is untouched
    bars = t.bars(days, ret)
    panel = harness.Panel({sym: bars})
    p = tt.paper(panel, sym, (12,))
    bdays = [b.date for b in bars]
    close = np.array([b.close for b in bars])
    bar = np.zeros(len(close))
    bar[1:] = close[1:] / close[:-1] - 1
    pos = infer_pos(p.ret[12], bar, 0.0002)
    k = next(i for i, d in enumerate(bdays) if d >= START)
    sd = bdays[k:]
    paper = p.ret[12][k:].copy()
    paper[0] = 0.0
    rule = paper.copy()
    used = 0
    for eq, first in gym or []:
        for i in range(1, len(sd)):
            if sd[i - 1] >= first and sd[i] in eq and sd[i - 1] in eq:
                rule[i] = eq[sd[i]] / eq[sd[i - 1]] - 1
                used += 1
    px = close[k:] / close[k]
    return Series(name, sd, px, rule, paper, pos[k:], np.array([rf.get(d, 0.0) for d in sd]),
                  used / max(len(sd) - 1, 1))  # fmt: skip


def load_primary() -> list[Series]:
    root = cache_root()
    snap = sorted(p for p in (root / "french").iterdir() if p.is_dir())[-1]
    fac = t.parse_factors(_lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), LAST)
    ind = t.parse_industries(_lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), LAST)
    days = sorted(d for d in fac if d >= FIRST)
    rf = {d: fac[d][1] for d in days}
    out = [build(t.MKT, days, np.array([fac[d][0] for d in days]), rf, gym_runs(t.MKT))]
    for j, n in enumerate(t.INDUSTRIES):
        r = np.array([ind[d][j] for d in days])
        keep = ~np.isnan(r)
        dd = [d for d, ok in zip(days, keep, strict=True) if ok]
        out.append(build(n, dd, r[keep], rf, gym_runs(n)))
    return out


def load_ind30(rf: dict[date, float]) -> list[Series]:
    names, rows = parse_vw(_lines(cache_root() / IND30_ZIP))
    days = sorted(d for d in rows if d >= FIRST)
    out = []
    for j, n in enumerate(names):
        r = np.array([rows[d][j] for d in days])
        keep = ~np.isnan(r)
        dd = [d for d, ok in zip(days, keep, strict=True) if ok]
        out.append(build(f"30-{n}", dd, r[keep], rf, None))
    return out


# --- episodes ---


@dataclass
class Episode:
    series: str
    peak: date
    trough: date
    depth: float
    hold: float  # log points, holding, (peak, trough]
    rule: float
    ins: float  # I
    rebound: float  # B
    ins_tb: float = 0.0
    net_tb: float = 0.0
    cluster: int = -1
    linked: int = -1
    idx: tuple[int, int, int] = (0, 0, 0)  # session index of peak, trough, rebound end

    @property
    def days(self) -> int:
        return (self.trough - self.peak).days

    @property
    def share(self) -> float:
        return self.ins / abs(self.hold) if self.hold else 0.0

    @property
    def net(self) -> float:
        return self.ins + self.rebound


def zigzag(px: np.ndarray, down: float, up: float) -> tuple[list[tuple[int, int]], int | None]:
    """Confirmed (peak, trough) index pairs, and the peak of an unfinished fall at the end."""
    out: list[tuple[int, int]] = []
    falling, pk, tr = False, 0, 0
    for i in range(1, len(px)):
        if not falling:
            if px[i] > px[pk]:
                pk = i
            elif px[i] <= px[pk] * (1 - down):
                falling, tr = True, i
        else:
            if px[i] < px[tr]:
                tr = i
            elif px[i] >= px[tr] * (1 + up):
                out.append((pk, tr))
                falling, pk = False, i
    return out, (pk if falling else None)


@dataclass
class Scored:
    s: Series
    eps: list[Episode]
    calm: float  # C, log points
    calm_tb: float
    total: float
    open_peak: date | None
    calm_by_era: dict[str, float] = field(default_factory=dict)
    calm_tb_by_era: dict[str, float] = field(default_factory=dict)
    in_mask: np.ndarray = field(default_factory=lambda: np.zeros(0, dtype=bool))


def score(s: Series, down: float, up: float, rule: np.ndarray | None = None) -> Scored:
    r = s.rule if rule is None else rule
    hold_lr = np.zeros(len(s.px))
    hold_lr[1:] = np.log(s.px[1:] / s.px[:-1])
    d = 100 * (np.log1p(r) - hold_lr)
    d[0] = 0.0
    d_tb = 100 * (np.log1p(r + (1 - s.pos) * s.rf) - hold_lr)
    d_tb[0] = 0.0
    cum, cum_tb = np.cumsum(d), np.cumsum(d_tb)
    pairs, open_pk = zigzag(s.px, down, up)
    mask = np.zeros(len(d), dtype=bool)
    ords = np.array([x.toordinal() for x in s.days])
    eps = []
    for j, (a, b) in enumerate(pairs):
        lim = s.days[b].toordinal() + REBOUND
        e = int(np.searchsorted(ords, lim, side="right")) - 1
        if j + 1 < len(pairs):
            e = min(e, pairs[j + 1][0])
        hold = 100 * math.log(s.px[b] / s.px[a])
        ins = float(cum[b] - cum[a])
        eps.append(Episode(
            s.name, s.days[a], s.days[b], 1 - s.px[b] / s.px[a], hold, hold + ins, ins,
            float(cum[e] - cum[b]), float(cum_tb[b] - cum_tb[a]), float(cum_tb[e] - cum_tb[a]),
            idx=(a, b, e),
        ))  # fmt: skip
        mask[a + 1 : e + 1] = True
    calm_d, calm_tb_d = np.where(mask, 0.0, d), np.where(mask, 0.0, d_tb)
    total = float(cum[-1])
    calm = float(calm_d.sum())
    check = sum(e.ins + e.rebound for e in eps) + calm
    if abs(check - total) > 1e-6:
        raise AssertionError(f"{s.name}: decomposition {check} != total {total}")
    by, by_tb = {}, {}
    for key, lo, hi in ERAS:
        m = (ords >= lo.toordinal()) & (ords <= hi.toordinal())
        by[key], by_tb[key] = float(calm_d[m].sum()), float(calm_tb_d[m].sum())
    return Scored(s, eps, calm, float(calm_tb_d.sum()), total,
                  s.days[open_pk] if open_pk is not None else None, by, by_tb, mask)  # fmt: skip


# --- clusters and tests ---


def link(eps: Sequence[Episode]) -> list[list[Episode]]:
    """Single linkage on overlapping [peak, trough] windows."""
    out: list[list[Episode]] = []
    end = date.min
    for e in sorted(eps, key=lambda x: x.peak):
        if out and e.peak <= end:
            out[-1].append(e)
            end = max(end, e.trough)
        else:
            out.append([e])
            end = e.trough
    return out


def market_anchored(eps: Sequence[Episode], market: str) -> list[list[Episode]]:
    mk = sorted((e for e in eps if e.series == market), key=lambda x: x.peak)
    groups: list[list[Episode]] = [[e] for e in mk]
    rest = []
    for e in eps:
        if e.series == market:
            continue
        home = next((g for g in groups if g[0].peak <= e.trough <= g[0].trough), None)
        home = home or next((g for g in groups if g[0].peak <= e.peak <= g[0].trough), None)
        if home is None:
            rest.append(e)
        else:
            home.append(e)
    return sorted(groups + link(rest), key=lambda g: min(x.peak for x in g))


def sign_test(vals: Sequence[float]) -> tuple[int, int, float]:
    v = [x for x in vals if x != 0]
    n, k = len(v), sum(1 for x in v if x > 0)
    p = sum(math.comb(n, j) for j in range(k, n + 1)) / 2**n if n else 1.0
    return k, n, p


def boot(vals: Sequence[float]) -> tuple[float, float, float, float]:
    """Mean, one-sided p (share of draws <= 0), 90% range of the mean, cluster bootstrap."""
    x = np.asarray(vals, dtype=float)
    rng = np.random.default_rng(SEED)
    m = x[rng.integers(0, len(x), size=(DRAWS, len(x)))].mean(axis=1)
    lo, hi = np.quantile(m, [0.05, 0.95])
    return float(x.mean()), float((m <= 0).mean()), float(lo), float(hi)


def cmean(g: Sequence[Episode], f: Callable[[Episode], float]) -> float:
    return float(np.mean([f(e) for e in g]))


def test_line(
    label: str, groups: Sequence[Sequence[Episode]], f: Callable[[Episode], float]
) -> str:
    vals = [cmean(g, f) for g in groups]
    k, n, p = sign_test(vals)
    m, bp, lo, hi = boot(vals)
    return f"| {label} | {n} | {k} | {p:.2g} | {m:+.1f} | {bp:.3f} | {lo:+.1f} to {hi:+.1f} |"


TEST_HEAD = [
    "| Test | Clusters (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p | 90% range |",
    "|---|---:|---:|---:|---:|---:|---|",
]


def verdict(ins_a: str, ins_l: str, net_a: str) -> str:
    def ok(line: str) -> bool:
        cells = [c.strip() for c in line.strip("|").split("|")]
        return float(cells[3]) < 0.05 and float(cells[5]) < 0.05

    if not (ok(ins_a) and ok(ins_l)):
        return "Insurance not shown"
    return (
        "Insurance real, and kept after the rebound"
        if ok(net_a)
        else "Insurance real, handed back in the rebound"
    )


# --- report ---


def sharpe_row(s: Series) -> tuple[float, float, float, float]:
    """Calendar-day Sharpe (365), total return, max drawdown, position flips a year."""
    first, last = s.days[0], s.days[-1]
    n = (last - first).days + 1
    cal = np.zeros(n)
    for d, x in zip(s.days[1:], s.rule[1:], strict=True):
        cal[(d - first).days] = x
    sd = cal[1:].std()
    sh = float(cal[1:].mean() / sd * math.sqrt(365)) if sd > 0 else 0.0
    eq = np.cumprod(1 + s.rule)
    mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
    flips = float(np.abs(np.diff(s.pos)).sum()) / (n / 365)
    return sh, float(eq[-1] - 1), mdd, flips


def log_tries(sets: Sequence[tuple[str, Sequence[Series]]]) -> int:
    text = harness.TRIES.read_text()
    rows = []
    for tag, ser in sets:
        for s in ser:
            v = f"tsmom12@{tag}-{s.name.removeprefix('30-')}"
            if f"| {IDEA} | {v} |" in text:
                continue
            sh, tot, mdd, fl = sharpe_row(s)
            rows.append(
                f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | insure-check | train | "
                f"{s.days[0]} | {s.days[-1]} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
            )
    with harness.TRIES.open("a") as f:
        f.writelines(rows)
    return len(rows)


def maxdd(x: np.ndarray) -> float:
    return float((1 - x / np.maximum.accumulate(x)).max())


def report(primary: list[Series], ind30: list[Series]) -> str:
    out = [
        "# insure-1: crash insurance of `tsmom12`, 1927-2025",
        "",
        "Card: `cards/crash-insurance.md`. Written by `lib/insure1.py`. Log points = 100 x natural",
        "log; every number is rule minus holding unless said otherwise. Cash earns 0 unless the",
        "column says T-bill.",
        "",
    ]
    sc = [score(s, *PRIMARY) for s in primary]
    eps = [e for x in sc for e in x.eps]
    mk = t.MKT

    # data check
    out += ["## Data and splice check", ""]
    out += [
        "| Series | Sessions | From | To | Share from saved gym runs |",
        "|---|---:|---|---|---:|",
    ]
    for s in primary:
        out.append(f"| {s.name} | {len(s.days)} | {s.days[0]} | {s.days[-1]} | {s.gym_share:.1%} |")
    pp = [score(s, *PRIMARY, rule=s.paper) for s in primary]
    worst = 0.0
    for a, b in zip(sc, pp, strict=True):
        for x, y in zip(a.eps, b.eps, strict=True):
            if x.trough.year <= 2001:
                worst = max(worst, abs(x.ins - y.ins))
    out += ["", f"Largest difference in one episode's insurance, gym splice against paper series "
            f"alone (episodes ending by 2001): {worst:.2f} log points.", ""]  # fmt: skip

    # per series
    out += ["## Per series (25% episodes)", ""]
    out += [
        "| Series | Episodes | Open fall at end (peak) | Sum I | Sum B (rebound) | C (calm) | "
        "Total | Premium P | P with T-bill | Worst loss rule / hold |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    def prem(si: float, sb: float, c: float) -> str:
        return f"{-(sb + c) / si:.2f}" if si > 0 else "no insurance"

    for x in sc:
        si, sb = sum(e.ins for e in x.eps), sum(e.rebound for e in x.eps)
        si_tb = sum(e.ins_tb for e in x.eps)
        sb_tb = sum(e.net_tb - e.ins_tb for e in x.eps)
        out.append(
            f"| {x.s.name} | {len(x.eps)} | {x.open_peak or '-'} | {si:+.0f} | {sb:+.0f} | "
            f"{x.calm:+.0f} | {x.total:+.0f} | {prem(si, sb, x.calm)} | "
            f"{prem(si_tb, sb_tb, x.calm_tb)} | "
            f"{maxdd(np.cumprod(1 + x.s.rule)):.0%} / {maxdd(x.s.px):.0%} |"
        )
    si = sum(e.ins for e in eps)
    sb = sum(e.rebound for e in eps)
    c = sum(x.calm for x in sc)
    si_tb = sum(e.ins_tb for e in eps)
    sb_tb = sum(e.net_tb - e.ins_tb for e in eps)
    c_tb = sum(x.calm_tb for x in sc)
    years = (LAST - START).days / 365.25
    out += [
        f"| **pooled, 11** | {len(eps)} | | {si:+.0f} | {sb:+.0f} | {c:+.0f} | "
        f"{sum(x.total for x in sc):+.0f} | {prem(si, sb, c)} | {prem(si_tb, sb_tb, c_tb)} | |",
        "",
        f"Per series and year ({years:.1f} years): insurance paid out {si / 11 / years:+.2f}, "
        f"rebound {sb / 11 / years:+.2f}, calm {c / 11 / years:+.2f} log points a year "
        f"(T-bill reading: {si_tb / 11 / years:+.2f}, {sb_tb / 11 / years:+.2f}, "
        f"{c_tb / 11 / years:+.2f}).",
        "",
    ]

    # per era
    out += ["## Premium by era (pooled over the 11 series)", ""]
    out += [
        "| Era | Episodes (by peak) | Sum I | Sum B | C | Premium P | P with T-bill |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for key, lo, hi in ERAS:
        ee = [e for e in eps if lo <= e.peak <= hi]
        a, b = sum(e.ins for e in ee), sum(e.rebound for e in ee)
        a_tb, b_tb = sum(e.ins_tb for e in ee), sum(e.net_tb - e.ins_tb for e in ee)
        cc, cc_tb = sum(x.calm_by_era[key] for x in sc), sum(x.calm_tb_by_era[key] for x in sc)
        out.append(
            f"| {key} | {len(ee)} | {a:+.0f} | {b:+.0f} | {cc:+.0f} | {prem(a, b, cc)} | "
            f"{prem(a_tb, b_tb, cc_tb)} |"
        )
    out.append("")

    # tests
    anch, lnk = market_anchored(eps, mk), link(eps)
    for i, g in enumerate(anch):
        for e in g:
            e.cluster = i
    for i, g in enumerate(lnk):
        for e in g:
            e.linked = i
    a_i = test_line("I, market-anchored", anch, lambda e: e.ins)
    l_i = test_line("I, linked", lnk, lambda e: e.ins)
    a_n = test_line("N = I + B, market-anchored", anch, lambda e: e.net)
    l_n = test_line("N = I + B, linked", lnk, lambda e: e.net)
    out += ["## Tests across effective episodes (primary set, 25%)", ""]
    out += TEST_HEAD + [
        a_i,
        l_i,
        a_n,
        l_n,
        test_line("Share avoided S, market-anchored", anch, lambda e: e.share),
        test_line("I with T-bill, market-anchored", anch, lambda e: e.ins_tb),
        test_line("N with T-bill, market-anchored", anch, lambda e: e.net_tb),
        test_line(
            "Market alone, I (its own episodes)",
            [[e] for e in eps if e.series == mk],
            lambda e: e.ins,
        ),  # fmt: skip
        test_line("Market alone, N", [[e] for e in eps if e.series == mk], lambda e: e.net),
        "",
        f"Episodes: {len(eps)}; market-anchored clusters: {len(anch)}; linked clusters: "
        f"{len(lnk)}. The share avoided S is a fraction (shown x 1, not log points).",
        "",
        f"**Verdict by the card: {verdict(a_i, l_i, a_n)}.**",
        "",
    ]

    # clusters
    out += ["## Market-anchored clusters", ""]
    out += [
        "| # | First peak | Last trough | Episodes | Series | Mean depth | Mean I | Mean S "
        "| Mean B | Mean N | Linked cluster |",
        "|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for i, g in enumerate(anch):
        names = ", ".join(sorted({e.series for e in g}, key=lambda n: (n != mk, n)))
        out.append(
            f"| {i + 1} | {min(e.peak for e in g)} | {max(e.trough for e in g)} | {len(g)} | "
            f"{names} | {cmean(g, lambda e: e.depth):.0%} | {cmean(g, lambda e: e.ins):+.0f} | "
            f"{cmean(g, lambda e: e.share):+.2f} | {cmean(g, lambda e: e.rebound):+.0f} | "
            f"{cmean(g, lambda e: e.net):+.0f} | {g[0].linked + 1} |"
        )
    out.append("")
    out += ["Linked clusters (conservative): spans", ""]
    out += [
        "| # | First peak | Last trough | Episodes | Mean I | Mean N |",
        "|---:|---|---|---:|---:|---:|",
    ]
    for i, g in enumerate(lnk):
        out.append(
            f"| {i + 1} | {min(e.peak for e in g)} | {max(e.trough for e in g)} | {len(g)} | "
            f"{cmean(g, lambda e: e.ins):+.0f} | {cmean(g, lambda e: e.net):+.0f} |"
        )
    out.append("")

    # speed
    out += ["## When it fails: speed of the fall (all 11 series, episode level)", ""]
    out += [
        "| Peak to trough | Episodes | Mean depth | Mean I | I > 0 | Mean S | Mean B | Mean N | "
        "N > 0 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, lo, hi in (
        (f"fast, <= {FAST} days", 0, FAST),
        (f"medium, {FAST + 1}-{MEDIUM}", FAST + 1, MEDIUM),
        (f"slow, > {MEDIUM}", MEDIUM + 1, 10**6),
    ):
        ee = [e for e in eps if lo <= e.days <= hi]
        if not ee:
            out.append(f"| {label} | 0 | | | | | | | |")
            continue
        out.append(
            f"| {label} | {len(ee)} | {cmean(ee, lambda e: e.depth):.0%} | "
            f"{cmean(ee, lambda e: e.ins):+.1f} | {sum(e.ins > 0 for e in ee)} | "
            f"{cmean(ee, lambda e: e.share):+.2f} | {cmean(ee, lambda e: e.rebound):+.1f} | "
            f"{cmean(ee, lambda e: e.net):+.1f} | {sum(e.net > 0 for e in ee)} |"
        )
    out.append("")

    # market list
    out += ["## The market's episodes", ""]
    out += [
        "| Peak | Trough | Days | Depth | Holding, log pts | Rule, log pts | I | S | B | N | "
        "I with T-bill | Industries in cluster |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for e in eps:
        if e.series != mk:
            continue
        n_ind = len(anch[e.cluster]) - 1
        out.append(
            f"| {e.peak} | {e.trough} | {e.days} | {e.depth:.0%} | {e.hold:+.0f} | "
            f"{e.rule:+.0f} | {e.ins:+.0f} | {e.share:+.2f} | {e.rebound:+.0f} | {e.net:+.0f} | "
            f"{e.ins_tb:+.0f} | {n_ind} |"
        )
    out.append("")

    # sensitivity
    out += ["## Sensitivity: other thresholds (description)", ""]
    out += ["| Fall / rise | Set | Episodes |" + TEST_HEAD[0].split("|", 2)[2]]
    out += ["|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for down, up in (PRIMARY, *SENS):
        ss = [score(s, down, up) for s in primary]
        ee = [e for x in ss for e in x.eps]
        for lab, groups, f in (
            ("I, anchored", market_anchored(ee, mk), lambda e: e.ins),
            ("I, linked", link(ee), lambda e: e.ins),
            ("N, anchored", market_anchored(ee, mk), lambda e: e.net),
        ):
            cells = test_line(lab, groups, f).strip("|").split("|")
            out.append(f"| {down:.0%} / {up:.0%} | {cells[0].strip()} | {len(ee)} |"
                       + "|".join(cells[1:]) + "|")  # fmt: skip
        si_, sb_, c_ = (sum(e.ins for e in ee), sum(e.rebound for e in ee),
                        sum(x.calm for x in ss))  # fmt: skip
        out.append(f"| {down:.0%} / {up:.0%} | premium P | {len(ee)} | {prem(si_, sb_, c_)} "
                   "| | | | | |")  # fmt: skip
    out.append("")

    # 30 industries
    s30 = [score(s, *PRIMARY) for s in ind30]
    e30 = [e for x in s30 for e in x.eps] + [e for e in eps if e.series == mk]
    an30, ln30 = market_anchored(e30, mk), link(e30)
    a30, l30 = sum(e.ins for x in s30 for e in x.eps), sum(e.rebound for x in s30 for e in x.eps)
    c30 = sum(x.calm for x in s30)
    out += ["## Robustness: 30 industries (paper series), market episodes as anchors", ""]
    out += TEST_HEAD + [
        test_line("I, market-anchored", an30, lambda e: e.ins),
        test_line("I, linked", ln30, lambda e: e.ins),
        test_line("N, market-anchored", an30, lambda e: e.net),
        "",
        f"Industry episodes: {len(e30) - sum(e.series == mk for e in eps)}; market-anchored "
        f"clusters: {len(an30)}; linked: {len(ln30)}. Premium P pooled over the 30: "
        f"{prem(a30, l30, c30)} (sum I {a30:+.0f}, "
        f"sum B {l30:+.0f}, C {c30:+.0f}).",
        "",
    ]
    return "\n".join(out) + "\n"


# --- card 2: exposure-matched controls ---

ROTATIONS = 1000


@dataclass
class Ctl:
    s_mean: float  # mean over market-anchored clusters of the share avoided S
    n_mean: float  # mean over clusters of N
    prem: float  # pooled premium P


def control_stats(
    rets: Sequence[np.ndarray], hl: Sequence[np.ndarray], eps: Sequence[Sequence[Episode]],
    clusters: Sequence[Sequence[tuple[int, Episode]]],
) -> Ctl:  # fmt: skip
    """Rule-minus-holding stats of one set of return series on card 1's episodes."""
    ins: dict[int, float] = {}
    net: dict[int, float] = {}
    sum_i, total = 0.0, 0.0
    for j, (r, h, ee) in enumerate(zip(rets, hl, eps, strict=True)):
        cum = np.cumsum(100 * (np.log1p(r) - h))
        total += float(cum[-1])
        for e in ee:
            a, b, x = e.idx
            ins[id(e)] = float(cum[b] - cum[a])
            net[id(e)] = float(cum[x] - cum[a])
            sum_i += ins[id(e)]
        del j
    s_vals = [np.mean([ins[id(e)] / abs(e.hold) for _, e in g]) for g in clusters]
    n_vals = [np.mean([net[id(e)] for _, e in g]) for g in clusters]
    prem = -(total - sum_i) / sum_i if sum_i > 0 else math.inf
    return Ctl(float(np.mean(s_vals)), float(np.mean(n_vals)), prem)


def card2(primary: list[Series]) -> str:
    if any(s.days != primary[0].days for s in primary):
        raise ValueError("card 2 needs one session calendar for the 11 series")
    sc = [score(s, *PRIMARY) for s in primary]
    eps = [x.eps for x in sc]
    anch = market_anchored([e for ee in eps for e in ee], t.MKT)
    clusters = [[(0, e) for e in g] for g in anch]
    hl = []
    bar = []
    for s in primary:
        h = np.zeros(len(s.px))
        h[1:] = np.log(s.px[1:] / s.px[:-1])
        hl.append(h)
        b = np.zeros(len(s.px))
        b[1:] = s.px[1:] / s.px[:-1] - 1
        bar.append(b)
    rule = control_stats([s.paper for s in primary], hl, eps, clusters)
    xs = [float(s.pos[1:].mean()) for s in primary]
    fixed = control_stats([x * b for x, b in zip(xs, bar, strict=True)], hl, eps, clusters)
    n = len(primary[0].px)
    rng = np.random.default_rng(SEED)
    rots = []
    for _ in range(ROTATIONS):
        k = int(rng.integers(365, n - 365))
        rr = []
        for s, b in zip(primary, bar, strict=True):
            p = np.roll(s.pos, k)
            flips = np.abs(np.diff(p, prepend=p[0]))
            r = p * b - 0.0002 * flips
            r[0] = 0.0
            rr.append(r)
        rots.append(control_stats(rr, hl, eps, clusters))
    rs = np.array([c.s_mean for c in rots])
    rn = np.array([c.n_mean for c in rots])
    rp = np.array([c.prem for c in rots])
    p_s = float((rs >= rule.s_mean).mean())
    p_p = float((rp <= rule.prem).mean())
    p_n = float((rn >= rule.n_mean).mean())
    if p_s < 0.05 and p_p < 0.05 and rule.prem < fixed.prem:
        verdict2 = "Timing, not just exposure"
    elif p_s >= 0.10 and p_p >= 0.10:
        verdict2 = "Exposure, not timing"
    else:
        verdict2 = "In between"

    def q(a: np.ndarray) -> str:
        lo, mid, hi = np.quantile(a, [0.05, 0.5, 0.95])
        return f"{mid:+.2f} ({lo:+.2f} to {hi:+.2f})"

    out = [
        "## Card 2: timing or just lower exposure? (exposure-matched controls)",
        "",
        "Same 11 series, card 1's 25% episodes and market-anchored clusters, cash at 0. The rule "
        "here is its paper series. Rotations: median (5th to 95th percentile) of 1,000.",
        "",
        "| | Mean cluster S (share avoided) | Mean cluster N, log pts | Pooled premium P |",
        "|---|---:|---:|---:|",
        f"| `tsmom12` (paper series) | {rule.s_mean:+.2f} | {rule.n_mean:+.1f} | {rule.prem:.2f} |",
        f"| Fixed exposure (x = rule's average position, mean {np.mean(xs):.0%}) | "
        f"{fixed.s_mean:+.2f} | {fixed.n_mean:+.1f} | {fixed.prem:.2f} |",
        f"| Random timing (rotated positions) | {q(rs)} | {q(rn)} | {q(rp)} |",
        f"| p: rotations at least as good as the rule | {p_s:.3f} | {p_n:.3f} | {p_p:.3f} |",
        "",
        "Average position per series: "
        + ", ".join(f"{s.name} {x:.0%}" for s, x in zip(primary, xs, strict=True))
        + ".",
        "",
        f"**Verdict by card 2: {verdict2}.**",
        "",
    ]
    return "\n".join(out) + "\n"


def main() -> None:
    primary = load_primary()
    rf = dict(zip(primary[0].days, primary[0].rf, strict=True))
    ind30 = load_ind30(rf)
    OUT.write_text(report(primary, ind30) + card2(primary))
    n = log_tries([("insure", primary), ("insure30", ind30)])
    print(f"wrote {OUT}; {n} new tries.md rows")


if __name__ == "__main__":
    main()
