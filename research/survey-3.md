# Survey 3: `xtsmom`, survey-2's second pick (2026-11-18)

Lane `survey-3` of the night lead (research only, fake money). Task: card and train test of
survey-2's rank 2, cross-asset time-series momentum, with the paper's years and the years after
it shown apart; then, since it failed, a ranked note on survey-2's remaining five candidates (no
new tests). Card `cards/xtsmom.md` (commit 137b21c) and code (067d221) were pushed before any
number. Table `results/xtsmom.md`; 9 rows in `tries.md` (3 variants, 6 robustness). Held-out
year unspent.

## Citation check

Pitkäjärvi, Suominen and Vaittinen, "Cross-asset signals and time series momentum", Journal of
Financial Economics 136(1), 2020, pp. 63-85, DOI 10.1016/j.jfineco.2019.02.011: confirmed
(VU Amsterdam research portal, search summary of the JFE page). Survey-2's citation was right.

- Abstract (paraphrased by the portal): 20 countries; past bond returns predict stock returns
  positively, past stock returns predict bond returns negatively; the diversified cross-asset
  portfolio's Sharpe is about 45% above plain TSMOM; slow-moving capital.
- Sample and rule (CXO Advisory on the December 2016 working paper, `[secondary]`): 1980-01 to
  2015-12, 20 developed countries, monthly stock and 5-year government-bond total-return
  indexes. Stocks long when the stock and bond 12-month returns are both positive, short when
  both negative, flat otherwise; bonds long when bonds up and stocks down. 1-month hold;
  look-backs 1 to 48 months; volatility-scaled; gross; gain "modest" in the US, none in Japan.
- Not confirmed: a search summary says the published sample ends 2016-12. 2016 is therefore
  shown apart, and "after the sample" is 2017-01-01 on.
- Not found (SSRN and Alpha Architect refuse automated reading): any absolute, long-only or
  stock-leg-only Sharpe. The 45% is for a long-short, two-leg, 20-country, volatility-scaled
  portfolio; nothing in the paper as far as I could read it says what the stock gate alone is
  worth to a long-only US book.

## Verdict: fails train, every variant

Bond signal: a 10-year par bond's trailing return from FRED `DGS10` (the paper used 5-year
government bonds), as of the day before; the gate drops a `tsmom12` stock slot while that
return is negative. Twin `tsmom12` (Sharpe 1.05). Family bar p < 0.10 / 61 = 0.00164.

| Variant | Sharpe | vs twin (p) | Eras ahead | Max DD | Since 2017 | Bars failed |
|---|---:|---:|---:|---:|---:|---|
| `xtsmom` (12-month bond) | 1.05 | +0.00 (0.49) | 1 / 5 | 35% vs 37% | -0.06 | 1, 2, 6, 7 |
| `xtsmom-b6` (6-month bond) | 1.02 | -0.03 (0.67) | 2 / 5 | 35% | -0.01 | 1, 2, 4, 6, 7 |
| `xtsmom-full` (+ bond leg) | 1.01 | -0.04 (0.76) | 2 / 5 | 39% | -0.06 | 1, 2, 4, 6 |
| `xtsmom-tlt` (robustness: TLT as bond) | 1.04 | -0.01 (0.59) | 2 / 5 | 35% | -0.04 | - |

**In the paper's years against after them** (Sharpe minus the twin's; the event study is SPY's
mean open-to-open return on its own up-trend days, bond up minus bond down, bps a day):

| Window | `xtsmom` six | ETFs | Indexes | Event study (t) |
|---|---:|---:|---:|---|
| 1962-1979 (before the paper's sample) | - | - | +0.04 | S&P 500 index +3.3 (0.7) |
| 1980-1993 (in sample) | - | - | +0.59 | S&P 500 index +21.5 (2.2) |
| 1994-2015 (in sample) | +0.05 | +0.08 | +0.08 | SPY -0.2 (-0.1) |
| 2016 (maybe in sample) | +0.05 | -0.15 | -0.52 | SPY +0.8 (0.1; 14 bond-down days) |
| 2017-2025/11 (after) | **-0.06** | +0.04 | -0.18 | **SPY +0.4 (0.1)** |

What this says:

- **The effect is in the US data only in the 1980s.** On the S&P 500 index in 1980-1993 the
  days with bonds falling earned 21.5 bps a day less (t 2.2), and the gate added +0.59 Sharpe
  to the index book there. Before the paper's sample (1962-1979) it was small (+3.3, t 0.7);
  in our book's years it is nothing: 1994-2015 -0.2 bps (still in the paper's sample), after
  2016 +0.4 (t 0.1). The paper's US result rests on years this book never traded.
