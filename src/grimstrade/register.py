"""The project-wide tries register: every try logged on any branch, counted once, and the bar a
new pick must clear at that count.

    git fetch origin
    uv run python -m grimstrade.register        # rewrites research/register/{tries.jsonl,BAR.md}

Each research lane appends rows to `research/tries.md` on its own branch, and branches share
rows through their history. The dedup rule (dsr-1's census, `research/dsr1.py`):

- A row is a line of a branch's `research/tries.md` starting `| 20` (a dated table row), compared
  after stripping surrounding white space. The same line on two branches is the same try.
- A line that appears k times on one branch (a re-run logged twice) is k tries; across branches
  the count is the largest k on any one branch, so shared history is not counted twice.
- A try's id is the first 16 hex digits of the line's SHA-256 and its occurrence number (1..k).
- The register only grows: every id already in `research/register/tries.jsonl` (on disk or on a
  remote branch) stays, so a deleted branch cannot take its tries with it.

Branches read: every remote-tracking branch except `paper-trail` (the record) and `origin/HEAD`:
what is pushed, so any machine regenerates the same file after `git fetch`. Live strategies are
the lines of `ledger/tries.jsonl` on the remote `paper-trail`.

Stdlib only; reads git objects, runs no backtest. Writes nothing but the two register files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import subprocess
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from statistics import NormalDist

from grimstrade import ledger, stats, tryshape

TRIES_MD = ledger.RESEARCH_TRIES
REGISTER = Path(ledger.RESEARCH_REGISTER)
BAR = REGISTER.parent / "BAR.md"
LIVE_TRIES = "ledger/tries.jsonl"  # on the record branch
MOMENTS = REGISTER.parent / "moments.jsonl"  # research/register2.py writes these two
TRIALS = REGISTER.parent / "trials.json"
SHAPES = Path(tryshape.SHAPES)  # the harness appends one per logged row (register-3)
REMOTES = ("refs/remotes",)
PRIMARY = ("1994-02-01", "2025-11-09")  # the six-asset train test `tsmom12` scored 1.05 on
DAYS_PER_YEAR = 365
PASS = 0.95  # deflated Sharpe needed
ALPHA = 0.05  # one-sided, for Bonferroni
# Standard error of a new rule's Sharpe edge over `tsmom12` on the primary test (dsr-1): a rule
# close to it (returns highly correlated) and a far one (review-1's SE against equal weight).
SE_CLOSE, SE_FAR = 0.065, 0.12
PRIMARY_WEEKS = 1_657  # weekly returns in the primary test, the record those SEs are for
WEEKS_PER_YEAR = 365.25 / 7
YEARS = (5, 10, 20, 32)  # record lengths in the per-record-length table
RHOS = (0.0, 0.5, 0.9)  # average correlation between trials (appendix A.3 of the DSR paper)
MIN_WINDOW_ROWS = 20  # windows with fewer selectable Sharpes are left out of the spread table
_Z = NormalDist()


class RegisterError(Exception):
    pass


@dataclass(frozen=True)
class Try:
    id: str
    line: str
    time: str
    idea: str
    variant: str
    kind: str
    period: str
    start: str
    end: str
    sharpe: float | None

    @property
    def selectable(self) -> bool:
        """A configuration that could have been picked: a variant or baseline on train data."""
        return self.kind in ("variant", "baseline") and self.period == "train"

    @property
    def primary(self) -> bool:
        """On the six assets over the full train period (an `@` in the variant: other assets)."""
        return (self.start, self.end) == PRIMARY and "@" not in self.variant

    def to_json(self) -> str:
        d = {
            "id": self.id,
            "time": self.time,
            "idea": self.idea,
            "variant": self.variant,
            "kind": self.kind,
            "period": self.period,
            "from": self.start,
            "to": self.end,
            "sharpe": self.sharpe,
            "line": self.line,
        }
        return json.dumps(d, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def line_hash(line: str) -> str:
    return hashlib.sha256(line.encode()).hexdigest()[:16]


def parse(line: str, occurrence: int) -> Try | None:
    """The try in a `research/tries.md` row (columns: time, idea, variant, kind, period, from,
    to, Sharpe, ...); None if the row has fewer than eight cells or no date."""
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 8 or cells[0][:2] != "20":
        return None
    try:
        sharpe: float | None = float(cells[7])
    except ValueError:
        sharpe = None
    if sharpe is not None and not math.isfinite(sharpe):
        sharpe = None
    time, idea, variant, kind, period, start, end = cells[:7]
    ident = f"{line_hash(line)}-{occurrence}"
    return Try(ident, line, time, idea, variant, kind, period, start, end, sharpe)


def _show(repo: Path, ref: str, rel: str) -> str:
    try:
        return ledger._git(repo, "show", f"{ref}:{rel}").decode()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def branch_lines(repo: Path) -> dict[str, Counter[str]]:
    """Each remote branch with a `research/tries.md`: its dated rows, with multiplicity."""
    out: dict[str, Counter[str]] = {}
    for ref in ledger.research_refs(repo, REMOTES):
        text = _show(repo, ref, TRIES_MD)
        lines = [ln.strip() for ln in text.splitlines() if ln.startswith("| 20")]
        if lines:
            out[ref] = Counter(lines)
    return out


def census(per_branch: dict[str, Counter[str]]) -> list[Try]:
    """Every distinct try: each line as many times as on the branch that has it most often."""
    best: dict[str, int] = {}
    for counts in per_branch.values():
        for line, k in counts.items():
            best[line] = max(best.get(line, 0), k)
    found = (parse(line, i) for line, k in best.items() for i in range(1, k + 1))
    return [t for t in found if t is not None]


def read_register(text: str, where: str) -> list[Try]:
    """A register file's tries. Raises RegisterError on a line that is not a try or whose id
    does not match its line: the register is generated, a hand edit must not pass silently."""
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            d = json.loads(raw)
            line, ident = d["line"], d["id"]
            occurrence = int(ident.rsplit("-", 1)[1])
        except (ValueError, KeyError, IndexError, TypeError, AttributeError) as e:
            raise RegisterError(f"{where}:{n}: not a register line ({e})") from e
        t = parse(line, occurrence)
        if t is None or t.id != ident or occurrence < 1 or t.to_json() != raw.strip():
            raise RegisterError(f"{where}:{n}: does not match its own line (edited by hand?)")
        out.append(t)
    return out


def merge(*sets: Iterable[Try]) -> list[Try]:
    """The union by id, sorted by time then id."""
    by_id: dict[str, Try] = {}
    for tries in sets:
        for t in tries:
            by_id.setdefault(t.id, t)
    return sorted(by_id.values(), key=lambda t: (t.time, t.id))


def live_strategies(repo: Path) -> int | None:
    """Lines in `ledger/tries.jsonl` on the remote record branch (the most on any remote); None
    if no remote record branch is there."""
    refs = ledger._git(repo, "for-each-ref", "--format=%(refname)", *REMOTES).decode().split()
    trails = [r for r in refs if r.rsplit("/", 1)[-1] == ledger.RECORD_BRANCH]
    if not trails:
        return None
    return max(
        sum(1 for ln in _show(repo, r, LIVE_TRIES).splitlines() if ln.strip()) for r in trails
    )


def logged_shapes(repo: Path, tries: Iterable[Try]) -> dict[str, tryshape.Shape]:
    """Register id -> the shape the harness logged for its row (`research/tries-shape.jsonl`
    on disk and on every remote branch; the same row text on two branches is the same run)."""
    by_row: dict[str, tryshape.Shape] = {}
    texts = [((repo / SHAPES).read_text(), str(SHAPES))] if (repo / SHAPES).exists() else []
    for ref in ledger.research_refs(repo, REMOTES):
        text = _show(repo, ref, SHAPES.as_posix())
        if text:
            texts.append((text, f"{ref}:{SHAPES.as_posix()}"))
    for text, where in texts:
        try:
            found = tryshape.read(text, where)
        except ValueError as e:
            raise RegisterError(str(e)) from e
        for row, shape in found.items():
            by_row.setdefault(row, shape)
    return {t.id: by_row[t.line] for t in tries if t.line in by_row}


@dataclass(frozen=True)
class Measured:
    """What `research/register2.py` measured from the tries' own weekly returns (register-2)."""

    rows: int  # register rows with record length, skew and kurtosis
    selectable: int  # of which selectable
    live: int  # live strategies with them
    sample: int  # M: distinct return series in the correlation window
    window: tuple[str, str]
    weeks: int
    rho_mean: float
    rho_median: float
    participation: float  # eigenvalue cross-check: (sum l)^2 / sum l^2
    onc_k: int
    onc_at_cap: bool
    cluster_var: float | None  # variance of the clusters' annual Sharpes
    check: tuple[str, int, float, int] | None  # other window: name, M, rho, K
    skew_median: float
    skew_p10: float
    ek_median: float
    ek_p90: float
    cap: int | None = None  # series per family in the sample (register-3); None: uncapped
    families: int | None = None
    uncapped: tuple[int, float] | None = None  # the uncapped sample: M, rho (comparison)

    def rows_for(self, n: int) -> list[tuple[str, float]]:
        """(label, N_eff) for `n` trials: the measured estimates the bar chooses from first,
        then comparisons."""
        capped = f", at most {self.cap} per family" if self.cap else ""
        out = [
            (f"measured rho {self.rho_mean:.2f} (A.3{capped})", effective(n, self.rho_mean)),
            (
                f"ONC {self.onc_k} clusters in {self.sample:,}, scaled to N",
                min(float(n), self.onc_k * n / self.sample),
            ),
            (f"ONC {self.onc_k} clusters, sample only", float(min(self.onc_k, n))),
        ]
        if self.uncapped:
            m, rho = self.uncapped
            out.append(
                (f"uncapped sample of {m:,}: rho {rho:.2f} (A.3, register-2)", effective(n, rho))
            )
        return out

    def headline(self, n: int) -> tuple[str, float]:
        """The bar's N: the more cautious of A.3 and ONC scaled (card register-2)."""
        return max(self.rows_for(n)[:2], key=lambda r: r[1])


