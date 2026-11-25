"""reconcile-1: does the live paper record match what the gym would have done?

    uv run python research/lib/reconcile1.py --work <scratch dir> [--json out.json]

Reads the `paper-trail` branch (default ref `origin/paper-trail` of the repo in the working
directory; `--ref` takes any commit of it, a sha too, e.g. to rerun on an older state of the
record) into a private clone under `--work`; nothing on the branch is changed. Tolerance and
mismatch classes are fixed in `research/reconcile-1.md`, written before any number.

Four checks per live book:

1. weights: ledger line against the strategy re-run at the line's own time on the bars stored in
   that run's commit, on the bars stored now, and at the backtest's 22:30 on the due day;
2. snapshot: `state/portfolio.json` of each commit against a replay of that commit's record by
   the code that ran (old gym, in a subprocess) and by the gym on `main` now;
3. day by day: the live book (`report.live_results`) against `gym.backtest` over the same days,
   with a third book (the backtest deciding at the live runs' own times) to tell (a) apart;
4. fills: every live fill checked against the bars without the gym (open, price, fee, cash).

The pure functions below take plain data, so the tests build small synthetic records.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any

from grimstrade import data, gym, ledger, report
from grimstrade.data import UNIVERSE, History, open_time, visible_history
from grimstrade.gym import Decision, Result

# --- tolerance (research/reconcile-1.md: "floating point only") ---

REL = 1e-9
CENT = 0.005


def same(a: float, b: float) -> bool:
    return abs(a - b) <= REL * max(1.0, abs(a), abs(b))


def same_cents(written: float, computed: float) -> bool:
    """A value the runner rounded to cents against the full-precision value."""
    return abs(written - computed) <= CENT + REL * abs(computed)


def same_weights(a: Mapping[str, float], b: Mapping[str, float]) -> bool:
    return all(same(a.get(s, 0.0), b.get(s, 0.0)) for s in set(a) | set(b))


def weight_gap(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    return max((abs(a.get(s, 0.0) - b.get(s, 0.0)) for s in set(a) | set(b)), default=0.0)


# The run due on day D starts between 12:00 UTC on D and 12:00 UTC on D+1 (DECISIONS 2026-11-24:
# scheduled 22:30 D, started 02:01-06:13 UTC D+1).
DUE_SHIFT = timedelta(hours=12)


def due_day(t: datetime) -> date:
    return (t - DUE_SHIFT).date()


def backtest_time(d: date) -> datetime:
    return datetime.combine(d, gym.DECIDE_AT, tzinfo=UTC)


# Classes, worst first (a day with several reasons gets the worst).
BUG, DATA, RULE, SCHEDULE = "c", "b", "d", "a"
ORDER = (BUG, DATA, RULE, SCHEDULE)


def worst(classes: Iterable[str]) -> str | None:
    got = set(classes)
    return next((c for c in ORDER if c in got), None)


@dataclass(frozen=True)
class Finding:
    book: str
    day: str  # UTC day (fills, cash, equity) or due day (weights) or run time (snapshot)
    check: str  # weights / snapshot / day / fill
    cls: str  # a b c d
    what: str


# --- 1. weights ---


def classify_weights(
    ledger_w: Mapping[str, float],
    at_run: Mapping[str, float],
    stored_now: Mapping[str, float],
    at_2230: Mapping[str, float] | None,
) -> str | None:
    """The class of the gap between a ledger line's weights and the backtest's for its due day
    (None: they match). `at_run`: the strategy at the line's time on the bars the run had;
    `stored_now`: the same on the bars stored now; `at_2230`: at 22:30 on the due day (None: the
    backtest makes no decision that day)."""
    if not same_weights(ledger_w, at_run):
        return BUG  # the run did not write what its strategy gives on its own bars
    if not same_weights(at_run, stored_now):
        return DATA  # a bar the run did not have changes the answer
    if at_2230 is not None and not same_weights(stored_now, at_2230):
        return SCHEDULE  # only the decision time differs
    return None


# --- 3. day by day ---


@dataclass(frozen=True)
class Day:
    fills: tuple[tuple[str, float, float, float], ...]  # (symbol, qty, price, fee) by time
    cash: float
    equity: float


def cash_flows(fills: Iterable[gym.Fill]) -> float:
    return sum(-f.qty * f.price - f.fee for f in fills)


def day_rows(res: Result) -> dict[date, Day]:
    """Fills, end-of-day cash and equity of a replay, per UTC day of `res.equity`. Cash is
    rebuilt from the fills and paid distributions (no cash interest on the record yet: the
    trail has no `data/rates.csv`; `check_fills` refuses a result that earned some)."""
    by_day: dict[date, list[gym.Fill]] = {}
    for f in res.fills:
        by_day.setdefault(f.time.date(), []).append(f)
    income: dict[date, float] = {}
    for t, _, paid in res.income:
        income[t.date()] = income.get(t.date(), 0.0) + paid
    out = {}
    cash = res.start_cash
    for d, eq in res.equity:
        todays = by_day.get(d, [])
        cash += cash_flows(todays) + income.get(d, 0.0)
        out[d] = Day(tuple((f.symbol, f.qty, f.price, f.fee) for f in todays), cash, eq)
    return out


def same_day(a: Day, b: Day) -> bool:
    if [f[0] for f in a.fills] != [f[0] for f in b.fills]:
        return False
    for fa, fb in zip(a.fills, b.fills, strict=True):
        if not all(same(x, y) for x, y in zip(fa[1:], fb[1:], strict=True)):
            return False
    return same(a.cash, b.cash) and same(a.equity, b.equity)


def describe_gap(a: Day, b: Day) -> str:
    parts = []
    if not all(
        fa[0] == fb[0] and all(same(x, y) for x, y in zip(fa[1:], fb[1:], strict=True))
        for fa, fb in zip(a.fills, b.fills, strict=False)
    ) or len(a.fills) != len(b.fills):
        fa = ", ".join(f"{s} {q:+.6g}@{p:.6g}" for s, q, p, _ in a.fills) or "none"
        fb = ", ".join(f"{s} {q:+.6g}@{p:.6g}" for s, q, p, _ in b.fills) or "none"
        parts.append(f"fills live [{fa}] vs gym [{fb}]")
    if not same(a.cash, b.cash):
        parts.append(f"cash {a.cash:.2f} vs {b.cash:.2f}")
    if not same(a.equity, b.equity):
        parts.append(f"equity {a.equity:.2f} vs {b.equity:.2f}")
    return "; ".join(parts)


@dataclass
class BookDays:
    days: int = 0
    matched: int = 0
    by_class: dict[str, int] = field(default_factory=dict)
    max_equity_gap: float = 0.0
    max_equity_gap_day: str = ""
    findings: list[Finding] = field(default_factory=list)


def compare_days(
    book: str,
    live: Result,
    same_times: Result,
    backtest: Result,
    weight_classes: Mapping[datetime, str],
) -> BookDays:
    """Day-by-day live against backtest. `same_times`: the backtest's strategy deciding at the
    live decisions' own times on today's bars; `weight_classes`: (b)/(c) classes of live
    decisions by the time they count from. A day where live and `same_times` already differ is
    put down to the worst (b)/(c) weight class in force by then (none: an unexplained gap, (c));
    otherwise, where `same_times` and the backtest differ, to the schedule (a)."""
    lv, st, bt = day_rows(live), day_rows(same_times), day_rows(backtest)
    out = BookDays()
    for d in sorted(set(lv) & set(bt)):
        out.days += 1
        gap = abs(lv[d].equity - bt[d].equity)
        if gap > out.max_equity_gap:
            out.max_equity_gap, out.max_equity_gap_day = gap, d.isoformat()
        if same_day(lv[d], bt[d]):
            out.matched += 1
            continue
        end = datetime.combine(d + timedelta(days=1), time(0, 0), tzinfo=UTC)
        if d not in st or not same_day(lv[d], st[d]):
            cls = worst(c for t, c in weight_classes.items() if t < end) or BUG
            why = "live weights differ" if cls != BUG or weight_classes else "unexplained"
        else:
            cls, why = SCHEDULE, "decision time only"
        out.by_class[cls] = out.by_class.get(cls, 0) + 1
        out.findings.append(
            Finding(book, d.isoformat(), "day", cls, f"{why}: {describe_gap(lv[d], bt[d])}")
        )
    return out


# --- 4. fills, without the gym ---


def in_force_at(decisions: Sequence[Decision], t: datetime) -> Decision | None:
    """The newest decision that counts from before `t` (the gym orders a decision after an open
    at the same instant)."""
    before = [d for d in decisions if d.time < t]
    return before[-1] if before else None


def check_fills(
    book: str,
    res: Result,
    decisions: Sequence[Decision],
    history: History,
    costs: Mapping[str, gym.Costs] = gym.COSTS,
) -> list[Finding]:
    """Each fill against the bars and the cost rules, with no gym code: (1) it is at the open of
    a stored bar of its asset; (2) a decision counted from before it; (3) price = open x (1 +/-
    slip); (4) fee = quantity x price x the tier rate for the asset class's fills in the 30 days
    before; (5) the cash it leaves, and the end cash, add up. Every problem is class (c)."""
    out: list[Finding] = []
    if any(g != 0 for g in res.cash_growth):
        raise ValueError("check_fills does not model cash interest (the trail has no rates)")
    opens = {
        (s, open_time(UNIVERSE[s], b.date)): b.open for s, bars in history.items() for b in bars
    }
    for i, f in enumerate(res.fills):
        day = f.time.date().isoformat()
        cls = UNIVERSE[f.symbol]

        def bad(what: str, day: str = day, f: gym.Fill = f) -> None:
            out.append(Finding(book, day, "fill", BUG, f"{f.symbol} {f.qty:+.6g}: {what}"))

        px = opens.get((f.symbol, f.time))
        if px is None:
            bad(f"at {f.time:%Y-%m-%d %H:%M}, not the open of a stored bar")
            continue
        if in_force_at(decisions, f.time) is None:
            bad("no decision counted from before this fill")
        c = costs[cls]
        want_px = px * (1 + c.slip if f.qty > 0 else 1 - c.slip)
        if not same(f.price, want_px):
            bad(f"price {f.price!r}, rules give {want_px!r}")
        since = f.time - gym.VOLUME_WINDOW
        volume = sum(
            abs(g.qty) * g.price
            for g in res.fills[:i]
            if since < g.time < f.time and UNIVERSE[g.symbol] == cls
        )
        want_fee = abs(f.qty) * f.price * c.fee_at(volume)
        if not same(f.fee, want_fee):
            bad(f"fee {f.fee!r}, rules give {want_fee!r}")
    cash = res.start_cash + cash_flows(res.fills) + sum(p for _, _, p in res.income)
    if not same(cash, res.cash):
        out.append(Finding(book, "end", "fill", BUG, f"cash {res.cash!r}, fills give {cash!r}"))
    if cash < -REL * res.start_cash:
        out.append(Finding(book, "end", "fill", BUG, f"cash below zero: {cash!r}"))
    return out


def late_bars(
    history: History, stored_at: Sequence[tuple[datetime, Mapping[str, int]]]
) -> list[tuple[str, str, str]]:
    """(run time, symbol, bar day) of each bar that had closed by a run but was not yet stored in
    that run's commit (bars are append-only, so the first n stored then are the first n now):
    a bar a backtest on today's bars sees and the run did not, class (b)."""
    out = []
    for run_at, counts in stored_at:
        for sym, bars in history.items():
            seen = len(data.visible(bars, UNIVERSE[sym], run_at))
            for b in bars[counts.get(sym, 0) : seen]:
                out.append((run_at.isoformat(), sym, b.date.isoformat()))
    return out


