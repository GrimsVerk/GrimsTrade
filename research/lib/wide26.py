"""Lane wide-26: gate W43 `drought-food-margin` (research/cards/wide-26.md; rule pushed
before this script's first run).

Descriptive only: no strategy, no backtest. Nothing after 2025-10 is read. Cached files only
(nClimDiv PDSI from parked-gates-1, Ken French files); run with `python -I`.

Run:  `uv run python -I research/lib/wide26.py`  (DRY=1: counts only)
Output: research/results/drought-food-margin.md
"""

from __future__ import annotations

import math
import os
import sys
import zipfile
from collections.abc import Mapping
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import gatenull2 as g2  # noqa: E402
import parkedgates1_events as pe  # noqa: E402
import wide17_events as e17  # noqa: E402
import wide26_events as ev  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = 2025 * 12 + 9  # 2025-10: nothing later is read
PDSI_FILE = "parked-gates-1/climdiv/2026-11-25/climdiv-pdsist-v1.0.0-20261105"
IND_FILE = "wide-26/french/2026-11-25/49_Industry_Portfolios_CSV.zip"
FAC_FILE = "french/2026-11-12/F-F_Research_Data_Factors_CSV.zip"
GATE = (1960 * 12, 2025 * 12 + 6)  # dose months 1960-01 .. 2025-07
REPL = (1931 * 12 + 4, 1959 * 12 + 9)  # R43: 1931-05 .. 1959-10 (card's 06 / 09 off by one)
POST = 2016 * 12  # after Hong, Li and Xu's sample
VW = "Average Value Weighted Returns -- Monthly"
EW = "Average Equal Weighted Returns -- Monthly"


def _zip_text(rel: str) -> str:
    z = zipfile.ZipFile(dw.cache_root() / rel)
    return z.read(z.namelist()[0]).decode("latin1")


def _pdsi(code: str) -> dict[int, float]:
    from datetime import date

    text = (dw.cache_root() / PDSI_FILE).read_text()
    return pe.parse_pdsi(text, date(2025, 10, 31), code)


def load() -> dict[str, object]:
    fac = ev.parse_factors(_zip_text(FAC_FILE), LAST)
    mkt = {m: v[0] for m, v in fac.items()}
    rf = {m: v[1] for m, v in fac.items()}
    ind = _zip_text(IND_FILE)
    out: dict[str, object] = {"mkt": mkt}
    for title, tag in ((VW, "vw"), (EW, "ew")):
        names, rows = ev.parse_block(ind, title, LAST)
        for col in ("Food", "Meals", "Agric"):
            j = names.index(col)
            out[f"{col}_{tag}"] = {
                m: v[j] - rf[m] for m, v in rows.items() if m in rf and not math.isnan(v[j])
            }
    out["d361"] = pe.drought_dose(_pdsi(ev.CORN_BELT))
    out["d110"] = pe.drought_dose(_pdsi(ev.NATIONAL))
    return out


def months(span: tuple[int, int]) -> list[int]:
    return list(range(span[0], span[1] + 1))


def ys(
    ex: Mapping[int, float], mkt: Mapping[int, float], span: tuple[int, int], **kw: object
) -> dict[int, float]:
    out = {}
    for m in months(span):
        v = ev.outcome(ex, mkt, m, **kw)  # type: ignore[arg-type]
        last_j = m + int(kw.get("first", 2)) + int(kw.get("length", 3)) - 1  # type: ignore[call-overload]
        if not math.isnan(v) and last_j <= LAST:
            out[m] = v
    return out


def placebo_ts(
    y: Mapping[int, float], dose: Mapping[int, float], span: tuple[int, int], lags: int
) -> tuple[list[float], list[float]]:
    """t of the 40 shifted calendars and of the 40 phase surrogates (seed 26)."""
    ms = months(span)
    sh = [ev.regress(ms, y, ev.shift_dose(dose, k), lags)[1] for k in e17.SHIFTS_W29]
    full = sorted(dose)
    if full != list(range(full[0], full[-1] + 1)):
        raise ValueError("dose has gaps; surrogates need a full series")
    x = np.array([dose[m] for m in full])
    sur = g2.phase_surrogates(np.random.default_rng(ev.SEED), x, 40)
    su = [ev.regress(ms, y, dict(zip(full, sur[:, i], strict=True)), lags)[1] for i in range(40)]
    return sh, su