def read_measured(repo: Path, known: set[str]) -> Measured | None:
    """The measured inputs, if both generated files are there. Raises RegisterError on a
    moments line whose id is not a register try (`live:<name>` for live strategies)."""
    if not (repo / TRIALS).exists() or not (repo / MOMENTS).exists():
        return None
    rows = sel = live = 0
    for n, raw in enumerate((repo / MOMENTS).read_text().splitlines(), 1):
        if not raw.strip():
            continue
        d = json.loads(raw)
        if d["id"].startswith("live:"):
            live += 1
            continue
        if d["id"] not in known:
            raise RegisterError(f"{MOMENTS}:{n}: {d['id']} is not in the register")
        rows += 1
        sel += d["kind"] in ("variant", "baseline")
    t = json.loads((repo / TRIALS).read_text())
    # register-3: the family-capped sample when there is one, the uncapped one as comparison.
    cap = t.get("family_cap")
    windows = cap["windows"] if cap else t["windows"]
    w = windows[t["main_window"]]
    others = [(k, v) for k, v in sorted(windows.items()) if k != t["main_window"]]
    check = None
    if others and "onc_k" in others[0][1]:
        k, v = others[0]
        check = (k, v["series"], v["rho_mean"], v["onc_k"])
    sh = t["shape"]
    return Measured(
        rows, sel, live, w["series"], (w["from"], w["to"]), w["weeks"], w["rho_mean"],
        w["rho_median"], w["participation_ratio"], w["onc_k"], w["onc_k_at_cap"],
        w["cluster_sharpe_var"], check, sh["skew_median"], sh["skew_p10"],
        sh["excess_kurtosis_median"], sh["excess_kurtosis_p90"],
        cap["cap"] if cap else None, cap["families"] if cap else None,
        (u["series"], u["rho_mean"]) if cap and (u := t["windows"][t["main_window"]]) else None,
    )  # fmt: skip


