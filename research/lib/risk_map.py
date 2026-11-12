"""The risk menu (card: research/cards/risk-map.md).

  uv run --with numpy python research/lib/risk_map.py run   # backtests: logs 20 tries
  uv run --with numpy python research/lib/risk_map.py       # tables and chart from saved runs

The second form reads the equity curves the first one saved in research/data/runs/risk-map/
(git-ignored), so the report can be rebuilt without logging tries again.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from datetime import date

import common as c
import harness
import numpy as np
import rules
import stats

from grimstrade.data import CRYPTO, UNIVERSE

IDEA = "risk-map"
RULES = ["hold", "tsmom12", "tv60", "tv40", "tv20"]
CAPS = {"tv60": 0.60, "tv40": 0.40, "tv20": 0.20}
SIZES: dict[str, float | None] = {"c00": 0.0, "c05": 0.05, "c10": 0.10, "c17": None}
WINDOWS = [
    ("1994-2025", date(1994, 2, 1)),
    ("2003-2025", date(2003, 1, 1)),
    ("2013-2025", date(2013, 1, 1)),
]
RULE_WORDS = {
    "hold": "Hold everything",
    "tsmom12": "Trend rule",
    "tv60": "Trend, swings capped (loose)",
    "tv40": "Trend, swings capped (medium)",
    "tv20": "Trend, swings capped (tight)",
}
SIZE_WORDS = {"c00": "none", "c05": "5% per coin", "c10": "10% per coin", "c17": "a sixth per coin"}


def menu(rule: str, size: float | None) -> c.ResearchStrategy:
    cap = CAPS.get(rule)

    def f(view: c.View) -> c.Weights:
        held = c.live(view)
        if not held:
            return {}
        coins = [s for s in held if UNIVERSE[s] == CRYPTO]
        rest = [s for s in held if UNIVERSE[s] != CRYPTO]
        if size is None:
            slot = {s: 1 / len(held) for s in held}
        else:
            slot = {s: size for s in coins}
            slot.update({s: (1 - size * len(coins)) / len(rest) for s in rest})
        out = {}
        for s in held:
            w = slot[s]
            if w <= 0 or (rule != "hold" and not c.tsmom_signal(view, s)):
                continue
            out[s] = w * rules.vol_cap(view, s, cap) if cap else w
        return out

    return f


def names() -> list[tuple[str, str, str]]:
    return [(f"{r}-{z}", r, z) for r in RULES for z in SIZES]


def run_all() -> None:
    six = c.ctx("six")
    for name, r, z in names():
        out = c.go(IDEA, name, c.weekly(menu(r, SIZES[z])), six)
        print(name, f"{stats.sharpe(out.rets):.2f}", flush=True)


@dataclass
class Row:
    name: str
    rule: str
    size: str
    cagr: float
    mdd: float
    worst_year: int
    worst_year_ret: float
    under_days: int  # longest spell below an earlier high
    under_open: bool  # that spell had not ended by the last day
    sharpe: float
    vol: float
    peak: date  # the worst drop: last high before it, its lowest day, first day back at the high
    trough: date
    back: date | None


def load(name: str) -> tuple[list[date], np.ndarray]:
    path = harness.DATA / "runs" / IDEA / f"{name}.train.csv"
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    days = [date.fromisoformat(r["date"]) for r in rows]
    return days, np.array([float(r["equity"]) for r in rows])


def measure(name: str, rule: str, size: str, days: list[date], eq: np.ndarray, start: date) -> Row:
    i = max((start - days[0]).days, 0)
    days, eq = days[i:], eq[i:]
    r = eq[1:] / eq[:-1] - 1
    peak = np.maximum.accumulate(eq)
    # longest spell below an earlier high
    best, open_, since = 0, False, 0
    for k in range(1, len(eq)):
        if eq[k] >= peak[k - 1]:
            since = k
        elif k - since > best:
            best, open_ = k - since, k == len(eq) - 1
    years: dict[int, list[float]] = {}
    for d, e in zip(days, eq, strict=True):
        years.setdefault(d.year, []).append(e)
    yr = {}
    prev = eq[0]
    for y in sorted(years):
        yr[y] = years[y][-1] / prev - 1
        prev = years[y][-1]
    wy = min(yr, key=lambda y: yr[y])
    lo = int(np.argmax(1 - eq / peak))
    hi = int(np.argmax(eq[: lo + 1]))
    later = np.nonzero(eq[lo:] >= eq[hi])[0]
    back = days[lo + int(later[0])] if len(later) else None
    return Row(name, rule, size, stats.cagr(r), float((1 - eq / peak).max()), wy, yr[wy], best,
               open_, stats.sharpe(r), stats.vol(r), days[hi], days[lo], back)  # fmt: skip


def shares() -> dict[str, tuple[float, float]]:
    """Average share of the account in crypto and in cash, by target weights, from the day all
    six assets are in the book. Reads the logged variants' decisions again; no backtest."""
    six = c.ctx("six")
    start = date(2017, 6, 1)
    out = {}
    for name, r, z in names():
        decs = harness.decisions(c.weekly(menu(r, SIZES[z])), six.panel, start, six.end)
        coin = [sum(w for s, w in d.weights.items() if UNIVERSE[s] == CRYPTO) for d in decs]
        cash = [1 - sum(d.weights.values()) for d in decs]
        out[name] = (float(np.mean(coin)), float(np.mean(cash)))
    return out


