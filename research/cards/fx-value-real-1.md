# fx-value-real-1: currency value with the real exchange rate, alone and in the century book (card)

Lane `fx-value-real-1`, written 2026-11-25 21:10 UTC **before any number on the tested data was
computed**: no real exchange rate, no signal, no sleeve or book return, no correlation of the
new signal with the old one. Branch `fx-value-real-1` from `origin/main` (`d84fe39`). Research
only: fake money, files already in the cache (read-only), no change to the gym, the daily
runner or the live strategies. Nothing after 2025-10-31 is parsed. Shorts are research-only
(B7), and the century book holds Ken French portfolios that the gym cannot trade, so **the
verdict is informational**: a pass would not be a pick.

What was seen before this card: `xs-century-1.md`, its card and its results table (#170: book
net z 2.75, gross 7.39; FX-value sleeve, spot-reversal proxy, net Sharpe 0.37, IR +0.30 vs the
comparator, NW z 1.89, 542 months from 1980-09), `vm-style-1`'s rows (#179), `data-long-4.md`
(#174: CPI coverage and timing, `real_fx_series`), the code of `lib/xs_century.py`,
`lib/xs_century_run.py`, `lib/long_macro.py` and `lib/long_macro_build.py`. No CPI value, real
exchange rate or return was looked at.

## What is new, and why the answer is not known from #170

- **New: the published signal.** #170's currency value was a stated deviation: with no CPI in
  the cache it used AMP's commodity form on spot, log(mean spot over months L-65..L-54) -
  log(spot at L). Asness, Moskowitz and Pedersen ("Value and Momentum Everywhere", JF 68(3)
  2013, section I.B) define currency value as the 5-year change in purchasing power parity:
  the negative 5-year return on the spot rate (average spot 4.5-5.5 years ago over spot today)
  minus the log change in foreign relative to US CPI over the same period. data-long-4 now
  gives monthly CPI for all nine currencies, so the real exchange rate q = S x P_f / P_us
  (S = USD per unit) can be built with each CPI as known at the spot's month end.
- **Why not knowable.** The two signals differ by the 5-year inflation differential. Among
  these nine currencies that differential was large and persistent in 1975-1995 (high-
  inflation GBP, NZD, AUD, SEK, NOK against low-inflation JPY, CHF, DEM), which is most of the
  sleeve's first half. A spot reversal there partly measures inflation (a currency that falls
  because its prices rise is not cheaper in real terms), so the proxy ranks those currencies
  as cheaper than PPP does. The rank correlation of the two signals is not known and will be
  reported **only after this card is pushed**, as a diagnostic (not a try).
- **What is knowable, said now.** The full book with the swapped sleeve is nearly determined
  by #170's numbers. After 1980 the FX-value sleeve is 1/9 of the book (three classes, three
  sleeves in currencies), live 45 of the book's 97 years. To lift the book from z 2.75 to 4.70
  at about the same residual risk (4.9% a year), its alpha must rise from +1.51 to about +2.6%
  a year, i.e. by about 1.07 x 97 / 45 x 9 = 21% a year of sleeve alpha: the sleeve's IR (at a
  10% volatility target) would have to rise from +0.30 to about +2.4. No published currency
  value strategy is near that. **So the full-book row is run because the brief asks for it,
  but its fail is foreseen**; the informative test is the sleeve alone.

## The test (one configuration, fixed now; nothing tuned)

Everything is #170's code and settings, unchanged, except the currency-value signal.

- **Assets, returns, timing**: #170's nine currencies against USD (JPY, GBP, CHF, CAD, EUR,
  AUD, NZD, SEK, NOK; carry-inclusive excess returns, USD-funded; EUR before 1999 = DEM
  monthly average), from 1973-03; spot window from 1973-02, as in #170 (the real rate uses the
  same months, so the sleeve starts in the same month as the proxy, about 1980-09).
- **Signal (the swap)**: q_i(m) = exp(`real_fx_series(cur)`(m)), the real exchange rate with
  CPI as known at the end of month m (`lm.real_fx_known`: monthly CPI of month k from the 1st
  of k+2; AUD, NZD quarterly from quarter start + 5 months). Value_i(t) =
  log(mean q_i over months L-65..L-54) - log(q_i(L)), L = t-2 (#170's `xc.reversal_value`,
  unchanged, applied to q instead of S). High = the currency is cheap in real terms
  against its own past = long. This is AMP's averaging window applied to the real rate.
- **Sleeve**: #170's `constructed_sleeve`: AMP rank weights (dollar-neutral, gross 2), at
  least 4 currencies, ex-ante 10% volatility (36 months, at least 24, scale cap 4), **5 bps
  per unit of one-way turnover** of the scaled weights (#170's primary FX cost).
- **Full book**: #170's primary book (HML 0.05%/mo, UMD 0.65%/mo, 0.5%/yr borrow, bonds and FX
  5 bps; equal weight across classes, equal weight across sleeves in a class), with only the
  FX-value sleeve replaced.
