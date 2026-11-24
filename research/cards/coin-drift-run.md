# coin-drift-run: does letting held coin slots drift pay on a book of ~90 other coins?

Lane coin-drift-1, written 2026-11-24 (about 20:30 UTC), **before any return of the books
below was computed**. A mechanism check, not a pick. Idea `coin-drift-run` (`ideas.md`), seen
post hoc in wide-16 (`wide-16.md`, `cards/cost-band.md`, `results/cost-band.md`).

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-19 00:30): **3,130 tries,
N 1,032 for a new pick; measured rho 0.53 gives N_eff 486: a new rule needs z >= 4.69 against
`tsmom12` on the primary test (edge +0.30 close rule, +0.56 far rule); Bonferroni p <= 1.0e-4.**
`cost-band` already failed it on the primary test (z 2.76 and 2.35). Nothing in this card can
make a pick: it runs on a coin book the live strategies do not trade, and its bar (z >= 2) is
far below 4.69. A selectable claim would need a new card on the primary test at z >= 4.69.

## What was seen before this card (disclosed)

- wide-16's result: on the six assets, `tsmom12` with the gym's rebalance band at 0.05 instead
  of 0.01 earned +0.049 Sharpe (z 2.76); with coin fills free in both books still +0.054, so the
  fee saving explains about none of it; the mean coin share while held was unchanged (0.274 vs
  0.273); the gain sat in 2010-16 and 2017-21 (the 2017 and 2020-21 coin runs). On the six
  other coins (LTC, XRP, BCH, ETC, XLM, DASH, from 2017-08): +0.039 (z 2.47).
- cointop-1's coin book results (`cointop-1.md`, `results/cointop-1-coins.md`): its twin (`TS`,
  weights reset each Friday, 30 bps a side) had book Sharpe 0.72 on the selection set, worst
  loss 64%, decisions 2019-04 .. 2025-11; tops cluster in 2020Q1, 2020Q3, 2021Q2-Q4, 2024Q1,
  2024Q4 (about 19 effective top months).
- Nothing else. No book of this card (daily drift, gym band, gym costs) has been run on the
  coin book, on real or shuffled prices.

## Hypothesis

On a multi-coin trend book, trimming a held slot back to 1/n only when it is far from 1/n beats
trimming it back almost daily, **net of costs**, because a coin's return trends within a holding
spell: a slot that has run up keeps running more often than not, so trimming it is a small
anti-momentum trade. The alternative explanations to separate: (a) fewer trades (fees saved
and fee tiers), which pays even with no trend; (b) a trend of the coin market as a whole
(coins against cash), which is the same 2020-21 episode wide-16 saw and so not independent
evidence.

## Data: the coin book as cointop-1 defined it

