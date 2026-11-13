"""Invest 1: monthly long-horizon allocator tests. Card: research/invest-1.md.

Run: uv run python -I research/lib/invest1.py   (appends rows to research/tries.md and writes
research/results/invest-1.md). Raw files are read from the cache root (research/macro.local.json
or GRIMSTRADE_DATA) and never written. Nothing after 2025-10 is loaded.
"""

from __future__ import annotations

import json
import sys
import zipfile
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from macro import cache_root  # noqa: E402
from stats import sharpe_diff_boot  # noqa: E402

RESEARCH = Path(__file__).resolve().parents[1]
TRIES = RESEARCH / "tries.md"
RESULTS = RESEARCH / "results" / "invest-1.md"

Y0 = 1871
LAST = (2025, 10)  # last month loaded; the protocol's held-out year starts 2025-11-11


def mi(y: int, m: int) -> int:
    """Month index: 1871-01 is 0."""
    return (y - Y0) * 12 + m - 1


N = mi(*LAST) + 1
LAG_CPI = 2
LAG_E = 6
COST = 0.001  # per side, on stock and bond weight changes
NAN = float("nan")


def ym(i: int) -> str:
    return f"{Y0 + i // 12}-{i % 12 + 1:02d}"


@dataclass(frozen=True)
class Raw:
    """Monthly inputs on the month grid (NaN where missing). Index i = end of month i."""

    P: np.ndarray  # S&P composite, monthly average of daily closes
    E: np.ndarray  # 12-month trailing earnings (Shiller, interpolated), forward-filled at end
    CPI: np.ndarray
    y: np.ndarray  # 10-year yield, decimal
    rf: np.ndarray  # T-bill return of month i, decimal
    S: np.ndarray  # stock total return of month i
    B: np.ndarray  # bond total return of month i (from yields)
    realtr: np.ndarray  # Shiller real total-return price (descriptive forecasts only)


def _grid() -> np.ndarray:
    return np.full(N, NAN)


# ---------------------------------------------------------------- loaders (raw cache, read only)


def _latest(path: Path) -> Path:
    return sorted(p for p in path.iterdir() if p.is_dir())[-1]


def load_shiller(root: Path) -> dict[str, np.ndarray]:
    import xlrd  # dev dependency; only the loader needs it

    book = xlrd.open_workbook(str(_latest(root / "shiller") / "ie_data.xls"))
    sh = book.sheet_by_name("Data")
    out = {k: _grid() for k in ("P", "E", "CPI", "GS10", "realtr")}
    cols = {"P": 1, "E": 3, "CPI": 4, "GS10": 6, "realtr": 9}
    for r in range(8, sh.nrows):
        row = sh.row_values(r)
        if not isinstance(row[0], float):
            continue
        y, m = (int(x) for x in f"{row[0]:.2f}".split("."))
        i = mi(y, m)
        if not 0 <= i < N:
            continue
        for k, c in cols.items():
            if isinstance(row[c], float):
                out[k][i] = row[c]
    return out


def load_french(root: Path) -> tuple[np.ndarray, np.ndarray]:
    z = zipfile.ZipFile(_latest(root / "french") / "F-F_Research_Data_Factors_CSV.zip")
    text = z.read(z.namelist()[0]).decode("latin1").splitlines()
    mkt, rf = _grid(), _grid()
    started = False
    for line in text:
        cells = [c.strip() for c in line.split(",")]
        if len(cells) == 5 and cells[0].isdigit() and len(cells[0]) == 6:
            started = True
            i = mi(int(cells[0][:4]), int(cells[0][4:]))
            if 0 <= i < N:
                mkt[i] = (float(cells[1]) + float(cells[4])) / 100
                rf[i] = float(cells[4]) / 100
        elif started:
            break  # the annual block follows
    return mkt, rf


def _fred(root: Path, sid: str) -> list[tuple[date, float]]:
    d = json.loads(
        (sorted((root / "fred" / "api" / "latest" / sid).glob("*.json"))[-1]).read_text()
    )
    return [(date.fromisoformat(o["date"]), float(o["value"])) for o in d["observations"]
            if o["value"] not in (".", "")]  # fmt: skip


