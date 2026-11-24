"""Weekly within-class rank IC of multi-signal's five signals on ls-trend-1's 34 ETFs
(card: research/cards/breadth-screen.md, written before this script and before any number).

    uv run python research/lib/breadth_screen.py          # prints the tables (logs nothing)
    uv run python research/lib/breadth_screen.py --log > research/results/breadth-screen.md

Descriptive only: no backtest, train bars only (nothing after harness.TRAIN_LAST_BAR is read).
Signal formulas, IC, bootstrap and placebos are multi-signal's (`multisignal_ic.py`, imported);
what is new is the universe and the ranking within each asset class. With `--log` each primary
signal (and the `tsmom12` reference) gets one `screen` row (run once). The cached CSVs written
by `lstrend1_fetch.py` are read as data only.
"""

from __future__ import annotations

import csv
import math
import sys
from datetime import UTC, date, datetime, timedelta

import harness
import macro
import numpy as np
from multisignal_ic import (
    BLOCK,
    ERAS,
    HORIZONS,
    N_BOOT,
    N_PLACEBO,
    NAN,
    boot_ci,
    ci,
    f3,
    fridays,
    logret_back,
    mean,
    ranks,
    row_corr,
    sigma,
    weekly_ic,
)

CLASSES = {
    "equity": ["SPY", "EWA", "EWG", "EWP", "EWQ", "EWI", "EWJ", "EWN", "EWU"],
    "bonds": ["SHY", "IEI", "IEF", "TLT"],
    "commodities": [
        "GLD", "SLV", "PPLT", "PALL", "CPER", "DBB", "USO", "BNO", "UGA", "UNG",
        "CORN", "WEAT", "SOYB", "CANE", "DBA",
    ],
    "currencies": ["FXE", "FXY", "FXB", "FXA", "FXC", "FXF"],
}  # fmt: skip
SYMS = [s for members in CLASSES.values() for s in members]
COLS = {c: [SYMS.index(s) for s in m] for c, m in CLASSES.items()}
LAST_BAR = harness.TRAIN_LAST_BAR
PRIMARY = ["value", "carry", "xsmom", "lowvol", "bab"]
SECONDARY = ["value_raw", "carry_raw", "xsmom_raw", "bab_cls"]
N_RELABEL = 2000
SEED = 20261119
FAR_EDGE = 0.59  # BAR.md: DSR 0.95 edge over tsmom12 for a far rule at N 1,012


# ---------------------------------------------------------------- data


class Etf:
    def __init__(self, sym: str) -> None:
        path = macro.cache_root() / "derived" / "ls-trend-1" / f"{sym}.csv"
        d, c, raw = [], [], []
        with path.open() as f:
            for row in csv.DictReader(f):
                day = date.fromisoformat(row["date"])
                if day > LAST_BAR:
                    break
                cl, adj = float(row["close"]), float(row["adjclose"])
                if not (cl > 0 and adj > 0):
                    continue
                d.append(day.toordinal())
                c.append(adj)
                raw.append(cl)
        self.sym = sym
        self.d = np.array(d)
        self.c = np.array(c)
        self.raw = np.array(raw)
        self.lr = np.concatenate([[NAN], np.diff(np.log(self.c))])
        self.bpy = 252

    def idx(self, t: int) -> int:
        return int(np.searchsorted(self.d, t, side="right")) - 1


def lagged(series: str) -> macro.Step:
    recs = macro.market_records(series)
    return macro.Step([r.obs + timedelta(days=1) for r in recs], [r.value for r in recs])


