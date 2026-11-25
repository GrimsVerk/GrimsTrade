# wide-26b card: W18 `elimination-mood`, a record-closing check (does a country's index fall on the session after its team is knocked out of a World Cup or Euro?)

Lane wide-26, written 2026-11-25 (UTC), **before the match file was fetched and before any
return was read for this rule** (card pushed first; the commit time is in git). **This is a
record-closing check, not a new idea**: W18 was listed by wide-8 (#88) and never gated for want
of a keyless match list; wide-24 (Q4) noted the list now exists and that W18's channel is the
mood shock W31 `air-disaster-mood` killed. Gate id **W18** (its own, from wide-8); replication
**R18**. W18 is already one of the counted mechanisms (wide-8 added it), so this adds a gate, not
a mechanism. Owner decision B5 (`owner-decisions.md`), recommended default option 1: the 2026
World Cup (held-out year) is not used.

## What was seen before this card (disclosed)

- The repository `martj42/international_results` on GitHub: licence (CC0-1.0), default branch
  and last push date, through the GitHub API. No file opened.
- `raw.githubusercontent.com/robots.txt`: 404 (no robots file), as wide-24 found.
- The 24 cached index files and ^GSPC: first/last dates, time zones (wide-24's disclosure;
  W40's results, which used the same closes, are published).
- The literature as remembered: Edmans, Garcia and Norli (Journal of Finance 2007 `[memory]`):
  after a World Cup elimination the losing country's index falls by about 0.4-0.5% the next
  trading day, a bit less after other tournaments, with no gain after wins; sample 1973-2004.

## Hypothesis (from wide-8)

A knockout loss lowers the national mood; investors in a sad mood sell; the losing country's
index falls on the next session against the world. **b < 0.**

## Data (keyless)

- **Matches**: `results.csv` and `shootouts.csv` of `martj42/international_results`, branch
  `master`, fetched once into the cache `wide-26/intl-results/<date>/` (CC0). Fields used: date
  (local date of the match), home_team, away_team, home_score, away_score, tournament; for
  shootouts: date, home_team, away_team, winner. Tournaments: exactly `FIFA World Cup` and
  `UEFA Euro` (finals, not qualifiers).
- **Markets**: wide-24's 25 index series and loader (`wide24.load_market`), nothing after
  2025-10-31. Team to market: Germany GDAXI, England FTSE, Japan N225, France FCHI, Italy
  FTSEMIB.MI, Spain IBEX, Netherlands AEX, Belgium BFX, Switzerland SSMI, Sweden OMX, Austria
  ATX, Brazil BVSP, Mexico MXX, South Korea KS11, Australia AORD, United States ^GSPC, Canada
  GSPTSE, New Zealand NZ50, Indonesia JKSE, Malaysia KLSE, India BSESN, Israel TA125.TA,
  Singapore STI, Taiwan TWII, Hong Kong HSI. Scotland, Wales and Northern Ireland are not
  mapped (the FTSE is England's market in this rule, as wide-8 wrote).

## Rule (frozen)

- **Knockout match**: a team's 4th or later match of one tournament edition (every World Cup
  since 1998 and every Euro since 1996 opens with three group matches per team). An edition is
  the set of a tournament's matches within one calendar year, except Euro 2020, played in 2021:
  editions are grouped by tournament and year of the match.
- **Elimination**: the team's first knockout match that it lost, in play or on penalties
  (`shootouts.csv` winner for a drawn knockout match). A semi-final loser's later third-place
  match is not a second event.
- **Event session**: s0 = the market's first session dated on or after the day after the match
  date (matches end in the evening or night in most markets; Edmans et al. use the next trading
  day). Dose D(i, s) = number of eliminations of i's team with s0 = s (0 or 1).
- **Outcome**: y(i, s) = [ln C_i(s) - ln C_i(s-1)] - W_i(s), W_i = mean over the other markets
  of the log change between their last closes on or before the dates of i's sessions s-1 and s
  (each within 7 calendar days of its date; wide-24's `world_change`).
- **Rows**: every session s >= 1 of every market dated **2006-01-01 .. 2025-10-31** (post-sample:
  Edmans et al. end in 2004), with a world change.
- **Statistic**: pooled OLS of y on market dummies and D; Driscoll-Kraay t of the D slope
  (`gatepower.dk_fit`, scores summed by calendar date of session s, 5 lags). No price controls
  (match outcomes do not follow index prices; F2 passes).
- Predicted sign: **b < 0**.

## Placebo null (the decider)

Shifted calendars, both ways (match results do not answer prices): every match date moved by
23k days, k = -20..-1, 1..20 (as W31 and W40), the whole 1974-2025 match list shifted, events
landing outside the rows dropping. 40 placebos, same rows, same function. The dose is a sparse
event series (expected lag-1 autocorrelation near 0, printed in the dry run); gate-null-2's
"both families" rule applies only at 0.8 or more.

## Gate (pass only if all hold)

1. b < 0. 2. t <= -2. 3. The true t ranks among the 2 lowest of 41.

**Kill-only**: perhaps 60-100 eliminations of mapped teams in ten tournaments 2006-2024, nearly
independent across countries but sharing tournament windows; smallest p 1/41 = 0.024, above
the family bar (0.10 / 109) and the register's 9.8e-5.

**Replication R18, fixed now, run only if W18 passes**: the same rule on rows 1974-01-01 ..
2004-12-31 (the markets cached then; mostly the published sample's years, so a check of the
data and code, not independent of the paper's evidence).

## Shown, not gating

- Round weight: D = match number minus 3 (1 = first knockout match, up to 4 = final).
- Group-stage exits: D = 1 on the session after the last group match of a team that played
  exactly three matches (predicted b < 0, smaller).
- Knockout wins as a placebo dose (each knockout match won; predicted 0).
- Own return, no world subtraction.
- World Cup only.
- Two-session window: ln C_i(s0+1) - ln C_i(s0-1) minus world (does a dip reverse?).
- The null's width: SD of placebo t, share with |t| >= 2, 5/50/95%, extremes.
- The eliminations by country (counts) and the five largest-|y| events.

## Power and my guess (written before any number)

A one-session excess index return has an SD of about 1%. With about 80 events and nearly
independent days, SE(b) is about 1 / sqrt(80) = 0.11%; a pass needs about -0.23%, half the
published effect. Guess: b between -0.15% and +0.1%, t between -1.5 and +1, a middle rank (the
mood class died post-sample in W31). Prior of a pass: 3%.

## On the outcome

Pass: run R18 and report both; even then it is kill-only and a one-session mood dip is not a
trade at the book's horizon (wide-24), so no strategy card follows. Fail: W18 is closed dead;
one `screen` row in `research/tries.md`, a `robustness` row for each shown cell.
