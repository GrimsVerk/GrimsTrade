# parked-gates-1: two parked candidates gated (W32 `drought-inflation`, W33 `margin-susceptibles`)

Lane parked-gates-1, written 2026-11-25 about 00:55 UTC, **before any return, slope or t of
either rule below was computed**. Candidates Y4 and Y5 of `research/wide-17.md` step 2 (both
scored 4, parked). Method: `research/gate-null.md` (40 placebos, the rank decides, t >= 2 also
needed, kill-only label). Script `research/lib/parkedgates1.py` (pure functions in
`research/lib/parkedgates1_events.py`, tests in `tests/test_parkedgates1.py`), pushed before its
first run. One dry run (`DRY=1`, counts only), then one real run.

**Train cut.** Nothing dated after **2025-10-31** is read: price bars, drought months and
Financial Accounts quarters alike (`LAST = 2025-10-31`; every exit bar on or before it).

## Which parked candidates, and why these two

Six parked candidates passed the #109 filters tonight without a gate: wide-17's Y4
`drought-inflation` (4), Y5 `margin-susceptibles` (4), Y3 `monsoon-gold` (3) and wide-20's P3
`panic-words`, P4 `mass-casualty-mood`, P12 `strike-idleness` (4 each). Top 2 by score, then
data (keyless, long, published with a known lag):

| Candidate | Score | Keyless data, length, lag | Gated? |
|---|---:|---|---|
| Y4 `drought-inflation` | 4 | NOAA nClimDiv Palmer drought index, contiguous US, monthly from 1895, one static file; month m posted about the 5th-10th of m+1 (the listing shows the 2026-11-05 file) | **yes, W32** |
| Y5 `margin-susceptibles` | 4 | FINRA's margin statistics page answers this script with 403 (the BLS/SEC policy class of data-wide-1; a browser User-Agent is not used). Substitute: the Federal Reserve's Financial Accounts (Z.1) via FRED's keyless graph CSV: broker-dealer receivables due from customers (margin loans and other receivables, `BOGZ1FL663067003Q`) and all-sector corporate equities at market value (`BOGZ1LM893064105Q`), quarterly from 1945; Z.1 comes about 10 weeks after the quarter | **yes, W33** (on the substitute data) |
| P3 `panic-words` | 4 | about 2,000 loc.gov API calls and a pre-1963 index; the heaviest fetch | no (next in line) |
| P4 `mass-casualty-mood` | 4 | public lists with unclear redistribution terms; P1's channel died as W31 | no |
| P12 `strike-idleness` | 4 | BLS refuses scripts without a contact e-mail in the User-Agent (data-wide-1); this public repo sends none | no |
| Y3 `monsoon-gold` | 3 | IMD rainfall; W13's dead channel, fails the flow-size check | no |

