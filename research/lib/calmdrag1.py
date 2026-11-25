"""calm-drag-1: what the calm-market drag of `tsmom12` is made of. Card: cards/calm-drag-1.md.

    uv run python -I research/lib/calmdrag1.py

Descriptive re-score, no new rule. The calm drag C (gap-2002-1's by-date calm part of
`tsmom12` minus holding, log points a year) split exactly into trading cost K and out-time O;
O into premium P (calm out-sessions at the average calm excess return) and timing T, and by
out-spell (edge spells: calm days before / between / after a fall episode; calm-only spells:
dip gain G and lag loss L, whipsaw losses W- and saved dips W+, short and long spells).
Series: the six live assets (rev-costloss-1's `six()`), the French US market and 10
industries (gap-2002-1's `french()`), the S&P 500 TR (insure-3). Nothing after 2025-10-31.
Writes research/results/calm-drag-1.md.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass, fields
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402

LAST = date(2025, 10, 31)
DOWN = UP = 0.25
REBOUND = 365
SHORT = 91  # calendar days, first to last out session
FR_START = date(1927, 7, 2)
ERAS = (
    ("1927-1961", FR_START, date(1961, 12, 31)),
    ("1962-2001", date(1962, 1, 1), date(2001, 12, 31)),
    ("2002-2025", date(2002, 1, 1), LAST),
)
OUT = harness.RESEARCH / "results" / "calm-drag-1.md"


@dataclass
class Ser:
    name: str
    days: list[date]
    hold: np.ndarray  # simple return per session (index 0 ignored)
    pos: np.ndarray  # position earning that session's return
    ok: np.ndarray  # eligible (the rule could hold)
    rf: np.ndarray  # bill simple return per session
    cost: float  # one way
    rule0: np.ndarray  # the paper series at cash 0 (check)
    ruleb: np.ndarray  # at bills (check)


@dataclass
class Parts:
    c: float = 0.0
    k: float = 0.0
    o: float = 0.0
    p: float = 0.0
    t: float = 0.0
    e_pre: float = 0.0
    e_mid: float = 0.0
    e_post: float = 0.0
    g: float = 0.0
    lag: float = 0.0
    w_minus: float = 0.0
    w_plus: float = 0.0
    short: float = 0.0
    long: float = 0.0
    out_share: float = 0.0  # of calm sessions
    calm_share: float = 0.0  # of window sessions
    spells_yr: float = 0.0  # calm-only spells a year
    med_days: float = 0.0  # median calm-only spell length, calendar days
    flips_yr: float = 0.0  # calm flip sessions a year
    resid: float = 0.0  # max |C - parts| checks


def zigzag(px: np.ndarray, down: float = DOWN, up: float = UP) -> list[tuple[int, int]]:
    import gap2002

    return gap2002.zigzag(px, down, up)


def labels(
    days: Sequence[date], hold: np.ndarray, down: float = DOWN, up: float = UP
) -> np.ndarray:
    """0 calm, 1 fall, 2 rebound: gap-2002-1's by-date labels."""
    hl = np.zeros(len(hold))
    hl[1:] = np.log1p(hold[1:])
    px = np.exp(np.cumsum(hl))
    ords = np.array([x.toordinal() for x in days])
    part = np.zeros(len(hold), dtype=int)
    pairs = zigzag(px, down, up)
    for j, (a, b) in enumerate(pairs):
        e = int(np.searchsorted(ords, days[b].toordinal() + REBOUND, side="right")) - 1
        if j + 1 < len(pairs):
            e = min(e, pairs[j + 1][0])
        part[a + 1 : b + 1] = 1
        part[b + 1 : e + 1] = 2
    return part


def spells(out: np.ndarray) -> list[tuple[int, int]]:
    """Maximal runs [a, b] of True."""
    res: list[tuple[int, int]] = []
    i, n = 0, len(out)
    while i < n:
        if out[i]:
            j = i
            while j + 1 < n and out[j + 1]:
                j += 1
            res.append((i, j))
            i = j + 1
        else:
            i += 1
    return res


