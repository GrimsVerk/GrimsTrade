"""fast-reentry-2: (a) `or3-12` against insure-1's card 2 exposure controls (description);
(b) `arm3-12`: exit as `tsmom12`, re-enter when the 3-month return turns positive. Card:
research/cards/fast-reentry-2.md.

    uv run python -I research/lib/fastreentry2.py [--no-log]

Reuses fast-reentry's loaders, scoring and report (`fastreentry.py`) and insure-1's card 2
controls. Writes research/results/fast-reentry-2.md; rows go to research/tries.md once
(`--no-log` skips them). Nothing after 2025-10-31 is parsed. Needs insure-2's setup.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import fastreentry as fr  # noqa: E402
import harness  # noqa: E402
import insure1 as i1  # noqa: E402
import insure2 as i2  # noqa: E402
import trend_1926 as t  # noqa: E402
import trend_tune as tt  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade import gym  # noqa: E402
from grimstrade.data import ETF, UNIVERSE  # noqa: E402

RULE = "arm3-12"
OUT = harness.RESEARCH / "results" / "fast-reentry-2.md"
BAR = 0.025  # family bar, second pick in the insure line


# --- the three rules on one series ---


def positions(panel: harness.Panel, s: str) -> tuple[np.ndarray, ...]:
    """Friday decisions as `tt.paper`: eligible, tsmom12, or3-12, arm3-12 (card's steps 1-5)."""
    dts = panel.ord[s]
    n = len(dts)
    p12, por, parm = np.zeros(n), np.zeros(n), np.zeros(n)
    ok = np.zeros(n, dtype=bool)
    first = date.fromordinal(int(dts[0]))
    fri = first + timedelta(days=(tt.FRIDAY - first.weekday()) % 7)
    last = date.fromordinal(int(dts[-1]))
    pos, armed, reentered = 0.0, False, False
    while fri < last:
        view = panel.view(harness.decide_time(fri))
        lo = int(np.searchsorted(dts, fri.toordinal(), side="right"))
        hi = int(np.searchsorted(dts, fri.toordinal() + 7, side="right"))
        if not c.eligible(view, s):
            pos, armed, reentered = 0.0, False, False
        else:
            ok[lo:hi] = True
            slow = tt.signal(view, s, fr.SLOW_M)
            fast = tt.signal(view, s, fr.FAST_M)
            p12[lo:hi] = 1.0 if slow else 0.0
            por[lo:hi] = 1.0 if (slow or fast) else 0.0
            if slow:
                pos, armed, reentered = 1.0, False, False
            else:
                if pos > 0 and reentered:
                    pos = 1.0 if fast else 0.0
                else:
                    pos = 1.0 if (armed and fast) else 0.0
                reentered = pos > 0
                if not fast:
                    armed = True
            parm[lo:hi] = pos
        fri += timedelta(days=7)
    return ok, p12, por, parm


@dataclass
class Trio:
    ts: i1.Series
    orr: i1.Series
    arm: i1.Series
    exits: int  # tsmom12 exits
    fast_on: int  # of those, 3-month return still positive (or3-12 stays, arm3-12 leaves)


def trio(name: str, days: list[date], ret: np.ndarray, rf: dict[date, float] | None,
         start: date | None) -> Trio:  # fmt: skip
    """As `fr.pair`, with the third rule."""
    sym = f"FR2-{name}"
    UNIVERSE[sym] = ETF  # research process only; src/ is untouched
    bars = t.bars(days, ret)
    panel = harness.Panel({sym: bars})
    ok, p12, por, parm = positions(panel, sym)
    cost = gym.COSTS[UNIVERSE[sym]]
    one_way = cost.fee + cost.slip
    close = np.array([b.close for b in bars])
    bar = i2.simple(close)

    def rets(pos: np.ndarray) -> np.ndarray:
        return pos * bar - one_way * np.abs(np.diff(pos, prepend=0.0))

    ref = tt.paper(harness.Panel({sym: bars}), sym, (12,)).ret[12]
    if np.max(np.abs(ref - rets(p12))) > 1e-15:
        raise AssertionError(f"{name}: tsmom12 replay differs from trend-tune's paper series")
    bdays = [b.date for b in bars]
    if start is not None:
        k = next(i for i, d in enumerate(bdays) if d >= start)
    else:
        k = max(int(np.argmax(ok)) - 1, 0)
    sd, px = bdays[k:], close[k:] / close[k]
    rfa = np.array([(rf or {}).get(d, 0.0) for d in sd])

    def series(pos: np.ndarray) -> i1.Series:
        x = rets(pos)[k:].copy()
        x[0] = 0.0
        return i1.Series(name, sd, px, x, x.copy(), pos[k:], rfa, 0.0)

    ex = np.nonzero(np.diff(p12[k:]) < 0)[0] + 1
    if np.any(parm[k:][ex] > 0):
        raise AssertionError(f"{name}: arm3-12 did not leave at a tsmom12 exit")
    return Trio(series(p12), series(por), series(parm), len(ex), int((por[k:][ex] > 0).sum()))


def load_us() -> list[Trio]:
    snap = sorted(p for p in (cache_root() / "french").iterdir() if p.is_dir())[-1]
    fac = t.parse_factors(i1._lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), i1.LAST)
    ind = t.parse_industries(i1._lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), i1.LAST)
    days = sorted(d for d in fac if d >= i1.FIRST)
    rf = {d: fac[d][1] for d in days}
    out = [trio(t.MKT, days, np.array([fac[d][0] for d in days]), rf, i1.START)]
    for j, n in enumerate(t.INDUSTRIES):
        r = np.array([ind[d][j] for d in days])
        keep = ~np.isnan(r)
        dd = [d for d, ok in zip(days, keep, strict=True) if ok]
        out.append(trio(n, dd, r[keep], rf, i1.START))
    return out