# --- the bar ---


def max_z(n: float) -> float:
    """Expected maximum of n independent standard normals (eq. 1 of the DSR paper, unit
    variance); takes a fractional n for the effective number of correlated trials."""
    if n <= 1:
        return 0.0
    g = stats.EULER_GAMMA
    return (1 - g) * _Z.inv_cdf(1 - 1 / n) + g * _Z.inv_cdf(1 - 1 / (n * math.e))


def effective(m: int, rho: float) -> float:
    """Appendix A.3, eq. 9: m trials with average correlation rho count as this many."""
    return rho + (1 - rho) * m


def sharpe_needed(
    n: float,
    v_annual: float,
    periods: int,
    per_year: float = DAYS_PER_YEAR,
    skew: float = 0.0,
    excess_kurtosis: float = 0.0,
) -> float:
    """Annual Sharpe a rule needs over `periods` returns (`per_year` of them a year, normal by
    default) for a deflated Sharpe of 0.95 against zero, when n trials' annual Sharpes spread
    with variance `v_annual`."""
    v = max(v_annual / per_year, stats.null_sharpe_variance(periods))
    sr0 = math.sqrt(v) * max_z(n)
    lo, hi = sr0, sr0 + 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        m = stats.Moments(periods, mid, skew, 3.0 + excess_kurtosis)
        lo, hi = (lo, mid) if stats.probabilistic_sharpe(m, sr0) >= PASS else (mid, hi)
    return hi * math.sqrt(per_year)


