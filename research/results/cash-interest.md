# What if cash earned the Treasury-bill rate?

Six live assets, train period, total-return prices. Left: the gym as it is (cash earns 0, Sharpe against 0). Right: cash earns the 13-week T-bill yield and Sharpe is measured above that yield. Average T-bill yield over the period: 2.4%.

| Variant | Avg cash share | Sharpe (gym) | CAGR (gym) | Sharpe above T-bills | CAGR with interest | Lead over equal weight: gym | above T-bills |
|---|---:|---:|---:|---:|---:|---:|---:|
| equal-weight | 0% | 0.88 | +18.2% | 0.77 | +18.2% | +0.00 | +0.00 |
| tsmom12 | 24% | 1.05 | +17.8% | 0.93 | +18.4% | +0.17 | +0.16 |
| sma200 | 30% | 1.01 | +15.9% | 0.90 | +16.6% | +0.13 | +0.13 |
| ensemble-tsmom | 32% | 1.10 | +16.1% | 0.98 | +16.9% | +0.22 | +0.21 |
| trend-vol | 28% | 1.03 | +13.3% | 0.89 | +13.8% | +0.15 | +0.12 |

- Sharpe above T-bills, 1994-99: equal-weight 1.05, tsmom12 1.05, sma200 0.84, ensemble-tsmom 0.99, trend-vol 1.05
- Sharpe above T-bills, 2000-09: equal-weight -0.10, tsmom12 0.04, sma200 -0.01, ensemble-tsmom 0.01, trend-vol 0.08
- Sharpe above T-bills, 2010-16: equal-weight 1.66, tsmom12 1.54, sma200 1.58, ensemble-tsmom 1.60, trend-vol 1.62
- Sharpe above T-bills, 2017-21: equal-weight 1.51, tsmom12 1.47, sma200 1.50, ensemble-tsmom 1.63, trend-vol 1.44
- Sharpe above T-bills, 2022-25: equal-weight 0.51, tsmom12 0.73, sma200 0.57, ensemble-tsmom 0.70, trend-vol 0.78

## Reading (2026-11-12)

Smaller than expected, and it corrects something this run assumed. Paying T-bill interest on idle
cash adds 0.5-0.8% a year to the rules that hold a quarter to a third of the book in cash (12-month
trend goes from +17.8% to +18.4% a year, just above equal weight's +18.2%). It does not change
the ranking or the size of anyone's lead: 12-month trend is +0.17 Sharpe ahead of equal weight in
the gym and +0.16 measured above T-bills. The reason is that measuring above T-bills costs a
low-volatility rule about as much Sharpe as its cash interest gives back.

So the gym's "cash earns 0" rule understates the growth of cautious rules a little and is not a
reason any idea in this run failed. The request to the M1 lane stays (it is the truthful
accounting, and it will matter more if rates rise), but it is a small correction, not a distortion
of the scoreboard. Dividends are the large one.
