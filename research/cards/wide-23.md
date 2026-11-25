# wide-23 card: `hack-drift`, does ETH keep falling in the week after a large crypto theft?

Lane wide-23, written 2026-11-25, **before any return was read for this rule** (card pushed
first; the commit time is in git). Field: criminology of cybercrime x crypto. Candidate C1 of
`research/wide-23.md`, step 2. Gate **W37** (provisional: W36 is taken by the open PR #202;
the merging lead may renumber), replication **R37** fixed below.

## What was seen before this card (disclosed)

- DefiLlama hack list (`https://api.llama.fi/hacks`), format and count probe: 1,377 rows,
  2011-06-19 .. 2026-11-24, one row's fields printed; counts of events of USD 10 m or more by
  year and target type (to 2025-10-31: 54 on centralised exchanges, 114 on all other targets).
  Dates are UTC days (every timestamp is midnight).
- First and last dates of the cached BTC and ETH bar files (BTC 2012-01-01, ETH 2016-05-18).
  No price, no return.
- The literature as remembered (below), and the survey's note on Liu and Tsyvinski.

## Hypothesis

Large thefts from DeFi protocols, bridges, tokens and wallets are unscheduled crimes. The
thief sells or launders the loot over days, users pull money from similar protocols, and the
market reprices the security of the platform its money sits on. Corbet, Cumming, Lucey, Peat
and Vigne (Economics Letters 2020) report negative returns and higher volatility after hacks
`[memory]`; Liu and Tsyvinski (RFS 2021) find that the "Bitcoin hack" search ratio predicts
-2.75% for BTC the following week (one sd; sample 2011-01 .. 2018-05). If the market
under-reacts, **ETH keeps falling in the week after the theft is public: b < 0.**

Filters (wide-11 F1/F2): F1 passes (a, b): thefts are not announced. F2 passes only with
controls: the loot in USD scales with token prices and value locked, and hacks cluster in bull
markets, so the gate carries price controls and the placebo calendars use **earlier doses
only** (gate-null step 1).

## Data (keyless)

- Hacks: DefiLlama `https://api.llama.fi/hacks`, fetched once into the shared cache
  `wide-23/defillama/2026-11-25/hacks.json` (write-once, manifest), read with `python -I` as
  untrusted data. Only statistics are committed. Fields used: `date` (UTC day), `amount`
  (USD as listed), `targetType`. Events with no amount or amount under USD 10 m are dropped;
  events dated after 2025-10-31 are never used. `returnedFunds` is ignored (known later).
  Caveats fixed now: the list is curated and back-filled, with no publication date per event
  and amounts as revised by the curators; a theft disclosed days after its listed date puts
  part of the news reaction inside the outcome window, which biases toward b < 0 (a false
  pass). A pass therefore needs the disclosure dates of the largest events checked before it
  is read as "not dead yet".
- Gate events **G**: `targetType` is not `CEX` (DeFi protocols, bridges, chains, tokens,
  wallets, ...). Replication events **X**: `targetType` is `CEX`. Disjoint sets.
- Prices: `harness.load_history("train", syms=["BTC", "ETH"])`, daily closes (the bar of day d
  closes at 00:00 UTC of d+1), no bar after **2025-10-31**.

## Rule (frozen)

- Weight of an event with amount A: w = log2(A / 5,000,000) (1 at USD 10 m, about 7 at
  USD 0.6 bn). Dose D(d) = sum of w over the gate events dated day d (0 on days without one).
- Outcome y(d) = ln C(d+8) - ln C(d+1), ETH, C = the close of the bar dated that day. The
  window starts at the end of day d+1 UTC, a full day after the theft's listed day.
- Controls: r7(d) = ln C(d+1) - ln C(d-6) and r30(d) = ln C(d+1) - ln C(d-29) (ETH), both
  known when the outcome starts (they include the day-0 and day-1 reaction).
- Rows: every day d with all of C(d-29), C(d+1), C(d+8) present, from ETH's first bar to
  d + 8 <= 2025-10-31.
- Statistic: OLS y = a + b D + c1 r7 + c2 r30; t of b with Newey-West standard errors, 7 lags
  (overlapping 7-day outcomes).
- Predicted sign: **b < 0**.

## Placebo null (the decider, `research/gate-null.md`)

Earlier doses only: D_k(d) = D(d - 23k), k = 1..40 (the dose 23 .. 920 days earlier; 23 is
not a multiple of a week). The hack calendar starts 2011-06-19; a placebo day before it has
dose 0. Same rows, same controls, same function (a `shift` argument). Placebos at small k pair
a theft with returns 3-5 weeks later; if an effect lasts a month they lean to the true sign,
which widens the null on the side a pass needs (harder, not easier).

## Gate (pass only if all hold)

1. b < 0.
2. t <= -2.
3. The true t ranks among the 2 lowest of 41 (empirical one-sided p = rank / 41 <= 0.049).

**Kill-only** (gate-null step 7): about 114 nearly independent events, but the smallest p a
rank shows is 1/41 = 0.024, above the family bar (0.10 / 104 = 0.00096 relative to `main`) and
the register's 9.9e-5. A fail kills the idea; a pass says only "not dead yet".

**Replication R37, fixed now, run only if the gate passes** (new, independent events): the
same construction with the **X** events (thefts from centralised exchanges) as the dose and
**BTC** as the asset (outcome and controls on BTC), rows from BTC's first bar to
d + 8 <= 2025-10-31, the same 40 earlier-dose placebos; pass b < 0, t <= -2, rank among the 2
lowest of 41. This is the setting of Liu and Tsyvinski's BTC result plus seven later years.

## Shown, not gating

- Reaction (the channel's first link): ln C(d+1) - ln C(d-1) on D(d), ETH, no controls, NW 2;
  predicted b < 0. If there is no reaction, a drift has nothing to continue.
- BTC with the gate design (BTC outcome and controls, G events).
- ETH minus BTC: y_ETH - y_BTC on D with ETH's controls.
- 30-day horizon: ln C(d+31) - ln C(d+1), NW 30.
- Binary dose (1 on a day with a G event), and events of USD 50 m or more only.
- After Liu and Tsyvinski's sample: rows d >= 2018-06-01.
- Surrogate families for the null (wide-21's note, wide-22's finding): 40 phase-randomised
  surrogates of D on the gate rows (same amplitude spectrum, random phases, seed 23; a poor
  model of a spike train, reported as asked), and 40 random-day surrogates (the same event
  weights put on days drawn uniformly from the gate rows, seed 23). Rank of the true t in each.
- The null's width: SD of placebo t, share with |t| >= 2, 5/50/95% quantiles, extremes.

## Power and my guess (written before any number)

ETH's 7-day log return has an sd of about 12%; the dose has about 114 non-zero days with a
mean weight near 2, so sum(w^2) is about 450 and SE(b) about 12 / sqrt(450) = 0.57% per unit.
At Liu and Tsyvinski's size (-2.75% for a one-sd attention spike, which a USD 100 m theft might
produce: about 4.3 units) b is about -0.6 and t about -1.1. A pass needs about -1.15% a week
per doubling. Guess: b < 0, t between -1.5 and +0.5, a middle rank, placebo SD 0.9-1.2
(independent events, normal-like null). Prior of a pass: 2%.

## On the outcome

Pass: check the disclosure dates of the ten largest G events (caveat above), run R37 at once
and report both. Fail: dead, one `screen` row in `research/tries.md` (descriptive, not
selectable); R37 is not run.
