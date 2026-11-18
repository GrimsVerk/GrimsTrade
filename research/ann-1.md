# Ann 1: the announcement premium, event study first (2026-11-18)

Lane `ann-1` of the night lead (research only, fake money). Survey-3 left `announcement-premium`
as the last live survey-2 candidate (prior 1%) and asked for an event study on FOMC days before
any card. This file: literature check, the decision rule (written and pushed before any event
study number was computed), then the event study and the verdict.

## Decision rule (fixed before any number)

Written and pushed before the event-study script was run. Nothing below may change it.

**Gate statistic.** SPY's dividend-adjusted close-to-close return on scheduled FOMC
announcement days (close of day -1 to close of day 0; day 0 = the statement day from
`<cache_root>/derived/survey-2/fomc.csv`), minus the mean return of all other trading days in the
same window. This is the daily-bar version of Lucca and Moench's 24-hour pre-FOMC window: their
window ends at 2 pm on day 0, the daily bar adds the 2 pm to 4 pm reaction, which averages near
zero in their paper. t = Welch two-sample t-statistic (FOMC days against other days).

**Gate window ("after publication").** 2015-01-01 to 2025-11-09 (the end of train). Lucca and
Moench was published in the Journal of Finance in February 2015 (vol. 70, issue 1); Savor and
Wilson's two papers in 2013 and 2014. About 87 meetings.

**Rule.** Only if the gate statistic is positive with t >= 2 does a card get written (idle cash
into SPY across the FOMC window, tested on train only, rows in `tries.md`, family count
updated). Otherwise the candidate is written down as dead, with the reason, and no strategy is
built or run.

**Shown, not gating.** The same statistic in the papers' years (1994-02 to 2011-03, Lucca and
Moench's sample; FOMC dates here start in 1994) and in 2011-04 to 2014-12 (after their sample,
before the journal); the day before (day -1 close-to-close); the open-to-open windows the gym
could trade (open of day -1 or day 0 to open of day +1); the exact 2 pm to 2 pm window from
cached SPY minute bars for 2016-2025 (Alpaca SIP, raw prices); the S&P 500 index (^GSPC), TLT
and BTC as secondary series. Scheduled meetings only. No bar after 2025-11-09 is read.