# --- 2. snapshot ---

SnapshotRow = Mapping[str, Any]  # as in state/portfolio.json


def snapshot_of(res: Result) -> dict[str, Any]:
    """What the runner writes for one book (`run_daily.run`), unrounded."""
    return {
        "cash": res.cash,
        "positions": {s: q for s, q in res.positions.items() if q},
        "equity": res.equity[-1][1] if res.equity else gym.START_CASH,
        "marked_on": res.equity[-1][0].isoformat() if res.equity else None,
        "fills": len(res.fills),
    }


def snapshot_gaps(written: SnapshotRow, computed: SnapshotRow) -> list[str]:
    gaps = []
    for key in ("cash", "equity"):
        if not same_cents(written[key], computed[key]):
            gaps.append(f"{key} {written[key]} vs {computed[key]:.4f}")
    if written["fills"] != computed["fills"] or written["marked_on"] != computed["marked_on"]:
        gaps.append(
            f"fills/marked {written['fills']}/{written['marked_on']} vs "
            f"{computed['fills']}/{computed['marked_on']}"
        )
    wp, cp = written["positions"], computed["positions"]
    for s in sorted(set(wp) | set(cp)):
        if not same(wp.get(s, 0.0), cp.get(s, 0.0)):
            gaps.append(f"{s} {wp.get(s, 0.0)!r} vs {cp.get(s, 0.0)!r}")
    return gaps


