"""eu-1 data sanity: coverage, gaps, largest daily moves, and each UCITS line against its US twin
in EUR. Stops at the train cut (never shows a held-out bar).

    uv run --with numpy python research/lib/eu1_check.py
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parents[1] / "data"
CUT = date(2025, 11, 10)  # harness.TRAIN_LAST_BAR

TWIN = {
    "IWDA": "EFA", "EUNL": "EFA", "VWRL": "EFA", "SXR8": "SPY", "CSPX": "SPY", "SXRV": "QQQ",
    "EQQQ": "QQQ", "EXSA": "EFA", "EMIM": "EEM", "IS3N": "EEM", "IQQE": "EEM", "IBGS": "IEF",
    "IBGM": "IEF", "IBGL": "TLT", "EXHE": "TLT", "4GLD": "GLD", "EXXY": "DBC", "IS04": "TLT",
}  # fmt: skip


def closes(sym: str) -> dict[date, float]:
    path = DATA / "adj" / f"{sym}.csv"
    if not path.exists():
        path = DATA / "bars" / f"{sym}.csv"
    with path.open(newline="") as f:
        out = {date.fromisoformat(r["date"]): float(r["close"]) for r in csv.DictReader(f)}
    return {d: c for d, c in out.items() if d <= CUT}


def weekly(c: dict[date, float]) -> dict[tuple[int, int], float]:
    out: dict[tuple[int, int], float] = {}
    for d in sorted(c):
        iso = d.isocalendar()
        out[(iso.year, iso.week)] = c[d]  # last close of each ISO week
    return out


def main() -> None:
    print("# eu-1 data sanity (up to the train cut, 2025-11-10)\n")
    print("Total-return closes in EUR. Twin = the US ETF in EUR (ECB rate). Weekly corr and the")
    print("CAGR gap are on the weeks both have. `uv run --with numpy python "
          "research/lib/eu1_check.py`\n")  # fmt: skip
    print("| Sym | First | Last | Bars | Gaps >5d | Biggest day | CAGR | Vol | Twin | "
          "Weekly corr | CAGR - twin's |")  # fmt: skip
    print("|---|---|---|---:|---:|---|---:|---:|---|---:|---:|")
    for sym, twin in TWIN.items():
        if not (DATA / "bars" / f"{sym}.csv").exists():
            continue
        c = closes(sym)
        ds = sorted(c)
        px = np.array([c[d] for d in ds])
        r = px[1:] / px[:-1] - 1
        gaps = sum((b - a).days > 5 for a, b in zip(ds, ds[1:], strict=False))
        k = int(np.argmax(np.abs(r)))
        yrs = (ds[-1] - ds[0]).days / 365.25
        cagr = (px[-1] / px[0]) ** (1 / yrs) - 1
        vol = r.std() * np.sqrt(252)
        tc = closes(f"{twin}-EUR")
        wa, wb = weekly(c), weekly(tc)
        keys = sorted(set(wa) & set(wb))
        a = np.array([wa[x] for x in keys])
        b = np.array([wb[x] for x in keys])
        corr = float(np.corrcoef(np.diff(np.log(a)), np.diff(np.log(b)))[0, 1])
        yrs2 = len(keys) / 52.18
        diff = (a[-1] / a[0]) ** (1 / yrs2) - (b[-1] / b[0]) ** (1 / yrs2)
        print(
            f"| {sym} | {ds[0]} | {ds[-1]} | {len(ds)} | {gaps} | {r[k]:+.1%} on {ds[k + 1]} | "
            f"{cagr:+.1%} | {vol:.1%} | {twin}-EUR | {corr:.2f} | {diff:+.1%} |"
        )


if __name__ == "__main__":
    main()
