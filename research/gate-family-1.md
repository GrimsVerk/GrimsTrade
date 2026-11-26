# gate-family-1: three kill-only passes among 40 first gates, how surprising under a null?

Lane gate-family-1, 2026-11-26. Card: `cards/gate-family-1.md` (committed before any number).
Descriptive arithmetic on the repo's own records (`gate-null.md` tables, `gate-null-2.md`);
no new data, no gate, **no count change**. Script: `lib/gatefamily1.py`
(`python research/lib/gatefamily1.py` prints every number below); tests:
`tests/test_gatefamily1.py`.

## The family

40 first gates: every gate row in `gate-null.md`'s verdict table except the replications R32,
R36, R45, with W41n included (ann-1, critical-slowing, W3, W12-W17, W19, seasonal-20y,
W20-W41, weather-1/2, W43, W18, W44, W41n, W45). Passes: W32, W36, W45, each killed by its
replication.

Per-gate null pass probability p_i, two record-based readings (full table in the script output):

- **Rank rule alone** (upper bound): k / (N + 1) under exchangeability. Rank <= 2 of 41 =
  0.049 for wide-9 on; rank 1 of 21 = 0.048 for W38 and W41n; the stored placebo counts for
  W3 (28), W13 (14), W15 (22), W16 (30) with k = 2 (k = 1 for W13, W15; their own threshold is
  not restated in `gate-null.md`, so these are bounds); the nominal one-sided 0.025 for the
  N(0, 1) gates (ann-1, critical-slowing, W14) and 0.05 for W12's permutation p. The t >= 2,
  sign, post-sample and second-family conditions only lower p, so this is an upper bound
  *if exchangeability holds*; #207 shows it does not for slow doses (rank-only 5.4-19%).
- **Rank and t >= 2 on the gate's own placebo null**: P(rank <= k and t >= 2) =
  E[min(m, k)] / (N + 1), m = draws past 2 on the predicted side, estimated from half the
  stored two-sided share of placebos with |t| >= 2 (a zero share counted as half a draw). A
  narrow null (W32 0%, W36 2%) puts p near 0.012; a wide one (W45 40%) leaves the rank
  binding at 0.049. Rough: halving assumes a symmetric null, and off-centre nulls (W33, W35,
  W39) are not.

## Result (independent gates, Poisson-binomial)

| p_i used | Expected passes | P(0) | P(1) | P(2) | **P(>= 3)** |
|---|---:|---:|---:|---:|---:|
| Rank rule alone (upper bound under exchangeability) | 1.93 | 0.139 | 0.281 | 0.277 | **0.30** |
| Rank and t >= 2, own placebo null | 1.47 | 0.223 | 0.342 | 0.255 | **0.18** |
| #207 flat 1% | 0.40 | 0.669 | 0.270 | 0.053 | **0.007** |
| #207 flat 2% | 0.80 | 0.446 | 0.364 | 0.145 | **0.046** |
| #207 flat 3% | 1.20 | 0.296 | 0.366 | 0.221 | **0.12** |
| #207 flat 5.5% (slow premium) | 2.20 | 0.104 | 0.242 | 0.275 | **0.38** |
| #207 mixed: slow doses 5.5%, others 2% | 1.50 | 0.215 | 0.339 | 0.258 | **0.19** |

**P(>= 3) ranges from 0.007 to 0.12 over #207's 1-3%, 0.046 at its middle (2%), and 0.18-0.38
under the rank bound, the gates' own nulls or the slow-premium rate.** By the card's readings
the outcome sits in the middle band: three passes are at the high end of #207's 1-3% (as the
review said), unremarkable at 3% or above, and only surprising (< 0.01) if the true rate were
about 1%.

## Do the three passes share something?

Yes, by the records:

| Gate | Dose | Outcome | Sample | Placebo null |
|---|---|---|---|---|
| W32 | -PDSI, monthly, physical, persistent | TLT next quarter (m+2..m+4), NW 3 | 276 months 2002-2025 | SD 0.94, 0% past \|t\| 2 |
| W36 | yoy growth of industrial electricity sales, monthly, persistent | Mkt-RF month m+3, NW 3 | 619 months 1974-2025 | SD 0.91, 2% |
| W45 | yoy growth of 3 months of NICS checks, monthly, acf1 0.935 | US market m+2..m+4 | 182 months 2008-2023 | SD 1.95, 40% (IAAFT SD 1.52) |

All three are slow monthly US doses (year-on-year growth or a drought index) read against
multi-month outcomes with Newey-West errors: the design #207 names as the one where the rank
rule is liberal (phi >= 0.8: rank-only 5.4-19%) and where a slow premium in returns lifts the
full gate to about 5.5%. Sample length and era do not line up (182-619 months, 1974-2025).

By my reading of the records (tagged in the script, acf measured only for W43, W44, W45), 10
of the 40 first gates are monthly slow-dose gates (W19, W29, W32-W36, W43, W44, W45) and 20
are slow-dose gates of any step. If every gate had the same p, the chance that all three
passes land in the 10 monthly slow-dose gates is **0.012** (hypergeometric; 0.12 for the 20).
Within those 10, three or more passes have P 0.011 at the rank bound 0.049, 0.015 at 5.5%,
0.034 at 7.5% and 0.083 at 10.7% (#207's rank-only rates at phi 0.8-0.9).

## Reading

- Three passes in 40 null gates are not strong evidence of anything: P(>= 3) is 0.05 at #207's
  middle rate and 0.12 or more at 3% or above. All three died in replication, so nothing is
  revived.
- The concentration is the more informative number: all three passes sit in the quarter of
  the family with slow monthly doses and multi-month outcomes, which would happen about 1 time
  in 80 if every gate had the same false-pass rate. That fits #207's finding that this design
  passes more often under the null than its nominal rate; within that subset the rate implied
  by three passes in ten is nearer 10% than 2-3%. Caveat: the subset was named after seeing
  which gates passed (post hoc), and the slow/not-slow tags are mine from the record text, so
  0.012 overstates the surprise; read it as consistent with #207, not as a test.
- Practical consequence, already in the procedure: for slow monthly doses the
  "both families" rule (#207, now pre-registered by W43-W45) and the replication step are the
  guards; W45 passed both families and still died in replication, so the second family alone
  does not close the gap.

## Limits

- Independence between gates is assumed; gates share data (French factors, US market) and
  dose types, which widens the count's spread (makes 3 passes less surprising, not more).
- Early gates' rank thresholds and N(0, 1) gates' real null rates are bounded, not known; W14
  and ann-1 on clustered N(0, 1) could have false-pass rates well above 2.5%.
- The own-null reading uses rounded stored shares and a symmetry assumption.
