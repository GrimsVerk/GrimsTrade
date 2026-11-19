"""risk-menu: the risk dials side by side on one footing (descriptive, no pick).
Card: research/cards/risk-menu.md.

    uv run --with openpyxl python -I research/lib/riskmenu_run.py <cache_root>

Reuses `lstrend2_run.py` Part A (the wide book at gross 1, the `tsmom12` sleeve, the equal-risk
blend) and vol-timing's own-volatility share. Appends the card's 7 replication rows to
`tries.md` (first run only), writes `research/results/risk-menu.md` and `research/risk-menu.svg`.
No day after 2025-10-31 is read.
"""

from __future__ import annotations

import bisect
import json
import math
import sys
from collections.abc import Callable
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cash_interest as ci  # noqa: E402
import common as c  # noqa: E402
import harness  # noqa: E402
import lstrend1_run as l1  # noqa: E402
import lstrend2_run as l2  # noqa: E402
import numpy as np  # noqa: E402
import stats  # noqa: E402
import survey5_live as s5  # noqa: E402

from grimstrade import gym  # noqa: E402

IDEA = "risk-menu"
P, LD, LAST_DAY = l2.P, l2.LD, l2.LAST_DAY
YRS = ((P[1] - P[0]).days + 1) / 365.25
DRAWS = 2_000
RESET_COST = l1.COST
CRASH = {
    "2008": (date(2008, 1, 1), date(2008, 12, 31)),
    "2020 Q1": (date(2020, 1, 1), date(2020, 3, 31)),
    "2022": (date(2022, 1, 1), date(2022, 12, 31)),
}


class Item:
    def __init__(self, key: str, name: str, group: str, ex: dict[date, float]) -> None:
        self.key, self.name, self.group, self.ex = key, name, group, ex
        self.expo: dict[date, float] = {}
        self.orders = math.nan
        self.orders_exact = False
        self.turnover = math.nan
        self.share1 = math.nan  # mean `tsmom12` share in P (mixes)


