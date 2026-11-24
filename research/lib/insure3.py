"""insure-3: is trend cheaper or dearer crash insurance than buying puts? Card: cards/insure-3.md.

    uv run python -I research/lib/fetch_insure3.py   # once: raw files into the data cache
    uv run python -I research/lib/insure3.py

Descriptive comparison on the S&P 500, 1986-07-01..2025-10-31: holding the total return,
`tsmom12` on it (trend_tune.paper, exactly the record's rule; idle cash at bills, and at 0 as a
check), CBOE's PPUT (5% out-of-the-money monthly puts on the index) and a 50/50 of trend and
PPUT rebalanced each month. Measures per card: CAGR, Sharpe above bills, worst loss, the loss in
each 15% fall (insure-1's zigzag), the insurance cost (CAGR gap to holding / mean loss avoided per
fall) and insure-1's pooled premium. Side table: PUT, BXM, CLL, VXTH on their own windows.
Raw index levels stay in the data cache (CBOE terms); only statistics go to
research/results/insure-3.md. Nothing after 2025-10-31 is parsed. tries.md rows are written once.
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import trend_tune as tt  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade.data import ETF, UNIVERSE, Bar  # noqa: E402

IDEA = "insure-3"
LAST = date(2025, 10, 31)  # nothing later is parsed
BASE = date(1986, 6, 30)  # PPUT's first level (100); returns from 1986-07-01
WARM = date(1985, 1, 2)  # the rule needs a year of bars before its first decision
SP500TR_FIRST = date(1988, 1, 4)
FALL = (0.15, 0.15)  # zigzag down / up
FAST = 92  # calendar days peak -> trough
REBOUND = 365
COST = 0.0002  # the gym's ETF cost, one way
RAW = f"insure-3/raw-{'2026-11-24'}"
SIDE = ("PUT", "BXM", "CLL", "VXTH")
SIDE_FIRST = {"PUT": date(2007, 1, 3)}  # PUT's file has 7 scattered points before 2007
NAMED_FAST = {"1987": (date(1987, 10, 1), date(1987, 12, 31)),
              "2020": (date(2020, 2, 1), date(2020, 4, 30))}  # fmt: skip
OUT = harness.RESEARCH / "results" / "insure-3.md"
TRIES = harness.RESEARCH / "tries.md"


# --- parsing (untrusted downloads, data only) ---


def parse_cboe(text: str, last: date = LAST) -> dict[date, float]:
    out: dict[date, float] = {}
    for line in text.splitlines()[1:]:
        cells = line.split(",")
        if len(cells) < 2:
            continue
        try:
            d = datetime.strptime(cells[0].strip(), "%m/%d/%Y").date()
            v = float(cells[1])
        except ValueError:
            continue
        if d <= last and v > 0:
            out[d] = v
    return out


def parse_yahoo(obj: dict[str, Any], last: date = LAST) -> dict[date, float]:
    """Daily closes of a Yahoo chart file, by exchange date (the stamp is the US open)."""
    r = obj["chart"]["result"][0]
    closes = r["indicators"]["quote"][0]["close"]
    out: dict[date, float] = {}
    for ts, cl in zip(r["timestamp"], closes, strict=True):
        d = datetime.fromtimestamp(ts, UTC).date()
        if d > last:
            break  # nothing later is parsed
        if cl is not None and cl > 0:
            out[d] = float(cl)
    return out


def built_tr(px: dict[date, float], div: dict[str, float]) -> dict[date, float]:
    """Total-return index from a price index and Shiller's monthly annual dividend rate,
    accrued per session as dividend / previous close / 252."""
    days = sorted(px)
    out = {days[0]: 1.0}
    for a, b in zip(days, days[1:], strict=False):
        d = div.get(f"{b:%Y-%m}", 0.0)
        out[b] = out[a] * (px[b] / px[a] + d / px[a] / 252)
    return out


def splice(early: dict[date, float], late: dict[date, float], first: date) -> dict[date, float]:
    """`early` up to the day before `first`, then chained on `late`'s own returns from the
    first day after it (the joining day's return is early's)."""
    out = {d: v for d, v in early.items() if d < first}
    last_e = max(out)
    k = early.get(first)
    if k is None:
        raise ValueError("early series must cover the joining day")
    out[first] = out[last_e] * k / early[last_e]
    prev = first
    for d in sorted(x for x in late if x > first):
        out[d] = out[prev] * late[d] / late[prev]
        prev = d
    return out


def align(days: Sequence[date], level: dict[date, float]) -> tuple[np.ndarray, int]:
    """Levels on `days`, the last earlier level carried over a missing day; and how many
    days were carried. The first day must be present."""
    if days[0] not in level:
        raise ValueError(f"no level on the first day {days[0]}")
    out = np.empty(len(days))
    miss = 0
    for i, d in enumerate(days):
        if d in level:
            out[i] = level[d]
        else:
            out[i] = out[i - 1]
            miss += 1
    return out, miss


def bill_returns(days: Sequence[date], yld: dict[date, float]) -> np.ndarray:
    """Per-session bill return: the last yield seen before the session, per calendar day."""
    ys = sorted(yld)
    out = np.zeros(len(days))
    j = 0
    for i in range(1, len(days)):
        while j + 1 < len(ys) and ys[j + 1] <= days[i - 1]:
            j += 1
        out[i] = yld[ys[j]] / 100 * (days[i] - days[i - 1]).days / 365
    return out


# --- the rule and the mix ---


def trend(days: Sequence[date], level: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """`tsmom12` paper series on a total-return level: (simple return, position) per session.
    Returns index i is the move from session i-1 to i; position i is what earned it."""
    sym = "I3-SPXTR"
    UNIVERSE[sym] = ETF  # research process only; src/ is untouched
    bars = []
    prev = float(level[0])
    for d, x in zip(days, level, strict=True):
        bars.append(Bar(d, prev, max(prev, x), min(prev, x), float(x), 0.0))
        prev = float(x)
    panel = harness.Panel({sym: bars})
    p = tt.paper(panel, sym, (12,))
    ret = p.ret[12]
    bar = np.zeros(len(level))
    bar[1:] = level[1:] / level[:-1] - 1
    pos = np.zeros(len(level))
    for i in range(1, len(level)):  # ret = pos * bar - COST * |flip| (insure-1's infer_pos)
        fit1 = min(abs(ret[i] - bar[i]), abs(ret[i] - bar[i] + COST)) < 1e-12
        fit0 = min(abs(ret[i]), abs(ret[i] + COST)) < 1e-12
        pos[i] = pos[i - 1] if fit1 == fit0 else (1.0 if fit1 else 0.0)
    return ret, pos


def own_positions(days: Sequence[date], level: np.ndarray) -> np.ndarray:
    """Independent restatement of the rule, for the tests. On each Friday (a calendar Friday,
    holiday or not), with the sessions closed on or before it visible: if at least 252 are
    visible and the last visible close is above the close on the last session on or before 365
    days earlier, hold from the next session through the next Friday, else cash."""
    ords = np.array([d.toordinal() for d in days])
    pos = np.zeros(len(days))
    fri = days[0] + timedelta(days=(4 - days[0].weekday()) % 7)
    while fri < days[-1]:
        k = int(np.searchsorted(ords, fri.toordinal(), side="right"))  # sessions visible
        lo, hi = k, int(np.searchsorted(ords, fri.toordinal() + 7, side="right"))
        if k >= 252:
            t0 = ords[k - 1] - 365
            if ords[0] <= t0:
                j = int(np.searchsorted(ords, t0, side="right")) - 1
                pos[lo:hi] = 1.0 if level[k - 1] > level[j] else 0.0
        fri += timedelta(days=7)
    return pos


def mix(days: Sequence[date], a: np.ndarray, b: np.ndarray, w: float = 0.5) -> np.ndarray:
    """Returns of w in a and 1 - w in b, weights drifting, reset at each month's last session."""
    out = np.zeros(len(days))
    wa = w
    for i in range(1, len(days)):
        out[i] = wa * a[i] + (1 - wa) * b[i]
        wa = wa * (1 + a[i]) / (1 + out[i])
        if i + 1 == len(days) or days[i + 1].month != days[i].month:
            wa = w
    return out


