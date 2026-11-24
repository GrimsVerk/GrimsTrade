"""power-map-1: minimum detectable edges per strategy class (card: research/power-map-1.md).

    uv run --with numpy python research/powermap1.py > research/results/power-map-1.md

Reads only the committed weekly returns store (`research/register/returns/`, train only) and
numbers quoted from the records. No backtest, no price bar, no network. Deterministic (fixed
seeds). Prints markdown.
"""

from __future__ import annotations

import math
import re
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from statistics import NormalDist

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from grimstrade import returnstore as rs  # noqa: E402
from grimstrade.register import max_z  # noqa: E402

Z = NormalDist()
Z80 = Z.inv_cdf(0.80)
BAR = 4.69  # BAR.md: N = 486 effective trials
ONC = 3.29  # BAR.md: the ONC end of the measured range
SR_B = 1.05  # tsmom12 on the primary test (BAR.md, dsr-1)
LAST = date(2025, 11, 10)  # held-out year starts here; nothing after it is read
BLOCK = 52
DRAWS = 2000
SEED = 20261124
MIN_WEEKS = 104

# Class by family / variant name, fixed in the card before any number.
XS = {"cointop-1-breadth", "cointop-1-fade", "breadth-book-1", "contagion-catchup"}
EVENT = {
    "fomc-cycle",
    "halloween",
    "opex-pin",
    "tax-drain",
    "month-end-bonds",
    "auction-concession",
    "coupon-dose",
    "dealer-backlog",
    "extension-dose",
    "rebalance-pressure",
    "hedge-regime",
}
COIN_FAMILIES = {"halving", "halving-2", "fng", "attention-peak"}
CARRY = {"ts-carry"}
SKIP = {"rl-3-control", "rl-4-control"}  # planted-signal controls, never strategies
COIN_SUFFIX = re.compile(r"@(coin|BTC|ETH|BCH|BSV|ETC|LTC|coin8)\b")


def klass(idea: str, variant: str) -> str | None:
    if idea in SKIP or idea == "live":
        return None
    if idea in XS or variant == "xs_momentum":
        return "C2 cross-sectional"
    if idea in EVENT:
        return "C4 event / calendar"
    if idea in CARRY:
        return "C5 carry (ETF term/yield, not perps)"
    if idea in COIN_FAMILIES or COIN_SUFFIX.search(variant):
        return "C3 coins"
    return "C1 slow trend / allocation"


@dataclass
class Series:
    idea: str
    variant: str
    start: str
    first: int  # ordinal of the first Friday
    r: np.ndarray


