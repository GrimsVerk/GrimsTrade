# Survey 7: `seasonal-20y` as an event-study gate (same-calendar-month seasonality)

Research run survey-7, 2026-11-19. Branch `survey-7` (from `wide-9`), draft PR into `wide-9`.
Research only: fake money, cached public prices, no change to the gym, the daily runner or the
live strategies.

**Why this, why a gate.** survey-4 (PR #72, `research/survey-4.md` on its branch) left
candidate C `seasonal-20y` as the next published effect, with the advice to run it as an event
study first and card it only if the same-month spread after 2016 is positive with t >= 2. This
run does that, under wide-9's gate procedure (`research/gate-null.md`): placebo family fixed in
the rule, 40 placebos, the same code path for true and placebo, the rank decides; rule, script
and tests pushed before any number; one dry run with counts only, then one real run. A gate is
descriptive: no `tries.md` row, no card, and it does not count as a tested mechanism.

## Count used

This base (`wide-9`) carries **72 mechanisms, 16 tested by a strategy, none passed**. survey-4's
count is **not** on this base: survey-4 branched from `ann-1` and added four mechanisms new to
both lines (A `ts-carry`, B `halloween`, C `seasonal-20y`, D `ts-value`) and tested two (A, B).
None of the four is in the wide line's 72 (`halloween` sat only as "parked" in `ideas.md`, which
survey-4 counted as new). The union is therefore **76 mechanisms, 18 tested, none passed**, and
this run reads any later strategy test against the union: **p < 0.10 / 76 = 0.00132** (family).
Project-wide (`git show origin/register-1:research/register/BAR.md`, read 2026-11-19): **2,904
tries, N 1,012 for a new pick, Bonferroni p <= 4.9e-5.** The mechanism list on this base is not
edited (survey-4's list lives on its own branch); the union is stated here for the next lane to
carry.

## Sources (citations checked on the web, 2026-11-19)

- **Heston and Sadka, "Seasonality in the Cross-Section of Stock Returns", Journal of Financial
  Economics 87(2), 2008, pp. 418-445, DOI 10.1016/j.jfineco.2007.02.003.** `[abstract]`
  (RePEc `eee:jfinec:v:87:y:2008:i:2:p:418-445`) NYSE/AMEX 1963-2002: a stock's return in a
  calendar month predicts its return in the same month for up to 20 annual lags; non-annual
  lags do not share it. Confirmed.
- **Keloharju, Linnainmaa and Nyberg, "Return Seasonalities", Journal of Finance 71(4), 2016,
  pp. 1557-1590, DOI 10.1111/jofi.12398.** `[abstract]` (RePEc
  `bla:jfinan:v:71:y:2016:i:4:p:1557-1590`) Same-calendar-month strategy about 13% a year in
  stocks; similar seasonalities in anomalies, commodities, country indexes. Confirmed.
- Correction to survey-4: the same authors' "seasonal reversals" follow-up, which survey-4 cited
  as a 2018 paper, is published as "Are Return Seasonalities Due to Risk or Mispricing?",
  Journal of Financial Economics 139(1), 2021, pp. 138-161 (RePEc
  `eee:jfinec:v:139:y:2021:i:1:p:138-161`). `[search summary]`
- Baltussen, Swinkels and van Vliet (2021), R5 in survey-4: the multi-asset seasonality signal
  is the asset's return in the same calendar month over the prior 20 years; it fails their
  1981-2011 replication sample in equities and bonds and goes to about zero when lagged a month.

The papers' samples end 2011 (KLN) and 2016 (R5's new sample). **Post-sample = holding months
2017-01 .. 2025-10.** No run on any branch has cut our prices by same-month history (survey-4
listed C but computed nothing for it).

## Gate rule (fixed and pushed before any number)

**Universe.** Every asset in the research cache with daily bars that is one of the six live
assets or an ETF: SPY, QQQ, TLT, GLD, BTC, ETH, and the cached ETFs DBC, EEM, EFA, IEF, IWM, LQD,
SLV, VNQ, XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY (23 assets). Dividend-adjusted closes where
the cache has them (`harness.load_history("train")`, so nothing after 2025-11-10). Indexes
(GSPC, FTSE, GDAXI, N225, IRX) and the other coins are out: not ETFs, not the book's assets.

