"""Lane gate-null-2, Part 3 (research/cards/gate-null-2.md): descriptive re-score of gates
W20-W28 under two surrogate placebo families (F2 phase, F3 IAAFT; 40 each, seed 2). No new
verdict, no strategy, no backtest.

Each gate is rebuilt through its own code: W20-W24 run the gate's own `main()` with the dose
builder patched to hand back a surrogate dose (its result file redirected to a temp folder, the
gate's rank function patched to record the true t and its placebo t); W25-W28 call the gate's
module-level `Panel.fit` / `Design.fit` directly. The true t must match the stored value to
0.02, else the gate is written as not reproduced.

Bars: the gates read `research/data/` of the lane that ran them (gitignored, not in this
worktree). Point `GATENULL2_DATA` at such a folder (it must hold `bars/`, and `adj/` where the
gate had it): W20, W21 ran on lane wide-10's folder (it also holds `nyfed/` and
`stablecoins/`), W22 on wide-11's, W23, W24 on wide-12's, W25, W26 on wide-13's (bars only,
no `adj/`), W27, W28 on wide-15's. Doses come from the shared cache (`macro.local.json`).

Run (one gate per process):
  `GATENULL2_DATA=<lane>/research/data uv run --with xlrd python -I \
     research/lib/gatenull2_rescore_a.py W25`
Output: research/results/gate-null-2-rescore/<gate>.json
"""

from __future__ import annotations

import contextlib
import io
import json
import math
import os
import sys
import tempfile
from collections.abc import Callable, Iterator, Mapping
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gatenull2 as g  # noqa: E402
import harness  # noqa: E402

OUTDIR = Path(__file__).resolve().parents[1] / "results" / "gate-null-2-rescore"
TMP = Path(tempfile.mkdtemp(prefix="gatenull2-a-"))
M = 40
FAMS = ("phase", "iaaft")

# Stored gate values (research/results/<gate>.md; research/gate-null.md tables).
STORED: dict[str, tuple[str, float, int]] = {
    "W20": ("fed-purchase-flow", 0.37, 11),
    "W21": ("stablecoin-mint", 1.06, 17),
    "W22": ("hedging-pressure", 0.49, 14),
    "W23": ("custody-selling", -1.20, 34),
    "W24": ("inflation-disagreement", -0.75, 36),
    "W25": ("act-haven", -1.02, 21),
    "W26": ("failure-premium", -0.48, 21),
    "W27": ("congress-workload", -0.19, 25),
    "W28": ("refund-runoff", 1.44, 7),
}


def use_data() -> None:
    """Point harness at the lane's research/data folder and memoise price loading."""
    d = os.environ.get("GATENULL2_DATA")
    if not d:
        raise SystemExit("set GATENULL2_DATA to a research/data folder (see the docstring)")
    p = Path(d).expanduser().resolve()
    harness.DATA = p
    harness.RESEARCH = p.parent
    orig = harness.load_history
    memo: dict[tuple[Any, ...], Any] = {}

    def load(period: str = "train", adjusted: bool = True, syms: Any = harness.SYMS) -> Any:
        key = (period, adjusted, tuple(syms))
        if key not in memo:
            memo[key] = orig(period, adjusted, syms)
        return memo[key]

    harness.load_history = load  # type: ignore[assignment]


@contextlib.contextmanager
def patched(obj: Any, attr: str, value: Any) -> Iterator[None]:
    old = getattr(obj, attr)
    setattr(obj, attr, value)
    try:
        yield
    finally:
        setattr(obj, attr, old)


_SURR: dict[tuple[Any, ...], list[dict[Any, float]]] = {}


def surrogate(d: Mapping[Any, float], fam: str, j: int) -> dict[Any, float]:
    """Surrogate j of family `fam` of the dose dict d (finite values only; NaN keys kept NaN).
    Built once per (family, series)."""
    fin = {k: float(v) for k, v in d.items() if v == v}
    key = (fam, min(fin), max(fin), len(fin), round(sum(fin.values()), 9))
    if key not in _SURR:
        _SURR[key] = g.surrogate_doses(fin, fam, M)
    out = dict(_SURR[key][j])
    out.update({k: math.nan for k, v in d.items() if v != v})
    return out


class Grab:
    """Stands in for a gate's rank function; records (true t, placebo t) of each call."""

    def __init__(self, orig: Callable[..., int]):
        self.orig = orig
        self.calls: list[tuple[float, list[float]]] = []

    def __call__(self, true: float, others: Any) -> int:
        self.calls.append((float(true), [float(o) for o in others]))
        return self.orig(true, others)


