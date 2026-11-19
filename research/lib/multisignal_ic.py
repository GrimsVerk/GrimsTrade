"""Weekly cross-sectional rank IC of value, carry, XS momentum, low-vol and BAB on the six assets
(card: research/cards/multi-signal.md, written before this script and before any number).

    uv run python research/lib/multisignal_ic.py          # prints the tables (logs nothing)
    uv run python research/lib/multisignal_ic.py --log > research/results/multi-signal.md

Descriptive only: no backtest, train bars only (nothing after harness.TRAIN_LAST_BAR is read).
With `--log` each signal (and the `tsmom12` reference) gets one `screen` row per universe in
tries.md (run once). Cached inputs are read as data only (csv / zip / json).
"""

from __future__ import annotations

import csv
import io
import itertools
import math
import sys
import zipfile
from datetime import UTC, date, datetime, timedelta

import harness
import macro
import numpy as np

from grimstrade.data import CRYPTO, UNIVERSE

SIX = ["SPY", "QQQ", "TLT", "GLD", "BTC", "ETH"]
ETFS = ["SPY", "QQQ", "TLT", "GLD"]
FIRST_FRIDAY = date(1994, 2, 4)
LAST_BAR = harness.TRAIN_LAST_BAR
HORIZONS = {"week": 7, "month": 28}
SIGNALS = ["value", "carry", "xsmom", "lowvol", "bab"]
ERAS = [
    ("2000-09", date(2000, 1, 1), date(2009, 12, 31)),
    ("2010-16", date(2010, 1, 1), date(2016, 12, 31)),
    ("2017-21", date(2017, 1, 1), date(2021, 12, 31)),
    ("2022-25", date(2022, 1, 1), date(2025, 12, 31)),
]
N_BOOT = 5000
BLOCK = 13
N_PLACEBO = 2000
SEED = 20261119
FUNDING = {"BTC": "BTCUSDT", "ETH": "ETHUSDT"}
NAN = math.nan


# ---------------------------------------------------------------- data


class Asset:
    def __init__(self, sym: str, adj: list, raw: list) -> None:  # type: ignore[type-arg]
        self.sym = sym
        self.d = np.array([b.date.toordinal() for b in adj])
        self.c = np.array([b.close for b in adj])
        raw_by_day = {b.date.toordinal(): b.close for b in raw}
        self.raw = np.array([raw_by_day.get(int(x), NAN) for x in self.d])
        self.lr = np.concatenate([[NAN], np.diff(np.log(self.c))])
        self.bpy = 365 if UNIVERSE[sym] == CRYPTO else 252

    def idx(self, t: int) -> int:
        """Index of the last bar on or before ordinal day t (-1 if none)."""
        return int(np.searchsorted(self.d, t, side="right")) - 1


def bill_and_ten() -> tuple[macro.Step, macro.Step]:
    out = []
    for series in ("DGS3MO", "DGS10"):
        recs = macro.market_records(series)
        # The value for day x is public on x and used from x + 1.
        out.append(macro.Step([r.obs + timedelta(days=1) for r in recs], [r.value for r in recs]))
    return out[0], out[1]


def funding(sym: str) -> tuple[np.ndarray, np.ndarray]:
    """Binance USDT-M funding: (calc time in ms, annualised rate), train window only."""
    folder = macro.cache_root() / "binance/futures/um/monthly/fundingRate" / FUNDING[sym]
    cut = datetime.combine(LAST_BAR + timedelta(days=1), datetime.min.time(), UTC)
    cut_ms = cut.timestamp() * 1000
    ts, rate = [], []
    for path in sorted(folder.glob("*.zip")):
        with zipfile.ZipFile(path) as z:
            text = z.read(z.namelist()[0]).decode()
        for row in csv.reader(io.StringIO(text)):
            if not row or not row[0].isdigit():
                continue
            t = float(row[0])
            if t >= cut_ms:
                continue
            hours = float(row[1]) if len(row) >= 3 else 8.0
            r = float(row[-1])
            ts.append(t)
            rate.append(r * (24.0 / hours) * 365.0)
    order = np.argsort(ts)
    return np.array(ts)[order], np.array(rate)[order]


