"""rev-costloss-1: the `tsmom12` exit scored as a crash warning. Card: cards/rev-costloss-1.md.

    uv run python -I research/lib/revcostloss1.py

Descriptive re-score, no new rule. Each Friday decision is a binary forecast (warning = the
rule is out for the next week); the event is a fall of at least X below Friday's close within
the next N weeks. Contingency table, hit and false-alarm rates, Peirce skill score and the
relative economic value V(C/L) of the static cost-loss model (Richardson 2000), against
climatology, a perfect forecast and the rule's own positions rotated to random dates.
Data: the French daily US market and 10 industries (insure-1's paper series, as gap-2002-1)
and the six assets (adjusted train bars, `trend_tune.paper`). Nothing after 2025-10-31 is used.
Writes research/results/rev-costloss-1.md.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402

LAST = date(2025, 10, 31)
XS = (0.05, 0.10, 0.20)
NS = (4, 13, 26)
PRIMARY = (0.10, 13)
ALPHAS = (0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80)
FINE = np.round(np.arange(0.005, 1.0, 0.005), 3)
ROTATIONS, SEED = 1000, 0
FAST, MEDIUM = 92, 365  # insure-1's fall-speed classes, calendar days peak -> trough
REBOUND = 365
ERAS = (
    ("1927-1961", date(1927, 7, 2), date(1961, 12, 31)),
    ("1962-2001", date(1962, 1, 1), date(2001, 12, 31)),
    ("2002-2025", date(2002, 1, 1), LAST),
)
OUT = harness.RESEARCH / "results" / "rev-costloss-1.md"


# --- scores (pure) ---


@dataclass(frozen=True)
class Table:
    a: int  # hits: warned, event came
    b: int  # false alarms: warned, no event
    c: int  # misses: not warned, event came
    d: int  # correct rejections

    @property
    def n(self) -> int:
        return self.a + self.b + self.c + self.d

    @property
    def s(self) -> float:
        return (self.a + self.c) / self.n if self.n else math.nan

    @property
    def h(self) -> float:
        return self.a / (self.a + self.c) if self.a + self.c else math.nan

    @property
    def f(self) -> float:
        return self.b / (self.b + self.d) if self.b + self.d else math.nan

    @property
    def pss(self) -> float:
        return self.h - self.f

    def __add__(self, o: Table) -> Table:
        return Table(self.a + o.a, self.b + o.b, self.c + o.c, self.d + o.d)


def table(w: np.ndarray, e: np.ndarray) -> Table:
    w, e = w.astype(bool), e.astype(bool)
    return Table(int((w & e).sum()), int((w & ~e).sum()), int((~w & e).sum()),
                 int((~w & ~e).sum()))  # fmt: skip


def value(alpha: float, h: float, f: float, s: float) -> float:
    """Relative economic value of a binary warning (Richardson 2000) for cost/loss ratio alpha."""
    clim = min(alpha, s)
    perf = s * alpha
    fc = alpha * (h * s + f * (1 - s)) + (1 - h) * s
    den = clim - perf
    return (clim - fc) / den if den > 0 else math.nan


def v_of(t: Table, alpha: float) -> float:
    return value(alpha, t.h, t.f, t.s)


def v_range(t: Table) -> tuple[float, float] | None:
    """Smallest and largest alpha on the 0.005 grid with V > 0 (None: nowhere)."""
    pos = [a for a in FINE if v_of(t, float(a)) > 0]
    return (float(pos[0]), float(pos[-1])) if pos else None


def alpha_hold(r: np.ndarray, e: np.ndarray) -> float:
    """A holder's cost/loss ratio: C = mean week return without event, L = C - mean with event."""
    e = e.astype(bool)
    if e.all() or not e.any():
        return math.nan
    c = float(r[~e].mean())
    loss = c - float(r[e].mean())
    return c / loss if c > 0 and loss > 0 else math.nan


def v_money(r: np.ndarray, w: np.ndarray, e: np.ndarray) -> float:
    """(rule - hold) / (perfect - hold), weekly log returns summed, cash at 0, no costs."""
    hold = np.log1p(r).sum()
    rule = np.log1p((1 - w) * r).sum()
    perf = np.log1p((1 - e) * r).sum()
    den = perf - hold
    return float((rule - hold) / den) if den > 0 else math.nan


# --- weekly forecasts (pure) ---


