"""jst-gates-1: two kill-only gates on the JST panel. Card: research/cards/jst-gates-1.md.

    uv run python -I research/lib/jstgates1.py [--log]

W38 `consumption-cycle`: next year's log equity return over bills on the Hamilton-filter
consumption cycle (JST `rconsbarro`), outcomes 1904-1913, 1920-1938, 1947, 20 earlier-dose
placebos. W39 `bank-capital-premium`: the same on JST `lev` minus its trailing 10-year mean,
outcomes 1925-2020 without 1939-1946, 40 earlier-dose placebos. Both pooled with country dummies
and Driscoll-Kraay t (2 lags). Nulls: earlier shifts (deciding), a returns-side AR-preserving
bootstrap under H0 (pass condition), phase-randomised surrogates with shared phases (shown).
Writes research/results/jst-gates-1.md (statistics only; JST R6 is CC BY-NC-SA 4.0); `--log`
appends the tries rows once. Replications R38/R39 run only if their gate passes (card).
"""

from __future__ import annotations

import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gatepower as gp  # noqa: E402
import jstautocorr2 as ja2  # noqa: E402

OUT = HERE.parent / "results" / "jst-gates-1.md"
TRIES = HERE.parent / "tries.md"
LAGS = 2
B_BOOT = 199
N_SURR = 40
BURN = 30
VARS = ["rconsbarro", "lev", "eq_tr", "bill_rate", "bond_tr", "eq_dp", "crisisJST", "cpi"]
SUSPECT: dict[str, tuple[int, int]] = {
    "NOR": (1881, 1920), "BEL": (1870, 1914), "DEU": (1890, 1913), "PRT": (1870, 1987),
    "ESP": (1941, 2017),
}  # fmt: skip

Panel = dict[str, dict[int, float]]  # iso -> year -> value


# --- data ---


def load_jst(path: Path | None = None) -> dict[str, Panel]:
    import long_macro as lm
    import long_macro_build as lmb
    import long_x as lx

    p = path or lmb.root() / "jst" / "JSTdatasetR6.xlsx"
    j = lm.parse_jst(lx.xlsx_rows(p, "Sheet1"), VARS)
    return {v: {iso: {d.year: x for d, x in ser} for iso, ser in j[v].items()} for v in VARS}


def excess(num: Panel, bill: Panel) -> Panel:
    """ln(1 + num) - ln(1 + bill_rate) per country-year (both present)."""
    out: Panel = {}
    for iso, s in num.items():
        b = bill.get(iso, {})
        out[iso] = {y: math.log1p(v) - math.log1p(b[y]) for y, v in s.items() if y in b}
    return out


def hyper_years(cpi: dict[int, float]) -> frozenset[int]:
    return frozenset(y for y in cpi if y - 1 in cpi and cpi[y] / cpi[y - 1] > 1.5)


def dropped(iso: str, y: int, hyper: frozenset[int]) -> bool:
    """jst-autocorr-2 point 2: war, closure, hyperinflation and interpolated years."""
    if ja2.disrupted(iso, y, hyper):
        return True
    a, b = ja2.INTERP.get(iso, (0, -1))
    return a <= y <= b


def suspect(iso: str, y: int) -> bool:
    a, b = SUSPECT.get(iso, (0, -1))
    return a <= y <= b


# --- doses ---


def hamilton(c: dict[int, float], min_pairs: int = 8) -> dict[int, float]:
    """cc(t) = c(t) - fitted value of OLS c(s) ~ 1 + c(s-2) + c(s-3) over s <= t (expanding),
    once at least `min_pairs` pairs exist."""
    out: dict[int, float] = {}
    rows: list[tuple[float, float, float]] = []
    for t in sorted(c):
        if t - 2 in c and t - 3 in c:
            rows.append((c[t], c[t - 2], c[t - 3]))
            if len(rows) >= min_pairs:
                a = np.array(rows)
                x = np.column_stack([np.ones(len(a)), a[:, 1], a[:, 2]])
                beta, *_ = np.linalg.lstsq(x, a[:, 0], rcond=None)
                out[t] = float(c[t] - (beta[0] + beta[1] * c[t - 2] + beta[2] * c[t - 3]))
    return out


