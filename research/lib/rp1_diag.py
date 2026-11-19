"""rp-1 step 1: why `where-vol` lost more than live risk-parity funds in 2022. Descriptive only.

    uv run python -I research/lib/rp1_diag.py <cache_root>

Re-scores two configurations already in `tries.md` (`where-vol`, `tsmom12`) through the harness
with `log=False` (no new strategy, nothing selectable), reads their target weights, and sets them
against the live risk-parity funds of survey-5 (ABRZX, AQRIX, RPAR; NAV with distributions, from
`<cache_root>/derived/survey-5/`). Fund exposures are read by trailing 63-day regressions of the
fund's daily return on SPY, TLT, GLD and DBC (US proxies; the funds hold global books, so the
betas are approximate). Nothing after 2023-12 is read. Writes `research/results/rp-1-diag.md`.
"""

from __future__ import annotations

import csv
import math
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common as c  # noqa: E402
import numpy as np  # noqa: E402
import stats  # noqa: E402
import trend_tune as tt  # noqa: E402
import trend_where as tw  # noqa: E402

IDEA = "rp-1"
SIX = ["SPY", "QQQ", "TLT", "GLD", "BTC", "ETH"]
FACT = ["SPY", "TLT", "GLD", "DBC"]
FUNDS = ["ABRZX", "AQRIX", "RPAR"]
Y0, Y1 = date(2021, 7, 1), date(2023, 12, 31)  # nothing outside this is read for 2022 tables
CAL22 = (date(2022, 1, 1), date(2022, 12, 31))
SHOCK = (date(2022, 1, 3), date(2022, 10, 12))  # the protocol's 2022 rate-shock window
WIN = 63  # trailing business days for fund betas and correlations
OUT = Path(__file__).resolve().parents[1] / "results" / "rp-1-diag.md"


def cal_days(a: date, b: date) -> list[date]:
    return [a + timedelta(days=k) for k in range((b - a).days + 1)]


def asset_rets(panel: object, s: str, days: list[date]) -> np.ndarray:
    """Close-to-close return credited to the calendar day of the later close (0 on no-bar days)."""
    o, px = panel.ord[s], panel.c[s]  # type: ignore[attr-defined]
    pos = {int(d): i for i, d in enumerate(o)}
    out = np.zeros(len(days))
    for k, d in enumerate(days):
        i = pos.get(d.toordinal())
        if i is not None and i > 0:
            out[k] = px[i] / px[i - 1] - 1
    return out


def closes(panel: object, s: str) -> dict[date, float]:
    o, p = panel.ord[s], panel.c[s]  # type: ignore[attr-defined]
    return {date.fromordinal(int(x)): float(y) for x, y in zip(o, p, strict=True)}


def fund_px(root: Path, t: str) -> dict[date, float]:
    out = {}
    with (root / "derived" / "survey-5" / f"{t}.csv").open() as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if date(2021, 1, 1) <= d <= Y1:
                out[d] = float(row["adjclose"])
    return out


def weights_by_day(run: c.Run, days: list[date]) -> np.ndarray:
    """Target weights in force for each calendar day's return: the latest decision strictly
    before that day (Friday's decision earns from the next bar)."""
    dec = sorted((d.time.date(), d.weights) for d in run.decisions)
    w = np.zeros((len(days), len(SIX)))
    j, cur = 0, {}
    for k, d in enumerate(days):
        while j < len(dec) and dec[j][0] < d:
            cur = dec[j][1]
            j += 1
        w[k] = [cur.get(s, 0.0) for s in SIX]
    return w


def comp(r: np.ndarray) -> float:
    return float(np.prod(1 + r) - 1)


def pct(x: float) -> str:
    return "-" if math.isnan(x) else f"{100 * x:+.1f}%"


