# xtsmom: hold the stock trend slots only while government bonds also trend up

Source: Pitkäjärvi, Suominen and Vaittinen, "Cross-asset signals and time series momentum",
Journal of Financial Economics 136(1), 2020, pp. 63-85, DOI 10.1016/j.jfineco.2019.02.011
(`survey-2.md`, S5; rank 2 of survey-2's note, prior 3%). Written 2026-11-18, lane survey-3,
before any test or number of this card.

## Citation check (2026-11-18, before the card)

- Journal, volume, issue, pages, DOI and authors: confirmed on the VU Amsterdam research portal
  (`research.vu.nl`, the publication record) and a search summary of the JFE page `[abstract]`.
- Abstract, as paraphrased by the portal: a "cross-asset time series momentum" in 20 countries;
  past bond returns predict future equity returns positively, past equity returns predict future
  bond returns negatively; a diversified cross-asset portfolio has a Sharpe ratio about 45%
  higher than a standard time-series momentum portfolio; explained by slow-moving capital.
- Sample and rules, from CXO Advisory's summary of the December 2016 working paper
  `[secondary]`: January 1980 to December 2015, 20 developed countries, monthly total-return
  indexes of each country's stocks and of its government bonds (constant 5-year maturity),
  excess returns over US one-month bills. Stocks: long when the past stock **and** bond returns
  are both positive, short when both negative, flat when they disagree. Bonds: long when the
  bond return is positive and the stock return negative, short in the reverse case, flat
  otherwise. Main setting: 12-month look-back, 1-month hold; 1, 3, 6, 9, 12, 24, 36, 48 months
  also tested. Positions averaged across countries, scaled to 10% volatility. Beats plain
  TSMOM on gross Sharpe in 18 of 20 countries; the gain is "modest" in the US, UK and Canada,
  none in Japan. Gross of costs, indexes, a bond bull market, lag choice and tests on the same
  data.
- Not confirmed: one search summary says the published sample ends December 2016, not 2015.
  So 2016 is treated as possibly in sample; "after the sample" below means 2017-01-01 on.
- Not found: an absolute Sharpe, a long-only result, or a stock-leg-only result (SSRN and the
  Alpha Architect write-up refuse automated reading). The headline 45% is for the long-short,
  two-leg, volatility-scaled portfolio across 20 countries, not for anything this book can hold.

## Claim (as this book can use it)

The trend book already holds SPY and QQQ only while their own 12-month return is positive.
The paper says the bond market's 12-month return adds information: stocks rising while bonds
fall earn less (and, the paper's reading, slow-moving capital means bond moves reach stocks
with a lag). If so, dropping the stock slots in those spells cuts risk more than return.

## Why it might work

- A published, refereed effect in 20 countries with a large stated gain; no new data needed.
- A bond sell-off tightens financing for everyone; 1994, 1999-2000 and 2022 were bond
  sell-offs that preceded or came with stock trouble.

## Why it might not

- The gain was modest in the US, which is where this book's stocks are.
- The sample (1980-2015) is one long bond bull market: the gate was rarely on, and when it
  was, a falling yield was the usual story. After 2016 bonds fell for years (2021-2024) while
  US stocks rose strongly in 2023-2024: visible before any test, it is the obvious way to lose.
- `tsmom12` already leaves stocks when their own trend breaks; the paper's flat-when-they-
  disagree state is half of what a long-only book does anyway.
- Every macro "leave early" gate here failed (`credit-spread`, `yield-curve`, `real-rate`,
  `fed-hiking`, `hedge-regime`).

## Data

- Prices: the six assets, the 8 other ETFs, the four indexes, as every run (train only).
- Bond signal: the 10-year Treasury constant-maturity yield, FRED `DGS10` (from 1962), the
  cached snapshot (`<cache_root>/fred/api/latest/DGS10/`), cut at 2025-11-10. Turned into the
  return of a 10-year par bond exactly as wide-1 step 4 did (`wide1_yields.bond`): each day,
  -duration x change in yield + yield x days / 365; days across a gap of more than 10 days
  count as 0. The bond's 12-month return is the sum of those returns over the last 365
  calendar days. The paper used 5-year constant-maturity government bond indexes per country;
  the US 10-year is the nearest series covering 1962-2025 (accepted; TLT itself is a
  robustness row).
- As of (protocol, "Macro tests"): a yield observed on day x is used from x + 1. A decision
  after the close of session `d` of a stock asset reads the bond signal with observations up to
  `d - 1`.

## Rule (fixed, no fitted parameter)

- Base: `tsmom12` on the six assets, decided weekly as always (Friday close, next-open fills,
  equal slots of the eligible assets).
- Gate: a stock slot (SPY, QQQ; in the other sets the stock ETFs and indexes) keeps its
  `tsmom12` weight only if the 10-year bond's trailing return, as of its last session `d`, is
  positive; else that weight is cash. If the bond signal is missing (never, after 1963), no
  gate. TLT, GLD, coins: untouched.

## Variants (all that will be run)

1. `xtsmom` (primary): the gate above, bond look-back 365 days (the paper's main setting).
2. `xtsmom-b6`: the same with a 182-day bond look-back (6 months, the middle of the paper's
   grid). The stock look-back stays 12 months (the book's own).
3. `xtsmom-full`: the primary gate plus the paper's bond leg, long-only: the bond slots (TLT
   in the six; IEF and LQD in the ETF set) keep their `tsmom12` weight only while the set's US
   stock market (SPY in the six; IWM in the ETF set) has a negative 365-day return. Not run on
   the indexes (no bond there).
4. Robustness, never selectable: `xtsmom-tlt`, the primary gate with TLT's own 365-day return
   as the bond signal (six only; before TLT has a year of bars there is no gate).

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight; the fraction of time the gate holds a stock slot
out that `tsmom12` would hold; and a descriptive table (no `tries.md` row): SPY's mean daily
open-to-open return (the interval a decision after session `d` holds) on days its own 12-month
trend is up, split by the bond signal (up / down), with the Welch t of the difference, for
1994-2015 (in the paper's sample), 2016 (possibly in sample), and 2017-01-01 to the end of
train (after the sample); the same for the S&P 500 index (close-to-close, as the index opens
are unreliable) for 1962-1979 (before the paper's sample) and 1980-1993.

## Out of universe

- The 8 other ETFs as a `tsmom12` book, the gate on IWM, EFA, EEM (US bond signal for EFA and
  EEM: the paper used each country's own bonds; accepted, it can only weaken the gate there).
- The four indexes as one `tsmom12` portfolio (`idx`) from 1962, the gate on all four, US
  bond signal for all (same caveat). 1962-1979 is before the paper's sample.
- Coins: not applicable.

## Pass bar

The default in `protocol.md` for each variant against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 61 = 0.00164**. The family is the `wide-*` lineage's list: 54 +
   survey-2's 7 candidates = 61, of which `xtsmom` is one; this card adds no mechanism, so the
   family stays 61 and this is the 14th of them tested. The three variants are one
   mechanism's tries: any of them passing counts against the same bar.
2. Ahead of the twin in at least 4 of the 5 eras.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive on both applicable out-of-universe sets (ETFs, indexes; `xtsmom-full`: ETFs, and
   indexes as for the primary, since its bond leg does not apply there).
5. Beats equal weight on Sharpe.
6. (card, after the sample) Not behind `tsmom12` on Sharpe over 2017-01-01 to the end of train.
7. (card, after the sample) For the primary: on SPY's up-trend days in 2017-01-01 to the end of
   train, the mean open-to-open return with the bond signal up minus with it down is positive
   with Welch t >= 2. (For `xtsmom-b6`, the same split with its 6-month signal.)

Held-out year: once, for the variant that passes all bars (if several, the primary first, then
`xtsmom-b6`), only if all bars pass.

## My guess before any number

Chance any variant passes: 3%. Primary against the twin: -0.05 to +0.03 Sharpe on full train
(the gate exits stocks in 1994, 1999-2000, parts of 2005-06, 2013-14, 2018, 2021-24; it helps
in 2000-01, costs in 1995, 2023-24). Since 2017: -0.02 to -0.10. SPY up-trend days after 2016:
bond-down days earn about as much as bond-up days or more (2023-24). `xtsmom-full` worse than
the primary (it drops TLT through most bond rallies while stocks also rose).

## Result

Tested 2026-11-18: **fails train, all three variants** (primary: bars 1, 2, 6, 7). `xtsmom`
1.05 against 1.05 (+0.002, p 0.49), ahead in 1 of 5 eras; since 2017 -0.06. SPY up-trend days,
bond-up minus bond-down: -0.2 bps a day in 1994-2015, +0.4 (t 0.1) after 2016; the effect
shows only on the S&P 500 index in 1980-1993 (+21.5, t 2.2). Table `results/xtsmom.md`;
verdict `survey-3.md`. Held-out year unspent.
