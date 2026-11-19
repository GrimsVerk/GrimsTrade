"""Trend 1926: `tsmom12` against holding on US stocks 1926-1961. Card: research/trend-1926.md.

    uv run python -I research/lib/trend_1926.py

Ken French's daily market and 10 industry returns (cache root from research/macro.local.json or
GRIMSTRADE_DATA; read as data, never written) become total-return bars, and the protocol's own
twins run on them through the unchanged gym. Rows go to research/tries.md the moment a
configuration runs; a configuration whose equity file exists under the git-ignored
research/data/runs/ is re-scored without a new row. Nothing after 1961-12-31 is parsed.
"""

from __future__ import annotations

import math
import os
import sys
import zipfile
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import harness  # noqa: E402
import stats  # noqa: E402
import trend_tune as tt  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade import gym  # noqa: E402
from grimstrade.data import ETF, UNIVERSE, Bar  # noqa: E402

IDEA = "trend-1926"
MARK = "<!-- tables below this line are written by lib/trend_1926.py -->"
FIRST, LAST = date(1926, 7, 1), date(1961, 12, 31)
START = FIRST + timedelta(days=366)  # first decision: a year after the first bar
INDUSTRIES = ["NoDur", "Durbl", "Manuf", "Enrgy", "HiTec", "Telcm", "Shops", "Hlth", "Utils",
              "Other"]  # fmt: skip
MKT = "Mkt"
BOOK = "ind10"
VW_BLOCK = "Average Value Weighted Returns -- Daily"
CONFIGS: dict[str, tuple[bool, float, str]] = {
    # suffix: (late fill, one-way cost, tries.md kind)
    "": (False, 0.0002, "baseline"),
    "-late": (True, 0.0002, "robustness"),
    "-10bps": (False, 0.0010, "robustness"),
    "-50bps": (False, 0.0050, "robustness"),
}
DRAWS = 2000
ERA = os.environ.get("TREND_ERA", "1926")  # "1962": card 2, 1962-2001
PREFIX, RESULT = "F", "trend-1926"
if ERA == "1962":
    FIRST, LAST = date(1961, 1, 1), date(2001, 12, 31)
    START = FIRST + timedelta(days=366)
    PREFIX, RESULT = "F62", "trend-1926-era2"


def sym(name: str) -> str:
    return f"{PREFIX}-{name}"


# --- loader (raw cache, read only) ---


@dataclass
class Raw:
    snapshot: str
    days: list[date]
    ret: dict[str, np.ndarray]  # simple daily returns by series name; NaN where missing
    rf: np.ndarray  # simple daily T-bill return


def _rows(lines: Sequence[str], ncols: int, last: date) -> Iterator[tuple[date, list[float]]]:
    """Daily rows of one block: stops at the first blank line after data, or after `last`."""
    started = False
    for line in lines:
        cells = [x.strip() for x in line.split(",")]
        if len(cells) == ncols and len(cells[0]) == 8 and cells[0].isdigit():
            d = date(int(cells[0][:4]), int(cells[0][4:6]), int(cells[0][6:]))
            if d > last:
                return  # nothing later is parsed
            started = True
            yield d, [float(x) for x in cells[1:]]
        elif started:
            return


def _lines(path: Path) -> list[str]:
    z = zipfile.ZipFile(path)
    return z.read(z.namelist()[0]).decode("latin1").splitlines()


def parse_factors(lines: Sequence[str], last: date = LAST) -> dict[date, tuple[float, float]]:
    """date -> (market total return, T-bill return), simple, from the daily factors file."""
    head = next(i for i, x in enumerate(lines) if x.replace(" ", "") == ",Mkt-RF,SMB,HML,RF")
    return {d: ((v[0] + v[3]) / 100, v[3] / 100) for d, v in _rows(lines[head + 1 :], 5, last)}