Overlap re-checked (`ideas.md`, `gate-null.md`, `tries.md`, 2026-11-25): W19 `enso-commodity`
tested ENSO -> crop yields -> DBC (dead); W32 uses a drought dose on bonds, the same crop
channel at its inflation end (said in wide-17's score: "not killed" 0). No gate or strategy used
margin debt or broker receivables (data-wide-1 listed FINRA margin debt as F2 and downloaded
nothing; E4 killed coin leverage through funding and basis). Neither is a copy of a gated idea.

**Disclosure (format probes before this card, no price, return or statistic).** NOAA climdiv
directory listing; the first row of `climdiv-pdsist-v1.0.0-20261105` (state 001, 1895) and the
first contiguous-US row (code 110, 1895). FRED series pages' titles for the two Z.1 series and
the first row of `BOGZ1FL663067003Q` (1945-10-01). The FINRA page's status code (403).

## W32 `drought-inflation`

**Hypothesis.** Widespread US drought cuts crop yields; food prices rise months later and
inflation prints come in higher; long Treasury prices fall as that inflation arrives. TLT earns
less in the months after drought spreads (predicted sign of b: **negative**).

**Data.** NOAA nClimDiv state file `climdiv-pdsist-v1.0.0-<date>` (PDSI, element 05; code 110
= contiguous US; monthly from 1895; keyless, US public domain), the 2026-11-05 vintage, fetched
once into the shared cache `parked-gates-1/climdiv/`. Today's vintage: the whole series is
recomputed each month and recent months can be revised `[memory]`; real-time vintages are not
used. Months after 2025-10 are never read; -99.99 is missing.

**Dose.** D(m) = -PDSI(m) (positive = drier; PDSI is already a standardised index, about -6 to
+6).

**Available on (no look-ahead).** Month m is posted in the first ten days of m+1. The outcome
for dose month m is TLT's log return over months m+2 .. m+4: from the close of the last bar on
or before the last day of m+1 to the close of the last bar on or before the last day of m+4
(dividend-adjusted closes, `harness.load_history("train")`). The row is dropped if a bar is
missing, the entry bar is not in month m+1 or the exit bar not in month m+4, or the exit bar is
after 2025-10-31.

**Statistic.** OLS y = a + b D, one row a dose month, t of b with Newey-West (Bartlett) 3 lags
over the month index (`wide11_events.ols_dk` with one row per period; the same code path for
every cell). No controls (F2 passes outright: drought does not follow prices).

**Placebo null (the decider).** Weather does not answer prices, so shifts both ways are
allowed: D_k(m) = D(m - k months), k in +-{13, 17, 21, ..., 89} (`wide17_events.SHIFTS_W29`,
step 4, never a multiple of 12): **40 placebos**. A row with a missing D_k (later doses past
2025-10) is dropped from that placebo only.

**Gate. Pass only if both hold** (dose months 2002-07 .. 2025-06, TLT's span):
1. b < 0 with t <= -2.
2. The true t ranks among the 2 lowest of 41.

**Kill-only.** US drought comes in a few multi-year episodes (2002, 2006-2008, 2011-2013,
2020-2022 and smaller ones): about 6-10 independent swings in 23 years. Smallest p 1/41 = 0.024,
above the family bar (0.10 / 97 = 0.00103) and the register's (9.9e-5). A fail kills the idea; a
pass only says "not dead yet".

**Shown (not gating).** GLD and DBC instead of TLT (predicted positive), IEF, SPY; the 1-month
horizon (month m+2 only); the 6-month horizon (m+2 .. m+7, NW 6 lags); growing-season dose
months only (May-September); the 3-month change PDSI(m-3) - PDSI(m) as the dose; the reaction
cell (TLT over month m+1, the release month); the null's width.

**Power, written before any number.** TLT's 3-month sd is about 7%; about 276 rows overlapping
by 2 (about 92 effective); if PDSI's sd is about 2, the standard error of b is near 7% / (2 x
sqrt(92)) = 0.36% per unit. t -2 needs b near -0.7% per unit per quarter, about -1.5% a quarter
per sd of drought (6% a year): only a very large effect passes.

**My guess before any number.** b of either sign, |t| < 1.5, middle rank; placebo t sd 1.3-1.8
(a persistent dose with few episodes). Chance of a pass: 1%.

## W33 `margin-susceptibles`

**Hypothesis.** A crash is an outbreak whose size needs a large susceptible stock (R0 = beta S
/ gamma): leveraged longs. A first fall triggers margin calls, forced sales push prices further
down, and only when margin credit is large relative to the market does the fall continue the
next month. Predicted: the slope of next month's return on this month's fall is larger when S is
high (interaction coefficient b3 **positive**: a fall (F < 0) with high s predicts a lower next
month).

**Data.** FRED graph CSV (keyless, Federal Reserve Z.1 data): R(q) = `BOGZ1FL663067003Q`
(security brokers and dealers; receivables due from customers, margin loans and other
receivables; level, USD millions), V(q) = `BOGZ1LM893064105Q` (all sectors; corporate equities;
market value), quarter-end levels, one snapshot each into `parked-gates-1/fred/`. Today's
vintage (revised data; the first-release values are not used). Quarters ending after 2025-10-31
are never read. R includes non-margin receivables (a noisier S than FINRA's margin debt).
Prices: GSPC (S&P 500 price index, daily from 1950 in the cache) and SPY (shown).

**Dose.** S(q) = R(q) / V(q); s(q) = ln S(q) minus the mean of ln S over the 40 quarters q-40 ..
q-1 (S drifts with the size of the broker sector). NaN without all 40.

**Available on (no look-ahead).** For decision month m, s(m) = s of the latest quarter whose
end month is <= m - 3 (Z.1 is released about 10 weeks after the quarter; in month m the quarter
that ended three months earlier is public by the month's end `[memory]`; a stricter shown cell
uses <= m - 6).

**Rule.** r(m) = GSPC log return over calendar month m (close of the last bar of m-1 to the
close of the last bar of m; both bars inside their months). Trigger F(m) = min(r(m), 0). Outcome
y(m) = r(m+1). Control c(m) = GSPC log return over months m-12 .. m-1 (the year before the
trigger month).

**Statistic.** OLS y = a + b1 F + b2 s + b3 F s + c1 c + c2 F c, one row a month, t of **b3**
with Newey-West 3 lags (`ols_dk`, one row per month; same code path for every cell). The
controls are there because margin credit swells after rallies (F2 passes only with them): F c
keeps "falls after a boom" from passing as "falls with many susceptibles".

**Placebo null (the decider).** S answers prices (debt follows bull markets; V is a price),
so only **earlier** doses: s_k(m) = s(m - k months), k in {25, 27, ..., 103} (odd, 40 values,
2 to 8.6 years back, never a lagged copy within the 10-week release delay): **40 placebos**,
F, c and y unchanged. Gate months start where every placebo has a dose, so all 41 fits use the
same rows.

**Gate. Pass only if both hold** (decision months 1965-01 .. 2025-09):
1. b3 > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41.

**Kill-only.** Falls deep enough to trigger margin calls cluster in perhaps 20-30 episodes since
1965 (1966, 1969-70, 1973-74, 1987, 1990, 1998, 2000-02, 2008-09, 2011, 2018, 2020, 2022 and
others). Smallest p 1/41 = 0.024, above both bars.

**Shown (not gating).** Without controls; the binary trigger 1[r(m) < -5%] instead of F (its
interaction with s); the stricter release lag (quarter end <= m - 6); SPY instead of GSPC
(months from 1993-02); halves 1965-01 .. 1994-12 and 1995-01 .. 2025-09; the main effects b1
(F) and b2 (s); the null's width.

**Power, written before any number.** GSPC's monthly sd is about 4.2%; F's sd about 2.5%; if
s's sd is about 0.3, F s has sd near 0.0075, and with 729 months the standard error of b3 is
near 0.042 / (0.0075 x 27) = 0.21. t 2 needs b3 near 0.42: with s one sd high, a 5% fall would
add about 0.6% of further fall the next month. Plausible in size, but monthly returns show weak
continuation at best.

**My guess before any number.** b3 of either sign, |t| < 1.5, middle rank; placebo t sd
1.0-1.3. Chance of a pass: 2%.

## Both gates

**On a pass:** "not dead yet" only; no strategy card in this run. **On a fail:** dead, one
`screen` row each in `tries.md`, a line in `ideas.md`, a row in `gate-null.md`.

Counts (carried in from wide-20's "Family count": 95 mechanisms, 23 tested by a strategy, none
passed; 25 gates, all failed). After this run: 97 mechanisms, 27 gates. Project-wide bar
(`research/register/BAR.md`, rows through 2026-11-24 23:32): 3,982 tries, N 1,099; measured rho
0.54 gives N_eff 504: z >= 4.70, +0.31 / +0.56 Sharpe over `tsmom12`, Bonferroni p <= 9.9e-5.
