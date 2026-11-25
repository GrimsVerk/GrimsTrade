# pooled-2: do `e4` and `vt-own-70-x` beat `tsmom12` outside equities?

Lane `pooled-2`, 2026-11-24 (night). Branch `pooled-2`, draft PR #159. Research only: fake
money, files already in the data cache (read-only), no change to the gym, the daily runner or
the live strategies. Train data only: nothing after 2025-10-31 parsed, held-out year untouched.
Card (pushed before any number, not amended): `cards/pooled-2.md`. Tables:
`results/pooled-2.md` (+ `.json`); plumbing on random walks: `results/pooled-2-plumbing.md`.
Code: `lib/pooled2_core.py`, `lib/pooled2.py` (rules from `lib/pooled1_core.py`); tests
`tests/test_pooled2.py`. One real run.

## The answer on one screen

**Out of sample, neither lead holds up outside equities. `e4` on bonds and currencies: +0.010 per
market (z 0.33), so it is still open only because the test cannot see an edge below about +0.10.
`vt-own-70-x`: -0.010 (z -0.57), killed by the card's rule (95% upper end +0.024, below +0.03).
Its sizing helps a little on bonds and costs on the commodity currencies. Combined with
pooled-1's 41 stock markets, `e4` is +0.045 (z 1.43): "unsettled, leaning positive", with the
lean coming from stocks. `vt-own-70-x` is "equity-only at best". Nothing passes z 2.50, and
nothing comes near the project bar of 4.70.**

Per market: d = Sharpe of the variant minus Sharpe of `tsmom12` on the same series and periods,
in excess of the US bill. D = the equal-weight mean. SE from a joint bootstrap of 12-month
calendar blocks on one monthly calendar, which keeps the dollar factor, the world-rates factor
and the cross-class calendar.

| Variant | Bonds + currencies, 21 (95%) | z | US bonds 3 | Foreign bonds 9 | Currencies 9 | Before 1994 | Beyond drift | Verdict (card) | Commodities, spot 8 (shown) | Equity 41 (pooled-1) | Combined 62 | Combined reading |
|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|---|
| `e4` | **+0.010** (-0.050..+0.070) | +0.33 | -0.001 | +0.014 | +0.010 | +0.042 (z 1.01) | +0.009 | still open | -0.019 (z -0.86) | +0.063 (z 1.57) | **+0.045** (z 1.43) | unsettled, leaning positive |
| `vt-own-70-x` | **-0.010** (-0.043..+0.024) | -0.57 | +0.023 | +0.022 | -0.052 | +0.004 (z 0.18) | -0.005 | **killed** | +0.056 (z 2.15) | +0.022 (z 1.40) | +0.011 (z 0.89) | equity-only at best |

Bars (card): "real small edge" needs z >= 2.50, D > 0 in 2 of the 3 judged groups, and D > 0
before 1994. The project bar for selectable is z >= 4.70 (`BAR.md`, rows through 2026-11-24
20:01: 3,855 tries, N = 500 effective). "Killed": the 95% upper end below +0.03, or z <= -2.50.
The combined readings were stated in the card before the run. The equity column is pooled-1's
41 markets, re-run with pooled-1's code inside this bootstrap. Its point D equals pooled-1's to
the 15th decimal (+0.0629480, +0.0216657).

## Variant by variant

- **`e4` (ensemble of 1/3/6/12-month signals): still open, nothing outside stocks.** +0.010 on
  bonds and currencies, 12 of 21 markets ahead. Each group is within 0.015 of zero, all at
  z < 0.4. It is +0.042 before 1994 (z 1.01), and the drift-matched null is +0.001, so part
  positions give no mechanical lift here (excess returns barely drift). Per market it is noise
  in both directions: Swedish 10y +0.19, Norwegian +0.08, Japanese -0.13, Canadian -0.10, US
  10y -0.05. On commodity spot it is -0.019 (4 of 8). Combined with stocks it is +0.045 (z 1.43,
  before 1994 +0.062, z 1.95). The class-balanced mean is +0.036 (z 1.26). The test finds an edge
  of +0.10 per market 80% of the time on the judged pool, and +0.11 on the combined pool. So an
  `e4` edge of the size pooled-1 saw (+0.06) would not be seen here. But the non-equity point
  estimate is a sixth of that, not a confirmation. Reading: on stocks maybe a few hundredths of
  Sharpe (part of it the mechanical drift effect pooled-1 measured), elsewhere about zero.
