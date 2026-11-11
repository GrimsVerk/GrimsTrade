# Next steps (repo agent, M0)

M0 checklist (see PLAN.md):
- [ ] Scaffold from grimsverk-template (in progress)
- [ ] data/: daily-bar ingest (BTC, ETH, SPY, QQQ, GLD, TLT), idempotent appends
- [ ] gym/: simulated broker (next-open fills, fees, spread, long-only, $10k)
- [ ] strategies/: benchmarks (BTC hold, SPY hold, 60/40, equal weight)
- [ ] ledger/: append-only JSONL + tries counter + integrity test
- [ ] runner + .github/workflows/daily.yml
- [ ] reports/: scoreboard
- [ ] README.md for the owner

Assumptions so far:
- No LICENSE until the owner picks one.
