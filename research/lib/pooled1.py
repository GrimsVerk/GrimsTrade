"""pooled-1: eight frozen near-miss variants of `tsmom12`, pooled over 41 markets.
Card: research/cards/pooled-1.md. Engine: pooled1_core.py.

    GRIMSTRADE_DATA=<cache root> uv run python -I research/lib/pooled1.py --random   # plumbing
    GRIMSTRADE_DATA=<cache root> uv run python -I research/lib/pooled1.py --log      # the run

Data (nothing after 2025-10-31 is parsed): Ken French 10 industries daily (cache `french/`),
insure-2's 23 Yahoo index files (cache `insure-2/raw-2026-11-18/yahoo/`), the harness's 8 other
ETFs (dividend-adjusted, `research/data/adj/<SYM>.csv`, git-ignored). `--random` replaces every
market's closes by a seeded random walk on the same dates (plumbing; writes
results/pooled-1-plumbing.md, logs nothing). The real run writes results/pooled-1.md and
results/pooled-1.json and, with `--log`, appends the card's rows to research/tries.md once.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pooled1_core as pc  # noqa: E402

IDEA = "pooled-1"
LAST = date(2025, 10, 31)  # nothing later is parsed
PRE = date(1994, 2, 1)  # the primary test's first day
PRE_MIN_WEEKS = 260
BLOCK, DRAWS, SEED = 52, 2000, 0
CHECK_BLOCKS = (13, 104)
NULL_REPS = 100
Z_BAR, Z_PROJ, KILL_HI = 2.50, 4.69, 0.03
RESEARCH = Path(__file__).resolve().parents[1]
OUT = RESEARCH / "results" / "pooled-1.md"
OUT_PLUMB = RESEARCH / "results" / "pooled-1-plumbing.md"
ETF8 = ["IWM", "EFA", "EEM", "IEF", "LQD", "VNQ", "DBC", "SLV"]
GROUPS = ("US10", "DEV13", "WIDE10", "ETF8")
LEAD = {  # in-sample lead on the six (card), for the write-up table only
    "e4": "+0.05",
    "or3-12": "+0.01 (+0.08 since 2003)",
    "arm3-12": "not scored",
    "vt-own-70-x": "+0.10",
    "vt-own-26-x": "+0.03",
    "tv40": "-0.01",
    "fade-28": "+0.04",
    "stop-0.25": "+0.04",
}


# --- data ---


def load_us10() -> list[tuple[str, str, list[date], np.ndarray]]:
    import insure1 as i1
    import trend_1926 as t
    from macro import cache_root

    snap = sorted(p for p in (cache_root() / "french").iterdir() if p.is_dir())[-1]
    ind = t.parse_industries(i1._lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), LAST)
    days = sorted(ind)
    out = []
    for j, n in enumerate(t.INDUSTRIES):
        r = np.array([ind[d][j] for d in days])
        keep = ~np.isnan(r)
        dd = [d for d, ok in zip(days, keep, strict=True) if ok]
        out.append((f"US-{n}", "US10", dd, 100 * np.cumprod(1 + r[keep])))
    return out


def load_indices() -> list[tuple[str, str, list[date], np.ndarray]]:
    import insure2 as i2
    from macro import cache_root

    root = cache_root() / i2.RAW / "yahoo"
    out = []
    for grp, tickers in (("DEV13", i2.PRIMARY_GEO), ("WIDE10", i2.WIDER_GEO)):
        for tk, n in tickers.items():
            days, ret = i2.load_yahoo(root / f"{tk}.json")
            if days[-1] > LAST:
                raise AssertionError(f"{tk}: a day after {LAST}")
            out.append((n, grp, days, 100 * np.cumprod(1 + ret)))
    return out


def load_etfs() -> list[tuple[str, str, list[date], np.ndarray]]:
    adj = RESEARCH / "data" / "adj"
    out = []
    for s in ETF8:
        days, px = [], []
        with (adj / f"{s}.csv").open(newline="") as f:
            for row in csv.DictReader(f):
                d = date.fromisoformat(row["date"])
                if d > LAST:
                    break  # rows are in date order; nothing later is parsed
                days.append(d)
                px.append(float(row["close"]))
        out.append((s, "ETF8", days, np.array(px)))
    return out


def load_all() -> list[tuple[str, str, list[date], np.ndarray]]:
    return load_us10() + load_indices() + load_etfs()


def randomise(
    raw: list[tuple[str, str, list[date], np.ndarray]],
) -> list[tuple[str, str, list[date], np.ndarray]]:
    rng = np.random.default_rng(12345)
    out = []
    for n, g, days, _ in raw:
        lr = rng.normal(0.06 / 252, 0.18 / math.sqrt(252), len(days))
        lr[0] = 0.0
        out.append((n, g, days, 100 * np.exp(np.cumsum(lr))))
    return out


def drift_matched(
    raw: list[tuple[str, str, list[date], np.ndarray]], seed: int
) -> list[tuple[str, str, list[date], np.ndarray]]:
    """Amendment 1: i.i.d. normal walk with each market's own daily log-return mean and sd."""
    rng = np.random.default_rng(seed)
    out = []
    for n, g, days, px in raw:
        real = np.diff(np.log(px))
        lr = rng.normal(real.mean(), real.std(), len(days))
        lr[0] = 0.0
        out.append((n, g, days, 100 * np.exp(np.cumsum(lr))))
    return out