def load_geo() -> tuple[list[Trio], list[Trio]]:
    root = cache_root() / i2.RAW
    dev = [trio(n, *i2.load_yahoo(root / "yahoo" / f"{tk}.json"), None, None)
           for tk, n in i2.PRIMARY_GEO.items()]  # fmt: skip
    reg = [trio(n, *i2.load_french_region(root / "french" / f), None, None)
           for f, n in i2.FRENCH_GEO.items()]  # fmt: skip
    return dev, reg


# --- (a) insure-1's card 2 controls for any rule ---


def controls(rule: str, ss: list[i1.Series]) -> list[str]:
    """insure-1's `card2` with the rule's own paper series and positions."""
    if any(s.days != ss[0].days for s in ss):
        raise ValueError("card 2 needs one session calendar for the 11 series")
    eps = [i1.score(s, *i1.PRIMARY).eps for s in ss]
    anch = i1.market_anchored([e for ee in eps for e in ee], t.MKT)
    clusters = [[(0, e) for e in g] for g in anch]
    hl, bar = [], []
    for s in ss:
        hl.append(np.concatenate([[0.0], np.log(s.px[1:] / s.px[:-1])]))
        bar.append(np.concatenate([[0.0], s.px[1:] / s.px[:-1] - 1]))
    me = i1.control_stats([s.paper for s in ss], hl, eps, clusters)
    xs = [float(s.pos[1:].mean()) for s in ss]
    fixed = i1.control_stats([x * b for x, b in zip(xs, bar, strict=True)], hl, eps, clusters)
    n = len(ss[0].px)
    rng = np.random.default_rng(i1.SEED)
    rots = []
    for _ in range(i1.ROTATIONS):
        k = int(rng.integers(365, n - 365))
        rr = []
        for s, b in zip(ss, bar, strict=True):
            p = np.roll(s.pos, k)
            r = p * b - 0.0002 * np.abs(np.diff(p, prepend=p[0]))
            r[0] = 0.0
            rr.append(r)
        rots.append(i1.control_stats(rr, hl, eps, clusters))
    rs = np.array([x.s_mean for x in rots])
    rn = np.array([x.n_mean for x in rots])
    rp = np.array([x.prem for x in rots])
    p_s = float((rs >= me.s_mean).mean())
    p_p = float((rp <= me.prem).mean())
    p_n = float((rn >= me.n_mean).mean())
    if p_s < 0.05 and p_p < 0.05 and me.prem < fixed.prem:
        label = "Timing, not just exposure"
    elif p_s >= 0.10 and p_p >= 0.10:
        label = "Exposure, not timing"
    else:
        label = "In between"
    return [
        f"| `{rule}` | {me.s_mean:+.2f} | {me.n_mean:+.1f} | {me.prem:.2f} |",
        f"| Fixed exposure (x = its average position, mean {np.mean(xs):.0%}) | "
        f"{fixed.s_mean:+.2f} | {fixed.n_mean:+.1f} | {fixed.prem:.2f} |",
        f"| Random timing (its positions rotated) | {i2.q(rs)} | {i2.q(rn, '+.1f')} | {i2.q(rp)} |",
        f"| p: rotations at least as good | {p_s:.3f} | {p_n:.3f} | {p_p:.3f} |",
        f"| **Reading: {label}** | | | |",
    ]


# --- (b) verdict and rows ---


def as_pairs(trios: list[Trio], which: str) -> list[fr.Pair]:
    return [fr.Pair(x.ts, getattr(x, which), x.exits, x.fast_on) for x in trios]


def verdict(us: dict, dev: dict) -> str:
    if us["mean_dn"] <= 0 or us["p_fr"] >= us["p_ts"]:
        return "Gives back more (no help)"
    if (us["p_sign"] < BAR and us["p_boot"] < BAR and dev["mean_dn"] > 0
            and dev["p_fr"] < dev["p_ts"] and us["s_fr"] >= us["s_ts"] - 0.10):  # fmt: skip
        return "Keeps more of the insurance"
    return "In between"


def log_tries(us: list[Trio], geo: list[Trio]) -> int:
    text = harness.TRIES.read_text()
    rows = []
    for x, tag in [(x, "insure") for x in us] + [(x, "insure-geo") for x in geo]:
        s = x.arm
        v = f"{RULE}@{tag}-{s.name}"
        if f"| {fr.IDEA} | {v} |" in text:
            continue
        kind = "variant" if (tag == "insure" and s.name == t.MKT) else "robustness"
        sh, tot, mdd, fl = i1.sharpe_row(s)
        rows.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {fr.IDEA} | {v} | {kind} | train | "
            f"{s.days[0]} | {s.days[-1]} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {fl:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(rows)
    return len(rows)


