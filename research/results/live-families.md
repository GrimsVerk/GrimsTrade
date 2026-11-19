# live-families: which strategy families paid live, net of fees

Card: `cards/live-families.md` (committed before any number). Descriptive, nothing selected, held-out year unread (no month after 2025-10). Monthly returns; Sharpe = monthly mean / sd x sqrt 12 of the return **above the 13-week T-bill**. Funds: net asset value with distributions (after fees and real costs). Matched holding: the plain index fund named per member (`bills` = cash). Composite: equal weight of the members alive each month, against the equal weight of their matched holdings.

## 1. Family composites over their live months

Gap = Sharpe minus the matched holding's Sharpe over the same months. Alpha, t, beta: OLS of the excess return on the matched holding's (for `bills`: the mean and its t). IR: alpha over residual sd. Mix: 80% VFINX + 20% the composite, monthly, minus VFINX alone (Sharpe; max drawdown in points, negative = shallower).

| Family | Live months | Span | Sharpe | Matched | Gap | Alpha/yr | t | Beta | IR | Corr VFINX | Max DD | Matched DD | Mix dSharpe | Mix dDD | Reading | Risk tool |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| value | 396 | 1992-11 .. 2025-10 | 0.53 | 0.55 | -0.02 | +0.1% | 0.1 | 1.00 | 0.02 | 0.90 | 59% | 52% | -0.01 | +1 | matched its holding (no edge) | - |
| momentum | 223 | 2007-04 .. 2025-10 | 0.58 | 0.64 | -0.06 | -0.2% | -0.1 | 1.01 | -0.03 | 0.92 | 56% | 51% | -0.01 | +1 | matched its holding (no edge) | - |
| quality | 184 | 2010-07 .. 2025-10 | 1.00 | 0.97 | +0.03 | +0.7% | 0.9 | 0.94 | 0.25 | 0.98 | 26% | 24% | +0.01 | +0 | matched its holding (no edge) | - |
| low-vol | 173 | 2011-06 .. 2025-10 | 0.70 | 0.69 | +0.01 | +1.0% | 0.7 | 0.65 | 0.20 | 0.86 | 18% | 25% | -0.01 | -1 | matched its holding (no edge) | - |
| multi-factor | 241 | 2005-10 .. 2025-10 | 0.59 | 0.65 | -0.05 | -0.8% | -1.6 | 1.04 | -0.37 | 0.99 | 53% | 51% | -0.01 | +0 | matched its holding (no edge) | - |
| dividend | 274 | 2003-01 .. 2025-10 | 0.67 | 0.71 | -0.04 | +0.2% | 0.2 | 0.85 | 0.03 | 0.93 | 47% | 51% | +0.00 | -1 | matched its holding (no edge) | - |
| style-premia (long-short) | 144 | 2013-11 .. 2025-10 | 0.50 | 0.00 | +0.50 | +5.4% | 1.7 | - | 0.50 | -0.01 | 35% | - | +0.08 | -7 | paid little | yes |
| fx-carry | 196 | 2009-07 .. 2025-10 | -0.03 | 0.00 | -0.03 | -0.2% | -0.1 | - | -0.03 | 0.59 | 26% | - | -0.08 | -3 | did not pay | - |
| merger-arb | 441 | 1989-02 .. 2025-10 | 0.40 | 0.55 | -0.15 | +2.1% | 2.2 | 0.06 | 0.37 | 0.39 | 11% | 18% | +0.01 | -8 | lagged its holding | - |
| option-writing | 454 | 1988-01 .. 2025-10 | 0.43 | 0.63 | -0.20 | -0.8% | -1.0 | 0.48 | -0.16 | 0.83 | 32% | 51% | -0.01 | -4 | lagged its holding | - |
| tail-hedge | 177 | 2011-02 .. 2025-10 | -0.54 | 0.44 | -0.98 | -13.5% | -1.6 | -4.60 | -0.43 | -0.66 | 97% | 5% | -0.13 | -5 | lagged its holding | - |
| gold-miners | 251 | 2004-12 .. 2025-10 | 0.32 | 0.59 | -0.27 | -5.5% | -1.2 | 1.71 | -0.27 | 0.32 | 78% | 43% | -0.01 | -3 | lagged its holding | - |
| defensive-sectors | 322 | 1999-01 .. 2025-10 | 0.57 | 0.48 | +0.08 | +2.1% | 1.5 | 0.60 | 0.30 | 0.80 | 34% | 51% | +0.03 | -3 | matched its holding (no edge) | - |
| trend (survey-5) | 224 | 2007-03 .. 2025-10 | 0.17 | 0.00 | +0.17 | +1.4% | 0.7 | - | 0.17 | -0.13 | 20% | - | +0.03 | -10 | paid little | yes |
| risk-parity (survey-5) | 196 | 2009-07 .. 2025-10 | 0.63 | 0.92 | -0.30 | -1.2% | -1.0 | 0.76 | -0.24 | 0.76 | 20% | 21% | -0.02 | -1 | lagged its holding | - |

