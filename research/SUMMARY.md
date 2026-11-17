# Research summary for the owner (2026-11-17)

**Nothing we tested beats the simple 12-month trend rule** (`tsmom12`: hold an asset only while its
price is above where it was a year ago, otherwise cash). 14 research runs so far. **The one lead
from outside it is "funding carry" on crypto futures: real at low trading costs, gone at the costs
a normal account pays.** The trend rule itself is insurance, not skill (see "How sure we are").

| Run | Question | Answer |
|---|---|---|
| [1](README.md#research-run-1-finished) | Do 14 ideas from about 150 papers beat the trend rule? | No: each equals a simpler rule or loses to it |
| [2](README.md#research-run-2-finished) | Does machine learning (ML) on price data? | No: its forecasts are a coin toss |
| [3](risk-map.md) | How much risk, how much crypto? | Three presets, from 9% a year with a 12% worst drop to 25% with 47%; none is skill |
| [review-1](https://github.com/GrimsVerk/grimstrade/blob/review-1/research/reviews/review-1.md) | Can runs 1 and 2 be trusted? | The numbers yes, one headline no (see "How sure we are") |
| [macro-1](macro-1.md), [ideas-1](https://github.com/GrimsVerk/grimstrade/blob/ideas-1/research/ideas-1.md) | Do Fed, rates, credit, the Bitcoin halving, or eight YouTube rules help? | No: all six macro ideas and all eight rules fail |
| [rl-1](rl-1.md) | Can a free RL agent beat the trend rule? | No: Sharpe 0.57-0.71 against 0.99 (Sharpe = return per unit of risk; higher is better) |
| [rl-2](rl-2.md) | An RL agent that may only nudge the trend rule? | 0.96-0.98 against 0.99: it adds nothing |
| [rl-3](rl-3.md) | Is the problem the learner or its inputs? | Both, and the inputs come first |
| [info-1](info-1.md) | Do 23 new inputs (positioning, options, on-chain, sentiment) forecast? | None is useful |
| [breadth-1](breadth-1.md) | More markets, or hourly trading? | One pass, in a wide coin book; still below Bitcoin alone |
| [short-1](short-1.md) | Does betting on falling coins add anything? | No. Near miss: funding carry |
| [carry-2](carry-2.md) | Does that carry hold on exchanges it never saw? | Partly: yes at 0.1% cost a trade, no at 0.3% |
| [invest-1](https://github.com/GrimsVerk/grimstrade/blob/invest-1/research/invest-1.md) | Slow signals for long-term investing, 1927-2025? | None passed; the trend rule buys safety, not return |
| [fm-1](https://github.com/GrimsVerk/grimstrade/blob/fm-1/research/fm-1.md) | Pretrained forecasting models (Chronos)? | No: they had memorised old prices |

## Leads
- **Funding carry** (short-1, carry-2). Holders of crypto futures pay each other a fee ("funding").
  Hold the coins where it is lowest, bet against those where it is highest: Sharpe 0.69 on about 550
  coins it had never seen, at 0.1% cost a trade. At 0.3%: 0.09. Our broker has no futures yet.
- **Quiet coins** (breadth-1). Among the 100 largest coins, favouring those traded little for their
  size lifted the trend rule's Sharpe from 0.72 to 1.06, also in the held-out year (the last 12
  months, kept locked for one final check). But Bitcoin alone made about 1.16: no reason to add coins.
- **Parked:** a valuation tilt (invest-1) and Bitcoin cycle clocks (macro-1, ideas-1; only 3-4 cycles).

## Dead ends (and why)
- **Clever maths from papers:** each turned out to equal a simpler rule, or lost to it.
- **ML and RL on prices, macro and on-chain data:** these inputs barely forecast next week. Left
  free, RL bought coins and lost up to 87%. Tied to the trend rule, it copied it. A planted fake
  signal had to be four times stronger than our best real input before the agent found it.
- **Macro phases, YouTube rules:** the trend rule steps out once prices fall; leaving earlier cost more.
- **More markets, hourly trading, betting on falls:** 33 markets add nothing; hourly costs are ten
  times the edge; a trend rule that also bets on falls scored 0.73 against 1.03 without.
- **Pretrained models:** brilliant on the old prices they had memorised, zero on 2020-2025.

## Not tested yet
- Carry: what trades in small coins really cost, a slower version, and its held-out-year check
  (running now: carry-3).
- RL on a book of many coins, and a learner with only a few inputs. Both must first pass rl-3's
  test: find a planted signal (running now: rl-4).
- Forecasts one to three months ahead, inputs from minute prices, other pretrained models.
- An AI research desk whose dated predictions get scored: not started.
- Broker gaps: no futures, no betting on falls, no dividends, no interest on cash.

## How sure we are
- Pass marks were fixed before each test, and every try is logged (about 1,070 rows).
- **Two write-ups disagree.** Run 1: the trend rule beats holding everything (Sharpe 1.05 against
  0.88). The independent review, which reproduced the numbers: that lead is 2000-2002 alone. Since
  2003 they tie (1.20 against 1.19); the trend rule's worst loss is 37% against 47%, for slower growth.
- "Dead" is firm where the gap is large (RL, ML, hourly). For near misses it means "not proven".
- The held-out year is less clean than run 1 says: two quoted figures include it; breadth-1 used it.
- Futures (carry) results rest on 2-6 years of data. Backtests charged 0.3% a crypto trade; live
  charges 0.65%.
- Live: 7 strategies and 4 yardsticks trade fake money daily, all deciding and filling (health
  check 2026-11-17). The record is 7 days old: no verdict yet.