- **What the gate does in our book is cut exposure, not pick better days.** Average exposure
  62% against 76%: the dot-com bust -17% against -28%, the 2022 rate shock -8% against -13%,
  but less return elsewhere; the Sharpe ends level (+0.002). That trade is the one every
  "leave early" macro gate here has made (`credit-spread`, `yield-curve`, `real-rate`,
  `fed-hiking`, `hedge-regime`): the sixth of its kind, the same result.
- **After the sample it loses**, as foreseen on the card: bonds fell in 2021-2024 while US
  stocks rose; the primary trails the twin by 0.06 Sharpe since 2017.
- The paper's bond leg (`xtsmom-full`: TLT only while stocks trend down) costs Sharpe and adds
  2.5 points of drawdown: in this period bonds and stocks mostly rose together, so it dropped
  TLT through most bond rallies.
- 2016 looks large in the window table (+0.25 for `xtsmom-full`, -0.52 on the indexes) but is
  one year with 14 bond-down SPY up-trend days; it is noise either way.

Compared with my guess on the card: primary -0.05 to +0.03 on full train (got +0.00), -0.02 to
-0.10 since 2017 (got -0.06), bond-down up-trend days after 2016 about equal (got +4.5 against
+5.0 bps), `xtsmom-full` worse than the primary (it is). Chance of a pass was 3%.

### Disclosures

- A plumbing run (`DRY=1`: last 120 days for the backtests, nothing logged) printed the event
  study on the full history before the logged run. Its output was checked only for its section
  headings and for errors (`grep`), not read. Nothing was changed after it; the logged run is
  the code of commit 067d221.
- No look-ahead: the runner first checks that all three variants (and the ETF bond leg) give
  the same weights as `gym.backtest` on four sample Fridays (1999-10-01, 2008-10-10,
  2018-12-21, 2023-06-02); it passed. The yield for day x is used from x + 1; tests in
  `tests/test_survey3.py` cover the bond return, the trailing window and the as-of rule.
- The index and ETF sets use the US 10-year yield for every country (the paper used each
  country's own bonds); noted on the card.
- The `DGS10` snapshot read is the cached FRED file of 2026-11-13, cut at 2025-11-10.

## The remaining five survey-2 candidates (ranked note, no new tests)

Written after `fomc-cycle` and `xtsmom` both failed. Both were published effects that held in
their papers' own years and not in the years after (or, for `xtsmom` in the US, not even in the
later in-sample years). Two lessons for the rest of the list: (1) a candidate is only worth a
test here if part of our train lies after its sample, or it gets no honest train test at all;
(2) idle cash into stocks (`opex-pin`, `even-overlay`) and gates that leave stocks early are
now 0 for 8 in this book.

| Rank | Candidate | Was | Now | Why |
|---:|---|---:|---:|---|
| 1 | `announcement-premium` (S2): idle cash into stocks on FOMC, CPI and payroll days | 2% | 1% | Still deserves a card, but as an event study first: FOMC-day returns can be read from the calendar survey-2 already parsed (free), 2017-2025 is after the classic papers (Savor and Wilson 2013; Lucca and Moench 2015; from memory, not opened in this lane). Against: the Management Science 2025 paper says the premium is small; idle cash into stocks failed twice; CPI and payroll days need 30 years of BLS dates and a fill a day early |
| 2 | `fomc-bond-drift` (S3): idle cash into TLT around FOMC days | 2% | <1% (forward only) | Its sample runs to the 2020s, so every year of our train is in sample: no honest train test exists. Half of it is the 1989-2020 fall in yields, which reversed in 2021-2024. Worth at most a forward descriptive check after the held-out year, not a card now |
| 3 | `turning-points` (S6): state-dependent slow/fast blend | 1% | dead | The paper's own gain is 0.52 against 0.51 gross; `ensemble-tsmom` (a static blend) already tied `tsmom12` here, and fast trend loses after costs |
| 4 | `nonlinear-tsmom` (S7): ML on past returns | 1% | dead | Seven ML cards here, pooled over 33 markets, gave AUC 0.50; the source is an unverified search summary of an SSRN paper |
| 5 | `crypto-corr` (S12): BTC timed by its correlation with stocks | <1% | dead | A daily horizon against 60 bps a round trip; out-of-sample R-squared 2% |

## Count after this lane

Family (`wide-*` lineage): 61 mechanisms, 14 tested, none passed. Survey-2's list is spent:
one live candidate (`announcement-premium`, event study first), one forward-only
(`fomc-bond-drift`), three dead. The next test is read at p < 0.10 / 61 = 0.00164, or lower if
a further list is added.
