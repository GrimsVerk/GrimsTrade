# wide-20 card: `air-disaster-mood`, does a large airliner disaster depress US stocks for two sessions?

Lane wide-20, written 2026-11-24, **before any return was read for this rule** (card pushed
first; the commit time is in git). Field: psychology of mood and anxiety (affect, the
availability heuristic) applied to markets. Candidate P1 of `research/wide-20.md`, step 2.
Gate W29 in the wide-lane numbering (provisional: parallel lanes tonight may take the same
number; the lead renumbers).

## What was seen before this card (disclosed)

A format probe of the event source only (Wikidata query below, without the day-precision
filter, 2026-11-24): 519 result rows; items with at least 50 deaths by decade 1950s 35, 1960s
88, 1970s 115, 1980s 92, 1990s 78, 2000s 65, 2010s 25, 2020s 8; 42 rows dated 2008-2025. No
price, return or statistic was computed. The published paper was read only as a search
summary (below); its event criteria are not known to this card.

## Hypothesis

Kaplanski and Levy, "Sentiment and stock prices: The case of aviation disasters", Journal of
Financial Economics 95(2), 2010, pp. 174-201 (sample January 1950 .. December 2007, `[search
summary]`): after a large aviation disaster the US market falls, by about USD 60 bn per
disaster against an economic loss below USD 1 bn, and the fall reverses within two days. The
cause story is mood: a salient, frightening event raises anxiety and perceived risk among
investors, who sell or hold back buying for a day or two. A later study reports that the index
effect weakens a lot once a few extreme accidents (mostly terrorism, such as 9/11) are
controlled for `[search summary]`.

Filters (wide-11 F1/F2, #109): F1 passes (a): the accident is unscheduled and the mood selling
it triggers is never public before the window. F2 passes outright: aircraft do not crash
because stocks moved. The test is **post-sample**: 2008-01 .. 2025-10, 17.8 train years after
the paper's sample end.

## Data (keyless)

- Events: Wikidata Query Service (`query.wikidata.org/sparql`, keyless, data CC0), one query,
  fetched once into the shared cache `wide-20/wikidata/<date>/air.csv` (write-once, manifest),
  read as untrusted data with `python -I`:
  items that are an instance of aviation accident (Q744913) or of any subclass of it
  (`wdt:P31/wdt:P279*`), with number of deaths (P1120) and point in time (P585) at **day
  precision** (time precision 11). Per item: date E = its earliest day-precision P585, deaths =
  its largest P1120. Items with deaths >= 50 enter. Terrorism, shoot-downs and collisions are
  not removed: the mood story covers them (a shown cell drops the three largest).
  Caveats, fixed now: Wikidata is edited after the fact (the death toll is the final one, a
  small look-ahead in the dose's size, none in its timing); dates are UTC calendar days of the
  accident, so a late-evening accident in the Americas can carry the next day's date (day 0 or
  day 1 then still catches the first session after it).
- Prices: `harness.load_history("train")` (dividend-adjusted where the cache has it). No bar
  after **2025-10-31** is used (stricter than the harness's 2025-11-10 cut; the held-out year
  is never read).

## Rule (frozen)

- Daily log return r(t) = ln(C_t / C_{t-1}) on SPY bars dated 2008-01-02 .. 2025-10-31.
- Event days: day 0 of an event = the first SPY bar dated >= E; day 1 = the next bar. Events
  with E in 2008-01-01 .. 2025-10-29 count.
- Dose x(t) = sum, over the events whose day 0 or day 1 is bar t, of log2(deaths / 25) (50
  deaths -> 1, 100 -> 2, 200 -> 3, 400 -> 4); 0 on other bars.
- Statistic: OLS r(t) = a + b x(t) over all bars; t of b with HC1 standard errors (daily
  returns; the near-independent-days design of W20, whose placebo SD was 0.99).
- Predicted sign: **b < 0** (two sessions of mood selling).

## Placebo null (the decider, `research/gate-null.md`)

Aircraft accidents do not answer prices, so shifts both ways are allowed (step 1). Each event
date moves by 23k calendar days, wrapped inside the window: E_k = W0 + ((E - W0 + 23k) mod L),
W0 = 2008-01-01, L = days from W0 to 2025-10-30; k in +-{1, ..., 20}: **40 placebos** (23 days
is not a multiple of a week, so shifted events land on all weekdays). Same function, same code
path, a `shift` argument.

## Gate (pass only if all hold)

1. b < 0.
2. t <= -2.
3. The true t ranks among the 2 lowest of 41 (empirical one-sided p = rank / 41 <= 0.049).

**Kill-only** (gate-null step 7): about 40 independent events; the smallest p a rank can show is
1/41 = 0.024, above the family bar (p < 0.10 / 88 = 0.0011 if this gate is counted) and the
register's Bonferroni 1.0e-4. A fail kills the idea; a pass says only "not dead yet" and would
need a tradeable form (the reversal) and more events (other countries' markets) before a card
for a strategy.

## Shown, not gating

- The binary event indicator instead of the dose.
- Days 0-2 instead of 0-1.
- The reversal: dose on days 2-4 (prediction b > 0): the only form a long-only daily book could
  trade (buy after the fall).
- Events with at least 100 deaths only.
- The three events with the most deaths in the window removed.
- Other assets, same rule: QQQ, IWM (small firms: the paper reports larger effects there), GLD,
  TLT (flight to safety: b > 0 expected if anything), BTC, ETH (from their first cached day;
  their bars include weekends, so day 0 is the accident's own day).
- GSPC (S&P 500 price index) 1950-01-04 .. 2007-12-31: the paper's own sample with this event
  list (in-sample for the paper, so a look at whether this event list sees the published
  effect at all), with its own 40 placebos over that window.
- GSPC 1950-2025 (full span).
- The null's width: SD of placebo t, share with |t| >= 2, 5/50/95% quantiles, extremes.

## Power and my guess (written before any number)

SPY's daily sd 2008-2025 is about 1.25%. About 42 events give about 84 dosed days with x near 2
(x^2 about 4.5), so SE(b) is about 1.25% / sqrt(84 x 4.5), near 0.064% per unit. The published
size, about -0.4% over two days for a typical disaster `[memory]`, is about -0.1% per day per
unit: t near -1.6 if the effect survived at full size, near -0.8 at half size. Guess: b of either
sign, t between -1.5 and +1.0, a middle rank, placebo t SD 0.9-1.2. Prior of a pass: 2%.

## On the outcome

Pass: "not dead yet"; a later lane may test the reversal as a forward rule and other markets.
Fail: dead, one `screen` row in `research/tries.md` (descriptive, not selectable), and the
mood-shock class (P1, P4 of `wide-20.md`) loses its lead candidate.
