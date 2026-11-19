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

## Literature check

Tags: `[pages read]` = the text itself was read; `[page read]` = a web page or blog post read in
full; `[abstract]` = abstract or index record only; `[search summary, unverified]` = a search
engine's summary, not opened.

- **Savor and Wilson (2013)**, "How Much Do Investors Care About Macroeconomic Risk? Evidence
  from Scheduled Economic Announcements", JFQA 48(2), pp. 343-375. `[pages read]` (pp. 1-4 of
  the 2011 accepted draft,
  <https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Draft20111128p_edited.pdf>;
  record <https://ideas.repec.org/a/cup/jfinqa/v48y2013i02p343-375_00.html>)
  - Announcement days = scheduled CPI, PPI, employment and FOMC releases. 1958-2009: excess
    market return 11.4 bps on announcement days against 1.1 bps on all other days; over 60% of
    the annual equity premium on 13% of days; Sharpe ratio ten times higher; realized volatility
    only 4% higher. Unscheduled FOMC days: -89.2 bps (15 days, 2001-2009). The risk-free rate
    is lower on announcement days.
  - The published numbers may differ slightly from the draft `[unverified]`.
- **Savor and Wilson (2014)**, "Asset pricing: A tale of two days", JFE 113(2), pp. 171-201,
  DOI 10.1016/j.jfineco.2014.04.005. `[abstract]`
  (<https://ideas.repec.org/a/eee/jfinec/v113y2014i2p171-201.html>)
  - Same announcement days: market beta is strongly and positively priced on them, unrelated to
    returns (implied premium typically negative) on other days. A cross-sectional claim; it does
    not add a timing rule beyond the 2013 paper. Wachter and Zhu reproduce it on later data
    `[search summary, unverified]`.
- **Lucca and Moench (2015)**, "The Pre-FOMC Announcement Drift", Journal of Finance 70(1),
  pp. 329-371, DOI 10.1111/jofi.12196 `[abstract]`
  (<https://econpapers.repec.org/RePEc:bla:jfinan:v:70:y:2015:i:1:p:329-371>); first as NY Fed
  Staff Report 512 (2011) `[abstract]`; the authors' Liberty Street post of July 2012 `[page
  read]` (<https://libertystreeteconomics.newyorkfed.org/2012/07/the-puzzling-pre-fomc-announcement-drift>).
  - S&P 500 rises about 49 bps in the 24 hours before scheduled FOMC statements (2 pm day -1 to
    2 pm day 0); close-to-close on FOMC days about 33 bps against about 1 bp on other days;
    "more than 80 percent of the equity premium" since 1994 earned in that window; nothing like
    it in 1970-1993; no effect in Treasuries or money-market futures; no pre-announcement return
    before other US macro releases (abstract).
  - Sample September 1994 to March 2011 (Kurov et al.'s abstract and the 2018 post; the 2012 post
    says "1994 to 2011").
- **Lucca and Moench (2018)**, "The Pre-FOMC Announcement Drift: More Recent Evidence", Liberty
  Street Economics, 2018-11-26 `[page read]`
  (<https://libertystreeteconomics.newyorkfed.org/2018/11/the-pre-fomc-announcement-drift-more-recent-evidence.html>).
  - April 2011 to June 2018: about 40 bps (open of day -1 to about lunchtime of day 0) before
    meetings with a Chair press conference; "no longer any evidence" before meetings without one.
    No test statistic or meeting count given. (Since 2019 every meeting has a press conference.)
- **Kurov, Wolfe and Gilbert (2021)**, "The disappearing pre-FOMC announcement drift", Finance
  Research Letters 40, 101781, DOI 10.1016/j.frl.2020.101781 `[abstract]`
  (<https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html>).
  - Extends Lucca and Moench's sample to December 2019: the drift "essentially disappeared after
    2015", at meetings with and without press conferences; reduced uncertainty as a possible
    cause. Their numbers were not read (the working-paper PDF link returned 404) `[unverified]`.
- **"Is There a Macro-Announcement Premium?"**, Management Science 2025, DOI
  10.1287/mnsc.2024.06960 `[abstract]` (authors not confirmed): volatility barely falls after
  announcements; the average announcement return is mostly monetary-policy surprises and
  small-sample luck; the premium is estimated to be small. (Survey-2 also lists Ai, Bansal and
  Guo, NBER w31923, 2023, for the opposite view.)

What the record says before our own numbers: the effect was large and significant in its
papers' years; the pre-announcement drift is an FOMC effect (Lucca and Moench find none before
other US releases); after the sample the record splits: the authors' 2018 update still saw it
at press-conference meetings to mid-2018, Kurov, Wolfe and Gilbert see it gone after 2015 at
both kinds. Not checked: any test after 2019 other than ours below.

## Event study (descriptive; full table `results/ann-1.md`)

Script `lib/ann1_event.py` (commit 9e4f93b, pushed before its first run; tests
`tests/test_ann1.py`), one logged run. Scheduled meetings from survey-2's calendar (256,
1994-2025); bars to 2025-11-09. Bps a day; "other" = all other trading days in the same years;
Welch t.

**SPY, FOMC days minus other days** (n = meetings):

| Years | n | Day 0 close-to-close (gate) | Day -1 close-to-close | 2 pm to 2 pm (minute bars) | Open day -1 to open day +1 (tradable) |
|---|---:|---:|---:|---:|---:|
| 1994-02..2011-03 (Lucca-Moench sample) | 138 | **+30.9 (t 3.06)** | +18.5 (1.44) | - | +51.1 (3.42) |
| 2011-04..2014-12 (post-sample, pre-journal) | 30 | +26.5 (1.06) | -19.7 (-0.72) | - | +6.6 (0.20) |
| 2015-01..2025-11 (after publication) | 87 | **-0.8 (t -0.06)** | +12.7 (1.18) | +8.9 (0.80; 79, from 2016) | -6.2 (-0.38) |
| of which 2015-2019 | 40 | -5.5 (-0.48) | +13.0 (1.29) | +4.1 (0.64; 32, from 2016) | -6.9 (-0.45) |
| of which 2020-2025/11 | 47 | +3.2 (0.14) | +12.4 (0.69) | +12.1 (0.66) | -5.6 (-0.20) |

- **The paper replicates in its own years.** SPY gained 33.9 bps on FOMC days against 2.9 on
  other days, 1994-2011 (Lucca and Moench: about 33 against 1); the S&P 500 index gives the same
  (+31.6, t 3.16). A buyer at day -1's open selling at day +1's open (what the gym could fill)
  earned +51 bps over two days against +6 (t 3.4).
- **After publication it is gone on day 0.** 2015-2025: 4.9 bps on FOMC days against 5.7 on
  other days. The exact 2 pm to 2 pm window, which the daily bar cannot isolate, is +8.9 bps
  over other days (t 0.8): a remnant at best, a fifth of the paper's 49 bps, and not tradable at
  next-open fills. The tradable two-day window is below an ordinary two days (-6.2 bps).
- The day before (day -1 close-to-close) is +12.7 bps (t 1.2) in both halves after 2015; it was
  not the gate, it is one of many cells shown, and the open-to-open window that would hold it
  loses it again on day 0.
- **Secondary series** (full table): ^GSPC tracks SPY. TLT is the one large cell: +26.5 bps on
  day 0 after 2015 (t 2.3), all from 2015-2019 (+37.4, t 3.1; 2020-2025 +17.2, t 0.9). That is
  `fomc-bond-drift` (survey-2 S3, Pan and Peng; Hillenbrand), whose paper sample covers these
  years, so this is an in-sample look, not an out-of-sample test; and it is one of about 70
  cells. BTC: +126 bps on day 0 in 2020-2025 (t 2.1), -93 in 2015-2019 (t -1.7): a sign flip,
  read as noise at this volatility. BTC rows before 2015 have 2-3 events and mean nothing.

## Decision: dead

The rule (top of this file, pushed in commit 969f20e before any number) needs SPY's FOMC-day
return minus other days to be positive with t >= 2 in 2015-01..2025-11. It is -0.8 bps,
t -0.06, over 87 meetings. **No card, no strategy, no `tries.md` row.** `announcement-premium` is
dead:

- The FOMC leg, which carried the published effect, replicates in the papers' years (+31 bps,
  t 3.1) and is zero in the ten years after publication. Same pattern as `fomc-cycle` (survey-2)
  and `xtsmom` (survey-3): a published calendar effect that held in its sample and not after.
- The CPI and payroll legs were never tested here and are dropped by literature, not by data:
  Lucca and Moench find no pre-announcement return before other US releases, the Management
  Science 2025 paper finds the premium mostly monetary-policy surprises, and an 8:30 release
  needs a fill a day early. Building 30 years of BLS dates for that is not worth it.
- Family count unchanged: 61 mechanisms, 14 tested by a strategy, none passed. This one is
  closed by an event study, not a strategy test, so it does not raise the count; the next test
  is still read at p < 0.10 / 61 = 0.00164.
- Forward note only: the TLT day-0 cell (+26.5 bps after 2015) is the `fomc-bond-drift` effect
  in its own sample years. It does not change survey-3's verdict (forward only); a forward
  descriptive check after the held-out year is all it can get.

### Disclosures

- One logged run of the script; no plumbing or dry run before it. Nothing was changed after it.
- SPY minute bars are raw prices (no dividend adjustment). Since 2016 day 0 is a Wednesday (77)
  or Thursday (3), so the 2 pm window runs Tuesday/Wednesday to Wednesday/Thursday and does not
  cross SPY's quarterly ex-dividend dates (usually a Friday or a Monday) `[not checked date by
  date]`. The 79 minute-bar meetings are the 87 daily ones minus 2015's 8 (the minute cache
  starts 2016-01).
- Yahoo's ^GSPC open is unreliable before about 2010 (protocol), so only close-to-close is shown
  for the index.
- The held-out year was not read: the loaders drop every bar after 2025-11-09.