- Coin Metrics community snapshot `2026-11-13`, breadth-1's book A (`breadth_books.cm_book()`):
  the 100 largest coins by 30-day median market cap among those with a year of prices and
  volume and size above the floors; no stablecoins or wrappers; dead coins in it. A value
  stamped day `x` is used from `x + 1`; a position decided on Friday `t` is set at the price
  stamped `t + 1` (cointop-1's `Lab`: `d`, `b`, `univ`, `up`, unchanged).
- **The selection set** (cointop-1's): the book without BTC and ETH (which generated the idea)
  and without LTC, XRP, BCH, ETC, XLM and DASH (wide-16's own out-of-universe set, where
  `band05` already showed +0.039). So the book shares no coin with either wide-16 test.
  Independent by asset, **not by time**: decisions 2019-04 .. 2025-11 contain the 2020-21 run
  that carried wide-16, and coins move together.
- Signal and slots: cointop-1's twin. Each Friday a universe coin whose 365-day log return is
  above zero gets 1 / (number of selection-set coins in the universe, about 90), the rest
  cash; nothing is held while fewer than 10 coins are in the universe.
- Train only: the panel is `cm-panel.npz` (bars to 2025-11-10); the script asserts that no row
  after 2025-11-10 exists. The held-out panel is not opened.

## The rule (frozen from wide-16) and how it is carried to ~90 slots

The only change between the books compared is the rebalance band; signal, slots, decision days
and costs are identical.

- **Why the band cannot be carried as 0.05 of equity.** The gym skips any trade smaller than
  `band` x equity, except a full exit, and an entry is such a trade. A slot here is about 1.1%
  of equity, so at `band` 0.05 (or 0.02, or even the default 0.01) no coin would ever be
  bought. In wide-16 the coin slots were 1/6 of the book (1/5 in 2013-16), and the cube-root
  law that set 0.05 used w = 1/6.
- **So the band is carried as a share of the slot, as it acted on a 1/6 coin slot in
  wide-16:** a held slot with target weight `w > 0` is traded back to `w` only once its value
  is at least `k x w x equity` away from it, with
  - `k = 0.06` (the gym's default 0.01 / (1/6)): the comparator, "trimmed back almost daily";
  - `k = 0.30` (0.05 / (1/6)): **`band05`, primary**;
  - `k = 0.12` (0.02 / (1/6)): **`band02`, secondary**.
  Entries (held 0, target > 0) and full exits (target 0) always trade (an entry is `w` away, so
  it is above every `k < 1`). No other `k` is run. The band is symmetric (losers are topped up
  at the same distance), as the gym's is; nothing else is changed.
- **Execution, as the gym's** (`gym._execute`): each day the target in force is that of the
  latest Friday decision (set at `t + 1`); trades happen at that day's price, sells first;
  when the buys that are outside the band need more cash than there is, slots above target are
  sold down to it even inside the band (audit G2); a buy that cash cannot pay in full buys what
  it can. A coin whose price stops is valued at its last price and, once its target is 0, sold
  at that price. Start equity 10,000 USD (the gym's `START_CASH`).
- **Costs, as the gym's** (`gym.COSTS`): every coin fill pays the Kraken taker fee of the tier
  set by the book's coin volume in the 30 days before that day (0.80% at no volume, falling with
  volume) and 0.05% slip on the price. Stated: not every coin of the book trades on Kraken; the
  gym's coin cost is used for all of them.

## Statistic

- Daily returns of the account (365 days a year). dSharpe = Sharpe(`band05`) - Sharpe(`k
  0.06`), same for `band02`.
- **Two cash conventions**: (a) cash earns 0 (`tries.md`'s convention); (b) idle cash earns the
  13-week bill (`harness.bill_rates()`, train sessions only), Sharpe above the bill. Required
  because a wider band holds slightly different cash (wide-16's rule, from diversifier-1).
- SE: paired stationary bootstrap of the difference (2,000 draws, mean block 20 days, seed 0;
  `stats._stationary_indices`), z = dSharpe / SE.
- Reported, not scored: the same with all costs at zero (the drift part alone, as wide-16's
  post hoc split); coin fills a year, fee and slip as a share of equity a year, the mean fee
  rate per traded dollar; the mean share of equity in coins on days a coin is held; tracking
  error and correlation of the pair; dSharpe per calendar year (2019 partial .. 2025 partial).

## Controls: the placebo books

The same code path on the same coin book, with the coins' daily log returns block-shuffled so
that a held slot has no trend of its own to ride. Blocks are calendar weeks of 7 days
(non-overlapping, from the panel's first day). Within a block, the coins that can be shuffled
are those with a known price on every day of the block and the day before, and that are
eligible for the book on the block's first day; every other coin keeps its own returns. Prices
are rebuilt from the shuffled returns (a coin keeps its first price and its missing days). The
book's universe (which coins are top-100) stays real; the trend signal, the slots and every
fill are recomputed from the placebo prices.

- **P1 (the brief's placebo): returns shuffled across coins.** In each block one random
  permutation of the shufflable coins: coin `i` gets coin `pi(i)`'s seven daily returns. Each
  day's cross-section of returns is kept exactly (so the coin market's move, its dispersion and
  the cross-coin correlation within the block stay), but a coin's own run lasts at most a week.
  What P1 keeps on purpose, stated: the trend of the coin market as a whole.
- **P2 (no trend at all): P1, plus the market's own path shuffled in time.** Each day's
  shufflable log returns are split into the cross-coin mean `m_t` and the rest `e_t,i`; the
  `e` are shuffled across coins as in P1, and the weeks of `m` are put in a random order (one
  permutation of all whole weeks; a week's seven days stay together). Coin `i` on day `t` gets
  `m` of the week moved there plus `e` of its partner. Every week's market move and every
  coin-week of idiosyncratic move still exists; no run lasts longer than a week.
- **40 shuffles of each kind** (seeds 1..40; gate-null's default), each run at `k` 0.06, 0.12
  and 0.30. The placebo statistic is the same dSharpe, computed by the same function.
- **Excess over a placebo** = d(real) - mean over the 40 shuffles of d(placebo); SE from the
  same paired date bootstrap applied jointly to the real pair and all 40 placebo pairs (the
  same resampled dates for every series), z = excess / SE. Also reported: the rank of d(real)
  among the 40 placebo d's (one-sided empirical p, smallest 1/41 = 0.024), and the placebo
  null's mean, SD, 5/50/95% and extremes (gate-null step 5).

## Pass bar (a mechanism check; each band on its own)

- **M1 (the effect, net of costs):** dSharpe > 0 with **z >= 2** in **both** cash conventions.
- **M2 (not fewer trades, not the coin market):** excess over **P1** with **z >= 2** (cash 0).
- **M2b (reported, decides the reading below):** excess over **P2** with z >= 2 (cash 0).

| Outcome | Reading |
|---|---|
| M1 and M2 hold for `band05` | **Mechanism confirmed** on the coin book: own-coin returns trend within a holding spell, and the wide band earns it net of costs. |
| M1 and M2b hold, M2 fails | Drift of the coin market as a whole (coins against cash), not of each coin: the same kind of gain wide-16 saw (coin slots against the rest of its book), in the same 2020-21 episode. **Not independent confirmation.** |
| M1 holds, M2 and M2b fail | Fewer trades (fees and tiers) or chance: **not confirmed.** |
| M1 fails | **Not confirmed** on the coin book (a fail does not kill wide-16's six-asset number, it removes the only independent support for its story). |

`band02` is read the same way, as secondary; the verdict is `band05`'s.

## Power (written before the run)

- **Episodes.** wide-16's gain sat in two coin bull runs. This book's years (2019-04 ..
  2025-11) hold about three: 2020-21, the 2023-24 rise, late 2024. The bootstrap's 20-day blocks
  treat the gain as if it were spread over about 120 blocks; it is not. So even z >= 2 here is
  "consistent with", not proof; the smallest honest p for "the mechanism exists" is that of
  about three episodes, which no test of this length can push below about 0.1. That is why
  this card can only confirm or fail to confirm a story, never select a rule.
- **SE.** The pair differs only in how far ~45 held slots drift. A slot drifting inside +-30%
  of itself (uniform, sd about 0.17 of the slot) on a coin with idiosyncratic volatility near
  90% a year gives about sqrt(45) x 0.17 x 0.011 x 0.9 = 1.1% a year of idiosyncratic tracking
  error; the common part (all held slots running together against cash) can add 1-3% a year.
  Against a book volatility near 35-45% and 6.6 years: SE of dSharpe about 0.01-0.03, so
  **z 2 needs about +0.02 to +0.06**. wide-16's sizes were +0.039 on six coins and +0.049 on the
  six assets; if the drift premium per coin is of that order, the test has a fair chance
  (roughly even) of z >= 2; if the effect is the coin-market path of 2020-21, M1 may pass and
  M2 fail.
- **Fees are larger here.** Every slot is a coin, so the comparator's near-daily trims cost far
  more of equity than in wide-16 (rough estimate before the run: several % a year at `k` 0.06),
  and the wider band saves much of it. **M1 can pass on fees alone**; that is what M2 and the
  costs-at-zero line are for.
- **Placebo excess.** Its SE is that of the real pair plus a little (the placebos are averaged
  over 40), so the excess needs about the same size again. The 40-shuffle rank can show at
  best p 0.024.

## Look-ahead and checks (tests before the real run)

Tests on synthetic prices (`tests/test_coindrift1.py`, offline, deterministic):

- the account on day `t` does not change when prices after `t` are scrambled (targets fixed);
- the placebo trend signal on decision `k` does not change when placebo prices after the
  decision's stamp are scrambled; the signal is lagged one day like the book's;
- band semantics: a 1/2 slot drifting 20% of itself is traded at `k` 0.06 and left at `k` 0.30;
  entries and full exits always trade; at `k` 0 with zero costs the account equals a daily
  reset to target;
- fee tiers: the fee rate of a day's fills depends only on fills of the 30 days before it;
- P1 keeps each day's multiset of shufflable returns; P2 keeps the multiset of weekly market
  moves; both keep every coin's missing days.

A plumbing run on random prices (`--synthetic`) only; **no dry run on real prices** (wide-16's
dry run printed real numbers by mistake). Then one real run.

## Rows in `tries.md` (idea `coin-drift-run`)

`k06` on the coin book: `baseline`; `band05@cm`, `band02@cm`: `robustness` (wide-16's
configurations on other data, after the choice); one `control` row per placebo kind and band
(the mean of the 40 shuffles); one `note` row for the costs-at-zero split. None is selectable
except the baseline, which is a benchmark.

## Not run, and why

- The literal bands (0.05 and 0.02 of equity, with entries forced through): a 1.1% slot would
  never be trimmed below 6% and never topped up, a buy-and-hold-within-spell book; a different
  rule from wide-16's, so not this card's test.
- Any other `k`, block length, book or period. The held-out year.
