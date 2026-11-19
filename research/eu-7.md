# eu-7: keep trend's crash insurance, lose less of the rest?

Lane `eu-7` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-7` from `eu-6`. Card `cards/eu-7.md` (pushed before any number). Code `lib/eu7.py`
(`check`, then `run`; reuses `eu6.py`); table `results/eu-7.md`; 24 rows in `tries.md` (idea
`eu-7`). eu family now 12 (bar p < 0.0083). Held-out year unspent.

## 1. What was tried

eu-6 found that on the seven `euw` funds (2012-2025, 5/25 band) trend (T, `tsmom12`) is crash
insurance, not a better investment. Two rules were written down before any number, to keep the
insurance and give up less of the rest:

- **A, trend on the stock funds only**: the three stock funds get the trend filter; euro bonds
  (short and long), gold and commodities are held at 1/7 always (trend-tune found the filter
  paid on Sharpe only on stocks).
- **B, hold the seven with a fixed cash share**: all seven at 67/7% each, 33% in cash at 0. The
  67% is T's average exposure on the train years, from T's positions (not its returns).

Same metrics, crash windows (incl. 2000-02 and 2008 via US proxies), band and fee tiers as eu-6.

## 2. Results (no fixed fee unless stated)

| | T trend | A trend on stocks | B hold7 + 33% cash | H hold7 |
|---|---:|---:|---:|---:|
| Sharpe (SE 0.27 each) | 0.62 | 0.60 | **0.79** | 0.78 |
| Yearly return / vol | +3.7% / 6.1% | +4.0% / 6.9% | +4.5% / 5.8% | +6.3% / 8.3% |
| Worst loss (max DD) | **13.6%** | 16.1% | **13.8%** | 19.8% |
| Longest under water | 58 mo | 56 mo | **31 mo** | **31 mo** |
| Worst 12 months | -11.5% | -13.1% | **-8.3%** | -11.4% |
| Orders a year | 21.1 | 10.1 | 2.3 | **1.9** |
| 2000-02 (US monthly proxy) | +8.8% | **+12.7%** | -0.7% | -1.2% |
| 2008 (US proxy, USD) | **-0.7%** | **-0.8%** | -15.7% | -23.1% |
| 2015-16 / 2018-Q4 | **-8.2%** / -4.2% | -11.2% / **-1.7%** | -10.0% / -2.5% | -13.8% / -3.4% |
| 2020 covid / 2022 rate shock | **-12.2%** / **+1.7%** | -14.5% / -3.8% | -13.0% / -4.3% | -18.7% / -6.7% |
| Worst loss on the US proxy 2007-2025 (with 2008) | **10.9%** | 14.1% | 22.1% | 32.0% |

- **Neither rule keeps the insurance (the card's test).** A is within 3 points of T in 4 of 6
  crash windows (5 needed) and its worst loss is 2.4 points worse (2 allowed); B is within 3
  points in 3 of 6. So neither earns a held-out-year card; the held-out year stays unspent.
- **A keeps the stock-crash insurance, loses the bond-crash insurance.** In the stock bear
  markets A matched or beat T (2000-02 +12.7%, 2008 -0.8%), but in 2022, when euro long bonds
  fell, A held them and lost 3.8% where T made 1.7%. Trend's 2022 protection came from the bond
  slots, which trend-tune's "pays only on stocks" (a Sharpe finding on US data) did not cover.
  A halves T's orders (10 vs 21 a year) at the same Sharpe (A - T -0.02, SE 0.08), but it wins
  no investor preference.
- **B matches T's worst loss in these 14 years, but not in a 2008-type crash.** On the euro book
  B's worst loss (13.8%) equals T's at H's Sharpe, with the shortest waits and the best worst 12
  months, at ~2 orders a year. But it simply holds less of everything: in 2008 it lost 15.7%
  (T -0.7%), and on the US proxy that includes 2008 its worst loss is 22% vs T's 11%. Its euro
  worst loss is a fact of a window without a sharp all-asset crash.
- **Sharpe gaps are noise.** B - T +0.17 (SE 0.13, p 0.10), B - H +0.01, A - T -0.02, A - H
  -0.18 (p 0.03); none passes p < 0.0083. B's Sharpe is H's by construction (cash at 0 scales
  return and risk alike).

## 3. Which fits which investor (card's rules, among T, A, B, H)

| Preference | Winner | Worth it at EUR 5-25k, EUR 1-3 per order? |
|---|---|---|
| P1 best Sharpe after fees | H (B ties, more orders) | yes, every cell |
| P2 smallest worst loss (in 2012-2025) | **B** (13.8%, ties T's 13.6%, better worst 12 months) | yes, every cell |
| P3 shortest time under water | H (B ties) | yes, every cell |
| P4 crash insurance | T (best in 4 of 6 windows; A 3, B 2, H 0) | yes from EUR 5k at EUR 1, from 10k at EUR 2-3 (eu-6) |
| P5 cheapest | H | yes |

## 4. The plain answer (one screen)

**You cannot keep trend's crash insurance by applying it in fewer places: the insurance is the
part that costs.**

- **If you mainly fear a big fall in the next few years** but can live with smaller dips: hold
  the seven funds with about a third in cash (rule B). In 2012-2025 its worst loss (14%) was as
  small as trend's, at the Sharpe of full holding, with the shortest waits under water (31
  months vs 58) and 2 orders a year. Know its limit: it is not insurance, just less exposure. In
  a 2008-type crash it would still lose about two thirds of what full holding loses (-16% vs
  -23%; trend about 0%).
- **If you want insurance against a sharp crash in any asset** (stocks in 2008, bonds in 2022):
  only full trend (T) does that, at 21 orders a year, a lower long-run return and long flat
  stretches, and only for a book of EUR 5k+ at EUR 1 per order or 10k+ at EUR 2-3 (eu-6).
- **Trend on stocks only (A)** halves trend's orders and kept the stock-crash protection (2000-02,
  2008), but held the long euro bonds through 2022 and had the deepest fall of the trend rules
  (16%). It is the best of neither world; no preference picks it.
- **If you care about the long-run result, waiting or cost**: hold the seven funds (H).
- **Honest uncertainty**: every Sharpe gap is about one standard error (SE 0.08-0.13 for the
  pairs); the data cannot rank these rules on Sharpe. B's case rests on cash earning 0 here; any
  cash interest helps B (and T) and was not modelled.
- **Held-out year**: nothing passed the card's test, so nothing is worth spending it on now.

## Rows counted

24 rows (idea `eu-7`): A and B on `euw` at no fee and 3 tiers x 3 books (20 `variant`), on
`usw` from 2007-03-01 (2 `robustness`), on the long monthly proxy (2 `robustness`, marked
`long-monthly`). T, H and M are eu-5's / eu-6's saved runs, re-scored without new rows. A and B
are selectable rules for this book: the eu family is now 12 (bar p < 0.10 / 12 = 0.0083); no
Sharpe lead passed it.
