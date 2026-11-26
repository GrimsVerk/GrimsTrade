# Card gate-null-3: would gate-null-2's proposed surrogate rule have blocked the three passes?

Lane `gate-null-3` (night run 2026-11-26, UTC). Descriptive retro-check, no new data, no new
gate, no verdict, no adoption decision (that is for the lead and the owner). **Card written and
pushed before any new number is computed.**

## Question

gate-null-2 (#207, `research/gate-null-2.md`) proposed, not adopted: for a gate whose dose has
lag-1 acf >= 0.8 at the gate's own step, a pass must also rank <= 2 of 41 among 40
phase-randomised surrogates (IAAFT for skewed or end-mismatched doses), on top of the shifted
calendars. gate-family-1 (#234) found all three kill-only passes (W32, W36, W45) sit on slow
monthly doses, and all three died in replication (R32, R36, R45).

For W32, W36, W45: (1) the dose's lag-1 acf; (2) does the proposal apply (acf >= 0.8);
(3) would the pass have survived (surrogate rank <= 2 of 41). For every gate that failed: the
rule can only add a condition to a pass, so it cannot change a fail; state that. Conclusion:
how many of the three replication-killed passes the rule would have blocked, i.e. how many
replications it would have saved.

## Method

Records first: `research/gate-null-2.md` (W32 re-score), `research/results/grid-load-premium.md`
(W36 phase surrogates), `research/wide-28.md` (W45). Only a number the records lack is
computed, from the gate's own cached code and inputs (`python -I`, < 5 min, no download): W36's
dose acf1 is the one expected gap. No surrogate is re-drawn where a stored rank exists; the
stored rank is the gate-time answer.

## Guess (before any new number)

W32 and W45 pass the rule (stored ranks 1 / 1 and 2 IAAFT / 1 phase); W36 has acf above 0.8
and phase rank 3, so it is blocked. The rule would have saved 1 of 3 replications.
