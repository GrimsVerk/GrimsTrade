# Ideas

One line per idea. Status: `new` (written down), `testing` (has a card, being tested),
`live` (forward paper), `dead` (and why), `parked` (not testable here yet, and why). Dead ideas
stay: they count as tries. "Dead (literature)" means the survey killed it and we did not spend a
backtest on it; "dead (tested)" means our own test killed it (see `results/`).

## Cards (tested in this run, strongest first)

| Idea | Field | Status | Card | Note |
|---|---|---|---|---|
| kelly-shrunk | Kelly / information theory | dead (tested) | [card](cards/kelly-shrunk.md) | Equals inverse-vol (+0.01 Sharpe): the no-leverage cap removes the Kelly scale. On high-volatility coins the scale halves drawdown at equal growth: see `vol-target-crypto`. [result](results/kelly-shrunk.md) |
| hmm-regime | Regime models | testing | [card](cards/hmm-regime.md) | Two-state HMM risk switch; twins vol-calm, sma200 |
| fracdiff-momentum | Fractional differentiation | dead (tested) | [card](cards/fracdiff-momentum.md) | Worse than 12-month momentum everywhere (-0.25 Sharpe, 3x turnover): it is a fast trend rule. [result](results/fracdiff-momentum.md) |
| drawdown-control | Optimal stopping / control | dead (tested) | [card](cards/drawdown-control.md) | Same as the 200-day switch (+0.07, p = 0.14; mixed out of universe). A smoother trend rule, not a better one. [result](results/drawdown-control.md) |
| universal-portfolio | Information theory | dead (tested) | [card](cards/universal-portfolio.md) | Indistinguishable from the constant mix it starts from; 30 years is too short for its guarantee. [result](results/universal-portfolio.md) |
| absorption-ratio | Random matrix theory / PCA | testing | [card](cards/absorption-ratio.md) | Kritzman et al. 2011, post-publication test; twin vol-shift |
| hawkes-clustering | Hawkes processes | testing | [card](cards/hawkes-clustering.md) | Crash-day intensity; twin vol-calm |
| month-end-liquidity | Calendar / microstructure | testing | [card](cards/month-end-liquidity.md) | Etula et al. 2020, post-sample test |
| dip-rsi2 | Short-term reversal | testing | [card](cards/dip-rsi2.md) | Connors 2008, post-publication test, next-open fills |

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
| vol-target-crypto | Volatility targeting | new | - | BTC/ETH weight = min(1, 40% / 20-day vol), trade only on 10-point moves (part 2). Supported by the kelly-shrunk coin result (same growth, half the drawdown). Overlaps the M1 lane's volatility targeting |
| ensemble-tsmom | Trend | new | - | Weight = share of 1/3/6/12-month returns that are positive (part 1) |
| hmm-switch-to-bonds | Regime models | new | - | Risk-off into TLT/GLD instead of cash, as in Shu, Yu, Mulvey 2024 (part 4) |
| turbulence | Statistics | new | - | Mahalanobis distance of the six returns; test only against a volatility trigger (part 4) |
| fixed-btc-sleeve | Allocation | new | - | 5% BTC in an SPY/GLD/TLT core, rebalanced quarterly versus never (part 2) |
