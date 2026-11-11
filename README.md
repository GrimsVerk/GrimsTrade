# grimstrade

Paper-trading agent: real market data, fake money, honest forward-test ledger

Made from [grimsverk-template](https://github.com/GrimsVerk/grimsverk-template).
Agents: start with `AGENTS.md`.

## Develop

```sh
uv sync                     # install (creates .venv and uv.lock; commit uv.lock)
uv run pytest               # tests
uv run pre-commit install   # checks on every commit
```

## Set up GitHub (once)

After the first commit, the repo owner (admin) runs `scripts/setup-github.sh --public`: it creates the repo, pushes, and sets merge settings and `main` protection.

## Template updates

`scripts/update-from-template.sh` pulls in the latest template on a branch and opens a PR.
