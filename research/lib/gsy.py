"""GSY 1: a Greenwood-Shleifer-You run-up flag as an exit overlay on `tsmom12`.
Card: research/cards/gsy-runup.md. Write-up: research/gsy-1.md.

    uv run python -I research/lib/gsy.py replicate   # step 2: descriptive, no strategy
    uv run python -I research/lib/gsy.py runs        # step 3: the card's variants

Ken French's industry files (cache root from research/macro.local.json or GRIMSTRADE_DATA; read
as data, never written). Nothing after 2025-11-10 (the train cut) is parsed; the held-out year
is never loaded. Rows go to research/tries.md the moment a configuration runs; a configuration
whose equity file exists under the git-ignored research/data/runs/ is re-scored without a row.
"""

from __future__ import annotations

import math
import sys
import zipfile
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsy_signals as g  # noqa: E402
from macro import cache_root  # noqa: E402

IDEA = "gsy-runup"
FRENCH = "french/2026-11-12"  # cached daily 10 industries and factors
EXTRA = "french-gsy/2026-11-18"  # downloaded for this lane
LAST = date(2025, 11, 10)  # train runs never load a later bar
LAST_MONTH = 202510  # last whole month before the held-out year
THRESHOLDS = (1.0, 1.5)


# --- loaders (raw cache, read only) ---


def _lines(path: Path) -> list[str]:
    z = zipfile.ZipFile(path)
    return z.read(z.namelist()[0]).decode("latin1").splitlines()


def _block(lines: Sequence[str], title: str) -> tuple[list[str], Iterator[list[str]]]:
    """Column names and the data rows (cells) of the block whose title line is `title`."""
    head = next(i for i, x in enumerate(lines) if x.strip() == title)
    names = [x.strip() for x in lines[head + 1].split(",")][1:]

    def rows() -> Iterator[list[str]]:
        started = False
        for line in lines[head + 2 :]:
            cells = [x.strip() for x in line.split(",")]
            if len(cells) == len(names) + 1 and cells[0].isdigit():
                started = True
                yield cells
            elif started:
                return

    return names, rows()


def _ret(x: str) -> float:
    v = float(x)
    return math.nan if v <= -99 else v / 100


@dataclass
class Monthly:
    months: list[int]  # yyyymm
    names: list[str]
    ret: np.ndarray  # months x industries, simple
    mkt: np.ndarray  # market total return, simple
    firms: np.ndarray  # months x industries, number of firms


def monthly(path: Path, factors: Path) -> Monthly:
    lines = _lines(path)
    names, rows = _block(lines, "Average Value Weighted Returns -- Monthly")
    data = {int(c[0]): [_ret(x) for x in c[1:]] for c in rows if int(c[0]) <= LAST_MONTH}
    _, frows = _block(lines, "Number of Firms in Portfolios")
    firms = {int(c[0]): [float(x) for x in c[1:]] for c in frows if int(c[0]) <= LAST_MONTH}
    fl = _lines(factors)
    head = next(i for i, x in enumerate(fl) if x.replace(" ", "") == ",Mkt-RF,SMB,HML,RF")
    fac: dict[int, float] = {}
    for line in fl[head + 1 :]:
        cells = [x.strip() for x in line.split(",")]
        if len(cells) != 5 or len(cells[0]) != 6 or not cells[0].isdigit():
            break
        if int(cells[0]) <= LAST_MONTH:
            fac[int(cells[0])] = (float(cells[1]) + float(cells[4])) / 100
    months = sorted(data)
    if months != sorted(fac):
        raise ValueError("industry and factor months disagree")
    return Monthly(
        months, names, np.array([data[m] for m in months]), np.array([fac[m] for m in months]),
        np.array([firms[m] for m in months]),
    )  # fmt: skip


def paths() -> dict[str, Path]:
    root = cache_root()
    e = root / EXTRA
    return {
        "49m": e / "49m" / "49_Industry_Portfolios_CSV.zip",
        "30m": e / "30m" / "30_Industry_Portfolios_CSV.zip",
        "10m": e / "10m" / "10_Industry_Portfolios_CSV.zip",
        "30d": e / "30d" / "30_Industry_Portfolios_daily_CSV.zip",
        "10d": root / FRENCH / "10_Industry_Portfolios_daily_CSV.zip",
        "fm": root / FRENCH / "F-F_Research_Data_Factors_CSV.zip",
        "fd": root / FRENCH / "F-F_Research_Data_Factors_daily_CSV.zip",
    }


# --- step 2: replication ---


