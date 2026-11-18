# eu-4: whipsaw in the small coin-free EUR book, and reducers that keep the rule

Lane `eu-4` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-4` from `eu-3`. Code: `lib/eu4.py`. Fees are described as generic tiers: EUR 1, 2
or 3 per ETF order on a constant book (eu-2's three schedules, reused unchanged so the numbers
compare with eu-2 and eu-3).

## 1. Diagnosis: where `euw` spends its order budget (step 1, descriptive)

Table: `results/eu-4-diag.md` (`uv run --with numpy python research/lib/eu4.py diag`). This
replays eu-3's `tsmom12@euw/slip` (the house rule on SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY,
2012-2025, no fixed fee) and sorts its 417 ETF orders by cause. No rule was compared, so no
`tries.md` row.

- **Thirds.** 30.1 orders a year: 10.0 signal entries, 9.8 signal exits, 10.0 drift top-ups or
  trims (plus 4 start-up buys). At a EUR 10k book that is EUR 30 / 60 / 90 a year at the EUR
  1 / 2 / 3 tiers, a Sharpe drag of 0.05 / 0.10 / 0.15 on a 5.9%-vol book; each third costs a
  third of that.
- **Most flips are whipsaw.** Of the ~20 flip orders a year, 16.4 (83%) sit in spells that the
  next flip reverses within 4 weeks, 18.5 (94%) within 13 weeks. 88 of 267 closed spells last
  a single Friday; 150 last 4 weeks or less. Whipsaw within 4 weeks alone costs EUR 16 / 33 /
  49 a year at 10k (Sharpe 0.03 / 0.06 / 0.08), i.e. **about half of the whole fee drag**.
- **The whipsaws are shallow.** Inside a 1-week spell the 12-month return never got further
  from zero than a median 0.05 of the asset's own yearly vol (|z|); 94% stayed under 0.25.
  2-week spells: median 0.14, 83% under 0.25. Spells that last more than half a year reach a
  median |z| of 1.9. The weekly change of z has an sd of **0.21**, the same for every asset
  (0.20-0.22), as it should be for a one-year return in vol units: a week's noise is ~0.2.
- **Every asset whipsaws, the quiet trends most.** Flips a year: EXXY (commodities) 4.0, IBGL
  (long euro govts) 3.4, IQQE (EM) 3.2, EXSA (Europe) 3.1, 4GLD (gold) 2.7, SXR8 (S&P 500) 2.0,
  IBGS (short euro govts) 1.3. EXXY, IBGL, EXSA and IQQE carry 71% of the whipsaws of 13 weeks
  or less. It is not one bad asset: no slot can be dropped to fix this.
- **Whipsaws are not free in the market either** (in-spells lost ~1.1, out-spells missed ~1.4
  log points a year of book within 4 weeks), but those numbers are picked by hindsight (a spell
  is a whipsaw because the asset turned), so they are not a cost a rule could save.

What this says for step 2: the cheap orders to remove are the 1-2 week flips around zero, and
the noise that makes them is a known size (~0.2 in z units). A confirmation rule (a flip needs
the new sign two Fridays in a row) removes exactly the 1-Friday spells; a dead zone around zero
of about one week's noise removes most 1-2 week spells. Drift (a third of the orders) is not
touched by either; eu-3 found that checking drift weekly saves only 2 orders a year.
