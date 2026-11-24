"""Lane gate-power: planted-effect power of five past event-study gates (research/gate-power.md).

Method study: no strategy, no backtest, no tries row. Train bars only (cut at 2025-11-10);
doses cut where each gate cut them. Reads the existing caches (data-wide-1, cftc, weather-1,
research/data); fetches nothing. Untrusted downloads: run with `python -I`.

Run: `uv run --with xlrd python -I research/lib/gatepower_run.py`  GATE=W25|W26|W22|W19|HDD
(default all); N_SIM to override 200; DRY=1 prints the rebuild check only.
Output: research/results/gate-power-<gate>.md
"""

from __future__ import annotations

import math
import os
import sys
from collections.abc import Callable
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import gatepower as gp  # noqa: E402
import harness  # noqa: E402
import macro  # noqa: E402
import weather1_events as wev  # noqa: E402
import weather1_hdd as whdd  # noqa: E402
import wide9_enso as w9  # noqa: E402
import wide9_events as ev9  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as ev  # noqa: E402
from wide10_events import ols_hc1  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
LAST = harness.TRAIN_LAST_BAR
DRY = bool(os.environ.get("DRY"))
N_SIM = int(os.environ.get("N_SIM", gp.N_SIM))
SEED = 20261119


def rotations(pool: dict[str, np.ndarray], gap: int, seed: int) -> Callable[[int], dict]:
    """Draw s: every asset's per-period returns moved by the same circular offset, at least
    `gap` periods from zero; offsets drawn without replacement where the pool allows."""
    n = len(next(iter(pool.values())))
    choices = np.arange(gap, n - gap + 1)
    rng = np.random.default_rng(seed)
    offs = rng.choice(choices, size=N_SIM, replace=len(choices) < N_SIM)
    return lambda s: {a: np.roll(r, int(offs[s])) for a, r in pool.items()}


def weekly_pool(
    px: dict[str, ev.Closes], days: list[date], entry: int
) -> tuple[list[date], dict[str, np.ndarray]]:
    """Per-week log returns R(d) = close(first bar >= d + entry + 7) / close(first bar >= d +
    entry), trimmed to the span where every asset has one. The 4-week outcome of the gates is
    then exactly the sum of four consecutive R."""
    raw = {
        a: np.array([ev.window_return(p, d, entry, entry + 7, 7, LAST) for d in days])
        for a, p in px.items()
    }
    ok = np.all([np.isfinite(v) for v in raw.values()], axis=0)
    idx = np.flatnonzero(ok)
    lo, hi = int(idx[0]), int(idx[-1]) + 1
    gaps = int((~ok[lo:hi]).sum())
    if gaps:
        print("pool gaps set to 0:", gaps)
    return days[lo:hi], {a: np.nan_to_num(v[lo:hi], nan=0.0) for a, v in raw.items()}


def dk_closure(assets: list[str], row_asset: np.ndarray, period: np.ndarray, lags: int) -> gp.Fit:
    dummies = [(row_asset == k).astype(float) for k in range(len(assets))]

    def fit(
        dose: np.ndarray, y: np.ndarray, ctrl: np.ndarray | None, m: np.ndarray | None
    ) -> tuple[float, float]:
        cols = [*dummies, dose]
        if ctrl is not None:
            cols += list(ctrl.T)
        x = np.column_stack(cols)
        if m is not None:
            x, y, p = x[m], y[m], period[m]
        else:
            p = period
        return gp.dk_fit(x, y, p, lags, len(assets))

    return fit


def check_dk(
    fit_cols: list[np.ndarray], y: np.ndarray, period: np.ndarray, lags: int, j: int
) -> float:
    """|fast t - wide11_events.ols_dk t| on one design (the vectorized statistic is the same)."""
    t_slow = e11.ols_dk(fit_cols, y, period, lags)[1][j]
    t_fast = gp.dk_fit(np.column_stack(fit_cols), y, period, lags, j)[1]
    return abs(float(t_slow) - t_fast)


