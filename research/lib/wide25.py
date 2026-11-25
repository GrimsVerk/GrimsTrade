"""Lane wide-25: gate W41 `cabinet-collapse` and replication R41 (research/cards/wide-25.md;
rule pushed before this script's first run).

Descriptive only: no strategy, no backtest. Nothing after 2025-10 is used. The cached files
(ParlGov `view_cabinet.csv`, Ken French international country returns, JST R6) are untrusted
downloads: run with `python -I`.

Gate W41:     `uv run python -I research/lib/wide25.py`      (DRY=1: counts only)
Replication:  `uv run python -I research/lib/wide25.py r41`  (only after a W41 pass)
Output: research/results/cabinet-collapse.md (and cabinet-collapse-r41.md)

The pure functions (parsing, events, dose, design, statistic) are tested offline in
tests/test_wide25.py.
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
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gatepower as gp  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
PARLGOV = "wide-25/parlgov/2026-11-25/view_cabinet.csv"
FRENCH_INTL = "data-long-4/french/2026-11-24/F-F_International_Countries.zip"

DOSED = {
    "AUS": "Austrlia.Dat", "AUT": "Austria.Dat", "BEL": "Belgium.Dat", "CAN": "Canada.Dat",
    "CHE": "Swtzrlnd.Dat", "DEU": "Germany.Dat", "DNK": "Denmark.Dat", "ESP": "Spain.Dat",
    "FIN": "Finland.Dat", "FRA": "France.Dat", "GBR": "UK.Dat", "IRL": "Ireland.Dat",
    "ITA": "Italy.Dat", "JPN": "Japan.Dat", "NLD": "Nethrlnd.Dat", "NOR": "Norway.Dat",
    "NZL": "NewZland.Dat", "SWE": "Sweden.Dat",
}  # fmt: skip
OTHERS = {"HKG": "HongKong.Dat", "SGP": "Singapor.Dat", "MYS": "Malaysia.Dat"}

H = 6
LAGS = 6
SHIFTS = tuple(range(25, 104, 2))  # 40 earlier-dose calendars, k months
N_SURR = 40
SEED = 2511


def mi(y: int, m: int) -> int:
    """Month index y * 12 + m - 1."""
    return y * 12 + m - 1


def ym(k: int) -> str:
    return f"{k // 12}-{k % 12 + 1:02d}"


FIRST_ROW = mi(1976, 1)
DOSE_END = mi(2022, 12)
LAST = mi(2025, 10)
POST_BL = mi(2001, 1)


# --- parsing ---


def parse_block(text: str, block: int = 0, last: int = LAST) -> dict[int, float]:
    """{month index: decimal return} from the `block`-th monthly block (0-based) of a French
    country file, column 1 (`Mkt`); values <= -99 are missing; months after `last` dropped."""
    out: dict[int, float] = {}
    n = -1
    inside = False
    for line in text.splitlines():
        p = line.split()
        is_month = bool(p) and len(p[0]) == 6 and p[0].isdigit()
        if is_month and not inside:
            n += 1
            inside = True
        elif not is_month:
            inside = False
        if is_month and n == block:
            k = mi(int(p[0][:4]), int(p[0][4:]))
            v = float(p[1])
            if v > -99.0 and k <= last:
                out[k] = v / 100.0
        if n > block:
            break
    return out


@dataclass(frozen=True)
class Cabinet:
    cid: str
    country: str
    start: date
    election: str
    prev: str
    caretaker: bool


def parse_cabinets(rows: Iterable[Mapping[str, str]]) -> dict[str, Cabinet]:
    """One Cabinet per `cabinet_id` (the file has one row per cabinet party)."""
    out: dict[str, Cabinet] = {}
    for r in rows:
        cid = r["cabinet_id"]
        if cid in out or not r["start_date"]:
            continue
        out[cid] = Cabinet(
            cid=cid,
            country=r["country_name_short"],
            start=date.fromisoformat(r["start_date"]),
            election=r["election_date"],
            prev=r["previous_cabinet_id"] or "",
            caretaker=r["caretaker"] == "1",
        )
    return out


def events(cabs: Mapping[str, Cabinet]) -> list[Cabinet]:
    """Mid-term cabinet starts: the previous cabinet exists and has the same election date."""
    out = [
        c
        for c in cabs.values()
        if c.prev in cabs and c.election and cabs[c.prev].election == c.election
    ]
    return sorted(out, key=lambda c: (c.country, c.start))


def post_election(c: Cabinet, cabs: Mapping[str, Cabinet]) -> bool:
    """The event follows a caretaker cabinet that ParlGov starts on its own election day: a
    government formed after an election, not a mid-term change."""
    p = cabs[c.prev]
    return p.caretaker and p.start.isoformat() == p.election


def first_start(cabs: Mapping[str, Cabinet]) -> dict[str, int]:
    out: dict[str, int] = {}
    for c in cabs.values():
        k = mi(c.start.year, c.start.month)
        out[c.country] = min(out.get(c.country, k), k)
    return out


Dose = dict[str, dict[int, float]]  # country -> month index -> dose (defined months only)
Row = tuple[str, int, float, float, float, float]  # (country, m, y, c1, c3, c12)


def dose_months(
    evs: Sequence[Cabinet],
    first: Mapping[str, int],
    countries: Sequence[str],
    end: int = DOSE_END,
    count: bool = False,
) -> Dose:
    """D(i, m) over i's defined months (first ParlGov start .. end): 1 (or the number of
    events, `count`) in a month with an event, else 0."""
    out: Dose = {}
    for i in countries:
        if i not in first:
            continue
        d = dict.fromkeys(range(first[i], end + 1), 0.0)
        for c in evs:
            if c.country == i:
                k = mi(c.start.year, c.start.month)
                if k in d:
                    d[k] = d[k] + 1.0 if count else 1.0
        out[i] = d
    return out


def excess(rets: Mapping[str, Mapping[int, float]]) -> dict[str, dict[int, float]]:
    """e(i, m) = ln(1 + r_i) - mean over the other markets with a value in m of ln(1 + r_j)."""
    lg = {c: {k: math.log1p(v) for k, v in s.items()} for c, s in rets.items()}
    months = sorted({k for s in lg.values() for k in s})
    out: dict[str, dict[int, float]] = {c: {} for c in lg}
    for k in months:
        have = [(c, s[k]) for c, s in lg.items() if k in s]
        if len(have) < 2:
            continue
        tot = sum(v for _, v in have)
        for c, v in have:
            out[c][k] = v - (tot - v) / (len(have) - 1)
    return out


# --- the statistic ---


def wsum(e: Mapping[int, float], a: int, b: int) -> float:
    """Sum of e over months a..b (inclusive); NaN if any is missing."""
    tot = 0.0
    for k in range(a, b + 1):
        if k not in e:
            return math.nan
        tot += e[k]
    return tot


@dataclass(frozen=True)
class Spec:
    h: int = H
    lags: int = LAGS
    controls: bool = True
    reaction: bool = False  # y = e(m-1) + e(m), no controls (overrides h and controls)
    first_row: int = FIRST_ROW
    last_dose: int = DOSE_END
    drop: frozenset[str] = frozenset()


def base_rows(e: Mapping[str, Mapping[int, float]], dose: Dose, spec: Spec) -> list[Row]:
    """(country, m, y, c1, c3, c12) for the rows of the card: D(i, m) defined, m in
    [first_row, last_dose], every e(i, m-11 .. m+h) present (reaction: e(m-1), e(m))."""
    out = []
    for i in sorted(dose):
        if i in spec.drop or i not in e:
            continue
        ei = e[i]
        for m in sorted(dose[i]):
            if not spec.first_row <= m <= spec.last_dose:
                continue
            if spec.reaction:
                y = wsum(ei, m - 1, m)
                c1 = c3 = c12 = 0.0
            else:
                y = wsum(ei, m + 1, m + spec.h)
                c12 = wsum(ei, m - 11, m)
                c1 = ei.get(m, math.nan)
                c3 = wsum(ei, m - 2, m)
            if any(math.isnan(v) for v in (y, c1, c3, c12)):
                continue
            out.append((i, m, y, c1, c3, c12))
    return out


def fit(rows: Sequence[Row], dose: Dose, spec: Spec, shift: int = 0) -> tuple[float, float, int]:
    """(b in % over the outcome window per unit of dose, Driscoll-Kraay t, rows) of
    100 y ~ D(i, m - shift) + controls + country dummies; rows whose shifted dose is undefined
    are dropped."""
    keep = [r for r in rows if r[1] - shift in dose[r[0]]]
    if len(keep) < 10:
        return math.nan, math.nan, len(keep)
    cs = sorted({r[0] for r in keep})
    ci = {c: j for j, c in enumerate(cs)}
    nc = 4 if (spec.controls and not spec.reaction) else 1
    x = np.zeros((len(keep), nc + len(cs)))
    y = np.empty(len(keep))
    per = np.empty(len(keep), dtype=int)
    for n, (i, m, yy, c1, c3, c12) in enumerate(keep):
        x[n, 0] = dose[i][m - shift]
        if nc == 4:
            x[n, 1:4] = (c1, c3, c12)
        x[n, nc + ci[i]] = 1.0
        y[n] = 100.0 * yy
        per[n] = m
    b, t = gp.dk_fit(x, y, per, spec.lags, 0)
    return b, t, len(keep)


def surrogate(dose: Dose, rows: Sequence[Row], rng: np.random.Generator) -> Dose:
    """Each country's event months (dose > 0 among its row months) moved to months drawn
    uniformly without replacement from its own row months; same doses."""
    out: Dose = {}
    by: dict[str, list[int]] = {}
    for r in rows:
        by.setdefault(r[0], []).append(r[1])
    for i, ms in by.items():
        vals = [dose[i][m] for m in ms if dose[i][m] > 0]
        d = dict.fromkeys(ms, 0.0)
        for m, v in zip(rng.choice(ms, size=len(vals), replace=False), vals, strict=True):
            d[int(m)] = v
        out[i] = d
    return out


def null_stats(ts: Sequence[float]) -> dict[str, float]:
    a = np.array([t for t in ts if not math.isnan(t)])
    return {
        "n": float(len(a)),
        "sd": float(a.std(ddof=1)),
        "share2": float(np.mean(np.abs(a) >= 2)),
        "q05": float(np.quantile(a, 0.05)),
        "q50": float(np.quantile(a, 0.50)),
        "q95": float(np.quantile(a, 0.95)),
        "min": float(a.min()),
        "max": float(a.max()),
    }


def lag1_acf(dose: Dose, rows: Sequence[Row]) -> float:
    """Pooled lag-1 autocorrelation of D(i, m) over row months (pairs within a country)."""
    s = {(r[0], r[1]) for r in rows}
    a = [(dose[i][m], dose[i][m - 1]) for i, m in s if (i, m - 1) in s]
    v = np.array(a)
    return float(np.corrcoef(v[:, 0], v[:, 1])[0, 1])


# --- run ---


def cache() -> Path:
    import datawide1 as dw

    return dw.cache_root()


def load_rets(block: int = 0) -> dict[str, dict[int, float]]:
    with zipfile.ZipFile(cache() / FRENCH_INTL) as z:
        return {
            c: parse_block(z.read(f).decode("latin-1"), block)
            for c, f in {**DOSED, **OTHERS}.items()
        }


def load_cabs() -> dict[str, Cabinet]:
    text = (cache() / PARLGOV).read_text(encoding="utf-8")
    return parse_cabinets(csv.DictReader(io.StringIO(text)))


def fmt(v: float, d: int = 2) -> str:
    return "nan" if math.isnan(v) else f"{v:+.{d}f}"


def main() -> None:
    cabs = load_cabs()
    evs = events(cabs)
    first = first_start(cabs)
    countries = list(DOSED)
    dose = dose_months(evs, first, countries)
    e = excess(load_rets(0))
    spec = Spec()
    rows = base_rows(e, dose, spec)
    n_ev = sum(1 for r in rows if dose[r[0]][r[1]] > 0)
    lines = [f"# W41 `cabinet-collapse` (wide-25), run {datetime.now(UTC):%Y-%m-%d %H:%M} UTC", ""]
    lines.append("## Counts (dry run)")
    lines.append("")
    lines.append(
        "| Country | ParlGov first start | last start | events (all years) | event months in rows"
        " | rows |"
    )
    lines.append("|---|---|---|---:|---:|---:|")
    for i in countries:
        ce = [c for c in evs if c.country == i]
        last = max((c.start for c in cabs.values() if c.country == i), default=None)
        rr = [r for r in rows if r[0] == i]
        ne = sum(1 for r in rr if dose[i][r[1]] > 0)
        lines.append(f"| {i} | {ym(first[i])} | {last} | {len(ce)} | {ne} | {len(rr)} |")
    lines.append("")
    span = (ym(min(r[1] for r in rows)), ym(max(r[1] for r in rows)))
    care = sum(
        1
        for c in evs
        if c.country in DOSED
        and FIRST_ROW <= mi(c.start.year, c.start.month) <= DOSE_END
        and c.caretaker
    )  # noqa: E501
    tot = sum(
        1
        for c in evs
        if c.country in DOSED and FIRST_ROW <= mi(c.start.year, c.start.month) <= DOSE_END
    )  # noqa: E501
    lines.append(
        f"Rows {len(rows)} ({span[0]} .. {span[1]}), event months in rows {n_ev}; events "
        f"1976-01 .. 2022-12 in the 18 countries {tot} (caretaker {care}); pooled lag-1 "
        f"autocorrelation of the dose {lag1_acf(dose, rows):+.3f}."
    )
    lines.append("")
    if DRY:
        print("\n".join(lines))
        return

    b, t, n = fit(rows, dose, spec)
    pl = [fit(rows, dose, spec, k) for k in SHIFTS]
    pt = [p[1] for p in pl]
    rank = gp.rank_highest(t, pt)
    ok = gp.passes(b, t, pt)
    ns = null_stats(pt)
    rng = np.random.default_rng(SEED)
    st = [fit(rows, surrogate(dose, rows, rng), spec)[1] for _ in range(N_SURR)]
    ss = null_stats(st)
    srank = gp.rank_highest(t, st)

    lines.append("## Gate")
    lines.append("")
    lines.append(
        f"**b {fmt(b, 3)}% over six months per event month, DK t {fmt(t)}, rows {n}; rank "
        f"{rank} of {1 + len(pt)} earlier-dose calendars; gate {'PASS' if ok else 'FAIL'}.**"
    )
    lines.append("")
    lines.append(
        f"Earlier-dose null (k = 25..103 months, odd): SD {ns['sd']:.2f}, share |t| >= 2 "
        f"{ns['share2']:.0%}, 5/50/95% {ns['q05']:+.2f} / {ns['q50']:+.2f} / {ns['q95']:+.2f}, "
        f"extremes {ns['min']:+.2f} / {ns['max']:+.2f}."
    )
    lines.append(
        f"Random-month surrogates (shown, seed {SEED}): SD {ss['sd']:.2f}, share |t| >= 2 "
        f"{ss['share2']:.0%}, 5/50/95% {ss['q05']:+.2f} / {ss['q50']:+.2f} / {ss['q95']:+.2f}, "
        f"extremes {ss['min']:+.2f} / {ss['max']:+.2f}; rank of the true t {srank} of 41."
    )
    lines.append("")
    lines.append("| k (months) | b | t | rows |")
    lines.append("|---:|---:|---:|---:|")
    for k, p in zip(SHIFTS, pl, strict=True):
        lines.append(f"| {k} | {fmt(p[0], 3)} | {fmt(p[1])} | {p[2]} |")
    lines.append("")

    # shown cells
    cells: list[tuple[str, float, float, int]] = [("Gate", b, t, n)]
    sp = Spec(reaction=True, lags=2)
    cells.append(
        ("Reaction e(m-1) + e(m), no controls, DK 2", *fit(base_rows(e, dose, sp), dose, sp))
    )
    for hh in (3, 12):
        sp = Spec(h=hh, lags=hh)
        cells.append((f"Horizon {hh} months, DK {hh}", *fit(base_rows(e, dose, sp), dose, sp)))
    el = excess(load_rets(1))
    cells.append(("Local-currency returns", *fit(base_rows(el, dose, spec), dose, spec)))
    sp = Spec(drop=frozenset({"ITA", "JPN"}))
    cells.append(("Without Italy and Japan", *fit(base_rows(e, dose, sp), dose, sp)))
    sp = Spec(first_row=POST_BL)
    cells.append(("Rows m >= 2001-01", *fit(base_rows(e, dose, sp), dose, sp)))
    for lab, flag in (("Non-caretaker events only", False), ("Caretaker events only", True)):
        d2 = dose_months([c for c in evs if c.caretaker == flag], first, countries)
        cells.append((lab, *fit(rows, d2, spec)))
    # added after the card, before any number (dry-run finding, write-up step 3)
    d3 = dose_months([c for c in evs if not post_election(c, cabs)], first, countries)
    cells.append(
        (
            "Without post-election formations (previous = caretaker from election day)",
            *fit(rows, d3, spec),
        )
    )  # noqa: E501
    dc = dose_months(evs, first, countries, count=True)
    cells.append(("Count dose", *fit(rows, dc, spec)))
    sp = Spec(controls=False)
    cells.append(("No controls", *fit(rows, dose, sp)))
    lines.append("## Cells (gate first; the rest shown, not gating)")
    lines.append("")
    lines.append("| Cell | b, % per event month | t | rows |")
    lines.append("|---|---:|---:|---:|")
    for lab, bb, tt, nn in cells:
        lines.append(f"| {lab} | {fmt(bb, 3)} | {fmt(tt)} | {nn} |")
    lines.append("")
    out = "\n".join(lines) + "\n"
    (RESULTS / "cabinet-collapse.md").write_text(out)
    print(out)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "r41":
        raise SystemExit("R41 runs only after a W41 pass (card); not implemented until then")
    main()
