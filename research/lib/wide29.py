"""Lane wide-29, gate W46 `ipo-heat` (research/cards/wide-29.md, pushed before any number).

Does the US market earn less in the twelve months after a hot IPO market? Dose: ln(1 + net
IPO count over twelve months, Ritter's IPOALL.xlsx) minus its mean over the previous 60
months. Row m enters at the end of month m+1; outcome French Mkt-RF over m+2 .. m+13.
Controls c12, c1, rv (as wide-28). Predicted b < 0: ranks are taken on -t.

    DRY=1 uv run python -I research/lib/wide29.py   # counts, acf, end mismatch only
    uv run python -I research/lib/wide29.py         # the one real run -> results/ipo-heat.md
"""

from __future__ import annotations

import math
import os
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "src"))

from wide27 import acf1, mi, null_stats, parse_factors, rank_high, ym  # noqa: E402
from wide28 import Spec, build, fit, parse_daily  # noqa: E402

RESULTS = HERE.parent / "results"
DRY = bool(os.environ.get("DRY"))
IPO = "wide-29/ritter/2026-11-26/IPOALL.xlsx"
FACTORS = "french/2026-11-12/F-F_Research_Data_Factors_CSV.zip"
DAILY = "french/2026-11-12/F-F_Research_Data_Factors_daily_CSV.zip"

LAST = mi(2025, 10)  # nothing after the train window
SHIFTS = tuple(range(25, 104, 2))
N_SURR = 40
SEED = 2746
ROW_FIRST = mi(1991, 1)
ROW_LAST = mi(2024, 9)
REP_FIRST = mi(1966, 1)
REP_LAST = mi(1989, 12)
HALF = mi(2008, 1)
DOTCOM = (mi(1998, 1), mi(2001, 12))
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _col(ref: str) -> str:
    return "".join(ch for ch in ref if ch.isalpha())


def read_sheet(data: bytes) -> list[dict[str, str]]:
    """First sheet of an xlsx as a list of {column letter: cell text} (stdlib only)."""
    import io

    z = zipfile.ZipFile(io.BytesIO(data))
    ss: list[str] = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(NS + "si"):
            ss.append("".join(t.text or "" for t in si.iter(NS + "t")))
    out: list[dict[str, str]] = []
    for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(NS + "row"):
        cells: dict[str, str] = {}
        for c in row.iter(NS + "c"):
            v = c.find(NS + "v")
            if v is None or v.text is None:
                continue
            cells[_col(c.get("r", ""))] = ss[int(v.text)] if c.get("t") == "s" else v.text
        out.append(cells)
    return out


def _float(s: str | None) -> float | None:
    try:
        return float(s) if s is not None else None
    except ValueError:
        return None


def parse_ipo(rows: Sequence[Mapping[str, str]], col: str = "D") -> dict[int, float]:
    """Month index -> value of `col` for rows whose A is a month 1-12 and B a two-digit year
    (60-99 -> 19xx, 00-59 -> 20xx); non-numeric cells are skipped."""
    out: dict[int, float] = {}
    for r in rows:
        m, y, v = _float(r.get("A")), _float(r.get("B")), _float(r.get(col))
        if m is None or y is None or v is None or not (1 <= m <= 12 and m == int(m)):
            continue
        yy = int(y)
        if not 0 <= yy <= 99:
            continue
        out[mi(1900 + yy if yy >= 60 else 2000 + yy, int(m))] = v
    return out


def heat(n: Mapping[int, float], window: int = 12, base: int = 60, mean: bool = False) -> dict[int, float]:
    """H(m) = L(m) - mean(L(m-base) .. L(m-1)), L = ln(1 + sum of `window` months) (or, with
    mean=True, the plain mean of `window` months). Months with a gap are undefined."""
    lv: dict[int, float] = {}
    for m in sorted(n):
        xs = [n.get(m - i) for i in range(window)]
        if any(x is None for x in xs):
            continue
        s = sum(x for x in xs if x is not None)
        lv[m] = s / window if mean else math.log(1.0 + max(s, 0.0))
    out: dict[int, float] = {}
    for m, v in lv.items():
        past = [lv.get(m - i) for i in range(1, base + 1)]
        if any(p is None for p in past):
            continue
        out[m] = v - sum(p for p in past if p is not None) / base
    return out


def passes_neg(b: float, t: float, r_shift: int, r_surr: int | None) -> bool:
    ok = b < 0 and t <= -2 and r_shift <= 2
    return ok and (r_surr is None or r_surr <= 2)


