# xs-century-1: does a century-long long-short style book add to `tsmom12`?

Lane `xs-century-1`, 2026-11-24 (night). Branch `xs-century-1` from `main` (`fac43c9`), PR
#170. Research only: fake money, cached keyless data (read-only), no change to the gym, the
daily runner or the live strategies. Nothing after 2025-10-31 parsed; held-out year untouched.
Card (pushed before any number, `c588626`, not amended): [`cards/xs-century-1.md`](cards/xs-century-1.md).
Code pushed before the run (`6a4eb6e`): `lib/xs_century.py` (pure parts; tests
`tests/test_xs_century.py`), `lib/xs_century_run.py` (one run, 3 s). Tables:
[`results/xs-century-1.md`](results/xs-century-1.md). Shorts are research-only (B7) and the
Ken French portfolios are not tradable in the gym, so the verdict is informational.

## The answer on one screen

**Fail, by the card's rule: z 2.75 against a bar of 4.70 (IR +0.31 against power-map-1's 0.51 /
0.60).** This was the one test power-map-1 (#150, row C2) said could pass honestly. It does not
pass after published trading costs. It passes easily before them (gross z 7.4, IR +0.88).
The costs that decide it are momentum's: the card's
Novy-Marx-Velikov charge of 0.65% a month on UMD wipes out US stock momentum (net Sharpe
0.03). The book's edge also fades over time: alpha +0.64% a year after 1994 (z 0.75), negative
in the 2010s and 2020s.

- **The book** (card, nothing tuned): Asness-Moskowitz-Pedersen 2013 value and momentum,
  Koijen-Moskowitz-Pedersen-Vrugt 2018 carry, Ilmanen et al. 2021 century construction. US
  stock selection (HML, UMD as published, from 1926/27), 10 government bonds (value, momentum,
  term-spread carry, from the 1960s) and 9 currencies against USD (spot-reversal value,
  momentum, rate-differential carry, from 1973). Rank-weighted dollar-neutral sleeves, each
  scaled to 10% ex-ante volatility (36-month window), equal weight across asset classes. OECD
  inputs lagged 3 months, FX spot 2.
- **The comparator**: `tsmom12`'s rule on the US market (Ken French, monthly, in when the
  12-month total return is positive, else bills), scored above bills. It is the only `tsmom12`
  proxy that exists for the whole century. Sharpe 0.55 over 1928-07..2025-10.