class Betas:
    """FP's beta on SPY's trading days: against SPY (card) and against the class's own market."""

    def __init__(self, etfs: dict[str, Etf]) -> None:
        self.d = etfs["SPY"].d
        self.lr1: dict[str, np.ndarray] = {}
        for s, a in etfs.items():
            k = np.searchsorted(a.d, self.d, side="right") - 1
            c = np.where(k >= 0, a.c[np.maximum(k, 0)], NAN)
            lc = np.log(c)
            self.lr1[s] = np.concatenate([[NAN], lc[1:] - lc[:-1]])
        self.mkt1 = {"SPY": self.lr1["SPY"]}
        for cls, members in CLASSES.items():
            stack = np.vstack([self.lr1[s] for s in members])
            ok = np.isfinite(stack)
            n = ok.sum(0)
            with np.errstate(invalid="ignore", divide="ignore"):
                self.mkt1[cls] = np.where(n > 0, np.where(ok, stack, 0.0).sum(0) / n, NAN)

    @staticmethod
    def three(x: np.ndarray) -> np.ndarray:
        return np.concatenate([[NAN] * 2, x[2:] + x[1:-1] + x[:-2]])

    def beta(self, s: str, market: str, t: int) -> float:
        j = int(np.searchsorted(self.d, t, side="right")) - 1
        if j < 0:
            return NAN
        a, m = self.lr1[s], self.mkt1[market]
        a1, m1 = a[max(j - 251, 0) : j + 1], m[max(j - 251, 0) : j + 1]
        ok = np.isfinite(a1) & np.isfinite(m1)
        if ok.sum() < 120:
            return NAN
        lo = int(np.searchsorted(self.d, t - int(5 * 365.25), side="right"))
        a3, m3 = self.three(a)[lo : j + 1], self.three(m)[lo : j + 1]
        ok3 = np.isfinite(a3) & np.isfinite(m3)
        if ok3.sum() < 750:
            return NAN
        rho = float(np.corrcoef(a3[ok3], m3[ok3])[0, 1])
        return rho * float(a1[ok].std(ddof=1) / m1[ok].std(ddof=1))


def build() -> tuple[list[date], dict[str, np.ndarray]]:
    etfs = {s: Etf(s) for s in SYMS}
    betas = Betas(etfs)
    bill, two, ten = lagged("DGS3MO"), lagged("DGS2"), lagged("DGS10")
    cls_of = {s: c for c, m in CLASSES.items() for s in m}
    weeks = fridays()
    shape = (len(weeks), len(SYMS))
    keys = PRIMARY + SECONDARY + ["tsmom12", "z365", "sigma"]
    keys += [f"y_{h}" for h in HORIZONS] + [f"yr_{h}" for h in HORIZONS]
    M = {k: np.full(shape, NAN) for k in keys}
    for w, day in enumerate(weeks):
        t = day.toordinal()
        b, y2, y10 = bill.at(day) / 100, two.at(day) / 100, ten.at(day) / 100
        bond_yield = {"SHY": y2, "IEI": y2 + 3 / 8 * (y10 - y2), "IEF": y10, "TLT": y10}
        for k, s in enumerate(SYMS):
            a, cls = etfs[s], cls_of[s]
            i = a.idx(t)
            if i < 0 or i + 1 < a.bpy:
                continue
            sg = sigma(a, i, t)  # type: ignore[arg-type]
            if not math.isfinite(sg):
                continue
            M["sigma"][w, k] = sg
            r365 = logret_back(a, i, t, 365)  # type: ignore[arg-type]
            if math.isfinite(r365):
                M["tsmom12"][w, k] = 1.0 if r365 > 0 else 0.0
                M["z365"][w, k] = r365 / sg
            lo_day, hi_day = t - int(5.5 * 365.25), t - int(4.5 * 365.25)
            if a.d[0] <= lo_day:
                m = (a.d >= lo_day) & (a.d <= hi_day)
                v = math.log(a.c[m].mean()) - math.log(a.c[i])
                M["value_raw"][w, k], M["value"][w, k] = v, v / sg
            carry = NAN
            if cls in ("equity", "currencies") and a.d[0] <= t - 365:
                j = a.idx(t - 365)
                dy = math.log(a.c[i] / a.c[j]) - math.log(a.raw[i] / a.raw[j])
                carry = dy - b
            elif cls == "bonds":
                carry = bond_yield[s] - b
            if math.isfinite(carry):
                M["carry_raw"][w, k], M["carry"][w, k] = carry, carry / sg
            if a.d[0] <= t - 365:
                mom = math.log(a.c[a.idx(t - 30)] / a.c[a.idx(t - 365)])
                M["xsmom_raw"][w, k], M["xsmom"][w, k] = mom, mom / sg
            M["lowvol"][w, k] = -sg
            M["bab"][w, k] = -betas.beta(s, "SPY", t)
            M["bab_cls"][w, k] = -betas.beta(s, cls, t)
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


# ---------------------------------------------------------------- within-class statistics


def class_ics(s: np.ndarray, y: np.ndarray, ctrl: np.ndarray | None = None) -> np.ndarray:
    """Weekly IC per class (weeks x classes); NaN where a class has fewer than 3 ETFs."""
    out = []
    for cols in COLS.values():
        out.append(weekly_ic(s[:, cols], y[:, cols], None if ctrl is None else ctrl[:, cols]))
    return np.column_stack(out)


