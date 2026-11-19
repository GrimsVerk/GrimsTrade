"""register-2: record length, skew and kurtosis of logged tries, and the effective number of
independent trials from their return correlations (card: research/register-2.md).

    git fetch origin
    uv run --with numpy python research/register2.py all      # needs research/data/ (prices)

Steps (each can run alone):

- `tree`: extract `src/` and `research/lib/` of a research branch at a pinned commit into
  `research/data/register2/tree/<sha>/` (the harness and its baselines, as they were run).
- `baselines`: re-simulate every baseline of `research/lib/baselines.py` in that tree on train
  (`log=False`: already counted) and save their weekly returns.
- `live`: the live strategies (`grimstrade.strategies.LIVE`) through `grimstrade.gym` on the six
  assets, train period, raw prices (what the paper system trades), weekly returns.
- `curves`: equity curves the harness saved for logged tries (`research/data/runs/...`) in the
  directories listed in `research/register2.local.json` (gitignored; see the `.example`).
- `export` (register-4): add the local series to the committed weekly-returns store
  `research/register/returns/` (`grimstrade.returnstore`): every baseline and live series, and
  every saved curve that fits a register row. Commit the store with the generated files.
- `estimate`: match every series to its register rows, write `research/register/moments.jsonl`
  and `research/register/trials.json`; `grimstrade.register` turns them into BAR.md. Reads the
  committed store first and adds local series not in it, all rounded to 1e-6 and in one
  canonical order, so a clean checkout (store only) computes the same files:

    uv run --with numpy python research/register2.py estimate    # no research/data/ needed

Everything is deterministic (seeded k-means). Prices and intermediate series stay in the
gitignored `research/data/`; only the generated files and the store are committed.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import math
import subprocess
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np

from grimstrade import returnstore

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
WORK = RESEARCH / "data" / "register2"
LOCAL = RESEARCH / "register2.local.json"
REGISTER = RESEARCH / "register" / "tries.jsonl"
MOMENTS = RESEARCH / "register" / "moments.jsonl"
TRIALS = RESEARCH / "register" / "trials.json"
STORE = ROOT / returnstore.STORE  # register-4: committed weekly returns
LOCAL_FILES = ("baselines", "curves", "live")  # intermediates in WORK, one per source kind

HARNESS_REF = "origin/summary-2"  # a research branch with research/lib/baselines.py
TRAIN_START, TRAIN_END, TRAIN_LAST_BAR = date(1994, 2, 1), date(2025, 11, 9), date(2025, 11, 10)
WEEKS_PER_YEAR = 365.25 / 7
SHARPE_TOL = 0.0051  # logged Sharpes have two decimals
START_TOL = timedelta(days=10)
# Correlation windows (Fridays). Main: every series covering it; check: the primary 1994 test.
WINDOWS = {
    "2012-2025": (date(2012, 1, 6), date(2025, 11, 7)),
    "1994-2025": (date(1994, 2, 4), date(2025, 11, 7)),
}
MAIN_WINDOW = "2012-2025"
SEED = 20261118
N_INIT = 5
K_MAX = 60  # ONC searches k = 2..min(K_MAX, M - 1); a best k at the cap is flagged
SELECTABLE = ("variant", "baseline")
# register-3: the correlation sample keeps at most CAP series per family (the `Idea` column),
# the first by SHA-256 of idea/variant/start (a pick that never looks at returns).
CAP = 10
CAP_SENSITIVITY = (1, 5, 20)


# --- weekly returns ---


def calendar(equity: Sequence[tuple[date, float]]) -> tuple[list[date], np.ndarray]:
    """Equity on every calendar day, carried over days without a bar (the harness's rule)."""
    first, last = equity[0][0], equity[-1][0]
    days = [first + timedelta(days=k) for k in range((last - first).days + 1)]
    known = dict(equity)
    out = np.empty(len(days))
    cur = equity[0][1]
    for k, d in enumerate(days):
        cur = known.get(d, cur)
        out[k] = cur
    return days, out


def daily_sharpe(eq: np.ndarray) -> float:
    """The harness's logged Sharpe: calendar-day returns, population sd, times sqrt(365)."""
    r = eq[1:] / eq[:-1] - 1
    sd = r.std()
    return float(r.mean() / sd * math.sqrt(365)) if sd > 0 else 0.0


def weekly(days: list[date], eq: np.ndarray) -> tuple[list[str], list[float]]:
    """Returns from Friday to Friday; each keyed by the Friday it ends on."""
    idx = [i for i, d in enumerate(days) if d.weekday() == 4]
    keys = [days[j].isoformat() for j in idx[1:]]
    rets = [float(eq[j] / eq[i] - 1) for i, j in zip(idx, idx[1:], strict=False)]
    return keys, rets


@dataclass
class Series:
    source: str  # "harness@<sha>", "live@<sha>", "curve"
    idea: str
    variant: str
    start: str  # first day of the record (the row's From)
    sharpe: float  # harness formula, daily
    weeks: list[str]
    rets: list[float]

    def to_json(self) -> str:
        return json.dumps(self.__dict__, separators=(",", ":"))


def series_of(source: str, idea: str, variant: str, equity: Sequence[tuple[date, float]]) -> Series:
    days, eq = calendar(equity)
    keys, rets = weekly(days, eq)
    return Series(source, idea, variant, days[0].isoformat(), daily_sharpe(eq), keys, rets)


def save(path: Path, series: Iterable[Series]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [s.to_json() for s in series]
    path.write_text("".join(r + "\n" for r in rows))
    return len(rows)


def load(path: Path) -> list[Series]:
    if not path.exists():
        return []
    return [Series(**json.loads(ln)) for ln in path.read_text().splitlines() if ln.strip()]


# --- the committed store (register-4) ---


def to_row(s: Series) -> returnstore.Row:
    return returnstore.Row.of(s.source, s.idea, s.variant, s.start, s.sharpe, s.weeks, s.rets)


def from_row(r: returnstore.Row) -> Series:
    return Series(r.source, r.idea, r.variant, r.start, r.sharpe, r.weeks(), list(r.rets))


def kind(source: str) -> str:
    """`harness`, `live` or `curve`."""
    return source.split("@")[0]


def local_rows() -> list[returnstore.Row]:
    """The local intermediates (gitignored, this machine only) as store rows."""
    return [to_row(s) for name in LOCAL_FILES for s in load(WORK / f"{name}.jsonl") if s.rets]


def sources() -> tuple[list[Series], list[Series], list[Series], list[returnstore.Row]]:
    """Baseline, curve and live series: the committed store first, then local series not in
    it; rounded to 1e-6 and in canonical order either way. Also: those local rows."""
    stored = returnstore.read(STORE)
    keys = {r.key() for r in stored}
    local = [r for r in returnstore.merge(local_rows()) if r.key() not in keys]
    out: dict[str, list[Series]] = {"harness": [], "curve": [], "live": []}
    for r in returnstore.merge(stored, local):
        out[kind(r.source)].append(from_row(r))
    return out["harness"], out["curve"], out["live"], local


def export() -> None:
    """Add the local series to the store: every baseline and live series, and every saved
    curve that fits a register row (ambiguous fits too). Stored rows always stay. Over the
    budget, drop curves that fit no selectable row, last by SHA-256 of idea/variant/start
    first, and say so (card register-4)."""
    stored = returnstore.read(STORE)
    keys = {r.key() for r in stored}
    rows = register_rows()
    keep = to_store([r for r in returnstore.merge(local_rows()) if r.key() not in keys], rows)
    store = returnstore.merge(stored, keep)
    total = store_bytes(store)
    if total > returnstore.BUDGET:
        store = within_budget(store, rows)
        print(f"export: over {returnstore.BUDGET:,} bytes, kept {len(store)}", file=sys.stderr)
    sizes = returnstore.write(STORE, store)
    print(
        f"export: {len(store)} series ({len(keep)} new) in {len(sizes)} files, "
        f"{sum(sizes.values()):,} bytes",
        file=sys.stderr,
    )


def to_store(new: list[returnstore.Row], rows: list[dict[str, Any]]) -> list[returnstore.Row]:
    """The rows the store takes: baselines, live series, curves that fit a register row."""
    curve_fits = fits([from_row(r) for r in new if kind(r.source) == "curve"], rows)
    fitting = {(s.idea, s.variant, s.start, s.sharpe) for ss in curve_fits.values() for s in ss}
    return [
        r
        for r in new
        if kind(r.source) != "curve" or (r.idea, r.variant, r.start, r.sharpe) in fitting
    ]


def store_bytes(store: list[returnstore.Row]) -> int:
    by_file: dict[str, list[returnstore.Row]] = {}
    for r in store:
        by_file.setdefault(returnstore.family_file(r.idea), []).append(r)
    return sum(len(returnstore.encode(v)) for v in by_file.values())


def within_budget(
    store: list[returnstore.Row], rows: list[dict[str, Any]]
) -> list[returnstore.Row]:
    """Keep baselines, live series and curves fitting a selectable row; add the other curves
    by SHA-256 of idea/variant/start while the store stays under the budget."""
    sel = [r for r in rows if r["kind"] in SELECTABLE]
    sel_fits = fits([from_row(r) for r in store if kind(r.source) == "curve"], sel)
    protected = {(s.idea, s.variant, s.start, s.sharpe) for ss in sel_fits.values() for s in ss}
    must, rest = [], []
    for r in store:
        key = (r.idea, r.variant, r.start, r.sharpe)
        (must if kind(r.source) != "curve" or key in protected else rest).append(r)
    rest.sort(key=lambda r: hashlib.sha256(f"{r.idea}/{r.variant}/{r.start}".encode()).hexdigest())
    lo, hi = 0, len(rest)
    while lo < hi:  # the most of `rest` (in that order) that fits
        mid = (lo + hi + 1) // 2
        if store_bytes(must + rest[:mid]) <= returnstore.BUDGET:
            lo = mid
        else:
            hi = mid - 1
    return returnstore.merge(must, rest[:lo])


# --- sources ---


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout


def tree(ref: str = HARNESS_REF) -> Path:
    sha = git("rev-parse", ref).strip()
    out = WORK / "tree" / sha[:12]
    if not (out / "research" / "lib" / "baselines.py").exists():
        out.mkdir(parents=True, exist_ok=True)
        tar = subprocess.run(
            ["git", "archive", sha, "src", "research/lib"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        subprocess.run(["tar", "-x", "-C", str(out)], input=tar, check=True)
        (out / "research" / "data").symlink_to(Path("../../../../"), target_is_directory=True)
    return out


def baselines(tree_dir: Path) -> None:
    """Runs inside the extracted tree (its own src and harness): `baselines.py`'s runs, unlogged."""
    sys.path[:0] = [str(tree_dir / "research" / "lib"), str(tree_dir / "src")]
    import baselines as b  # type: ignore[import-not-found]
    import common as c  # type: ignore[import-not-found]

    src = f"harness@{tree_dir.name}"
    out: list[Series] = []

    def keep(variant: str, strategy: Any, u: Any) -> None:
        r = c.go(b.IDEA, variant, strategy, u, "baseline", log=False)
        out.append(series_of(src, b.IDEA, r.variant, list(zip(r.days, r.equity, strict=True))))

    six = c.ctx("six")
    keep("bh-spy", c.weekly(c.hold("SPY")), six)
    keep("bh-btc", c.weekly(c.hold("BTC")), six)
    keep("sixty-forty", c.weekly(c.sixty_forty), six)
    for n, f in b.twins().items():
        keep(n, f, six)
    for name in ("etf", "coin", "idx"):
        u = c.ctx(name)
        for n, f in b.twins().items():
            keep(n, f, u)
    for name in b.SINGLES:
        u = c.ctx(name)
        for n, f in b.twins().items():
            if n != "inverse-vol":
                keep(n, f, u)
    print(f"baselines: {save(WORK / 'baselines.jsonl', out)} series", file=sys.stderr)


def live() -> None:
    """The live strategies on the six assets, train period, through the repo's own gym (a
    bisect slice per day instead of `gym.backtest`'s scan; same bars seen)."""
    sys.path.insert(0, str(ROOT / "src"))
    from grimstrade import data, gym
    from grimstrade.strategies import LIVE

    hist = data.load_all(RESEARCH, list(data.UNIVERSE))
    hist = {s: [b for b in bars if b.date <= TRAIN_LAST_BAR] for s, bars in hist.items()}
    closes = {
        s: [data.close_time(data.UNIVERSE[s], b.date) for b in bars] for s, bars in hist.items()
    }
    sha = git("rev-parse", "HEAD").strip()[:12]
    out = []
    for name, decide in LIVE.items():
        decs = []
        d = TRAIN_START
        while d <= TRAIN_END:
            t = datetime.combine(d, gym.DECIDE_AT, tzinfo=UTC)
            seen = {s: bars[: bisect.bisect_right(closes[s], t)] for s, bars in hist.items()}
            decs.append(gym.Decision(t, decide(seen)[0]))
            d += timedelta(days=1)
        res = gym.simulate(decs, hist)
        out.append(series_of(f"live@{sha}", "live", name, res.equity))
        print(f"live: {name} done", file=sys.stderr)
    save(WORK / "live.jsonl", out)


def curves() -> None:
    """Saved harness curves (`<dir>/<idea>/<variant>.train.csv`) from the local directories."""
    if not LOCAL.exists():
        print(f"curves: no {LOCAL.name}, skipped", file=sys.stderr)
        save(WORK / "curves.jsonl", [])
        return
    dirs = [ROOT / p for p in json.loads(LOCAL.read_text())["run_dirs"]]  # relative: to the repo
    seen: set[str] = set()
    out = []
    for top in dirs:
        for path in sorted(top.glob("*/*.train.csv")):
            raw = path.read_bytes()
            h = hashlib.sha256(raw).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            rows = list(csv.reader(raw.decode().splitlines()))[1:]
            if len(rows) < 30:
                continue
            eq = [(date.fromisoformat(a), float(b)) for a, b in rows]
            variant = path.name[: -len(".train.csv")]
            out.append(series_of("curve", path.parent.name, variant, eq))
    print(f"curves: {save(WORK / 'curves.jsonl', out)} distinct curves", file=sys.stderr)


# --- matching ---


def register_rows() -> list[dict[str, Any]]:
    return [json.loads(ln) for ln in REGISTER.read_text().splitlines() if ln.strip()]


def fits(series: list[Series], rows: list[dict[str, Any]]) -> dict[str, list[Series]]:
    """Register id -> every series that fits the row: idea, variant and period (train) agree,
    it starts within START_TOL of the row's From and its Sharpe equals the logged one to two
    decimals."""
    by_key: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for r in rows:
        if r["period"] == "train" and r["sharpe"] is not None:
            by_key.setdefault((r["idea"], r["variant"]), []).append(r)
    out: dict[str, list[Series]] = {}
    for s in series:
        for r in by_key.get((s.idea, s.variant), []):
            dt = abs(date.fromisoformat(s.start) - date.fromisoformat(r["from"]))
            if dt <= START_TOL and abs(s.sharpe - r["sharpe"]) <= SHARPE_TOL:
                out.setdefault(r["id"], []).append(s)
    return out


def match(series: list[Series], rows: list[dict[str, Any]]) -> dict[str, Series]:
    """Register id -> its series (`fits`). A row two different series fit is dropped
    (ambiguous)."""
    out = {}
    for ident, ss in fits(series, rows).items():
        if len({tuple(np.round(x.rets, 12)) for x in ss}) == 1:
            out[ident] = ss[0]
    return out


def logged() -> dict[str, Any]:
    """Register id -> the shape the harness logged with the row (register-3), from
    `research/tries-shape.jsonl` on disk and on every remote branch."""
    sys.path.insert(0, str(ROOT / "src"))
    from grimstrade import register

    return register.logged_shapes(ROOT, register.read_register(REGISTER.read_text(), "register"))


# --- moments and clustering ---


def shape(rets: Sequence[float]) -> tuple[int, float, float, float]:
    """Weeks, annualised weekly Sharpe, skew, excess kurtosis (population moments)."""
    r = np.asarray(rets)
    m, sd = r.mean(), r.std()
    if sd == 0:
        return len(r), 0.0, 0.0, 0.0
    z = (r - m) / sd
    return (
        len(r),
        float(m / sd * math.sqrt(WEEKS_PER_YEAR)),
        float((z**3).mean()),
        float((z**4).mean() - 3),
    )


def window_matrix(series: list[Series], a: date, b: date) -> tuple[list[int], np.ndarray]:
    """Indexes of the series that cover every Friday in [a, b], and their returns there
    (weeks x series)."""
    keys = []
    d = a + timedelta(days=7)
    while d <= b:
        keys.append(d.isoformat())
        d += timedelta(days=7)
    cols, idx = [], []
    for i, s in enumerate(series):
        pos = {k: j for j, k in enumerate(s.weeks)}
        if keys[0] in pos and keys[-1] in pos and pos[keys[-1]] - pos[keys[0]] == len(keys) - 1:
            col = np.asarray(s.rets[pos[keys[0]] : pos[keys[-1]] + 1])
            if col.std() > 0:
                cols.append(col)
                idx.append(i)
    return idx, np.column_stack(cols) if cols else np.empty((len(keys), 0))


def silhouette(dist: np.ndarray, labels: np.ndarray) -> np.ndarray:
    """Rousseeuw's silhouette of each point from a full distance matrix."""
    n = len(labels)
    ks = np.unique(labels)
    onehot = (labels[:, None] == ks[None, :]).astype(float)
    sums = dist @ onehot  # n x k: total distance to each cluster
    sizes = onehot.sum(0)
    own = np.searchsorted(ks, labels)
    a_cnt = sizes[own] - 1
    a = np.where(a_cnt > 0, sums[np.arange(n), own] / np.maximum(a_cnt, 1), 0.0)
    mean_other = sums / sizes[None, :]
    mean_other[np.arange(n), own] = np.inf
    b = mean_other.min(1)
    s = (b - a) / np.maximum(np.maximum(a, b), 1e-300)
    return np.where(a_cnt > 0, s, 0.0)  # a singleton's silhouette is 0 (Rousseeuw)


def kmeans(x: np.ndarray, k: int, rng: np.random.Generator, iters: int = 100) -> np.ndarray:
    """Lloyd's k-means with k-means++ seeding (as scikit-learn's default), on the rows of x."""
    n = len(x)
    sq = (x**2).sum(1)
    centers = [x[rng.integers(n)]]
    d2 = ((x - centers[0]) ** 2).sum(1)
    for _ in range(1, k):
        p = d2 / d2.sum() if d2.sum() > 0 else np.full(n, 1 / n)
        c = x[rng.choice(n, p=p)]
        centers.append(c)
        d2 = np.minimum(d2, ((x - c) ** 2).sum(1))
    cen = np.array(centers)
    labels = np.full(n, -1)
    for _ in range(iters):
        dist = sq[:, None] - 2 * x @ cen.T + (cen**2).sum(1)[None, :]
        new = dist.argmin(1)
        if (new == labels).all():
            break
        labels = new
        for j in range(k):
            members = x[labels == j]
            if len(members):
                cen[j] = members.mean(0)
    return np.unique(labels, return_inverse=True)[1]


def tstat(s: np.ndarray) -> float:
    sd = s.std()
    return float(s.mean() / sd) if sd > 0 else -math.inf


def onc_base(corr: np.ndarray, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """ONC's base stage: k-means on x = sqrt((1 - rho) / 2), the silhouette from Euclidean
    distances between rows of x (the paper's D-tilde), best mean/std of silhouettes over
    k = 2..k_max and N_INIT initialisations."""
    x = np.sqrt(np.clip((1 - corr) / 2, 0, None))
    sq = (x**2).sum(1)
    dist = np.sqrt(np.clip(sq[:, None] + sq[None, :] - 2 * x @ x.T, 0, None))
    best: tuple[float, np.ndarray, np.ndarray] | None = None
    for _ in range(N_INIT):
        for k in range(2, min(K_MAX, len(corr) - 1) + 1):
            lab = kmeans(x, k, rng)
            if len(np.unique(lab)) < 2:
                continue
            s = silhouette(dist, lab)
            q = tstat(s)
            if best is None or q > best[0]:
                best = (q, lab, s)
    if best is None:
        return np.zeros(len(corr), dtype=int), np.zeros(len(corr))
    return best[1], best[2]


def _quality(s: np.ndarray, lab: np.ndarray) -> dict[int, float]:
    return {int(k): tstat(s[lab == k]) for k in np.unique(lab)}


def onc(corr: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """ONC's top stage (section 8.1): re-cluster the clusters of below-average quality when
    there are more than two of them; keep the result only if the average quality improves."""
    lab, s = onc_base(corr, rng)
    q = _quality(s, lab)
    mean_q = float(np.mean(list(q.values())))
    redo = [k for k, v in q.items() if v < mean_q]
    if len(redo) <= 2:
        return lab
    idx = np.where(np.isin(lab, redo))[0]
    sub = onc(corr[np.ix_(idx, idx)], rng)
    new = lab.copy()
    keep = sorted(set(np.unique(lab)) - set(redo))
    remap = {k: i for i, k in enumerate(keep)}
    for i in range(len(new)):
        if lab[i] in remap:
            new[i] = remap[lab[i]]
    new[idx] = sub + len(keep)
    x = np.sqrt(np.clip((1 - corr) / 2, 0, None))
    sq = (x**2).sum(1)
    dist = np.sqrt(np.clip(sq[:, None] + sq[None, :] - 2 * x @ x.T, 0, None))
    s_new = silhouette(dist, new)
    old_redo_q = float(np.mean([q[k] for k in redo]))
    new_q = float(np.mean(list(_quality(s_new, new).values())))
    return new if new_q > old_redo_q else lab


def cluster_sharpes(rets: np.ndarray, lab: np.ndarray, how: str = "ivp") -> list[float]:
    """Annualised Sharpe of each cluster's portfolio. `minvar`: the minimum-variance weights of
    section 8.2; with two near-identical series in a cluster they go long one and short the
    other, and the portfolio's Sharpe means nothing (register-3 found 4.87). `ivp` (used):
    inverse-variance weights, long only."""
    out = []
    for k in np.unique(lab):
        r = rets[:, lab == k]
        if r.shape[1] == 1:
            agg = r[:, 0]
        elif how == "ivp":
            w = 1 / r.var(0)
            agg = r @ (w / w.sum())
        else:
            cov = np.cov(r, rowvar=False)
            w = np.linalg.pinv(cov) @ np.ones(r.shape[1])
            w = w / w.sum() if abs(w.sum()) > 1e-12 else np.full(r.shape[1], 1 / r.shape[1])
            agg = r @ w
        out.append(
            float(agg.mean() / agg.std() * math.sqrt(WEEKS_PER_YEAR)) if agg.std() > 0 else 0.0
        )
    return out


def effective_trials(series: list[Series], a: date, b: date) -> dict[str, Any]:
    idx, rets = window_matrix(series, a, b)
    m = len(idx)
    if m < 3:
        return {"series": m}
    corr = np.corrcoef(rets, rowvar=False)
    off = corr[~np.eye(m, dtype=bool)]
    eig = np.clip(np.linalg.eigvalsh(corr), 0, None)
    lab = onc(corr, np.random.default_rng(SEED))
    k = int(len(np.unique(lab)))
    srs = cluster_sharpes(rets, lab)
    srs_minvar = cluster_sharpes(rets, lab, "minvar")
    sizes = sorted((int((lab == j).sum()) for j in np.unique(lab)), reverse=True)
    return {
        "from": a.isoformat(),
        "to": b.isoformat(),
        "weeks": int(rets.shape[0]),
        "series": m,
        "rho_mean": round(float(off.mean()), 4),
        "rho_median": round(float(np.median(off)), 4),
        "participation_ratio": round(float(eig.sum() ** 2 / (eig**2).sum()), 2),
        "onc_k": k,
        "onc_k_at_cap": k >= min(K_MAX, m - 1),
        "onc_sizes": sizes,
        "cluster_sharpe_mean": round(float(np.mean(srs)), 4),
        "cluster_sharpe_var": round(float(np.var(srs, ddof=1)), 4) if k > 1 else None,
        "cluster_sharpes": [round(x, 4) for x in srs],
        "cluster_sharpes_minvar": [round(x, 4) for x in srs_minvar],
    }


def onc_check() -> list[list[int]]:
    """ONC on planted block structures (as in section 9 of the paper): [planted K, found K]."""
    rng = np.random.default_rng(1)
    out = []
    for k, n, t in ((6, 60, 700), (10, 200, 700), (20, 300, 700)):
        f, mkt = rng.normal(size=(t, k)), rng.normal(size=t)
        cols = [
            0.5 * mkt + f[:, j] + 0.6 * rng.normal(size=t) for j in range(k) for _ in range(n // k)
        ]
        corr = np.corrcoef(np.column_stack(cols), rowvar=False)
        out.append([k, int(len(np.unique(onc(corr, np.random.default_rng(SEED)))))])
    return out


def one_per_family(series: list[Series], a: date, b: date) -> dict[str, Any]:
    """Sensitivity (not on the card): the first series of each idea only."""
    first: dict[str, Series] = {}
    for s in series:
        first.setdefault(s.idea, s)
    return effective_trials(list(first.values()), a, b)


def pick_key(s: Series) -> str:
    return hashlib.sha256(f"{s.idea}/{s.variant}/{s.start}".encode()).hexdigest()


def capped(series: list[Series], a: date, b: date, cap: int) -> list[Series]:
    """The series covering the window, at most `cap` per family (card register-3)."""
    idx, _ = window_matrix(series, a, b)
    by_family: dict[str, list[Series]] = {}
    for s in sorted((series[i] for i in idx), key=pick_key):
        by_family.setdefault(s.idea, []).append(s)
    return [s for fam in sorted(by_family) for s in by_family[fam][:cap]]


def family_sizes(series: list[Series]) -> list[int]:
    count: dict[str, int] = {}
    for s in series:
        count[s.idea] = count.get(s.idea, 0) + 1
    return sorted(count.values(), reverse=True)


def register_weighted_rho(
    series: list[Series], a: date, b: date, register_share: dict[str, int]
) -> dict[str, Any]:
    """Sensitivity (register-3 card): the uncapped sample's average correlation with each pair
    weighted so every family counts by its share of the register's selectable rows."""
    idx, rets = window_matrix(series, a, b)
    fams = [series[i].idea for i in idx]
    n_f: dict[str, int] = {}
    for f in fams:
        n_f[f] = n_f.get(f, 0) + 1
    w = np.array([register_share.get(f, 0) / n_f[f] for f in fams], dtype=float)
    corr = np.corrcoef(rets, rowvar=False)
    pw = np.outer(w, w)
    np.fill_diagonal(pw, 0.0)
    return {
        "series": len(idx),
        "families": len(n_f),
        "rho_mean": round(float((pw * corr).sum() / pw.sum()), 4),
    }


def estimate() -> None:
    rows = register_rows()
    by_id = {r["id"]: r for r in rows}
    harness, curves_, lives, local = sources()
    if unstored := len(to_store(local, rows)):
        print(
            f"estimate: {unstored} local series for the register are not in {returnstore.STORE} "
            "(run `export` and commit the store, or a clean checkout gets other numbers)",
            file=sys.stderr,
        )
    matched = match(harness, rows)  # re-simulated first: they win over a saved curve
    from_curves = match(curves_, rows)
    for ident, s in from_curves.items():
        matched.setdefault(ident, s)
    shapes = logged()  # the row's own run, logged with it: wins over a rebuilt series
    lines = []
    for ident in sorted(set(matched) | set(shapes)):
        r = by_id[ident]
        if ident in shapes:
            x = shapes[ident]
            w, sr, sk, ek, source = x.weeks, x.sharpe_weekly, x.skew, x.excess_kurtosis, "logged"
        else:
            w, sr, sk, ek = shape(matched[ident].rets)
            source = matched[ident].source
        lines.append({
            "id": ident, "idea": r["idea"], "variant": r["variant"], "kind": r["kind"],
            "weeks": w, "skew": round(sk, 4), "excess_kurtosis": round(ek, 4),
            "sharpe_weekly": round(sr, 4), "sharpe_logged": r["sharpe"], "source": source,
        })  # fmt: skip
    for s in lives:
        w, sr, sk, ek = shape(s.rets)
        lines.append({
            "id": f"live:{s.variant}", "idea": "live", "variant": s.variant, "kind": "live",
            "weeks": w, "skew": round(sk, 4), "excess_kurtosis": round(ek, 4),
            "sharpe_weekly": round(sr, 4), "sharpe_logged": None, "source": s.source,
        })  # fmt: skip
    MOMENTS.write_text(
        "".join(json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n" for x in lines)
    )
    # The sample for correlations: one series per distinct selectable try (+ the live ones).
    sel_ids = [i for i in matched if by_id[i]["kind"] in SELECTABLE]
    uniq: dict[tuple[float, ...], Series] = {}
    for i in sorted(sel_ids):
        uniq.setdefault(tuple(np.round(matched[i].rets, 12)), matched[i])
    for s in lives:
        uniq.setdefault(tuple(np.round(s.rets, 12)), s)
    sample = list(uniq.values())
    sel_lines = [x for x in lines if x["kind"] in (*SELECTABLE, "live")]
    sk = np.array([x["skew"] for x in sel_lines])
    ek = np.array([x["excess_kurtosis"] for x in sel_lines])
    out = {
        "generated_by": "uv run --with numpy python research/register2.py all",
        "card": "research/register-2.md",
        "method": "Lopez de Prado and Lewis (2019), ONC; Bailey and Lopez de Prado (2014), A.3",
        "harness_ref": HARNESS_REF,
        "seed": SEED,
        "n_init": N_INIT,
        "k_max": K_MAX,
        "rows_backfilled": sum(1 for x in lines if x["kind"] != "live"),
        "rows_backfilled_selectable": sum(1 for x in lines if x["kind"] in SELECTABLE),
        "rows_backfilled_by_source": {
            src: sum(1 for x in lines if x["source"].split("@")[0] == src)
            for src in ("logged", "harness", "curve", "live")
        },
        "harness_series": len(harness),
        "harness_series_matched": len({id(matched[i]) for i in matched if matched[i] in harness}),
        "sample_series": len(sample),
        "shape": {
            "series": len(sel_lines),
            "skew_median": round(float(np.median(sk)), 3),
            "skew_p10": round(float(np.percentile(sk, 10)), 3),
            "excess_kurtosis_median": round(float(np.median(ek)), 3),
            "excess_kurtosis_p90": round(float(np.percentile(ek, 90)), 3),
        },
        "windows": {name: effective_trials(sample, a, b) for name, (a, b) in WINDOWS.items()},
        "main_window": MAIN_WINDOW,
        "onc_check_planted_found": onc_check(),
        "sensitivity_one_per_family": one_per_family(sample, *WINDOWS[MAIN_WINDOW]),
    }
    a0, b0 = WINDOWS[MAIN_WINDOW]
    main = [sample[i] for i in window_matrix(sample, a0, b0)[0]]
    share: dict[str, int] = {}
    for r in rows:
        if r["kind"] in SELECTABLE and r["period"] == "train":
            share[r["idea"]] = share.get(r["idea"], 0) + 1
    share["live"] = len(lives)
    out["family_cap"] = {
        "card": "research/register-3.md",
        "cap": CAP,
        "rule": "at most CAP series per family (Idea), first by sha256(idea/variant/start)",
        "families": len(family_sizes(main)),
        "largest_families_uncapped": family_sizes(main)[:5],
        "windows": {
            name: effective_trials(capped(sample, a, b, CAP), a, b)
            for name, (a, b) in WINDOWS.items()
        },
        "sensitivity_caps": {
            str(c): effective_trials(capped(sample, a0, b0, c), a0, b0) for c in CAP_SENSITIVITY
        },
        "sensitivity_register_weighted": register_weighted_rho(sample, a0, b0, share),
    }
    TRIALS.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    p.add_argument(
        "step", choices=("all", "tree", "baselines", "live", "curves", "export", "estimate")
    )
    p.add_argument("--tree", type=Path, help="extracted tree (for `baselines`)")
    a = p.parse_args(argv)
    if a.step == "tree":
        print(tree())
    elif a.step == "baselines":
        baselines(a.tree or tree())
    elif a.step == "live":
        live()
    elif a.step == "curves":
        curves()
    elif a.step == "export":
        export()
    elif a.step == "estimate":
        estimate()
    else:
        t = tree()
        me = [sys.executable, str(Path(__file__).resolve())]
        subprocess.run([*me, "baselines", "--tree", str(t)], check=True)
        subprocess.run([*me, "live"], check=True)
        curves()
        export()
        estimate()


if __name__ == "__main__":
    main()
