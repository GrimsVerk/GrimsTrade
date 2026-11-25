"""Forward-only shadow registry: a rule is frozen now and judged only on what happens after.

Research only. The daily runner never imports this; `python -m grimstrade.forward` is a separate
offline command (design: `docs/forward-registry.md`).

- `research/forward/registry.jsonl`: one line per frozen rule, append-only (git history is checked
  with `ledger.check_append_only`). A line holds the rule's id, the sha256 of each code file, its
  parameters and data source, one hash over all three (`rule_hash`), and the test written down in
  advance: metric, one-sided alpha, power, the effect assumed true, observations per year, and
  the minimum sample that effect needs (`min_sample`). A frozen id is never frozen again; a
  changed rule is a new id.
- A rule counts as frozen from the later of its own `frozen_at` and the first commit on HEAD's
  first-parent chain that holds its line (`ledger.recorded_at(..., first_parent=True)`): a line
  merged from a side branch counts from the merge, whatever date the side commit claims. An
  uncommitted line is not frozen: nothing proves when it was written.
- `research/forward/obs/<id>.jsonl`: observations, append-only like the registry (`read_obs`
  runs the same history check: a committed line changed or removed stops the score).
- Observations (`{"start", "end", "value", "rule_hash"}`, one per bar or event) are scored only if
  their holding period starts at or after that time and they carry the frozen `rule_hash`.
  Anything else is refused, not skipped: a pre-freeze bar in a forward file means someone mixed
  backtest into it.
- The verdict is read once, on exactly the first `min_sample` observations. Before that the
  score is "waiting"; later observations are shown but never change the verdict (no peeking until
  the p-value looks good).
- The `mean` and `sharpe` verdicts use a dependence-robust standard error (`SE_RULE`, DECISIONS
  2026-11-25): Bartlett long-run variance over one year of lags, p-value from a Student-t
  approximation to its fixed-b distribution. Weekly strategy returns are serially dependent; an
  iid standard error rejected a true null 4-9% of the time at nominal 2.5% (evalue-forward-1).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import NormalDist
from typing import Any

from grimstrade import ledger, stats

REGISTRY = Path("research/forward/registry.jsonl")
CANDIDATES = Path("research/forward/candidates.jsonl")
METRICS = ("sharpe", "mean", "win_rate")
SE_RULE = "bartlett-1y"  # recorded on each new line; the rule lives in `hac_t` and `lag`
_N = NormalDist()


class ForwardError(Exception):
    pass


class AlreadyFrozen(ForwardError):
    """The id is in the registry already: a changed rule needs a new id."""


class HashMismatch(ForwardError):
    """Code, parameters or data source differ from what was frozen."""


class LookAhead(ForwardError):
    """An observation starts before the rule was frozen."""


class NotFrozen(ForwardError):
    """The rule has no committed freeze line, so there is no proven freeze time."""


class MissingFreezeTime(ForwardError):
    """A registry line has no valid `frozen_at`: it was not written by `freeze` (a proposal
    copied in, or a hand edit), so nothing says when it was meant to count from."""


# --- the test written down at freeze, and the sample it needs ---


@dataclass(frozen=True)
class Plan:
    """A one-sided test fixed in advance.

    metric: "sharpe" (per-period mean / sd of the values; `effect` is the annual Sharpe),
            "mean" (mean of per-event values; `effect` in the values' unit, `sd` their sd),
            "win_rate" (share of events with value > 0, against 1/2; `effect` the true share).
    per_year: observations per year (52 weekly bars, 8 FOMC meetings, ...), for years needed.
    """

    metric: str
    effect: float
    per_year: float
    alpha: float = 0.025
    power: float = 0.8
    sd: float | None = None
    skew: float = 0.0
    kurtosis: float = 3.0  # raw, 3 for a normal distribution
    lrv: float = 1.0  # long-run variance / variance assumed true (train record's, at least 1)

    def __post_init__(self) -> None:
        if self.metric not in METRICS:
            raise ValueError(f"metric must be one of {METRICS}, not {self.metric!r}")
        if not (0 < self.alpha < 0.5 and 0.5 <= self.power < 1):
            raise ValueError("need 0 < alpha < 0.5 and 0.5 <= power < 1")
        if self.per_year <= 0:
            raise ValueError("per_year must be positive")
        if self.metric == "mean" and (self.sd is None or self.sd <= 0):
            raise ValueError("the mean metric needs the values' sd")
        if self.metric == "win_rate" and not 0.5 < self.effect < 1:
            raise ValueError("a win rate to detect must be between 1/2 and 1")
        if self.metric != "win_rate" and self.effect <= 0:
            raise ValueError("the effect to detect must be positive (one-sided test)")
        if not self.lrv >= 1:
            raise ValueError("lrv (long-run variance ratio) must be at least 1; write 1 if lower")


def _z(alpha: float, power: float) -> float:
    return _N.inv_cdf(1 - alpha) + _N.inv_cdf(power)


# --- the dependence-robust test (DECISIONS 2026-11-25, card research/cards/forward-se-1.md) ---


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction of the incomplete beta function (modified Lentz)."""
    tiny = 1e-300
    c, d = 1.0, 1 - (a + b) * x / (a + 1)
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 10_000):
        for num in (
            m * (b - m) * x / ((a + 2 * m - 1) * (a + 2 * m)),
            -(a + m) * (a + b + m) * x / ((a + 2 * m) * (a + 2 * m + 1)),
        ):
            d = 1 + num * d
            d = 1 / (d if abs(d) > tiny else tiny)
            c = 1 + num / c
            c = c if abs(c) > tiny else tiny
            h *= d * c
        if abs(d * c - 1) < 1e-15:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    log_front = (
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)
    )
    if x < (a + 1) / (a + b + 2):
        return math.exp(log_front) * _betacf(a, b, x) / a
    return 1 - math.exp(log_front) * _betacf(b, a, 1 - x) / b


