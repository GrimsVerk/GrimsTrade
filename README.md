# GrimsTrade

A trading robot that plays with **fake money on real prices**. No real money is ever involved.

Every evening after the US stock market closes, a robot on GitHub:

1. downloads the day's prices for Bitcoin, Ethereum and four big stock/bond/gold funds
   (SPY, QQQ, GLD, TLT),
2. asks each strategy what it wants to hold,
3. writes those choices into a logbook that can never be changed afterwards,
4. "buys and sells" at the **next** day's opening price, paying realistic fees,
5. updates the scoreboard.

Each strategy starts with a pretend 10,000 USD. The simple yardsticks (hold Bitcoin, hold SPY,
60% stocks / 40% bonds, equal parts of everything) run next to five classic strategies from
published research (trend following, momentum, volatility targeting, risk parity, and short-term
"buy the dip" in crypto). A strategy only counts as good if it beats the yardsticks over months,
after fees, and after allowing for how many ideas we tried (more tries means more luck to discount).

## Where to look

- **Start here:** `reports/weekly.md` on the [paper-trail branch](../../tree/paper-trail): one
  screen, plain language, rewritten every run.
- Scoreboard: `reports/scoreboard.md` on the
  [paper-trail branch](../../tree/paper-trail) (appears after the first daily run).
- What each strategy *would* have done in past years: `reports/backtest.md`. This is a
  backtest (hindsight, easy to flatter), so it is kept apart from the real forward record.
- The logbook of every decision: `ledger/decisions.jsonl` on the same branch.
- What's being worked on: `next-steps.md`.

Agents: start with `AGENTS.md`. License: MIT.
