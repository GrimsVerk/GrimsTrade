"""Lane wide-27, gate W44 `revision-noise` (research/cards/wide-27.md, pushed before any number).

Does the US market earn more in the three months after a spell of large payroll revisions?
Dose: the 12-month mean of first + second revisions of the monthly payroll change (Philadelphia
Fed real-time vintages), in logs, minus its trailing 10-year mean. Outcome: French Mkt-RF over
months v+1 .. v+3. Controls from vintage v. Two placebo families (earlier doses; phase
surrogates, gate-null-2's proposed rule, adopted by the card).

    DRY=1 uv run python -I research/lib/wide27.py   # counts, acf, end mismatch only
    uv run python -I research/lib/wide27.py         # the one real run -> results/revision-noise.md
"""

from __future__ import annotations

import io
import math
import os
import re
import sys
import zipfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "src"))

RESULTS = HERE.parent / "results"
DRY = bool(os.environ.get("DRY"))
EMPLOY = "philly-rtdsm/2026-11-12/employmvmd.xlsx"
FACTORS = "french/2026-11-12/F-F_Research_Data_Factors_CSV.zip"

SHIFTS = tuple(range(25, 104, 2))  # 40 earlier-dose calendars, k months
N_SURR = 40
SEED = 2744
H = 3
LAGS = 3


def mi(y: int, m: int) -> int:
    """Month index: months since 0000-01."""
    return 12 * y + m - 1


def ym(k: int) -> str:
    return f"{k // 12}-{k % 12 + 1:02d}"


FIRST_VINTAGE = mi(1964, 12)
LAST_VINTAGE = mi(2025, 10)
LAST = mi(2025, 10)  # last return month (train)
ROW_FIRST = mi(1990, 1)
ROW_LAST = mi(2025, 7)
REP_FIRST = mi(1976, 1)
REP_LAST = mi(1989, 9)
HALF = mi(2008, 1)

Vintages = dict[int, dict[int, float]]  # vintage month -> {reference month -> level}

_VCOL = re.compile(r"^EMPLOY(\d{2})M(\d{1,2})$")


def vintage_month(col: str) -> int | None:
    """`EMPLOY64M12` -> month index of 1964-12; two-digit years 64-99 are 19xx, else 20xx."""
    m = _VCOL.match(col)
    if not m:
        return None
    yy, mm = int(m.group(1)), int(m.group(2))
    return mi(1900 + yy if yy >= 64 else 2000 + yy, mm)


def parse_vintages(rows: Sequence[Sequence[str]]) -> Vintages:
    """Vintages FIRST_VINTAGE .. LAST_VINTAGE from the sheet's cell text. Missing: #N/A or ''."""
    head = list(rows[0])
    cols = {i: vintage_month(c) for i, c in enumerate(head)}
    out: Vintages = {}
    for v in cols.values():
        if v is not None and FIRST_VINTAGE <= v <= LAST_VINTAGE:
            out[v] = {}
    for r in rows[1:]:
        if not r or not r[0] or ":" not in r[0]:
            continue
        y, m = r[0].split(":")
        ref = mi(int(y), int(m))
        for i, v in cols.items():
            if v is None or v not in out or i >= len(r):
                continue
            cell = r[i].strip()
            if cell and cell != "#N/A":
                out[v][ref] = float(cell)
    return out


def delta(vint: Mapping[int, float], j: int) -> float:
    a, b = vint.get(j), vint.get(j - 1)
    if a is None or b is None or a <= 0 or b <= 0:
        return math.nan
    return 100.0 * math.log(a / b)


def revision(vs: Vintages, v: int, first_only: bool = False) -> float:
    """rev(v) = |D_v(v-2) - D_{v-1}(v-2)| + |D_v(v-3) - D_{v-1}(v-3)|."""
    if v not in vs or v - 1 not in vs:
        return math.nan
    a = abs(delta(vs[v], v - 2) - delta(vs[v - 1], v - 2))
    if first_only:
        return a
    return a + abs(delta(vs[v], v - 3) - delta(vs[v - 1], v - 3))


def rolling_mean(x: Mapping[int, float], v: int, n: int) -> float:
    vals = [x.get(u, math.nan) for u in range(v - n + 1, v + 1)]
    return math.nan if any(math.isnan(a) for a in vals) else sum(vals) / n


def dose_series(vs: Vintages, first_only: bool = False, detrend: bool = True) -> dict[int, float]:
    """D(v) = ln R12(v) - mean of ln R12 over v-120 .. v-1 (or ln R12 if not detrend)."""
    rev = {v: revision(vs, v, first_only) for v in vs}
    lr: dict[int, float] = {}
    for v in vs:
        r12 = rolling_mean(rev, v, 12)
        if not math.isnan(r12) and r12 > 0:
            lr[v] = math.log(r12)
    if not detrend:
        return lr
    out: dict[int, float] = {}
    for v in lr:
        past = [lr.get(u) for u in range(v - 120, v)]
        if all(p is not None for p in past):
            out[v] = lr[v] - sum(p for p in past if p is not None) / 120
    return out


