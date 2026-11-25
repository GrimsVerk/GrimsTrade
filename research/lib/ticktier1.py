"""tick-tier-1: `tsmom12` and `e4` Sharpe above bills before and after 2009, by asset class.
Card: research/cards/tick-tier-1.md. Descriptive re-score (a `note` row, not a try).

    uv run python -I research/lib/ticktier1.py          # writes results/tick-tier-1.md (+ .json)
    uv run python -I research/lib/ticktier1.py --log    # and appends the note row to tries.md

Series and rules are pooled-1's 41 (`pooled1.load_all`, `pooled1_core.run_market`) and
pooled-2's 29 (`pooled2.load_nonequity`, `pooled2.run_specs`), unchanged. pooled-1's equity
returns get the US bill subtracted per unit of position (cash at the bill); pooled-2's already are
in excess of the bill. `hold` = the series itself, always invested. Nothing after 2025-10-31 is
parsed (the two loaders' guards).
"""

from __future__ import annotations

import json
import math
import sys
import warnings
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pooled1_core as pc  # noqa: E402
import pooled2_core as qc  # noqa: E402

IDEA = "tick-tier-1"
RULES = ("tsmom12", "e4", "hold")
TIMED = ("tsmom12", "e4")
PRE = (date(1995, 1, 1), date(2008, 12, 31))
POST = (date(2009, 1, 1), date(2025, 10, 31))
POST_2010 = (date(2010, 1, 1), date(2025, 10, 31))
PRE_2010 = (date(1995, 1, 1), date(2009, 12, 31))
MIN_WINDOW = {"w": 260, "m": 60}  # five years of periods in each window
BLOCK, DRAWS, SEED = 12, 2000, 0
CHECK_BLOCKS = (3, 24)
Z_READ = -2.0
CLASSES = ("EQ", "FX", "BD", "CM")
ETF_CLASS = {"IEF": "BD", "LQD": "BD", "DBC": "CM", "SLV": "CM"}
GROUP_CLASS = {"USB3": "BD", "GOV9": "BD", "FX9": "FX", "COM8": "CM"}
RESEARCH = Path(__file__).resolve().parents[1]
OUT = RESEARCH / "results" / "tick-tier-1.md"


def asset_class(name: str, group: str, as_is: bool = False) -> str:
    """The card's class of a series; `as_is` keeps pooled-1's 41 all in EQ (check)."""
    if group.startswith("EQ-"):
        return "EQ" if as_is else ETF_CLASS.get(name, "EQ")
    return GROUP_CLASS[group]


# --------------------------------------------------------------------------- windows


def month_sel(cal: np.ndarray, win: tuple[date, date]) -> np.ndarray:
    lo = qc.month_index(win[0].toordinal())
    hi = qc.month_index(win[1].toordinal())
    return (cal >= lo) & (cal <= hi)


def window_sharpe(c: qc.Cells, S: Sequence[np.ndarray]) -> np.ndarray:
    """Sharpe[rule, market] from total sums S = (n, s1, s2)[rule, market] (one year minimum)."""
    ppy = np.array([qc.PPY[f] for f in c.freq], dtype=float)
    mn = np.array([qc.MIN_PERIODS[f] for f in c.freq], dtype=float)
    return qc.sharpe_from(S[0], S[1], S[2], ppy, mn)


def eligible(c: qc.Cells, sels: Sequence[np.ndarray]) -> np.ndarray:
    """Series with at least five years of scored periods in every window."""
    need = np.array([MIN_WINDOW[f] for f in c.freq], dtype=float)
    ok = np.ones(len(c.names), dtype=bool)
    for sel in sels:
        ok &= c.S[0][0][:, sel].sum(-1) >= need
    return ok


