# Wide 20: twelve mechanisms from economic history, demography, psychology, sociology and linguistics, scored before any price, the top one gated

Research run wide-20, 2026-11-24/25 (night run, WIDER lane). Branch `wide-20` (from `main`
fac43c9), draft PR into `main`. Research only: fake money, keyless public data, no change to
the gym, the daily runner or the live strategies. Train only: no bar after 2025-10-31 is used.

Other lanes tonight take biology / ecology / epidemiology / climate (wide-17), physics / signal
processing / control / networks (wide-18), meteorology / actuarial science / operations research
(wide-19) and the 2024-2026 finance literature (survey-7); candidates in those fields are left
out here (sunshine and air-pollution mood, for example, are meteorology and environment).

**Count carried in.** wide-15 (`wide-15.md`, "Family count"): **87 mechanisms, 18 tested by a
strategy, none passed; 22 gates, all failed.** Parallel lanes may add gates tonight; the lead
reconciles the count. As in wide-12/13/15, only mechanisms that get a gate or a strategy test
enter the count.

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-24 20:01): **3,855 tries,
N 1,083; measured rho 0.54 gives N_eff 500: a new rule needs z >= 4.70 against `tsmom12`
(+0.31 close rule, +0.56 far rule), Bonferroni p <= 1.0e-4.** Family bar after this run's gate:
p < 0.10 / 88 = 0.0011.

Method as wide-15: wide-11's filters F1 (not announced: an unscheduled flow (a) or a premium
(b)) and F2 (not price-driven; passing only with controls costs 1 point), then wide-10's six
points (structural cause 1, dose 2, post-sample 1, power 1, unseen 1, not killed 1), plus
keyless long data. Gates follow `research/gate-null.md` (40 placebos, the rank decides, t >= 2
also required, rule pushed before any number, one dry run with counts only, then one real
run). `[memory]` marks a literature fact not checked tonight.

## Step 1. Fields already used, and what is new here

Fields used by earlier runs are listed in `wide-15.md` step 1. The nearest earlier uses of
tonight's five fields: demography (W12 `rmd-december`, cohort flows on a legal age line), sport
sociology (W18 `elimination-mood`, never gated: no keyless match list), anthropology of
calendars (W13), survey methodology (W24, forecaster dispersion), computational linguistics
(wide-15's X10 `news-text-vol`, filtered; data-wide-1's EPU inventory row, scored 3:
"heavily studied, fails unseen"; it is not listed again here), attention (wide-3,
`attention-peak`). Searched in `research/` on 2026-11-24 for: aviation, airline, plane crash,
lottery, jackpot, skyscraper, MY ratio, middle-aged, birth, fertil, daylight, Kamstra,
Michigan, consumer sentiment, Malmendier, Chronicling, narrative, doomsday, shooting,
Kaplanski. No hit, except `lottery` (an unrelated word in `rl-5.md`) and BLS work stoppages
(data-wide-1: the BLS server answers scripts with 403).

## Step 2. Twelve mechanisms, scored (2026-11-24, before any price was read)