def classify_snapshot(
    written: SnapshotRow, by_old_code: SnapshotRow | None, by_main: SnapshotRow
) -> tuple[str | None, list[str]]:
    """(c) when the code that ran does not reproduce what it wrote, (d) when it does and the gym
    on `main` gives something else, None when all agree."""
    if by_old_code is not None and (gaps := snapshot_gaps(written, by_old_code)):
        return BUG, gaps
    if gaps := snapshot_gaps(written, by_main):
        return RULE, gaps
    return None, []


# --- the run over the real record ---

OLD_CODE_SCRIPT = """
import json, sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from grimstrade import data, report
root = Path(sys.argv[2])
res = report.live_results(root, data.load_all(root))
out = {n: {"cash": r.cash, "positions": {s: q for s, q in r.positions.items() if q},
           "equity": r.equity[-1][1] if r.equity else 10000.0,
           "marked_on": r.equity[-1][0].isoformat() if r.equity else None,
           "fills": len(r.fills)} for n, r in res.items()}
print(json.dumps(out))
"""


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout


def code_src(repo: Path, commit: str, work: Path) -> Path:
    """`src/` of `commit`, unpacked once under `work`."""
    dest = work / f"code-{commit[:12]}"
    if not dest.exists():
        dest.mkdir(parents=True)
        tar = subprocess.run(
            ["git", "archive", commit, "src"], cwd=repo, check=True, capture_output=True
        ).stdout
        tmp = dest / "src.tar"
        tmp.write_bytes(tar)
        with tarfile.open(tmp) as t:
            t.extractall(dest, filter="data")
        tmp.unlink()
    return dest / "src"


