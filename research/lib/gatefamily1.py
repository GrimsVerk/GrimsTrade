"""Lane gate-family-1 (research/cards/gate-family-1.md): how surprising are three kill-only
passes among the 40 first gates under a null? Pure arithmetic on the gate records in
`research/gate-null.md` (hand-copied below); no file, price or network is read.

Run: `python research/lib/gatefamily1.py` prints the tables used in `research/gate-family-1.md`.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb


@dataclass(frozen=True)
class Gate:
    gid: str
    n_placebo: int  # placebo draws; 0 = judged against N(0, 1) or a permutation p
    k: int  # pass needs rank <= k of n_placebo + 1
    share_t2: float | None  # share of placebos with |t| >= 2 (gate-null.md table), if stored
    monthly_persistent: bool  # monthly, slow dose (acf1 about 0.8 or more by the records)
    persistent: bool  # any slow dose (weekly/monthly/quarterly/annual), by the records
    passed: bool
    nominal: float = 0.025  # used when n_placebo == 0


# Rank rules from gate-null.md step 4 (rank <= 2 of 41, plus t >= 2 with the predicted sign)
# for wide-9 on; N = 20 gates (W38, W41n) read as rank 1 of 21 (about 0.048, as step 4's 0.05).
# Gates before wide-9: the placebo counts stored in the gate-null.md tables; their own rank
# threshold is not restated there, so k = 2 is used (an upper bound for p if theirs was k = 1).
GATES: list[Gate] = [
    Gate("ann-1", 0, 0, None, False, False, False),
    Gate("critical-slowing", 0, 0, None, False, False, False),
    Gate("W3", 28, 2, 0.11, False, False, False),
    Gate("W12", 0, 0, None, False, False, False, nominal=0.05),
    Gate("W13", 14, 1, 0.0, False, False, False),
    Gate("W14", 0, 0, None, False, False, False),
    Gate("W15", 22, 1, None, False, False, False),
    Gate("W16", 30, 2, 0.20, False, False, False),
    Gate("W17", 40, 2, 0.02, False, False, False),
    Gate("W19", 40, 2, 0.20, True, True, False),
    Gate("seasonal-20y", 40, 2, 0.02, False, False, False),
    Gate("W20", 40, 2, 0.02, False, False, False),
    Gate("W21", 40, 2, 0.28, False, True, False),
    Gate("W22", 40, 2, 0.08, False, True, False),
    Gate("W23", 40, 2, 0.10, False, True, False),
    Gate("W24", 40, 2, 0.0, False, True, False),
    Gate("W25", 40, 2, 0.12, False, True, False),
    Gate("W26", 40, 2, 0.25, False, True, False),
    Gate("weather-1", 40, 2, 0.10, False, False, False),
    Gate("weather-2", 40, 2, 0.10, False, False, False),
    Gate("W27", 40, 2, 0.05, False, False, False),
    Gate("W28", 40, 2, 0.32, False, True, False),
    Gate("W29", 40, 2, 0.22, True, True, False),
    Gate("W30", 40, 2, 0.22, False, False, False),
    Gate("W31", 40, 2, 0.02, False, False, False),
    Gate("W32", 40, 2, 0.0, True, True, True),
    Gate("W33", 40, 2, 0.30, True, True, False),
    Gate("W34", 40, 2, 0.10, True, True, False),
    Gate("W35", 40, 2, 0.25, True, True, False),
    Gate("W36", 40, 2, 0.02, True, True, True),
    Gate("W37", 40, 2, 0.05, False, False, False),
    Gate("W38", 20, 1, 0.05, False, True, False),
    Gate("W39", 40, 2, 0.12, False, True, False),
    Gate("W40", 40, 2, 0.05, False, False, False),
    Gate("W41", 40, 2, 0.08, False, False, False),
    Gate("W43", 40, 2, 0.08, True, True, False),
    Gate("W18", 40, 2, 0.0, False, False, False),
    Gate("W44", 40, 2, None, True, True, False),
    Gate("W41n", 20, 1, None, False, True, False),
    Gate("W45", 40, 2, 0.40, True, True, True),
]


def p_rank(g: Gate) -> float:
    """Null pass probability from the rank rule alone (exchangeability): k / (N + 1); the
    nominal one-sided level for N(0, 1) or permutation gates. An upper bound when the rule adds
    t / sign / post-sample / second-family conditions."""
    return g.nominal if g.n_placebo == 0 else g.k / (g.n_placebo + 1)


def p_own_t(g: Gate) -> float:
    """Rank rule and t >= 2 together, from the gate's own placebo null: under exchangeability
    P(rank <= k and t >= 2) = E[min(m, k)] / (N + 1), m = draws past 2 on the predicted side.
    Estimated with m = (share_t2 / 2) * (N + 1) (half the two-sided share; a zero share is set
    to half a draw). Falls back to p_rank when no share is stored."""
    if g.n_placebo == 0 or g.share_t2 is None:
        return p_rank(g)
    n1 = g.n_placebo + 1
    m = max(g.share_t2 / 2 * n1, 0.5)
    return min(m, g.k) / n1


def poisson_binomial(ps: list[float]) -> list[float]:
    """Distribution of the number of successes of independent Bernoulli(p_i)."""
    dist = [1.0]
    for p in ps:
        new = [0.0] * (len(dist) + 1)
        for j, d in enumerate(dist):
            new[j] += d * (1 - p)
            new[j + 1] += d * p
        dist = new
    return dist


def tail(ps: list[float], at_least: int) -> float:
    return float(sum(poisson_binomial(ps)[at_least:]))


def all_in_subset(n: int, m: int, r: int) -> float:
    """P(all r passes fall in a given subset of m of n gates), equal p_i (hypergeometric)."""
    return comb(m, r) / comb(n, r)


def scenarios(gates: list[Gate]) -> dict[str, list[float]]:
    n = len(gates)
    out = {
        "rank rule alone (upper bound)": [p_rank(g) for g in gates],
        "rank and t >= 2, own placebo null": [p_own_t(g) for g in gates],
    }
    for p in (0.01, 0.02, 0.03, 0.055):
        out[f"#207 flat {p:.1%}"] = [p] * n
    # #207 R3: persistent doses at the slow-premium rate, the rest at 2-3%.
    out["#207 mixed: persistent 5.5%, others 2%"] = [0.055 if g.persistent else 0.02 for g in gates]
    return out


def main() -> None:
    gates = GATES
    n = len(gates)
    print(f"first gates: {n}, passes: {sum(g.passed for g in gates)}")
    print("| Scenario | sum p_i (expected passes) | P(0) | P(1) | P(2) | P(>= 3) |")
    print("|---|---:|---:|---:|---:|---:|")
    for name, ps in scenarios(gates).items():
        d = poisson_binomial(ps)
        print(
            f"| {name} | {sum(ps):.2f} | {d[0]:.3f} | {d[1]:.3f} | {d[2]:.3f} | {tail(ps, 3):.3f} |"
        )
    print()
    print("| Gate | N | k | rank p | own-t p | monthly slow | slow | passed |")
    print("|---|---:|---:|---:|---:|---|---|---|")
    for g in gates:
        print(
            f"| {g.gid} | {g.n_placebo or '-'} | {g.k or '-'} | {p_rank(g):.3f} | "
            f"{p_own_t(g):.3f} | {'y' if g.monthly_persistent else ''} | "
            f"{'y' if g.persistent else ''} | {'PASS' if g.passed else ''} |"
        )
    mm = sum(g.monthly_persistent for g in gates)
    ma = sum(g.persistent for g in gates)
    print()
    print(
        f"monthly slow-dose gates: {mm}; P(all 3 there | equal p) = {all_in_subset(n, mm, 3):.4f}"
    )
    print(f"any slow-dose gates: {ma}; P(all 3 there | equal p) = {all_in_subset(n, ma, 3):.4f}")
    sub = [p_rank(g) for g in gates if g.monthly_persistent]
    print(f"monthly slow subset at rank-alone p: P(>= 3 of {mm}) = {tail(sub, 3):.4f}")
    for p in (0.03, 0.055, 0.075, 0.107):
        print(f"monthly slow subset at p = {p}: P(>= 3 of {mm}) = {tail([p] * mm, 3):.4f}")


if __name__ == "__main__":
    main()
