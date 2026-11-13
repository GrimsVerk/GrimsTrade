"""Research run carry-2: short-1's carry book on venues and coins it never saw (card in
research/carry-2.md).

    uv run python -I research/lib/carry2.py [--log] [--legs]

Reads (never runs) the raw downloads of `scripts/fetch_carry2.py` from the shared cache, builds
one daily panel per venue (cached under `<cache_root>/derived/carry-2/`, bars after the train
cut dropped), and runs short-1's `ls-premium` / `ls-funding` books unchanged with
`short_engine.simulate`. Writes `research/results/carry-2.md`. Without `--log` nothing is
written to tries.md.
"""

from __future__ import annotations

import json
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import carry2_panel  # noqa: E402
import macro  # noqa: E402
import short_engine as se  # noqa: E402
import stats  # noqa: E402
from breadth_agg import _kline_rows  # noqa: E402
from breadth_xs import logret, roll_mean, roll_median  # noqa: E402
from carry2_panel import DAY0, N_DAYS, Acc  # noqa: E402
from harness import TRAIN_END, TRAIN_LAST_BAR  # noqa: E402

assert TRAIN_LAST_BAR == carry2_panel.TRAIN_LAST_BAR
ERAS = [(2020, 2021), (2022, 2025)]
YEARS = list(range(2020, 2026))
PERP_COST, HIGH_COST, TWIN_COST = 0.001, 0.003, 0.003
OUT = Path(__file__).resolve().parents[1] / "results" / "carry-2.md"
SIGNALS = ("premium", "funding")


def raw() -> Path:
    return macro.cache_root()


