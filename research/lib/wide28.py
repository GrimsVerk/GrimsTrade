"""Lane wide-28, gate W45 `arms-fear` (research/cards/wide-28.md, pushed before any number).

Does the US market earn more in the three months after a surge in household gun buying?
Dose: year-on-year log growth of three months of FBI NICS sales checks (handgun + long_gun +
multiple, all states). Row m enters at the end of month m+1; outcome French Mkt-RF over
months m+2 .. m+4. Controls c12, c1 and the market's own realised variance. Two placebo
families (earlier doses; phase surrogates).

    DRY=1 uv run python -I research/lib/wide28.py   # counts, acf, end mismatch only
    uv run python -I research/lib/wide28.py         # the one real run -> results/arms-fear.md
"""

from __future__ import annotations

import csv
import io
import math
import os
import sys
import zipfile
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "src"))

from wide27 import acf1, null_stats, parse_factors, passes, rank_high, ym  # noqa: E402
from wide27 import mi as mi  # noqa: E402

RESULTS = HERE.parent / "results"
DRY = bool(os.environ.get("DRY"))
NICS = "wide-28/nics/2026-11-26/nics-firearm-background-checks.csv"
FACTORS = "french/2026-11-12/F-F_Research_Data_Factors_CSV.zip"
DAILY = "french/2026-11-12/F-F_Research_Data_Factors_daily_CSV.zip"

SHIFTS = tuple(range(25, 104, 2))  # 40 earlier-dose calendars, k months
N_SURR = 40
SEED = 2745
LAST = mi(2025, 10)  # last return month (train)
ROW_FIRST = mi(2008, 8)
ROW_LAST = mi(2023, 9)
REP_FIRST = mi(2000, 1)
REP_LAST = mi(2008, 5)
HALF = mi(2016, 1)
PANDEMIC = (mi(2020, 2), mi(2021, 6))
SALES = ("handgun", "long_gun", "multiple")


def _num(s: str | None) -> float:
    s = (s or "").strip()
    return float(s) if s else 0.0


def parse_nics(rows: Iterable[Mapping[str, str]], cols: Sequence[str] = SALES) -> dict[int, float]:
    """Month index -> sum over all rows of the named columns (empty cells count 0)."""
    out: dict[int, float] = {}
    for r in rows:
        y, m = r["month"].split("-")
        k = mi(int(y), int(m))
        out[k] = out.get(k, 0.0) + sum(_num(r.get(c)) for c in cols)
    return out


def dose_series(s: Mapping[int, float], window: int = 3) -> dict[int, float]:
    """D(m) = ln(sum S(m-window+1..m) / sum S(m-12-window+1..m-12)), all months present."""
    out: dict[int, float] = {}
    for m in sorted(s):
        now = [s.get(m - i) for i in range(window)]
        ago = [s.get(m - 12 - i) for i in range(window)]
        if any(x is None for x in now + ago):
            continue
        a = sum(x for x in now if x is not None)
        b = sum(x for x in ago if x is not None)
        if a > 0 and b > 0:
            out[m] = math.log(a / b)
    return out


def parse_daily(text: str, last: int = LAST) -> dict[int, list[float]]:
    """Month index -> daily Mkt-RF values (%), months <= last."""
    out: dict[int, list[float]] = {}
    for line in io.StringIO(text):
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) >= 2 and len(parts[0]) == 8 and parts[0].isdigit():
            k = mi(int(parts[0][:4]), int(parts[0][4:6]))
            if k <= last:
                out.setdefault(k, []).append(float(parts[1]))
    return out


@dataclass(frozen=True)
class Spec:
    h: int = 3
    lags: int = 3
    ctrl: tuple[str, ...] = ("c12", "c1", "rv")
    first: int = ROW_FIRST
    last: int = ROW_LAST
    drop: tuple[int, int] | None = None


