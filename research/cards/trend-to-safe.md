# trend-to-safe: when a risk asset is out of trend, hold bonds or gold instead of cash

Field: trend following / regime allocation (Antonacci's dual momentum; Shu, Yu, Mulvey 2024;
survey part 1 idea 4 and part 4 idea 1).
Written 2026-11-12 02:05 UTC, run 3. Before any test of this rule. Seen before: `tsmom12` on all
universes, and that 2022 hurt stocks and bonds together.

## Claim

In the 12-month trend rule, a slot that is out of trend sits in cash at 0. Giving that slot to
the safe assets that are themselves in trend (TLT, GLD) beats leaving it in cash.

## Why it might work

When stocks fall, bonds or gold have often risen (2000-02, 2008, 2020). Cash earns nothing in the
gym. The safe asset must pass its own trend test, which should keep the rule out of bonds in 2022.

## Why it might not

It doubles up on bonds and gold exactly when everything else is out, so the book becomes one or
two positions. The stock-bond hedge is a 2000-2020 regime (survey part 2); before 2000 and in
2022 they fell together. Gold and bond trends reverse too.

## Rule (fixed)

- Each Friday. Every eligible asset with a positive 365-day return holds its equal slot.
- The slots of the assets that fail are split equally among the safe assets (TLT, GLD) that
  pass. If neither passes, those slots stay in cash.

## Variants (all that will be run)

1. `safe` (the only one).

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight.

## Out-of-universe

The 8 other ETFs, with IEF and LQD as the safe assets. The coin and index sets have no safe
asset, so the rule equals its twin there; only one set applies.

## Pass bar

The default in `protocol.md`, with bar 4 read on the one applicable set. Also required: not
behind the twin in 2022-25 (the era the hedge failed).

## Result

See `results/trend-to-safe.md` once tested.
