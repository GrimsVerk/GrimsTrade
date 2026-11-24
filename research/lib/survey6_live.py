"""survey-6 live check by strategy family (card: research/cards/live-families.md). Descriptive,
nothing selected.

    uv run --with openpyxl python -I research/lib/survey6_live.py <cache_root>

Reads the live fund series written by `survey5_fetch.py` and `survey6_fetch.py`, the Ken French
and AQR factor files and the CBOE index files from the cache (data only), appends one
`live-check` row per family composite to `tries.md` and writes
`research/results/live-families.md`. No month after 2025-10 of any series is read.
"""

from __future__ import annotations

import calendar
import csv
import io
import math
import sys
import zipfile
from collections import defaultdict
from datetime import UTC, date, datetime
from pathlib import Path
from statistics import NormalDist

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness  # noqa: E402
import numpy as np  # noqa: E402
from survey5_live import (  # noqa: E402
    LAST_MONTH,
    Month,
    Series,
    bill_daily,
    bill_monthly,
    corr,
    cut,
    f2,
    months,
    sharpe_m,
    span,
)

IDEA = "survey-6"
MKT = "VFINX"  # the plain market holding for context columns and the 80/20 mix
CASH = "bills"  # matched holding "bills": the excess return over bills is 0

# family -> (members, matched holding per member). Fixed by the card.
FAMILIES: dict[str, dict[str, str]] = {
    "value": {"DFLVX": "VFINX", "DFSVX": "NAESX", "DFIVX": "VGTSX", "VIVAX": "VFINX",
              "IWD": "IWB", "IWN": "IWM", "VTV": "VFINX", "RPV": "VFINX"},
    "momentum": {"PDP": "VTSMX", "MTUM": "VFINX"},
    "quality": {"SPHQ": "VFINX", "QUAL": "VFINX"},
    "low-vol": {"SPLV": "VFINX", "USMV": "VFINX", "ACWV": "ACWI", "EEMV": "EEM"},
    "multi-factor": {"DFEOX": "VTSMX", "DFQTX": "VTSMX", "LRGF": "VFINX", "GSLC": "VFINX"},
    "dividend": {"DVY": "VFINX", "SDY": "VFINX", "VIG": "VFINX", "VYM": "VFINX",
                 "SCHD": "VFINX", "VDIGX": "VFINX"},
    "style-premia (long-short)": {"QSPIX": CASH, "QRPIX": CASH},
    "fx-carry": {"CEW": CASH},
    "merger-arb": {"MERFX": "VBMFX", "ARBFX": "VBMFX", "MNA": "VBMFX"},
    "option-writing": {"GATEX": "VFINX", "PBP": "VFINX", "XYLD": "VFINX", "QYLD": "QQQ"},
    "tail-hedge": {"TAIL": CASH, "VIXY": CASH, "BTAL": CASH, "SWAN": "VBINX"},
    "gold-miners": {"INIVX": "GLD", "FSAGX": "GLD", "VGPMX": "GLD", "GDX": "GLD", "GDXJ": "GLD"},
    "defensive-sectors": {"XLP": "SPY", "XLU": "SPY", "XLV": "SPY", "SECT": "SPY"},
    "trend (survey-5)": {t: CASH for t in ("RYMFX", "AQMIX", "ASFYX", "WTMF", "PQTIX", "ABYIX",
                                           "DBMF", "KMLM", "CTA")},
    "risk-parity (survey-5)": {"ABRZX": "VBINX", "AQRIX": "VBINX", "RPAR": "VBINX"},
}  # fmt: skip
SURVEY5 = {"QRPIX", "RYMFX", "AQMIX", "ASFYX", "WTMF", "PQTIX", "ABYIX", "DBMF", "KMLM", "CTA",
           "ABRZX", "AQRIX", "RPAR"}  # fmt: skip
# Series cut where the fund stopped being the family (survey-6.md, verified changes).
LAST: dict[str, Month] = {"VGPMX": (2018, 8)}  # Global Capital Cycles from 2018-09-26
FIRST: dict[str, Month] = {
    "SPHQ": (2010, 7),  # Value Line Timeliness until 2010-06-30, quality from then
    "VDIGX": (2003, 1),  # a utilities fund until 2002-12-06, dividend growth from then
    "GATEX": (1988, 1),  # index calls and puts "since 1988"; single-stock calls before
}
INDEXES = {"BXM": "VFINX", "PUT": "VFINX"}  # CBOE strategy indexes (no fees), context