def month(d: date | None) -> str:
    return f"{d:%B %Y}" if d else "not yet"


def span(days: int, open_: bool) -> str:
    y = days / 365.25
    s = f"{y:.1f} years" if y >= 1 else f"{round(days / 30.44)} months"
    return s + (" and counting" if open_ else "")


def rows_for(start: date) -> list[Row]:
    return [measure(n, r, z, *load(n), start) for n, r, z in names()]


def detail_table(rows: list[Row]) -> str:
    out = [
        "| Variant | Growth a year | Worst drop | High before it | Low | Back at the high |"
        " Worst year | Longest below a high | Sharpe | Vol |",
        "|---|---:|---:|---|---|---|---:|---:|---:|---:|",
    ]
    for x in rows:
        out.append(
            f"| {x.name} | {x.cagr:+.1%} | {x.mdd:.1%} | {x.peak} | {x.trough} |"
            f" {x.back or 'not yet'} | {x.worst_year_ret:+.1%} ({x.worst_year}) |"
            f" {span(x.under_days, x.under_open)} | {x.sharpe:.2f} | {x.vol:.1%} |"
        )
    return "\n".join(out)


def report(held: dict[str, tuple[float, float]]) -> None:
    out = ["# risk-map: every choice on the menu, three windows", ""]
    out += [
        "Card: `cards/risk-map.md`. Six live assets, dividend-adjusted prices, the gym's costs,"
        " decided each Friday. One backtest per variant from 1994-02-01 to 2025-11-09; the later"
        " windows are slices of the same account, with the worst drop and the time below a high"
        " counted from the window's first day. Built by `lib/risk_map.py`.",
        "",
        "Names: `hold` always holds; `tsmom12` holds a slot only when the asset is up over a"
        " year; `tv60`, `tv40`, `tv20` add a cap on each slot's volatility (60%, 40%, 20% a"
        " year). `c00`, `c05`, `c10`: 0%, 5%, 10% in each coin; `c17`: equal slots (a sixth"
        " each once all six assets exist).",
        "",
    ]
    for label, start in WINDOWS:
        out += [f"## {label}", "", detail_table(rows_for(start)), ""]
    out += [
        "## Average share in crypto and in cash",
        "",
        "By target weights, 2017-06-01 to 2025-11-09 (all six assets in the book).",
        "",
        "| Variant | In crypto | In cash |",
        "|---|---:|---:|",
    ]
    out += [f"| {k} | {a:.1%} | {b:.1%} |" for k, (a, b) in held.items()]
    c.write_result(IDEA, "\n".join(out))


# --- the owner's page: research/risk-map.md and research/risk-map.svg ---