def section(ss: fr.SetScore, ss_or: fr.SetScore, eras: tuple) -> tuple[list[str], dict]:
    lines, st = fr.set_section(ss, eras)
    exits = sum(p.exits for p in ss.pairs)
    on = sum(p.delayed for p in ss.pairs)
    out = []
    for ln in lines:
        if ln.startswith("`tsmom12` exits:"):
            ln = (f"`tsmom12` exits: {exits}; at {on} of them the 3-month return was still "
                  "positive (`or3-12` stays in; `arm3-12` leaves and waits for a dip and "
                  "recovery).")  # fmt: skip
        out.append(ln.replace("`or3-12`", "`arm3-12`"))
    net = lambda e: e.net  # noqa: E731
    d = [a - b for a, b in zip(fr.cvals(ss, net, True), fr.cvals(ss_or, net, True), strict=True)]
    k, m_, p = i1.sign_test(d)
    out += [f"`arm3-12` minus `or3-12` (description): mean cluster dN {np.mean(d):+.1f}, "
            f"higher in {k} of {m_} falls (two rules' N, same episodes).", ""]  # fmt: skip
    del p
    return out, st


def main() -> None:
    us = load_us()
    dev, reg = load_geo()
    # (a)
    head_a = [
        "## (a) Timing or exposure? insure-1's card 2 controls, US 11 series",
        "",
        "Card 1's 25% episodes and market-anchored clusters, cash at 0, each rule's paper "
        "series. Rotations: median (5th to 95th percentile) of 1,000, insure-1's seed; p = "
        "share of rotations at least as good. Description only.",
        "",
        "| | Mean cluster S (share avoided) | Mean cluster N, log pts | Pooled premium P |",
        "|---|---:|---:|---:|",
    ]
    tab_a = []
    for name, which in (("tsmom12", "ts"), ("or3-12", "orr"), (RULE, "arm")):
        tab_a += controls(name, [getattr(x, which) for x in us])
    # (b)
    ss_us = fr.score_set("US: market + 10 industries, 1927-2025 (decides)", as_pairs(us, "arm"),
                         None)  # fmt: skip
    ss_us_or = fr.score_set("", as_pairs(us, "orr"), None)
    us_mkt = ss_us.sc_ts[0].eps
    ss_dev = fr.score_set("Non-US: 13 developed indices, price (decides, direction)",
                          as_pairs(dev, "arm"), us_mkt)  # fmt: skip
    ss_dev_or = fr.score_set("", as_pairs(dev, "orr"), us_mkt)
    ss_reg = fr.score_set("French regions, total return, USD (description)",
                          as_pairs(reg, "arm"), us_mkt)  # fmt: skip
    ss_reg_or = fr.score_set("", as_pairs(reg, "orr"), us_mkt)
    t_us, st_us = section(ss_us, ss_us_or, i1.ERAS)
    t_dev, st_dev = section(ss_dev, ss_dev_or, i2.GEO_ERAS)
    t_reg, _ = section(ss_reg, ss_reg_or, i2.GEO_ERAS)
    v = verdict(st_us, st_dev)
    head = [
        "# fast-reentry-2: `or3-12` against exposure controls; `arm3-12` against `tsmom12`",
        "",
        "Card: `cards/fast-reentry-2.md`. Written by `lib/fastreentry2.py`. Log points = 100 x "
        "natural log; I, B, N are rule minus holding; differences in (b) are `arm3-12` minus "
        "`tsmom12`. Paper series (Friday decisions, 2 bps a side, cash at 0), same 25% "
        "episodes and clusters as fast-reentry.",
        "",
    ]
    head_b = [
        "## (b) `arm3-12`: exit as `tsmom12`, re-enter when the 3-month return turns positive",
        "",
        f"**Verdict by the card (family bar p < {BAR}): {v}.** US mean dN "
        f"{st_us['mean_dn']:+.1f} (sign test {st_us['k']} of {st_us['m']}, p "
        f"{st_us['p_sign']:.2g}; bootstrap p {st_us['p_boot']:.3f}); non-US mean dN "
        f"{st_dev['mean_dn']:+.1f}; premium US {st_us['p_ts']:.2f} -> {st_us['p_fr']:.2f}, "
        f"non-US {st_dev['p_ts']:.2f} -> {st_dev['p_fr']:.2f}; share avoided US "
        f"{st_us['s_ts']:.2f} -> {st_us['s_fr']:.2f} (guard: drop at most 0.10).",
        "",
    ]
    OUT.write_text("\n".join(head + head_a + tab_a + [""] + head_b + t_us + t_dev + t_reg))
    n = 0 if "--no-log" in sys.argv else log_tries(us, dev + reg)
    print(f"wrote {OUT}; {n} new tries.md rows; verdict: {v}")


if __name__ == "__main__":
    main()
