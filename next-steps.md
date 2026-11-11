# Next steps (repo agent, M0)

M0 checklist (see docs/DESIGN.md):
- [x] Scaffold from grimsverk-template (PLAN.md folded into docs/)
- [x] data.py + sources.py: daily-bar ingest (BTC, ETH, SPY, QQQ, GLD, TLT), append-only CSV
- [x] gym.py: simulated broker (next-open fills, fees, spread, long-only, $10k). Gymnasium wrapper deferred (BACKLOG)
- [x] strategies/: benchmarks (BTC hold, SPY hold, 60/40, equal weight)
- [x] ledger.py: append-only JSONL + tries counter + git-history integrity test
- [ ] run_daily.py + .github/workflows/daily.yml (writes to `paper-trail` branch) (in progress)
- [x] report.py: scoreboard (live ledger + optional --backtest)
- [ ] README.md for the owner

Assumptions so far:
- License: MIT (owner ruling via Chief of Staff).
- CSV instead of parquet; stdlib only (no pandas). Raw prices, no dividends yet.
- Daily bot commits to orphan branch `paper-trail` because `main` requires PRs.
- Live fetch (Kraken/Coinbase/Yahoo/Stooq) unverified: container can't reach them.
- Costs: crypto 25 bps fee + 5 bps slip; ETFs 0 fee + 2 bps slip; 1% rebalance band.
