# breadth-anatomy-1: why does a broader `tsmom12` book have a lower Sharpe?

Research lane `breadth-anatomy-1`, 2026-11-25. Card [`cards/breadth-anatomy-1.md`](cards/breadth-anatomy-1.md)
(6eee6b7, pushed before any number), script `lib/banat1.py` + `lib/banat1_core.py`, tests
`tests/test_banat1.py` (040c4e2, pushed before the run). Tables:
[`results/breadth-anatomy-1.md`](results/breadth-anatomy-1.md). Descriptive only: no new rule,
nothing selected, no candidate book. Train only, decisions 2008-01-02 .. 2025-10-31, no bar
after 2025-10-31. Same bars, rule and universes as `breadth-book-1` (#143).

## In plain words

**Breadth fails here because the added markets have a low trend Sharpe, about a quarter of the
six's, not because they co-move with it.** Theory says an added market helps only if its Sharpe
beats its correlation with the book times the book's Sharpe. The six's book scores 1.19, so
even at a correlation of 0.38 an added book needs about 0.45. The 29 added ETFs score 0.29 as
a book, and their sleeves average 0.17 (the six's: 0.65). So any weight on them lowers the
Sharpe (best weight: 0). Equal weight puts 83% of the book on them. About two thirds of
`L-all`'s fall is the coin share shrinking, one third is the ETFs.

## The split (Sharpe above bills, 2008-01 .. 2025-10)

Step 0 reproduces `breadth-book-1` on this window: `six` 1.19, `L-12` 0.97, `L-20` 0.84,
`L-all` 0.65, `four` 0.82, `E-all` 0.37.

**(a) Coin share.** `K` books keep the coins at the six's weight (mean 0.147, 83-88% of the
variance) and spread the six's ETF budget over the set's ETFs:

| k | SR(L) - SR(six) | ETF breadth, coins fixed (K - six) | Coin dilution (L - K) | Coin share of the gap |
|---|---|---|---|---:|
| 12 | -0.23 (SE 0.09) | -0.17 (0.05, z -3.2) | -0.06 (0.07) | 26% |
| 20 | -0.36 (0.15) | -0.17 (0.06, z -2.6) | -0.19 (0.12) | 54% |
| all (35) | -0.54 (0.19) | -0.17 (0.07, z -2.6) | -0.37 (0.17, z -2.2) | 68% |

With the coins left out of both sides, the ETF loss is the same at every size: `four` 0.82
against `four` + 6 / 14 / 29 added ETFs 0.38 / 0.36 / 0.37 (z -2.7 to -3.2). The ETF part
is all there from the first 6 added ETFs onward. The growing part of the gap is coin dilution.

**(b) The added markets' own `tsmom12` Sharpe.** Mean sleeve Sharpe: six 0.65 (BTC 1.28,
ETH 0.81, QQQ 0.72, SPY 0.55, GLD 0.36, TLT 0.16); added A-6 -0.04, A-14 0.10, A-29 0.17. By
class (A-29): currencies -0.31, international equity 0.04, commodities 0.06, US equity 0.33,
bonds 0.41. Buy-and-hold on the same days scores 0.26 on average for the added ETFs, so the
trend filter took about 0.09 off them; on the six it took 0.03. As books: `A-6` -0.10,
`A-14` 0.18, `A-29` 0.29.

**(c) Correlation.** Weekly above-bill sleeve returns: mean pairwise correlation 0.14 within the
six, 0.31 within A-29, 0.20 between them. The A-29 book's correlation with the six's book is
0.42; daily it is 0.38. The effective number of bets on sleeves goes from 4.0 (six) to only 5.8 (35). In
market crises (2008, covid, 2022 rates; 110 weeks) the co-movement rises: within the six
0.39 (0.10 otherwise), A-29 book vs six book 0.66 (0.37 otherwise). Within A-29 it does not
(0.28 vs 0.33). The two-book test:

| Ref | Added | SR_ref | SR_A | rho | rho x SR_ref | SR_A - rho x SR_ref | best weight on A |
|---|---|---:|---:|---:|---:|---:|---:|
| `six` | `A-6` | 1.19 | -0.10 | 0.27 | 0.32 | -0.42 | 0 |
| `six` | `A-14` | 1.19 | 0.18 | 0.33 | 0.39 | -0.21 | 0 |
| `six` | `A-29` | 1.19 | 0.29 | 0.38 | 0.45 | -0.16 | 0 |
| `four` | `A-29` | 0.82 | 0.29 | 0.73 | 0.59 | -0.31 | 0 |

