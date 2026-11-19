# research/register: the project-wide register and the bar

| File | What | Written by |
|---|---|---|
| `tries.jsonl` | every distinct try on every pushed branch (only grows) | `uv run python -m grimstrade.register` |
| `BAR.md` | counts and the bar a new pick must clear | same |
| `moments.jsonl` | record length, skew, kurtosis per measured try | `research/register2.py estimate` |
| `trials.json` | correlation sample, effective number of trials | same |
| `returns/` | weekly returns of every measured series (store) | `research/register2.py export` |

Never edit them by hand. Cards: `research/register-1.md` to `research/register-4.md`.

## The returns store (`returns/`, register-4)

One gzip CSV per family (the register's `Idea`; the live strategies are `live`), one row per
series: `source,idea,variant,start,sharpe,first_friday,micro_returns`. Weekly simple returns
Friday to Friday, as integers in millionths. Strategy returns only: no prices or other market
data ever go here. Format details: the docstring of `src/grimstrade/returnstore.py`.

It holds every re-simulated baseline, every live strategy and every saved equity curve that
fits a register row, so `moments.jsonl` and `trials.json` regenerate on any checkout, with no
price caches and no other lane's files:

    uv run --with numpy python research/register2.py estimate
    uv run python -m grimstrade.register      # after `git fetch origin`; rewrites BAR.md too

Size budget: 5 MB for the whole directory (3.9 MB at 1,178 series, 2026-11-19). `export`
prints the size; over the budget it keeps baselines, live series and curves that fit a
selectable row, adds the others by SHA-256 of `idea/variant/start` while they fit, and says so.

## How a lane adds its returns

A lane whose tries are logged through the research harness has an equity curve per try in
its gitignored `research/data/runs/<idea>/<variant>.train.csv` (header, then `date,equity`
rows). To put their weekly returns in the store (needs this branch's `register2.py` and
`grimstrade.returnstore` on the lane's branch, or a checkout of the register branch):

1. `git fetch origin && uv run python -m grimstrade.register`, so the register holds the
   lane's pushed `research/tries.md` rows (a curve is stored only if it fits a register row:
   same idea and variant, train period, start within 10 days of From, Sharpe to 0.0051).
2. List the run directory in `research/register2.local.json` (copy the `.example`; paths
   relative to the repo, e.g. `"research/data/runs"` or `"../grimstrade-<lane>/research/data/runs"`).
3. `uv run --with numpy python research/register2.py curves`, then `... register2.py export`.
   Stored rows always stay; only the families with new series get a changed file.
4. Commit only `research/register/returns/` (check `git diff --stat`: your families' files),
   and push. Leave `tries.jsonl`, `BAR.md`, `moments.jsonl` and `trials.json` to whoever
   regenerates the register (`estimate`, then `grimstrade.register`), unless that is your task.

Tries logged by a script that does not save a curve: save one in the same place and format
(`date,equity`, one row per day with a bar) before step 3, or log the row's shape with
`grimstrade.tryshape.log` (shape only, not in the correlation sample).
`estimate` warns when local series that fit the register are missing from the store: the
numbers then differ from a clean checkout until they are exported and committed.