def month_last(obs: list[tuple[date, float]]) -> np.ndarray:
    g = _grid()
    for d, v in obs:  # observations are in date order: the last one of a month wins
        i = mi(d.year, d.month)
        if 0 <= i < N:
            g[i] = v
    return g


def month_mean(obs: list[tuple[date, float]]) -> np.ndarray:
    s, n = np.zeros(N), np.zeros(N)
    for d, v in obs:
        i = mi(d.year, d.month)
        if 0 <= i < N:
            s[i] += v
            n[i] += 1
    with np.errstate(invalid="ignore"):
        return np.where(n > 0, s / np.maximum(n, 1), NAN)


def yahoo_daily(root: Path, sym: str, field: str = "adjclose") -> list[tuple[date, float]]:
    d = json.loads((_latest(root / "yahoo-1d") / f"{sym}.json").read_text())
    r = d["chart"]["result"][0]
    vals = (
        r["indicators"]["adjclose"][0]["adjclose"]
        if field == "adjclose"
        else (r["indicators"]["quote"][0][field])
    )
    return [(datetime.fromtimestamp(t, UTC).date(), float(v))
            for t, v in zip(r["timestamp"], vals, strict=True) if v is not None]  # fmt: skip


def bond_returns(y: np.ndarray, years: float = 10.0) -> np.ndarray:
    """Monthly return of a par bond bought at yield y[i-1] and repriced at y[i] a month later."""
    out = _grid()
    n = 2 * (years - 1 / 12)
    for i in range(1, N):
        c, yn = y[i - 1], y[i]
        if np.isnan(c) or np.isnan(yn):
            continue
        h = yn / 2
        price = c / 2 * (1 - (1 + h) ** -n) / h + (1 + h) ** -n
        out[i] = price - 1 + c / 12
    return out


def load() -> Raw:
    root = cache_root()
    sh = load_shiller(root)
    S, rf = load_french(root)
    cut = mi(2023, 8)  # Shiller's last row (2023-09) is a single day's close
    P = sh["P"].copy()
    P[cut + 1 :] = month_mean(yahoo_daily(root, "^GSPC", "close"))[cut + 1 :]
    E = sh["E"].copy()
    last_e = int(np.flatnonzero(~np.isnan(E))[-1])
    E[last_e + 1 :] = E[last_e]  # stale earnings after Shiller's last value (card)
    CPI = sh["CPI"].copy()
    k47 = mi(1947, 1)
    CPI[k47:] = month_mean(_fred(root, "CPIAUCSL"))[k47:]
    y = sh["GS10"] / 100
    k62 = mi(1962, 1)
    y[k62:] = month_last(_fred(root, "DGS10"))[k62:] / 100
    realtr = sh["realtr"].copy()
    realtr[cut + 1 :] = NAN
    return Raw(P=P, E=E, CPI=CPI, y=y, rf=rf, S=S, B=bond_returns(y), realtr=realtr)


# ---------------------------------------------------------------- signals (as-of only)


def shift(a: np.ndarray, k: int) -> np.ndarray:
    """out[i] = a[i-k] (NaN before the start)."""
    out = np.full_like(a, NAN)
    out[k:] = a[: len(a) - k]
    return out


def index_of(r: np.ndarray) -> np.ndarray:
    """Total-return index at month ends (NaN before the first return)."""
    out = _grid()
    v = 1.0
    seen = False
    for i, x in enumerate(r):
        if np.isnan(x):
            if seen:
                out[i] = v
            continue
        seen = True
        v *= 1 + x
        out[i] = v
    return out


def mom12(idx: np.ndarray) -> np.ndarray:
    return idx / shift(idx, 12) - 1


def sma10_up(idx: np.ndarray) -> np.ndarray:
    win = np.lib.stride_tricks.sliding_window_view(idx, 10).mean(axis=1)
    avg = np.full(N, NAN)
    avg[9:] = win
    out = np.where(np.isnan(avg), NAN, (idx > avg).astype(float))
    return out


