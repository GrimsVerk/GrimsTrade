"""fx-value-real-1: currency value with the real exchange rate, alone and in #170's book.

    uv run python -I research/lib/fx_value_real_run.py

Card: research/cards/fx-value-real-1.md. Reuses #170's code (`xs_century`, `xs_century_run`)
unchanged except the currency-value signal (passed to `build(fx_value=...)`). Reads only the
cache; nothing after 2025-10-31. Writes research/results/fx-value-real-1.md (statistics only)
and appends rows to research/tries.md the moment the run is scored.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Mapping
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / "src"))
import long_macro_build as lmb  # noqa: E402
import xs_century as xc  # noqa: E402
import xs_century_run as xr  # noqa: E402

IDEA = "fx-value-real-1"
RESULT = REPO / "research" / "results" / "fx-value-real-1.md"
TRIES = REPO / "research" / "tries.md"
LAG = xr.FX_SPOT_LAG  # 2, as #170's spot (the real rate is dated by its spot month)
SPOT_FROM = xr.add(xr.FX_FLOAT, -1)  # #170's spot window starts 1973-02
BAR, ONC = 4.70, 3.25

M = dict[date, float]


def point_value(lnq: Mapping[date, float], t: date, lag: int) -> float | None:
    """S3: -(ln q(L) - ln q(L-60)), L = t - lag: the plain 5-year fall of the real rate."""
    a, b = lnq.get(xc.add_months(t, -lag)), lnq.get(xc.add_months(t, -lag - 60))
    return None if a is None or b is None else b - a


def real_rates() -> dict[str, M]:
    """ln q per currency, CPI as known at the spot's month end, #170's spot window."""
    out: dict[str, M] = {}
    for cur in xr.lb.FX_LINES:
        out[cur] = {
            d: v for d, v in lmb.real_fx_series(cur) if SPOT_FROM <= d <= xr.LAST
        }  # fmt: skip
    return out


def sleeve(fr: dict[str, M], fn: xr.Sig, cost: float, gross: bool = False) -> M:
    return xr.net(xc.constructed_sleeve(xr.signals(fr, fn), fr, cost), gross)


def spearman(a: Mapping[str, float], b: Mapping[str, float]) -> float | None:
    ks = sorted(set(a) & set(b))
    if len(ks) < xc.MIN_ASSETS:
        return None
    ra = np.argsort(np.argsort([a[k] for k in ks])).astype(float)
    rb = np.argsort(np.argsort([b[k] for k in ks])).astype(float)
    if ra.std() == 0 or rb.std() == 0:
        return None
    return float(np.corrcoef(ra, rb)[0, 1])


def tries_row(variant: str, kind: str, ms: np.ndarray, r: np.ndarray, now: str) -> str:
    tot, dd = xr.total_dd(r)
    sr = float(r.mean() / r.std(ddof=1)) * math.sqrt(12)
    to = date(ms[-1].year + ms[-1].month // 12, ms[-1].month % 12 + 1, 1) - timedelta(days=1)
    return (f"| {now} | {IDEA} | {variant} | {kind} | train | {ms[0].isoformat()} | "
            f"{to.isoformat()} | {sr:.2f} | {tot * 100:+.1f}% | {dd * 100:.1f}% | - |")  # fmt: skip


def verdict(z: float, both: bool) -> str:
    return "PASS (informational)" if z >= BAR and both else "NEAR" if z >= ONC else "FAIL"


def main() -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    mkt_rf, rf, hml, umd = xr.us_stocks()
    fxd = xr.currencies()
    data: dict[str, object] = {"hml": hml, "umd": umd, "bonds": xr.bonds(), "fx": fxd}
    fr, spot, _, _ = fxd
    lnq = real_rates()
    q = {c: {d: math.exp(v) for d, v in s.items()} for c, s in lnq.items()}
    tm = xr.tsmom_market(mkt_rf, rf)
    six = xr.tsmom_six(rf)
    c1 = xr.COST["fx"]

    def real(a: str, t: date) -> float | None:
        return xc.reversal_value(q[a], t, LAG)

    def proxy(a: str, t: date) -> float | None:
        return xc.reversal_value(spot[a], t, LAG)

    def p2p(a: str, t: date) -> float | None:
        return point_value(lnq[a], t, LAG)

    # check: #170's primary book through the unchanged default path (must give z 2.75)
    check = xc.score(*xr.aligned(xr.build(data)[0], tm)[:2])

    sl = sleeve(fr, real, c1)
    post = date(1994, 1, 1)
    runs: dict[str, tuple[str, str, M, M, date | None]] = {
        "sleeve": ("sleeve real-rate value (primary 1)", "variant", sl, tm, None),
        "book": ("book with real-rate FX value (primary 2)", "variant",
                 xr.build(data, fx_value=real)[0], tm, None),
        "S1": ("S1 sleeve gross", "robustness", sleeve(fr, real, 0.0, gross=True), tm, None),
        "S2": ("S2 sleeve FX cost x2", "robustness", sleeve(fr, real, 2 * c1), tm, None),
        "S3": ("S3 sleeve point-to-point 60m", "robustness", sleeve(fr, p2p, c1), tm, None),
        "S4": ("S4 sleeve 1994-01..2025-10", "robustness", sl, tm, post),
        "S5": ("S5 sleeve vs six-asset tsmom12", "robustness", sl, six, None),
        "B1": ("B1 book gross", "robustness",
               xr.build(data, gross=True, fx_value=real)[0], tm, None),
        "B2": ("B2 book UMD cost 0.34%/mo", "robustness",
               xr.build(data, umd_cost=xr.UMD_C_MIT, fx_value=real)[0], tm, None),
        "B3": ("B3 bonds + FX only", "robustness",
               xr.build(data, with_us=False, fx_value=real)[0], tm, None),
        "C1": ("C1 proxy sleeve (spot reversal, #170)", "control", sleeve(fr, proxy, c1), tm,
               None),
    }  # fmt: skip
    scores = {}
    for key, (_, _, b, t, lo) in runs.items():
        r, x, ms = xr.aligned(b, t, lo)
        scores[key] = (xc.score(r, x), ms, r, x)

    # halves
    _, ms_s, _, _ = scores["sleeve"]
    mid = ms_s[len(ms_s) // 2]
    halves: dict[str, dict[str, tuple[dict[str, float], int]]] = {"sleeve": {}, "book": {}}
    for nm, lo, hi in [(f"{ms_s[0]:%Y-%m}..{xr.add(mid, -1):%Y-%m}", None, mid),
                       (f"{mid:%Y-%m}..2025-10", mid, None)]:  # fmt: skip
        r, x, ms = xr.aligned(sl, tm, lo, hi)
        halves["sleeve"][nm] = (xc.alpha(r, x), len(r))
    for nm, lo, hi in [("1928..1972", None, xr.HALF), ("1973..2025", xr.HALF, None)]:
        r, x, ms = xr.aligned(runs["book"][2], tm, lo, hi)
        halves["book"][nm] = (xc.alpha(r, x), len(r))
    both = {k: all(a["a"] > 0 for a, _ in v.values()) for k, v in halves.items()}
    vs = {k: verdict(scores[k][0]["z"], both[k]) for k in ("sleeve", "book")}

    # tries rows first (the moment the run is scored)
    rows = []
    for key, (label, kind, *_rest) in runs.items():
        s, ms, r, _ = scores[key]
        v = (f"{label}: alpha vs tsmom12 IR {s['ir']:+.2f} z {s['z']:+.2f} "
             f"(monthly excess x sqrt12)")  # fmt: skip
        rows.append(tries_row(v, kind, ms, r, now))
    with TRIES.open("a") as fh:
        fh.write("\n".join(rows) + "\n")

    # diagnostics
    corr_by: dict[str, list[float]] = {}
    for t in sorted(sl):
        a = {c: v for c in fr if (v := real(c, t)) is not None and t in fr[c]}
        b = {c: v for c in fr if (v := proxy(c, t)) is not None and t in fr[c]}
        rc = spearman(a, b)
        if rc is not None:
            corr_by.setdefault(f"{t.year // 10 * 10}s", []).append(rc)
            corr_by.setdefault("all", []).append(rc)
    r_real, r_proxy, _ = xr.aligned(sl, runs["C1"][2])
    ret_corr = float(np.corrcoef(r_real, r_proxy)[0, 1])

    L: list[str] = []
    L.append("# fx-value-real-1 results (generated by research/lib/fx_value_real_run.py)\n")
    L.append(f"Run {now} UTC. Card: `research/cards/fx-value-real-1.md`. Monthly, excess "
             "returns. Statistics only.\n")  # fmt: skip
    s0, s1 = scores["sleeve"][0], scores["book"][0]
    L.append(f"**Verdicts (card's rules): sleeve {vs['sleeve']}** (z {s0['z']:.2f}, IR "
             f"{s0['ir']:+.2f}; alpha > 0 in both halves: {'yes' if both['sleeve'] else 'no'}); "
             f"**book {vs['book']}** (z {s1['z']:.2f}, IR {s1['ir']:+.2f}; both halves "
             f"{'yes' if both['book'] else 'no'}). Bar 4.70, ONC end 3.25.\n")  # fmt: skip
    L.append(f"Check: #170's primary book through the unchanged default path: z {check['z']:.2f} "
             f"(#170: 2.75), IR {check['ir']:+.2f} (#170: +0.31).\n")  # fmt: skip
    L.append("## Alpha against the `tsmom12` proxy\n")
    L.append("| Run | Kind | Months | From | Years | Sharpe | Vol | rho | alpha %/yr | IR | "
             "NW z | boot z | z (decides) | mix gain |")  # fmt: skip
    L.append("|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for key, (label, kind, *_rest) in runs.items():
        s, ms, _, _ = scores[key]
        L.append(
            f"| {label} | {kind} | {s['n']} | {ms[0]:%Y-%m} | {s['years']:.1f} | "
            f"{s['sr_r']:.2f} | {s['vol_r'] * 100:.1f}% | {s['rho']:+.2f} | "
            f"{s['a'] * 1200:+.2f} | {s['ir']:+.2f} | {s['z_nw']:.2f} | {s['z_boot']:.2f} | "
            f"**{s['z']:.2f}** | {s['mix_gain']:+.3f} |"
        )
    L.append("\n## Halves (NW only)\n")
    L.append("| Primary | Half | Months | alpha %/yr | IR | NW z |")
    L.append("|---|---|---:|---:|---:|---:|")
    for k, hv in halves.items():
        for nm, (a, n) in hv.items():
            L.append(f"| {k} | {nm} | {n} | {a['a'] * 1200:+.2f} | {a['ir']:+.2f} | "
                     f"{a['z_nw']:.2f} |")  # fmt: skip
    L.append("\n## Diagnostics (not tries)\n")
    L.append("Rank correlation (Spearman, per month, then averaged) of the real-rate and proxy "
             "signals over the sleeve's months; and correlation of the two sleeves' monthly "
             "net returns.\n")  # fmt: skip
    L.append("| Period | Months | Mean rank corr | Min |")
    L.append("|---|---:|---:|---:|")
    for k in ["all"] + sorted(x for x in corr_by if x != "all"):
        v = corr_by[k]
        L.append(f"| {k} | {len(v)} | {np.mean(v):+.2f} | {min(v):+.2f} |")
    L.append(f"\nSleeve return correlation, real vs proxy: {ret_corr:+.2f} "
             f"({len(r_real)} common months).\n")  # fmt: skip
    L.append("## Sleeves by decade (net Sharpe)\n")
    L.append("| Decade | Real-rate sleeve | Proxy sleeve |")
    L.append("|---|---:|---:|")
    for dec in range(1980, 2030, 10):
        cells = []
        for b in (sl, runs["C1"][2]):
            r, _, _ = xr.aligned(b, tm, date(dec, 1, 1), date(dec + 10, 1, 1))
            cells.append(f"{r.mean() / r.std(ddof=1) * math.sqrt(12):.2f}" if len(r) >= 24
                         else "-")  # fmt: skip
        L.append(f"| {dec}s | {cells[0]} | {cells[1]} |")
    RESULT.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