def derived() -> Path:
    d = macro.cache_root() / "derived" / "carry-2"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ts(a: np.ndarray) -> np.ndarray:
    t = a.astype(float).copy()
    t[t > 1e14] /= 1000.0  # some 2025 Binance files are in microseconds
    return (t // 1000).astype(np.int64)


def load_binance() -> None:
    root = raw() / "binance" / "futures" / "um" / "monthly"
    acc = Acc()
    for d in sorted((root / "klines").iterdir()):
        files = sorted((d / "1d").glob("*.zip"))
        fz = sorted((root / "fundingRate" / d.name).glob("*.zip"))
        if not files or not fz:
            continue  # never passed the volume pre-filter (or no funding history)
        k = np.concatenate([a for a in (_kline_rows(p) for p in files) if len(a)])
        rows = []
        for p in fz:
            with zipfile.ZipFile(p) as z:
                for ln in z.read(z.namelist()[0]).decode().splitlines():
                    f = ln.split(",")
                    if f[0].isdigit():
                        rows.append((int(f[0]) // 1000, float(f[-1])))
        f = np.array(sorted(set(rows)))
        pf = [
            a
            for a in (
                _kline_rows(p)
                for p in sorted((root / "premiumIndexKlines" / d.name / "1h").glob("*.zip"))
            )
            if len(a)
        ]
        pt = pv = None
        if pf:
            a = np.concatenate(pf)
            pt, i = np.unique(_ts(a[:, 0]), return_index=True)
            pv = a[i, 4]
        acc.add(d.name, _ts(k[:, 0]), k[:, 4], k[:, 7], f[:, 0].astype(np.int64), f[:, 1], pt, pv)
    acc.save(derived(), "binance")


def load_bybit() -> None:
    base = raw() / "bybit" / "linear" / "to-2025-11-10"
    acc = Acc()
    for d in sorted(base.iterdir()):
        if not (d / "funding.json").exists():
            continue
        k = np.array(json.loads((d / "kline-D.json").read_text()), dtype=float)
        fl = json.loads((d / "funding.json").read_text())
        ft = np.array([int(x["fundingRateTimestamp"]) // 1000 for x in fl], dtype=np.int64)
        fr = np.array([float(x["fundingRate"]) for x in fl])
        ft, i = np.unique(ft, return_index=True)
        pt = pv = None
        if (d / "premium-1h.json").exists():
            p = np.array(json.loads((d / "premium-1h.json").read_text()), dtype=float)
            if len(p):
                pt, i2 = np.unique((p[:, 0] // 1000).astype(np.int64), return_index=True)
                pv = p[i2, 4]
        acc.add(d.name, (k[:, 0] // 1000).astype(np.int64), k[:, 4], k[:, 6], ft, fr[i], pt, pv)
    acc.save(derived(), "bybit")


def load_hyperliquid() -> None:
    base = raw() / "hyperliquid" / "perp" / "to-2025-11-10"
    acc = Acc()
    for d in sorted(base.iterdir()):
        if not (d / "funding.json").exists():
            continue
        c = json.loads((d / "candles-1d.json").read_text())
        t = np.array([int(x["t"]) // 1000 for x in c], dtype=np.int64)
        close = np.array([float(x["c"]) for x in c])
        qv = np.array([float(x["v"]) * float(x["c"]) for x in c])
        fl = json.loads((d / "funding.json").read_text())
        ft = np.array([int(x["time"]) // 1000 for x in fl], dtype=np.int64)
        fr = np.array([float(x["fundingRate"]) for x in fl])
        pv = np.array([float(x["premium"]) for x in fl])
        ft, i = np.unique(ft, return_index=True)
        acc.add(d.name, t, close, qv, ft, fr[i], ft, pv[i])
    acc.save(derived(), "hyperliquid")


# ---------------------------------------------------------------- books


class Venue:
    def __init__(
        self, label: str, file: str, keep: list[str] | None = None, drop: set[str] | None = None
    ) -> None:
        z = np.load(derived() / f"{file}.npz")
        names = [str(x) for x in z["names"]]
        cols = [
            j
            for j, s in enumerate(names)
            if (keep is None or s in keep) and s not in (drop or set())
        ]
        self.label = label
        self.names = [names[j] for j in cols]
        self.px = z["px"][:, cols]
        qv = z["qv"][:, cols]
        self.fund = z["fsim"][:, cols]
        cnt = z["fcnt"][:, cols]
        alive = (cnt > 0) | (np.vstack([np.zeros((1, len(cols))), cnt[:-1]]) > 0)
        hist = bb.history_days(self.px)
        elig = (hist >= 365) & (roll_median(qv, 30) >= 5e6) & np.isfinite(self.px)
        self.tradable = elig & alive
        with np.errstate(invalid="ignore", divide="ignore"):
            self.sig = {
                "funding": -roll_mean(z["fsig"][:, cols], 7, 0.5),
                "premium": -roll_mean(z["prem"][:, cols], 7, 0.5),
            }
            self.up = logret(self.px, 365, 0) > 0
        last_px = np.where(
            np.isfinite(self.px).any(0), N_DAYS - 1 - np.isfinite(self.px[::-1]).argmax(0), -1
        )
        self.delisted = last_px < N_DAYS - 31  # no price in the last month of train


def run_venue(v: Venue, log: bool, legs: bool) -> dict[str, Any] | None:
    n_days, n = v.px.shape
    cnt = v.tradable.sum(1)
    if not (cnt >= 10).any():
        return None
    s0 = int(np.argmax(cnt >= 10))
    days = np.arange(s0, n_days)
    wd = np.array([(DAY0 + timedelta(days=int(i))).weekday() for i in days])
    dec = days[(wd == 4) & (days <= (TRAIN_END - DAY0).days)]
    dw, _, _ = xs.schedule(n_days, dec, 0)
    b0 = int(dw[0])
    first = DAY0 + timedelta(days=b0 + 1)
    years = (n_days - b0) / 365

    def mask(t: int) -> np.ndarray:
        return v.tradable[t] & np.isfinite(v.px[t])

    def ts(t: int) -> np.ndarray:
        m = mask(t)
        return np.where(m & v.up[t], 1.0 / max(m.sum(), 1), 0.0)

    targets: dict[str, tuple[np.ndarray, str]] = {
        "tsmom12 twin": (np.array([ts(t) for t in dw]), "baseline"),
        "tsmom12 perp": (np.array([ts(t) for t in dw]), "baseline"),
        "EW perp": (np.array([mask(t) / max(mask(t).sum(), 1) for t in dw]), "baseline"),
    }
    for k in SIGNALS:
        s = v.sig[k]
        if not np.isfinite(s[dw][v.tradable[dw]]).any():
            continue
        w = np.array([se.long_short(s[t], mask(t) & np.isfinite(s[t])) for t in dw])
        targets[f"ls-{k}"] = (w, "variant")
    rows: dict[str, dict[str, Any]] = {}
    series: dict[str, np.ndarray] = {}
    for name, (tg, kind) in targets.items():
        turn = float(np.abs(np.diff(tg, axis=0)).sum() / years)
        costs = [TWIN_COST] if name == "tsmom12 twin" else [PERP_COST, HIGH_COST]
        for c in costs:
            fund = None if name == "tsmom12 twin" else v.fund
            run = se.simulate(v.px, fund, tg, dw, c, b0)
            key = name if c == costs[0] else f"{name} @30"
            series[key] = run.r
            rows[key] = summary(run.r, first) | {
                "funding_yr": float(run.funding.sum() / years),
                "turn_yr": turn,
            }
            if log:
                kd = kind if c == costs[0] else "robustness"
                cd = (
                    "perp close as spot, 30 bps"
                    if fund is None
                    else f"perp {c * 1e4:.0f} bps + funding"
                )
                bb.log_row(f"carry-2-{v.label}", f"{name}, {cd}", kd, first, run.r, turn)
        if name.startswith("ls-"):
            ever = (tg != 0).any(0)
            rows[name]["coins_used"] = int(ever.sum())
            rows[name]["delisted_used"] = int((ever & v.delisted).sum())
            if legs:
                for sign, leg in ((1, "long"), (-1, "short")):
                    lt = np.where(sign * tg > 0, tg, 0.0)
                    run = se.simulate(v.px, v.fund, lt, dw, PERP_COST, b0)
                    rows[name][f"{leg}_leg"] = (
                        stats.sharpe(run.r),
                        stats.cagr(run.r),
                        float(run.funding.sum() / years),
                    )
                    if log:
                        lturn = float(np.abs(np.diff(lt, axis=0)).sum() / years)
                        bb.log_row(
                            f"carry-2-{v.label}",
                            f"{name} {leg} leg alone (diagnostic)",
                            "robustness",
                            first,
                            run.r,
                            lturn,
                        )
    add_blends(rows, series, first)
    info = {
        "label": v.label,
        "first": str(first),
        "coins": n,
        "delisted": int(v.delisted.sum()),
        "tradable_median": float(np.median(cnt[b0:])),
        "weeks": len(dw),
        "years": years,
    }
    return {"info": info, "rows": rows, "series": series, "b0": b0}


def summary(r: np.ndarray, first: date) -> dict[str, Any]:
    yrs = np.array([(first + timedelta(days=i)).year for i in range(len(r))])

    def sub(y0: int, y1: int) -> float | None:
        m = (yrs >= y0) & (yrs <= y1)
        return stats.sharpe(r[m]) if m.sum() >= 180 else None

    eq = np.cumprod(1 + r)
    return {
        "sharpe": stats.sharpe(r),
        "cagr": stats.cagr(r),
        "mdd": stats.max_drawdown(r),
        "worst_week": float((eq[7:] / eq[:-7] - 1).min()) if len(r) > 7 else float("nan"),
        "eras": [sub(a, b) for a, b in ERAS],
        "years": [sub(y, y) for y in YEARS],
    }


def add_blends(rows: dict[str, dict[str, Any]], series: dict[str, np.ndarray], first: date) -> None:
    tw = series["tsmom12 twin"]
    for key, r in series.items():
        rows[key]["corr_ts"] = float(np.corrcoef(r, tw)[0, 1]) if r.std() > 0 else 0.0
        if key.startswith("ls-"):
            blend = 0.5 * tw + 0.5 * r
            d, p, _, _ = stats.sharpe_diff_boot(blend, tw)
            _, p0, _, _ = stats.sharpe_diff_boot(r, np.zeros_like(r))
            rows[key] |= {
                "p_zero": p0,
                "blend_sharpe": stats.sharpe(blend),
                "blend_diff": d,
                "blend_p": p,
                "blend_mdd": stats.max_drawdown(blend),
                "dd_spells": se.dd_spells(r),
            }


def pooled(outs: list[dict[str, Any]], log: bool) -> dict[str, Any]:
    """Equal capital per venue book on each day it exists."""
    keys = sorted(set.intersection(*(set(o["series"]) for o in outs)))
    start = min(o["b0"] for o in outs) + 1
    n = N_DAYS - start
    series: dict[str, np.ndarray] = {}
    for k in keys:
        tot = np.zeros(n)
        cnt = np.zeros(n)
        for o in outs:
            off = o["b0"] + 1 - start
            tot[off:] += o["series"][k]
            cnt[off:] += 1
        series[k] = tot / cnt
    first = DAY0 + timedelta(days=start)
    rows = {k: summary(r, first) for k, r in series.items()}
    for k in rows:
        rows[k] |= {"funding_yr": float("nan"), "turn_yr": float("nan")}
        if log:
            kind = (
                "robustness"
                if k.endswith("@30")
                else ("variant" if k.startswith("ls-") else "baseline")
            )
            bb.log_row(
                "carry-2-pooled",
                f"{k}, equal capital per venue",
                kind,
                first,
                series[k],
                float("nan"),
            )
    add_blends(rows, series, first)
    label = "pooled (" + ", ".join(o["info"]["label"] for o in outs) + ")"
    info = {"label": label, "first": str(first), "years": n / 365}
    return {"info": info, "rows": rows, "series": series}


def verdict(pool: dict[str, Any], venues: dict[str, dict[str, Any]], sig: str) -> dict[str, Any]:
    key = f"ls-{sig}"
    p = pool["rows"][key]
    bout = venues["B-out"]["rows"].get(key, {})
    others = []
    for lab in ("Bybit", "Hyperliquid"):
        o = venues.get(lab)
        if o and key in o["rows"] and (lab != "Hyperliquid" or o["info"]["weeks"] >= 52):
            others.append(o["rows"][key]["sharpe"] > 0)
    eras = [e for e in p["eras"] if e is not None]
    p30 = pool["rows"].get(f"{key} @30", {})
    bars = {
        "1 pooled Sharpe > 0, p < 0.10": p["sharpe"] > 0 and p["p_zero"] < 0.10,
        "2 B-out > 0 and Bybit or Hyperliquid > 0": bool(bout)
        and bout["sharpe"] > 0
        and any(others),
        "3 pooled blend beats twin, p < 0.10": p["blend_p"] < 0.10,
        "4 pooled > 0 in both eras": bool(eras) and all(e > 0 for e in eras),
        "(5) at 30 bps: pooled > 0 and blend p < 0.20": bool(p30)
        and p30["sharpe"] > 0
        and p30.get("blend_p", 1) < 0.20,
    }
    ok = all(v for k, v in bars.items() if not k.startswith("("))
    return {"signal": sig, "bars": bars, "replicates": ok}


# ---------------------------------------------------------------- report


def f(x: Any, fmt: str) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else format(x, fmt)


def table(o: dict[str, Any]) -> str:
    i = o["info"]
    head = f"### {i['label']}\n\nFirst return day {i['first']}, {i['years']:.1f} years."
    if "coins" in i:
        head += (
            f" Coins with data: {i['coins']} ({i['delisted']} without a price in train's last"
            f" month, i.e. delisted); tradable per day median {i['tradable_median']:.0f};"
            f" weekly decisions {i['weeks']}."
        )
    cols = ["Shape", "Sharpe", "CAGR", "Max DD", "Worst week", "2020-21", "2022-25"]
    cols += [str(y) for y in YEARS]
    cols += [
        "Funding/yr",
        "Turn/yr",
        "Corr twin",
        "p(S>0)",
        "Blend",
        "Blend - twin (p)",
        "Blend DD",
    ]
    lines = [head, "", "| " + " | ".join(cols) + " |", "|---|" + "---:|" * (len(cols) - 1)]
    for k, r in o["rows"].items():
        cells = [
            k,
            f(r["sharpe"], ".2f"),
            f(r["cagr"], "+.1%"),
            f(r["mdd"], ".0%"),
            f(r["worst_week"], "+.0%"),
        ]
        cells += [f(e, "+.2f") for e in r["eras"]] + [f(e, "+.2f") for e in r["years"]]
        cells += [f(r["funding_yr"], "+.1%"), f(r["turn_yr"], ".0f"), f(r["corr_ts"], "+.2f")]
        if "blend_p" in r:
            cells += [
                f(r["p_zero"], ".3f"),
                f(r["blend_sharpe"], ".2f"),
                f"{r['blend_diff']:+.2f} ({r['blend_p']:.3f})",
                f(r["blend_mdd"], ".0%"),
            ]
        else:
            cells += ["", "", "", ""]
        lines.append("| " + " | ".join(cells) + " |")
    extra = []
    for k, r in o["rows"].items():
        if "coins_used" in r:
            s = (
                f"- `{k}`: {r['coins_used']} coins ever held,"
                f" {r['delisted_used']} of them delisted later in train"
            )
            if "long_leg" in r:
                lg, sh = r["long_leg"], r["short_leg"]
                s += (
                    f"; long leg alone Sharpe {lg[0]:.2f} (CAGR {lg[1]:+.1%}, funding"
                    f" {lg[2]:+.1%}/yr), short leg alone {sh[0]:.2f} (CAGR {sh[1]:+.1%},"
                    f" funding {sh[2]:+.1%}/yr)"
                )
            extra.append(s + ".")
    return "\n".join(lines + [""] + extra) + "\n"


def main() -> None:
    log = "--log" in sys.argv
    legs = "--legs" in sys.argv
    for venue, fn in (
        ("binance", load_binance),
        ("bybit", load_bybit),
        ("hyperliquid", load_hyperliquid),
    ):
        if not (derived() / f"{venue}.npz").exists():
            fn()
            print("panel", venue, flush=True)
    p30 = [p.name.split("-")[1] for p in bb.derived().glob("binance-*-1h.npz")]
    venues: dict[str, dict[str, Any]] = {}
    for v in (
        Venue("B-out", "binance", drop=set(p30)),
        Venue("Bybit", "bybit"),
        Venue("Hyperliquid", "hyperliquid"),
    ):
        o = run_venue(v, log, legs)
        if o:
            venues[v.label] = o
            print("ran", v.label, flush=True)
    pool = pooled(list(venues.values()), log)
    extra = []
    for v in (Venue("B-all", "binance"), Venue("B-P30 (perp closes)", "binance", keep=p30)):
        o = run_venue(v, False, False)
        if o:
            extra.append(o)
            if log:  # robustness only: the card's tests are on B-out, Bybit, Hyperliquid
                for k, r in o["series"].items():
                    bb.log_row(
                        f"carry-2-{v.label.split()[0]}",
                        f"{k} (robustness set)",
                        "robustness",
                        date.fromisoformat(o["info"]["first"]),
                        r,
                        o["rows"][k]["turn_yr"],
                    )
    verdicts = [verdict(pool, venues, s) for s in SIGNALS]
    vtxt = []
    for vd in verdicts:
        vtxt.append(
            f"**`ls-{vd['signal']}`: {'REPLICATES' if vd['replicates'] else 'does not replicate'}**"
        )
        vtxt += [f"- bar {k}: {'yes' if ok else 'no'}" for k, ok in vd["bars"].items()]
        vtxt.append("")
    head = (
        "# Carry 2: raw tables (train, decisions to 2025-11-09)\n\n"
        "Script `lib/carry2.py`; card and reading in `research/carry-2.md`. `ls-` books and"
        " perp baselines at 10 bps a side plus every funding event; `@30`: the same at 30 bps."
        " `tsmom12 twin`: long-only on the venue's perp closes (standing in for spot), 30 bps,"
        " no funding. Sharpe on daily returns, 365 days; per-era and per-year Sharpe need 180"
        " days. `p(S>0)`: one-sided stationary-bootstrap p that the book's Sharpe is above 0."
        " Blend: 50% twin + 50% the book, re-split daily; p one-sided. Pooled: equal capital per"
        " venue book on each day it exists (funding and turnover not pooled).\n\n"
        "## Verdict (card bars)\n\n" + "\n".join(vtxt) + "\n"
    )
    body = [table(pool)] + [table(o) for o in venues.values()]
    body.append(
        "## Robustness sets (not part of the bars)\n\n" + "\n".join(table(o) for o in extra)
    )
    OUT.write_text(head + "\n".join(body))
    dump = {"verdicts": verdicts, "pool": {**pool, "series": None}}
    dump |= {k: {**o, "series": None} for k, o in venues.items()}
    (derived() / "results.json").write_text(json.dumps(dump, indent=1, default=str))
    print(OUT.read_text())


if __name__ == "__main__":
    main()
