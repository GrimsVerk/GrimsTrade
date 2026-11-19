"""fast-reentry: does `or3-12` (12-month OR 3-month return positive) keep more of `tsmom12`'s
crash insurance after the low? Card: research/cards/fast-reentry.md.

    uv run python -I research/lib/fastreentry.py [--no-log]

Both rules as gym-free paper series (trend-tune's `paper` mechanics: Friday decisions, next
session, 2 bps a side, cash at 0) on insure-1's US series (French daily market + 10 industries,
1927-2025) and insure-2's 13 developed indices and 3 French total-return regions. Episodes,
clusters and metrics are insure-1/insure-2's, reused through their modules; both rules are scored
on the same episodes. Writes research/results/fast-reentry.md; rows go to research/tries.md once
(`--no-log` skips them). Nothing after 2025-10-31 is parsed. Needs insure-2's setup (saved
trend-1926 runs, macro.local.json, insure-2's data cache).
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import insure2 as i2  # noqa: E402
import trend_1926 as t  # noqa: E402
import trend_tune as tt  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade import gym  # noqa: E402
from grimstrade.data import ETF, UNIVERSE  # noqa: E402

IDEA = "fast-reentry"
RULE = "or3-12"
OUT = harness.RESEARCH / "results" / "fast-reentry.md"
FAST_M, SLOW_M = 3, 12


# --- the two rules on one series ---


@dataclass
class Pair:
    ts: i1.Series  # tsmom12
    fr: i1.Series  # or3-12
    exits: int  # tsmom12 exits (1 -> 0) from the series' start
    delayed: int  # of those, sessions where or3-12 stayed in


def positions(panel: harness.Panel, s: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """`tt.paper`'s loop, keeping the positions: eligible, 12-month, OR rule."""
    dts = panel.ord[s]
    n = len(dts)
    p12, por = np.zeros(n), np.zeros(n)
    ok = np.zeros(n, dtype=bool)
    first = date.fromordinal(int(dts[0]))
    fri = first + timedelta(days=(tt.FRIDAY - first.weekday()) % 7)
    last = date.fromordinal(int(dts[-1]))
    while fri < last:
        view = panel.view(harness.decide_time(fri))
        lo = int(np.searchsorted(dts, fri.toordinal(), side="right"))
        hi = int(np.searchsorted(dts, fri.toordinal() + 7, side="right"))
        if c.eligible(view, s):
            ok[lo:hi] = True
            slow = tt.signal(view, s, SLOW_M)
            p12[lo:hi] = 1.0 if slow else 0.0
            por[lo:hi] = 1.0 if (slow or tt.signal(view, s, FAST_M)) else 0.0
        fri += timedelta(days=7)
    return ok, p12, por


def pair(name: str, days: list[date], ret: np.ndarray, rf: dict[date, float] | None,
         start: date | None) -> Pair:  # fmt: skip
    """Both rules' Series. US (start given): from the first session on or after `start`, as
    insure-1's `build`; non-US (start None): from the session before the first eligible one, as
    insure-2's `build_geo`."""
    sym = f"FR-{name}"
    UNIVERSE[sym] = ETF  # research process only; src/ is untouched
    bars = t.bars(days, ret)
    panel = harness.Panel({sym: bars})
    ok, p12, por = positions(panel, sym)
    cost = gym.COSTS[UNIVERSE[sym]]
    one_way = cost.fee + cost.slip
    close = np.array([b.close for b in bars])
    bar = i2.simple(close)

    def rets(pos: np.ndarray) -> np.ndarray:
        return pos * bar - one_way * np.abs(np.diff(pos, prepend=0.0))

    r12, ror = rets(p12), rets(por)
    ref = tt.paper(harness.Panel({sym: bars}), sym, (12,)).ret[12]
    if np.max(np.abs(ref - r12)) > 1e-15:
        raise AssertionError(f"{name}: tsmom12 replay differs from trend-tune's paper series")
    bdays = [b.date for b in bars]
    if start is not None:
        k = next(i for i, d in enumerate(bdays) if d >= start)
    else:
        k = max(int(np.argmax(ok)) - 1, 0)
    sd, px = bdays[k:], close[k:] / close[k]
    rfa = np.array([(rf or {}).get(d, 0.0) for d in sd])

    def series(r: np.ndarray, pos: np.ndarray) -> i1.Series:
        x = r[k:].copy()
        x[0] = 0.0
        return i1.Series(name, sd, px, x, x.copy(), pos[k:], rfa, 0.0)

    d12 = np.diff(p12[k:])
    ex = np.nonzero(d12 < 0)[0] + 1
    return Pair(series(r12, p12), series(ror, por), len(ex), int((por[k:][ex] > 0).sum()))