def run_all(
    raw: list[tuple[str, str, list[date], np.ndarray]], quiet: bool = False
) -> list[pc.Market]:
    markets = []
    for n, g, days, px in raw:
        if days[-1] > LAST:
            raise AssertionError(f"{n}: a day after {LAST}")
        d = np.array([x.toordinal() for x in days], dtype=np.int64)
        markets.append(pc.run_market(n, g, d, px))
        if not quiet:
            print(f"  {n}: {days[0]}..{days[-1]}, {len(days)} sessions", file=sys.stderr)
    return markets


def null_D(raw: list[tuple[str, str, list[date], np.ndarray]], reps: int = NULL_REPS) -> np.ndarray:
    """D[variant, replication] under the drift-matched null (point estimates)."""
    out = np.zeros((len(pc.VARIANTS), reps))
    for b in range(reps):
        p = pc.panel(run_all(drift_matched(raw, 1000 + b), quiet=True))
        out[:, b] = np.nanmean(pc.diffs_of(*pc.sums(p.R)), axis=1)
        print(f"  null {b + 1}/{reps}", file=sys.stderr)
    return out


# --- run ---


def market_stats(m: pc.Market, r: str) -> tuple[float, float, float, float]:
    """(weekly Sharpe, total return, max drawdown, position change a year) on the scored span."""
    f, w = pc.weekly(m.d, m.daily[r], m.start)
    eq = np.cumprod(1 + m.daily[r][m.start :])
    mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
    years = (int(m.d[-1]) - int(m.d[m.start])) / 365.25
    pos = m.pos.get(r)
    turn = math.nan if pos is None else float(np.abs(np.diff(pos[m.start - 1 :])).sum() / years)
    return pc.sharpe(w), float(eq[-1] - 1), mdd, turn


def corr_with_twin(p: pc.Panel, a: int) -> float:
    cs = []
    for i in range(p.R.shape[1]):
        x, y = p.R[a, i], p.R[0, i]
        ok = ~np.isnan(x)
        if x[ok].std() > 0 and y[ok].std() > 0:
            cs.append(float(np.corrcoef(x[ok], y[ok])[0, 1]))
    return float(np.mean(cs))


def analyse(markets: list[pc.Market]) -> dict:  # type: ignore[type-arg]
    p = pc.panel(markets)
    groups = np.array(p.groups)
    sets = {"all": np.ones(len(markets), bool), **{g: groups == g for g in GROUPS}}
    bt = pc.bootstrap(p, sets, BLOCK, DRAWS, SEED)
    checks = {b: pc.bootstrap(p, {"all": sets["all"]}, b, DRAWS, SEED) for b in CHECK_BLOCKS}
    sel = p.cal < PRE.toordinal()
    n_pre = (~np.isnan(p.R[0][:, sel])).sum(-1)
    pre_mask = n_pre >= PRE_MIN_WEEKS
    bt_pre = pc.bootstrap(p, {"pre": pre_mask}, BLOCK, DRAWS, SEED, sel=sel)
    res: dict = {"variants": {}, "markets": []}  # type: ignore[type-arg]
    for v, name in enumerate(pc.VARIANTS):
        a = pc.pooled(bt, "all", v)
        g = {gr: pc.pooled(bt, gr, v) for gr in GROUPS}
        pre = pc.pooled(bt_pre, "pre", v)
        gpos = sum(1 for x in g.values() if x.D > 0)
        res["variants"][name] = {
            "all": vars(a),
            "groups": {k: vars(x) for k, x in g.items()},
            "pre1994": vars(pre),
            "pre1994_markets": int(pre_mask.sum()),
            "groups_pos": gpos,
            "se_block": {str(b): pc.pooled(c, "all", v).se for b, c in checks.items()},
            "mde80": (Z_BAR + 0.8416) * a.se,
            "mde80_proj": (Z_PROJ + 0.8416) * a.se,
            "corr_twin": corr_with_twin(p, v + 1),
            "verdict": pc.verdict(a, gpos, pre.D > 0, Z_BAR, Z_PROJ, KILL_HI),
        }
    for i, m in enumerate(markets):
        row = {
            "name": m.name,
            "group": m.group,
            "from": str(date.fromordinal(int(m.d[m.start]))),
            "to": str(date.fromordinal(int(m.d[-1]))),
            "weeks": int((~np.isnan(p.R[0, i])).sum()),
            "stats": {r: market_stats(m, r) for r in pc.RULES},
            "d": {v: float(bt.d[k, i]) for k, v in enumerate(pc.VARIANTS)},
        }
        res["markets"].append(row)
    return res