- **`vt-own-70-x` (own-vol targeting at a 70% mean share): killed outside equities.** -0.010,
  95% range -0.043..+0.024. On bonds it is slightly ahead (US +0.023, foreign +0.022, neither
  significant). On currencies it is behind (-0.052, z -1.60), driven by the commodity
  currencies: CAD -0.19, AUD -0.11, NZD -0.11, NOK -0.08. Not examined further; one plausible
  cause is that their volatility spikes come during sell-offs that `tsmom12` has already left,
  so the sleeve is cut again for the rebound. On commodity spot it is +0.056 (z 2.15, 6 of 8). That comes mostly from PPI steel
  (+0.24) and primary nonferrous metals (+0.15). These are smoothed producer-price indices whose
  volatility is very uneven and not investable, so this is shown, not judged, and it is below
  2.50 anyway. Combined with stocks: +0.011 (z 0.89). Reading: own-vol stays what pooled-1 called
  it, a risk dial. Its small Sharpe gain is a stock-market effect (strongest on US industries)
  and does not carry over to bonds and currencies.

## The eight points from data-long-3, as applied

1. Bar: z >= 2.50 kept (comparable with pooled-1; Bonferroni over 2 would be 1.96. No result is
   between the two, so the choice decided nothing). Project bar 4.70.
2. Frequency: weekly engine on daily US bonds and eight currencies, monthly frozen versions on
   foreign bonds, `FX-EUR`, PPI and gold (36-month own-vol sigma).
3. Lags: the weekly signal reads Thursday's H.15 yield or the previous week's H.10 rate, and
   own-vol's sigma skips the last week. Monthly gap 1 for averaged series and 2 for PPI. Strict
   OECD publication gap of 3 (check): `e4` +0.001, `vt-own-70-x` -0.013 on the judged pool.
4. Excess over the bill, cash at the bill, signals on the excess-return level. FX signals on
   spot only (check): `e4` +0.019, `vt-own-70-x` -0.006.
5. 29 series, no nested ones; 21 judged.
6. Joint 12-month block bootstrap. Mean pairwise correlation of per-market d over draws: `e4`
   0.13 on the judged pool (US bonds 0.40, foreign bonds 0.28, currencies 0.27, commodities
   0.06). The realised SE of 0.030 sits between the card's prior rows for rho 0.1 and 0.3.
   Blocks of 3 and 24 months: SE 0.029 / 0.033.
7. Costs of 2 / 3 / 10 bps. With costs doubled: `e4` -0.002, `vt-own-70-x` -0.014 (judged).
8. Judged on bonds and currencies; commodities shown apart. No pass, so nothing to qualify.

## How sure

- One run of the pre-registered evaluation. Card, code, tests and the plumbing run were pushed
  before any real number, and the card was not amended. Plumbing (zero-drift random walks): D
  -0.010 / -0.000, |z| <= 0.6.
- On the 11 daily-data markets the rules are pooled-1's code (with zero lag the weekly engine
  equals `pooled1_core.decide` / `own_vol` exactly, tests). The 10 monthly markets (GOV9,
  FX-EUR) use the card's monthly versions, which are new code: `e4` on 1/3/6/12-month changes,
  own-vol with a 36-month sigma instead of 52 weeks (chosen in the card, not tested against
  alternatives). Split of the judged D: `e4` weekly +0.003 / monthly +0.018; `vt-own-70-x`
  weekly -0.038 / monthly +0.022, so the kill comes from pooled-1's own code on currencies
  (review of #159). The equity re-run reproduces pooled-1's D exactly.
- Rebuilt series, not traded ones. Bonds are constant-maturity par bonds; foreign bonds come
  from monthly averages (smoothed, half a month late); carry uses interbank rates (an upper
  estimate); PPI is a mid-month producer price with revisions. These affect each variant and its
  twin alike, but smoothing favours trend rules in general (PPI steel and coal `tsmom12` Sharpe
  0.6). That is one more reason commodities are not judged.
- Long or flat, as frozen: on currencies and bonds a long/short trend rule is the usual form.
  These results say nothing about the short side.
- Power: an edge below about +0.10 per market on bonds and currencies (+0.06 for own-vol), or
  +0.11 combined, is not ruled out for `e4`. Keyless data with more independent calendars than
  these 21 series are not in the cache.

## For the live rule

Nothing changes. `tsmom12` stays the rule. `e4` remains the only near-miss with a positive sign
on the combined pool, and its lean comes from stocks. `vt-own-70-x` is a risk dial with no Sharpe
gain outside stocks. The held-out year stays unspent.

## Logged

`tries.md`: 93 rows, idea `pooled-2`. 6 `variant` rows (`<v>@pooled2-nonequity-21`,
`@pooled2-com-8`, `@pooled2-combined-62`; Sharpe cell = mean per-market Sharpe of the variant)
and 87 `robustness` rows (`<rule>@<group>-<series>`, `tsmom12`, `e4`, `vt-own-70-x` on 29
series; Sharpe at the series' frequency, turnover = position change a year, `-` for own-vol).

## Next lanes (not started)

1. None for these two variants on keyless data: the open question (`e4` at +0.03-0.06 on stocks)
   is below what any pool here can see.
2. If the trend rule is ever revised, a long/short version on bonds and currencies is a
   different rule and needs its own card. It is not a continuation of this one.
