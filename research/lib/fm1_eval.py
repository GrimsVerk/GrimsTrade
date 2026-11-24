# ruff: noqa: E501
"""Judge the fm-1 zero-shot forecasts (card: research/fm-1.md). numpy only, no GPU.

    uv run python -I research/lib/fm1_eval.py <model ...>          # print, dry
    uv run python -I research/lib/fm1_eval.py --log <model ...>    # + gate runs and tries rows

Reads research/data/fm/<model>.npz from `fm1_forecast.py`. Weekly: IC with `rl3_plant.week_z`,
chance level and walk-forward gain over the trend inputs as `info1_ic.py`, then the rl-3 gate
(residual tilt on `tsmom12`, gym replay, 2000-2025). Daily and hourly: IC only, before and
after each model's release. Writes research/data/fm/eval-<model>.json.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_hf  # noqa: E402
import harness  # noqa: E402
import info1_ic as ic1  # noqa: E402
import ml  # noqa: E402
import rl2_data  # noqa: E402
import rl3_plant  # noqa: E402
from harness import TRAIN_END  # noqa: E402

IDEA = "fm-1"
OOS_START = date(2000, 1, 7)
RELEASE = {"bolt-small": date(2024, 12, 1), "bolt-base": date(2024, 12, 1),
           "chronos2": date(2025, 10, 20)}  # fmt: skip
SD_WEEKS = 104
DIR = Path(__file__).resolve().parents[1] / "data" / "fm"
corr = ic1.corr


def partial(x: np.ndarray, y: np.ndarray, ctrl: np.ndarray) -> float:
    """Correlation of x and y after removing (OLS, in sample) the control columns from both."""
    a = np.column_stack([np.ones(len(x)), ctrl])
    rx = x - a @ np.linalg.lstsq(a, x, rcond=None)[0]
    ry = y - a @ np.linalg.lstsq(a, y, rcond=None)[0]
    return corr(rx, ry)


def split_ic(x: np.ndarray, y: np.ndarray, when: np.ndarray, rel: date, eff: float = 1.0) -> dict:
    """IC full / before / after release, with n and a standard error 1/sqrt(n / eff)."""
    out = {}
    for name, m in (("all", np.ones(len(x), bool)), ("pre", when < rel), ("post", when >= rel)):
        n = int(m.sum())
        out[name] = {"ic": corr(x[m], y[m]) if n > 2 else math.nan, "n": n,
                     "se": 1 / math.sqrt(max(n / eff, 1))}  # fmt: skip
    return out


def weekly(model: str, fc: np.ndarray) -> dict:
    t = rl2_data.load()["six"].t
    z = rl3_plant.week_z(t)
    vol = np.exp(t.X[:, :, ml.LOG_VOL])
    fz = fc / (vol * math.sqrt(7 / 365))
    F, n = z.shape
    i0 = t.index(OOS_START)
    m = np.isfinite(z) & np.isfinite(fz)
    m[:i0] = False
    days = np.repeat(np.array(t.fridays, dtype=object)[:, None], n, 1)
    res = split_ic(fz[m], z[m], days[m], RELEASE[model], eff=n / 2)
    res["rank_ic"] = corr(ic1.rank(fz[m]), ic1.rank(z[m]))
    res["per_asset"] = {
        s: corr(fz[:, j][m[:, j]], z[:, j][m[:, j]]) for j, s in enumerate(t.book.syms)
    }
    # chance level: circularly shifted forecast series (info1_ic.py's null)
    rng = np.random.default_rng(0)
    null = []
    for s in rng.integers(ic1.MIN_SHIFT, F - ic1.MIN_SHIFT, ic1.N_SHIFT):
        xs = np.roll(fz, s, axis=0)
        ms = m & np.isfinite(xs)
        null.append(abs(corr(xs[ms], z[ms])))
    res["chance"] = float(np.percentile(null, 95))
    # walk-forward gain over the 7 trend inputs
    years = np.repeat(np.array([d.year for d in t.fridays])[:, None], n, 1)
    week = np.repeat(np.arange(F)[:, None], n, 1)
    blocks = []
    for y0 in range(2000, 2026, 2):
        tr = m & (years < y0 - 1)
        te = m & (years >= y0) & (years < y0 + 2)
        if te.sum() and len(np.unique(week[tr])) >= ic1.MIN_TRAIN_WEEKS:
            blocks.append((tr, te))
    trend = [t.X[:, :, k] for k in range(ic1.TREND.start, ic1.TREND.stop)]
    fzz = np.nan_to_num(fz)
    res["wf_fc"] = ic1.walk_forward(blocks, [fzz], z)
    res["wf_trend"] = ic1.walk_forward(blocks, trend, z)
    res["gain"] = ic1.walk_forward(blocks, [*trend, fzz], z) - res["wf_trend"]
    res["overlap"] = max(
        abs(corr(fz[m], t.X[:, :, k][m])) for k in range(ic1.TREND.start, ic1.TREND.stop)
    )
    return res


def gate_scores(fc: np.ndarray) -> np.ndarray:
    """fc / sd of that asset's forecasts over the previous 104 Fridays; 0 before that or if NaN."""
    s = np.zeros(fc.shape)
    for i in range(SD_WEEKS, len(fc)):
        past = fc[i - SD_WEEKS : i]
        for j in range(fc.shape[1]):
            p = past[:, j][np.isfinite(past[:, j])]
            if len(p) >= SD_WEEKS // 2 and p.std() > 0 and np.isfinite(fc[i, j]):
                s[i, j] = fc[i, j] / p.std()
    return s


