# diversifier-1: a held merger-arb slot next to `tsmom12` (verdict)

Card `cards/diversifier-1.md` (2edebd5, before numbers), script d3c13b5, one run (b1c0025):
`results/diversifier-1.md`. Post-hoc re-score above T-bills (off-card, no new try):
`results/diversifier-1-posthoc.md`. Book: 6/7 x `tsmom12` + 1/7 MERFX always held, train
1994-2025, gym costs. Tries: `merfx7` (variant, a pick) and `mna7@mna` (robustness).

| 1994-2025 | `tsmom12` | `merfx7` | 6/7 x `tsmom12` (arithmetic, ~cash slot) |
|---|---:|---:|---:|
| Sharpe (gym: cash 0, vs 0) | 1.05 | 1.09 (+0.041, SE 0.008, z 4.86) | 1.05 |
| Sharpe above T-bills (cash earns bills) | 0.93 | 0.95 (+0.018, SE 0.008, z 2.23, p 0.012) | 0.93 |
| CAGR (gym) | +17.8% | +16.1% | - |
| Max drawdown | 36.5% | 30.8% | ~31.3% |
| Worst year (2000) | -24.2% | -18.7% | ~-20.7% |
| 2008 crisis / covid crash / 2022 shock | -3.5% / -21.8% / -13.5% | -3.7% / -19.3% / -11.5% | ~-3.0% / -18.7% / -11.6% |
| Longest under water | 2,227 d | 2,109 d | - |

MNA (the ETF), 2010-11..2025: gym +0.019 (z 1.6), above bills +0.008 (z 0.65); max DD 36.5% ->
31.5%, covid -21.8% -> -19.9%, 2022 shock -13.5% -> -11.9%. Weekly correlation with SPY +0.48
(MERFX) and +0.50 (MNA); with `tsmom12` +0.13 / +0.21.

## Verdict

1. **Risk: "preferred on risk" by the card's rule** (smaller max DD, better in 2 of 3 crash
   windows, shorter time under water), for MERFX and MNA alike. But the third column shows
   why: almost all of it is **holding 1/7 less of the risky book**. Merger arb did no better
   than cash in the crashes (2008 -3.7% vs ~-3.0% for a cash slot; covid -19.3% vs ~-18.7%).
   It is not a crash hedge here (stock correlation about 0.5 in weekly data). A preference,
   not an edge, and a 1/7 T-bill slot buys nearly the same drawdown cut without the fee.
2. **Sharpe: no edge.** On the card's measure `merfx7` passes the family bar (p < 0.001, 5/5
   eras, smaller DD, beats equal weight; out-of-universe n/a, so not a train pass) and
   nominally clears the project z (4.86 >= 4.65; bootstrap p resolution 5e-4). The post-hoc
   check shows this is mostly the gym's cash-earns-0 convention: an always-held low-vol fund
   earning about bills beats idle cash. Above T-bills the gain is **+0.018, z 2.2**: fails the
   project bar (z 4.65; Bonferroni p <= 1.2e-4, z 3.68). MNA, the buyable ETF: z 0.65.
3. Count: 1 pick (`merfx7`) + 1 robustness row. Nothing passes; nothing goes to the paper book.

Disclosures: the card's stated time (23:20 UTC) is a slip; its commit is 23:16, the run 23:18.
The post-hoc script ran once before its commit (a lint fix blocked the commit; content
unchanged). The 6/7 column is arithmetic on the logged returns' window totals, not a run.

Lesson for later cards: score any always-held diversifier **above T-bills from the card**, and
compare it with a T-bill slot of the same size; at cash 0 any bond-like slot looks like skill.
