# grimstrade: rules for agents

Paper-trading agent: real market data, fake money, honest forward-test ledger

## This project

- Fake money only. Never connect a real-money broker or add code that could.
- The daily runner (`grimstrade.run_daily`, `.github/workflows/daily.yml`) is plain Python: never put an LLM (`claude -p`, Agent SDK) in it.
- Never rewrite lines in `ledger/` or rows in `data/bars/` on the `paper-trail` branch. Append only.
- No look-ahead: strategies get only bars closed before the decision; fills are at the next open (rules in `docs/DESIGN.md`).
- Every strategy you try gets a line in `ledger/tries.jsonl` (`grimstrade.ledger.register_try`), even if it dies.

## Every session

- Read `next-steps.md` first. Write your task there before you start; delete it when done. Nothing may live only in chat: the next session starts fresh with only these files.
- One feature per session.
- When unsure, pick a reasonable default, note the assumption (in `docs/DECISIONS.md` if it will matter later), and keep going.

## Files

- `docs/VISION.md`: what matters, the tiebreaker. `docs/DESIGN.md`: what we are building.
- `docs/DECISIONS.md`: settled decisions and why. Don't relitigate them.
- `docs/BACKLOG.md`: ideas not started. Forget by deleting; git history is the archive.

## Working

- Non-trivial work: plan it in plan mode first. `/adversarial-review` attacks a plan before you build it (optional).
- A feature too big for one context: `/orchestrate`.
- Work on a branch, never on `main`. Run the checks below locally, then open a PR and merge it (`gh pr merge --rebase --delete-branch`). CI runs only on `main`; a red `main` is the next task.
- Never force-push, rewrite pushed history, or skip hooks (`--no-verify`).
- Paths in repo files are relative, so any computer can resume the work. Machine-specific values go in one gitignored local file with a committed `.example`.

## Checks

```sh
uv sync && uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
```

## Tests

- Test behaviour, not implementation. Keep tests that protect what matters: core user flows, anything that can lose data, payments.
- Tests run offline and deterministically: no real network, clock or randomness.
- For logic with a clear interface, the `test-writer` subagent can write tests from the spec while you write the code.

## Processes and agents

- Never stop processes or agents by name pattern (`pkill -f`, `killall`): other agents run identical commands. Stop only what you started, by its own ID.
- Before a big fan-out of subagents, check remaining usage; hitting the limit mid-run kills them all.

## Licensing

Don't add a LICENSE or license field. The owner picks one per repo.