def run_main(
    mod: Any, rank_owner: Any, patches: list[tuple[Any, str, Any]]
) -> tuple[float, list[float]]:
    """Run mod.main() with patches, output to a temp file; (true t, placebo t) of its gate."""
    grab = Grab(rank_owner.rank_highest)
    with contextlib.ExitStack() as st:
        st.enter_context(patched(rank_owner, "rank_highest", grab))
        st.enter_context(patched(mod, "OUT", TMP / "out.md"))
        for obj, attr, val in patches:
            st.enter_context(patched(obj, attr, val))
        st.enter_context(contextlib.redirect_stdout(io.StringIO()))
        mod.main()
    return grab.calls[0]


def via_main(
    mod: Any,
    rank_owner: Any,
    shifts_owner: Any,
    shifts_attr: str,
    builder_owner: Any,
    builder_attr: str,
    make_builder: Callable[[Callable[..., Any], str, int], Callable[..., Any]],
) -> tuple[float, list[float], dict[str, list[float]]]:
    """True t and shift placebos from one plain run; then one run per surrogate with the dose
    builder swapped (placebo list cut to one shift: only the true fit is used)."""
    t, shift_t = run_main(mod, rank_owner, [])
    one = [getattr(shifts_owner, shifts_attr)[0]]
    orig = getattr(builder_owner, builder_attr)
    sur: dict[str, list[float]] = {}
    for fam in FAMS:
        sur[fam] = []
        for j in range(M):
            b = make_builder(orig, fam, j)
            tj, _ = run_main(
                mod,
                rank_owner,
                [(shifts_owner, shifts_attr, one), (builder_owner, builder_attr, b)],
            )
            sur[fam].append(tj)
    return t, shift_t, sur


def dict_builder(orig: Callable[..., Any], fam: str, j: int) -> Callable[..., Any]:
    """A dose builder returning a surrogate of the dict the original returns."""

    def f(*a: Any, **kw: Any) -> Any:
        return surrogate(orig(*a, **kw), fam, j)

    return f


# ---------------------------------------------------------------- W20-W24 (via main)


def w20() -> dict[str, Any]:
    import wide10_fedflow as mod

    ev = mod.ev

    def make(orig: Callable[..., Any], fam: str, j: int) -> Callable[..., Any]:
        calls = [0]

        def f(days: Any, par: Any) -> np.ndarray:
            x = orig(days, par)
            calls[0] += 1
            if calls[0] > 1:  # only the gate's TLT dose; shown cells keep theirs
                return x
            s = surrogate(dict(enumerate(x.tolist())), fam, j)
            return np.array([s[i] for i in range(len(x))])

        return f

    t, sh, sur = via_main(mod, ev, ev, "SHIFTS_W20", ev, "dose_series", make)
    tlt = mod.Series("TLT")
    x = ev.dose_series(tlt.days, ev.daily_par(mod.operations(), 20, None))
    return record(
        "W20", t, sh, sur, x.tolist(),
        "x = ln(1 + 20y+ par bought) on every TLT train day (zeros kept); surrogates of the"
        " whole daily series, gate rows 2014-2025; HC1 t",
    )  # fmt: skip


def w21() -> dict[str, Any]:
    import wide10_mint as mod

    ev = mod.ev
    supply = ev.parse_supply(json.loads(mod.FILE.read_text()), harness.TRAIN_LAST_BAR)
    fr = ev.fridays(min(supply), max(supply))
    dose = {f: ev.issuance(supply, f)[0] for f in fr}
    dose = {f: v for f, v in dose.items() if v == v}
    orig = ev.issuance

    def make(_o: Callable[..., Any], fam: str, j: int) -> Callable[..., Any]:
        s = surrogate(dose, fam, j)

        def f(sup: Any, friday: date) -> tuple[float, str]:
            v, why = orig(sup, friday)
            return (s.get(friday, math.nan), why) if v == v else (v, why)

        return f

    t, sh, sur = via_main(mod, ev, ev, "SHIFTS_W21", ev, "issuance", make)
    return record(
        "W21", t, sh, sur, [dose[f] for f in sorted(dose)],
        "m = weekly log change of stablecoin supply on every Friday it passes the guards"
        " (full DefiLlama span); surrogate values on the same Fridays; control kept",
    )  # fmt: skip