def months_in(a: date, b: date) -> list[date]:
    out, d = [], date(a.year, a.month, 1)
    while d <= b:
        if d >= a:
            out.append(d)
        d = date(d.year + d.month // 12, d.month % 12 + 1, 1)
    return out


def gym_fills(run: harness.Run, hist: dict) -> int:
    res = gym.simulate(run.decisions, hist)
    return sum(1 for f in res.fills if P[0] <= f.time.date() <= P[1])


def held_count(run: harness.Run) -> Callable[[date], int]:
    days = [x.time.date() for x in run.decisions]
    n = [sum(1 for w in x.weights.values() if w > 0) for x in run.decisions]

    def f(d: date) -> int:
        i = bisect.bisect_right(days, d) - 1
        return n[i] if i >= 0 else 0

    return f


class Mix:
    def __init__(self) -> None:
        self.ex: dict[date, float] = {}
        self.share1: dict[date, float] = {}
        self.expo: dict[date, float] = {}
        self.reset_traded = 0.0  # in P
        self.reset_orders = 0  # in P


def mix(
    s1: l2.Sleeve,
    s2: l2.Sleeve | None,
    target: Callable[[date, float], tuple[float, float]],
    start: date,
    held: Callable[[date], int],
) -> Mix:
    """`tsmom12` share v1, second sleeve v2, bills the rest; reset to target(d, v1) on each 1st,
    5 bps on the traded notional (at the sleeves' gross), drift in between."""
    out = Mix()
    v1 = v2 = 0.0
    for d in l2.cal_days(start, LAST_DAY):
        cost = 0.0
        g1 = s1.gross(d)
        g2 = s2.gross(d) if s2 is not None else 0.0
        if d.day == 1:
            a1, a2 = target(d, v1)
            t1, t2 = abs(a1 - v1), abs(a2 - v2)
            cost = RESET_COST * (t1 * g1 + t2 * g2)
            if P[0] <= d <= P[1]:
                out.reset_traded += t1 * g1 + t2 * g2
                if t1 >= 0.01:
                    out.reset_orders += held(d)
            v1, v2 = a1, a2
        x1 = s1.ex.get(d, 0.0)
        x2 = s2.ex.get(d, 0.0) if s2 is not None else 0.0
        out.share1[d] = v1
        out.expo[d] = v1 * g1 + v2 * g2
        out.ex[d] = v1 * x1 + v2 * x2 - cost
        n1, n2, nb = v1 * (1 + x1), v2 * (1 + x2), 1 - v1 - v2
        tot = n1 + n2 + nb
        v1, v2 = n1 / tot, n2 / tot
    return out


def vt_target(s1: l2.Sleeve, start: date, mean_share: float, held: Callable[[date], int]) -> Mix:
    sig = {d: s1.sigma(d - timedelta(days=1)) for d in months_in(start, LAST_DAY)}

    def build(k: float) -> Mix:
        def tgt(d: date, v: float) -> tuple[float, float]:
            sg = sig[d]
            return (min(1.0, k / sg), 0.0) if sg > 0 and math.isfinite(sg) else (v, 0.0)

        return mix(s1, None, tgt, start, held)

    lo, hi = 0.0, 2.0
    for _ in range(50):
        k = (lo + hi) / 2
        m = float(np.mean([v for d, v in build(k).share1.items() if P[0] <= d <= P[1]]))
        lo, hi = (k, hi) if m < mean_share else (lo, k)
    return build((lo + hi) / 2)


def gym_item(key: str, name: str, f: c.ResearchStrategy, six: c.Ctx) -> Item:
    run = c.go(IDEA, key, f, six, "baseline", log=False)  # re-score of a logged baseline
    days, ylds = ci.bill_yield()
    r, rf = ci.rescored(run, days, ylds)
    dd = run.days[1:]
    it = Item(key, name, "hold", {d: float(x - y) for d, x, y in zip(dd, r, rf, strict=True)})
    ddays = [x.time.date() for x in run.decisions]
    ex_ = [sum(x.weights.values()) for x in run.decisions]
    for d in l2.cal_days(*P):
        i = bisect.bisect_right(ddays, d) - 1
        it.expo[d] = ex_[i] if i >= 0 else 0.0
    it.orders, it.orders_exact = gym_fills(run, six.hist) / YRS, True
    it.turnover = run.score.turnover
    return it


def underwater_years(eq: np.ndarray) -> float:
    peak = np.maximum.accumulate(eq)
    best = cur = 0
    for e, p in zip(eq, peak, strict=True):
        cur = cur + 1 if e < p * (1 - 1e-12) else 0
        best = max(best, cur)
    return best / 365.25


def worst_12m(eq: np.ndarray) -> float:
    return float((eq[365:] / eq[:-365]).min() - 1)


def svg_map(items: list[Item], m: dict[str, dict[str, float]]) -> str:
    W, H, L, R, T, B = 720, 500, 70, 80, 50, 60
    xs = [m[i.key]["mdd"] * 100 for i in items]
    ys = [m[i.key]["cagr"] * 100 for i in items]
    x1 = 5 * math.ceil(max(xs) / 5 + 0.2)
    y0, y1 = 4 * math.floor(min(ys) / 4 - 0.1), 4 * math.ceil(max(ys) / 4 + 0.1)
    y0 = min(y0, 0)
    px = lambda x: L + (W - L - R) * x / x1  # noqa: E731
    py = lambda y: T + (H - T - B) * (1 - (y - y0) / (y1 - y0))  # noqa: E731
    col = {"hold": "#c2410c", "size": "#1d4ed8", "vt": "#047857", "blend": "#7c3aed"}
    lab = {
        "hold": "plain holding",
        "size": "tsmom12 + T-bills, fixed share",
        "vt": "tsmom12 + T-bills, own-vol target",
        "blend": "tsmom12 + wide long-short book",
    }
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
        f'height="{H}" font-family="sans-serif" font-size="12">',
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
        f'<text x="{L}" y="24" font-size="15" font-weight="bold" fill="#111">Risk menu: '
        "growth a year against worst loss, 2007-04 to 2025-10</text>",
        f'<text x="{L}" y="40" fill="#555">Total return, T-bill interest on cash, costs '
        "included. One history: no point is a proven edge.</text>",
    ]
    for gx in range(0, int(x1) + 1, 5):
        o.append(f'<line x1="{px(gx):.1f}" y1="{T}" x2="{px(gx):.1f}" y2="{H - B}" '
                 'stroke="#e5e7eb"/>')  # fmt: skip
        o.append(f'<text x="{px(gx):.1f}" y="{H - B + 16}" text-anchor="middle" '
                 f'fill="#444">{gx}%</text>')  # fmt: skip
    for gy in range(int(y0), int(y1) + 1, 4):
        o.append(f'<line x1="{L}" y1="{py(gy):.1f}" x2="{W - R}" y2="{py(gy):.1f}" '
                 'stroke="#e5e7eb"/>')  # fmt: skip
        o.append(f'<text x="{L - 8}" y="{py(gy) + 4:.1f}" text-anchor="end" '
                 f'fill="#444">{gy}%</text>')  # fmt: skip
    o.append(f'<text x="{(L + W - R) / 2:.0f}" y="{H - 18}" text-anchor="middle" fill="#111">'
             "Worst loss (largest fall from a high)</text>")  # fmt: skip
    o.append(f'<text x="18" y="{(T + H - B) / 2:.0f}" text-anchor="middle" fill="#111" '
             f'transform="rotate(-90 18 {(T + H - B) / 2:.0f})">Growth a year</text>')  # fmt: skip
    placed: list[tuple[float, float]] = []
    for it, x, y in sorted(zip(items, xs, ys, strict=True), key=lambda t: -t[2]):
        cx, cy = px(x), py(y)
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" fill="{col[it.group]}" '
                 'stroke="#fff" stroke-width="1"/>')  # fmt: skip
        ly = cy + 4
        while any(abs(ly - q) < 13 and abs(cx - p) < 150 for p, q in placed):
            ly += 13
        placed.append((cx, ly))
        o.append(f'<text x="{cx + 9:.1f}" y="{ly:.1f}" fill="#111">{it.key}</text>')
    o.append(f'<rect x="{W - R - 165}" y="{H - B - 105}" width="200" height="92" fill="#fff" '
             'stroke="#d1d5db"/>')  # fmt: skip
    for k, g in enumerate(col):
        yy = H - B - 90 + 20 * k
        o.append(f'<circle cx="{W - R - 150}" cy="{yy}" r="5.5" fill="{col[g]}"/>')
        o.append(f'<text x="{W - R - 140}" y="{yy + 4}" fill="#111" font-size="11">'
                 f"{lab[g]}</text>")  # fmt: skip
    o.append("</svg>")
    return "\n".join(o) + "\n"