**Calendar-month returns (the signal's input).** r(s, Y, m) = log(close of the last bar of month
m / close of the last bar of month m - 1), both bars in their own months; missing otherwise.

**Signal.** For holding month M (year Y), with placebo shift s (s = 0 is the true signal) and
start offset a (a = 0 for the true signal):
S(s, a) = the mean of r over the months that lie 12j + s months before M, for j = 1 + a ..
20 + a, using as many of those 20 months as exist (stated in the output: mean, minimum and
maximum years used); an asset needs **at least 5** of them, else it has no signal that month.
For s = 0, a = 0 this is the asset's average return in the same calendar month over the past
20 years (or as many as available, at least 5). Every input month ended at least 11 months
before the holding month starts: no look-ahead.

**Decisions on the book's weekly clock.** The book decides on Fridays (`common.weekly`). F(M) =
the last Friday on or before the last calendar day of month M. Holding return R(s, M) =
log(close on or before F(M)) - log(close on or before F(M - 1)), each close no more than 5
calendar days before its Friday (else missing). So month M's position is chosen at the last
Friday of M - 1 and held to the last Friday of M (close to close: an event study, not a fill
model; a card would fill at the next open).

**Spread.** In month M, the assets with both a signal and a holding return are ranked by S;
k = max(1, round(n / 5)); y(M) = mean R of the top k minus mean R of the bottom k (ties broken
by symbol name). A month counts only if n >= 6.

**Statistic.** Over a sample of months, mean y and the plain t (mean / (sd / sqrt(n months)));
holding months do not overlap.

**Placebo null (the decider), one family, fixed here.** The same function with the month index
shifted off the annual cycle: s = 1 .. 10 crossed with a = 0, 1, 2, 3 (**40 placebos**). s = 0
is the true signal; s = 11 is left out (lags 12(j + 1) - 1 sit one month before the next annual
lag, the shift closest to the true calendar) and no s is negative (lags 1-11 would add the
short-term reversal, a different effect). Every placebo lag is 13 months or more. Same inclusion
rules (5 years, n >= 6). Note before any number: Heston-Sadka and KLN 2021 report that
non-annual lags tend to predict *low* returns, so the placebo null may sit below zero; the
rank then asks exactly the papers' question (do annual lags beat non-annual ones?), and the
t >= 2 condition guards the absolute level.

**Gate. Pass only if both hold** (gate sample: holding months 2017-01 .. 2025-10, all of them
inside train):
1. Mean y > 0 with t >= 2 (survey-4's condition).
2. The true t ranks among the 2 highest of 41 (true plus 40 placebos); empirical one-sided p =
   rank / 41 <= 0.049.

**Shown, not gating** (each with mean, t and months): the calendar-month version (r(s, Y, M)
as the holding return instead of the Friday one) 2017-2025; both versions on the earlier years
(every month from the first with n >= 6 through 2016-12); the six live assets only and the 17
ETFs only (2017-2025, Friday version); the placebo t's standard deviation, the share with
|t| >= 2, the 5/50/95% quantiles and the extremes (gate-null step 5); the median number of
assets and years used.

**On a pass:** no card and no trading test now (lane order). This file gets a *proposed* card
for the next window only: a cross-sectional overlay is not long-only, so the proposal would map
it to the book (e.g. long-only top-k on the Friday clock against equal weight), read at the
family bar p < 0.00132 and the register's p <= 4.9e-5, with z = (t - placebo median) / placebo
sd (gate-null step 7). **On a fail:** `seasonal-20y` dead by the gate, no card, no row.

**Power, written before any number.** With about 21-23 assets, k = 4-5 a leg, and the coins in
the cross-section (a coin month moves 20-30%), the monthly spread's standard deviation is likely
4-7%; over 106 months the standard error is 0.4-0.7% a month, so t >= 2 needs about 0.8-1.4% a
month (10-17% a year). R5's equity seasonality in 1981-2011 had Sharpe 0.36, which over nine
years is t of about 1.1. Only a large effect can pass.

**My guess before any number.** Mean y between -0.5% and +0.5% a month, |t| < 1.5, rank
somewhere in the upper half (the placebos may lean negative); placebo t sd 0.9-1.3 (independent
monthly spreads). Chance of a pass: 3%.