# ---------------------------------------------------------------- signals


def sigma(a: Asset, i: int, t: int) -> float:
    lo = a.idx(t - 365)
    x = a.lr[max(lo + 1, 1) : i + 1]
    x = x[np.isfinite(x)]
    return float(x.std(ddof=1) * math.sqrt(a.bpy)) if len(x) >= 120 else NAN


def logret_back(a: Asset, i: int, t: int, days: int) -> float:
    target = t - days
    if a.d[0] > target:
        return NAN
    return float(math.log(a.c[i] / a.c[a.idx(target)]))


class Grid:
    """Closes of every asset on SPY's trading days (for FP's beta)."""

    def __init__(self, assets: dict[str, Asset]) -> None:
        spy = assets["SPY"]
        self.d = spy.d
        self.lr1: dict[str, np.ndarray] = {}
        self.lr3: dict[str, np.ndarray] = {}
        for s, a in assets.items():
            k = np.searchsorted(a.d, self.d, side="right") - 1
            c = np.where(k >= 0, a.c[np.maximum(k, 0)], NAN)
            lc = np.log(c)
            self.lr1[s] = np.concatenate([[NAN], lc[1:] - lc[:-1]])
            self.lr3[s] = np.concatenate([[NAN] * 3, lc[3:] - lc[:-3]])

    def beta(self, s: str, t: int) -> float:
        j = int(np.searchsorted(self.d, t, side="right")) - 1
        if j < 0:
            return NAN
        a1, m1 = self.lr1[s][max(j - 251, 0) : j + 1], self.lr1["SPY"][max(j - 251, 0) : j + 1]
        ok = np.isfinite(a1) & np.isfinite(m1)
        if ok.sum() < 120:
            return NAN
        lo = int(np.searchsorted(self.d, t - int(5 * 365.25), side="right"))
        a3, m3 = self.lr3[s][lo : j + 1], self.lr3["SPY"][lo : j + 1]
        ok3 = np.isfinite(a3) & np.isfinite(m3)
        if ok3.sum() < 750:
            return NAN
        rho = float(np.corrcoef(a3[ok3], m3[ok3])[0, 1])
        return rho * float(a1[ok].std(ddof=1) / m1[ok].std(ddof=1))


def fridays() -> list[date]:
    out, d = [], FIRST_FRIDAY
    while d + timedelta(days=7) <= LAST_BAR:
        out.append(d)
        d += timedelta(days=7)
    return out