def parse_industries(lines: Sequence[str], last: date = LAST) -> dict[date, list[float]]:
    """date -> the ten value-weighted industry returns (NaN where marked missing)."""
    head = next(i for i, x in enumerate(lines) if x.strip() == VW_BLOCK)
    names = [x.strip() for x in lines[head + 1].split(",")][1:]
    if names != INDUSTRIES:
        raise ValueError(f"unexpected industry columns: {names}")
    return {
        d: [math.nan if x <= -99 else x / 100 for x in v]
        for d, v in _rows(lines[head + 2 :], 11, last)
    }


def load(root: Path | None = None) -> Raw:
    root = root or cache_root()
    snap = sorted(p for p in (root / "french").iterdir() if p.is_dir())[-1]
    fac = parse_factors(_lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), LAST)
    ind = parse_industries(_lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), LAST)
    days = sorted(d for d in fac if d >= FIRST)
    if days != sorted(d for d in ind if d >= FIRST):
        raise ValueError("the market and industry files disagree on the sessions")
    ret = {MKT: np.array([fac[d][0] for d in days])}
    for j, name in enumerate(INDUSTRIES):
        ret[name] = np.array([ind[d][j] for d in days])
    return Raw(snap.name, days, ret, np.array([fac[d][1] for d in days]))


def bars(days: Sequence[date], ret: np.ndarray, late: bool = False) -> list[Bar]:
    """Total-return bars (100 before the first return). Primary: open = previous close, so the
    gym's next-open fill is at the close the signal saw. `late`: open = the day's own close, so
    the fill comes one session later. A missing return gives no bar."""
    out: list[Bar] = []
    prev = 100.0
    for d, x in zip(days, ret, strict=True):
        if math.isnan(x):
            continue
        cl = prev * (1 + float(x))
        o = cl if late else prev
        out.append(Bar(d, o, max(o, cl), min(o, cl), cl, 0.0))
        prev = cl
    return out


def universe(raw: Raw, names: Sequence[str], label: str, late: bool = False) -> c.Ctx:
    hist = {}
    for n in names:
        UNIVERSE[sym(n)] = ETF  # research process only; src/ is untouched
        hist[sym(n)] = bars(raw.days, raw.ret[n], late)
    end = max(b[-1].date for b in hist.values()) - timedelta(days=1)
    return c.Ctx(sym(label), "train", hist, harness.Panel(hist), START, end)


# --- runs ---


def rule() -> c.ResearchStrategy:
    return c.weekly(c.slots(c.tsmom_signal))


def hold() -> c.ResearchStrategy:
    return c.weekly(c.equal_weight)


def run_once(variant: str, strategy: c.ResearchStrategy, u: c.Ctx, kind: str, cost: float) -> c.Run:
    """Run and log a configuration once; later calls re-score it without a new `tries.md` row."""
    tag = f"{variant}@{u.name}"
    done = (harness.DATA / "runs" / IDEA / f"{tag}.train.csv").exists()
    costs = {**gym.COSTS, ETF: gym.Costs(fee=0.0, slip=cost)}
    return harness.run(
        IDEA, tag, strategy, kind=kind, period="train", panel=u.panel, history=u.hist,
        start=u.start, end=u.end, costs=costs, log=not done and not c.DRY,
    )  # fmt: skip


@dataclass
class Pair:
    name: str
    rule: c.Run
    hold: c.Run


def pair(raw: Raw, names: Sequence[str], label: str, suffix: str) -> tuple[Pair, c.Ctx]:
    late, cost, kind = CONFIGS[suffix]
    u = universe(raw, names, label, late)
    twin = "hold" if len(names) == 1 else "equal-weight"
    h = run_once(f"{twin}{suffix}", hold(), u, kind, cost)
    r = run_once(f"tsmom12{suffix}", rule(), u, kind, cost)
    return Pair(label, r, h), u


# --- windows ---


@dataclass(frozen=True)
class Window:
    key: str
    label: str
    lo: date = date.min
    hi: date = date.max
    drop: tuple[tuple[date, date], ...] = ()

    def mask(self, ords: np.ndarray) -> np.ndarray:
        m = (ords >= self.lo.toordinal()) & (ords <= self.hi.toordinal())
        for a, b in self.drop:
            m &= ~((ords >= a.toordinal()) & (ords <= b.toordinal()))
        return np.asarray(m, dtype=bool)