def trail_dev(s: dict[int, float], n: int = 10, need: int = 8) -> dict[int, float]:
    """s(t) minus the mean of s over t-n..t-1 (at least `need` of those values)."""
    out: dict[int, float] = {}
    for t in sorted(s):
        past = [s[u] for u in range(t - n, t) if u in s]
        if len(past) >= need:
            out[t] = s[t] - float(np.mean(past))
    return out


def zscore(d: dict[int, float], y0: int, y1: int) -> dict[int, float]:
    v = np.array([x for y, x in d.items() if y0 <= y <= y1])
    if len(v) < 3 or v.std() == 0:
        return {}
    m, s = float(v.mean()), float(v.std())
    return {y: (x - m) / s for y, x in d.items() if y0 <= y <= y1}


# --- the statistic ---


@dataclass
class Design:
    rows: list[tuple[str, int]]  # (iso, outcome year)
    dp: Panel
    crisis: Panel | None  # None: no crisis control
    controls: bool = True


def base_rows(
    countries: Sequence[str], years: Sequence[int], y: Panel, z: Panel, dp: Panel,
    crisis: Panel | None, hyper: dict[str, frozenset[int]],
) -> list[tuple[str, int]]:  # fmt: skip
    """Rows (iso, t+1): outcome kept and present, dose of t, controls of t present."""
    out = []
    for iso in countries:
        ys, zs, ds = y.get(iso, {}), z.get(iso, {}), dp.get(iso, {})
        for t1 in years:
            t = t1 - 1
            if dropped(iso, t1, hyper.get(iso, frozenset())) or t1 not in ys or t not in zs:
                continue
            if not all(u in ys for u in (t - 2, t - 1, t)) or t not in ds:
                continue
            if crisis is not None and t not in crisis.get(iso, {}):
                continue
            out.append((iso, t1))
    return out


@dataclass
class Fit:
    b: float
    t: float
    n: int


def stat(des: Design, y: Panel, z: Panel, k: int = 0, rows: Sequence[tuple[str, int]] | None = None,
         out_y: Panel | None = None) -> Fit:  # fmt: skip
    """Pooled OLS of outcome(i, t+1) on z(i, t-k), country dummies and controls (trailing 1- and
    3-year log excess returns from `y`, eq_dp, crisis); Driscoll-Kraay t, 2 lags, by year."""
    oy = out_y if out_y is not None else y
    rs = [(i, t1) for i, t1 in (rows if rows is not None else des.rows)
          if t1 - 1 - k in z.get(i, {}) and t1 in oy.get(i, {})]  # fmt: skip
    if len(rs) < 10:
        return Fit(math.nan, math.nan, len(rs))
    isos = sorted({i for i, _ in rs})
    cols = []
    for i, t1 in rs:
        t = t1 - 1
        r = [z[i][t - k]]
        if des.controls:
            yi = y[i]
            r += [yi[t], yi[t - 2] + yi[t - 1] + yi[t], des.dp[i][t]]
            if des.crisis is not None:
                r.append(des.crisis[i][t])
        r += [1.0 if i == c else 0.0 for c in isos]
        cols.append(r)
    x = np.array(cols)
    yy = np.array([oy[i][t1] for i, t1 in rs])
    per = np.array([t1 for _, t1 in rs])
    b, t = gp.dk_fit(x, yy, per, LAGS, 0)
    return Fit(b, t, len(rs))