def load_us() -> list[Pair]:
    snap = sorted(p for p in (cache_root() / "french").iterdir() if p.is_dir())[-1]
    fac = t.parse_factors(i1._lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), i1.LAST)
    ind = t.parse_industries(i1._lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), i1.LAST)
    days = sorted(d for d in fac if d >= i1.FIRST)
    rf = {d: fac[d][1] for d in days}
    out = [pair(t.MKT, days, np.array([fac[d][0] for d in days]), rf, i1.START)]
    for j, n in enumerate(t.INDUSTRIES):
        r = np.array([ind[d][j] for d in days])
        keep = ~np.isnan(r)
        dd = [d for d, ok in zip(days, keep, strict=True) if ok]
        out.append(pair(n, dd, r[keep], rf, i1.START))
    return out


def load_geo() -> tuple[list[Pair], list[Pair]]:
    root = cache_root() / i2.RAW
    dev = [pair(n, *i2.load_yahoo(root / "yahoo" / f"{tk}.json"), None, None)
           for tk, n in i2.PRIMARY_GEO.items()]  # fmt: skip
    reg = [pair(n, *i2.load_french_region(root / "french" / f), None, None)
           for f, n in i2.FRENCH_GEO.items()]  # fmt: skip
    return dev, reg


# --- scoring ---


@dataclass
class SetScore:
    label: str
    pairs: list[Pair]
    sc_ts: list[i1.Scored]
    sc_fr: list[i1.Scored]
    clusters: list[list[i1.Episode]]  # tsmom12's episode objects
    twin: dict[int, i1.Episode]  # id(tsmom12 episode) -> or3-12 episode


def score_set(label: str, pairs: list[Pair], us_anchor: Sequence[i1.Episode] | None) -> SetScore:
    sc_ts = [i1.score(p.ts, *i1.PRIMARY) for p in pairs]
    sc_fr = [i1.score(p.fr, *i1.PRIMARY) for p in pairs]
    twin: dict[int, i1.Episode] = {}
    for a, b in zip(sc_ts, sc_fr, strict=True):
        for x, y in zip(a.eps, b.eps, strict=True):
            if x.idx != y.idx:
                raise AssertionError("episodes differ between rules")
            twin[id(x)] = y
    eps = [e for x in sc_ts for e in x.eps]
    cl = i1.market_anchored(eps, t.MKT) if us_anchor is None else i2.anchored(us_anchor, eps)
    return SetScore(label, pairs, sc_ts, sc_fr, cl, twin)


F = Callable[[i1.Episode], float]


def cvals(ss: SetScore, f: F, fr: bool) -> list[float]:
    return [float(np.mean([f(ss.twin[id(e)] if fr else e) for e in g])) for g in ss.clusters]


def dvals(ss: SetScore, f: F) -> list[float]:
    return [a - b for a, b in zip(cvals(ss, f, True), cvals(ss, f, False), strict=True)]


def premium(scs: Sequence[i1.Scored]) -> tuple[float, float, float, float]:
    si = sum(e.ins for x in scs for e in x.eps)
    sb = sum(e.rebound for x in scs for e in x.eps)
    cc = sum(x.calm for x in scs)
    return (-(sb + cc) / si if si > 0 else float("inf")), si, sb, cc