Multiple testing: 15 family composites; Bonferroni one-sided 0.05/15 needs t >= 2.71. Families at or above it: none. (Descriptive; not picks. Project-wide bar for a new pick: see the card.)

## 2. Crash windows (total return; VFINX in brackets)

| Family | 2000-04..2002-09 | 2007-11..2009-02 | 2020-02..03 | 2022 |
|---|---:|---:|---:|---:|
| value | -12.8% (-43.8%) | -57.4% (-51.0%) | -29.1% (-19.6%) | -5.1% (-18.2%) |
| momentum | - (-43.8%) | -55.7% (-51.0%) | -18.0% (-19.6%) | -21.3% (-18.2%) |
| quality | - (-43.8%) | - (-51.0%) | -17.8% (-19.6%) | -18.1% (-18.2%) |
| low-vol | - (-43.8%) | - (-51.0%) | -18.3% (-19.6%) | -9.6% (-18.2%) |
| multi-factor | - (-43.8%) | -52.4% (-51.0%) | -22.1% (-19.6%) | -15.7% (-18.2%) |
| dividend | - (-43.8%) | -46.2% (-51.0%) | -21.3% (-19.6%) | -2.9% (-18.2%) |
| style-premia (long-short) | - (-43.8%) | - (-51.0%) | -7.1% (-19.6%) | +28.2% (-18.2%) |
| fx-carry | - (-43.8%) | - (-51.0%) | -9.3% (-19.6%) | -1.7% (-18.2%) |
| merger-arb | +14.3% (-43.8%) | -2.5% (-51.0%) | -5.2% (-19.6%) | -0.6% (-18.2%) |
| option-writing | -13.6% (-43.8%) | -31.0% (-51.0%) | -17.7% (-19.6%) | -13.7% (-18.2%) |
| tail-hedge | - (-43.8%) | - (-51.0%) | +46.0% (-19.6%) | -10.3% (-18.2%) |
| gold-miners | - (-43.8%) | -40.8% (-51.0%) | -23.7% (-19.6%) | -12.6% (-18.2%) |
| defensive-sectors | -13.5% (-43.8%) | -32.6% (-51.0%) | -15.5% (-19.6%) | -3.3% (-18.2%) |
| trend (survey-5) | - (-43.8%) | +12.6% (-51.0%) | +3.8% (-19.6%) | +20.0% (-18.2%) |
| risk-parity (survey-5) | - (-43.8%) | - (-51.0%) | -9.3% (-19.6%) | -16.2% (-18.2%) |

## 3. Members