@dataclass(frozen=True)
class BarRow:
    label: str
    n: float
    z_dsr: float  # z = edge / SE needed for DSR 0.95 (difference form)
    p_bonferroni: float  # one-sided p needed
    z_bonferroni: float


@dataclass(frozen=True)
class Summary:
    tries: int
    families: int
    by_kind: list[tuple[str, int]]
    without_sharpe: int
    selectable: int
    live: int | None
    through: str
    branches: int
    v_selectable: float | None  # variance of selectable variants' annual Sharpes
    mean_selectable: float | None
    windows: list[tuple[str, str, int, float, float]]  # from, to, rows, mean, variance
    measured: Measured | None = None
    logged: tuple[int, int] = (0, 0)  # tries with a harness-logged shape: all, selectable

    @property
    def n(self) -> int:
        """N for a new pick: selectable rows plus the live strategies."""
        return self.selectable + (self.live or 0)

    def bar(self) -> list[BarRow]:
        """Independent trials, then the measured estimates (or, without them, assumed rhos)."""
        if self.measured is None:
            counts = [
                ("independent" if rho == 0 else f"rho {rho}", effective(self.n, rho))
                for rho in RHOS
            ]
        else:
            counts = [("independent", float(self.n)), *self.measured.rows_for(self.n)]
        return [bar_row(label, n) for label, n in counts]

    def headline(self) -> BarRow:
        """The bar quoted for a new pick: the measured estimate, or all trials independent."""
        if self.measured is None:
            return bar_row("independent", float(self.n))
        return bar_row(*self.measured.headline(self.n))


def bar_row(label: str, n: float) -> BarRow:
    p = ALPHA / max(n, 1.0)
    return BarRow(label, n, _Z.inv_cdf(PASS) + max_z(n), p, _Z.inv_cdf(1 - p))


def summarize(
    tries: list[Try],
    live: int | None,
    branches: int,
    measured: Measured | None = None,
    logged: dict[str, tryshape.Shape] | None = None,
) -> Summary:
    sel = [t for t in tries if t.selectable]
    xs = [t.sharpe for t in sel if t.kind == "variant" and t.sharpe is not None]
    windows: dict[tuple[str, str], list[float]] = {}
    for t in sel:
        if t.sharpe is not None:
            windows.setdefault((t.start, t.end), []).append(t.sharpe)
    spread = [
        (a, b, len(v), statistics.mean(v), statistics.variance(v))
        for (a, b), v in windows.items()
        if len(v) >= max(MIN_WINDOW_ROWS, 2)
    ]
    spread.sort(key=lambda w: (-w[2], w[0], w[1]))
    return Summary(
        tries=len(tries),
        families=len({t.idea for t in tries}),
        by_kind=sorted(Counter(t.kind for t in tries).items(), key=lambda kv: (-kv[1], kv[0])),
        without_sharpe=sum(t.sharpe is None for t in tries),
        selectable=len(sel),
        live=live,
        through=max((t.time for t in tries), default="-"),
        branches=branches,
        v_selectable=statistics.variance(xs) if len(xs) >= 2 else None,
        mean_selectable=statistics.mean(xs) if xs else None,
        windows=spread[:10],
        measured=measured,
        logged=(
            sum(t.id in (logged or {}) for t in tries),
            sum(t.id in (logged or {}) for t in sel),
        ),
    )


