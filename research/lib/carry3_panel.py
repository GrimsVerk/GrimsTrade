"""Daily venue panels for research run carry-3 (card in research/carry-3.md): carry-2's panels
(`carry2_panel.py`, copied, not edited) plus each day's high and low, on a day grid that ends
at the train cut by default. Only the guarded held-out run asks for a later `last`. Kept free of
`harness` so tests can import it."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

TRAIN_LAST_BAR = date(2025, 11, 10)  # == harness.TRAIN_LAST_BAR (checked in carry3.py)
HELD_LAST_BAR = date(2026, 11, 10)
DAY0 = date(2019, 9, 1)
KEYS = ("px", "hi", "lo", "qv", "fsig", "fsim", "fcnt")


class Grid:
    """Calendar days DAY0 .. last (UTC)."""

    def __init__(self, last: date = TRAIN_LAST_BAR) -> None:
        if last not in (TRAIN_LAST_BAR, HELD_LAST_BAR):
            raise ValueError("a panel ends at the train cut or at the held-out cut")
        self.last = last
        self.n_days = (last - DAY0).days + 1
        self.t0 = int(datetime.combine(DAY0, datetime.min.time(), UTC).timestamp())
        self.cut = self.t0 + self.n_days * 86400  # first second after the last day

    @property
    def tag(self) -> str:
        return "train" if self.last == TRAIN_LAST_BAR else "heldout"


class Acc:
    """Collects one venue's daily panels column by column."""

    def __init__(self, grid: Grid | None = None) -> None:
        self.grid = grid or Grid()
        self.names: list[str] = []
        self.cols: dict[str, list[np.ndarray]] = {k: [] for k in KEYS}

    def add(
        self,
        name: str,
        day_s: np.ndarray,
        high: np.ndarray,
        low: np.ndarray,
        close: np.ndarray,
        qv: np.ndarray,
        ft: np.ndarray,
        fr: np.ndarray,
    ) -> None:
        """day_s: bar start (s, UTC day start); ft/fr: funding events (s, rate)."""
        g = self.grid
        n = g.n_days
        px, hi, lo, q = (np.full(n, np.nan) for _ in range(4))
        d = (day_s - g.t0) // 86400
        k = (d >= 0) & (d < n) & np.isfinite(close) & (close > 0)
        px[d[k]], hi[d[k]], lo[d[k]], q[d[k]] = close[k], high[k], low[k], qv[k]
        fsig = np.full(n, np.nan)
        fsim = np.zeros(n)
        fcnt = np.zeros(n)
        keep = ft < g.cut
        ft, fr = ft[keep], fr[keep]
        if len(ft):
            fd = (ft - g.t0) // 86400  # known by the end of day fd (short-1's signal rule)
            kk = (fd >= 0) & (fd < n)
            num = np.bincount(fd[kk], weights=fr[kk], minlength=n)
            cnt = np.bincount(fd[kk], minlength=n)
            fsig[cnt > 0] = (num / np.maximum(cnt, 1) * 3)[cnt > 0]
            dd = (ft - 1 - g.t0) // 86400  # event at 00:00 of t+1 belongs to return day t
            kk = (dd >= 0) & (dd < n)
            fsim = np.bincount(dd[kk], weights=fr[kk], minlength=n).astype(float)
            fcnt = np.bincount(dd[kk], minlength=n).astype(float)
        self.names.append(name)
        for key, arr in zip(self.cols, (px, hi, lo, q, fsig, fsim, fcnt), strict=True):
            self.cols[key].append(arr)

    def save(self, folder: Path, venue: str) -> None:
        arrs = {k: np.column_stack(v) for k, v in self.cols.items()}
        path = folder / f"{venue}-{self.grid.tag}.npz"
        np.savez(path, names=np.array(self.names), **arrs)  # type: ignore[arg-type]