def f2(x: float) -> str:
    return f"{x:+.3f}"


def report(res: dict, title: str) -> str:  # type: ignore[type-arg]
    L = [
        f"# {title}",
        "",
        "Card: `cards/pooled-1.md`. Code: `lib/pooled1.py`, `lib/pooled1_core.py`. Weekly "
        "Sharpe (sqrt 52), cash 0, fill one session late, 2 bps a side. d = Sharpe(variant) - "
        f"Sharpe(`tsmom12`) on the same market and weeks; D = equal-weight mean over markets; SE "
        f"from a joint circular block bootstrap of calendar weeks ({BLOCK}-week blocks, {DRAWS} "
        f"draws, seed {SEED}). Bars: z >= {Z_BAR} (8 variants, Bonferroni); project z >= "
        f"{Z_PROJ}; killed if the 95% upper end < +{KILL_HI} or z <= -{Z_BAR}.",
        "",
        "## Pooled, 41 markets",
        "",
        "| Variant | Lead on the six | D | SE | z | 95% (normal) | 95% (percentile) | d > 0 | "
        "US10 | DEV13 | WIDE10 | ETF8 | Before 1994 (markets) | SE, 13 / 104-week blocks | "
        "Edge seen 80% (z 2.50 / 4.69) | Corr. with twin | Verdict |",
        "|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---|",
    ]
    for v, r in res["variants"].items():
        a, g, pre = r["all"], r["groups"], r["pre1994"]
        gs = [f"{f2(g[k]['D'])} ({g[k]['se']:.3f})" for k in GROUPS]
        sb = r["se_block"]
        L.append(
            f"| `{v}` | {LEAD.get(v, '')} | {f2(a['D'])} | {a['se']:.3f} | {a['z']:+.2f} | "
            f"{f2(a['lo'])}..{f2(a['hi'])} | {f2(a['plo'])}..{f2(a['phi'])} | "
            f"{a['n_pos']} of {a['n']} | {' | '.join(gs)} | {f2(pre['D'])} ({pre['se']:.3f}, z "
            f"{pre['z']:+.2f}; {r['pre1994_markets']}) | {sb['13']:.3f} / {sb['104']:.3f} | "
            f"+{r['mde80']:.2f} / +{r['mde80_proj']:.2f} | {r['corr_twin']:.2f} | "
            f"**{r['verdict']}** |"
        )
    L += [
        "",
        "Group cells: D (SE). Before 1994: weeks before 1994-02-01, markets with at least "
        f"{PRE_MIN_WEEKS} scored weeks there.",
        "",
        *null_table(res),
        "## Per market: `tsmom12` and d of each variant",
        "",
        "| Market | Group | Scored from | Weeks | `tsmom12` Sharpe | Max DD | "
        + " | ".join(f"`{v}`" for v in pc.VARIANTS)
        + " |",
        "|---|---|---|---:|---:|---:|" + "---:|" * len(pc.VARIANTS),
    ]
    for m in res["markets"]:
        sh, _, mdd, _ = m["stats"]["tsmom12"]
        L.append(
            f"| {m['name']} | {m['group']} | {m['from']} | {m['weeks']} | {sh:.2f} | "
            f"{mdd:.0%} | " + " | ".join(f2(m["d"][v]) for v in pc.VARIANTS) + " |"
        )
    L += [
        "",
        "## Per market: Sharpe of each rule",
        "",
        "| Market | " + " | ".join(f"`{r}`" for r in pc.RULES) + " |",
        "|---|" + "---:|" * len(pc.RULES),
    ]
    for m in res["markets"]:
        L.append(
            f"| {m['name']} | " + " | ".join(f"{m['stats'][r][0]:.2f}" for r in pc.RULES) + " |"
        )
    return "\n".join(L) + "\n"


