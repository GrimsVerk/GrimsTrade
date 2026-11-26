# wide-29 card: `ipo-heat`, does the US market earn less after a hot IPO market?

Lane wide-29, written 2026-11-26 (about 08:15 UTC), **before any return was read for this
rule** (card pushed first; the commit time is in git). Field: corporate finance (the market
for new issues: firms sell stock when it is dear). Candidate Q1 of `research/wide-29.md`.
Gate **W46** (W45 was wide-28), replication **R46** fixed below. No second gate.

## What was seen before this card (disclosed)

- Jay Ritter's `IPOALL.xlsx` (monthly US IPO counts and average first-day returns, 1960 on),
  downloaded 2026-11-26 08:15 UTC from site.warrington.ufl.edu (robots.txt read first: only
  /wp-admin/ and news paths disallowed, no AI-agent rule), 43,043 bytes, sha256
  6eadbb4371e1983cb4eb0405d43a30ccd7d5aa2409f7f3d25eca19cada97b57e, cached under
  `wide-29/ritter/2026-11-26/`. Seen: the sheet layout (811 rows; column A month, B year
  (two digits), C average first-day return, D net count, then gross count and the share
  priced above the midpoint; notes on the right), the twelve 1960 rows' first numbers, and
  the three footnote rows at the end. No sum, growth or dose was computed.
- Ken French monthly and daily factors (cached 2026-11-12): other lanes read the US market
  from them many times, never against IPO counts.

## Hypothesis

Firms go public when equity is overpriced (market timing: Ritter 1991, Loughran-Ritter 1995,
Baker-Wurgler 2000 "equity share", Lowry 2003 `[memory]`); the number of IPOs is one of the
six parts of the Baker-Wurgler sentiment index `[memory]`. A burst of new listings is a
costly act by insiders who know their firms. **When the IPO market is hot, the US market's
excess return over the next twelve months is lower: b < 0.** Published (post-sample 0); the
test asks whether it holds 1991-2025 with the series' placebo nulls.

Filters (wide-11): F1 passes as a premium (b), a state. F2 passes only with controls: IPOs
follow past returns (issuers wait for a rally), so the gate carries the market's past
12-month return, last month's return and its realised variance; placebo calendars use
earlier doses only.

## Data (keyless, cached)

- The Ritter file above: N(m) = **net count** (column D) for month m; blank or non-numeric
  cells make the month missing. IPOs are public on their day; **row m enters at the end of
  month m+1** (one month of slack, as wide-28). The file is a 2025-26 vintage compiled by
  hand; the counts of past months are not known to be revised in substance `[memory]`.
- Returns: French factors, monthly `Mkt-RF` and daily `Mkt-RF`, up to **2025-10**.

## Rule (frozen)

- **Dose.** N12(m) = N(m) + ... + N(m-11); H(m) = ln(1 + N12(m)) minus the mean of
  ln(1 + N12) over months m-60 .. m-1 (five-year detrended, past only). Defined where all
  72 months are present.
- **Outcome.** y(m) = Mkt-RF(m+2) + ... + Mkt-RF(m+13), % (twelve months after entry).
- **Controls**, as wide-28: c12(m) = sum of Mkt-RF over m-10 .. m+1; c1(m) = Mkt-RF(m+1);
  rv(m) = ln of the sum of squared daily Mkt-RF over m-1 .. m+1. Constant.
- **Rows.** m = **1991-01 .. 2024-09** with H, controls and y defined (405 months if all are).
- **Statistic.** OLS of y on H, c12, c1, rv, constant; t of b with Newey-West (Bartlett) 12
  lags (`gatepower.dk_fit`); b in % over twelve months per unit of H.
- **Predicted sign: b < 0.** Ranks are taken on -t (the most negative t ranks 1).

## Placebo nulls (as wide-28)

- **Shifted family**: H_k(m) = H(m - k), k = 25, 27, ..., 103 (40, odd); same rows and
  controls.
- **Surrogate family**: 40 surrogates of the full H series, `gatenull2.surrogate_doses`,
  seed 2746: phase, or IAAFT if the dry run shows |end - start| of H above one SD of H. The
  family gates if the dry run's lag-1 acf of H is 0.8 or more; otherwise shown only.

## Gate (pass only if all hold)

1. b < 0.
2. t <= -2.
3. -t ranks among the 2 highest of 41 in the shifted family **and** (when gating) among the
   2 highest of 41 in the surrogate family.

**Kill-only** (gate-null step 7): smallest p a rank shows is 1/41 = 0.024, above the family
bar (0.10 / 113 = 0.00088 with this card) and the register's 9.8e-5.

**Replication R46, fixed now, run only if the gate passes** (earlier, non-overlapping
years): the same rule on rows m = 1966-01 .. 1989-12 (outcomes end 1991-01, before the
gate's first outcome month 1991-03), against the same 40 surrogates. Pass: b < 0, t <= -2,
-t among the 2 highest of 41.

## Shown, not gating

- Horizons 3 months (NW 3) and 6 months (NW 6); no controls; without rv.
- Dose from the average first-day return (12-month mean of column C, same detrending).
- Halves: rows 1991-01 .. 2007-12 and 2008-01 .. 2024-09; without rows 1998-01 .. 2001-12
  (the dot-com boom and bust).
- The null's width in both families.

## Power and my guess (written before any number)

Twelve-month excess returns have an SD near 16%; 405 overlapping months of a dose with acf
near 0.98 are perhaps 10-20 independent stretches; the result will rest on 1999-2000 (the
IPO peak, then the bust) and 2020-21 (SPAC era; the net count excludes SPACs). **Guess: b
negative, t between -2.5 and -0.5, middle-to-high ranks (the shifted null of a cyclical
dose is wide, as W45 showed); pass 5%.**
