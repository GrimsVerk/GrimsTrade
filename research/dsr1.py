"""dsr-1: every try the project has logged, on every branch, counted once.

    git fetch origin
    python research/dsr1.py census      # markdown tables for research/dsr-1.md
    python research/dsr1.py dsr         # deflated Sharpe and Holm tables (card in dsr-1.md)

Each research lane appends rows to `research/tries.md` on its own branch, and branches share
rows through their ancestry. A row is the same try on two branches when its line is identical.
A line that appears k times on one branch (a re-run logged twice) counts k times; across
branches the count is the largest k seen on any branch, so shared history is not double counted.

Stdlib plus the repo's own `grimstrade.stats` (eq. 2 of Bailey and Lopez de Prado 2014); reads
git objects, runs no backtest, writes nothing.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from statistics import NormalDist

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from grimstrade import stats  # noqa: E402

TRIES = "research/tries.md"
RESEARCH_TRIES = "ledger/research_tries.jsonl"  # the daily runner's copy, on paper-trail
LIVE_TRIES = "ledger/tries.jsonl"  # live strategies, on paper-trail
PRIMARY = ("1994-02-01", "2025-11-09")  # the six-asset train test of research run 1
DAYS_PER_YEAR = 365


@dataclass(frozen=True)
class Row:
    time: str
    idea: str
    variant: str
    kind: str
    period: str
    start: str
    end: str
    sharpe: float | None

    @property
    def primary(self) -> bool:
        """On the six assets over the full train period (the test `tsmom12` scored 1.05 on)."""
        return (self.start, self.end) == PRIMARY and "@" not in self.variant


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    return out.stdout if out.returncode == 0 else ""


def branches() -> list[str]:
    refs = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").split()
    return sorted(r for r in refs if r not in ("origin", "origin/HEAD"))


def parse(line: str) -> Row | None:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 8 or cells[0][:2] != "20":
        return None
    try:
        sharpe: float | None = float(cells[7])
    except ValueError:
        sharpe = None
    if sharpe is not None and not math.isfinite(sharpe):
        sharpe = None
    return Row(cells[0], cells[1], cells[2], cells[3], cells[4], cells[5], cells[6], sharpe)


@dataclass
class Census:
    branches: list[str]  # remote branches read
    with_file: dict[str, int]  # branch -> data lines in its tries.md
    rows: list[tuple[Row, str]]  # every distinct try (with multiplicity) and its lane
    raw_lines: int  # data lines summed over branches, before removing shared history


def collect() -> Census:
    per_branch: dict[str, Counter[str]] = {}
    for b in branches():
        text = git("show", f"{b}:{TRIES}")
        lines = [ln.strip() for ln in text.splitlines() if ln.startswith("| 20")]
        if lines:
            per_branch[b] = Counter(lines)
    tip = {b: git("log", "-1", "--format=%cI", b).strip() for b in per_branch}
    best: dict[str, int] = {}
    homes: dict[str, list[str]] = defaultdict(list)
    for b, counts in per_branch.items():
        for line, k in counts.items():
            best[line] = max(best.get(line, 0), k)
            homes[line].append(b)
    rows: list[tuple[Row, str]] = []
    for line, k in sorted(best.items()):
        row = parse(line)
        if row is None:
            continue
        # The lane that logged it: the smallest file holding the line (ties: the oldest tip).
        lane = min(homes[line], key=lambda b: (sum(per_branch[b].values()), tip[b], b))
        rows += [(row, lane.removeprefix("origin/"))] * k
    return Census(
        branches(),
        {b: sum(c.values()) for b, c in per_branch.items()},
        rows,
        sum(sum(c.values()) for c in per_branch.values()),
    )


def var(xs: list[float]) -> float:
    return statistics.variance(xs) if len(xs) >= 2 else float("nan")


def sharpe_line(name: str, rows: list[Row]) -> str:
    xs = [r.sharpe for r in rows if r.sharpe is not None]
    if len(xs) < 2:
        return f"| {name} | {len(rows)} | {len(xs)} | | | | |"
    v = var(xs)
    return (
        f"| {name} | {len(rows)} | {len(xs)} | {statistics.mean(xs):.2f} | {v:.3f} | "
        f"{math.sqrt(v):.2f} | {min(xs):.2f} .. {max(xs):.2f} |"
    )


def paper_trail_check(rows: list[Row]) -> list[str]:
    """The daily runner's own copy of research tries: is anything there missing from the union?"""
    text = git("show", f"origin/paper-trail:{RESEARCH_TRIES}")
    seen = [json.loads(ln) for ln in text.splitlines() if ln.strip()]
    ours = {(r.idea.lower(), r.variant.lower()) for r in rows}
    with_variant = [s for s in seen if s.get("variant")]
    missing = [s for s in with_variant if (s["idea"].lower(), s["variant"].lower()) not in ours]
    idea_only = len(seen) - len(with_variant)
    live = [ln for ln in git("show", f"origin/paper-trail:{LIVE_TRIES}").splitlines() if ln]
    return [
        f"- `{RESEARCH_TRIES}` on `paper-trail` (the daily runner's copy, last filled "
        f"{max((s.get('seen') or '') for s in seen)[:10] if seen else '-'}): {len(seen)} "
        f"entries; {len(with_variant)} name a variant and {len(missing)} of those are missing "
        f"from the union (case ignored); {idea_only} name only an idea (ideas-list entries, "
        "several never backtested). It stopped growing after research run 2: it is not a "
        "project-wide register.",
        f"- `{LIVE_TRIES}` on `paper-trail`: {len(live)} live strategies (M0/M1 yardsticks and "
        "rules, no backtest Sharpe recorded there). Counted separately below, not in the rows.",
    ]


