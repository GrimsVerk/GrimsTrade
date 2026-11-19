# vol-timing: is ls-trend-2's control just volatility timing of `tsmom12`?

Lane `vol-timing` of the night run, 2026-11-19. Branch `vol-timing` from `ls-trend-2` (draft PR
#98 into `ls-trend-2`). Descriptive only: no new pick, nothing proposed for the book. Research
harness only; fake money.

## Step 0: card (d1854ec, before any number)

[`cards/vol-timing.md`](cards/vol-timing.md). Five series on ls-trend-2's footing (daily
calendar excess over the 13-week bill, bill interest on idle cash, P = 2007-04..2025-10 main,
L = 2010-02..2025-10): `tsmom12`; b1 (ls-trend-2's control: `tsmom12` + bills, share set monthly
by equal risk against the wide long-short book); const (`tsmom12` at b1's mean share 0.26, rest
in bills: the same-size bill slot diversifier-1 asks for); vt-own (`tsmom12` at
min(1, k / own trailing 52-week vol), same mean share, rest in bills: plain volatility
targeting); `trend-vol` (tv40). The rule for step 2 was fixed in the card.

## Step 1: the numbers (script 3234309; run after two fixes, below)

Tables: [`results/vol-timing.md`](results/vol-timing.md). Disclosure: the first launch timed out
after 20 minutes with nothing printed or logged (the share bisection re-ran the whole series once
per day; fixed in e32468d), the second stopped at once on a harness kind check for the tv40
re-score (292057a). Neither printed a number. b1 reproduces ls-trend-2 exactly (1.26 / 5.6%).

| P = 2007-04..2025-10 | Mean share | Sharpe P | Sharpe L | Vol | Max DD (total) | 2008 | 2020-02..03 | 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 1.00 | 1.21 | 1.32 | 18.3% | 35.6% | -1.6% | -14.1% | -12.9% |
| b1 (ls-trend-2 control) | 0.26 | **1.26** | 1.46 | 3.6% | **5.6%** | +0.9% | -2.4% | -1.5% |
| const: 0.26 x `tsmom12` + bills | 0.26 | 1.21 | 1.32 | 4.8% | 8.0% | -0.3% | -3.4% | -3.4% |
| vt-own: own-vol target + bills | 0.26 | **1.34** | 1.51 | 3.9% | 6.3% | -0.4% | -2.7% | -1.4% |
| `trend-vol` tv40 | 0.72 (1994-2025) | 1.21 | 1.34 | 11.7% | 20.7% | -0.5% | -9.6% | -12.1% |

Sharpe gains over `tsmom12` in P, paired bootstrap (description, not a test): b1 +0.05
(p 0.36, 5%..95% -0.19..+0.28), vt-own +0.13 (p 0.17, -0.09..+0.36), tv40 +0.00 (p 0.49).

**Decomposition of b1's gain** (P / L): constant scaling +0.000 / +0.000 (Sharpe does not move
with a constant scale, as the card said in advance); time-varying +0.052 / +0.142, so **0%
constant, 100% time-varying**. Inside the time-varying part, `tsmom12`'s own volatility gives
+0.134 / +0.189 and the wide book's volatility in the split takes back -0.083 / -0.047.

**Weekly correlation** (P / L): b1 with `trend-vol` 0.88 / 0.88 raw; the overlays (weekly
residuals on `tsmom12`, what each adds beyond a constant scale) 0.54 / 0.49. b1's overlay with
vt-own's: 0.88 / 0.88; vt-own's with `trend-vol`'s: 0.40 / 0.34.

Plain reading:

1. **Yes, b1 is volatility timing of `tsmom12`.** Its whole Sharpe gain is time-varying; its
   overlay moves 0.88 with plain own-volatility targeting, and the wide book's volatility in the
   split only adds noise (it costs 0.05-0.08 of Sharpe against vt-own).
2. **Against the same-size bill slot it is a risk improvement, not a return edge at any bar.**
   At 26% in `tsmom12` the bill-slot twin already has max drawdown 8.0%; volatility timing cuts
   that to 5.6-6.3% and the 2022 loss from -3.4% to -1.5%. The Sharpe gain (+0.05 to +0.13 on
   train) is a fraction of the +0.30 the project bar asks of a close rule, with bootstrap p
   0.17-0.36.
3. **`trend-vol` is a different, weaker form of the same bet.** Its per-asset 40% cap binds
   mostly on crypto, gives no Sharpe gain here (+0.001) and keeps most of `tsmom12`'s 2022 loss
   (-12.1%). The overlays are correlated about one half.

## Step 2: card or not (rule fixed in the card)

- Material: S(b1) - S(const) >= +0.05 in both P and L: **yes** (+0.052, +0.142; P only just).
- Covered by `trend-vol`: overlay correlation >= 0.5 **or** the same Sharpe gain within 0.03:
  overlay 0.54 in P (0.49 in L), Sharpe gain not the same (+0.05 vs +0.00). The first test
  holds in the main window.

**Verdict by the card's rule: covered by trend-vol, no card.** Honest caveat: the rule hit on a
borderline value (0.54 in P, 0.49 in L), and `trend-vol` does not deliver b1's Sharpe gain, so
"covered" means "the same hold-less bet already counted", not "the same result". The cleaner form,
vt-own (own-volatility targeting of `tsmom12`, overlay with `trend-vol` 0.40), was in the card but
the card's decision is about b1. A card for vt-own would need z >= 4.65, an edge of +0.30 over
`tsmom12` (register-2 BAR.md at 2026-11-18 23:04: 3,023 tries, N 1,027, effective N 433,
Bonferroni p <= 1.2e-04); it showed +0.13 in-sample on the same data that suggested it, so a try
slot would be spent on a known shortfall. Not proposed.

## Count

3 `replication` rows in `tries.md` (`const-tsmom12@L07`, `vt-own-tsmom12@L07`, `tv40-ex@L07`),
not selectable. No `ledger/tries.jsonl` line (no strategy tried). Project-wide N unchanged by
this lane. Held-out year unspent.

## Next

1. If a drawdown cap is wanted at a small size, own-volatility targeting of `tsmom12` belongs on
   the risk map (ls-trend-2 next item 2) as a risk choice next to fixed splits, not as a pick.
2. Nothing further on volatility timing as an edge: three forms (per-asset cap, split against a
   second book, own-vol target) give +0.00 to +0.13, all far below the bar.
