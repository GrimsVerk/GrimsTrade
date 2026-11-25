# asset-ledger-1: what trend-timing buys and costs, per live asset

Lane `asset-ledger-1` (DEEPER, descriptive), 2026-11-25 night (UTC). Card:
[`cards/asset-ledger-1.md`](cards/asset-ledger-1.md), pushed before any number. Code:
`lib/assetledger1.py` (tests `tests/test_assetledger1.py`). Tables:
[`results/asset-ledger-1.md`](results/asset-ledger-1.md). Research only, fake money, data
already in the cache (no download), nothing after 2025-10-31. **No new rule, no tuning, nothing
selectable. No rule change is proposed or tested here.**

## Question

The live rule `tsmom12` times six assets. Merged records give pieces: the exit has crash-warning
skill on US stocks and none on gold, bonds or coins (#182); the calm drag on TLT and GLD is
mostly the premium of long time out (#203); fall gain against buy-back was measured on US series
since 2002 (#162). This lane puts the pieces into one ledger per asset: (a) fall gain I (log
points a year avoided in 25%+ falls), (b) late buy-back cost B (the year after each low), (c)
calm drag C with calm-drag-1's split, (d) the net N = I + B + C against holding the asset, and
(e) each asset's share of the six-asset book's worst drawdown with and without timing.

**Not already done (checked first):** gap-2002-1 has I/B/C only for US series since 2002;
calm-drag-1 has only C; rev-costloss-1 scores warnings, not log points; risk-menu has book
drawdowns but no per-asset split. So this table did not exist.

## The ledger (one table)

`tsmom12` minus holding the asset, log points a year, cash 0 (the gym's convention) unless
marked. Falls: 25% / 25% zigzag on the asset's own total-return index (gap-2002-1's labels).
Book shares: the gym's six-asset books, cash 0: `equal-weight` (the same equal slots, always
held: the book without timing) and `tsmom12`, each over its own worst drawdown, 1994-2025.

| Asset | Series | Window | 25% falls | Fall gain I | Buy-back B | Calm drag C (premium P) | **Net N** | Net, cash at bills | Share of book's worst drawdown, without / with timing |
|---|---|---|---:|---:|---:|---|---:|---:|---|
| SPY | SPY | 1994-2025 | 3 | +4.15 | -3.22 | -1.51 (-0.77) | **-0.57** | -0.20 | 26% / 4% |
| | SPY | 2002-2025 | 3 | +4.85 | -4.29 | -1.94 (-0.86) | **-1.38** | -1.07 | |
| | French US market | 1927-2025 | 21 | +7.03 | -5.78 | -1.35 (-0.91) | **-0.10** | +0.66 | |
| | S&P 500 TR | 1986-2025 | 4 | +3.39 | -3.11 | -1.12 (-0.76) | **-0.84** | -0.34 | |
| QQQ | QQQ | 2000-2025 | 8 | +12.06 | -8.92 | -2.08 (-0.40) | **+1.06** | +1.52 | 74% / 0% |
| | QQQ | 2002-2025 | 4 | +5.88 | -5.13 | -2.24 (-0.42) | **-1.48** | -1.17 | |
| | French HiTec (loose proxy) | 1927-2025 | 32 | +10.25 | -9.26 | -1.39 (-0.73) | **-0.40** | +0.46 | |
| TLT | TLT | 2003-2025 | 2 | +1.96 | -1.16 | -2.28 (-1.68) | **-1.48** | -0.70 | 0% / -8% |
| | 30-year Treasury rebuild | 1978-2025 | 4 | +1.66 | -1.54 | -2.24 (-1.92) | **-2.12** | -0.67 | |
| GLD | GLD | 2005-2025 | 2 | +1.64 | -2.53 | -1.43 (-2.45) | **-2.33** | -2.09 | 0% / -3% |
| | Gold, monthly averages (flagged) | 1972-2025 | 5 | +3.08 | -1.89 | -0.96 (-1.75) | **+0.22** | - | |
| BTC | BTC | 2013-2025 | 33 | +26.93 | -30.64 | +0.00 | **-3.72** | -3.29 | 0% / 34% |
| ETH | ETH | 2017-2025 | 23 | +63.60 | -67.16 | +0.00 | **-3.55** | -2.53 | 0% / 73% |

The book shares: without timing the worst drawdown is 2000-03-24 .. 2002-10-09 (68.8%), when
the book held only SPY and QQQ; with timing it is 2018-01-13 .. 2020-03-12 (37.4%), the coins
carrying 107% of it and TLT and GLD offsetting 11% (shares sum to 100%; a negative share is a
gain in the drawdown). Since 2002 (results table B) the book without timing has its worst
drawdown in 2018-01 .. 2018-12 (47.6%), 97% of it from the coins; with timing it is the same
2018-2020 drawdown as above.

Checks (all pass): C of the six equals calm-drag-1's (SPY -1.51, QQQ -2.08, GLD -1.43, TLT
-2.28, coins 0.00); French US market and S&P 500 TR 2002-2025 equal gap-2002-1's N, I, B, C to
the hundredth (-1.41 / +6.64 / -5.89 / -2.16 and -1.00 / +4.93 / -4.28 / -1.65); I + B + C =
N and the calm split add up to 1e-14 on every row; the book attribution, rebuilt from the
gym's fills, sums to the equity change to 3e-16 of equity and the re-simulation equals the
harness run exactly. More rows (since-2002 windows of every proxy, cost K and timing T, gold
monthly on 2005-2025): the results file.

