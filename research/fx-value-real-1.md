# fx-value-real-1: currency value with the real exchange rate, alone and in the century book

Lane `fx-value-real-1`, 2026-11-25 (night, UTC). Branch `fx-value-real-1` from `main`
(`d84fe39`). Research only: fake money, cached keyless data (read-only), no change to the gym,
the daily runner or the live strategies. Nothing after 2025-10-31 parsed. Card (pushed before
any number, `bdc7e8e`, 21:03 UTC; not amended; its header says "21:10", a typo for the commit
time): [`cards/fx-value-real-1.md`](cards/fx-value-real-1.md). Code and tests pushed before the
run (`e34f288`): `lib/fx_value_real_run.py` (one run, a few seconds), tests
`tests/test_fx_value_real.py`. The only change to #170's code is a keyword argument of
`xs_century_run.build` (`fx_value`, default = #170's proxy). Tables:
[`results/fx-value-real-1.md`](results/fx-value-real-1.md). Shorts are research-only (B7) and
the book holds Ken French portfolios, so the verdict is informational.

## The answer on one screen

**Fail, both primaries, by the card's rules.** The published currency-value signal (5-year
change in the real exchange rate, Asness-Moskowitz-Pedersen 2013) is no better than #170's
spot-reversal proxy: sleeve IR +0.28, z 1.71 (proxy +0.30, z 1.89; bar 4.70, ONC end 3.25).
Swapped into #170's book it leaves the book where it was: z 2.74 (#170: 2.75). The two signals
rank the nine currencies alike (mean monthly rank correlation +0.77; sleeve returns +0.83).
Both sleeves earned their alpha before about 2003 and nothing since.

| Run (nine currencies vs USD; alpha vs `tsmom12` on the US market, above bills) | Months | Sharpe | alpha %/yr | IR | z (decides) |
|---|---:|---:|---:|---:|---:|
| **Sleeve, real-rate value (primary 1)**, 5 bps per unit turnover | 542 (1980-09..) | 0.33 | +2.91 | **+0.28** | **1.71** |
| **Book with the real-rate sleeve (primary 2)**, #170's costs | 1,168 (1928-07..) | 0.40 | +1.50 | **+0.31** | **2.74** |
| S1 sleeve gross | 542 | 0.36 | +3.26 | +0.31 | 1.91 |
| S2 sleeve, FX costs x2 | 542 | 0.29 | +2.56 | +0.24 | 1.50 |
| S3 sleeve, point-to-point 60-month change (no averaging) | 547 | 0.31 | +2.73 | +0.26 | 1.63 |
| S4 sleeve 1994-01..2025-10 | 382 | 0.14 | +1.12 | +0.11 | 0.57 |
| S5 sleeve vs the six-asset `tsmom12`, 1994-03.. | 380 | 0.14 | +1.08 | +0.10 | 0.52 |
| B1 book gross | 1,168 | 0.97 | +4.31 | +0.89 | 7.38 |
| B2 book, UMD at 0.34%/mo | 1,168 | 0.60 | +2.46 | +0.51 | 4.43 |
| B3 bonds + FX only, with the swap (1962-04..) | 763 | 0.46 | +2.08 | +0.44 | 2.65 |
| C1 control: #170's proxy sleeve, same scoring | 542 | 0.37 | +3.10 | +0.30 | 1.89 |

Sleeve halves (the card's "both positive" rule): 1980-09..2003-03 IR +0.70 (NW z 3.04),
2003-04..2025-10 IR -0.14 (z -0.65): not both positive, so the sleeve would have failed the
pass rule even at a higher z. Book halves: +0.28 and +0.40, both positive, z fails.
Check: #170's primary book through the unchanged default code path gives z 2.75, IR +0.31,
exactly #170's numbers.

## What it means

1. **The proxy was not what held the book back.** #170 failed on the cost of stock momentum;
   the currency-value sleeve was one of its better net sleeves, and the published definition
   does not improve it (IR -0.02 against the proxy, well inside noise: the sleeves correlate
   +0.83). The book moves by 0.01 in z, as the card's arithmetic foresaw (a book pass needed a
   sleeve IR of about 2.4).
2. **Where the inflation adjustment matters, it does not help on balance.** The signals differ
   most in the 1980s (rank correlation +0.54), when 5-year inflation gaps among these
   currencies were wide; there the proxy did better (net Sharpe 0.56 vs 0.43). In the 1990s
   the real rate did better (1.09 vs 0.80). From the 2000s the two are nearly the same signal
   (+0.85 to +0.91) and both are weak or negative (2020s: -0.53 / -0.41).
3. **G10 currency value has been flat for two decades.** Since 2003 the real-rate sleeve's
   alpha is -1.4% a year; since 1994 IR +0.11 (z 0.57). The century-style evidence for it rests
   on 1980-2002.
4. **Kill rules applied (card, rule 3).** Currency value on this nine-currency G10 panel is
   closed as a candidate at the project bar: no lookback, window, cost or currency-set
   variants. It may come back only as a fixed component of a new book on a new card, or on
   independent currencies (outside these nine) on its own card. The century book is closed on
   this data: no further sleeve swaps of #170's book.

## How sure

- One run of the pre-registered evaluation; card and code pushed before it; card not amended.
  Before the run only file existence was checked (no CPI, rate or return looked at).
- The fail is robust: every sleeve row is below z 2 (gross 1.91), and the proxy control sits
  at the same level, so the conclusion does not hinge on a cost or a form choice.
- The test had little power against the published effect size (the card: a pass needed IR
  about 0.70; published G10 currency value is about 0.3-0.5), so "fail" says the sleeve is not
  a large surprise, not that currency value is zero. The measurement (IR +0.28, SE about 0.16)
  is the useful output.
- Limits: nine currencies only (rank weights on 4-9 assets are coarse); CPI is today's BIS
  vintage (small revisions, not measured); EUR before 1999 is the mark's monthly average spot
  with German CPI; AUD and NZD CPI quarterly (used only from quarter start + 5 months); FX
  returns are carry-inclusive (data-long-3's upper estimate of carry, which does not enter the
  value signal).

## Logged

`research/tries.md`: 11 rows, idea `fx-value-real-1`: two `variant` (sleeve, book), eight
`robustness` (S1-S5, B1-B3), one `control` (C1, the proxy sleeve, never logged before as a
row). #170's book re-run (the check) is not logged again. Sharpe there is of monthly excess
returns x sqrt(12). No `ledger/tries.jsonl` line (the gym cannot hold shorts). No new download
(0 bytes: all inputs were already cached by data-long-3 and data-long-4).