def rank_low(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly below `true` (1 = the lowest)."""
    return 1 + sum(o < true for o in others if not math.isnan(o))


# --- nulls ---


def ar1(pairs: Sequence[tuple[float, float]]) -> tuple[float, float]:
    """(intercept, slope) of OLS x(t) ~ 1 + x(t-1) over (x(t-1), x(t)) pairs."""
    a = np.array(pairs)
    x = np.column_stack([np.ones(len(a)), a[:, 0]])
    beta, *_ = np.linalg.lstsq(x, a[:, 1], rcond=None)
    return float(beta[0]), float(beta[1])


@dataclass
class BootModel:
    years: list[int]
    cm: tuple[float, float]
    em: dict[int, float]
    cd: dict[str, tuple[float, float]]
    ed: dict[str, dict[int, float]]
    cz: dict[str, tuple[float, float]]
    ez: dict[str, dict[int, float]]
    both: dict[str, list[int]] = field(default_factory=dict)


def boot_model(
    countries: Sequence[str], y: Panel, z: Panel, y0: int, y1: int,
    hyper: dict[str, frozenset[int]],
) -> BootModel:  # fmt: skip
    """AR(1) of the common mean m, of each country's d = y - m (kept years) and of each dose z,
    with their residuals by year (card, null 2)."""
    keep = {i: {t: v for t, v in y.get(i, {}).items()
                if y0 <= t <= y1 and not dropped(i, t, hyper.get(i, frozenset()))}
            for i in countries}  # fmt: skip
    years = list(range(y0, y1 + 1))
    m = {t: float(np.mean(v)) for t in years if (v := [keep[i][t] for i in countries if t in keep[i]])}

    def resid(s: dict[int, float]) -> tuple[tuple[float, float], dict[int, float]]:
        pr = [(s[t - 1], s[t]) for t in sorted(s) if t - 1 in s]
        c = ar1(pr)
        return c, {t: s[t] - c[0] - c[1] * s[t - 1] for t in sorted(s) if t - 1 in s}

    cm, em = resid(m)
    cd, ed, cz, ez = {}, {}, {}, {}
    for i in countries:
        d = {t: v - m[t] for t, v in keep[i].items()}
        cd[i], ed[i] = resid(d)
        cz[i], ez[i] = resid(z[i])
    both = {i: sorted(set(ed[i]) & set(ez[i])) for i in countries}
    return BootModel(years, cm, em, cd, ed, cz, ez, both)


def simulate(bm: BootModel, rng: np.random.Generator, zyears: dict[str, Sequence[int]]
             ) -> tuple[Panel, Panel]:  # fmt: skip
    """One path under H0: years drawn jointly (all residuals of one historical year)."""
    pool = sorted(bm.em)
    n = BURN + len(bm.years)
    taus = [pool[j] for j in rng.integers(0, len(pool), n)]
    m = 0.0
    msim = []
    for tau in taus:
        m = bm.cm[0] + bm.cm[1] * m + bm.em[tau]
        msim.append(m)
    ys: Panel = {}
    zs: Panel = {}
    for i in bm.cd:
        d = zv = 0.0
        ysi, zsi = {}, {}
        own = bm.both[i]
        for j, tau in enumerate(taus):
            if tau in bm.ed[i] and tau in bm.ez[i]:
                s = tau
            else:
                s = own[int(rng.integers(0, len(own)))]
            d = bm.cd[i][0] + bm.cd[i][1] * d + bm.ed[i][s]
            zv = bm.cz[i][0] + bm.cz[i][1] * zv + bm.ez[i][s]
            if j >= BURN:
                t = bm.years[j - BURN]
                ysi[t] = msim[j] + d
                zsi[t] = zv
        ys[i] = ysi
        zyr = set(zyears[i])
        zs[i] = {t: v for t, v in zsi.items() if t in zyr}
    return ys, zs


def bootstrap(des: Design, y: Panel, z: Panel, countries: Sequence[str], y0: int, y1: int,
              hyper: dict[str, frozenset[int]], seed: int, b: int = B_BOOT) -> list[float]:  # fmt: skip
    bm = boot_model(countries, y, z, y0, y1, hyper)
    rng = np.random.default_rng(seed)
    zyears = {i: sorted(z[i]) for i in countries}
    out = []
    for _ in range(b):
        ys, zs = simulate(bm, rng, zyears)
        out.append(stat(des, ys, zs).t)
    return out


def phase_panel(z: Panel, countries: Sequence[str], g0: int, g1: int, m: int, seed: int
                ) -> list[Panel]:  # fmt: skip
    """m multivariate phase surrogates (Prichard-Theiler): each country's own Fourier transform on
    the grid g0..g1 (gaps linearly filled for the transform, ends held), the same random phase
    ADDED to every country's own phases, so amplitudes and cross-country phase differences
    stay; the surrogate keeps only the country's real dose years."""
    grid = np.arange(g0, g1 + 1)
    n = len(grid)
    nf = n // 2 + 1
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 2 * np.pi, (m, nf))
    ph[:, 0] = 0.0
    if n % 2 == 0:
        ph[:, -1] = 0.0
    out: list[Panel] = [{} for _ in range(m)]
    for i in countries:
        yrs = sorted(t for t in z[i] if g0 <= t <= g1)
        if len(yrs) < 4:
            continue
        x = np.interp(grid, yrs, [z[i][t] for t in yrs])
        f = np.fft.rfft(x - x.mean())
        s = np.fft.irfft(f[None, :] * np.exp(1j * ph), n=n, axis=1) + x.mean()
        idx = {int(t): j for j, t in enumerate(grid)}
        for j in range(m):
            out[j][i] = {t: float(s[j, idx[t]]) for t in yrs}
    return out