## Plain reading for the owner

**Where has the insurance paid for its premium (net N > 0)? Almost nowhere at cash 0; on the
long US stock record it about broke even.**

- **US stocks (SPY and its long proxies): about break-even over the long record, a cost since
  2002.** Trend-timing avoids more in falls than it gives back in the year after the low (I is
  larger than B on every US row), and the calm drag (about 1-2 a year) then tips the net to
  slightly negative: -0.10 a year on the French US market since 1927 (+0.66 if idle cash earns
  bills), -0.6 to -0.8 on SPY since 1994 and the S&P since 1986, about -1.0 to -1.4 since 2002.
  This is the one asset class where the exit also has measured skill as a crash warning (#182).
  So here the insurance is roughly fairly priced: you pay about what you get back, and what
  you get is shallower drawdowns.
- **QQQ: paid once, in a big way.** Since 2000 it is +1.06 a year ahead of holding, entirely
  thanks to the 2000-2002 crash (QQQ fell over 80%). Without that crash (since 2002) it trails
  by 1.48. The loose long proxy (French technology industry since 1927) is -0.40 (+0.46 with
  bills). QQQ also carried three quarters of the book's worst drawdown without timing (2000-2002),
  and timing cut that drawdown from 68.8% to 27.7% over the same dates.
- **Bonds (TLT and the 30-year Treasury since 1978): has not paid.** Bonds had few 25% falls (2
  since 2003, 4 since 1978); the fall gain is small (about +1.6 to +2.0 a year), the buy-back
  costs most of it, and the calm drag, mostly premium from being out about a quarter of calm
  time, makes the net -1.5 (TLT) to -2.1 (since 1978) a year at cash 0. With cash at bills it
  is less bad (-0.7) because bills paid well while out in the 1980s. Bonds never carried the
  book's worst drawdown; in the timed book's worst one they gained.
- **Gold (GLD): has not paid.** GLD lost even inside its falls (buy-back -2.53 against a fall
  gain of +1.64) and pays a large calm premium (out 20% of calm time): net -2.33 a year. The
  only long gold series (monthly averages since 1972) shows +0.22, but averaging flatters
  trend timing: on the same 2005-2025 years the averaged series gives -1.43 against GLD's
  -2.33. So "about zero at best" over 1972-2025, negative since 2002. Gold never carried the
  book's worst drawdown.
- **Coins (BTC, ETH): has not paid in their 9-12 years.** Coins are in a 25% fall or its
  rebound almost all the time, so the ledger is all I and B: huge gains in falls (+27 and +64 a
  year) and even larger give-backs after the lows (-31 and -67). Net -3.7 and -3.6 a year; the
  gym's crypto trading cost is about a third to a half of that (-1.0 and -1.9 a year). And
  timing did not protect the book from the coins: the timed book's worst drawdown (37.4%,
  2018-01 .. 2020-03) is a coin drawdown, and over those same dates the book without timing
  lost less (27.1%): the rule sold the coins in 2018, bought back higher in 2019 and was in for
  the March 2020 fall. Over the untimed book's own worst coin drawdown since 2002 (2018,
  47.6%) timing did help (29.3% over the same dates).

