# Card: asset-ledger-1 (what trend-timing buys and costs, per live asset, in one ledger)

Lane `asset-ledger-1`, 2026-11-25 (night, UTC). Descriptive re-score of finished tries with
merged code, unchanged: no new rule, no tuning, nothing selectable. Written and pushed before
any number of this lane is computed.

## Question

Per live asset of `tsmom12` (SPY, QQQ, TLT, GLD, BTC, ETH) and per long proxy the project
already uses for them, in one consistent ledger: what has trend-timing the asset bought (fall
gain) and cost (late buy-back, calm drag), what is the net against holding it, and how much of
the six-asset book's worst drawdown did the asset carry with and without timing?

## Already done? (checked before this card)

- gap-2002-1 (#162): fall gain I, rebound lag B, calm drag C by date, 2002-2025 only, on the
  French US market, 10 French industries and the S&P 500 TR. Not the six assets, not their
  long proxies, no calm split, no book drawdown.
- calm-drag-1 (#203): C split into cost K, premium P, timing T (and by spell) on the six and
  the US series. No I, no B, no net, no bond or gold proxy, no book drawdown.
- rev-costloss-1 (#182): the exit scored as a crash warning (hit and false-alarm rates, value
  at a cost/loss ratio). No log-point ledger.
- risk-menu (#101, #105, #110): book-level growth, worst loss and crash returns of eleven ways
  to hold the six. No per-asset split, no per-asset contribution to the worst drawdown.
- insure-2 (#87, #90): per-fall share avoided and premium on US series and other markets; not
  the six's ETFs, gold or bonds.

So the per-asset table (a)-(e) does not exist yet; its C-split columns reuse calm-drag-1's
code and must reproduce its numbers.

## Data (all in the cache; no download)

Rows (ledger series), each over its longest clean history and over 2002-01-01 .. 2025-10-31:

| Live asset | Series | Loader (merged, unchanged) | Own window |
|---|---|---|---|
| SPY, QQQ, GLD, TLT, BTC, ETH | adjusted train bars, the paper series `trend_tune.paper` (Friday decisions, gym costs one way) | `calmdrag1.load_six` (= rev-costloss-1's `six()`) | first eligible session .. 2025-10-31 |
| SPY (long) | French US market, daily | `calmdrag1.load_french()[0]` (insure-1's paper series) | 1927-07-02 .. 2025-10-31 |
| SPY (long) | S&P 500 total return, daily | `calmdrag1.load_spx` (insure-3) | 1986-07-01 .. 2025-10-31 |
| QQQ (loose proxy) | French HiTec industry, daily | `calmdrag1.load_french()` | 1927-07-02 .. 2025-10-31 |
| TLT (long) | 30-year constant-maturity Treasury rebuilt from `DGS30` (data-long-3, exact par-bond repricing; pooled-2's US bond series) | `long_x_build.daily_bond("DGS30", 30)`; the rule is insure-1's paper series on those returns (`trend_1926.bars`, `trend_tune.paper`, 2 bps a side), eligibility from the paper series | first eligible session (1978) .. 2025-10-31 |
| GLD (long) | datahub monthly gold (data-long-1/2; monthly averages of the London fix, from 1971, `long_gold.FREE_FROM`) | `trend_where_long.load_series()["gold"]` and its monthly `tsmom12` (`weights(g, "tsmom12", 1)`, 2 bps on weight changes, cash 0) | first eligible month (1972) .. 2025-10 |

Gold monthly is the only long gold the project has (LBMA daily and the Pink Sheet are blocked
to scripts, data-long-3). Monthly averages are smoothed, which flatters trend timing (the
jst-autocorr-1 caveat), so its rows are flagged and also run on 2005-2025 next to GLD as a check
of how far the averaged series is from the ETF. No long proxy exists for the coins.

Bills (secondary convention only): `^IRX` (insure-3's `bill_returns`) for the six, S&P, UST30;
French RF for the French series; none for monthly gold (cash 0 only).

The book for (e): the six-asset train panel (`common.ctx("six")`, 1994-02-01 on, adjusted
bars), the gym twins already logged by `baselines.py`: `tsmom12` (equal slot per eligible
asset, held while its 365-day log return is > 0, Friday decisions) and `equal-weight` (the same
slots, always held: the book without timing). Gym costs, cash 0 (the protocol's convention),
re-run with `log=False` (same configuration, already counted). Nothing after 2025-10-31.

## Definitions (fixed now)

**Labels, per series.** gap-2002-1's and calm-drag-1's (`calmdrag1.labels`): on the series'
own total-return index over its whole loaded history, zigzag 25% down / 25% up; fall =
sessions (peak, trough]; rebound = (trough, earlier of trough + 365 days and the next peak];
calm = the rest. Monthly gold: the same function on monthly sessions.

**Window.** Eligible sessions dated in the window; Y = (window end - max(window start, first
eligible session)) / 365.25 (calm-drag-1's divisor; equals gap-2002-1's on its rows).

**Per session**, log points (x 100): d_t = ln(1 + r_rule) - ln(1 + r_hold), r_rule = pos bar -
c flip + (1 - pos) rf (rf = 0 at cash 0, primary).

- (a) **Fall gain I** = sum of d_t over fall sessions / Y (log points avoided in 25%+ falls).
- (b) **Late buy-back cost B** = sum over rebound sessions / Y (negative = cost).
- (c) **Calm drag C** = sum over calm sessions / Y, split exactly as calm-drag-1 does
  (`calmdrag1.decompose`, unchanged): C = cost K + premium P + timing T. Also the out share of
  calm time.
- (d) **Net N = I + B + C** = the whole gap to holding over the window (log points a year;
  negative = timing trailed holding). Shown at cash 0 and with idle cash at bills.
- "The insurance paid for its premium" on a row means N > 0 there: the fall gain exceeded
  the buy-back cost plus the calm drag. Descriptive, one history, no standard error.
- Also per row: the number of 25% falls whose trough lies in the window.

**(e) Book worst drawdown.** For each book (with timing: `tsmom12`; without: `equal-weight`),
worst peak-to-trough drawdown of its gym equity over the window (1994-02-01 .. 2025-10-31, and
the same run's equity from 2002-01-01 on). Contribution of asset i = its dollar P&L over the
drawdown's sessions (peak, trough], rebuilt exactly from the gym's fills and the bar prices
(position value change plus the cash it took or gave, fees and slippage included), divided by
equity at the peak; the six contributions sum to minus the drawdown (check: residual below
1e-9 of equity, reported). Share = contribution / sum of contributions. Shown: each book's own
worst drawdown with its dates, the asset shares, and (side table) the `tsmom12` book's
contributions over the `equal-weight` book's worst-drawdown dates.

**Checks** (a mismatch above 0.01 is reported, not fixed): C of the six (own window, cash 0)
equals calm-drag-1's (SPY -1.51, QQQ -2.08, GLD -1.43, TLT -2.28, BTC +0.00, ETH +0.00);
French US market and S&P 500 TR 2002-2025: N, I, B, C equal gap-2002-1's (-1.41 / +6.64 /
-5.89 / -2.16 and -1.00 / +4.93 / -4.28 / -1.65); I + B + C = N to 1e-9 on every row; my
re-simulation of each book equals the harness run's equity.

## Expectation (stated so it can be wrong)

- US stocks (SPY, French market, S&P): fall gain larger than the buy-back cost; net about -1
  since 2002, closer to 0 over the long record. QQQ: large I and B, net negative since 2002.
- TLT and the 30-year proxy: few 25% falls (2020-2023 is the big one), small I, net about
  -1 to -2 a year: the insurance has not paid there. GLD: one big fall (2011-2015) avoided in
  part, net about -1. Monthly gold 1972-2025: net closer to 0 or positive (averaging flatters).
- BTC and ETH: I and B both very large; net unclear in sign.
- Book: without timing the worst drawdown 1994-2025 is 2000-2002, carried mostly by QQQ; since
  2002 the 2021-2022 coin crash, carried mostly by BTC and ETH. With timing the worst drawdown
  is smaller and also coin-led.

## Output and rows

- `research/lib/assetledger1.py` (calls merged loaders and `calmdrag1.decompose` unchanged)
  writes `research/results/asset-ledger-1.md`; tests `tests/test_assetledger1.py` (offline,
  synthetic) for the new glue: I/B/C sum, window divisor, book attribution sum.
- `research/asset-ledger-1.md`: one table and a plain-language reading for the owner: for
  which assets the insurance has paid for its premium historically and for which not.
- **No rule change is proposed or tested.** Any change (for example not trend-timing an asset)
  would be a new strategy try needing its own card, its family bar and the project bar.
- `tries.md`: one `note` row per ledger series and one for the book drawdown split (re-scores,
  not tries; not selectable; N for a new pick unchanged).
- Bar for scale only (`research/register/BAR.md`, rows through 2026-11-25 01:16): 4,126
  distinct tries, N for a new pick 1,116 (z >= 4.93), measured rho 0.55 gives N 506 (z >=
  4.70, Bonferroni p <= 9.9e-05); mechanisms 103 / 29 tested / 30 gates, family bar p < 0.10 /
  103 = 0.00097 (`gate-null.md`). Not applicable: no test, no pick.