def acf1(z: Panel, countries: Sequence[str]) -> float:
    """Pooled lag-1 autocorrelation of the dose (within country, demeaned)."""
    num = den = 0.0
    for i in countries:
        s = z[i]
        mu = float(np.mean(list(s.values())))
        num += sum((s[t] - mu) * (s[t - 1] - mu) for t in s if t - 1 in s)
        den += sum((v - mu) ** 2 for v in s.values())
    return num / den


def spread(ts: Sequence[float]) -> str:
    a = np.array([t for t in ts if not math.isnan(t)])
    q = np.quantile(a, [0.05, 0.5, 0.95])
    return (f"SD {a.std(ddof=1):.2f}, share |t| >= 2 {np.mean(np.abs(a) >= 2):.0%}, 5/50/95% "
            f"{q[0]:+.2f} / {q[1]:+.2f} / {q[2]:+.2f}, extremes {a.min():+.2f} / {a.max():+.2f}")  # fmt: skip


# --- one gate ---


@dataclass
class Gate:
    gid: str
    idea: str
    countries: list[str]
    years: list[int]
    halves: tuple[list[int], list[int]]
    shifts: list[int]
    span: tuple[int, int]  # y span for the bootstrap
    zspan: tuple[int, int]  # dose grid
    seeds: tuple[int, int]  # bootstrap, phase
    kill_rank: int
    crisis: bool


@dataclass
class GateResult:
    fit: Fit
    shift_t: list[float]
    rank: int
    boot_t: list[float]
    boot_p: float
    phase_t: list[float]
    phase_rank: int
    acf: float
    halves: tuple[Fit, Fit]
    nosus: Fit
    verdict: str
    lines: list[str] = field(default_factory=list)


def verdict(r: GateResult, g: Gate, n_null: int) -> str:
    if not r.fit.b < 0 or r.rank > g.kill_rank:
        return "KILL (clean): " + ("b >= 0" if not r.fit.b < 0 else
                                   f"rank {r.rank} of {n_null + 1} worse than {g.kill_rank}")  # fmt: skip
    ok = (r.rank <= 2 and r.fit.t <= -2 and r.halves[0].b < 0 and r.halves[1].b < 0
          and r.nosus.b < 0 and r.boot_p <= 0.05)  # fmt: skip
    return "NOT DEAD YET (kill-only pass)" if ok else "FAIL (not a clean kill; not supported)"