def w22() -> dict[str, Any]:
    import wide11_hp as mod

    ev = mod.ev
    orig_rz = ev.read_zips
    memo: dict[str, Any] = {}

    def rz(paths: Any, codes: Any, last: date) -> Any:
        if "x" not in memo:
            memo["x"] = orig_rz(paths, codes, last)
        return memo["x"]

    with patched(ev, "read_zips", rz):
        t, sh, sur = via_main(mod, ev, ev, "SHIFTS_W22", ev, "zscores", dict_builder)
        hp = rz(None, None, mod.LAST)
    z = {a: ev.zscores(hp[a]) for a in mod.GATE_ASSETS}
    acfs = ", ".join(f"{a} {g.acf1(np.array([z[a][d] for d in sorted(z[a])])):.2f}" for a in z)
    a0 = mod.GATE_ASSETS[0]
    return record(
        "W22", t, sh, sur, [z[a0][d] for d in sorted(z[a0])],
        f"surrogate of each market's final z dict (156-week z of hedging pressure), same seed;"
        f" dose stats below are {a0}'s z; lag-1 acf by market: {acfs}",
    )  # fmt: skip


def w23() -> dict[str, Any]:
    import wide12_custody as mod

    w11 = mod.w11
    t, sh, sur = via_main(mod, w11, w11, "SHIFTS_W22", w11, "zscores", dict_builder)
    h = mod.ev.read_h41(
        mod.macro.cache_root() / "fed-ddp" / "h41-2026-11-19" / "H41.zip", mod.ev.SERIES, mod.LAST
    )
    z = w11.zscores(mod.ev.flows(h))
    return record(
        "W23", t, sh, sur, [z[d] for d in sorted(z)],
        "surrogate of the final z dict (4-week custody flow against its 156 weeks)",
    )  # fmt: skip


def w24() -> dict[str, Any]:
    import wide12_spf as mod

    ev = mod.ev
    t, sh, sur = via_main(mod, mod.w11, ev, "SHIFTS_W24", ev, "zscores_q", dict_builder)
    book = mod.macro.cache_root() / "philly-spf" / "2026-11-19" / "Dispersion_1.xlsx"
    d10 = ev.quarter_column(ev.read_xlsx_sheet(book, "CPI10"), "CPI10_D1")
    d10 = {q: v for q, v in d10.items() if ev.entry_target(q) <= mod.LAST}
    z = ev.zscores_q(d10)
    return record(
        "W24", t, sh, sur, [z[q] for q in sorted(z)],
        "surrogate of the final quarterly z dict (SPF 10-year CPI dispersion against 40 surveys);"
        " short series",
    )  # fmt: skip


# ---------------------------------------------------------------- W25-W28 (direct fit)