@dataclass
class Weekly:
    name: str
    fri: list[date]  # forecast Fridays (eligible, with a following session)
    w: np.ndarray  # warning: 1 = the rule is out for the next week
    r: np.ndarray  # holding's simple return over the week after the Friday
    k: np.ndarray  # index of the last session at or before the Friday
    days: list[date]
    px: np.ndarray  # total-return index per session


def weekly(name: str, days: Sequence[date], px: np.ndarray, pos: np.ndarray, ok: np.ndarray,
           last: date = LAST) -> Weekly:  # fmt: skip
    """Friday forecasts: pos[i] is the position earning session i's return (decided on the
    Friday before it); ok[i] marks sessions on which the asset was eligible."""
    ords = np.array([d.toordinal() for d in days])
    first = days[0]
    f = first + timedelta(days=(4 - first.weekday()) % 7)
    end = min(days[-1], last)
    fri, w, r, ks = [], [], [], []
    while f + timedelta(days=7) <= end:
        k = int(np.searchsorted(ords, f.toordinal(), side="right")) - 1
        lo = k + 1
        j = int(np.searchsorted(ords, f.toordinal() + 7, side="right")) - 1
        if k >= 0 and lo <= j and ok[lo]:
            fri.append(f)
            w.append(1.0 - pos[lo])
            r.append(px[j] / px[k] - 1)
            ks.append(k)
        f += timedelta(days=7)
    return Weekly(name, fri, np.array(w), np.array(r), np.array(ks, dtype=int), list(days), px)


def events(wk: Weekly, x: float, n: int, last: date = LAST) -> tuple[np.ndarray, np.ndarray]:
    """(valid, event): the window (f, f + 7n days] must end by the last session (and `last`)."""
    ords = np.array([d.toordinal() for d in wk.days])
    end = min(wk.days[-1], last).toordinal()
    valid = np.zeros(len(wk.fri), dtype=bool)
    ev = np.zeros(len(wk.fri), dtype=bool)
    for i, (f, k) in enumerate(zip(wk.fri, wk.k, strict=True)):
        top = f.toordinal() + 7 * n
        if top > end:
            continue
        hi = int(np.searchsorted(ords, top, side="right")) - 1
        valid[i] = True
        ev[i] = bool(wk.px[k + 1 : hi + 1].min() <= wk.px[k] * (1 - x))
    return valid, ev


def zigzag(px: np.ndarray, down: float = 0.25, up: float = 0.25) -> list[tuple[int, int]]:
    """Confirmed (peak, trough) index pairs (insure-1's zigzag, as gap-2002-1)."""
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
    return out