def weekly_design(
    name: str,
    assets: list[str],
    px: dict[str, ev.Closes],
    days: list[date],
    entry: int,
    rows: list[tuple[str, date]],
    dose_true: Callable[[str, date], float],
    dose_k: Callable[[str, date, int], float],
    old_shifts: list[int],
    controls: tuple[int, ...],
    lags: int,
    stored_t: float,
) -> gp.Design:
    pdays, pool = weekly_pool(px, days, entry)
    where = {d: i for i, d in enumerate(pdays)}
    keep = [(a, t) for a, t in rows if t in where]
    row_asset = np.array([assets.index(a) for a, _ in keep])
    row_i = np.array([where[t] for _, t in keep])
    true = np.array([dose_true(a, t) for a, t in keep])
    old = [np.array([dose_k(a, t, k) for a, t in keep]) for k in old_shifts]
    new = [np.array([dose_k(a, t, k) for a, t in keep]) for k in gp.EARLIER_SHIFTS]
    sigma = {a: float(pool[a].std()) for a in assets}
    pos = {}
    span = np.zeros(len(pdays), dtype=bool)
    span[row_i.min() : min(row_i.max() + 4, len(pdays))] = True
    for k, a in enumerate(assets):
        z = np.full(len(pdays), np.nan)
        m = row_asset == k
        z[row_i[m]] = gp.standardize(true[m])
        pos[a] = gp.position(z, 4, span)
    fit = dk_closure(assets, row_asset, row_i, lags)
    d = gp.Design(
        name,
        assets,
        rotations(pool, 52, SEED),
        sigma,
        pos,
        row_asset,
        row_i,
        4,
        true,
        old,
        new,
        fit,
        controls,
    )
    y0, c0 = gp.outcomes(d, pool)
    b0, t0 = fit(true, y0, c0, None)
    cols = [(row_asset == k).astype(float) for k in range(len(assets))] + [true]
    if c0 is not None:
        cols += list(c0.T)
    diff = check_dk(cols, y0, row_i, lags, len(assets))
    print(f"{name}: pool {pdays[0]}..{pdays[-1]} ({len(pdays)} weeks), rows {len(keep)}")
    print(f"{name}: rebuilt true t {t0:+.2f} (stored {stored_t:+.2f}); |fast - ols_dk| {diff:.1e}")
    print(f"{name}: sigma " + ", ".join(f"{a} {s * 100:.2f}%" for a, s in sigma.items()))
    d.name = f"{name}|rebuilt t {t0:+.2f}, stored {stored_t:+.2f}, |fast-ols_dk| {diff:.0e}"
    return d