# --- measures ---


def cagr(r: np.ndarray, days: Sequence[date]) -> float:
    yrs = (days[-1] - days[0]).days / 365.25
    return float(np.exp(np.log1p(r[1:]).sum() / yrs) - 1)


def sharpe_x(r: np.ndarray, rf: np.ndarray) -> tuple[float, float]:
    x = (r - rf)[1:]
    sr = float(x.mean() / x.std() * math.sqrt(252))
    yrs = len(x) / 252
    return sr, math.sqrt((1 + sr**2 / 2) / yrs)


def mdd(r: np.ndarray) -> float:
    eq = np.cumprod(1 + r)
    return float(1 - (eq / np.maximum.accumulate(eq)).min())


def zigzag(px: np.ndarray, down: float, up: float) -> list[tuple[int, int]]:
    """insure-1's zigzag: confirmed (peak, trough) index pairs (an unfinished fall at the end
    is closed at its lowest point so far, and flagged by the caller)."""
    out: list[tuple[int, int]] = []
    falling, pk, tr = False, 0, 0
    for i in range(1, len(px)):
        if not falling:
            if px[i] > px[pk]:
                pk = i
            elif px[i] <= px[pk] * (1 - down):
                falling, tr = True, i
        else:
            if px[i] < px[tr]:
                tr = i
            elif px[i] >= px[tr] * (1 + up):
                out.append((pk, tr))
                falling, pk = False, i
    if falling:
        out.append((pk, tr))
    return out


