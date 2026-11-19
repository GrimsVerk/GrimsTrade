# halving: the window moved six months either way

Script `lib/halving_shift.py`, run after the card was judged. Months after the last
halving during which coins are out; `m18-30` is the card's window.

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| halving-and-m12-24 | 1.12 (0.18) | +16.8% | 14.8% | 28.9% | 2.5 | 73% | 1.34 | 0.19 | 1.92 | 1.49 | 1.09 | +0.08 (p=0.21; -0.08..+0.24) | 2/5 |
| halving-and-m18-30 | 1.20 (0.18) | +19.9% | 16.2% | 28.9% | 2.7 | 74% | 1.34 | 0.19 | 1.67 | 1.94 | 1.11 | +0.15 (p=0.00; +0.06..+0.25) | 3/5 |
| halving-and-m24-36 | 1.05 (0.18) | +17.8% | 17.0% | 39.0% | 2.7 | 75% | 1.34 | 0.19 | 1.57 | 1.49 | 0.88 | +0.00 (p=0.49; -0.03..+0.04) | 2/5 |

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| halving-and-m12-24 | -28% | -4% | -22% | -7% | +11% | -5% | -6% |
| halving-and-m18-30 | -28% | -4% | -22% | -8% | +4% | +3% | -7% |
| halving-and-m24-36 | -28% | -4% | -22% | -13% | -6% | -19% | -20% |

## Reading (2026-11-13)

Six months later gives nothing (the trend rule is already out by then); six months earlier gives half the gain, not significant. The card's result needs the folklore's exact window, which is what a rule fitted to three cycles looks like.