def run_gate(g: Gate, y: Panel, z: Panel, dp: Panel, crisis: Panel | None,
             hyper: dict[str, frozenset[int]], with_phase_rank: bool = True) -> GateResult:  # fmt: skip
    rows = base_rows(g.countries, g.years, y, z, dp, crisis, hyper)
    des = Design(rows, dp, crisis)
    fit = stat(des, y, z)
    sh = [stat(des, y, z, k).t for k in g.shifts]
    rank = rank_low(fit.t, sh)
    boot = bootstrap(des, y, z, g.countries, *g.span, hyper, g.seeds[0])
    bp = (1 + sum(t <= fit.t for t in boot)) / (len(boot) + 1)
    surr = phase_panel(z, g.countries, *g.zspan, N_SURR, g.seeds[1])
    pt = [stat(des, y, s).t for s in surr]
    prank = rank_low(fit.t, pt)
    h = tuple(stat(des, y, z, rows=[r for r in rows if r[1] in set(hh)]) for hh in g.halves)
    nosus = stat(des, y, z, rows=[r for r in rows if not suspect(*r)])
    res = GateResult(fit, sh, rank, boot, bp, pt, prank, acf1(z, g.countries),
                     (h[0], h[1]), nosus, "")  # fmt: skip
    res.verdict = verdict(res, g, len(g.shifts))
    return res


def shown(g: Gate, y: Panel, z: Panel, z2: Panel | None, dp: Panel, crisis: Panel | None,
          hyper: dict[str, frozenset[int]], bond: Panel | None) -> list[tuple[str, str]]:  # fmt: skip
    rows = base_rows(g.countries, g.years, y, z, dp, crisis, hyper)
    des = Design(rows, dp, crisis)
    out: list[tuple[str, str]] = []

    def fmt(f: Fit) -> str:
        return f"b {f.b:+.4f}, t {f.t:+.2f}, rows {f.n}"

    out.append(("(a) no controls", fmt(stat(Design(rows, dp, crisis, controls=False), y, z))))
    lag2 = stat(des, y, z, 1)
    out.append(("(b) dose of year t-1 (second lag)", fmt(lag2)))
    if z2 is not None:
        rows2 = base_rows(g.countries, g.years, y, z2, dp, crisis, hyper)
        d2 = Design(rows2, dp, crisis)
        f2 = stat(d2, y, z2)
        r2 = rank_low(f2.t, [stat(d2, y, z2, k).t for k in g.shifts])
        out.append(("(c) second form: c(t) minus mean c(t-10..t-1)",
                    f"{fmt(f2)}, shift rank {r2} of {len(g.shifts) + 1}"))  # fmt: skip
    sus = [r for r in rows if suspect(*r)]
    out.append(("(d) without suspect periods",
                f"{fmt(stat(des, y, z, rows=[r for r in rows if not suspect(*r)]))} "
                f"({len(sus)} suspect rows left out)"))  # fmt: skip
    for lab, hh in zip(("(e) half 1", "(e) half 2"), g.halves, strict=True):
        out.append((lab, fmt(stat(des, y, z, rows=[r for r in rows if r[1] in set(hh)]))))
    # (f) feedback: z(i, t) on y(i, t), y(i, t-1), country dummies
    fr = [(i, t1 - 1) for i, t1 in rows if t1 - 2 in y[i]]
    isos = sorted({i for i, _ in fr})
    x = np.array([[y[i][t], y[i][t - 1]] + [1.0 if i == c else 0.0 for c in isos] for i, t in fr])
    zz = np.array([z[i][t] for i, t in fr])
    per = np.array([t for _, t in fr])
    b0, t0 = gp.dk_fit(x, zz, per, LAGS, 0)
    b1, t1_ = gp.dk_fit(x, zz, per, LAGS, 1)
    out.append(("(f) feedback: z(t) on y(t), y(t-1)",
                f"on y(t) b {b0:+.3f} t {t0:+.2f}; on y(t-1) b {b1:+.3f} t {t1_:+.2f}; rows {len(fr)}"))  # fmt: skip
    # (i) common rows: rows every placebo has
    common = [r for r in rows if all(r[1] - 1 - k in z[r[0]] for k in g.shifts)]
    if len(common) >= 10:
        fc = stat(des, y, z, rows=common)
        rc = rank_low(fc.t, [stat(des, y, z, k, rows=common).t for k in g.shifts])
        out.append(("(i) common rows", f"{fmt(fc)}, shift rank {rc} of {len(g.shifts) + 1}"))
    # (j) per-country sign count, no controls
    neg = tot = 0
    for c in g.countries:
        rc_ = [r for r in rows if r[0] == c]
        if len(rc_) >= 10:
            f = stat(Design(rc_, dp, crisis, controls=False), y, z)
            tot += 1
            neg += f.b < 0
    out.append(("(j) countries with a negative own slope (no controls, >= 10 rows)", f"{neg} of {tot}"))
    if bond is not None:
        out.append(("(k) government bond excess return as outcome", fmt(stat(des, y, z, out_y=bond))))
    if crisis is not None:
        out.append(("(l) without the crisis control", fmt(stat(Design(rows, dp, None), y, z))))
    return out