def controls(vs: Vintages, v: int) -> tuple[float, float]:
    """(g12, s12) from vintage v: payroll growth over a year; ln mean abs deviation of the
    monthly changes j = v-12 .. v-1."""
    vint = vs.get(v, {})
    a, b = vint.get(v - 1), vint.get(v - 13)
    g12 = 100.0 * math.log(a / b) if a and b else math.nan
    d = [delta(vint, j) for j in range(v - 12, v)]
    if any(math.isnan(x) for x in d):
        return g12, math.nan
    mu = sum(d) / len(d)
    mad = sum(abs(x - mu) for x in d) / len(d)
    return g12, (math.log(mad) if mad > 0 else math.nan)


def parse_factors(text: str, last: int = LAST) -> dict[int, float]:
    """Monthly Mkt-RF (%) from the French factors CSV text, months <= last."""
    out: dict[int, float] = {}
    for line in io.StringIO(text):
        parts = [p.strip() for p in line.strip().split(",")]
        if out and "Annual" in line:
            break
        if len(parts) == 5 and len(parts[0]) == 6 and parts[0].isdigit():
            k = mi(int(parts[0][:4]), int(parts[0][4:]))
            if k <= last:
                out[k] = float(parts[1])
    return out


@dataclass(frozen=True)
class Spec:
    h: int = H
    lags: int = LAGS
    ctrl: tuple[str, ...] = ("g12", "s12", "c12", "c1")
    first: int = ROW_FIRST
    last: int = ROW_LAST


def build(
    vs: Vintages, mkt: Mapping[int, float], spec: Spec
) -> dict[int, tuple[float, dict[str, float]]]:
    """Row month v -> (y, controls), rows with y and every control defined."""
    out: dict[int, tuple[float, dict[str, float]]] = {}
    for v in range(spec.first, spec.last + 1):
        fut = [mkt.get(v + i) for i in range(1, spec.h + 1)]
        past = [mkt.get(u) for u in range(v - 11, v + 1)]
        if any(x is None for x in fut) or any(x is None for x in past):
            continue
        g12, s12 = controls(vs, v)
        c = {
            "g12": g12,
            "s12": s12,
            "c12": float(sum(x for x in past if x is not None)),
            "c1": float(mkt[v]),
        }
        if any(math.isnan(c[k]) for k in spec.ctrl):
            continue
        out[v] = (float(sum(x for x in fut if x is not None)), c)
    return out


def fit(
    rows: Mapping[int, tuple[float, dict[str, float]]],
    dose: Mapping[int, float],
    spec: Spec,
    shift: int = 0,
) -> tuple[float, float, int]:
    """(b, NW t, n) of y on D(v - shift), the controls and a constant."""
    from gatepower import dk_fit

    xs, ys, ps = [], [], []
    for v, (y, c) in sorted(rows.items()):
        d = dose.get(v - shift)
        if d is None or math.isnan(d):
            continue
        xs.append([d, 1.0] + [c[k] for k in spec.ctrl])
        ys.append(y)
        ps.append(v)
    if len(ys) < 10:
        return math.nan, math.nan, len(ys)
    b, t = dk_fit(np.array(xs), np.array(ys), np.array(ps), spec.lags, 0)
    return b, t, len(ys)


def rank_high(true: float, others: Sequence[float]) -> int:
    return 1 + sum(1 for o in others if o >= true)


def null_stats(ts: Sequence[float]) -> dict[str, float]:
    a = np.array([t for t in ts if not math.isnan(t)])
    return {
        "sd": float(a.std(ddof=1)),
        "share2": float(np.mean(np.abs(a) >= 2)),
        "q05": float(np.quantile(a, 0.05)),
        "q50": float(np.quantile(a, 0.5)),
        "q95": float(np.quantile(a, 0.95)),
        "min": float(a.min()),
        "max": float(a.max()),
    }


def acf1(dose: Mapping[int, float], months: Sequence[int]) -> float:
    x = np.array([dose[v] for v in months if v in dose and v - 1 in dose])
    x0 = np.array([dose[v - 1] for v in months if v in dose and v - 1 in dose])
    return float(np.corrcoef(x, x0)[0, 1])


def surrogates(dose: Mapping[int, float], family: str) -> list[dict[int, float]]:
    import gatenull2

    return gatenull2.surrogate_doses(dose, family, N_SURR, SEED)


