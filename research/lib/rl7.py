"""rl-7: a small learned monthly policy against `tsmom12`, pooled over ~80 long series.

Card: research/cards/rl-7.md (pushed before any number). Data: `rl7_data`. Statistic:
pooled-2's joint circular 12-month block bootstrap (`pooled2_core.cells`, `bootstrap`).

    uv run python research/lib/rl7.py split   # counts only: which series train / hold out
    uv run python research/lib/rl7.py gate    # planted-signal gate, training cell only
    uv run python research/lib/rl7.py final   # the single held-out run (only after the gate)
"""

from __future__ import annotations

import json
import math
import sys
import warnings
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e4indep1_data as ed  # noqa: E402
import pooled2_core as qc  # noqa: E402

RESEARCH = Path(__file__).resolve().parents[1]
FEATURES = ("m1", "m3", "m6", "m12", "m24", "up1", "up3", "up6", "up12", "dvol", "drift")
LAGS = (1, 3, 6, 12, 24)
UPS = (1, 3, 6, 12)
WARM = 36  # s >= 36: sigma36 needs 36 log returns before s
Y_CLIP = 5.0
CUT_K = ed.mi(1990, 1)
MIN_SIDE = 60  # eligible months on a side of 1990-01 for a "spanning" series
SPLIT_SEED = 707
PEEK_SEED = 7070
GROUP_ORDER = ("US10", "DEV13", "WIDE10", "ETF8", "USB3", "GOV9", "FX9", "COM8", "P4", "N5")
ALPHAS = (0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05)
FOLDS, PURGE = 5, 36
PG_RISK, PG_L2, PG_LR, PG_STEPS = 1.0, 0.01, 0.05, 500
BLOCK, DRAWS, SEED = 12, 2000, 0
STRENGTHS = (None, 0.0, 0.05, 0.10)
Z_PICK, Z_FAMILY, KILL_HI = 4.70, 1.96, 0.05
CLASSES = ("equity", "rates", "fx", "commodity")


# --------------------------------------------------------------------------- features