def _n(x: float) -> str:
    return f"{x:,.0f}" if x >= 10 else f"{x:.1f}"


def render(s: Summary) -> str:
    live = (
        f"{s.live} (lines of `{LIVE_TRIES}` on the remote `paper-trail`)"
        if s.live is not None
        else "not counted: no remote `paper-trail` branch was found"
    )
    kinds = ", ".join(f"{k} {n:,}" for k, n in s.by_kind)
    out = [
        "# The bar for a new pick",
        "",
        "Generated by `uv run python -m grimstrade.register` (after `git fetch origin`) from every",
        f"pushed branch's `{TRIES_MD}`; do not edit by hand. The dedup rule is in the docstring",
        "of `src/grimstrade/register.py`. Convention (PROPOSED): every card quotes the",
        "project-wide count and the bar below, next to its own family bar (`docs/DESIGN.md`).",
        "",
        f"Rows through {s.through}. Remote branches with a `{TRIES_MD}`: {s.branches}.",
        "",
        "## Counts",
        "",
        "| What | Count |",
        "|---|---:|",
        f"| Distinct tries, project-wide (`{REGISTER.as_posix()}`) | **{s.tries:,}** |",
        f"| Families (the `Idea` column) | {s.families:,} |",
        f"| Tries without a Sharpe | {s.without_sharpe:,} |",
        f"| Selectable tries (`variant` or `baseline`, period `train`) | {s.selectable:,} |",
        f"| Live strategies | {live} |",
        f"| **N for a new pick** (selectable + live) | **{s.n:,}** |",
        f"| Tries whose shape the harness logged (`{SHAPES.as_posix()}`) | "
        f"{s.logged[0]:,} ({s.logged[1]:,} selectable) |",
        "",
        f"By kind: {kinds}.",
        "",
        f"## The bar for a new pick at N = {s.n:,}",
        "",
        "Deflated Sharpe, difference form (Bailey and Lopez de Prado 2014, as in",
        "`research/dsr-1.md`): a new rule's Sharpe edge d over the current bar (`tsmom12`), with",
        f"standard error SE, passes a DSR of {PASS} when z = d / SE >= {_Z.inv_cdf(PASS):.3f} +",
        "E[max of N standard normals]. Bonferroni (one-sided, alpha 0.05): p <= 0.05 / N.",
        "Correlated trials count as N_eff = rho + (1 - rho) N (appendix A.3)"
        + (
            "; rho and the cluster count are measured (next section)."
            if s.measured
            else ", rho assumed."
        ),
        "",
        "| Trials counted as | N | DSR 0.95: z needed | Edge, close rule (SE "
        f"{SE_CLOSE}) | Edge, far rule (SE {SE_FAR}) | Bonferroni: p below | Bonferroni: z |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for b in s.bar():
        out.append(
            f"| {b.label} | {_n(b.n)} | {b.z_dsr:.2f} | +{b.z_dsr * SE_CLOSE:.2f} | "
            f"+{b.z_dsr * SE_FAR:.2f} | {b.p_bonferroni:.1e} | {b.z_bonferroni:.2f} |"
        )
    out += [
        "",
        "SE: a rule close to `tsmom12` on the primary test (six assets,",
        f"{PRIMARY[0]}..{PRIMARY[1]}), and a far one (review-1's SE against equal weight).",
        "A card on other data or another comparator uses its own SE with the z column.",
        "",
    ]
    if s.measured:
        out += render_measured(s, s.measured)
    out += ["## Against zero", ""]
    if s.v_selectable is None or s.mean_selectable is None:
        out.append("Too few selectable Sharpes for a spread.")
    else:
        out += [
            f"Selectable variants' annual Sharpes: mean {s.mean_selectable:.2f}, variance "
            f"{s.v_selectable:.3f}",
            "(the project-wide spread; cautious, since it mixes data sets).",
            "Annual Sharpe a new rule needs for a deflated Sharpe of 0.95 against zero (normal",
            "returns; fat tails need more):",
            "",
            "| Trials counted as | N | Luck alone, SR0 | Needed, 32 years | 10 years | 5 years |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for b in s.bar():
            sr0 = math.sqrt(s.v_selectable) * max_z(b.n)
            need = [sharpe_needed(b.n, s.v_selectable, d) for d in (11_605, 3_653, 1_826)]
            out.append(
                f"| {b.label} | {_n(b.n)} | {sr0:.2f} | "
                + " | ".join(f"{x:.2f}" for x in need)
                + " |"
            )
    if s.windows:
        out += [
            "",
            "## Spread per test window",
            "",
            "Selectable rows with a Sharpe, by (From, To), windows with at least "
            f"{MIN_WINDOW_ROWS} rows,",
            "largest first (one window can hold several data sets):",
            "",
            "| From | To | Rows | Mean | Variance |",
            "|---|---|---:|---:|---:|",
        ]
        out += [f"| {a} | {b} | {n} | {m:.2f} | {v:.3f} |" for a, b, n, m, v in s.windows]
    return "\n".join(out) + "\n"


def render_measured(s: Summary, m: Measured) -> list[str]:
    head = s.headline()
    a, b = m.window
    out = [
        f"**The bar for a new pick: N = {_n(head.n)} effectively independent trials "
        f"({head.label}): z >= {head.z_dsr:.2f}, an edge over `tsmom12` of "
        f"+{head.z_dsr * SE_CLOSE:.2f} (close rule) to +{head.z_dsr * SE_FAR:.2f} (far rule) on "
        f"the primary test; Bonferroni p <= {head.p_bonferroni:.1e}.**",
        "",
        "## How many independent trials (measured)",
        "",
        f"From `{TRIALS.as_posix()}` and `{MOMENTS.as_posix()}`, written by",
        "`uv run --with numpy python research/register2.py all` (card `research/register-2.md`).",
        f"Tries with a measured record length, skew and kurtosis: {m.rows:,} rows "
        f"({m.selectable:,} of the {s.selectable:,} selectable) and {m.live} live strategies,",
        "from the shape the harness logs with each row (`research/tries-shape.jsonl`), the",
        "research harness (baselines re-simulated, each matching its logged Sharpe) and the",
        "equity curves the harness saved when the try was logged.",
        "",
        f"Correlation sample: {m.sample:,} distinct selectable or live return series that cover "
        f"every week {a}..{b} ({m.weeks:,} weekly returns)"
        + (
            f", at most {m.cap} per family ({m.families} families; first by SHA-256 of "
            f"idea/variant/start, card `research/register-3.md`; uncapped: {m.uncapped[0]:,})."
            if m.cap and m.uncapped
            else "."
        ),
        "",
        "| Estimate | Value | Method |",
        "|---|---:|---|",
        f"| Average pairwise correlation | {m.rho_mean:.2f} (median {m.rho_median:.2f}) | "
        "N_eff = rho + (1 - rho) N, appendix A.3 of Bailey and Lopez de Prado (2014) |",
        f"| ONC clusters | {m.onc_k}{' (at the search cap)' if m.onc_at_cap else ''} of "
        f"{m.sample:,} | Lopez de Prado and Lewis (2019), sections 8.1-8.2: k-means on "
        "sqrt((1 - rho) / 2), best mean/std of silhouettes, recursive re-clustering |",
        f"| Eigenvalue participation ratio | {m.participation:.1f} of {m.sample:,} | "
        "(sum l)^2 / sum l^2, cross-check only |",
    ]
    if m.cluster_var is not None:
        out.append(
            f"| Variance of the clusters' annual Sharpes | {m.cluster_var:.3f} | "
            "minimum-variance portfolio per cluster (section 8.2) |"
        )
    if m.check:
        name, cm, crho, ck = m.check
        out.append(
            f"| Check, window {name} | rho {crho:.2f}, {ck} clusters of {cm:,} | same methods |"
        )
    out += [
        "",
        "The sample is the part of the register whose returns could be rebuilt; the ONC count is",
        "scaled to all N tries by clusters per series (K N / M). The bar uses the more cautious",
        "(larger) of that and A.3 with the measured rho, never more than N.",
        "",
        "Shape of the weekly returns of the measured selectable and live tries: skew median "
        f"{m.skew_median:+.2f} (10th percentile {m.skew_p10:+.2f}), excess kurtosis median "
        f"{m.ek_median:.1f} (90th percentile {m.ek_p90:.1f}).",
        "",
        "## The bar per record length",
        "",
        f"At N = {_n(head.n)}. Edge over `tsmom12`: the SEs above are for the primary test's "
        f"{PRIMARY_WEEKS:,} weeks and scale with 1 / sqrt(weeks) (same correlation with",
        "`tsmom12` assumed). Against zero: annual Sharpe for a deflated Sharpe of 0.95 on weekly",
        "returns (Bailey and Lopez de Prado 2014, eq. 2 with skew and kurtosis), trials' Sharpes",
    ]
    # The larger of the clusters' and the selectable variants' spread: with few clusters the
    # former rests on a handful of numbers (register-2 results).
    v = max((x for x in (m.cluster_var, s.v_selectable) if x is not None), default=None)
    if v is None:
        return [*out, "spread unknown: no table.", ""]
    out += [
        f"spread with variance {v:.3f} (the larger of the clusters' and the selectable",
        "variants' spread).",
        "",
        "| Years | Weeks | Edge, close rule | Edge, far rule | Against zero: normal | "
        "median shape | fat tail (p10 skew, p90 kurtosis) |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for years in YEARS:
        w = round(years * WEEKS_PER_YEAR)
        scale = math.sqrt(PRIMARY_WEEKS / w)
        need = [
            sharpe_needed(head.n, v, w, WEEKS_PER_YEAR, sk, ek)
            for sk, ek in ((0.0, 0.0), (m.skew_median, m.ek_median), (m.skew_p10, m.ek_p90))
        ]
        out.append(
            f"| {years} | {w:,} | +{head.z_dsr * SE_CLOSE * scale:.2f} | "
            f"+{head.z_dsr * SE_FAR * scale:.2f} | " + " | ".join(f"{x:.2f}" for x in need) + " |"
        )
    return [*out, ""]


def regenerate(repo: Path) -> Summary:
    """Rewrite the register and BAR.md under `repo` from every remote branch. Returns the
    summary BAR.md was written from."""
    per_branch = branch_lines(repo)
    old = (
        [read_register((repo / REGISTER).read_text(), str(REGISTER))]
        if (repo / REGISTER).exists()
        else []
    )
    for ref in ledger.research_refs(repo, REMOTES):
        text = _show(repo, ref, REGISTER.as_posix())
        if text:
            old.append(read_register(text, f"{ref}:{REGISTER.as_posix()}"))
    tries = merge(*old, census(per_branch))
    measured = read_measured(repo, {t.id for t in tries})
    logged = logged_shapes(repo, tries)
    summary = summarize(tries, live_strategies(repo), len(per_branch), measured, logged)
    (repo / REGISTER).parent.mkdir(parents=True, exist_ok=True)
    (repo / REGISTER).write_text("".join(t.to_json() + "\n" for t in tries))
    (repo / BAR).write_text(render(summary))
    return summary


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    p.add_argument("--repo", type=Path, default=Path("."), help="code checkout (fetched)")
    args = p.parse_args(argv)
    s = regenerate(args.repo)
    print(
        f"{REGISTER.as_posix()}: {s.tries:,} tries ({s.selectable:,} selectable, "
        f"{s.live if s.live is not None else 'no'} live); N for a new pick {s.n:,}; "
        f"{BAR.as_posix()} written."
    )


if __name__ == "__main__":
    main()