def decompose(s: Ser, lo: date, hi: date, bills: bool, part: np.ndarray | None = None) -> Parts:
    if part is None:
        part = labels(s.days, s.hold)
    n = len(s.days)
    ords = np.array([d.toordinal() for d in s.days])
    win = s.ok & (ords >= lo.toordinal()) & (ords <= hi.toordinal())
    win[0] = False
    first_ok = s.days[int(np.argmax(s.ok & (np.arange(n) > 0)))]
    lo_eff = max(lo, first_ok)
    yrs = (hi - lo_eff).days / 365.25
    rf = s.rf if bills else np.zeros(n)
    flip = np.abs(np.diff(s.pos, prepend=0.0))
    r = s.pos * s.hold - s.cost * flip + (1 - s.pos) * rf
    ref = s.ruleb if bills else s.rule0
    if np.max(np.abs((r - ref)[win])) > 1e-12:
        raise AssertionError(f"{s.name}: rebuilt rule differs from the paper series")
    h = 100 * np.log1p(s.hold)
    d = 100 * np.log1p(r) - h
    calm = win & (part == 0)
    kk = 100 * (np.log1p(r) - np.log1p(r + s.cost * flip))
    x = h - 100 * np.log1p(rf)
    outm = calm & (s.pos == 0)
    oo = np.where(outm, -x, 0.0)
    res = Parts()
    res.c = float(d[calm].sum()) / yrs
    res.k = float(kk[calm].sum()) / yrs
    res.o = float(oo.sum()) / yrs
    resid = abs(res.c - res.k - res.o)
    m = float(x[calm].mean()) if calm.any() else 0.0
    res.p = -int(outm.sum()) * m / yrs
    res.t = res.o - res.p
    lens = []
    for a, b in spells(s.ok & (s.pos == 0)):
        idx = np.arange(a, b + 1)
        cw = idx[calm[idx]]
        if not len(cw):
            continue
        nc = idx[part[idx] != 0]
        if len(nc):
            res.e_pre += float(oo[cw[cw < nc[0]]].sum())
            res.e_post += float(oo[cw[cw > nc[-1]]].sum())
            res.e_mid += float(oo[cw[(cw > nc[0]) & (cw < nc[-1])]].sum())
            continue
        xs = np.concatenate([[0.0], np.cumsum(x[cw])])
        js = int(np.argmin(xs))
        res.g += -float(xs[js])
        res.lag += -float(xs[-1] - xs[js])
        tot = -float(xs[-1])
        if xs[-1] > 0:
            res.w_minus += tot
        else:
            res.w_plus += tot
        ln = (s.days[b] - s.days[a]).days
        lens.append(ln)
        if ln <= SHORT:
            res.short += tot
        else:
            res.long += tot
    for f in ("e_pre", "e_mid", "e_post", "g", "lag", "w_minus", "w_plus", "short", "long"):
        setattr(res, f, getattr(res, f) / yrs)
    by_spell = res.e_pre + res.e_mid + res.e_post + res.g + res.lag
    resid = max(resid, abs(res.o - by_spell),
                abs(res.o - res.e_pre - res.e_mid - res.e_post - res.w_minus - res.w_plus),
                abs(res.o - res.e_pre - res.e_mid - res.e_post - res.short - res.long))  # fmt: skip
    res.resid = resid
    res.out_share = float(outm.sum()) / max(int(calm.sum()), 1)
    res.calm_share = float(calm.sum()) / max(int(win.sum()), 1)
    res.spells_yr = len(lens) / yrs
    res.med_days = float(np.median(lens)) if lens else 0.0
    res.flips_yr = float((calm & (flip > 0)).sum()) / yrs
    return res


def mean_parts(ps: Sequence[Parts]) -> Parts:
    out = Parts()
    for f in fields(Parts):
        setattr(out, f.name, float(np.mean([getattr(p, f.name) for p in ps])))
    out.resid = max(p.resid for p in ps)
    return out


# --- loaders (the projects' own) ---


def repair(pos: np.ndarray, hold: np.ndarray, rule0: np.ndarray, cost: float) -> np.ndarray:
    """`infer_pos` keeps the old position when a flip day has a zero return (both fit); take
    the position that reproduces the paper series' cost on that day instead."""

    def fits(i: int, v: float, prev: float) -> bool:
        return abs(v * hold[i] - cost * abs(v - prev) - rule0[i]) < 1e-12

    p = pos.copy()
    n = len(p)
    for i in range(1, n):
        cand = [v for v in (p[i], 1.0 - p[i]) if fits(i, v, p[i - 1])]
        if len(cand) > 1 and i + 1 < n:  # both fit (a zero or cost-sized return): look ahead
            cand = [v for v in cand if fits(i + 1, p[i + 1], v) or fits(i + 1, 1 - p[i + 1], v)]
        if cand:
            p[i] = cand[0]
    return p


def irx() -> dict[date, float]:
    import insure3 as i3
    from macro import cache_root

    p = cache_root() / "yahoo-1d" / "2026-11-12" / "^IRX.json"
    return i3.parse_yahoo(json.loads(p.read_text()))  # type: ignore[no-any-return]


