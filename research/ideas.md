# Ideas

One line per idea. Status: `new` (written down), `testing` (has a card, being tested),
`live` (forward paper), `dead` (and why), `parked` (not testable here yet, and why). Dead ideas
stay: they count as tries. "Dead (literature)" means the survey killed it and we did not spend a
backtest on it; "dead (tested)" means our own test killed it (see `results/`).

## Cards tested in run 1 (all nine failed their pre-set bar; none used the held-out year)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| kelly-shrunk | Kelly / information theory | dead (tested) | [card](cards/kelly-shrunk.md) | Equals inverse-vol (+0.01 Sharpe): the no-leverage cap removes the Kelly scale. On high-volatility coins the scale halves drawdown at equal growth: see `vol-target`. [result](results/kelly-shrunk.md) |
| hmm-regime | Regime models | dead (tested) | [card](cards/hmm-regime.md) | Beats a volatility threshold (+0.14, p = 0.03) but equals equal weight (0.89 vs 0.88) and loses to the 200-day average (1.01); sat through the dot-com bust. [result](results/hmm-regime.md) |
| fracdiff-momentum | Fractional differentiation | dead (tested) | [card](cards/fracdiff-momentum.md) | Worse than 12-month momentum everywhere (-0.25 Sharpe, 3x turnover): it is a fast trend rule. [result](results/fracdiff-momentum.md) |
| drawdown-control | Optimal stopping / control | dead (tested) | [card](cards/drawdown-control.md) | Same as the 200-day switch (+0.07, p = 0.14; mixed out of universe). A smoother trend rule, not a better one. [result](results/drawdown-control.md) |
| universal-portfolio | Information theory | dead (tested) | [card](cards/universal-portfolio.md) | Indistinguishable from the constant mix it starts from; 30 years is too short for its guarantee. [result](results/universal-portfolio.md) |
| absorption-ratio | Random matrix theory / PCA | dead (tested) | [card](cards/absorption-ratio.md) | Worked inside the paper's sample (0.97 vs 0.56 to 2010), behind its plain twin ever since (1.13 vs 1.44); missed 2022. [result](results/absorption-ratio.md) |
| hawkes-clustering | Hawkes processes | dead (tested) | [card](cards/hawkes-clustering.md) | Self-excitation at daily bars is weak; the rule is equal weight minus a few days (0.87 vs 0.88), 7x the turnover. [result](results/hawkes-clustering.md) |
| month-end-liquidity | Calendar / microstructure | dead (tested) | [card](cards/month-end-liquidity.md) | Real in old data (S&P 1962-93 t = 4.0, FTSE 4.2, Nikkei 3.1), faded since 2014, never in TLT; in-or-out loses to a constant one-third holding on Sharpe. [result](results/month-end-liquidity.md) |
| dip-rsi2 | Short-term reversal | dead (tested) | [card](cards/dip-rsi2.md) | Bounce is real on SPY (21.6 vs 3.9 bps a day, t = 2.5), halved since publication, weak on 7 other markets, and only 5% exposure: +2.3% a year. [result](results/dip-rsi2.md) |

## Cards for run 2 (written after run 1; each card says what had been seen)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| vol-target | Volatility targeting | dead (tested) | [card](cards/vol-target.md) | Same Sharpe as equal weight (0.87 vs 0.88); cuts volatility, and on coins halves it at equal growth. A risk dial, not an edge. No help in slow bear markets. [result](results/vol-target.md) |
| ensemble-tsmom | Trend | dead (tested) | [card](cards/ensemble-tsmom.md) | +0.05 over tsmom12 (p = 0.21), right sign in all three other sets, 2x turnover. Indistinguishable from 12-month momentum. [result](results/ensemble-tsmom.md) |
| trend-vol | Trend + volatility | failed bar; paper candidate on drawdown only | [card](cards/trend-vol.md) | Same Sharpe as tsmom12 (1.03 vs 1.05) but worst loss 26% vs 37% (equal weight 69%), growth 13.3% vs 17.8% a year. A risk choice, not an edge. [result](results/trend-vol.md) |