def fmt_null(ts: list[float]) -> str:
    sd, share, q5, q50, q95, lo, hi = ev.null_spread(ts)
    return (
        f"SD {sd:.2f}, {share:.0%} past |t| 2, 5/50/95% {q5:+.2f} / {q50:+.2f} / {q95:+.2f}, "
        f"extremes {lo:+.2f} / {hi:+.2f}"
    )


def gate(
    data: dict[str, object], span: tuple[int, int], label: str
) -> tuple[list[str], bool, dict[str, float]]:
    mkt: dict[int, float] = data["mkt"]  # type: ignore[assignment]
    dose: dict[int, float] = data["d361"]  # type: ignore[assignment]
    y = ys(data["Food_vw"], mkt, span)  # type: ignore[arg-type]
    b, t, n = ev.regress(months(span), y, dose, 3)
    sh, su = placebo_ts(y, dose, span, 3)
    r_sh, r_su = ev.rank_lowest(t, sh), ev.rank_lowest(t, su)
    a1 = ev.acf1(dose)
    both = a1 >= 0.8
    ok = b < 0 and t <= -2 and r_sh <= 2 and (r_su <= 2 or not both)
    lines = [
        f"### {label}",
        "",
        f"- b {b:+.3f}% per PDSI unit, Newey-West t {t:+.2f}, {n} dose months.",
        f"- Shifted calendars: rank {r_sh} of 41 (lowest = 1); null {fmt_null(sh)}.",
        f"- Phase surrogates (seed 26): rank {r_su} of 41; null {fmt_null(su)}.",
        f"- Dose lag-1 autocorrelation (1895-2025): {a1:.3f}; 'both families' rule "
        f"{'applies' if both else 'does not apply'}.",
        f"- **Verdict: {'PASS (kill-only)' if ok else 'FAIL'}.**",
        "",
    ]
    return lines, ok, {"b": b, "t": t, "n": n, "r_sh": r_sh, "r_su": r_su, "acf": a1}


def cells(data: dict[str, object]) -> list[tuple[str, float, float, int]]:
    mkt: dict[int, float] = data["mkt"]  # type: ignore[assignment]
    d361: dict[int, float] = data["d361"]  # type: ignore[assignment]
    d110: dict[int, float] = data["d110"]  # type: ignore[assignment]
    food: dict[int, float] = data["Food_vw"]  # type: ignore[assignment]
    ms = months(GATE)
    base = ys(food, mkt, GATE)
    out: list[tuple[str, float, float, int]] = []

    def add(name: str, y: Mapping[int, float], dose: Mapping[int, float], lags: int = 3,
            rows: list[int] | None = None) -> None:  # fmt: skip
        b, t, n = ev.regress(rows or ms, y, dose, lags)
        out.append((name, b, t, n))

    add("Raw Food minus market (no beta)", ys(food, mkt, GATE, adjust="raw"), d361)
    add("W32's dose: contiguous-US PDSI (code 110)", base, d110)
    pd361 = {m: -v for m, v in d361.items()}
    add("Drying: PDSI(m-3) - PDSI(m), Corn Belt", base, ev.drying(pd361))
    add("12-month horizon (m+2 .. m+13), NW 12", ys(food, mkt, GATE, length=12), d361, 12)
    add("Growing-season dose months only (Jun-Sep)", base, d361,
        rows=[m for m in ms if m % 12 in (5, 6, 7, 8)])  # fmt: skip
    add("Restaurants (Meals), beta-adjusted", ys(data["Meals_vw"], mkt, GATE), d361)  # type: ignore[arg-type]
    add("Farms (Agric), beta-adjusted, no sign predicted", ys(data["Agric_vw"], mkt, GATE), d361)  # type: ignore[arg-type]
    add("Equal-weighted Food, beta-adjusted", ys(data["Food_ew"], mkt, GATE), d361)  # type: ignore[arg-type]
    add("The market itself (Mkt-RF, m+2 .. m+4)", ys(mkt, mkt, GATE, adjust="none"), d361)
    add("After Hong-Li-Xu: dose months 2016-01 on", base, d361,
        rows=[m for m in ms if m >= POST])  # fmt: skip
    return out


def ym(m: int) -> str:
    return f"{m // 12}-{m % 12 + 1:02d}"


