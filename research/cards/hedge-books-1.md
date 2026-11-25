# hedge-books-1: a regret-guaranteed allocator (Hedge) across the existing books

Written 2026-11-24 ~23:55 UTC, lane `hedge-books-1` (DEEPER: combine models whose strengths
cover each other's weaknesses), branch from `main` fac43c9, **before any number of this card is
computed**. Research only: fake money, the research price cache, no change to the gym, the
runner or the live books. Train data only: no bar after 2025-10-31 is loaded.

## Question

Does an online-learning allocator with a regret guarantee, run across the project's existing
strategy books, beat `tsmom12`, or the equal-weight blend of the same books?

## Already tested? (read before writing this card)

- `universal-portfolio` (run 1, 2026-11-12): Cover's universal portfolio across the six
  **assets**, not across books. Dead: it stays near the constant mix it starts from.
- deep-1 Part B: three walk-forward mixes across 29 models (`stack`: least-like-it by risk;
  `switch`: best model per trend state; `meta`: ridge regression on all). None is an online
  learner with a regret guarantee; all fail. Its hindsight ceiling: best fixed mix 1.22.
- combo-1 / combo-2: two hand-picked equal-risk pairs (`blend-iv`, `blend-ws`), yearly refit.
  Fail (closest miss `blend-ws` 1.13 vs 1.05, p 0.059).
- evo-1 / evo-2: rule search, not allocation; multi-signal: a signal screen.

So multiplicative weights across books has not been run. This card runs it.

## The allocator (one published form, textbook rate, nothing tuned)

**Hedge** (Freund and Schapire 1997), in the form of the exponentially weighted average
forecaster of Cesa-Bianchi and Lugosi (2006), *Prediction, Learning, and Games*, Theorem 2.2:

- K books are the experts. Rounds are 7-day blocks ending at the end of a Thursday (UTC):
  theta_0 = 1994-02-03, theta_t = theta_0 + 7t, last theta_T = 2025-10-30, so **T = 1,656**
  rounds (from the calendar, not the data).
- Outcome of round t for book i: its gross return x_{t,i} = E_i(theta_t) / E_i(theta_{t-1}),
  from the book's own stand-alone gym replay (end-of-day equity).
- Loss, bounded in [0, 1] with no parameter: l_{t,i} = 1 - x_{t,i} / max_j x_{t,j} (the
  normalisation by the round's best expert that online portfolio selection uses, Cover 1991,
  Helmbold et al. 1998).
- Weights: w_{t,i} proportional to exp(-eta * sum_{s<t} l_{s,i}), uniform at the start.
- **eta = sqrt(8 ln K / T)** (the theorem's rate for a known horizon). Bound: Hedge's
  cumulative loss minus the best book's is at most **sqrt(T ln K / 2)**.

Expectation written before any number: the loss is linear in a book's weekly return, so Hedge
rewards a high *arithmetic* weekly return, not Sharpe. It should tilt towards the books with the
largest mean weekly return (the coin-heavy ones), and the bound (about 48 loss units for K = 16)
is likely larger than the spread of the books' cumulative losses, so it may also stay close to
the equal-weight blend.

**No look-ahead.** The weights used from the Friday decision theta_t + 1 to the Thursday decision
theta_{t+1} (inclusive) are w_{t+1}, computed from rounds 1..t only, whose last equity point is
the end of Thursday theta_t: both ETF closes (21:00 UTC) and the coin close (00:00 UTC Friday)
are before the Friday 22:30 UTC decision. Before the first Friday: uniform weights. A unit test
scrambles every book's equity after a date and checks the weights up to it are unchanged.

## The tradable book (weight level, one account, through the gym)

On each daily decision (22:30 UTC, every calendar day 1994-02-01..2025-10-31, the books' own
decision days), the combined target weights are sum_i w_i(day) x (book i's target weights that
day), summed per asset; long-only, sum at most 1 (each book's weights sum to at most 1 and w is on
the simplex). This one account is replayed through `gym.simulate` (unchanged) with the gym's 1%
band. The allocator's weights move weekly (the weekly rebalance); the books' own targets move
when the books trade, as they do on their own.

**Costs: the project's standard research costs** (protocol, as combo-1 and risk-menu): crypto
25 bps fee + 5 bps slip, ETFs 2 bps slip, for every book, the comparators and the combined
account. Robustness (logged, not judged): the same with the gym's live default costs (Kraken
taker tiers + 5 bps slip on coins). Prices dividend-adjusted (the protocol's primary test); idle
cash earns 0 (the protocol's convention).

## The book universe (fixed now, from books that existed before tonight)

K = 16, all long-only six-asset target-weight rules (SPY, QQQ, TLT, GLD, BTC, ETH):

- **The 12 live paper books** (`grimstrade.strategies.LIVE` at fac43c9): `buy_hold_btc`,
  `buy_hold_spy`, `sixty_forty`, `equal_weight`, `ts_momentum`, `xs_momentum`,
  `vol_target_spy`, `risk_parity`, `crypto_mean_reversion`, `preset_careful`,
  `preset_middle`, `own_vol_70`. Decisions as `gym.backtest` makes them (each day at 22:30 UTC,
  bars closed by then).
- **`tsmom12`** (the research yardstick, `c.weekly(c.slots(c.tsmom_signal))`, the harness
  baseline behind `BAR.md`).
- **Three research books** with weekly returns in `research/register/returns/`, named before
  tonight as the strongest finished near-misses: `halving-alone` (`halving`, #137, the closest
  result to the bar in SUMMARY.md), `where-vol` (`trend-where`) and `stop-0.25`
  (`cointop-1-stop`), the two models ahead of `tsmom12` on combo-1's failure map. Rebuilt with
  their logged code (`rules.macro_gate` with the halving-bear calendar, trend off, coins only;
  `trend_where.Where("vol")`; `cointop1_carry.rule(stop_ok)`). Check before use: each rebuild,
  run on the stored window (to 2025-11-09) at protocol costs, must match its stored Sharpe to
  0.005. The coin rebalance band (`cost-band`, #145) is left out: it is a band rule, not a
  target-weight rule, and the combined account has one band.

Picking research books that are known to have done well is in-sample for the choice. It can
only flatter the allocator, so it weakens a pass and strengthens a kill.

## Variants and comparators (all fixed now)

| Name | Kind | What |
|---|---|---|
| `hedge16` | variant (**primary, judged**) | Hedge over the 16 books |
| `ew16` | baseline | the same 16 books at fixed 1/16 each, same machinery |
| `hedge-pair` | variant (secondary, reported) | Hedge over `tsmom12` and `own_vol_70` only (K = 2, eta = sqrt(8 ln 2 / T)) |
| `ew-pair` | baseline | `tsmom12` and `own_vol_70` at 1/2 each |
| `tsmom12` | baseline | the comparator, rebuilt on this window and these costs |
| each of the 16 books alone | robustness | stand-alone replays (the experts' outcomes) |
| `hedge16`, `ew16`, `hedge-pair`, `tsmom12` at the gym's live costs | robustness | cost check |

Window for every judged number: daily returns 1994-02-01..2025-10-31 (365-day Sharpe, zero
risk-free rate, the repo's convention). All rows go to `research/tries.md` under idea
`hedge-books-1`.

## Pass / kill rule (primary `hedge16`; `hedge-pair` read the same way, reported only)

Paired stationary bootstrap of daily returns on the same days (mean block 20 days, 2,000 draws,
seed 0), SE = standard deviation of the bootstrapped Sharpe differences, z = difference / SE.

- **PASS** (a candidate for a separate held-out card, nothing more) only if both:
  1. z of Sharpe(`hedge16`) - Sharpe(`tsmom12`) **>= 4.70** (`BAR.md`, N = 500 effectively
     independent trials; the SE is this pair's own, so the bar applies at whatever correlation
     with `tsmom12` the book has; the correlation of weekly returns and the edge the close/far
     rule columns would ask are reported next to it).
  2. Sharpe(`hedge16`) > Sharpe(`ew16`) (it beats the equal-weight blend of the same books).
- **KILL** otherwise. Also reported, not bars: z against `ew16` (does the learning add anything
  over no learning: z >= 1.645 would say yes for this one pre-registered comparison), worst
  loss, growth a year, Sharpe since 2003 and in 2022-25, average and final weights, the
  effective number of books (1 / sum w^2).

## Regret actually achieved (reported for `hedge16` and `hedge-pair`)

1. In the theorem's units: Hedge's cumulative loss minus the best single book's, against the
   bound sqrt(T ln K / 2).
2. In log wealth on the experts' outcomes: log of the best single book's growth over the T
   rounds minus log of Hedge's (sum_t log(w_t . x_t)), and per year.
3. In log wealth on the tradable book: the gym replay of `hedge16` against the gym replay of
   the best single book in hindsight (by final wealth) and of the best by Sharpe.

## Family and multiple testing

New pick, new family `hedge-books-1`: two `variant` rows (`hedge16`, `hedge-pair`), two
baselines, and robustness rows. Project-wide count and bar quoted from `BAR.md` (2026-11-24
20:01): 3,855 tries, N for a new pick 1,083, N_eff 500, z >= 4.70.