def tries_row(variant: str, r: np.ndarray, turnover: float) -> str:
    return (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | replication | train | "
        f"{P[0]} | {P[1]} | {stats.sharpe(r):.2f} | {np.prod(1 + r) - 1:+.1%} | {l2.mdd(r):.1%} | "
        f"{turnover:.2f} |\n"
    )


def main(root: Path) -> None:
    rf_day = s5.bill_daily()
    g1 = l2.Book("wide-LS-g1", l1.WIDE, gross1=True)
    l2.run_books(l2.wide_prices(root), rf_day, [g1])
    w = l2.wide_sleeve(g1)
    s1, rf1, _drag, run = l2.tsmom12_sleeve()
    six = c.ctx("six")
    held = held_count(run)
    ts_orders = gym_fills(run, six.hist) / YRS
    ts_turn = run.score.turnover
    bl = l2.blend(s1, w, l1.COST)
    start = bl.start
    # wide book: positions held at each month start in P (one order each, monthly), traded / yr
    wi = {d: i for i, d in enumerate(g1.days)}
    wide_pos = []
    for m0 in months_in(*P):
        d = m0
        while d not in wi:
            d += timedelta(days=1)
        wide_pos.append(sum(1 for t in g1.assets if g1.sign[t][wi[d]] != 0))
    wide_orders = float(np.mean(wide_pos)) * 12
    wide_turn = sum(x for d, x in zip(g1.days, g1.traded_d, strict=True) if P[0] <= d <= P[1]) / YRS

    items: list[Item] = [
        gym_item("hold six", "Hold the six (equal weight)", c.weekly(c.equal_weight), six),
        gym_item("60/40", "60/40 (SPY / TLT)", c.weekly(c.sixty_forty), six),
    ]
    it = Item("tsmom12", "`tsmom12`, full size", "size", s1.ex)
    it.expo = {d: s1.gross(d) for d in l2.cal_days(*P)}
    it.orders, it.orders_exact, it.turnover, it.share1 = ts_orders, True, ts_turn, 1.0
    items.append(it)

    def from_mix(key: str, name: str, group: str, mx: Mix, wide: bool) -> Item:
        x = Item(key, name, group, mx.ex)
        x.expo = {d: mx.expo[d] for d in l2.cal_days(*P)}
        x.share1 = float(np.mean([mx.share1[d] for d in l2.cal_days(*P)]))
        x.orders = ts_orders + mx.reset_orders / YRS + (wide_orders if wide else 0.0)
        x.turnover = x.share1 * ts_turn + mx.reset_traded / YRS
        if wide:
            x.turnover += (1 - x.share1) * wide_turn
        return x

    for sh in (0.70, 0.26):
        mx = mix(s1, None, lambda d, v, sh=sh: (sh, 0.0), start, held)
        items.append(from_mix(f"tsmom12 {sh:.0%}", f"`tsmom12` {sh:.0%} + T-bills", "size", mx,
                              False))  # fmt: skip
    for sh in (0.26, 0.70):
        mx = vt_target(s1, start, sh, held)
        items.append(from_mix(f"vt-own {sh:.0%}", f"Own-vol target, mean share {sh:.0%}", "vt",
                              mx, False))  # fmt: skip
    it = Item("equal-risk blend", "Equal-risk blend with wide-LS (ls-trend-2)", "blend", bl.ex)
    it.expo = {d: bl.gross[d] for d in l2.cal_days(*P)}
    it.share1 = float(np.mean([bl.a[d] for d in l2.cal_days(*P)]))
    rto = sum(v for d, v in bl.reset_traded.items() if P[0] <= d <= P[1]) / YRS
    it.turnover = it.share1 * ts_turn + (1 - it.share1) * wide_turn + rto
    it.orders = ts_orders + wide_orders + 12 * float(np.mean([held(d) for d in months_in(*P)]))
    items.append(it)
    for a in (0.90, 0.70, 0.50):
        mx = mix(s1, w, lambda d, v, a=a: (a, 1 - a), start, held)
        nm = f"`tsmom12` {a:.0%} / wide-LS {1 - a:.0%}"
        items.append(from_mix(f"split {a:.0%}/{1 - a:.0%}", nm, "blend", mx, True))

    # measures
    rf_p = l2.on_cal(rf1, *P)
    ex = {i.key: l2.on_cal(i.ex, *P) for i in items}
    m: dict[str, dict[str, float]] = {}
    for i in items:
        e = ex[i.key]
        tot = e + rf_p
        eq = np.concatenate([[1.0], np.cumprod(1 + tot)])
        cr = {}
        for n, (a_, b_) in CRASH.items():
            k0, k1 = (a_ - P[0]).days, (b_ - P[0]).days
            cr[n] = float(eq[k1 + 1] / eq[k0] - 1)
        m[i.key] = {
            "sharpe": stats.sharpe(e), "se": stats.sharpe_se(e),
            "sharpe_l": stats.sharpe(l2.on_cal(i.ex, *LD)),
            "cagr": stats.cagr(tot), "vol": stats.vol(tot), "mdd": l2.mdd(tot),
            "w12": worst_12m(eq), "uw": underwater_years(eq),
            "expo": float(np.mean(list(i.expo.values()))), **cr,
        }  # fmt: skip
    best = max(items, key=lambda i: m[i.key]["sharpe"]).key
    boot = {}
    for i in items:
        boot[i.key] = {
            ref: stats.sharpe_diff_boot(ex[i.key], ex[ref], draws=DRAWS, mean_block=20, seed=0)
            for ref in ("hold six", "tsmom12", best)
            if ref != i.key
        }

    out = [
        "# risk-menu: the risk dials side by side (descriptive, no pick)",
        "",
        "Card: `cards/risk-menu.md` (committed before any number). P = 2007-04-01..2025-10-31; "
        "Sharpe on daily excess returns over the 13-week T-bill (365-day convention); every other "
        "measure on the total-return curve (bill interest on idle cash). Costs: gym costs for "
        "gym-run rules, 5 bps a side and 1% borrow in the wide book, 5 bps on each monthly share "
        "reset. Nothing after 2025-10-31 read.",
        "",
        f"Equal-risk blend reproduced: Sharpe P {m['equal-risk blend']['sharpe']:.2f} "
        "(ls-trend-2: 0.97).",
        "",
        "## 1. Return and risk",
        "",
        "| Item | Sharpe P (SE) | Sharpe L | Growth/yr | Vol | Worst loss | Worst 12 months | "
        "Longest under water | 2008 | 2020 Q1 | 2022 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for i in items:
        q = m[i.key]
        out.append(
            f"| {i.name} | {q['sharpe']:.2f} ({q['se']:.2f}) | {q['sharpe_l']:.2f} | "
            f"{q['cagr']:.1%} | {q['vol']:.1%} | {q['mdd']:.1%} | {q['w12']:+.1%} | "
            f"{q['uw']:.1f} y | {q['2008']:+.1%} | {q['2020 Q1']:+.1%} | {q['2022']:+.1%} |"
        )
    out += [
        "",
        "## 2. How it is held",
        "",
        "| Item | Mean `tsmom12` share | Average exposure (gross) | Orders a year | "
        "Turnover a year |",
        "|---|---:|---:|---:|---:|",
    ]
    for i in items:
        q = m[i.key]
        sh = "-" if math.isnan(i.share1) else f"{i.share1:.2f}"
        od = f"{i.orders:.0f}" + ("" if i.orders_exact else " (approx.)")
        out.append(f"| {i.name} | {sh} | {q['expo']:.2f} | {od} | {i.turnover:.2f} |")
    out += [
        "",
        "Orders: exact gym fills in P for gym-run rules. Mixes: `tsmom12`'s fills, plus one "
        "order per held `tsmom12` asset at each monthly reset that moves its share by at least "
        "1 point, plus for blends the wide book's held positions once a month "
        f"({wide_orders:.0f} a year). Turnover: gym-run rules over their whole run; mixes "
        "share-weighted sleeve turnover in P plus resets.",
        "",
        "## 3. Sharpe differences (paired stationary bootstrap, block 20 days, "
        f"{DRAWS:,} draws, seed 0; description, not a test)",
        "",
        f"| Item | vs hold six: d (5%..95%) | vs `tsmom12`: d (5%..95%) | vs best ({best}): "
        "d (5%..95%) |",
        "|---|---:|---:|---:|",
    ]
    for i in items:

        def cell(ref: str, i: Item = i) -> str:
            b = boot[i.key].get(ref)
            return "-" if b is None else f"{b[0]:+.2f} ({b[2]:+.2f}..{b[3]:+.2f})"

        out.append(f"| {i.name} | {cell('hold six')} | {cell('tsmom12')} | {cell(best)} |")
    path = harness.RESEARCH / "results" / "risk-menu.md"
    path.write_text("\n".join(out).rstrip() + "\n")
    (harness.RESEARCH / "risk-menu.svg").write_text(svg_map(items, m))
    dump = {
        i.key: {
            **m[i.key],
            "orders": i.orders,
            "turnover": i.turnover,
            "share1": i.share1,
            "boot": {k: list(v) for k, v in boot[i.key].items()},
        }
        for i in items
    }
    (harness.RESEARCH / "results" / "risk-menu.json").write_text(json.dumps(dump, indent=1) + "\n")
    new = ["tsmom12 70%", "tsmom12 26%", "vt-own 26%", "vt-own 70%", "split 90%/10%",
           "split 70%/30%", "split 50%/50%"]  # fmt: skip
    tag = {k: k.replace(" ", "-").replace("%", "").replace("/", "-") + "@L07" for k in new}
    if f"| {IDEA} | {tag[new[0]]} |" not in harness.TRIES.read_text():
        by = {i.key: i for i in items}
        with harness.TRIES.open("a") as f:
            f.writelines(tries_row(tag[k], ex[k], by[k].turnover) for k in new)
        print("logged 7 rows")
    print("\n".join(out))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
