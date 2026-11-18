# Wide 2: two more mechanisms from wide-1's list (trend age, patch-leaving)

Research run wide-2, 2026-11-18, two bursts of about ten minutes each. **Both picks fail on
train.** The first is described first; the second has its own section below. Branch `wide-2` (from
`wide-1`). Research only: fake money, public data, no change to the gym, the daily runner or the
live strategies.

Question: wide-1 wrote down 46 mechanisms from other fields and tested 4. Of the 42 left, which
one is most worth a test on the six assets' weekly data, and does it pass?

## In plain words

**It fails. Waiting four weeks before trusting a new trend makes the trend rule worse, not
better: Sharpe 0.99 against 1.05 for plain `tsmom12`, behind in all five eras. The held-out
year was not looked at.**

- **Picked:** Q5, "the chance a trend ends depends on its age" (queueing / reliability theory:
  hazard rate of a renewal process). Reason: it needs only weekly closes, has over a hundred
  dated events instead of a handful of bear markets, and wide-1 killed it by argument, with no
  number. Most of the other 41 need data we do not have, or are a tested idea in other words.
- **Rule** (`cards/trend-age.md`, pushed before any number): hold an asset's slot only if its
  12-month trend signal is on this Friday and was on at each of the three Fridays before. Entry
  three weeks later than `tsmom12`, exit the same week. One variant, nothing fitted.
- **Bar:** the protocol's default, with p < 0.10 / 42 = 0.0024 because this was the pick of 42.

| | `age4` | `tsmom12` |
|---|---:|---:|
| Sharpe, six assets, 1994-2025 | 0.99 | 1.05 |
| Difference (90% range; share of bootstrap draws with the twin ahead) | -0.06 (-0.11 to -0.01; 97%) | |
| Eras ahead | 0 of 5 | |
| Return a year | +16.4% | +17.8% |
| Max drawdown | 37.9% | 36.5% |
| Trades a year (turnover) | 1.9 | 2.7 |
| Other ETFs / other coins / four indexes (difference) | +0.00 / -0.17 / -0.02 | |

**The mechanism is real, the trade is not.** The hazard is front-loaded as claimed: of 111
on-spells of the signal, 21% ended in their first week, 15% a week in weeks two and three, 5%
in week four, and 1.5% a week after that. 50 of 111 spells were over within four weeks, and the
rule skips them all. It still loses. My reading of why (points 1 and 3 are reasoning from the
tables, not separately measured):

1. **A whipsaw is cheap.** The signal flips when the price is about where it was a year ago. A
   spell that dies in two weeks buys and sells near that same price; the loss is mostly the cost
   of the round trip (4 bps in ETFs).
2. **The first three weeks of a spell that lasts are not cheap to miss.** The rule holds 71% of
   the book on average against 76%, and gives up 1.4 points of return a year for 0.4 points
   less volatility.
3. **In coins, where a round trip costs 60 bps and whipsaws should hurt most, it is worst**
   (-0.17 on the six other coins): new coin trends move too fast to wait three weeks.

**How sure.** Sure it does not help: the whole 90% range of the difference is below zero, every
era agrees, and two of three out-of-universe sets agree. Not a proof that no age rule works: one
delay (four weeks) was tested, on purpose. The DAX alone came out ahead (+0.08, p 0.02); it is
one of seven side comparisons and the FTSE went the other way by as much (-0.09).

**Compared with my guess before any number** (card): 3% chance of a pass, difference between
-0.05 and +0.03. It came out at -0.06, just below that range. The hazard table came out as
expected.

**What it teaches.** wide-1's kill reason ("changes when the trend rule acts, not where the edge
comes from") now has a number behind it. wide-1 already lists three smoother trend rules as
dead (`ensemble-tsmom`, `drawdown-control`, `fracdiff-momentum`); a delayed entry joins them.
Entry timing of the trend rule does not look like a place where anything is left.

**Next lanes.** None from this card. wide-1's three (month-end bonds, a volume screen, the
month-end stock bounce with a placebo) stand as written.

## Second pick: patch-leaving (burst 2, same day)