def t_sf(t: float, nu: float) -> float:
    """P(T > t) for Student's t with `nu` (> 0, not necessarily whole) degrees of freedom."""
    if nu > 1e7:
        return 1 - _N.cdf(t)
    tail = 0.5 * _betainc(nu / 2, 0.5, nu / (nu + t * t))
    return tail if t >= 0 else 1 - tail


def t_ppf(q: float, nu: float) -> float:
    """The `q` quantile of Student's t (bisection on `t_sf`), q in (0.5, 1)."""
    lo, hi = 0.0, 1.0
    while t_sf(hi, nu) > 1 - q:
        hi *= 2
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if t_sf(mid, nu) > 1 - q else (lo, mid)
    return (lo + hi) / 2


def lag(n: int, per_year: float) -> int:
    """Bartlett lags for a window of `n` observations: one year of them, at most n / 4."""
    q = max(1, round(per_year))
    return max(0, min(q - 1, n // 4))


def _ref(n: int, lags: int) -> tuple[float, float]:
    """(c, nu): T * sqrt(c) is about Student-t with nu degrees of freedom. Fixed-b (Kiefer and
    Vogelsang 2005): the Bartlett estimator's mean is c = 1 - b + b^2 / 3 of the true long-run
    variance at b = lags / n, its variance 4b / 3 (Andrews 1991), so nu = 1.5 / b."""
    if lags == 0:
        return 1.0, n - 1.0
    b = lags / n
    return 1 - b + b * b / 3, 1.5 / b


def long_run_variance(values: Sequence[float], lags: int) -> float:
    """Bartlett (Newey-West) long-run variance, scaled by n / (n - 1): with 0 lags it is the
    sample variance."""
    n = len(values)
    mean = math.fsum(values) / n
    d = [v - mean for v in values]
    w = math.fsum(x * x for x in d) / n
    for j in range(1, lags + 1):
        w += 2 * (1 - j / (lags + 1)) * math.fsum(d[t] * d[t - j] for t in range(j, n)) / n
    return w * n / (n - 1)


def hac_t(values: Sequence[float], per_year: float) -> tuple[float, float] | None:
    """(T, one-sided p) for "mean > 0" with the Bartlett one-year long-run variance; None under 2
    values or with no variation."""
    n = len(values)
    if n < 2:
        return None
    lags = lag(n, per_year)
    w = long_run_variance(values, lags)
    if not w > 0:
        return None
    t = (math.fsum(values) / n) / math.sqrt(w / n)
    c, nu = _ref(n, lags)
    return t, t_sf(t * math.sqrt(c), nu)


def critical(n: int, per_year: float, alpha: float) -> float:
    """The value T must exceed at `n` observations for p < alpha."""
    c, nu = _ref(n, lag(n, per_year))
    return t_ppf(1 - alpha, nu) / math.sqrt(c)


def _smallest(need: Callable[[int], float], start: int) -> int:
    """Smallest n >= 2 with n >= need(n), for `need` falling in n (n at or above `start` ok)."""
    lo, hi = 2, max(start, 2)
    while hi < need(hi):
        lo, hi = hi, hi * 2
    while lo < hi:
        mid = (lo + hi) // 2
        lo, hi = (lo, mid) if mid >= need(mid) else (mid + 1, hi)
    return lo


def min_periods_sharpe(
    sharpe: float,
    per_year: float,
    alpha: float = 0.025,
    power: float = 0.8,
    skew: float = 0.0,
    kurtosis: float = 3.0,
    lrv: float = 1.0,
) -> int:
    """Periods needed so the verdict's one-sided test of "Sharpe > 0" finds an annual Sharpe of
    `sharpe` with the given power. Mertens' (2002) variance under the alternative (as in
    `stats.probabilistic_sharpe`) times the assumed long-run variance ratio `lrv`, and the
    dependence-robust test's critical value at that n instead of z(1 - alpha):
    n = 1 + lrv k ((cv(n) + z_power) / sr)^2, k = 1 - skew sr + (kurtosis - 1) / 4 sr^2."""
    sr = sharpe / math.sqrt(per_year)
    k = 1 - skew * sr + (kurtosis - 1) / 4 * sr**2
    zp = _N.inv_cdf(power)

    def need(n: int) -> float:
        return 1 + lrv * k * ((critical(n, per_year, alpha) + zp) / sr) ** 2

    return _smallest(need, math.ceil(1 + lrv * k * (_z(alpha, power) / sr) ** 2))


def min_events_mean(
    effect: float,
    sd: float,
    alpha: float = 0.025,
    power: float = 0.8,
    per_year: float = 1.0,
    lrv: float = 1.0,
) -> int:
    """Events needed so the verdict's one-sided test of "mean > 0" finds a true mean of `effect`:
    n = lrv ((cv(n) + z_power) sd / effect)^2, cv(n) the test's critical value at n."""
    zp = _N.inv_cdf(power)

    def need(n: int) -> float:
        return lrv * ((critical(n, per_year, alpha) + zp) * sd / effect) ** 2

    return _smallest(need, math.ceil(lrv * (_z(alpha, power) * sd / effect) ** 2))


def binom_tail(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p), exact."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    logs = [
        math.lgamma(n + 1)
        - math.lgamma(i + 1)
        - math.lgamma(n - i + 1)
        + i * math.log(p)
        + (n - i) * math.log1p(-p)
        for i in range(k, n + 1)
    ]
    top = max(logs)
    return min(1.0, math.exp(top) * math.fsum(math.exp(x - top) for x in logs))


def _critical(n: int, alpha: float) -> int:
    """Smallest k with P(X >= k | n, 1/2) <= alpha (n + 1 if none)."""
    k = n + 1
    while k > 0 and binom_tail(k - 1, n, 0.5) <= alpha:
        k -= 1
    return k


def min_trials_win_rate(
    p: float, alpha: float = 0.025, power: float = 0.8, limit: int = 2000
) -> int:
    """Smallest n at which an exact one-sided sign test (wins >= critical count) finds a true win
    rate `p` with at least `power`. Exact power saw-tooths in n; this is the first n that
    reaches it."""
    for n in range(1, limit + 1):
        if binom_tail(_critical(n, alpha), n, p) >= power:
            return n
    raise ValueError(f"win rate {p} needs more than {limit} events")


def min_sample(plan: Plan) -> int:
    if plan.metric == "sharpe":
        return min_periods_sharpe(
            plan.effect, plan.per_year, plan.alpha, plan.power, plan.skew, plan.kurtosis, plan.lrv
        )
    if plan.metric == "mean":
        assert plan.sd is not None  # checked in Plan
        return min_events_mean(
            plan.effect, plan.sd, plan.alpha, plan.power, plan.per_year, plan.lrv
        )
    return min_trials_win_rate(plan.effect, plan.alpha, plan.power)


def years_needed(plan: Plan) -> float:
    return min_sample(plan) / plan.per_year


# --- hashes ---


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def code_hashes(repo: Path, paths: Iterable[str], ref: str | None = None) -> dict[str, str]:
    """sha256 of each file (relative to `repo`), from the working tree, or from commit `ref`."""
    out = {}
    for rel in paths:
        if ref is None:
            data = (repo / rel).read_bytes()
        else:
            data = subprocess.run(
                ["git", "--no-replace-objects", "cat-file", "blob", f"{ref}:{rel}"],
                cwd=repo,
                check=True,
                capture_output=True,
            ).stdout
        out[rel] = sha256(data)
    return out


def rule_hash(code: Mapping[str, str], params: Mapping[str, Any], data: Mapping[str, Any]) -> str:
    """One hash over what defines the rule: its code files' hashes, parameters, data source."""
    return sha256(_canonical({"code": dict(code), "params": dict(params), "data": dict(data)}))


# --- the registry ---


def read(path: Path) -> list[dict[str, Any]]:
    """Every line, checked: unique ids, a `frozen_at` UTC time on each (only `freeze` writes
    registry lines; a proposal pasted in has none), and each line's `rule_hash` agrees with its
    own code, params and data (a line edited before its commit shows here)."""
    text = path.read_text() if path.exists() else ""
    rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    seen: set[str] = set()
    for n, r in enumerate(rows, 1):
        try:
            ledger.parse_time(r["frozen_at"])
        except (KeyError, TypeError, ValueError):
            raise MissingFreezeTime(
                f"{path}: line {n} ({r.get('id', '?')}) has no valid frozen_at "
                "(YYYY-MM-DDTHH:MM:SSZ); registry lines come only from `freeze`"
            ) from None
        if r["id"] in seen:
            raise AlreadyFrozen(f"{r['id']}: frozen twice in {path}")
        seen.add(r["id"])
        if rule_hash(r["code"], r["params"], r["data"]) != r["rule_hash"]:
            raise HashMismatch(f"{r['id']}: rule_hash does not match its code, params and data")
    return rows


def entry(
    rule_id: str,
    *,
    code: Mapping[str, str],
    code_ref: str,
    params: Mapping[str, Any],
    data: Mapping[str, Any],
    plan: Plan,
    source: str,
    note: str = "",
) -> dict[str, Any]:
    """A registry line without its freeze time (the shape of a proposal too)."""
    if not code:
        raise ValueError("a rule with no code files cannot be frozen")
    return {
        "id": rule_id,
        "rule_hash": rule_hash(code, params, data),
        "code": dict(code),
        "code_ref": code_ref,
        "params": dict(params),
        "data": dict(data),
        "metric": plan.metric,
        "effect": plan.effect,
        "sd": plan.sd,
        "skew": plan.skew,
        "kurtosis": plan.kurtosis,
        "lrv": plan.lrv,
        "se": SE_RULE if plan.metric != "win_rate" else "exact sign test",
        "per_year": plan.per_year,
        "alpha": plan.alpha,
        "power": plan.power,
        "min_sample": min_sample(plan),
        "years_needed": round(years_needed(plan), 1),
        "source": source,
        "note": note,
    }


def plan_of(row: Mapping[str, Any]) -> Plan:
    return Plan(
        metric=row["metric"],
        effect=row["effect"],
        per_year=row["per_year"],
        alpha=row["alpha"],
        power=row["power"],
        sd=row.get("sd"),
        skew=row.get("skew", 0.0),
        kurtosis=row.get("kurtosis", 3.0),
        lrv=row.get("lrv", 1.0),
    )


def freeze(path: Path, row: Mapping[str, Any], now: datetime) -> dict[str, Any]:
    """Append `row` (from `entry`) to the registry, stamped `now`. Refuses a known id, a file
    whose committed lines were ever changed, and a `min_sample` that is not the calculator's."""
    ledger.check_append_only(path)  # raises LedgerTampered
    if any(r["id"] == row["id"] for r in read(path)):
        raise AlreadyFrozen(f"{row['id']}: already frozen; a changed rule needs a new id")
    if rule_hash(row["code"], row["params"], row["data"]) != row["rule_hash"]:
        raise HashMismatch(f"{row['id']}: rule_hash does not match its code, params and data")
    if row["min_sample"] != min_sample(plan_of(row)):
        raise ValueError(f"{row['id']}: min_sample is not what its test needs")
    line = {**row, "frozen_at": ledger.iso(now)}
    ledger._append(path, line)
    return line


def freeze_times(path: Path) -> dict[str, datetime | None]:
    """When each rule counts as frozen: the later of its `frozen_at` and the first commit on
    HEAD's first-parent chain that holds its line (on main: the merge, never older than main's
    previous tip, not a side commit whose date its author chose; branch protection keeps merges
    to PRs); None while the line is not committed."""
    ledger.check_append_only(path)
    rows = read(path)
    at = ledger.recorded_at(path, first_parent=True)
    if len(at) != len(rows):
        raise ForwardError(f"{path}: lines and commit times disagree")
    out: dict[str, datetime | None] = {}
    for r, committed in zip(rows, at, strict=True):
        own = ledger.parse_time(r["frozen_at"])
        out[r["id"]] = None if committed is None else max(own, committed)
    return out


def check_code(row: Mapping[str, Any], repo: Path, ref: str | None = None) -> None:
    """Raise HashMismatch if a frozen code file now hashes differently (on disk, or at `ref`)."""
    try:
        now = code_hashes(repo, row["code"], ref)
    except (OSError, subprocess.CalledProcessError) as e:
        raise HashMismatch(f"{row['id']}: a frozen code file is missing ({e})") from e
    changed = sorted(p for p, h in row["code"].items() if now[p] != h)
    if changed:
        raise HashMismatch(f"{row['id']}: code changed since freeze: {', '.join(changed)}")


# --- scoring ---


@dataclass(frozen=True)
class Obs:
    start: datetime  # the holding period (or event window) starts here
    end: datetime
    value: float
    rule_hash: str


def read_obs(path: Path) -> list[Obs]:
    """A rule's observations. The file is append-only like the registry: an observation
    committed once and later changed or removed raises `ledger.LedgerTampered` (a dropped loss
    or an edited value would bias the verdict), and so does a file on disk that does not start
    with its committed content."""
    ledger.check_append_only(path)  # raises LedgerTampered
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            out.append(
                Obs(
                    ledger.parse_time(r["start"]),
                    ledger.parse_time(r["end"]),
                    float(r["value"]),
                    r["rule_hash"],
                )
            )
    return out


@dataclass(frozen=True)
class Score:
    rule_id: str
    n: int
    min_sample: int
    estimate: float | None  # annual Sharpe, mean, or win rate on the window below
    p: float | None  # one-sided
    verdict: str  # "waiting" (n < min_sample, numbers are interim), "pass" or "fail"


def _stat(metric: str, values: Sequence[float], per_year: float) -> tuple[float, float] | None:
    """(estimate, one-sided p). `mean` and `sharpe` share the dependence-robust test of
    "mean > 0" (`hac_t`; at the null Sharpe 0, Lo's (2002) variance of the Sharpe ratio is the
    long-run variance of the mean over sigma^2); `sharpe` shows the annualised sample Sharpe."""
    n = len(values)
    if metric == "win_rate":
        if n == 0:
            return None
        wins = sum(v > 0 for v in values)
        return wins / n, binom_tail(wins, n, 0.5)
    got = hac_t(values, per_year)
    if got is None:
        return None
    if metric == "sharpe":
        m = stats.moments(values)
        if m is None:
            return None
        return m.sharpe * math.sqrt(per_year), got[1]
    return math.fsum(values) / n, got[1]


def score(row: Mapping[str, Any], frozen: datetime | None, obs: Iterable[Obs]) -> Score:
    """Score a frozen rule on its forward observations. Refuses (raises) rather than skips: an
    uncommitted freeze, an observation starting before the freeze, one made by other code."""
    if frozen is None:
        raise NotFrozen(f"{row['id']}: freeze line not committed; no proven freeze time")
    items = sorted(obs, key=lambda o: o.start)
    for o in items:
        if o.rule_hash != row["rule_hash"]:
            raise HashMismatch(f"{row['id']}: observation {ledger.iso(o.start)} made by other code")
        if o.start < frozen:
            raise LookAhead(
                f"{row['id']}: observation starts {ledger.iso(o.start)}, "
                f"before the freeze at {ledger.iso(frozen)}"
            )
        if o.end <= o.start:
            raise ValueError(
                f"{row['id']}: observation {ledger.iso(o.start)} ends before it starts"
            )
    for a, b in zip(items, items[1:], strict=False):
        if b.start < a.end:
            raise ValueError(f"{row['id']}: observations overlap at {ledger.iso(b.start)}")
    need = int(row["min_sample"])
    values = [o.value for o in items]
    window = values[:need]  # the verdict sees exactly the first `need`, never more
    got = _stat(row["metric"], window, float(row["per_year"]))
    estimate, p = got if got is not None else (None, None)
    if len(values) < need:
        verdict = "waiting"
    else:
        verdict = "pass" if p is not None and p < float(row["alpha"]) else "fail"
    return Score(row["id"], len(values), need, estimate, p, verdict)


# --- command line ---


def table(rows: Iterable[Mapping[str, Any]], alt_alpha: float = 0.10) -> str:
    """Markdown table of each rule's test, with the sample at the registered alpha and at
    `alt_alpha` for comparison."""
    out = [
        "| Id | Metric | Effect assumed | Per year | Alpha | n needed | Years | "
        f"n at alpha {alt_alpha:g} | Years |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        t = plan_of(r)
        alt = Plan(
            t.metric, t.effect, t.per_year, alt_alpha, t.power, t.sd, t.skew, t.kurtosis, t.lrv
        )
        out.append(
            f"| `{r['id']}` | {t.metric} | {t.effect:g} | {t.per_year:g} | {t.alpha:g} | "
            f"{min_sample(t)} | {years_needed(t):.1f} | {min_sample(alt)} | "
            f"{years_needed(alt):.1f} |"
        )
    return "\n".join(out)


def main(argv: Sequence[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Forward-only shadow registry (research only).")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("table", help="sample needed per rule, as a markdown table")
    t.add_argument("file", type=Path, nargs="?", default=CANDIDATES)
    s = sub.add_parser("score", help="score frozen rules on their forward observations")
    s.add_argument("--registry", type=Path, default=REGISTRY)
    s.add_argument("--obs", type=Path, default=Path("research/forward/obs"))
    s.add_argument("--repo", type=Path, default=Path())
    s.add_argument("--ref", default=None, help="check frozen code at this commit, not on disk")
    args = p.parse_args(argv)
    if args.cmd == "table":
        rows = [json.loads(line) for line in args.file.read_text().splitlines() if line.strip()]
        print(table(rows))
        return
    frozen = freeze_times(args.registry)
    print("| Id | n | Needed | Estimate | p (one-sided) | Verdict |")
    print("|---|---:|---:|---:|---:|---|")
    for r in read(args.registry):
        check_code(r, args.repo, args.ref)
        sc = score(r, frozen[r["id"]], read_obs(args.obs / f"{r['id']}.jsonl"))
        est = "-" if sc.estimate is None else f"{sc.estimate:.3g}"
        pv = "-" if sc.p is None else f"{sc.p:.3g}"
        print(f"| `{sc.rule_id}` | {sc.n} | {sc.min_sample} | {est} | {pv} | {sc.verdict} |")


if __name__ == "__main__":
    main()