def build() -> tuple[list[date], dict[str, np.ndarray]]:
    adj = harness.load_history("train", adjusted=True, syms=SIX)
    raw = harness.load_history("train", adjusted=False, syms=SIX)
    assets = {s: Asset(s, adj[s], raw[s]) for s in SIX}
    grid = Grid(assets)
    bill, ten = bill_and_ten()
    fund = {s: funding(s) for s in FUNDING}
    weeks = fridays()
    shape = (len(weeks), len(SIX))
    keys = SIGNALS + ["tsmom12", "z365", "sigma"]
    keys += [f"y_{h}" for h in HORIZONS] + [f"yr_{h}" for h in HORIZONS]
    M = {k: np.full(shape, NAN) for k in keys}
    for w, day in enumerate(weeks):
        t = day.toordinal()
        b = bill.at(day) / 100  # the value for day x is used from x + 1: at t, Thursday's print
        y10 = ten.at(day) / 100
        for k, s in enumerate(SIX):
            a = assets[s]
            i = a.idx(t)
            if i < 0 or i + 1 < a.bpy:
                continue
            sg = sigma(a, i, t)
            if not math.isfinite(sg):
                continue
            M["sigma"][w, k] = sg
            r365 = logret_back(a, i, t, 365)
            if math.isfinite(r365):
                M["tsmom12"][w, k] = 1.0 if r365 > 0 else 0.0
                M["z365"][w, k] = r365 / sg
            # value: AMP, ln(mean close 5.5y..4.5y ago) - ln(close now)
            lo_day, hi_day = t - int(5.5 * 365.25), t - int(4.5 * 365.25)
            if a.d[0] <= lo_day:
                m = (a.d >= lo_day) & (a.d <= hi_day)
                M["value"][w, k] = (math.log(a.c[m].mean()) - math.log(a.c[i])) / sg
            # carry: Koijen et al., per year above cash, then / sigma
            carry = NAN
            if s in ("SPY", "QQQ") and a.d[0] <= t - 365:
                j = a.idx(t - 365)
                dy = math.log(a.c[i] / a.c[j]) - math.log(a.raw[i] / a.raw[j])
                carry = dy - b
            elif s == "TLT":
                carry = y10 - b
            elif s == "GLD":
                carry = -b
            elif s in FUNDING:
                ts, rate = fund[s]
                end_ms = datetime.combine(day + timedelta(days=1), datetime.min.time(), UTC)
                e = end_ms.timestamp() * 1000
                sel = (ts < e) & (ts >= e - 7 * 86400 * 1000)
                if sel.sum() >= 15:
                    carry = -float(rate[sel].mean())
            if math.isfinite(carry):
                M["carry"][w, k] = carry / sg
            # cross-sectional momentum: AMP MOM2-12
            if a.d[0] <= t - 365:
                c30, c365 = a.c[a.idx(t - 30)], a.c[a.idx(t - 365)]
                M["xsmom"][w, k] = math.log(c30 / c365) / sg
            M["lowvol"][w, k] = -sg
            M["bab"][w, k] = -grid.beta(s, t)
            for h, days in HORIZONS.items():
                if day + timedelta(days=days) > LAST_BAR:
                    continue
                f = a.idx(t + days)
                if a.d[f] <= t:
                    continue
                y = math.log(a.c[f] / a.c[i])
                M[f"y_{h}"][w, k] = y
                M[f"yr_{h}"][w, k] = y / sg
    return weeks, M


# ---------------------------------------------------------------- statistics


def ranks(x: np.ndarray, m: np.ndarray) -> np.ndarray:
    """Average ranks within each row over the valid entries (ties share the mean rank)."""
    xi, xj, mj = x[:, :, None], x[:, None, :], m[:, None, :]
    lt = ((xj < xi) & mj).sum(2)
    eq = ((xj == xi) & mj).sum(2) - 1
    return np.where(m, lt + 0.5 * eq + 1.0, NAN)


def centred(x: np.ndarray, m: np.ndarray) -> np.ndarray:
    n = np.maximum(m.sum(1, keepdims=True), 1)
    mu = np.where(m, x, 0.0).sum(1, keepdims=True) / n
    return np.where(m, x - mu, 0.0)


def row_corr(a: np.ndarray, b: np.ndarray, m: np.ndarray) -> np.ndarray:
    ac, bc = centred(a, m), centred(b, m)
    den = np.sqrt((ac * ac).sum(1) * (bc * bc).sum(1))
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 1e-12, (ac * bc).sum(1) / den, NAN)


