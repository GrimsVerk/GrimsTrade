# Wide 16: how to build and size the book, ideas from other fields, one tested on a design that can pass

Research run wide-16, 2026-11-24. Branch `wide-16` (from `main`), draft PR into `main`.
Research only: fake money, the price cache on disk, no change to the gym, the daily runner or
the live strategies. Train only: no bar after 2025-11-10 is loaded; the held-out year is unread.

**Why this run changes kind.** wide-1 .. wide-15 scored about 87 mechanisms, almost all of the
shape "a calendar or flow dose predicts the next weeks' return", and gated 22: all failed. With
40 placebos the smallest reachable rank p is 1/41 = 0.024, while the family bar is near 0.001,
so most of those gates could only kill. This run asks a different question: not *what* to hold,
but *how much and how to keep it*, with a test whose pass region is reachable (a paired Sharpe
difference against `tsmom12`, whose standard error shrinks as the rule gets closer to
`tsmom12`).

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-19 00:30): **3,130 tries,
N 1,032 for a new pick; measured rho 0.53 gives N_eff 486: a new rule needs z >= 4.69 against
`tsmom12` on the primary test (edge +0.30 for a close rule, +0.56 for a far one); Bonferroni
p <= 1.0e-4 (z 3.71).**

## Step 1. Candidates, checked against the record (2026-11-24, before any number)

