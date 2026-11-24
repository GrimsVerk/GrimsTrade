# seasonal-20y: hold a slot only in calendar months that were good in the past 20 years

Lane `seasonal-1`, 2026-11-24. Written and pushed **before any number of this test was
computed**. Research only: fake money, cached keyless public prices, train data only (no bar
after 2025-11-10 is loaded or parsed).

## Sources

- Heston and Sadka, "Seasonality in the Cross-Section of Stock Returns", JFE 87(2), 2008,
  pp. 418-445: a stock's return in a calendar month predicts its return in the same month for up
  to 20 annual lags (NYSE/AMEX 1963-2002).
- Keloharju, Linnainmaa and Nyberg, "Return Seasonalities", JF 71(4), 2016, pp. 1557-1590: the
  same-calendar-month strategy works in stocks, anomalies, commodities and country indexes.
- Baltussen, Swinkels and van Vliet, JFE 2021 (R5 in `survey-4.md`): the asset-class seasonality
  signal (same calendar month over the prior 20 years) is strong in their 1800s-1980 sample and in
  2012-2016, but fails their 1981-2011 replication (equities Sharpe 0.36, t 2.0; bonds -0.09) and
  goes to about zero with a one-month lag.

All documented forms are **cross-sectional** (rank assets against each other). The time-series
form below (each asset against its own average month) is this project's construction
(`survey-4.md`, candidate C).

## What had been seen when this was written

- `survey-4.md` (the papers' numbers above) and `survey-7.md`: the cross-sectional same-month
  spread on 23 ETFs and coins was absent in 2017-2025 (+0.12% a month, t 0.19, rank 31 of 41
  placebos) and in 2004-2016 (-0.10%, t -0.31). That was a different design (cross-section,
  ETF histories of at most 20 years) on overlapping assets; this card is the time-series form on
  long histories, which no branch has run (`tries.md` has no `seasonal` row).
- `tsmom12` on the primary test: Sharpe 1.05 (`tries.md`, baselines). The long US and
  13-market data sets were used by `trend-1926`, `insure-1` and `insure-2` for trend and crash
  questions; no calendar-month statistic was computed on them by any lane I know of.
- Other calendar rules already tested and not re-tested here: `month-end-bonds`,
  `month-end-liquidity`, `halloween`, `opex-pin`, `fomc-cycle`, `tax-drain`, `coupon-dose`.
- General knowledge an agent cannot unlearn: US stocks have had a weak September and a strong
  January on average in the 20th century.

## Prior (stated before the run)

Low. R5's own time-series-free replication sample fails, `survey-7` found nothing in our ETFs,
and an asset's same-month mean over 20 years has a standard error of about sd / sqrt(20), i.e.
about 1% a month for stocks, the same size as any plausible seasonal: most of the signal is
noise. My guess: the US long book's standalone Sharpe difference against holding between -0.10
and +0.10 over 1946-2025, z below 1.5; possibly positive before 1981 and not after. Chance the
overlay clears the project bar on the primary test: under 1%.

## Rule (frozen; no fitted parameter)

Per asset, from **month-end closes** (the last close of each calendar month in that asset's own
series): r(Y, m) = log(close at end of month m / close at end of the previous calendar month).

For a **holding month M** (year Y, month m):
- S = mean of r(Y - j, m) for j = 1 .. 20 (the same calendar month in the 20 years before).
- A = mean of r over the 240 months M - 1 .. M - 240 (every month of the same 20 years).
- Missing data: S needs at least 19 of its 20 values and A at least 228 of its 240, else the
  asset has **no signal** for M.
- **Season on** for M if S >= A, else off.

Every input ends at the month-end close before M starts: the month's own return (and anything
later) never enters its signal. A unit test checks this by changing every bar from the first day
of M on and asserting the signal for M is unchanged.

**Clock and fills.** The gym decides every day at 22:30 UTC on closed bars and fills at the next
open (unchanged). The holding month of a decision is the calendar month of the next weekday
after the latest visible close. So the decision on the last session of M - 1 switches to M's
season and fills at the first open of M. When the last weekday of a month is a holiday the switch
comes one session late (rare; stated in the record).

**The four strategies of each test** (equal slots, cash at 0, the protocol's convention):
1. `tsmom12`: the live rule, Friday decisions (`common.weekly(slots(tsmom_signal))`).
2. **Overlay** `seasonal-20y-overlay`: `tsmom12`'s weights, but a slot whose season is off for
   the current holding month sits in cash (no reweighting).
3. **Standalone** `seasonal-20y-alone`: each slot held only while its season is on.
4. **Hold**: equal weight, Friday rebalancing (`common.weekly(equal_weight)`).

**Slots.** In the long data sets an asset gets a slot (in all four strategies alike) only from
the first holding month it has a signal; before that it is not in the test. In the primary
six-asset test the slots are the protocol's (an asset is eligible after a year of bars), and an
asset with no signal keeps its season on, so its slot is exactly `tsmom12`'s (or held, in the
standalone).