- **The statistic**: OLS alpha of the book's monthly excess returns on the comparator's. z
  takes the larger of the Newey-West and the 12-month block-bootstrap SE (alpha-form-1's rule).

| Run (97.3 years unless noted) | Book Sharpe | rho with `tsmom12` | alpha %/yr | IR | z (decides) | Mix gain |
|---|---:|---:|---:|---:|---:|---:|
| **Primary** (HML 0.05%/mo, UMD 0.65%/mo, 0.5%/yr borrow, bonds/FX 5 bps per unit turnover) | 0.40 | +0.17 | +1.51 | **+0.31** | **2.75** | +0.08 |
| R1 gross (no costs) | 0.96 | +0.17 | +4.32 | +0.88 | 7.39 | +0.49 |
| R2 UMD at 0.34%/mo (NMV's staggered-rebalancing momentum) | 0.59 | +0.17 | +2.48 | +0.51 | 4.44 | +0.20 |
| R3 bond / FX costs x2 | 0.34 | +0.17 | +1.22 | +0.25 | 2.22 | +0.05 |
| R4 + commodity spot (not investable) | 0.39 | +0.16 | +1.30 | +0.31 | 2.61 | +0.08 |
| R5 1994-01..2025-10 (31.8 y) | 0.20 | +0.01 | +0.64 | +0.19 | 0.75 | +0.03 |
| R6 vs the six-asset `tsmom12` itself, 1994-03.. (31.7 y) | 0.20 | -0.02 | +0.72 | +0.22 | 0.84 | +0.03 |
| R7 bonds + FX only, 1962-04.. (63.6 y) | 0.45 | +0.04 | +2.11 | +0.43 | 2.63 | +0.16 |

Halves (the card's "both positive" rule): 1928-1972 alpha +1.64%/yr (IR +0.28), 1973-2025
+1.41%/yr (IR +0.39). Both positive, but the z fails anyway.

## What it means

1. **The power map's best case fails, and it fails on costs, not on the comparator.** The book
   hardly correlates with `tsmom12` (+0.17), so its alpha is nearly its own Sharpe. Gross, it
   is a 0.96-Sharpe book that would clear the bar by a wide margin. After the published cost of
   trading stock momentum it is 0.40. Even R2, the cheaper published momentum cost, stops at
   z 4.44, just under 4.70. The card fixed the primary cost in advance; R2 is a robustness row
   and cannot turn a fail into a pass. The cost of momentum in 1930-1990 is not known well:
   Novy-Marx and Velikov measured 1963-2013, and Jones (2002) puts earlier costs higher.
   The verdict is therefore "gross edge real, net edge unproven at the bar".
2. **What survives costs is carry and value outside equities, plus HML.** Net sleeve alphas
   against the comparator: bond carry IR +0.45 (z 3.2), FX value +0.30, HML +0.25 (z 2.1),
   FX carry +0.21. Bond value, bond momentum and UMD (net) are about 0. Bonds and FX alone
   (R7, 64 years) give IR +0.43, z 2.6.
3. **It matches survey-6's live record.** Since 1994 the book's Sharpe is 0.20 and its alpha is
   insignificant (z 0.75; z 0.84 against the real six-asset `tsmom12`). The 2010s were
   negative (-0.59 Sharpe), the decade of the live style-premia funds' 2018-2020 drawdown. The
   century average rests on 1940-2009, much of it before these premia were published.
4. **Nothing changes for the book.** Shorts stay parked (B7). The alpha form against
   `tsmom12` does not open a door here, because what was left after costs is a few tenths of
   Sharpe, as the record already said (live style premia 0.50 over 12 years, t 1.7). A
   long-short style sleeve would be a diversifier (mix gain +0.08 Sharpe in-sample, net),
   not an edge at the bar.

## How sure

- One run of the pre-registered evaluation, card not amended. The code and tests were
  pushed before the run. The tests check rank weights, signal lags (the skipped month and the
  lagged value data), vol scaling and its cap, turnover costs, book weights, and recovery of
  a planted IR. The only data looked at before the run was a coverage check (first and last
  month per series). No return was looked at.
- **The fail is robust to everything except the cost of momentum.** At every cost setting the
  card named, z is below 3.29 except R2 (4.44). Gross z 7.4 shows the test has the power
  power-map-1 promised: a gross IR of 0.88 over 97 years is detected easily.
- **Limits.** UMD and HML costs are one number for 97 years (NMV's 1963-2013 estimate), on
  scaled notional. Rescaling turnover and class-weight changes are not charged. The short
  borrow of 0.5% a year is a flat guess. Bond and FX costs (5 bps) are futures-like and
  probably low for the 1960s-70s (R3 doubles them: z 2.2). Bonds are rebuilt from monthly-
  average yields (smoothed). FX value is a spot-reversal proxy for PPP (no CPI cached), and
  FX carry is an upper estimate (data-long-3). Defensive (BAB) is missing. The comparator is
  `tsmom12` on one market, not the six-asset book; R6 uses the real one, but only since 1994.
- **Trial count.** 8 rows logged (1 variant, 7 robustness) plus the comparator baseline. The
  bar was not lowered for the alpha form or the new comparator; a stricter count would only
  raise it.

## Logged

`research/tries.md`: 9 rows, idea `xs-century-1`. One `variant` (the primary), seven
`robustness` (R1-R7) and one `baseline` (the comparator). Sharpe there is of monthly excess
returns x sqrt(12), stated in each Variant cell. No `ledger/tries.jsonl` line, because the gym
cannot hold shorts (as in ls-trend-2).