"Kill" means the book change is a tested idea in other words; the record that tested it is
named. Records read for this table: `ideas.md` (all tables), `results/` and `cards/` for
kelly-shrunk, universal-portfolio, vol-target, trend-vol, ensemble-tsmom, drawdown-control,
crypto-slot-size; `risk-menu.md`, `vol-timing.md`, `combo-1.md`, `combo-2.md`, `rp-1.md`,
`diversifier-1.md`, `eu-3.md`, `eu-4.md`, `trend-tune.md`, wide-2's `trend-age` and
`patch-leaving`, and wide-15 (branch `origin/wide-15`, PR #139).

| # | Candidate | Field | What it would change in the book | Overlapping record | Verdict |
|---:|---|---|---|---|---|
| B1 | Bet-hedging with a dormant fraction (Cohen 1966, seed germination: germinate only a fraction g each year) | Evolutionary ecology | Keep a fixed share of every slot held whatever the signal (the "seed bank"), the rest timed by `tsmom12` | combo-1 `blend-iv` (`tsmom12` + always-held inverse-vol, 1.07, p 0.39); insure-2's fixed-exposure controls (trend is cheaper insurance than holding less in every era); deep-1-meta (average of sleeves) | **Kill**: a trend/hold blend, tested |
| B2 | Phenotype switching with sensing (Kussell and Leibler 2005: switch at the environment's rate; with a noisy sensor, bet in proportion to the posterior) | Systems biology | A soft slot: weight = posterior probability the asset is in an up-trend, or a lookback matched to the regime length | kelly-shrunk (posterior-proportional Kelly = inverse-vol, +0.01); ensemble-tsmom (share of 1/3/6/12-month signals positive, +0.05, p 0.21); trend-tune surface (lookback plateau 6-12 months, best cell inside luck); ml-sizing | **Kill**: proportional betting and lookback matching, tested |
| B3 | Shannon's demon between the trend book and cash (volatility pumping with a constant share f) | Information theory | Hold f of `tsmom12`, rest cash, rebalanced to f | vol-timing's `const` row (0.26 x `tsmom12` + bills: Sharpe identical by construction); risk-menu (constant shares are a risk dial) | **Kill**: a constant scale cannot move Sharpe; the pumping gain is growth, not Sharpe |
| B4 | Shannon's demon *among the slots*: how tightly to rebalance volatile, weakly correlated slots (pump) against letting them drift (let winners run), when each rebalance costs a fee | Information theory x stochastic control | The drift rule inside a held slot: today every slot is topped up or trimmed to 1/n whenever it is 1% of equity away (gym band); coins pay 0.8% taker plus 0.05% slip per trade at small volume | eu-3 V0 (drift checked weekly instead of daily, coin-free EUR book: 2 orders a year saved, no Sharpe effect); never on coin slots, never cost-optimal | **Keep** (merged with C1) |
| E1 | Ecological portfolio effect (Tilman 1996; Doak et al. 1998: variance of the sum falls with the number of weakly correlated species) | Community ecology | More, less correlated slots | ls-trend-2's 34-ETF book, breadth-1, the 8-ETF out-of-universe set (`tsmom12` weaker there), trend-where | **Kill**: breadth, tested |
| E2 | Functional groups (species in one functional group add no stability): one budget per group (stocks, bonds, gold, coins) | Community ecology | SPY+QQQ share one slot, BTC+ETH share one slot | eu-3 V4 `c4` class slots (+0.09, p 0.19, drawdown +3.5); crypto-slot-size (Sharpe flat from 5% to 1/6 per coin); rp-1 / `where-rp` (risk budgets) | **Kill**: class slots and coin size, tested |
| E3 | Taylor's power law (variance scales as a power of the mean) as a risk forecast for sizing | Population ecology | Size each slot by a variance forecast from the cross-asset mean-variance law | vol-target, trend-vol, own-vol targeting (risk-menu, vol-timing): any variance forecast used to size is a volatility target; on returns (mean near 0) the law has no hold | **Kill**: a volatility target in other words |
| R1 | k-out-of-n voting across several trend lookbacks (redundant sensors, majority logic) | Reliability engineering | Hold a slot when k of n lookbacks agree, or hold k/n of it | ensemble-tsmom (exactly k/n over 1/3/6/12 months); turning-points (literature); multi-signal | **Kill**: tested in other words |
| C1 | Deadband (hysteresis) on the *weights*, sized by the cost of a correction: the no-trade region of control with proportional costs (Magill and Constantinides 1976; Davis and Norman 1990; width by the cube-root law of Rogers 2001 and Janecek and Shreve 2004), trading back to the band's edge, not to the target | Control theory (stochastic control with proportional costs) | A coin slot in trend is left to drift inside a band of about +-5 points around 1/n and only pulled back to the band's edge; signal entries and exits unchanged; ETF slots unchanged (their theory band, about 1.4 points, is near the gym's 1%) | Hysteresis on the *signal* is eu-4 C2 `dz25` (deeper covid drawdown); eu-3 V0 above. No record changes how a held coin slot is rebalanced | **Keep: the pick** |
| C2 | Anti-windup / slew-rate limit on exposure changes (a slot moves at most 1/k of its size a week) | Control theory | Entries and exits spread over k weeks | trend-age (entry after four Fridays: 0.99 vs 1.05, dead); eu-4 C1 `confirm2` (exit a week later: covid drawdown +3.3 points); eu-3 V3 `hold4w`; trend-tune (later exits cost what fewer whipsaws save) | **Kill**: slower entries and exits, tested; the exit side is the insurance |
| C3 | Temporal bet-hedging / tranching (sub-books re-deciding on different Fridays of the month; "rebalance timing luck") | Evolutionary ecology x portfolio practice | Each slot holds the average of its last four Friday signals | Same as C2 with k = 4 (a moving average of the on/off signal); the signal is already weekly, so timing luck is small | **Kill**: C2 in other words |
| Q1 | Leaky / token bucket on orders (an order budget that refills at a fixed rate) | Queueing theory | At most m drift orders a month per slot | eu-3 / eu-4 order budgets on the coin-free book; on coins it is a crude form of C1 (the band is the cost-optimal order budget) | **Kill**: merged into C1 |
| Q2 | (s, S) inventory policy: reorder only below s, then up to S | Operations research | The band's edges and the refill point | C1's "trade to the edge" is the (s, S) policy with S = s for a two-sided band | **Kill**: merged into C1 |
| A1 | Ruin theory / a floor: exposure = m x (equity - floor) (CPPI) | Actuarial science | Book exposure falls as a drawdown deepens | drawdown-control (+0.07, p 0.14, "a smoother trend rule") | **Kill**: tested |
| F1 | Ideal free distribution (foragers spread in proportion to patch quality) | Behavioural ecology | Weight in-trend slots by trend strength | patch-leaving (hold only the stronger in-trend assets: -0.19, dead); ml-sizing (follow a forecast: worse) | **Kill**: tested |
| S1 | Derating / safety factors (run parts below their rating when stress is high) | Structural and electrical engineering | Cut a slot when its volatility is high | vol-target, trend-vol, own-vol (risk-menu) | **Kill**: a volatility target |

**What survives.** Of 16 candidates, 14 are tested ideas in other words. The two that survive
(B4, C1) are one book change: how a held, volatile, costly slot is kept near its size. It is
the only candidate that changes neither the signal nor the average exposure, so it is the only
one whose paired test against `tsmom12` has a small standard error, and the only one whose
gain, if any, comes from something close to certain (fees not paid) rather than from a
forecast. That is also its weakness: the gain cannot exceed what the drift trades cost today.

**Before the card: the size of the prize (step 1b, below).** Before freezing a rule, the
ceiling is measured on the baseline alone: `tsmom12` replayed with zero cost on coin trades
(not a rule anyone can trade; no new configuration of a rule). If even removing every coin fee
cannot reach z 4.69, no rule of this kind can pass on the primary test, and the card says so.

## Step 1b. The size of the prize (baseline only, 2026-11-24 about 19:43 UTC; first written as "~20:15", a slip)

`uv run --with numpy python research/lib/wide16_ceiling.py`: `tsmom12` through the gym, once
with its costs (Sharpe 1.045, the logged 1.05) and once with coin fills free. No rule, no try
(one `note` row in `tries.md`).

| Coin fills from 2015 (10.9 years) | Fills a year | Volume, x equity a year | Fee, % of equity a year | Slip |
|---|---:|---:|---:|---:|
| Entries | 1.6 | 0.27 | 0.106% | 0.013% |
| Exits | 1.4 | 0.23 | 0.081% | 0.012% |
| Drift top-ups and trims | **59.4** | **0.75** | **0.242%** | 0.038% |

Erratum (after the real run, 2026-11-24 19:50 UTC): the first version of this table, the one
the card quotes, counted coin fills from BTC's first eligible year (2013) but divided by the
10.9 years from 2015, so it read 1.7 / 1.5 / 76.1 fills a year and drift costs 0.378% + 0.053%.
Fixed in `wide16_ceiling.py` (date filter); the rows above are the corrected ones and match
the run's own count (59.4 drift fills, 0.279% a year for `tsmom12`). The ceilings below never
used the per-year table and do not change. The card's band does not depend on these numbers.

| Ceiling (not tradable) | dSharpe vs `tsmom12` | Paired SE | z |
|---|---:|---:|---:|
| All coin costs zero, 1994-2025 | +0.0103 | 0.0017 | 6.0 |
| All coin costs zero, from 2015 | +0.0175 | 0.0038 | 4.6 |
| Only the drift fills' costs added back, 1994-2025 (approximate) | +0.0085 | 0.0008 | 10.0 |
| Same, from 2015 | +0.0134 | 0.0010 | 14.1 |

Reading: the whole coin cost budget is worth about +0.01 Sharpe, but it is a steady stream,
so its z is high. A rule that kept the book and stopped paying for drift could clear z 4.69;
the question is how much tracking noise the saving brings with it. The card
(`cards/cost-band.md`) states the power before any run: the noise allowed is about 0.16 s % a
year, the expected noise 1-2% a year, so the expected result is a fail.

## Step 2. The pick: `cost-band` (card `cards/cost-band.md`, pushed before any run)

C1 + B4: `tsmom12`'s weights unchanged, only the gym's rebalance band widened, so a held slot
is traded back to 1/n only once it is `b` of equity away. `band05` (primary): b = 0.05, the
cube-root law's no-trade half-width for a 1/6 coin slot at the gym's zero-volume coin cost
(0.85%) and risk aversion 2. `band02` (secondary): b = 0.02. Pass = z >= 4.69 on the primary
test in both cash conventions (cash 0 and above bills), dSharpe > 0 on the 6-coin set, max
drawdown at most 1 point worse. Power stated in the card before the run: the bar is reachable
(drift costs alone are worth z 10 at zero tracking error), but the tracking error allowed is
about 0.16% a year x the share of the cost saved; expected z 0.5-1.5, expected fail.

Order: card 0320cf7 (19:45 UTC), script and tests 0c76dca (19:48), one dry run (see the card's
disclosure: it printed the last 120 days' pass lines by mistake), then one real run (19:48).

## Step 3. Result (one real run, 2026-11-24 19:48 UTC): fails the bar, nearest miss on this design

Tables: [`results/cost-band.md`](results/cost-band.md) (`uv run --with numpy python
research/lib/wide16.py`).

| Primary test, 1994-2025 | Sharpe | dSharpe vs `tsmom12` | Paired SE | z | One-sided p | Max DD | Turnover | Coin drift fills/yr (cost) | Tracking error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` (b = 0.01) | 1.045 | - | - | - | - | 37.4% | 2.81 | 59.4 (0.28%) | - |
| `band05` | 1.093 | **+0.049** | 0.018 | **2.76** | 0.001 | 32.5% | 2.06 | 6.2 (0.16%) | 1.48% |
| `band05`, above bills | 0.982 | +0.051 | 0.017 | 3.04 | 0.001 | | | | |
| `band02` | 1.058 | +0.014 | 0.006 | 2.35 | 0.007 | 36.1% | 2.44 | 22.7 (0.21%) | 0.56% |
| `band02`, above bills | 0.943 | +0.012 | 0.006 | 2.13 | 0.013 | | | | |

| 6 other coins, 2017-08..2025 | Sharpe | dSharpe | SE | z |
|---|---:|---:|---:|---:|
| `tsmom12` | 0.520 | - | - | - |
| `band05@coin` | 0.559 | +0.039 | 0.016 | 2.47 |
| `band02@coin` | 0.527 | +0.007 | 0.006 | 1.08 |

Per era (`band05` minus `tsmom12`): 1994-99 0.000, 2000-09 -0.004, 2010-16 +0.079, 2017-21
+0.133, 2022-25 +0.007. The gain sits in the coin years, mostly the 2017 and 2020-21 runs.

**Verdict: both fail the project bar** (z 2.76 and 2.35 against 4.69, in both cash
conventions); conditions 2 and 3 hold (coins positive, drawdown 4.9 points smaller). Even
the family bar of wide-15's count (p < 0.00115, z about 3.05) is not met; the above-bills
reading of `band05` (z 3.04) sits right at it. Nothing goes to the paper book.

**It is not the fee (post hoc, not a try: `lib/wide16_posthoc.py`, coin fills set free in
both books).** The card's mechanism was the fee saving; the run says otherwise:

- Total coin costs fall only from 0.55% to 0.44% of equity a year (2013-2025): coin volume
  falls 40%, but the fee per dollar rises from 0.41% to 0.55% because fewer fills mean less
  30-day volume and a dearer Kraken tier.
- With coin fills free in both books, `band05` still leads by **+0.054** (`band02` +0.015); the
  fee and tier part is about zero (-0.005 on the six, +0.008 on the coins).
- The mean coin share of the book while coins are held is unchanged (0.274 against 0.273), so
  it is not "more coin". It is *when*: a coin slot left to run above 1/6 after a rise, instead
  of being trimmed back daily, earned more in the coin bull runs. That is a short-horizon trend
  bet inside the slot (daily trimming of a rising coin is anti-momentum), found here after the
  fact, on the data that found it.

**The power statement was wrong in its expectation, not in its arithmetic.** The card
expected z 0.5-1.5 from a fee saving drowned by tracking noise. The tracking error was as
predicted (1.5% and 0.6% a year), but the drift itself earned a return, which the card had
named as the only way to a pass and called implausible. It earned enough for z 2.8, not 4.7.

## What this says about the kind

- **Sizing and building ideas from other fields mostly are tested ideas in other words**:
  14 of 16 candidates map onto a tested record (blends with holding, Kelly and soft signals,
  constant scale, breadth, class slots, volatility targets, lookback ensembles, slower
  entries/exits, order budgets, drawdown floors).
- **Where the bar is reachable.** On the primary test the bar can be met only by a gain that
  is nearly riskless relative to `tsmom12`: the whole coin cost budget is worth z 6.0, the
  drift costs z 10 at zero tracking error. Any rule that changes exposure has a paired SE of
  0.006 (2-point band) to 0.1 (own-vol) and needs +0.03 to +0.5 Sharpe. A close rule (corr
  0.9962 here) brings the bar in Sharpe units down to about +0.08, but nothing in the book's
  costs is worth that; only a return effect is.
- **The one lead.** `coin-drift-run` (`ideas.md`): let held coin slots drift. Seen post hoc,
  two bull runs carry it (2017, 2020-21), and no untouched data exist to test it (the 6-coin
  set from 2017 is the only other coin history and was already run: +0.039). Weak; a card
  would have to be a forward test on the paper trail.

## Count

wide-15's count was 87 mechanisms (if both of its gates are counted), 22 gates, none passed.
This run adds **1 mechanism tested by a strategy (`cost-band`, 2 variants), 14 killed as
overlaps (not counted, as wide-12/13 did for the scored-but-parked), none passed**: 88
mechanisms, 19 strategy tests, 22 gates, none passed.

Rows in `tries.md` (idea `cost-band`): `band05`, `band02` (variant); `band05/bills`,
`band02/bills`, `band05@coin`, `band02@coin` (robustness); two `note` rows (the step-1b
ceiling and the post-hoc split, neither a try). The held-out year was not read.