def _row(months: list[int], ym: int) -> int:
    return months.index(ym)


def replicate() -> str:
    p = paths()
    out = [
        "## Step 2. Replication of GSY's conditional crash probability (descriptive)",
        "",
        "Monthly value-weighted French industries. Episode: the first month an industry's "
        "24-month return is at least the threshold, raw and net of the market, with no run-up "
        "month in that industry in the 24 months before. `Crash`: a peak-to-trough fall of 40% "
        "or more within the next 24 months (peak counted from the signal month on). `Strict`: "
        "a month-end 40% or more below the signal month's level within 24 months. `Base`: the "
        "same two shares over every industry-month in the window (no condition). Only "
        "episodes whose 24 months after end by 2025-10 count.",
        "",
        "| Industries | Window (signal months) | Threshold | Episodes | Crash | Strict | "
        "Median return next 6 m | Median return next 24 m | Base crash | Base strict |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    windows = [
        ("1928-07 to 2014-12 (GSY)", 192807, 201412),
        ("1928-07 to 2001-12", 192807, 200112),
        ("2002-01 to 2023-10", 200201, 202310),
        ("2015-01 to 2023-10", 201501, 202310),
    ]
    detail: list[str] = []
    for key in ("49m", "30m", "10m"):
        mo = monthly(p[key], p["fm"])
        idx = g.index_of(mo.ret)
        mk = g.index_of(mo.mkt[:, None])[:, 0]
        for label, a, b in windows:
            for th in THRESHOLDS:
                eps, base, hit, hit_s = g.episodes(
                    idx, mk, th, _row(mo.months, a), _row(mo.months, b)
                )
                med6 = float(np.median([e.r6 for e in eps])) if eps else math.nan
                med24 = float(np.median([e.r24 for e in eps])) if eps else math.nan
                out.append(
                    f"| {key[:-1]} | {label} | {th:.0%} | {len(eps)} | "
                    f"{_pc(g.share([e.crash for e in eps]))} | "
                    f"{_pc(g.share([e.strict for e in eps]))} | {_pc(med6)} | {_pc(med24)} | "
                    f"{_pc(hit / base if base else math.nan)} | "
                    f"{_pc(hit_s / base if base else math.nan)} |"
                )
                if key == "49m" and a == 192807 and b == 201412 and th == 1.0:
                    detail = [
                        f"| {mo.months[e.month]} | {mo.names[e.industry]} | "
                        f"{'yes' if e.crash else 'no'} | {'yes' if e.strict else 'no'} | "
                        f"{_pc(e.r6)} | {_pc(e.r24)} |"
                        for e in eps
                    ]
    out += [
        "",
        "**Added after the table above was seen (a re-reading, not the card's definition):** "
        "the same episodes, keeping only those whose industry had at least 10 firms in the "
        "signal month (a small-industry filter GSY may have used; not checked in the paper).",
        "",
        "| Industries | Window | Threshold | Episodes | Crash | Strict |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for key in ("49m", "30m"):
        mo = monthly(p[key], p["fm"])
        idx = g.index_of(mo.ret)
        mk = g.index_of(mo.mkt[:, None])[:, 0]
        for label, a, b in windows[:3]:
            for th in THRESHOLDS:
                eps, *_ = g.episodes(idx, mk, th, _row(mo.months, a), _row(mo.months, b))
                big = [e for e in eps if mo.firms[e.month, e.industry] >= 10]
                out.append(
                    f"| {key[:-1]} | {label} | {th:.0%} | {len(big)} | "
                    f"{_pc(g.share([e.crash for e in big]))} | "
                    f"{_pc(g.share([e.strict for e in big]))} |"
                )
    out += [
        "",
        "49 industries, 100%, 1928-2014: every episode.",
        "",
        "| Signal month | Industry | Crash | Strict | Next 6 m | Next 24 m |",
        "|---|---|---|---|---:|---:|",
        *detail,
        "",
    ]
    return "\n".join(out)


def _pc(x: float) -> str:
    return "-" if math.isnan(x) else f"{x * 100:.0f}%"


def main() -> None:
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "replicate":
        text = replicate()
        path = Path(__file__).resolve().parents[1] / "results" / "gsy-1-replication.md"
        path.write_text(
            "# gsy-1: replication of GSY on French industries\n\nCard: "
            "`cards/gsy-runup.md`, step 2. Written by `lib/gsy.py replicate`.\n\n" + text
        )
        print(text)
    else:
        raise SystemExit("usage: gsy.py replicate | runs")


if __name__ == "__main__":
    main()