| Family | Fund | Matched | Span | Months | Sharpe | Matched | Gap | Alpha/yr | t | Corr VFINX | Max DD |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| value | DFLVX | VFINX | 1993-03 .. 2025-10 | 392 | 0.50 | 0.60 | -0.10 | -0.6% | -0.5 | 0.90 | 61% |
| value | DFSVX | NAESX | 1993-03 .. 2025-10 | 392 | 0.50 | 0.47 | +0.04 | +1.2% | 1.1 | 0.80 | 61% |
| value | DFIVX | VGTSX | 1994-03 .. 2025-10 | 354 | 0.35 | 0.28 | +0.07 | +1.6% | 1.5 | 0.78 | 62% |
| value | VIVAX | VFINX | 1992-11 .. 2025-10 | 396 | 0.54 | 0.61 | -0.06 | -0.4% | -0.5 | 0.94 | 55% |
| value | IWD | IWB | 2000-06 .. 2025-10 | 305 | 0.44 | 0.49 | -0.05 | -0.3% | -0.3 | 0.94 | 55% |
| value | IWN | IWM | 2000-08 .. 2025-10 | 303 | 0.44 | 0.39 | +0.04 | +1.1% | 1.1 | 0.83 | 55% |
| value | VTV | VFINX | 2004-02 .. 2025-10 | 261 | 0.56 | 0.65 | -0.09 | -0.8% | -0.8 | 0.95 | 55% |
| value | RPV | VFINX | 2006-04 .. 2025-10 | 235 | 0.41 | 0.65 | -0.24 | -3.3% | -1.2 | 0.86 | 70% |
| momentum | PDP | VTSMX | 2007-04 .. 2025-10 | 223 | 0.51 | 0.62 | -0.11 | -1.2% | -0.7 | 0.91 | 56% |
| momentum | MTUM | VFINX | 2013-05 .. 2025-10 | 150 | 0.87 | 0.88 | -0.01 | +1.4% | 0.7 | 0.88 | 30% |
| quality | SPHQ | VFINX | 2010-07 .. 2025-10 | 184 | 1.02 | 0.97 | +0.06 | +1.2% | 1.3 | 0.97 | 24% |
| quality | QUAL | VFINX | 2013-08 .. 2025-10 | 147 | 0.82 | 0.86 | -0.05 | -0.5% | -0.6 | 0.98 | 28% |
| low-vol | SPLV | VFINX | 2011-06 .. 2025-10 | 173 | 0.74 | 0.88 | -0.14 | +0.7% | 0.3 | 0.78 | 21% |
| low-vol | USMV | VFINX | 2011-11 .. 2025-10 | 168 | 0.90 | 0.96 | -0.06 | +0.7% | 0.5 | 0.87 | 19% |
| low-vol | ACWV | ACWI | 2011-11 .. 2025-10 | 168 | 0.72 | 0.73 | -0.01 | +1.1% | 0.7 | 0.82 | 17% |
| low-vol | EEMV | EEM | 2011-11 .. 2025-10 | 168 | 0.26 | 0.25 | +0.01 | +0.3% | 0.3 | 0.67 | 23% |
| multi-factor | DFEOX | VTSMX | 2005-10 .. 2025-10 | 241 | 0.60 | 0.63 | -0.03 | -0.5% | -1.1 | 0.99 | 52% |
| multi-factor | DFQTX | VTSMX | 2005-10 .. 2025-10 | 241 | 0.56 | 0.63 | -0.07 | -1.1% | -1.6 | 0.98 | 54% |
| multi-factor | LRGF | VFINX | 2015-05 .. 2025-10 | 126 | 0.71 | 0.80 | -0.09 | -1.2% | -1.2 | 0.98 | 23% |
| multi-factor | GSLC | VFINX | 2015-10 .. 2025-10 | 121 | 0.84 | 0.88 | -0.04 | -0.5% | -1.1 | 1.00 | 25% |
| dividend | DVY | VFINX | 2003-12 .. 2025-10 | 263 | 0.51 | 0.67 | -0.16 | -0.6% | -0.3 | 0.83 | 57% |
| dividend | SDY | VFINX | 2005-12 .. 2025-10 | 239 | 0.52 | 0.66 | -0.14 | -0.7% | -0.4 | 0.86 | 49% |
| dividend | VIG | VFINX | 2006-06 .. 2025-10 | 233 | 0.67 | 0.66 | +0.01 | +0.5% | 0.6 | 0.96 | 41% |
| dividend | VYM | VFINX | 2006-12 .. 2025-10 | 227 | 0.55 | 0.64 | -0.09 | -0.7% | -0.5 | 0.93 | 52% |
| dividend | SCHD | VFINX | 2011-11 .. 2025-10 | 168 | 0.79 | 0.96 | -0.17 | -0.6% | -0.4 | 0.88 | 22% |
| dividend | VDIGX | VFINX | 2003-01 .. 2025-10 | 274 | 0.75 | 0.71 | +0.04 | +1.0% | 1.1 | 0.94 | 38% |
| style-premia (long-short) | QSPIX | bills | 2013-11 .. 2025-10 | 144 | 0.46 | 0.00 | +0.46 | +5.8% | 1.6 | -0.01 | 40% |
| style-premia (long-short) | QRPIX | bills | 2017-10 .. 2025-10 | 97 | 0.37 | 0.00 | +0.37 | +3.9% | 1.0 | -0.01 | 30% |
| fx-carry | CEW | bills | 2009-07 .. 2025-10 | 196 | -0.03 | 0.00 | -0.03 | -0.2% | -0.1 | 0.59 | 26% |
| merger-arb | MERFX | VBMFX | 1989-02 .. 2025-10 | 441 | 0.44 | 0.55 | -0.11 | +2.1% | 2.6 | 0.38 | 14% |
| merger-arb | ARBFX | VBMFX | 2000-10 .. 2025-10 | 301 | 0.25 | 0.47 | -0.22 | +1.7% | 1.1 | 0.32 | 19% |
| merger-arb | MNA | VBMFX | 2009-12 .. 2025-10 | 191 | 0.30 | 0.25 | +0.04 | +1.3% | 1.1 | 0.43 | 10% |
| option-writing | GATEX | VFINX | 1988-01 .. 2025-10 | 454 | 0.45 | 0.61 | -0.16 | -0.4% | -0.6 | 0.83 | 24% |
| option-writing | PBP | VFINX | 2008-01 .. 2025-10 | 214 | 0.35 | 0.66 | -0.31 | -2.6% | -1.9 | 0.88 | 40% |
| option-writing | XYLD | VFINX | 2013-07 .. 2025-10 | 148 | 0.57 | 0.89 | -0.32 | -2.6% | -1.7 | 0.90 | 23% |
| option-writing | QYLD | QQQ | 2014-01 .. 2025-10 | 142 | 0.56 | 0.98 | -0.42 | -3.1% | -1.8 | 0.85 | 23% |
| tail-hedge | TAIL | bills | 2017-05 .. 2025-10 | 102 | -0.77 | 0.00 | -0.77 | -8.8% | -2.2 | -0.69 | 49% |
| tail-hedge | VIXY | bills | 2011-02 .. 2025-10 | 177 | -0.74 | 0.00 | -0.74 | -47.4% | -2.8 | -0.77 | 100% |
| tail-hedge | BTAL | bills | 2011-10 .. 2025-10 | 169 | -0.24 | 0.00 | -0.24 | -3.5% | -0.9 | -0.62 | 37% |
| tail-hedge | SWAN | VBINX | 2018-12 .. 2025-10 | 83 | 0.40 | 0.65 | -0.25 | -2.0% | -0.9 | 0.81 | 30% |
| gold-miners | INIVX | GLD | 1980-02 .. 2025-10 | 251 | 0.37 | 0.59 | -0.22 | -4.1% | -0.9 | 0.24 | 75% |
| gold-miners | FSAGX | GLD | 1986-01 .. 2025-10 | 251 | 0.30 | 0.59 | -0.29 | -6.6% | -1.6 | 0.23 | 74% |
| gold-miners | VGPMX | GLD | 1984-06 .. 2018-08 | 165 | 0.14 | 0.40 | -0.26 | -3.5% | -0.5 | 0.33 | 76% |
| gold-miners | GDX | GLD | 2006-06 .. 2025-10 | 233 | 0.25 | 0.53 | -0.28 | -7.1% | -1.5 | 0.23 | 77% |
| gold-miners | GDXJ | GLD | 2009-12 .. 2025-10 | 191 | 0.19 | 0.46 | -0.26 | -7.1% | -1.1 | 0.28 | 87% |
| defensive-sectors | XLP | SPY | 1999-01 .. 2025-10 | 322 | 0.40 | 0.48 | -0.08 | +1.3% | 0.7 | 0.63 | 33% |
| defensive-sectors | XLU | SPY | 1999-01 .. 2025-10 | 322 | 0.44 | 0.48 | -0.04 | +3.2% | 1.2 | 0.47 | 44% |
| defensive-sectors | XLV | SPY | 1999-01 .. 2025-10 | 322 | 0.49 | 0.48 | +0.00 | +1.6% | 0.9 | 0.77 | 35% |
| defensive-sectors | SECT | SPY | 2017-10 .. 2025-10 | 97 | 0.69 | 0.79 | -0.09 | -1.1% | -0.8 | 0.97 | 21% |
| trend (survey-5) | RYMFX | bills | 2007-03 .. 2025-10 | 224 | -0.02 | 0.00 | -0.02 | -0.2% | -0.1 | -0.03 | 30% |
| trend (survey-5) | AQMIX | bills | 2010-02 .. 2025-10 | 189 | 0.29 | 0.00 | +0.29 | +2.9% | 1.1 | -0.20 | 24% |
| trend (survey-5) | ASFYX | bills | 2010-09 .. 2025-10 | 182 | 0.17 | 0.00 | +0.17 | +2.2% | 0.7 | -0.02 | 34% |
| trend (survey-5) | WTMF | bills | 2011-02 .. 2025-10 | 177 | -0.11 | 0.00 | -0.11 | -0.7% | -0.4 | 0.21 | 30% |
| trend (survey-5) | PQTIX | bills | 2014-02 .. 2025-10 | 141 | 0.25 | 0.00 | +0.25 | +2.5% | 0.9 | -0.26 | 24% |
| trend (survey-5) | ABYIX | bills | 2014-08 .. 2025-10 | 135 | 0.28 | 0.00 | +0.28 | +2.4% | 0.9 | -0.12 | 15% |
| trend (survey-5) | DBMF | bills | 2019-06 .. 2025-10 | 77 | 0.49 | 0.00 | +0.49 | +5.6% | 1.2 | -0.18 | 17% |
| trend (survey-5) | KMLM | bills | 2021-01 .. 2025-10 | 58 | 0.07 | 0.00 | +0.07 | +0.9% | 0.2 | -0.39 | 26% |
| trend (survey-5) | CTA | bills | 2022-04 .. 2025-10 | 43 | 0.40 | 0.00 | +0.40 | +6.3% | 0.8 | -0.37 | 17% |
| risk-parity (survey-5) | ABRZX | VBINX | 2009-07 .. 2025-10 | 196 | 0.57 | 0.92 | -0.35 | -1.4% | -1.2 | 0.75 | 18% |
| risk-parity (survey-5) | AQRIX | VBINX | 2010-10 .. 2025-10 | 181 | 0.63 | 0.87 | -0.24 | -0.5% | -0.3 | 0.74 | 15% |
| risk-parity (survey-5) | RPAR | VBINX | 2020-01 .. 2025-10 | 70 | 0.14 | 0.56 | -0.43 | -4.8% | -1.7 | 0.79 | 29% |