CHART_WINDOW = WINDOWS[1]  # 2003-2025: the first window in which the book is not SPY and QQQ only
PRESETS = [("Careful", "tv20-c05"), ("Middle", "tsmom12-c10"), ("Bold", "hold-c17")]
LIVE = "tv40-c17"  # nearest row to the paper lane's ts_momentum (equal slots, 40% volatility cap)
# Chart colours: the dataviz skill's reference palette, slots 1-5 in their validated order
# (adjacent lines pass its colour-blind and contrast checks on the light surface).
COLOUR = {"hold": "#2a78d6", "tsmom12": "#eb6834", "tv60": "#1baf7a", "tv40": "#eda100",
          "tv20": "#e87ba4"}  # fmt: skip
RADIUS = {"c00": 4.0, "c05": 5.5, "c10": 7.0, "c17": 8.5}
SURFACE, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
MUTED, GRID, AXIS = "#898781", "#e1e0d9", "#c3c2b7"
LEGEND_WORDS = {
    "hold": "Hold everything",
    "tsmom12": "Trend rule",
    "tv60": "Trend rule + loose swing cap",
    "tv40": "Trend rule + medium swing cap",
    "tv20": "Trend rule + tight swing cap",
}


def money(mdd: float) -> str:
    return f"{round(10_000 * (1 - mdd), -1):,.0f}"


