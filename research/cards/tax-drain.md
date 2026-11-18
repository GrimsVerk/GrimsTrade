# tax-drain: step out of stocks and long bonds while tax receipts drain bank reserves

Field: hydraulics (a reservoir drained into another one on dates fixed by law). It is W2, a
mechanism added to wide-1's list by wide-3 (`wide-1.md`, last section), not one of the
original 46.
Written 2026-11-18, run wide-4, before any test or number of this card. Seen before: every
earlier result in `tries.md` (wide-3's `opex-pin`, a calendar overlay, failed: its expiry week
was an average week). No tax-date return, Treasury balance or reserve figure has been printed
by me or, as far as `tries.md` and `ideas.md` show, by any earlier run.

## The institutional fact, checked first (wide-3 wrote "2008" from memory)

Source read for this card: Paul J. Santoro, "The Evolution of Treasury Cash Management during
the Financial Crisis", Federal Reserve Bank of New York, *Current Issues in Economics and
Finance* 18(3), 2012 (newyorkfed.org/research/current_issues, ci18-3). What it says:

- **Before the crisis** the Treasury kept its account at the Fed (the TGA) "in a narrow band
  around $5 billion" (a target set in 1988, raised to $7 billion around tax dates) and put the
  rest of its cash in Treasury Tax and Loan (TT&L) accounts at private banks, by cash calls and
  direct investments each morning. A rising TGA drains bank reserves; keeping the TGA stable was
  the Treasury's way of not draining them. Occasionally tax inflows were so large that the
  banks' TT&L capacity ran out and the TGA rose "by more than several billion dollars" (April
  2000 is its example), and the Fed offset TGA swings with open-market operations to hold the
  funds rate at target. (1974-78 the TGA swung widely; fixed by the 1978 reorganisation.)
- **Fall 2008.** The TGA mostly sat near $5 billion until Lehman (2008-09-15). From October
  2008 the Fed paid interest on reserves; once the funds rate fell below 25 bps (target range
  0-0.25% from 2008-12-16) the TT&L rate went to zero and it paid the Treasury to keep its cash
  in the TGA. "Since the fall of 2008, TT&L balances have fluctuated in a narrow band around $2
  billion and the TGA has varied widely." TT&L kept $2 billion until 2011-12-29; by 2012 the
  investment program was shut.
- **But** after 2008 "expanding TGA balances did not reduce the quantity of reserves available
  to the banking system to a level at all close to what banks wanted or were required to hold
  and thus did not put upward pressure on the funds rate": reserves were abundant.

So wide-3's date is right (the switch is late 2008), and the source adds a condition wide-3 did
not have: a tax date drains reserves **only since the TGA switch**, and the drain can **only
bite when reserves are not abundant**. That splits the period into three regimes, fixed here:

| Regime | Dates | Prediction |
|---|---|---|
| A, TT&L era (placebo) | 1994-02-01 to 2008-09-14 | No effect: the TGA was held near $5 billion and the Fed offset what was left |
| B, TGA era, abundant reserves | 2008-12-16 to 2017-12-31 and 2020-01-01 to 2022-05-31 | Drain real, harmless: small or no effect |
| C, TGA era, reserves shrinking | 2018-01-01 to 2019-12-31 and 2022-06-01 to 2025-11-09 | The effect, if any: the Fed shrank its balance sheet (2017-10 to 2019-08; from 2022-06) and repo rates spiked on 2019-09-16/17, a corporate tax date |

2008-09-15 to 2008-12-15 belongs to no regime (transition).

## Claim

On federal tax dates the Treasury's account at the Fed jumps as tax payments arrive, which
drains bank reserves for some days; dealers' balance sheets tighten and financing costs rise,
and leveraged holders of stocks and long bonds sell. Stocks and long bonds earn less than
usual from the session before a tax date to three sessions after. A `tsmom12` book that leaves
SPY, QQQ and TLT for those five sessions does better than one that stays in.

## Why it might work

The dates are fixed by law and the flow is forced: taxes must be paid on the date, whatever the
price. The size is large (tens of billions of dollars in a day or two on the quarterly corporate
dates). The September 2019 repo spike happened on exactly this mechanism.

## Why it might not

- Since 2008 reserves were abundant almost all of the time (the source says so): the drain did
  not move the funds rate. Regime C has about 5.5 years, roughly 27 tax dates: low power.
- The Fed and the Treasury know the dates as well as anyone and smooth them (the standing repo
  facility since 2021, reverse-repo balances that absorb the drain first since 2021).
- Anyone can trade it with futures; any effect large enough to see may be gone.
- The rule only removes exposure. Three slots out for five sessions on five dates a year is
  25 sessions: if the effect is -30 bps a window on stocks, the book gains about +0.5% a year,
  roughly +0.03 Sharpe. **The bar of p < 0.0020 cannot be met by a gain that small**; the
  event study is where the mechanism can show.