## 4. CBOE option-writing indexes (paper: no fees, no costs)

| Index | Window | Months | Sharpe | VFINX | Gap | Corr VFINX | Max DD | VFINX DD |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| BXM | own file (2002-04 .. 2025-10) | 283 | 0.43 | 0.59 | -0.17 | 0.88 | 36% | 51% |
| BXM | after 2007-06 (2007-07 .. 2025-10) | 220 | 0.41 | 0.64 | -0.23 | 0.88 | 36% | 51% |
| PUT | own file (2007-02 .. 2025-10) | 225 | 0.53 | 0.64 | -0.11 | 0.87 | 33% | 51% |
| PUT | after 2007-06 (2007-07 .. 2025-10) | 220 | 0.54 | 0.64 | -0.10 | 0.87 | 33% | 51% |

## 5. Published factors: paper sample against later years and the live funds

Long-short paper portfolios (no fees, no costs), Sharpe of the excess return. S = the paper's sample; O = after the sample to 2025-10; Pub = from the January after the journal year; F = the family composite's live months. Live = the family composite's IR against its holding (long-only funds: the comparable 'active Sharpe'). Kept = live / S; h = 1 - kept.

| Factor | S | Sharpe S | Sharpe O | Sharpe Pub | Sharpe F | Corr with family's active return (F) | Live (family IR) | Kept | h |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HML (Fama-French 1993) | 1963-07..1991-12 | 0.52 | 0.21 | 0.12 | 0.16 | 0.88 | 0.02 | 4% | 96% |
| UMD (Jegadeesh-Titman 1993) | 1965-01..1989-12 | 0.80 | 0.34 | 0.26 | 0.08 | 0.52 | -0.03 | -4% | 104% |
| RMW (Fama-French 2015) | 1963-07..2013-12 | 0.41 | 0.40 | 0.45 | 0.37 | 0.36 | 0.25 | 60% | 40% |
| QMJ US (Asness-Frazzini-Pedersen) | 1957-07..2012-12 | 0.56 | 0.30 | -0.03 | 0.30 | 0.44 | 0.25 | 44% | 56% |
| BAB US (Frazzini-Pedersen 2014) | 1926-01..2012-03 | 0.70 | 0.71 | 0.42 | 0.71 | 0.42 | 0.20 | 28% | 72% |
| CMA (Fama-French 2015) | 1963-07..2013-12 | 0.56 | -0.19 | -0.09 | - | - | - | - | - |