def residual(a: np.ndarray, c: np.ndarray, m: np.ndarray) -> np.ndarray:
    """Row-wise OLS residual of a on (1, c) over the valid entries."""
    ac, cc = centred(a, m), centred(c, m)
    ss = (cc * cc).sum(1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        beta = np.where(ss > 1e-12, (ac * cc).sum(1, keepdims=True) / ss, 0.0)
    return np.where(m, ac - beta * cc, NAN)


def weekly_ic(score: np.ndarray, y: np.ndarray, ctrl: np.ndarray | None = None) -> np.ndarray:
    m = np.isfinite(score) & np.isfinite(y)
    if ctrl is not None:
        m &= np.isfinite(ctrl)
    rs, ry = ranks(score, m), ranks(y, m)
    if ctrl is not None:
        rs = residual(rs, ctrl, m)
    ic = row_corr(rs, ry, m)
    return np.where(m.sum(1) >= 3, ic, NAN)


def boot_ci(ic: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float, float]:
    x = ic[np.isfinite(ic)]
    n = len(x)
    if n < 20:
        return NAN, NAN, NAN, NAN
    idx = np.empty((N_BOOT, n), dtype=np.int64)
    idx[:, 0] = rng.integers(0, n, N_BOOT)
    for k in range(1, n):
        jump = rng.random(N_BOOT) < 1.0 / BLOCK
        idx[:, k] = np.where(jump, rng.integers(0, n, N_BOOT), (idx[:, k - 1] + 1) % n)
    means = x[idx].mean(1)
    q = np.percentile(means, [2.5, 97.5, 0.25, 99.75])
    return float(q[0]), float(q[1]), float(q[2]), float(q[3])


def placebo_shuffle(score: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Mean IC when each week's scores are permuted among that week's assets."""
    m = np.isfinite(score) & np.isfinite(y)
    keep = m.sum(1) >= 3
    s, yy, m = score[keep], y[keep], m[keep]
    order = np.argsort(~m, axis=1, kind="stable")  # valid entries first, asset order kept
    s = np.take_along_axis(s, order, 1)
    yy = np.take_along_axis(yy, order, 1)
    m = np.take_along_axis(m, order, 1)
    ry = ranks(yy, m)
    rs = ranks(s, m)
    out = np.empty(N_PLACEBO)
    for d in range(N_PLACEBO):
        key = np.where(m, rng.random(m.shape), 2.0)
        perm = np.argsort(key, axis=1)
        out[d] = np.nanmean(row_corr(np.take_along_axis(rs, perm, 1), ry, m))
    return out


def placebo_relabel(
    score: np.ndarray, y: np.ndarray, ctrl: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Mean IC and partial IC under every non-identity fixed relabelling of the assets."""
    n = score.shape[1]
    ics, parts = [], []
    for p in itertools.permutations(range(n)):
        if p == tuple(range(n)):
            continue
        sp = score[:, list(p)]
        ics.append(np.nanmean(weekly_ic(sp, y)))
        parts.append(np.nanmean(weekly_ic(sp, y, ctrl)))
    return np.array(ics), np.array(parts)


def mean(x: np.ndarray) -> float:
    return float(np.nanmean(x)) if np.isfinite(x).any() else NAN


# ---------------------------------------------------------------- report


def analyse(
    weeks: list[date], M: dict[str, np.ndarray], cols: list[int], rng: np.random.Generator
) -> list[dict[str, object]]:
    sub = {k: v[:, cols] for k, v in M.items()}
    t12, z = sub["tsmom12"], sub["z365"]
    rows = []
    for name in SIGNALS + ["tsmom12", "z365"]:
        s = sub[name]
        r: dict[str, object] = {"name": name}
        for h in HORIZONS:
            y, yr = sub[f"y_{h}"], sub[f"yr_{h}"]
            ic = weekly_ic(s, y)
            r[f"ic_{h}"] = mean(ic)
            r[f"ci_{h}"] = boot_ci(ic, rng)
            r[f"nw_{h}"] = int(np.isfinite(ic).sum())
            r[f"icr_{h}"] = mean(weekly_ic(s, yr))
            if name not in ("tsmom12",):
                part = weekly_ic(s, y, t12)
                r[f"part_{h}"] = mean(part)
                r[f"pci_{h}"] = boot_ci(part, rng)
            if h == "week":
                ok = np.where(np.isfinite(ic))[0]
                r["from"], r["to"] = (weeks[ok[0]], weeks[ok[-1]]) if len(ok) else (None, None)
                valid = np.isfinite(s) & np.isfinite(y)
                r["n_mean"] = float(valid[ok].sum(1).mean()) if len(ok) else NAN
                r["eras"] = [
                    mean(np.where([lo <= wk <= hi for wk in weeks], ic, NAN)) for _, lo, hi in ERAS
                ]
                if name not in ("tsmom12",):
                    r["eras_part"] = [
                        mean(np.where([lo <= wk <= hi for wk in weeks], part, NAN))
                        for _, lo, hi in ERAS
                    ]
                null = placebo_shuffle(s, y, rng)
                r["pA95"] = float(np.percentile(np.abs(null), 95))
                r["pA_p"] = float((np.abs(null) >= abs(float(r["ic_week"]))).mean())  # type: ignore[arg-type]
                ics, parts = placebo_relabel(s, y, t12)
                r["pB_p"] = float((np.abs(ics) >= abs(float(r["ic_week"]))).mean())  # type: ignore[arg-type]
                if name != "tsmom12":
                    pw = float(r["part_week"])  # type: ignore[arg-type]
                    r["pB_part_p"] = float((np.abs(parts) >= abs(pw)).mean())
                r["pB_n"] = len(ics)
        mt = np.isfinite(s) & np.isfinite(t12)
        r["corr_t12"] = mean(
            np.where(mt.sum(1) >= 3, row_corr(ranks(s, mt), ranks(t12, mt), mt), NAN)
        )
        mz = np.isfinite(s) & np.isfinite(z)
        r["corr_z"] = mean(np.where(mz.sum(1) >= 3, row_corr(ranks(s, mz), ranks(z, mz), mz), NAN))
        rows.append(r)
    return rows


def f3(x: object) -> str:
    v = float(x)  # type: ignore[arg-type]
    return f"{v:+.3f}" if math.isfinite(v) else "-"


def ci(x: object, wide: bool = False) -> str:
    q = x  # type: ignore[assignment]
    lo, hi = (q[2], q[3]) if wide else (q[0], q[1])  # type: ignore[index]
    return f"{f3(lo)}..{f3(hi)}"


def verdict(r: dict[str, object], etf: dict[str, object]) -> str:
    if r["name"] in ("tsmom12", "z365"):
        return "reference"
    pw, pm = float(r["part_week"]), float(r["part_month"])  # type: ignore[arg-type]
    q = r["pci_week"]
    checks = {
        "1 partial>0 (99.5%), month same sign": q[2] > 0 and pm > 0,  # type: ignore[index]
        "2 placebos": abs(float(r["ic_week"])) > float(r["pA95"])  # type: ignore[arg-type]
        and float(r["pB_p"]) < 0.05,  # type: ignore[arg-type]
        "3 ETF sign, 3/4 eras": np.sign(float(etf["part_week"])) == np.sign(pw)  # type: ignore[arg-type]
        and sum(1 for e in r["eras_part"] if math.isfinite(e) and np.sign(e) == np.sign(pw)) >= 3,  # type: ignore[attr-defined]
        "4 partial >= 0.10": pw >= 0.10,
    }
    failed = [k.split(" ")[0] for k, ok in checks.items() if not ok]
    return "worth a card" if not failed else "no (fails " + ", ".join(failed) + ")"


def table(title: str, rows: list[dict[str, object]], etf_rows: list[dict[str, object]]) -> None:
    by = {r["name"]: r for r in etf_rows}
    print(f"\n## {title}\n")
    print("Raw-return target. IC = mean weekly Spearman across the assets; 95% stationary block")
    print("bootstrap interval (mean block 13 weeks); partial = beyond the `tsmom12` indicator.\n")
    print(
        "| Signal | Weeks | From | Assets/wk | IC week (95%) | IC month (95%) | Partial week "
        "(95%; 99.5%) | Partial month | Placebo A 95th / p | Placebo B p (partial) | "
        "corr `tsmom12` / `z365` | Verdict |"
    )
    print("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        part_w = (
            f"{f3(r['part_week'])} ({ci(r['pci_week'])}; {ci(r['pci_week'], True)})"
            if "part_week" in r
            else "-"
        )
        part_m = f3(r["part_month"]) if "part_month" in r else "-"
        pb = f"{float(r['pB_p']):.2f}"  # type: ignore[arg-type]
        if "pB_part_p" in r:
            pb += f" ({float(r['pB_part_p']):.2f})"  # type: ignore[arg-type]
        etf = by[r["name"]]
        print(
            f"| `{r['name']}` | {r['nw_week']} | {r['from']} | {float(r['n_mean']):.1f} | "  # type: ignore[arg-type]
            f"{f3(r['ic_week'])} ({ci(r['ci_week'])}) | "
            f"{f3(r['ic_month'])} ({ci(r['ci_month'])}) | "
            f"{part_w} | {part_m} | {float(r['pA95']):.3f} / {float(r['pA_p']):.2f} | {pb} | "  # type: ignore[arg-type]
            f"{f3(r['corr_t12'])} / {f3(r['corr_z'])} | {verdict(r, etf)} |"
        )
    print(
        "\nRisk-adjusted target (return / sigma), IC week / month; and partial IC by era (week):\n"
    )
    print(
        "| Signal | IC week | IC month | "
        + " | ".join(f"IC {e[0]}" for e in ERAS)
        + " | "
        + " | ".join(f"partial {e[0]}" for e in ERAS)
        + " |"
    )
    print("|---|---:|---:|" + "---:|" * (2 * len(ERAS)))
    for r in rows:
        ep = r.get("eras_part", [NAN] * len(ERAS))
        print(
            f"| `{r['name']}` | {f3(r['icr_week'])} | {f3(r['icr_month'])} | "
            + " | ".join(f3(e) for e in r["eras"])
            + " | "  # type: ignore[attr-defined]
            + " | ".join(f3(e) for e in ep)
            + " |"
        )  # type: ignore[attr-defined]


def log_rows(label: str, rows: list[dict[str, object]]) -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    with harness.TRIES.open("a") as f:
        for r in rows:
            if r["name"] == "z365":
                continue
            part = f", partial {f3(r['part_week'])}" if "part_week" in r else ""
            desc = (
                f"{r['name']}{label} (IC wk {f3(r['ic_week'])} [{ci(r['ci_week'])}], "
                f"mo {f3(r['ic_month'])}{part}, placebo B p {float(r['pB_p']):.2f}, "  # type: ignore[arg-type]
                f"corr tsmom12 {f3(r['corr_t12'])})"
            )
            f.write(
                f"| {now} | multi-signal-screen | {desc} | screen | train | {r['from']} | "
                f"{r['to']} | - | - | - | - |\n"
            )


def main(log: bool) -> None:
    rng = np.random.default_rng(SEED)
    weeks, M = build()
    six = analyse(weeks, M, list(range(len(SIX))), rng)
    etf = analyse(weeks, M, [SIX.index(s) for s in ETFS], rng)
    print("# multi-signal: weekly cross-sectional rank IC (train, Fridays 1994-02-04 .. 2025-11)")
    print("\nCard `cards/multi-signal.md`; script `lib/multisignal_ic.py`. Descriptive screen, no")
    print("backtest. Placebo A: scores shuffled among each week's assets (2,000 draws); placebo B:")
    print(
        "every fixed relabelling of the assets (719 for six, 23 for the ETFs). Verdict = the card's"
    )
    print(
        "four-part bar (1 partial IC > 0 at 99.5%; 2 placebos; 3 ETF sign and eras; 4 size 0.10)."
    )
    table("Six assets (SPY, QQQ, TLT, GLD, BTC, ETH)", six, etf)
    table("Four ETFs (SPY, QQQ, TLT, GLD)", etf, etf)
    if log:
        log_rows("", six)
        log_rows("@etf", etf)


if __name__ == "__main__":
    main("--log" in sys.argv)
