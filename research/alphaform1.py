"""alpha-form-1: the stored record re-scored in alpha form (card: research/alpha-form-1.md).

    uv run python research/alphaform1.py > research/results/alpha-form-1.md

For every selectable stored series (variant or baseline, train): regress its weekly returns on
its universe's `tsmom12` (residual IR, Newey-West z, block-bootstrap check) and find the best
long-only mix of the two (Sharpe gain over `tsmom12` alone). Reads only the committed weekly
returns store, the committed register and this branch's `research/tries.md`. No backtest, no
price bar, nothing after 2025-11-10. Deterministic (fixed seed). Prints markdown.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from statistics import NormalDist
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "research"))
import register2 as r2  # noqa: E402

from grimstrade import register as greg  # noqa: E402
from grimstrade import returnstore as rs  # noqa: E402

WPY = 52.18
LAST = date(2025, 11, 10)  # the held-out year starts here; nothing after it is read
MIN_WEEKS = 261  # 5 years of common weeks
BAR = 4.69  # BAR.md: N_eff 486
ONC = 3.29  # BAR.md: the ONC end of the measured range
BOOT_FROM = 3.0  # bootstrap check for every series at NW z >= this, and the top 20
BLOCK = 52
DRAWS = 2000
SEED = 20261124
GRID = np.linspace(0.0, 1.0, 201)
PRIMARY = ("baselines", "tsmom12")


# --- statistics (tested in tests/test_alphaform1.py) ---


def nw_lag(n: int) -> int:
    """Newey-West (1994) rule of thumb, Bartlett kernel."""
    return int(math.floor(4 * (n / 100) ** (2 / 9)))


def alpha(r: np.ndarray, t: np.ndarray) -> dict[str, float]:
    """OLS r = a + b t + e: weekly alpha, beta, annual residual IR, Newey-West SE and z of a."""
    n = len(r)
    x = np.column_stack([np.ones(n), t])
    xtx_inv = np.linalg.inv(x.T @ x)
    coef = xtx_inv @ (x.T @ r)
    e = r - x @ coef
    sd_e = float(e.std(ddof=2))
    lag = nw_lag(n)
    u = x * e[:, None]
    s = u.T @ u
    for j in range(1, lag + 1):
        g = u[j:].T @ u[:-j]
        s += (1 - j / (lag + 1)) * (g + g.T)
    cov = xtx_inv @ s @ xtx_inv
    se = math.sqrt(max(float(cov[0, 0]), 0.0))
    a = float(coef[0])
    ir = a / sd_e * math.sqrt(WPY) if sd_e > 0 else 0.0
    return {
        "a": a,
        "b": float(coef[1]),
        "ir": ir,
        "se_nw": se,
        "z_nw": a / se if se > 0 else 0.0,
        "lag": lag,
    }


def _mix_sharpe(mr: Any, mt: Any, vr: Any, vt: Any, c: Any, w: Any) -> Any:
    m = w * mr + (1 - w) * mt
    v = w**2 * vr + (1 - w) ** 2 * vt + 2 * w * (1 - w) * c
    return np.where(v > 0, m / np.sqrt(np.maximum(v, 1e-300)), -np.inf)


def tangency_w(mr: float, mt: float, vr: float, vt: float, c: float) -> float | None:
    """Weight on r of the two-asset max-Sharpe portfolio (fully invested), None if undefined."""
    det = vr * vt - c * c
    if det <= 0:
        return None
    vr_, vt_ = (vt * mr - c * mt) / det, (vr * mt - c * mr) / det
    tot = vr_ + vt_
    if tot <= 0:
        return None
    return vr_ / tot


def best_mix(r: np.ndarray, t: np.ndarray) -> dict[str, float]:
    """Long-only, fully invested mix w r + (1 - w) t with the largest in-sample Sharpe."""
    mr, mt = float(r.mean()), float(t.mean())
    vr, vt = float(r.var(ddof=1)), float(t.var(ddof=1))
    c = float(np.cov(r, t)[0, 1])
    cand = list(GRID)
    w0 = tangency_w(mr, mt, vr, vt, c)
    if w0 is not None and 0 <= w0 <= 1:
        cand.append(w0)
    ws = np.array(cand)
    sr = _mix_sharpe(mr, mt, vr, vt, c, ws)
    i = int(np.argmax(sr))
    sr_t = mt / math.sqrt(vt) if vt > 0 else 0.0
    return {
        "w": float(ws[i]),
        "sr_mix": float(sr[i]) * math.sqrt(WPY),
        "sr_t": sr_t * math.sqrt(WPY),
        "gain": (float(sr[i]) - sr_t) * math.sqrt(WPY),
    }


def boot(r: np.ndarray, t: np.ndarray, rng: np.random.Generator) -> dict[str, float]:
    """Circular block bootstrap (52-week blocks): SE of the weekly alpha and of the mix gain
    (w re-optimised on the grid in every draw)."""
    n = len(r)
    nb = -(-n // BLOCK)
    out_a, out_g = [], []
    for chunk in range(0, DRAWS, 250):
        k = min(250, DRAWS - chunk)
        starts = rng.integers(0, n, size=(k, nb))
        idx = (starts[:, :, None] + np.arange(BLOCK)[None, None, :]).reshape(k, -1)[:, :n] % n
        rs_, ts_ = r[idx], t[idx]
        mr, mt = rs_.mean(1), ts_.mean(1)
        vr, vt = rs_.var(1, ddof=1), ts_.var(1, ddof=1)
        c = ((rs_ - mr[:, None]) * (ts_ - mt[:, None])).sum(1) / (n - 1)
        b = c / vt
        out_a.append(mr - b * mt)
        sr = _mix_sharpe(mr[:, None], mt[:, None], vr[:, None], vt[:, None], c[:, None], GRID)
        out_g.append((sr.max(1) - mt / np.sqrt(vt)) * math.sqrt(WPY))
    a, g = np.concatenate(out_a), np.concatenate(out_g)
    return {"se_a": float(a.std(ddof=1)), "se_gain": float(g.std(ddof=1))}


def diff_z(r: np.ndarray, t: np.ndarray) -> float:
    """The bar's difference form, for contrast: (SR_r - SR_t) / SE (Jobson-Korkie, Memmel)."""
    sa = r.mean() / r.std(ddof=1) * math.sqrt(WPY)
    sb = t.mean() / t.std(ddof=1) * math.sqrt(WPY)
    rho = float(np.corrcoef(r, t)[0, 1])
    yrs = len(r) / WPY
    var = (2 - 2 * rho + (sa**2 + sb**2 - 2 * rho**2 * sa * sb) / (2 * WPY)) / yrs
    return float((sa - sb) / math.sqrt(var)) if var > 0 else 0.0


