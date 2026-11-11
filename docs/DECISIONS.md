# Decisions: grimstrade

Settled decisions and why, newest first. Don't relitigate; update an entry if the owner changes it.

- 2026-11-11: Daily bot writes to the `paper-trail` branch, not `main`. Why: `main` requires PRs;
  a data-only branch keeps the record's history clean and CI quiet.
- 2026-11-11: Bars and ledger are CSV/JSONL, stdlib only. Why: diff-able in git (the tamper
  evidence), no dependencies to break the unattended runner.
- 2026-11-11: Prices are raw (not dividend-adjusted); dividends are not credited yet. Why: adjusted
  history changes retroactively, which breaks append-only data. Understates SPY/TLT a little.
- 2026-11-11: Sharpe uses 365 calendar days and a zero risk-free rate. Why: crypto trades every day;
  one convention for all strategies.
- 2026-11-11: No real-money broker, ever, without the owner's explicit decision. No keys in git.
- 2026-11-11: License is MIT. Why: owner's ruling.