def census() -> None:
    c = collect()
    rows = [r for r, _ in c.rows]
    out = [
        f"Remote branches read: {len(c.branches)}; with a `{TRIES}`: {len(c.with_file)}. "
        f"Data lines summed over branches: {c.raw_lines}; distinct tries after removing "
        f"shared history: **{len(rows)}**.",
        "",
        "### By kind",
        "",
        "| Kind | Rows | With Sharpe | Mean | Variance | SD | Range |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for kind, _n in Counter(r.kind for r in rows).most_common():
        out.append(sharpe_line(kind, [r for r in rows if r.kind == kind]))
    out.append(sharpe_line("**all**", rows))
    sel = [r for r in rows if r.kind == "variant" and r.period == "train"]
    prim = [r for r in rows if r.primary and r.kind in ("variant", "baseline")]
    out += [
        "",
        "### Sharpe spread on the tests the deflated Sharpe needs",
        "",
        "Annualised Sharpe (365 days, zero rate). Per-day variance = annual variance / 365.",
        "",
        "| Set | Rows | With Sharpe | Mean | Variance | SD | Range |",
        "|---|---:|---:|---:|---:|---:|---|",
        sharpe_line("selectable: `variant`, train, any data", sel),
        sharpe_line("primary test: six assets, 1994-02-01..2025-11-09, variant+baseline", prim),
        sharpe_line("primary test, `variant` only", [r for r in prim if r.kind == "variant"]),
        "",
        "### By lane (the branch that logged the row; approximate)",
        "",
        "| Lane | Rows | Variants | Families | With Sharpe |",
        "|---|---:|---:|---:|---:|",
    ]
    by_lane: dict[str, list[Row]] = defaultdict(list)
    for r, lane in c.rows:
        by_lane[lane].append(r)
    for lane, rs in sorted(by_lane.items(), key=lambda kv: min(r.time for r in kv[1])):
        out.append(
            f"| {lane} | {len(rs)} | {sum(r.kind == 'variant' for r in rs)} | "
            f"{len({r.idea for r in rs})} | {sum(r.sharpe is not None for r in rs)} |"
        )
    out += [
        "",
        "### By family (the `Idea` column), largest first",
        "",
        "| Family | Rows | Variants | With Sharpe | Sharpe variance |",
        "|---|---:|---:|---:|---:|",
    ]
    fams: dict[str, list[Row]] = defaultdict(list)
    for r in rows:
        fams[r.idea].append(r)
    for idea, rs in sorted(fams.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        xs = [r.sharpe for r in rs if r.sharpe is not None]
        v = f"{var(xs):.3f}" if len(xs) >= 2 else ""
        out.append(
            f"| {idea} | {len(rs)} | {sum(r.kind == 'variant' for r in rs)} | {len(xs)} | {v} |"
        )
    no_sharpe = Counter(r.kind for r in rows if r.sharpe is None)
    out += [
        "",
        "### Gaps",
        "",
        f"- Rows without a Sharpe: {sum(no_sharpe.values())} "
        f"({', '.join(f'{k} {n}' for k, n in no_sharpe.most_common())}).",
        f"- Families: {len(fams)}. Periods: "
        f"{', '.join(f'{k} {n}' for k, n in Counter(r.period for r in rows).most_common())}.",
        *paper_trail_check(rows),
    ]
    print("\n".join(out))


# ---------------------------------------------------------------------------------------------
# Step 2: deflated Sharpe and Bonferroni/Holm (card: research/dsr-1.md, section 2)

CUTOFF = "2026-11-18 22:17"  # the census snapshot; later rows are left out so the numbers repeat
LIVE = 11  # strategies in ledger/tries.jsonl on paper-trail (M0/M1): tried, so counted in N
RISK_MAP_CARD = "2026-11-12 07:15"  # UTC; research-3's risk-map card picked the presets
STRESS = (-1.0, 30.0)  # skew, raw kurtosis of the stress case (not logged anywhere)
PASS = 0.95
_Z = NormalDist()


def calendar_days(start: str, end: str) -> int:
    def d(x: str) -> dt.date:
        return dt.date.fromisoformat(x if len(x) == 10 else x + "-01")

    return (d(end) - d(start)).days + 1


def max_z(n: float) -> float:
    """Expected maximum of n independent standard normals (the paper's eq. 1, unit variance).
    Takes a fractional n, for the effective number of trials of appendix A.3."""
    if n <= 1:
        return 0.0
    g = stats.EULER_GAMMA
    return (1 - g) * _Z.inv_cdf(1 - 1 / n) + g * _Z.inv_cdf(1 - 1 / (n * math.e))


def effective(m: int, rho: float) -> float:
    """Appendix A.3, eq. 9: M trials with average correlation rho count as this many."""
    return rho + (1 - rho) * m


def dsr_abs(
    sr: float, t: int, n: float, v_ann: float, mean: float = 0.0, moments: tuple = (0.0, 3.0)
) -> tuple[float, float]:
    """(DSR, SR0 annualised) for an annualised Sharpe over t calendar days (eq. 2). `mean` = 0 is
    the paper's null; a positive mean is test 2 (the trials' own average, eq. 1)."""
    v = max(v_ann / DAYS_PER_YEAR, stats.null_sharpe_variance(t))
    sr0 = mean / math.sqrt(DAYS_PER_YEAR) + math.sqrt(v) * max_z(n)
    m = stats.Moments(t, sr / math.sqrt(DAYS_PER_YEAR), moments[0], moments[1])
    return stats.probabilistic_sharpe(m, sr0), sr0 * math.sqrt(DAYS_PER_YEAR)


def dsr_diff(z: float, n: float) -> float:
    """Edge in difference form: Z((d - SE maxZ(N)) / SE) = Z(z - maxZ(N)), z = d / SE."""
    return _Z.cdf(z - max_z(n))


def break_even(f: Callable[[float], float]) -> float:
    """Largest number of independent trials at which f(N) is still >= 0.95."""
    if f(1) < PASS:
        return 0
    hi = 2.0
    while f(hi) >= PASS:
        hi *= 2
        if hi > 1e15:
            return math.inf
    lo = hi / 2
    while hi - lo > max(1.0, lo * 1e-4):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) >= PASS else (lo, mid)
    return lo


@dataclass(frozen=True)
class Candidate:
    name: str
    lane: str
    comparator: str
    d: float  # edge as the lane reported it
    p: float  # one-sided, as the lane reported it
    se: float | None  # from the lane's 90% range when it gave one, else d / z(p)
    n_family: int  # the family bar's size: max(variant rows of the family, the lane's own count)
    heldout: str
    sharpe: float | None  # its own Sharpe, for the absolute DSR
    start: str
    end: str
    source: str

    @property
    def z(self) -> float:
        if self.se:
            return self.d / self.se
        return _Z.inv_cdf(1 - self.p)


TSMOM_EDGE = Candidate(
    "`tsmom12` vs equal weight", "research-1", "equal weight", 0.17, 0.08, None, 0, "-",
    1.05, *PRIMARY, "results/baselines.md; review-1 (SE 0.12)",
)  # fmt: skip
TSMOM_2003 = Candidate(
    "`tsmom12` vs equal weight, 2003-2025", "review-1", "equal weight", 0.00, 0.49, None, 0, "-",
    1.20, "2003-01-01", PRIMARY[1], "review-1 finding 1",
)  # fmt: skip
# The five near-misses by the card's rule (section 2b of dsr-1.md; how each was found is there).
NEAR = [
    Candidate(
        "`gsy-runup` flag100-sma", "gsy-1", "`tsmom12`, 30 French industries 1928-2001",
        0.027, 0.001, None, 12, "unspent", 1.01, "1928-07-02", "2001-12-30",
        "gsy-1: results/gsy-1.md (G30 disc)",
    ),
    Candidate(
        "`halving-and`", "macro-1", "`tsmom12`, six assets", 0.15, 0.005, (0.25 - 0.06) / 3.29,
        13, "unspent", 1.20, *PRIMARY, "macro-1: results/halving.md",
    ),
    Candidate(
        "quiet coins (`turnover` TOP-TS)", "breadth-1", "`tsmom12` on the same coin book",
        0.34, 0.005, None, 61, "spent (passed: 0.61 vs 0.31)", 1.06, "2019-03-01", PRIMARY[1],
        "breadth-1: results/breadth-1.md (p printed 0.00; 0.005 used)",
    ),
    Candidate(
        "funding carry `band`", "carry-3", "zero (pooled Sharpe > 0)", 0.79, 0.025, None, 25,
        "spent (failed: -0.65)", 0.79, "2021-02-20", PRIMARY[1],
        "carry-3: results/carry-3.md, carry-3.md",
    ),
    Candidate(
        "coin `stop-0.25`", "coin-cap 1-4", "a coin cap of the same cost (sign test, 21 episodes)",
        15 / 21, 0.0392, None, 16, "unspent", 1.09, *PRIMARY,
        "coin-cap-4: coin-cap-verdict.md",
    ),
]  # fmt: skip


def holm(ps: list[float], m: int) -> list[float]:
    """Holm-adjusted p-values for the smallest len(ps) of m tests (the rest assumed larger)."""
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out = [1.0] * len(ps)
    run = 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (m - k) * ps[i]))
        out[i] = run
    return out


