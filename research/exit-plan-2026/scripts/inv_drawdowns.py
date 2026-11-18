"""Peak-to-trough drawdowns and beta of BRK-B vs the S&P 500 in named windows (lane inv).

Input: Yahoo chart-API JSON files (v8/finance/chart, interval=1d), passed as arguments:
    python -I inv_drawdowns.py <brkb.json> <spx.json>
Uses close prices (price only, no dividends; BRK pays none, the index is price-only too).
"""

import json
import sys
from datetime import UTC, date, datetime


def load(path: str) -> dict[date, float]:
    with open(path) as f:
        res = json.load(f)["chart"]["result"][0]
    ts = res["timestamp"]
    close = res["indicators"]["quote"][0]["close"]
    return {
        datetime.fromtimestamp(t, UTC).date(): c
        for t, c in zip(ts, close, strict=True)
        if c is not None
    }


def max_dd(s: dict[date, float], a: date, b: date) -> tuple[float, date, date]:
    peak_v, peak_d, worst, worst_pk, worst_tr = 0.0, a, 0.0, a, a
    for d in sorted(s):
        if d < a or d > b:
            continue
        v = s[d]
        if v > peak_v:
            peak_v, peak_d = v, d
        dd = v / peak_v - 1
        if dd < worst:
            worst, worst_pk, worst_tr = dd, peak_d, d
    return worst, worst_pk, worst_tr


def beta(x: dict[date, float], m: dict[date, float], a: date, b: date) -> float:
    days = sorted(d for d in x if d in m and a <= d <= b)
    rx = [x[d1] / x[d0] - 1 for d0, d1 in zip(days, days[1:])]
    rm = [m[d1] / m[d0] - 1 for d0, d1 in zip(days, days[1:])]
    mx, mm = sum(rx) / len(rx), sum(rm) / len(rm)
    cov = sum((p - mx) * (q - mm) for p, q in zip(rx, rm, strict=True))
    var = sum((q - mm) ** 2 for q in rm)
    return cov / var


def main() -> None:
    brk, spx = load(sys.argv[1]), load(sys.argv[2])
    windows = {
        "dotcom 2000-01..2002-12": (date(2000, 1, 1), date(2002, 12, 31)),
        "GFC 2007-10..2009-06": (date(2007, 10, 1), date(2009, 6, 30)),
        "COVID 2020-02..2020-04": (date(2020, 2, 1), date(2020, 4, 30)),
        "2022 bear 2022-01..2022-12": (date(2022, 1, 1), date(2022, 12, 31)),
        "2025 tariff 2025-02..2025-05": (date(2025, 2, 1), date(2025, 5, 31)),
        "2026 to date 2026-01..": (date(2026, 1, 1), date(2026, 12, 31)),
    }
    print("window | BRK-B maxDD (peak->trough) | S&P maxDD (peak->trough)")
    for name, (a, b) in windows.items():
        bd, bp, bt = max_dd(brk, a, b)
        sd, sp, st = max_dd(spx, a, b)
        print(f"{name} | {bd:.1%} ({bp}->{bt}) | {sd:.1%} ({sp}->{st})")
    last = max(brk)
    print(f"last BRK-B date {last}, close {brk[last]:.2f}; last S&P {max(spx)} {spx[max(spx)]:.2f}")
    for name, (a, b) in {
        "beta 2000-2025": (date(2000, 1, 1), date(2025, 12, 31)),
        "beta 2016-2025": (date(2016, 1, 1), date(2025, 12, 31)),
    }.items():
        print(f"{name}: {beta(brk, spx, a, b):.2f}")
    # S&P closes at dated warnings / calls used in inv.md (first trading day on or after).
    events = {
        "Greenspan 'irrational exuberance' speech (1996-12-05)": date(1996, 12, 5),
        "dot-com S&P peak": date(2000, 3, 24),
        "dot-com S&P trough": date(2002, 10, 9),
        "Buffett 'Buy American' op-ed (2008-10-16)": date(2008, 10, 16),
        "GFC trough": date(2009, 3, 9),
        "Grantham 'Waiting for the Last Dance' (2021-01-05)": date(2021, 1, 5),
        "2022 peak": date(2022, 1, 3),
        "2022 trough": date(2022, 10, 12),
        "Marks 'Is It a Bubble?' (2025-12-09)": date(2025, 12, 9),
    }
    for name, d in events.items():
        d0 = min(x for x in spx if x >= d)
        print(f"{name}: S&P close {d0} = {spx[d0]:.2f}")
    for y in range(2025, 2027):
        a, b = date(y, 1, 1), date(y, 12, 31)
        bd = sorted(d for d in brk if a <= d <= b)
        sd = sorted(d for d in spx if a <= d <= b)
        prev_b = max(d for d in brk if d < a)
        prev_s = max(d for d in spx if d < a)
        print(
            f"{y} (to {bd[-1]}): BRK-B {brk[bd[-1]] / brk[prev_b] - 1:.1%}, "
            f"S&P {spx[sd[-1]] / spx[prev_s] - 1:.1%}"
        )


if __name__ == "__main__":
    main()