def w25() -> tuple[gp.Design, dict]:
    assets = ["GLD", "TLT"]
    hist = harness.load_history("train", adjusted=False, syms=assets)  # as wide-13 ran
    px = {a: ev.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    rows_g = [g for g in dw.read_gpr_xls(dw.snapshot("gpr") / "data_gpr_daily_recent.xls")]
    rows_g = [g for g in rows_g if g.day <= LAST]
    za = e11.zscores(
        ev.weekly_log_mean({g.day: g.act for g in rows_g}, ev.mondays(date(1985, 1, 7), LAST))
    )
    gate = ev.mondays(date(2005, 1, 3), date(2025, 10, 6))
    rows = [(a, t) for a in assets for t in gate]
    d = weekly_design(
        "W25 act-haven",
        assets,
        px,
        ev.mondays(date(2004, 11, 1), LAST),
        9,
        rows,
        lambda a, t: za.get(t, math.nan),
        lambda a, t, k: ev.shifted(za, t, k),
        ev.SHIFTS,
        (),
        4,
        -1.02,
    )
    zs = np.array([za.get(t, math.nan) for t in gate])
    return d, {"per_year": 52, "n_eff": gp.n_eff(zs), "episodes": "n/a (continuous index)"}


def w26() -> tuple[gp.Design, dict]:
    hist = harness.load_history("train", adjusted=False, syms=["XLF"])  # as wide-13 ran
    px = {"XLF": ev.Closes({b.date: b.close for b in hist["XLF"]})}
    fs = dw.parse_fdic_failures((dw.snapshot("fdic") / "failures.json").read_text())
    fs = [f for f in fs if f.kind in ("FAILURE", "ASSISTANCE")]
    x = ev.failure_dose(((f.day, f.assets_k) for f in fs), ev.fridays(date(1990, 1, 5), LAST), LAST)
    gate = ev.fridays(date(2000, 1, 7), date(2025, 10, 3))
    d = weekly_design(
        "W26 failure-premium",
        ["XLF"],
        px,
        ev.fridays(date(1998, 12, 1), LAST),
        3,
        [("XLF", t) for t in gate],
        lambda a, t: x.get(t, math.nan),
        lambda a, t, k: ev.shifted(x, t, k),
        ev.SHIFTS,
        (4, 13, 26, 52),
        4,
        -0.48,
    )
    xs = np.array([x.get(t, math.nan) for t in gate])
    fw = [t for t in gate if x.get(t, 0) > 0]
    clusters = sum(1 for i, t in enumerate(fw) if i == 0 or (t - fw[i - 1]).days > 26 * 7)
    big = [t for t in gate if x.get(t, 0) > np.nanpercentile(xs[xs > 0], 90)]
    big_cl = sum(1 for i, t in enumerate(big) if i == 0 or (t - big[i - 1]).days > 26 * 7)
    ep = f"{len(fw)} failure weeks in {clusters} clusters (26-week gap)"
    ep += f"; top-decile weeks in {big_cl}"
    return d, {"per_year": 52, "n_eff": gp.n_eff(xs), "episodes": ep}


def w22() -> tuple[gp.Design, dict]:
    import wide11_hp as hp_mod

    assets = list(e11.GATE_CODES)
    folder = macro.cache_root() / "cftc" / "legacy"
    zips = [folder / "deacot1986_2016.zip"] + [folder / f"deacot{y}.zip" for y in range(2017, 2026)]
    hp = e11.read_zips(zips, e11.GATE_CODES, LAST)
    z = {a: e11.zscores(m) for a, m in hp.items()}
    hist = harness.load_history("train", syms=assets)  # wide-11 ran with adjusted bars
    px = {a: ev.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    lo, hi = hp_mod.GATE
    ref = hp_mod.REF
    # Report dates are Tuesdays bar holiday weeks; snap each row to its week's Tuesday.
    days = [ref + timedelta(days=7 * k) for k in range(250, 1350)]
    days = [t for t in days if t <= LAST]
    snap = {}
    rows = []
    for a in assets:
        for t in sorted(hp[a]):
            if lo <= t <= hi:
                tue = ref + timedelta(days=7 * hp_mod.week_of(t))
                snap[(a, tue)] = t
                rows.append((a, tue))
    d = weekly_design(
        "W22 hedging-pressure",
        assets,
        px,
        days,
        7,
        rows,
        lambda a, t: z[a].get(snap[(a, t)], math.nan),
        lambda a, t, k: e11.shifted_z(z[a], snap[(a, t)], k),
        e11.SHIFTS_W22,
        (4, 52),
        4,
        0.49,
    )
    ne = [
        gp.n_eff(np.array([z[a].get(snap[(a, t)], math.nan) for b, t in rows if b == a]))
        for a in assets
    ]
    return d, {
        "per_year": 52,
        "n_eff": float(np.mean(ne)),
        "episodes": "n/a (per-asset z, mean N_eff shown)",
    }


def w19() -> tuple[gp.Design, dict]:
    dbc = w9.Series("DBC")
    oni = ev9.parse_oni(w9.ONI.read_text())
    months = ev9.months((2006, 2), (2025, 10))
    r = np.array([ev9.horizon_return(dbc.days, dbc.logc, m, 1, LAST) for m in months])
    ok = np.flatnonzero(np.isfinite(r))
    months = months[ok[0] : ok[-1] + 1]
    r = np.nan_to_num(r[ok[0] : ok[-1] + 1], nan=0.0)
    where = {m: i for i, m in enumerate(months)}
    gate = [m for m in ev9.months(*w9.GATE) if m in where]
    row_i = np.array([where[m] for m in gate])
    row_asset = np.zeros(len(gate), dtype=int)
    true = np.array([ev9.dose(oni, m) for m in gate])
    old = [np.array([ev9.dose(oni, m, k) for m in gate]) for k in w9.SHIFTS]
    zp = np.full(len(months), np.nan)
    zp[row_i] = gp.standardize(true)
    span = np.zeros(len(months), dtype=bool)
    span[row_i.min() : min(row_i.max() + w9.H, len(months))] = True
    pos = {"DBC": gp.position(zp, w9.H, span)}

    def fit(
        dose: np.ndarray, y: np.ndarray, ctrl: np.ndarray | None, m: np.ndarray | None
    ) -> tuple[float, float]:
        ok2 = np.isfinite(dose) & np.isfinite(y)
        return w9.fit(dose[ok2], y[ok2])

    d = gp.Design(
        "W19 enso-commodity",
        ["DBC"],
        rotations({"DBC": r}, 12, SEED),
        {"DBC": float(r.std())},
        pos,
        row_asset,
        row_i,
        w9.H,
        true,
        old,
        None,
        fit,
    )
    y0, _ = gp.outcomes(d, {"DBC": r})
    b0, t0 = fit(true, y0, None, None)
    print(f"W19: pool {months[0]}..{months[-1]} ({len(months)} months), rows {len(gate)}")
    print(f"W19: rebuilt true t {t0:+.2f} (stored -0.92); sigma DBC {r.std() * 100:.2f}%/month")
    d.name = f"W19 enso-commodity|rebuilt t {t0:+.2f}, stored -0.92"
    return d, {"per_year": 12, "n_eff": gp.n_eff(true), "episodes": "about 8 ENSO swings (wide-9)"}


def hdd() -> tuple[gp.Design, dict]:
    root = macro.cache_root() / "weather-1"
    design = whdd.Design(whdd.load_hdd(root / "cpc-dd"))
    ung = whdd.load_ung(root / "yahoo" / "UNG.json")
    rows, ys = [], []
    for f in design.fridays:
        ij = wev.entry_exit(ung.days, f, LAST)
        if ij is None or math.isnan(design.x[f]):
            continue
        rows.append(f)
        ys.append(float(ung.logc[ij[1]] - ung.logc[ij[0]]))
    y = np.array(ys)
    where = {f: i for i, f in enumerate(rows)}
    true = np.array([design.dose(f, None) for f in rows])
    perms = wev.derangements(len(whdd.WINTERS), whdd.N_PLACEBO)  # the gate's own 40
    old = [np.array([design.dose(f, p) for f in rows]) for p in perms]
    noise_perms = wev.derangements(len(whdd.WINTERS), N_SIM, seed=SEED + 1)
    ok_rows = set(rows)

    def base(s: int) -> dict[str, np.ndarray]:
        p = noise_perms[s]
        out = np.full(len(rows), np.nan)
        for i, f in enumerate(rows):
            w = whdd.WINTERS.index(wev.winter_of(f))
            g = wev.placebo_friday(f, whdd.WINTERS[p[w]], design.by_winter)
            if g is not None and g in ok_rows:
                out[i] = y[where[g]]
        return {"UNG": out}

    halves = [np.array([wev.winter_of(f) in h for f in rows]) for h in whdd.HALVES]

    def fit(
        dose: np.ndarray, yy: np.ndarray, ctrl: np.ndarray | None, m: np.ndarray | None
    ) -> tuple[float, float]:
        if m is not None:
            return ols_hc1(dose[m], yy[m])
        return ols_hc1(dose, yy)

    n = len(rows)
    d = gp.Design(
        "weather-1 hdd-gas",
        ["UNG"],
        base,
        {"UNG": float(y.std())},
        {"UNG": gp.standardize(true)},
        np.zeros(n, dtype=int),
        np.arange(n),
        1,
        true,
        old,
        None,
        fit,
        (),
        halves,
    )
    b0, t0 = fit(true, y, None, None)
    print(
        f"HDD: rows {n}; rebuilt true t {t0:+.2f} (stored -0.29);"
        f" sigma UNG {y.std() * 100:.2f}%/week"
    )
    d.name = f"weather-1 hdd-gas|rebuilt t {t0:+.2f}, stored -0.29"
    return d, {"per_year": 52, "n_eff": gp.n_eff(true), "episodes": "18 winters"}


GATES: dict[str, Callable[[], tuple[gp.Design, dict]]] = {
    "W25": w25,
    "W26": w26,
    "W22": w22,
    "W19": w19,
    "HDD": hdd,
}


def spread(a: np.ndarray) -> str:
    return (
        f"SD {a.std(ddof=1):.2f}, median {np.median(a):+.2f},"
        f" share |t| >= 2 {np.mean(np.abs(a) >= 2):.0%}."
    )


def report(key: str, d: gp.Design, info: dict, res: gp.SimResult) -> list[str]:
    name, check = d.name.split("|", 1)
    py = info["per_year"]
    unit = "week" if py == 52 else "month"
    sig = ", ".join(f"{a} {s * 100:.2f}%" for a, s in d.sigma.items())
    same = d.new is None
    no = np.array(res.null_old)
    nn = np.array(res.null_new)
    b0 = d.base(0)
    n_a = len(d.assets)
    rho = 0.0
    if n_a > 1:
        cm = np.corrcoef(np.array([b0[a] for a in d.assets]))
        rho = float((cm.sum() - n_a) / (n_a * (n_a - 1)))
    mult = math.sqrt(n_a / (1 + (n_a - 1) * rho))

    def irr(f: float) -> float:
        return gp.ir(f, py) * mult

    L = [
        f"# Gate power: {name} (lane gate-power)",
        "",
        "Card: `research/gate-power.md` (pushed before this ran).",
        "Script `research/lib/gatepower_run.py`",
        f"(GATE={key}). {N_SIM} simulations per effect size; noise = the gate's real returns"
        + (" with winters permuted" if key == "HDD" else " rotated against the dose calendar")
        + f"; planted effect f x sigma per unit-SD position (sigma per {unit}: {sig}).",
        f"Rebuild check: {check}. Rows {len(d.row_i)}. Dose N_eff {info['n_eff']:.0f};"
        f" episodes: {info['episodes']}.",
        "",
        "## Detection rate by planted effect",
        "",
        f"IR = f x sqrt({py}) x {mult:.2f}: the standalone information ratio of the timing rule"
        f" trading all {n_a} gate asset(s) with equal risk (mean pairwise return correlation"
        f" {rho:+.2f}; x sqrt(n / (1 + (n - 1) rho))). Added = Sharpe gained over `tsmom12`"
        " (1.05) if that rule is mixed in uncorrelated, in the best mix.",
        "",
        "| f | %/"
        + unit
        + " per SD | IR | Added | t >= 2 only | Old rule | Corrected rule"
        + (" | Old + halves |" if d.subsets else " |"),
        "|---:|---:|---:|---:|---:|---:|---:|" + ("---:|" if d.subsets else ""),
    ]
    sig_mean = float(np.mean(list(d.sigma.values())))
    for q, f in enumerate(res.fs):
        i = irr(f)
        row = (
            f"| {f:.2f} | {f * sig_mean * 100:.3f} | {i:.2f} | {gp.added_sharpe(i):+.3f} |"
            f" {res.rate_t2[q]:.0%} | {res.rate_old[q]:.0%} | {res.rate_new[q]:.0%} |"
        )
        if d.subsets:
            row += f" {res.rate_old_plus[q]:.0%} |"
        L.append(row)
    L += [
        "",
        "## Minimum detectable effect, 80% power",
        "",
        "| Rule | f | %/" + unit + " per SD | IR | Added Sharpe |",
        "|---|---:|---:|---:|---:|",
    ]
    rules = [
        ("t >= 2 only (N(0,1) null)", res.rate_t2),
        ("Old rule (placebos as run)", res.rate_old),
    ]
    rules.append(
        (
            "Corrected rule" + (" (= old here)" if same else " (earlier doses k = +27..+183)"),
            res.rate_new,
        )
    )
    if d.subsets:
        rules.append(("Old rule + both halves > 0 (gate as carded)", res.rate_old_plus))
    for nm, rates in rules:
        m = gp.mde(res.fs, rates)
        top = res.fs[-1]
        if math.isnan(m):
            L.append(
                f"| {nm} | > {top:.2f} | > {top * sig_mean * 100:.2f} | > {irr(top):.2f} |"
                f" > {gp.added_sharpe(irr(top)):+.2f} |"
            )
        else:
            i = irr(m)
            L.append(
                f"| {nm} | {m:.3f} | {m * sig_mean * 100:.3f} | {i:.2f} |"
                f" {gp.added_sharpe(i):+.3f} |"
            )
    tn = np.array(res.true_null)
    L += [
        "",
        "## Null at f = 0 (all draws pooled)",
        "",
        f"True-dose t over {len(tn)} draws: " + spread(tn),
        "Old placebos: " + spread(no),
    ]
    if not same:
        L.append("Corrected placebos: " + spread(nn))
    L += [
        f"False-pass rate (f = 0): old {res.rate_old[0]:.1%}, corrected"
        f" {res.rate_new[0]:.1%}, t >= 2 only {res.rate_t2[0]:.1%}.",
        "",
    ]
    return L


def main() -> None:
    which = os.environ.get("GATE", "W25,W26,W22,W19,HDD").split(",")
    for key in which:
        d, info = GATES[key]()
        if DRY:
            continue
        res = gp.simulate(d, n_sim=N_SIM)
        out = report(key, d, info, res)
        (RESULTS / f"gate-power-{key.lower()}.md").write_text("\n".join(out))
        print("\n".join(out))


if __name__ == "__main__":
    main()
