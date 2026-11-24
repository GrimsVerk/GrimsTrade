# ownvol-anatomy-1: where does own-vol's lead (or loss) over `tsmom12` come from?

Lane `ownvol-anatomy-1`, 2026-11-24 (night). Branch `ownvol-anatomy-1`, PR #172. Research
only: fake money, files already in the data cache (read-only), no change to the gym, the daily
runner, the live strategies or the `own_vol_70` paper book. Train data only: the loaders of
pooled-1, pooled-2 and risk-menu-3 stop at 2025-10-31. A **descriptive re-score** of finished
tries (risk-menu-3 #110, pooled-1 #142, pooled-2 #159) on their own series and rule code: no new
rule, own-vol not retuned, nothing selected, not a new test. Card (pushed before any number,
not amended): `cards/ownvol-anatomy-1.md`. Tables: `results/ownvol-anatomy-1.md` (+ `.json`).
Code: `lib/ownvolanatomy.py`, `lib/ownvolanatomy_core.py`; tests `tests/test_ownvolanatomy.py`.

## The answer on one screen

**Own-vol's lead is not holding less, and it is not the leverage effect either. It is risk
removal: when a stock market's recent swings are large, the sleeve earns about the same return
as in calm spells (+9.5% against +9.4% a year, pool means) but with twice the variance (0.040
against 0.020). Cutting the share then removes risk, not return. On the 41 stock markets that
risk channel is +0.024 Sharpe a market (SE 0.011, "carries" by the card's rule); the mean
channel is -0.003 (SE 0.018); holding less (a fixed share at own-vol's average, 0.73) is
+0.001. By regime the gain comes in falls that `tsmom12` is still invested in (25% zigzag: slow
bears +0.033, fast crashes +0.016, 21% of the time together) and is partly paid back in calm
markets (-0.018) and rebounds (-0.008; -0.038 under the 15% zigzag, where rebounds are a third
of the time). On the six (#110) the same picture, larger: +0.101 = risk +0.251, mean -0.153,
exposure +0.003. There the volatile spells are the ones that pay (sleeve +33% a year against
+12% in calm spells: coin rallies), and own-vol gives that up but removes more risk.**

**Currencies lose through the mean channel, and only the commodity currencies do.** CAD, AUD,
NZD and NOK: -0.123 a market = mean -0.132 (SE 0.051, carries) + risk +0.009. Their `tsmom12`
sleeve earns +8.1% a year in its volatile spells and +0.2% in calm ones, the reverse of stocks:
their trends pay when they are volatile, and own-vol cuts exactly those. About 60% of the loss is
in the first six months after `tsmom12` re-enters (-0.075), pooled-2's guess, and the rest in
later held spells (-0.049). The other five currencies are +0.006. Of the +0.073 gap between
stocks and the nine currencies, +0.053 is the mean channel and +0.020 the risk channel
("through the mean channel"). Commodity spot gains (+0.056) through the risk channel (+0.075):
volatile PPI spells have 2.6 times the variance at less than twice the mean. Bonds are small either way.
Leverage correlation (return now against the change in volatility next): stocks -0.14,
currencies -0.01, commodities -0.09. Volatility persistence is positive in every class (0.18 to
0.42), so the risk channel works everywhere; what differs is whether volatile spells pay.

Everything here describes D values already reported (pooled-1 +0.022, z 1.37; pooled-2 -0.010,
z -0.57); it cannot make them significant. The SEs are a linearised calendar bootstrap, a
description of how much the split moves with the calendar, not a test. Bar for scale: z >= 4.70.

## The split (card)

Per series, d = SR(own-vol) - SR(`tsmom12`) = E + M + R exactly:

- **E, exposure**: Sharpe of a fixed-share twin F (same monthly resets, drift and reset cost as
  own-vol, share always own-vol's average while `tsmom12` is invested) minus `tsmom12`'s.
- **M, mean channel**: (mean of own-vol - mean of F) / sd of own-vol. M > 0 if own-vol earns more
  than the same average exposure held fixed (high-volatility spells earn less: the leverage /
  volatility-feedback effect).
- **R, risk channel**: F's mean x (1 / sd own-vol - 1 / sd F). R > 0 if own-vol has smaller
  swings than F at F's mean (volatility clusters, and cutting in volatile spells removes risk).

Each term is a sum over periods, so regimes, volatility states and trend phases split it exactly.

| Pool | n | d (SE) | E | M (SE) | R (SE) | Avg share | Reading (a) |
|---|---:|---|---:|---|---|---:|---|
| Equity 41 | 41 | +0.022 (0.017) | +0.001 | -0.003 (0.018) | **+0.024** (0.011) | 0.73 | risk channel carries |
| US industries | 10 | +0.061 (0.025) | +0.003 | +0.012 (0.028) | **+0.046** (0.021) | 0.71 | risk channel carries |
| Developed 13 | 13 | +0.026 (0.025) | -0.000 | +0.011 (0.029) | +0.016 (0.014) | 0.71 | within noise |
| Wider 10 | 10 | +0.016 (0.026) | +0.001 | -0.009 (0.025) | +0.024 (0.015) | 0.77 | within noise |
| ETF8 | 8 | -0.027 (0.023) | -0.002 | -0.036 (0.026) | +0.010 (0.013) | 0.70 | within noise |
| Bonds + FX (judged) | 21 | -0.010 (0.018) | +0.000 | -0.015 (0.018) | +0.005 (0.006) | 0.65 | within noise |
| US bonds | 3 | +0.023 (0.038) | -0.000 | -0.001 (0.047) | +0.024 (0.021) | 0.64 | within noise |
| Foreign bonds | 9 | +0.022 (0.025) | -0.000 | +0.022 (0.027) | -0.000 (0.011) | 0.70 | within noise |
| Currencies | 9 | -0.052 (0.033) | +0.000 | -0.056 (0.035) | +0.004 (0.009) | 0.61 | within noise |
| Commodity currencies | 4 | -0.123 (0.047) | -0.000 | **-0.132** (0.051) | +0.009 (0.014) | 0.56 | mean channel carries |
| Other currencies | 5 | +0.006 (0.030) | +0.001 | +0.005 (0.032) | -0.000 (0.007) | 0.65 | within noise |
| Commodity spot (shown) | 8 | +0.056 (0.037) | -0.001 | -0.018 (0.034) | **+0.075** (0.024) | 0.61 | risk channel carries |
| The six (#110, daily) | 1 | +0.101 | +0.003 | -0.153 | +0.251 | 0.65 | - (one series) |

Reproduction (card check): every per-series d equals pooled-1's and pooled-2's published d
(max difference 3e-16); the six's d is +0.101 (1.035 - 0.933; #110 printed 1.036 - 0.937, the
gap is later bill-rate code, not this lane). The replayed own-vol loops give the frozen code's
returns exactly (checked on every series and in the tests).

## (b) Is the lead just holding less? No.

Sharpe does not change when a fixed share of the same sleeve is held (cash at 0 or at the bill),
so E is about zero by construction: +0.001 on stocks, +0.000 on bonds and currencies, +0.003 on
the six, at most 0.003 in any pool (reading: "not holding less" everywhere). Holding less does
change growth and worst loss, and there the fixed twin explains most of what own-vol does on
single markets (pool means; Sharpe / growth a year / worst loss):

| Pool | `tsmom12` | Fixed twin | Own-vol |
|---|---|---|---|
| Equity 41 | 0.478 / 5.8% / 45% | 0.478 / 4.4% / 35% | 0.499 / 4.4% / 35% |
| Bonds + FX 21 | 0.287 / 1.3% / 27% | 0.287 / 0.9% / 18% | 0.277 / 0.9% / 19% |
| Commodity spot 8 | 0.364 / 2.9% / 56% | 0.364 / 2.2% / 38% | 0.421 / 2.2% / 31% |
| The six | 0.933 / 15.6% / 39% | 0.937 / 10.3% / 27% | 1.035 / 9.1% / 16% |

On a single stock market, own-vol's smaller worst loss (35% against 45%) is the smaller average
share; at the same share it is no better. On the six the timing adds a lot to the worst loss
(16% against 27% for the fixed twin), at 1.2 points less growth a year.

## (a) Volatility timing: the risk channel, not the mean channel

Split by own-vol's share at the start of each period (terciles of the in-market periods; low
share = high recent volatility):

| Pool | M low / mid / high share | R low / mid / high share | Sleeve mean a year, low / high share | Sleeve variance, low / high |
|---|---|---|---|---|
| Equity 41 | -0.049 / -0.003 / +0.052 | +0.058 / +0.003 / -0.040 | +9.5% / +9.4% | 0.040 / 0.020 |
| Commodity currencies | -0.096 / -0.011 / -0.024 | +0.039 / +0.005 / -0.033 | +8.1% / +0.2% | 0.012 / 0.006 |
| Commodity spot | -0.055 / -0.015 / +0.053 | +0.093 / +0.008 / -0.028 | +5.9% / +3.2% | 0.069 / 0.027 |
| The six | -0.291 / +0.028 / +0.102 | +0.283 / +0.043 / -0.071 | +32.6% / +11.5% | 0.062 / 0.010 |

- On stocks own-vol gives up return in volatile spells (-0.049) and wins it back by holding more
  in calm ones (+0.052): the mean channel nets to about zero because the sleeve earns about the
  same in both. The leverage effect is there in prices (L -0.14: falls raise volatility) but it
  does not make volatile spells earn less once `tsmom12` has filtered them. What is left is the
  variance: twice as high in volatile spells, so cutting there removes more risk than the higher
  share adds in calm spells (+0.058 - 0.040). The Moreira-Muir condition (return does not rise
  with variance) holds; a volatility-feedback mean gain does not show.
- On the commodity currencies the sleeve's return is concentrated in volatile spells (+8.1% a
  year against +0.2%), so cutting there costs return (-0.096) and the higher calm share earns
  nothing (-0.024). The risk channel works (+0.039 - 0.033), but it is small against that.
- On the six the same as the currencies in direction (volatile spells pay, mostly coin rallies),
  but the variance falls far more (0.062 against 0.010), so the risk channel wins: +0.251 against
  -0.153.

## (c) Regimes

M + R by regime, primary reading A (25% / 25% zigzag on the traded level; share of time):

| Pool | Fast crash | Slow bear | Rebound | Whipsaw | Calm |
|---|---|---|---|---|---|
| Equity 41 | +0.016 (0.007), 1% | **+0.033** (0.013), 20% | -0.008 (0.006), 20% | -0.001 (0.003), 14% | -0.018 (0.012), 45% |
| US industries | +0.019 (0.007), 1% | +0.039 (0.016), 18% | -0.007 (0.009), 18% | +0.006 (0.004), 12% | +0.000 (0.013), 52% |
| Commodity currencies | 0% | -0.026 (0.026), 36% | -0.002 (0.010), 8% | -0.029 (0.020), 20% | **-0.066** (0.037), 36% |
| Commodity spot | +0.002, 0% | **+0.087** (0.037), 31% | -0.012 (0.007), 11% | +0.004 (0.006), 6% | -0.025 (0.020), 52% |
| The six | +0.027, 0% | +0.197, 16% | -0.075, 17% | -0.014, 33% | -0.037, 33% |

- **Stocks: falls give, rebounds and calm take.** Slow bears (+0.033) and fast crashes (+0.016)
  carry by the card's rule in readings A and C (B: slow bears). In a fall that `tsmom12` is
  still holding, recent volatility rises and own-vol cuts before the 12-month signal leaves.
  That is mostly the mean channel (slow bears M +0.025, R +0.008): inside a fall, the high-vol
  spell does earn less. Paid back in calm markets (-0.018) and in rebounds (-0.008 under A,
  -0.038 under C): after the low the sigma still carries the crash, and own-vol holds little as
  the market recovers.
- **Fast crashes were expected at zero and are positive** (+0.016 under A, +0.033 under C): the
  expectation in the card was wrong. Why was not checked; possible reasons are that a monthly
  reset inside a crash month already sees part of it, or that volatility was already up before
  some crashes.
- **Commodity currencies lose in calm and whipsaw spells**, not in falls (falls of their
  excess-return level are slow and long here). Calm is when their volatile up-trends run; what
  drives those (commodity cycles, carry) was not examined.
- **The six**: slow bears +0.197 of the hold-the-six level, given back in rebounds (-0.075)
  and calm (-0.037). Which episodes carry it was not split out.

Readings B (zigzag at 1.5 x the series' volatility) and C (15% / 15%) agree in sign for the
stock pool in every regime (B: slow +0.035, rebound -0.004, calm -0.018; C: fast +0.033, slow
+0.034, rebound -0.038). For bonds and currencies B and C find more falls; there bonds gain in
slow bears (GOV9 +0.045 under B) and lose in calm stretches.

## (d) Why stocks and commodities gain but currencies lose

| Equity 41 minus | Gap in d | E | M | R | Reading (card) |
|---|---:|---:|---:|---:|---|
| Currencies 9 | +0.073 | +0.000 | +0.053 | +0.020 | through the mean channel |
| Commodity currencies 4 | +0.145 | +0.001 | +0.129 | +0.015 | through the mean channel |
| Bonds + FX 21 | +0.031 | +0.001 | +0.012 | +0.019 | through the risk channel |
| Commodity spot 8 | -0.035 | +0.001 | +0.015 | -0.051 | through the risk channel |

| Pool | Leverage corr. L | Vol persistence | Sleeve mean / variance, low / high share |
|---|---:|---:|---|
| Equity 41 | -0.140 | +0.415 | +2.35 / +4.77 |
| Bonds + FX 21 | -0.014 | +0.242 | +3.34 / +4.70 |
| Commodity currencies 4 | +0.008 | +0.414 | +6.63 / +0.30 |
| Other currencies 5 | -0.027 | +0.179 | +1.09 / +2.58 |
| Commodity spot 8 | -0.087 | +0.291 | +0.86 / +1.19 |

- Volatility persists in every class (the sigma own-vol uses predicts next month's volatility
  with a correlation of 0.18 to 0.42), so the risk channel is positive or zero everywhere.
- The classes differ in where the return is. On stocks and commodities return per unit of
  variance is lower in volatile spells (2.35 against 4.77; 0.86 against 1.19), so cutting there
  is cheap. On the commodity currencies it is twenty times higher in volatile spells (6.63
  against 0.30): their profitable `tsmom12` spells are the volatile ones, and own-vol sizes
  against them. The other five currencies behave like stocks in direction (1.09 against 2.58)
  but have little volatility to time, so they end near zero.
- Leverage correlation separates stocks (-0.14, falls raise volatility) from currencies (about
  zero; a currency against the dollar has no natural "down" side). The expectation in the card
  that JPY and CHF would show L > 0 was wrong (-0.05, -0.02).
- Trend phase on the commodity currencies: the first six months after a `tsmom12` entry -0.075,
  later held periods -0.049. pooled-2's guess (the sleeve is cut again for the rebound) is about
  60% of the loss; the rest is that their trends keep paying while volatile.

## Expectation (card) against result

- E about zero everywhere: yes (|E| <= 0.003).
- Stocks: risk channel most of D, mean channel small or negative: yes (+0.024 / -0.003).
- Stocks lose in rebounds and the entry phase, gain in slow bears: rebounds and slow bears yes;
  the entry phase is positive on stocks (+0.005; US industries +0.025), not negative.
- Fast crashes about zero: no, positive (+0.016 / +0.033).
- Currencies: risk channel small, mean channel negative, in the entry phase and the low-share
  tercile of the commodity currencies: yes (-0.075 entry, -0.096 low-share M).
- L negative for stocks, near zero for currencies: yes; positive for JPY and CHF: no.

## How sure

- One run. Card, code and tests pushed before the numbers; the card was not amended. A first
  run with 200 draws showed that the exact E terms with fixed standard deviations give E a
  spurious SE (0.035: F is a scaled `tsmom12`, and that linearisation is not scale-free), so E's
  SE (and d's) uses the delta-method Sharpe influence instead (scale-free; d's SE then matches
  pooled-1's 0.016 for this rule). Point numbers and the M, R splits are unchanged by that, and
  the card's readings do not use E's SE. Noted here as the one change after a number was seen.
- The SEs are linearised (means and sds held at full-sample values), on 12-month calendar
  blocks. They say how much the split moves with the calendar. Several splits are read from the
  same 70 series; "carries" is a description, not a test.
- The fixed twin uses own-vol's whole-sample average share: a descriptive twin, not a rule.
- Regime labels use the whole history (the zigzag's turning points and the whipsaw window look
  ahead): they describe periods, they are not signals.
- Commodity spot is smoothed producer-price data (pooled-2: shown, not judged); its risk channel
  may partly be smoothing. Four commodity currencies are four series with a shared driver.
- The six is one 32-year series; #110's paired SE of its lead is about 0.1. Its split says
  where the +0.10 came from in that sample, not that it will recur.

## For the live rule and the paper book

Nothing changes. `tsmom12` stays the rule; `own_vol_70` stays a paper risk dial. What the split
adds: on stocks own-vol is a risk-removal dial whose Sharpe gain (if any) comes from cutting in
volatile falls and is paid for in rebounds; it should be expected to trail `tsmom12` after a
crash low. On the six its lead depends on the coin slots' volatile rallies being outweighed by
the variance they remove. Where an asset's trends pay mostly while volatile (the commodity
currencies here), own-vol loses. That is a reason to read the paper book's record by asset
class, not a new rule.

## Logged

`tries.md`: one `note` row, idea `ownvol-anatomy-1` (re-score, not a try). `ideas.md`: a line
under `own-vol-target`.