def gate(model: str, fc: np.ndarray, log: bool) -> dict:
    import rl2_env
    import rl_eval as r1

    r1.IDEA = IDEA
    r1.DRY = not log
    hist = harness.load_history("train")
    base = r1.baselines(hist, OOS_START)
    ts = base["tsmom12"]
    rt = rl2_data.load()["six"]
    t = rt.t
    i0 = t.index(OOS_START)
    bd = rl2_env.base_daily(hist, t.book.syms, OOS_START, TRAIN_END)
    sc = gate_scores(fc)[i0:]
    run = r1.log_run(f"fm-{model}-tilt", "variant",
                     rl2_env.res_decisions(rt, i0, sc[:, None, :], bd, TRAIN_END),
                     hist, OOS_START, TRAIN_END)  # fmt: skip
    w = rl2_env.residual(rt.B[i0:], rt.L[i0:], t.elig[i0:], rt.coin, sc)
    d, p = r1.vs(run, ts)
    return {**r1.describe(run), "diff": d, "p": p, "active": rl2_env.active_share(w, rt.B[i0:]),
            "tsmom12": r1.describe(ts), "since2020": dict(zip(("diff", "p"), r1.vs(run, ts, date(2020, 1, 1)), strict=True))}  # fmt: skip


def ewm_vol(r: np.ndarray, hl: float = 60) -> np.ndarray:
    """Past-only EWMA volatility of a return series (value at i uses r up to i)."""
    a = 1 - 0.5 ** (1 / hl)
    v = np.full(len(r), np.nan)
    s = np.nan
    for i, x in enumerate(r):
        if np.isfinite(x):
            s = x * x if not np.isfinite(s) else (1 - a) * s + a * x * x
        v[i] = math.sqrt(s) if np.isfinite(s) else np.nan
    return v