## Cards for run 3

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| trend-to-safe | Trend / regime allocation | testing | [card](cards/trend-to-safe.md) | Out-of-trend slots go to TLT/GLD if those are in trend; twin tsmom12 |
| crypto-slot-size | Allocation | testing | [card](cards/crypto-slot-size.md) | 5% / 10% / 0% per coin against 1/6; descriptive, no out-of-universe set |

## Plain twins and benchmarks (baselines, see `results/baselines.md`)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| sma200 | Trend | baseline | protocol.md | 1994-2025 Sharpe 1.01 vs 0.88 equal weight (p = 0.17); halves drawdowns. M1 lane owns the live version |
| tsmom12 | Trend | baseline | protocol.md | 1.05 vs 0.88 (p = 0.08); the strongest plain rule on the six assets, weaker out of universe |
| inverse-vol | Risk parity, unlevered | baseline | protocol.md | 0.85: no better than equal weight on Sharpe; lower volatility |
| vol-calm | Volatility switch | baseline | protocol.md | 0.74: worse than equal weight. Stepping aside when volatility is high misses the rebounds |

## Not tested: killed or parked by the survey

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| tda-landscape | Topological data analysis | dead (literature) | - | Landscape norm is proportional to variance; the one controlled comparison finds nothing beyond mean correlation (survey part 6, C) |
| transfer-entropy | Information theory | dead (literature) | - | Descriptive only; crypto and ETF bars close at different times, so a daily lead is not tradable at next open (part 6, D) |
| critical-slowing | Ecology (early warning) | dead (literature) | - | Careful tests reject rising autocorrelation before crashes; the surviving part is rising variance = volatility targeting (part 6, F) |
| changepoint-momentum | Change-point detection | dead (literature) | - | Wood, Roberts, Zohren: edge over plain trend gone above about 2 bps a trade (part 4) |
| crypto-daily-reversal | Short-term reversal | dead (literature) | - | Not real in large coins even before our 60 bps round trip (part 3, A) |
| pre-fomc-drift | Calendar | dead (literature) | - | Gone after 2015; window does not fit next-open fills (part 3, E4) |
| ou-optimal-entry | Optimal stopping | dead (literature) | - | Needs a mean-reverting spread; long-only we cannot trade one (part 4) |
| return-forecast-foundation-model | Deep learning | dead (literature) | - | Chronos/TimesFM: negative R-squared against a zero forecast on daily returns (part 5). Do not spend the GPU on raw-return forecasting in M3 |
| llm-trading-agent | LLM | parked | - | Backtests before the model's training cutoff are contaminated; only forward paper scoring counts (part 5). Fits the M3 "research desk" as designed |
| lppls-bubble | Econophysics | parked | - | Three or four crypto bubbles cannot validate a warning signal (part 6, E) |
| hurst-entropy-gate | Econophysics / information theory | parked | - | Time-varying efficiency is documented, exploiting it is not; about five independent readings in ten years (part 6, D-E) |
| signature-leadlag | Path signatures | parked | - | No daily out-of-sample evidence; level 2 is lead-lag areas, which hit the non-synchronous-close problem; level 3+ overfits (part 6, B) |
| halloween | Calendar | parked | - | One observation a year: cannot be confirmed or rejected in our lifetime (part 3, E5) |
| crypto-carry | Carry | parked | - | Real, but needs perpetual futures; the gym has spot only (part 3, C3) |

## New (not yet carded; candidates for the next run)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| ensemble-tsmom | Trend | new | - | Weight = share of 1/3/6/12-month returns that are positive (part 1) |
| turbulence | Statistics | new | - | Mahalanobis distance of the six returns; test only against a volatility trigger (part 4) |
| vol-shift | Volatility | new | - | Risk assets to cash when SPY's 20-day volatility jumps 1 sd above its 1-year norm. Was the plain twin of absorption-ratio and beat equal weight there (1.17 vs 1.04, not significant). Needs its own card |