## Data

- Prices: the six assets, the 8 other ETFs and the S&P 500 index, as every run (cache copied
  from wide-3's worktree).
- Treasury's account at the Fed, to check that the drain exists (the first stage): FRED
  `WDTGAL` (TGA, Wednesday level) or, if it does not exist or starts later than 2002,
  `WTREGEN` (week average); and `WRESBAL` (reserve balances, week average), both from FRED's
  keyless CSV download (`fred.stlouisfed.org/graph/fredgraph.csv?id=...`), saved to a new
  directory under `<cache_root>/fred/graph-2026-11-18/`, parsed with `python -I` by
  `lib/wide4_fred.py` into `<cache_root>/derived/wide-4/`. The download script prints only
  the number of rows and the first and last date of each series. Values after 2025-11-10 are
  dropped.

## Tax dates (fixed)

D = the first SPY session on or after the 15th of January, April, June, September and
December (individual estimated tax: Jan, Apr, Jun, Sep; corporate estimated tax: Apr, Jun, Sep,
Dec; individual returns: Apr). One exception, from Treasury and IRS notices: in 2020 the April
and June dates were moved to 15 July, so 2020 has Jan, Jul, Sep, Dec. April due dates moved
to the 17th or 18th by the District of Columbia's Emancipation Day holiday are not modelled:
the window runs to D+3 and covers them. The trading calendar (dates only) is taken as known in
advance, as in `month-end-liquidity` and `auction-concession`.

## Rule (fixed, no fitted parameter)

- Base: the `tsmom12` book on the six assets, decided weekly as always.
- Gate, decided daily (as `auction-concession`): the slots of **SPY, QQQ and TLT are empty** at
  a decision after the close of sessions D-2, D-1, D, D+1, D+2, so they are out from the open
  of D-1 to the open of D+4 (the returns of sessions D-1 .. D+3, at the gym's next-open
  fills). The freed weight is cash. GLD and the coins are not touched.
- **Active only in the TGA era, from 2008-12-16.** Before, the rule is its twin (regime A is
  the placebo, by the source above).

## Variants (all that will be run)

1. `drain` (only variant): as above.
2. Placebo, logged as `robustness`, never selectable: `drain-ttl`, the same gate active only
   before 2008-09-15 (regime A), the twin after.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, `drain-ttl`, and two descriptive tables (no
`tries.md` row):

1. **Event study.** For SPY, TLT, IEF and LQD: the close-to-close log return over sessions
   D-1 .. D+3 (close of D-2 to close of D+3), minus the average return of all 5-session
   windows of the same regime; mean in bps, t, number of dates; for regimes A, B, C and B+C,
   and for the four quarterly corporate dates (Apr, Jun, Sep, Dec) of C alone.
2. **First stage.** The change in the TGA (and in reserves) from the last Wednesday on or
   before D-2 to the first Wednesday on or after D+1, in billions of dollars, mean and t by
   regime, against the same change over all other Wednesday-to-Wednesday spans of equal length.

## Out-of-universe

- The 8 other ETFs as a `tsmom12` book with the gate on the US stock and bond ETFs (IWM, VNQ,
  IEF, LQD); EFA, EEM, DBC and SLV untouched.
- The S&P 500 index alone (`idx` set, the gate on GSPC only, active from 2008-12-16).
Coins: not applicable.

## Pass bar

The default in `protocol.md` for `drain` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 49 = 0.0020**: every pick out of the list of 46 plus wide-3's three
   new mechanisms counts.
2. Eras counted from 2000-09 (before 2008-12-16 the rule is its twin), ahead in at least 3 of 4.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive, and positive on both out-of-universe sets.
5. Beats equal weight on Sharpe.
6. (card) `drain`'s gain over the twin is larger than its placebo `drain-ttl`'s.

Reading of the event study, fixed now: **the mechanism is supported** only if (a) the first
stage shows the TGA rising over the tax window in B+C by more than in A, with t >= 2 for B+C;
(b) the SPY excess in B+C is negative with t <= -2, or the SPY excess in C alone is negative
with t <= -2; and (c) the SPY excess in A is not more negative than in B+C. Either way it is
evidence, not a pass.

Held-out year: once, `drain` only, only if all bars pass.

## My guess before any number

Chance it passes: 1-2%. Difference to the twin: -0.02 to +0.03 Sharpe. First stage: a clear
rise of the TGA on tax dates since 2008 (tens of billions of dollars), little before. Event
study on SPY in C: -50 to +20 bps; in A: about zero.

## Result

See `results/tax-drain.md` once tested.
