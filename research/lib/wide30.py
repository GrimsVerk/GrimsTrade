"""Lane wide-30, gate W47 `payout-ratio` (research/cards/wide-30.md, pushed before any number).

Does the US market earn more in the twelve months after a high payout ratio? Dose: ln(D/E)
from Shiller's ie_data.xls minus its mean over the previous 60 months. Row m enters at the
end of month m+4; outcome French Mkt-RF over m+5 .. m+16. Controls c12 (m-7 .. m+4), c1
(m+4), rv (m+2 .. m+4). Predicted b > 0: ranks are taken on t.

Implementation: wide28's builder enters a row at the end of m'+1, so the dose is re-indexed
to m' = m + 3; every window in the card then matches wide28's (y over m'+2 .. m'+13 etc.).

    DRY=1 uv run python -I research/lib/wide30.py   # counts, acf, end mismatch only
    uv run python -I research/lib/wide30.py         # the one real run -> results/payout-ratio.md
"""

from __future__ import annotations

import math
import os
import sys
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "src"))

from wide27 import acf1, null_stats, parse_factors, rank_high, ym  # noqa: E402
from wide27 import mi as mi  # noqa: E402
from wide28 import Spec, build, fit, parse_daily  # noqa: E402

RESULTS = HERE.parent / "results"
DRY = bool(os.environ.get("DRY"))
SHILLER = "shiller/2026-11-12/ie_data.xls"
FACTORS = "french/2026-11-12/F-F_Research_Data_Factors_CSV.zip"
DAILY = "french/2026-11-12/F-F_Research_Data_Factors_daily_CSV.zip"

LAST = mi(2025, 10)
LAG = 3  # m' = m + 3: wide28 enters at m'+1 = m+4
SHIFTS = tuple(range(25, 104, 2))
N_SURR = 40
SEED = 2747
ROW_FIRST = mi(1991, 1) + LAG
ROW_LAST = mi(2024, 6) + LAG
REP_FIRST = mi(1932, 1) + LAG
REP_LAST = mi(1989, 12) + LAG
HALF = mi(2008, 1) + LAG
GFC = (mi(2008, 7) + LAG, mi(2010, 6) + LAG)


def parse_shiller(rows: Sequence[Sequence[object]]) -> dict[int, float]:
    """Month index -> ln(D/E) for rows with a yyyy.mm date and positive D (col 2), E (col 3)."""
    out: dict[int, float] = {}
    for v in rows:
        if len(v) < 4 or not isinstance(v[0], float):
            continue
        y = int(v[0])
        m = round((v[0] - y) * 100)
        d, e = v[2], v[3]
        if not 1 <= m <= 12 or not isinstance(d, float) or not isinstance(e, float):
            continue
        if d > 0 and e > 0:
            out[mi(y, m)] = math.log(d / e)
    return out


def detrend(p: Mapping[int, float], base: int = 60) -> dict[int, float]:
    """H(m) = P(m) - mean(P(m-base) .. P(m-1)); undefined if any of those months is missing."""
    out: dict[int, float] = {}
    for m, v in p.items():
        past = [p.get(m - i) for i in range(1, base + 1)]
        if any(x is None for x in past):
            continue
        out[m] = v - sum(x for x in past if x is not None) / base
    return out


def reindex(h: Mapping[int, float], lag: int = LAG) -> dict[int, float]:
    return {m + lag: v for m, v in h.items()}


def passes_pos(b: float, t: float, r_shift: int, r_surr: int | None) -> bool:
    ok = b > 0 and t >= 2 and r_shift <= 2
    return ok and (r_surr is None or r_surr <= 2)


def pos_rank(t: float, others: Sequence[float]) -> int:
    """Rank of t among others (1 = most positive t)."""
    return rank_high(t, list(others))


