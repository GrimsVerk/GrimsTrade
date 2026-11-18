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

from grimstrade import ledger, stats

TRIES_MD = ledger.RESEARCH_TRIES
REGISTER = Path(ledger.RESEARCH_REGISTER)
BAR = REGISTER.parent / "BAR.md"
LIVE_TRIES = "ledger/tries.jsonl"  # on the record branch
REMOTES = ("refs/remotes",)
PRIMARY = ("1994-02-01", "2025-11-09")  # the six-asset train test `tsmom12` scored 1.05 on
DAYS_PER_YEAR = 365
PASS = 0.95  # deflated Sharpe needed
ALPHA = 0.05  # one-sided, for Bonferroni
# Standard error of a new rule's Sharpe edge over `tsmom12` on the primary test (dsr-1): a rule
# close to it (returns highly correlated) and a far one (review-1's SE against equal weight).
SE_CLOSE, SE_FAR = 0.065, 0.12
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


def sharpe_needed(n: float, v_annual: float, days: int) -> float:
    """Annual Sharpe a rule needs over `days` (normal returns) for a deflated Sharpe of 0.95
    against zero, when n trials' annual Sharpes spread with variance `v_annual`."""
    v = max(v_annual / DAYS_PER_YEAR, stats.null_sharpe_variance(days))
    sr0 = math.sqrt(v) * max_z(n)
    lo, hi = sr0, sr0 + 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        psr = stats.probabilistic_sharpe(stats.Moments(days, mid, 0.0, 3.0), sr0)
        lo, hi = (lo, mid) if psr >= PASS else (mid, hi)
    return hi * math.sqrt(DAYS_PER_YEAR)


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

    @property
    def n(self) -> int:
        """N for a new pick: selectable rows plus the live strategies."""
        return self.selectable + (self.live or 0)

    def bar(self) -> list[BarRow]:
        rows = []
        for rho in RHOS:
            n = effective(self.n, rho)
            p = ALPHA / max(n, 1.0)
            label = "independent" if rho == 0 else f"rho {rho}"
            rows.append(BarRow(label, n, _Z.inv_cdf(PASS) + max_z(n), p, _Z.inv_cdf(1 - p)))
        return rows


def summarize(tries: list[Try], live: int | None, branches: int) -> Summary:
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
        "",
        f"By kind: {kinds}.",
        "",
        f"## The bar for a new pick at N = {s.n:,}",
        "",
        "Deflated Sharpe, difference form (Bailey and Lopez de Prado 2014, as in",
        "`research/dsr-1.md`): a new rule's Sharpe edge d over the current bar (`tsmom12`), with",
        f"standard error SE, passes a DSR of {PASS} when z = d / SE >= {_Z.inv_cdf(PASS):.3f} +",
        "E[max of N standard normals]. Bonferroni (one-sided, alpha 0.05): p <= 0.05 / N.",
        "Correlated trials count as N_eff = rho + (1 - rho) N (appendix A.3).",
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
        "## Against zero",
        "",
    ]
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
    summary = summarize(tries, live_strategies(repo), len(per_branch))
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