def combine(per_class: np.ndarray) -> np.ndarray:
    ok = np.isfinite(per_class)
    n = ok.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, np.where(ok, per_class, 0.0).sum(1) / np.maximum(n, 1), NAN)


def wic(s: np.ndarray, y: np.ndarray, ctrl: np.ndarray | None = None) -> np.ndarray:
    return combine(class_ics(s, y, ctrl))


def placebo_shuffle(s: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Mean IC when each week's scores are permuted among that week's ETFs within each class."""
    prepared = []
    for cols in COLS.values():
        sc, yc = s[:, cols], y[:, cols]
        m = np.isfinite(sc) & np.isfinite(yc)
        order = np.argsort(~m, axis=1, kind="stable")
        sc = np.take_along_axis(sc, order, 1)
        yc = np.take_along_axis(yc, order, 1)
        m = np.take_along_axis(m, order, 1)
        prepared.append((ranks(sc, m), ranks(yc, m), m, m.sum(1) >= 3))
    out = np.empty(N_PLACEBO)
    for d in range(N_PLACEBO):
        per = []
        for rs, ry, m, keep in prepared:
            key = np.where(m, rng.random(m.shape), 2.0)
            perm = np.argsort(key, axis=1)
            ic = row_corr(np.take_along_axis(rs, perm, 1), ry, m)
            per.append(np.where(keep, ic, NAN))
        out[d] = mean(combine(np.column_stack(per)))
    return out


def placebo_relabel(
    s: np.ndarray, y: np.ndarray, ctrl: np.ndarray, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Mean IC and partial IC under random fixed relabellings within each class."""
    ics, parts = np.empty(N_RELABEL), np.empty(N_RELABEL)
    for d in range(N_RELABEL):
        perm = np.arange(len(SYMS))
        for cols in COLS.values():
            perm[cols] = rng.permutation(cols)
        sp = s[:, perm]
        ics[d] = mean(wic(sp, y))
        parts[d] = mean(wic(sp, y, ctrl))
    return ics, parts


def icir(x: np.ndarray) -> float:
    v = x[np.isfinite(x)]
    return float(v.mean() / v.std(ddof=1) * math.sqrt(52)) if len(v) > 20 else NAN


def era_means(weeks: list[date], x: np.ndarray) -> list[float]:
    return [mean(np.where([lo <= wk <= hi for wk in weeks], x, NAN)) for _, lo, hi in ERAS]


def analyse(
    weeks: list[date], M: dict[str, np.ndarray], name: str, rng: np.random.Generator, full: bool
) -> dict[str, object]:
    s, t12, z = M[name], M["tsmom12"], M["z365"]
    r: dict[str, object] = {"name": name}
    partial = name != "tsmom12"
    for h in HORIZONS:
        y, yr = M[f"y_{h}"], M[f"yr_{h}"]
        ic = wic(s, y)
        r[f"ic_{h}"], r[f"ci_{h}"] = mean(ic), boot_ci(ic, rng)
        r[f"icr_{h}"] = mean(wic(s, yr))
        r[f"pool_{h}"] = mean(weekly_ic(s, y))
        if partial:
            pc = class_ics(s, y, t12)
            part = combine(pc)
            r[f"part_{h}"], r[f"pci_{h}"] = mean(part), boot_ci(part, rng)
        if h != "week":
            continue
        ok = np.where(np.isfinite(ic))[0]
        r["nw"] = len(ok)
        r["from"], r["to"] = (weeks[ok[0]], weeks[ok[-1]]) if len(ok) else (None, None)
        valid = np.isfinite(s) & np.isfinite(y)
        r["n_mean"] = float(valid[ok].sum(1).mean()) if len(ok) else NAN
        r["ncls"] = float(np.isfinite(class_ics(s, y))[ok].sum(1).mean()) if len(ok) else NAN
        r["eras"] = era_means(weeks, ic)
        r["cls"] = [mean(c) for c in class_ics(s, y).T]
        r["icir"] = icir(ic)
        if partial:
            r["eras_part"] = era_means(weeks, part)
            r["cls_part"] = [mean(c) for c in pc.T]
            r["icir_part"] = icir(part)
        if full:
            null = placebo_shuffle(s, y, rng)
            r["pA95"] = float(np.percentile(np.abs(null), 95))
            r["pA_p"] = float((np.abs(null) >= abs(float(r["ic_week"]))).mean())  # type: ignore[arg-type]
            ics, parts = placebo_relabel(s, y, t12, rng)
            r["pB_p"] = float((np.abs(ics) >= abs(float(r["ic_week"]))).mean())  # type: ignore[arg-type]
            if partial:
                r["pB_part_p"] = float((np.abs(parts) >= abs(float(r["part_week"]))).mean())  # type: ignore[arg-type]
    pt, pz = [], []
    for cols in COLS.values():
        sc, tc, zc = s[:, cols], t12[:, cols], z[:, cols]
        mt = np.isfinite(sc) & np.isfinite(tc)
        pt.append(np.where(mt.sum(1) >= 3, row_corr(ranks(sc, mt), ranks(tc, mt), mt), NAN))
        mz = np.isfinite(sc) & np.isfinite(zc)
        pz.append(np.where(mz.sum(1) >= 3, row_corr(ranks(sc, mz), ranks(zc, mz), mz), NAN))
    r["corr_t12"] = mean(combine(np.column_stack(pt)))
    r["corr_z"] = mean(combine(np.column_stack(pz)))
    return r


# ---------------------------------------------------------------- report


def sign_back(r: dict[str, object]) -> str:
    q = r["ci_week"]
    if q[0] > 0:  # type: ignore[index]
        return "yes"
    if q[1] < 0:  # type: ignore[index]
        return "no, reversed"
    return "positive, not distinct from 0" if float(r["ic_week"]) > 0 else "no (inside 0)"  # type: ignore[arg-type]


def verdict(r: dict[str, object]) -> str:
    pw, pm = float(r["part_week"]), float(r["part_month"])  # type: ignore[arg-type]
    q = r["pci_week"]
    eras = [e for e in r["eras_part"] if math.isfinite(e)]  # type: ignore[attr-defined]
    cls = [c for c in r["cls_part"] if math.isfinite(c)]  # type: ignore[attr-defined]
    checks = {
        "1": q[2] > 0 and pm > 0,  # type: ignore[index]
        "2": abs(float(r["ic_week"])) > float(r["pA95"]) and float(r["pB_p"]) < 0.05,  # type: ignore[arg-type]
        "3": sum(np.sign(e) == np.sign(pw) for e in eras) >= 3
        and 2 * sum(np.sign(c) == np.sign(pw) for c in cls) >= len(cls),
        "4a": pw >= 0.10,
        "4b": float(r["icir_part"]) >= FAR_EDGE,  # type: ignore[arg-type]
    }
    failed = [k for k, ok in checks.items() if not ok]
    if not failed:
        return "worth a card"
    if failed == ["4a"]:
        return "worth a card (wide-book size only)"
    return "no (fails " + ", ".join(failed) + ")"


def main(log: bool) -> None:
    rng = np.random.default_rng(SEED)
    weeks, M = build()
    prim = [analyse(weeks, M, n, rng, True) for n in PRIMARY + ["tsmom12", "z365"]]
    sec = [analyse(weeks, M, n, rng, False) for n in SECONDARY]
    print("# breadth-screen: weekly within-class rank IC, 34 ETFs (train, Fridays to 2025-11)")
    print("\nCard `cards/breadth-screen.md`; script `lib/breadth_screen.py` (signals, IC and")
    print("bootstrap from `lib/multisignal_ic.py`). Descriptive screen, no backtest. Weekly IC =")
    print("mean over the classes with >= 3 ETFs that week of the within-class Spearman IC.")
    print(f"Bootstrap: stationary, mean block {BLOCK} weeks, {N_BOOT} draws. Placebo A: scores")
    print(f"shuffled within class each week ({N_PLACEBO} draws); placebo B: {N_RELABEL} random")
    print("fixed relabels within class. Bar: 1 partial > 0 at 99.5% and month same sign;")
    print("2 placebos; 3 eras 3/4 and half the classes; 4a partial >= 0.10; 4b partial IC-IR")
    print(f"(mean / sd x sqrt 52) >= {FAR_EDGE} (BAR.md far-rule edge at N 1,012).")
    print("\n## Primary (raw next-week / next-month log return)\n")
    print(
        "| Signal | Weeks | From | ETFs/wk | Classes/wk | IC week (95%) | IC month (95%) | "
        "Partial week (95%; 99.5%) | Partial month | IC-IR / partial IC-IR | "
        "Placebo A 95th / p | Placebo B p (partial) | corr `tsmom12` / `z365` | "
        "Sign back? | Verdict |"
    )
    print("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for r in prim:
        pw = (
            f"{f3(r['part_week'])} ({ci(r['pci_week'])}; {ci(r['pci_week'], True)})"
            if "part_week" in r
            else "-"
        )
        pm = f3(r["part_month"]) if "part_month" in r else "-"
        ir = f"{float(r['icir']):+.2f}"  # type: ignore[arg-type]
        ir += f" / {float(r['icir_part']):+.2f}" if "icir_part" in r else ""  # type: ignore[arg-type]
        pb = f"{float(r['pB_p']):.2f}"  # type: ignore[arg-type]
        pb += f" ({float(r['pB_part_p']):.2f})" if "pB_part_p" in r else ""  # type: ignore[arg-type]
        ref = r["name"] in ("tsmom12", "z365")
        print(
            f"| `{r['name']}` | {r['nw']} | {r['from']} | {float(r['n_mean']):.1f} | "  # type: ignore[arg-type]
            f"{float(r['ncls']):.1f} | {f3(r['ic_week'])} ({ci(r['ci_week'])}) | "  # type: ignore[arg-type]
            f"{f3(r['ic_month'])} ({ci(r['ci_month'])}) | {pw} | {pm} | {ir} | "
            f"{float(r['pA95']):.3f} / {float(r['pA_p']):.2f} | {pb} | "  # type: ignore[arg-type]
            f"{f3(r['corr_t12'])} / {f3(r['corr_z'])} | "
            f"{'-' if ref else sign_back(r)} | {'reference' if ref else verdict(r)} |"
        )
    print("\n## By era and by class (raw weekly target)\n")
    names = list(CLASSES)
    print(
        "| Signal | IC risk-adj. week / month | pooled IC (no classes) week / month | "
        + " | ".join(f"IC {e[0]}" for e in ERAS)
        + " | "
        + " | ".join(f"partial {e[0]}" for e in ERAS)
        + " | "
        + " | ".join(f"IC {c}" for c in names)
        + " | "
        + " | ".join(f"partial {c}" for c in names)
        + " |"
    )
    print("|---|---:|---:|" + "---:|" * (2 * len(ERAS) + 2 * len(names)))
    for r in prim + sec:
        ep = r.get("eras_part", [NAN] * len(ERAS))
        cp = r.get("cls_part", [NAN] * len(names))
        print(
            f"| `{r['name']}` | {f3(r['icr_week'])} / {f3(r['icr_month'])} | "
            f"{f3(r['pool_week'])} / {f3(r['pool_month'])} | "
            + " | ".join(f3(e) for e in r["eras"])  # type: ignore[attr-defined]
            + " | "
            + " | ".join(f3(e) for e in ep)  # type: ignore[attr-defined]
            + " | "
            + " | ".join(f3(c) for c in r["cls"])  # type: ignore[attr-defined]
            + " | "
            + " | ".join(f3(c) for c in cp)  # type: ignore[attr-defined]
            + " |"
        )
    print("\n## Secondary (descriptive, not in the bar)\n")
    print("`*_raw`: no `/ sigma` (the papers' raw within-class ranks); `bab_cls`: beta against")
    print("the class's own equal-weight market (FP's construction).\n")
    print(
        "| Signal | Weeks | IC week (95%) | IC month (95%) | Partial week (95%) | "
        "Partial month | IC-IR / partial IC-IR | corr `tsmom12` / `z365` |"
    )
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in sec:
        print(
            f"| `{r['name']}` | {r['nw']} | {f3(r['ic_week'])} ({ci(r['ci_week'])}) | "
            f"{f3(r['ic_month'])} ({ci(r['ci_month'])}) | "
            f"{f3(r['part_week'])} ({ci(r['pci_week'])}) | {f3(r['part_month'])} | "
            f"{float(r['icir']):+.2f} / {float(r['icir_part']):+.2f} | "  # type: ignore[arg-type]
            f"{f3(r['corr_t12'])} / {f3(r['corr_z'])} |"
        )
    if log:
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
        with harness.TRIES.open("a") as f:
            for r in prim:
                if r["name"] == "z365":
                    continue
                part = f", partial {f3(r['part_week'])}" if "part_week" in r else ""
                desc = (
                    f"{r['name']}@wide34 (within-class IC wk {f3(r['ic_week'])} "
                    f"[{ci(r['ci_week'])}], mo {f3(r['ic_month'])}{part}, "
                    f"placebo B p {float(r['pB_p']):.2f}, corr tsmom12 {f3(r['corr_t12'])})"  # type: ignore[arg-type]
                )
                f.write(
                    f"| {now} | breadth-screen | {desc} | screen | train | {r['from']} | "
                    f"{r['to']} | - | - | - | - |\n"
                )


if __name__ == "__main__":
    main("--log" in sys.argv)