def per_country_rows(rows: Sequence[tuple[str, int]]) -> str:
    c: dict[str, int] = {}
    for i, _ in rows:
        c[i] = c.get(i, 0) + 1
    return ", ".join(f"{k} {v}" for k, v in sorted(c.items()))


# --- main ---


def gates(jst: dict[str, Panel]) -> tuple[Gate, Gate]:
    y = excess(jst["eq_tr"], jst["bill_rate"])
    cons_years = list(range(1904, 1914)) + list(range(1920, 1939)) + [1947]
    zc = cons_dose(jst)
    cc = [i for i in sorted(y) if sum(1 for t in cons_years if t - 1 in zc.get(i, {}) and t in y[i]) >= 25]
    w38 = Gate("W38", "consumption-cycle", cc, cons_years,
               (list(range(1904, 1914)), list(range(1920, 1939)) + [1947]),
               list(range(4, 24)), (1871, 1947), (1880, 1946), (38, 381), 5, False)  # fmt: skip
    bank_years = [t for t in range(1925, 2021) if not 1939 <= t <= 1946]
    zb = bank_dose(jst)
    bc = [i for i in sorted(y) if zb.get(i)]
    w39 = Gate("W39", "bank-capital-premium", bc, bank_years,
               ([t for t in bank_years if t <= 1970], [t for t in bank_years if t >= 1971]),
               list(range(5, 45)), (1871, 2020), (1880, 2019), (39, 391), 10, True)  # fmt: skip
    return w38, w39


def cons_dose(jst: dict[str, Panel], second: bool = False) -> Panel:
    out: Panel = {}
    for i, s in jst["rconsbarro"].items():
        c = {t: math.log(v) for t, v in s.items() if v > 0}
        d = trail_dev(c) if second else hamilton(c)
        z = zscore(d, 1880, 1946)
        if z:
            out[i] = z
    return out


def bank_dose(jst: dict[str, Panel]) -> Panel:
    out: Panel = {}
    for i, s in jst["lev"].items():
        z = zscore(trail_dev(s), 1880, 2019)
        if z:
            out[i] = z
    return out