def load() -> list[Series]:
    out = []
    for row in rs.read(ROOT / rs.STORE):
        first = date.fromisoformat(row.first_friday).toordinal()
        r = np.array(row.rets, dtype=float)
        n_ok = min(len(r), (LAST.toordinal() - first) // 7 + 1)
        out.append(Series(row.idea, row.variant, row.start, first, r[:n_ok]))
    return out


def align(a: Series, b: Series) -> tuple[np.ndarray, np.ndarray]:
    lo = max(a.first, b.first)
    hi = min(a.first + 7 * (len(a.r) - 1), b.first + 7 * (len(b.r) - 1))
    if hi < lo:
        return np.empty(0), np.empty(0)
    ia, ib = (lo - a.first) // 7, (lo - b.first) // 7
    n = (hi - lo) // 7 + 1
    x, y = a.r[ia : ia + n], b.r[ib : ib + n]
    ok = np.isfinite(x) & np.isfinite(y)
    return x[ok], y[ok]


def sharpe(x: np.ndarray) -> float:
    sd = x.std(ddof=1)
    return float(x.mean() / sd * math.sqrt(52)) if sd > 0 else float("nan")


def jk_se(sa: float, sb: float, rho: float, years: float, q: float = 52) -> float:
    """Jobson-Korkie / Memmel SE of an annual Sharpe difference."""
    return math.sqrt((2 - 2 * rho + (sa**2 + sb**2 - 2 * rho**2 * sa * sb) / (2 * q)) / years)


def boot_se(x: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> float:
    """Circular block bootstrap (52-week blocks) SE of the annual Sharpe difference."""
    n = len(x)
    nb = -(-n // BLOCK)
    starts = rng.integers(0, n, size=(DRAWS, nb))
    idx = (starts[:, :, None] + np.arange(BLOCK)[None, None, :]).reshape(DRAWS, -1)[:, :n] % n
    xs, ys = x[idx], y[idx]
    sx = xs.mean(1) / xs.std(1, ddof=1)
    sy = ys.mean(1) / ys.std(1, ddof=1)
    return float(np.nanstd((sx - sy) * math.sqrt(52), ddof=1))


def comparator(s: Series, by_key: dict[tuple[str, str], Series], primary: Series) -> Series:
    if "@" in s.variant:
        suffix = s.variant.split("@", 1)[1]
        for idea, name in (
            ("baselines", f"tsmom12@{suffix}"),
            (s.idea, f"tsmom12@{suffix}"),
            (s.idea, f"TS@{suffix}"),
        ):
            if (idea, name) in by_key:
                return by_key[(idea, name)]
    return primary


def fmt(v: float, d: int = 2, sign: bool = False) -> str:
    if not math.isfinite(v):
        return "-"
    return f"{v:+.{d}f}" if sign else f"{v:.{d}f}"


def q(vals: list[float], p: float) -> float:
    v = sorted(x for x in vals if math.isfinite(x))
    if not v:
        return float("nan")
    k = (len(v) - 1) * p
    lo = math.floor(k)
    return v[lo] + (v[min(lo + 1, len(v) - 1)] - v[lo]) * (k - lo)


# --- M5: measured inputs ---


def measure(series: list[Series]) -> tuple[Series, dict[str, list[dict[str, float]]], list[str]]:
    by_key: dict[tuple[str, str], Series] = {}
    for s in series:
        by_key.setdefault((s.idea, s.variant), s)
    primary = by_key[("baselines", "tsmom12")]
    rng = np.random.default_rng(SEED)
    per: dict[str, list[dict[str, float]]] = defaultdict(list)
    lines = []
    lines_top: list[tuple[str, float, str, float, float, float]] = []
    for s in series:
        c = klass(s.idea, s.variant)
        if c is None:
            continue
        b = comparator(s, by_key, primary)
        if b is s or (b.idea, b.variant) == (s.idea, s.variant):
            continue
        x, y = align(s, b)
        if len(x) < MIN_WEEKS or x.std() == 0 or y.std() == 0:
            continue
        rho = float(np.corrcoef(x, y)[0, 1])
        if rho > 0.999:  # the comparator itself under another name
            continue
        yrs = len(x) / 52.18
        sa, sb = sharpe(x), sharpe(y)
        f = jk_se(sa, sb, rho, yrs)
        bse = boot_se(x, y, rng)
        per[c].append({"rho": rho, "years": yrs, "d": sa - sb, "se": bse, "k": bse / f})
        lines_top.append((c, sa - sb, f"{s.idea}/{s.variant} vs {b.variant}", rho, yrs, bse))
    lines.append(f"Comparator for the primary test: `baselines/tsmom12` from {primary.start}, ")
    lines.append(f"{len(primary.r)} weeks, weekly Sharpe {sharpe(primary.r):.3f}.")
    lines += [
        "",
        "Largest d per class (descriptive: logged tries against their own universe's `tsmom12`,"
        " z = d / bootstrap SE; not candidates):",
        "",
        "| Class | Series vs comparator | rho | Years | d | z |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for c in sorted(per):
        top = sorted((t for t in lines_top if t[0] == c), key=lambda t: -t[1])[:3]
        for _, d, name, rho, yrs, bse in top:
            lines.append(f"| {c} | {name} | {rho:.2f} | {yrs:.1f} | {d:+.2f} | {d / bse:.1f} |")
    return primary, per, lines


def table_classes(per: dict[str, list[dict[str, float]]]) -> list[str]:
    out = [
        "| Class (store) | Series | rho with its `tsmom12`: p25 / median / p75 | Years, median "
        "| d over `tsmom12`, median / max | Bootstrap SE of d, median | k = bootstrap / formula, "
        "median (p25-p75) |",
        "|---|---:|---|---:|---|---:|---|",
    ]
    for c in sorted(per):
        v = per[c]
        rho = [x["rho"] for x in v]
        out.append(
            f"| {c} | {len(v)} | {fmt(q(rho, 0.25))} / {fmt(q(rho, 0.5))} / {fmt(q(rho, 0.75))} "
            f"| {fmt(q([x['years'] for x in v], 0.5), 1)} "
            f"| {fmt(q([x['d'] for x in v], 0.5), 2, True)} / "
            f"{fmt(max(x['d'] for x in v), 2, True)} "
            f"| {fmt(q([x['se'] for x in v], 0.5), 3)} "
            f"| {fmt(q([x['k'] for x in v], 0.5))} "
            f"({fmt(q([x['k'] for x in v], 0.25))}-{fmt(q([x['k'] for x in v], 0.75))}) |"
        )
    allk = [x["k"] for v in per.values() for x in v]
    out.append("")
    out.append(f"All classes: k median {fmt(q(allk, 0.5))}, p75 {fmt(q(allk, 0.75))}.")
    return out


def markets(series: list[Series]) -> tuple[list[str], float]:
    """Cross-market correlation of (rule - tsmom12) difference series, same rule on each market."""
    mk = ["FTSE", "GDAXI", "GSPC", "N225"]
    by = defaultdict(dict)
    for s in series:
        if "@" in s.variant:
            base, suf = s.variant.split("@", 1)
            if suf in mk:
                by[(s.idea, base)][suf] = s
    tsm = {m: by[("baselines", "tsmom12")][m] for m in mk}
    corrs, tcorr = [], []
    used = []
    for (idea, base), d in sorted(by.items()):
        if (idea, base) == ("baselines", "tsmom12") or len(d) < 4:
            continue
        diffs = {}
        for m in mk:
            x, y = align(d[m], tsm[m])
            if len(x) < MIN_WEEKS:
                break
            diffs[m] = Series("d", m, "", max(d[m].first, tsm[m].first), x - y)
        if len(diffs) < 4:
            continue
        used.append(f"{idea}/{base}")
        for i, a in enumerate(mk):
            for b in mk[i + 1 :]:
                x, y = align(diffs[a], diffs[b])
                if len(x) >= MIN_WEEKS and x.std() > 0 and y.std() > 0:
                    corrs.append(float(np.corrcoef(x, y)[0, 1]))
    for i, a in enumerate(mk):
        for b in mk[i + 1 :]:
            x, y = align(tsm[a], tsm[b])
            tcorr.append(float(np.corrcoef(x, y)[0, 1]))
    rho_d = statistics.mean(corrs) if corrs else float("nan")
    lines = [
        f"Rules with a `@FTSE/@GDAXI/@GSPC/@N225` set: {len(used)} ({', '.join(used[:8])}"
        f"{', ...' if len(used) > 8 else ''}).",
        f"Average cross-market correlation of the weekly difference series (rule minus that "
        f"market's `tsmom12`): **{rho_d:.2f}** ({len(corrs)} pairs; median "
        f"{statistics.median(corrs):.2f}). Of the markets' `tsmom12` returns themselves: "
        f"{statistics.mean(tcorr):.2f}.",
    ]
    return lines, rho_d


# --- M1-M4: arithmetic ---


def mde(z: float, se: float, power: float = 0.80) -> float:
    return (z + Z.inv_cdf(power)) * se


def ir_to_mix(ir: float) -> float:
    return math.sqrt(SR_B**2 + ir**2) - SR_B


def chance(edge: float, se: float, z: float) -> float:
    """Probability a true edge `edge` (SE se) clears z."""
    return 1 - Z.cdf(z - edge / se)


@dataclass
class Cls:
    name: str
    data: str
    years: float
    rho: float
    plaus_d: tuple[float, float]  # plausible true edge over tsmom12 (difference form)
    plaus_ir: tuple[float, float]  # plausible residual IR (alpha form)
    source: str


def class_table(classes: list[Cls], k: float) -> list[str]:
    out = [
        "| Class | Data | Y_eff (years) | rho | SE of d | Edge at z 4.69: 50% / 80% power "
        "| at z 3.29, 80% | Alpha form: IR needed 80% (adds to best mix) "
        "| Plausible true size (record) | Chance to pass at z 4.69 |",
        "|---|---|---:|---:|---:|---|---:|---|---|---:|",
    ]
    for c in classes:
        se = k * math.sqrt(2 * (1 - c.rho) / c.years)
        ir80 = (BAR + Z80) * k / math.sqrt(c.years)
        p_hi_d = chance(c.plaus_d[1], se, BAR)
        p_hi_ir = 1 - Z.cdf(BAR - c.plaus_ir[1] * math.sqrt(c.years) / k)
        out.append(
            f"| {c.name} | {c.data} | {c.years:.0f} | {c.rho:.2f} | {se:.3f} "
            f"| +{BAR * se:.2f} / +{mde(BAR, se):.2f} | +{mde(ONC, se):.2f} "
            f"| {ir80:.2f} (+{ir_to_mix(ir80):.2f}) "
            f"| d {c.plaus_d[0]:+.2f}..{c.plaus_d[1]:+.2f}; IR {c.plaus_ir[0]:.2f}-"
            f"{c.plaus_ir[1]:.2f} ({c.source}) "
            f"| d: {p_hi_d:.1e}; alpha: {p_hi_ir:.1e} |"
        )
    return out


def event_table(k: float) -> list[str]:
    rows = [
        ("FOMC days 1994-2025 (8 a year)", 8 * 31.8, 31.8),
        ("monthly calendar effect 1994-2025", 12 * 31.8, 31.8),
        ("monthly calendar effect 1927-2025", 12 * 98, 98),
        ("weekly dose, effectively 1 independent week in 4", 52 * 31.8 / 4, 31.8),
        ("sparse episodes (gate-power W26-like)", 20, 25),
        ("seasonal, one per winter (weather-1-like)", 18, 18),
        ("BTC daily bets 2014-2025 (one a day)", 365 * 11.2, 11.2),
        ("BTC hourly bets 2017-2025 (Binance 1-minute, one an hour)", 24 * 365 * 8.2, 8.2),
    ]
    out = [
        "| Bets | Independent bets E | Per-bet Sharpe needed, z 4.69 at 80% | Same at z 3.29 "
        "| Annual IR that is (any E) |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, e, y in rows:
        s = (BAR + Z80) * k / math.sqrt(e)
        out.append(
            f"| {name} | {e:,.0f} | {s:.3f} | {(ONC + Z80) * k / math.sqrt(e):.3f} "
            f"| {s * math.sqrt(e / y):.2f} |"
        )
    return out


def btc_bps(series: list[Series], k: float) -> list[str]:
    by = {(s.idea, s.variant): s for s in series}
    r = by[("baselines", "bh-btc")].r
    r = r[r != 0]
    wsd = float(r.std(ddof=1))
    dsd, hsd = wsd / math.sqrt(7), wsd / math.sqrt(7 * 24)
    out = [
        f"BTC weekly return SD from the store's `bh-btc` (non-zero weeks, {len(r)} weeks): "
        f"{wsd * 100:.1f}%; random-walk scaling gives a daily SD of {dsd * 100:.2f}% and an hourly "
        f"SD of {hsd * 100:.2f}%.",
        "",
        "| Bets | E | Per-bet Sharpe needed (z 4.69, 80%) | Mean net edge per bet | "
        "Cost of one round trip at 10 / 30 bps, as a share of that edge |",
        "|---|---:|---:|---:|---|",
    ]
    for name, e, sd in (
        ("daily, 2014-2025", 365 * 11.2, dsd),
        ("hourly, 2017-2025", 24 * 365 * 8.2, hsd),
    ):
        s = (BAR + Z80) * k / math.sqrt(e)
        edge = s * sd * 1e4
        out.append(
            f"| {name} | {e:,.0f} | {s:.3f} | {edge:.1f} bps | "
            f"{10 / edge:.1f}x / {30 / edge:.1f}x (net edge must be this on top of costs) |"
        )
    return out


def forward_tables(series: list[Series], primary: Series, k: float) -> tuple[list[str], list[str]]:
    zs = [
        ("one book registered first, z 1.645", 1.645),
        ("best of the 11 live books, z %.2f" % (1.645 + max_z(11)), 1.645 + max_z(11)),
        ("the bar, z 4.69", BAR),
    ]
    out = [
        "Years of forward record for 80% power, edge d over `tsmom12` (difference form):",
        "",
        "| rho with `tsmom12` | z | d +0.05 | +0.10 | +0.20 | +0.30 | +0.50 |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for rho in (0.95, 0.77, 0.0):
        for zn, z in zs:
            cells = [
                ((z + Z80) * k * math.sqrt(2 * (1 - rho)) / d) ** 2
                for d in (0.05, 0.10, 0.20, 0.30, 0.50)
            ]
            out.append(f"| {rho:.2f} | {zn} | " + " | ".join(f"{c:,.0f}" for c in cells) + " |")
    out += [
        "",
        "Against zero (a book's own Sharpe S, alpha form uses the same row with IR for S):",
        "",
        "| z | S 0.25 | 0.50 | 0.75 | 1.00 | 1.50 | 2.00 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for zn, z in zs:
        cells = [((z + Z80) * k / s) ** 2 for s in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0)]
        out.append(f"| {zn} | " + " | ".join(f"{c:,.1f}" for c in cells) + " |")
    live = [
        "| Live book | rho with `tsmom12` (1994-2025 backtest) | Backtest d (weekly Sharpe) "
        "| Forward years for 80% at z 1.645 if that d were true | at z 4.69 |",
        "|---|---:|---:|---:|---:|",
    ]
    for s in series:
        if s.idea != "live":
            continue
        x, y = align(s, primary)
        rho = float(np.corrcoef(x, y)[0, 1])
        d = sharpe(x) - sharpe(y)
        se1 = k * math.sqrt(2 * (1 - rho))
        if d > 0:
            y1 = f"{((1.645 + Z80) * se1 / d) ** 2:,.0f}"
            y2 = f"{((BAR + Z80) * se1 / d) ** 2:,.0f}"
        else:
            y1 = y2 = "never (d <= 0)"
        live.append(f"| `{s.variant}` | {rho:.2f} | {d:+.2f} | {y1} | {y2} |")
    return out, live


# --- M6: simulation ---


def simulate() -> list[str]:
    rng = np.random.default_rng(SEED + 1)
    out = [
        "Draws per cell: 1,000 (400 at 98 years; the card said 2,000).",
        "",
        "| rho | Years | Formula SE at the true Sharpes | Monte Carlo SD of d (t(4)) | Ratio "
        "| Detection at the formula's MDE80, z 4.69 |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    nu = 4.0
    for rho in (0.0, 0.5, 0.77, 0.93):
        for yrs in (6, 11, 32, 98):
            n = int(round(yrs * 52))
            se = jk_se(SR_B, SR_B, rho, yrs)
            d_true = mde(BAR, se)
            se_true = jk_se(SR_B + d_true, SR_B, rho, yrs)
            ds, hits = [], 0
            for _ in range(1000 if yrs < 98 else 400):
                e = rng.standard_t(nu, size=(2, n)) / math.sqrt(nu / (nu - 2))
                a = e[0]
                b = rho * e[0] + math.sqrt(1 - rho**2) * e[1]
                sa_w, sb_w = (SR_B + d_true) / math.sqrt(52), SR_B / math.sqrt(52)
                d_sim = sharpe(a + sa_w) - sharpe(b + sb_w)
                ds.append(d_sim - d_true)
                hits += d_sim / se >= BAR
            mc = float(np.std(ds, ddof=1))
            out.append(
                f"| {rho:.2f} | {yrs} | {se_true:.3f} | {mc:.3f} | {mc / se_true:.2f} "
                f"| {hits / len(ds):.0%} |"
            )
    # frequency check: same 32 years, daily / weekly / monthly sampling of one random walk
    yrs, per_year = 32, 252
    sds = defaultdict(list)
    for _ in range(2000):
        x = rng.standard_normal(yrs * per_year) * 0.01 + 0.01 / math.sqrt(per_year)
        for name, step in (("daily", 1), ("weekly", 5), ("monthly", 21)):
            agg = x[: len(x) // step * step].reshape(-1, step).sum(1)
            sds[name].append(agg.mean() / agg.std(ddof=1) * math.sqrt(per_year / step))
    out += [
        "",
        "Frequency check (32 years, true annual Sharpe 1.0, normal, 2,000 draws): SD of the "
        "estimated annual Sharpe "
        + ", ".join(f"{n} {np.std(v, ddof=1):.3f}" for n, v in sds.items())
        + "; formula sqrt((1 + SR^2 / (2 q)) / Y): "
        + ", ".join(
            f"{n} {math.sqrt((1 + 1 / (2 * per_year / st)) / yrs):.3f}"
            for n, st in (("daily", 1), ("weekly", 5), ("monthly", 21))
        )
        + ".",
    ]
    return out


def main() -> None:
    series = load()
    primary, per, head = measure(series)
    allk = [x["k"] for v in per.values() for x in v]
    k = max(1.0, q(allk, 0.5))
    mlines, rho_d = markets(series)
    m = 13
    y13 = 59.8 * m / (1 + (m - 1) * rho_d)
    c1 = per["C1 slow trend / allocation"]
    rho_c1 = q([x["rho"] for x in c1], 0.5)
    rho_c2 = q([x["rho"] for x in per["C2 cross-sectional"]], 0.5)
    rho_c3 = q([x["rho"] for x in per["C3 coins"]], 0.5)
    rho_c4 = q([x["rho"] for x in per["C4 event / calendar"]], 0.5)
    classes = [
        Cls(
            "C1 trend, six assets",
            "daily 1994-2025",
            31.8,
            rho_c1,
            (0.0, 0.10),
            (0.05, 0.15),
            "project max +0.23; spread SD 0.12; live trend 0.17",
        ),
        Cls(
            "C1 trend, US 1927-2025",
            "S&P / Ken French weekly",
            98,
            rho_c1,
            (0.0, 0.10),
            (0.05, 0.15),
            "same rules, more years",
        ),
        Cls(
            "C1 trend, 13 markets pooled",
            f"1966-2025, Y_eff = 59.8 x {m} / (1 + 12 x {rho_d:.2f})",
            y13,
            rho_c1,
            (0.0, 0.10),
            (0.05, 0.15),
            "insure-2 markets",
        ),
        Cls(
            "C2 cross-sectional, 34 ETFs / coins",
            "about 2007-2025",
            18,
            rho_c2,
            (0.0, 0.10),
            (0.0, 0.30),
            "survey-6: momentum live IR -0.03, style premia 0.50 long-short",
        ),
        Cls(
            "C2 cross-sectional, Ken French 1927-",
            "monthly portfolios, research only",
            98,
            rho_c2,
            (0.0, 0.10),
            (0.0, 0.30),
            "UMD 0.80 paper, 0.26 after publication",
        ),
        Cls(
            "C3 crypto daily / intraday",
            "BTC daily 2014-2025",
            11.2,
            rho_c3,
            (0.0, 0.30),
            (0.0, 1.0),
            "unknown live; rl-6, cointop-1 found none",
        ),
        Cls(
            "C3 crypto 1-minute",
            "Binance 2017-08..2025-11",
            8.2,
            0.1,
            (0.0, 0.30),
            (0.0, 1.5),
            "unknown; costs decide",
        ),
        Cls(
            "C4 event study",
            "events 1994-2025",
            31.8,
            rho_c4,
            (0.0, 0.05),
            (0.05, 0.15),
            "gate-power yardstick; 0 of 19 gates",
        ),
        Cls(
            "C5 perp carry (blocked B6/B7)",
            "funding 2019-09..2025-11",
            6.2,
            0.2,
            (0.0, 0.5),
            (0.0, 1.5),
            "carry-3 train 10.8%/yr, held-out -0.65",
        ),
    ]
    print("# power-map-1 results (generated by `research/powermap1.py`; do not edit)\n")
    print("## M5. Measured from the committed store\n")
    print("\n".join(head) + "\n")
    print("\n".join(table_classes(per)) + "\n")
    print(f"k used below: {k:.2f} (the median over all classes, floored at 1).\n")
    print("### 13 markets\n")
    print("\n".join(mlines))
    print(f"Pooled effective years for 13 markets x 59.8 years: **{y13:.0f}**.\n")
    print("## M1/M2. Edge needed per class\n")
    print(
        "rho per class: the store's median for the class (C1, C2, C3, C4), assumed 0.1 for "
        "1-minute crypto and 0.2 for perp carry (no series in the store). 'Chance to pass' is "
        "the probability a true edge at the top of the plausible range clears z 4.69 (d "
        "form, then alpha form).\n"
    )
    print("\n".join(class_table(classes, k)) + "\n")
    print("## M3. Events and many bets\n")
    print("\n".join(event_table(k)) + "\n")
    print("\n".join(btc_bps(series, k)) + "\n")
    print("## M4. Forward paper scoring\n")
    fwd, live = forward_tables(series, primary, k)
    print("\n".join(fwd) + "\n")
    print("\n".join(live) + "\n")
    print("## M6. Simulation checks\n")
    print("\n".join(simulate()))


if __name__ == "__main__":
    main()
