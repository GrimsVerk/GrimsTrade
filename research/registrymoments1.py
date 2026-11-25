"""registry-moments-1: size the forward registry's rule for a noisy measured lrv, and check how
noisy the measured skew and kurtosis are (engineering; synthetic records only, no store data).

    uv run python research/registrymoments1.py > research/results/registry-moments-1.md

`forward.measure_lrv` sizes a line with the upper `level` confidence value of the train
record's long-run variance ratio (`forward.lrv_upper`). This script picks `level`: the smallest
value on a 0.05 grid at which a line's expected power, averaged over its train record's
measurement noise, reaches the plan's 0.80 in every sizing cell (AR(1) records, five and ten
years of weekly values, phi 0 to 0.6, i.e. true lrv 1 to 4). Power at a used lrv U for a line
whose true lrv is L: the sample is U / L times the one the truth needs, so the test's power is
about Phi(sqrt(U / L) (cv + z_power) - cv), cv the verdict's critical value at that sample
(checked against a Monte Carlo of the verdict's own test below). Other cells (8 events a year,
fat tails, slow dependence) are reported, not used for sizing.

Deterministic: numpy Generator (PCG64) seeded from SeedSequence((SEED, cell)), one stream per
cell, never consecutive LCG seeds. Vectorised measurement checked against
`forward.measure_lrv` record by record. Prints markdown. About 20 s.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from statistics import NormalDist

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from grimstrade import forward  # noqa: E402

Z = NormalDist()
SEED = 20261125
RECORDS = 4000
POWER = 0.8
ALPHA = 0.025
GRID = [round(0.5 + 0.05 * i, 2) for i in range(9)]  # 0.50 .. 0.90
PHIS = (0.0, 0.2, 1 / 3, 0.5, 0.6)
BURN = 200


def rng(*cell: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence((SEED, *cell)))


def ar1(e: np.ndarray, phi: float) -> np.ndarray:
    """AR(1) on innovations e (records x (BURN + n)), burn-in dropped."""
    x = np.empty_like(e)
    x[:, 0] = e[:, 0]
    for t in range(1, e.shape[1]):
        x[:, t] = phi * x[:, t - 1] + e[:, t]
    return x[:, BURN:]


def ratio(x: np.ndarray, per_year: float) -> tuple[np.ndarray, float, float, int]:
    """`measure_lrv`'s raw ratio per record (row), and its c, nu and lags."""
    n = x.shape[1]
    lags = forward.lag(n, per_year)
    d = x - x.mean(axis=1, keepdims=True)
    v = (d * d).sum(axis=1) / n
    w = v.copy()
    for j in range(1, lags + 1):
        w += 2 * (1 - j / (lags + 1)) * (d[:, j:] * d[:, :-j]).sum(axis=1) / n
    c, nu = forward._ref(n, lags)
    return w / v, c, nu, lags


def used(r: np.ndarray, c: float, nu: float, level: float | None) -> np.ndarray:
    """The lrv a line is sized with: the point estimate (level None) or its upper value."""
    point = r / c
    if level is None:
        return np.maximum(1.0, point)
    return np.maximum(1.0, np.array([forward.lrv_upper(p, nu, level) for p in point]))


def power(u: np.ndarray, true: float, cv: float) -> np.ndarray:
    zp = Z.inv_cdf(POWER)
    s = np.sqrt(u / true) * (cv + zp) - cv
    return np.array([Z.cdf(v) for v in s])


def check_vectorised() -> float:
    """Largest relative gap between this script's measurement and `forward.measure_lrv`."""
    g = rng(0)
    worst = 0.0
    for n, per_year, phi in ((260, 52, 0.5), (520, 52, 0.2), (40, 8, 0.33)):
        x = ar1(g.standard_normal((5, BURN + n)), phi)
        r, c, nu, _ = ratio(x, per_year)
        for row, ri in zip(x, r, strict=True):
            m = forward.measure_lrv(row.tolist(), per_year)
            assert m["c"] == c and m["nu"] == nu
            worst = max(worst, abs(m["ratio"] / ri - 1))
            mine = max(1.0, forward.lrv_upper(ri / c, nu))
            worst = max(worst, abs(m["lrv"] / mine - 1))
    return worst