def resample(S: Sequence[np.ndarray], block: int, rng: np.random.Generator) -> list[np.ndarray]:
    """One circular block draw of the months in S (sums over the drawn months), pooled-2's way."""
    nm = S[0].shape[-1]
    nb = -(-nm // block)
    tail = nm - (nb - 1) * block
    st = rng.integers(0, nm, nb)
    out = []
    for s in S:
        full = qc.block_sums(s, block)
        part = qc.block_sums(s, tail)
        out.append(full[..., st[:-1]].sum(-1) + part[..., st[-1]])
    return out


@dataclass
class Split:
    pre: np.ndarray  # Sharpe[rule, market]
    post: np.ndarray
    draws_pre: np.ndarray  # [draw, rule, market]
    draws_post: np.ndarray


def split(
    c: qc.Cells,
    pre: tuple[date, date] = PRE,
    post: tuple[date, date] = POST,
    block: int = BLOCK,
    draws: int = DRAWS,
    seed: int = SEED,
) -> tuple[Split, np.ndarray]:
    """Point and bootstrap window Sharpes; blocks drawn separately inside each window, the same
    months for every series. Returns (Split, eligible mask)."""
    sp, so = month_sel(c.cal, pre), month_sel(c.cal, post)
    Sp = [s[..., sp] for s in c.S]
    So = [s[..., so] for s in c.S]
    p0 = window_sharpe(c, [x.sum(-1) for x in Sp])
    o0 = window_sharpe(c, [x.sum(-1) for x in So])
    rng = np.random.default_rng(seed)
    dp = np.full((draws, *p0.shape), np.nan)
    do = np.full((draws, *o0.shape), np.nan)
    for b in range(draws):
        dp[b] = window_sharpe(c, resample(Sp, block, rng))
        do[b] = window_sharpe(c, resample(So, block, rng))
    return Split(p0, o0, dp, do), eligible(c, [sp, so])


# --------------------------------------------------------------------------- contrasts


def class_means(x: np.ndarray, cls: np.ndarray, ok: np.ndarray) -> dict[str, np.ndarray]:
    """Equal-weight nan-skipping mean over the eligible series of each class; x[..., market]."""
    out = {}
    for k in CLASSES:
        m = ok & (cls == k)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            out[k] = np.nanmean(x[..., m], axis=-1) if m.any() else np.full(x.shape[:-1], np.nan)
    return out


def contrasts(delta: np.ndarray, cls: np.ndarray, ok: np.ndarray) -> dict[str, np.ndarray]:
    """C (primary), C_4 (with commodities) and the market-weighted C, on x[..., market]."""
    k = class_means(delta, cls, ok)
    small = ok & np.isin(cls, ("EQ", "FX"))
    bd = ok & (cls == "BD")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        mw = np.nanmean(delta[..., small], axis=-1) - np.nanmean(delta[..., bd], axis=-1)
    return {
        **k,
        "C": (k["EQ"] + k["FX"]) / 2 - k["BD"],
        "C4": (k["EQ"] + k["FX"]) / 2 - (k["BD"] + k["CM"]) / 2,
        "Cmw": mw,
    }


def summarise_split(sp: Split, ok: np.ndarray, cls: np.ndarray) -> dict[str, Any]:
    """Per rule: class levels, class Deltas, contrasts, each with bootstrap SE; also the timing
    part (rule minus hold) for `tsmom12` and `e4`."""

    def est(point: np.ndarray, draws: np.ndarray) -> dict[str, float]:
        d = draws[np.isfinite(draws)]
        se = float(d.std(ddof=1)) if len(d) > 1 else math.nan
        v = float(point)
        return {"est": v, "se": se, "z": v / se if se > 0 else math.nan}

    out: dict[str, Any] = {}
    delta = sp.post - sp.pre
    ddelta = sp.draws_post - sp.draws_pre
    for a, r in enumerate(RULES):
        lv_pre = class_means(sp.pre[a], cls, ok)
        lv_post = class_means(sp.post[a], cls, ok)
        cp = contrasts(delta[a], cls, ok)
        cd = contrasts(ddelta[:, a], cls, ok)
        out[r] = {
            "pre": {k: float(v) for k, v in lv_pre.items()},
            "post": {k: float(v) for k, v in lv_post.items()},
            **{k: est(cp[k], cd[k]) for k in cp},
        }
    h = RULES.index("hold")
    for r in TIMED:
        a = RULES.index(r)
        cp = contrasts(delta[a] - delta[h], cls, ok)
        cd = contrasts(ddelta[:, a] - ddelta[:, h], cls, ok)
        out[f"{r}-timing"] = {k: est(cp[k], cd[k]) for k in cp}
    return out


def reading(s: Mapping[str, Any]) -> str:
    """The card's three readings on one rule's (or timing part's) contrasts."""
    c = s["C"]
    if c["est"] >= 0:
        return "not seen at the class level"
    if c["z"] <= Z_READ and s["EQ"]["est"] < 0 and s["FX"]["est"] < 0:
        return "consistent with the paper (class level)"
    return "inconclusive"


# --------------------------------------------------------------------------- data


def _bill_steps(d: np.ndarray, bill: list[tuple[date, float]]) -> np.ndarray:
    """Per session j: the bill earned from d[j-1] to d[j] (rate on or before d[j-1])."""
    bd = np.array([x.toordinal() for x, _ in bill], dtype=np.int64)
    bv = np.array([v for _, v in bill], dtype=float)
    out = np.zeros(len(d))
    idx = np.searchsorted(bd, d[:-1], side="right") - 1
    rate = np.where(idx >= 0, bv[np.maximum(idx, 0)], 0.0)
    out[1:] = rate / 100.0 * np.diff(d) / 365.0
    return out


def equity_markets(bill: list[tuple[date, float]] | None) -> list[qc.Mkt]:
    """pooled-1's 41 with `tsmom12`, `e4` (and `hold`) above the bill; None = cash at 0."""
    import pooled1 as p1

    out = []
    for m in p1.run_all(p1.load_all(), quiet=True):
        b = np.zeros(len(m.d)) if bill is None else _bill_steps(m.d, bill)
        bar = np.zeros(len(m.px))
        bar[1:] = m.px[1:] / m.px[:-1] - 1
        series = {r: m.daily[r] - m.pos[r] * b for r in TIMED}
        series["hold"] = bar - b
        mk = qc.Mkt(m.name, "EQ-" + m.group, "w", np.zeros(0, dtype=np.int64))
        for r, x in series.items():
            f, w = pc.weekly(m.d, x, m.start)
            mk.periods, mk.rets[r] = f, w
        out.append(mk)
    return out


def nonequity_markets() -> list[qc.Mkt]:
    """pooled-2's 29 (its run, unchanged) plus `hold` on the same periods."""
    import pooled2 as p2

    specs = p2.load_nonequity()
    runs = p2.run_specs(specs)
    for s, m in zip(specs, runs, strict=True):
        if s.freq == "w":
            assert s.d is not None and s.px_ret is not None and s.av is not None
            dec = qc.decide_weekly(s.d, s.px_ret, s.av)
            start = dec.first_ok + 1 + pc.LAG
            bar = np.zeros(len(s.px_ret))
            bar[1:] = s.px_ret[1:] / s.px_ret[:-1] - 1
            f, w = pc.weekly(s.d, bar, start)
            if not np.array_equal(f, m.periods):
                raise AssertionError(f"{s.name}: hold periods differ")
            m.rets["hold"] = w
        else:
            assert s.r_ret is not None
            h = s.r_ret[12 + s.gap :]
            if len(h) != len(m.periods):
                raise AssertionError(f"{s.name}: hold periods differ")
            m.rets["hold"] = h
    return runs


def published_check(eq0: list[qc.Mkt], ne: list[qc.Mkt]) -> dict[str, Any]:
    """Full-sample `tsmom12` Sharpe (pooled-1: cash at 0) against the logged robustness rows."""
    text = (RESEARCH / "tries.md").read_text()
    logged: dict[str, float] = {}
    for line in text.splitlines():
        cells = [x.strip() for x in line.split("|")]
        if (
            len(cells) > 8
            and cells[2] in ("pooled-1", "pooled-2")
            and cells[4] == "robustness"
            and cells[3].startswith("tsmom12@")
        ):
            logged[cells[2] + ":" + cells[3]] = float(cells[8])
    worst, n = 0.0, 0
    for m in eq0:
        k = f"pooled-1:tsmom12@{m.group[3:]}-{m.name}"
        if k in logged:
            worst = max(worst, abs(round(qc.stats(m, "tsmom12")[0], 2) - logged[k]))
            n += 1
    for m in ne:
        k = f"pooled-2:tsmom12@{m.group}-{m.name}"
        if k in logged:
            worst = max(worst, abs(round(qc.stats(m, "tsmom12")[0], 2) - logged[k]))
            n += 1
    return {"matched": n, "max_abs_diff": worst}


# --------------------------------------------------------------------------- report


def f2(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:+.2f}"


def est_cell(e: Mapping[str, float]) -> str:
    return f"{f2(e['est'])} ({e['se']:.2f}, z {f2(e['z'])})"


def report(res: dict[str, Any]) -> str:
    p = res["primary"]
    L = [
        "# tick-tier-1: results",
        "",
        f"Generated {res['generated']} by `research/lib/ticktier1.py`. Card: "
        "`research/cards/tick-tier-1.md`. Descriptive re-score: a `note` row, not a try.",
        "",
        f"Pre {PRE[0]}..{PRE[1]}, post {POST[0]}..{POST[1]}; Sharpe above the US bill "
        "(cash at the bill), at each series' frequency; series with at least five years in each "
        f"window: {res['n_eligible']} of {res['n_series']} "
        f"({', '.join(f'{k} {v}' for k, v in res['n_class'].items())}). SE: joint 12-month "
        f"circular block bootstrap inside each window, {DRAWS} draws, seed {SEED}.",
        "",
        "## Class mean Sharpe, before and after",
        "",
        "| Rule | " + " | ".join(f"{k} pre | {k} post | {k} Delta (SE)" for k in CLASSES) + " |",
        "|---|" + "---:|" * (3 * len(CLASSES)),
    ]
    for r in RULES:
        s = p[r]
        row = [
            f"{f2(s['pre'][k])} | {f2(s['post'][k])} | {f2(s[k]['est'])} ({s[k]['se']:.2f})"
            for k in CLASSES
        ]
        L.append(f"| `{r}` | " + " | ".join(row) + " |")
    L += [
        "",
        "## Contrasts (Delta small-tick classes minus Delta large-tick)",
        "",
        "C = (Delta_EQ + Delta_FX) / 2 - Delta_BD (primary). C_4 adds commodities to the large "
        "side, Cmw is market-weighted (both shown). Timing = the rule's Delta minus holding's.",
        "",
        "| Series | C (SE, z) | C_4 (SE, z) | Cmw (SE, z) | Reading (card) |",
        "|---|---|---|---|---|",
    ]
    for r in (*RULES, *(f"{x}-timing" for x in TIMED)):
        s = p[r]
        rd = res["readings"].get(r, "-")
        L.append(
            f"| `{r}` | {est_cell(s['C'])} | {est_cell(s['C4'])} | {est_cell(s['Cmw'])} | {rd} |"
        )
    L += [
        "",
        "## Checks (reported, not deciding)",
        "",
        "| Check | `tsmom12` C (SE, z) | `tsmom12` timing C | `e4` C | `e4` timing C |",
        "|---|---|---|---|---|",
    ]
    for name, s in res["checks"].items():
        L.append(
            f"| {name} | {est_cell(s['tsmom12']['C'])} | {est_cell(s['tsmom12-timing']['C'])} "
            f"| {est_cell(s['e4']['C'])} | {est_cell(s['e4-timing']['C'])} |"
        )
    pcx = res["published_check"]
    L += [
        "",
        f"Reproduction: full-sample `tsmom12` Sharpe of {pcx['matched']} series against their "
        f"logged pooled-1 / pooled-2 robustness rows, largest difference "
        f"{pcx['max_abs_diff']:.2f} (2-decimal rows).",
        "",
        "## Per series (eligible only)",
        "",
        "| Series | Class | `tsmom12` pre | post | `e4` pre | post | hold pre | post |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for m in res["series"]:
        if not m["eligible"]:
            continue
        v = m["sharpe"]
        L.append(
            f"| {m['name']} | {m['class']} | {f2(v['tsmom12'][0])} | {f2(v['tsmom12'][1])} | "
            f"{f2(v['e4'][0])} | {f2(v['e4'][1])} | {f2(v['hold'][0])} | {f2(v['hold'][1])} |"
        )
    skipped = [m["name"] for m in res["series"] if not m["eligible"]]
    L += ["", f"Not eligible (under five years in a window): {', '.join(skipped) or 'none'}.", ""]
    return "\n".join(L)


def analyse(markets: list[qc.Mkt], as_is: bool = False, **kw: Any) -> dict[str, Any]:
    c = qc.cells(markets, RULES)
    cls = np.array([asset_class(n, g, as_is) for n, g in zip(c.names, c.groups, strict=True)])
    sp, ok = split(c, **kw)
    return {"sum": summarise_split(sp, ok, cls), "sp": sp, "ok": ok, "cls": cls, "cells": c}


def main() -> None:
    import long_x_build as lb

    bill = lb.alfred("DTB3")
    eq = equity_markets(bill)
    eq0 = equity_markets(None)
    ne = nonequity_markets()
    base = analyse(eq + ne)
    s = base["sum"]
    c, ok, cls, sp = base["cells"], base["ok"], base["cls"], base["sp"]
    res: dict[str, Any] = {
        "generated": f"{datetime.now(UTC):%Y-%m-%d %H:%M} UTC",
        "primary": s,
        "readings": {r: reading(s[r]) for r in (*TIMED, *(f"{x}-timing" for x in TIMED))},
        "n_series": len(c.names),
        "n_eligible": int(ok.sum()),
        "n_class": {k: int((ok & (cls == k)).sum()) for k in CLASSES},
        "series": [
            {
                "name": n,
                "group": g,
                "class": str(cls[i]),
                "eligible": bool(ok[i]),
                "sharpe": {
                    r: [float(sp.pre[a, i]), float(sp.post[a, i])] for a, r in enumerate(RULES)
                },
            }
            for i, (n, g) in enumerate(zip(c.names, c.groups, strict=True))
        ],
        "published_check": published_check(eq0, ne),
        "checks": {},
    }
    checks: dict[str, dict[str, Any]] = {
        "break at 2010-01": dict(markets=eq + ne, pre=PRE_2010, post=POST_2010),
        "blocks of 3 months": dict(markets=eq + ne, block=3),
        "blocks of 24 months": dict(markets=eq + ne, block=24),
        "equity cash at 0": dict(markets=eq0 + ne),
        "pooled-1's 41 all in EQ": dict(markets=eq + ne, as_is=True),
    }
    for name, kw in checks.items():
        mk = kw.pop("markets")
        res["checks"][name] = analyse(mk, **kw)["sum"]
        print(f"  check {name} done", file=sys.stderr)
    OUT.write_text(report(res))
    OUT.with_suffix(".json").write_text(json.dumps(res, indent=1, default=float) + "\n")
    print(report(res))
    if "--log" in sys.argv:
        log_note(res)


def log_note(res: dict[str, Any]) -> None:
    tries = RESEARCH / "tries.md"
    text = tries.read_text()
    if f"| {IDEA} | re-score" in text:
        print("note row already logged", file=sys.stderr)
        return
    p = res["primary"]

    def c(r: str) -> str:
        e = p[r]["C"]
        return f"{e['est']:+.2f} (SE {e['se']:.2f})"

    t = p["tsmom12"]
    cls = " / ".join(
        f"{k} {t['pre'][k]:+.2f}->{t['post'][k]:+.2f}" for k in ("EQ", "FX", "BD", "CM")
    )
    body = (
        "re-score (not a try): tsmom12/e4 Sharpe above bills 1995-2008 vs 2009-2025-10 by asset "
        f"class on pooled-1/pooled-2 series ({res['n_eligible']} eligible); tsmom12 class means "
        f"{cls}; contrast C = (dEQ+dFX)/2 - dBD: tsmom12 {c('tsmom12')}, timing part "
        f"{c('tsmom12-timing')}, e4 {c('e4')}, e4 timing {c('e4-timing')}; reading: "
        f"{res['readings']['tsmom12']} (research/tick-tier-1.md)"
    )
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"
    with tries.open("a") as f:
        f.write(
            f"| {now} | {IDEA} | {body} | note | train | 1995-01-01 | 2025-10-31 "
            "| - | - | - | - |\n"
        )
    print("logged 1 note row", file=sys.stderr)


if __name__ == "__main__":
    main()