def daily(model: str, fc: np.ndarray) -> dict:
    t = rl2_data.load()["six"].t
    cl = t.book.closes
    xs, ys, ws, ctrl = [], [], [], []
    for j in range(cl.shape[1]):
        ks = np.flatnonzero(np.isfinite(cl[:, j]))
        lc = np.log(cl[ks, j])
        r = np.diff(lc, prepend=np.nan)
        v = ewm_vol(r)
        nxt = np.append(r[1:], np.nan)
        f = fc[ks, j]
        ok = np.isfinite(f) & np.isfinite(nxt) & (v > 0) & (np.arange(len(ks)) >= 260)
        ok &= np.array([t.book.date(int(k)) <= TRAIN_END for k in ks])
        lag = {h: np.concatenate([np.full(h, np.nan), lc[h:] - lc[:-h]]) for h in (1, 5, 20, 250)}
        ok &= np.isfinite(lag[250])
        xs.append(f[ok] / v[ok])
        ys.append(nxt[ok] / v[ok])
        ws.append(np.array([t.book.date(int(k)) for k in ks[ok]], dtype=object))
        ctrl.append(np.column_stack([lag[h][ok] / (v[ok] * math.sqrt(h)) for h in (1, 5, 20, 250)]))
    x, y, when, c = (np.concatenate(a) for a in (xs, ys, ws, ctrl))
    res = split_ic(x, y, when, RELEASE[model], eff=2.0)
    res["partial_trend"] = partial(x, y, c)
    res["ic_r1d"] = corr(c[:, 0], y)
    return res


def hourly(model: str, z: np.lib.npyio.NpzFile) -> dict:
    out = {}
    rel = RELEASE[model]
    for name in breadth_hf.SERIES:
        if f"{name}_fc" not in z:
            continue
        h = breadth_hf.load(name)
        fc = z[f"{name}_fc"][: len(h.t)]
        lc = h.lc
        for col, hz in ((0, 1), (1, 24)):
            y = np.full(len(lc), np.nan)
            y[:-hz] = lc[hz:] - lc[:-hz]
            r1h = np.diff(lc, prepend=np.nan)
            r24 = np.concatenate([np.full(24, np.nan), lc[24:] - lc[:-24]])
            r168 = np.concatenate([np.full(168, np.nan), lc[168:] - lc[:-168]])
            ok = np.isfinite(fc[:, col]) & np.isfinite(y) & np.isfinite(r168)
            when = np.array(
                [datetime.fromtimestamp(int(s), UTC).date() for s in h.t[ok]], dtype=object
            )
            res = split_ic(fc[ok, col], y[ok], when, rel, eff=float(hz))
            res["ic_r1h"] = corr(r1h[ok], y[ok])
            res["partial_trend"] = partial(
                fc[ok, col], y[ok], np.column_stack([r1h[ok], r24[ok], r168[ok]])
            )
            post = ok & (h.t >= datetime(rel.year, rel.month, rel.day, tzinfo=UTC).timestamp())
            res["partial_trend_post"] = (partial(fc[post, col], y[post], np.column_stack([r1h[post], r24[post], r168[post]]))
                                         if post.sum() > 50 else math.nan)  # fmt: skip
            res["ic_r1h_post"] = corr(r1h[post], y[post]) if post.sum() > 2 else math.nan
            out[f"{name}-{hz}h"] = res
    return out


PERIODS = [("to2009", date(1900, 1, 1), date(2010, 1, 1)), ("2010-19", date(2010, 1, 1), date(2020, 1, 1)),
           ("2020-25", date(2020, 1, 1), date(2026, 1, 1))]  # fmt: skip


def era_ic(t, fz: np.ndarray, z: np.ndarray, rel: date) -> dict:  # type: ignore[no-untyped-def]
    """IC pooled and per asset, by period and after release (vol-scaled forecast vs week_z)."""
    days = np.array(t.fridays, dtype=object)
    m = np.isfinite(z) & np.isfinite(fz)
    out: dict[str, dict] = {}
    cols = [("pooled", slice(None))] + [(s, slice(j, j + 1)) for j, s in enumerate(t.book.syms)]
    for name, sl in cols:
        row = {}
        for p, a, b in [*PERIODS, ("post", rel, date(2026, 1, 1))]:
            w = ((days >= a) & (days < b))[:, None] & m
            x, y = fz[:, sl][w[:, sl]], z[:, sl][w[:, sl]]
            row[p] = corr(x, y) if len(x) > 20 else math.nan
        out[name] = row
    return out


