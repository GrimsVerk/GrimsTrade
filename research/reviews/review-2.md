# Review 2 of night 3 (the claims in `research/SUMMARY.md`)

Reviewer: lane `review-2`, an agent that wrote none of the reviewed code. Branch `review-2`,
made from `pr-map` at `91968a9`. Written 2026-11-19. Status: **in progress** (sections are
added as they are done).

## Required fixes

(filled in as the sections below are finished)

## How the review was done

- Read the code, the reports and the tries rows on each lane's branch (`git show
  origin/<branch>:<path>`); no branch other than `review-2` was changed.
- Numbers marked "recomputed" come from small scripts run against committed data. No held-out
  year data was read. No whole analysis was re-run.

## 1. The project-wide bar (dsr-1 #74, register-1..5 #79 #92 #100 #108 #111)

**Verdict: the bar holds (z >= 4.69, about +0.30 Sharpe for a close rule). Two statements
around it need fixing: "the largest lead ever seen on the main test was +0.18" is wrong, and
"worth about 486 independent shots" is the cautious end of a measured range, not a
measurement.**

### 1a. Formulas: hold

- Expected best of N trials, `E + sqrt(V) * ((1 - g) Z^-1(1 - 1/N) + g Z^-1(1 - 1/(N e)))`,
  and `DSR = Z((SR - SR0) sqrt(T - 1) / sqrt(1 - skew SR + (kurt - 1)/4 SR^2))` with raw
  kurtosis: both match Bailey and Lopez de Prado (2014), eq. 1-2 (`research/dsr-1.md` on
  `dsr-1`, section 2; `src/grimstrade/stats.py` reproduces the paper's worked example,
  DSR 0.9004 at N = 100, as dsr-1 states). N_eff = rho + (1 - rho) M is the paper's
  appendix approximation, quoted correctly.
- Difference form: pass when `(d - SE * maxZ(N)) / SE >= 1.645`, i.e. z >= 1.645 + maxZ(N).
  Under the null the spread of the trials' edges is their own sampling SE, so using SE as
  sqrt(V) is right.
- Recomputed (stdlib): maxZ(486) = 3.044, z 4.69, edge 4.69 x 0.065 = +0.305 and
  4.69 x 0.12 = +0.563. maxZ(1,032) 3.26 -> +0.32/+0.59; maxZ(3,130, every row) 3.57 ->
  +0.34/+0.63. All as in `research/register/BAR.md` (branch `register-5`).
- The SEs are realistic. Recomputed from the committed weekly returns
  (`research/register/returns/*.csv.gz`, delta-method SE of a Sharpe difference, iid):
  tuned `tsmom12` variants with weekly correlation 0.90-0.95 to it have SE 0.06-0.08; equal
  weight (correlation 0.82) 0.106, close to review-1's bootstrap 0.12. **Caveat:** SE 0.12 is
  a rule correlated about 0.77 with `tsmom12`, not a "far" rule. An uncorrelated rule has SE
  about 0.25 on 32 years and needs about +1.2 Sharpe. BAR.md says to use the z column for such
  cards; SUMMARY's "+0.30 to +0.56" range should say it covers rules correlated 0.77-0.93
  with `tsmom12`.

### 1b. N_eff = 486: holds as the cautious choice, overstated as "measured"

- The register measures two very different things: A.3 with the average pairwise
  correlation (0.53) gives 486; ONC finds 2 clusters (12 when scaled to N); the eigenvalue
  participation ratio is 2.6 (`BAR.md`, "How many independent trials"). The bar takes the
  largest. `register-2.md` lines 110-113 argue for A.3 and state the disagreement, which is
  honest.
- A.3 is itself cautious here. For M equicorrelated trials the expected best edge is exactly
  sqrt(1 - rho) x maxZ(M) = 0.686 x 3.26 = 2.24 standard errors, i.e. z >= 3.88 (+0.25 close
  rule), against A.3's 4.69. So the defensible close-rule bar is **+0.25 to +0.32**, and the
  three-way choice of method moves it from +0.21 (ONC) to +0.32 (independent).
- The correlation is measured on the trials' raw returns. The difference test's luck term
  depends on the correlation of their **edges over `tsmom12`**, which strips the common
  market part and is likely lower, i.e. closer to independent (+0.32). Because maxZ grows
  slowly with N, none of this moves the close-rule bar outside +0.25..+0.32.
- Counting: N counts selectable rows (variant or baseline on train) plus 11 live
  strategies. Not counted: 1,226 robustness rows and 232 screens. Screens select which ideas
  get a backtest, so they are trials in spirit; robustness rows were sometimes used to choose
  a variant (`trend-tune-surface`). Counting all 3,130 rows moves the bar to +0.34: immaterial.
  Double counting goes the cautious way: an identical try re-logged with a new timestamp on
  another branch is two lines, so two tries (dedup is by exact line, `register.py` docstring),
  and the live `tsmom12` is also a baseline row.
- Cluster Sharpe variance 0.136 (used for the "against zero" table) is the sample variance of
  **two** numbers (0.937, 1.459; `trials.json`), so it has almost no precision. The "against
  zero" bar is a rough figure. `cluster_sharpes_minvar` of 4.8-5.4 in `trials.json` are the
  in-sample minimum-variance portfolios (long-short weights). They are not used in the bar,
  but they should be dropped from the file or labelled, so nobody quotes them.

### 1c. "The largest lead ever seen on the main test was +0.18": wrong

`research/register/tries.jsonl` (branch `register-5`), primary test (six assets,
1994-02-01..2025-11-09), sorted by Sharpe: `halving / halving-alone`, kind `variant`, Sharpe
**1.28** against `tsmom12`'s 1.05, a lead of **+0.23** (lane's 90% range +0.12..+0.36,
`research/results/halving.md:10`). Then `fomc-cycle / even-gate` 1.22 (+0.17) and
`halving-and` 1.20 (+0.15). Recomputed from the committed weekly returns: `halving-alone`
+0.25, weekly correlation 0.93, iid SE 0.070, **z 3.6**; `halving-and` +0.15, z 3.0;
`even-gate` +0.19, z 2.2.

dsr-1 quoted +0.18 because it took each family's pre-named primary variant (`halving-and`).
That is a fair rule for its own test, but it does not make +0.18 the largest lead seen.
`halving-alone` still fails the bar (3.6 < 4.69, and < 3.88 under the exact equicorrelated
count). But it **passes the ONC-scaled row (z 3.31)**, so it is the one result where the
choice of N_eff method decides the verdict. Its iid z is also too kind: the edge sits in two
or three coin halving cycles, with fat tails. Severity: medium. The decision does not change,
but SUMMARY tells the owner nothing came near, and that is not so.

## 2. Crash insurance (insure-1 #87, insure-2 #90)

**Verdict: holds with caveats. The insurance and its timing component are solid. Three
SUMMARY wordings overstate it: "50 independent falls", "48 of 50" as the evidence, and an
unqualified "cheaper than simply holding less".**

### 2a. "50 independent US falls": overstated wording (medium)

`research/lib/insure1.py` (branch `insure-1`), `market_anchored` (about line 287): the 50 are
the 21 falls of the US market, each with the industry falls inside it, **plus 29 clusters of
industry-only falls**, single-linked when their windows overlap. So 29 of the 50 are falls of
one or a few of 10 industry portfolios while the market did not fall 25%. They are separate
in time, but they are not "US falls" in the sense a reader takes. The market zigzag also
counts five legs of 1929-1933 as five episodes (the lane says so, `insure-1.md`, "How sure").
The stricter linkage gives 37 (36 of 37). The market alone gives **20 of 21**, and that is
the figure to quote for "US falls". Fix: "in 21 US market falls of 25% or more since 1927 it
lost less in 20 (50 when industry falls are added, 37 under strict grouping)".

### 2b. "Lost less than holding in 48": the easy test is not the evidence (low-medium)

The lane itself calls the sign test "easy by construction" (`insure-1.md`, bar paragraph).
Any rule that is out of the market part of the time loses less in most falls. The evidence
that the rule times falls is card 2: share of the fall avoided **0.50**, against 0.27 for
the rule's own positions rotated to random dates and 0.29 for a fixed 73% exposure (0 of
1,000 rotations as good). SUMMARY gives "48 of 50" and "about half". The comparison with
random timing at the same exposure (0.50 vs 0.27) should replace the count.

### 2c. "It is cheaper than simply holding less": true in direction, proven only before 1962 (medium)

From insure-2's own multiple-testing paragraph (`insure-2.md`, step 1): with 8 rotation
p-values at Bonferroni 0.006, "trend buys that cheaper than random timing" survives **only
in 1927-1961**. US 1962-2001 premium p 0.013, 1962-2025 p 0.020, **2002-2025 p 0.19**. Of the
non-US sets, only the 13 developed price indices pass (p 0.009). The lane reads this
correctly ("solid only in 1927-1961, suggestive after"). SUMMARY drops the qualifier, in the
period the owner cares about most (since 2002: trend 1.34, fixed 1.53, random 1.91, an
"in between" verdict on 13 episodes). Fix: "cheaper than holding less in every era and
market in direction; statistically shown only for 1927-1961 and the developed-market price
indices; since 2002 not shown".

### 2d. Look-ahead and independence

- Episodes are defined with hindsight on holding's prices, which does not favour the rule.
  The rebound window (365 days after the trough, cut at the next peak) charges the late
  buy-back to the insurance, and the decomposition I + B + C = total is asserted in code
  (`score`, `AssertionError` if off by 1e-6). Fine.
- **Small fill optimism (low):** the paper series (`research/lib/trend_tune.py`, `paper`,
  about lines 154-186) decides on Friday's close, visible at 22:30 UTC, and earns the bars
  **after** that close: in effect a fill at Friday's close, not the next open
  (`AGENTS.md`: "fills are at the next open"). The daily index files have no open, so this is
  a necessary approximation. It is the only source for US 2002-2025 and for every non-US set.
  insure-1 bounds the gap at 3.7 log points in one episode on 1927-2001, where both sources
  exist. Not material for a 12-month signal, but it should be stated where the paper series
  stands alone.
- Non-US independence: insure-2 anchors non-US clusters on US falls and says the sets
  "are not independent of each other or of the US after 1966". SUMMARY's "17 of 18" is
  correct; it should not be read as 18 more independent confirmations on top of the US 50.

### 2e. The premium figures: hold

Premium = -(B + C) / I (`insure1.py`, `prem`, about line 430): growth given up in rebounds
and calm markets per log point of loss avoided. Pooled 1.07 (0.97 with T-bills on cash),
per era 0.86 / 1.38 / 1.34, matched by insure-2's paper series (0.85 / 1.38 / 1.34).
"About 2 points of growth a year behind holding since 2002" is insure-2's total-return
figure (US 2.2, regions 2.7, wider set 2.1). The price-index set gives about 0.8, and the
lane says price indices flatter the level. Consistent.

## 3. Risk menu (#101, #105, #110)

(pending)

## 4. Live track records (survey-5 #78, survey-6 #91)

(pending)

## 5. Gates (wide-9 gate-null #93, wide-11 #109, weather-1 #116)

(pending)