## Data (all cached, nothing new downloaded)

1. **US long (primary for the effect).** Ken French daily value-weighted market (Mkt-RF + RF)
   and 10 industries (snapshot `french/2026-11-12`), total return, 1926-07-01 .. 2025-11-10.
   Signal from each series' own month-ends, so the first holding month is about 1946-07. Tests:
   the **ten-industry book** (decides) and the market alone; each industry alone (shown).
   Bars as `trend_1926.bars` (open = previous close, 2 bps a side, as `trend-1926`/`insure-2`).
2. **13 developed markets.** `insure-2`'s Yahoo price indices (N225, GSPTSE, FTSE, AORD, HSI,
   GDAXI, STI, FCHI, SSMI, BFX, AEX, ATX, IBEX; snapshot `insure-2/raw-2026-11-18`), local
   currency, closes up to 2025-11-10; bars as above, 2 bps a side. Signal from each index's own
   month-ends, so most enter only after 2005. Tests: the **13-market book** and each market alone
   (shown).
3. **Primary six-asset test**, decisions 1994-02-01 .. 2025-11-09, the harness's adjusted bars
   and default costs. The six assets' own histories are too short for a 20-year signal, so the
   season comes from a long proxy, read as data and cut at 2025-11-10:
   SPY from `^GSPC` (1950-), QQQ from `^IXIC` (1971-), TLT from `^TNX` turned into a bond return
   r = y(m-1) / 1200 - 17 * (y(m) - y(m-1)) / 100, y the month-end yield in percent (carry
   plus duration 17, about TLT's; 1962-). GLD, BTC
   and ETH have no 20-year month-end proxy in the cache (the datahub gold file is monthly
   averages, which shifts the calendar month by half), so their season stays on.

## Statistics

Weekly returns (Friday to Friday, from the gym's calendar equity). Sharpe annualised on the
repo's convention. **Paired Sharpe difference** rule minus comparator on the same weeks, with
SE = standard deviation of 2,000 paired stationary-bootstrap draws (mean block 8 weeks, seed 0);
z = difference / SE. Comparisons: overlay - `tsmom12`, standalone - hold.

**Splits (pre-stated robustness):** by holding date, before 1981-01-01 / from 1981-01-01 (R5's
replication break), and before 2008-01-01 / from 2008-01-01 (Heston and Sadka's publication).
The 13 markets and the primary test have no pre-1981 weeks; reported as such.

**Shown, not deciding:** each series alone; a late-fill run of the US book (bars with open =
the day's own close, fill one session later); a placebo set on the US book in monthly arithmetic
(not the gym): the same rule with the "same month" replaced by months 12j + s before M,
s = 1 .. 10, j = 1 .. 20 (10 placebos), standalone Sharpe difference against holding, so the
true annual lag can be read against off-cycle lags that share every asset's long-run mean.

## Pass bars

- **A pick (changes the book):** the overlay beats `tsmom12` on the primary test with
  z >= 4.69 (`research/register/BAR.md`, 3,130 tries, N = 486 effective, Bonferroni
  p <= 1.0e-04; z >= 3.29 would be "the counting method decides"). Expected: no.
- **The effect, read on the US ten-industry book, standalone - hold** (the idea in its plainest
  form, and the data with the most independent years):
  - *present*: z >= 1.645 over 1946-2025, and the difference > 0 in 1946-1980, 1981-2025 and
    2008-2025;
  - *early only*: z >= 1.645 in 1946-1980, and in 1981-2025 the difference <= 0 or z < 1;
  - *absent*: whole-period z < 1.645 and not *early only*;
  - *mixed*: anything else.
  The same labels are printed for the 13-market book (whole period and the 2008 split) and the
  overlay comparisons, for reading, not deciding.
- Every configuration is logged to `tries.md` once, rows of kind `variant` (primary overlay and
  standalone), `baseline` (primary `tsmom12` and hold on this script's run) and `robustness`
  (everything on the long data sets). One real run; nothing is tuned or rerun.

## What each outcome means

- *absent* or *early only*: `seasonal-20y` is dead for this book (status `dead (tested)` in
  `ideas.md`); "early only" matches R5's "strong pre-1981, absent in replication".
- *present* without the pick bar: a documented effect too small for the bar; no change to the
  book; the held-out year is not spent on it.
- A pick: cannot happen without z >= 4.69; it would go to the owner with the held-out year
  unspent.