def signals(raw: Raw) -> dict[str, np.ndarray]:
    """Every signal at the decision at the end of month i, from as-of data only."""
    cpi_l = shift(raw.CPI, LAG_CPI)
    real_e = shift(raw.E / raw.CPI, LAG_E)
    e10 = np.full(N, NAN)
    e10[119:] = np.lib.stride_tricks.sliding_window_view(real_e, 120).mean(axis=1)
    ey = e10 / (raw.P / cpi_l)
    infl12 = cpi_l / shift(cpi_l, 12) - 1
    infl10 = (cpi_l / shift(cpi_l, 120)) ** 0.1 - 1
    return {
        "ey": ey,
        "ecy": ey - (raw.y - infl10),
        "term": raw.y - 12 * raw.rf,
        "real": raw.y - infl12,
        "infl": infl12,
        "mom_s": mom12(index_of(raw.S)),
        "mom_b": mom12(index_of(raw.B)),
        "mom_c": mom12(index_of(raw.rf)),
        "sma_s": sma10_up(index_of(raw.S)),
        "sma_b": sma10_up(index_of(raw.B)),
    }


def pctile(x: np.ndarray, min_hist: int = 120) -> np.ndarray:
    """Share of earlier finite values below x[i]; 0.5 until there are min_hist of them."""
    out = np.full(len(x), 0.5)
    hist: list[float] = []
    for i, v in enumerate(x):
        if np.isnan(v):
            continue
        if len(hist) >= min_hist:
            out[i] = float(np.mean(np.asarray(hist) < v))
        hist.append(float(v))
    return out


# ---------------------------------------------------------------- rules -> (stocks, bonds) weights

Rule = Callable[[dict[str, np.ndarray]], tuple[np.ndarray, np.ndarray]]


def _const(s: float, b: float) -> Rule:
    return lambda g: (np.full(N, s), np.full(N, b))