def chart(rows: list[Row], label: str) -> str:
    w, h, left, top, pw, ph = 800, 600, 70, 70, 700, 440
    x0, x1, y0, y1 = 5.0, 50.0, 5.0, 27.0

    def px(v: float) -> float:
        return left + (v * 100 - x0) / (x1 - x0) * pw

    def py(v: float) -> float:
        return top + ph - (v * 100 - y0) / (y1 - y0) * ph

    by = {r.name: r for r in rows}
    font = 'font-family="system-ui, -apple-system, Segoe UI, sans-serif"'
    s = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"'
        f' role="img" aria-label="Growth per year against worst drop, {label}, one dot per'
        f' choice" {font}>',
        f'<rect width="{w}" height="{h}" rx="8" fill="{SURFACE}"/>',
        f'<text x="{left}" y="30" font-size="17" font-weight="600" fill="{INK}">Risk map: growth'
        f" per year against the worst drop, {label}</text>",
        f'<text x="{left}" y="52" font-size="13" fill="{INK2}">One dot per choice. Higher is'
        " faster growth. Further right is a deeper worst drop. Bigger dot: more crypto.</text>",
    ]
    for t in (10, 20, 30, 40, 50):
        x = px(t / 100)
        s.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + ph}" stroke="{GRID}"/>')
        s.append(f'<text x="{x:.1f}" y="{top + ph + 20}" font-size="12" text-anchor="middle"'
                 f' fill="{MUTED}">{t}%</text>')  # fmt: skip
    for t in (5, 10, 15, 20, 25):
        y = py(t / 100)
        stroke = AXIS if t == 5 else GRID
        s.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + pw}" y2="{y:.1f}"'
                 f' stroke="{stroke}"/>')  # fmt: skip
        s.append(f'<text x="{left - 10}" y="{y + 4:.1f}" font-size="12" text-anchor="end"'
                 f' fill="{MUTED}">{t}%</text>')  # fmt: skip
    s.append(f'<text x="{left + pw / 2}" y="{top + ph + 48}" font-size="13" text-anchor="middle"'
             f' fill="{INK2}">Worst drop from a high (further right is worse)</text>')  # fmt: skip
    s.append(f'<text transform="translate(20 {top + ph / 2}) rotate(-90)" font-size="13"'
             f' text-anchor="middle" fill="{INK2}">Growth per year</text>')  # fmt: skip
    # one line per rule, from no crypto to a sixth per coin
    for r in RULES:
        pts = " ".join(f"{px(by[f'{r}-{z}'].mdd):.1f},{py(by[f'{r}-{z}'].cagr):.1f}" for z in SIZES)
        s.append(f'<polyline points="{pts}" fill="none" stroke="{COLOUR[r]}" stroke-width="2"'
                 ' stroke-linejoin="round" stroke-linecap="round"/>')  # fmt: skip
    for z in reversed(list(SIZES)):  # big dots first, small ones on top
        for r in RULES:
            d = by[f"{r}-{z}"]
            s.append(
                f'<circle cx="{px(d.mdd):.1f}" cy="{py(d.cagr):.1f}" r="{RADIUS[z]}"'
                f' fill="{COLOUR[r]}" stroke="{SURFACE}" stroke-width="2"><title>'
                f"{LEGEND_WORDS[r]}, crypto {SIZE_WORDS[z]}: growth {d.cagr:.1%} a year, worst drop"
                f" {d.mdd:.1%} (10,000 fell to {money(d.mdd)})</title></circle>"
            )
    # the three presets: a ring and a label in ink
    place = {"Careful": (-16, 4, "end"), "Middle": (-14, -22, "end"), "Bold": (-18, -12, "end")}
    for name, key in PRESETS:
        d = by[key]
        cx, cy = px(d.mdd), py(d.cagr)
        dx, dy, anchor = place[name]
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{RADIUS[d.size] + 4.5}" fill="none"'
                 f' stroke="{INK}" stroke-width="1.5"/>')  # fmt: skip
        s.append(f'<text x="{cx + dx:.1f}" y="{cy + dy:.1f}" font-size="13" font-weight="600"'
                 f' text-anchor="{anchor}" fill="{INK}">{name}</text>')  # fmt: skip
        s.append(f'<text x="{cx + dx:.1f}" y="{cy + dy + 15:.1f}" font-size="11.5"'
                 f' text-anchor="{anchor}" fill="{INK2}">10,000 fell to'
                 f" {money(d.mdd)}</text>")  # fmt: skip
    # note on the three dots that coincide
    d = by["tsmom12-c00"]
    s.append(f'<text x="{px(d.mdd) + 12:.1f}" y="{py(d.cagr) + 16:.1f}" font-size="11.5"'
             f' fill="{MUTED}">With no crypto, the trend rule and the loose and medium caps'
             " are the same dot</text>")  # fmt: skip
    # legend, in the empty top-left corner, in the order the lines end from top to bottom
    lx, ly = left + 18, top + 24
    s.append(f'<rect x="{lx - 12}" y="{top - 1}" width="372" height="{21 * len(RULES) + 55}"'
             f' fill="{SURFACE}"/>')  # fmt: skip
    for k, r in enumerate(RULES):
        y = ly + 21 * k
        s.append(f'<line x1="{lx}" y1="{y}" x2="{lx + 26}" y2="{y}" stroke="{COLOUR[r]}"'
                 ' stroke-width="2" stroke-linecap="round"/>')  # fmt: skip
        s.append(f'<circle cx="{lx + 13}" cy="{y}" r="5" fill="{COLOUR[r]}" stroke="{SURFACE}"'
                 ' stroke-width="2"/>')  # fmt: skip
        s.append(f'<text x="{lx + 36}" y="{y + 4}" font-size="12.5" fill="{INK}">'
                 f"{LEGEND_WORDS[r]}</text>")  # fmt: skip
    y = ly + 21 * len(RULES) + 12
    s.append(f'<text x="{lx}" y="{y + 4}" font-size="12.5" fill="{INK2}">Crypto per coin:</text>')
    x = lx + 112
    for z, words in SIZE_WORDS.items():
        s.append(f'<circle cx="{x}" cy="{y}" r="{RADIUS[z]}" fill="{MUTED}"/>')
        s.append(f'<text x="{x + RADIUS[z] + 5}" y="{y + 4}" font-size="12.5" fill="{INK}">'
                 f"{words.replace(' per coin', '')}</text>")  # fmt: skip
        x += RADIUS[z] + 5 + 7 * len(words.replace(" per coin", "")) + 18
    s.append("</svg>")
    return "\n".join(s) + "\n"