@dataclass
class Fall:
    peak: date
    trough: date
    hold: float  # simple loss of holding, peak -> trough
    loss: dict[str, float]  # simple return of each series, peak -> trough
    ins: dict[str, float]  # loss avoided, log points
    net: dict[str, float]  # ins + next 365 days (cut at the next peak), log points
    share: dict[str, float]

    @property
    def days(self) -> int:
        return (self.trough - self.peak).days


def falls(days: Sequence[date], series: dict[str, np.ndarray], hold: str) -> list[Fall]:
    eq = {k: np.cumprod(1 + v) for k, v in series.items()}
    px = eq[hold]
    pairs = zigzag(px, *FALL)
    ords = np.array([d.toordinal() for d in days])
    out = []
    for j, (a, b) in enumerate(pairs):
        e = int(np.searchsorted(ords, ords[b] + REBOUND, side="right")) - 1
        if j + 1 < len(pairs):
            e = min(e, pairs[j + 1][0])
        hl = 100 * math.log(px[b] / px[a])
        loss, ins, net, share = {}, {}, {}, {}
        for k, q in eq.items():
            loss[k] = float(q[b] / q[a] - 1)
            ins[k] = 100 * math.log(q[b] / q[a]) - hl
            net[k] = ins[k] + 100 * (math.log(q[e] / q[b]) - math.log(px[e] / px[b]))
            share[k] = ins[k] / abs(hl)
        out.append(Fall(days[a], days[b], float(px[b] / px[a] - 1), loss, ins, net, share))
    return out


def premium(r: np.ndarray, h: np.ndarray, ff: Sequence[Fall], k: str) -> float:
    """insure-1's pooled premium: log points given up outside the falls per point saved."""
    total = 100 * float(np.log1p(r[1:]).sum() - np.log1p(h[1:]).sum())
    si = sum(f.ins[k] for f in ff)
    return -(total - si) / si if si > 0 else math.inf


def cost_ratio(gap_pts: float, ff: Sequence[Fall], k: str) -> float:
    m = float(np.mean([f.ins[k] for f in ff])) if ff else 0.0
    return gap_pts / m if m > 0 else math.inf