def main() -> None:
    data = load()
    d361: dict[int, float] = data["d361"]  # type: ignore[assignment]
    mkt: dict[int, float] = data["mkt"]  # type: ignore[assignment]
    y = ys(data["Food_vw"], mkt, GATE)  # type: ignore[arg-type]
    yr = ys(data["Food_vw"], mkt, REPL)  # type: ignore[arg-type]
    print(f"dose 361 months {ym(min(d361))} .. {ym(max(d361))}: {len(d361)}")
    print(f"gate rows {len([m for m in months(GATE) if m in y and m in d361])}, "
          f"first {ym(min(y))}, last {ym(max(y))}")  # fmt: skip
    print(f"R43 rows {len([m for m in months(REPL) if m in yr and m in d361])}")
    print(f"dose acf1 1895-2025: {ev.acf1(d361):.3f}")
    gm = [m for m in months(GATE) if m in y]
    dz = np.array([d361[m] for m in gm])
    print(f"gate-row dose: SD {dz.std(ddof=1):.2f}, months with D >= 2 (PDSI <= -2): "
          f"{int((dz >= 2).sum())}, D >= 4: {int((dz >= 4).sum())}")  # fmt: skip
    if DRY:
        return
    lines, ok, res = gate(
        data,
        GATE,
        "W43 gate (dose months 1960-01 .. 2025-07; rows end 2025-06, whose outcome ends 2025-10)",
    )
    print("\n".join(lines))
    rep: list[str] = []
    if ok:
        rep, _, _ = gate(data, REPL, "R43 replication (dose months 1931-05 .. 1959-10)")
        print("\n".join(rep))
    cl = cells(data)
    for c in cl:
        print(f"{c[0]}: b {c[1]:+.3f} t {c[2]:+.2f} n {c[3]}")
    top = sorted(gm, key=lambda m: -d361[m])[:10]
    post = [m for m in months(GATE) if m >= POST]
    pb, pt, pn = ev.regress(post, y, d361, 3)
    psh, psu = placebo_ts(y, d361, (POST, GATE[1]), 3)
    post_lines = [
        "## Post-2016 cell through both placebo families (shown, not gating)",
        "",
        "Added after the main run because the post-sample cell's t crossed 2 (gate-null step 6);",
        "the first numbers came from an ad hoc call with the same functions, reproduced here.",
        "",
        f"- b {pb:+.3f}% per unit, t {pt:+.2f}, {pn} dose months (2016-01 .. 2025-06).",
        f"- Shifted calendars: rank {ev.rank_lowest(pt, psh)} of 41; null {fmt_null(psh)}.",
        f"- Phase surrogates: rank {ev.rank_lowest(pt, psu)} of 41; null {fmt_null(psu)}.",
        "- All 14 of its months at PDSI <= -2 lie in 2022-10 .. 2024-03: one drought episode.",
        "",
    ]
    out = [
        "# W43 `drought-food-margin`: results",
        "",
        "Rule: [`cards/wide-26.md`](../cards/wide-26.md) (pushed before any number). Code:",
        "`research/lib/wide26.py`, `research/lib/wide26_events.py`. Outcome: French 49-industry",
        "value-weighted Food minus its 60-month beta times Mkt-RF, summed over months m+2..m+4,",
        "percent; dose D = -PDSI of the Corn Belt (nClimDiv 361) in month m.",
        "",
        "Vintage caveat: the PDSI is today's nClimDiv vintage (2026-11-05), recomputed each month;",
        "real-time vintages were not used (as in W32). The fail does not depend on it; any future",
        "pass of this design would need a real-time vintage check before it is read.",
        "",
        *lines,
        *(rep or ["R43 not run (the card runs it only after a pass).", ""]),
        "## Shown cells (not gating; beta-adjusted Food, NW 3, gate rows, unless named)",
        "",
        "| Cell | b, % per unit | t | Rows |",
        "|---|---:|---:|---:|",
        f"| **Gate** | **{res['b']:+.3f}** | **{res['t']:+.2f}** | **{int(res['n'])}** |",
        *[f"| {c[0]} | {c[1]:+.3f} | {c[2]:+.2f} | {c[3]} |" for c in cl],
        "",
        *post_lines,
        "## The ten driest dose months in the gate rows",
        "",
        "| Dose month | D (-PDSI) | y, % |",
        "|---|---:|---:|",
        *[f"| {ym(m)} | {d361[m]:+.2f} | {y[m]:+.2f} |" for m in top],
        "",
    ]
    (RESULTS / "drought-food-margin.md").write_text("\n".join(out))
    print("wrote results/drought-food-margin.md")


if __name__ == "__main__":
    main()