def parts(days: Sequence[date], px: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Per session: part (0 calm, 1 fall, 2 rebound) and, in falls, the fall's speed class
    (1 fast <= 92 days, 2 medium, 3 slow > 365; 0 outside falls)."""
    ords = np.array([d.toordinal() for d in days])
    part = np.zeros(len(px), dtype=int)
    speed = np.zeros(len(px), dtype=int)
    pairs = zigzag(px)
    for j, (a, b) in enumerate(pairs):
        e = int(np.searchsorted(ords, ords[b] + REBOUND, side="right")) - 1
        if j + 1 < len(pairs):
            e = min(e, pairs[j + 1][0])
        dur = int(ords[b] - ords[a])
        part[a + 1 : b + 1] = 1
        speed[a + 1 : b + 1] = 1 if dur <= FAST else (2 if dur <= MEDIUM else 3)
        part[b + 1 : e + 1] = 2
    return part, speed


def rotated(w: np.ndarray, k: int) -> np.ndarray:
    return np.roll(w, k)


# --- data ---


def french() -> list[tuple[str, list[date], np.ndarray, np.ndarray]]:
    """insure-2 step 1's 11 series (gap-2002-1's loader): name, days, index, position."""
    import insure1 as i1
    import trend_1926 as t
    from macro import cache_root

    snap = sorted(p for p in (cache_root() / "french").iterdir() if p.is_dir())[-1]
    fac = t.parse_factors(i1._lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), i1.LAST)
    ind = t.parse_industries(i1._lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), i1.LAST)
    days = sorted(d for d in fac if d >= i1.FIRST)
    rf = {d: fac[d][1] for d in days}
    raw = [(t.MKT, days, np.array([fac[d][0] for d in days]))]
    for j, n in enumerate(t.INDUSTRIES):
        r = np.array([ind[d][j] for d in days])
        keep = ~np.isnan(r)
        raw.append((n, [d for d, ok in zip(days, keep, strict=True) if ok], r[keep]))
    out = []
    for n, dd, r in raw:
        s = i1.build(n, dd, r, rf, None)
        out.append((n, s.days, s.px, s.pos))
    return out


def six() -> list[tuple[str, list[date], np.ndarray, np.ndarray, np.ndarray]]:
    """The six assets: name, days, adjusted close, position, eligible (paper series, train)."""
    import insure1 as i1
    import trend_tune as tt

    from grimstrade import gym
    from grimstrade.data import UNIVERSE

    hist = harness.load_history("train")
    out = []
    for s in harness.SYMS:
        bars = [b for b in hist[s] if b.date <= LAST]
        p = tt.paper(harness.Panel({s: bars}), s, (12,))
        close = np.array([b.close for b in bars])
        bar = np.zeros(len(close))
        bar[1:] = close[1:] / close[:-1] - 1
        cost = gym.COSTS[UNIVERSE[s]]
        one_way = cost.fee + cost.slip
        pos = i1.infer_pos(p.ret[12], bar, one_way)
        back = pos * bar - one_way * np.abs(np.diff(pos, prepend=0.0))
        if np.max(np.abs(back - p.ret[12])) > 1e-12:
            raise AssertionError(f"{s}: positions do not reproduce the paper series")
        out.append((s, [b.date for b in bars], close, pos, p.ok))
    return out


# --- report ---


def fmt(x: float, nd: int = 2, sign: bool = True) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "n/a"
    return f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"


def rng_txt(r: tuple[float, float] | None) -> str:
    return "none" if r is None else f"{r[0]:.3f}-{r[1]:.3f}"


@dataclass
class Cell:
    ws: list[np.ndarray]  # per series, valid weeks only
    es: list[np.ndarray]
    rs: list[np.ndarray]
    labels: list[np.ndarray]  # part per forecast
    speeds: list[np.ndarray]
    fris: list[list[date]]

    @property
    def t(self) -> Table:
        out = Table(0, 0, 0, 0)
        for w, e in zip(self.ws, self.es, strict=True):
            out = out + table(w, e)
        return out


def cell(wks: Sequence[Weekly], x: float, n: int, lo: date | None = None,
         hi: date | None = None) -> Cell:  # fmt: skip
    ws, es, rs, ls, ss, fs = [], [], [], [], [], []
    for wk in wks:
        valid, ev = events(wk, x, n)
        if lo is not None and hi is not None:
            inside = np.array([lo <= f <= hi for f in wk.fri], dtype=bool)
            valid &= inside
        part, speed = parts(wk.days, wk.px)
        ws.append(wk.w[valid])
        es.append(ev[valid])
        rs.append(wk.r[valid])
        ls.append(part[wk.k][valid])
        ss.append(speed[wk.k][valid])
        fs.append([f for f, v in zip(wk.fri, valid, strict=True) if v])
    return Cell(ws, es, rs, ls, ss, fs)


@dataclass
class Rot:
    pss: np.ndarray
    v: dict[float, np.ndarray]


def rotations(c: Cell, alphas: Sequence[float] = ALPHAS) -> Rot:
    """Each series' warnings rotated by a common fraction u of its length (k in [52, n - 52])."""
    rng = np.random.default_rng(SEED)
    pss = np.zeros(ROTATIONS)
    v = {a: np.zeros(ROTATIONS) for a in alphas}
    for i in range(ROTATIONS):
        u = float(rng.random())
        tot = Table(0, 0, 0, 0)
        for w, e in zip(c.ws, c.es, strict=True):
            m = len(w)
            k = 52 + int(u * max(m - 104, 1))
            tot = tot + table(rotated(w, k), e)
        pss[i] = tot.pss
        for a in alphas:
            v[a][i] = v_of(tot, a)
    return Rot(pss, v)


def q(a: np.ndarray) -> str:
    lo, mid, hi = np.nanquantile(a, [0.05, 0.5, 0.95])
    return f"{mid:+.2f} ({lo:+.2f} to {hi:+.2f})"