def old_snapshot(src: Path, root: Path) -> dict[str, Any]:
    out = subprocess.run(
        [sys.executable, "-c", OLD_CODE_SCRIPT, str(src), str(root)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    result: dict[str, Any] = json.loads(out)
    return result


def code_of_run(repo: Path, rows: Sequence[Mapping[str, Any]], run_at: datetime) -> str:
    """The commit whose code ran: the `code` field of the run's lines, else the newest `main`
    commit (first-parent) at or before the run."""
    codes = {r["code"] for r in rows if r.get("code")}
    if len(codes) == 1:
        return codes.pop()
    return git(
        repo, "rev-list", "-1", "--first-parent", f"--before={run_at.isoformat()}", "origin/main"
    ).strip()


Strategies = Mapping[str, Callable[[History], tuple[dict[str, float], str]]]


def run(repo: Path, work: Path, ref: str, live: Strategies) -> dict[str, Any]:
    clone = work / "clone"
    if clone.exists():
        shutil.rmtree(clone)
    git(work, "clone", "-q", "--no-checkout", str(repo.resolve()), str(clone))
    # Any commit-ish of `repo` (a remote-tracking or local branch, a tag, a sha): resolved there,
    # then fetched by its sha.
    sha = git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").strip()
    git(clone, "fetch", "-q", str(repo.resolve()), f"+{sha}:refs/heads/trail")
    commits = git(clone, "rev-list", "--reverse", "trail").split()
    findings: list[Finding] = []
    at_run: dict[tuple[str, str], dict[str, float]] = {}  # (book, line time) -> weights
    snapshots: list[dict[str, Any]] = []
    stored_at: list[tuple[datetime, dict[str, int]]] = []  # bars per symbol in each run's commit
    seen_rows = 0
    for k, commit in enumerate(commits):
        run_at = datetime.fromtimestamp(int(git(clone, "log", "-1", "--format=%ct", commit)), UTC)
        if k == 0:  # the first run wrote into a branch with no commits: nothing committed yet
            root = work / "root0"
            if root.exists():
                shutil.rmtree(root)
            root.mkdir()
            tar = subprocess.run(
                ["git", "archive", commit], cwd=clone, check=True, capture_output=True
            ).stdout
            (work / "root0.tar").write_bytes(tar)
            with tarfile.open(work / "root0.tar") as t:
                t.extractall(root, filter="data")
        else:  # the parent's commit, with this run's files staged but not committed (as at run)
            root = clone
            git(clone, "checkout", "-q", "-f", "--detach", commits[k - 1])
            git(clone, "clean", "-q", "-fdx")
            git(clone, "checkout", "-q", commit, "--", ".")
        history = data.load_all(root)
        stored_at.append((run_at, {s: len(b) for s, b in history.items()}))
        rows = ledger.decisions(root)
        new = rows[seen_rows:]
        seen_rows = len(rows)
        for r in new:
            t = ledger.parse_time(r["time"])
            w, _ = live[r["strategy"]](visible_history(history, t))
            at_run[(r["strategy"], r["time"])] = dict(w)
        state_file = root / "state" / "portfolio.json"
        written = json.loads(state_file.read_text()) if state_file.exists() else {}
        old_src = code_src(repo, code_of_run(repo, new, run_at), work)
        by_old = old_snapshot(old_src, root)
        by_main = {n: snapshot_of(r) for n, r in report.live_results(root, history).items()}
        for book, row in sorted(written.items()):
            cls, gaps = classify_snapshot(row, by_old.get(book), by_main[book])
            snapshots.append(
                {
                    "commit": commit[:10],
                    "run": run_at.isoformat(),
                    "book": book,
                    "code": old_src.parent.name[5:],
                    "class": cls,
                    "gaps": gaps,
                }
            )
            if cls:
                findings.append(Finding(book, run_at.isoformat(), "snapshot", cls, "; ".join(gaps)))
    # The record as it stands, every line committed.
    git(clone, "checkout", "-q", "-f", "--detach", commits[-1])
    git(clone, "clean", "-q", "-fdx")
    history = data.load_all(clone)
    counted, late_lines = ledger.in_force(clone)
    late = late_bars(history, stored_at)
    findings += [
        Finding(s, d, "bars", DATA, f"visible at run {t}, stored later") for t, s, d in late
    ]
    live_res = report.live_results(clone, history)
    books: dict[str, Any] = {}
    for book in sorted(live_res):
        mine = [(t, r) for t, r in counted if r["strategy"] == book]
        decs = [Decision(t, r["weights"]) for t, r in mine]
        strat = live[book]
        first, last = due_day(mine[0][0]), due_day(ledger.parse_time(mine[-1][1]["time"]))
        bt_decs = gym.backtest(strat, history, first, last)
        bt_by_day = {d.time.date(): d.weights for d in bt_decs}
        now_w = {
            r["time"]: dict(strat(visible_history(history, ledger.parse_time(r["time"])))[0])
            for _, r in mine
        }
        weight_classes: dict[datetime, str] = {}
        per_due: dict[date, tuple[datetime, dict[str, Any]]] = {}
        for t, r in mine:
            per_due[due_day(ledger.parse_time(r["time"]))] = (t, r)  # the last line of the day
            had = at_run[(book, r["time"])]
            c = classify_weights(r["weights"], had, now_w[r["time"]], None)
            if c:
                weight_classes[t] = c
                gap = max(weight_gap(r["weights"], had), weight_gap(had, now_w[r["time"]]))
                findings.append(Finding(book, r["time"], "weights", c, f"gap {gap:.3g}"))
        w_days, w_match, w_class = 0, 0, {}
        for d, (_, r) in sorted(per_due.items()):
            w_days += 1
            c = classify_weights(
                r["weights"], at_run[(book, r["time"])], now_w[r["time"]], bt_by_day.get(d)
            )
            if c is None:
                w_match += 1
            else:
                w_class[c] = w_class.get(c, 0) + 1
                if c == SCHEDULE:
                    gap = weight_gap(now_w[r["time"]], bt_by_day[d])
                    findings.append(
                        Finding(
                            book,
                            d.isoformat(),
                            "weights",
                            c,
                            f"live run saw crypto bar {d}: gap {gap:.3g}",
                        )
                    )
        same_t = gym.simulate([Decision(t, now_w[r["time"]]) for t, r in mine], history)
        bt = gym.simulate(bt_decs, history)
        days = compare_days(book, live_res[book], same_t, bt, weight_classes)
        fill_problems = check_fills(book, live_res[book], decs, history)
        fill_problems += [
            Finding(f.book, f.day, f.check, f.cls, "backtest: " + f.what)
            for f in check_fills(book, bt, bt_decs, history)
        ]
        findings += days.findings + fill_problems
        books[book] = {
            "decisions": len(mine),
            "weights": {"due_days": w_days, "matched": w_match, "by_class": w_class},
            "days": days.days,
            "matched": days.matched,
            "by_class": days.by_class,
            "max_equity_gap": days.max_equity_gap,
            "max_equity_gap_day": days.max_equity_gap_day,
            "live_equity": live_res[book].equity[-1][1],
            "backtest_equity": bt.equity[-1][1],
            "live_fills": len(live_res[book].fills),
            "backtest_fills": len(bt.fills),
            "fill_problems": len(fill_problems),
        }
    snap_classes: dict[str, int] = {}
    for s in snapshots:
        key = s["class"] or "match"
        snap_classes[key] = snap_classes.get(key, 0) + 1
    return {
        "trail_head": commits[-1][:10],
        "late_bars": len(late),
        "late_ledger_lines": late_lines,
        "runs": len(commits),
        "books": books,
        "snapshots": {"rows": len(snapshots), "by_class": snap_classes, "detail": snapshots},
        "findings": [asdict(f) for f in findings],
    }


def render(result: Mapping[str, Any]) -> str:
    lines = [
        "| Book | Decisions | Due days: weights matched / (a) | Days | Matched | (a) | (b) | (c) "
        "| Max equity gap (USD, day) | Live / backtest equity | Fill problems |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for book, b in result["books"].items():
        w = b["weights"]
        lines.append(
            f"| `{book}` | {b['decisions']} | {w['due_days']}: {w['matched']} / "
            f"{w['by_class'].get('a', 0)} | {b['days']} | {b['matched']} | "
            f"{b['by_class'].get('a', 0)} | {b['by_class'].get('b', 0)} | "
            f"{b['by_class'].get('c', 0)} | {b['max_equity_gap']:.2f} ({b['max_equity_gap_day']}) "
            f"| {b['live_equity']:.2f} / {b['backtest_equity']:.2f} | {b['fill_problems']} |"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path("."))
    p.add_argument("--work", type=Path, required=True, help="scratch folder (a clone goes here)")
    p.add_argument(
        "--ref",
        default="origin/paper-trail",
        help="the record to read: any commit of --repo (branch, remote branch, tag or sha)",
    )
    p.add_argument("--json", type=Path)
    args = p.parse_args(argv)
    from grimstrade.strategies import LIVE

    args.work.mkdir(parents=True, exist_ok=True)
    result = run(args.repo, args.work.resolve(), args.ref, LIVE)
    if args.json:
        args.json.write_text(json.dumps(result, indent=1, default=str) + "\n")
    print(render(result))
    print("snapshots:", result["snapshots"]["by_class"])
    for f in result["findings"]:
        print(f"[{f['cls']}] {f['check']} {f['book']} {f['day']}: {f['what']}")


if __name__ == "__main__":
    main()