def fmt_n(x: float) -> str:
    if x == math.inf:
        return "> 1e15"
    if x == 0:
        return "none (fails at N = 1)"
    return f"{x:,.0f}" if x >= 10 else f"{x:.1f}"


def deflate_all() -> None:
    c = collect()
    rows = [r for r, _ in c.rows if r.time <= CUTOFF]
    selectable = [r for r in rows if r.kind in ("variant", "baseline") and r.period == "train"]
    prim = [r for r in selectable if r.primary and r.sharpe is not None]
    first = min(r.time for r in rows)
    n1 = sum(r.primary and r.kind == "baseline" and r.time == first for r in rows)
    n2 = sum(r.time < RISK_MAP_CARD for r in prim) + sum(r.idea == "risk-map" for r in rows) + LIVE
    n3 = len(selectable) + LIVE
    m4 = sum(r.sharpe is not None for r in rows) + LIVE
    v_prim = var([r.sharpe for r in prim if r.sharpe is not None])
    mean_prim = statistics.mean(r.sharpe for r in prim if r.sharpe is not None)
    sel_sh = [r.sharpe for r in selectable if r.kind == "variant" and r.sharpe is not None]
    v_proj, mean_proj = var(sel_sh), statistics.mean(sel_sh)
    t = calendar_days(*PRIMARY)
    # The repo's stats.expected_max_sharpe and max_z must agree (same equation).
    assert abs(stats.expected_max_sharpe(100, 1.0) - max_z(100)) < 1e-12

    ns = [
        ("N1 bar (first harness run)", n1),
        ("N2 live preset (risk map)", n2),
        ("N3 if chosen today", n3),
        ("M4 every row with a Sharpe", m4),
    ]
    out = [
        f"Rows up to {CUTOFF} UTC: {len(rows)}. T for the primary test = {t:,} calendar days. "
        f"Luck floor 1/T = {365 / t:.4f} a year (variance of an annual Sharpe).",
        "",
        "| Trial count | N | at rho 0.5 | at rho 0.9 |",
        "|---|---:|---:|---:|",
    ]
    out += [
        f"| {lab} | {n:,} | {fmt_n(effective(n, 0.5))} | {fmt_n(effective(n, 0.9))} |"
        for lab, n in ns
    ]
    out += [
        "",
        f"Variance of trial Sharpes (annual): primary test {v_prim:.4f} (mean {mean_prim:.2f}, "
        f"{len(prim)} rows); project-wide selectable variants {v_proj:.4f} (mean "
        f"{mean_proj:.2f}). The primary-test spread is below the luck floor "
        f"{365 / t:.4f}, so the floor is used there.",
        "",
        "#### (a1) `tsmom12`, absolute (paper's null: no trial has skill)",
        "",
        "| N | V | SR0 (annual) | DSR normal | DSR stress (skew -1, kurt 30) |",
        "|---|---|---:|---:|---:|",
    ]
    vs = [("primary", v_prim), ("project", v_proj)]
    for lab, n in ns:
        for rho in (0.0, 0.9):
            ne = effective(n, rho)
            for vlab, v in vs:
                d0, sr0 = dsr_abs(1.05, t, ne, v)
                ds, _ = dsr_abs(1.05, t, ne, v, moments=STRESS)
                rl = f" (rho {rho})" if rho else ""
                out.append(f"| {lab}{rl}: {fmt_n(ne)} | {vlab} | {sr0:.2f} | {d0:.4f} | {ds:.4f} |")
    ew = [
        f"{lab}: {dsr_abs(0.88, t, n, v)[0]:.3f}"
        for lab, n in ns[2:3]
        for vlab, v in vs
        if vlab == "project"
    ] + [f"N1, V primary: {dsr_abs(0.88, t, n1, v_prim)[0]:.4f}"]
    out += [
        "",
        "For comparison, equal weight (Sharpe 0.88, a rule nobody searched for) in the same "
        f"test: V project, {'; '.join(ew)}. The absolute test cannot tell a trend rule from "
        "holding the market.",
        "",
        "Break-even N (largest number of independent trials with DSR >= 0.95): "
        + "; ".join(
            f"V {vlab}: {fmt_n(break_even(lambda n, v=v: dsr_abs(1.05, t, n, v)[0]))}"
            for vlab, v in vs
        )
        + ".",
        "",
        "#### (a2) `tsmom12` against the project's own trials (eq. 1 with their mean)",
        "",
        "| N | Mean and V of the trials | SR0 (annual) | DSR normal | DSR stress |",
        "|---|---|---:|---:|---:|",
    ]
    mv = [(f"primary ({mean_prim:.2f})", mean_prim, v_prim), (f"project ({mean_proj:.2f})",
          mean_proj, v_proj)]  # fmt: skip
    for lab, n in ns:
        for rho in (0.0, 0.9):
            ne = effective(n, rho)
            for mlab, mu, v in mv:
                d0, sr0 = dsr_abs(1.05, t, ne, v, mean=mu)
                ds, _ = dsr_abs(1.05, t, ne, v, mean=mu, moments=STRESS)
                rl = f" (rho {rho})" if rho else ""
                out.append(f"| {lab}{rl}: {fmt_n(ne)} | {mlab} | {sr0:.2f} | {d0:.3f} | {ds:.3f} |")
    out += [
        "",
        "Break-even N: "
        + "; ".join(
            f"{mlab}: {fmt_n(break_even(lambda n, mu=mu, v=v: dsr_abs(1.05, t, n, v, mean=mu)[0]))}"
            for mlab, mu, v in mv
        )
        + ".",
        "",
        "#### (a3) `tsmom12`'s edge over equal weight (difference form)",
        "",
        "| Window | d | z | N | DSR | Edge left after luck (d - SE maxZ) |",
        "|---|---:|---:|---|---:|---:|",
    ]
    for cand in (TSMOM_EDGE, TSMOM_2003):
        se = cand.se or (cand.d / cand.z if cand.z else 0.12)
        for lab, n in ns:
            out.append(
                f"| {cand.name} | {cand.d:+.2f} | {cand.z:.2f} | {lab}: {n:,} | "
                f"{dsr_diff(cand.z, n):.3f} | "
                f"{f'{cand.d - se * max_z(n):+.2f}' if cand.d else '-'} |"
            )
    out.append(
        f"| | | | break-even N (1994-2025) | "
        f"{fmt_n(break_even(lambda n: dsr_diff(TSMOM_EDGE.z, n)))} | |"
    )

    out += [
        "",
        "#### (b) The five near-misses",
        "",
        "| Near-miss | Lane | Against | d | p | z | N_family | DSR at N_family | "
        f"DSR at N3 = {n3:,} | at N3, rho 0.9 | Absolute DSR at N3 (V project) | Held-out year |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for cand in NEAR:
        a = ""
        if cand.sharpe is not None:
            a = f"{dsr_abs(cand.sharpe, calendar_days(cand.start, cand.end), n3, v_proj)[0]:.3f}"
        out.append(
            f"| {cand.name} | {cand.lane} | {cand.comparator} | {cand.d:+.3g} | {cand.p:.4f} | "
            f"{cand.z:.2f} | {cand.n_family} | {dsr_diff(cand.z, cand.n_family):.3f} | "
            f"{dsr_diff(cand.z, n3):.3f} | {dsr_diff(cand.z, effective(n3, 0.9)):.3f} | {a} | "
            f"{cand.heldout} |"
        )
    out += [
        "",
        "#### Bonferroni and Holm (one-sided p, alpha 0.05)",
        "",
        "| Hypothesis | p | Survives Bonferroni up to m = | Holm-adjusted, m = 6 | "
        f"Bonferroni at N_family | Holm-adjusted at m = N3 = {n3:,} |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    hyps = [TSMOM_EDGE, *NEAR]
    ps = [h.p for h in hyps]
    h6, hn = holm(ps, len(hyps)), holm(ps, n3)
    for h, a6, an in zip(hyps, h6, hn, strict=True):
        nf = h.n_family or n1
        out.append(
            f"| {h.name} | {h.p:.4f} | {fmt_n(0.05 / h.p)} | {a6:.3f} | "
            f"{min(1.0, h.p * nf):.3f} (m = {nf}) | {an:.3f} |"
        )
    abs_p = 1 - dsr_abs(1.05, t, 1, 0.0)[0]
    out += [
        "",
        f"`tsmom12` absolute (Sharpe > 0): p = {abs_p:.1e}, survives Bonferroni up to "
        f"m = {fmt_n(0.05 / abs_p) if abs_p > 0 else '> 1e15'}.",
        "",
        "Card's held-out rule (unspent, DSR >= 0.95 at N_family and >= 0.50 at N3):",
        "",
    ]
    for cand in NEAR:
        ok = (
            cand.heldout == "unspent"
            and dsr_diff(cand.z, cand.n_family) >= PASS
            and dsr_diff(cand.z, n3) >= 0.5
        )
        out.append(f"- {cand.name}: {'worth a held-out year' if ok else 'no'}")
    print("\n".join(out))


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "census"
    if cmd == "census":
        census()
    elif cmd == "dsr":
        deflate_all()
    else:
        sys.exit(f"unknown command {cmd!r}")


if __name__ == "__main__":
    main()