def neg_rank(t: float, others: Sequence[float]) -> int:
    """Rank of -t among -others (1 = most negative t)."""
    return rank_high(-t, [-o for o in others])


def main() -> None:  # pragma: no cover - needs the cache
    import gatenull2

    from grimstrade.cache import cache_root

    root = cache_root()
    rows = read_sheet((root / IPO).read_bytes())
    n = {m: v for m, v in parse_ipo(rows).items() if m <= LAST}  # train window only
    with zipfile.ZipFile(root / FACTORS) as z:
        mkt = parse_factors(z.read(z.namelist()[0]).decode("latin-1"))
    with zipfile.ZipFile(root / DAILY) as z:
        daily = parse_daily(z.read(z.namelist()[0]).decode("latin-1"))
    dose = heat(n)
    full = sorted(dose)
    contiguous = full[-1] - full[0] + 1 == len(full)
    acf = acf1(dose, full)
    dv = np.array([dose[m] for m in full])
    endgap = abs(dv[-1] - dv[0]) / dv.std(ddof=1)
    spec = Spec(h=12, lags=12, first=ROW_FIRST, last=ROW_LAST)
    grows = {m: r for m, r in build(mkt, daily, spec).items() if m in dose}
    shift_ok = all(all((m - k) in dose for m in grows) for k in SHIFTS)
    print(f"IPO months {ym(min(n))} .. {ym(max(n))}: {len(n)}")
    print(f"dose defined {ym(full[0])} .. {ym(full[-1])}: {len(full)}, contiguous {contiguous}")
    print(f"gate rows {len(grows)} ({ym(min(grows))} .. {ym(max(grows))})")
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
    r_shift, r_surr = neg_rank(t, ts_shift), neg_rank(t, ts_surr)
    ok = passes_neg(b, t, r_shift, r_surr if gating_surr else None)
    cells: list[tuple[str, float, float, int]] = [("Gate", b, t, nn)]

    def cell(name: str, sp: Spec, d: Mapping[int, float]) -> None:
        rr = {m: r for m, r in build(mkt, daily, sp).items() if m in d}
        cells.append((name, *fit(rr, d, sp)))

    g = {"first": ROW_FIRST, "last": ROW_LAST}
    cell("Horizon 3 months (NW 3)", Spec(h=3, lags=3, **g), dose)
    cell("Horizon 6 months (NW 6)", Spec(h=6, lags=6, **g), dose)
    cell("No controls", Spec(h=12, lags=12, ctrl=(), **g), dose)
    cell("Without rv", Spec(h=12, lags=12, ctrl=("c12", "c1"), **g), dose)
    c_ret = {m: v for m, v in parse_ipo(rows, "C").items() if m <= LAST}
    cell("Dose from first-day return (col C)", spec, heat(c_ret, mean=True))
    cell("Rows 1991-01 .. 2007-12", Spec(h=12, lags=12, first=ROW_FIRST, last=HALF - 1), dose)
    cell("Rows 2008-01 .. 2024-09", Spec(h=12, lags=12, first=HALF, last=ROW_LAST), dose)
    cell("Without rows 1998-01 .. 2001-12", Spec(h=12, lags=12, drop=DOTCOM, **g), dose)
    rep = None
    if ok:
        rsp = Spec(h=12, lags=12, first=REP_FIRST, last=REP_LAST)
        rrows = {m: r for m, r in build(mkt, daily, rsp).items() if m in dose}
        rb, rt, rn = fit(rrows, dose, rsp)
        rr = neg_rank(rt, [fit(rrows, s, rsp)[1] for s in sur])
        rep = (rb, rt, rn, rr, rb < 0 and rt <= -2 and rr <= 2)
    ns, nu = null_stats(ts_shift), null_stats(ts_surr)
    lines = [
        "# W46 `ipo-heat`: results",
        "",
        "Card: `research/cards/wide-29.md`. Code: `research/lib/wide29.py`. One real run.",
        "",
        f"- IPO months {ym(min(n))} .. {ym(max(n))}; dose defined {ym(full[0])} .. "
        f"{ym(full[-1])} ({len(full)} months), SD {dv.std(ddof=1):.3f}; gate rows {nn}.",
        f"- Lag-1 acf {acf:.3f}; |end - start| / SD {endgap:.2f}; surrogates `{family}`, "
        f"gating: {gating_surr}.",
        f"- **Gate: b {b:+.3f} % per unit of H over 12 months, t {t:+.2f}; rank of -t "
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
    lines += ["", "R46: " + ("not run (the gate failed)" if rep is None else str(rep))]
    text = "\n".join(lines) + "\n"
    (RESULTS / "ipo-heat.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