def build(
    mkt: Mapping[int, float], daily: Mapping[int, Sequence[float]], spec: Spec
) -> dict[int, tuple[float, dict[str, float]]]:
    """Row month m -> (y, controls). Entry at the end of m+1; y over m+2 .. m+1+h."""
    out: dict[int, tuple[float, dict[str, float]]] = {}
    for m in range(spec.first, spec.last + 1):
        if spec.drop and spec.drop[0] <= m <= spec.drop[1]:
            continue
        fut = [mkt.get(m + 1 + i) for i in range(1, spec.h + 1)]
        past = [mkt.get(u) for u in range(m - 10, m + 2)]
        dd = [daily.get(u) for u in (m - 1, m, m + 1)]
        if any(x is None for x in fut + past) or any(not d for d in dd):
            continue
        ss = sum(x * x for d in dd if d for x in d)
        c = {
            "c12": float(sum(x for x in past if x is not None)),
            "c1": float(mkt[m + 1]),
            "rv": math.log(ss) if ss > 0 else math.nan,
        }
        if any(math.isnan(c[k]) for k in spec.ctrl):
            continue
        out[m] = (float(sum(x for x in fut if x is not None)), c)
    return out


def fit(
    rows: Mapping[int, tuple[float, dict[str, float]]],
    dose: Mapping[int, float],
    spec: Spec,
    shift: int = 0,
) -> tuple[float, float, int]:
    """(b, NW t, n) of y on D(m - shift), the controls and a constant."""
    from gatepower import dk_fit

    xs, ys, ps = [], [], []
    for m, (y, c) in sorted(rows.items()):
        d = dose.get(m - shift)
        if d is None or math.isnan(d):
            continue
        xs.append([d, 1.0] + [c[k] for k in spec.ctrl])
        ys.append(y)
        ps.append(m)
    if len(ys) < 10:
        return math.nan, math.nan, len(ys)
    b, t = dk_fit(np.array(xs), np.array(ys), np.array(ps), spec.lags, 0)
    return b, t, len(ys)


