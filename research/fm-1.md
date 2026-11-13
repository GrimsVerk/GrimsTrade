# FM 1: do time-series foundation models know anything the trend rule doesn't?

Research run fm-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-fm-1.md`. Branch `fm-1`
(from `invest-1`). Research only: no live change. Held-out year not loaded unless something
passes on train (then once, by the protocol).

Question: every hand-made input so far has weekly IC <= 0.05 (`rl-3.md`, `info-1.md`,
`breadth-1.md`). Pretrained time-series models (DESIGN.md ladder rung 4) are the other GPU route.
Do their zero-shot forecasts of our own price series carry information the trend inputs lack?

## In plain words (results, 2026-11-13)

**No. The foundation models' forecasts do not beat the trend inputs. The two Chronos-Bolt
models look excellent at first (weekly IC 0.10-0.15, three times anything found before, and
+0.10 / +0.18 Sharpe over `tsmom12` in the rl-3 gate), but they are recalling stock-market history
they saw in pretraining, not forecasting it. On the years they have not seen (2020-2025), their
IC is zero and the gate edge disappears. Chronos-2, which does not recall the series, has no skill
in any period. So this route gives the RL agent nothing as is, and the "too good" result is a
warning for any pretrained model tested on old market data.** Research only; the held-out year
was not looked at. Tables: `results/fm-1.md`.

- **What was run.** Three official Amazon models, zero-shot, bf16 on the 5080: Chronos-Bolt
  small (48M) and base (205M), and Chronos-2 (120M). Each forecast every Friday's next week for the
  six assets (2000-2025), every next day, and every next hour and next day of hourly BTC/ETH
  (2023-2025). Everything the card fixed, plus memorisation checks added after the first result.
- **The first result looked too good.** Bolt-base: weekly IC +0.148 (chance level 0.043),
  walk-forward gain over the trend inputs +0.110 (the info-1 bar was +0.05), and the gate passed
  train bars 1-3 (Sharpe 1.17 vs 0.99, p 0.0005, ahead in 3 of 4 eras, smaller drawdown). SPY's
  weekly IC was +0.29. Nothing hand-made ever came near.
- **Why it is memory, not skill (three checks that agree):**
  1. *Time pattern.* On every equity series (the six assets, 8 other ETFs, 4 world indexes, 9 US
     sectors) Bolt's IC is +0.15 to +0.32 up to 2019 and about **0.00 in 2020-2025**. On the
     S&P 500 index **1964-1993** it is also about 0 (+0.005 / +0.013). Real skill would not switch
     on in 1994 and off in 2020. A pretraining corpus holding daily stock prices from roughly the
     1990s to 2019 would do exactly this.
  2. *Inverted prices.* The same six series fed as 1 / price (the same patterns, mirrored): a
     model that reads patterns should score about the same. Bolt's IC drops from +0.17 / +0.23 to
     **+0.00 / +0.02** (SPY +0.29 to +0.06). It recognises the exact series, not its shape.
  3. *Model that doesn't remember.* Chronos-2 shows neither the 1994-2019 bump nor any IC
     anywhere (-0.06 to +0.07 in every book and period; weekly gate -0.000).
  The gate edge also goes with the memory: from 2020 on, Bolt-small is +0.04 (p 0.31) and Bolt-base
  **-0.10** against `tsmom12`.
- **After release (the only window certainly outside the weights).** Bolt, Dec 2024 - Nov 2025:
  weekly IC +0.10 / +0.16 on 280 cells, but the inverted series score the same (+0.14 / +0.15), so
  it is a symmetric pattern of one crash-and-rebound year (April 2025). Its standard error is
  about 0.10-0.14 with these few, highly correlated weeks. The five unremembered years before it
  (2020-24) say zero. Daily after release: -0.03 / -0.01 (1,628 cells). Hourly after release:
  Bolt's 1-hour IC is -0.04 to +0.03 with opposite signs on BTC and ETH; Chronos-2's 3 weeks show
  +0.13, but its earlier hours were negative. Breadth-1 found that an hourly signal needs an IC
  near 0.6 to pay 30 bps; these are 0.03.
- **Fine-tune: not run.** The card's trigger (a post-release IC more than two standard errors
  from zero, the same sign as before release, and adding to the trend inputs) is met by the
  letter in 2 of 18 post-release tests (12 hourly, 3 weekly, 3 daily): Bolt-small ETH 1 h
  (+0.028) and Bolt-base BTC 1 h (-0.038). They point in opposite directions, close to the one
  or two that chance gives across 18 tests, and they are 20 times
  below the cost break-even. A fine-tune on the train years would also train on exactly the years
  the models already remember. Judgement call, written here so it can be challenged.
- **GPU time and memory.** The whole zero-shot run took under a minute of GPU time: 9-22 s per model
  for ~6,000 weekly, ~35,000 daily and ~50,000 hourly forecasts, plus a few seconds per check.
  Peak GPU memory 0.25-0.76 GB of 16 GB; process RAM about 2.5 GB. The 5080 is nowhere near a limit
  for inference; a bf16 fine-tune of Bolt-small would also fit easily.
- **How sure.** Sure that the weekly train-period result is memorisation: three independent
  checks agree, on 27 series. Sure that there is no skill in 2020-24 (5 years, 27 series, IC about
  0 for all three models). Not sure about skill after release: 11 months is too short. The clean
  test would be the held-out year (after every release); the protocol allows that look only for an
  idea that passes on train, and this pass is void.

### Is this route worth more work for the RL agent?

Not as a source of forecasts on price history alone. Zero-shot, the one model without memory
has no skill, and the remembering models have none outside their memory. A fine-tune would teach
them the same price history our own models already failed to find anything in. Worth keeping:

1. **The memorisation test is the lesson.** Any pretrained model (time-series or LLM) tested on
   market data before its cutoff can look brilliant for this reason alone. Cheap checks: 1 / price
   input, IC by year around the probable corpus end, an old pre-1994 series. Use them on any future
   model before believing a train-period number.
2. If the owner still wants rung 4, the honest design is a **forward-only test**: log a model's
   forecasts on the paper trail from now on (no backtest), and judge after a year. That costs
   seconds of GPU a week. Recommended only as a low-priority side log, not an RL input.
3. TimesFM 2.5 and Moirai were not run (card). They are trained on similar public corpora, so the
   same checks would be needed first. Not worth it unless the forward log shows something.

### Disclosures

- The memorisation checks (inverted prices, the out-of-universe books, IC by period, the gate
  from 2020) were written and run **after** the first weekly result was seen. They are checks of
  that result, not new variants; their forecast runs are not strategies and have no tries rows.
  The 21 rows in `tries.md` are the card's runs: 3 gate `variant`s and 18 `screen`s.
- By the letter, Bolt-base's gate passes train bars 1-3 (bar 4, out-of-universe, was not run as
  a gate; bar 5, equal weight, not checked). It is declared void because of the leakage shown
  above, and the held-out year is left unspent.
- Data: the six-asset tables were copied from the breadth-1 worktree's git-ignored cache (read
  only); hourly bars from the shared data root.

## Card (written 2026-11-13, before any forecast was computed)

### Models (zero-shot first)

Official publisher accounts only, safetensors only, no `trust_remote_code`, loaded through the
`chronos-forecasting` package (Amazon's own code from PyPI, installed only in a throwaway
`uv run --with` environment, never in the project's dependencies). Revisions pinned: the commit
of each download is written into the result file and the table below.

| Variant | Weights | Size | Released on HF | Documented pretraining data |
|---|---|---:|---|---|
| `fm-bolt-small` | `amazon/chronos-bolt-small` | 48M | 2024-11 | Chronos corpus (Ansari et al. 2024): ~28 public datasets (energy, transport, retail, web, weather, some finance such as the M4 finance subset) plus TSMixup and KernelSynth synthetic series; Bolt: "nearly 100 billion observations". No data cutoff published. |
| `fm-bolt-base` | `amazon/chronos-bolt-base` | 205M | 2024-11 | as above |
| `fm-chronos2` | `amazon/chronos-2` | 120M | 2025-10 | Chronos corpus plus further real and synthetic (multivariate) series; no cutoff published. |

Not run in this pass (budget; written here so the gap is visible): TimesFM 2.5 (`google/
timesfm-2.5-200m-pytorch`, needs Google's `timesfm` package from source) and Salesforce Moirai
(`uni2ts`, heavy dependencies; its LOTSA corpus is documented and does include some finance).
If Chronos shows anything they are the next variants; if not, a second family is unlikely to
change the answer (they are trained on similar public corpora, and the benchmarks rank them
within a few percent of each other).

### Inputs and forecast

- Context: the asset's last 512 observed closes (daily bars, or hourly bars for the hourly
  target), raw price level as the models expect; nothing after the decision bar.
- Forecast: the median (0.5 quantile) at the target horizon. Score `fc = log(median_h /
  last close)`. ETFs: horizon 5 trading bars for a week, 1 for a day. Crypto: 7 and 1 daily bars;
  1 and 24 hourly bars.

### Targets and periods

1. **Weekly, six assets** (main test, with the gate): `rl3_plant.week_z`, Fridays 2000-01-07 ..
   2025-11-07, the rows of `results/rl-3-inputs.md` and `results/info-1.md`.
2. **Daily, six assets**: next-day close-to-close log return / EWMA vol, 2000-2025 (IC only).
3. **Hourly BTC/ETH (Binance)**: next 1 h and next 24 h log return, 2023-01-01 .. 2025-11-09
   (IC only). The breadth-1 hourly reversal (`r_1h`, IC -0.06 to -0.09) is the input to beat.
4. Wider books from breadth-1: not in this pass (budget). Only if 1-3 show anything.

### Leakage (the models may have seen our test years)

Pretraining corpora are only partly documented and no cutoff is published, so the **release date
is the only safe bound**: data after it cannot be in the weights. Every IC is reported three ways:
full period, before release, after release. Data after release inside the train period
(decisions before 2025-11-10):

- Chronos-Bolt (2024-11-26): ~49 weeks x 6 assets ~ 290 weekly cells (one standard error of an
  IC ~ 0.06 even before cross-asset correlation); ~ 1,450 daily cells; ~ 8,300 hours x 2 coins.
- Chronos-2 (2025-10-20): 3 weeks. Effectively no clean weekly or daily test; hourly ~ 480 h.

So the clean tests are the **hourly** ones and, weakly, Bolt's daily ones. The weekly test is
mostly in-sample for the pretraining (a positive weekly IC before release and none after would
mark leakage or luck, not skill). The held-out year (2025-11-11 .. 2026-11-09) is after every
release and would be the clean weekly test, but the protocol lets it be looked at only for an
idea that passes on train.

### Measures and bars (fixed now)

- **IC**: Pearson correlation of `fc` with the target, pooled over assets; standard error and,
  for the weekly target, the circular-shift chance level of `info1_ic.py`.
- **Against the trend inputs**: weekly, the walk-forward gain of `info1_ic.walk_forward`
  (7 trend inputs + `fc` minus trend inputs alone, OLS refitted every two years). Hourly, the
  IC of `fc` next to `r_1h` and its partial correlation with the target given `r_1h`, `r_24h`,
  `r_168h`.
- **Gate (rl-3)**: a residual tilt on `tsmom12` exactly as the rl-3 ceiling rule (same action,
  same costs, gym replay, 2000-2025): score = `fc / sd_past(fc)` (the forecast divided by the
  standard deviation of that asset's forecasts over the previous 104 Fridays; 0 before that).
  One `variant` row per model in `tries.md`. Pass = the protocol's train bars 1-3 (Sharpe beats
  `tsmom12` with bootstrap p < 0.10, ahead in at least 3 of 4 eras, drawdown not 5 points
  worse).
- **"Shows anything"** (the condition for a fine-tune): the gate passes for some model, or a
  post-release IC is more than two standard errors from zero with the same sign as before
  release and adds to the trend inputs (partial correlation of the same sign). Otherwise no
  fine-tune, and the write-up says why.
- **Fine-tune (only if triggered)**: Chronos-Bolt-small, bf16 on the 5080, trained on the
  pooled six-asset (or hourly) series before each walk-forward refit year, same measures.

### Counting

Every model x target run gets a `tries.md` row: the weekly gate runs as `variant`, the IC-only
runs as `screen`. GPU time and peak memory are recorded per run.

## Status

2026-11-13: done. Zero-shot run on three models, memorisation checks, write-up. No fine-tune
(reason above). Not run: TimesFM, Moirai, the wider breadth-1 books (card). Held-out year
unspent. Usage at stop: weekly 16%, session 18%. Draft PR #25 (`fm-1` -> `invest-1`).
