## Follow-up: `where-vol` on ten US industries, 1926-1961

French cache snapshot `french/2026-11-12`; decisions 1927-07-02 to 1961-12-28; ten industries as one equal-slot book; 2 bps a side; cash earns 0. Twin: always-on `tsmom12`. Benchmark: equal weight.

| Variant | Sharpe | Against `tsmom12` (p; 90% range) | Growth/yr | Worst loss | Trades a year | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|
| where-vol@F-ind10 | 1.07 | +0.00 (p=1.00; +0.00..+0.00) | +12.6% | 32.5% | 1.3 | 70% |
| tsmom12@F-ind10 | 1.07 | - | +12.6% | 32.5% | 1.3 | 70% |
| equal-weight@F-ind10 | 0.62 | -0.45 (p=1.00; -0.72..-0.19) | +10.6% | 81.9% | 0.1 | 100% |

Worst loss inside each window:

| Window | where-vol@F-ind10 | tsmom12@F-ind10 | equal-weight@F-ind10 |
|---|---:|---:|---:|
| whole period | 32.5% | 32.5% | 81.9% |
| 1929-09-03 to 1932-07-08 | 29.3% | 29.3% | 81.9% |
| 1937-03-10 to 1938-03-31 | 19.4% | 19.4% | 47.2% |

Answers (yes = keep the filter), shown when one changed:

| Refit | NoDur | Durbl | Manuf | Enrgy | HiTec | Telcm | Shops | Hlth | Utils | Other |
|---|---|---|---|---|---|---|---|---|---|---|
| 1927 | yes | yes | yes | yes | yes | yes | yes | yes | yes | yes |

Industry-years answered no: 0 of 340 (refits 1928 to 1961).

What the last refit saw:

| Industry | Out bars | In bars | Volatility out | Volatility in | Keep filter |
|---|---:|---:|---:|---:|---|
| NoDur | 2861 | 6682 | 19.1% | 11.1% | yes |
| Durbl | 3260 | 6283 | 37.3% | 22.7% | yes |
| Manuf | 3174 | 6369 | 28.8% | 18.1% | yes |
| Enrgy | 3299 | 6244 | 24.2% | 18.2% | yes |
| HiTec | 2649 | 6894 | 35.3% | 20.5% | yes |
| Telcm | 2393 | 7150 | 20.6% | 12.4% | yes |
| Shops | 2863 | 6680 | 25.7% | 14.2% | yes |
| Hlth | 2983 | 6560 | 25.2% | 14.2% | yes |
| Utils | 2989 | 6554 | 30.6% | 17.1% | yes |
| Other | 3503 | 6040 | 28.0% | 17.1% | yes |