def main_rows(sets: Sequence[tuple[str, Cell]]) -> list[str]:
    head = [
        "| Set | Weeks | Base rate s | Warned | H | F | PSS = V_max | Rotations PSS, median "
        "(5-95%) | p | V > 0 for C/L | alpha_hold | V(alpha_hold) | V_money |",
        "|---|---:|---:|---:|---:|---:|---:|---|---:|---|---:|---:|---:|",
    ]
    out = []
    for name, c in sets:
        t = c.t
        rot = rotations(c)
        p = float((rot.pss >= t.pss).mean())
        w = np.concatenate(c.ws)
        e = np.concatenate(c.es).astype(float)
        r = np.concatenate(c.rs)
        ah = alpha_hold(r, e)
        vah = v_of(t, ah) if not math.isnan(ah) else math.nan
        out.append(
            f"| {name} | {t.n:,} | {t.s:.2f} | {(t.a + t.b) / t.n:.2f} | {t.h:.2f} | {t.f:.2f} "
            f"| {fmt(t.pss)} | {q(rot.pss)} | {p:.3f} | {rng_txt(v_range(t))} | "
            f"{fmt(ah, 2, False)} | {fmt(vah)} | {fmt(v_money(r, w, e))} |"
        )
    return head + out


def curve_rows(sets: Sequence[tuple[str, Cell]]) -> list[str]:
    head = [
        "| Set | " + " | ".join(f"{a:.2f}" for a in ALPHAS) + " |",
        "|---|" + "---:|" * len(ALPHAS),
    ]
    out = []
    for name, c in sets:
        t = c.t
        rot = rotations(c)
        out.append(f"| {name} | " + " | ".join(fmt(v_of(t, a)) for a in ALPHAS) + " |")
        out.append(
            f"| {name}: rotations, median | "
            + " | ".join(fmt(float(np.nanmedian(rot.v[a]))) for a in ALPHAS)
            + " |"
        )
        out.append(
            f"| {name}: rotations, 95% | "
            + " | ".join(fmt(float(np.nanquantile(rot.v[a], 0.95))) for a in ALPHAS)
            + " |"
        )
    return head + out


def grid_rows(name: str, wks: Sequence[Weekly]) -> list[str]:
    out = []
    for x in XS:
        for n in NS:
            c = cell(wks, x, n)
            t = c.t
            rot = rotations(c, ())
            p = float((rot.pss >= t.pss).mean())
            w = np.concatenate(c.ws)
            e = np.concatenate(c.es).astype(float)
            r = np.concatenate(c.rs)
            ah = alpha_hold(r, e)
            vah = v_of(t, ah) if not math.isnan(ah) else math.nan
            out.append(
                f"| {name} | {x:.0%} in {n} wk | {t.s:.2f} | {t.h:.2f} | {t.f:.2f} | "
                f"{fmt(t.pss)} | {float(np.median(rot.pss)):+.2f} | {p:.3f} | "
                f"{rng_txt(v_range(t))} | {fmt(ah, 2, False)} | {fmt(vah)} | "
                f"{fmt(v_money(r, w, e))} |"
            )
    return out


GRID_HEAD = [
    "| Set | Event | s | H | F | PSS | Rot. median | p | V > 0 for C/L | alpha_hold | "
    "V(alpha_hold) | V_money |",
    "|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|",
]


