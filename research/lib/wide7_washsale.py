"""Lane wide-7, step 1: event-study gate for W14 `wash-sale-echo` (research/wide-7.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).

Run: `uv run python -I research/lib/wide7_washsale.py`  (DRY=1: asset-year counts only)
Output: research/results/wash-sale-echo.md
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide6_rules as r6  # noqa: E402
import wide7_rules as r  # noqa: E402

ETFS = ["SPY", "QQQ", "IWM", "XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY",
        "EFA", "EEM", "VNQ", "TLT", "IEF", "LQD", "GLD", "SLV", "DBC"]  # fmt: skip
COINS = ["BTC", "ETH", "LTC", "XRP", "BCH", "ETC", "DASH", "XLM"]
YEARS = range(1993, 2025)
SPLIT = 2012  # in-sample tax years < 2012, post-sample >= 2012
OUT = Path(__file__).resolve().parents[1] / "results" / "wash-sale-echo.md"
DRY = bool(os.environ.get("DRY"))

Row = tuple[str, int, dict[str, float]]


def panel(syms: list[str]) -> list[Row]:
    hist = harness.load_history("train", syms=syms)
    rows: list[Row] = []
    for s in syms:
        days = [b.date for b in hist[s]]
        logc = np.log(np.array([b.close for b in hist[s]]))
        for y in YEARS:
            v = r.wash_sale_year(days, logc, y, harness.TRAIN_LAST_BAR)
            if v is not None:
                rows.append((s, y, v))
    return rows


def fit(rows: list[Row], target: str, dose: str = "loss", fe: bool = True) -> tuple[float, float]:
    if len(rows) < 5 or len({y for _, y, _ in rows}) < 2:
        return float("nan"), float("nan")
    years = [y for _, y, _ in rows]
    yv = np.array([v[target] for _, _, v in rows])
    d = np.array([v[dose] for _, _, v in rows])[:, None]
    base = r.year_dummies(years) if fe else np.ones((len(rows), 1))
    beta, t = r6.ols_dk(yv, np.hstack([d, base]), years, 0)
    return float(beta[0]), float(t[0])


def cell(rows: list[Row], target: str, dose: str = "loss", fe: bool = True) -> str:
    b, t = fit(rows, target, dose, fe)
    return f"{b:+.3f} ({t:+.2f})"


def main() -> None:
    etf, coin = panel(ETFS), panel(COINS)
    parts = {
        "ETF in-sample 1993-2011": [x for x in etf if x[1] < SPLIT],
        "ETF post-sample 2012-2024": [x for x in etf if x[1] >= SPLIT],
        "ETF all 1993-2024": etf,
        "Coins 2013-2018": [x for x in coin if x[1] < 2019],
        "Coins 2019-2024": [x for x in coin if x[1] >= 2019],
        "Coins all": coin,
    }
    if DRY:
        for k, rows in parts.items():
            n_loss = sum(v["loss"] > 0 for _, _, v in rows)
            print(k, len(rows), n_loss, len({y for _, y, _ in rows}))
        return
    b_in, t_in = fit(parts["ETF in-sample 1993-2011"], "echo")
    b_post, t_post = fit(parts["ETF post-sample 2012-2024"], "echo")
    b_all, _ = fit(etf, "echo")
    b_coin, _ = fit(coin, "echo")
    passed = b_in > 0 and t_in >= 2 and b_post > 0 and t_post >= 2 and b_coin < b_all
    out = [
        "# Wash-sale echo: event-study gate (wide-7, W14)",
        "",
        "Rule: `research/wide-7.md` (pushed before this ran). Script",
        "`research/lib/wide7_washsale.py`.",
        "Slope b of a window's log return on the November YTD loss L = max(0, -YTD), year fixed",
        "effects, t clustered by year (no small-sample correction). Echo = calendar days",
        "S+31..S+45 after the third Friday of December S; turn of year = 31 Dec..10 Jan; late",
        "placebo = S+46..S+60.",
        "",
        "## Gate",
        "",
        "| Test | b (t) | Needed |",
        "|---|---:|---|",
        f"| ETF echo, tax years 1993-2011 | {b_in:+.3f} ({t_in:+.2f}) | b > 0, t >= 2 |",
        f"| ETF echo, tax years 2012-2024 | {b_post:+.3f} ({t_post:+.2f}) | b > 0, t >= 2 |",
        f"| Coin echo b below ETF echo b (all years) | {b_coin:+.3f} vs {b_all:+.3f} | yes |",
        "",
        f"**Gate: {'PASS' if passed else 'fail'}.**",
        "",
        "## Shown",
        "",
        "| Sample | Asset-years (with a loss, years) | Echo | Turn of year | Late placebo |"
        " Echo on YTD | Echo, no year effects |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for k, rows in parts.items():
        n_loss = sum(v["loss"] > 0 for _, _, v in rows)
        n_y = len({y for _, y, _ in rows})
        out.append(
            f"| {k} | {len(rows)} ({n_loss}, {n_y}) | {cell(rows, 'echo')} | "
            f"{cell(rows, 'toy')} | {cell(rows, 'late')} | {cell(rows, 'echo', 'ytd')} | "
            f"{cell(rows, 'echo', fe=False)} |"
        )
    out += [
        "",
        "Echo on YTD: the slope on the signed YTD return (a positive slope on a loss is a",
        "negative slope on YTD).",
        "",
        "## Mean echo return of losers minus non-losers, by tax year (ETFs, bps)",
        "",
        "| Tax year | Losers | Others | Losers minus others |",
        "|---|---:|---:|---:|",
    ]
    for y in YEARS:
        lo = [v["echo"] for _, yy, v in etf if yy == y and v["loss"] > 0]
        hi = [v["echo"] for _, yy, v in etf if yy == y and v["loss"] == 0]
        if lo and hi:
            dm = (np.mean(lo) - np.mean(hi)) * 1e4
            out.append(f"| {y} | {len(lo)} | {len(hi)} | {dm:+.0f} |")
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