- **Comparator and statistic** (as #170): `tsmom12`'s rule on the US market (Ken French,
  monthly, in when the 12-month total return > 0), above bills. OLS B_t = a + b T_t + e_t;
  IR = a / sd(e) x sqrt(12); z = a / SE, SE the larger of Newey-West (Bartlett, lag
  floor(4 (n/100)^(2/9))) and a 12-month circular block bootstrap (2,000 draws, seed
  20261124).

## Bar and power

- **Project bar** (`research/register/BAR.md` on `main`, rows through 2026-11-25 01:16: 4,126
  distinct tries, N for a new pick 1,116, N_eff 506 at measured rho 0.55): **z >= 4.70**
  (DSR 0.95; Bonferroni p <= 9.9e-05). The ONC end of the range, **z >= 3.25**, is reported
  beside it. Not lowered for the alpha form or the comparator (alpha-form-1).
- **Family bar.** This is not a gated idea, so gate-null's family bar (p < 0.10 / 103) does not
  apply. In the style-book family (`xs-century-1`, `vm-style-1`, this lane) this card adds two
  decision rows; a family Bonferroni over the family's decision rows (at most 4) would ask
  z >= 2.50, below the project bar, which decides.
- **Power (said now).** The sleeve has about 45 years (about 540 months). z 4.70 then needs a
  net IR of about **0.70 (50% power) to 0.82 (80% power)**, the ONC end 3.25 about 0.48. The
  proxy sleeve had +0.30. Published gross Sharpe ratios of G10 currency value are of the order
  of 0.3-0.5 (AMP 2013; Menkhoff, Sarno, Schmeling and Schrimpf, "Currency Value", RFS 2017;
  from memory, not re-read tonight). Against that the test has a few percent power: it can
  find a large surprise, and it will measure the real-rate sleeve with an SE of about 0.15 in
  IR, which says whether a future book should use the published definition.

## Verdict and kill rules (fixed now)

1. **Sleeve (primary 1)**: pass (informational) if z >= 4.70 and a > 0 in both halves of its
   sample (split at the middle month); near if 3.25 <= z < 4.70; fail if z < 3.25.
2. **Book (primary 2)**: #170's rule: pass if z >= 4.70 and a > 0 in 1928-1972 and 1973-2025;
   near if 3.25 <= z < 4.70; fail below. (Foreseen: fail.)
3. **Kill.** If the sleeve fails (z < 3.25): currency value on this nine-currency G10 panel is
   closed as a candidate at the project bar; no lookback, averaging-window, cost or currency-
   set variants will be run on it (they would be data-mining a closed question). It may be
   used again only as a fixed component of a new book on a new card, or tested on independent
   currencies (outside these nine) on its own card. If the book fails, the century book is
   closed on this data: no further sleeve swaps of #170's book (each would be another try at a
   failed book). If near: no pick and no retune; only independent currencies on a new card.
4. Robustness rows describe; none can turn a fail into a pass or a pass into a fail.

## Robustness rows (run after the primaries, each logged; none decides)

- S1 sleeve gross (no costs).
- S2 sleeve, FX costs x2 (10 bps).
- S3 sleeve, point-to-point form: -(ln q(L) - ln q(L-60)), no averaging (the plain "5-year
  change in the real rate").
- S4 sleeve 1994-01..2025-10 (post-publication of the factor literature; #170's R5 split).
- S5 sleeve against the store's six-asset `tsmom12` (#170's R6 comparator), 1994-03..2025-10.
- B1 book gross. B2 book with UMD at 0.34%/mo (#170's R2). B3 bonds + FX only (#170's R7),
  with the swap.
- C1 **control**: the proxy sleeve alone, same scoring (#170 reported it only as a sleeve
  table line, never as a try row). Also run, not logged as a new row because it is a re-run:
  #170's primary book with the proxy, which must reproduce z 2.75 (a check that the code path
  is unchanged).

Diagnostics (statistics, not tries): pooled cross-sectional rank correlation of the real-rate
and proxy signals over the sleeve's months, by decade; correlation of the two sleeves'
monthly returns.

## Honest prior

It will probably fail. #170 failed on the cost of stock momentum, not on currency value: the
FX-value sleeve was already one of its better net sleeves (IR +0.30). Switching to the real
rate could raise or lower that; the expected change is small, a pass of the sleeve needs an IR
more than twice the proxy's and above the published range, and the book cannot pass
(arithmetic above). My guess: sleeve IR +0.2 to +0.5, z 1.5-3.5; chance of a sleeve pass about
3%, of "near" about 15%. The value of the run is the measurement (and closing the question),
not the expected pass.

## Outputs

- `research/lib/fx_value_real_run.py` (reads the cache; imports #170's `xs_century` and
  `xs_century_run`; the only change to #170's code is a keyword argument of `build` that lets a
  caller pass the FX-value signal, default = #170's proxy, behaviour unchanged) writes
  `research/results/fx-value-real-1.md` (statistics only; no CPI, rate or return series
  committed: BIS and OECD terms).
- Rows in `research/tries.md`, idea `fx-value-real-1`: sleeve and book as `variant`, S1-S5 and
  B1-B3 as `robustness`, C1 as `control`; Sharpe = monthly excess x sqrt(12), stated in each
  Variant cell. No `ledger/tries.jsonl` line (the gym cannot hold shorts).
- `research/fx-value-real-1.md`: the answer on one screen.
