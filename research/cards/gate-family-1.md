# gate-family-1: how surprising are three kill-only passes among about 40 first gates?

Card written 2026-11-26 ~08:15 UTC, before any number of this lane was computed. Descriptive
work on the repo's own records (`research/gate-null.md`, `research/gate-null-2.md`); no new
data, no gate, no count change.

## Question

The gate family has 40 first gates (every gate row in `gate-null.md` except the replications
R32, R36, R45; W41n included) and three kill-only passes (W32, W36, W45), each killed by its
replication. #207 (`gate-null-2.md`) measured a null gate's false-pass rate at about 1-3% (up
to 5.5% with a slow premium in returns). How surprising are three passes if every first gate
were null?

## What is computed

1. A table of the 40 first gates with each gate's pass rule as recorded (placebo count N, rank
   threshold k, t / sign / post-sample conditions, one or two families, or N(0, 1) for the
   gates before wide-9), and a per-gate null pass probability p_i:
   - **rank bound**: k / (N + 1) under exchangeability (an upper bound: extra conditions only
     lower it); for N(0, 1) gates, the nominal one-sided level (about 0.023-0.025), and for
     permutation-p gates the stated p level.
   - **#207 reading**: p_i = 1%, 2%, 3% and 5.5% for every gate (empirical full-gate rate).
2. The number of passes under independence: Poisson-binomial distribution of the count,
   P(>= 3), for each p_i set; plus P(>= 3) with the rank bound inflated as #207 found for
   persistent doses (rank-only up to 7.5-10.7% at phi 0.8-0.9).
3. Whether W32, W36 and W45 share what #207 says inflates false passes: persistent monthly dose
   (acf1 >= 0.8), multi-month overlapping outcomes, sample length, era.

## Readings, fixed now

- P(>= 3) >= 0.10 under #207's 1-3% upper end or the rank bound: **three passes are
  ordinary** for a family of null gates; nothing to explain.
- P(>= 3) between 0.01 and 0.10 under #207's range: **at the high end**, as the review said;
  mild evidence that the gate's false-pass rate in this family is above #207's 1-3% (for
  example from shared design features), not evidence for any mechanism (all three died in
  replication).
- P(>= 3) < 0.01 under #207's 3%: **surprising under the null**; the likeliest reading is that
  the false-pass rate for the designs the three passes share is higher than #207 measured, and
  the lane names the shared feature.
- In no case does a result revive W32, W36 or W45 (their replications stand), and independence
  between gates is an assumption (shared data and doses make it approximate).