CRASHES: dict[str, tuple[Month, Month]] = {
    "2000-04..2002-09": ((2000, 4), (2002, 9)),
    "2007-11..2009-02": ((2007, 11), (2009, 2)),
    "2020-02..03": ((2020, 2), (2020, 3)),
    "2022": ((2022, 1), (2022, 12)),
}

# Paper factors: (source, column, paper sample, publication year, family). Fixed by the card.
PAPERS: dict[str, tuple[str, str, Month, Month, int, str]] = {
    "HML (Fama-French 1993)": ("ff3", "HML", (1963, 7), (1991, 12), 1993, "value"),
    "UMD (Jegadeesh-Titman 1993)": ("mom", "Mom", (1965, 1), (1989, 12), 1993, "momentum"),
    "RMW (Fama-French 2015)": ("ff5", "RMW", (1963, 7), (2013, 12), 2015, "quality"),
    "QMJ US (Asness-Frazzini-Pedersen)": ("qmj", "USA", (1957, 7), (2012, 12), 2019, "quality"),
    "BAB US (Frazzini-Pedersen 2014)": ("bab", "USA", (1926, 1), (2012, 3), 2014, "low-vol"),
    "CMA (Fama-French 2015)": ("ff5", "CMA", (1963, 7), (2013, 12), 2015, "context"),
}  # fmt: skip


def ols(y: np.ndarray, x: np.ndarray) -> tuple[float, float, float, float]:
    """alpha a year, alpha t, beta, information ratio of the residual (a year)."""
    xm = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(xm, y, rcond=None)
    res = y - xm @ coef
    s2 = float(res @ res) / (len(y) - 2)
    cov = s2 * np.linalg.inv(xm.T @ xm)
    a, b = float(coef[0]), float(coef[1])
    t = a / math.sqrt(cov[0, 0])
    ir = a / math.sqrt(s2) * math.sqrt(12) if s2 > 0 else math.nan
    return a * 12, t, b, ir


def max_dd(total: list[float]) -> float:
    eq = np.cumprod(1 + np.array(total))
    return float((1 - eq / np.maximum.accumulate(eq)).max())


# --- data ---


def monthly_from_closes(last: dict[Month, float], rf: Series) -> Series:
    ks = sorted(k for k in last if k <= LAST_MONTH)
    out = {}
    for a, b in zip(ks, ks[1:], strict=False):
        if months(a, b)[1:2] == [b]:  # consecutive months only
            out[b] = last[b] / last[a] - 1 - rf[b]
    return out


def fund(root: Path, t: str, rf: Series) -> Series:
    sub = "survey-5" if t in SURVEY5 else "survey-6"
    last: dict[Month, float] = {}
    with (root / "derived" / sub / f"{t}.csv").open() as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            last[(d.year, d.month)] = float(row["adjclose"])
    s = monthly_from_closes(last, rf)
    return {k: v for k, v in s.items() if FIRST.get(t, (0, 0)) <= k <= LAST.get(t, LAST_MONTH)}


def cboe(root: Path, name: str, rf: Series) -> Series:
    last: dict[Month, float] = {}
    with (root / "downloads" / "survey-6" / "cboe" / f"{name}.csv").open() as f:
        for row in csv.DictReader(f):
            d = datetime.strptime(row["DATE"], "%m/%d/%Y").date()
            if row[name]:
                last[(d.year, d.month)] = float(row[name])
    return monthly_from_closes(last, rf)


def french(root: Path, name: str, col: str) -> Series:
    z = zipfile.ZipFile(root / "downloads" / "survey-6" / "french" / f"{name}.zip")
    text = z.read(z.namelist()[0]).decode("latin-1")
    out: Series = {}
    header: list[str] | None = None
    for row in csv.reader(io.StringIO(text)):
        if not row or not row[0].strip():
            if header is not None and out:
                break  # end of the monthly block (the annual block follows)
            if row and len(row) > 1:
                header = [c.strip() for c in row]
            continue
        k = row[0].strip()
        if header is not None and len(k) == 6 and k.isdigit():
            m = (int(k[:4]), int(k[4:]))
            if m <= LAST_MONTH:
                out[m] = float(row[header.index(col)]) / 100
    return out