def load_french() -> list[Ser]:
    import insure1 as i1
    import trend_1926 as t
    from macro import cache_root

    snap = sorted(p for p in (cache_root() / "french").iterdir() if p.is_dir())[-1]
    fac = t.parse_factors(i1._lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), i1.LAST)
    ind = t.parse_industries(i1._lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), i1.LAST)
    days = sorted(d for d in fac if d >= i1.FIRST)
    rf = {d: fac[d][1] for d in days}
    raw = [(t.MKT, days, np.array([fac[d][0] for d in days]))]
    for j, nm in enumerate(t.INDUSTRIES):
        rr = np.array([ind[d][j] for d in days])
        keep = ~np.isnan(rr)
        raw.append((nm, [d for d, k in zip(days, keep, strict=True) if k], rr[keep]))
    out = []
    for nm, dd, rr in raw:
        s = i1.build(nm, dd, rr, rf, None)
        hold = np.zeros(len(s.px))
        hold[1:] = s.px[1:] / s.px[:-1] - 1
        ok = np.ones(len(hold), dtype=bool)
        pos = repair(s.pos, hold, s.paper, 0.0002)
        # the bills series is built from these positions, so its check is circular; the
        # cash-0 check against the paper series carries the weight
        out.append(Ser(nm, s.days, hold, pos, ok, s.rf, 0.0002, s.paper,
                       s.paper + (1 - pos) * s.rf))  # fmt: skip
    return out


def load_spx(bill: dict[date, float]) -> Ser:
    import insure1 as i1
    import insure3 as i3

    days, s, _, _ = i3.load()
    hold, r0, rb = s["hold"], s["trend@cash0"], s["trend"]
    pos = i1.infer_pos(r0, hold, i3.COST)
    if abs(r0[1] - pos[1] * hold[1]) < 1e-12:  # the window opens already in that position
        pos[0] = pos[1]
    pos = repair(pos, hold, r0, i3.COST)
    rf = i3.bill_returns(days, bill)
    ok = np.ones(len(hold), dtype=bool)
    return Ser("S&P 500 TR", list(days), hold, pos, ok, rf, i3.COST, r0, rb)


def load_six(bill: dict[date, float]) -> list[Ser]:
    import insure3 as i3
    import revcostloss1 as rc

    from grimstrade import gym
    from grimstrade.data import UNIVERSE

    out = []
    for nm, days, close, pos, ok in rc.six():
        hold = np.zeros(len(close))
        hold[1:] = close[1:] / close[:-1] - 1
        cost = gym.COSTS[UNIVERSE[nm]]
        c = cost.fee + cost.slip
        r0 = pos * hold - c * np.abs(np.diff(pos, prepend=0.0))
        rf = i3.bill_returns(days, bill)
        out.append(Ser(nm, list(days), hold, pos, np.asarray(ok, dtype=bool), rf, c, r0,
                       r0 + (1 - pos) * rf))  # fmt: skip
    return out


# --- report ---

HA = ("| Series | Window | Calm share | C | Cost K | Out O | Premium P | Timing T | Out share "
      "of calm | Calm flips / yr |")  # fmt: skip
HB = ("| Series | Window | O | E-pre | E-mid | E-post | Calm-only: G (dip) | L (lag) | W- (back "
      "higher) | W+ (saved) | <=13 wk | >13 wk | Spells / yr | Median days |")  # fmt: skip


def ra(nm: str, w: str, p: Parts) -> str:
    return (f"| {nm} | {w} | {p.calm_share:.2f} | {p.c:+.2f} | {p.k:+.2f} | {p.o:+.2f} | "
            f"{p.p:+.2f} | {p.t:+.2f} | {p.out_share:.3f} | {p.flips_yr:.2f} |")  # fmt: skip


def rb(nm: str, w: str, p: Parts) -> str:
    return (f"| {nm} | {w} | {p.o:+.2f} | {p.e_pre:+.2f} | {p.e_mid:+.2f} | {p.e_post:+.2f} | "
            f"{p.g:+.2f} | {p.lag:+.2f} | {p.w_minus:+.2f} | {p.w_plus:+.2f} | {p.short:+.2f} | "
            f"{p.long:+.2f} | {p.spells_yr:.2f} | {p.med_days:.0f} |")  # fmt: skip