WHOLE = Window("whole", "1927-07 to 1961-12")
WINDOWS = [
    WHOLE,
    Window("1927-45", "1927-07 to 1945-12", hi=date(1945, 12, 31)),
    Window("1946-61", "1946-01 to 1961-12", lo=date(1946, 1, 1)),
    Window("d1", "without 1929-1932", drop=((date(1929, 1, 1), date(1932, 12, 31)),)),
    Window("d2", "without 1929-09-03 to 1932-07-08", drop=((date(1929, 9, 3), date(1932, 7, 8)),)),
    Window("d3", "1933-01 to 1961-12", lo=date(1933, 1, 1)),
]
KEYS = ("1927-45", "1946-61", "d1", "d3")  # two eras, then the two cuts that decide
if ERA == "1962":
    Y73 = (date(1973, 1, 1), date(1974, 12, 31))
    Y87 = (date(1987, 1, 1), date(1987, 12, 31))
    WHOLE = Window("whole", "1962-01 to 2001-12")
    WINDOWS = [
        WHOLE,
        Window("1962-81", "1962-01 to 1981-12", hi=date(1981, 12, 31)),
        Window("1982-01", "1982-01 to 2001-12", lo=date(1982, 1, 1)),
        Window("x1", "without 1973-1974", drop=(Y73,)),
        Window("x2", "without 1987", drop=(Y87,)),
        Window("x3", "without 1973-1974 and 1987", drop=(Y73, Y87)),
        Window("to1993", "1962-01 to 1993-12", hi=date(1993, 12, 31)),
    ]
    KEYS = ("1962-81", "1982-01", "x3", "x1")


def day_ords(run: c.Run) -> np.ndarray:
    """Ordinal of the day each entry of run.rets belongs to."""
    return np.array([d.toordinal() for d in run.days[1:]], dtype=np.int64)


@dataclass
class Diff:
    rule: float
    hold: float
    diff: float
    p: float
    lo: float
    hi: float
    mdd_rule: float
    mdd_hold: float
    cagr_rule: float
    cagr_hold: float


def compare(a: np.ndarray, b: np.ndarray, block: float = 20) -> Diff:
    """Rule returns `a` against twin returns `b` on the same days."""
    d, p, lo, hi = stats.sharpe_diff_boot(a, b, draws=DRAWS, mean_block=block, seed=0)
    return Diff(stats.sharpe(a), stats.sharpe(b), d, p, lo, hi, stats.max_drawdown(a),
                stats.max_drawdown(b), stats.cagr(a), stats.cagr(b))  # fmt: skip


_DIFFS: dict[tuple[str, str, float], Diff] = {}


def window_diff(pr: Pair, w: Window, block: float = 20) -> Diff:
    key = (pr.rule.variant, w.key, block)
    if key not in _DIFFS:
        m = w.mask(day_ords(pr.rule))
        _DIFFS[key] = compare(pr.rule.rets[m], pr.hold.rets[m], block)
    return _DIFFS[key]


# --- the mechanism: sessions in and out ---


@dataclass
class Spell:
    out: date
    back: date
    days: int
    move: float  # log(price at re-entry / price at exit): positive = bought back higher
    closed: bool


@dataclass
class Solo:
    name: str
    ords: np.ndarray  # session ordinals from the twin's entry fill on
    lr: np.ndarray  # the asset's log return over each of those sessions (close to close)
    state: np.ndarray  # True where the rule held the asset over that session
    spells: list[Spell]


def states(n: int, i0: int, flips: dict[int, bool]) -> np.ndarray:
    """In/out per bar from fills at bar opens (`flips`: bar -> True for a buy)."""
    out = np.zeros(n, bool)
    cur = False
    for i in range(i0, n):
        cur = flips.get(i, cur)
        out[i] = cur
    return out


