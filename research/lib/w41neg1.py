"""Lane w41-neg-1: kill-only gate `cabinet-drift` (provisional W41n), card
research/cards/w41-neg-1.md (pushed before this script's first run).

    uv run python -I research/lib/w41neg1.py        (DRY=1: counts only)

Next-year JST log equity return over bills, minus the cross-country mean, on a ParlGov mid-term
cabinet start in year t (wide-25's event rule), 15 countries, outcomes 1921-1959 without
1939-1946 and the jst-autocorr-2 drop list; predicted b < 0. Nulls: 20 earlier-dose calendars
and a returns-side AR-preserving bootstrap (jstgates1). Writes research/results/cabinet-drift.md
(statistics only: JST is CC BY-NC-SA 4.0; the ParlGov licence was not read, so no event list).
Pure functions are tested offline in tests/test_w41neg1.py.
"""

from __future__ import annotations

import math
import os
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gatepower as gp  # noqa: E402
import jstgates1 as jg  # noqa: E402
import wide25 as w25  # noqa: E402

OUT = HERE.parent / "results" / "cabinet-drift.md"
DRY = bool(os.environ.get("DRY"))
COUNTRIES = (
    "AUS", "BEL", "CAN", "CHE", "DEU", "DNK", "FIN", "FRA",
    "GBR", "IRL", "ITA", "JPN", "NLD", "NOR", "SWE",
)  # fmt: skip
YEARS = tuple(t for t in range(1921, 1960) if not 1939 <= t <= 1946)
HALVES = (tuple(t for t in YEARS if t <= 1938), tuple(t for t in YEARS if t >= 1947))
DOSE_END = 1958
SHIFTS = tuple(range(2, 22))
SPAN = (1900, 1959)
B_BOOT = 199
SEED = 4101
LAGS = 2

Panel = dict[str, dict[int, float]]


def dose_years(
    starts: Mapping[str, Sequence[int]],
    first: Mapping[str, int],
    countries: Sequence[str],
    end: int = DOSE_END,
    count: bool = False,
) -> Panel:
    """D(i, t) for t from i's first cabinet year to `end`: 1 if any event starts in t (or the
    number of events if `count`)."""
    out: Panel = {}
    for i in countries:
        if i not in first:
            continue
        ys = list(starts.get(i, []))
        out[i] = {
            t: float(ys.count(t)) if count else float(t in ys) for t in range(first[i], end + 1)
        }
    return out


def demean(x: Panel, countries: Sequence[str]) -> Panel:
    """d(i, t) = x(i, t) - mean of x(j, t) over the countries with a value in year t."""
    years = sorted({t for i in countries for t in x.get(i, {})})
    m = {}
    for t in years:
        v = [x[i][t] for i in countries if t in x.get(i, {})]
        m[t] = sum(v) / len(v)
    return {i: {t: v - m[t] for t, v in x.get(i, {}).items()} for i in countries}


def rows_for(
    d: Panel, z: Panel, countries: Sequence[str], years: Sequence[int]
) -> list[tuple[str, int]]:
    out = []
    for i in countries:
        di, zi = d.get(i, {}), z.get(i, {})
        for t1 in years:
            t = t1 - 1
            if t1 in di and t in zi and all(u in di for u in (t - 2, t - 1, t)):
                out.append((i, t1))
    return out


@dataclass(frozen=True)
class Fit:
    b: float
    t: float
    n: int


def fit(
    d: Panel, z: Panel, rows: Sequence[tuple[str, int]], k: int = 0, controls: bool = True
) -> Fit:
    """OLS of 100 d(i, t+1) on z(i, t-k), d(i, t), d(i, t-2..t) summed, country dummies; DK t."""
    rs = [(i, t1) for i, t1 in rows if t1 - 1 - k in z.get(i, {})]
    if len(rs) < 10:
        return Fit(math.nan, math.nan, len(rs))
    isos = sorted({i for i, _ in rs})
    cols = []
    for i, t1 in rs:
        t = t1 - 1
        r = [z[i][t - k]]
        if controls:
            r += [d[i][t], d[i][t - 2] + d[i][t - 1] + d[i][t]]
        r += [1.0 if i == c else 0.0 for c in isos]
        cols.append(r)
    x = np.array(cols)
    yy = np.array([100.0 * d[i][t1] for i, t1 in rs])
    per = np.array([t1 for _, t1 in rs])
    b, t = gp.dk_fit(x, yy, per, LAGS, 0)
    return Fit(float(b), float(t), len(rs))


def rank_low(true: float, others: Sequence[float]) -> int:
    return 1 + sum(o < true for o in others if not math.isnan(o))


def boot_p(true: float, boot: Sequence[float]) -> float:
    return (1 + sum(t <= true for t in boot)) / (len(boot) + 1)


def verdict(f: Fit, rank: int, bp: float, halves: Sequence[Fit]) -> str:
    if not f.b < 0:
        return "DEAD (wrong sign: b >= 0)"
    ok = f.t <= -2 and rank <= 2 and bp <= 0.05 and all(h.b < 0 for h in halves)
    return "NOT DEAD YET (kill-only pass)" if ok else "DEAD (gate not met)"


