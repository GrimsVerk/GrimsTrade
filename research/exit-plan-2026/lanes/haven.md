# Lane `haven`: what held its value while stocks crashed (short run and whole fall)

Lane note for the exit plan (`research/exit-plan-2026/README.md`), night lead 2026-11-18.
Descriptive history only: no strategy was tested, nothing fitted, so nothing went into
`research/tries.md`. Practical Dutch products (which savings account, which money-market ETF,
costs) are the `park` lane's job; this note covers how the assets **behaved**.

## Bottom line

- **The only assets that never put a euro holder under water in any crash measured here are
  euro cash and euro money-market-like holdings** (savings account, 3-month Euribor, the EUR
  overnight-rate ETF: at worst -0.5% in 2020, the cost of negative rates). Short (1-3 year)
  government bonds come next: at worst -3% to -5% (2020 dash for cash, 2022 rate shock).
- **Every "haven" with a price swing failed in at least one crash, and often in the first
  days**: gold fell 22% inside the 2008 Lehman leg and 12% in March 2020; long government bonds
  lost 16-32% in 2022 when stocks and bonds fell together; Berkshire fell with the market in
  1987, 2008 and 2020; the dollar fell together with US stocks in the 2025 tariff shock.
- **For a euro holder the currency often matters more than the asset.** US T-bills earned
  +13% in euros over the Lehman leg and +17% in 2022 (dollar up), but -4% in the 2025 shock
  and were 15% under water at one point in 2000-02 (dollar down).
- **For parking the proceeds of a small portfolio for 6 weeks to many months, the evidence supports euro cash (deposit
  guarantee) or a euro government/overnight money-market fund, optionally short euro
  government bonds.** Gold, long bonds, CHF, JPY, USD and Berkshire are bets on the *kind* of
  crash, not parking places. Cash also keeps the full amount ready to buy back in at the bottom.

## Method

Script: `research/exit-plan-2026/scripts/haven_crash_table.py`; full output:
[`haven-table.md`](haven-table.md) (every number below comes from it unless a link is given).

- **Episodes.** For each crash the script finds the S&P 500 (^GSPC, price index) highest close
  before the lowest close inside a fixed search window: 1929-32, 1973-74, 1987, 2000-02,
  2007-09, the 2008 Lehman leg (fixed start: close of Fri 2008-09-12), 2020, 2022, Aug 2024,
  2025 tariff shock. Exact peak and trough dates are in the table.