def aqr(root: Path, name: str, col: str) -> Series:
    import openpyxl  # only this script needs it: uv run --with openpyxl

    path = root / "downloads" / "survey-6" / "aqr" / f"{name}.xlsx"
    ws = openpyxl.load_workbook(path, read_only=True)[f"{name.upper()} Factors"]
    out: Series = {}
    header = None
    for row in ws.iter_rows(values_only=True):
        if header is None:
            if row and row[0] == "DATE":
                header = list(row)
            continue
        d, v = row[0], row[header.index(col)]
        if isinstance(d, str):
            try:
                d = datetime.strptime(d, "%m/%d/%Y")
            except ValueError:
                continue
        if (
            isinstance(d, datetime)
            and isinstance(v, (int, float))
            and (d.year, d.month) <= LAST_MONTH
        ):
            out[(d.year, d.month)] = float(v)
    return out


# --- measures ---


def row_measures(s: Series, m: Series | None, mkt: Series, rf: Series) -> dict[str, float]:
    """s and m are excess returns; m None means the matched holding is bills."""
    ks = sorted(s if m is None else set(s) & set(m))
    x = np.array([s[k] for k in ks])
    y = np.zeros(len(ks)) if m is None else np.array([m[k] for k in ks])
    sub = {k: s[k] for k in ks}
    sr = sharpe_m(sub)
    srm = 0.0 if m is None else sharpe_m({k: m[k] for k in ks})
    out = {"n": len(ks), "sr": sr, "srm": srm, "gap": sr - srm}
    if m is None:
        t = float(x.mean() / x.std(ddof=1) * math.sqrt(len(x)))
        out.update(alpha=float(x.mean() * 12), t=t, beta=math.nan, ir=sr)
    else:
        a, t, b, ir = ols(x, y)
        out.update(alpha=a, t=t, beta=b, ir=ir)
    out["corr_mkt"] = corr(s, mkt)[0]
    out["dd"] = max_dd([s[k] + rf[k] for k in ks])
    out["dd_m"] = math.nan if m is None else max_dd([m[k] + rf[k] for k in ks])
    # 80% market + 20% this, monthly rebalanced, against the market alone (same months)
    km = [k for k in ks if k in mkt]
    if len(km) > 24:
        mix = {k: 0.8 * mkt[k] + 0.2 * s[k] for k in km}
        alone = {k: mkt[k] for k in km}
        out["mix_dsr"] = sharpe_m(mix) - sharpe_m(alone)
        out["mix_ddd"] = max_dd([mix[k] + rf[k] for k in km]) - max_dd(
            [alone[k] + rf[k] for k in km]
        )
    else:
        out["mix_dsr"] = out["mix_ddd"] = math.nan
    return out


def crash(s: Series, rf: Series, w: tuple[Month, Month]) -> float:
    ks = months(*w)
    if not all(k in s for k in ks):
        return math.nan
    return float(np.prod([1 + s[k] + rf[k] for k in ks]) - 1)


def pct(x: float) -> str:
    return "-" if math.isnan(x) else f"{x:+.1%}"


def reading(fam: str, r: dict[str, float], cash_matched: bool) -> str:
    """The card's reading rules."""
    if cash_matched:
        verdict = ("paid (above bills)" if r["sr"] >= 0.3 and r["t"] >= 2
                   else "did not pay" if r["sr"] < 0.1 else "paid little")  # fmt: skip
    elif r["gap"] >= 0.10 and r["t"] >= 2:
        verdict = "beat its holding"
    elif r["gap"] <= -0.10:
        verdict = "lagged its holding"
    else:
        verdict = "matched its holding (no edge)"
    return verdict


def risk_tool(r: dict[str, float], crash_beats: int) -> bool:
    low_corr = not math.isnan(r["corr_mkt"]) and r["corr_mkt"] <= 0.3
    mix_ok = r["mix_ddd"] <= -0.03 and r["mix_dsr"] >= -0.05
    return bool(low_corr and (crash_beats >= 2 or mix_ok))