def spells_of(
    dates: Sequence[date], o: np.ndarray, cl: np.ndarray, state: np.ndarray, i0: int
) -> list[Spell]:
    """Spells out that begin with an exit: from the exit fill to the re-entry fill (both at the
    bar's open). A spell still open at the end is marked not closed."""
    out: list[Spell] = []
    start = -1
    for i in range(i0 + 1, len(state)):
        if state[i - 1] and not state[i]:
            start = i
        elif state[i] and not state[i - 1] and start >= 0:
            out.append(Spell(dates[start], dates[i], (dates[i] - dates[start]).days,
                             float(math.log(o[i] / o[start])), True))  # fmt: skip
            start = -1
    if start >= 0 and not state[-1]:
        out.append(Spell(dates[start], dates[-1], (dates[-1] - dates[start]).days,
                         float(math.log(cl[-1] / o[start])), False))  # fmt: skip
    return out


def solo(name: str, pr: Pair, u: c.Ctx) -> Solo:
    """In/out sessions of the primary run, from the gym's own fills. With open = previous close
    a fill at bar i's open comes before the whole of bar i's close-to-close return."""
    s = sym(name)
    hist = u.hist[s]
    dates = [b.date for b in hist]
    idx = {d: i for i, d in enumerate(dates)}
    o = np.array([b.open for b in hist])
    cl = np.array([b.close for b in hist])
    hold_fills = gym.simulate(pr.hold.decisions, u.hist).fills
    rule_fills = gym.simulate(pr.rule.decisions, u.hist).fills
    i0 = idx[hold_fills[0].time.date()]
    state = states(len(hist), i0, {idx[f.time.date()]: f.qty > 0 for f in rule_fills})
    lr = np.zeros(len(hist))
    lr[1:] = np.log(cl[1:] / cl[:-1])
    ords = np.array([d.toordinal() for d in dates], dtype=np.int64)
    return Solo(name, ords[i0:], lr[i0:], state[i0:], spells_of(dates, o, cl, state, i0))


@dataclass
class Mech:
    time_in: float
    vol_in: float
    vol_out: float
    ratio: float
    p: float
    worst_out: int
    ann_in: float  # the asset's log points per year of in-time
    ann_out: float
    n_out: int


def rotation_p(lr: np.ndarray, state: np.ndarray, draws: int = DRAWS, seed: int = 0) -> float:
    """Share of rotations of the in/out sequence against the returns whose out/in volatility
    ratio is at least the observed one. Keeps the spells, breaks their timing."""
    n = len(lr)
    obs = lr[~state].std() / lr[state].std()
    rng = np.random.default_rng(seed)
    hits = 0
    for off in rng.integers(1, n, size=draws):
        s = np.roll(state, int(off))
        hits += lr[~s].std() / lr[s].std() >= obs
    return hits / draws


_MECHS: dict[tuple[str, str], Mech | None] = {}


def mechanism(so: Solo, w: Window) -> Mech | None:
    key = (so.name, w.key)
    if key not in _MECHS:
        _MECHS[key] = _mechanism(so, w)
    return _MECHS[key]


def _mechanism(so: Solo, w: Window) -> Mech | None:
    m = w.mask(so.ords)
    lr, st = so.lr[m], so.state[m]
    n_in, n_out = int(st.sum()), int((~st).sum())
    if n_in < 20 or n_out < 20:
        return None
    kept_days = int(w.mask(np.arange(so.ords[0], so.ords[-1] + 1)).sum())
    per_year = len(lr) / (kept_days / 365.25)
    vol_in = float(lr[st].std() * math.sqrt(per_year))
    vol_out = float(lr[~st].std() * math.sqrt(per_year))
    worst = np.argsort(lr)[:20]
    return Mech(
        float(st.mean()), vol_in, vol_out, vol_out / vol_in, rotation_p(lr, st),
        int((~st[worst]).sum()), float(lr[st].mean() * per_year * 100),
        float(lr[~st].mean() * per_year * 100), n_out,
    )  # fmt: skip


# --- cash at the T-bill rate (a re-scoring of the primary runs) ---


