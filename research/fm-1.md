# FM 1: do time-series foundation models know anything the trend rule doesn't?

Research run fm-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-fm-1.md`. Branch `fm-1`
(from `invest-1`). Research only: no live change. Held-out year not loaded unless something
passes on train (then once, by the protocol).

Question: every hand-made input so far has weekly IC <= 0.05 (`rl-3.md`, `info-1.md`,
`breadth-1.md`). Pretrained time-series models (DESIGN.md ladder rung 4) are the other GPU route.
Do their zero-shot forecasts of our own price series carry information the trend inputs lack?

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