def where_rows(sets: Sequence[tuple[str, Cell]]) -> list[str]:
    head = [
        "| Set | False alarms | in falls | in rebounds | in calm | Misses | in falls | in "
        "rebounds | in calm | Warned share: falls / rebounds / calm |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    out = []
    for name, c in sets:
        w = np.concatenate(c.ws).astype(bool)
        e = np.concatenate(c.es).astype(bool)
        lab = np.concatenate(c.labels)
        fa, mi = w & ~e, ~w & e
        sh = [float(w[lab == k].mean()) if (lab == k).any() else math.nan for k in (1, 2, 0)]
        out.append(
            f"| {name} | {int(fa.sum()):,} | "
            + " | ".join(f"{(fa & (lab == k)).sum() / max(fa.sum(), 1):.2f}" for k in (1, 2, 0))
            + f" | {int(mi.sum()):,} | "
            + " | ".join(f"{(mi & (lab == k)).sum() / max(mi.sum(), 1):.2f}" for k in (1, 2, 0))
            + " | "
            + " / ".join(f"{x:.2f}" for x in sh)
            + " |"
        )
    return head + out


def hit_txt(w: np.ndarray, e: np.ndarray, m: np.ndarray) -> str:
    k = int((e & m).sum())
    return f"{(w & e & m).sum() / k:.2f} (n {k:,})" if k else "n/a"


def speed_rows(sets: Sequence[tuple[str, Cell]]) -> list[str]:
    head = [
        "| Set | Event weeks | H, all | H in fast falls (<= 92 d) | medium (93-365 d) | slow "
        "(> 365 d) | H outside 25% falls |",
        "|---|---:|---:|---|---|---|---|",
    ]
    out = []
    for name, c in sets:
        w = np.concatenate(c.ws).astype(bool)
        e = np.concatenate(c.es).astype(bool)
        sp = np.concatenate(c.speeds)

        out.append(
            f"| {name} | {int(e.sum()):,} | {(w & e).sum() / max(e.sum(), 1):.2f} | "
            + " | ".join(hit_txt(w, e, sp == k) for k in (1, 2, 3))
            + f" | {hit_txt(w, e, sp == 0)} |"
        )
    return head + out


def report() -> str:
    fr = [weekly(n, d, px, pos, np.ones(len(px), dtype=bool)) for n, d, px, pos in french()]
    sx = [weekly(n, d, px, pos, ok) for n, d, px, pos, ok in six()]
    x, n = PRIMARY
    mkt, ind = fr[:1], fr
    prim: list[tuple[str, Cell]] = [("US market 1927-2025", cell(mkt, x, n))]
    for era, lo, hi in ERAS:
        prim.append((f"US market {era}", cell(mkt, x, n, lo, hi)))
    prim.append(("11 French series, pooled", cell(ind, x, n)))
    for era, lo, hi in ERAS:
        prim.append((f"11 French series {era}", cell(ind, x, n, lo, hi)))
    six_sets: list[tuple[str, Cell]] = [(w.name, cell([w], x, n)) for w in sx]
    six_sets.append(("Six, pooled", cell(sx, x, n)))
    etfs = [w for w in sx if w.name in ("SPY", "QQQ", "GLD", "TLT")]
    six_sets.append(("Four ETFs, pooled", cell(etfs, x, n)))
    alt = [(f"{w.name}, 20% in 13 wk", cell([w], 0.20, 13)) for w in sx]
    span = ", ".join(f"{w.name} {w.fri[0]}..{w.fri[-1]}" for w in sx)
    md = [
        "# rev-costloss-1 results (generated by `research/lib/revcostloss1.py`; do not edit)",
        "",
        "Card: `research/cards/rev-costloss-1.md`. Forecast = each eligible Friday; warning = "
        "`tsmom12` out for the next week. Event = the total-return close falls at least X "
        "below the Friday close within N weeks. H hit rate, F false-alarm rate, PSS = H - F "
        "(= the maximum of V, at C/L = s). V(C/L) = relative economic value (Richardson 2000): "
        "0 = climatology, 1 = perfect. Rotations: the rule's own warnings shifted to random "
        f"dates ({ROTATIONS:,}, seed {SEED}); p = share with PSS at least the rule's. "
        "alpha_hold = a holder's cost/loss ratio from the weekly returns (card, bridge 2); "
        "V_money = (rule - hold) / (perfect - hold) in weekly log returns, cash 0, no costs. "
        "Nothing after 2025-10-31 is used.",
        "",
        f"Forecast Fridays: French series {fr[0].fri[0]}..{fr[0].fri[-1]}; six: {span}.",
        "",
        f"## Primary event: {x:.0%} fall within {n} weeks",
        "",
        *main_rows(prim + six_sets),
        "",
        "## V(C/L), primary event",
        "",
        *curve_rows(prim[:1] + prim[4:5] + six_sets[-2:]),
        "",
        "## Where the false alarms and misses sit (insure-1's 25% / 25% zigzag), primary event",
        "",
        *where_rows(prim + six_sets),
        "",
        "## Hit rate by fall speed (event weeks inside a 25% fall, by its peak-to-trough days)",
        "",
        *speed_rows(prim[:1] + prim[4:5] + six_sets[-2:]),
        "",
        "## All event definitions",
        "",
        *GRID_HEAD,
        *grid_rows("US market", mkt),
        *grid_rows("11 French series", ind),
        *grid_rows("Six, pooled", sx),
        "",
        "## The six at 20% within 13 weeks (coins' primary base rates are near 1)",
        "",
        *main_rows(alt),
        "",
    ]
    return "\n".join(md)


def main() -> None:
    md = report()
    OUT.write_text(md)
    print(md)


if __name__ == "__main__":
    main()