def above_bills(run: c.Run, rf_by_day: dict[date, float]) -> np.ndarray:
    """Daily returns above the T-bill return, with the bill return earned on the cash share.
    The weights decided on a day earn from the next day (the primary fill convention)."""
    expo = {d.time.date(): sum(d.weights.values()) for d in run.decisions}
    out = run.rets.copy()
    cash = 1 - expo.get(run.days[0], 0.0)
    for k, d in enumerate(run.days[1:]):
        rf = rf_by_day.get(d, 0.0)
        out[k] += cash * rf - rf
        cash = 1 - expo.get(d, 1 - cash)
    return out


# --- the replay check: the gym against a paper series that shares no fill code with it ---


def replay_gap(pr: Pair, u: c.Ctx, s: str) -> tuple[float, float]:
    """(difference in total log growth, largest daily difference) between the gym's rule run
    and trend-tune's gym-free paper series for the same asset."""
    p = tt.paper(u.panel, s, (12,))
    eq = dict(zip(pr.rule.days, pr.rule.equity, strict=True))
    first = (START + timedelta(days=14)).toordinal()  # the paper series starts a session earlier
    keep = [i for i, o in enumerate(p.ord) if o > first and date.fromordinal(int(o)) in eq]
    g = np.array([eq[date.fromordinal(int(p.ord[i]))] / eq[date.fromordinal(int(p.ord[i - 1]))] - 1
                  for i in keep])  # fmt: skip
    q = p.ret[12][keep]
    return float(np.log1p(g).sum() - np.log1p(q).sum()), float(np.abs(g - q).max())


# --- report ---


def pct(x: float, digits: int = 0) -> str:
    return "-" if math.isnan(x) else f"{x * 100:.{digits}f}%"


def dp(d: Diff) -> str:
    return f"{d.diff:+.2f} ({d.p:.2f})"


def section_data(
    raw: Raw, solos: dict[str, Solo], gaps: dict[str, tuple[float, float]]
) -> list[str]:
    early = sum(d.year < 1952 for d in raw.days) / ((date(1952, 1, 1) - FIRST).days / 365.25)
    lateyrs = sum(d.year >= 1952 for d in raw.days) / ((LAST - date(1951, 12, 31)).days / 365.25)
    sat = sum(d.weekday() == 5 for d in raw.days)
    allyrs = len(raw.days) / ((LAST - FIRST).days / 365.25)
    missing = {n: int(np.isnan(r).sum()) for n, r in raw.ret.items()}
    out = ["## 0. Data and checks", ""]
    out += [
        f"- Cache snapshot `french/{raw.snapshot}`. {len(raw.days)} sessions from {raw.days[0]} "
        f"to {raw.days[-1]}; {sat} of them Saturdays. Sessions a year: "
        + (
            f"{early:.0f} before 1952, {lateyrs:.0f} from 1952."
            if ERA != "1962"
            else f"{allyrs:.0f}."
        ),
        f"- Returns marked missing in the window: {sum(missing.values())}"
        + ("." if not sum(missing.values()) else f" ({missing})."),
        f"- First decision {START}; holding's first fill "
        f"{date.fromordinal(int(solos[MKT].ords[0]))}.",
        "- Replay check (the gym against trend-tune's paper series, which computes position x "
        "close-to-close return minus cost with no gym code): difference in total log growth "
        "from two weeks after the start, and the largest difference on any one day: "
        + "; ".join(f"{n} {g[0]:+.4f} / {g[1]:.5f}" for n, g in gaps.items())
        + ".",
        "",
    ]
    return out