def null_line(ts: Sequence[float]) -> str:
    a = np.array([t for t in ts if not math.isnan(t)])
    q = np.quantile(a, [0.05, 0.5, 0.95])
    return (
        f"SD {a.std(ddof=1):.2f}, {100 * np.mean(np.abs(a) >= 2):.0f}% past |t| 2, "
        f"5/50/95% {q[0]:+.2f} / {q[1]:+.2f} / {q[2]:+.2f}, extremes {a.min():+.2f} / "
        f"{a.max():+.2f}"
    )


def lag1(z: Panel, rows: Sequence[tuple[str, int]]) -> float:
    s = {(i, t1 - 1) for i, t1 in rows}
    a = np.array([(z[i][t], z[i][t - 1]) for i, t in s if (i, t - 1) in s])
    return float(np.corrcoef(a[:, 0], a[:, 1])[0, 1])


# --- run ---


def main() -> None:
    cabs = w25.load_cabs()
    evs = w25.events(cabs)
    first = {i: k // 12 for i, k in w25.first_start(cabs).items()}

    def starts(keep: bool = True) -> dict[str, list[int]]:
        out: dict[str, list[int]] = {}
        for c in evs:
            if keep or not w25.post_election(c, cabs):
                out.setdefault(c.country, []).append(c.start.year)
        return out

    z = dose_years(starts(), first, COUNTRIES)
    z_cnt = dose_years(starts(), first, COUNTRIES, count=True)
    z_npe = dose_years(starts(False), first, COUNTRIES)

    jst = jg.load_jst()
    xr = jg.excess(jst["eq_tr"], jst["bill_rate"])
    hyper = {i: jg.hyper_years(jst["cpi"].get(i, {})) for i in COUNTRIES}
    x = {
        i: {t: v for t, v in xr.get(i, {}).items() if not jg.dropped(i, t, hyper[i])}
        for i in COUNTRIES
    }
    d = demean(x, COUNTRIES)
    rows = rows_for(d, z, COUNTRIES, YEARS)
    ev_rows = sum(z[i][t1 - 1] for i, t1 in rows)
    per_c = {i: sum(1 for r in rows if r[0] == i) for i in COUNTRIES}
    ev_c = {i: int(sum(z[i][t1 - 1] for j, t1 in rows if j == i)) for i in COUNTRIES}
    lines = [
        "# cabinet-drift (w41-neg-1, provisional W41n): statistics only",
        "",
        f"Rows {len(rows)}, event rows {int(ev_rows)}, dose lag-1 acf {lag1(z, rows):+.3f}.",
        "Rows / event rows per country: "
        + ", ".join(f"{i} {per_c[i]}/{ev_c[i]}" for i in COUNTRIES),
    ]
    if DRY:
        print("\n".join(lines))
        return

    f = fit(d, z, rows)
    sh = [fit(d, z, [r for r in rows if r[1] - 1 - k in z[r[0]]], k).t for k in SHIFTS]
    rank = rank_low(f.t, sh)
    active = [i for i in COUNTRIES if per_c[i]]  # JST R6 has no CAN or IRL
    bm = jg.boot_model(active, xr, z, *SPAN, hyper)
    rng = np.random.default_rng(SEED)
    zyears = {i: sorted(z[i]) for i in active}
    boot = []
    for _ in range(B_BOOT):
        ys, _zs = jg.simulate(bm, rng, zyears)
        xs = {i: {t: ys[i][t] for t in x[i] if t in ys[i]} for i in active}
        ds = demean(xs, active)
        boot.append(fit(ds, z, rows_for(ds, z, active, YEARS)).t)
    bp = boot_p(f.t, boot)
    halves = [fit(d, z, [r for r in rows if r[1] in h]) for h in HALVES]
    v = verdict(f, rank, bp, halves)
    no_fra = [r for r in rows if r[0] != "FRA"]
    shown = [
        ("Outcomes 1921-1938", halves[0]),
        ("Outcomes 1947-1959", halves[1]),
        ("No controls", fit(d, z, rows, controls=False)),
        ("Without France", fit(d, z, no_fra)),
        ("Without post-election formations", fit(d, z_npe, rows)),
        ("Count dose", fit(d, z_cnt, rows)),
    ]
    lines += [
        "",
        f"**Gate: b {f.b:+.3f}% per event year, t {f.t:+.2f}, rows {f.n}; shift rank {rank} of "
        f"{len(SHIFTS) + 1} from the bottom; bootstrap p {bp:.3f} ({B_BOOT} paths). {v}.**",
        "",
        f"Shift null (k {SHIFTS[0]}..{SHIFTS[-1]}): {null_line(sh)}.",
        f"Bootstrap null: {null_line(boot)}.",
        "Shift t by k: " + ", ".join(f"{k} {t:+.2f}" for k, t in zip(SHIFTS, sh, strict=True)),
        "",
        "| Cell | b, % per event year | t | Rows |",
        "|---|---:|---:|---:|",
        f"| **Gate** | **{f.b:+.3f}** | **{f.t:+.2f}** | **{f.n}** |",
    ]
    lines += [f"| {n} | {g.b:+.3f} | {g.t:+.2f} | {g.n} |" for n, g in shown]
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