def owner_table(now: list[Row], full: list[Row]) -> str:
    out = [
        "| Rule | Crypto per coin | Growth a year | Worst drop | 10,000 fell to | Time to recover |"
        " Worst year | Longest wait for a new high | 1994-2025: growth a year |"
        " 1994-2025: worst drop |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for a, b in zip(now, full, strict=True):
        out.append(
            f"| {LEGEND_WORDS[a.rule]} | {SIZE_WORDS[a.size].replace(' per coin', '')} |"
            f" {a.cagr:.1%} | {a.mdd:.0%} | {money(a.mdd)} | {recovery(a)} |"
            f" {a.worst_year_ret:+.0%} ({a.worst_year}) | {span(a.under_days, a.under_open)} |"
            f" {b.cagr:.1%} | {b.mdd:.0%} |"
        )
    return "\n".join(out)


def recovery(r: Row) -> str:
    """From the high before the worst drop to the first day back at that high."""
    return span((r.back - r.peak).days, False) if r.back else "not yet"


def story(r: Row) -> str:
    return (
        f"The worst drop ran from {month(r.peak)} to {month(r.trough)}; the account was back at"
        f" its old high in {month(r.back)}."
    )


def owner_page(held: dict[str, tuple[float, float]]) -> None:
    label, start = CHART_WINDOW
    now, full = rows_for(start), rows_for(WINDOWS[0][1])
    n, f = {r.name: r for r in now}, {r.name: r for r in full}
    (harness.RESEARCH / "risk-map.svg").write_text(chart(now, label))

    def preset_row(name: str, key: str) -> str:
        a, b = n[key], f[key]
        return (
            f"| **{name}** | {LEGEND_WORDS[a.rule]}, crypto {SIZE_WORDS[a.size]} | {a.cagr:.0%} |"
            f" {a.mdd:.0%} | **{money(a.mdd)}** | {recovery(a)} |"
            f" {a.worst_year_ret:+.0%} ({a.worst_year}) | {span(a.under_days, a.under_open)} |"
            f" {held[key][0]:.0%} / {held[key][1]:.0%} | {b.mdd:.0%} ({money(b.mdd)}) |"
        )

    def pair(a: str, b: str) -> str:
        return (
            f"growth {n[a].cagr:.0%} to {n[b].cagr:.0%} a year, worst drop {n[a].mdd:.0%} to"
            f" {n[b].mdd:.0%}"
        )

    careful, middle, bold, live = (n[k] for k in [p[1] for p in PRESETS] + [LIVE])
    preset_head = (
        "| Preset | What it is | Growth a year | Worst drop | 10,000 fell to, at worst |"
        " Time to recover | Worst calendar year | Longest wait for a new high |"
        " Held in crypto / in cash, on average | 1994-2025: worst drop |"
    )
    text = f"""# Risk map: how big a drop, how much crypto

For the owner. Built 2026-11-12 by `lib/risk_map.py` (research run 3); card `cards/risk-map.md`.

**The question.** How big a worst drop could you stomach, and how much crypto do you want? No
backtest can answer that for you. This page shows what each answer would have meant in money.

**What was done.** The same six assets (SPY, QQQ, TLT, GLD, BTC, ETH) run 20 ways: five rules
times four crypto sizes, fake money, real prices with dividends, trading costs included. No new
ideas and nothing tuned: these are the rules from runs 1 and 2 at different settings.

![Growth per year against worst drop, {label}, one dot per choice](risk-map.svg)

**How to read it.** Each dot is one choice. Higher means the account grew faster. Further right
means its worst fall from a high was deeper. Colour is the rule; a bigger dot holds more crypto.
The dots form one rising band: every step up in growth came with a deeper drop. There is no dot
in the top-left corner, and the research found no rule that puts one there.

## Three presets

Numbers are for {label}. "Fell to" is what 10,000 at the account's high had shrunk to at the
bottom of its worst drop.

{preset_head}
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{preset_row(*PRESETS[0])}
{preset_row(*PRESETS[1])}
{preset_row(*PRESETS[2])}

- **Careful.** Hold an asset only while it is up over the last year, hold less of anything
  that swings a lot, and keep crypto small. 10,000 fell to about {money(careful.mdd)} at
  worst. {story(careful)} The price is slow growth: {careful.cagr:.0%} a year where Bold made
  {bold.cagr:.0%}.
- **Middle.** The plain trend rule, with 10% of the account for each coin. 10,000 fell to
  about {money(middle.mdd)} at worst. {story(middle)}
- **Bold.** Hold all six in equal parts, always. The fastest growth on the menu, and 10,000
  fell to about {money(bold.mdd)}: nearly half gone. {story(bold)}
- **Where the paper lane is today.** Its trend strategy uses equal slots and a medium swing
  cap, so the nearest row is "{LEGEND_WORDS[live.rule]}" with {SIZE_WORDS[live.size]}. That
  lands beside Middle by another route: growth {live.cagr:.0%} a year, worst drop
  {live.mdd:.0%}, 10,000 fell to {money(live.mdd)}.

To choose: go down the "fell to" column and stop at the lowest figure you could watch without
selling. That row is your answer. Then expect worse than that figure one day: a worst drop is
only the worst so far.

## What moves a dot

- **Crypto size moves it most.** Holding everything, from no crypto to a sixth per coin:
  {pair("hold-c00", "hold-c17")}.
- **The trend rule buys a shallower drop and pays for it in growth.** At a sixth per coin,
  from holding to the trend rule: {pair("hold-c17", "tsmom12-c17")}. At 5% per coin:
  {pair("hold-c05", "tsmom12-c05")}. It is insurance, not extra return. On average it keeps
  about {held["tsmom12-c17"][1]:.0%} of the account in cash.
- **The swing cap is a second dose of the same.** It shrinks a slot when the asset turns
  jumpy, which mostly means it shrinks crypto. The trend rule at a sixth per coin, from no cap
  to the tight cap: {pair("tsmom12-c17", "tv20-c17")}. Crypto actually held falls from
  {held["tsmom12-c17"][0]:.0%} to {held["tv20-c17"][0]:.0%} of the account.

## The whole menu

{label} on the left (the chart), 1994-2025 in the last two columns. "Time to recover" runs
from the high before the worst drop to the day the account is back at that high.

{owner_table(now, full)}

Sharpe ratios, dates of each worst drop, average crypto and cash held, and a 2013-2025 view
are in `results/risk-map.md`. Sharpe is left out here on purpose: the menu is not a contest,
and no row has shown skill over another.

## Why two periods

The review of runs 1 and 2 (`reviews/review-1.md`, branch `review-1`) found that the trend
rule's lead over holding everything comes from 2000-2002. In those years the "six-asset" book
held two assets, SPY and QQQ, and holding them lost {f["hold-c17"].mdd:.0%} and took
{recovery(f["hold-c17"])} to recover. The live book will never be that one. So the chart and
the presets use {label}, the years in which bonds, then gold, then crypto join. The 1994-2025
columns are there so nothing is hidden. Over the full period every "hold everything" row shows
that same {f["hold-c17"].mdd:.0%} drop whatever its crypto size, and the trend rows look far
better against it than they have since.

## What these numbers cannot tell you

- **The growth column is flattered.** The six assets were picked knowing they went up, and
  Bitcoin rose about a thousandfold from 2013. That will not repeat. The more crypto in a
  row, the more its growth figure is flattered.
- **The worst-drop column is the better guide, and still only the past.** Crypto is in the
  book from 2013 (Bitcoin) and 2017 (Ether), so the crypto rows have lived through three
  crypto winters, no more. From 2013 to 2017 "a sixth per coin" meant a fifth in Bitcoin.
- **Dividends are counted.** The ETFs use dividend-adjusted prices (Yahoo, no key needed), as
  in runs 1 and 2; gold pays none. Cash earns nothing in the test. Run 1 put that at 0.5 to
  0.8% a year against the rules that sit in cash (`results/cash-interest.md`).
- **Longest wait for a new high** is the longest stretch the account spent below any earlier
  high. It can be longer than the recovery from the worst drop.
- **Averages held** are measured from June 2017, when all six assets are in the book.
- **Counted as tries.** All 20 rows are logged in `tries.md`. The held-out year (the last 12
  months) was not used.
"""
    (harness.RESEARCH / "risk-map.md").write_text(text)


if __name__ == "__main__":
    if sys.argv[1:] == ["run"]:
        run_all()
    weights = shares()
    report(weights)
    owner_page(weights)