- **Windows.** Whole drawdown (peak close to trough close); "worst point" (the asset's lowest
  value, measured from the stock peak, at any close up to the trough); "own max drawdown" (the
  asset's own largest peak-to-trough fall inside the window); and the short run: the first 1, 5
  and 15 trading days of the worst leg (the 15-day window with the worst S&P fall) plus the
  single worst S&P day.
- **Data (public; raw files kept out of git).** Yahoo chart API daily (^GSPC, ^IXIC, GC=F gold
  futures from 2000-08, GLD, SHY, IEF, TLT, BRK-A, OBX.OL total return, EXX6.DE long Bunds,
  EUNH.DE euro govt, DBXP.DE euro govt 1-3y, XEON.DE EUR overnight-rate swap ETF); FRED
  ([fredgraph.csv](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10)) DGS2, DGS10,
  DGS30, DEXSZUS, DEXJPUS, DEXUSEU, DEXNOUS; Ken French daily factors (1-month T-bill, US market
  total return, from 1926); ECB 3-month Euribor monthly
  ([FM.M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA](https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA?format=csvdata));
  Shiller monthly 10y bond return and CPI ([shillerdata.com](https://shillerdata.com/));
  World Bank Pink Sheet monthly gold
  ([CMO-Historical-Data-Monthly.xlsx](https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx)).
- **Approximations.** US Treasury returns are rebuilt from constant-maturity yields as par
  bonds; checked against the ETFs where both exist (10y vs IEF: GFC +21.5 vs +20.2, 2020 +7.8
  vs +6.4, 2022 -16.4 vs -15.4). Currency columns are the exchange-rate move only, without the
  interest the currency earns. Gold before 2000-08 is a monthly average (blurs the short run).
  Euro view only from 1999 (DEM/USD from FRED could not be downloaded: bot check). OBX trades
  in Oslo hours, so its one-day numbers are not the same session as New York.

## Crash table, USD investor (whole drawdown, own max drawdown in brackets, %)

| Episode (S&P peak - trough) | S&P 500 | T-bills | US 2y | US 10y | Gold | CHF | JPY | Berkshire |
|---|---|---|---|---|---|---|---|---|
| 1929-09-16 - 1932-06-01 | -86.2 | +5.1 | n/a | +8.7 (monthly) | 0 (fixed $20.67) | n/a | n/a | n/a |
| 1973-01-11 - 1974-10-03 | -48.2 | +13.5 | n/a | +1.0 (-5.2) | +145 (monthly avg) | +27.8 (-21.2) | +0.8 (-16.7) | n/a |
| 1987-08-25 - 1987-12-04 | -33.5 | +1.7 | +2.4 (-1.4) | +1.1 (-7.9) | +5.4 (monthly avg) | +10.2 (-3.4) | +7.8 (-4.0) | -29.5 (-37.1) |
| 2000-03-24 - 2002-10-09 | -49.1 (Nasdaq -77.6) | +10.6 | +22.3 (-1.6) | +39.5 (-7.4) | +10.8 (monthly avg) | +10.1 (-11.9) | -13.2 (-23.8) | +24.3 (-21.5) |
| 2007-10-09 - 2009-03-09 | -56.8 | +2.7 | +9.6 (-2.7) | +21.5 (-8.0) | +21.0 (-29.7) | +1.8 (-19.4) | +18.3 (-12.3) | -40.3 (-51.5) |
| Lehman leg 2008-09-12 - 2008-11-20 | -39.9 | +0.1 | +2.8 (-1.0) | +6.2 (-5.2) | -1.5 (-21.9) | -7.1 (-11.3) | +13.2 (-7.8) | -35.1 (-47.3) |
| 2020-02-19 - 2020-03-23 | -33.9 | +0.2 | +2.3 (-0.4) | +7.8 (-6.0) | +3.3 (-11.7) | +0.2 (-5.8) | -0.2 (-7.9) | -30.2 (-30.2) |
| 2022-01-03 - 2022-10-12 | -25.4 | +0.5 | -4.7 (-4.9) | -16.4 (-16.9) | -6.8 (-19.9) | -7.9 (-9.2) | -21.5 (-22.6) | -12.1 (-26.0) |
| 2024-07-16 - 2024-08-05 | -8.5 | +0.3 | +1.3 (-0.1) | +3.5 (-0.9) | -1.2 (-4.3) | +5.0 (-0.8) | +10.2 (-0.5) | -6.1 (-7.6) |
| 2025-02-19 - 2025-04-08 | -18.9 | +0.7 | +1.6 (-0.2) | +2.7 (-2.0) | +4.9 (-5.6) | +5.8 (-1.0) | +3.2 (-2.5) | +1.8 (-8.6) |

Notes: 1929-32 gold was fixed by law at $20.67/oz until the 1934 devaluation to $35
([Federal Reserve History](https://www.federalreservehistory.org/essays/gold-reserve-act),
[gold.org](https://www.gold.org/sites/default/files/documents/after-the-gold-standard/1934jan31.pdf)),
so it equalled cash in dollars. US CPI fell 21% over 1929-09 to 1932-06 (cash +5% nominal was
about +34% real) and rose 20% over 1973-01 to 1974-10 (T-bills +13.5% nominal were about -5%
real; 10y bonds about -16% real), both from the Shiller CPI column.

## Crash table, EUR investor (whole drawdown, own max drawdown in brackets, %)

| Episode | S&P in EUR | EUR cash (Euribor) | EUR o/n ETF (XEON) | EZ govt 1-3y | Bund 10.5y+ | US 10y in EUR | T-bills in EUR | Gold in EUR | CHF in EUR | JPY in EUR | BRK in EUR | Oslo OBX in EUR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2000-02 | -49.9 (-54.4) | +11.0 | n/a | n/a | n/a | +37.4 (-12.1) | +9.0 (-15.3) | n/a | +8.5 (-3.0) | -14.5 (-26.8) | +22.5 (-28.5) | n/a |
| 2007-09 | -51.8 | +6.3 | n/a | n/a | n/a | +35.5 (-11.0) | +14.5 (-13.3) | +34.9 (-18.1) | +13.5 (-9.0) | +32.0 (-11.3) | -33.4 (-43.6) | -61.7 (-69.6) |
| Lehman leg | -32.0 | +0.9 | +0.7 (0.0) | +3.4 (-0.5) | +8.1 (-8.6) | +20.1 (-7.0) | +13.3 (-4.5) | +11.4 (-16.0) | +5.2 (-5.6) | +28.1 (-11.3) | -26.6 (-39.5) | -54.2 |
| 2020 | -33.7 | -0.0 | -0.2 (-0.5) | -1.7 (-3.1) | +1.8 (-10.3) | +8.2 (-1.5) | +0.5 (-5.4) | +3.6 (-12.6) | +0.5 (-0.7) | +0.1 (-2.3) | -30.0 | -42.2 (-42.3) |
| 2022 | -13.1 (-18.0) | -0.1 (-0.2) | -0.3 (-0.4) | -4.1 (-4.6) | -31.7 (-32.6) | -2.6 (-9.6) | +17.1 (-3.6) | +8.5 (-11.6) | +7.2 (-4.4) | -8.6 (-13.3) | +2.4 (-22.0) | -9.0 (-22.0) |
| Aug 2024 | -9.1 | +0.2 | +0.2 (0.0) | +0.7 (-0.1) | +3.7 (-1.1) | +2.8 (-0.6) | -0.4 (-1.5) | -1.8 (-4.0) | +4.3 (-0.3) | +9.4 (-0.5) | -6.7 (-7.8) | -6.6 (-8.9) |
| 2025 | -22.7 | +0.3 | +0.3 (0.0) | +0.8 (-0.5) | -2.6 (-7.6) | -2.0 (-5.3) | -4.0 (-5.4) | 0.0 (-6.5) | +0.9 (-3.0) | -1.6 (-4.5) | -2.9 (-9.5) | -8.5 (-15.1) |

The euro-ETF columns start in 2008, so they miss the 2007 peak; Euribor cash is a smooth
accrual, so its own drawdown is zero by construction (negative rates in 2020-22 show up as a
small minus in the whole-period number).

## The short run (first days of the worst leg, worst single day)

From the "leg 1d / 5d / 15d" and "worst day" rows of [`haven-table.md`](haven-table.md):

- **Cash and T-bills were never negative in any window, in any episode.** US 2y notes lost at
  most 0.5% over 5 days (1987) and 1.0% over 15 days (2022).
- **Long bonds wobbled first**: in 1987 the 10y lost 1.5% in the 5 days before Black Monday,
  then gained 6.4% over 15 days; in the Lehman leg the 10y lost 0.4-0.5% over the first 1-5
  days; in 2022 they fell with stocks the whole way (30y -5.5% in the worst 15 days).
- **Gold**: on the worst day of the GFC (2008-10-15, S&P -9.0%) gold fell 4.1%; on
  2024-08-05 (S&P -3.0%) it fell 1.5%; in 2020 it rose in the first days of the leg (+3.1%
  day 1) and then fell 11.8% from its 2020-03-09 close ($1,674.5) to 2020-03-18 ($1,477.3,
  GC=F) in the "dash for cash". In 2008 it fell 22% from 2008-09-22 to 2008-11-13. This matches
  the literature: gold's haven effect is short-lived and can reverse when investors need cash.
- **Berkshire** fell 10.9% on day 1 of the 2008 worst leg (2008-09-22) and 18.5% on Black
  Monday 1987: in the short run it behaves like a stock.
- **CHF and JPY** were the steadiest non-cash assets in the first days (mostly within ±1% on
  the worst day, often up), but JPY fell 1.3% on the worst 2022 day.
- **For a euro holder, the dollar can swing both ways in one day**: day 1 of the 2008 worst
  leg, T-bills were -2.1% in euros (dollar fell) while the S&P fell 5.9% in euros; over the
  15-day leg the dollar then rose about 9%, leaving T-bills +6.9% in euros.

## What the literature says

- **Gold: hedge on average, safe haven only briefly.** Baur and Lucey (2010, *Financial
  Review* 45(2), [RePEc](https://econpapers.repec.org/RePEc:bla:finrev:v:45:y:2010:i:2:p:217-229))
  define a hedge (uncorrelated or negatively correlated on average) and a safe haven
  (uncorrelated or negative in extreme falls). Their working paper on US, UK and German data
  ([TCD IIIS DP 198](https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp198.pdf), abstract,
  verified): "Gold is a safe haven for stocks only for 15 trading days after an extreme shock
  occurred", and it is neither hedge nor haven for bonds. Baur and McDermott (2010, *J.
  Banking & Finance* 34(8),
  [RePEc](https://econpapers.repec.org/RePEc:eee:jbfina:v:34:y:2010:i:8:p:1886-1898),
  [WP](https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp310.pdf)): over 1979-2009 gold is a hedge
  and safe haven for major European markets and the US, not for Australia, Canada, Japan or the
  BRICs; a strong haven at the peak of the 2008 crisis (abstract checked on RePEc; the 15-day figure belongs to Baur and Lucey, not this paper). Our table
  agrees on the whole drawdown (GFC +21%) but shows the in-crisis falls (Lehman leg -22%,
  2020 -12%) that a "15 days" haven allows.
- **Safe-haven currencies.** Ranaldo and Söderlind (2010, *Review of Finance* 14(3),
  [RePEc](https://econpapers.repec.org/RePEc:oup:revfin:v:14:y:2010:i:3:p:385-407)), 1993-2008
  high-frequency data: CHF and JPY gain against the USD when US stocks fall and FX volatility
  rises, over hours to days, more strongly in crises (abstract checked on RePEc).
  Our table: CHF and JPY rose against USD in most episodes, but JPY fell 21.5% in 2022 and
  13% in 2000-02, and CHF fell 7% against USD in the Lehman leg.
- **Flight to quality in government bonds, and when it failed.** In March 2020 investors sold
  even Treasuries for cash: the FSB's
  [Holistic Review of the March Market Turmoil](https://www.fsb.org/2020/11/holistic-review-of-the-march-market-turmoil/)
  (Nov 2020) describes a "dash for cash", with open-ended funds net sellers of government bonds
  and dealers unable to absorb the selling (from the FSB summary page and secondary coverage).
  The New York Fed's [Liberty Street Economics](https://libertystreeteconomics.newyorkfed.org/2022/09/how-can-safe-asset-markets-be-fragile/)
  discusses the fragility of safe-asset markets and Vissing-Jorgensen's (2021) finding that
  foreign and mutual-fund Treasury sales exceeded liquidity needs (secondary). Our table: the
  US 10y still ended 2020 up 7.8% but long Bunds fell 10.3% peak to trough in euros.
- **Stocks and bonds falling together.** Brixton, Brooks, Hecht, Ilmanen, Maloney and McQuinn
  (2023, *J. Portfolio Management*,
  [AQR](https://www.aqr.com/insights/research/journal-article/a-changing-stock-bond-correlation))
  explain the stock-bond correlation by the relative volatility of growth versus inflation
  news: positive when inflation uncertainty dominates (the US correlation was positive over
  most of 1926-1999, negative 2000-2022, per a secondary summary). 2022 (long Bunds -32%, US
  30y -30%) and 1973-74 (bonds about -16% real) are the failures of the bond haven; both were
  inflation crashes.
- **Trend following / "crisis alpha".** Hurst, Ooi and Pedersen (2017, *J. Portfolio
  Management*, "A Century of Evidence on Trend-Following Investing";
  [summary](https://alphaarchitect.com/time-series-momentum-aka-trend-following-the-historical-evidence/))
  report positive trend returns in 8 (or 9, depending on version) of the 10 worst 60/40
  drawdowns since the late 1800s. Neville, Draaisma, Funnell, Harvey and Van Hemert (2021,
  *JPM*, [Man Institute](https://www.man.com/maninstitute/best-strategies-for-inflationary-times))
  find trend following and commodities did best, and bonds and equities worst, in US
  inflationary regimes. Both are by firms that sell trend products; not tested here (no free
  daily CTA index); a managed-futures fund is a strategy with its own losing years, not a
  parking place.
- **Money-market funds can break.** The Reserve Primary Fund fell to 97 cents on 2008-09-16
  after writing its Lehman paper to zero and suspended redemptions
  ([InvestmentNews](https://www.investmentnews.com/mutual-funds/huge-money-market-fund-breaks-the-buck/17433)).
  The EU answer is the MMF Regulation ([EU 2017/1131](https://eur-lex.europa.eu/eli/reg/2017/1131/oj)):
  three types (public-debt CNAV, which must hold at least 99.5% public debt; LVNAV; VNAV) and
  mandatory stress tests (Art. 28). In March 2020 euro-area LVNAV funds (especially USD ones)
  lost about EUR 85bn, 16% of assets, between 11 and 25 March, while CNAV (public-debt) funds
  had inflows ([ECB Macroprudential Bulletin 12, April 2021](https://www.ecb.europa.eu/pub/financial-stability/macroprudential-bulletin/html/ecb.mpbu202104_2~a205b46756.en.html),
  verified: "around €85 billion (16% of their total assets) between 11 and 25 March"). The ESRB recommended reform in Dec 2021. Lesson: a
  government-only money-market fund or a deposit is safer than a "prime" (corporate paper)
  money fund.
- **Deposit guarantee (NL).** Up to EUR 100,000 per person per bank (brands of one bank count
  together); temporarily up to EUR 500,000 for six months for some life events
  ([De Nederlandsche Bank (DNB) FAQ](https://www.dnb.nl/en/reliable-financial-sector/dutch-deposit-guarantee/faq-dutch-deposit-guarantee/)).
  A small portfolio of a few thousand euros is far inside the limit.

## Verdict per haven

| Haven | Short run (days-weeks) | Whole drawdown | Failure modes | For a EUR holder |
|---|---|---|---|---|
| **EUR savings account (guaranteed)** | never down | small plus | inflation (1973-74 cash lost ~5% real); negative rates (2015-22); bank failure above EUR 100k | the reference: no currency risk |
| **EUR government / overnight MMF or ETF** | at worst -0.5% (XEON 2020) | ≈ cash | prime/LVNAV funds can gate or lose (2008, Mar 2020); swap-based ETF has counterparty risk (`park` lane) | as cash, slightly more yield, no guarantee |
| **Short govt bonds (1-3y)** | at worst -3% (EZ 1-3y 2020), -4.6% (EZ 1-3y 2022), -4.9% (US 2y 2022) | mostly up (US 2y +22% in 2000-02) | rate shocks (2022); euro-area spread risk inside "Eurozone govt" indices | fine for months if euro-denominated |
| **Long govt bonds** | wobbly first days (1987, 2008), dash for cash (2020: long Bunds -10%) | big win in deflationary crashes (2000-02 +40%, GFC +22%), big loss in inflationary ones (2022 -16% to -32%) | inflation, rising rates, liquidity selling | long Bunds -32% in 2022; US bonds add dollar swings |
| **Gold** | unreliable: -4% on the worst GFC day, -12% (2020), -22% (Lehman leg) | usually up (1973-74, 1987, 2000-02, GFC, 2025), down in 2022 (USD) | liquidity selling, rising real rates, 15-20% yearly swings | in EUR: -16% (Lehman leg), -13% (2020), -12% (2022) at worst |
| **CHF** | steady, mostly up vs EUR | up vs EUR in all 7 euro-era episodes (+0.5 to +13.5) | central-bank caps and policy jumps; ~0% interest | best behaved non-cash haven in this table, but a currency bet (worst point -2.3%) |
| **JPY** | up in carry unwinds (Aug 2024 +9%) | mixed: +28% (Lehman leg, EUR) but -9% (2022), -15% (2000-02) | rate differentials; fails in inflation/rate rises | a carry-unwind hedge, not a parking place |
| **USD cash / T-bills** | swings ±2% a day vs EUR | +13% to +17% in 2008 and 2022, -4% in 2025, -15% at worst in 2000-02 | dollar can fall with US stocks (2025) | adds currency risk larger than the haven effect |
| **Berkshire Hathaway** | falls like the market (-18.5% on Black Monday, -10.9% day 1 of 2008 leg) | won in the tech-only pop (+24% 2000-02) but -40% GFC, -30% 2020 | it is a stock: beta < 1, not a haven | plus dollar risk; -44% at worst in GFC in EUR |
| **Trend following** | literature: positive in 8-9 of 10 worst 60/40 drawdowns | strategy-dependent | fees, losing years, whipsaw | not tested here |

Berkshire detail (BRK-A closes, Yahoo): it fell 49% from 1998-06-19 ($80,900) to 2000-03-10
($41,300), the very day the Nasdaq peaked, while the Nasdaq rose 183% and the S&P 27%; from
2000-03-10 to 2002-10-09 it then rose 65% while the Nasdaq fell 78%. In 2007-09 its own
drawdown was -51.5% (low 2009-03-05). So it was a great "anti-tech-bubble" stock once, but
not a crash haven: in broad crashes it fell nearly as much as the index.

Oslo detail: the OBX total-return index lost 62% in euros over 2007-09 (own max drawdown
-70%; the krone fell with the oil price), 54% in the Lehman leg and 42% in 2020, more than the
S&P in euros each time (-52%, -32%, -34%). In the smaller falls it lost less than the S&P in
euros (2022 -9.0 vs -13.1, Aug 2024 -6.6 vs -9.1, 2025 -8.5 vs -22.7), but its own drawdowns
were still -22% (2022) and -15% (2025). For a euro holder, Oslo-listed stocks are a stock
holding with extra currency risk that fell hardest in the two deep crashes, not a haven.

Correction 2026-11-18 (review round 1): the OBX-in-EUR numbers first published here were
wrong. The script built EUR/NOK as (NOK per USD) / (USD per EUR), giving about 3.9 instead of
7.7 in Oct 2007; it now multiplies (FRED DEXNOUS 5.4469 x DEXUSEU 1.4092 = 7.68 on
2007-10-09) and stops if EUR/NOK leaves 6-15. Changed (whole drawdown, own max drawdown):
2007-09 -69.2 (-80.5) -> -61.7 (-69.6); Lehman leg -64.3 (-66.0) -> -54.2 (-54.2); 2020
-42.6 (-42.9) -> -42.2 (-42.3); 2022 -32.9 (-39.3) -> -9.0 (-22.0); Aug 2024 -5.3 (-7.2) ->
-6.6 (-8.9); 2025 +0.7 (-13.4) -> -8.5 (-15.1). The earlier text ("43% in 2020 and 33% in
2022, more than the S&P in euros each time") was wrong for 2022: OBX lost less than the S&P in
euros there (-9.0 vs -13.1), and also in Aug 2024 and 2025. All OBX-in-EUR cells
of [`haven-table.md`](haven-table.md) changed; no other column did (the USD-to-EUR conversion
and the CHF/JPY quotes were checked and are right).

## Which havens the evidence supports for ~6 weeks to many months

1. **First choice: euro cash under the deposit guarantee, or a euro government / overnight
   money-market fund.** It is the only holding that kept its nominal euro value in every
   episode and every window, including the first days. Its weakness, inflation, costs little
   over months (it mattered in 1973-74 over two years). It also gives the cleanest re-entry:
   the full amount is there at the bottom.
2. **Acceptable addition: short (≤2-3 year) euro government bonds**, at worst a few percent
   down in a rate shock. Little extra yield over cash for a horizon of months.
3. **Not supported as parking**: gold (falls in the liquidity phase of a crash, exactly
   when parking must hold, and swings 15-20% a year), long bonds (fail in an inflationary crash, as in 2022),
   USD anything (currency risk bigger than the haven effect, and the dollar fell with US stocks
   in 2025), JPY (fails when rates rise), Berkshire (a stock).
4. **Defensible only as a small, deliberate hedge**: CHF. It was the best-behaved non-cash
   asset for a euro holder in this table, but it pays about nothing and is a currency
   position, not parking.

Which crash would an AI-bubble pop resemble? The closest analogue is 2000-02 (tech -78%,
S&P -49%): long bonds, Berkshire, gold and CHF all ended up, but over 2.5 years with deep
interim swings, and the dollar first rose then fell. If the pop came with inflation (as in
2022), bonds and gold would fail too. Cash is the only holding that did not depend on which.

## Could not verify / gaps

- Daily gold before 2000-08 (LBMA, stooq and Bundesbank pages answered with bot checks);
  1987 and 2000-02 gold are monthly averages. A claim that gold rose 4.2% intraday on Black
  Monday to $491.50 appears only in a dealer blog (unverified).
- DEM/USD (FRED DEXGEUS) download was blocked, so no euro view before 1999.
- Literature figures marked "via search summary" or "secondary" (FSB findings, Vissing-Jorgensen,
  Hurst-Ooi-Pedersen 8-9 of 10, AQR correlation numbers) were read from abstracts or
  summaries, not the full papers. The Baur-Lucey 15-day sentence was read in the paper;
  the Baur-McDermott and Ranaldo-Söderlind abstracts were checked on RePEc.
- Treasury returns are rebuilt from yields (checked against ETFs, gaps of 1-5 points over
  long windows). Price indices ^GSPC/^IXIC exclude dividends; the French total-return column
  is next to them in the full table.
