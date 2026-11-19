# ls-trend-2 Part B: the 1/3/12-month signal on the wide long-short book

Card: `cards/ls-trend-2.md` Part B (committed before any number). Descriptive, no pick. Signal = mean of the signs of the 1-, 3- and 12-month excess returns (Hurst-Ooi-Pedersen 2017), otherwise ls-trend-1's wide-LS unchanged (40% / sigma / N, monthly, 5 bps, 1% borrow). Raw = leverage at the bill; g1 = rescaled to gross 1. Monthly excess returns over the T-bill; nothing after 2025-10 read.

## 1. Sharpe, cost, correlation

| Cell | Sharpe L | Sharpe L07 | Vol L07 | Mean gross L | Turnover/yr L | Costs/yr L | Borrow/yr L | Corr. TC (L) | Corr. tsmom12 (L) | Corr. wide-LS (L) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wide-LS | 0.15 | 0.21 | 16.5% | 4.27 | 13.4 | 0.67% | 1.83% | 0.61 | 0.08 | 1.00 |
| hop-wide-LS | -0.09 | 0.06 | 13.6% | 2.87 | 28.6 | 1.43% | 1.23% | 0.65 | 0.02 | 0.75 |
| wide-LS-g1 | 0.09 | 0.14 | 4.6% | 1.00 | 2.9 | 0.14% | 0.44% | 0.62 | 0.05 | 0.97 |
| hop-wide-LS-g1 | -0.04 | 0.09 | 5.1% | 1.00 | 10.0 | 0.50% | 0.44% | 0.66 | 0.01 | 0.71 |

(Daily Sharpe, calendar days, 365, on excess returns; the repo's row convention. ls-trend-1's monthly Sharpe for wide-LS was 0.15 in L.)

## 2. Fast crashes (and the slow ones, for the cost of speed)

Compounded monthly excess; at 10% vol = x 10% / the cell's monthly vol in L07 (display scaling, ex post).

| Window | wide-LS | hop-wide-LS | wide-LS-g1 | hop-wide-LS-g1 | wide-LS at 10% | hop-wide-LS at 10% | TC |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2020-02..03 | +24.6% | +35.2% | +5.5% | +8.5% | +15.0% | +25.9% | +3.6% |
| 2018-10..12 | -3.0% | -2.1% | -0.5% | -0.3% | -1.8% | -1.5% | -3.6% |
| 2011-08..09 | -14.1% | -0.4% | -4.2% | -0.3% | -8.6% | -0.3% | -2.9% |
| 2015-08..09 | +3.6% | +0.6% | +1.0% | +0.3% | +2.2% | +0.4% | -0.2% |
| 2008 | +34.9% | +32.7% | +13.9% | +15.7% | +21.2% | +24.1% | +7.1% |
| 2022 | +12.8% | +5.4% | +3.3% | +1.4% | +7.8% | +4.0% | +17.6% |

Card's reading: 2020-02..03 at 10% vol, hop minus 12-month = +11.0 points -> helps in the fast crash (rule: > 2 points); Sharpe L -0.09 vs 0.15 -> costs.

## 3. Where the 2020-02..03 result came from (hop-wide-LS, additive daily P&L)

| Class | Long legs | Short legs | Total |
|---|---:|---:|---:|
| equity | -0.3% | +10.0% | +9.7% |
| bonds | +6.1% | +0.0% | +6.1% |
| commodities | -0.5% | +14.9% | +14.4% |
| currencies | -0.2% | +3.3% | +3.1% |

## 4. 1987 on the S&P 500 alone (price index, no dividends; long-short, 40% / sigma)

| Cell | 1987-10 | 1987-10..12 | Cell's 1987-09 | Sharpe 1961..2025-10 | Position held 1987-10-02..10-30 (x capital) |
|---|---:|---:|---:|---:|---:|
| gspc-12m | -58.1% | -55.8% | -8.6% | 0.22 | +2.58 |
| gspc-hop | -16.5% | -14.1% | -8.6% | 0.21 | +0.86 |

S&P 500 price index: 1987-09 -2.4%, 1987-07..09 +5.9%, 1987-10 -21.8%. The cells size one market at 40% / sigma, so a calm September means about 2-3x leverage; divide by 4 for a 10% volatility reading.

Rows logged this run: 0.
