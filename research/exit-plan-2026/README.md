# Exit plan 2026 (research, 2026-11-18)

Research help only: the investor places every order themselves; no accounts, no orders, no logins.

Question: a euro-based retail investor living in the Netherlands, with a small stock portfolio
(index funds and shares), wants to be fully out of stocks by a fixed date (the worked example uses
31 Dec 2026), avoid a bad sell date, park the cash safely in euros against a stock-market crash
(short run included), and buy back in later.

## Layout

- `report.md`: the merged report (playbook, parking, re-entry). The one file a reader needs.
- `review-log.md`: review rounds (fresh reviewer each round, max 5) and what changed.
- `lanes/<lane>.md`: lane notes with sources, merged into the report by the lead.
- `scripts/`: scripts behind every number (backtest lane); card in `research/cards/exit-rules.md`,
  every try in `research/tries.md`.

## Lanes (night lead, started 2026-11-18 ~18:55 UTC)

Priority order: literature first, then proven investors, then commonly heard ideas.

| Lane | Branch / worktree | Topic |
|---|---|---|
| lit | `research/exit-1-lit` / `grimstrade-exit-lit` | literature: late-stage bubble and top signals, exits |
| haven | `research/exit-1-haven` / `grimstrade-exit-haven` | crash behaviour of havens incl. the short run |
| bt | `research/exit-1-bt` / `grimstrade-exit-bt` | backtests of exit rules on past episodes + current readings |
| inv | `research/exit-1-inv` / `grimstrade-exit-inv` | investors with proven records: documented actions vs talk |
| reentry | `research/exit-1-reentry` / `grimstrade-exit-reentry` | re-entry after crashes; IPO waves and sentiment as top signals |
| park | `research/exit-1-park` / `grimstrade-exit-park` | practical parking for a euro investor in the Netherlands; selling costs and settlement |