def section_whole(pairs: dict[str, Pair], solos: dict[str, Solo]) -> list[str]:
    out = ["## 1. (a) The whole period: the rule against holding", ""]
    out += [
        "One series, the whole account. `Difference` is Sharpe of the rule minus Sharpe of "
        "holding; p is the one-sided bootstrap p-value that the rule is better (mean block 20 "
        "days; `p125` with a mean block of 125 days). Sharpe on calendar days, cash earns 0. "
        "`F-ind10` is the ten industries as one equal-slot book against equal weight.",
        "",
        "| Series | Sharpe hold | Sharpe rule | Difference (p) | 90% range | p125 | Growth/yr "
        "hold | Growth/yr rule | Worst loss hold | Worst loss rule | Time in |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, pr in pairs.items():
        d = window_diff(pr, WHOLE)
        p125 = f"{window_diff(pr, WHOLE, 125).p:.2f}" if name in (MKT, BOOK) else "-"
        time_in = pct(float(solos[name].state.mean())) if name in solos else pct(pr.rule.exposure)
        out.append(
            f"| {sym(name)} | {d.hold:.2f} | {d.rule:.2f} | {dp(d)} | {d.lo:+.2f}..{d.hi:+.2f} | "
            f"{p125} | {pct(d.cagr_hold, 1)} | {pct(d.cagr_rule, 1)} | {pct(d.mdd_hold)} | "
            f"{pct(d.mdd_rule)} | {time_in} |"
        )
    pos = sum(window_diff(pairs[n], WHOLE).diff > 0 for n in INDUSTRIES)
    out += ["", f"Industries where the rule is ahead: {pos} of 10.", ""]
    return out


def section_mechanism(solos: dict[str, Solo]) -> list[str]:
    out = ["## 2. (b) The mechanism: were the days out rougher than the days in?", ""]
    out += [
        "Sessions are split by whether the rule held the asset (from the gym's fills). "
        "Volatility is that of the asset's daily log returns, annualised. `p` is the share of "
        "2,000 rotations of the in/out sequence against the returns that give a ratio at least "
        "as large. `Asset while in / out`: log points a year of in-time and of out-time.",
        "",
        "| Series | Time in | Volatility in | Volatility out | Ratio out/in | p | Of the 20 worst "
        "sessions, rule was out | Asset while in | Asset while out |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, so in solos.items():
        m = mechanism(so, WHOLE)
        assert m is not None
        out.append(
            f"| {sym(name)} | {pct(m.time_in)} | {pct(m.vol_in)} | {pct(m.vol_out)} | "
            f"{m.ratio:.2f} | {m.p:.2f} | {m.worst_out} | {m.ann_in:+.1f} | {m.ann_out:+.1f} |"
        )
    return out + [""]


def section_windows(pairs: dict[str, Pair], solos: dict[str, Solo]) -> list[str]:
    out = ["## 3. (c) Two eras and (d) without the great crash", ""]
    out += ["Windows: " + "; ".join(f"`{w.key}` = {w.label}" for w in WINDOWS) + ".", ""]
    head = "| Series |" + "".join(f" {w.key} |" for w in WINDOWS)
    sep = "|---|" + "---:|" * len(WINDOWS)
    out += ["Sharpe of the rule minus Sharpe of holding (p):", "", head, sep]
    diffs = {n: {w.key: window_diff(pr, w) for w in WINDOWS} for n, pr in pairs.items()}
    for n in pairs:
        out.append(f"| {sym(n)} |" + "".join(f" {dp(diffs[n][w.key])} |" for w in WINDOWS))
    out.append(
        "| industries ahead |"
        + "".join(f" {sum(diffs[n][w.key].diff > 0 for n in INDUSTRIES)} of 10 |" for w in WINDOWS)
    )
    out += ["", "Levels for the market and the book (Sharpe hold / rule; worst loss hold / rule):"]
    out += ["", head, sep]
    for n in (MKT, BOOK):
        cells = (
            f" {d.hold:.2f} / {d.rule:.2f}; {pct(d.mdd_hold)} / {pct(d.mdd_rule)} |"
            for d in (diffs[n][w.key] for w in WINDOWS)
        )
        out.append(f"| {sym(n)} |" + "".join(cells))
    out += ["", "Volatility ratio, sessions out over sessions in (rotation p):", "", head, sep]
    mech = {n: {w.key: mechanism(so, w) for w in WINDOWS} for n, so in solos.items()}
    for n in solos:
        cells = (
            " - |" if m is None else f" {m.ratio:.2f} ({m.p:.2f}) |"
            for m in (mech[n][w.key] for w in WINDOWS)
        )
        out.append(f"| {sym(n)} |" + "".join(cells))
    present = (
        sum(1 for n in INDUSTRIES if (m := mech[n][w.key]) and m.ratio > 1 and m.p < 0.10)
        for w in WINDOWS
    )
    out.append("| industries where present |" + "".join(f" {k} of 10 |" for k in present))
    out += ["", "Market, by window: share of sessions in, volatility in and out:", "", head, sep]
    cells = (
        " - |" if m is None else f" {pct(m.time_in)}; {pct(m.vol_in)} / {pct(m.vol_out)} |"
        for m in (mech[MKT][w.key] for w in WINDOWS)
    )
    out.append(f"| {sym(MKT)} |" + "".join(cells))
    return out + [""]


def section_robust(raw: Raw, pairs: dict[str, Pair], alt: dict[str, dict[str, Pair]]) -> list[str]:
    rf = dict(zip(raw.days, (float(x) for x in raw.rf), strict=True))
    out = ["## 4. Robustness: a later fill, higher costs, interest on cash", ""]
    out += [
        "Sharpe of the rule minus Sharpe of its twin over the whole period (p). `late`: filled "
        "one session later. `10 bps`, `50 bps`: cost a side. `T-bill`: cash earns the T-bill "
        "return and both Sharpes are measured above it (a re-scoring of the primary runs).",
        "",
        "| Series | Primary | late | 10 bps | 50 bps | T-bill | Sharpe above T-bills, hold / "
        "rule |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for n, pr in pairs.items():
        row = f"| {sym(n)} | {dp(window_diff(pr, WHOLE))} |"
        for suffix in ("-late", "-10bps", "-50bps"):
            row += f" {dp(window_diff(alt[suffix][n], WHOLE))} |"
        a, b = above_bills(pr.rule, rf), above_bills(pr.hold, rf)
        d = compare(a, b)
        out.append(row + f" {dp(d)} | {d.hold:.2f} / {d.rule:.2f} |")
    years = (LAST - START).days / 365.25
    bill = float(np.prod(1 + raw.rf[[d >= START for d in raw.days]]) ** (1 / years) - 1)
    out += ["", f"Average T-bill return over the period: {bill:.1%} a year.", ""]
    return out


def section_spells(solos: dict[str, Solo]) -> list[str]:
    out = ["## 5. Spells out (description)", ""]
    out += [
        "A spell runs from an exit fill to the re-entry fill. A whipsaw is a spell bought back "
        "higher than it was sold. `Net` is the sum over spells of the price move avoided "
        "(positive: the rule gained by being out), in log points.",
        "",
        "| Series | Spells | Whipsaws | Under 13 weeks: spells, net | 13 weeks or more: spells, "
        "net |",
        "|---|---:|---:|---:|---:|",
    ]
    for n, so in solos.items():
        sp = so.spells
        short = [s for s in sp if s.days < 91]
        long = [s for s in sp if s.days >= 91]
        out.append(
            f"| {sym(n)} | {len(sp)} | {sum(s.move > 0 for s in sp)} | {len(short)}, "
            f"{-sum(s.move for s in short) * 100:+.0f} | {len(long)}, "
            f"{-sum(s.move for s in long) * 100:+.0f} |"
        )
    out += ["", "The market's spells out of 13 weeks or more:", ""]
    out += ["| Out | Back | Days | Price at re-entry against price at exit |"]
    out += ["|---|---|---:|---:|"]
    for s in solos[MKT].spells:
        if s.days >= 91:
            back = f"{s.back}" if s.closed else f"{s.back} (still out)"
            out.append(f"| {s.out} | {back} | {s.days} | {(math.exp(s.move) - 1) * 100:+.0f}% |")
    return out + [""]


def section_outcome(pairs: dict[str, Pair], solos: dict[str, Solo], late_mkt: Pair) -> list[str]:
    def d(n: str, k: str) -> float:
        return window_diff(pairs[n], next(w for w in WINDOWS if w.key == k)).diff

    def present(n: str, k: str) -> bool:
        m = mechanism(solos[n], next(w for w in WINDOWS if w.key == k))
        return m is not None and m.ratio > 1 and m.p < 0.10

    yn = {True: "yes", False: "no"}
    ea, eb, c1, c2 = KEYS
    m_whole, b_whole = d(MKT, "whole"), d(BOOK, "whole")
    late = window_diff(late_mkt, WHOLE).diff
    checks = [
        ("market ahead over the whole period", m_whole > 0),
        (f"market ahead in {ea}", d(MKT, ea) > 0),
        (f"market ahead in {eb}", d(MKT, eb) > 0),
        (f"market ahead in `{c1}`", d(MKT, c1) > 0),
        (f"market ahead in `{c2}`", d(MKT, c2) > 0),
        ("book agrees in sign over the whole period", b_whole * m_whole > 0),
        (f"book agrees in sign in `{c1}`", d(BOOK, c1) * d(MKT, c1) > 0),
        ("mechanism present on the market, whole period", present(MKT, "whole")),
        (f"mechanism present on the market, `{c2}`", present(MKT, c2)),
    ]
    fragile = b_whole * m_whole <= 0 or late * m_whole <= 0
    remains = d(MKT, c1) > 0 and d(MKT, c2) > 0
    if fragile:
        verdict = "Too fragile to call"
    elif m_whole <= 0:
        verdict = "No"
    elif not remains:
        verdict = "One crash again" if ERA != "1962" else "Crashes only"
    elif all(ok for _, ok in checks):
        verdict = "A property"
    else:
        verdict = "Something remains, but short of the card's conditions for a property"
    out = ["## 6. The card's outcome, applied mechanically", ""]
    out += [f"- {text}: {yn[ok]}" for text, ok in checks]
    out += [f"- primary and `late` fills agree in sign on the market: {yn[late * m_whole > 0]}"]
    both = [sum(present(n, k) for n in INDUSTRIES) for k in (ea, eb)]
    out += [
        f"- mechanism on its own: market present in {ea} {yn[present(MKT, ea)]}, in "
        f"{eb} {yn[present(MKT, eb)]}; industries present {both[0]} of 10 and "
        f"{both[1]} of 10.",
        "",
        f"**Outcome: {verdict}.**",
        "",
    ]
    return out


def main() -> None:
    raw = load()
    series = [MKT, *INDUSTRIES]
    pairs: dict[str, Pair] = {}
    solos: dict[str, Solo] = {}
    gaps: dict[str, tuple[float, float]] = {}
    for n in series:
        pairs[n], u = pair(raw, [n], n, "")
        solos[n] = solo(n, pairs[n], u)
        if n in (MKT, "Durbl", "Utils"):
            gaps[sym(n)] = replay_gap(pairs[n], u, sym(n))
    pairs[BOOK], _ = pair(raw, INDUSTRIES, BOOK, "")
    alt: dict[str, dict[str, Pair]] = {}
    for suffix in ("-late", "-10bps", "-50bps"):
        alt[suffix] = {n: pair(raw, [n], n, suffix)[0] for n in series}
        alt[suffix][BOOK] = pair(raw, INDUSTRIES, BOOK, suffix)[0]
    body = [MARK, ""]
    body += section_data(raw, solos, gaps)
    body += section_whole(pairs, solos)
    body += section_mechanism(solos)
    body += section_windows(pairs, solos)
    body += section_robust(raw, pairs, alt)
    body += section_spells(solos)
    body += section_outcome(pairs, solos, alt["-late"][MKT])
    path = harness.RESEARCH / "results" / (f"{RESULT}.md" if not c.DRY else f"{RESULT}.dry.md")
    head = (
        f"# {RESULT}: `tsmom12` on US stocks {FIRST.year}-{LAST.year}\n\nCard: `trend-1926.md`.\n"
    )
    if path.exists() and MARK in path.read_text():
        head = path.read_text().split(MARK)[0].rstrip() + "\n"
    path.write_text(head + "\n" + "\n".join(body).rstrip() + "\n")
    print("\n".join(body))


if __name__ == "__main__":
    main()
