"""Lane gate-null-2, Parts 1-2 (research/cards/gate-null-2.md): size and power of placebo
families on synthetic doses with a known null. No strategy, no backtest.

Run:  `uv run python -I research/lib/gatenull2_sim.py [sims] [workers]`  (default 2000, 4)
      `uv run python -I research/lib/gatenull2_sim.py report`  (tables from the saved cells)
Cells are saved under `<cache_root>/gate-null-2/sim/` (one .npz per cell); the report goes to
research/results/gate-null-2.md (Part 1-2 section).
"""

from __future__ import annotations

import io
import json
import sys
import time
import zipfile
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gatenull2 as g  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PHIS = [0.0, 0.5, 0.8, 0.9, 0.95, 0.98, 0.99]
DOSES = [f"ar{p}" for p in PHIS] + ["cycle", "skew"]
RETS = ["garch-t", "real", "slow-premium"]
TS = [300, 600]
R2S = [0.0025, 0.005, 0.01, 0.02]
FAMS = ["F1 shift-earlier", "F1b shift-both", "F2 phase", "F3 iaaft", "F4 block24", "F5 rotation"]
M = 40


def cache_dir() -> Path:
    cfg = json.loads((ROOT / "research" / "macro.local.json").read_text())
    d = Path(cfg["cache_root"]).expanduser() / "gate-null-2" / "sim"
    d.mkdir(parents=True, exist_ok=True)
    return d


def french_mkt() -> np.ndarray:
    """French Mkt-RF monthly (percent), 1926-07..2025-10, from the cached factors zip."""
    cfg = json.loads((ROOT / "research" / "macro.local.json").read_text())
    p = Path(cfg["cache_root"]).expanduser() / "french" / "2026-11-12"
    with zipfile.ZipFile(p / "F-F_Research_Data_Factors_CSV.zip") as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    out = []
    for line in io.StringIO(text):
        parts = line.strip().split(",")
        ym = parts[0].strip()
        if len(parts) == 5 and len(ym) == 6 and ym.isdigit() and int(ym) <= 202510:
            out.append(float(parts[1]))
        elif out and "Annual" in line:
            break
    return np.array(out)


def make_dose(rng: np.random.Generator, kind: str, n: int) -> np.ndarray:
    if kind.startswith("ar"):
        return g.ar1(rng, n, float(kind[2:]))
    if kind == "cycle":
        noise = g.ar1(rng, n, 0.9)
        noise = noise / noise.std()
        ph = rng.uniform(0, 2 * np.pi)
        cyc = np.sqrt(2) * np.sin(2 * np.pi * np.arange(n) / 132 + ph)
        return cyc + noise
    if kind == "skew":
        a = g.ar1(rng, n, 0.95)
        e = np.exp(a / a.std())
        return (e - e.mean()) / e.std()
    raise ValueError(kind)


def make_returns(rng: np.random.Generator, kind: str, n: int, mkt: np.ndarray) -> np.ndarray:
    if kind == "garch-t":
        return g.garch_t(rng, n)
    if kind == "real":
        off = int(rng.integers(0, len(mkt)))
        return np.roll(mkt, -off)[:n] / mkt.std()
    if kind == "slow-premium":
        r = g.garch_t(rng, n)
        mu = g.ar1(rng, n, 0.98)
        return r + mu / mu.std() * np.sqrt(0.02 / 0.98)
    raise ValueError(kind)


def run_cell(args: tuple[str, str, int, int]) -> str:
    ret, dose, n, sims = args
    out = cache_dir() / f"{ret}_{dose}_T{n}_S{sims}.npz"
    if out.exists():
        return f"{out.name} cached"
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(f"{ret}|{dose}|{n}")) * 7919 % (2**31)
    rng = np.random.default_rng(seed)
    mkt = french_mkt()
    k = 1 + len(FAMS) * M
    t3 = np.empty((sims, k), np.float32)  # NW 3, next month
    t12 = np.empty((sims, k), np.float32)  # NW 12, next month
    tq = np.empty((sims, k), np.float32)  # 3-month overlapping outcome, NW 3
    tp = np.empty((len(R2S), sims, k), np.float32)  # planted, NW 3, next month
    ac = np.empty(sims)
    t0 = time.time()
    for s in range(sims):
        ext = make_dose(rng, dose, g.PRE + n + g.POST)
        x = ext[g.PRE : g.PRE + n]
        fam = [
            g.shifted(ext, g.SHIFT_EARLIER, g.PRE, n),
            g.shifted(ext, g.SHIFT_BOTH, g.PRE, n),
            g.phase_surrogates(rng, x, M),
            g.iaaft_surrogates(rng, x, M),
            g.block_bootstrap(rng, x, M, 24),
            g.rotations(rng, x, M, 24),
        ]
        xm = np.column_stack([x, *fam])
        r = make_returns(rng, ret, n + 3, mkt)
        y = r[1 : n + 1]
        t3[s] = g.nw_slope_t(y, xm, 3)[1]
        t12[s] = g.nw_slope_t(y, xm, 12)[1]
        tq[s] = g.nw_slope_t(r[1 : n + 1] + r[2 : n + 2] + r[3 : n + 3], xm, 3)[1]
        xs = (x - x.mean()) / x.std()
        for j, r2 in enumerate(R2S):
            yp = y + np.sqrt(r2 / (1 - r2)) * y.std() * xs
            tp[j, s] = g.nw_slope_t(yp, xm, 3)[1]
        ac[s] = g.acf1(x)
    np.savez_compressed(out, t3=t3, t12=t12, tq=tq, tp=tp, ac=ac, seed=seed)
    return f"{out.name} {time.time() - t0:.0f}s"


def cells(sims: int) -> list[tuple[str, str, int, int]]:
    return [(r, d, n, sims) for n in TS for r in RETS for d in DOSES]


def main() -> None:
    sims = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    todo = cells(sims)
    with Pool(workers) as pool:
        for msg in pool.imap_unordered(run_cell, todo):
            print(msg, flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        import gatenull2_report

        gatenull2_report.main()
    else:
        main()
