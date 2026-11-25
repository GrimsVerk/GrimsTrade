# evalue-forward-1: would an anytime-valid sequential test let the forward record confirm an edge? (card)

Lane `evalue-forward-1`, written 2026-11-25 00:40 UTC **before any number below was computed**.
Branch `evalue-forward-1` from `origin/main` (`0ae15d0`). Methods study: simulation only, on the
committed weekly returns store (`research/register/returns/`, train only, nothing after
2025-11-09). No strategy backtest, no price bar, no held-out year, no live record. No change to
`src/`, the forward registry (`research/forward/`), the gym or the daily runner.

What was seen before this card: `research/power-map-1.md` (forward years at fixed horizon:
+0.10 over `tsmom12` at rho 0.95 needs 72 years at 80% power and z 1.645, 356 at z 4.69),
`docs/forward-registry.md` and `src/grimstrade/forward.py` (verdict read once at `min_sample`,
alpha 0.025 per rule), `research/register/BAR.md` (z 4.70 at N 504). No simulation of any
sequential test has been run in this repo (grep of `tries.md`, `ideas.md`: only `cusum-exit`,
a trading rule, not a test).

## Question

The forward registry reads its verdict once, at a sample fixed in advance, because looking
every week with a fixed-horizon test inflates false rejections. An anytime-valid test (an
e-process: a nonnegative process with expectation at most 1 under the null at every stopping
time; Ville's inequality gives P(sup_t E_t >= 1/alpha) <= alpha) may be looked at every week and
stopped whenever it crosses 1/alpha (Ramdas, Grunwald, Vovk and Shafer 2023, "Game-theoretic
statistics and safe anytime-valid inference", Statistical Science 38(4)). Big edges can stop
early; small ones pay in power. **Does it change power-map-1's answer that forward scoring
cannot confirm an edge over `tsmom12` in useful time?**

## The statistic and the null

Weekly paired difference D_t = A_t - B_t, B = `tsmom12`, A = the registered book scaled to
B's volatility by a ratio fixed at registration (from the train record). With equal
volatilities, mean(D) > 0 is the same as Sharpe(A) > Sharpe(B), and
E[D] = d sigma / sqrt(52), sd(D) = sigma sqrt(2 (1 - rho)), with d the annual Sharpe edge.

**Null H0: E[D_t | past] <= 0 every week** (mean-difference form; a test martingale tests the
conditional mean, which is stronger than the unconditional mean; the simulation measures what
serial dependence does to it). The Sharpe-difference form is not used: it needs a variance
estimate inside the e-process; with the volatility ratio fixed at registration the mean form is
the Sharpe form up to volatility drift (noted as a limit).

## The e-processes (fixed now)

Both work on the difference in units of the train-record sd of D, fixed at registration:
X_t = D_t / s0, s0 = sd of D over the train record (in the simulation: the population value,
sqrt(2 (1 - rho))).

**E1 (primary): betting e-process, ONS.** Waudby-Smith and Ramdas (2024, JRSS-B, "Estimating
means of bounded random variables by betting"); Shekhar and Ramdas (2023, IEEE Trans. Inf.
Theory, "Nonparametric two-sample testing by betting"), ONS betting fraction of Cutkosky and
Orabona (2018). Bounded by clipping: Y_t = clip(X_t / 5, -1, 1) (a clip at 5 train sds, fixed
now). Wealth K_t = prod (1 + lambda_t Y_t), lambda_t predictable in [0, 1/2] (one-sided: a
nonnegative bet makes K a nonnegative supermartingale under E[Y_t | past] <= 0). ONS:
lambda_1 = 0; g_t = Y_t / (1 + lambda_t Y_t); A_t = 1 + sum_{s<=t} g_s^2;
lambda_{t+1} = clip(lambda_t + (2 / (2 - ln 3)) g_t / A_t, 0, 1/2). Its null is the mean of the
clipped difference (a pre-registered, winsorised estimand); with a symmetric D it has the sign
of E[D].

**E2 (comparison): one-sided normal-mixture SPRT, self-normalised.** Robbins (1970) mixture;
self-normalised form of de la Pena (1999): for conditionally symmetric X with mean 0,
exp(lambda S_t - lambda^2 V_t / 2) is a supermartingale (S_t = sum X, V_t = sum X^2). Mixed
over lambda ~ half-normal(0, tau^2):

    E_t = 2 / sqrt(1 + tau^2 V_t) * exp(tau^2 S_t^2 / (2 (1 + tau^2 V_t))) * Phi(tau S_t / sqrt(1 + tau^2 V_t))

tau = 0.05 (per-week signal-to-noise, about d +0.10 at rho 0.95), fixed now. Valid only for
symmetric differences; under skew and fat tails approximately (the simulation measures it).

**Contrasts on the same paths:** (F) the registry's fixed-horizon one-sided z-test of mean(D)
(t-statistic with the sample sd) read once at Y years; (P) the same z-test looked at every week
and stopped at the first crossing (the naive peeking the registry forbids).

## Levels

- **alpha 0.025** (primary): the registry's per-rule alpha (`forward.py`, docs/forward-registry.md:
  forward data are fresh, so the train search's N does not apply; four rules share 0.10).
  This is the "per-family bar if a book is registered alone".
- **alpha 0.05** (z 1.645): power-map-1's "registered alone" row, for a like-for-like
  comparison with its 72 years.
- **alpha 1.3e-6** (z 4.70 one-sided, BAR.md at N 504): what a new pick would need if the
  forward record were asked to clear the project bar.
Thresholds: E crosses 1/alpha (Ville). One run per path gives all three.

## Scenarios

Edges d in {0, +0.05, +0.10, +0.30} annual Sharpe over `tsmom12`; rho in {0.77, 0.88, 0.95}
(0.77 and 0.95: BAR.md's far and close rules / presets; 0.88: the store's C1 median, power-map-1).
Weekly steps, horizon 100 years (5,200 weeks) per path.

**Fat tails (primary): block resampling of the committed store.** B~ = the primary
`baselines/tsmom12` weekly series (1994-02-01 onwards, cut at 2025-11-09), demeaned, unit sd.
Donors: every stored series of class C1 (power-map-1's name rule, which already leaves out the
`live` family and the planted-signal controls), other than `tsmom12` itself, with at least 20 years of overlap with B and a correlation with B in
[0.77, 0.95]; each donor's residual on B over the overlap, demeaned, unit sd, is E~ (paired
week by week with B~). Each path picks one donor (uniformly, seeded) and draws circular blocks
of 52 weeks from the overlap, the same weeks for B~ and E~ (keeps joint tails, volatility
clustering and autocorrelation), and sets

    X_t = [(rho - 1) B~_t + sqrt(1 - rho^2) E~_t + d / sqrt(52)] / sqrt(2 (1 - rho))

so E[X] = d / (sqrt(52) sqrt(2 (1 - rho))) and sd(X) = 1 in the resampling population (the
null d = 0 has mean exactly 0 there). **Gaussian control:** iid normal X with the same mean and
sd 1.

Also, against zero (the registry's `sharpe` metric, e.g. `carry-3-band@1`): X_t = B~_t + S /
sqrt(52), S in {0, 0.5, 1.0}, block-resampled `tsmom12` alone, same e-processes.

Paths: 2,000 per cell with d > 0; 10,000 per null cell (d = 0, S = 0). Seed 20261125, one
generator per cell seeded from (seed, cell index). numpy only.

## Outputs

Per cell and level: P(reject by 5, 10, 20, 50, 100 years) for E1, E2, F (at that horizon) and
P (peeking); median years to rejection (">100" if under half reject); the years at which 80%
have rejected (sequential) against power-map-1's fixed-horizon years for 80% power
((z + 0.84) k sqrt(2 (1 - rho)) / d)^2 with k = 1 (the simulation's own F row is the
fat-tail check of that). Null cells: false-rejection rate by 100 years with a binomial 95%
upper bound, and the largest log E seen (for alpha 1.3e-6, which 10,000 paths cannot resolve).

Script `research/evalue1.py` (`uv run --with numpy python research/evalue1.py`), printout
in `research/results/evalue-forward-1.md`; write-up `research/evalue-forward-1.md`; a small
offline test of the e-process arithmetic in `tests/test_evalue1.py`; one `note` row in
`research/tries.md` (no selectable try).

## How the answer is read (fixed now)

- **Adopt-worthy** if, at alpha 0.025, E1 (the method valid without symmetry) both (a) keeps
  the false-rejection rate at or below 0.025 on the resampled null (binomial upper bound), and
  (b) reaches 80% rejection for some plausible edge (d <= +0.10, power-map-1's plausible range)
  within 20 years, or stops large edges (+0.30) at least 30% sooner in median than the
  fixed-horizon test's 80%-power years.
- **No change to the answer** if E1's 80% time for d +0.10 is still beyond 20 years at every
  rho: then the sequential test is a monitoring convenience (look any week, stop early for big
  edges or kill early), not a way to confirm plausible edges.
- Recommendation to the lead either way (engineering follow-up: whether the registry adds an
  e-process score next to the fixed-horizon verdict). This lane changes neither.