**Disclosure.** Before this table two sources were probed for format only (no price, no
return, no statistic): the Wikidata aviation-accident query of P1 (counts by decade, in the
card) and three lottery result files for P2 (NY Open Data Powerball and Mega Millions, a state
lottery's Powerball CSV: draw dates, numbers and multipliers, **no jackpot column**).

### The mechanisms (cause story each)

- **P1 `air-disaster-mood`** (psychology of mood and anxiety). A large airliner disaster is a
  salient, frightening event; anxious investors sell or hold back for a day or two, and prices
  recover when the mood passes. Kaplanski and Levy (Journal of Financial Economics 2010,
  sample 1950-2007): about USD 60 bn of US market value lost per disaster, reversed within two
  days `[search summary]`. Dose: deaths (log scale).
- **P2 `jackpot-substitution`** (behavioural economics of gambling). Speculative trading is
  partly entertainment; when a lottery jackpot is huge, retail gamblers buy tickets instead of
  speculative assets (Gao and Lin, Review of Financial Studies 2015: Taiwan, big jackpots cut
  retail trading `[memory]`). Jackpots roll over after random draws, a clean natural
  experiment. Prediction: lower BTC, ETH, QQQ returns in weeks of very large US jackpots.
- **P3 `panic-words`** (historical linguistics x narrative economics, Shiller 2019 `[memory]`).
  Fear narratives spread like a contagion before they are acted on; the share of US newspaper
  pages using "panic" or "crash" (Library of Congress Chronicling America OCR, 1880-1963) should
  lead monthly US stock returns (Cowles / Shiller index) negatively.
- **P4 `mass-casualty-mood`** (sociology of collective trauma). Same mood channel as P1, other
  events: public mass shootings in the US (about 150 since 1982 in public lists `[memory]`).
- **P5 `my-ratio`** (demography). The ratio of middle-aged (40-49) to young (20-29) adults sets
  the demand for equities over decades (Geanakoplos, Magill and Quinzii 2004; Favero, Gozluklu
  and Tamoni, JFQA 2011 `[memory]`): a high ratio, high prices, low later returns.
- **P6 `conception-lead`** (demography of fertility). Conceptions fall several quarters before
  recessions (Buckles, Hungerman and Lugauer, Economic Journal 2021 `[memory]`); births nine
  months later reveal it, so falling births should lead weak stock returns.
- **P7 `dst-sleep`** (sleep psychology). The Monday after a daylight-saving change has lower
  returns from lost sleep (Kamstra, Kramer and Levi, AER 2000; disputed by Pinegar 2002
  `[memory]`).
- **P8 `sad-onset`** (clinical psychology). Seasonal affective disorder raises risk aversion
  as nights lengthen in autumn, lowering returns then and raising them in winter (Kamstra,
  Kramer and Levi, AER 2003 `[memory]`).
- **P9 `experience-weighted`** (psychology of personal experience). Investors' risk-taking
  follows the returns they lived through (Malmendier and Nagel, QJE 2011 `[memory]`); a
  population-weighted lifetime return (age pyramid x past returns) should predict demand.
- **P10 `consumer-sentiment`** (survey psychology). High consumer confidence marks optimism
  that later corrects (Lemmon and Portniaguina, RFS 2006, sample to 2002 `[memory]`):
  University of Michigan index, monthly from 1952, contrarian.
- **P11 `skyscraper-index`** (economic history of building booms). Record-tall buildings are
  completed at the top of credit booms (Lawrence 1999 `[memory]`); a new record height signals
  a coming crash.
- **P12 `strike-idleness`** (labour sociology). Waves of strikes signal a rise in labour's
  bargaining power, a risk to the profit share for which equity should pay a premium afterwards;
  BLS major work stoppages, monthly days idle from 1947.

### Score

| # | F1 not announced | F2 not price-driven | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| P1 `air-disaster-mood` | pass (a): accidents are unscheduled; the mood selling is never public before the window | pass: aircraft do not crash because stocks moved | 0 (mood) | 2 (deaths vary, the story scales with salience) | 1 (2008-01 .. 2025-10: 17.8 years after the 2007 sample end) | 0 (about 42 events, under 200) | 1 | 1 (no mood-shock gate has run: W18 was never gated) | 0 | **5** | 2% |
| P2 `jackpot-substitution` | pass (a): the jackpot is public, the substituted purchases are not (wide-15's X1 reading) | pass: rollovers follow random draws | 0 | 2 | 0 (US form formed tonight) | 1 (about 800 draw weeks 2010-2025) | 1 | 1 | 0 | **5** | 0.5% |
| P3 `panic-words` | pass (a): narrative-driven selling is not public | with controls: newspapers write "panic" after falls | 0 | 2 | 0 (Garcia, JF 2013, NYT columns 1905-2005 `[memory]`, covers the span) | 1 (about 1,000 months) | 1 | 1 | -1 | 4 | 0.5% |
| P4 `mass-casualty-mood` | pass (a) | pass | 0 | 2 | 0 (formed tonight) | 0 (about 150 events) | 1 | 1 | 0 | 4 | 0.5% |
| P5 `my-ratio` | **fail**: the age structure is known decades ahead; a slow demand shift the market can price, neither a surprise flow nor a premium | pass | - | - | - | - (one or two demographic waves) | - | - | - | - | filtered |
| P6 `conception-lead` | **fail**: births are public statistics read as news (wide-15's X4 class) | pass | - | - | - | - | - | - | - | - | filtered |
| P7 `dst-sleep` | **fail**: scheduled dates, no dose (a calendar mean) | pass | - | - | - | - | - | - | - | - | filtered |
| P8 `sad-onset` | **fail**: fixed calendar (hours of night are the calendar), no dose; seasonality died (#148) | pass | - | - | - | - | - | - | - | - | filtered |
| P9 `experience-weighted` | pass (b) | **fail**: a weighted average of past returns, a price transform (a trend signal with demographic weights) | - | - | - | - | - | - | - | - | filtered |
| P10 `consumer-sentiment` | **fail**: a published survey read as news; the contrarian story is a mispricing, not a premium | **fail** as a story: confidence follows stock prices (Otoo 1999 `[memory]`) | - | - | - | - | - | - | - | - | filtered |
| P11 `skyscraper-index` | pass (a) | with controls: records are financed in booms, i.e. after rises | 0 | 0 (a record or not; height adds nothing to the story) | 0 | 0 (about 15 record completions since 1900) | 1 | 0 (Barr, Mizrach and Mundra, 2015: heights follow GDP, no predictive power `[memory]`) | -1 | 0 | dead (literature) |
| P12 `strike-idleness` | pass (b): a labour-conflict premium | with controls: strikes rise in tight labour markets, i.e. in booms | 0 | 2 | 0 (no return literature known to me `[memory]`) | 1 (about 940 months) | 1 | 1 | -1 | 4 | 0.5% |

**Size check (wide-15 step 3 suggestion, shown, not part of the rule).** P2 is a flow story:
the largest jackpots raise ticket sales by about USD 1-2 bn in a draw cycle `[memory]`; if a
tenth of that came out of retail crypto and tech buying, USD 100-200 m against a USD 1-3 tn coin
market moves it about 0.01% at an inelastic-markets multiplier of 5, against a weekly sd near
10%: an expected t near 0. P1 and P4 are not flow stories (mood moves prices through
reservation values, not net buying), so the check does not apply; P1's published size is about
-0.4% over two days `[memory]`.

**Picked by the rule.** P1 and P2 score 5. Tie-break (wide-10): fewest data fetches, then the
higher prior. P1 needs one keyless Wikidata query; **P2 has no keyless jackpot history** (the
probed files have no jackpot; jackpots cannot be rebuilt without per-draw winner counts), so it
is parked for data. **Gated: P1 as W29 `air-disaster-mood`** (card: `cards/wide-20.md`, pushed
before any price was read). The task allowed one or two gates; the next candidates (P3, P4, P12
at 4) need, in turn, about 2,000 Chronicling America API calls (the service moved to loc.gov in
2025 `[memory]`), a dataset with unclear redistribution terms, and a BLS server that refuses
scripts (data-wide-1). None is gated; all are parked, not counted.

## Step 3. W29 `air-disaster-mood` gate

The rule, data, placebo family, gate, shown cells, power and guess are in
[`cards/wide-20.md`](cards/wide-20.md), pushed before any number. Code:
`research/lib/wide20_events.py` (pure functions, tested offline in `tests/test_wide20.py`) and
`research/lib/wide20.py` (fetch and run). Results: `research/results/air-disaster-mood.md`.