def log_rows(rows: list[tuple[str, Series, Series]]) -> None:
    if f"| {IDEA} | value@live-fund | live-check |" in harness.TRIES.read_text():
        return  # logged by the first run; a rerun only rewrites the tables
    lines = []
    for fam, s, rf in rows:
        ks = sorted(s)
        total = [s[k] + rf[k] for k in ks]
        a, b = ks[0], ks[-1]
        lines.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {fam.split(' ')[0]}@live-fund | "
            f"live-check | train | {a[0]}-{a[1]:02d}-01 | "
            f"{b[0]}-{b[1]:02d}-{calendar.monthrange(*b)[1]} | "
            f"{sharpe_m(s):.2f} | {float(np.prod(1 + np.array(total)) - 1):+.1%} | "
            f"{max_dd(total):.1%} | - |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(lines)


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    rf = bill_monthly(bill_daily())
    tick = {t for fam in FAMILIES.values() for t in fam} | {
        h for fam in FAMILIES.values() for h in fam.values() if h != CASH
    }
    ser = {t: fund(root, t, rf) for t in sorted(tick | {MKT})}
    mkt = ser[MKT]
    out = [
        "# live-families: which strategy families paid live, net of fees",
        "",
        "Card: `cards/live-families.md` (committed before any number). Descriptive, nothing "
        "selected, held-out year unread (no month after 2025-10). Monthly returns; Sharpe = "
        "monthly mean / sd x sqrt 12 of the return **above the 13-week T-bill**. Funds: net "
        "asset value with distributions (after fees and real costs). Matched holding: the plain "
        "index fund named per member (`bills` = cash). Composite: equal weight of the members "
        "alive each month, against the equal weight of their matched holdings.",
        "",
        "## 1. Family composites over their live months",
        "",
        "Gap = Sharpe minus the matched holding's Sharpe over the same months. Alpha, t, beta: "
        "OLS of the excess return on the matched holding's (for `bills`: the mean and its t). "
        "IR: alpha over residual sd. Mix: 80% VFINX + 20% the composite, monthly, minus VFINX "
        "alone (Sharpe; max drawdown in points, negative = shallower).",
        "",
        "| Family | Live months | Span | Sharpe | Matched | Gap | Alpha/yr | t | Beta | IR | "
        "Corr VFINX | Max DD | Matched DD | Mix dSharpe | Mix dDD | Reading | Risk tool |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    fam_rows: list[tuple[str, Series, Series]] = []
    comp: dict[str, Series] = {}
    matched: dict[str, Series] = {}
    crash_lines = []
    member_lines = []
    summary: dict[str, dict[str, float]] = {}
    for fam, members in FAMILIES.items():
        cash_matched = all(h == CASH for h in members.values())
        # each month: the members alive whose matched holding also has that month
        pairs: dict[Month, list[tuple[float, float]]] = defaultdict(list)
        for t, h in members.items():
            for k, v in ser[t].items():
                if h == CASH or k in ser[h]:
                    pairs[k].append((v, 0.0 if h == CASH else ser[h][k]))
        s = {k: float(np.mean([p[0] for p in v])) for k, v in sorted(pairs.items())}
        m = (
            None
            if cash_matched
            else {k: float(np.mean([p[1] for p in v])) for k, v in pairs.items()}
        )
        comp[fam] = s
        matched[fam] = m if m is not None else {k: 0.0 for k in s}
        r = row_measures(s, m, mkt, rf)
        beats = 0
        cells = []
        for w in CRASHES.values():
            a, b = crash(s, rf, w), crash(mkt, rf, w)
            cells.append((a, b))
            beats += int(not math.isnan(a) and a - b >= 0.10)
        tool = risk_tool(r, beats)
        verdict = reading(fam, r, cash_matched)
        summary[fam] = {**r, "tool": float(tool)}
        fam_rows.append((fam, s, rf))
        dd_m = "-" if math.isnan(r["dd_m"]) else f"{r['dd_m']:.0%}"
        out.append(
            f"| {fam} | {r['n']} | {span(s)} | {f2(r['sr'])} | {f2(r['srm'])} | {r['gap']:+.2f} | "
            f"{pct(r['alpha'])} | {r['t']:.1f} | {f2(r['beta'])} | {f2(r['ir'])} | "
            f"{f2(r['corr_mkt'])} | {r['dd']:.0%} | "
            f"{dd_m} | {r['mix_dsr']:+.2f} | "
            f"{r['mix_ddd'] * 100:+.0f} | {verdict} | {'yes' if tool else '-'} |"
        )
        crash_lines.append(f"| {fam} | " + " | ".join(f"{pct(a)} ({pct(b)})" for a, b in cells)
                           + " |")  # fmt: skip
        for t, h in members.items():
            mm = None if h == CASH else ser[h]
            rr = row_measures(ser[t], mm, mkt, rf)
            member_lines.append(
                f"| {fam} | {t} | {h} | {span(ser[t])} | {rr['n']} | {f2(rr['sr'])} | "
                f"{f2(rr['srm'])} | {rr['gap']:+.2f} | {pct(rr['alpha'])} | {rr['t']:.1f} | "
                f"{f2(rr['corr_mkt'])} | {rr['dd']:.0%} |"
            )
    n_fam = len(FAMILIES)
    z_b = NormalDist().inv_cdf(1 - 0.05 / n_fam)
    out += [
        "",
        f"Multiple testing: {n_fam} family composites; Bonferroni one-sided 0.05/{n_fam} needs "
        f"t >= {z_b:.2f}. Families at or above it: "
        + (", ".join(f for f, r in summary.items() if r["t"] >= z_b) or "none")
        + ". (Descriptive; not picks. Project-wide bar for a new pick: see the card.)",
        "",
        "## 2. Crash windows (total return; VFINX in brackets)",
        "",
        "| Family | " + " | ".join(CRASHES) + " |",
        "|---|" + "---:|" * len(CRASHES),
        *crash_lines,
        "",
        "## 3. Members",
        "",
        "| Family | Fund | Matched | Span | Months | Sharpe | Matched | Gap | Alpha/yr | t | "
        "Corr VFINX | Max DD |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        *member_lines,
    ]

    # 4. CBOE strategy indexes (no fees)
    out += ["", "## 4. CBOE option-writing indexes (paper: no fees, no costs)", "",
            "| Index | Window | Months | Sharpe | VFINX | Gap | Corr VFINX | Max DD | VFINX DD |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    idx = {n: cboe(root, n, rf) for n in INDEXES}
    for n, s in idx.items():
        for label, w in (
            ("own file", (min(s), LAST_MONTH)),
            ("after 2007-06", ((2007, 7), LAST_MONTH)),
        ):
            sub = cut(s, w)
            r = row_measures(sub, mkt, mkt, rf)
            out.append(f"| {n} | {label} ({span(sub)}) | {r['n']} | {f2(r['sr'])} | "
                       f"{f2(r['srm'])} | {r['gap']:+.2f} | {f2(r['corr_mkt'])} | {r['dd']:.0%} | "
                       f"{r['dd_m']:.0%} |")  # fmt: skip

    # 5. paper factors: in sample, after the sample, after publication, family's live months
    out += [
        "",
        "## 5. Published factors: paper sample against later years and the live funds",
        "",
        "Long-short paper portfolios (no fees, no costs), Sharpe of the excess return. S = the "
        "paper's sample; O = after the sample to 2025-10; Pub = from the January after the "
        "journal year; F = the family composite's live months. Live = the family composite's "
        "IR against its holding (long-only funds: the comparable 'active Sharpe'). Kept = live "
        "/ S; h = 1 - kept.",
        "",
        "| Factor | S | Sharpe S | Sharpe O | Sharpe Pub | Sharpe F | Corr with family's "
        "active return (F) | Live (family IR) | Kept | h |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, (src, col, p0, p1, pub, fam) in PAPERS.items():
        f = french(root, src, col) if src.startswith(("ff", "mom")) else aqr(root, src, col)
        s_s = sharpe_m(cut(f, (p0, p1)))
        win = f"{p0[0]}-{p0[1]:02d}..{p1[0]}-{p1[1]:02d}"
        s_o = sharpe_m(cut(f, (months(p1, (p1[0] + 1, p1[1]))[1], LAST_MONTH)))
        s_p = sharpe_m(cut(f, ((pub + 1, 1), LAST_MONTH)))
        if fam in summary:
            fc, fm = comp[fam], matched[fam]
            s_f = sharpe_m({k: v for k, v in f.items() if k in fc})
            act = {kk: fc[kk] - fm[kk] for kk in fc if kk in fm}
            rc = corr(act, f)[0]
            live = summary[fam]["ir"]
            kept = live / s_s if s_s > 0 else math.nan
            out.append(f"| {name} | {win} | {f2(s_s)} | {f2(s_o)} | "
                       f"{f2(s_p)} | {f2(s_f)} | {f2(rc)} | {f2(live)} | "
                       f"{'-' if math.isnan(kept) else f'{kept:.0%}'} | "
                       f"{'-' if math.isnan(kept) else f'{1 - kept:.0%}'} |")  # fmt: skip
        else:
            out.append(f"| {name} | {win} | {f2(s_s)} | {f2(s_o)} | "
                       f"{f2(s_p)} | - | - | - | - | - |")  # fmt: skip

    text = "\n".join(out) + "\n"
    path = harness.RESEARCH / "results" / "live-families.md"
    path.write_text(text)
    print(text)
    log_rows(fam_rows)


if __name__ == "__main__":
    main()
