"""Research run short-1: a short side on Binance USDT perpetuals (card in research/short-1.md).

    uv run python -I research/lib/short1.py [--log] [--cost30]

Reuses breadth-1's cached aggregates (spot daily closes, signals, funding events). Writes the
tables to research/results/short-1.md. Without `--log` nothing is written to tries.md.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import short_engine as se  # noqa: E402
import stats  # noqa: E402

ERAS = [(2020, 2021), (2022, 2025)]
PERP_COST, SPOT_COST, HIGH_COST = 0.001, 0.003, 0.003
OUT = Path(__file__).resolve().parents[1] / "results" / "short-1.md"
WEEKLY_LS = ["low_vol", "size", "turnover", "funding", "premium", "trend", "combo"]


def funding_panel(book: bb.Book) -> tuple[np.ndarray, np.ndarray]:
    """(sum of funding rates per return day, perp alive: an event in the two days up to t)."""
    n_days = book.px.shape[0]
    t0 = int(datetime.combine(book.day0, datetime.min.time(), UTC).timestamp())
    fund = np.zeros_like(book.px)
    cnt = np.zeros_like(book.px)
    for j, s in enumerate(book.names):
        p = bb.derived() / f"binance-{s}-funding.npz"
        if not p.exists():
            continue
        z = np.load(p)
        if "ft" not in z:
            continue
        day = (z["ft"] - 1 - t0) // 86400  # event at 00:00 of t+1 belongs to return day t
        k = (day >= 0) & (day < n_days)
        fund[:, j] = np.bincount(day[k], weights=z["fr"][k], minlength=n_days)
        cnt[:, j] = np.bincount(day[k], minlength=n_days)
    alive = (cnt > 0) | (np.vstack([np.zeros((1, cnt.shape[1])), cnt[:-1]]) > 0)
    return fund, alive


@dataclass
class Shape:
    name: str
    kind: str  # variant | baseline
    targets: np.ndarray
    base: np.ndarray
    spot: bool = False  # spot twin: no funding, 30 bps
    meta: dict[str, object] = field(default_factory=dict)


def build(
    book: bb.Book, tradable: np.ndarray, cols: list[int], min_n: int
) -> tuple[list[Shape], int]:
    n_days, n = book.px.shape
    sub = np.zeros(n, bool)
    sub[cols] = True
    s0 = int(np.argmax((tradable & sub).sum(1) >= min_n))
    dec_w, _ = bb.decisions(book, "weekly", s0)
    dec_d, _ = bb.decisions(book, "daily", s0)
    dw, _, _ = xs.schedule(n_days, dec_w, 0)
    dd, _, _ = xs.schedule(n_days, dec_d, 0)
    dd = dd[dd >= dw[0]]
    sig = dict(book.signals)
    sig["size"] = -book.signals["size"]  # long large (breadth-1's measured sign)
    sig["trend"] = book.signals["mom_365"]
    shapes: list[Shape] = []

    def mask(t: int) -> np.ndarray:
        return tradable[t] & sub & np.isfinite(book.px[t])

    def tw(fn: object, dec: np.ndarray) -> np.ndarray:
        return np.array([fn(t, mask(t)) for t in dec])  # type: ignore[operator]

    def ts(t: int, m: np.ndarray, short: bool, long: bool = True) -> np.ndarray:
        nm = max(m.sum(), 1)
        up = book.up[t]
        w = np.where(m & up, 1.0 / nm, 0.0) if long else np.zeros(n)
        return w - np.where(m & ~up, 1.0 / nm, 0.0) if short else w

    shapes.append(Shape("tsmom12 spot", "baseline", tw(lambda t, m: ts(t, m, False), dw), dw, True))
    shapes.append(Shape("tsmom12 perp", "baseline", tw(lambda t, m: ts(t, m, False), dw), dw))
    shapes.append(Shape("EW perp", "baseline", tw(lambda t, m: m / max(m.sum(), 1), dw), dw))
    shapes.append(Shape("tsmom12-ls", "variant", tw(lambda t, m: ts(t, m, True), dw), dw))
    if len(cols) >= 10:

        def combo(t: int, m: np.ndarray) -> np.ndarray:
            ks = ("low_vol", "size", "turnover", "funding")
            rk = np.vstack([se.rank01(sig[k][t], m) for k in ks])
            ok = np.isfinite(rk).sum(0) >= 2
            with np.errstate(invalid="ignore"):
                v = np.where(ok, np.nanmean(np.where(np.isfinite(rk), rk, np.nan), 0), np.nan)
            return v

        sig_at = {k: (lambda t, k=k: sig[k][t]) for k in WEEKLY_LS if k != "combo"}
        sig_at["combo"] = lambda t: combo(t, mask(t))
        for k in WEEKLY_LS:
            f = sig_at[k]
            w = tw(lambda t, m, f=f: se.long_short(f(t), m & np.isfinite(f(t))), dw)
            shapes.append(Shape(f"ls-{k}", "variant", w, dw))
        r1 = sig["rev_1"]
        w = tw(lambda t, m: se.long_short(r1[t], m & np.isfinite(r1[t])), dd)
        shapes.append(Shape("ls-rev_1 (daily)", "variant", w, dd))
    return shapes, int(dw[0])


def worst_week(r: np.ndarray) -> float:
    eq = np.cumprod(1 + r)
    return float((eq[7:] / eq[:-7] - 1).min()) if len(r) > 7 else float("nan")


def era_sharpes(day0: object, first: int, r: np.ndarray) -> list[float | None]:
    yrs = np.array([(day0 + timedelta(days=first + i)).year for i in range(len(r))])  # type: ignore[operator]
    out: list[float | None] = []
    for y0, y1 in ERAS:
        m = (yrs >= y0) & (yrs <= y1)
        out.append(stats.sharpe(r[m]) if m.sum() >= 180 else None)
    return out


def run_book(
    label: str,
    book: bb.Book,
    fund: np.ndarray,
    tradable: np.ndarray,
    cols: list[int],
    min_n: int,
    log: bool,
) -> dict[str, object]:
    shapes, b0 = build(book, tradable, cols, min_n)
    first = b0 + 1
    years = (book.px.shape[0] - b0) / 365
    res: dict[str, dict[str, object]] = {}
    series: dict[str, np.ndarray] = {}
    for sh in shapes:
        for cost in (PERP_COST, HIGH_COST):
            if sh.spot and cost != PERP_COST:
                continue
            c = SPOT_COST if sh.spot else cost
            run = se.simulate(book.px, None if sh.spot else fund, sh.targets, sh.base, c, b0)
            key = sh.name if cost == PERP_COST else f"{sh.name} @30"
            series[key] = run.r
            turn = float(np.abs(np.diff(sh.targets, axis=0)).sum() / years)
            res[key] = {
                "sharpe": stats.sharpe(run.r),
                "cagr": stats.cagr(run.r),
                "mdd": stats.max_drawdown(run.r),
                "worst_week": worst_week(run.r),
                "eras": era_sharpes(book.day0, first, run.r),
                "funding_yr": float(run.funding.sum() / years),
                "turn_yr": turn,
                "max_gross": float(run.gross.max()),
                "min_day": float(run.r.min()),
            }
            if log:
                kind = sh.kind if cost == PERP_COST else "robustness"
                cdesc = "spot 30 bps" if sh.spot else f"perp {cost * 1e4:.0f} bps + funding"
                bb.log_row(
                    f"short-1-{label}",
                    f"{sh.name}, {cdesc}",
                    kind,
                    book.day0 + timedelta(days=first),
                    run.r,
                    turn,
                )
    tw = series["tsmom12 spot"]
    tp = series["tsmom12 perp"]
    for key, r in series.items():
        row = res[key]
        row["corr_ts"] = float(np.corrcoef(r, tw)[0, 1])
        if key.startswith("ls-"):
            blend = 0.5 * tw + 0.5 * r
            d, p, _, _ = stats.sharpe_diff_boot(blend, tw)
            row |= {
                "blend_sharpe": stats.sharpe(blend),
                "blend_diff": d,
                "blend_p": p,
                "blend_mdd": stats.max_drawdown(blend),
                "blend_eras": era_sharpes(book.day0, first, blend),
                "dd_spells": se.dd_spells(r),
            }
        if key.startswith("tsmom12-ls"):
            d, p, _, _ = stats.sharpe_diff_boot(r, tw)
            d2, p2, _, _ = stats.sharpe_diff_boot(r, tp)
            row |= {"diff_spot": d, "p_spot": p, "diff_perp": d2, "p_perp": p2}
    ts_row = res["tsmom12 spot"]
    for key, row in res.items():
        row["verdict"] = verdict(key, row, ts_row, res)
    # episodes
    sub = np.zeros(book.px.shape[1], bool)
    sub[cols] = True
    down = ~book.up & tradable & sub
    per_coin = sum(se.spells(down[b0:, j]) for j in cols)
    btc = book.names.index("BTCUSDT")
    eps = {
        "weeks": int(len([s for s in shapes if s.name == "tsmom12-ls"][0].base)),
        "short_spells_all_coins": int(per_coin),
        "short_spells_btc": int(se.spells(down[b0:, btc])),
        "coins": len(cols),
        "first": str(book.day0 + timedelta(days=first)),
        "tradable_median": float(np.median((tradable & sub)[b0:].sum(1))),
    }
    return {"label": label, "rows": res, "episodes": eps}


def verdict(
    key: str, row: dict[str, object], ts_row: dict[str, object], res: dict[str, dict[str, object]]
) -> str:
    if key.endswith("@30"):
        return ""
    eras_ts = ts_row["eras"]
    if key.startswith("ls-"):
        eras = [e for e in row["eras"] if e is not None]  # type: ignore[union-attr]
        r30 = res.get(f"{key} @30", {})
        bars = [
            row["blend_p"] < 0.10,  # type: ignore[operator]
            row["sharpe"] > 0 and all(e > 0 for e in eras),  # type: ignore[operator]
            row["blend_mdd"] <= ts_row["mdd"] + 0.05,  # type: ignore[operator]
            row["mdd"] <= ts_row["mdd"],  # type: ignore[operator]
            bool(r30) and r30.get("blend_p", 1) < 0.20 and r30.get("sharpe", -1) > 0,  # type: ignore[operator]
        ]
    elif key == "tsmom12-ls":
        ahead = [
            a > b
            for a, b in zip(row["eras"], eras_ts, strict=True)
            if a is not None and b is not None
        ]  # type: ignore[arg-type, operator]
        bars = [
            row["p_spot"] < 0.10 and row["diff_perp"] >= 0,  # type: ignore[operator]
            bool(ahead) and all(ahead),
            row["mdd"] <= ts_row["mdd"] + 0.05,  # type: ignore[operator]
        ]
    else:
        return ""
    failed = [str(i + 1) for i, ok in enumerate(bars) if not ok]
    return "PASS" if not failed else "fails " + ",".join(failed)


def f2(x: object, pct: bool = False) -> str:
    if x is None:
        return "-"
    return f"{x:.0%}" if pct else f"{x:+.2f}" if isinstance(x, float) else str(x)


COLS = [
    "Shape",
    "Sharpe",
    "CAGR",
    "Max DD",
    "Worst week",
    "2020-21",
    "2022-25",
    "Funding/yr",
    "Turn/yr",
    "Corr ts",
    "vs tsmom12 (p)",
    "Blend Sharpe",
    "Blend - ts (p)",
    "Blend DD",
    "DD>10% spells",
    "Verdict",
]


def table(out: dict[str, Any]) -> str:
    rows: dict[str, dict[str, Any]] = out["rows"]
    e: dict[str, Any] = out["episodes"]
    intro = (
        f"From {e['first']} (first return day) to 2025-11-10. Coins: {e['coins']}, tradable"
        f" per day median {e['tradable_median']:.0f}. Weekly decisions: {e['weeks']}. Short"
        " spells of `tsmom12-ls` (365-day return < 0, gaps < 30 days merged, >= 30 days):"
        f" {e['short_spells_all_coins']} over all coins, {e['short_spells_btc']} for BTC."
    )
    lines = [f"### Book {out['label']}", "", intro, "", "| " + " | ".join(COLS) + " |"]
    lines.append("|---|" + "---:|" * (len(COLS) - 2) + "---|")
    for k, r in rows.items():
        e1, e2 = r["eras"]
        vs = ""
        if "diff_spot" in r:
            vs = f"{r['diff_spot']:+.2f} ({r['p_spot']:.2f}); perp {r['diff_perp']:+.2f}"
        bl = ["", "", "", ""]
        if "blend_p" in r:
            bl = [
                f"{r['blend_sharpe']:.2f}",
                f"{r['blend_diff']:+.2f} ({r['blend_p']:.2f})",
                f"{r['blend_mdd']:.0%}",
                str(r["dd_spells"]),
            ]
        cells = [
            k,
            f"{r['sharpe']:.2f}",
            f"{r['cagr']:+.1%}",
            f"{r['mdd']:.0%}",
            f"{r['worst_week']:+.0%}",
            f2(e1),
            f2(e2),
            f"{r['funding_yr']:+.1%}",
            f"{r['turn_yr']:.0f}",
            f"{r['corr_ts']:+.2f}",
            vs,
            *bl,
            r["verdict"],
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    log = "--log" in sys.argv
    book = bb.binance_book()
    fund, alive = funding_panel(book)
    tradable = book.elig & alive
    all_cols = list(range(len(book.names)))
    two = [book.names.index("BTCUSDT"), book.names.index("ETHUSDT")]
    outs = [
        run_book("P30", book, fund, tradable, all_cols, 10, log),
        run_book("BTC-ETH", book, fund, tradable, two, 1, log),
    ]
    head = (
        "# Short 1: raw tables (train, decisions to 2025-11-09)\n\n"
        "Script `lib/short1.py`; card and reading in `research/short-1.md`. Perp shapes at"
        " 10 bps a side plus every funding event; `@30` rows: the same at 30 bps (robustness)."
        " `tsmom12 spot`: long-only on spot at 30 bps, no funding (the twin). Sharpe on daily"
        " returns, 365 days. `Funding/yr`: funding received (+) or paid (-) per year, share of"
        " equity. `Corr ts`: daily correlation with `tsmom12 spot`. `vs tsmom12 (p)`: Sharpe"
        " difference to the spot twin, bootstrap one-sided p, and to the perp long-only twin."
        " Blend: 50% `tsmom12 spot` + 50% the long-short book, re-split daily. Verdict: the"
        " card's bars that failed, by number.\n\n"
    )
    OUT.write_text(head + "\n".join(table(o) for o in outs))
    (bb.derived().parent / "short-1").mkdir(exist_ok=True)
    (bb.derived().parent / "short-1" / "results.json").write_text(
        json.dumps(outs, indent=1, default=str)
    )
    print(OUT.read_text())


if __name__ == "__main__":
    main()