def main() -> None:  # pragma: no cover - needs the cache
    import gatenull2
    import xlrd  # type: ignore[import-untyped]

    from grimstrade.cache import cache_root

    root = cache_root()
    sheet = xlrd.open_workbook(str(root / SHILLER)).sheet_by_name("Data")
    raw = parse_shiller([sheet.row_values(i) for i in range(sheet.nrows)])
    p = {m: v for m, v in raw.items() if m <= LAST}
    with zipfile.ZipFile(root / FACTORS) as z:
        mkt = parse_factors(z.read(z.namelist()[0]).decode("latin-1"))
    with zipfile.ZipFile(root / DAILY) as z:
        daily = parse_daily(z.read(z.namelist()[0]).decode("latin-1"))
    dose = reindex(detrend(p))
    full = sorted(dose)
    contiguous = full[-1] - full[0] + 1 == len(full)
    acf = acf1(dose, full)
    dv = np.array([dose[m] for m in full])
    endgap = abs(dv[-1] - dv[0]) / dv.std(ddof=1)
    spec = Spec(h=12, lags=12, first=ROW_FIRST, last=ROW_LAST)
    grows = {m: r for m, r in build(mkt, daily, spec).items() if m in dose}
    shift_ok = all(all((m - k) in dose for m in grows) for k in SHIFTS)
    print(f"D/E months {ym(min(p))} .. {ym(max(p))}: {len(p)}")
    print(f"dose (m' index) {ym(full[0])} .. {ym(full[-1])}: {len(full)}, contiguous {contiguous}")
    print(f"gate rows {len(grows)} (m' {ym(min(grows))} .. {ym(max(grows))})")
    print(f"lag-1 acf {acf:.3f}; |end - start| / SD {endgap:.2f}; shifts defined {shift_ok}")
    family = "iaaft" if endgap > 1 else "phase"
    gating_surr = acf >= 0.8
    print(f"surrogate family: {family}; gating: {gating_surr}")
    if DRY:
        return
    sur = gatenull2.surrogate_doses(dose, family, N_SURR, SEED)
    b, t, nn = fit(grows, dose, spec)
    ts_shift = [fit(grows, dose, spec, k)[1] for k in SHIFTS]
    ts_surr = [fit(grows, s, spec)[1] for s in sur]
    r_shift, r_surr = pos_rank(t, ts_shift), pos_rank(t, ts_surr)
    ok = passes_pos(b, t, r_shift, r_surr if gating_surr else None)
    cells: list[tuple[str, float, float, int]] = [("Gate", b, t, nn)]

    def cell(name: str, sp: Spec) -> None:
        rr = {m: r for m, r in build(mkt, daily, sp).items() if m in dose}
        cells.append((name, *fit(rr, dose, sp)))

    cell("Horizon 3 months (NW 3)", Spec(h=3, lags=3, first=ROW_FIRST, last=ROW_LAST))
    cell("Horizon 6 months (NW 6)", Spec(h=6, lags=6, first=ROW_FIRST, last=ROW_LAST))
    cell("No controls", Spec(h=12, lags=12, ctrl=(), first=ROW_FIRST, last=ROW_LAST))
    cell("Without rv", Spec(h=12, lags=12, ctrl=("c12", "c1"), first=ROW_FIRST, last=ROW_LAST))
    cell("Rows 1991-01 .. 2007-12", Spec(h=12, lags=12, first=ROW_FIRST, last=HALF - 1))
    cell("Rows 2008-01 .. 2024-06", Spec(h=12, lags=12, first=HALF, last=ROW_LAST))
    cell(
        "Without rows 2008-07 .. 2010-06",
        Spec(h=12, lags=12, drop=GFC, first=ROW_FIRST, last=ROW_LAST),
    )
    rep = None
    if ok:
        rsp = Spec(h=12, lags=12, first=REP_FIRST, last=REP_LAST)
        rrows = {m: r for m, r in build(mkt, daily, rsp).items() if m in dose}
        rb, rt, rn = fit(rrows, dose, rsp)
        rr = pos_rank(rt, [fit(rrows, s, rsp)[1] for s in sur])
        rep = (rb, rt, rn, rr, rb > 0 and rt >= 2 and rr <= 2)
    ns, nu = null_stats(ts_shift), null_stats(ts_surr)
    lines = [
        "# W47 `payout-ratio`: results",
        "",
        "Card: `research/cards/wide-30.md`. Code: `research/lib/wide30.py`. One real run.",
        "Row months below are the card's m (the code's m' minus 3).",
        "",
        f"- D/E months {ym(min(p))} .. {ym(max(p))}; dose SD {dv.std(ddof=1):.3f}; gate rows {nn}.",
        f"- Lag-1 acf {acf:.3f}; |end - start| / SD {endgap:.2f}; surrogates `{family}`, "
        f"gating: {gating_surr}.",
        f"- **Gate: b {b:+.3f} % per unit of H over 12 months, t {t:+.2f}; rank of t "
        f"{r_shift} of 41 (shifted), {r_surr} of 41 (surrogates). Pass: {ok}.**",
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
    lines += ["", "R47: " + ("not run (the gate failed)" if rep is None else str(rep))]
    text = "\n".join(lines) + "\n"
    (RESULTS / "payout-ratio.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
