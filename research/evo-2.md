# Evo 2: a narrower evolved-rule search, gated on a calibrated plant

Research run evo-2, 2026-11-18. Branch `evo-2` (from `evo-1`). Research only: nothing here
touches the live runner, the gym's rules or the live strategies. Card:
`research/cards/evo-2.md` (committed before any evo-2 number). Tables: `results/evo-2.md`.

## Verdict (2026-11-18 ~19:50 UTC): the gate fails; no replay, no real search; close the evo line

**The redesigned search finds the calibrated 0.8 plant in only 1 of 3 fresh worlds (the card
needs 2).** Noise is found in 0 of 3 worlds (passes). By the card evo-2 stops here: no replay
world was run, no real price entered a fitness, the held-out year was not loaded. No evo
procedure (evo-1 or evo-2) has a real-data number, so the evo line used **no real-data look**.

- **0.8 plant:** world 36 found (`evo-top1` 0.69, `evo-ens10` 0.81, ceiling 0.80); world 34
  missed by 0.001 (`evo-val` 0.391, p 0.021, half the ceiling is 0.392); world 35 missed by
  0.03 (`evo-top1` 0.37, p 0.039, need 0.40). The near miss does not change the reading: the
  gate was written before the run and is applied as written.
- **0.5 plant (reported, not a gate):** found in 1 of 3 (world 34, `evo-top1` 0.32 of 0.49).
- **Better than evo-1, not good enough:** mean recovery at the 0.8 ceiling 0.45 (0.26 / 0.34 /
  0.76), against evo-1's 0.26 at a 0.72 ceiling; noise stays clean (procedures -0.37 to 0.11).
  The procedure that does best changes from world to world (`evo-val`, `evo-top1`,
  `evo-ens10`), so no one of them is reliably able to recover the plant.
- **Why it falls short (diagnostic):** once the window is long the search assembles `H`'s exact
  conditions (in world 34 the 2020 fit's `evo-top1` *is* `H`); the early fits, with 4-8 years
  of SPY alone or SPY and QQQ (the six-asset window before 2002), pick other rules, and the
  `full` switch often rescales `H`'s holding. Dropping the index warm-up (card change 2) cost
  the early fits most of their data; that is the likely main loss, not verified here.

**What it means for the real question:** on this data a rule search needs an edge of about
Sharpe 0.8 *over cash, inside its own 8-input grammar* to be found reliably, and even that only
in 1 of 3 worlds. Any real edge over `tsmom12` would be a fraction of that. A real-data fail
would read "too weak to tell", so spending the one real look is not worth it.

## Recommendation for the lead

**Close the evo line** (recommended, as the card says on a gate fail). Two redesigns in a row
could not pass a planted control that is far stronger than any plausible real edge over
`tsmom12`. Keep the tools: `evo_score.py` (a gym-exact weekly scorer, ~0.4 ms a rule),
`evo_world.py` (shuffle and block worlds, the plant) and `evo2.calibrate` (a plant at a fixed
ceiling) are reusable by any lane that needs a power check.

If the lead still wants a third try, it would be a new card (evo-3) and a new pick, and the
obvious changes are, in order: put the index warm-up back for per-asset inputs (it is 31 years
of data the early fits now lack), fix `slot` mode (drop the `full` switch), and gate on the
plant before anything else again. That would be tuning the design to the control worlds after
seeing them; the controls of evo-3 would need fresh seeds, and its gate should be harder (3 of
3), not easier.

## Multiple testing

evo-2 was registered as a new pick (card, "Multiple testing"). It produced no `variant`,
`search` or real-data row, so it adds **no real-data try** to the lab's count; its 39 rows are
`control` rows, which are not counted as strategy tries (protocol, "Planted-signal controls").
The evo line's real-data look is still unspent.

## Run log

- ~19:40 UTC: card committed and pushed (`research/cards/evo-2.md`) before any code or number.
- Implementation: `research/lib/evo2.py` (configure, calibration, controls, gate, replay and
  real commands with the gate as a precondition); `evo_gp.INPUT_SET` (a narrowed input set;
  evo-1's draws unchanged by default, tested); `evo_wf.IDEA` / `evo_wf.WARMUP`; `evo_real`
  takes the idea name and logs transfer rows as `name@set` (they had the bare procedure name).
  Tests in `tests/test_evo_wf.py`.
- Card note ~19:55 UTC, before any evo-2 number: `H`'s Sharpe is not monotone in `k` (the plant
  feeds `H`'s own trend; a large `k` sinks an asset `H` never re-enters), so `k` is scanned in
  steps of 0.005 and then bisected. Found by the unit test on the toy world.
- Ceilings (6 rows), then the controls (33 rows): gate FAIL. Stopped.
- Price cache: copied from the evo-1 worktree into this worktree's git-ignored `research/data/`
  (with `research/macro.local.json`); the held-out bars are in that cache but `load_history`
  cuts at the train end and no evo-2 command asks for `heldout`.