def features(r: np.ndarray, gap: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """For one segment of monthly returns r: (t of each eligible month, X[t, 11], sigma36).
    The row for return t reads levels through return t - 1 - gap only (s = t - gap)."""
    lr = np.log1p(r)
    L = np.concatenate([[0.0], np.cumsum(lr)])  # L[i] = log level after i returns
    ts, rows, sig = [], [], []
    for t in range(WARM + gap, len(r)):
        s = t - gap
        s36 = float(lr[s - 36 : s].std(ddof=1))
        s12 = float(lr[s - 12 : s].std(ddof=1))
        if not (s36 > 0 and s12 > 0):
            continue
        x = [(L[s] - L[s - k]) / (s36 * math.sqrt(k)) for k in LAGS]
        x += [1.0 if L[s] > L[s - k] else 0.0 for k in UPS]
        x += [math.log(s12 / s36), (L[s] - L[0]) / (s * s36)]
        ts.append(t)
        rows.append(x)
        sig.append(s36)
    return np.array(ts, dtype=int), np.array(rows).reshape(-1, len(FEATURES)), np.array(sig)


@dataclass
class Rows:
    """Every eligible month of every series, in (market, segment, month) order."""

    market: np.ndarray  # index into names
    seg: np.ndarray  # global segment id
    k: np.ndarray  # month index of the return
    X: np.ndarray
    y: np.ndarray  # r / sigma36 (unclipped)
    r: np.ndarray  # the month's return (excess where the series is excess)
    cost: np.ndarray
    names: list[str]
    groups: list[str]
    classes: list[str]

    def up12(self) -> np.ndarray:
        return self.X[:, FEATURES.index("up12")]


def build_rows(series: Sequence[object]) -> Rows:
    cols: dict[str, list[np.ndarray]] = {c: [] for c in ("m", "g", "k", "X", "y", "r", "c")}
    names, groups, classes = [], [], []
    gid = 0
    for i, s in enumerate(series):
        names.append(s.name)  # type: ignore[attr-defined]
        groups.append(s.group)  # type: ignore[attr-defined]
        classes.append(s.cls)  # type: ignore[attr-defined]
        for k0, r in s.segs:  # type: ignore[attr-defined]
            t, X, sig = features(np.asarray(r, dtype=float), s.gap)  # type: ignore[attr-defined]
            if len(t) == 0:
                continue
            rr = np.asarray(r, dtype=float)[t]
            cols["m"].append(np.full(len(t), i))
            cols["g"].append(np.full(len(t), gid))
            cols["k"].append(k0 + t)
            cols["X"].append(X)
            cols["y"].append(rr / sig)
            cols["r"].append(rr)
            cols["c"].append(np.full(len(t), s.cost))  # type: ignore[attr-defined]
            gid += 1
    cat = {c: np.concatenate(v) for c, v in cols.items()}
    return Rows(
        cat["m"],
        cat["g"],
        cat["k"],
        cat["X"],
        cat["y"],
        cat["r"],
        cat["c"],
        names,
        groups,
        classes,
    )


# --------------------------------------------------------------------------- split


def split(rows: Rows, seed: int = SPLIT_SEED) -> np.ndarray:
    """Boolean per market: True = train market (card: spanning series halved per group)."""
    n = len(rows.names)
    pre = np.bincount(rows.market[rows.k < CUT_K], minlength=n)
    post = np.bincount(rows.market[rows.k >= CUT_K], minlength=n)
    train = np.zeros(n, dtype=bool)
    span = (pre >= MIN_SIDE) & (post >= MIN_SIDE)
    train[(post < MIN_SIDE)] = True
    rng = np.random.default_rng(seed)
    for g in GROUP_ORDER:
        idx = sorted(
            (i for i in range(n) if rows.groups[i] == g and span[i]), key=lambda i: rows.names[i]
        )
        if not idx:
            continue
        perm = rng.permutation(len(idx))
        for j in perm[: len(idx) // 2]:
            train[idx[j]] = True
    return train


# --------------------------------------------------------------------------- learners


def purged_folds(
    k: np.ndarray, n: int = FOLDS, purge: int = PURGE
) -> list[tuple[np.ndarray, np.ndarray]]:
    """n contiguous blocks of calendar months with about equal row counts; fit rows exclude
    months within `purge` of the validation block."""
    ks = np.sort(k)
    cuts = [ks[0]] + [ks[int(round(j * len(ks) / n))] for j in range(1, n)] + [ks[-1] + 1]
    out = []
    for j in range(n):
        lo, hi = cuts[j], cuts[j + 1]  # validation months [lo, hi)
        val = (k >= lo) & (k < hi)
        fit = (k < lo - purge) | (k >= hi + purge)
        out.append((np.flatnonzero(fit), np.flatnonzero(val)))
    return out


@dataclass
class Model:
    kind: str
    mu: np.ndarray
    sd: np.ndarray
    w: np.ndarray
    b: float
    alpha: float = math.nan

    def score(self, X: np.ndarray) -> np.ndarray:
        return ((X - self.mu) / self.sd) @ self.w + self.b

    def position(self, X: np.ndarray) -> np.ndarray:
        s = self.score(X)
        if self.kind == "lasso":
            return (s > 0).astype(float)
        return 1.0 / (1.0 + np.exp(-s))


def _std(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mu, sd = X.mean(0), X.std(0)
    return mu, np.where(sd > 0, sd, 1.0)


def _lasso(Z: np.ndarray, y: np.ndarray, alpha: float) -> tuple[np.ndarray, float]:
    if alpha == 0:
        A = np.column_stack([np.ones(len(Z)), Z])
        beta = np.linalg.lstsq(A, y, rcond=None)[0]
        return beta[1:], float(beta[0])
    from sklearn.linear_model import Lasso

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = Lasso(alpha=alpha, max_iter=20000, tol=1e-6).fit(Z, y)
    return np.asarray(m.coef_, dtype=float), float(m.intercept_)


def fit_lasso(
    X: np.ndarray, y: np.ndarray, k: np.ndarray, alphas: Sequence[float] = ALPHAS
) -> Model:
    yc = np.clip(y, -Y_CLIP, Y_CLIP)
    if len(alphas) == 1:
        a = alphas[0]
    else:
        mse = np.zeros(len(alphas))
        for fit, val in purged_folds(k):
            mu, sd = _std(X[fit])
            Zf, Zv = (X[fit] - mu) / sd, (X[val] - mu) / sd
            for i, al in enumerate(alphas):
                w, b = _lasso(Zf, yc[fit], al)
                mse[i] += float(np.mean((yc[val] - Zv @ w - b) ** 2))
        a = float(alphas[int(np.argmin(mse))])
    mu, sd = _std(X)
    w, b = _lasso((X - mu) / sd, yc, a)
    return Model("lasso", mu, sd, w, b, a)


def fit_pg(X: np.ndarray, y: np.ndarray, k: np.ndarray | None = None) -> Model:
    """Linear-sigmoid policy, exact-gradient ascent on mean(p y - (risk/2)(p y)^2) - l2/2 |w|^2."""
    yc = np.clip(y, -Y_CLIP, Y_CLIP)
    mu, sd = _std(X)
    Z = (X - mu) / sd
    th = np.zeros(Z.shape[1] + 1)
    m1, m2 = np.zeros_like(th), np.zeros_like(th)
    b1, b2, eps = 0.9, 0.999, 1e-8
    A = np.column_stack([Z, np.ones(len(Z))])
    for step in range(1, PG_STEPS + 1):
        p = 1.0 / (1.0 + np.exp(-(A @ th)))
        dJdp = yc - PG_RISK * p * yc * yc
        g = A.T @ (dJdp * p * (1 - p)) / len(Z)
        g[:-1] -= PG_L2 * th[:-1]
        m1 = b1 * m1 + (1 - b1) * g
        m2 = b2 * m2 + (1 - b2) * g * g
        th += PG_LR * (m1 / (1 - b1**step)) / (np.sqrt(m2 / (1 - b2**step)) + eps)
    return Model("pg", mu, sd, th[:-1].copy(), float(th[-1]))


FITTERS: dict[str, Callable[..., Model]] = {"lasso-sign": fit_lasso, "pg-lin": fit_pg}


def fit(learner: str, X: np.ndarray, y: np.ndarray, k: np.ndarray, ols: bool = False) -> Model:
    if learner == "lasso-sign":
        return fit_lasso(X, y, k, (0.0,) if ols else ALPHAS)
    return fit_pg(X, y, k)


# --------------------------------------------------------------------------- returns, statistic


def net(rows: Rows, sel: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Net monthly returns over the selected rows (in row order) for positions p (one per
    selected row); the position before a segment's first selected row is 0."""
    seg = rows.seg[sel]
    prev = np.concatenate([[0.0], p[:-1]])
    prev[np.concatenate([[True], seg[1:] != seg[:-1]])] = 0.0
    return p * rows.r[sel] - rows.cost[sel] * np.abs(p - prev)


def markets(rows: Rows, sel: np.ndarray, rets: dict[str, np.ndarray]) -> list[qc.Mkt]:
    """One `Mkt` per market with selected rows; rets: {rule: net return per selected row}."""
    out = []
    mk, kk = rows.market[sel], rows.k[sel]
    for i in np.unique(mk):
        j = mk == i
        per = np.array([ed.month_of(int(x)).toordinal() for x in kk[j]], dtype=np.int64)
        m = qc.Mkt(rows.names[i], rows.classes[i], "m", per)
        for rule, v in rets.items():
            m.rets[rule] = v[j]
        out.append(m)
    return out


def compare(ms: Sequence[qc.Mkt], rules: Sequence[str]) -> dict[str, object]:
    """Pooled paired Sharpe difference of rules[1:] against rules[0]."""
    c = qc.cells(ms, rules)
    sets = {"all": np.ones(len(ms), dtype=bool)}
    for cl in CLASSES:
        msk = np.array([g == cl for g in c.groups])
        if msk.any():
            sets[cl] = msk
    bt = qc.bootstrap(c, sets, BLOCK, DRAWS, SEED)
    out: dict[str, object] = {}
    for v, rule in enumerate(rules[1:]):
        p = qc.pooled(bt, "all", v)
        by = {}
        for cl in CLASSES:
            if cl in sets:
                q = qc.pooled(bt, cl, v)
                by[cl] = {"D": q.D, "se": q.se, "n": q.n, "n_pos": q.n_pos}
        out[rule] = {
            "D": p.D,
            "se": p.se,
            "z": p.z,
            "p_one": 0.5 * math.erfc(p.z / math.sqrt(2)),
            "n": p.n,
            "n_pos": p.n_pos,
            "by_class": by,
            "per_market": {nm: float(bt.d[v, i]) for i, nm in enumerate(c.names)},
        }
    return out


def sharpe(w: np.ndarray) -> float:
    sd = w.std()
    return float(w.mean() / sd * math.sqrt(12)) if sd > 0 else 0.0


def mean_sharpe(ms: Sequence[qc.Mkt], rule: str) -> float:
    return float(np.mean([sharpe(m.rets[rule]) for m in ms]))


# --------------------------------------------------------------------------- gate


def peek(rows: Rows, cell: np.ndarray, s: float, seed: int = PEEK_SEED) -> np.ndarray:
    """Planted input on the cell's rows: s * yz + sqrt(1 - s^2) * e, one fixed noise draw."""
    y = rows.y[cell]
    yz = (y - y.mean()) / y.std()
    e = np.random.default_rng(seed).standard_normal(len(y))
    return s * yz + math.sqrt(1 - s * s) * e


def oof(
    learner: str, X: np.ndarray, y: np.ndarray, k: np.ndarray, ols: bool = False
) -> tuple[np.ndarray, list[dict[str, object]]]:
    p = np.full(len(y), np.nan)
    info = []
    for fit_i, val_i in purged_folds(k):
        m = fit(learner, X[fit_i], y[fit_i], k[fit_i], ols)
        p[val_i] = m.position(X[val_i])
        info.append(
            {
                "alpha": m.alpha,
                "w": [round(float(x), 4) for x in m.w],
                "b": m.b,
                "mean_p": float(p[val_i].mean()),
            }
        )
    return p, info


def gate(rows: Rows, train: np.ndarray) -> dict[str, object]:
    cell = train[rows.market] & (rows.k < CUT_K)
    X, y, k = rows.X[cell], rows.y[cell], rows.k[cell]
    up = rows.up12()[cell]
    res: dict[str, object] = {"rows": int(cell.sum()), "markets": int(train.sum())}
    rets = {"tsmom12": net(rows, cell, up)}
    info: dict[str, object] = {}
    ics: dict[str, float] = {}
    for s in STRENGTHS:
        tag = "none" if s is None else f"{s:.2f}"
        if s is None:
            Xs = X
        else:
            pk = peek(rows, cell, s)
            ics[tag] = float(np.corrcoef(pk, y)[0, 1])
            Xs = np.column_stack([X, pk])
        for ln in FITTERS:
            p, inf = oof(ln, Xs, y, k)
            rets[f"{ln}@{tag}"] = net(rows, cell, p)
            info[f"{ln}@{tag}"] = inf
            if s is not None:
                Xc = np.column_stack([up, pk])
                pc_, infc = oof(ln, Xc, y, k, ols=True)
                rets[f"{ln}-ceil@{tag}"] = net(rows, cell, pc_)
                info[f"{ln}-ceil@{tag}"] = infc
            print(f"  {ln}@{tag} done", flush=True)
    res["peek_ic"] = ics
    res["fits"] = info
    ms = markets(rows, cell, rets)
    res["mean_sharpe"] = {r: mean_sharpe(ms, r) for r in rets}
    res["vs_tsmom12"] = compare(ms, list(rets))
    gates: dict[str, object] = {}
    for ln in FITTERS:
        lift = compare(ms, [f"{ln}@0.00", f"{ln}@0.05", f"{ln}@0.10"])
        ceil = compare(ms, [f"{ln}-ceil@0.00", f"{ln}-ceil@0.05", f"{ln}-ceil@0.10"])
        noise = compare(ms, [f"{ln}@none", f"{ln}@0.00"])[f"{ln}@0.00"]
        L5, L10 = lift[f"{ln}@0.05"], lift[f"{ln}@0.10"]
        C5 = ceil[f"{ln}-ceil@0.05"]
        g1 = L5["D"] > 0 and L5["p_one"] < 0.10  # type: ignore[index, operator]
        g2 = C5["D"] > 0 and L5["D"] >= C5["D"] / 3  # type: ignore[index, operator]
        g3 = L10["D"] > 0 and L10["p_one"] < 0.10  # type: ignore[index, operator]
        g4 = noise["D"] >= -0.025 and not (noise["D"] > 0 and noise["p_one"] < 0.10)  # type: ignore[index, operator]
        gates[ln] = {
            "lift_0.05": _short(L5),
            "lift_0.10": _short(L10),
            "ceil_0.05": _short(C5),
            "ceil_0.10": _short(ceil[f"{ln}-ceil@0.10"]),
            "noise_cost": _short(noise),
            "G1": bool(g1),
            "G2": bool(g2),
            "G3": bool(g3),
            "G4": bool(g4),
            "passes": bool(g1 and g2 and g3 and g4),
        }
    res["gate"] = gates
    return res


def _short(p: object) -> dict[str, float]:
    assert isinstance(p, dict)
    return {x: float(p[x]) for x in ("D", "se", "z", "p_one")}


# --------------------------------------------------------------------------- final


def final(rows: Rows, train: np.ndarray, learners: Sequence[str]) -> dict[str, object]:
    tcell = train[rows.market] & (rows.k < CUT_K)
    res: dict[str, object] = {"learners": list(learners)}
    pos = {"tsmom12": rows.up12()}
    models = {}
    for ln in learners:
        m = fit(ln, rows.X[tcell], rows.y[tcell], rows.k[tcell])
        models[ln] = {
            "alpha": m.alpha,
            "w": dict(zip(FEATURES, map(float, m.w), strict=True)),
            "b": m.b,
        }
        pos[ln] = m.position(rows.X)
    res["models"] = models
    allrows = np.ones(len(rows.k), dtype=bool)
    nets = {r: net(rows, allrows, p) for r, p in pos.items()}  # positions carry across 1990
    cells = {
        "primary: holdout markets x 1990-01..2025-10": ~train[rows.market] & (rows.k >= CUT_K),
        "train markets x 1990-01..2025-10": train[rows.market] & (rows.k >= CUT_K),
        "holdout markets x before 1990": ~train[rows.market] & (rows.k < CUT_K),
    }
    out = {}
    for name, sel in cells.items():
        if not sel.any():
            continue
        ms = markets(rows, sel, {r: v[sel] for r, v in nets.items()})
        cmp_ = compare(ms, list(pos))
        cmp_["mean_sharpe"] = {r: mean_sharpe(ms, r) for r in pos}
        cmp_["span"] = [
            ed.month_of(int(rows.k[sel].min())).isoformat(),
            ed.month_of(int(rows.k[sel].max())).isoformat(),
        ]
        cmp_["mean_position"] = {r: float(p[sel].mean()) for r, p in pos.items()}
        cmp_["turnover_per_year"] = {r: _turnover(rows, sel, p) for r, p in pos.items()}
        out[name] = cmp_
    res["cells"] = out
    prim = out["primary: holdout markets x 1990-01..2025-10"]
    verdicts = {}
    for ln in learners:
        p = prim[ln]
        assert isinstance(p, dict)
        D, se, z = p["D"], p["se"], p["z"]
        pos_cls = sum(1 for v in p["by_class"].values() if v["D"] > 0)
        if z >= Z_PICK and pos_cls >= 3:
            v = "pick candidate (held-out-year test next)"
        elif z >= Z_FAMILY:
            v = "positive, below the bar"
        elif D + 1.645 * se < KILL_HI:
            v = "killed (one-sided 95% upper bound below +0.05)"
        else:
            v = "not shown"
        verdicts[ln] = {"verdict": v, "classes_positive": pos_cls, "hi95": D + 1.645 * se}
    res["verdicts"] = verdicts
    return res


def _turnover(rows: Rows, sel: np.ndarray, p: np.ndarray) -> float:
    q = p[sel]
    seg = rows.seg[sel]
    d = np.abs(np.diff(q))[seg[1:] == seg[:-1]]
    return float(d.sum() / (len(q) / 12))


# --------------------------------------------------------------------------- tries rows


def _row(when: str, idea: str, variant: str, kind: str, lo: str, hi: str, sh: str) -> str:
    return f"| {when} | {idea} | {variant} | {kind} | train | {lo} | {hi} | {sh} | - | - | - |"


def gate_rows(res: dict, when: str, lo: str) -> list[str]:  # type: ignore[type-arg]
    hi = "1989-12-01"
    ms, vs, g = res["mean_sharpe"], res["vs_tsmom12"], res["gate"]
    out = [
        _row(
            when,
            "rl-7-control",
            "tsmom12@rl7-trainingcell (reference for the gate; 23 "
            "train markets x before 1990, mean per-market Sharpe)",
            "control",
            lo,
            hi,
            f"{ms['tsmom12']:.2f}",
        )
    ]
    for ln in FITTERS:
        for tag in ("none", "0.00", "0.05", "0.10"):
            for ceil in ("", "-ceil"):
                r = f"{ln}{ceil}@{tag}"
                if r not in ms:
                    continue
                v = vs[r]
                txt = (
                    f"{r} (planted gate, out of fold; vs tsmom12 D {v['D']:+.3f}, SE {v['se']:.3f}"
                )
                if tag in ("0.05", "0.10"):
                    lift = g[ln][f"{'ceil' if ceil else 'lift'}_{tag}"]
                    txt += f"; lift over @0.00 {lift['D']:+.3f}, z {lift['z']:+.2f}"
                if tag == "0.10" and not ceil:
                    txt += f"; gate {'PASSES' if g[ln]['passes'] else 'fails'}"
                    txt += " (" + ", ".join(k for k in ("G1", "G2", "G3", "G4") if g[ln][k])
                    txt += " met)"
                out.append(_row(when, "rl-7-control", txt + ")", "control", lo, hi, f"{ms[r]:.2f}"))
    return out


def final_rows(res: dict, when: str) -> list[str]:  # type: ignore[type-arg]
    out = []
    for name, c in res["cells"].items():
        lo, hi = c["span"]
        prim = name.startswith("primary")
        tag = {True: "primary-56", False: name.split(" x ")[0].replace(" ", "-")}[prim]
        if not prim:
            tag = "trainmkts-post1990" if name.startswith("train") else "holdmkts-pre1990"
        ms = c["mean_sharpe"]
        out.append(
            _row(
                when,
                "rl-7",
                f"tsmom12@rl7-{tag} (comparator, mean per-market Sharpe; {name})",
                "baseline" if prim else "robustness",
                lo,
                hi,
                f"{ms['tsmom12']:.2f}",
            )
        )
        for ln in res["learners"]:
            v = c[ln]
            txt = (
                f"{ln}@rl7-{tag} ({name}; frozen fit on the training cell; pooled dSharpe vs "
                f"tsmom12 {v['D']:+.3f}, SE {v['se']:.3f}, z {v['z']:+.2f}, d>0 in "
                f"{v['n_pos']}/{v['n']}"
            )
            if prim:
                vd = res["verdicts"][ln]
                txt += f"; one-sided 95% upper {vd['hi95']:+.3f}; {vd['verdict']}"
            out.append(
                _row(
                    when,
                    "rl-7",
                    txt + ")",
                    "variant" if prim else "robustness",
                    lo,
                    hi,
                    f"{ms[ln]:.2f}",
                )
            )
            if prim:
                for cl, b in v["by_class"].items():
                    out.append(
                        _row(
                            when,
                            "rl-7",
                            f"{ln}@rl7-primary-{cl} (class slice of the "
                            f"primary cell; dSharpe {b['D']:+.3f}, SE {b['se']:.3f}, d>0 "
                            f"in {b['n_pos']}/{b['n']})",
                            "robustness",
                            lo,
                            hi,
                            "-",
                        )
                    )
    return out


# --------------------------------------------------------------------------- main


def load() -> tuple[Rows, np.ndarray]:
    import rl7_data

    rows = build_rows(rl7_data.load_all())
    return rows, split(rows)


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "split"
    rows, train = load()
    out = RESEARCH / "results"
    if cmd == "split":
        for i, nm in enumerate(rows.names):
            pre = int(((rows.market == i) & (rows.k < CUT_K)).sum())
            post = int(((rows.market == i) & (rows.k >= CUT_K)).sum())
            side = "TRAIN" if train[i] else "hold "
            print(f"{nm:22s} {rows.groups[i]:7s} {side} pre {pre:5d} post {post:5d}")
        tc = train[rows.market] & (rows.k < CUT_K)
        pc_ = ~train[rows.market] & (rows.k >= CUT_K)
        print("training cell rows", int(tc.sum()), "markets", int(train.sum()))
        print("primary cell rows", int(pc_.sum()), "markets", int((~train).sum()))
    elif cmd == "gate":
        res = gate(rows, train)
        res["split"] = {nm: bool(train[i]) for i, nm in enumerate(rows.names)}
        (out / "rl-7-gate.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
        print(json.dumps(res["gate"], indent=1))
    elif cmd == "gate-rows":
        res = json.loads((out / "rl-7-gate.json").read_text())
        cell = train[rows.market] & (rows.k < CUT_K)
        lo = ed.month_of(int(rows.k[cell].min())).isoformat()
        print("\n".join(gate_rows(res, sys.argv[2], lo)))
    elif cmd == "final-rows":
        res = json.loads((out / "rl-7-final.json").read_text())
        print("\n".join(final_rows(res, sys.argv[2])))
    elif cmd == "final":
        g = json.loads((out / "rl-7-gate.json").read_text())["gate"]
        passed = [ln for ln in FITTERS if g[ln]["passes"]]
        if not passed:
            raise SystemExit("no learner passed the gate: the card forbids the final run")
        res = final(rows, train, passed)
        res["run_at"] = date.today().isoformat()
        (out / "rl-7-final.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
        print(json.dumps({k: v for k, v in res.items() if k != "cells"}, indent=1))
        for name, c in res["cells"].items():  # type: ignore[attr-defined]
            print(
                name, {ln: {x: c[ln][x] for x in ("D", "se", "z", "n", "n_pos")} for ln in passed}
            )


if __name__ == "__main__":
    main()