# --- data ---


@dataclass
class S:
    source: str
    idea: str
    variant: str
    start: str
    first: int  # ordinal of the first Friday
    r: np.ndarray
    rows: list[str] = field(default_factory=list)  # selectable register ids it fits

    @property
    def key(self) -> tuple[str, str]:
        return (self.idea, self.variant)

    @property
    def name(self) -> str:
        return f"{self.idea}/{self.variant}"


def align(a: S, b: S) -> tuple[np.ndarray, np.ndarray]:
    lo = max(a.first, b.first)
    hi = min(a.first + 7 * (len(a.r) - 1), b.first + 7 * (len(b.r) - 1))
    if hi < lo:
        return np.empty(0), np.empty(0)
    ia, ib = (lo - a.first) // 7, (lo - b.first) // 7
    n = (hi - lo) // 7 + 1
    x, y = a.r[ia : ia + n], b.r[ib : ib + n]
    ok = np.isfinite(x) & np.isfinite(y)
    return x[ok], y[ok]


def register_rows() -> tuple[list[dict[str, Any]], int]:
    """The committed register plus this branch's `research/tries.md` rows not in it."""
    rows = r2.register_rows()
    known = {r["id"] for r in rows}
    lines = [
        ln.strip()
        for ln in (ROOT / "research" / "tries.md").read_text().splitlines()
        if ln.startswith("| 20")
    ]
    extra = [json.loads(t.to_json()) for t in greg.census({"here": Counter(lines)})]
    extra = [r for r in extra if r["id"] not in known]
    return rows + extra, len(extra)


