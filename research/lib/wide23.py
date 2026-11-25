"""Lane wide-23: gate W37 `hack-drift` and replication R37 (research/cards/wide-23.md; rule
pushed before this script's first run).

Descriptive only: no strategy, no backtest. Train bars only: load_history("train") cuts at
2025-11-10 and this script cuts again at 2025-10-31. The hack list is an untrusted download in
the shared cache: run with `python -I`.

Fetch once:   `uv run python -I research/lib/wide23.py fetch`
Gate W37:     `uv run python -I research/lib/wide23.py`      (DRY=1: counts only)
Replication:  `uv run python -I research/lib/wide23.py r37`  (only after a W37 pass)
Output: research/results/hack-drift.md (and hack-drift-r37.md)
"""

from __future__ import annotations

import os
import sys
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import wide23_events as ev  # noqa: E402

from grimstrade import cache  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)
URL = "https://api.llama.fi/hacks"
REL = "wide-23/defillama/2026-11-25/hacks.json"
UA = "research-script/0.1 (offline statistics)"
POST_LT = date(2018, 6, 1).toordinal()  # after Liu and Tsyvinski's sample

Closes = dict[int, float]
DoseFn = Callable[[int], float]


def fetch() -> None:
    root = dw.cache_root()
    if (root / REL).exists():
        print("cached", root / REL)
        return
    req = urllib.request.Request(URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    cache.write_once(root, REL, data, URL)
    print("fetched", root / REL, len(data))


def load() -> tuple[list[ev.Event], dict[str, Closes]]:
    root = dw.cache_root()
    events = ev.parse_hacks((root / REL).read_text(encoding="utf-8", errors="replace"), LAST)
    hist = harness.load_history("train", syms=["BTC", "ETH"])
    px = {
        s: {b.date.toordinal(): b.close for b in bars if b.date <= LAST} for s, bars in hist.items()
    }
    return events, px


def fit(
    rs: Sequence[int],
    y: Sequence[float],
    ctl: Sequence[Sequence[float]],
    x: DoseFn,
    lags: int,
) -> tuple[float, float, int]:
    """(b, t, rows) of y = a + b x + controls, Newey-West t. One code path for every cell,
    true, placebo and surrogate."""
    xx = np.array([x(d) for d in rs])
    beta, tt = ev.ols_nw([xx, *(np.asarray(c) for c in ctl)], np.asarray(y), lags)
    return float(beta[1]), float(tt[1]), len(rs)


def fit_arr(
    y: Sequence[float], ctl: Sequence[Sequence[float]], xx: np.ndarray, lags: int
) -> tuple[float, float]:
    beta, tt = ev.ols_nw([xx, *(np.asarray(c) for c in ctl)], np.asarray(y), lags)
    return float(beta[1]), float(tt[1])


def design(c: Closes, rs: Sequence[int], ahead: int = 8) -> tuple[list[float], list[list[float]]]:
    """Outcome and the two controls; `rows` guarantees the closes they need (no gaps)."""
    y = [ev.logret(c, d + 1, d + ahead) for d in rs]
    r7 = [ev.logret(c, d - 6, d + 1) for d in rs]
    r30 = [ev.logret(c, d - 29, d + 1) for d in rs]
    return y, [r7, r30]


def iso(d: int) -> str:
    return date.fromordinal(d).isoformat()


def gaps(rs: Sequence[int]) -> int:
    return sum(1 for a, b in zip(rs, rs[1:], strict=False) if b != a + 1)


def null_block(name: str, t: float, others: Sequence[float], labels: Sequence[str]) -> list[str]:
    sd, share, q5, q50, q95, lo, hi = ev.null_spread(others)
    rank = ev.rank_lowest(t, others)
    out = [
        f"**{name}**: true t {t:+.2f}, rank {rank} of {len(others) + 1} from the lowest;"
        f" SD of the {len(others)} t {sd:.2f}, share with |t| >= 2 {share:.0%}; quantiles"
        f" 5% {q5:+.2f}, 50% {q50:+.2f}, 95% {q95:+.2f}; smallest {lo:+.2f}, largest {hi:+.2f}.",
        "",
    ]
    if labels:
        out += ["| placebo | t |", "|---|---:|"]
        out += [f"| {lab} | {v:+.2f} |" for lab, v in zip(labels, others, strict=True)]
        out.append("")
    return out


def gate_cells(
    name: str, c: Closes, events: Sequence[ev.Event], last: int
) -> tuple[dict[str, object], list[str]]:
    """True t, 40 earlier-dose placebos, 40 phase and 40 random-day surrogates."""
    rs = ev.rows(c, last)
    y, ctl = design(c, rs)
    dz = ev.dose(events)
    b, t, n = fit(rs, y, ctl, lambda d: ev.at(dz, d), ev.LAGS)
    plac = [fit(rs, y, ctl, lambda d, k=k: ev.at(dz, d, k), ev.LAGS)[1] for k in ev.SHIFTS]
    xx = np.array([ev.at(dz, d) for d in rs])
    ph = [fit_arr(y, ctl, s, ev.LAGS)[1] for s in ev.phase_surrogates(xx)]
    dy = [fit_arr(y, ctl, s, ev.LAGS)[1] for s in ev.day_surrogates(xx)]
    rank = ev.rank_lowest(t, plac)
    verdict = b < 0 and t <= -2 and rank <= 2
    lines = [
        f"## {name}",
        "",
        f"Rows {n} (days {iso(rs[0])} .. {iso(rs[-1])}), event days in rows"
        f" {int(np.count_nonzero(xx))}, sum of weights {xx.sum():.1f}.",
        "",
        f"**b {b * 100:+.3f}% over the week per unit of dose (one doubling of the USD stolen),"
        f" t {t:+.2f}, rank {rank} of 41 earlier-dose calendars: {'PASS' if verdict else 'FAIL'}"
        f" (b < 0: {b < 0}, t <= -2: {t <= -2}, rank <= 2: {rank <= 2}).**",
        "",
        *null_block(
            "Earlier-dose placebos (the decider)", t, plac, [f"k = {k} days" for k in ev.SHIFTS]
        ),
        *null_block("Phase-randomised surrogates (shown)", t, ph, []),
        *null_block("Random-day surrogates (shown)", t, dy, []),
    ]
    return {"b": b, "t": t, "n": n, "rank": rank, "pass": verdict, "plac": plac}, lines


def shown_cells(events: Sequence[ev.Event], px: Mapping[str, Closes], last: int) -> list[str]:
    ce, cb = px["ETH"], px["BTC"]
    rs = ev.rows(ce, last)
    y, ctl = design(ce, rs)
    dz = ev.dose(events)

    def x(dd: Mapping[int, float]) -> DoseFn:
        return lambda d: ev.at(dd, d)

    out = ["## Shown cells (not gating)", "", "| Cell | b, % | t | Rows |", "|---|---:|---:|---:|"]

    def row(lab: str, r: tuple[float, float, int]) -> None:
        out.append(f"| {lab} | {r[0] * 100:+.3f} | {r[1]:+.2f} | {r[2]} |")

    y0 = [ev.logret(ce, d - 1, d + 1) for d in rs]
    row("Reaction: ETH ln C(d+1) - ln C(d-1), no controls, NW 2", fit(rs, y0, [], x(dz), 2))
    rb = ev.rows(cb, last)
    yb, cbl = design(cb, rb)
    row("BTC, gate design (BTC's own rows and controls)", fit(rb, yb, cbl, x(dz), ev.LAGS))
    both = [d for d in rs if d + 1 in cb and d + 8 in cb]
    yd = [ev.logret(ce, d + 1, d + 8) - ev.logret(cb, d + 1, d + 8) for d in both]
    _, cboth = design(ce, both)
    row("ETH minus BTC, ETH's controls", fit(both, yd, cboth, x(dz), ev.LAGS))
    r30 = ev.rows(ce, last, ahead=31)
    y30, c30 = design(ce, r30, ahead=31)
    row("30-day horizon ln C(d+31) - ln C(d+1), NW 30", fit(r30, y30, c30, x(dz), 30))
    row(
        "Binary dose (1 per event; 114 events on 109 days)",
        fit(rs, y, ctl, x(ev.dose(events, binary=True)), 7),
    )
    row("Events of USD 50 m or more only", fit(rs, y, ctl, x(ev.dose(events, min_usd=5e7)), 7))
    rp = [i for i, d in enumerate(rs) if d >= POST_LT]
    row(
        "After Liu-Tsyvinski's sample (d >= 2018-06-01)",
        fit(
            [rs[i] for i in rp],
            [y[i] for i in rp],
            [[c[i] for i in rp] for c in ctl],
            x(dz),
            ev.LAGS,
        ),
    )
    out.append("")
    return out


def run(r37: bool = False) -> None:
    events, px = load()
    g, xs = ev.split(events)
    last = LAST.toordinal()
    asset, evs, tag = ("BTC", xs, "R37") if r37 else ("ETH", g, "W37")
    c = px[asset]
    rs = ev.rows(c, last)
    dz = ev.dose(evs)
    nz = sum(1 for d in rs if ev.at(dz, d) != 0)
    print(
        f"{tag}: events G {len(g)} X {len(xs)}; {asset} closes {len(c)}"
        f" ({iso(min(c))} .. {iso(max(c))}); rows {len(rs)} ({iso(rs[0])} .. {iso(rs[-1])}),"
        f" gaps {gaps(rs)}, event days in rows {nz}"
    )
    if DRY:
        return
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    if r37:
        res, lines = gate_cells("R37: BTC on thefts from centralised exchanges", c, xs, last)
        head = "# R37 `hack-drift` replication (cards/wide-23.md)"
        path = RESULTS / "hack-drift-r37.md"
        body = lines
    else:
        res, lines = gate_cells("W37: ETH on thefts from non-exchange targets", c, g, last)
        head = "# W37 `hack-drift` (cards/wide-23.md)"
        path = RESULTS / "hack-drift.md"
        body = lines + shown_cells(g, px, last)
    text = [
        head,
        "",
        f"Generated by `research/lib/wide23.py{' r37' if r37 else ''}` at {stamp}; train data"
        " only (no bar or event after 2025-10-31). b is in % of the 7-day log return per unit"
        " of dose; Newey-West t, 7 lags, controls r7 and r30 unless named.",
        "",
        *body,
    ]
    path.write_text("\n".join(text).rstrip() + "\n")
    print(f"{tag}: b {res['b']:+.5f} t {res['t']:+.2f} rank {res['rank']} pass {res['pass']}")
    print("wrote", path)


# Post hoc (review of PR #205, after the real run; not a rule): events not public at their
# listed date. LuBian (USD 3.5 bn, listed 2020-12-28) became public in 2025-08; Mirror (USD 90 m,
# listed 2021-10-08) by its own description was discovered 2022-05-17.
LATE = {"LuBian": (date(2020, 12, 28), 3.5e9), "Mirror": (date(2021, 10, 8), 89.7e6)}


def drop(events: Sequence[ev.Event], names: Sequence[str]) -> list[ev.Event]:
    """Events without the named LATE ones (matched on day and amount within 1%)."""
    keys = [LATE[n] for n in names]
    out = [
        e
        for e in events
        if not any(e[0] == d.toordinal() and abs(e[1] / a - 1) < 0.01 for d, a in keys)
    ]
    if len(out) != len(events) - len(names):
        raise SystemExit(f"post hoc: expected to drop {names}, dropped {len(events) - len(out)}")
    return out


MARK = "## Post hoc: events not public at their listed date"


def posthoc() -> None:
    events, px = load()
    g, _ = ev.split(events)
    last = LAST.toordinal()
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    text = [
        MARK,
        "",
        f"`research/lib/wide23.py posthoc`, {stamp}, added after the gate's number on review of"
        " PR #205 (not a rule, not a gate). Same code path, events dropped only.",
        "",
    ]
    for names in (["LuBian"], ["LuBian", "Mirror"]):
        gg = drop(g, names)
        _, lines = gate_cells(f"W37 design without {' and '.join(names)}", px["ETH"], gg, last)
        text += ["#" + lines[0], *lines[1:4]] + [
            ln for ln in lines[4:] if not ln.startswith(("| k", "| placebo", "|---|---:|"))
        ]
        if names == ["LuBian"]:
            sc = shown_cells(gg, px, last)
            text += ["### Shown cells without LuBian", *sc[1:]]
    path = RESULTS / "hack-drift.md"
    old = path.read_text()
    if MARK in old:
        old = old[: old.index(MARK)].rstrip() + "\n"
    path.write_text(old.rstrip() + "\n\n" + "\n".join(text).rstrip() + "\n")
    print("wrote", path)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "fetch":
        fetch()
    elif arg == "posthoc":
        posthoc()
    else:
        run(r37=arg == "r37")
