# ts-carry: hold a stock or bond trend slot only while its carry is positive

Sources: Koijen, Moskowitz, Pedersen and Vrugt, "Carry", Journal of Financial Economics 127(2),
2018, pp. 197-225 (R6 in `survey-4.md`); Baltussen, Swinkels and van Vliet, "Global Factor
Premiums", JFE 142(3), 2021, pp. 1128-1154 (R5). Pick A of `survey-4.md` (score 5 of 5).
Written 2026-11-18, lane survey-4, before any test or number of this card.

## Claim (as this book can use it)

Carry is what an asset earns if its price does not move: for a stock index its dividend yield
minus the cash rate, for a 10-year bond about its yield minus the cash rate (plus roll-down).
R6 finds that the sign of an asset's own carry times its returns (Table 6: global equities
Sharpe 0.41 with cut-off 0, 0.75 with cut-off at the running mean; 10-year bonds 0.65 / 0.69),
in a sample ending September 2012. R5 finds carry in equities and bonds in 1800-1980 data too,
one of only five premiums that pass both its strict and its pre-sample tests. If carry still
times returns, a trend slot held only while carry is positive should lose less than it gives up.

## Why it might work

- The strongest out-of-sample record of any family this lineage has tried apart from trend
  itself: two centuries before the original sample (R5), and a mechanism (a risk premium paid
  for holding the asset) that publication need not arbitrage away.
- Different information from price trend (R6: carry is not explained by momentum or TSMOM).

## Why it might not

- R6 and R5 are long-short, volatility-scaled and diversified across 10-24 markets; we hold one
  US bond and two US stock funds, and only long or flat. R6 itself warns that with cut-off 0 the
  timing strategy is mostly a passive position where carry rarely changes sign.
- Known before any test (common knowledge, not computed here): US equity carry (dividend yield
  1-2% minus bills) was negative most of 1994-2001, 2005-2008 and from 2022 on: the gate takes
  stocks out of the late-1990s and 2023-2025 rallies. The gym pays 0 on cash, so leaving stocks
  for bills that paid 5% looks worse here than it was (shown with interest on cash too).
- Every "leave early on a macro reading" gate here has failed (`yield-curve`, `real-rate`,
  `credit-spread`, `fed-hiking`, `xtsmom`). The bond leg reads the curve slope, which
  `yield-curve` read for stocks; macro-1's skill table showed a faint slope-TLT link (rho +0.11,
  t 2.0): seen before this card.

## Data

- Prices: the six assets, the 8 other ETFs, the S&P 500 index, train only, as every run.
- Dividends: for each ETF, from Yahoo's dividend-adjusted and raw closes (`research/data/adj`
  and `bars`): with f = adjusted close / raw close, a session t where f(t-1) / f(t) differs from
  1 by more than 1e-5 is an ex-date with dividend D = raw close(t-1) x (1 - f(t-1) / f(t)).
  Trailing yield at session d = the sum of D over ex-dates in (d - 365 days, d] / raw close(d);
  missing until the fund has 365 days of bars. Known at the close of d (ex-dates are announced
  before they happen).
- Cash rate: the 13-week T-bill yield, Yahoo `^IRX` (cached as `IRX`, from 1960), a close on
  day x used from x + 1 (protocol, "Macro tests").
- 10-year yield: FRED `DGS10` (cached snapshot, from 1962), used from x + 1.
- S&P 500 index (out-of-universe only): Shiller's monthly S&P dividends (`ie_data.xls`, cached
  2026-11-12; annual dividend rate), the value for month m used from the first day of month m + 4
  (Shiller's dividends come from quarterly reports; three months' lag is my conservative
  default). Yield = D / index close at the decision.

## Carry (no fitted parameter)

- Equity funds (SPY, QQQ; IWM, EFA, EEM, VNQ; the S&P 500 index): trailing dividend yield minus
  the bill yield. EFA and EEM use the US bill (R6 uses each country's rate; accepted).
- Bond funds (TLT; IEF, LQD): DGS10 minus the bill yield (R6's slope term; the roll-down needs a
  9-year yield we do not have, and is positive whenever the curve slopes up, so it rarely
  changes the sign). LQD's credit spread is ignored (accepted).
- GLD, DBC, SLV, coins: no carry is measurable from spot data (commodity carry needs the futures
  curve; coin carry is perp funding, `carry-2`): untouched, plain `tsmom12`.
- Carry is read as of the asset's last session d before the decision (inputs with x + 1 <= d).
  If any input is missing, no gate (the slot is the twin's).

## Rule

`tsmom12` on the six assets, weekly (Friday close, next-open fills, equal slots of the eligible
assets). A carry-bearing slot keeps its `tsmom12` weight only while its carry is above the
cut-off; else that weight is cash.

## Variants (all that will be run)

1. `carry` (primary): cut-off 0 (R6's first timing rule).
2. `carry-mean`: cut-off = the running mean of the asset's own daily carry from its first value
   up to d (R6's second rule uses the asset-class mean; with one or two funds per class, the
   asset's own mean is the nearest).
3. Robustness, never selectable: `carry-bond` (only the TLT leg gated) and `carry-equity` (only
   SPY and QQQ gated), to show where the result comes from.

## Twin and baselines

Twin `tsmom12`; equal weight shown. Also shown (no extra row): the share of `tsmom12`'s stock
and bond weeks the gate removes; each variant rescored with T-bill interest on cash
(`cash_interest.rescored`); and a descriptive table: SPY and TLT mean daily open-to-open return
on days their own 12-month trend is up, split by carry above / not above 0, with Welch t, for
1994-2012-09 (inside R6's sample) and 2012-10-01 to the end of train (after it); the same for the
S&P 500 index (close to close) for 1962-1987 (before R6's sample) and 1988-1993.

## Out of universe

- The 8 other ETFs as a `tsmom12` book with the gate on IWM, EFA, EEM, VNQ, IEF, LQD.
- The S&P 500 index alone, 1962-1993 (the protocol's `GSPC` context), with Shiller dividends.
  N225, FTSE, DAX: no dividend data, not applicable. Coins: not applicable.

## Pass bar

The default in `protocol.md` for each variant against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 65 = 0.00154** (the lineage's family: 61 + survey-4's 4; this is the
   15th tested). Both variants are one mechanism's tries.
2. Ahead of the twin in at least 4 of the 5 eras.
3. Max drawdown not more than 5 points worse than the twin's.
4. Sharpe difference positive on both applicable out-of-universe sets (ETFs, S&P 500 index).
5. Beats equal weight on Sharpe.
6. (card, after the sample) Not behind `tsmom12` on Sharpe over 2012-10-01 to the end of train.
7. (card, after the sample) In the descriptive table, 2012-10-01 to the end of train: the
   carry-positive minus carry-negative spread is positive for both SPY and TLT, with Welch
   t >= 2 for at least one (for `carry-mean`, the split at the running mean).

Held-out year: once, for a variant that passes all seven (primary first), only then.

## My guess before any number

Chance any variant passes: 2%. `carry` against the twin: -0.05 to -0.15 Sharpe (stocks out of
1995-1999 and 2023-2025); `carry-bond` about even or slightly ahead (TLT out in 2022, also out
in 2006-07 and 2019 when TLT rose); `carry-mean` closer to the twin than `carry`. With interest
on cash the gap narrows by 0.05-0.1 but does not close.
