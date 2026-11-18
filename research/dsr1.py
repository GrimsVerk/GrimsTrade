"""dsr-1: every try the project has logged, on every branch, counted once.

    git fetch origin
    python research/dsr1.py census      # markdown tables for research/dsr-1.md

Each research lane appends rows to `research/tries.md` on its own branch, and branches share
rows through their ancestry. A row is the same try on two branches when its line is identical.
A line that appears k times on one branch (a re-run logged twice) counts k times; across
branches the count is the largest k seen on any branch, so shared history is not double counted.

Stdlib only; reads git objects, runs no backtest, writes nothing.
"""

from __future__ import annotations

import json
import math
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass

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


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "census"
    if cmd == "census":
        census()
    else:
        sys.exit(f"unknown command {cmd!r}")


if __name__ == "__main__":
    main()
