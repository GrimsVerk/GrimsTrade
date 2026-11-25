"""Lane wide-20: gate W31 `air-disaster-mood` (research/cards/wide-20.md; rule pushed before
this script's first run).

Descriptive only: no strategy, no backtest. Train bars only: load_history("train") cuts at
2025-11-10 and this script cuts again at 2025-10-31. The event file is an untrusted download in
the shared cache: run with `python -I`.

Fetch the events once:  `uv run python -I research/lib/wide20.py fetch`
Run:                    `uv run python -I research/lib/wide20.py`  (DRY=1: counts only)
Output: research/results/air-disaster-mood.md
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from collections import Counter
from collections.abc import Sequence
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import wide20_events as ev  # noqa: E402

from grimstrade import cache  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)
SNAP = "2026-11-24"
REL = f"wide-20/wikidata/{SNAP}/air.csv"
URL = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": ev.QUERY})
UA = "research-script/0.1 (offline statistics)"
GATE = ("SPY", date(2008, 1, 1), LAST)
LONG = ("GSPC", date(1950, 1, 1), date(2007, 12, 31))
OTHERS = ["QQQ", "IWM", "GLD", "TLT", "BTC", "ETH"]
# Shown cell "list completed" (wide-20.md, dry-run addendum, written before any return):
# accidents of the gate window with >= 50 deaths that the frozen query missed, by memory.
EXTRA_TITLES = [
    "Ethiopian Airlines Flight 409",
    "Air India Express Flight 812",
    "Airblue Flight 202",
    "Malaysia Airlines Flight 370",
    "Indonesia AirAsia Flight 8501",
    "2015 Medan Hercules crash",
    "Saratov Airlines Flight 703",
    "Iran Aseman Airlines Flight 3704",
    "US-Bangla Airlines Flight 211",
    "2018 Algerian Air Force Ilyushin Il-76 crash",
    "Cubana de Aviación Flight 972",
    "Lion Air Flight 610",
    "Ethiopian Airlines Flight 302",
    "Ukraine International Airlines Flight 752",
    "Pakistan International Airlines Flight 8303",
    "2021 Philippine Air Force Lockheed C-130 crash",
    "Yeti Airlines Flight 691",
    "2024 Belgorod Ilyushin Il-76 crash",
]
REL_WP = f"wide-20/wikipedia/{SNAP}/pageprops.json"
REL_WD = f"wide-20/wikidata/{SNAP}/extra-entities.json"


def fetch() -> None:
    root = dw.cache_root()
    if (root / REL).exists():
        print("already cached:", root / REL)
        return
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "text/csv"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data: bytes = r.read()
    cache.write_once(root, REL, data, URL)
    print("fetched", len(data), "bytes into", root / REL)


def fetch_extra() -> None:
    """Resolve EXTRA_TITLES to Wikidata items (Wikipedia API), then read their claims."""
    root = dw.cache_root()
    if not (root / REL_WP).exists():
        q = {"action": "query", "prop": "pageprops", "ppprop": "wikibase_item"}
        q |= {"redirects": "1", "format": "json", "titles": "|".join(EXTRA_TITLES)}
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(q)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            cache.write_once(root, REL_WP, r.read(), url)
    pages = json.loads((root / REL_WP).read_text())["query"]["pages"].values()
    ids = sorted({p["pageprops"]["wikibase_item"] for p in pages if "pageprops" in p})
    missing = [p.get("title") for p in pages if "pageprops" not in p]
    print("resolved", len(ids), "of", len(EXTRA_TITLES), "titles; unresolved:", missing)
    if not (root / REL_WD).exists():
        q = {"action": "wbgetentities", "props": "claims", "format": "json", "ids": "|".join(ids)}
        url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(q)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            cache.write_once(root, REL_WD, r.read(), url)


def load_extra(known: set[str]) -> list[ev.Event]:
    ents = json.loads((dw.cache_root() / REL_WD).read_text())["entities"]
    out = []
    for qid, ent in ents.items():
        e = ev.parse_entity(ent)
        if qid in known or e is None or e[1] < ev.MIN_DEATHS or e[0] > LAST:
            continue
        out.append(e)
    return sorted(out)


def load_events() -> list[ev.Event]:
    text = (dw.cache_root() / REL).read_text(encoding="utf-8", errors="replace")
    return [e for e in ev.parse_events(text) if e[0] <= LAST]


class Series:
    """Daily log returns of one asset on bars dated lo .. hi (first return needs a bar < lo)."""

    def __init__(self, bars: Sequence[harness.Bar], lo: date, hi: date):
        bs = [b for b in bars if b.date <= hi]
        i0 = next(i for i, b in enumerate(bs) if b.date >= lo)
        i0 = max(i0, 1)
        self.dates = [b.date for b in bs[i0:]]
        c = np.array([b.close for b in bs[i0 - 1 :]], dtype=float)
        self.r = np.diff(np.log(c))
        self.lo, self.hi = max(lo, self.dates[0]), hi


def fit(
    s: Series, events: Sequence[ev.Event], days: Sequence[int] = (0, 1), binary: bool = False
) -> tuple[float, float, int]:
    """The one code path: OLS of daily return on the dose, HC1 t, also for every placebo."""
    return ev.ols_hc1(ev.dose(s.dates, events, days, binary), s.r)


def placebos(s: Series, events: Sequence[ev.Event]) -> list[float]:
    return [fit(s, ev.shift(events, k, s.lo, s.hi))[1] for k in ev.SHIFTS]


def cell(name: str, s: Series, events: Sequence[ev.Event], **kw: object) -> str:
    b, t, n = fit(s, events, **kw)  # type: ignore[arg-type]
    return f"| {name} | {len(events)} | {b * 100:+.4f} ({t:+.2f}) | {n} |"


def null_line(placebo: Sequence[float]) -> str:
    sd, share, q5, med, q95 = ev.null_spread(placebo)
    return (
        f"40 placebo t: sd {sd:.2f}, share with |t| >= 2 {share:.0%}; quantiles 5% {q5:+.2f},"
        f" 50% {med:+.2f}, 95% {q95:+.2f}; smallest {min(placebo):+.2f}, largest"
        f" {max(placebo):+.2f}."
    )


def main() -> None:
    events = load_events()
    hist = harness.load_history("train", syms=["SPY", "GSPC", *OTHERS])
    sym, lo, hi = GATE
    spy = Series(hist[sym], lo, hi)
    gate_ev = ev.in_window(events, spy.lo, spy.hi)
    if DRY:
        print("events (deaths >= 50, day precision), all years:", len(events))
        print("by decade:", sorted(Counter(e[0].year // 10 * 10 for e in events).items()))
        print("gate window", spy.lo, spy.hi, "SPY returns", len(spy.r), "events", len(gate_ev))
        print("gate events by year:", sorted(Counter(e[0].year for e in gate_ev).items()))
        x = ev.dose(spy.dates, gate_ev)
        print("dosed bars", int((x > 0).sum()), "mean dose on them", round(x[x > 0].mean(), 2))
        for k in (ev.SHIFTS[0], ev.SHIFTS[-1]):
            xs = ev.dose(spy.dates, ev.shift(gate_ev, k, spy.lo, spy.hi))
            print("placebo", k, "dosed bars", int((xs > 0).sum()))
        g = Series(hist[LONG[0]], LONG[1], LONG[2])
        print("GSPC 1950-2007 returns", len(g.r), "events", len(ev.in_window(events, g.lo, g.hi)))
        for a in OTHERS:
            s = Series(hist[a], lo, hi)
            print(a, s.lo, len(s.r), "events", len(ev.in_window(events, s.lo, s.hi)))
        return

    b, t, n = fit(spy, gate_ev)
    plac = placebos(spy, gate_ev)
    rank = ev.rank_lowest(t, plac)
    met = [b < 0, t <= -2, rank <= 2]
    out = [
        "# W31 `air-disaster-mood`: result",
        "",
        "Card: `research/cards/wide-20.md` (pushed before this run). Script:"
        " `research/lib/wide20.py`. Train only: bars to 2025-10-31; held-out year unread.",
        f"Events: Wikidata aviation accidents with >= 50 deaths, day precision ({len(events)}"
        f" in all years to {LAST}; {len(gate_ev)} in the gate window).",
        "",
        "## Gate (SPY daily return on the dose of days 0-1, HC1)",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| b, % a day per unit of log2(deaths / 25), {n} days | {b * 100:+.4f} | < 0 | {met[0]} |",
        f"| t (HC1) | {t:+.2f} | <= -2 | {met[1]} |",
        f"| Rank of true t among 41 calendars (1 = lowest) | {rank} | <= 2 | {met[2]} |",
        "",
        f"**Gate: {'PASS (kill-only design: not dead yet)' if all(met) else 'fail'}.**"
        f" Empirical one-sided p = {rank}/41 = {rank / 41:.3f}.",
        "",
        "## Placebo null (each event moved 23k days, wrapped in the window, k = +-1..20)",
        "",
        null_line(plac),
        "",
        "| k | t |",
        "|---:|---:|",
        *[f"| {k:+d} | {v:+.2f} |" for k, v in zip(ev.SHIFTS, plac, strict=True)],
        "",
        "## Shown (not gating)",
        "",
        "| Cut | Events | b, % a day per unit (t) | Days |",
        "|---|---:|---:|---:|",
        cell("Gate (SPY, dose, days 0-1)", spy, gate_ev),
        cell("Binary indicator, days 0-1", spy, gate_ev, binary=True),
        cell("Dose, days 0-2", spy, gate_ev, days=(0, 1, 2)),
        cell("Reversal: dose on days 2-4 (predicted > 0)", spy, gate_ev, days=(2, 3, 4)),
        cell("Only >= 100 deaths", spy, [e for e in gate_ev if e[1] >= 100]),
        cell(
            "Three largest removed",
            spy,
            sorted(sorted(gate_ev, key=lambda e: e[1])[:-3]),
        ),
    ]
    for a in OTHERS:
        s = Series(hist[a], lo, hi)
        out.append(cell(f"{a} from {s.lo}", s, ev.in_window(events, s.lo, s.hi)))
    known = ev.items_in((dw.cache_root() / REL).read_text(encoding="utf-8", errors="replace"))
    extra = ev.in_window(load_extra(known), spy.lo, spy.hi)
    full = sorted(gate_ev + extra)
    out.append(cell(f"List completed (+{len(extra)} items, wide-20.md addendum)", spy, full))
    ct = fit(spy, full)[1]
    cplac = placebos(spy, full)
    g = Series(hist[LONG[0]], LONG[1], LONG[2])
    g_ev = ev.in_window(events, g.lo, g.hi)
    gb, gt, _ = fit(g, g_ev)
    gplac = placebos(g, g_ev)
    out.append(cell("GSPC 1950-2007 (the paper's span, in-sample for it)", g, g_ev))
    out.append(cell("GSPC 1950-2007, binary", g, g_ev, binary=True))
    out.append(cell("GSPC 1950-2007, reversal days 2-4", g, g_ev, days=(2, 3, 4)))
    gall = Series(hist[LONG[0]], LONG[1], LAST)
    out.append(cell("GSPC 1950-2025 (full span)", gall, ev.in_window(events, gall.lo, gall.hi)))
    out += [
        "",
        f"GSPC 1950-2007 with its own 40 placebos (shown): t {gt:+.2f}, rank"
        f" {ev.rank_lowest(gt, gplac)} of 41 (1 = lowest). {null_line(gplac)}",
        "",
        f"List completed with its own 40 placebos (shown): t {ct:+.2f}, rank"
        f" {ev.rank_lowest(ct, cplac)} of 41. {null_line(cplac)} Added events: "
        + ", ".join(f"{e} {d:.0f}" for e, d in extra)
        + ".",
        "",
        "Largest events in the gate window (date, deaths): "
        + ", ".join(f"{e} {d:.0f}" for e, d in sorted(gate_ev, key=lambda e: -e[1])[:5])
        + ".",
        "",
    ]
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "air-disaster-mood.md").write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    if sys.argv[1:] == ["fetch"]:
        fetch()
    elif sys.argv[1:] == ["fetch-extra"]:
        fetch_extra()
    else:
        main()