def cell_rows(
    label: str, x: np.ndarray, per_year: float, true: float, levels: list[float | None]
) -> list[str]:
    r, c, nu, _ = ratio(x, per_year)
    cv = forward.critical(10 * round(per_year), per_year, ALPHA)  # ~10-year forward sample
    out = []
    for lv in levels:
        u = used(r, c, nu, lv)
        pw = power(u, true, cv)
        name = "point" if lv is None else f"{lv:.2f}"
        out.append(
            f"| {label} | {true:.2f} | {name} | {np.median(u):.2f} | {u.mean():.2f} | "
            f"{np.mean(u < true):.2f} | {pw.mean():.3f} | {np.mean(pw < 0.75):.2f} | "
            f"{u.mean() / true:.2f} |"
        )
    return out


def main() -> None:
    print("# registry-moments-1: results (`research/registrymoments1.py`)\n")
    print(f"Seed {SEED}, {RECORDS} records per cell, plan power {POWER}, alpha {ALPHA}.")
    print(f"Vectorised vs `forward.measure_lrv`: largest relative gap {check_vectorised():.1e}.\n")

    # --- 1. sizing: the smallest level with expected power >= POWER in every cell ---
    sizing: list[tuple[str, np.ndarray, float, float]] = []
    for i, n in enumerate((260, 520)):
        for j, phi in enumerate(PHIS):
            x = ar1(rng(1, i, j).standard_normal((RECORDS, BURN + n)), phi)
            sizing.append((f"weekly {n // 52} y, phi {phi:.2f}", x, 52.0, (1 + phi) / (1 - phi)))
    table: dict[float | None, list[float]] = {}
    for lv in [None, *GRID]:
        table[lv] = []
        for _, x, per_year, true in sizing:
            r, c, nu, _ = ratio(x, per_year)
            cv = forward.critical(10 * round(per_year), per_year, ALPHA)
            table[lv].append(float(power(used(r, c, nu, lv), true, cv).mean()))
    chosen = next(lv for lv in GRID if min(table[lv]) >= POWER)
    print("## 1. Sizing: lowest expected power over the 10 weekly AR(1) cells, by level\n")
    print("| Level | Lowest expected power | Its cell | Highest (true lrv 1) |")
    print("|---|---:|---|---:|")
    for lv, pws in table.items():
        k = int(np.argmin(pws))
        name = "point estimate" if lv is None else f"{lv:.2f}"
        print(f"| {name} | {pws[k]:.3f} | {sizing[k][0]} | {max(pws):.3f} |")
    print(f"\n**Chosen level: {chosen:.2f}** (`forward.LRV_LEVEL` = {forward.LRV_LEVEL}).\n")
    assert chosen == forward.LRV_LEVEL, "update forward.LRV_LEVEL to the chosen level"

    head = (
        "| Cell | True lrv | Rule | Median used | Mean used | P(used < true) | "
        "Expected power | P(power < 0.75) | Mean used / true |"
    )
    sep = "|---|---:|---|---:|---:|---:|---:|---:|---:|"
    print("## 2. Sizing cells: point estimate vs the chosen level\n")
    print(head)
    print(sep)
    for label, x, per_year, true in sizing:
        print("\n".join(cell_rows(label, x, per_year, true, [None, chosen])))

    # --- 3. other cells, reported only ---
    print("\n## 3. Other records (not used for sizing)\n")
    print(head)
    print(sep)
    for i, n in enumerate((40, 80)):
        for j, phi in enumerate((0.0, 1 / 3, 0.5)):
            x = ar1(rng(3, i, j).standard_normal((RECORDS, BURN + n)), phi)
            label = f"8 a year, {n // 8} y, phi {phi:.2f}"
            print("\n".join(cell_rows(label, x, 8.0, (1 + phi) / (1 - phi), [None, chosen])))
    t4 = rng(4).standard_t(4, (RECORDS, BURN + 260)) / math.sqrt(2)
    print("\n".join(cell_rows("weekly 5 y, phi 0.50, t(4) shocks", ar1(t4, 0.5), 52.0, 3.0,
                              [None, chosen])))
    # slow dependence: white noise plus a small AR(1) phi 0.98 component (true lrv 3 for the
    # mean of a long record, most of it at lags beyond a year)
    g = rng(5)
    rho = 0.98
    share = 2 / ((1 + rho) / (1 - rho) - 1)  # (1 - s) + s (1 + rho) / (1 - rho) = 3
    for n in (260, 520):
        slow = ar1(g.standard_normal((RECORDS, BURN + n)) * math.sqrt(1 - rho**2), rho)
        noise = g.standard_normal((RECORDS, n))
        x = math.sqrt(share) * slow + math.sqrt(1 - share) * noise
        true = (1 - share) + share * (1 + rho) / (1 - rho)
        label = f"weekly {n // 52} y, slow (phi 0.98 part)"
        print("\n".join(cell_rows(label, x, 52.0, true, [None, chosen])))

    # --- 4. the power approximation against the verdict's own test ---
    print("\n## 4. Power approximation vs a Monte Carlo of the verdict's test\n")
    print("AR(1) phi 0.5 (true lrv 3) forward records with a true mean `effect`; the sample is")
    print("sized with lrv U (`forward.min_events_mean`); rejections of `forward`'s fixed-b HAC")
    print("test at alpha 0.025, 2,000 records per row.\n")
    print("| Sized with lrv | n | Approximate power | Monte Carlo power |")
    print("|---:|---:|---:|---:|")
    g = rng(6)
    sd = 1 / math.sqrt(1 - 0.25)  # stationary sd of an AR(1) phi 0.5 with unit shocks
    for u in (1.5, 3.0, 4.5):
        n = forward.min_events_mean(0.1 * sd, sd, ALPHA, POWER, 52, u)
        x = ar1(g.standard_normal((2000, BURN + n)), 0.5) + 0.1 * sd
        r, c, nu, lags = ratio(x, 52)
        d = x - x.mean(axis=1, keepdims=True)
        w = r * (d * d).sum(axis=1) / n * n / (n - 1)
        t = x.mean(axis=1) / np.sqrt(w / n)
        mc = float(np.mean(t > forward.critical(n, 52, ALPHA)))
        approx = float(power(np.array([u]), 3.0, forward.critical(n, 52, ALPHA))[0])
        print(f"| {u:g} | {n} | {approx:.3f} | {mc:.3f} |")

    # --- 5. how noisy the measured skew and kurtosis (k) are ---
    print("\n## 5. Measured Mertens factor k on skewed, fat-tailed weekly records\n")
    print("Returns: N(0, 1) with probability 0.95, N(-2.5, 2^2) with 0.05 (a crash state),")
    print("iid; k = 1 - skew sr + (kurtosis - 1) / 4 sr^2 at the plan's per-week Sharpe sr.")
    print("Truth from 4,000,000 draws. The default plan (skew 0, kurtosis 3) is k0.\n")
    print("| Annual Sharpe | Years | True k | k0 | Median measured k | sd | P(measured < true) |")
    print("|---:|---:|---:|---:|---:|---:|---:|")
    g = rng(7)

    def draw(shape: tuple[int, ...]) -> np.ndarray:
        crash = g.random(shape) < 0.05
        return np.where(crash, g.normal(-2.5, 2.0, shape), g.standard_normal(shape))

    big = draw((4_000_000,))
    zc = (big - big.mean()) / big.std()
    s0, k0 = float((zc**3).mean()), float((zc**4).mean())
    for sharpe in (0.5, 0.79, 1.5):
        for years in (5, 10):
            x = draw((RECORDS, 52 * years))
            zs = (x - x.mean(axis=1, keepdims=True)) / x.std(axis=1, keepdims=True)
            sk, ku = (zs**3).mean(axis=1), (zs**4).mean(axis=1)
            km = np.array([forward.k_factor(a, b, sharpe, 52) for a, b in zip(sk, ku, strict=True)])
            kt = forward.k_factor(s0, k0, sharpe, 52)
            kd = forward.k_factor(0.0, 3.0, sharpe, 52)
            print(
                f"| {sharpe:g} | {years} | {kt:.3f} | {kd:.3f} | {np.median(km):.3f} | "
                f"{km.std():.3f} | {np.mean(km < kt):.2f} |"
            )
    print(f"\nPopulation skew {s0:.2f}, kurtosis {k0:.2f}.")


if __name__ == "__main__":
    main()
