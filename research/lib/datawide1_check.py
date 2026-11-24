"""Lane data-wide-1, step 3: describe the verified downloads (counts, spans, gaps, lags).

Descriptive only: no price, no return, no correlation is read. Needs the files from
`scripts/fetch_datawide1.py` in the cache.

Run: `uv run --with xlrd python -I research/lib/datawide1_check.py`
Output: research/results/data-wide-1.md
"""

from __future__ import annotations

import csv
import io
import json
import sys
import zipfile
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "data-wide-1.md"
LINES: list[str] = []


def say(s: str = "") -> None:
    LINES.append(s)
    print(s, flush=True)


def longest_gap(days: list[date]) -> tuple[int, date | None, date | None]:
    best = (0, None, None)
    for a, b in zip(days, days[1:], strict=False):
        g = (b - a).days
        if g > best[0]:
            best = (g, a, b)
    return best


def per_decade(days: list[date]) -> str:
    c = Counter(d.year // 10 * 10 for d in days)
    return ", ".join(f"{k}s {c[k]}" for k in sorted(c))


def usgs() -> None:
    folder = dw.snapshot("usgs")
    files = sorted(folder.glob("*.csv"))
    qs = dw.load_quakes(folder)
    m6 = [q for q in qs if q.mag >= 6]
    m5 = [q for q in qs if q.mag >= 5 and q.time.year >= 1973]
    say("## 1. USGS ComCat earthquakes")
    say()
    say(f"Snapshot `{folder.name}`, {len(files)} files, {len(qs):,} distinct earthquake rows.")
    say(
        f"- M >= 6: {len(m6):,} events, {m6[0].time:%Y-%m-%d} .. {m6[-1].time:%Y-%m-%d}; "
        f"per decade: {per_decade([q.time.date() for q in m6])}."
    )
    yrs = Counter(q.time.year for q in m6)
    empty = [y for y in range(1900, 2026) if yrs[y] == 0]
    more = " ..." if len(empty) > 10 else ""
    say(f"- Years with no M >= 6 event: {len(empty)} ({empty[:10]}{more}).")
    g, a, b = longest_gap(sorted({q.time.date() for q in m6 if q.time.year >= 1973}))
    say(f"- Longest gap between M >= 6 days since 1973: {g} days ({a} .. {b}).")
    say(
        f"- M >= 5 since 1973: {len(m5):,} events; per decade: "
        f"{per_decade([q.time.date() for q in m5])}."
    )
    for t in (6.5, 7.0, 7.5, 8.0):
        n = sum(q.mag >= t and q.time.year >= 1973 for q in qs)
        say(f"- M >= {t} since 1973: {n} events.")
    late = sum((q.updated - q.time) > timedelta(days=30) for q in m6 if q.time.year >= 1973)
    n73 = sum(q.time.year >= 1973 for q in m6)
    say(
        f"- Revisions: {late} of {n73} M >= 6 rows since 1973 were last updated more than 30 "
        "days after the event (the catalogue holds reviewed magnitudes, not first estimates)."
    )
    types = Counter(q.mag_type for q in m6)
    say(f"- Magnitude types (M >= 6): {dict(types.most_common(6))}.")
    say("- Release: real time (minutes); no dated vintages, only the `updated` stamp.")
    say()


def gpr() -> None:
    folder = dw.snapshot("gpr")
    rows = dw.read_gpr_xls(folder / "data_gpr_daily_recent.xls")
    days = [r.day for r in rows]
    say("## 2. Geopolitical risk, daily (Caldara-Iacoviello)")
    say()
    say(f"Snapshot `{folder.name}`: {len(rows):,} daily rows, {days[0]} .. {days[-1]}.")
    full = (days[-1] - days[0]).days + 1
    say(
        f"- Calendar days in span {full:,}; missing {full - len(set(days))}; duplicate days "
        f"{len(days) - len(set(days))}; rows with no index value "
        f"{sum(r.gprd != r.gprd for r in rows)}."
    )
    zero = sum(r.articles == 0 for r in rows)
    say(f"- Days with 0 articles searched (N10D): {zero}.")
    say(
        f"- Weekday of the last row: {days[-1]:%A}; file posted 2026-11-17 18:00 UTC "
        "(Last-Modified header)."
    )
    say()
    say("Archived vintages (authors' GitHub): last day carried vs the vintage date, and revisions")
    say("against the current file on days both carry.")
    say()
    say(
        "| Vintage (file date) | Weekday | Last day carried | Lag, days | Days compared | "
        "Changed by > 0.5% | Median abs change |"
    )
    say("|---|---|---|---:|---:|---:|---:|")
    cur = {r.day: r.gprd for r in rows}
    vfolder = dw.snapshot("gprvint")
    for p in sorted(vfolder.glob("*.xls")):
        v = dw.read_gpr_xls(p)
        vd = datetime.strptime(p.stem, "%Y%m%d").date()
        both = [(r.gprd, cur[r.day]) for r in v if r.day in cur and r.gprd == r.gprd]
        ch = [abs(b - a) / a for a, b in both if a > 0]
        big = sum(c > 0.005 for c in ch)
        med = sorted(ch)[len(ch) // 2] if ch else float("nan")
        last = v[-1].day
        say(
            f"| {vd} | {vd:%a} | {last} | {(vd - last).days} | {len(both):,} | {big:,} | "
            f"{med:.4%} |"
        )
    say()


def nuc() -> None:
    folder = dw.snapshot("nuc")
    z = zipfile.ZipFile(folder / "NUC_STATUS.zip")
    kinds: Counter[str] = Counter()
    us_series = []
    gens = set()
    first, last = "99999999", "00000000"
    with z.open(z.infolist()[0]) as f:
        for line in io.TextIOWrapper(f):
            o = json.loads(line)
            sid = o.get("series_id", "")
            if "data" not in o:
                continue
            parts = sid.split(".")
            kinds[parts[1]] += 1
            if "US" in parts[2]:
                us_series.append((sid, o.get("name"), len(o["data"]), o.get("start"), o.get("end")))
            else:
                gens.add(parts[2])
            first, last = min(first, o.get("start", first)), max(last, o.get("end", last))
    say("## 3. EIA NUC_STATUS (US nuclear outages)")
    say()
    say(
        f"Snapshot `{folder.name}`: series by kind {dict(kinds)}; {len(gens)} plant/generator "
        f"ids; span {first} .. {last}."
    )
    for s in us_series:
        exp = (datetime.strptime(s[4], "%Y%m%d") - datetime.strptime(s[3], "%Y%m%d")).days + 1
        say(f"- `{s[0]}` ({s[1]}): {s[2]:,} rows, {s[3]} .. {s[4]}, missing {exp - s[2]} days.")
    say(
        "- No planned/unplanned flag in the file; the NRC reason text (row 25 of the inventory) "
        "was not reachable."
    )
    say()


def flu() -> None:
    folder = dw.snapshot("flu")
    o = json.loads((folder / "fluview_nat_latest.json").read_text())["epidata"]
    weeks = [r["epiweek"] for r in o]
    say("## 4. Delphi FluView (US national ILI)")
    say()
    say(f"Snapshot `{folder.name}`: {len(o):,} weekly rows, epiweeks {weeks[0]} .. {weeks[-1]}.")
    yrs = Counter(w // 100 for w in weeks)
    short = {
        y: n for y, n in yrs.items() if n < 52 and y not in (weeks[0] // 100, weeks[-1] // 100)
    }
    say(f"- Years with fewer than 52 weeks (inside the span): {short or 'none'}.")
    say(
        f"- Latest issue {o[-1]['issue']}, released {o[-1]['release_date']}; the oldest rows "
        f"carry issue {o[0]['issue']} (lag {o[0]['lag']} weeks), i.e. early history is a "
        "back-fill, not a real-time vintage."
    )
    v = json.loads((folder / "fluview_nat_issue201001.json").read_text())["epidata"]
    cur = {r["epiweek"]: r["wili"] for r in o}
    diffs = [abs(r["wili"] - cur[r["epiweek"]]) for r in v if r["epiweek"] in cur]
    say(
        f"- Vintage check: issue 201001 has {len(v)} rows; weighted ILI differs from today's "
        f"value by up to {max(diffs):.2f} points (median {sorted(diffs)[len(diffs) // 2]:.2f}): "
        "revisions are real, so a card must read `issues=`."
    )
    say()


def hacks() -> None:
    folder = dw.snapshot("hacks")
    o = json.loads((folder / "hacks.json").read_text())
    days = sorted(datetime.fromtimestamp(int(h["date"]), tz=UTC).date() for h in o)
    say("## 5. DefiLlama hacks")
    say()
    say(f"Snapshot `{folder.name}`: {len(o):,} events, {days[0]} .. {days[-1]}.")
    c = Counter(d.year for d in days)
    say(f"- Per year: {', '.join(f'{y} {c[y]}' for y in sorted(c))}.")
    amt = sum(h.get("amount") not in (None, 0) for h in o)
    say(
        f"- With a USD amount: {amt:,}; bridge hacks {sum(bool(h.get('bridgeHack')) for h in o)}; "
        f"with returned funds {sum(h.get('returnedFunds') not in (None, 0) for h in o)}."
    )
    chains = Counter(ch for h in o for ch in (h.get("chain") or []))
    say(f"- Top chains: {dict(chains.most_common(5))}.")
    say(
        "- No publication timestamp per event (curated, back-filled): treat each event as known "
        "only some days later; no vintages."
    )
    say()


def fdic() -> None:
    folder = dw.snapshot("fdic")
    fs = dw.parse_fdic_failures((folder / "failures.json").read_text())
    days = [f.day for f in fs]
    say("## 6. FDIC bank failures")
    say()
    say(
        f"Snapshot `{folder.name}`: {len(fs):,} failures and assistance transactions, "
        f"{days[0]} .. {days[-1]}."
    )
    say(f"- Per decade: {per_decade(days)}.")
    say(
        f"- Kinds: {dict(Counter(f.kind for f in fs))}; funds: {dict(Counter(f.fund for f in fs))}."
    )
    wd = Counter(d.strftime("%a") for d in days if d.year >= 2000)
    say(f"- Weekday of closing since 2000: {dict(wd.most_common())} (Friday-evening closures).")
    say(
        f"- Missing assets {sum(f.assets_k != f.assets_k for f in fs)}, missing cost "
        f"{sum(f.cost_k != f.cost_k for f in fs)}."
    )
    g, a, b = longest_gap(sorted(set(d for d in days if d.year >= 1990)))
    say(f"- Longest gap between failures since 1990: {g} days ({a} .. {b}).")
    say()


def portwatch() -> None:
    folder = dw.snapshot("portwatch")
    per: dict[str, list[date]] = {}
    rows = 0
    for p in sorted(folder.glob("page_*.json")):
        for f in json.loads(p.read_text())["features"]:
            a = f["attributes"]
            per.setdefault(a["portname"], []).append(date.fromisoformat(a["date"]))
            rows += 1
    say("## 7. IMF PortWatch daily chokepoint transits")
    say()
    say(f"Snapshot `{folder.name}`: {rows:,} rows, {len(per)} chokepoints.")
    say()
    say("| Chokepoint | Rows | First | Last | Missing days |")
    say("|---|---:|---|---|---:|")
    for k in sorted(per):
        ds = sorted(set(per[k]))
        miss = (ds[-1] - ds[0]).days + 1 - len(ds)
        say(f"| {k} | {len(per[k]):,} | {ds[0]} | {ds[-1]} | {miss} |")
    say()


def mof() -> None:
    folder = dw.snapshot("mof")
    raw = (folder / "foreign_exchange_intervention_operations.csv").read_bytes()
    ops = dw.parse_mof_csv(raw)
    q = dw.mof_quarter_totals(raw)
    say("## 8. Japan MOF FX intervention")
    say()
    days = [o.day for o in ops]
    say(
        f"Snapshot `{folder.name}`: {len(ops)} operation days, {days[0]} .. {days[-1]}; "
        f"{len(q)} published quarter totals."
    )
    sums: Counter[tuple[int, int]] = Counter()
    for o in ops:
        sums[(o.day.year, (o.day.month - 1) // 3 + 1)] += o.amount
    off = {k: (sums[k], v) for k, v in q.items() if abs(sums[k] - v) > 2}
    say(
        f"- Daily rows summed per quarter vs the published totals: {len(off)} quarters differ "
        f"by more than 2 (x 100 million yen){': ' + str(off) if off else ''}."
    )
    say(
        f"- Yen bought (support) days {sum(o.yen_sign > 0 for o in ops)}, yen sold days "
        f"{sum(o.yen_sign < 0 for o in ops)}, yen not involved {sum(o.yen_sign == 0 for o in ops)}."
    )
    eps, prev = 0, None
    for d in days:
        if prev is None or (d - prev).days > 30:
            eps += 1
        prev = d
    say(
        f"- Episodes (operation days more than 30 days apart start a new one): {eps}; "
        f"per decade (days): {per_decade(days)}."
    )
    say()


def kev() -> None:
    folder = dw.snapshot("kev")
    rows = list(
        csv.DictReader(io.StringIO((folder / "known_exploited_vulnerabilities.csv").read_text()))
    )
    days = sorted(date.fromisoformat(r["dateAdded"]) for r in rows)
    say("## 9. CISA KEV")
    say()
    c = Counter(d.year for d in days)
    say(
        f"Snapshot `{folder.name}`: {len(rows):,} rows, added {days[0]} .. {days[-1]}; per year "
        f"{', '.join(f'{y} {c[y]}' for y in sorted(c))}. The first day holds the initial "
        f"catalogue ({c[days[0].year] and sum(d == days[0] for d in days)} rows on {days[0]})."
    )
    say()


def main() -> None:
    say("# Data wide 1: verification of the downloads")
    say()
    say("Script `research/lib/datawide1_check.py`, files from `scripts/fetch_datawide1.py` in")
    say("the git-ignored cache. Counts, spans, gaps, release lags only: no price, no return, no")
    say("correlation was read. Generated " + datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC") + ".")
    say()
    for f in (usgs, gpr, nuc, flu, hacks, fdic, portwatch, mof, kev):
        f()
    OUT.write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