def main() -> None:
    bill = irx()
    six = load_six(bill)
    fr = load_french()
    spx = load_spx(bill)
    rows: list[tuple[str, str, Parts, Parts]] = []

    def add(nm: str, s: Ser, lo: date, hi: date, part: np.ndarray) -> tuple[Parts, Parts]:
        p0, pb = decompose(s, lo, hi, False, part), decompose(s, lo, hi, True, part)
        first = s.days[int(np.argmax(s.ok & (np.arange(len(s.days)) > 0)))]
        w = f"{max(lo, first).year}-{hi.year}"
        rows.append((nm, w, p0, pb))
        return p0, pb

    for s in six:
        add(s.name, s, s.days[0], LAST, labels(s.days, s.hold))
    mk = fr[0]
    pm = labels(mk.days, mk.hold)
    add("French US market", mk, FR_START, LAST, pm)
    for nm, lo, hi in ERAS:
        add(f"French US market {nm}", mk, lo, hi, pm)
    ps = labels(spx.days, spx.hold)
    add("S&P 500 TR", spx, spx.days[0], LAST, ps)
    sp02 = add("S&P 500 TR 2002-2025", spx, date(2002, 1, 1), LAST, ps)
    ind = [(decompose(s, date(2002, 1, 1), LAST, False), decompose(s, date(2002, 1, 1), LAST, True))
           for s in fr[1:]]  # fmt: skip
    rows.append(("Mean, 10 industries", "2002-2025", mean_parts([a for a, _ in ind]),
                 mean_parts([b for _, b in ind])))  # fmt: skip
    fr02 = next(r for r in rows if r[0] == "French US market 2002-2025")
    resid = max(max(r[2].resid, r[3].resid) for r in rows)
    md = [
        "# calm-drag-1 results (generated by `research/lib/calmdrag1.py`; do not edit)",
        "",
        "Log points a year, `tsmom12` minus holding, calm sessions only (gap-2002-1's labels: "
        "outside every 25% / 25% zigzag fall and its 365-day rebound). C = K + O; O = P + T = "
        "E-pre + E-mid + E-post + G + L = E-pre + E-mid + E-post + W- + W+ = E + short + long "
        "(calm-only spells). Negative = costs the rule. Card: `research/cards/calm-drag-1.md`.",
        "",
        f"Checks: largest |C - sum of parts| over all rows {resid:.1e}. gap-2002-1's C "
        f"(cash 0): French market 2002-2025 {fr02[2].c:+.2f} (published -2.16), S&P 500 TR "
        f"2002-2025 {sp02[0].c:+.2f} (-1.65), mean of 10 industries {rows[-1][2].c:+.2f} "
        "(-1.85).",
        "",
    ]
    for tag, j in (("cash 0 (gym convention, primary)", 2), ("idle cash at bills", 3)):
        md += [f"## A. C = cost + premium + timing, {tag}", "", HA, "|---|---|" + "---:|" * 8]
        md += [ra(r[0], r[1], r[j]) for r in rows]  # type: ignore[arg-type]
        md += ["", f"## B. Out O by spell, {tag}", "", HB, "|---|---|" + "---:|" * 12]
        md += [rb(r[0], r[1], r[j]) for r in rows]  # type: ignore[arg-type]
        md += [""]
    md += ["## Industries 2002-2025, cash 0 (each)", "", HA, "|---|---|" + "---:|" * 8]
    md += [ra(s.name, "2002-2025", a) for s, (a, _) in zip(fr[1:], ind, strict=True)]
    md += ["", HB, "|---|---|" + "---:|" * 12]
    md += [rb(s.name, "2002-2025", a) for s, (a, _) in zip(fr[1:], ind, strict=True)]
    md += [""]
    # post hoc (not on the card): under 25% the coins have almost no calm sessions
    md += [
        "## Post hoc (not on the card): the coins with a 50% / 50% zigzag",
        "",
        "Under the card's 25% zigzag BTC and ETH have almost no calm sessions (table A), so the "
        "card says nothing about them. Diagnostic only, chosen after seeing that: falls of 50% "
        "down / 50% up, same rebound rule, everything else unchanged.",
        "",
    ]
    coin = [(s.name, decompose(s, s.days[0], LAST, False, labels(s.days, s.hold, 0.5, 0.5)),
             decompose(s, s.days[0], LAST, True, labels(s.days, s.hold, 0.5, 0.5)))
            for s in six if s.name in ("BTC", "ETH")]  # fmt: skip
    for tag, j in (("cash 0", 1), ("bills", 2)):
        md += [f"{tag}:", "", HA, "|---|---|" + "---:|" * 8]
        md += [ra(c[0], "own", c[j]) for c in coin]  # type: ignore[arg-type]
        md += ["", HB, "|---|---|" + "---:|" * 12]
        md += [rb(c[0], "own", c[j]) for c in coin]  # type: ignore[arg-type]
        md += [""]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