def main(root: Path) -> None:
    six = c.ctx("six")
    etf = c.ctx("etf")
    strategies = {
        "where-vol": tw.Where("vol").strategy(),
        "tsmom12": c.weekly(c.slots(c.tsmom_signal)),
    }
    runs = {k: c.go(IDEA, k, f, six, "baseline", log=False) for k, f in strategies.items()}
    lines = ["# rp-1 step 1: `where-vol` in 2022 against live risk-parity funds", ""]
    lines += [
        "Descriptive. Script `lib/rp1_diag.py`. `where-vol` and `tsmom12` are re-scores of logged "
        "configurations (`log=False`; no new row). Returns are total returns, cash earns 0 (the "
        "gym's rule), so 2022 figures are about 1.5 points above survey-5's excess-of-bills ones. "
        "Funds: NAV with distributions (after fees). Nothing after 2023-12 is read.",
        "",
    ]
    lines.append(
        "Re-scores (full train, repo Sharpe): "
        + ", ".join(f"`{k}` {stats.sharpe(r.rets):.2f}" for k, r in runs.items())
        + "."
    )
    lines.append("")

    # 1. the yes/no answers in force around 2022
    lines += ["## 1. Which slots had the filter (yes) or were simply held (no)", ""]
    lines += [
        "Refit = first Friday of the year; out/in = daily volatility of the asset's own "
        "bars while `tsmom12` was out / in, all bars visible at the refit.",
        "",
    ]
    lines += ["| Refit | " + " | ".join(SIX) + " |", "|---|" + "---|" * len(SIX)]
    wv = tw.Where("vol")
    for y in (2020, 2021, 2022, 2023):
        ff = tt.first_friday(y)
        cells = []
        for s in SIX:
            e = wv.evidence(six.panel, s, ff)
            tag = "yes" if e.keep else "**no**"
            ratio = e.out / e.inn if e.inn else math.nan
            cells.append(f"{tag} ({ratio:.2f})" if not math.isnan(ratio) else tag)
        lines.append(f"| {ff} | " + " | ".join(cells) + " |")
    lines += ["", "(ratio = out-bar vol / in-bar vol; yes needs > 1, or thin evidence)", ""]

    # 2. weights through 2022
    days = cal_days(Y0, Y1)
    k22 = [i for i, d in enumerate(days) if CAL22[0] <= d <= CAL22[1]]
    ks = [i for i, d in enumerate(days) if SHOCK[0] <= d <= SHOCK[1]]
    R = np.column_stack([asset_rets(six.panel, s, days) for s in SIX])
    W = {k: weights_by_day(r, days) for k, r in runs.items()}
    lines += ["## 2. Target weights by month, 2022 (mean over the month's days)", ""]
    for name, w in W.items():
        lines += [
            f"`{name}`:",
            "",
            "| Month | " + " | ".join(SIX) + " | Invested |",
            "|---|" + "---:|" * (len(SIX) + 1),
        ]
        for m in range(1, 13):
            idx = [i for i in k22 if days[i].month == m]
            mw = w[idx].mean(axis=0)
            lines.append(
                f"| 2022-{m:02d} | " + " | ".join(f"{x:.2f}" for x in mw) + f" | {mw.sum():.2f} |"
            )
        lines.append("")

    # 3. attribution
    lines += [
        "## 3. Where the 2022 loss came from (arithmetic sum of daily weight x asset "
        "return; residual = gym minus this: costs, fills, compounding)",
        "",
    ]
    lines += [
        "| Book, window | " + " | ".join(SIX) + " | Sum | Gym | Residual |",
        "|---|" + "---:|" * (len(SIX) + 3),
    ]
    attrib: dict[str, np.ndarray] = {}
    for name, w in W.items():
        run = runs[name]
        for lab, idx in (("cal. 2022", k22), ("rate shock", ks)):
            contrib = (w[idx] * R[idx]).sum(axis=0)
            if lab == "cal. 2022":
                attrib[name] = contrib
            a, b = days[idx[0]] - timedelta(days=1), days[idx[-1]]
            gym = comp(run.rets_between(a, b))
            lines.append(
                f"| `{name}`, {lab} | "
                + " | ".join(pct(x) for x in contrib)
                + f" | {pct(contrib.sum())} | {pct(gym)} | {pct(gym - contrib.sum())} |"
            )
    asset22 = [comp(R[k22, j]) for j in range(len(SIX))]
    lines.append("| asset itself, cal. 2022 | " + " | ".join(pct(x) for x in asset22) + " | | | |")
    lines.append("")

    # 4. funds: 2022 return, betas, vol
    bd = [d for d in etf.panel.grid_dates if Y0 <= d <= Y1]  # business days
    px = {s: closes(six.panel, s) for s in ("SPY", "TLT", "GLD")}
    px |= {s: closes(etf.panel, s) for s in ("DBC", "IEF")}
    for f in FUNDS:
        px[f] = fund_px(root, f)
    common = [d for d in bd if all(d in px[k] for k in [*FACT, *FUNDS])]
    pairs = list(zip(common[:-1], common[1:], strict=True))
    br = {k: np.array([px[k][b] / px[k][a] - 1 for a, b in pairs]) for k in px}
    bdays = common[1:]
    X = np.column_stack([br[k] for k in FACT])
    rc = np.mean([br[f] for f in FUNDS], axis=0)  # equal-weight composite, daily rebalanced
    br["RC"] = rc
    i22 = [i for i, d in enumerate(bdays) if CAL22[0] <= d <= CAL22[1]]

    lines += ["## 4. The live risk-parity funds in 2022", ""]
    lines += ["Calendar 2022 total return (NAV with distributions):", ""]
    lines += [
        "| | " + " | ".join([*FUNDS, "RC", *FACT, "IEF"]) + " |",
        "|---|" + "---:|" * (len(FUNDS) + 2 + len(FACT)),
    ]
    lines.append(
        "| 2022 | " + " | ".join(pct(comp(br[k][i22])) for k in [*FUNDS, "RC", *FACT, "IEF"]) + " |"
    )
    lines.append("")

    def betas(y: np.ndarray, end: int) -> np.ndarray:
        a = max(end - WIN, 0)
        Xa = np.column_stack([np.ones(end - a), X[a:end]])
        coef, *_ = np.linalg.lstsq(Xa, y[a:end], rcond=None)
        return coef

    lines += [
        f"Trailing {WIN}-day betas on SPY / TLT / GLD / DBC at each quarter end "
        "(the exposure the fund carried into the next quarter), and its annualised vol "
        "over the same window. `where-vol`'s own weights are its targets, for scale "
        "(TLT weight is directly comparable with a TLT beta).",
        "",
    ]
    lines += [
        "| Date | Book | SPY | TLT | GLD | DBC | Sum | Vol |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    qends = [
        date(2021, 12, 31),
        date(2022, 3, 31),
        date(2022, 6, 30),
        date(2022, 9, 30),
        date(2022, 12, 31),
    ]
    wv_w = W["where-vol"]
    for q in qends:
        end = max(i for i, d in enumerate(bdays) if d <= q) + 1
        for k in [*FUNDS, "RC"]:
            b = betas(br[k], end)[1:]
            vol = float(br[k][max(end - WIN, 0) : end].std() * math.sqrt(252))
            lines.append(
                f"| {q} | {k} | "
                + " | ".join(f"{x:+.2f}" for x in b)
                + f" | {b.sum():+.2f} | {100 * vol:.0f}% |"
            )
        kq = days.index(q)
        ww = wv_w[kq]
        lines.append(
            f"| {q} | `where-vol` weights | {ww[0] + ww[1]:.2f} (SPY+QQQ) | {ww[2]:.2f} | "
            f"{ww[3]:.2f} | 0 | {ww.sum():.2f} (coins {ww[4] + ww[5]:.2f}) | |"
        )
    lines.append("")

    # 5. attribution of the RC composite by rolling betas, set against where-vol's slots
    lines += ["## 5. The gap, slot by slot (calendar 2022, arithmetic contributions)", ""]
    contrib_rc = np.zeros(len(FACT))
    resid = 0.0
    for i in i22:
        b = betas(rc, i)  # betas from the 63 days before day i only
        contrib_rc += b[1:] * X[i]
        resid += rc[i] - b[1:] @ X[i]
    wvc = attrib["where-vol"]
    tsc = attrib["tsmom12"]
    rows = [
        ("Stocks (SPY+QQQ / SPY beta)", wvc[0] + wvc[1], tsc[0] + tsc[1], contrib_rc[0]),
        ("Long bonds (TLT)", wvc[2], tsc[2], contrib_rc[1]),
        ("Gold (GLD)", wvc[3], tsc[3], contrib_rc[2]),
        ("Commodities (DBC)", 0.0, 0.0, contrib_rc[3]),
        ("Coins (BTC+ETH)", wvc[4] + wvc[5], tsc[4] + tsc[5], 0.0),
        ("Fund residual (alpha, non-US, fees)", 0.0, 0.0, resid),
    ]
    lines += [
        "| Slot | `where-vol` | `tsmom12` | RC (beta x factor) | `where-vol` minus RC |",
        "|---|---:|---:|---:|---:|",
    ]
    for lab, a, t, r in rows:
        lines.append(f"| {lab} | {pct(a)} | {pct(t)} | {pct(r)} | {pct(a - r)} |")
    tot = (sum(r[1] for r in rows), sum(r[2] for r in rows), sum(r[3] for r in rows))
    lines.append(
        f"| **Sum** | {pct(tot[0])} | {pct(tot[1])} | {pct(tot[2])} | {pct(tot[0] - tot[2])} |"
    )
    lines.append(f"| RC actual (compounded) | | | {pct(comp(rc[i22]))} | |")
    lines.append("")

    # 6. the stock-bond correlation and the funds' de-risking path
    lines += ["## 6. Stock-bond correlation and when each book cut risk", ""]
    lines += [
        f"Trailing {WIN}-day correlation of daily SPY and TLT returns, month ends; RC's "
        "trailing vol and TLT beta; `where-vol`'s TLT and coin weights and invested share.",
        "",
    ]
    lines += [
        "| Month end | SPY-TLT corr | RC vol | RC TLT beta | RC SPY beta | `where-vol` TLT "
        "| `where-vol` coins | `where-vol` invested | `tsmom12` invested |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    me = []
    d = date(2021, 6, 30)
    while d <= date(2023, 6, 30):
        nxt = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        me.append(nxt - timedelta(days=1))
        d = date(nxt.year + (nxt.month == 12), nxt.month % 12 + 1, 1) - timedelta(days=1)
    me = sorted(set(x for x in me if date(2021, 9, 30) <= x <= date(2023, 6, 30)))
    for m in me:
        end = max(i for i, dd in enumerate(bdays) if dd <= m) + 1
        a = max(end - WIN, 0)
        corr = float(np.corrcoef(br["SPY"][a:end], br["TLT"][a:end])[0, 1])
        vol = float(rc[a:end].std() * math.sqrt(252))
        b = betas(rc, end)
        k = days.index(m)
        w1, w2 = W["where-vol"][k], W["tsmom12"][k]
        lines.append(
            f"| {m} | {corr:+.2f} | {100 * vol:.0f}% | {b[2]:+.2f} | {b[1]:+.2f} | "
            f"{w1[2]:.2f} | {w1[4] + w1[5]:.2f} | {w1.sum():.2f} | {w2.sum():.2f} |"
        )
    lines.append("")

    # 7. ex-ante risk shares going into 2022
    lines += [
        "## 7. Risk shares going into 2022 (`where-vol`'s weights on 2021-12-31, covariance "
        "of daily returns 2021-07..2021-12)",
        "",
    ]
    pre = [i for i, dd in enumerate(days) if date(2021, 7, 1) <= dd <= date(2021, 12, 31)]
    # weekday-only rows so that ETF zero-return weekends do not dilute the covariance
    pre = [i for i in pre if days[i].weekday() < 5]
    cov = np.cov(R[pre].T) * 252
    w0 = W["where-vol"][days.index(date(2021, 12, 31))]
    tot_var = float(w0 @ cov @ w0)
    share = w0 * (cov @ w0) / tot_var
    lines += ["| | " + " | ".join(SIX) + " | Book vol |", "|---|" + "---:|" * (len(SIX) + 1)]
    lines.append("| Weight | " + " | ".join(f"{x:.2f}" for x in w0) + " | |")
    lines.append(
        "| Risk share | "
        + " | ".join(f"{100 * x:.0f}%" for x in share)
        + f" | {100 * math.sqrt(tot_var):.0f}% |"
    )
    vols = np.sqrt(np.diag(cov))
    lines.append("| Asset vol | " + " | ".join(f"{100 * x:.0f}%" for x in vols) + " | |")
    lines.append("")

    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(Path(sys.argv[1]).expanduser())
