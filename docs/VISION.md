# Vision: grimstrade

What matters when two reasonable choices disagree. Not requirements (those are in `DESIGN.md`).

## What this is for

A trading agent that decides on **real, live market data** but trades **only fake money** in our own
simulated broker (the gym). Success = it makes money in that world, measured honestly against real
prices as they arrive, and beats simple benchmarks after costs. A research side reads the
literature and borrows ideas from other fields (maths first) to find better strategies.

## Priorities, in order

1. **Honesty of the record.** No look-ahead, no rewritten history, every try counted. A worse but
   honest result beats a better one we can't trust.
2. **No real money.** Agents never connect a real-money account. Moving to real money is the
   owner's call alone, and only after the graduation bar in `DESIGN.md`.
3. **Runs without anyone.** The daily runner is plain Python on GitHub Actions: no LLM, no desktop.
4. **Simple, rip-out-able parts.** Each module can be replaced without breaking the rest.
5. **Ambition on research** (owner's RTX 5080, 16 GB) once the plumbing is proven.

## Not doing

- Real-money brokers or keys to them.
- Intraday trading before daily works.
- `claude -p` / Agent SDK loops in the repo. Research runs are `claude --bg` sessions started by the
  Chief of Staff with weekly usage that would otherwise expire.
- Judging success by beating cash. The bar is the benchmarks, after costs.
