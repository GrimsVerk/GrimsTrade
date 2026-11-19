"""Daily venue panels for research run carry-2 (card in research/carry-2.md), with short-1's day
rules. Kept free of `harness` so tests can import it."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

TRAIN_LAST_BAR = date(2025, 11, 10)  # == harness.TRAIN_LAST_BAR (checked in carry2.py)
DAY0 = date(2019, 9, 1)
N_DAYS = (TRAIN_LAST_BAR - DAY0).days + 1
T0 = int(datetime.combine(DAY0, datetime.min.time(), UTC).timestamp())
CUT = T0 + N_DAYS * 86400  # first second after the train cut


class Acc:
    """Collects one venue's daily panels column by column."""

    def __init__(self) -> None:
        self.names: list[str] = []
        self.cols: dict[str, list[np.ndarray]] = {
            k: [] for k in ("px", "qv", "fsig", "fsim", "fcnt", "prem")
        }

    def add(
        self,
        name: str,
        day_s: np.ndarray,
        close: np.ndarray,
        qv: np.ndarray,
        ft: np.ndarray,
        fr: np.ndarray,
        pt: np.ndarray | None,
        pv: np.ndarray | None,
    ) -> None:
        """day_s: bar start (s, UTC day start); ft/fr: funding events (s, rate);
        pt/pv: hourly premium samples (bar start or sample time, s)."""
        px = np.full(N_DAYS, np.nan)
        q = np.full(N_DAYS, np.nan)
        d = (day_s - T0) // 86400
        k = (d >= 0) & (d < N_DAYS) & np.isfinite(close) & (close > 0)
        px[d[k]], q[d[k]] = close[k], qv[k]
        fsig = np.full(N_DAYS, np.nan)
        fsim = np.zeros(N_DAYS)
        fcnt = np.zeros(N_DAYS)
        keep = ft < CUT
        ft, fr = ft[keep], fr[keep]
        if len(ft):
            fd = (ft - T0) // 86400  # known by the end of day fd (short-1's signal rule)
            kk = (fd >= 0) & (fd < N_DAYS)
            num = np.bincount(fd[kk], weights=fr[kk], minlength=N_DAYS)
            cnt = np.bincount(fd[kk], minlength=N_DAYS)
            fsig[cnt > 0] = (num / np.maximum(cnt, 1) * 3)[cnt > 0]
            dd = (ft - 1 - T0) // 86400  # event at 00:00 of t+1 belongs to return day t
            kk = (dd >= 0) & (dd < N_DAYS)
            fsim = np.bincount(dd[kk], weights=fr[kk], minlength=N_DAYS).astype(float)
            fcnt = np.bincount(dd[kk], minlength=N_DAYS).astype(float)
        prem = np.full(N_DAYS, np.nan)
        if pt is not None and pv is not None and len(pt):
            keep = pt < CUT
            pdx = (pt[keep] - T0) // 86400
            v = pv[keep]
            kk = (pdx >= 0) & (pdx < N_DAYS) & np.isfinite(v)
            num = np.bincount(pdx[kk], weights=v[kk], minlength=N_DAYS)
            cnt = np.bincount(pdx[kk], minlength=N_DAYS)
            prem[cnt > 0] = (num / np.maximum(cnt, 1))[cnt > 0]
        self.names.append(name)
        for key, arr in zip(self.cols, (px, q, fsig, fsim, fcnt, prem), strict=True):
            self.cols[key].append(arr)

    def save(self, folder: Path, venue: str) -> None:
        arrs = {k: np.column_stack(v) for k, v in self.cols.items()}
        np.savez(folder / f"{venue}.npz", names=np.array(self.names), **arrs)  # type: ignore[arg-type]