def w25() -> dict[str, Any]:
    import wide13 as mod

    ev, e11, dw = mod.ev, mod.e11, mod.dw
    hist = harness.load_history("train", syms=["GLD", "TLT"])
    px = {a: ev.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    rows = [r for r in dw.read_gpr_xls(dw.snapshot("gpr") / "data_gpr_daily_recent.xls")]
    rows = [r for r in rows if r.day <= mod.LAST]
    ends = ev.mondays(date(1985, 1, 7), mod.LAST)
    za = e11.zscores(ev.weekly_log_mean({r.day: r.act for r in rows}, ends))
    dates = ev.mondays(date(2005, 1, 3), date(2025, 10, 6))
    p = mod.Panel(px, date(2000, 1, 3), 9, 37)

    def fit(src: Mapping[date, float], k: int = 0) -> float:
        return p.fit(["GLD", "TLT"], dates, lambda d: ev.shifted(src, d, k), controls=False)[1]

    return direct("W25", za, fit, ev.SHIFTS, "surrogate of the acts z dict (Mondays from 1988)")


def w26() -> dict[str, Any]:
    import wide13 as mod

    ev, dw = mod.ev, mod.dw
    hist = harness.load_history("train", syms=["XLF"])
    px = {a: ev.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    fs = dw.parse_fdic_failures((dw.snapshot("fdic") / "failures.json").read_text())
    fs = [f for f in fs if f.kind in ("FAILURE", "ASSISTANCE")]
    x = ev.failure_dose(
        ((f.day, f.assets_k) for f in fs), ev.fridays(date(1990, 1, 5), mod.LAST), mod.LAST
    )
    dates = ev.fridays(date(2000, 1, 7), date(2025, 10, 3))
    p = mod.Panel(px, date(2000, 1, 7), 3, 31)

    def fit(src: Mapping[date, float], k: int = 0) -> float:
        return p.fit(["XLF"], dates, lambda d: ev.shifted(src, d, k), controls=True)[1]

    return direct(
        "W26", x, fit, ev.SHIFTS,
        "surrogate of the weekly failure dose ln(1 + assets) from 1990 (mostly zeros: phase"
        " surrogates are Gaussian, IAAFT keeps the zeros and spikes); controls kept",
    )  # fmt: skip


def w27() -> dict[str, Any]:
    import wide15 as mod

    ev, e13 = mod.ev, mod.e13
    hist = harness.load_history("train", syms=["SPY"])
    px = {a: e13.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    weeks = e13.fridays(date(1960, 1, 1), mod.LAST)
    dose = ev.workload_dose(ev.weekly_counts(mod.load_rollcalls(), weeks))
    dates = e13.fridays(date(1994, 2, 4), date(2025, 10, 3))
    d = mod.Design(px, date(1994, 2, 4), 3, 31)
    sess = {f: v[0] for f, v in dose.items() if v[1] > 0}

    def fit_pair(src: Mapping[date, tuple[float, float]], k: int = 0) -> float:
        doses = [lambda t: ev.shifted_pair(src, t, k)[0], lambda t: ev.shifted_pair(src, t, k)[1]]
        return d.fit(["SPY"], dates, doses, controls=True)[1]

    t = fit_pair(dose)
    sh = [fit_pair(dose, k) for k in ev.SHIFTS_EARLY]
    sur: dict[str, list[float]] = {}
    for fam in FAMS:
        sur[fam] = []
        for j in range(M):
            s = surrogate(sess, fam, j)
            sur[fam].append(fit_pair({f: (s.get(f, v[0]), v[1]) for f, v in dose.items()}))
    return record(
        "W27", t, sh, sur, [sess[f] for f in sorted(sess)],
        "x (Anscombe roll-call count) surrogated over in-session weeks only, in time order;"
        " out-of-session weeks keep x = anscombe(0) and the session dummy is unchanged",
    )  # fmt: skip


def w28() -> dict[str, Any]:
    import wide15 as mod

    ev, e13 = mod.ev, mod.e13
    gate = ["QQQ", "IWM", "BTC", "ETH"]
    hist = harness.load_history("train", syms=gate)
    px = {a: e13.Closes({b.date: b.close for b in bars}) for a, bars in hist.items()}
    daily = mod.load_refunds()
    weeks = e13.fridays(date(2005, 10, 7), mod.LAST)
    u = ev.runoff(ev.refund_surprise(ev.weekly_sums(daily, weeks), ev.year_totals(daily)), weeks)
    dates = e13.fridays(date(2008, 1, 4), date(2025, 10, 3))
    d = mod.Design(px, date(2008, 1, 4), 5, 33)

    def fit(src: Mapping[date, float], k: int = 0) -> float:
        return d.fit(gate, dates, [lambda t: e13.shifted(src, t, k)], controls=False)[1]

    return direct(
        "W28", u, fit, e13.SHIFTS,
        "surrogate of the weekly refund-runoff dose u (seasonal: large about 15 weeks a year;"
        " surrogates keep the spectrum, so the annual peak, but not its calendar date)",
    )  # fmt: skip


def direct(
    gate: str,
    dose: Mapping[date, float],
    fit: Callable[..., float],
    shifts: list[int],
    design: str,
) -> dict[str, Any]:
    t = fit(dose)
    sh = [fit(dose, k) for k in shifts]
    sur = {fam: [fit(surrogate(dose, fam, j)) for j in range(M)] for fam in FAMS}
    vals = [dose[k] for k in sorted(dose) if dose[k] == dose[k]]
    return record(gate, t, sh, sur, vals, design)


# ---------------------------------------------------------------- output


def record(
    gate: str,
    t: float,
    sh: list[float],
    sur: dict[str, list[float]],
    dose: list[float],
    design: str,
) -> dict[str, Any]:
    name, st, sr = STORED[gate]
    rec = g.rescore_record(
        gate, f"{name}: {design}", 1, st, sr, t, sh, sur["phase"], sur["iaaft"], dose
    )
    rec["reproduced"] = abs(t - st) <= 0.02 and rec["shift_rank"] == sr
    rec["data_dir_lane"] = os.environ.get("GATENULL2_LANE", "")
    if not rec["reproduced"]:
        rec["note"] = f"true t {t:+.3f} or shift rank {rec['shift_rank']} differs from stored"
    return rec


GATES: dict[str, Callable[[], dict[str, Any]]] = {
    "W20": w20,
    "W21": w21,
    "W22": w22,
    "W23": w23,
    "W24": w24,
    "W25": w25,
    "W26": w26,
    "W27": w27,
    "W28": w28,
}


def main() -> None:
    use_data()
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for gate in sys.argv[1:] or list(GATES):
        try:
            rec = GATES[gate]()
        except FileNotFoundError as e:
            rec = {"gate": gate, "reproduced": False, "note": f"cached input missing: {e}"}
        (OUTDIR / f"{gate}.json").write_text(json.dumps(rec, indent=1) + "\n")
        keys = ("true_t", "stored_t", "stored_rank", "shift_rank", "phase_rank", "iaaft_rank")
        print(gate, {k: rec.get(k) for k in (*keys, "dose_acf1", "dose_neff", "reproduced")})


if __name__ == "__main__":
    main()
