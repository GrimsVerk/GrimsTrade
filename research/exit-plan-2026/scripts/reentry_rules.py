"""Re-entry rules test, card `research/cards/reentry.md` (rules, samples and bar fixed there).

Every run appends one row per rule and sample to `research/tries.md`.
Run: GRIMSTRADE_DATA=... uv run --with xlrd --with pandas python <this file>
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from reentry_data import monthly_frame

TRIES = Path(__file__).resolve().parents[2] / "tries.md"
HORIZONS = (60, 120)
SPLIT = pd.Period("1972-01", freq="M")
NAMED = [
    "1929-08", "1937-02", "1968-11", "1972-12", "1987-08", "2000-03", "2007-10", "2021-12",
    "1996-12", "1997-12", "1998-12", "2005-12", "2019-12",
]  # fmt: skip

# A rule maps (frame arrays, decision index i, month index k >= i) -> target invested fraction.
Rule = Callable[[dict, int, int], float]


def _seen(cond: np.ndarray, i: int, k: int) -> bool:
    return bool(cond[i : k + 1].any())


def rule_now(a: dict, i: int, k: int) -> float:
    return 1.0


def rule_dca12(a: dict, i: int, k: int) -> float:
    return min(1.0, (k - i + 1) / 12)


def make_dd(level: float, deadline: int | None = None) -> Rule:
    def rule(a: dict, i: int, k: int) -> float:
        if deadline is not None and k - i >= deadline:
            return 1.0
        return 1.0 if _seen(a["DD"] <= -level, i, k) else 0.0

    return rule


def rule_dd20_sma10(a: dict, i: int, k: int) -> float:
    hit = np.flatnonzero(a["DD"][i : k + 1] <= -0.20)
    if hit.size == 0:
        return 0.0
    j = i + int(hit[0])
    return 1.0 if _seen(a["C"] > a["SMA10"], j, k) else 0.0


def rule_cape_median(a: dict, i: int, k: int) -> float:
    return 1.0 if _seen(a["CAPE"] <= a["CAPE_MED"], i, k) else 0.0


def rule_staged24(a: dict, i: int, k: int) -> float:
    if k - i >= 24:
        return 1.0
    worst = a["DD"][i : k + 1].min()
    return (worst <= -0.20) / 3 + (worst <= -0.30) / 3 + (worst <= -0.40) / 3


RULES: dict[str, tuple[Rule, str]] = {
    "now": (rule_now, "baseline"),
    "dca12": (rule_dca12, "variant"),
    "dd20": (make_dd(0.20), "variant"),
    "dd30": (make_dd(0.30), "variant"),
    "dd20-sma10": (rule_dd20_sma10, "variant"),
    "cape-median": (rule_cape_median, "variant"),
    "staged-24": (rule_staged24, "variant"),
    "dd30-24": (make_dd(0.30, deadline=24), "variant"),
}


def simulate(a: dict, rule: Rule, i: int, horizon: int) -> tuple[float, float]:
    """Terminal wealth and invested fraction at i + horizon; start 1 in cash at month-end i."""
    cash, eq, f_prev = 1.0, 0.0, 0.0
    for k in range(i, i + horizon + 1):
        if k > i:
            eq *= 1 + a["R"][k]
            cash *= 1 + a["RF"][k]
        if k == i + horizon:
            break
        f = max(f_prev, rule(a, i, k))
        if f > f_prev:
            move = cash * (f - f_prev) / (1 - f_prev)
            cash -= move
            eq += move
            f_prev = f
    return cash + eq, f_prev


def frame_arrays(df: pd.DataFrame) -> dict:
    out = {c: df[c].to_numpy(dtype=float) for c in ("C", "R", "RF", "DD", "SMA10", "CAPE")}
    out["CAPE_MED"] = df["CAPE_MED"].to_numpy(dtype=float)
    return out


def episodes(months: pd.PeriodIndex) -> int:
    if len(months) == 0:
        return 0
    n, prev = 1, months[0]
    for m in months[1:]:
        if (m - prev).n >= 12:
            n += 1
        prev = m
    return n


def summarise(ratios: pd.Series, invested: pd.Series) -> dict:
    return {
        "n": len(ratios),
        "median": ratios.median(),
        "mean": ratios.mean(),
        "share>1": (ratios > 1).mean(),
        "p10": ratios.quantile(0.10),
        "not_in": (invested < 1).mean(),
    }


def log_try(rows: list[str]) -> None:
    with TRIES.open("a") as fh:
        fh.write("".join(rows))


def run(symbol: str, dividends: bool, first: str, kind_override: str | None) -> list[str]:
    spx = monthly_frame("^GSPC")
    cape = spx["CAPE"]
    cape_med = cape.expanding().median()
    cape_p80 = cape.expanding().quantile(0.80)
    df = monthly_frame(symbol, dividends=dividends)
    df["CAPE"] = cape.reindex(df.index)
    df["CAPE_MED"] = cape_med.reindex(df.index)
    df["HIGH"] = (cape >= cape_p80).reindex(df.index)
    a = frame_arrays(df)
    months = df.index
    last_full = len(df) - 2  # the final row is a partial month
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    tries: list[str] = []
    print(f"\n######## {symbol} (dividends={dividends}), decisions from {first}")
    for h in HORIZONS:
        idx = [i for i in range(len(df)) if months[i] >= pd.Period(first, freq="M")]
        idx = [i for i in idx if i + h <= last_full and not np.isnan(a["CAPE"][i])]
        res = {name: [simulate(a, r, i, h) for i in idx] for name, (r, _) in RULES.items()}
        w = pd.DataFrame({n: [x[0] for x in v] for n, v in res.items()}, index=months[idx])
        inv = pd.DataFrame({n: [x[1] for x in v] for n, v in res.items()}, index=months[idx])
        high = df["HIGH"].iloc[idx].to_numpy(dtype=bool)
        samples = {
            "A": np.ones(len(idx), dtype=bool),
            "B": high,
            "B<1972": high & (months[idx] < SPLIT),
            "B>=1972": high & (months[idx] >= SPLIT),
        }
        print(f"\n=== horizon {h} months; decisions {months[idx[0]]}..{months[idx[-1]]}")
        for sname, mask in samples.items():
            ep = episodes(months[idx][mask])
            print(f"\n-- sample {sname}: {mask.sum()} decision months, {ep} episodes")
            tab = {}
            for name in RULES:
                ratio = (w[name] / w["now"])[mask]
                tab[name] = summarise(ratio, inv[name][mask])
            t = pd.DataFrame(tab).T
            print(t.to_string(float_format=lambda x: f"{x:.3f}"))
            if h == 120 and sname in ("A", "B"):
                for name, (_, kind) in RULES.items():
                    k = kind_override or kind
                    r = tab[name]
                    tries.append(
                        f"| {stamp} | reentry | {name}@{symbol} sample {sname} 10y "
                        f"(R vs now; share>1 {r['share>1']:.2f}, mean {r['mean']:.3f}, "
                        f"{ep} episodes) | {k} | train | {months[idx][mask][0]} | "
                        f"{months[idx][mask][-1]} | n/a | {r['median'] - 1:+.1%} | "
                        f"{r['p10'] - 1:+.1%} | n/a |\n"
                    )
        named = [pd.Period(m, freq="M") for m in NAMED if pd.Period(m, freq="M") in w.index]
        if named:
            print(f"\n-- named months, wealth ratio vs now at {h} months")
            print(
                (w.loc[named].div(w.loc[named, "now"], axis=0)).to_string(
                    float_format=lambda x: f"{x:.2f}"
                )
            )
            print("-- named months, now: terminal wealth multiple")
            print(w.loc[named, "now"].to_string(float_format=lambda x: f"{x:.2f}"))
            entry = {}
            for name, (r, _) in RULES.items():
                col = []
                for m in named:
                    i = months.get_loc(m)
                    ks = [k for k in range(i, min(i + h, len(df))) if r(a, i, k) >= 1.0]
                    col.append(str(months[ks[0]]) if ks else "never")
                entry[name] = col
            print("-- named months, month fully invested")
            print(pd.DataFrame(entry, index=named).to_string())
    return tries


def main() -> None:
    pd.set_option("display.width", 220)
    rows = run("^GSPC", True, "1928-01", None)
    rows += run("^IXIC", False, "1981-02", "robustness")
    log_try(rows)


if __name__ == "__main__":
    main()