def main() -> None:  # pragma: no cover - needs the cache
    import gatenull2

    from grimstrade.cache import cache_root

    root = cache_root()
    with (root / NICS).open(newline="") as f:
        nrows = list(csv.DictReader(f))
    sales = parse_nics(nrows)
    with zipfile.ZipFile(root / FACTORS) as z:
        mkt = parse_factors(z.read(z.namelist()[0]).decode("latin-1"))
    with zipfile.ZipFile(root / DAILY) as z:
        daily = parse_daily(z.read(z.namelist()[0]).decode("latin-1"))
    dose = dose_series(sales)
    spec = Spec()
    full = sorted(dose)
    acf = acf1(dose, full)
    dv = np.array([dose[m] for m in full])
    endgap = abs(dv[-1] - dv[0]) / dv.std(ddof=1)
    rows = {m: r for m, r in build(mkt, daily, spec).items() if m in dose}
    shift_ok = all(all((m - k) in dose for m in rows) for k in SHIFTS)
    print(f"NICS months {ym(min(sales))} .. {ym(max(sales))}: {len(sales)}")
    print(f"dose defined {ym(full[0])} .. {ym(full[-1])}: {len(full)} months")
    print(f"gate rows {len(rows)} ({ym(min(rows))} .. {ym(max(rows))})")
    print(f"lag-1 acf of the dose {acf:.3f}; |end - start| / SD {endgap:.2f}")
    print(f"every shift defined on every row: {shift_ok}")
    family = "iaaft" if endgap > 1 else "phase"
    gating_surr = acf >= 0.8
    print(f"surrogate family: {family}; gating: {gating_surr}")
    if DRY:
        return
    sur = gatenull2.surrogate_doses(dose, family, N_SURR, SEED)
    b, t, n = fit(rows, dose, spec)
    ts_shift = [fit(rows, dose, spec, k)[1] for k in SHIFTS]
    ts_surr = [fit(rows, s, spec)[1] for s in sur]
    r_shift = rank_high(t, ts_shift)
    r_surr = rank_high(t, ts_surr)
    ok = passes(b, t, r_shift, r_surr if gating_surr else None)
    cells: list[tuple[str, float, float, int]] = [("Gate", b, t, n)]

    def cell(name: str, sp: Spec, d: Mapping[int, float]) -> None:
        rr = {m: r for m, r in build(mkt, daily, sp).items() if m in d}
        cells.append((name, *fit(rr, d, sp)))

    cell("Horizon 1 month (NW 0)", Spec(h=1, lags=0), dose)
    cell("Horizon 6 months (NW 6)", Spec(h=6, lags=6), dose)
    cell("Horizon 12 months (NW 12)", Spec(h=12, lags=12), dose)
    cell("No controls", Spec(ctrl=()), dose)
    cell("Without rv", Spec(ctrl=("c12", "c1")), dose)
    cell("One-month dose ln(S(m)/S(m-12))", spec, dose_series(sales, window=1))
    cell("Dose from `totals`", spec, dose_series(parse_nics(nrows, ("totals",))))
    cell("Rows 2008-08 .. 2015-12", Spec(last=HALF - 1), dose)
    cell("Rows 2016-01 .. 2023-09", Spec(first=HALF), dose)
    cell("Without rows 2020-02 .. 2021-06", Spec(drop=PANDEMIC), dose)
    rep = None
    if ok:
        rsp = Spec(first=REP_FIRST, last=REP_LAST)
        rrows = {m: r for m, r in build(mkt, daily, rsp).items() if m in dose}
        rb, rt, rn = fit(rrows, dose, rsp)
        rr = rank_high(rt, [fit(rrows, s, rsp)[1] for s in sur])
        rep = (rb, rt, rn, rr, rb > 0 and rt >= 2 and rr <= 2)
    ns, nu = null_stats(ts_shift), null_stats(ts_surr)
    lines = [
        "# W45 `arms-fear`: results",
        "",
        "Card: `research/cards/wide-28.md`. Code: `research/lib/wide28.py`. One real run.",
        "",
        f"- NICS months {ym(min(sales))} .. {ym(max(sales))}; dose defined {ym(full[0])} .. "
        f"{ym(full[-1])} ({len(full)} months), SD {dv.std(ddof=1):.3f}; gate rows {n}.",
        f"- Lag-1 acf of the dose {acf:.3f}; |end - start| / SD {endgap:.2f}; surrogate family "
        f"`{family}`, gating: {gating_surr}.",
        f"- **Gate: b {b:+.3f} % per unit of D over 3 months, t {t:+.2f}; rank {r_shift} of 41 "
        f"(shifted), {r_surr} of 41 (surrogates). Pass: {ok}.**",
        "",
        "| Cell | b, % | t | Rows |",
        "|---|---:|---:|---:|",
    ]
    lines += [f"| {c[0]} | {c[1]:+.3f} | {c[2]:+.2f} | {c[3]} |" for c in cells]
    lines += ["", "| Null | SD | share \\|t\\|>=2 | 5% | 50% | 95% | min | max |"]
    lines += ["|---|---:|---:|---:|---:|---:|---:|---:|"]
    for name, s in (("Shifted (k 25..103)", ns), (f"Surrogates ({family})", nu)):
        lines.append(
            f"| {name} | {s['sd']:.2f} | {s['share2']:.2f} | {s['q05']:+.2f} | {s['q50']:+.2f} "
            f"| {s['q95']:+.2f} | {s['min']:+.2f} | {s['max']:+.2f} |"
        )
    pairs = list(zip(SHIFTS, ts_shift, strict=True))
    lines += ["", "Shifted t by k: " + ", ".join(f"{k}: {x:+.2f}" for k, x in pairs)]
    lines += ["", "R45: " + ("not run (the gate failed)" if rep is None else str(rep))]
    text = "\n".join(lines) + "\n"
    (RESULTS / "arms-fear.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