def _tilt(name: str, sign: float = 1.0) -> Rule:
    def rule(g: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
        s = 0.6 + sign * 0.6 * (pctile(g[name]) - 0.5)
        return s, 1 - s

    return rule


def _on(x: np.ndarray) -> np.ndarray:
    """1 while a 12-month return is positive (NaN: held, the rule is its base until data)."""
    return np.where(np.isnan(x), 1.0, (x > 0).astype(float))


def tsmom12(g: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    return 0.5 * _on(g["mom_s"]), 0.5 * _on(g["mom_b"])


def infl_regime(g: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    hot = np.nan_to_num(g["infl"], nan=0.0) > 0.04
    return np.full(N, 0.6), np.where(hot, 0.0, 0.4)


def sma10_6040(g: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    return 0.6 * np.nan_to_num(g["sma_s"], nan=1.0), 0.4 * np.nan_to_num(g["sma_b"], nan=1.0)


def xmom(g: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    ms, mb, mc = (np.nan_to_num(g[k], nan=-np.inf) for k in ("mom_s", "mom_b", "mom_c"))
    mc = np.where(np.isinf(mc), 0.0, mc)
    stocks = (ms >= mb) & (ms > mc)
    bonds = (mb > ms) & (mb > mc)
    return stocks.astype(float), bonds.astype(float)


def ecy_trend(g: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    s, b = _tilt("ecy")(g)
    return s * _on(g["mom_s"]), b * _on(g["mom_b"])


BASELINES: dict[str, Rule] = {"6040": _const(0.6, 0.4), "bh-stocks": _const(1.0, 0.0),
                              "tsmom12-m": tsmom12}  # fmt: skip
VARIANTS: dict[str, Rule] = {
    "cape-tilt": _tilt("ey"),
    "ecy-tilt": _tilt("ecy"),
    "term-tilt": _tilt("term"),
    "real-tilt": _tilt("real", -1.0),
    "infl-regime": infl_regime,
    "6040-sma10": sma10_6040,
    "xmom": xmom,
    "ecy-trend": ecy_trend,
}


# ---------------------------------------------------------------- simulation


@dataclass(frozen=True)
class Run:
    first: int  # first return month
    ret: np.ndarray  # net monthly returns
    excess: np.ndarray  # over cash
    turnover: float  # sum of |weight changes| in stocks+bonds per year


def simulate(
    ws: np.ndarray, wb: np.ndarray, S: np.ndarray, B: np.ndarray, rf: np.ndarray,
    first: int, last: int, cost: float = COST, wg: np.ndarray | None = None,
    G: np.ndarray | None = None,
) -> Run:  # fmt: skip
    """Weights decided at the end of month i-1 earn month i, for return months first..last."""
    risky = [(ws, S), (wb, B)] + ([(wg, G)] if wg is not None and G is not None else [])
    drift = [w[first - 1] for w, _ in risky]
    rets, turn = [], 0.0
    for i in range(first, last + 1):
        target = [w[i - 1] for w, _ in risky]
        dw = sum(abs(t - d) for t, d in zip(target, drift, strict=True))
        turn += dw
        gross = sum(t * r[i] for t, (_, r) in zip(target, risky, strict=True))
        gross += (1 - sum(target)) * rf[i]
        net = gross - cost * dw
        rets.append(net)
        vals = [t * (1 + r[i]) for t, (_, r) in zip(target, risky, strict=True)]
        total = sum(vals) + (1 - sum(target)) * (1 + rf[i])
        drift = [v / total for v in vals]
    r = np.asarray(rets)
    return Run(first, r, r - rf[first : last + 1], turn / (len(r) / 12))


def sharpe_m(x: np.ndarray) -> float:
    sd = x.std(ddof=1)
    return float(x.mean() / sd * np.sqrt(12)) if sd > 0 else 0.0


def max_dd(r: np.ndarray) -> float:
    eq = np.cumprod(1 + r)
    return float((1 - eq / np.maximum.accumulate(eq)).max())


def cagr(r: np.ndarray) -> float:
    return float(np.prod(1 + r) ** (12 / len(r)) - 1)


# ---------------------------------------------------------------- long-horizon forecasts


def _ols(x: np.ndarray, y: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    X = np.column_stack([np.ones_like(x), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return float(beta[1]), X, y - X @ beta


def _hac_se(X: np.ndarray, u: np.ndarray, lags: int, bartlett: bool) -> float:
    xu = X * u[:, None]
    s = xu.T @ xu
    for k in range(1, lags + 1):
        w = 1 - k / (lags + 1) if bartlett else 1.0
        g = xu[k:].T @ xu[:-k]
        s += w * (g + g.T)
    xx = np.linalg.inv(X.T @ X)
    v = xx @ s @ xx
    return float(np.sqrt(v[1, 1])) if v[1, 1] > 0 else NAN


def forecast(
    sig: np.ndarray, realtr: np.ndarray, years: int, first: int, last: int
) -> dict[str, float]:
    """Slope of the next `years`-year log real stock return on a signal, three standard errors."""
    h = 12 * years
    fwd = np.full(N, NAN)
    fwd[: N - h] = np.log(realtr[h:] / realtr[: N - h])
    ok = [i for i in range(first, last + 1) if not np.isnan(sig[i]) and not np.isnan(fwd[i])]
    x, y = sig[ok], fwd[ok]
    b, X, u = _ols(x, y)
    r2 = 1 - u.var() / y.var()
    nw = _hac_se(X, u, int(1.5 * h), True)
    hh = _hac_se(X, u, h - 1, False)
    sub = ok[::h]
    bn, Xn, un = _ols(sig[sub], fwd[sub])
    sn = float(np.sqrt(un @ un / max(len(sub) - 2, 1) * np.linalg.inv(Xn.T @ Xn)[1, 1]))
    return {"b": b, "r2": r2, "t_nw": b / nw, "t_hh": b / hh, "n": len(ok),
            "b_non": bn, "t_non": bn / sn, "n_non": len(sub),
            "from": ok[0], "to": ok[-1]}  # fmt: skip


# ---------------------------------------------------------------- report

PERIODS = {"train": (mi(1927, 1), mi(1989, 12)), "oos": (mi(1990, 1), N - 1)}
DECADES = [(1927, 1939), (1940, 1949), (1950, 1959), (1960, 1969), (1970, 1979), (1980, 1989),
           (1990, 1999), (2000, 2009), (2010, 2019), (2020, 2025)]  # fmt: skip
ERAS = [(1994, 1999), (2000, 2009), (2010, 2016), (2017, 2021), (2022, 2025)]


NO_LOG = "--no-log" in sys.argv  # report-only rerun of configurations already logged


def log_try(variant: str, kind: str, period: str, run: Run, rf: np.ndarray) -> None:
    if NO_LOG:
        return
    last = run.first + len(run.ret) - 1
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | invest-1 | {variant} | {kind} | {period} | "
        f"{ym(run.first)} | {ym(last)} | {sharpe_m(run.excess):.2f} | "
        f"{np.prod(1 + run.ret) - 1:+.1%} | {max_dd(run.ret):.1%} | {run.turnover:.2f} |\n"
    )
    with TRIES.open("a") as f:
        f.write(row)


def sub(run: Run, a: int, b: int) -> np.ndarray:
    return run.excess[max(a - run.first, 0) : b - run.first + 1]


def _ffill(a: np.ndarray) -> np.ndarray:
    """Descriptive only (real returns): carry the last CPI into the final, unpublished month."""
    out = a.copy()
    for i in range(1, len(out)):
        if np.isnan(out[i]):
            out[i] = out[i - 1]
    return out


def real_cagr(run: Run, cpi: np.ndarray) -> float:
    cpi = _ffill(cpi)
    i0 = run.first
    infl = cpi[i0 : i0 + len(run.ret)] / cpi[i0 - 1 : i0 - 1 + len(run.ret)]
    return cagr((1 + run.ret) / infl - 1)


def worst_10y_real(run: Run, cpi: np.ndarray) -> float:
    cpi = _ffill(cpi)
    i0 = run.first
    infl = cpi[i0 : i0 + len(run.ret)] / cpi[i0 - 1 : i0 - 1 + len(run.ret)]
    lg = np.cumsum(np.log((1 + run.ret) / infl))
    lg = np.concatenate([[0.0], lg])
    return float(np.exp((lg[120:] - lg[:-120]).min() / 10) - 1)


def pval(a: np.ndarray, b: np.ndarray) -> float:
    return sharpe_diff_boot(a, b, draws=2000, mean_block=24, seed=0)[1]


def main() -> None:
    raw = load()
    g = signals(raw)
    rules = {**BASELINES, **VARIANTS}
    kinds = {k: "baseline" for k in BASELINES} | {k: "variant" for k in VARIANTS}
    weights = {k: f(g) for k, f in rules.items()}
    runs: dict[tuple[str, str], Run] = {}
    for k, (ws, wb) in weights.items():
        for p, (a, b) in PERIODS.items():
            runs[k, p] = simulate(ws, wb, raw.S, raw.B, raw.rf, a, b)
            log_try(k, kinds[k], p, runs[k, p], raw.rf)
    full = {k: simulate(ws, wb, raw.S, raw.B, raw.rf, PERIODS["train"][0], N - 1)
            for k, (ws, wb) in weights.items()}  # fmt: skip
    out = ["# Invest 1 results (generated by `research/lib/invest1.py`; card in `invest-1.md`)", ""]
    out += [f"Generated {datetime.now(UTC):%Y-%m-%d %H:%M} UTC. Monthly; Sharpe is in excess of "
            "T-bills x sqrt(12); p = one-sided paired stationary bootstrap (block 24 months, "
            "2,000 draws); costs 10 bps per side.", ""]  # fmt: skip
    verdict: dict[str, dict[str, object]] = {}
    for p, (a, b) in PERIODS.items():
        out += [
            f"## {p} ({ym(a)} .. {ym(b)})",
            "",
            "| Rule | Kind | Sharpe | vs 6040 | p | vs tsmom12-m | p | CAGR | Real CAGR | "
            "Max DD | Turnover/yr |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        base, trend = runs["6040", p], runs["tsmom12-m", p]
        for k in rules:
            r = runs[k, p]
            d6 = sharpe_m(r.excess) - sharpe_m(base.excess)
            dt = sharpe_m(r.excess) - sharpe_m(trend.excess)
            p6 = pval(r.excess, base.excess) if k != "6040" else NAN
            pt = pval(r.excess, trend.excess) if k != "tsmom12-m" else NAN
            verdict.setdefault(k, {})[p] = (d6, p6, dt, pt, max_dd(r.ret) - max_dd(base.ret))
            out.append(f"| {k} | {kinds[k]} | {sharpe_m(r.excess):.2f} | {d6:+.2f} | {p6:.3f} | "
                       f"{dt:+.2f} | {pt:.3f} | {cagr(r.ret):.1%} | {real_cagr(r, raw.CPI):.1%} | "
                       f"{max_dd(r.ret):.1%} | {r.turnover:.2f} |")  # fmt: skip
        out.append("")
    # decades
    out += ["## Sharpe by decade (whole run 1927-2025)", "",
            "| Rule | " + " | ".join(f"{a}-{b % 100:02d}" for a, b in DECADES)
            + " | ahead of 6040 |",
            "|---|" + "---:|" * (len(DECADES) + 1)]  # fmt: skip
    ahead: dict[str, int] = {}
    for k in rules:
        row, n_ahead = [], 0
        for a, b in DECADES:
            lo, hi = mi(a, 1), min(mi(b, 12), N - 1)
            s = sharpe_m(sub(full[k], lo, hi))
            s0 = sharpe_m(sub(full["6040"], lo, hi))
            n_ahead += s > s0
            row.append(f"{s:.2f}")
        ahead[k] = n_ahead
        out.append(f"| {k} | " + " | ".join(row) + f" | {n_ahead} |")
    out.append("")
    out += ["## Out-of-sample eras (protocol)", "",
            "| Rule | " + " | ".join(f"{a}-{b % 100:02d}" for a, b in ERAS) + " | worst 10y real |",
            "|---|" + "---:|" * (len(ERAS) + 1)]  # fmt: skip
    for k in rules:
        cells = [f"{sharpe_m(sub(full[k], mi(a, 1), min(mi(b, 12), N - 1))):.2f}" for a, b in ERAS]
        out.append(
            f"| {k} | " + " | ".join(cells) + f" | {worst_10y_real(full[k], raw.CPI):+.1%} |"
        )
    out.append("")
    # pass bars
    out += ["## Pass bars", "",
            "| Variant | 1 train p<0.10 | 2 OOS p<0.10 | 3 decades >= 6 | 4 DD | beats 60/40 | "
            "adds to trend |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    passed = []
    for k in VARIANTS:
        v = verdict[k]
        tr, oo = v["train"], v["oos"]
        assert isinstance(tr, tuple) and isinstance(oo, tuple)
        b1 = tr[0] > 0 and tr[1] < 0.10
        b2 = oo[0] > 0 and oo[1] < 0.10
        b3 = ahead[k] >= 6
        b4 = tr[4] <= 0.05 and oo[4] <= 0.05
        ok = b1 and b2 and b3 and b4
        tr_ok = ok and tr[2] > 0 and tr[3] < 0.10 and oo[2] > 0 and oo[3] < 0.10
        if ok:
            passed.append(k)
        yn = {True: "yes", False: "no"}
        out.append(f"| {k} | {yn[b1]} | {yn[b2]} | {yn[b3]} ({ahead[k]}) | {yn[b4]} | "
                   f"**{yn[ok]}** | {yn[tr_ok]} |")  # fmt: skip
    out.append("")
    for k in passed:  # robustness: 30 bps
        ws, wb = weights[k]
        for p, (a, b) in PERIODS.items():
            r = simulate(ws, wb, raw.S, raw.B, raw.rf, a, b, cost=0.003)
            log_try(f"{k} (30 bps)", "robustness", p, r, raw.rf)
            out.append(f"- {k} at 30 bps, {p}: Sharpe {sharpe_m(r.excess):.2f}")
    out += forecasts_section(raw, g)
    out += etf_section(raw, g)
    RESULTS.write_text("\n".join(out) + "\n")
    print("\n".join(out))


def forecasts_section(raw: Raw, g: dict[str, np.ndarray]) -> list[str]:
    out = ["", "## Long-horizon forecasts (descriptive)", "",
           "Next h-year log real stock return (Shiller real total-return price) on the as-of "
           "signal. t-values: Newey-West (lags 1.5h), Hansen-Hodrick (lags h-1), and plain OLS on "
           "non-overlapping windows (n_non points).", "",
           "| Signal | h | From | To | slope | R2 | t NW | t HH | n_non | slope non | t non |",
           "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    for name in ("ey", "ecy", "term", "real", "infl"):
        for h in (1, 5, 10):
            f = forecast(g[name], raw.realtr, h, mi(1881, 1), N - 1)
            out.append(f"| {name} | {h} | {ym(int(f['from']))} | {ym(int(f['to']))} | "
                       f"{f['b']:.2f} | {f['r2']:.2f} | {f['t_nw']:.1f} | {f['t_hh']:.1f} | "
                       f"{int(f['n_non'])} | {f['b_non']:.2f} | {f['t_non']:.1f} |")  # fmt: skip
    return out


def etf_section(raw: Raw, g: dict[str, np.ndarray]) -> list[str]:
    root = cache_root()
    mret = {}
    for sym in ("SPY", "IEF", "GLD"):
        px = month_last(yahoo_daily(root, sym))
        mret[sym] = px / shift(px, 1) - 1
    e = replace(raw, S=mret["SPY"], B=mret["IEF"])
    ge = signals(e) | {k: g[k] for k in ("ey", "ecy", "term", "real", "infl")}
    mom_g = mom12(index_of(mret["GLD"]))
    first, last = mi(2003, 9), N - 1
    out = ["", f"## ETF check (SPY / IEF / GLD, {ym(first)} .. {ym(last)}, robustness)", "",
           "| Rule | Sharpe | vs 6040 | p | vs tsmom12-m | p | CAGR | Max DD |",
           "|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    runs = {}
    for k, f in {**BASELINES, **VARIANTS}.items():
        ws, wb = f(ge)
        if k == "xmom":  # gold joins once it has 12 months of history
            ms, mb, mg = (np.nan_to_num(x, nan=-np.inf) for x in (ge["mom_s"], ge["mom_b"], mom_g))
            mc = np.nan_to_num(ge["mom_c"], nan=0.0)
            best = np.argmax(np.stack([ms, mb, mg]), axis=0)
            top = np.max(np.stack([ms, mb, mg]), axis=0)
            on = top > mc
            ws, wb, wg = ((best == j) & on for j in range(3))
            runs[k] = simulate(ws.astype(float), wb.astype(float), e.S, e.B, raw.rf, first, last,
                               wg=wg.astype(float), G=np.nan_to_num(mret["GLD"]))  # fmt: skip
        else:
            runs[k] = simulate(ws, wb, e.S, e.B, raw.rf, first, last)
        log_try(f"{k} (ETF)", "robustness", "oos", runs[k], raw.rf)
    for k, r in runs.items():
        d6 = sharpe_m(r.excess) - sharpe_m(runs["6040"].excess)
        dt = sharpe_m(r.excess) - sharpe_m(runs["tsmom12-m"].excess)
        p6 = pval(r.excess, runs["6040"].excess) if k != "6040" else NAN
        pt = pval(r.excess, runs["tsmom12-m"].excess) if k != "tsmom12-m" else NAN
        out.append(
            f"| {k} | {sharpe_m(r.excess):.2f} | {d6:+.2f} | {p6:.3f} | {dt:+.2f} | "
            f"{pt:.3f} | {cagr(r.ret):.1%} | {max_dd(r.ret):.1%} |"
        )
    return out


if __name__ == "__main__":
    main()