The static mix at the L weights tracks the real books (`L-all` 0.65 and 0.65, `L-12` 1.01 and
0.97). By the card's reading this is **"low Sharpe"** against the six (SR_A 0.29 < 0.5 x 1.19,
rho 0.38 < 0.5). Against the coin-free four it is **both**: rho 0.73 and SR_A 0.29 < 0.41.
Per sleeve, 8 of 29 pass the test against the six (SHY, IEF, LQD, SLV, XLY, XLP, XLK, XLV)
and 4 against the four. That list is hindsight, not a pick.

**(d) Equal weight vs risk weight.** Inverse-vol weighting (the live runner's EWMA vol) is
**not** the fix; it widens the gap. `six-rw` 1.20, `L-12-rw` 0.51, `L-20-rw` 0.48, `L-all-rw`
0.39 (gap -0.81, z -4.5; equal weight -0.54). `E-all-rw` 0.36 vs `four-rw` 0.86 (-0.49). Inverse vol
gives the quietest sleeves most of the book: SHY's vol is 1.3%, the currency trusts' about
5%. It also cuts the coins to under 1% of an `L` book (4.1% of `six-rw`). By the card's reading,
weighting is no explanation.

**(e) Period (one row).** `L-all` - `six`: -0.19 in 2008-2009 (all books negative: six -0.13,
`L-all` -0.32), -0.54 in 2010-2025-10 (six 1.29, `L-all` 0.74, `A-29` 0.35, `K-all` 1.11).
The gap is not confined to the post-2009 drought. Lane `tick-tier-1` studies the break by
asset class.

## Answer

1. The six's 1.19 rests on high-Sharpe sleeves: the coins (83% of the variance) plus a
   hindsight-picked four (sleeve mean 0.45).
2. The mechanically added ETFs have a trend Sharpe near 0.1-0.3, against a required
   rho x 1.19 of about 0.3-0.45. They fail the marginal test, so the best weight on them is
   zero, and equal weighting gives them 50-83% of the book.
3. Correlation is a secondary factor. It is moderate on average and higher in crises (the
   A-29 book vs the six's: 0.66). Within the added set it is 0.31, so 29 sleeves give fewer
   than 2 extra effective bets.
4. Neither risk weighting nor the period explains the fall.

Breadth theory is not refuted: its condition (added sleeves with a positive Sharpe that is
high relative to their correlation with the book) does not hold for this pool.

## Caveats

- In-sample: the marginal test, w* and the per-sleeve pass list use full-period Sharpes and
  correlations. They describe 2008-2025. They are no rule for choosing markets.
- The `K` and `rw` books are counterfactuals made for the split. They were not tuned and are
  not candidates. The static-mix blend approximates the gym book (error <= 0.04 here).
- SEs are bootstrap SEs of single differences. Nothing is corrected for multiple looks,
  because nothing is selected.
- The pool and survivorship caveats of `breadth-book-1` carry over unchanged.

## Disclosures

- Window ends 2025-10-31 (the lane rule), 9 days before `breadth-book-1`'s. The headline
  numbers move by at most 0.01.
- Two crashes before any number was printed: `python -I` does not put `research/lib` on the
  path, so the script runs without `-I`, and a coin sleeve's view was empty before its first
  bar, which now means cash.
- After the first full output, one reporting bug was fixed and the script rerun
  (deterministic). The coins' variance share of the `K` books had used the slot 1/N instead
  of the six's slot (0.43 / 0.25 / 0.14, now 0.88 / 0.87 / 0.83). No other number changed (diff
  checked).

**Logged:** one `tries.md` row, kind `note`, "re-score (not a try)", as `gap-2002-1` and
`e4-anatomy-1`. No ledger rows, the bar count is unchanged.

Reproduce: `uv run python research/lib/banat1.py run` (needs `breadth-book-1`'s research cache
in `research/data/{bars,adj}` and `research/macro.local.json`).