def load() -> tuple[list[S], list[S], dict[str, Any]]:
    """(all stored series, distinct selectable series, counts)."""
    store = list(rs.read(r2.STORE))
    allser, r2ser = [], []
    for row in store:
        first = date.fromisoformat(row.first_friday).toordinal()
        rets = np.array(row.rets, dtype=float)
        n_ok = max(0, min(len(rets), (LAST.toordinal() - first) // 7 + 1))
        allser.append(S(row.source, row.idea, row.variant, row.start, first, rets[:n_ok]))
        r2ser.append(r2.from_row(row))
    rows, n_extra = register_rows()
    by_id = {r["id"]: r for r in rows}
    pos = {id(x): i for i, x in enumerate(r2ser)}
    sel_ids = 0
    for ident, s2 in r2.match(r2ser, rows).items():
        r = by_id[ident]
        if r["kind"] in r2.SELECTABLE and r["period"] == "train":
            allser[pos[id(s2)]].rows.append(ident)
            sel_ids += 1
    # distinct series: identical weekly returns scored once (harness copy first)
    order = sorted(
        (s for s in allser if s.rows),
        key=lambda s: (not s.source.startswith("harness"), s.idea, s.variant, s.start),
    )
    seen: set[tuple[int, bytes]] = set()
    distinct = []
    for s in order:
        k = (s.first, np.round(s.r, 6).tobytes())
        if k not in seen:
            seen.add(k)
            distinct.append(s)
    distinct.sort(key=lambda s: (s.idea, s.variant, s.start))
    counts = {
        "store": len(store),
        "register": len(rows),
        "register_extra": n_extra,
        "selectable_rows_matched": sel_ids,
        "distinct": len(distinct),
    }
    return allser, distinct, counts


def comparator(s: S, by_key: dict[tuple[str, str], list[S]], primary: S) -> tuple[S, str]:
    cands: list[S] = []
    if "@" in s.variant:
        u = s.variant.split("@", 1)[1]
        for key in (("baselines", f"tsmom12@{u}"), (s.idea, f"tsmom12@{u}"), (s.idea, f"TS@{u}")):
            if key in by_key:
                cands = by_key[key]
                break
    if not cands:
        return primary, "six-asset"

    def overlap(c: S) -> tuple[int, bool]:
        return (len(align(s, c)[0]), c.source.startswith("harness"))

    best = max(cands, key=overlap)
    return best, "same universe"


# --- the run ---


@dataclass
class Score:
    s: S
    comp: S
    how: str
    years: float
    rho: float
    al: dict[str, float]
    mix: dict[str, float]
    zd: float
    bs: dict[str, float] | None = None

    @property
    def z(self) -> float:
        """Decision z: alpha over the larger of the NW and bootstrap SEs (NW alone if not
        bootstrapped, which only happens below BOOT_FROM)."""
        se = self.al["se_nw"]
        if self.bs is not None:
            se = max(se, self.bs["se_a"])
        return self.al["a"] / se if se > 0 else 0.0


def score_all(
    distinct: list[S], comp_of: Any, rng: np.random.Generator
) -> tuple[list[Score], Counter[str], list[str]]:
    skipped: Counter[str] = Counter()
    near: list[str] = []
    out = []
    for s in distinct:
        comp, how = comp_of(s)
        if comp.key == s.key:
            skipped["same key as the comparator"] += 1
            continue
        x, y = align(s, comp)
        if len(x) < MIN_WEEKS:
            skipped["overlap under 5 years"] += 1
            continue
        if x.std() == 0 or y.std() == 0:
            skipped["constant returns"] += 1
            continue
        rho = float(np.corrcoef(x, y)[0, 1])
        if rho > 0.999:
            skipped["weekly correlation above 0.999 with it"] += 1
            al = alpha(x, y)
            near.append(f"`{s.name}` (IR {al['ir']:+.2f}, NW z {al['z_nw']:.1f})")
            continue
        sc = Score(s, comp, how, len(x) / WPY, rho, alpha(x, y), best_mix(x, y), diff_z(x, y))
        out.append(sc)
    out.sort(key=lambda sc: -sc.al["z_nw"])
    for i, sc in enumerate(out):
        if i < 20 or sc.al["z_nw"] >= BOOT_FROM:
            x, y = align(sc.s, sc.comp)
            sc.bs = boot(x, y, rng)
    out.sort(key=lambda sc: (-sc.z, sc.s.name))
    return out, skipped, near


def f(v: float, d: int = 2, sign: bool = False) -> str:
    if not math.isfinite(v):
        return "-"
    return f"{v:+.{d}f}" if sign else f"{v:.{d}f}"


def table(scores: list[Score]) -> list[str]:
    out = [
        "| # | Series | Family | Comparator | Years | rho | beta | IR | z NW | z boot | **z** "
        "| w* | Mix gain (boot SE) | z diff form |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|",
    ]
    for i, sc in enumerate(scores, 1):
        zb = sc.al["a"] / sc.bs["se_a"] if sc.bs and sc.bs["se_a"] > 0 else float("nan")
        gse = f"({f(sc.bs['se_gain'], 3)})" if sc.bs else ""
        comp = sc.comp.variant if sc.how == "same universe" else "`tsmom12` (six assets)"
        out.append(
            f"| {i} | `{sc.s.variant}` | {sc.s.idea} | {comp} | {sc.years:.1f} | {sc.rho:.2f} "
            f"| {sc.al['b']:.2f} | {f(sc.al['ir'], 2, True)} | {f(sc.al['z_nw'], 2)} | {f(zb, 2)} "
            f"| **{f(sc.z, 2)}** | {sc.mix['w']:.2f} | {f(sc.mix['gain'], 3, True)} {gse} "
            f"| {f(sc.zd, 2)} |"
        )
    return out


def q(v: list[float], p: float) -> float:
    return float(np.quantile(np.array(v), p)) if v else float("nan")


def report(scores: list[Score], skipped: Counter[str]) -> list[str]:
    zs = [sc.z for sc in scores]
    n = len(scores)
    nd = NormalDist()

    def tail(z: float) -> float:
        return 1 - nd.cdf(z)

    lines = [
        f"Scored: **{n}** series ({', '.join(f'{v} {k}' for k, v in sorted(skipped.items()))} "
        "not scored).",
        "",
        f"- Passing z >= {BAR} (the bar): **{sum(z >= BAR for z in zs)}**.",
        f"- Passing z >= {ONC} (ONC end of the range): **{sum(z >= ONC for z in zs)}**"
        f" (expected by luck if all {n} were independent nulls: {n * tail(ONC):.2f}).",
        f"- z >= 2.0: {sum(z >= 2.0 for z in zs)} (luck: {n * tail(2.0):.1f}); z >= 1.645: "
        f"{sum(z >= 1.645 for z in zs)} (luck: {n * tail(1.645):.1f}); z <= -1.645: "
        f"{sum(z <= -1.645 for z in zs)}.",
        f"- z quantiles p10 / p50 / p90 / max: {f(q(zs, 0.1))} / {f(q(zs, 0.5))} / "
        f"{f(q(zs, 0.9))} / {f(max(zs) if zs else float('nan'))}.",
        f"- IR median {f(q([sc.al['ir'] for sc in scores], 0.5), 2, True)}, max "
        f"{f(max(sc.al['ir'] for sc in scores), 2, True)}; mix gain median "
        f"{f(q([sc.mix['gain'] for sc in scores], 0.5), 3, True)}, p90 "
        f"{f(q([sc.mix['gain'] for sc in scores], 0.9), 3, True)}, max "
        f"{f(max(sc.mix['gain'] for sc in scores), 3, True)}.",
        f"- Difference form for the same pairs (contrast): z_d >= {ONC}: "
        f"{sum(sc.zd >= ONC for sc in scores)}, >= {BAR}: {sum(sc.zd >= BAR for sc in scores)}; "
        f"max {f(max(sc.zd for sc in scores))}.",
    ]
    return lines


def families(scores: list[Score]) -> list[str]:
    by: dict[str, list[Score]] = defaultdict(list)
    for sc in scores:
        by[sc.s.idea].append(sc)
    rows = sorted(by.items(), key=lambda kv: -kv[1][0].z)
    out = [
        "| Family | Series scored | Best series | Best z | Its IR | Its mix gain | z >= 3.29 "
        "| z >= 2 | Median z |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for fam, v in rows[:20]:
        b = v[0]
        out.append(
            f"| {fam} | {len(v)} | `{b.s.variant}` | {f(b.z)} | {f(b.al['ir'], 2, True)} "
            f"| {f(b.mix['gain'], 3, True)} | {sum(x.z >= ONC for x in v)} "
            f"| {sum(x.z >= 2 for x in v)} | {f(q([x.z for x in v], 0.5))} |"
        )
    top = Counter(sc.s.idea for sc in scores[:20])
    top50 = Counter(sc.s.idea for sc in scores[:50])
    out += [
        "",
        f"Families in the top 20: {', '.join(f'{k} {v}' for k, v in top.most_common())}.",
        f"Families in the top 50: {', '.join(f'{k} {v}' for k, v in top50.most_common())}.",
    ]
    return out


def capped(scores: list[Score], cap: int = 10) -> list[Score]:
    seen: Counter[str] = Counter()
    out = []
    for sc in scores:
        if seen[sc.s.idea] < cap:
            out.append(sc)
            seen[sc.s.idea] += 1
    return out


def main() -> None:
    allser, distinct, counts = load()
    by_key: dict[tuple[str, str], list[S]] = defaultdict(list)
    for s in allser:
        by_key[s.key].append(s)
    primary = sorted(by_key[PRIMARY], key=lambda s: not s.source.startswith("harness"))[0]
    rng = np.random.default_rng(SEED)

    scores, skipped, near = score_all(distinct, lambda s: comparator(s, by_key, primary), rng)
    how = Counter(sc.how for sc in scores)

    p = print
    p("# alpha-form-1: results (generated by `research/alphaform1.py`; do not edit by hand)")
    p()
    p("Card: [`../alpha-form-1.md`](../alpha-form-1.md). Inputs: the committed store and register;")
    p(f"train weeks only (cut before {LAST}). Bootstrap: {BLOCK}-week circular blocks, {DRAWS} ")
    p(f"draws, seed {SEED}. Decision z = alpha / max(Newey-West SE, bootstrap SE).")
    p()
    p("## Inputs")
    p()
    p(f"- Store rows: {counts['store']}. Register rows: {counts['register']} (committed ")
    p(f"  `tries.jsonl` + {counts['register_extra']} rows of `research/tries.md` not in it).")
    p("- Selectable register rows (variant/baseline, train) matched to a stored series: ")
    n_sel, n_dist = counts["selectable_rows_matched"], counts["distinct"]
    p(f"  {n_sel}; distinct series among them: **{n_dist}**.")
    p(f"- Primary comparator: `{primary.name}` ({primary.source}, from {primary.start}, ")
    p(f"  {len(primary.r)} weeks).")
    p(f"- Comparator met: {', '.join(f'{v} {k}' for k, v in sorted(how.items()))}.")
    p()
    p("## Headline (same-universe `tsmom12`)")
    p()
    for ln in report(scores, skipped):
        p(ln)
    p()
    p(f"Not scored as near-copies of their comparator (rho > 0.999): {', '.join(near)}.")
    p()
    p("## Top 20 by decision z")
    p()
    p("IR: annual residual information ratio. w*: weight on the rule in the best long-only mix.")
    p("Mix gain: annual Sharpe of that mix minus `tsmom12`'s (in sample, >= 0 by construction).")
    p("z diff form: the bar's own Sharpe-difference z for the same pair (Jobson-Korkie).")
    p()
    for ln in table(scores[:20]):
        p(ln)
    cap = capped(scores)
    if [sc.s.name for sc in cap[:20]] != [sc.s.name for sc in scores[:20]]:
        p()
        p("### Top 20 with at most 10 series per family (BAR's cap)")
        p()
        for ln in table(cap[:20]):
            p(ln)
    else:
        p()
        p("At most 10 per family (BAR's cap) leaves the top 20 unchanged.")
    p()
    p("## Families (best series each, top 20 families by best z)")
    p()
    for ln in families(scores):
        p(ln)

    p()
    p("## Sensitivity: every series against the primary six-asset `tsmom12`")
    p()
    rng2 = np.random.default_rng(SEED + 1)
    s6, sk6, _ = score_all(distinct, lambda s: (primary, "six-asset"), rng2)
    for ln in report(s6, sk6):
        p(ln)
    p()
    p("Top 10:")
    p()
    for ln in table(s6[:10]):
        p(ln)


if __name__ == "__main__":
    main()