def check(model: str) -> dict:
    """Memorisation checks: the six assets fed 1 / price (sign flipped back), and other books."""
    c = np.load(DIR / f"{model}-check.npz")
    tabs = rl2_data.load()
    rel = RELEASE[model]
    res = {}
    for key in ["six", "six_inv", "etf", "coin", "idx", "sec", "gspc"]:
        book = "six" if key == "six_inv" else key
        t = tabs[book].t
        fc = np.load(DIR / f"{model}.npz")["week_fc"] if key == "six" else c[key]
        if key == "six_inv":
            fc = -fc
        z = rl3_plant.week_z(t)
        fz = fc / (np.exp(t.X[:, :, ml.LOG_VOL]) * math.sqrt(7 / 365))
        res[key] = era_ic(t, fz, z, rel)
    return res


def print_check(model: str, res: dict) -> None:
    print(
        f"\n{model} memorisation checks: weekly IC by period (to2009 / 2010-19 / 2020-25 / post-release)"
    )
    for key, rows in res.items():
        for name, r in rows.items():
            print(
                f"  {key:8s} {name:7s} "
                + " ".join(f"{r[p]:+.3f}" if np.isfinite(r[p]) else "   -  " for p in r)
            )


def _json(x: object) -> object:
    if isinstance(x, date):
        return x.isoformat()
    if isinstance(x, np.floating | np.integer):
        return x.item()
    raise TypeError(type(x))


def main(models: list[str], log: bool) -> None:
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    for model in models:
        z = np.load(DIR / f"{model}.npz")
        res = {"model": model, "release": RELEASE[model].isoformat(),
               "weekly": weekly(model, z["week_fc"]), "daily": daily(model, z["day_fc"]),
               "hourly": hourly(model, z)}  # fmt: skip
        res["gate"] = gate(model, z["week_fc"], log)
        (DIR / f"eval-{model}.json").write_text(json.dumps(res, indent=1, default=_json))
        wk, dy = res["weekly"], res["daily"]
        g = res["gate"]
        print(
            f"{model}: weekly IC {wk['all']['ic']:+.3f} (pre {wk['pre']['ic']:+.3f}, post {wk['post']['ic']:+.3f} n={wk['post']['n']}), "
            f"chance {wk['chance']:.3f}, WF {wk['wf_fc']:+.3f}, gain {wk['gain']:+.3f}; daily IC {dy['all']['ic']:+.3f} "
            f"(post {dy['post']['ic']:+.3f} n={dy['post']['n']}), partial {dy['partial_trend']:+.3f}; "
            f"gate Sharpe {g['sharpe']:.3f} vs {g['tsmom12']['sharpe']:.3f} diff {g['diff']:+.3f} p {g['p']:.2f}"
        )
        for k, v in res["hourly"].items():
            print(
                f"  {k}: IC {v['all']['ic']:+.4f} post {v['post']['ic']:+.4f} (n={v['post']['n']}) r1h {v['ic_r1h']:+.4f} "
                f"partial {v['partial_trend']:+.4f} partial-post {v['partial_trend_post']:+.4f}"
            )
        if log:
            with harness.TRIES.open("a") as f:
                f.write(
                    f"| {stamp} | {IDEA} | fm-{model} weekly IC {wk['all']['ic']:+.3f} (post-release {wk['post']['ic']:+.3f}), "
                    f"WF gain {wk['gain']:+.3f} | screen | train | 2000-01 | 2025-11 | - | - | - | - |\n"
                )
                f.write(
                    f"| {stamp} | {IDEA} | fm-{model} daily IC {dy['all']['ic']:+.3f} (post-release {dy['post']['ic']:+.3f}) "
                    f"| screen | train | 2000-01 | 2025-11 | - | - | - | - |\n"
                )
                for k, v in res["hourly"].items():
                    f.write(
                        f"| {stamp} | {IDEA} | fm-{model} hourly {k} IC {v['all']['ic']:+.4f} (post-release {v['post']['ic']:+.4f}, "
                        f"partial {v['partial_trend']:+.4f}) | screen | train | 2023-01 | 2025-11 | - | - | - | - |\n"
                    )


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--check" in sys.argv:
        for mdl in args:
            r = check(mdl)
            (DIR / f"check-{mdl}.json").write_text(json.dumps(r, indent=1, default=_json))
            print_check(mdl, r)
    else:
        main(args, "--log" in sys.argv)