**In one line:** historically the insurance has about paid for its premium on US stocks over the
long record (and clearly on QQQ only because of 2000-2002); it has not paid on bonds, gold or the
coins, where it cost 1.5-3.7 log points a year against holding. This matches the crash-warning
skill pattern (#182: skill on US stocks, none on gold, bonds or coins).

**This is a description, not a recommendation.** No rule change is proposed or tested. Not
trend-timing bonds, gold or coins would be a new strategy try: it needs its own card (written
before any number), its family bar and the project bar (BAR.md: N for a new pick 1,116, z >=
4.93; measured rho N 506, z >= 4.70), and it would be a choice with hindsight on exactly these
histories. Whether to hold the insurance remains a drawdown preference (`owner-decisions.md`:
`tsmom12` is a risk choice, not an edge).

## How sure

- **One history per asset, few independent falls.** Bonds and gold have 2 falls each in their
  ETF windows, the coins one regime of 9-12 years. A single crash moves a row by points a year
  (QQQ: +1.06 with 2000-2002, -1.48 without). No standard errors: these are descriptions.
- **Proxies differ from the ETFs.** The 30-year rebuild (data-long-3) has a longer maturity
  than TLT's 20+ year basket; the French technology industry is not the Nasdaq-100 (loose);
  the gold series is monthly averages, which smooth prices and flatter trend timing (the
  jst-autocorr-1 caveat; here by about 0.9 a year on 2005-2025). Yields of day d are public
  the next business day (H.15); the bond rule reads them on day d, as the French and S&P
  series read their index level (a one-day publishing lag, not a market look-ahead).
- **The 25% cut-off decides what is a fall** (calm-drag-1's caveat: 2022 is a fall on some
  US series and calm on others). It changes the I/B/C split, not N.
- **N weights each asset alone.** In the book each asset has one equal slot, so an asset's
  ledger moves the book by about a sixth of its N (less before all six were eligible).
- **The book drawdown split is exact for the gym's fills, but rests on one worst episode per
  book.** Before 2003 the book held only SPY and QQQ (TLT and GLD became eligible in 2003 and
  2005, the coins in 2013 and 2017), which is why the untimed 1994-2025 worst is all stocks.
- **Deviations from the card, disclosed.** (1) Added side columns not on the card: trading
  cost over all sessions, and a side row "`equal-weight` over the `tsmom12` dates" (the mirror
  of the card's side row). (2) For the coins and the 30-year rebuild, the "since 2002" window
  equals the own window (they start later), so only one row is shown in the table above
  (the results file has every row).
- Bar for scale (BAR.md, rows through 2026-11-25 01:16): 4,126 distinct tries, N for a new
  pick 1,116 (z >= 4.93; measured rho: N 506, z >= 4.70; Bonferroni p <= 9.9e-05). Not
  applicable: no test, no pick.
- `tries.md`: 12 `note` rows (one per ledger series, one for the book split). Notes are not
  selectable; N for a new pick does not change.

## For the live rule

Nothing changes. For SUMMARY (the lead's call): per asset, trend-timing roughly paid for itself
on US stocks over the long record (French US market 1927-2025 -0.10 a year at cash 0, +0.66
with bills; since 2002 about -1.0 to -1.4) and on QQQ only through 2000-2002; it has not paid on
bonds (-1.5 to -2.1), gold (-2.3; monthly-average gold since 1972 about 0) or coins (-3.7,
-3.6). The timed book's worst drawdown (37.4%, 2018-2020) is a coin drawdown, deeper than the
untimed book over the same dates (27.1%).