**It fails too, on all five bars, and by more: Sharpe 0.85 against 1.05 for `tsmom12`. The
held-out year was not looked at.**

- **Picked:** E6, optimal foraging's marginal value theorem ("leave a patch when its yield falls
  below the average of all patches"). Reason: price-only, decides every week, never run on the
  six assets as a rule, and it does not sit in cash (wide-1's lesson 3).
- **Rule** (`cards/patch-leaving.md`, pushed before any number): keep the twin's total
  exposure, but hold only those in-trend assets whose 12-month return per unit of risk is at
  least the average of all eligible assets; split the weight equally among them. One variant.
- **Bar:** as before, p < 0.10 / 42 (every pick out of the 42 is counted).

| | `mvt` | `tsmom12` |
|---|---:|---:|
| Sharpe, six assets, 1994-2025 | 0.85 | 1.05 |
| Difference (90% range; share of bootstrap draws with the twin ahead) | -0.19 (-0.36 to -0.02; 97%) | |
| Eras ahead | 0 of 5 (1994-99 is a tie: SPY alone) | |
| Return a year | +18.6% | +17.8% |
| Volatility | 23.2% | 17.1% |
| Max drawdown | 53.2% | 36.5% |
| Trades a year (turnover) | 9.7 | 2.7 |
| Assets held on an average invested Friday | 2.1 | 3.1 |
| Other ETFs / other coins / four indexes (difference) | -0.06 / -0.39 / -0.06 | |

**Why (read from the table, not separately measured).** The rule earns slightly more a year and
pays for it with a third more volatility: it holds two assets where the twin holds three, so
the book loses the spread across assets that makes `tsmom12` smooth. It also trades 3.6 times
as much, because "above or below the average" flips far more often than "above or below zero".
It is below even equal weight (0.88). Every out-of-universe set has the same sign; the coins,
where each switch costs 60 bps, are worst.

**How sure.** Sure: all five bars fail, the 90% range is below zero, and all three other sets
agree. It is one form of the idea (no switching band, equal split); a band would cut the trading
but not the concentration, which is where most of the gap comes from.

**Compared with my guess** (card): 2% chance of a pass, -0.15 to +0.05, a clearly deeper
drawdown. It came out at -0.19, below the range; the drawdown was as feared (+17 points).

**What the two picks say together.** Both changed *which* trend positions are held or when
(later entry, fewer and stronger assets), and both lost to the plain rule. The 40 mechanisms
left on wide-1's list are mostly gates, smoother trends or ideas that need other data; neither
test gives a reason to card a third from the price-only ones.

## Disclosures

- **`patch-leaving`: one run, no dry run** (2026-11-18 11:16 UTC), 4 rows in `tries.md` (1
  variant, 3 robustness); two more tests in `tests/test_wide2.py` (same exposure as the twin,
  never an asset the twin does not hold, no later bar read). The repo checks were run before
  its card was pushed. An asset whose z cannot be computed is left out of the average.
- **One run, no dry run.** The script ran once (2026-11-18 11:13 UTC); plumbing was checked by
  `tests/test_wide2.py` on synthetic bars (entry three weeks after the twin, exit with it, no
  bar after the decision read). 7 rows in `tries.md`: 1 variant, 6 robustness.
- **The card commit was pushed before the repo checks were run** (it changed one markdown file).
  The checks were run, and passed, before the next push.
- **Price cache:** copied from the wide-1 worktree (the cache wide-1 used). `tsmom12` and equal
  weight reproduce 1.05 and 0.88.
- **Reading of bar 4** for the indexes (mean of the four differences) was on the card before
  the run.
- **Holiday Fridays:** when a set has no bar on a Friday, the three earlier checks are still
  anchored on Fridays (7, 14, 21 days before that Friday), as the card says.
- **The choice of Q5 was mine, made in a few minutes** from wide-1's one-line verdicts; the 41
  others were not re-examined in depth.
- **Not run:** the held-out year.

Tables: `results/trend-age.md`, `results/patch-leaving.md`. Scripts:
`lib/idea_wide2_trend_age.py`, `lib/idea_wide2_patch_leaving.py`.