def calendar_sharpe(r: np.ndarray, days: Sequence[date]) -> float:
    """tries.md convention: daily calendar returns (0 on closed days), x sqrt(365), rf 0."""
    n = (days[-1] - days[0]).days
    cal = np.zeros(n)
    for i in range(1, len(days)):
        cal[(days[i] - days[0]).days - 1] = r[i]
    return float(cal.mean() / cal.std() * math.sqrt(365))


# --- run ---


def load() -> tuple[list[date], dict[str, np.ndarray], np.ndarray, dict[str, Any]]:
    root = cache_root()
    raw = root / RAW
    cboe = {n: parse_cboe((raw / "cboe" / f"{n}.csv").read_text()) for n in ("PPUT", *SIDE)}
    tr_y = parse_yahoo(json.loads((raw / "yahoo" / "SP500TR.json").read_text()))
    yd = root / "yahoo-1d" / "2026-11-12"
    gspc = parse_yahoo(json.loads((yd / "^GSPC.json").read_text()))
    irx = parse_yahoo(json.loads((yd / "^IRX.json").read_text()))
    div = {}
    for line in (root / "derived" / "survey-4" / "shiller_div.csv").read_text().splitlines()[1:]:
        m, v = line.split(",")
        div[m] = float(v)
    early = built_tr({d: v for d, v in gspc.items() if WARM <= d <= LAST}, div)
    tr = splice(early, tr_y, SP500TR_FIRST)
    # check: the built series against the official one, 1988-2025
    common = sorted(set(early) & set(tr_y))
    b = np.array([early[d] for d in common])
    o = np.array([tr_y[d] for d in common])
    rb, ro = b[1:] / b[:-1] - 1, o[1:] / o[:-1] - 1
    yrs = (common[-1] - common[0]).days / 365.25
    chk = {
        "corr": float(np.corrcoef(rb, ro)[0, 1]),
        "cagr_gap": float((b[-1] / b[0]) ** (1 / yrs) - (o[-1] / o[0]) ** (1 / yrs)),
        "from": common[0], "to": common[-1],
    }  # fmt: skip
    # warm-up sessions: the TR index's own days before BASE; window: PPUT's days
    pput = cboe["PPUT"]
    win = sorted(d for d in pput if BASE <= d <= LAST)
    warm = sorted(d for d in tr if WARM <= d < BASE)
    full = warm + win
    lvl, miss_tr = align(full, tr)
    r_tr, pos = trend(full, lvl)
    k = len(warm)
    days = full[k:]
    hold = np.zeros(len(days))
    hold[1:] = lvl[k + 1 :] / lvl[k:-1] - 1
    rule = r_tr[k:].copy()
    rule[0] = 0.0
    pos = pos[k:]
    rf = bill_returns(days, irx)
    pp, miss_pp = align(days, pput)
    r_pp = np.zeros(len(days))
    r_pp[1:] = pp[1:] / pp[:-1] - 1
    trend_tb = rule + (1 - pos) * rf
    series = {
        "hold": hold, "trend": trend_tb, "PPUT": r_pp, "mix": mix(days, trend_tb, r_pp),
        "trend@cash0": rule, "mix@cash0": mix(days, rule, r_pp),
    }  # fmt: skip
    for n in SIDE:
        lv = cboe[n]
        first = max(SIDE_FIRST.get(n, min(lv)), min(lv))
        # first full month: from the last session of the month the index starts in
        nxt = date(first.year + first.month // 12, first.month % 12 + 1, 1)
        start = max(d for d in days if d < nxt)
        idx = days.index(start)
        sub = days[idx:]
        lv2 = {d: v for d, v in lv.items() if d >= start}
        if start not in lv2:
            lv2[start] = lv[max(d for d in lv if d <= start)]
        a, miss = align(sub, lv2)
        r = np.zeros(len(days))
        r[idx + 1 :] = a[1:] / a[:-1] - 1
        series[n] = r
        chk[f"{n}_start"], chk[f"{n}_miss"] = start, miss
    chk["miss_tr"], chk["miss_pput"] = miss_tr, miss_pp
    chk["trend_flips_yr"] = float(np.abs(np.diff(pos)).sum() / ((days[-1] - days[0]).days / 365.25))
    chk["trend_in"] = float(pos[1:].mean())
    chk["pos"] = pos  # window positions (insure-4 reuses them)
    return days, series, rf, chk


def stats_block(days: list[date], s: dict[str, np.ndarray], rf: np.ndarray,
                names: Sequence[str]) -> tuple[list[str], list[Fall]]:  # fmt: skip
    ff = falls(days, {n: s[n] for n in names}, "hold")
    ch = cagr(s["hold"], days)
    rows = []
    for n in names:
        g = cagr(s[n], days)
        sr, se = sharpe_x(s[n], rf)
        gap = 100 * (ch - g)
        mi = float(np.mean([f.ins[n] for f in ff])) if ff else math.nan
        ms = float(np.mean([f.share[n] for f in ff])) if ff else math.nan
        cr = cost_ratio(gap, ff, n) if n != "hold" else math.nan
        pr = premium(s[n], s["hold"], ff, n) if n != "hold" else math.nan
        rows.append(
            f"| {n} | {g:.2%} | {gap:+.2f} | {sr:.2f} ({se:.2f}) | {mdd(s[n]):.1%} | "
            f"{mi:+.1f} | {ms:.2f} | {cr:.3f} | {pr:.2f} |"
        )
    return rows, ff


HEAD = (
    "| Series | CAGR | Gap to hold, pts/yr | Sharpe above bills (SE) | Worst loss | "
    "Mean loss avoided per fall, log pts | Mean share avoided | Insurance cost | Premium P |\n"
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|"
)


def fall_table(ff: Sequence[Fall], names: Sequence[str]) -> list[str]:
    out = [
        "| Peak | Trough | Days | " + " | ".join(f"{n} loss" for n in names) + " |",
        "|---|---|---:|" + "---:|" * len(names),
    ]
    for f in ff:
        out.append(f"| {f.peak} | {f.trough} | {f.days} | "
                   + " | ".join(f"{f.loss[n]:+.1%}" for n in names) + " |")  # fmt: skip
    return out


def subset(ff: Sequence[Fall], names: Sequence[str], label: str) -> str:
    if not ff:
        return f"| {label} | 0 | " + " | ".join("-" for _ in names) + " |"
    cells = []
    for n in names:
        sh = np.mean([f.share[n] for f in ff])
        nt = np.mean([f.net[n] for f in ff])
        cells.append(f"{sh:.2f} / {nt:+.1f}")
    return f"| {label} | {len(ff)} | " + " | ".join(cells) + " |"


def tries_rows(days: list[date], s: dict[str, np.ndarray], chk: dict[str, Any]) -> list[str]:
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"
    spec = [
        ("hold-spx-tr@insure3", "hold", "baseline", "-"),
        ("tsmom12-spx-tr-bills@insure3", "trend", "robustness", f"{chk['trend_flips_yr']:.2f}"),
        ("tsmom12-spx-tr-cash0@insure3", "trend@cash0", "robustness",
         f"{chk['trend_flips_yr']:.2f}"),
        ("cboe-pput@insure3", "PPUT", "baseline", "12.00"),
        ("mix50-tsmom12-pput-bills@insure3", "mix", "robustness", "-"),
        ("mix50-tsmom12-pput-cash0@insure3", "mix@cash0", "robustness", "-"),
    ]  # fmt: skip
    for n in SIDE:
        spec.append((f"cboe-{n.lower()}@insure3", n, "baseline", "12.00"))
    out = []
    for var, key, kind, turn in spec:
        r = s[key]
        lo = 0 if key not in SIDE else days.index(chk[f"{key}_start"])
        d, x = days[lo:], r[lo:].copy()
        x[0] = 0.0
        out.append(
            f"| {now} | {IDEA} | {var} | {kind} | train | {d[0]} | {d[-1]} | "
            f"{calendar_sharpe(x, d):.2f} | {np.prod(1 + x) - 1:+.1%} | {mdd(x):.1%} | {turn} |"
        )
    return out


def main() -> None:
    days, s, rf, chk = load()
    names = ["hold", "trend", "PPUT", "mix", "trend@cash0", "mix@cash0"]
    rows, ff = stats_block(days, s, rf, names)
    md = [
        "# insure-3 results (generated by `research/lib/insure3.py`; do not edit)",
        "",
        f"Window {days[0]}..{days[-1]} ({len(days) - 1} sessions). Falls: zigzag "
        f"{FALL[0]:.0%} / {FALL[1]:.0%} on hold's daily closes. Insurance cost = gap to hold "
        "(points a year) / mean loss avoided per fall (log points). Premium P: insure-1's pooled "
        "premium (log points given up outside falls per log point saved in them).",
        "",
        "## Main table",
        "",
        HEAD,
        *rows,
        "",
        "## Every 15% fall",
        "",
        *fall_table(ff, names[:4]),
        "",
        "## By kind of fall: mean share avoided / mean net of the next 365 days (log pts)",
        "",
        "| Subset | Falls | " + " | ".join(names[:4]) + " |",
        "|---|---:|" + "---:|" * 4,
    ]
    named = [f for f in ff if any(lo <= f.trough <= hi for lo, hi in NAMED_FAST.values())]
    md.append(subset(named, names[:4], "named fast: 1987, 2020"))
    md.append(subset([f for f in ff if f.days <= FAST], names[:4], f"<= {FAST} days"))
    md.append(subset([f for f in ff if f.days > FAST], names[:4], f"> {FAST} days"))
    md.append(subset([f for f in ff if f.days > 365], names[:4], "> 365 days"))
    md.append(subset(ff, names[:4], "all"))
    md += ["", "Named fast falls, loss peak -> trough:", ""]
    for f in named:
        md.append(f"- {f.peak}..{f.trough} ({f.days} days): "
                  + ", ".join(f"{n} {f.loss[n]:+.1%}" for n in names[:4]))  # fmt: skip
    md += ["", "## Side table (each index from its first full month)", ""]
    for n in SIDE:
        lo = days.index(chk[f"{n}_start"])
        d = days[lo:]
        sub = {k: v[lo:].copy() for k, v in s.items()}
        for v in sub.values():
            v[0] = 0.0
        r2, f2 = stats_block(d, sub, rf[lo:], ["hold", "trend", "PPUT", "mix", n])
        md += [f"### {n}, {d[0]}..{d[-1]} ({chk[f'{n}_miss']} sessions carried)", "",
               HEAD, *r2, "", *fall_table(f2, ["hold", "trend", "PPUT", "mix", n]), ""]  # fmt: skip
    md += [
        "## Data checks",
        "",
        f"- Built S&P 500 total return (price + Shiller dividends) against Yahoo `^SP500TR`, "
        f"{chk['from']}..{chk['to']}: daily correlation {chk['corr']:.4f}, CAGR gap "
        f"{100 * chk['cagr_gap']:+.2f} points a year (the built series is used only before "
        f"{SP500TR_FIRST}).",
        f"- PPUT sessions in the window without an S&P level (carried): {chk['miss_tr']}; "
        f"PPUT gaps: {chk['miss_pput']}.",
        f"- Trend: in the market {chk['trend_in']:.0%} of sessions, "
        f"{chk['trend_flips_yr']:.2f} flips a year.",
        "",
    ]
    OUT.write_text("\n".join(md))
    print("\n".join(md))
    text = TRIES.read_text()
    new = [r for r in tries_rows(days, s, chk) if f"| {r.split(' | ')[2]} |" not in text]
    if new:
        with TRIES.open("a") as f:
            f.write("\n".join(new) + "\n")
    print(f"{len(new)} tries rows appended")


if __name__ == "__main__":
    main()