def main(argv: Sequence[str]) -> None:
    jst = load_jst()
    y = excess(jst["eq_tr"], jst["bill_rate"])
    bond = excess(jst["bond_tr"], jst["bill_rate"])
    hyper = {i: hyper_years(c) for i, c in jst["cpi"].items()}
    dp = jst["eq_dp"]
    crisis = jst["crisisJST"]
    w38, w39 = gates(jst)
    zc, zb = cons_dose(jst), bank_dose(jst)
    lines = [
        "# jst-gates-1: W38 `consumption-cycle` and W39 `bank-capital-premium` (JST R6)\n",
        "Card: `research/cards/jst-gates-1.md`. Statistics only (JST R6, CC BY-NC-SA 4.0; Jorda, "
        "Schularick and Taylor 2017). Generated by `research/lib/jstgates1.py`. Predicted sign b < 0; "
        "ranks count from the lowest t.\n",
    ]
    results = {}
    for g, z, z2, cr, bd in ((w38, zc, cons_dose(jst, second=True), None, None),
                             (w39, zb, None, crisis, bond)):  # fmt: skip
        r = run_gate(g, y, z, dp, cr, hyper)
        results[g.gid] = r
        rows = base_rows(g.countries, g.years, y, z, dp, cr, hyper)
        n = len(g.shifts)
        both = r.rank <= 2 and r.phase_rank <= 2 and r.fit.t <= -2
        lines += [
            f"## {g.gid} `{g.idea}`\n",
            f"- Countries ({len(g.countries)}): {', '.join(g.countries)}; rows {r.fit.n} "
            f"({per_country_rows(rows)}).",
            f"- **True: b {r.fit.b:+.4f} (log return per 1 sd of dose), DK t {r.fit.t:+.2f}; shift "
            f"rank {r.rank} of {n + 1}.**",
            f"- Shift null ({n} earlier doses, k = {g.shifts[0]}..{g.shifts[-1]}): {spread(r.shift_t)}.",
            f"- Bootstrap under H0 (B {len(r.boot_t)}): p {r.boot_p:.3f}; {spread(r.boot_t)}.",
            f"- Phase surrogates ({N_SURR}, shown): rank {r.phase_rank} of {N_SURR + 1}; "
            f"{spread(r.phase_t)}.",
            f"- Dose pooled lag-1 acf {r.acf:+.2f}; PR #207's proposed rule "
            f"({'applies' if r.acf >= 0.8 else 'does not apply'}: acf >= 0.8 needed) would "
            f"{'pass' if both else 'fail'} the rank-and-t part in both families.",
            f"- Halves: {r.halves[0].b:+.4f} (t {r.halves[0].t:+.2f}, {r.halves[0].n} rows) and "
            f"{r.halves[1].b:+.4f} (t {r.halves[1].t:+.2f}, {r.halves[1].n} rows); without "
            f"suspect periods {r.nosus.b:+.4f} (t {r.nosus.t:+.2f}, {r.nosus.n} rows).",
            f"- Shift placebo t by k: " + ", ".join(f"{k} {t:+.2f}" for k, t in zip(g.shifts, r.shift_t, strict=True)) + ".",
            f"- **Verdict by the card: {r.verdict}.**\n",
            "Shown, not gating:\n",
            "| Cell | Result |",
            "|---|---|",
        ]  # fmt: skip
        for lab, txt in shown(g, y, z, z2, dp, cr, hyper, bd):
            lines.append(f"| {lab} | {txt} |")
        lines.append("")
    passes = [gid for gid, r in results.items() if r.verdict.startswith("NOT DEAD")]
    lines.append(f"Replications: {'run for ' + ', '.join(passes) if passes else 'not run (no gate passed; card)'}.\n")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    if "--log" in argv:
        log_rows(results, w38, w39)


def log_rows(results: dict[str, GateResult], w38: Gate, w39: Gate) -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    rows = []
    for g, first, last in ((w38, "1904-12-31", "1947-12-31"), (w39, "1925-12-31", "2020-12-31")):
        r = results[g.gid]
        rows.append(
            f"| {now} | {g.idea} | {g.gid} (provisional id), jst-gates-1: next-year JST log equity "
            f"return over bills on {'the Hamilton consumption cycle (rconsbarro)' if g.gid == 'W38' else 'lev minus its trailing 10-year mean'}, "
            f"{len(g.countries)} countries, {r.fit.n} rows, DK 2 (b {r.fit.b:+.4f}, t {r.fit.t:+.2f}, "
            f"shift rank {r.rank}/{len(g.shifts) + 1}, bootstrap p {r.boot_p:.3f}, phase rank "
            f"{r.phase_rank}/41 shown): {r.verdict} | screen | train | {first} | {last} | - | - | - | - |"
        )  # fmt: skip
    with TRIES.open("a") as fh:
        fh.write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])