def null_table(res: dict) -> list[str]:  # type: ignore[type-arg]
    if not all("null" in r for r in res["variants"].values()):
        return []
    out = [
        "",
        f"## Drift-matched null (amendment 1; {NULL_REPS} random walks with each market's own "
        "drift and volatility)",
        "",
        "| Variant | D | Null mean | Null 5% / 95% | D beyond drift | Verdict | Reading |",
        "|---|---:|---:|---|---:|---|---|",
    ]
    for v, r in res["variants"].items():
        nl = r["null"]
        out.append(
            f"| `{v}` | {f2(r['all']['D'])} | {f2(nl['mean'])} | {f2(nl['q5'])} / "
            f"{f2(nl['q95'])} | {f2(r['beyond_drift'])} | {r['verdict']} | {r['reading']} |"
        )
    return [*out, ""]


def log_tries(res: dict) -> int:  # type: ignore[type-arg]
    tries = RESEARCH / "tries.md"
    text = tries.read_text()
    now = f"{datetime.now(UTC):%Y-%m-%d %H:%M}"
    rows = []
    first = min(m["from"] for m in res["markets"])
    last = max(m["to"] for m in res["markets"])
    for v, r in res["variants"].items():
        a = r["all"]
        name = (
            f"{v}@pooled-41 (pooled dSharpe vs tsmom12 {a['D']:+.3f}, SE {a['se']:.3f}, "
            f"z {a['z']:+.2f}; weekly Sharpe; {r['verdict']}; {r.get('reading', '-')})"
        )
        mean_sh = float(np.mean([m["stats"][v][0] for m in res["markets"]]))
        if f"| {IDEA} | {v}@pooled-41 " not in text:
            rows.append(
                f"| {now} | {IDEA} | {name} | variant | train | {first} | {last} | "
                f"{mean_sh:.2f} | - | - | - |\n"
            )
    for m in res["markets"]:
        for r in pc.RULES:
            tag = f"{r}@{m['group']}-{m['name']}"
            if f"| {IDEA} | {tag} |" in text:
                continue
            sh, tot, mdd, turn = m["stats"][r]
            ts = "-" if math.isnan(turn) else f"{turn:.2f}"
            rows.append(
                f"| {now} | {IDEA} | {tag} | robustness | train | {m['from']} | "
                f"{m['to']} | {sh:.2f} | {tot:+.1%} | {mdd:.1%} | {ts} |\n"
            )
    with tries.open("a") as f:
        f.writelines(rows)
    return len(rows)


def main() -> None:
    random_mode = "--random" in sys.argv
    raw = load_all()
    if random_mode:
        raw = randomise(raw)
    res = analyse(run_all(raw))
    if random_mode:
        OUT_PLUMB.write_text(report(res, "pooled-1 plumbing run: random-walk prices (not data)"))
        print(f"wrote {OUT_PLUMB}")
        return
    nd = null_D(raw)
    for v, name in enumerate(pc.VARIANTS):
        r = res["variants"][name]
        q5, q95 = (float(x) for x in np.percentile(nd[v], [5, 95]))
        r["null"] = {"mean": float(nd[v].mean()), "q5": q5, "q95": q95}
        r["beyond_drift"] = r["all"]["D"] - r["null"]["mean"]
        if r["verdict"] in ("real small edge", "selectable candidate") and r["all"]["D"] <= q95:
            r["reading"] = "exposure, not timing"
        elif r["verdict"] == "killed" and q5 <= r["all"]["D"] <= q95:
            r["reading"] = "no timing effect either way"
        else:
            r["reading"] = "-"
    OUT.write_text(report(res, "pooled-1: eight near-miss variants, pooled over 41 markets"))
    OUT.with_suffix(".json").write_text(json.dumps(res, indent=1) + "\n")
    print(f"wrote {OUT}")
    if "--log" in sys.argv:
        print(f"tries.md: {log_tries(res)} rows")


if __name__ == "__main__":
    main()