def passes(b: float, t: float, rank_shift: int, rank_surr: int | None) -> bool:
    ok = b > 0 and t >= 2 and rank_shift <= 2
    return ok and (rank_surr is None or rank_surr <= 2)


def main() -> None:  # pragma: no cover - needs the cache
    import long_x

    from grimstrade.cache import cache_root

    root = cache_root()
    vs = parse_vintages(long_x.xlsx_rows(root / EMPLOY, "employ"))
    with zipfile.ZipFile(root / FACTORS) as z:
        mkt = parse_factors(z.read(z.namelist()[0]).decode("latin-1"))
    dose = dose_series(vs)
    spec = Spec()
    rows = build(vs, mkt, spec)
    dmonths = sorted(dose)
    full = [v for v in dmonths if v <= ROW_LAST]
    acf = acf1(dose, full)
    dv = np.array([dose[v] for v in full])
    endgap = abs(dv[-1] - dv[0]) / dv.std(ddof=1)
    gate_rows = {v: r for v, r in rows.items() if v in dose}
    shift_ok = all(all((v - k) in dose for v in gate_rows) for k in SHIFTS)
    print(f"vintages {ym(min(vs))} .. {ym(max(vs))}: {len(vs)}")
    print(f"dose defined {ym(full[0])} .. {ym(full[-1])}: {len(full)} months")
    print(f"gate rows {len(gate_rows)} ({ym(min(gate_rows))} .. {ym(max(gate_rows))})")
    print(f"lag-1 acf of the dose {acf:.3f}; |end - start| / SD {endgap:.2f}")
    print(f"every shift defined on every row: {shift_ok}")
    family = "iaaft" if endgap > 1 else "phase"
    print(f"surrogate family: {family}; gating: {acf >= 0.8}")
    if DRY:
        return
    surr_dose = {v: dose[v] for v in full}
    sur = surrogates(surr_dose, family)
    b, t, n = fit(gate_rows, dose, spec)
    ts_shift = [fit(gate_rows, dose, spec, k)[1] for k in SHIFTS]
    ts_surr = [fit(gate_rows, s, spec)[1] for s in sur]
    r_shift = rank_high(t, ts_shift)
    r_surr = rank_high(t, ts_surr)
    gating_surr = acf >= 0.8
    ok = passes(b, t, r_shift, r_surr if gating_surr else None)
    cells: list[tuple[str, float, float, int]] = [("Gate", b, t, n)]

    def cell(name: str, sp: Spec, d: Mapping[int, float]) -> None:
        rr = build(vs, mkt, sp)
        rr = {v: r for v, r in rr.items() if v in d}
        cells.append((name, *fit(rr, d, sp)))

    cell("Horizon 1 month (NW 0)", Spec(h=1, lags=0), dose)
    cell("Horizon 6 months (NW 6)", Spec(h=6, lags=6), dose)
    cell("Horizon 12 months (NW 12)", Spec(h=12, lags=12), dose)
    cell("No controls", Spec(ctrl=()), dose)
    cell("Without s12", Spec(ctrl=("g12", "c12", "c1")), dose)
    cell("First revision only", spec, dose_series(vs, first_only=True))
    cell("Dose in levels (ln R12, no trailing mean)", spec, dose_series(vs, detrend=False))
    cell("Rows 1990-01 .. 2007-12", Spec(last=HALF - 1), dose)
    cell("Rows 2008-01 .. 2025-07", Spec(first=HALF), dose)
    rep = None
    if ok:
        rsp = Spec(first=REP_FIRST, last=REP_LAST)
        rrows = {v: r for v, r in build(vs, mkt, rsp).items() if v in dose}
        rb, rt, rn = fit(rrows, dose, rsp)
        rts = [fit(rrows, s, rsp)[1] for s in sur]
        rr = rank_high(rt, rts)
        rep = (rb, rt, rn, rr, rb > 0 and rt >= 2 and rr <= 2)
    ns, nu = null_stats(ts_shift), null_stats(ts_surr)
    lines = [
        "# W44 `revision-noise`: results",
        "",
        "Card: `research/cards/wide-27.md`. Code: `research/lib/wide27.py`. One real run.",
        "",
        f"- Vintages {ym(min(vs))} .. {ym(max(vs))}; dose defined {ym(full[0])} .. "
        f"{ym(full[-1])} ({len(full)} months); gate rows {n}.",
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
    lines += [
        "",
        "Shifted t by k: " + ", ".join(f"{k}: {x:+.2f}" for k, x in pairs),
    ]
    lines += ["", "R44: " + ("not run (the gate failed)" if rep is None else str(rep))]
    text = "\n".join(lines) + "\n"
    (RESULTS / "revision-noise.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