def series_years(ss: SetScore, lo: date, hi: date) -> float:
    return sum(max(0, (min(hi, p.ts.days[-1]) - max(lo, p.ts.days[0])).days) / 365.25
               for p in ss.pairs)  # fmt: skip


def era_premium(scs: Sequence[i1.Scored], lo: date, hi: date) -> tuple[float, float]:
    """Pooled premium and rule-minus-holding sum over a window: episodes by peak, calm by date."""
    a = b = cc = 0.0
    for x in scs:
        for e in x.eps:
            if lo <= e.peak <= hi:
                a += e.ins
                b += e.rebound
        d = 100 * (np.log1p(x.s.rule) - i2.logret(x.s.px))
        d[0] = 0.0
        m = np.array([lo <= dd <= hi for dd in x.s.days]) & ~x.in_mask
        cc += float(d[m].sum())
    return (-(b + cc) / a if a > 0 else float("inf")), a + b + cc


# --- report ---


def set_section(ss: SetScore, eras: Sequence[tuple[str, date, date]]) -> tuple[list[str], dict]:
    n = len(ss.clusters)
    ins, reb, net = (lambda e: e.ins), (lambda e: e.rebound), (lambda e: e.net)
    share = lambda e: e.share  # noqa: E731
    d_n = dvals(ss, net)
    k, m_, p_sign = i1.sign_test(d_n)
    mean_dn, p_boot, lo, hi = i1.boot(d_n)
    p_ts, si_ts, sb_ts, c_ts = premium(ss.sc_ts)
    p_fr, si_fr, sb_fr, c_fr = premium(ss.sc_fr)
    s_ts, s_fr = float(np.mean(cvals(ss, share, False))), float(np.mean(cvals(ss, share, True)))
    first = min(p.ts.days[0] for p in ss.pairs)
    yrs = series_years(ss, first, i1.LAST)
    tot_ts = sum(x.total for x in ss.sc_ts) / yrs
    tot_fr = sum(x.total for x in ss.sc_fr) / yrs
    exits = sum(p.exits for p in ss.pairs)
    delayed = sum(p.delayed for p in ss.pairs)

    def row(label: str, f: F, fmt: str = "+.1f") -> str:
        a, b = cvals(ss, f, False), cvals(ss, f, True)
        d = [y - x for x, y in zip(a, b, strict=True)]
        return (f"| {label} | {np.mean(a):{fmt}} | {np.mean(b):{fmt}} | {np.mean(d):{fmt}} | "
                f"{sum(x > 0 for x in d)} of {sum(x != 0 for x in d)} |")  # fmt: skip

    out = [
        f"### {ss.label}",
        "",
        f"Effective falls (clusters): {n}; episodes: {sum(len(g) for g in ss.clusters)}.",
        "",
        "| Mean over effective falls | `tsmom12` | `or3-12` | Difference | Falls where `or3-12` "
        "is higher |",
        "|---|---:|---:|---:|---:|",
        row("I, loss avoided peak -> trough", ins),
        row("B, the year after the low", reb),
        row("**N = I + B**", net),
        row("S, share of the fall avoided", share, "+.2f"),
        f"| N > 0 (falls) | {sum(v > 0 for v in cvals(ss, net, False))} of {n} | "
        f"{sum(v > 0 for v in cvals(ss, net, True))} of {n} | | |",
        "",
        f"Test of the difference in N (H1: `or3-12` higher): sign test {k} of {m_}, "
        f"p {p_sign:.2g}; "
        f"cluster bootstrap mean {mean_dn:+.1f}, p {p_boot:.3f}, 90% range {lo:+.1f} to {hi:+.1f}.",
        "",
        "| Full period | `tsmom12` | `or3-12` |",
        "|---|---:|---:|",
        f"| Sum I / sum B / C, log pts | {si_ts:+.0f} / {sb_ts:+.0f} / {c_ts:+.0f} | "
        f"{si_fr:+.0f} / {sb_fr:+.0f} / {c_fr:+.0f} |",
        f"| **Premium P** | **{p_ts:.2f}** | **{p_fr:.2f}** |",
        f"| Rule minus holding, log pts per series-year | {tot_ts:+.2f} | {tot_fr:+.2f} |",
        f"| Mean position | {np.mean([p.ts.pos[1:].mean() for p in ss.pairs]):.0%} | "
        f"{np.mean([p.fr.pos[1:].mean() for p in ss.pairs]):.0%} |",
        f"| Position flips a year (mean over series) | "
        f"{np.mean([i1.sharpe_row(p.ts)[3] for p in ss.pairs]):.2f} | "
        f"{np.mean([i1.sharpe_row(p.fr)[3] for p in ss.pairs]):.2f} |",
        f"| Worst loss, first series ({ss.pairs[0].ts.name}) | "
        f"{i1.maxdd(np.cumprod(1 + ss.pairs[0].ts.rule)):.0%} | "
        f"{i1.maxdd(np.cumprod(1 + ss.pairs[0].fr.rule)):.0%} |",
        "",
        f"`tsmom12` exits: {exits}; `or3-12` stayed in at {delayed} of them (3-month return "
        "still positive).",
        "",
    ]
    out += ["| Era (episodes by peak, calm by date) | Premium `tsmom12` | Premium `or3-12` | "
            "Rule minus holding per series-year: `tsmom12` / `or3-12` |",
            "|---|---:|---:|---|"]  # fmt: skip
    for key, a, b in eras:
        pa, ta = era_premium(ss.sc_ts, a, b)
        pb, tb = era_premium(ss.sc_fr, a, b)
        y = series_years(ss, a, b)
        out.append(f"| {key} | {pa:.2f} | {pb:.2f} | {ta / y:+.2f} / {tb / y:+.2f} |")
    out += ["", "| Peak to trough (episode level) | Episodes | Mean dI | Mean dB | Mean dN | "
            "dN > 0 | `tsmom12` N | `or3-12` N |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    eps = [e for x in ss.sc_ts for e in x.eps]
    for label, lo_d, hi_d in (("fast, <= 92 days", 0, i1.FAST),
                              ("medium, 93-365", i1.FAST + 1, i1.MEDIUM),
                              ("slow, > 365", i1.MEDIUM + 1, 10**6)):  # fmt: skip
        ee = [e for e in eps if lo_d <= e.days <= hi_d]
        if not ee:
            continue
        di = [ss.twin[id(e)].ins - e.ins for e in ee]
        db = [ss.twin[id(e)].rebound - e.rebound for e in ee]
        dn = [a + b for a, b in zip(di, db, strict=True)]
        out.append(
            f"| {label} | {len(ee)} | {np.mean(di):+.1f} | {np.mean(db):+.1f} | "
            f"{np.mean(dn):+.1f} | {sum(x > 0 for x in dn)} | "
            f"{np.mean([e.net for e in ee]):+.1f} | "
            f"{np.mean([ss.twin[id(e)].net for e in ee]):+.1f} |"
        )
    out += ["", "Effective falls, largest |dN| first (10):", "",
"| First peak | Last trough | Episodes | Mean depth | `tsmom12` N | `or3-12` N | "
            "dI | dB | dN |", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    rows = []
    for g, dn_ in zip(ss.clusters, d_n, strict=True):
        di_ = float(np.mean([ss.twin[id(e)].ins - e.ins for e in g]))
        rows.append((abs(dn_), (
            f"| {min(e.peak for e in g)} | {max(e.trough for e in g)} | {len(g)} | "
            f"{i1.cmean(g, lambda e: e.depth):.0%} | {i1.cmean(g, net):+.0f} | "
            f"{float(np.mean([ss.twin[id(e)].net for e in g])):+.0f} | {di_:+.0f} | "
            f"{dn_ - di_:+.0f} | {dn_:+.0f} |"
        )))  # fmt: skip
    out += [r for _, r in sorted(rows, key=lambda x: -x[0])[:10]] + [""]
    stats = {"mean_dn": mean_dn, "p_sign": p_sign, "p_boot": p_boot, "p_ts": p_ts, "p_fr": p_fr,
             "s_ts": s_ts, "s_fr": s_fr, "k": k, "m": m_, "n": n}  # fmt: skip
    return out, stats


def verdict(us: dict, dev: dict) -> str:
    if us["mean_dn"] <= 0 or us["p_fr"] >= us["p_ts"]:
        return "Gives back more (no help)"
    if (us["p_sign"] < 0.05 and us["p_boot"] < 0.05 and dev["mean_dn"] > 0
            and dev["p_fr"] < dev["p_ts"] and us["s_fr"] >= us["s_ts"] - 0.10):  # fmt: skip
        return "Keeps more of the insurance"
    return "In between"


def log_tries(us: list[Pair], geo: list[Pair]) -> int:
    text = harness.TRIES.read_text()
    rows = []
    for p, tag in [(x, "insure") for x in us] + [(x, "insure-geo") for x in geo]:
        v = f"{RULE}@{tag}-{p.fr.name}"
        if f"| {IDEA} | {v} |" in text:
            continue
        kind = "variant" if (tag == "insure" and p.fr.name == t.MKT) else "robustness"
        sh, tot, mdd, fl = i1.sharpe_row(p.fr)
        rows.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {v} | {kind} | train | "
            f"{p.fr.days[0]} | {p.fr.days[-1]} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(rows)
    return len(rows)


def main() -> None:
    us = load_us()
    dev, reg = load_geo()
    ss_us = score_set("US: market + 10 industries, 1927-2025 (decides)", us, None)
    us_mkt = ss_us.sc_ts[0].eps  # the US market's 25% falls: insure-2's anchors
    ss_dev = score_set("Non-US: 13 developed indices, price (decides, direction)", dev, us_mkt)
    ss_reg = score_set("French regions, total return, USD (description)", reg, us_mkt)
    t_us, st_us = set_section(ss_us, i1.ERAS)
    t_dev, st_dev = set_section(ss_dev, i2.GEO_ERAS)
    t_reg, _ = set_section(ss_reg, i2.GEO_ERAS)
    v = verdict(st_us, st_dev)
    head = [
        "# fast-reentry: `or3-12` against `tsmom12` on insure-1/2's crash episodes",
        "",
        "Card: `cards/fast-reentry.md`. Written by `lib/fastreentry.py`. Log points = 100 x "
        "natural log; I, B, N are rule minus holding; differences are `or3-12` minus `tsmom12` "
        "(dI, dB, dN). Both rules as paper series (Friday decisions, 2 bps a side, cash at 0), "
        "scored on the same 25% episodes; clusters as insure-1 (US, market-anchored) and "
        "insure-2 (non-US, anchored on the US market's falls).",
        "",
        f"**Verdict by the card: {v}.** US mean dN {st_us['mean_dn']:+.1f} (sign test "
        f"{st_us['k']} of {st_us['m']}, p {st_us['p_sign']:.2g}; "
        f"bootstrap p {st_us['p_boot']:.3f}); "
        f"non-US mean dN {st_dev['mean_dn']:+.1f}; premium US {st_us['p_ts']:.2f} -> "
        f"{st_us['p_fr']:.2f}, non-US {st_dev['p_ts']:.2f} -> {st_dev['p_fr']:.2f}; share avoided "
        f"US {st_us['s_ts']:.2f} -> {st_us['s_fr']:.2f}.",
        "",
    ]
    OUT.write_text("\n".join(head + t_us + t_dev + t_reg))
    n = 0 if "--no-log" in sys.argv else log_tries(us, dev + reg)
    print(f"wrote {OUT}; {n} new tries.md rows; verdict: {v}")


if __name__ == "__main__":
    main()
