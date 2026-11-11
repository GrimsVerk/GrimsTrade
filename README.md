# GrimsTrade

A trading robot that plays with **fake money on real prices**. No real money is ever involved.

Every evening after the US stock market closes, a robot on GitHub:

1. downloads the day's prices for Bitcoin, Ethereum and four big stock/bond/gold funds
   (SPY, QQQ, GLD, TLT),
2. asks each strategy what it wants to hold,
3. writes those choices into a logbook that can never be changed afterwards,
4. "buys and sells" at the **next** day's opening price, paying realistic fees,
5. updates the scoreboard.

Each strategy starts with a pretend 10,000 USD. Right now only the simple yardsticks run
(hold Bitcoin, hold SPY, 60% stocks / 40% bonds, equal parts of everything). Smarter strategies only
count as good if they beat these yardsticks over months.

## Where to look

- Scoreboard: `reports/scoreboard.md` on the
  [paper-trail branch](../../tree/paper-trail) (appears after the first daily run).
- The logbook of every decision: `ledger/decisions.jsonl` on the same branch.
- What's being worked on: `next-steps.md`.

Agents: start with `AGENTS.md`. License: MIT.
